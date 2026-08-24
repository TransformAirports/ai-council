from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from cli.resume_repair import _effective_model_for_resume


class ResumeRepairModelTests(unittest.TestCase):
    def test_explicit_run_model_overrides_every_legacy_role_and_agent_route(self) -> None:
        spec = SimpleNamespace(council_model="gpt-5.6-sol")
        agent = SimpleNamespace(model_override="claude-fable-5")

        with patch("cli.orchestrator._model", return_value="opus"):
            self.assertEqual(
                _effective_model_for_resume(spec, agent, "research"),
                "gpt-5.6-sol",
            )

    def test_legacy_run_keeps_agent_then_role_routing(self) -> None:
        spec = SimpleNamespace(council_model="")
        with patch("cli.orchestrator._model", return_value="opus"):
            self.assertEqual(
                _effective_model_for_resume(
                    spec, SimpleNamespace(model_override="claude-fable-5"), "research"
                ),
                "claude-fable-5",
            )
            self.assertEqual(
                _effective_model_for_resume(
                    spec, SimpleNamespace(model_override=None), "research"
                ),
                "opus",
            )


if __name__ == "__main__":
    unittest.main()
