from __future__ import annotations

import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from cli.codex_subscription import (
    CODEX_EVENT_STREAM_LIMIT_BYTES,
    CodexSubscriptionError,
    CodexSubscriptionStatus,
    codex_subscription_status,
    run_codex_exec,
)


class _AsyncLines:
    def __init__(self, lines: list[bytes]) -> None:
        self._lines = iter(lines)

    def __aiter__(self):
        return self

    async def __anext__(self) -> bytes:
        try:
            return next(self._lines)
        except StopIteration as exc:
            raise StopAsyncIteration from exc


class _Stdin:
    def __init__(self) -> None:
        self.value = b""
        self.closed = False

    def write(self, value: bytes) -> None:
        self.value += value

    async def drain(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True


class _Stderr:
    async def read(self) -> bytes:
        return b""


class _Process:
    def __init__(self, *, include_final_text: bool = True) -> None:
        events = [
            {"type": "turn.started"},
            {
                "type": "item.started",
                "item": {"type": "web_search", "query": "airport primary source"},
            },
            {
                "type": "turn.completed",
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 60,
                    "output_tokens": 25,
                    "reasoning_output_tokens": 5,
                },
            },
        ]
        if include_final_text:
            events.insert(
                2,
                {
                    "type": "item.completed",
                    "item": {
                        "type": "agent_message",
                        "text": '{"answer":"done"}',
                    },
                },
            )
        self.stdin = _Stdin()
        self.stdout = _AsyncLines(
            [(json.dumps(event) + "\n").encode("utf-8") for event in events]
        )
        self.stderr = _Stderr()
        self.returncode = 0

    async def wait(self) -> int:
        return self.returncode

    def terminate(self) -> None:
        self.returncode = -15

    def kill(self) -> None:
        self.returncode = -9


