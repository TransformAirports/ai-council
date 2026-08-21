from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

import cli.menu as menu


class ClaudeAuthenticationTests(unittest.TestCase):
    def tearDown(self) -> None:
        menu._auth_probe_cache = None

    def test_not_logged_in_probe_is_a_confirmed_authentication_failure(self) -> None:
        result = subprocess.CompletedProcess(
            args=["claude"],
            returncode=0,
            stdout="Not logged in · Please run /login",
            stderr="",
        )
        menu._auth_probe_cache = None
        with (
            patch.dict(menu.os.environ, {}, clear=True),
            patch("cli.menu.shutil.which", return_value="/usr/bin/claude"),
            patch("subprocess.run", return_value=result),
        ):
            ok, message = menu.check_claude_auth(force=True)

        self.assertFalse(ok)
        self.assertIn("claude auth login", message)

    def test_organization_access_denial_requires_key_or_admin(self) -> None:
        result = subprocess.CompletedProcess(
            args=["claude"],
            returncode=1,
            stdout=(
                '{"is_error":true,"api_error_status":403,'
                '"result":"Your organization has disabled Claude subscription '
                'access for Claude Code · Use an Anthropic API key instead"}'
            ),
            stderr="",
        )
        with (
            patch.dict(menu.os.environ, {}, clear=True),
            patch("cli.menu.shutil.which", return_value="/usr/bin/claude"),
            patch("subprocess.run", return_value=result) as runner,
        ):
            ok, message = menu.check_claude_auth(force=True)

        self.assertFalse(ok)
        self.assertIn("ANTHROPIC_API_KEY", message)
        self.assertIn("administrator", message)
        command = runner.call_args.args[0]
        self.assertIn("--max-budget-usd", command)
        self.assertIn("--tools", command)


if __name__ == "__main__":
    unittest.main()
