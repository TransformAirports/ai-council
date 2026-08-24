from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from cli.agents import Agent
from cli.codex_subscription import CodexExecResult
from cli.openai_council import run_openai_council_agent


def _usage(input_tokens: int, cached_tokens: int, output_tokens: int):
    return SimpleNamespace(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        input_tokens_details=SimpleNamespace(cached_tokens=cached_tokens),
    )


def _agent(root: Path, *, tools: tuple[str, ...] = ("Read", "Write")) -> Agent:
    charter = root / "agent.md"
    charter.write_text("Write the requested artifact.", encoding="utf-8")
    return Agent(
        name="test-agent",
        display_name="Test Agent",
        description="Test role",
        tools=tools,
        order=1,
        system_prompt="Write the requested artifact.",
        path=charter,
    )


class OpenAICouncilRunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_live_route_uses_chatgpt_subscription_without_api_cost(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output_root = root / "outputs" / "stage1"
            output_root.mkdir(parents=True)
            captured: dict[str, object] = {}

            async def fake_codex(**kwargs):
                captured.update(kwargs)
                return CodexExecResult(
                    final_text="Completed the assignment.",
                    input_tokens=100,
                    cached_input_tokens=30,
                    output_tokens=20,
                    reasoning_output_tokens=5,
                    tool_calls=2,
                    turns=1,
                )

            with patch(
                "cli.codex_subscription.run_codex_exec", new=fake_codex
            ):
                metrics = await run_openai_council_agent(
                    agent=_agent(root),
                    user_prompt="Write outputs/stage1/report.md",
                    model="gpt-5.6-sol",
                    cwd=root,
                    max_turns=4,
                    write_roots=(output_root,),
                )

            self.assertEqual(captured["model"], "gpt-5.6-sol")
            self.assertEqual(captured["sandbox"], "workspace-write")
            self.assertEqual(captured["execution_cwd"], output_root.resolve())
            self.assertFalse(captured["require_final_text"])
            self.assertIn(str(root.resolve()), str(captured["prompt"]))
            self.assertEqual(metrics.cost_usd, 0.0)
            self.assertEqual(metrics.total_tokens, 125)

    async def test_one_model_executes_tool_loop_and_writes_workspace_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outputs").mkdir()
            calls: list[dict[str, object]] = []

            async def response_fn(**kwargs):
                calls.append(kwargs)
                if len(calls) == 1:
                    tool = SimpleNamespace(
                        type="function_call",
                        name="workspace_write",
                        call_id="call-write",
                        arguments=json.dumps(
                            {
                                "path": "outputs/report.md",
                                "content": "# Report\n\n" + "evidence " * 40,
                            }
                        ),
                    )
                    return SimpleNamespace(
                        status="completed",
                        error=None,
                        output=[tool],
                        usage=_usage(100, 20, 50),
                    )
                return SimpleNamespace(
                    status="completed",
                    error=None,
                    output=[],
                    usage=_usage(200, 100, 20),
                )

            metrics = await run_openai_council_agent(
                agent=_agent(root),
                user_prompt="Write outputs/report.md",
                model="gpt-5.6-sol",
                cwd=root,
                max_turns=4,
                response_fn=response_fn,
            )

            self.assertTrue((root / "outputs" / "report.md").is_file())
            self.assertEqual([call["model"] for call in calls], ["gpt-5.6-sol"] * 2)
            self.assertTrue(all(call["store"] is False for call in calls))
            first_tool_types = {tool["type"] for tool in calls[0]["tools"]}
            self.assertIn("function", first_tool_types)
            self.assertEqual(metrics.turns, 2)
            self.assertEqual(metrics.tool_calls, 1)
            self.assertEqual(metrics.input_tokens, 300)
            self.assertEqual(metrics.cached_input_tokens, 120)
            self.assertEqual(metrics.output_tokens, 70)
            self.assertAlmostEqual(metrics.cost_usd, 0.002168)

    async def test_workspace_write_refuses_escape_and_returns_error_to_model(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outputs").mkdir()
            histories: list[list[dict[str, object]]] = []

            async def response_fn(**kwargs):
                histories.append(kwargs["input"])
                if len(histories) == 1:
                    return SimpleNamespace(
                        status="completed",
                        error=None,
                        output=[
                            SimpleNamespace(
                                type="function_call",
                                name="workspace_write",
                                call_id="escape",
                                arguments=json.dumps(
                                    {"path": "../escape.md", "content": "no"}
                                ),
                            )
                        ],
                        usage=_usage(1, 0, 1),
                    )
                return SimpleNamespace(
                    status="completed",
                    error=None,
                    output=[],
                    usage=_usage(1, 0, 1),
                )

            await run_openai_council_agent(
                agent=_agent(root, tools=("Write",)),
                user_prompt="Try the path.",
                model="gpt-5.6-sol",
                cwd=root,
                max_turns=3,
                response_fn=response_fn,
            )

            self.assertFalse((root.parent / "escape.md").exists())
            output = next(
                item
                for item in histories[1]
                if item.get("type") == "function_call_output"
            )
            self.assertIn("Tool error", output["output"])
            self.assertIn("inside the Council workspace", output["output"])


if __name__ == "__main__":
    unittest.main()
