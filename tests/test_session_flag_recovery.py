"""A session flag with no fault behind it must not kill a stage-4 run.

Observed live: the fact-checker's sampled draft matched a harness stop
sequence mid-write, the CLI marked the session ``is_error`` with
``stop_reason: stop_sequence`` and ``subtype: success`` — no error text, no
denial, no API status. The artifacts are the ground truth: complete work is
accepted, incomplete work earns one clean retry, and a genuine fault still
fails with diagnostics that name the actual trigger.
"""
from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from claude_agent_sdk import ResultMessage

from cli.artifacts import ArtifactContract
from cli.orchestrator import CostTally, _run_agent
from tests.test_orchestrator_runtime import _agent


def _flagged(cost: float = 0.4) -> ResultMessage:
    return ResultMessage(
        subtype="success",
        duration_ms=1,
        duration_api_ms=1,
        is_error=True,
        num_turns=6,
        session_id="s",
        stop_reason="stop_sequence",
        total_cost_usd=cost,
    )


def _clean() -> ResultMessage:
    return ResultMessage(
        subtype="success", duration_ms=1, duration_api_ms=1, is_error=False,
        num_turns=4, session_id="s", stop_reason="end_turn", total_cost_usd=0.3,
    )


class SessionFlagRecoveryTests(unittest.TestCase):
    def _scaffold(self, root: Path) -> tuple[Path, Path, ArtifactContract]:
        outputs = root / "outputs"
        stage3 = outputs / "stage3"
        stage3.mkdir(parents=True)
        manifest = outputs / "run-manifest.json"
        manifest.write_text(
            json.dumps({"schema_version": "2.0",
                        "run": {"resume_identity_sha256": "a" * 64},
                        "artifacts": []}), encoding="utf-8")
        return manifest, stage3 / "final-draft.md", ArtifactContract("markdown", min_words=20)

    def test_complete_artifacts_survive_a_flagged_session(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, output, contract = self._scaffold(root)

            async def fake_query(*, prompt, options):
                del prompt, options
                output.write_text(" ".join(["finished"] * 30), encoding="utf-8")
                yield _flagged()

            with patch("claude_agent_sdk.query", fake_query):
                result = asyncio.run(_run_agent(
                    agent=_agent(root), user_prompt="Verify.", model="m",
                    cwd=root, step_label="stage3/fact-checker",
                    tally=CostTally(), output_path=output,
                    artifact_contract=contract, manifest_path=manifest))
            self.assertFalse(result["skipped"])
            self.assertTrue(output.is_file(), "completed work must be kept")

    def test_incomplete_work_earns_one_retry_and_the_retry_wins(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, output, contract = self._scaffold(root)
            calls = {"n": 0}

            async def fake_query(*, prompt, options):
                del prompt, options
                calls["n"] += 1
                if calls["n"] == 1:
                    yield _flagged()  # stopped early, wrote nothing usable
                else:
                    output.write_text(" ".join(["retried"] * 30), encoding="utf-8")
                    yield _clean()

            with patch("claude_agent_sdk.query", fake_query), \
                 patch("cli.orchestrator.asyncio.sleep", new=lambda *_: _noop()):
                result = asyncio.run(_run_agent(
                    agent=_agent(root), user_prompt="Verify.", model="m",
                    cwd=root, step_label="stage3/fact-checker",
                    tally=CostTally(), output_path=output,
                    artifact_contract=contract, manifest_path=manifest))
            self.assertEqual(calls["n"], 2, "the flagged attempt must be retried")
            self.assertFalse(result["skipped"])
            self.assertIn("retried", output.read_text(encoding="utf-8"))

    def test_a_genuine_fault_still_fails_and_names_the_trigger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, output, contract = self._scaffold(root)

            async def fake_query(*, prompt, options):
                del prompt, options
                yield _flagged()  # never writes output, both attempts

            with patch("claude_agent_sdk.query", fake_query), \
                 patch("cli.orchestrator.asyncio.sleep", new=lambda *_: _noop()):
                with self.assertRaises(RuntimeError) as raised:
                    asyncio.run(_run_agent(
                        agent=_agent(root), user_prompt="Verify.", model="m",
                        cwd=root, step_label="stage3/fact-checker",
                        tally=CostTally(), output_path=output,
                        artifact_contract=contract, manifest_path=manifest))
            message = str(raised.exception)
            self.assertIn("is_error", message,
                          "the diagnostic must name the actual trigger")


async def _noop():
    return None
