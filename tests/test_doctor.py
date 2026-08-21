from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from rich.console import Console

from cli.doctor import collect_doctor_checks, render_doctor


class DoctorTests(unittest.TestCase):
    def test_ready_machine_passes_without_exposing_credentials(self) -> None:
        paths = {
            "claude": "/usr/local/bin/claude",
            "soffice": "/Applications/LibreOffice/soffice",
            "pdftoppm": "/usr/local/bin/pdftoppm",
        }

        def which(name: str) -> str | None:
            return paths.get(name)

        def runner(*args, **kwargs):
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps({"loggedIn": True, "authMethod": "claude.ai"}),
                stderr="",
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("outputs", "reports", "runs"):
                (root / name).mkdir()
            (root / ".env").write_text("ANTHROPIC_API_KEY=secret-value\n")
            checks = collect_doctor_checks(
                root,
                environment={"OPENAI_API_KEY": "also-secret"},
                which=which,
                runner=runner,
                disk_usage=lambda _: SimpleNamespace(free=8 * 1024 ** 3),
                python_version=(3, 12, 2),
            )

        self.assertFalse([check for check in checks if check.required and not check.ok])
        console = Console(record=True, width=120)
        render_doctor(checks, console=console)
        rendered = console.export_text()
        self.assertNotIn("secret-value", rendered)
        self.assertNotIn("also-secret", rendered)
        self.assertIn("Claude authentication", rendered)

    def test_missing_renderers_old_python_auth_disk_and_permissions_are_blockers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("outputs", "reports", "runs"):
                (root / name).mkdir()
            real_access = os.access

            def access(path, mode):
                return False if Path(path).name == "outputs" else real_access(path, mode)

            with patch("cli.doctor.os.access", side_effect=access):
                checks = collect_doctor_checks(
                    root,
                    environment={},
                    which=lambda _: None,
                    runner=lambda *args, **kwargs: SimpleNamespace(
                        returncode=1, stdout="{}", stderr=""
                    ),
                    disk_usage=lambda _: SimpleNamespace(free=128 * 1024 ** 2),
                    python_version=(3, 10, 14),
                )

        failed = {check.key: check for check in checks if check.required and not check.ok}
        self.assertTrue(
            {"python", "claude-cli", "claude-auth", "libreoffice", "poppler", "workspace", "disk"}
            .issubset(failed)
        )
        self.assertIn("brew install poppler", failed["poppler"].fix)
        self.assertIn("claude auth login", failed["claude-auth"].fix)

    def test_api_key_without_claude_binary_is_configured_but_unverified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checks = collect_doctor_checks(
                Path(directory),
                environment={"ANTHROPIC_API_KEY": "x"},
                which=lambda name: "/usr/bin/soffice" if name == "soffice" else "/usr/bin/pdftoppm" if name == "pdftoppm" else None,
                disk_usage=lambda _: SimpleNamespace(free=2 * 1024 ** 3),
                python_version=(3, 11, 9),
            )
        by_key = {check.key: check for check in checks}
        self.assertFalse(by_key["claude-auth"].ok)
        self.assertTrue(by_key["claude-auth"].required)
        self.assertTrue(by_key["claude-cli"].required)
        self.assertIn("configured", by_key["claude-auth"].detail)
        self.assertIn("unverified", by_key["claude-auth"].detail)
        self.assertNotIn("ANTHROPIC_API_KEY=x", by_key["claude-auth"].detail)

    def test_api_key_still_requires_cli_auth_status_verification(self) -> None:
        calls: list[tuple[object, ...]] = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=1, stdout="{}", stderr="")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checks = collect_doctor_checks(
                root,
                environment={"ANTHROPIC_API_KEY": "x"},
                which=lambda name: f"/usr/bin/{name}",
                runner=runner,
                disk_usage=lambda _: SimpleNamespace(free=2 * 1024 ** 3),
                python_version=(3, 11, 9),
            )
        by_key = {check.key: check for check in checks}
        self.assertFalse(by_key["claude-auth"].ok)
        self.assertEqual(calls[0][0], ["/usr/bin/claude", "auth", "status", "--json"])

    def test_doctor_reports_malformed_config_without_changing_its_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "council.toml"
            config_path.write_bytes(b"[models\ncontext = 'opus'\n")
            before = config_path.read_bytes()
            checks = collect_doctor_checks(
                root,
                environment={},
                which=lambda name: f"/usr/bin/{name}",
                runner=lambda *args, **kwargs: SimpleNamespace(
                    returncode=0,
                    stdout=json.dumps({"loggedIn": True, "authMethod": "claude.ai"}),
                    stderr="",
                ),
                disk_usage=lambda _: SimpleNamespace(free=2 * 1024 ** 3),
                python_version=(3, 11, 9),
            )
            after = config_path.read_bytes()

        model_check = {check.key: check for check in checks}["models"]
        self.assertFalse(model_check.ok)
        self.assertTrue(model_check.required)
        self.assertIn("could not be parsed", model_check.detail)
        self.assertEqual(after, before)

    def test_doctor_reports_blocked_model_without_rewriting_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config_path = root / "council.toml"
            config_path.write_text(
                '[models]\ncontext = "claude-opus-5-0"\n',
                encoding="utf-8",
            )
            before = config_path.read_bytes()
            checks = collect_doctor_checks(
                root,
                environment={},
                which=lambda name: f"/usr/bin/{name}",
                runner=lambda *args, **kwargs: SimpleNamespace(
                    returncode=0,
                    stdout=json.dumps({"loggedIn": True, "authMethod": "claude.ai"}),
                    stderr="",
                ),
                disk_usage=lambda _: SimpleNamespace(free=2 * 1024 ** 3),
                python_version=(3, 11, 9),
            )
            after = config_path.read_bytes()

        model_check = {check.key: check for check in checks}["models"]
        self.assertFalse(model_check.ok)
        self.assertIn("context: claude-opus-5-0 → opus", model_check.detail)
        self.assertEqual(after, before)

    def test_cli_doctor_dispatches_before_the_interactive_menu(self) -> None:
        from cli import __main__ as command

        with patch("cli.doctor.run_doctor", return_value=7) as run:
            status = command.main(["--doctor"])
        self.assertEqual(status, 7)
        run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
