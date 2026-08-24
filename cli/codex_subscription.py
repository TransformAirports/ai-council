"""ChatGPT-subscription authentication and non-interactive Codex execution.

The Council uses the locally installed Codex CLI as the supported bridge to a
person's ChatGPT plan.  No OpenAI API key is read or forwarded.  ``codex exec``
reuses the browser-authenticated session created by ``codex login``.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Callable, Mapping


@dataclass(frozen=True)
class CodexSubscriptionStatus:
    available: bool
    authenticated: bool
    executable: str | None
    detail: str


@dataclass(frozen=True)
class CodexExecResult:
    final_text: str
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int
    reasoning_output_tokens: int
    tool_calls: int
    turns: int


class CodexSubscriptionError(RuntimeError):
    """The local subscription-backed Codex process could not complete."""


Runner = Callable[..., subprocess.CompletedProcess[str]]
Which = Callable[[str], str | None]
ToolReporter = Callable[[str, str], Awaitable[None]]

# Codex emits newline-delimited JSON. Tool results and a role's final artifact
# can legitimately make one event much larger than asyncio's 64 KiB default.
# Keep a bounded ceiling aligned with the Claude SDK transport instead of
# allowing a valid event to fail with "Separator is not found".
CODEX_EVENT_STREAM_LIMIT_BYTES = 64 * 1024 * 1024


def codex_subscription_status(
    *,
    which: Which = shutil.which,
    runner: Runner = subprocess.run,
    environment: Mapping[str, str] | None = None,
) -> CodexSubscriptionStatus:
    """Check for a ChatGPT-authenticated Codex CLI without making a model call."""

    executable = which("codex")
    if not executable:
        return CodexSubscriptionStatus(
            available=False,
            authenticated=False,
            executable=None,
            detail="Codex CLI is not installed",
        )
    try:
        completed = runner(
            [executable, "login", "status"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
            env=dict(os.environ if environment is None else environment),
        )
    except (OSError, subprocess.SubprocessError):
        return CodexSubscriptionStatus(
            available=True,
            authenticated=False,
            executable=executable,
            detail="Codex login status could not be verified",
        )
    detail = " ".join(
        part.strip() for part in (completed.stdout, completed.stderr) if part.strip()
    )
    authenticated = completed.returncode == 0 and "chatgpt" in detail.casefold()
    return CodexSubscriptionStatus(
        available=True,
        authenticated=authenticated,
        executable=executable,
        detail=(
            "ChatGPT subscription session present"
            if authenticated
            else "Codex is not signed in with ChatGPT"
        ),
    )


def _subscription_environment() -> dict[str, str]:
    """Preserve the local login while preventing API-key billing fallback."""

    environment = dict(os.environ)
    for name in (
        "OPENAI_API_KEY",
        "CODEX_API_KEY",
        "ANTHROPIC_API_KEY",
        "CLAUDE_CODE_OAUTH_TOKEN",
    ):
        environment.pop(name, None)
    return environment


def _event_target(item: dict[str, Any]) -> str:
    for key in ("command", "query", "path", "name", "server", "url"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()[:500]
    return ""


def _safe_failure(detail: str) -> str:
    folded = detail.casefold()
    if "requires a newer version of codex" in folded:
        return (
            "GPT-5.6 Sol requires a newer Codex CLI. Run the official installer: "
            "`curl -fsSL https://chatgpt.com/codex/install.sh | sh`, then restart the Council."
        )
    if any(token in folded for token in ("not logged in", "login required", "authentication")):
        return "Codex is not signed in with ChatGPT. Run `codex login` and restart the Council."
    if "rate limit" in folded or "usage limit" in folded or "429" in folded:
        return "The ChatGPT plan has reached a Codex usage limit. Wait for the plan window to reset, then resume."
    if "model" in folded and any(token in folded for token in ("not found", "not available", "unsupported")):
        return "GPT-5.6 Sol is not available to this ChatGPT workspace. Check the active Codex account and plan."
    return "The subscription-backed Codex run did not complete. Check the Council error log and try Resume."


async def run_codex_exec(
    *,
    prompt: str,
    model: str,
    execution_cwd: Path,
    sandbox: str,
    output_schema: dict[str, Any] | None = None,
    additional_write_dirs: tuple[Path, ...] = (),
    on_tool: ToolReporter | None = None,
    timeout_seconds: float = 3_600,
    skip_git_repo_check: bool = False,
    reasoning_effort: str = "high",
    require_final_text: bool = True,
) -> CodexExecResult:
    """Run one ephemeral Codex turn with saved ChatGPT subscription auth.

    Structured/text callers require an ``agent_message``. Workspace-producing
    Council roles do not: Codex can legitimately finish after its last tool
    command without a ceremonial chat response, and their typed artifacts are
    validated by the orchestrator immediately afterward.
    """

    status = await asyncio.to_thread(codex_subscription_status)
    if not status.authenticated or not status.executable:
        raise CodexSubscriptionError(
            "Codex is not signed in with ChatGPT. Run `codex login`, complete the browser sign-in, and restart the Council."
        )

    execution_cwd = execution_cwd.resolve()
    execution_cwd.mkdir(parents=True, exist_ok=True)
    for directory in additional_write_dirs:
        directory.resolve().mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="council-codex-") as temporary:
        command = [
            status.executable,
            "exec",
            "--json",
            "--ephemeral",
            "--model",
            model,
            "--sandbox",
            sandbox,
            "--ignore-user-config",
            "--ignore-rules",
            "--color",
            "never",
            "--config",
            f'model_reasoning_effort="{reasoning_effort}"',
            "--cd",
            str(execution_cwd),
        ]
        for directory in additional_write_dirs:
            command.extend(("--add-dir", str(directory.resolve())))
        if skip_git_repo_check:
            command.append("--skip-git-repo-check")
        if output_schema is not None:
            schema_path = Path(temporary) / "output-schema.json"
            schema_path.write_text(
                json.dumps(output_schema, ensure_ascii=False, sort_keys=True),
                encoding="utf-8",
            )
            command.extend(("--output-schema", str(schema_path)))
        command.append("-")

        process = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=_subscription_environment(),
            limit=CODEX_EVENT_STREAM_LIMIT_BYTES,
        )
        assert process.stdin is not None
        assert process.stdout is not None
        assert process.stderr is not None
        process.stdin.write(prompt.encode("utf-8"))
        await process.stdin.drain()
        process.stdin.close()

        final_text = ""
        usage = {"input": 0, "cached": 0, "output": 0, "reasoning": 0}
        tool_calls = 0
        turns = 0
        failures: list[str] = []

        async def read_stdout() -> None:
            nonlocal final_text, tool_calls, turns
            async for raw_line in process.stdout:
                try:
                    event = json.loads(raw_line.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
                if not isinstance(event, dict):
                    continue
                event_type = str(event.get("type", ""))
                if event_type == "turn.started":
                    turns += 1
                elif event_type == "turn.completed":
                    raw_usage = event.get("usage")
                    if isinstance(raw_usage, dict):
                        for source, destination in (
                            ("input_tokens", "input"),
                            ("cached_input_tokens", "cached"),
                            ("output_tokens", "output"),
                            ("reasoning_output_tokens", "reasoning"),
                        ):
                            value = raw_usage.get(source, 0)
                            if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                                usage[destination] += value
                elif event_type in {"turn.failed", "error"}:
                    failures.append(json.dumps(event, ensure_ascii=False)[:2_000])
                elif event_type == "item.completed":
                    item = event.get("item")
                    if not isinstance(item, dict):
                        continue
                    if item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                        final_text = item["text"]
                elif event_type == "item.started":
                    item = event.get("item")
                    if not isinstance(item, dict):
                        continue
                    item_type = str(item.get("type", ""))
                    if item_type not in {"reasoning", "agent_message", "plan_update"}:
                        tool_calls += 1
                        if on_tool is not None:
                            await on_tool(item_type or "codex_tool", _event_target(item))

        async def read_stderr() -> str:
            return (await process.stderr.read()).decode("utf-8", errors="replace")[-8_000:]

        stderr_task = asyncio.create_task(read_stderr())
        stdout_task = asyncio.create_task(read_stdout())
        wait_task = asyncio.create_task(process.wait())
        try:
            await asyncio.wait_for(
                asyncio.gather(stdout_task, wait_task),
                timeout=max(1.0, timeout_seconds),
            )
        except asyncio.TimeoutError as exc:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=10)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
            stdout_task.cancel()
            raise CodexSubscriptionError(
                "The subscription-backed Codex role timed out. Work already validated by the Council remains resumable."
            ) from exc
        finally:
            stderr = await stderr_task

    if process.returncode != 0 or failures:
        raise CodexSubscriptionError(_safe_failure("\n".join([stderr, *failures])))
    if require_final_text and not final_text.strip():
        raise CodexSubscriptionError(
            "The subscription-backed Codex role ended without a final response."
        )
    return CodexExecResult(
        final_text=final_text,
        input_tokens=usage["input"],
        cached_input_tokens=usage["cached"],
        output_tokens=usage["output"],
        reasoning_output_tokens=usage["reasoning"],
        tool_calls=tool_calls,
        turns=max(1, turns),
    )


__all__ = [
    "CodexExecResult",
    "CodexSubscriptionError",
    "CodexSubscriptionStatus",
    "codex_subscription_status",
    "run_codex_exec",
]
