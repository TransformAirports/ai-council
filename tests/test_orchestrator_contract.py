from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from cli.orchestrator import (
    CONTEXT_SOURCES_CONTRACT,
    PIPELINE_DEFINITION,
    _stage1_prompt,
    _stage2_prompts,
    assert_resume_identity,
    run_pipeline,
)
from cli.artifacts import validate_artifact
from cli.run_manifest import ResumeContractMismatch


class OrchestratorContractTests(unittest.TestCase):
    def test_context_source_inventory_is_atomic_and_verifier_bound(self) -> None:
        context_step = next(
            step for step in PIPELINE_DEFINITION if step.id == "airport-context"
        )
        fact_step = next(
            step for step in PIPELINE_DEFINITION if step.id == "fact-checker"
        )
        self.assertEqual(context_step.output, "context/airport-context.md")
        self.assertIn(
            "context/context-sources.jsonl",
            fact_step.inputs,
        )
        with tempfile.TemporaryDirectory() as tmp:
            empty_inventory = Path(tmp) / "context-sources.jsonl"
            empty_inventory.write_text("\n", encoding="utf-8")
            self.assertTrue(
                validate_artifact(
                    empty_inventory, CONTEXT_SOURCES_CONTRACT
                ).valid
            )

    def test_declarative_sequence_contains_distinct_review_roles(self) -> None:
        synthesis_ids = [
            step.id for step in PIPELINE_DEFINITION if step.phase == "synthesis"
        ]
        self.assertEqual(
            synthesis_ids,
            [
                "creative-director",
                "strategist-v1",
                "evidence-prosecutor",
                "strategist-v2",
                "airport-executive-review",
                "strategist-v3",
            ],
        )

    def test_research_prompt_requires_context_and_evidence_companion(self) -> None:
        agent = SimpleNamespace(provider="anthropic")
        prompt = _stage1_prompt(
            agent,
            Path("prompts/runs/test.md"),
            Path("outputs/stage1/alpha-brief.md"),
            "",
        )
        self.assertIn("outputs/context/airport-context.md", prompt)
        self.assertIn("alpha-evidence.jsonl", prompt)
        self.assertIn("is_primary", prompt)

    def test_synthesis_prompt_has_no_fixed_eight_agent_assumption(self) -> None:
        prompts = _stage2_prompts(Path("prompts/runs/test.md"))
        self.assertNotIn("all eight", prompts["strategist-v1"].lower())
        self.assertIn("run-manifest.json", prompts["strategist-v1"])

    def test_resume_receipts_cover_each_step_scoped_prompt_input(self) -> None:
        expected = {
            "creative-director": {
                "run-manifest.json",
                "context/airport-context.md",
                "evidence-ledger.jsonl",
                "stage1/evidence-map.md",
            },
            "strategist-v1": {
                "run-manifest.json",
                "context/airport-context.md",
                "stage1/*-brief.md",
                "stage2/narrative-options.md",
                "stage1/evidence-map.md",
                "evidence-ledger.jsonl",
            },
            "evidence-prosecutor": {
                "run-manifest.json",
                "stage1/*-brief.md",
                "stage1/evidence-map.md",
                "stage2/strategist-draft-v1.md",
                "evidence-ledger.jsonl",
            },
            "strategist-v2": {
                "run-manifest.json",
                "stage1/*-brief.md",
                "stage1/evidence-map.md",
                "evidence-ledger.jsonl",
                "stage2/narrative-options.md",
                "stage2/strategist-draft-v1.md",
                "stage2/red-team-critique-v1.md",
            },
            "airport-executive-review": {
                "run-manifest.json",
                "stage2/strategist-draft-v2.md",
                "stage2/red-team-critique-v1.md",
                "context/airport-context.md",
                "stage1/evidence-map.md",
            },
            "strategist-v3": {
                "run-manifest.json",
                "stage1/*-brief.md",
                "stage1/evidence-map.md",
                "evidence-ledger.jsonl",
                "stage2/narrative-options.md",
                "stage2/strategist-draft-v2.md",
                "stage2/red-team-critique-v2.md",
            },
            "editor": {
                "run-manifest.json",
                "stage2/strategist-draft-v3.md",
            },
            "humanizer": {
                "run-manifest.json",
                "stage3/edited-draft.md",
            },
            "fact-checker": {
                "run-manifest.json",
                "stage1/*-brief.md",
                "stage1/evidence-map.md",
                "stage3/humanized-draft.md",
                "evidence-ledger.jsonl",
                "context/airport-context.md",
                "context/context-sources.jsonl",
            },
            "art-director": {
                "stage3/final-draft.md",
                "stage3/fact-check-report.md",
                "run-manifest.json",
                "stage1/evidence-map.md",
                "evidence-ledger.jsonl",
                "claim-lineage.jsonl",
                "context/airport-context.md",
            },
            "presentation": {
                "stage4/visual-brief.json",
                "stage3/final-draft.md",
                "stage3/fact-check-report.md",
                "claim-lineage.jsonl",
                "evidence-ledger.jsonl",
                "context/airport-context.md",
                "run-manifest.json",
            },
        }
        steps = {step.id: set(step.inputs) for step in PIPELINE_DEFINITION}
        for step_id, inputs in expected.items():
            self.assertEqual(steps[step_id], inputs, step_id)

    def test_resume_requires_matching_marker_and_manifest_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            outputs = Path(tmp)
            (outputs / ".active-run.json").write_text(
                '{"slug": "run-a"}', encoding="utf-8"
            )
            (outputs / "run-manifest.json").write_text(
                '{"run": {"slug": "run-a"}}', encoding="utf-8"
            )
            assert_resume_identity(outputs, "run-a")

            with self.assertRaisesRegex(RuntimeError, "belongs to 'run-a'"):
                assert_resume_identity(outputs, "run-b")

            (outputs / "run-manifest.json").write_text(
                '{"run": {"slug": "run-c"}}', encoding="utf-8"
            )
            with self.assertRaisesRegex(RuntimeError, "marker names 'run-a'"):
                assert_resume_identity(outputs, "run-a")

    def test_resume_contract_is_validated_before_marker_is_refreshed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outputs = root / "outputs"
            outputs.mkdir()
            marker_path = outputs / ".active-run.json"
            original_marker = '{"slug": "run-a", "started": "original"}'
            marker_path.write_text(original_marker, encoding="utf-8")
            (outputs / "run-manifest.json").write_text(
                '{"run": {"slug": "run-a"}}', encoding="utf-8"
            )
            run_file = root / "run-a.md"
            run_file.write_text("# Run: A", encoding="utf-8")
            spec = SimpleNamespace(
                slug="run-a",
                title="Run A",
                thesis="Test",
                selected_research_agents=[],
                output_format="brief",
                want_pptx=False,
                deck_mode="board_decision",
            )

            with (
                patch("cli.orchestrator.load_all_agents", return_value=[]),
                patch("cli.orchestrator._model", return_value="test-model"),
                patch(
                    "cli.orchestrator.create_run_manifest",
                    side_effect=ResumeContractMismatch("changed contract"),
                ),
                patch("cli.orchestrator.write_run_marker") as write_marker,
                self.assertRaisesRegex(ResumeContractMismatch, "changed contract"),
            ):
                asyncio.run(
                    run_pipeline(
                        spec=spec,
                        run_file=run_file,
                        repo_root=root,
                        auto_approve=True,
                        resume=True,
                    )
                )

            write_marker.assert_not_called()
            self.assertEqual(
                marker_path.read_text(encoding="utf-8"), original_marker
            )


if __name__ == "__main__":
    unittest.main()
