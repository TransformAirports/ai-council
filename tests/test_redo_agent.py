"""Changing one agent's instructions must not condemn the whole run.

The resume guard refuses to reuse artifacts produced under different agent
instructions — correctly. But it refuses at whole-run granularity, so editing
the fact-checker blocked a resume whose only at-risk artifacts were the
fact-checker's own, which the resume regenerates anyway. `--redo-agent` makes
the guarantee precise: discard that agent's output, keep everyone else's.
"""
from __future__ import annotations

import unittest

from cli.resume_repair import _discard_agent_artifacts


def _artifact(path: str, producer: str) -> dict:
    return {"path": path, "producer": producer, "status": "complete",
            "sha256": "a" * 64, "dependencies": {"inputs": []},
            "record_count": 12, "completed_at": "2026-08-07T00:00:00+00:00"}


class RedoAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = {"artifacts": [
            _artifact("stage3/final-draft.md", "fact-checker"),
            _artifact("claim-lineage.jsonl", "fact-checker"),
            _artifact("stage1/economist-brief.md", "infrastructure-economist"),
            _artifact("stage2/strategist-draft.md", "strategist"),
        ]}

    def test_the_edited_agents_artifacts_are_reset_for_regeneration(self) -> None:
        discarded = _discard_agent_artifacts(self.manifest, {"fact-checker"})
        self.assertEqual(sorted(discarded),
                         ["claim-lineage.jsonl", "stage3/final-draft.md"])
        for a in self.manifest["artifacts"]:
            if a["producer"] == "fact-checker":
                self.assertEqual(a["status"], "pending")
                # The receipt must go too: a stale hash would let the
                # orchestrator treat the old file as still valid.
                for gone in ("sha256", "dependencies", "record_count", "completed_at"):
                    self.assertNotIn(gone, a)

    def test_other_agents_paid_work_is_untouched(self) -> None:
        _discard_agent_artifacts(self.manifest, {"fact-checker"})
        others = [a for a in self.manifest["artifacts"]
                  if a["producer"] != "fact-checker"]
        self.assertEqual(len(others), 2)
        for a in others:
            self.assertEqual(a["status"], "complete")
            self.assertEqual(a["sha256"], "a" * 64)
            self.assertIn("dependencies", a)

    def test_an_unknown_agent_name_discards_nothing(self) -> None:
        self.assertEqual(_discard_agent_artifacts(self.manifest, {"nobody"}), [])
        self.assertTrue(all(a["status"] == "complete"
                            for a in self.manifest["artifacts"]))

    def test_several_agents_can_be_redone_at_once(self) -> None:
        discarded = _discard_agent_artifacts(
            self.manifest, {"fact-checker", "strategist"})
        self.assertEqual(len(discarded), 3)
        kept = [a for a in self.manifest["artifacts"] if a["status"] == "complete"]
        self.assertEqual([a["producer"] for a in kept], ["infrastructure-economist"])
