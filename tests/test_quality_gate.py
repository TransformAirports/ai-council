from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cli.evidence import bind_claim_lineage_to_draft
from cli.quality_gate import (
    PublicationQualityError,
    inspect_publication_markdown,
    publication_word_count,
    resolve_word_count_bounds,
    run_publication_quality_gate,
)


class QualityGateTests(unittest.TestCase):
    @staticmethod
    def _write_ledger(root: Path) -> Path:
        ledger = root / "evidence-ledger.jsonl"
        ledger.write_text(
            '{"evidence_id":"ev-1","claim":"The airport invested $4 million '
            'in 2024.",'
            '"source_title":"Financial statements",'
            '"source_url":"https://airport.example/financials",'
            '"source_type":"audited_financial","is_primary":true,'
            '"confidence":"high","agent_id":"alpha"}\n',
            encoding="utf-8",
        )
        return ledger

    def test_clean_cited_draft_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The airport invested $4 million in 2024.[^1]\n\n"
                + " ".join(["Operational context matters."] * 150)
                + "\n\n[^1]: Airport audited financial statements, p. 14.\n",
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"The airport invested $4 million '
                'in 2024.","citation":"Airport audited financial statements, '
                'p. 14.","footnote_id":"1","evidence_ids":["ev-1"],'
                '"retained":true,"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(
                final_draft=final, output_path=lineage
            )
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=self._write_ledger(root),
                claim_lineage_path=lineage,
            )
            self.assertTrue(payload["passed"])

    def test_word_count_contract_uses_run_prompt_range_before_summary_target(
        self,
    ) -> None:
        self.assertEqual(
            resolve_word_count_bounds(
                "report",
                "8,000–10,000 words for the report; ~1,100-word executive summary.",
            ),
            (8_000, 10_000),
        )
        self.assertEqual(
            resolve_word_count_bounds("brief", ""),
            (700, 1_000),
        )

    def test_reader_word_count_excludes_footnote_definitions(self) -> None:
        text = (
            "# Decision\n\nAuthorize the controlled pilot now.[^1]\n\n"
            "[^1]: A very long citation definition with words that do not count.\n"
            "    An indented citation continuation does not count either."
        )
        self.assertEqual(publication_word_count(text), 6)

    def test_final_word_count_outside_run_contract_blocks_publication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The airport invested $4 million in 2024.[^1]\n\n"
                + " ".join(["Operational context matters."] * 150)
                + "\n\n[^1]: Airport audited financial statements, p. 14.\n",
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"The airport invested $4 million '
                'in 2024.","citation":"Airport audited financial statements, '
                'p. 14.","footnote_id":"1","evidence_ids":["ev-1"],'
                '"retained":true,"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(final_draft=final, output_path=lineage)
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=self._write_ledger(root),
                claim_lineage_path=lineage,
                output_format="brief",
                length_instruction="A 700–1,000-word brief.",
                raise_on_failure=False,
            )

        self.assertFalse(payload["passed"])
        self.assertEqual(
            payload["word_count_bounds"],
            {"minimum": 700, "maximum": 1_000},
        )
        self.assertIn(
            "word_count_out_of_range",
            {issue["code"] for issue in payload["issues"]},
        )

    def test_internal_source_tag_blocks_publication(self) -> None:
        issues = inspect_publication_markdown(
            "The result is clear. [Source: operations-analyst-brief]"
        )
        self.assertTrue(
            any(issue.code == "internal_source_tag" for issue in issues)
        )

    def test_named_footnote_is_rejected_before_word_production(self) -> None:
        issues = inspect_publication_markdown(
            "The finding is supported.[^FAA]\n\n[^FAA]: FAA report."
        )
        self.assertTrue(
            any(issue.code == "nonnumeric_footnote_label" for issue in issues)
        )

    def test_orphan_footnote_blocks_publication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                + " ".join(["Context"] * 260)
                + "\n\n[^1]: Unused source.\n",
                encoding="utf-8",
            )
            with self.assertRaises(PublicationQualityError):
                run_publication_quality_gate(
                    final_draft=final,
                    report_path=root / "quality-gate.json",
                    evidence_ledger_path=self._write_ledger(root),
                )

    def test_unverified_lineage_blocks_publication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The airport invested $4 million in 2024.[^1]\n\n"
                + " ".join(["Operational context matters."] * 150)
                + "\n\n[^1]: Airport financial statements.\n",
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"Investment","citation":"Airport '
                'financial statements","footnote_id":"1",'
                '"evidence_ids":["ev-1"],"retained":true,'
                '"verification_status":"unverified",'
                '"primary_source_checked":false}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(
                final_draft=final, output_path=lineage
            )
            with self.assertRaises(PublicationQualityError):
                run_publication_quality_gate(
                    final_draft=final,
                    report_path=root / "quality-gate.json",
                    evidence_ledger_path=self._write_ledger(root),
                    claim_lineage_path=lineage,
                )

    def test_unknown_evidence_reference_blocks_publication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The airport invested $4 million in 2024.[^1]\n\n"
                + " ".join(["Operational context matters."] * 260)
                + "\n\n[^1]: Airport financial statements.\n",
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"Investment","citation":"Airport '
                'financial statements","footnote_id":"1",'
                '"evidence_ids":["E-DOES-NOT-EXIST"],"retained":true,'
                '"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(
                final_draft=final, output_path=lineage
            )
            with self.assertRaises(PublicationQualityError):
                run_publication_quality_gate(
                    final_draft=final,
                    report_path=root / "quality-gate.json",
                    evidence_ledger_path=self._write_ledger(root),
                    claim_lineage_path=lineage,
                )

    def test_unrelated_lineage_claim_and_citation_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The airport invested $4 million in 2024.[^1]\n\n"
                + " ".join(["Operational context matters."] * 260)
                + "\n\n[^1]: Airport audited financial statements, p. 14.\n",
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"Passenger satisfaction rose",'
                '"citation":"An unrelated press release","footnote_id":"1",'
                '"evidence_ids":["ev-1"],"retained":true,'
                '"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(final_draft=final, output_path=lineage)
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=self._write_ledger(root),
                claim_lineage_path=lineage,
                raise_on_failure=False,
            )

        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("lineage_claim_not_in_draft", codes)
        self.assertIn("lineage_citation_mismatch", codes)
        self.assertIn("stale_claim_lineage", codes)

    def test_each_numeric_sentence_needs_its_own_footnote(self) -> None:
        issues = inspect_publication_markdown(
            "Traffic grew 12 percent.[^1] The project cost $4 million in 2024.\n\n"
            "[^1]: Airport traffic report."
        )
        numeric_errors = [
            issue
            for issue in issues
            if issue.code == "numeric_claims_without_footnotes"
        ]
        self.assertEqual(len(numeric_errors), 1)
        self.assertEqual(numeric_errors[0].count, 1)

    def test_abbreviations_do_not_break_cited_sentence_localization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "At 6 a.m. the rule in 49 U.S.C. 47107 protects U.S. airport "
                "operations.[^1]\n\n"
                "[^1]: Airport operations statute.\n",
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"At 6 a.m. the rule in 49 '
                'U.S.C. 47107 protects U.S. airport operations.",'
                '"citation":"Airport operations statute.","footnote_id":"1",'
                '"evidence_ids":["ev-1"],"retained":true,'
                '"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )

            records = bind_claim_lineage_to_draft(
                final_draft=final,
                output_path=lineage,
            )
            issues = inspect_publication_markdown(final.read_text(encoding="utf-8"))

        self.assertIn("draft_sha256", records[0])
        self.assertNotIn(
            "numeric_claims_without_footnotes",
            {issue.code for issue in issues},
        )

    def test_airport_numeric_units_require_citations(self) -> None:
        claims = (
            "Traffic grew 12 percent.",
            "Throughput rose 12 percentage points.",
            "The staffing ratio is 3:1.",
            "The terminal has 45 checkpoints.",
            "The airport handled 12 million passengers.",
            "The average walk is 6.2 minutes.",
            "Demand is 1.8x baseline.",
            "The spread widened 250 basis points.",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                issues = inspect_publication_markdown(claim)
                self.assertTrue(
                    any(
                        issue.code == "numeric_claims_without_footnotes"
                        for issue in issues
                    )
                )

    def test_swapped_claim_footnotes_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The airport invested $4 million in 2024.[^1] "
                "Traffic reached 12 million passengers.[^2]\n\n"
                + " ".join(["Operational context matters."] * 260)
                + "\n\n[^1]: Airport audited financial statements, p. 14."
                "\n[^2]: Airport traffic report, p. 8.\n",
                encoding="utf-8",
            )
            ledger = root / "evidence-ledger.jsonl"
            ledger.write_text(
                '{"evidence_id":"ev-1","claim":"Investment",'
                '"source_title":"Airport audited financial statements",'
                '"source_url":"https://airport.example/financials",'
                '"source_type":"audited_financial","is_primary":true,'
                '"confidence":"high","agent_id":"alpha"}\n'
                '{"evidence_id":"ev-2","claim":"Traffic",'
                '"source_title":"Airport traffic report",'
                '"source_url":"https://airport.example/traffic",'
                '"source_type":"official_report","is_primary":true,'
                '"confidence":"high","agent_id":"alpha"}\n',
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"The airport invested $4 million '
                'in 2024.","citation":"Airport traffic report, p. 8.",'
                '"footnote_id":"2","evidence_ids":["ev-2"],"retained":true,'
                '"verification_status":"verified","primary_source_checked":true}\n'
                '{"claim_id":"claim-2","claim":"Traffic reached 12 million '
                'passengers.","citation":"Airport audited financial statements, '
                'p. 14.","footnote_id":"1","evidence_ids":["ev-1"],'
                '"retained":true,"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(final_draft=final, output_path=lineage)
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=ledger,
                claim_lineage_path=lineage,
                raise_on_failure=False,
            )

        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("lineage_claim_footnote_mismatch", codes)

    def test_known_but_unrelated_evidence_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The airport invested $4 million in 2024.[^1]\n\n"
                + " ".join(["Operational context matters."] * 260)
                + "\n\n[^1]: Airport audited financial statements, p. 14.\n",
                encoding="utf-8",
            )
            ledger = root / "evidence-ledger.jsonl"
            ledger.write_text(
                '{"evidence_id":"ev-unrelated","claim":"Weather delays",'
                '"source_title":"National weather report",'
                '"source_url":"https://weather.example/report",'
                '"source_type":"official_report","is_primary":true,'
                '"confidence":"high","agent_id":"alpha"}\n',
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"The airport invested $4 million '
                'in 2024.","citation":"Airport audited financial statements, '
                'p. 14.","footnote_id":"1","evidence_ids":["ev-unrelated"],'
                '"retained":true,"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(final_draft=final, output_path=lineage)
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=ledger,
                claim_lineage_path=lineage,
                raise_on_failure=False,
            )

        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("claim_evidence_citation_mismatch", codes)

    def test_excluded_unverified_claim_can_remain_in_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The supported recommendation is to run a pilot.[^1]\n\n"
                + " ".join(["Operational context matters."] * 150)
                + "\n\n[^1]: Airport pilot authorization, p. 2.\n",
                encoding="utf-8",
            )
            ledger = root / "evidence-ledger.jsonl"
            ledger.write_text(
                '{"evidence_id":"ev-1","claim":"The supported recommendation '
                'is to run a pilot.",'
                '"source_title":"Airport pilot authorization",'
                '"source_url":"https://airport.example/pilot",'
                '"source_type":"official_report","is_primary":true,'
                '"confidence":"high","agent_id":"alpha"}\n',
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"The supported recommendation '
                'is to run a pilot.","citation":"Airport pilot authorization, '
                'p. 2.","footnote_id":"1","evidence_ids":["ev-1"],'
                '"retained":true,"verification_status":"verified",'
                '"primary_source_checked":true}\n'
                '{"claim_id":"claim-2","claim":"The terminal will save $9 '
                'million.","citation":"","footnote_id":null,"evidence_ids":[],'
                '"retained":false,"verification_status":"unverified",'
                '"primary_source_checked":false}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(final_draft=final, output_path=lineage)
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=ledger,
                claim_lineage_path=lineage,
            )

        self.assertTrue(payload["passed"])

    def test_excluded_only_lineage_cannot_release_substantive_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                + " ".join(["Operational context matters."] * 260),
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"An excluded assertion.",'
                '"citation":"","footnote_id":null,"evidence_ids":[],'
                '"retained":false,"verification_status":"unverified",'
                '"primary_source_checked":false}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(final_draft=final, output_path=lineage)
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=self._write_ledger(root),
                claim_lineage_path=lineage,
                raise_on_failure=False,
            )

        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("no_retained_verified_claims", codes)
        self.assertIn("insufficient_citation_coverage", codes)

    def test_same_source_unrelated_evidence_claim_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The airport invested $4 million in 2024.[^1]\n\n"
                + " ".join(["Operational context matters."] * 260)
                + "\n\n[^1]: Airport annual report, p. 14.\n",
                encoding="utf-8",
            )
            ledger = root / "evidence-ledger.jsonl"
            ledger.write_text(
                '{"evidence_id":"ev-1","claim":"Weather delays increased.",'
                '"source_title":"Airport annual report",'
                '"source_url":"https://airport.example/annual",'
                '"source_type":"official_report","is_primary":true,'
                '"confidence":"high","agent_id":"alpha"}\n',
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"The airport invested $4 million '
                'in 2024.","citation":"Airport annual report, p. 14.",'
                '"footnote_id":"1","evidence_ids":["ev-1"],"retained":true,'
                '"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(final_draft=final, output_path=lineage)
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=ledger,
                claim_lineage_path=lineage,
                raise_on_failure=False,
            )

        codes = {issue["code"] for issue in payload["issues"]}
        self.assertIn("claim_not_supported_by_evidence_record", codes)

    def test_compound_claim_can_be_supported_collectively(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            final = root / "final-draft.md"
            final.write_text(
                "# Decision\n\n"
                "The runway is 9,400 feet long and its approach lights extend "
                "2,400 feet.[^1]\n\n"
                "[^1]: Runway record; FAA approach-lighting specification.\n",
                encoding="utf-8",
            )
            ledger = root / "evidence-ledger.jsonl"
            ledger.write_text(
                '{"evidence_id":"ev-runway","claim":"The runway is 9,400 '
                'feet long.","source_title":"Runway record",'
                '"is_primary":true}\n'
                '{"evidence_id":"ev-lights","claim":"The approach lights '
                'extend 2,400 feet.","source_title":"FAA approach-lighting '
                'specification","is_primary":true}\n',
                encoding="utf-8",
            )
            lineage = root / "claim-lineage.jsonl"
            lineage.write_text(
                '{"claim_id":"claim-1","claim":"The runway is 9,400 feet '
                'long and its approach lights extend 2,400 feet.",'
                '"citation":"Runway record; FAA approach-lighting '
                'specification.","footnote_id":"1",'
                '"evidence_ids":["ev-runway","ev-lights"],"retained":true,'
                '"verification_status":"verified",'
                '"primary_source_checked":true}\n',
                encoding="utf-8",
            )
            bind_claim_lineage_to_draft(final_draft=final, output_path=lineage)
            payload = run_publication_quality_gate(
                final_draft=final,
                report_path=root / "quality-gate.json",
                evidence_ledger_path=ledger,
                claim_lineage_path=lineage,
                raise_on_failure=False,
            )

        codes = {issue["code"] for issue in payload["issues"]}
        self.assertNotIn("claim_not_supported_by_evidence_record", codes)
        self.assertNotIn("claim_evidence_citation_mismatch", codes)


if __name__ == "__main__":
    unittest.main()
