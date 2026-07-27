from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cli.evidence import (
    build_evidence_ledger,
    ensure_claim_lineage,
    normalise_evidence_ledger,
)


class EvidenceContractTests(unittest.TestCase):
    def test_structured_and_legacy_evidence_merge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage1 = root / "stage1"
            stage1.mkdir()
            (stage1 / "alpha-evidence.jsonl").write_text(
                json.dumps(
                    {
                        "claim": "The airport served ten million passengers.",
                        "source": "Airport annual report",
                        "source_url": "https://airport.example/report",
                        "source_type": "official airport report",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (stage1 / "alpha-brief.md").write_text(
                "A brief with structured evidence.", encoding="utf-8"
            )
            (stage1 / "beta-brief.md").write_text(
                "Gate utilization reached 82 percent. "
                "[Source: https://airport.example/gates]",
                encoding="utf-8",
            )

            ledger = root / "evidence-ledger.jsonl"
            mirror = stage1 / "evidence-ledger.jsonl"
            result = build_evidence_ledger(
                selected_agents=["alpha", "beta"],
                stage1_dir=stage1,
                output_path=ledger,
                compatibility_path=mirror,
            )

            self.assertEqual(result.structured_records, 1)
            self.assertEqual(result.legacy_records, 1)
            self.assertEqual(result.record_count, 2)
            self.assertEqual(ledger.read_text(), mirror.read_text())
            records = [
                json.loads(line) for line in ledger.read_text().splitlines()
            ]
            alpha = next(record for record in records if record["agent_id"] == "alpha")
            self.assertTrue(alpha["is_primary"])

    def test_claim_lineage_fallback_matches_evidence_url(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = root / "evidence-ledger.jsonl"
            ledger.write_text(
                json.dumps(
                    {
                        "evidence_id": "ev-1",
                        "claim": "Passenger growth",
                        "source": "Annual report",
                        "source_url": "https://airport.example/report",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            final = root / "final-draft.md"
            final.write_text(
                "Passenger volume rose ten percent.[^1]\n\n"
                "[^1]: Airport annual report, https://airport.example/report\n",
                encoding="utf-8",
            )
            lineage_path = root / "claim-lineage.jsonl"
            lineage, generated = ensure_claim_lineage(
                final_draft=final,
                evidence_ledger=ledger,
                output_path=lineage_path,
            )
            self.assertTrue(generated)
            self.assertEqual(lineage[0]["evidence_ids"], ["ev-1"])
            self.assertEqual(lineage[0]["verification_status"], "unverified")
            self.assertEqual(
                lineage[0]["match_status"], "matched_to_evidence_ledger"
            )
            self.assertFalse(lineage[0]["primary_source_checked"])

    def test_agent_local_evidence_ids_are_namespaced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stage1 = root / "stage1"
            stage1.mkdir()
            for agent in ("alpha", "beta"):
                (stage1 / f"{agent}-evidence.jsonl").write_text(
                    json.dumps(
                        {
                            "evidence_id": "E-0001",
                            "claim": f"{agent} claim",
                            "source_title": f"{agent} report",
                            "source_url": f"https://{agent}.example/report",
                            "source_type": "official_statement",
                            "confidence": "high",
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )
            result = build_evidence_ledger(
                selected_agents=["alpha", "beta"],
                stage1_dir=stage1,
                output_path=root / "evidence-ledger.jsonl",
            )
            ids = {record["evidence_id"] for record in result.records}
            self.assertEqual(ids, {"alpha::E-0001", "beta::E-0001"})

    def test_normalisation_is_idempotent_for_generated_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence-ledger.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "claim": "Peak-hour queues exceeded the airport target.",
                        "source_title": "Airport operations report",
                        "source_url": "https://airport.example/operations",
                        "source_type": "official airport report",
                        "confidence": "high",
                        "agent_id": "operations-analyst",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            first = normalise_evidence_ledger(path)
            second = normalise_evidence_ledger(path)
            self.assertEqual(first.invalid_records, [])
            self.assertEqual(second.invalid_records, [])
            self.assertEqual(first.records, second.records)
            self.assertTrue(
                first.records[0]["evidence_id"].startswith(
                    "operations-analyst::ev-"
                )
            )
            # A curator-authored map created between normalization passes must
            # continue to resolve against the canonical ledger.
            evidence_map_id = first.records[0]["evidence_id"]
            ledger_ids = {record["evidence_id"] for record in second.records}
            self.assertIn(evidence_map_id, ledger_ids)


if __name__ == "__main__":
    unittest.main()
