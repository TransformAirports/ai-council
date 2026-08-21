from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from cli.checkpoints import _capture_review_snapshot, checkpoint_after_stage2
from cli.run_manifest import (
    CheckpointInputsChanged,
    build_dependency_fingerprint,
    checkpoint_approval_matches,
    record_checkpoint_decision,
)


class CheckpointPersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.outputs = Path(self._tmp.name) / "outputs"
        self.outputs.mkdir()
        self.manifest = self.outputs / "run-manifest.json"
        self.manifest.write_text(
            json.dumps(
                {
                    "schema_version": "2.0",
                    "run": {"resume_identity_sha256": "a" * 64},
                    "artifacts": [],
                }
            ),
            encoding="utf-8",
        )
        self.draft = self.outputs / "stage2" / "strategist-draft-v3.md"
        self.critique = self.outputs / "stage2" / "red-team-critique-v2.md"
        self.draft.parent.mkdir(parents=True)
        self.draft.write_text("approved draft", encoding="utf-8")
        self.critique.write_text("approved critique", encoding="utf-8")
        self.inputs = (
            "stage2/strategist-draft-v3.md",
            "stage2/red-team-critique-v2.md",
        )

    def test_approval_is_reused_only_for_the_reviewed_bytes(self) -> None:
        record_checkpoint_decision(
            self.manifest,
            "stage2",
            approved=True,
            action="continue",
            declared_inputs=self.inputs,
        )
        self.assertTrue(
            checkpoint_approval_matches(
                self.manifest, "stage2", self.inputs
            )
        )

        self.draft.write_text("changed after approval", encoding="utf-8")
        self.assertFalse(
            checkpoint_approval_matches(
                self.manifest, "stage2", self.inputs
            )
        )

    def test_abort_is_recorded_for_audit_but_never_skips_review(self) -> None:
        record_checkpoint_decision(
            self.manifest,
            "stage2",
            approved=False,
            action="abort",
            declared_inputs=self.inputs,
        )
        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        self.assertEqual(payload["checkpoints"]["stage2"]["action"], "abort")
        self.assertFalse(
            checkpoint_approval_matches(
                self.manifest, "stage2", self.inputs
            )
        )

    def test_different_declared_input_set_never_reuses_approval(self) -> None:
        record_checkpoint_decision(
            self.manifest,
            "stage2",
            approved=True,
            action="continue",
            declared_inputs=self.inputs,
        )
        self.assertFalse(
            checkpoint_approval_matches(
                self.manifest,
                "stage2",
                ("stage2/strategist-draft-v3.md",),
            )
        )

    def test_reviewed_snapshot_is_persisted_when_inputs_are_unchanged(self) -> None:
        reviewed = build_dependency_fingerprint(self.manifest, self.inputs)
        record_checkpoint_decision(
            self.manifest,
            "stage2",
            approved=True,
            action="continue",
            declared_inputs=self.inputs,
            reviewed_fingerprint=reviewed,
        )

        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["checkpoints"]["stage2"]["dependencies"], reviewed
        )

    def test_mutation_before_record_rejects_reviewed_snapshot(self) -> None:
        reviewed = build_dependency_fingerprint(self.manifest, self.inputs)
        self.draft.write_text(
            "mutated while awaiting decision", encoding="utf-8"
        )

        with self.assertRaisesRegex(
            CheckpointInputsChanged, "changed while the checkpoint"
        ):
            record_checkpoint_decision(
                self.manifest,
                "stage2",
                approved=True,
                action="continue",
                declared_inputs=self.inputs,
                reviewed_fingerprint=reviewed,
            )

        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        self.assertNotIn("checkpoints", payload)

    def test_mutation_during_web_review_is_detected_at_record(self) -> None:
        third = self.outputs / "stage2" / "red-team-critique-v1.md"
        third.write_text("first critique", encoding="utf-8")
        shown_draft = ""

        async def mutate_then_continue(kind, payload):
            nonlocal shown_draft
            self.assertEqual(kind, "stage2")
            shown_draft = payload["documents"][0]["content"]
            self.draft.write_text(
                "mutated while the reviewer was deciding", encoding="utf-8"
            )
            return {"action": "continue"}

        with (
            patch("cli.checkpoints.get_sink", return_value=object()),
            patch(
                "cli.checkpoints.request_checkpoint",
                new=AsyncMock(side_effect=mutate_then_continue),
            ),
            patch("cli.checkpoints._show_file_excerpt"),
        ):
            result = asyncio.run(checkpoint_after_stage2(self.outputs))

        self.assertTrue(result.approved)
        self.assertEqual(shown_draft, "approved draft")
        self.assertIsNotNone(result.reviewed_fingerprint)
        with self.assertRaises(CheckpointInputsChanged):
            record_checkpoint_decision(
                self.manifest,
                "stage2",
                approved=result.approved,
                action="continue",
                declared_inputs=(
                    "stage2/strategist-draft-v3.md",
                    "stage2/red-team-critique-v2.md",
                    "stage2/red-team-critique-v1.md",
                ),
                reviewed_fingerprint=result.reviewed_fingerprint,
            )

    def test_mutation_during_snapshot_capture_fails_closed(self) -> None:
        from cli.run_manifest import build_dependency_fingerprint as build

        calls = 0

        def mutate_after_first_fingerprint(manifest_path, declarations):
            nonlocal calls
            fingerprint = build(manifest_path, declarations)
            calls += 1
            if calls == 1:
                self.draft.write_text("changed during capture", encoding="utf-8")
            return fingerprint

        with patch(
            "cli.checkpoints.build_dependency_fingerprint",
            side_effect=mutate_after_first_fingerprint,
        ):
            with self.assertRaisesRegex(RuntimeError, "changed while.*captured"):
                _capture_review_snapshot(self.outputs, self.inputs)


if __name__ == "__main__":
    unittest.main()