class CodexSubscriptionTests(unittest.TestCase):
    def test_status_requires_chatgpt_auth_not_an_api_key_session(self) -> None:
        chatgpt = codex_subscription_status(
            which=lambda _: "/usr/bin/codex",
            runner=lambda *args, **kwargs: SimpleNamespace(
                returncode=0,
                stdout="Logged in using ChatGPT",
                stderr="",
            ),
            environment={"OPENAI_API_KEY": "not-used"},
        )
        api_key = codex_subscription_status(
            which=lambda _: "/usr/bin/codex",
            runner=lambda *args, **kwargs: SimpleNamespace(
                returncode=0,
                stdout="Logged in using an API key",
                stderr="",
            ),
        )

        self.assertTrue(chatgpt.authenticated)
        self.assertFalse(api_key.authenticated)

    def test_exec_reuses_subscription_and_strips_api_keys(self) -> None:
        async def exercise() -> None:
            captured: dict[str, object] = {}
            process = _Process()

            async def factory(*command, **kwargs):
                captured["command"] = command
                captured["env"] = kwargs["env"]
                captured["limit"] = kwargs["limit"]
                return process

            tools: list[tuple[str, str]] = []

            async def on_tool(name: str, target: str) -> None:
                tools.append((name, target))

            with tempfile.TemporaryDirectory() as directory:
                with (
                    patch(
                        "cli.codex_subscription.codex_subscription_status",
                        return_value=CodexSubscriptionStatus(
                            available=True,
                            authenticated=True,
                            executable="/usr/bin/codex",
                            detail="ready",
                        ),
                    ),
                    patch(
                        "cli.codex_subscription.asyncio.create_subprocess_exec",
                        new=factory,
                    ),
                    patch.dict(
                        os.environ,
                        {
                            "OPENAI_API_KEY": "secret-openai",
                            "CODEX_API_KEY": "secret-codex",
                            "ANTHROPIC_API_KEY": "secret-anthropic",
                        },
                    ),
                ):
                    result = await run_codex_exec(
                        prompt="Produce the commissioned artifact.",
                        model="gpt-5.6-sol",
                        execution_cwd=Path(directory),
                        sandbox="workspace-write",
                        on_tool=on_tool,
                        skip_git_repo_check=True,
                    )

            command = tuple(str(value) for value in captured["command"])
            environment = captured["env"]
            self.assertIn("gpt-5.6-sol", command)
            self.assertIn("--ephemeral", command)
            self.assertIn("--ignore-user-config", command)
            self.assertNotIn("OPENAI_API_KEY", environment)
            self.assertNotIn("CODEX_API_KEY", environment)
            self.assertNotIn("ANTHROPIC_API_KEY", environment)
            self.assertEqual(captured["limit"], CODEX_EVENT_STREAM_LIMIT_BYTES)
            self.assertEqual(process.stdin.value, b"Produce the commissioned artifact.")
            self.assertTrue(process.stdin.closed)
            self.assertEqual(result.final_text, '{"answer":"done"}')
            self.assertEqual(result.input_tokens, 100)
            self.assertEqual(result.cached_input_tokens, 60)
            self.assertEqual(result.output_tokens, 25)
            self.assertEqual(result.reasoning_output_tokens, 5)
            self.assertEqual(result.tool_calls, 1)
            self.assertEqual(tools, [("web_search", "airport primary source")])

        asyncio.run(exercise())

    def test_workspace_role_can_defer_success_to_artifact_validation(self) -> None:
        async def exercise() -> None:
            process = _Process(include_final_text=False)

            async def factory(*command, **kwargs):
                del command, kwargs
                return process

            with tempfile.TemporaryDirectory() as directory:
                with (
                    patch(
                        "cli.codex_subscription.codex_subscription_status",
                        return_value=CodexSubscriptionStatus(
                            available=True,
                            authenticated=True,
                            executable="/usr/bin/codex",
                            detail="ready",
                        ),
                    ),
                    patch(
                        "cli.codex_subscription.asyncio.create_subprocess_exec",
                        new=factory,
                    ),
                ):
                    result = await run_codex_exec(
                        prompt="Write the commissioned file.",
                        model="gpt-5.6-sol",
                        execution_cwd=Path(directory),
                        sandbox="workspace-write",
                        require_final_text=False,
                    )

            self.assertEqual(result.final_text, "")
            self.assertEqual(result.tool_calls, 1)
            self.assertEqual(result.turns, 1)

        asyncio.run(exercise())

    def test_text_caller_still_requires_a_final_response(self) -> None:
        async def exercise() -> None:
            process = _Process(include_final_text=False)

            async def factory(*command, **kwargs):
                del command, kwargs
                return process

            with tempfile.TemporaryDirectory() as directory:
                with (
                    patch(
                        "cli.codex_subscription.codex_subscription_status",
                        return_value=CodexSubscriptionStatus(
                            available=True,
                            authenticated=True,
                            executable="/usr/bin/codex",
                            detail="ready",
                        ),
                    ),
                    patch(
                        "cli.codex_subscription.asyncio.create_subprocess_exec",
                        new=factory,
                    ),
                ):
                    with self.assertRaisesRegex(
                        CodexSubscriptionError, "without a final response"
                    ):
                        await run_codex_exec(
                            prompt="Return structured text.",
                            model="gpt-5.6-sol",
                            execution_cwd=Path(directory),
                            sandbox="read-only",
                        )

        asyncio.run(exercise())

    def test_exec_accepts_a_json_event_larger_than_asyncio_default(self) -> None:
        async def exercise() -> None:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                executable = root / "fake-codex"
                executable.write_text(
                    "#!/usr/bin/env python3\n"
                    "import json, sys\n"
                    "sys.stdin.read()\n"
                    "print(json.dumps({'type': 'turn.started'}), flush=True)\n"
                    "print(json.dumps({'type': 'item.completed', 'item': "
                    "{'type': 'agent_message', 'text': 'x' * 70000}}), flush=True)\n"
                    "print(json.dumps({'type': 'turn.completed', 'usage': "
                    "{'input_tokens': 1, 'output_tokens': 1}}), flush=True)\n",
                    encoding="utf-8",
                )
                executable.chmod(0o700)
                with patch(
                    "cli.codex_subscription.codex_subscription_status",
                    return_value=CodexSubscriptionStatus(
                        available=True,
                        authenticated=True,
                        executable=str(executable),
                        detail="ready",
                    ),
                ):
                    result = await run_codex_exec(
                        prompt="oversized event regression",
                        model="gpt-5.6-sol",
                        execution_cwd=root,
                        sandbox="read-only",
                        skip_git_repo_check=True,
                    )
                self.assertEqual(len(result.final_text), 70_000)
                self.assertEqual(result.turns, 1)

        asyncio.run(exercise())


if __name__ == "__main__":
    unittest.main()
