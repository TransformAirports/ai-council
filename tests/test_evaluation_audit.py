from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cli.agents import Agent
from cli.audit import audit_runs, load_run, render_audit_report
from cli.evaluation import (
    RUBRIC_DIMENSIONS,
    load_quality_reviews,
    record_quality_review,
    write_human_review,
)


def _agent(name: str, display_name: str) -> Agent:
    return Agent(
        name=name,
        display_name=display_name,
        description="",
        tools=(),
        order=1,
        system_prompt="",
        path=Path(f".claude/agents/{name}.md"),
    )


class EvaluationAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.runs_dir = Path(self.temp.name) / "runs"
        self.runs_dir.mkdir()
        self.agents = [
            _agent("operations-analyst", "Operations Analyst"),
            _agent("contrarian", "Contrarian"),
        ]

    def _run_dir(self, slug: str = "test-run") -> Path:
        path = self.runs_dir / f"2026-07-23-{slug}"
        path.mkdir(parents=True)
        return path

    def test_legacy_archive_never_infers_contribution_from_agent_names(self) -> None:
        run_dir = self._run_dir("legacy")
        (run_dir / "stage1").mkdir()
        (run_dir / "stage1" / "operations-analyst-brief.md").write_text(
            "brief words " * 20,
            encoding="utf-8",
        )
        (run_dir / "stage2").mkdir()
        (run_dir / "stage2" / "strategist-draft-v3.md").write_text(
            "draft",
            encoding="utf-8",
        )
        (run_dir / "stage3").mkdir()
        # The display name appears repeatedly. It must not be treated as evidence
        # contribution.
        (run_dir / "stage3" / "final-draft.md").write_text(
            "Operations Analyst Operations Analyst Operations Analyst "
            "[UNVERIFIED: source not found]",
            encoding="utf-8",
        )
        (run_dir / "stage4").mkdir()
        (run_dir / "stage4" / "report.docx").write_bytes(b"not-a-real-docx")
        (run_dir / "retrospective.md").write_text(
            "Total estimated cost: **$12.50**\n",
            encoding="utf-8",
        )

        result = audit_runs(self.runs_dir, self.agents)
        run = result["runs"][0]
        score = result["scores"]["operations-analyst"]

        self.assertEqual(run.unverified_count, 1)
        self.assertEqual(run.cost_total, 12.50)
        self.assertTrue(run.completed_stage4)
        self.assertIsNone(run.evidence_commissioned)
        self.assertIsNone(run.evidence_used)
        self.assertEqual(score.structured_runs, 0)
        self.assertEqual(score.evidence_used, 0)

        report = render_audit_report(result, self.agents)
        self.assertIn("data unavailable", report)
        self.assertIn("never searches final prose for agent names", report)
        self.assertNotIn("citations per 1k", report.lower())
        self.assertNotIn("3 citations", report.lower())

    def test_structured_manifest_ledger_lineage_and_review_are_aggregated(self) -> None:
        run_dir = self._run_dir("structured")
        telemetry = run_dir / "telemetry"
        telemetry.mkdir()
        manifest = {
            "schema_version": "1.0",
            "selected_agents": ["operations-analyst", "contrarian"],
            "cost": {"total_usd": 42.75},
            "stages": {
                "stage1": {"status": "complete"},
                "stage2": {"status": "complete"},
                "stage3": {"status": "complete"},
                "stage4": {"status": "failed"},
            },
            "artifacts": {
                "evidence_ledger": {"path": "telemetry/evidence.jsonl"},
                "claim_lineage": {"path": "telemetry/claims.json"},
                "human_reviews": {"path": "telemetry/reviews.json"},
            },
        }
        (run_dir / "run-manifest.json").write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )
        evidence = [
            {
                "evidence_id": "e1",
                "agent_id": "operations-analyst",
                "is_primary": True,
            },
            {
                "evidence_id": "e2",
                "agent_id": "operations-analyst",
                "source_type": "secondary",
            },
            {
                "evidence_id": "e3",
                "agent_id": "contrarian",
                "source": {"is_primary": True},
            },
            {
                "evidence_id": "e4",
                "source_type": "trade_press",
            },
        ]
        (telemetry / "evidence.jsonl").write_text(
            "\n".join(json.dumps(record) for record in evidence) + "\n",
            encoding="utf-8",
        )
        claims = {
            "claims": [
                {
                    "claim_id": "c1",
                    "verification_status": "verified",
                    "evidence_ids": ["e1"],
                    "primary_source_checked": True,
                },
                {
                    "claim_id": "c2",
                    "verification_status": "removed",
                    "evidence_ids": ["e2"],
                    "primary_source_checked": False,
                    "corrected": True,
                },
                {
                    "claim_id": "c3",
                    "verification_status": "unverified",
                    "evidence_ids": ["e3"],
                    "primary_source_checked": True,
                },
                {
                    "claim_id": "c4",
                    "verification_status": "verified",
                    "evidence_ids": ["missing-ledger-record"],
                    "primary_source_checked": False,
                },
            ]
        }
        (telemetry / "claims.json").write_text(
            json.dumps(claims),
            encoding="utf-8",
        )
        reviews = {
            "reviews": [
                {
                    "review_id": "human-1",
                    "reviewer": {"type": "human", "name": "Airport executive"},
                    "rubric": {
                        "originality": 4,
                        "airport_specificity": 5,
                        "decision_usefulness": 4,
                        "writing": 3,
                        "visual_quality": 2,
                    },
                },
                {
                    "review_id": "model-1",
                    "reviewer": {"type": "model"},
                    "rubric": {"originality": 5},
                },
            ]
        }
        (telemetry / "reviews.json").write_text(
            json.dumps(reviews),
            encoding="utf-8",
        )

        result = audit_runs(self.runs_dir, self.agents)
        run = result["runs"][0]

        self.assertEqual(run.evidence_commissioned, 4)
        self.assertEqual(run.evidence_used, 4)
        self.assertEqual(run.matched_evidence_used, 3)
        self.assertEqual(run.missing_evidence_references, 1)
        self.assertEqual(run.verified_claims, 2)
        self.assertEqual(run.removed_claims, 1)
        self.assertEqual(run.unverified_claims, 1)
        self.assertEqual(run.corrected_claims, 1)
        self.assertEqual(run.corrected_outcome_claims, 0)
        self.assertEqual(run.qualified_claims, 0)
        self.assertEqual(run.claims_with_unknown_outcome, 0)
        self.assertEqual(run.correction_rate, 0.25)
        self.assertEqual(run.primary_source_claims, 2)
        self.assertEqual(run.primary_source_evaluable_claims, 3)
        self.assertEqual(run.primary_source_unclassified_claims, 0)
        self.assertAlmostEqual(run.primary_source_coverage or 0, 2 / 3)
        self.assertEqual(len(run.human_reviews), 1)
        self.assertEqual(run.cost_total, 42.75)
        self.assertFalse(run.completed_stage4)

        operations = result["scores"]["operations-analyst"]
        contrarian = result["scores"]["contrarian"]
        self.assertEqual(operations.structured_runs, 1)
        self.assertEqual(operations.evidence_commissioned, 2)
        self.assertEqual(operations.evidence_used, 2)
        self.assertEqual(contrarian.evidence_commissioned, 1)
        self.assertEqual(contrarian.evidence_used, 1)

        report = render_audit_report(result, self.agents)
        self.assertIn("2/3 (67%)", report)
        self.assertIn(
            "2 verified / 0 qualified / 0 corrected / 1 removed / 1 unverified",
            report,
        )
        self.assertIn("25% of lineage records", report)
        self.assertIn("Originality | 4.0 | 1", report)
        self.assertIn("1 reference(s) do not", report)

    def test_canonical_qualified_and_corrected_are_first_class_outcomes(self) -> None:
        run_dir = self._run_dir("canonical-outcomes")
        (run_dir / "evidence-ledger.jsonl").write_text(
            json.dumps({
                "evidence_id": "e1",
                "agent_id": "operations-analyst",
                "source_type": "airport_document",
            }) + "\n",
            encoding="utf-8",
        )
        (run_dir / "claim-lineage.jsonl").write_text(
            "\n".join(
                json.dumps(record)
                for record in (
                    {
                        "claim_id": "c1",
                        "verification_status": "qualified",
                        "evidence_ids": ["e1"],
                        "primary_source_checked": True,
                    },
                    {
                        "claim_id": "c2",
                        "verification_status": "corrected",
                        "evidence_ids": ["e1"],
                        "primary_source_checked": True,
                    },
                )
            ) + "\n",
            encoding="utf-8",
        )

        run = load_run(run_dir)

        self.assertEqual(run.qualified_claims, 1)
        self.assertEqual(run.corrected_outcome_claims, 1)
        self.assertEqual(run.corrected_claims, 1)
        self.assertEqual(run.claims_with_unknown_outcome, 0)

    def test_unknown_source_classification_is_not_counted_as_secondary(self) -> None:
        run_dir = self._run_dir("unknown-primary")
        (run_dir / "evidence-ledger.json").write_text(
            json.dumps(
                {
                    "evidence": [
                        {"evidence_id": "e1", "agent_id": "operations-analyst"}
                    ]
                }
            ),
            encoding="utf-8",
        )
        (run_dir / "claim-lineage.json").write_text(
            json.dumps(
                {
                    "claims": [
                        {
                            "claim_id": "c1",
                            "status": "verified",
                            "evidence_ids": ["e1"],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )

        run = load_run(run_dir)
        self.assertIsNone(run.primary_source_coverage)
        self.assertEqual(run.primary_source_unclassified_claims, 1)

    def test_council_v2_manifest_and_compatibility_ledger_are_not_double_counted(
        self,
    ) -> None:
        run_dir = self._run_dir("v2-contract")
        (run_dir / "stage1").mkdir()
        (run_dir / "stage2").mkdir()
        evidence_line = json.dumps(
            {
                "evidence_id": "ev-1",
                "agent_id": "operations-analyst",
                "is_primary": True,
            }
        ) + "\n"
        (run_dir / "evidence-ledger.jsonl").write_text(
            evidence_line,
            encoding="utf-8",
        )
        (run_dir / "stage1" / "evidence-ledger.jsonl").write_text(
            evidence_line,
            encoding="utf-8",
        )
        (run_dir / "claim-lineage.jsonl").write_text(
            json.dumps(
                {
                    "claim_id": "claim-1",
                    "evidence_ids": ["ev-1"],
                    "verification_status": "matched_to_evidence_ledger",
                    "primary_source_checked": False,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        (run_dir / "stage2" / "red-team-critique-v1.md").write_text(
            "This is prose, not a machine-readable human rubric.",
            encoding="utf-8",
        )
        manifest = {
            "schema_version": "2.0",
            "selected_research_agents": [
                {"name": "operations-analyst", "display_name": "Operations Analyst"}
            ],
            "contracts": {
                "evidence_ledger": "evidence-ledger.jsonl",
                "evidence_ledger_compatibility": "stage1/evidence-ledger.jsonl",
                "claim_lineage": "claim-lineage.jsonl",
                "quality_reviews": ["stage2/red-team-critique-v1.md"],
            },
            "artifacts": [
                {
                    "id": "stage1/operations-analyst/brief",
                    "path": "stage1/operations-analyst-brief.md",
                    "stage": "research",
                    "required": True,
                    "status": "complete",
                },
                {
                    "id": "evidence/ledger",
                    "path": "evidence-ledger.jsonl",
                    "stage": "evidence",
                    "required": True,
                    "status": "complete",
                },
                {
                    "id": "stage2/strategist-v1",
                    "path": "stage2/strategist-draft-v1.md",
                    "stage": "synthesis",
                    "required": True,
                    "status": "pending",
                },
            ],
            "stages": {},
        }
        (run_dir / "run-manifest.json").write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )

        run = load_run(run_dir)
        self.assertEqual(run.seated_agents, ["operations-analyst"])
        self.assertEqual(run.evidence_commissioned, 1)
        self.assertEqual(len(run.evidence_paths), 1)
        self.assertEqual(run.unverified_claims, 1)
        self.assertEqual(run.primary_source_coverage, 0.0)
        self.assertEqual(run.stage_statuses["stage1"], "complete")
        self.assertEqual(run.stage_statuses["stage2"], "pending")
        self.assertEqual(run.review_paths, ())
        self.assertFalse(any("duplicate evidence" in warning.lower() for warning in run.warnings))

    def test_unreadable_structured_artifact_reports_unavailable_not_zero(self) -> None:
        run_dir = self._run_dir("bad-json")
        (run_dir / "evidence-ledger.jsonl").write_text(
            "{this is not json}\n",
            encoding="utf-8",
        )
        (run_dir / "claim-lineage.json").write_text(
            "not json",
            encoding="utf-8",
        )

        run = load_run(run_dir)
        self.assertFalse(run.has_evidence_ledger)
        self.assertFalse(run.has_claim_lineage)
        self.assertIsNone(run.evidence_commissioned)
        self.assertIsNone(run.verified_claims)
        self.assertTrue(run.warnings)

    def test_quality_review_helpers_write_machine_readable_records(self) -> None:
        run_dir = self._run_dir("reviews")
        ratings = {dimension: 4 for dimension in RUBRIC_DIMENSIONS}
        path = record_quality_review(
            run_dir,
            "checkpoint-2",
            ratings,
            notes="Ready for board review.",
            approved=True,
        )
        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["checkpoint"], "checkpoint-2")
        self.assertTrue(payload["approved"])
        self.assertEqual(payload["rubric"]["visual_quality"]["score"], 4.0)

        reviews, warnings = load_quality_reviews([path])
        self.assertFalse(warnings)
        self.assertEqual(len(reviews), 1)
        self.assertTrue(reviews[0].is_human)
        self.assertEqual(set(reviews[0].rubric), set(RUBRIC_DIMENSIONS))

        second = write_human_review(
            run_dir,
            {"originality": 5},
            review_id="partial",
        )
        self.assertTrue(second.is_file())

    def test_quality_review_helper_rejects_incomplete_or_out_of_range_rubric(self) -> None:
        run_dir = self._run_dir("bad-review")
        with self.assertRaises(ValueError):
            record_quality_review(
                run_dir,
                "checkpoint-1",
                {"originality": 4},
            )
        ratings = {dimension: 4 for dimension in RUBRIC_DIMENSIONS}
        ratings["writing"] = 6
        with self.assertRaises(ValueError):
            record_quality_review(
                run_dir,
                "checkpoint-1",
                ratings,
            )

    def test_empty_runs_directory_renders_compatible_markdown(self) -> None:
        result = audit_runs(self.runs_dir, self.agents)
        report = render_audit_report(result, self.agents)
        self.assertEqual(result["runs"], [])
        self.assertIn("No archived runs found", report)


if __name__ == "__main__":
    unittest.main()
