from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import cli.server as server
from cli.library_lifecycle import LibraryLifecycle, LifecycleSafetyError
from cli.publish import ReportSource


ORIGIN = "http://127.0.0.1:8723"
CLIENT_ID = "library_endpoint_client_12345"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LibraryEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(
            server.app,
            base_url=ORIGIN,
            client=("127.0.0.1", 51000),
        )
        self.previous_task = server._active_task
        self.previous_sink = server._active_sink
        self.previous_owner = server._active_owner
        self.previous_live_clients = dict(server._live_clients)
        self.previous_service = server._library_lifecycle_service
        self.previous_recovery_failure = server._library_recovery_failure
        server._active_task = None
        server._active_sink = None
        server._active_owner = None
        server._live_clients.clear()
        server._library_lifecycle_service = None
        server._set_library_recovery_failure(None)

    def tearDown(self) -> None:
        server._active_task = self.previous_task
        server._active_sink = self.previous_sink
        server._active_owner = self.previous_owner
        server._live_clients.clear()
        server._live_clients.update(self.previous_live_clients)
        server._library_lifecycle_service = self.previous_service
        server._set_library_recovery_failure(self.previous_recovery_failure)
        self.client.close()

    @property
    def headers(self) -> dict[str, str]:
        return {
            "origin": ORIGIN,
            server._SESSION_HEADER: server._SESSION_TOKEN,
            server._CLIENT_HEADER: CLIENT_ID,
        }

    def _fixture(self, root: Path, slug: str = "terminal-choice") -> ReportSource:
        archive = root / "runs" / f"2026-08-21-{slug}"
        final = archive / "stage3" / "final-draft.md"
        office = archive / "stage4" / f"{slug}.docx"
        final.parent.mkdir(parents=True)
        office.parent.mkdir(parents=True)
        final.write_text("# Finished report\n\nA source-checked decision.\n", encoding="utf-8")
        office.write_bytes(b"archived word")
        prompt = f"# Run: Terminal Choice\n\n## Thesis\nA contested claim.\n".encode()
        (archive / "run-prompt.md").write_bytes(prompt)
        (archive / "run-manifest.json").write_text(
            json.dumps(
                {
                    "run": {
                        "slug": slug,
                        "run_prompt_sha256": hashlib.sha256(prompt).hexdigest(),
                        "run_prompt_size": len(prompt),
                    }
                }
            )
        )
        reports = root / "reports"
        reports.mkdir(exist_ok=True)
        (reports / f"{slug}.docx").write_bytes(b"published word")
        (reports / f"{slug}-release-manifest.json").write_text("{}\n")
        prompt_live = root / "prompts" / "runs" / f"{slug}.md"
        prompt_live.parent.mkdir(parents=True, exist_ok=True)
        prompt_live.write_bytes(prompt)
        source_copy = root / "sources" / "runs" / slug / "input.pdf"
        source_copy.parent.mkdir(parents=True, exist_ok=True)
        source_copy.write_bytes(b"source")
        unrelated = root / "reports" / f"{slug}-other.docx"
        unrelated.write_bytes(b"unrelated")
        return ReportSource(slug, archive, office, final, None)

    def test_metadata_edit_delete_preview_and_permanent_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = self._fixture(root)
            immutable = [
                source.final_md,
                source.stage4_docx,
                root / "reports" / f"{source.slug}.docx",
            ]
            before = {path: _sha(path) for path in immutable}

            def discover():
                return [source] if source.final_md and source.final_md.is_file() else []

            with (
                patch.object(server, "REPO_ROOT", root),
                patch("cli.publish.discover_reports", side_effect=discover),
                patch("cli.menu.detect_interrupted_run", return_value=None),
                patch.object(server, "_downloads_for_slug", return_value=[]),
                patch.object(server, "_scope_home_entries", return_value=[]),
                patch.object(server, "_argument_home_entries", return_value=[]),
            ):
                forbidden = self.client.patch(
                    f"/api/library/report/{source.slug}",
                    json={"title": "Board choice"},
                )
                edited = self.client.patch(
                    f"/api/library/report/{source.slug}",
                    headers=self.headers,
                    json={
                        "title": "The Board's Terminal Choice",
                        "summary": "What to decide before concrete is committed.",
                        "tags": ["Board", "Capital"],
                    },
                )
                home = self.client.get("/api/home")
                immutable_unchanged_after_edit = before == {
                    path: _sha(path) for path in immutable
                }
                plan = self.client.post(
                    f"/api/library/report/{source.slug}/delete-plan",
                    headers=self.headers,
                )
                plan_body = plan.json()
                deleted = self.client.request(
                    "DELETE",
                    f"/api/library/report/{source.slug}",
                    headers=self.headers,
                    json={
                        "plan_id": plan_body["plan_id"],
                        "confirmation": plan_body["confirmation"],
                    },
                )
                after_delete = self.client.get("/api/home")
                receipt = deleted.json()["receipt"]

            self.assertEqual(forbidden.status_code, 403)
            self.assertEqual(edited.status_code, 200)
            card = home.json()["archives"][0]
            self.assertEqual(card["title"], "The Board's Terminal Choice")
            self.assertEqual(card["tags"], ["Board", "Capital"])
            self.assertTrue(immutable_unchanged_after_edit)
            self.assertEqual(plan.status_code, 200)
            self.assertGreater(plan_body["file_count"], 0)
            self.assertIn("run_archive", plan_body["groups"])
            self.assertEqual(plan_body["confirmation"], source.slug)
            self.assertTrue(plan_body["permanent"])
            self.assertFalse(plan_body["recoverable"])
            self.assertEqual(deleted.status_code, 200)
            self.assertFalse(receipt["recoverable"])
            self.assertTrue(receipt["permanent"])
            self.assertFalse(receipt["cleanup_pending"])
            self.assertEqual(receipt["reclaimed_bytes"], plan_body["total_bytes"])
            self.assertEqual(after_delete.json()["archives"], [])
            self.assertTrue((root / "reports" / f"{source.slug}-other.docx").is_file())
            self.assertTrue(
                all(not (root / target["path"]).exists() for target in plan_body["targets"])
            )
            self.assertFalse(source.final_md.exists())

    def test_startup_recovery_failure_is_typed_and_home_stays_readable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = self._fixture(root)
            service = LibraryLifecycle(root)
            server._library_lifecycle_service = service

            with (
                patch.object(server, "REPO_ROOT", root),
                patch.object(
                    service,
                    "recover_pending_transactions",
                    side_effect=LifecycleSafetyError("receipt state is ambiguous"),
                ),
                patch("cli.publish.discover_reports", return_value=[source]),
                patch("cli.menu.detect_interrupted_run", return_value=None),
                patch.object(server, "_downloads_for_slug", return_value=[]),
                patch.object(server, "_scope_home_entries", return_value=[]),
                patch.object(server, "_argument_home_entries", return_value=[]),
                TestClient(
                    server.app,
                    base_url=ORIGIN,
                    client=("127.0.0.1", 51001),
                ) as startup_client,
            ):
                home = startup_client.get("/api/home")

            self.assertEqual(home.status_code, 200)
            self.assertEqual(len(home.json()["archives"]), 1)
            warning = home.json()["library_recovery_warning"]
            self.assertEqual(warning["code"], "library_recovery_required")
            self.assertEqual(warning["cause_code"], "library_safety_error")
            self.assertIn("paused", warning["message"])
            self.assertIsInstance(
                server._library_recovery_failure,
                server.LibraryRecoveryFailure,
            )
            self.assertIs(
                server.app.state.library_recovery_failure,
                server._library_recovery_failure,
            )

    def test_recovery_failure_blocks_every_mutation_and_websocket_start(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            live = self._fixture(root, "terminal-choice")
            trashed = self._fixture(root, "restore-choice")
            service = LibraryLifecycle(root)
            terminal_plan = service.create_delete_plan(
                "report", live.slug, client_id=CLIENT_ID
            )
            restore_plan = service.create_delete_plan(
                "report", trashed.slug, client_id=CLIENT_ID
            )
            restore_receipt = service.commit_delete(
                restore_plan.plan_id,
                client_id=CLIENT_ID,
                confirmation=trashed.slug,
            )
            plans_before = set(service._plans)
            server._library_lifecycle_service = service

            def discover():
                return [
                    source
                    for source in (live, trashed)
                    if source.final_md is not None and source.final_md.is_file()
                ]

            with (
                patch.object(server, "REPO_ROOT", root),
                patch.object(
                    service,
                    "recover_pending_transactions",
                    side_effect=LifecycleSafetyError("manual recovery is required"),
                ) as recover,
                patch("cli.publish.discover_reports", side_effect=discover),
                patch("cli.menu.detect_interrupted_run", return_value=None),
                patch.object(server, "_downloads_for_slug", return_value=[]),
                patch.object(server, "_scope_home_entries", return_value=[]),
                patch.object(server, "_argument_home_entries", return_value=[]),
            ):
                edited = self.client.patch(
                    f"/api/library/report/{live.slug}",
                    headers=self.headers,
                    json={"title": "Must not be saved"},
                )
                preview = self.client.post(
                    f"/api/library/report/{live.slug}/delete-plan",
                    headers=self.headers,
                )
                deleted = self.client.request(
                    "DELETE",
                    f"/api/library/report/{live.slug}",
                    headers=self.headers,
                    json={
                        "plan_id": terminal_plan.plan_id,
                        "confirmation": live.slug,
                    },
                )
                restored = self.client.post(
                    f"/api/library/trash/{restore_receipt.receipt_id}/restore",
                    headers=self.headers,
                )
                home = self.client.get("/api/home")

                ws_path = (
                    f"/ws?token={server._SESSION_TOKEN}"
                    f"&client_id={CLIENT_ID}"
                )
                with self.client.websocket_connect(
                    ws_path,
                    headers={"origin": ORIGIN, "host": "127.0.0.1:8723"},
                ) as socket:
                    socket.send_json(
                        {
                            "type": "start",
                            "mode": "new",
                            "session_token": server._SESSION_TOKEN,
                            "client_id": CLIENT_ID,
                        }
                    )
                    ws_error = socket.receive_json()

            for response in (edited, preview, deleted, restored):
                self.assertEqual(response.status_code, 409)
                self.assertEqual(
                    response.json()["code"], "library_recovery_required"
                )
            self.assertGreaterEqual(recover.call_count, 5)
            self.assertEqual(home.status_code, 200)
            self.assertEqual(
                home.json()["library_recovery_warning"]["code"],
                "library_recovery_required",
            )
            self.assertEqual(ws_error["type"], "run_error")
            self.assertEqual(ws_error["status"], 409)
            self.assertEqual(ws_error["code"], "library_recovery_required")
            self.assertIsNone(server._active_task)
            self.assertEqual(set(service._plans), plans_before)
            self.assertTrue((root / "reports" / f"{live.slug}.docx").is_file())
            self.assertFalse(
                (
                    root
                    / ".council-state"
                    / "library"
                    / "metadata"
                    / "report"
                    / f"{live.slug}.json"
                ).exists()
            )
            receipt_dir = root / restore_receipt.trash_path
            self.assertFalse((receipt_dir / "restore-receipt.json").exists())
            self.assertFalse(trashed.final_md.is_file())


if __name__ == "__main__":
    unittest.main()
