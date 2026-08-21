from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import cli.server as server
from cli.publish import ReportSource, resolve_report_prompt


ORIGIN = "http://127.0.0.1:8723"
CLIENT_ID = "library_client_123456789"


def _source(root: Path, slug: str = "terminal-choice") -> ReportSource:
    archive = root / "runs" / f"2026-08-21-{slug}"
    (archive / "stage3").mkdir(parents=True)
    (archive / "stage4").mkdir()
    final = archive / "stage3" / "final-draft.md"
    final.write_text("# Finished report\n", encoding="utf-8")
    office = archive / "stage4" / f"{slug}.docx"
    office.write_bytes(b"office")
    return ReportSource(slug, archive, office, final, None)


def _write_verified_prompt(source: ReportSource, text: str) -> Path:
    prompt = source.archive_dir / "run-prompt.md"
    raw = text.encode("utf-8")
    prompt.write_bytes(raw)
    (source.archive_dir / "run-manifest.json").write_text(
        json.dumps(
            {
                "run": {
                    "slug": source.slug,
                    "run_prompt_sha256": hashlib.sha256(raw).hexdigest(),
                    "run_prompt_size": len(raw),
                }
            }
        ),
        encoding="utf-8",
    )
    return prompt


class PromptProvenanceTests(unittest.TestCase):
    def test_exact_archive_is_verified_and_tampering_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = _source(Path(directory))
            prompt = _write_verified_prompt(source, "# Run: Terminal Choice\n")

            record = resolve_report_prompt(source)
            self.assertTrue(record.available)
            self.assertTrue(record.exact)
            self.assertEqual(record.provenance, "verified_archive")

            prompt.write_text("# Changed after the run\n", encoding="utf-8")
            tampered = resolve_report_prompt(source)
            self.assertFalse(tampered.available)
            self.assertEqual(tampered.provenance, "integrity_failure")

    def test_live_legacy_prompt_is_available_but_never_called_exact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = _source(root)
            prompts = root / "prompts" / "runs"
            prompts.mkdir(parents=True)
            (prompts / f"{source.slug}.md").write_text(
                "# Run: Mutable legacy candidate\n", encoding="utf-8"
            )

            record = resolve_report_prompt(source, run_prompts_dir=prompts)
            self.assertTrue(record.available)
            self.assertFalse(record.exact)
            self.assertEqual(record.provenance, "legacy_live_candidate")
            self.assertIn("may have changed", record.notice)

    def test_archived_prompt_symlink_is_rejected_without_live_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = _source(root)
            outside = root / "outside.md"
            outside.write_text("secret", encoding="utf-8")
            (source.archive_dir / "run-prompt.md").symlink_to(outside)
            prompts = root / "prompts" / "runs"
            prompts.mkdir(parents=True)
            (prompts / f"{source.slug}.md").write_text("fallback", encoding="utf-8")

            record = resolve_report_prompt(source, run_prompts_dir=prompts)
            self.assertFalse(record.available)
            self.assertEqual(record.provenance, "integrity_failure")


class LibraryPromptEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(
            server.app,
            base_url=ORIGIN,
            client=("127.0.0.1", 51000),
        )

    def tearDown(self) -> None:
        self.client.close()

    @property
    def auth_headers(self) -> dict[str, str]:
        return {
            "origin": ORIGIN,
            server._SESSION_HEADER: server._SESSION_TOKEN,
            server._CLIENT_HEADER: CLIENT_ID,
        }

    def test_prompt_endpoint_requires_session_and_home_exposes_only_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = _source(Path(directory))
            sentinel = "<script>never render me</script>"
            _write_verified_prompt(source, f"# Run: Terminal Choice\n\n{sentinel}\n")
            with (
                patch("cli.publish.discover_reports", return_value=[source]),
                patch("cli.menu.detect_interrupted_run", return_value=None),
            ):
                forbidden = self.client.post(
                    f"/api/library/report/{source.slug}/prompt"
                )
                response = self.client.post(
                    f"/api/library/report/{source.slug}/prompt",
                    headers=self.auth_headers,
                )
                home = self.client.get("/api/home")

            self.assertEqual(forbidden.status_code, 403)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["markdown"].splitlines()[-1], sentinel)
            self.assertTrue(response.json()["exact"])
            prompt_metadata = home.json()["archives"][0]["prompt"]
            self.assertTrue(prompt_metadata["available"])
            self.assertTrue(prompt_metadata["exact"])
            self.assertNotIn(sentinel, home.text)


class AgentCatalogEndpointTests(unittest.TestCase):
    def test_api_returns_complete_unique_browsable_roster(self) -> None:
        with TestClient(server.app, base_url=ORIGIN) as client:
            response = client.get("/api/agents")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        research = [member for group in payload["groups"] for member in group["members"]]
        process = payload["process"]
        all_names = [item["name"] for item in research + process]
        self.assertEqual(len(research), 38)
        self.assertEqual(len(process), 16)
        self.assertEqual(len(all_names), len(set(all_names)))
        self.assertTrue(all(item["display"] and item["description"] for item in research + process))


if __name__ == "__main__":
    unittest.main()
