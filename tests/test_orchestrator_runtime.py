from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from claude_agent_sdk import ResultMessage

from cli.agents import Agent
from cli.artifacts import ArtifactContract, validate_artifact
from cli.orchestrator import (
    EVIDENCE_LEDGER_CONTRACT,
    CostTally,
    RunBudgetExceeded,
    _required_outputs_match_manifest,
    _run_agent,
    run_quality_gate_with_remediation,
)
from cli.quality_gate import PublicationQualityError, QualityIssue
from cli.run_manifest import build_dependency_fingerprint, update_artifact


def _agent(root: Path) -> Agent:
    return Agent(
        name="test-agent",
        display_name="Test Agent",
        description="Runtime contract test",
        tools=(),
        order=1,
        system_prompt="Write the requested artifact.",
        path=root / "test-agent.md",
    )


def _result(
    *,
    is_error: bool = False,
    stop_reason: str | None = "end_turn",
    cost: float = 0.25,
) -> ResultMessage:
    return ResultMessage(
        subtype="success",
        duration_ms=1,
        duration_api_ms=1,
        is_error=is_error,
        num_turns=2,
        session_id="test-session",
        stop_reason=stop_reason,
        total_cost_usd=cost,
    )


class CostTallyTests(unittest.TestCase):
    def test_parallel_reservations_share_one_hard_ceiling(self) -> None:
        tally = CostTally(budget_usd=10)
        tally.plan_calls(4)
        self.assertEqual(tally.reserve("one"), 2.5)
        self.assertEqual(tally.reserve("two"), 2.5)
        self.assertEqual(tally.remaining, 5.0)
        tally.add("one", 1.0)
        tally.release("one")
        self.assertEqual(tally.remaining, 6.5)

    def test_zero_budget_refuses_first_call(self) -> None:
        tally = CostTally(budget_usd=0)
        tally.plan_calls(1)
        with self.assertRaises(RunBudgetExceeded):
            tally.reserve("first")


