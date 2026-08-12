"""The publication gate must get more than one chance to converge.

A run that reaches stage 4 has already been paid for end to end. When the gate
reported 45 blockers, a single remediation pass cleared only some of them and
the whole run was discarded — so the pipeline retries, re-gating after each
pass and stopping the moment it is clean, within a hard bound.
"""
from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cli.agents import Agent
from cli.orchestrator import (
    MAX_REMEDIATION_PASSES,
    CostTally,
    run_quality_gate_with_remediation,
)
from cli.quality_gate import PublicationQualityError, QualityIssue


class RemediationPassTests(unittest.TestCase):
    def _run(self, passes_on_call: int | None):
        """Drive the gate; it succeeds on `passes_on_call` (None = never)."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = root / "outputs"
            stage3 = outputs / "stage3"
            stage3.mkdir(parents=True)
            run_file = root / "prompts" / "runs" / "t.md"
            run_file.parent.mkdir(parents=True)
            run_file.write_text("# Run: T", encoding="utf-8")
            (outputs / "run-manifest.json").write_text(
                json.dumps({"schema_version": "2.0",
                            "run": {"resume_identity_sha256": "a" * 64},
                            "artifacts": []}), encoding="utf-8")
            (stage3 / "final-draft.md").write_text(" ".join(["w"] * 30), encoding="utf-8")
            (stage3 / "fact-check-report.md").write_text(" ".join(["v"] * 30), encoding="utf-8")
            record = {"claim_id": "C1", "claim": "A claim.", "citation": "Source.",
                      "footnote_id": "1", "evidence_ids": ["E1"],
                      "verification_status": "verified", "primary_source_checked": True,
                      "retained": True, "draft_sha256": "b" * 64}
            (outputs / "claim-lineage.jsonl").write_text(
                json.dumps(record) + "\n", encoding="utf-8")
            (outputs / "evidence-ledger.jsonl").write_text(
                json.dumps({"evidence_id": "E1", "agent_id": "r", "claim": "A claim.",
                            "source_title": "S", "source_type": "primary",
                            "is_primary": True, "confidence": "high",
                            "source_url": "https://e.com"}) + "\n", encoding="utf-8")

            calls = {"gate": 0, "agent": 0}

            def fake_gate(**kwargs):
                calls["gate"] += 1
                ok = passes_on_call is not None and calls["gate"] >= passes_on_call
                report = kwargs["report_path"]
                payload = {"schema_version": "1.0", "passed": ok,
                           "error_count": 0 if ok else 1, "warning_count": 0,
                           "issues": [] if ok else [{"severity": "error",
                                                     "code": "t", "message": "Fix."}]}
                report.write_text(json.dumps(payload), encoding="utf-8")
                if not ok:
                    raise PublicationQualityError(
                        report, [QualityIssue("error", "t", "Fix.")])
                return payload

            async def fake_run_agent(**kwargs):
                calls["agent"] += 1
                kwargs["output_path"].write_text(" ".join(["r"] * 30), encoding="utf-8")
                for path, _c in kwargs["required_outputs"]:
                    if path.suffix == ".jsonl":
                        path.write_text(json.dumps(record) + "\n", encoding="utf-8")
                    else:
                        path.write_text(" ".join(["r"] * 50), encoding="utf-8")
                return {"skipped": False, "provider": "anthropic", "cost": 0.0, "turns": 1}

            verifier = Agent(name="fact-checker", display_name="Fact-checker",
                             description="v", tools=(), order=1,
                             system_prompt="Verify.", path=root / "fc.md")
            spec = type("Spec", (), {"output_format": "report", "length": ""})()

            with (
                patch("cli.orchestrator.run_publication_quality_gate", fake_gate),
                patch("cli.orchestrator._run_agent", fake_run_agent),
                patch("cli.orchestrator.ensure_claim_lineage", return_value=([record], False)),
                patch("cli.orchestrator.bind_claim_lineage_to_draft", return_value=[record]),
            ):
                error = None
                try:
                    payload = asyncio.run(run_quality_gate_with_remediation(
                        spec=spec, run_file=run_file, outputs_dir=outputs,
                        all_agents=[verifier], tally=CostTally(),
                        manifest_path=outputs / "run-manifest.json",
                        agent_names=["fact-checker"]))
                except PublicationQualityError as exc:
                    payload, error = None, exc
            return payload, error, calls

    def test_a_second_pass_runs_when_the_first_does_not_clear_the_gate(self) -> None:
        payload, error, calls = self._run(passes_on_call=3)
        self.assertIsNone(error)
        self.assertTrue(payload["passed"])
        self.assertEqual(calls["agent"], 2, "the verifier must get a second attempt")
        self.assertEqual(calls["gate"], 3)

    def test_it_stops_the_moment_the_gate_is_clean(self) -> None:
        payload, error, calls = self._run(passes_on_call=2)
        self.assertIsNone(error)
        self.assertEqual(calls["agent"], 1, "no pass may run after the gate is clean")
        self.assertEqual(calls["gate"], 2)

    def test_retries_are_bounded_and_the_failure_still_surfaces(self) -> None:
        payload, error, calls = self._run(passes_on_call=None)
        self.assertIsNone(payload)
        self.assertIsInstance(error, PublicationQualityError)
        self.assertEqual(calls["agent"], MAX_REMEDIATION_PASSES)
        self.assertEqual(calls["gate"], MAX_REMEDIATION_PASSES + 1)
