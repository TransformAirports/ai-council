from __future__ import annotations

import asyncio
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cli.agents import Agent
from cli.artifacts import ArtifactContract
from cli.orchestrator import (
    CostTally,
    REVISION_SYSTEM_PROMPT_INPUTS,
    _publish_revision_release,
    _run_revision_agent,
    _snapshot_revision_remediation_inputs,
    _revision_system_dependencies,
    _revision_system_prompt_block,
)
from cli.publish import stage_release_artifacts
from cli.publishing_quality import QualityReport
from cli.revise import (
    RELEASE_CRITICAL_REVISION_STEPS,
    latest_draft_path,
    next_revision_version,
)
from cli.revision_state import (
    RevisionDependency,
    record_revision_step,
)


def _words(token: str, count: int = 80) -> str:
    return " ".join([token] * count)


class RevisionResumeTests(unittest.TestCase):
    @staticmethod
    def _digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _released_revision_fixture(
        self,
        root: Path,
    ) -> dict[str, Path]:
        slug = "terminal-chain"
        archive = root / "runs" / f"2026-07-23-{slug}"
        original = archive / "stage3" / "final-draft.md"
        original.parent.mkdir(parents=True)
        original.write_text(_words("original", 300), encoding="utf-8")

        revision = archive / "revisions" / "v1"
        stage4 = revision / "stage4"
        stage4.mkdir(parents=True)
        feedback = revision / "feedback.md"
        feedback.write_text("Make the decision sharper.", encoding="utf-8")
        final_draft = revision / "final-draft.md"
        final_draft.write_text(_words("released", 300), encoding="utf-8")
        lineage = revision / "claim-lineage.jsonl"
        lineage.write_text('{"claim":"released"}\n', encoding="utf-8")
        gate = revision / "quality-gate.json"
        gate.write_text(
            json.dumps({"passed": True}) + "\n",
            encoding="utf-8",
        )
        release_slug = f"{slug}-revised-v1"
        word_report = stage4 / f"{release_slug}.docx"
        word_report.write_bytes(b"synthetic exact Word package")

        dependency = archive / "receipt-input.md"
        dependency.write_text(_words("receipt-input"), encoding="utf-8")
        state = revision / "revision-execution.json"
        receipt_dir = revision / "receipt-outputs"
        receipt_dir.mkdir()
        for step_id in sorted(RELEASE_CRITICAL_REVISION_STEPS):
            if step_id == "fact-checker":
                output = final_draft
            elif step_id == "word-production":
                output = word_report
            else:
                output = receipt_dir / f"{step_id}.bin"
                output.write_bytes(f"complete:{step_id}".encode("utf-8"))
            record_revision_step(
                state_path=state,
                repo_root=root,
                step_id=step_id,
                dependencies=(
                    RevisionDependency(
                        dependency.relative_to(root).as_posix()
                    ),
                ),
                values={"step": step_id},
                outputs=((output, ArtifactContract("binary")),),
            )

        with (
            patch(
                "cli.publish.qa_docx",
                side_effect=lambda path: QualityReport(
                    artifact=str(path),
                    kind="docx",
                ),
            ),
            patch(
                "cli.publish.render_office_artifact",
                return_value=([], []),
            ),
        ):
            stage_release_artifacts(
                stage4_dir=stage4,
                slug=release_slug,
                release_dir=revision / "release",
            )
        release_manifest = revision / "release" / "release-manifest.json"
        terminal = {
            "schema_version": "1.0",
            "slug": slug,
            "revision": 1,
            "created_at": "2026-07-23T12:00:00-04:00",
            "source_archive": archive.name,
            "source_draft_sha256": self._digest(original),
            "feedback_sha256": self._digest(feedback),
            "final_draft_sha256": self._digest(final_draft),
            "claim_lineage_sha256": self._digest(lineage),
            "quality_gate_sha256": self._digest(gate),
            "visual_brief_sha256": None,
            "word_report_sha256": self._digest(word_report),
            "executive_summary_sha256": None,
            "release_manifest_sha256": self._digest(release_manifest),
            "revision_execution_sha256": self._digest(state),
            "required_steps": sorted(RELEASE_CRITICAL_REVISION_STEPS),
            "status": "released",
        }
        (revision / "revision-manifest.json").write_text(
            json.dumps(terminal, indent=2) + "\n",
            encoding="utf-8",
        )
        return {
            "archive": archive,
            "original": original,
            "revision": revision,
            "final": final_draft,
            "state": state,
            "released_word": revision / "release" / word_report.name,
        }

    def test_system_prompt_reads_have_exact_dependency_mappings(self) -> None:
        expected = {
            "strategist-a": {
                "run_prompt",
                "run_manifest",
                "evidence_map",
                "evidence_ledger",
                "narrative_options",
                "briefs",
            },
            "strategist-b": {
                "run_prompt",
                "run_manifest",
                "evidence_map",
                "evidence_ledger",
                "narrative_options",
                "briefs",
            },
            "red-team": {
                "run_manifest",
                "evidence_map",
                "evidence_ledger",
                "briefs",
            },
            "fact-checker": {
                "run_manifest",
                "evidence_map",
                "evidence_ledger",
                "airport_context",
                "context_sources",
                "briefs",
            },
            "fact-check-remediation": {
                "run_manifest",
                "evidence_ledger",
            },
            "art-direction": {
                "run_prompt",
                "run_manifest",
                "final_draft",
                "fact_check_report",
                "evidence_map",
                "evidence_ledger",
                "airport_context",
                "context_sources",
            },
        }
        self.assertEqual(
            {
                step: set(keys)
                for step, keys in REVISION_SYSTEM_PROMPT_INPUTS.items()
            },
            expected,
        )
        catalog = {
            key: RevisionDependency(f"archive/{key}")
            for key in set().union(*expected.values())
        }
        for step, keys in expected.items():
            dependencies = _revision_system_dependencies(step, catalog)
            self.assertEqual(
                {dependency.declaration for dependency in dependencies},
                {f"archive/{key}" for key in keys},
            )
            block = _revision_system_prompt_block(step, catalog)
            for key in keys:
                self.assertIn(
                    f"- {key}: `archive/{key}`",
                    block,
                )

    def _fixture(self, root: Path):
        (root / "AGENTS.md").write_text("revision contract", encoding="utf-8")
        charter = root / ".claude" / "agents" / "test-agent.md"
        charter.parent.mkdir(parents=True)
        charter.write_text("test charter", encoding="utf-8")
        agent = Agent(
            name="test-agent",
            display_name="Test Agent",
            description="Revision resume test",
            tools=(),
            order=1,
            system_prompt="test charter",
            path=charter,
        )
        base = root / "runs" / "archive" / "revisions" / "v1"
        base.mkdir(parents=True)
        dependency = root / "runs" / "archive" / "source.md"
        dependency.write_text(_words("source"), encoding="utf-8")
        return agent, base, dependency

    def test_exact_receipt_skips_but_changed_input_quarantines_and_reruns(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agent, base, dependency = self._fixture(root)
            state = base / "revision-execution.json"
            output = base / "draft.md"
            calls = 0

            async def fake_run_agent(**kwargs):
                nonlocal calls
                calls += 1
                kwargs["output_path"].write_text(
                    _words(f"attempt-{calls}"), encoding="utf-8"
                )
                return {
                    "skipped": False,
                    "provider": "anthropic",
                    "cost": 0.0,
                    "turns": 1,
                }

            kwargs = {
                "state_path": state,
                "repo_root": root,
                "step_id": "draft",
                "agent": agent,
                "user_prompt": "Revise the source.",
                "model": "model-a",
                "step_label": "revision-v1/draft",
                "tally": CostTally(),
                "output_path": output,
                "dependencies": (
                    RevisionDependency(
                        dependency.relative_to(root).as_posix()
                    ),
                ),
            }
            with (
                patch(
                    "cli.orchestrator.REVISION_EXECUTION_CONTRACTS",
                    ("AGENTS.md",),
                ),
                patch("cli.orchestrator._run_agent", fake_run_agent),
            ):
                asyncio.run(_run_revision_agent(**kwargs))
            self.assertEqual(calls, 1)

            # The real runtime exits through its file-valid skip before it
            # reaches the SDK, proving exact paid work is preserved.
            with patch(
                "cli.orchestrator.REVISION_EXECUTION_CONTRACTS",
                ("AGENTS.md",),
            ):
                result = asyncio.run(_run_revision_agent(**kwargs))
            self.assertTrue(result["skipped"])
            self.assertEqual(calls, 1)

            dependency.write_text(_words("changed"), encoding="utf-8")
            with (
                patch(
                    "cli.orchestrator.REVISION_EXECUTION_CONTRACTS",
                    ("AGENTS.md",),
                ),
                patch("cli.orchestrator._run_agent", fake_run_agent),
            ):
                asyncio.run(_run_revision_agent(**kwargs))
            self.assertEqual(calls, 2)
            self.assertTrue(
                any(base.glob("draft.md.partial-*")),
                "stale paid output should be quarantined",
            )

    def test_model_prompt_and_charter_are_part_of_the_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agent, base, dependency = self._fixture(root)
            state = base / "revision-execution.json"
            output = base / "draft.md"
            calls = 0

            async def fake_run_agent(**kwargs):
                nonlocal calls
                calls += 1
                kwargs["output_path"].write_text(
                    _words(f"call-{calls}"), encoding="utf-8"
                )
                return {
                    "skipped": False,
                    "provider": "anthropic",
                    "cost": 0.0,
                    "turns": 1,
                }

            def run(prompt: str, model: str) -> None:
                with (
                    patch(
                        "cli.orchestrator.REVISION_EXECUTION_CONTRACTS",
                        ("AGENTS.md",),
                    ),
                    patch("cli.orchestrator._run_agent", fake_run_agent),
                ):
                    asyncio.run(
                        _run_revision_agent(
                            state_path=state,
                            repo_root=root,
                            step_id="draft",
                            agent=agent,
                            user_prompt=prompt,
                            model=model,
                            step_label="revision-v1/draft",
                            tally=CostTally(),
                            output_path=output,
                            dependencies=(
                                RevisionDependency(
                                    dependency.relative_to(root).as_posix()
                                ),
                            ),
                        )
                    )

            run("Prompt one.", "model-a")
            run("Prompt two.", "model-a")
            run("Prompt two.", "model-b")
            agent.path.write_text("changed charter bytes", encoding="utf-8")
            run("Prompt two.", "model-b")
            self.assertEqual(calls, 4)
            self.assertEqual(len(list(base.glob("draft.md.partial-*"))), 3)

    def test_missing_dependency_fails_before_a_paid_call(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agent, base, dependency = self._fixture(root)
            output = base / "draft.md"
            output.write_text(_words("stale"), encoding="utf-8")
            dependency.unlink()

            async def should_not_run(**_kwargs):
                self.fail("paid agent should not run with a missing input")

            with (
                patch(
                    "cli.orchestrator.REVISION_EXECUTION_CONTRACTS",
                    ("AGENTS.md",),
                ),
                patch("cli.orchestrator._run_agent", should_not_run),
                self.assertRaisesRegex(RuntimeError, "missing or unsafe"),
            ):
                asyncio.run(
                    _run_revision_agent(
                        state_path=base / "revision-execution.json",
                        repo_root=root,
                        step_id="draft",
                        agent=agent,
                        user_prompt="Revise.",
                        model="model-a",
                        step_label="revision-v1/draft",
                        tally=CostTally(),
                        output_path=output,
                        dependencies=(
                            RevisionDependency(
                                dependency.relative_to(root).as_posix()
                            ),
                        ),
                    )
                )
            self.assertFalse(output.exists())
            self.assertTrue(any(base.glob("draft.md.partial-*")))

    def test_atomic_companions_are_quarantined_together(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agent, base, dependency = self._fixture(root)
            output = base / "final-draft.md"
            report = base / "fact-check-report.md"
            calls = 0

            async def fake_run_agent(**kwargs):
                nonlocal calls
                calls += 1
                self.assertFalse(kwargs["output_path"].exists())
                self.assertFalse(report.exists())
                kwargs["output_path"].write_text(
                    _words(f"draft-{calls}", 300), encoding="utf-8"
                )
                report.write_text(
                    _words(f"report-{calls}", 60), encoding="utf-8"
                )
                return {
                    "skipped": False,
                    "provider": "anthropic",
                    "cost": 0.0,
                    "turns": 1,
                }

            kwargs = {
                "state_path": base / "revision-execution.json",
                "repo_root": root,
                "step_id": "fact-checker",
                "agent": agent,
                "user_prompt": "Verify.",
                "model": "model-a",
                "step_label": "revision-v1/fact-checker",
                "tally": CostTally(),
                "output_path": output,
                "dependencies": (
                    RevisionDependency(
                        dependency.relative_to(root).as_posix()
                    ),
                ),
                "required_outputs": (
                    (
                        report,
                        ArtifactContract("markdown", min_words=40),
                    ),
                ),
            }
            with (
                patch(
                    "cli.orchestrator.REVISION_EXECUTION_CONTRACTS",
                    ("AGENTS.md",),
                ),
                patch("cli.orchestrator._run_agent", fake_run_agent),
            ):
                asyncio.run(_run_revision_agent(**kwargs))
                dependency.write_text(
                    _words("new-source"), encoding="utf-8"
                )
                asyncio.run(_run_revision_agent(**kwargs))
            self.assertEqual(calls, 2)
            self.assertTrue(any(base.glob("final-draft.md.partial-*")))
            self.assertTrue(any(base.glob("fact-check-report.md.partial-*")))

    def test_remediation_inputs_are_immutable_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "final-draft.md"
            source.write_text("before", encoding="utf-8")
            snapshots = _snapshot_revision_remediation_inputs(
                base=base,
                sources={"final-draft.md": source},
            )
            source.write_text("after", encoding="utf-8")
            self.assertEqual(
                snapshots["final-draft.md"].read_text(encoding="utf-8"),
                "before",
            )

    def test_interrupted_receipt_aware_revision_reuses_its_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "runs" / "interrupted"
            revision = archive / "revisions" / "v1"
            revision.mkdir(parents=True)
            (revision / "final-draft.md").write_text(
                _words("verified", 300), encoding="utf-8"
            )
            (revision / "revision-execution.json").write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "steps": {"fact-checker": {"status": "complete"}},
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(next_revision_version(archive), 1)
            (revision / "revision-manifest.json").write_text(
                json.dumps(
                    {
                        "status": "released",
                        "revision": 1,
                    }
                ),
                encoding="utf-8",
            )
            # A status marker alone is not a release commit. The same v1 is
            # retained until its complete terminal chain verifies.
            self.assertEqual(next_revision_version(archive), 1)

    def test_intact_receipt_aware_revision_advances_and_becomes_source(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = self._released_revision_fixture(Path(directory))
            self.assertEqual(next_revision_version(fixture["archive"]), 2)
            self.assertEqual(
                latest_draft_path(fixture["archive"]),
                fixture["final"],
            )

    def test_tampered_terminal_bytes_do_not_advance_or_become_source(
        self,
    ) -> None:
        for target in ("final", "state", "released_word"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                fixture = self._released_revision_fixture(Path(directory))
                fixture[target].write_bytes(
                    fixture[target].read_bytes() + b"\ntampered"
                )
                self.assertEqual(next_revision_version(fixture["archive"]), 1)
                self.assertEqual(
                    latest_draft_path(fixture["archive"]),
                    fixture["original"],
                )

    def test_non_file_execution_marker_is_not_treated_as_legacy(self) -> None:
        for marker_kind in ("directory", "dangling-symlink"):
            with self.subTest(marker_kind=marker_kind), tempfile.TemporaryDirectory() as directory:
                archive = Path(directory) / "runs" / "marker-test"
                original = archive / "stage3" / "final-draft.md"
                original.parent.mkdir(parents=True)
                original.write_text(_words("original", 300), encoding="utf-8")
                revision = archive / "revisions" / "v1"
                revision.mkdir(parents=True)
                (revision / "final-draft.md").write_text(
                    _words("untrusted", 300),
                    encoding="utf-8",
                )
                execution = revision / "revision-execution.json"
                if marker_kind == "directory":
                    execution.mkdir()
                else:
                    execution.symlink_to(revision / "missing-state.json")

                self.assertEqual(next_revision_version(archive), 1)
                self.assertEqual(latest_draft_path(archive), original)

    def test_stale_optional_remediation_receipt_does_not_block_release(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dependency = root / "source.md"
            dependency.write_text(_words("source"), encoding="utf-8")
            report = root / "report.md"
            report.write_text(_words("report"), encoding="utf-8")
            stale_dependency = root / "remediation-source.md"
            stale_dependency.write_text(_words("before"), encoding="utf-8")
            stale_output = root / "remediated.md"
            stale_output.write_text(_words("remediated"), encoding="utf-8")
            state = root / "revision-execution.json"
            record_revision_step(
                state_path=state,
                repo_root=root,
                step_id="word-production",
                dependencies=(RevisionDependency("source.md"),),
                values={},
                outputs=((report, ArtifactContract("markdown", min_words=20)),),
            )
            record_revision_step(
                state_path=state,
                repo_root=root,
                step_id="fact-check-remediation",
                dependencies=(RevisionDependency("remediation-source.md"),),
                values={},
                outputs=(
                    (
                        stale_output,
                        ArtifactContract("markdown", min_words=20),
                    ),
                ),
            )
            stale_dependency.write_text(
                _words("changed-after-remediation"),
                encoding="utf-8",
            )
            with (
                patch("cli.publish.stage_release_artifacts") as stage,
                patch(
                    "cli.publish.promote_release",
                    return_value={"word_report": report},
                ) as promote,
            ):
                published = _publish_revision_release(
                    state_path=state,
                    repo_root=root,
                    required_steps={"word-production"},
                    stage4_dir=root / "stage4",
                    slug="sample",
                    release_dir=root / "release",
                    require_executive_summary=False,
                    out_dir=root / "reports",
                )
            self.assertEqual(published["word_report"], report)
            stage.assert_called_once()
            promote.assert_called_once()

    def test_required_remediation_receipt_still_blocks_when_stale(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dependency = root / "source.md"
            dependency.write_text(_words("source"), encoding="utf-8")
            output = root / "remediated.md"
            output.write_text(_words("remediated"), encoding="utf-8")
            state = root / "revision-execution.json"
            record_revision_step(
                state_path=state,
                repo_root=root,
                step_id="fact-check-remediation",
                dependencies=(RevisionDependency("source.md"),),
                values={},
                outputs=(
                    (
                        output,
                        ArtifactContract("markdown", min_words=20),
                    ),
                ),
            )
            dependency.write_text(_words("changed"), encoding="utf-8")
            with (
                patch("cli.publish.stage_release_artifacts") as stage,
                patch("cli.publish.promote_release") as promote,
                self.assertRaisesRegex(
                    RuntimeError,
                    "pre-commit validation failed",
                ),
            ):
                _publish_revision_release(
                    state_path=state,
                    repo_root=root,
                    required_steps={"fact-check-remediation"},
                    stage4_dir=root / "stage4",
                    slug="sample",
                    release_dir=root / "release",
                    require_executive_summary=False,
                    out_dir=root / "reports",
                )
            stage.assert_not_called()
            promote.assert_not_called()

    def test_duplicate_required_step_records_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root / "revision-execution.json"
            state.write_text(
                (
                    '{"schema_version":"1.0","steps":{'
                    '"word-production":{"status":"complete"},'
                    '"word-production":{"status":"complete"}}}'
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "missing required"):
                _publish_revision_release(
                    state_path=state,
                    repo_root=root,
                    required_steps={"word-production"},
                    stage4_dir=root / "stage4",
                    slug="sample",
                    release_dir=root / "release",
                    require_executive_summary=False,
                    out_dir=root / "reports",
                )

    def test_revision_precommit_mutation_blocks_staging_and_promotion(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dependency = root / "source.md"
            dependency.write_text(_words("source"), encoding="utf-8")
            output = root / "report.md"
            output.write_text(_words("report"), encoding="utf-8")
            state = root / "revision-execution.json"
            record_revision_step(
                state_path=state,
                repo_root=root,
                step_id="word-production",
                dependencies=(RevisionDependency("source.md"),),
                values={"format": "report"},
                outputs=(
                    (
                        output,
                        ArtifactContract("markdown", min_words=20),
                    ),
                ),
            )
            dependency.write_text(
                _words("mutated-before-publish"), encoding="utf-8"
            )
            with (
                patch("cli.publish.stage_release_artifacts") as stage,
                patch("cli.publish.promote_release") as promote,
                self.assertRaisesRegex(
                    RuntimeError,
                    "pre-commit validation failed",
                ),
            ):
                _publish_revision_release(
                    state_path=state,
                    repo_root=root,
                    required_steps={"word-production"},
                    stage4_dir=root / "stage4",
                    slug="sample",
                    release_dir=root / "release",
                    require_executive_summary=False,
                    out_dir=root / "reports",
                )
            stage.assert_not_called()
            promote.assert_not_called()


if __name__ == "__main__":
    unittest.main()