class AgentRuntimeTests(unittest.TestCase):
    def test_gate_remediation_binds_outputs_to_immutable_input_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            stage3 = outputs / "stage3"
            stage3.mkdir(parents=True)
            run_file = root / "prompts" / "runs" / "test.md"
            run_file.parent.mkdir(parents=True)
            run_file.write_text("# Run: Test", encoding="utf-8")
            manifest = outputs / "run-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": "2.0",
                        "run": {
                            "resume_identity_sha256": "a" * 64,
                        },
                        "artifacts": [],
                    }
                ),
                encoding="utf-8",
            )
            final_draft = stage3 / "final-draft.md"
            final_draft.write_text(
                " ".join(["original"] * 30), encoding="utf-8"
            )
            fact_report = stage3 / "fact-check-report.md"
            fact_report.write_text(
                " ".join(["verified"] * 30), encoding="utf-8"
            )
            lineage = outputs / "claim-lineage.jsonl"
            lineage_record = {
                "claim_id": "C1",
                "claim": "A verified airport claim.",
                "citation": "Primary source.",
                "footnote_id": "1",
                "evidence_ids": ["E1"],
                "verification_status": "verified",
                "primary_source_checked": True,
                "retained": True,
                "draft_sha256": "b" * 64,
            }
            lineage.write_text(
                json.dumps(lineage_record) + "\n", encoding="utf-8"
            )
            (outputs / "evidence-ledger.jsonl").write_text(
                json.dumps(
                    {
                        "evidence_id": "E1",
                        "agent_id": "researcher",
                        "claim": "A verified airport claim.",
                        "source_title": "Primary source",
                        "source_type": "primary",
                        "is_primary": True,
                        "confidence": "high",
                        "source_url": "https://example.com",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            verifier = Agent(
                name="fact-checker",
                display_name="Fact-checker",
                description="Test verifier",
                tools=(),
                order=1,
                system_prompt="Verify.",
                path=root / "fact-checker.md",
            )
            gate_calls = 0
            captured_dependencies: tuple[str, ...] = ()

            def fake_gate(**kwargs):
                nonlocal gate_calls
                gate_calls += 1
                report_path = kwargs["report_path"]
                payload = {
                    "schema_version": "1.0",
                    "passed": gate_calls == 2,
                    "error_count": 0 if gate_calls == 2 else 1,
                    "warning_count": 0,
                    "issues": (
                        []
                        if gate_calls == 2
                        else [
                            {
                                "severity": "error",
                                "code": "test",
                                "message": "Fix the claim.",
                            }
                        ]
                    ),
                }
                report_path.write_text(
                    json.dumps(payload), encoding="utf-8"
                )
                if gate_calls == 1:
                    raise PublicationQualityError(
                        report_path,
                        [QualityIssue("error", "test", "Fix the claim.")],
                    )
                return payload

            async def fake_run_agent(**kwargs):
                nonlocal captured_dependencies
                captured_dependencies = kwargs["dependency_inputs"]
                for dependency in captured_dependencies:
                    if dependency == "run-manifest.json":
                        continue
                    self.assertTrue((outputs / dependency).is_file())
                kwargs["output_path"].write_text(
                    " ".join(["remediated"] * 30), encoding="utf-8"
                )
                for path, _contract in kwargs["required_outputs"]:
                    if path.suffix == ".jsonl":
                        path.write_text(
                            json.dumps(lineage_record) + "\n",
                            encoding="utf-8",
                        )
                    else:
                        path.write_text(
                            " ".join(["remediated"] * 50),
                            encoding="utf-8",
                        )
                return {
                    "skipped": False,
                    "provider": "anthropic",
                    "cost": 0.0,
                    "turns": 1,
                }

            spec = type(
                "Spec",
                (),
                {"output_format": "report", "length": ""},
            )()
            with (
                patch(
                    "cli.orchestrator.run_publication_quality_gate",
                    fake_gate,
                ),
                patch("cli.orchestrator._run_agent", fake_run_agent),
                patch(
                    "cli.orchestrator.ensure_claim_lineage",
                    return_value=([lineage_record], False),
                ),
                patch(
                    "cli.orchestrator.bind_claim_lineage_to_draft",
                    return_value=[lineage_record],
                ),
            ):
                payload = asyncio.run(
                    run_quality_gate_with_remediation(
                        spec=spec,
                        run_file=run_file,
                        outputs_dir=outputs,
                        all_agents=[verifier],
                        tally=CostTally(),
                        manifest_path=manifest,
                        agent_names=["fact-checker"],
                    )
                )

            self.assertTrue(payload["passed"])
            self.assertEqual(gate_calls, 2)
            self.assertIn(
                "stage3/remediation-inputs/final-draft-before-gate.md",
                captured_dependencies,
            )
            self.assertIn(
                "stage3/remediation-inputs/quality-gate-before-remediation.json",
                captured_dependencies,
            )
            manifest_payload = json.loads(
                manifest.read_text(encoding="utf-8")
            )
            final_record = next(
                item
                for item in manifest_payload["artifacts"]
                if item["path"] == "stage3/final-draft.md"
            )
            self.assertTrue(final_record["dependencies"]["complete"])

    def test_changed_stage1_invalidates_curated_evidence_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            context = outputs / "context"
            stage1 = outputs / "stage1"
            context.mkdir(parents=True)
            stage1.mkdir(parents=True)
            manifest = outputs / "run-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": "2.0",
                        "run": {
                            "resume_identity_sha256": "a" * 64,
                        },
                        "artifacts": [],
                    }
                ),
                encoding="utf-8",
            )
            (context / "airport-context.md").write_text(
                " ".join(["context"] * 30), encoding="utf-8"
            )
            brief = stage1 / "researcher-brief.md"
            brief.write_text(
                " ".join(["research"] * 30), encoding="utf-8"
            )
            (stage1 / "researcher-evidence.jsonl").write_text(
                '{"claim":"claim","source_title":"source",'
                '"source_type":"primary","confidence":"high",'
                '"source_url":"https://example.com"}\n',
                encoding="utf-8",
            )
            ledger_record = (
                '{"evidence_id":"E1","agent_id":"researcher",'
                '"claim":"claim","source_title":"source",'
                '"source_type":"primary","is_primary":true,'
                '"confidence":"high","source_url":"https://example.com"}\n'
            )
            ledger = outputs / "evidence-ledger.jsonl"
            compatibility = stage1 / "evidence-ledger.jsonl"
            curation = stage1 / "evidence-map.md"
            ledger.write_text(ledger_record, encoding="utf-8")
            compatibility.write_text(ledger_record, encoding="utf-8")
            curation.write_text(
                " ".join(["curated"] * 30), encoding="utf-8"
            )
            dependency_inputs = (
                "run-manifest.json",
                "context/airport-context.md",
                "stage1/researcher-brief.md",
                "stage1/researcher-evidence.jsonl",
            )
            dependencies = build_dependency_fingerprint(
                manifest, dependency_inputs
            )
            outputs_to_check = (
                (ledger, EVIDENCE_LEDGER_CONTRACT),
                (compatibility, EVIDENCE_LEDGER_CONTRACT),
                (curation, ArtifactContract("markdown", min_words=20)),
            )
            for path, contract in outputs_to_check:
                update_artifact(
                    manifest,
                    path,
                    validate_artifact(path, contract),
                    dependencies=dependencies,
                )

            self.assertTrue(
                _required_outputs_match_manifest(
                    outputs_to_check,
                    manifest,
                    dependency_inputs,
                )
            )
            brief.write_text(
                " ".join(["regenerated"] * 30), encoding="utf-8"
            )
            self.assertFalse(
                _required_outputs_match_manifest(
                    outputs_to_check,
                    manifest,
                    dependency_inputs,
                )
            )
            brief.unlink()
            self.assertFalse(
                _required_outputs_match_manifest(
                    outputs_to_check,
                    manifest,
                    dependency_inputs,
                )
            )

    def test_legacy_manifest_without_dependency_receipt_cannot_skip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            stage1 = outputs / "stage1"
            stage2 = outputs / "stage2"
            stage1.mkdir(parents=True)
            stage2.mkdir(parents=True)
            manifest = outputs / "run-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": "2.0",
                        "run": {
                            "resume_identity_sha256": "a" * 64,
                        },
                        "artifacts": [],
                    }
                ),
                encoding="utf-8",
            )
            upstream = stage1 / "researcher-brief.md"
            output = stage2 / "strategist-draft-v1.md"
            upstream.write_text(" ".join(["source"] * 30), encoding="utf-8")
            output.write_text(" ".join(["legacy"] * 30), encoding="utf-8")
            contract = ArtifactContract("markdown", min_words=20)
            update_artifact(
                manifest,
                output,
                validate_artifact(output, contract),
            )
            invoked = False

            async def fake_query(*, prompt, options):
                nonlocal invoked
                del prompt, options
                invoked = True
                output.write_text(
                    " ".join(["rebound"] * 30), encoding="utf-8"
                )
                yield _result()

            with patch("claude_agent_sdk.query", fake_query):
                result = asyncio.run(
                    _run_agent(
                        agent=_agent(root),
                        user_prompt="Write it.",
                        model="test-model",
                        cwd=root,
                        step_label="stage2/strategist-v1",
                        tally=CostTally(),
                        output_path=output,
                        artifact_contract=contract,
                        manifest_path=manifest,
                        dependency_inputs=("stage1/researcher-brief.md",),
                    )
                )

            self.assertFalse(result["skipped"])
            self.assertTrue(invoked)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertTrue(payload["artifacts"][0]["dependencies"]["complete"])

    def test_changed_upstream_dependency_invalidates_downstream_skip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            stage1 = outputs / "stage1"
            stage2 = outputs / "stage2"
            stage1.mkdir(parents=True)
            stage2.mkdir(parents=True)
            manifest = outputs / "run-manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": "2.0",
                        "run": {
                            "resume_identity_sha256": "a" * 64,
                        },
                        "artifacts": [],
                    }
                ),
                encoding="utf-8",
            )
            upstream = stage1 / "researcher-brief.md"
            output = stage2 / "strategist-draft-v1.md"
            upstream.write_text(
                " ".join(["original"] * 30), encoding="utf-8"
            )
            output.write_text(
                " ".join(["stale"] * 30), encoding="utf-8"
            )
            contract = ArtifactContract("markdown", min_words=20)
            dependency_inputs = ("stage1/researcher-brief.md",)
            update_artifact(
                manifest,
                output,
                validate_artifact(output, contract),
                dependencies=build_dependency_fingerprint(
                    manifest, dependency_inputs
                ),
            )
            invocations = 0

            async def fake_query(*, prompt, options):
                nonlocal invocations
                del prompt, options
                invocations += 1
                output.write_text(
                    " ".join(["regenerated"] * 30), encoding="utf-8"
                )
                yield _result()

            with patch("claude_agent_sdk.query", fake_query):
                first = asyncio.run(
                    _run_agent(
                        agent=_agent(root),
                        user_prompt="Write it.",
                        model="test-model",
                        cwd=root,
                        step_label="stage2/strategist-v1",
                        tally=CostTally(),
                        output_path=output,
                        artifact_contract=contract,
                        manifest_path=manifest,
                        dependency_inputs=dependency_inputs,
                    )
                )
                self.assertTrue(first["skipped"])
                self.assertEqual(invocations, 0)

                upstream.write_text(
                    " ".join(["changed"] * 30), encoding="utf-8"
                )
                second = asyncio.run(
                    _run_agent(
                        agent=_agent(root),
                        user_prompt="Write it.",
                        model="test-model",
                        cwd=root,
                        step_label="stage2/strategist-v1",
                        tally=CostTally(),
                        output_path=output,
                        artifact_contract=contract,
                        manifest_path=manifest,
                        dependency_inputs=dependency_inputs,
                    )
                )

            self.assertFalse(second["skipped"])
            self.assertEqual(invocations, 1)
            self.assertEqual(len(list(stage2.glob("*.partial-*"))), 1)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            artifact = payload["artifacts"][0]
            current_dependencies = build_dependency_fingerprint(
                manifest, dependency_inputs
            )
            self.assertEqual(
                artifact["dependencies"]["sha256"],
                current_dependencies["sha256"],
            )

    def test_refusal_result_is_not_accepted_and_partial_is_quarantined(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "report.md"

            async def fake_query(*, prompt, options):
                del prompt, options
                output.write_text(" ".join(["partial"] * 30), encoding="utf-8")
                yield _result(stop_reason="refusal")

            tally = CostTally()
            journaled: list[float] = []
            with patch("claude_agent_sdk.query", fake_query):
                with self.assertRaisesRegex(
                    RuntimeError, "unsuccessful model result"
                ):
                    asyncio.run(
                        _run_agent(
                            agent=_agent(root),
                            user_prompt="Write it.",
                            model="test-model",
                            cwd=root,
                            step_label="test/refusal",
                            tally=tally,
                            output_path=output,
                            cost_journal=lambda current: journaled.append(
                                current.total
                            ),
                        )
                    )

            self.assertFalse(output.exists())
            self.assertEqual(len(list(root.glob("report.md.partial-*"))), 1)
            self.assertAlmostEqual(tally.total, 0.25)
            self.assertEqual(journaled, [0.25])

    def test_max_turn_result_and_cleanup_error_accept_complete_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "report.md"
            evidence = root / "evidence.jsonl"

            async def fake_query(*, prompt, options):
                del prompt, options
                output.write_text(
                    " ".join(["complete"] * 120), encoding="utf-8"
                )
                evidence.write_text(
                    json.dumps({"claim": "A supported claim."}) + "\n",
                    encoding="utf-8",
                )
                yield ResultMessage(
                    subtype="error_max_turns",
                    duration_ms=1,
                    duration_api_ms=1,
                    is_error=True,
                    num_turns=24,
                    session_id="test-session",
                    stop_reason="tool_use",
                    total_cost_usd=0.75,
                )
                raise Exception(
                    "Claude Code returned an error result: "
                    "Reached maximum number of turns (24)"
                )

            tally = CostTally()
            with patch("claude_agent_sdk.query", fake_query):
                result = asyncio.run(
                    _run_agent(
                        agent=_agent(root),
                        user_prompt="Research and write the required files.",
                        model="test-model",
                        cwd=root,
                        step_label="test/max-turn-recovery",
                        tally=tally,
                        output_path=output,
                        artifact_contract=ArtifactContract(
                            "markdown", min_words=100
                        ),
                        required_outputs=((
                            evidence,
                            ArtifactContract("jsonl", min_records=1),
                        ),),
                    )
                )

            self.assertFalse(result["skipped"])
            self.assertEqual(result["turns"], 24)
            self.assertEqual(result["cost"], 0.75)
            self.assertTrue(output.is_file())
            self.assertTrue(evidence.is_file())
            self.assertEqual(list(root.glob("*.partial-*")), [])
            self.assertAlmostEqual(tally.total, 0.75)

    def test_resume_requires_the_complete_atomic_artifact_set(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "report.md"
            companion = root / "evidence.json"
            output.write_text(" ".join(["complete"] * 30), encoding="utf-8")
            invoked = False

            async def fake_query(*, prompt, options):
                nonlocal invoked
                del prompt, options
                invoked = True
                companion.write_text('{"ok": true}\n', encoding="utf-8")
                yield _result()

            with patch("claude_agent_sdk.query", fake_query):
                asyncio.run(
                    _run_agent(
                        agent=_agent(root),
                        user_prompt="Complete the set.",
                        model="test-model",
                        cwd=root,
                        step_label="test/atomic",
                        tally=CostTally(),
                        output_path=output,
                        required_outputs=(
                            (companion, ArtifactContract("json")),
                        ),
                    )
                )

            self.assertTrue(invoked)
            self.assertTrue(companion.is_file())

    def test_per_call_sdk_budget_uses_planned_fair_share(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "report.md"
            seen_budget: list[float | None] = []

            async def fake_query(*, prompt, options):
                del prompt
                seen_budget.append(options.max_budget_usd)
                output.write_text(" ".join(["complete"] * 30), encoding="utf-8")
                yield _result(cost=1.0)

            tally = CostTally(budget_usd=10)
            tally.plan_calls(2)
            with patch("claude_agent_sdk.query", fake_query):
                asyncio.run(
                    _run_agent(
                        agent=_agent(root),
                        user_prompt="Write it.",
                        model="test-model",
                        cwd=root,
                        step_label="test/budget",
                        tally=tally,
                        output_path=output,
                    )
                )

            self.assertEqual(seen_budget, [5.0])
            self.assertAlmostEqual(tally.total, 1.0)


if __name__ == "__main__":
    unittest.main()
