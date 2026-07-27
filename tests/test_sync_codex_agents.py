from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.sync_codex_agents import sync_agents


class SyncCodexAgentsTests(unittest.TestCase):
    def test_check_detects_drift_and_sync_removes_stale_mirrors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            target = root / "target"
            source.mkdir()
            target.mkdir()
            (source / "alpha.md").write_text(
                "---\n"
                "name: alpha\n"
                "description: Test agent\n"
                "---\n"
                "Follow the evidence.\n",
                encoding="utf-8",
            )
            (target / "stale.toml").write_text("name = \"stale\"\n", encoding="utf-8")

            clean, messages = sync_agents(
                source_dir=source, target_dir=target, check=True
            )
            self.assertFalse(clean)
            self.assertTrue(any("out of sync" in message for message in messages))
            self.assertTrue(any("stale mirror" in message for message in messages))

            clean, _ = sync_agents(source_dir=source, target_dir=target)
            self.assertTrue(clean)
            self.assertTrue((target / "alpha.toml").is_file())
            self.assertFalse((target / "stale.toml").exists())

            clean, messages = sync_agents(
                source_dir=source, target_dir=target, check=True
            )
            self.assertTrue(clean)
            self.assertEqual(messages, [])


if __name__ == "__main__":
    unittest.main()
