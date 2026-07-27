from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cli.artifacts import ArtifactContract, validate_artifact


class ArtifactValidationTests(unittest.TestCase):
    def test_markdown_contract_checks_words_not_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            path.write_text(" ".join(["evidence"] * 25), encoding="utf-8")
            result = validate_artifact(
                path, ArtifactContract("markdown", min_words=20)
            )
            self.assertTrue(result.valid)
            self.assertEqual(result.word_count, 25)
            self.assertIsNotNone(result.sha256)

    def test_unresolved_placeholder_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            path.write_text(
                " ".join(["evidence"] * 25) + "\n{{AIRPORT_NAME}}",
                encoding="utf-8",
            )
            result = validate_artifact(
                path, ArtifactContract("markdown", min_words=20)
            )
            self.assertFalse(result.valid)
            self.assertIn("placeholder", " ".join(result.errors))

    def test_jsonl_contract_reports_bad_line(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text('{"claim": "ok"}\nnot-json\n', encoding="utf-8")
            result = validate_artifact(
                path, ArtifactContract("jsonl", min_records=1)
            )
            self.assertFalse(result.valid)
            self.assertEqual(result.record_count, 1)
            self.assertIn("line 2", " ".join(result.errors))

    def test_jsonl_contract_supports_alternative_source_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.jsonl"
            path.write_text(
                '{"claim":"x","source_title":"Report","source_type":"official",'
                '"confidence":"high","source_path":"sources/report.pdf"}\n',
                encoding="utf-8",
            )
            contract = ArtifactContract(
                "jsonl",
                min_records=1,
                required_keys=(
                    "claim",
                    "source_title",
                    "source_type",
                    "confidence",
                ),
                required_any=(("source_url", "source_path"),),
            )
            self.assertTrue(validate_artifact(path, contract).valid)


if __name__ == "__main__":
    unittest.main()
