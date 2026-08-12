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
        self.assertIn("claude login", message)


if __name__ == "__main__":
    unittest.main()
