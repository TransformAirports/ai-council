"""One unsourced line must not destroy an agent's paid output.

Research agents periodically record a professional-judgment claim they cannot
attribute to a retrievable document. It must stay out of the evidence ledger —
the fact-checker would treat it as sourced — but discarding a whole agent's
work over two lines out of twenty-five has already killed two runs.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from cli.artifacts import validate_artifact
from cli.orchestrator import (
    RESEARCH_EVIDENCE_CONTRACT as CONTRACT,
    _sequester_unsourced_evidence,
)


def _sourced(claim: str) -> dict:
    return {"claim": claim, "source_title": "FAA AC 150/5210-6D",
            "source_type": "regulation", "confidence": "high",
            "source_url": "https://www.faa.gov/x"}


def _judgment(claim: str) -> dict:
    return {"claim": claim, "source_title": "professional judgment",
            "source_type": "professional_judgment", "confidence": "medium"}


class SequesterTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def _write(self, records: list[dict]) -> Path:
        p = self.dir / "agent-evidence.jsonl"
        p.write_text("".join(json.dumps(r) + "\n" for r in records), encoding="utf-8")
        return p

    def test_judgment_records_move_aside_and_the_file_then_validates(self) -> None:
        p = self._write([_sourced("a"), _judgment("ARFF lead times run 24-30 months"),
                         _sourced("b"), _judgment("hiring runs 12-18 months")])
        self.assertFalse(validate_artifact(p, CONTRACT).valid)

        moved = _sequester_unsourced_evidence(p, CONTRACT)

        self.assertEqual([n for n, _ in moved], [2, 4])
        self.assertTrue(validate_artifact(p, CONTRACT).valid,
                        "the surviving evidence file must satisfy the contract")
        kept = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertEqual([r["claim"] for r in kept], ["a", "b"])

    def test_nothing_is_lost__the_moved_records_land_in_a_sidecar(self) -> None:
        p = self._write([_sourced("a"), _judgment("ARFF lead times run 24-30 months")])
        _sequester_unsourced_evidence(p, CONTRACT)
        sidecar = p.with_suffix(p.suffix + ".unsourced.jsonl")
        self.assertTrue(sidecar.is_file())
        held = [json.loads(l) for l in sidecar.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertEqual([r["claim"] for r in held], ["ARFF lead times run 24-30 months"])

    def test_an_all_unsourced_file_is_a_real_failure_and_is_left_alone(self) -> None:
        p = self._write([_judgment("x"), _judgment("y")])
        self.assertEqual(_sequester_unsourced_evidence(p, CONTRACT), [])
        self.assertFalse(validate_artifact(p, CONTRACT).valid)
        self.assertFalse(p.with_suffix(p.suffix + ".unsourced.jsonl").exists())

    def test_structural_defects_still_fail_loudly(self) -> None:
        broken = {"claim": "no source_title or confidence keys at all"}
        p = self._write([_sourced("a"), broken])
        self.assertEqual(_sequester_unsourced_evidence(p, CONTRACT), [],
                         "a malformed record is a defect, not a judgment call")
        self.assertFalse(validate_artifact(p, CONTRACT).valid)

    def test_a_fully_sourced_file_is_untouched(self) -> None:
        p = self._write([_sourced("a"), _sourced("b")])
        before = p.read_text(encoding="utf-8")
        self.assertEqual(_sequester_unsourced_evidence(p, CONTRACT), [])
        self.assertEqual(p.read_text(encoding="utf-8"), before)

    def test_offline_citations_are_kept_not_sequestered(self) -> None:
        standard = {"claim": "STI >= 0.50", "source_title": "NFPA 72 (2022)",
                    "source_type": "technical_standard", "confidence": "high",
                    "source_citation": "NFPA 72, 2022 ed.",
                    "page_or_section": "Ch.18 §18.4.11.2"}
        p = self._write([_sourced("a"), standard])
        self.assertEqual(_sequester_unsourced_evidence(p, CONTRACT), [])
        self.assertTrue(validate_artifact(p, CONTRACT).valid)
