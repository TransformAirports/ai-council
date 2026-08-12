"""A re-baseline must move the receipts that point at the run identity.

Every completed artifact records the run identity it was bound to. Moving the
run's identity without moving those receipts leaves each artifact pointing at an
identity that no longer exists — and the orchestrator quarantines and re-runs
any artifact whose receipt does not match. A re-baseline meant to make resume
safe would instead silently discard every paid brief in the run.
"""
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cli.resume_repair import _restamp_dependency_identities

OLD = "a" * 64
NEW = "b" * 64
OTHER = "c" * 64


def _artifact(path: str, sha256: str, identity: str) -> dict:
    return {
        "path": path,
        "sha256": sha256,
        "status": "complete",
        "dependencies": {
            "inputs": [
                {
                    "declared_input": "run-manifest.json",
                    "files": [
                        {"path": "run-manifest.json",
                         "kind": "run_identity", "sha256": identity}
                    ],
                }
            ]
        },
    }


class RestampTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.outputs = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def _write(self, name: str, body: str) -> str:
        target = self.outputs / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        return hashlib.sha256(target.read_bytes()).hexdigest()

    def test_intact_artifacts_follow_the_new_identity(self) -> None:
        digest = self._write("stage1/brief.md", "settled work")
        manifest = {"artifacts": [_artifact("stage1/brief.md", digest, OLD)]}
        touched = _restamp_dependency_identities(
            manifest, OLD, NEW, outputs_dir=self.outputs
        )
        self.assertEqual(touched, ["stage1/brief.md"])
        entry = manifest["artifacts"][0]["dependencies"]["inputs"][0]["files"][0]
        self.assertEqual(entry["sha256"], NEW)

    def test_changed_bytes_are_left_for_the_orchestrator_to_rerun(self) -> None:
        digest = self._write("stage1/brief.md", "settled work")
        self._write("stage1/brief.md", "rewritten since the receipt")
        manifest = {"artifacts": [_artifact("stage1/brief.md", digest, OLD)]}
        touched = _restamp_dependency_identities(
            manifest, OLD, NEW, outputs_dir=self.outputs
        )
        self.assertEqual(touched, [], "a real mismatch must not be laundered")
        entry = manifest["artifacts"][0]["dependencies"]["inputs"][0]["files"][0]
        self.assertEqual(entry["sha256"], OLD)

    def test_receipts_from_another_run_are_untouched(self) -> None:
        digest = self._write("stage1/brief.md", "settled work")
        manifest = {"artifacts": [_artifact("stage1/brief.md", digest, OTHER)]}
        touched = _restamp_dependency_identities(
            manifest, OLD, NEW, outputs_dir=self.outputs
        )
        self.assertEqual(touched, [])
        entry = manifest["artifacts"][0]["dependencies"]["inputs"][0]["files"][0]
        self.assertEqual(entry["sha256"], OTHER)

    def test_missing_files_are_skipped(self) -> None:
        manifest = {"artifacts": [_artifact("stage1/gone.md", "d" * 64, OLD)]}
        touched = _restamp_dependency_identities(
            manifest, OLD, NEW, outputs_dir=self.outputs
        )
        self.assertEqual(touched, [])

    def test_a_no_op_identity_move_changes_nothing(self) -> None:
        digest = self._write("stage1/brief.md", "settled work")
        manifest = {"artifacts": [_artifact("stage1/brief.md", digest, OLD)]}
        self.assertEqual(
            _restamp_dependency_identities(
                manifest, OLD, OLD, outputs_dir=self.outputs
            ),
            [],
        )
