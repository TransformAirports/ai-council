from __future__ import annotations

import unittest

from cli.agents import (
    PROCESS_AGENT_NAMES,
    RESEARCH_AGENT_NAMES,
    load_all_agents,
    process_agents,
)
from cli.config import DEFAULT_MODELS


class CouncilV2RegistryTests(unittest.TestCase):
    def test_v2_process_agents_are_registered_and_loadable(self) -> None:
        required = {
            "airport-context-builder",
            "evidence-curator",
            "creative-director",
            "evidence-prosecutor",
            "airport-executive-reviewer",
            "art-director",
        }
        self.assertTrue(required.issubset(PROCESS_AGENT_NAMES))
        loaded = process_agents(load_all_agents())
        self.assertTrue(required.issubset(loaded))
        for name in required:
            self.assertTrue(loaded[name].system_prompt)

    def test_v2_model_roles_have_defaults(self) -> None:
        for role in {
            "context",
            "curation",
            "creative",
            "executive_review",
            "art_direction",
        }:
            self.assertIn(role, DEFAULT_MODELS)
            self.assertTrue(DEFAULT_MODELS[role])

    def test_quantitative_analyst_is_a_standard_research_lens(self) -> None:
        self.assertIn("quantitative-analyst", RESEARCH_AGENT_NAMES)
        loaded = {agent.name: agent for agent in load_all_agents()}
        self.assertTrue(loaded["quantitative-analyst"].is_standard_research)
        self.assertIn("Bash", loaded["quantitative-analyst"].tools)


if __name__ == "__main__":
    unittest.main()
