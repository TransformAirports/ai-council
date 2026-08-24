"""OpenAI Responses runner for a complete GPT-backed Council role.

The Council's agent charters were written for a local workspace: agents read
receipts, write typed artifacts, run trusted render/QA commands, inspect images,
and search the web.  This adapter exposes those same bounded capabilities as
Responses API function tools so GPT-5.6 Sol can execute any report role without
silently delegating work to Claude.
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Callable

from cli.agents import Agent


GPT_5_6_INPUT_USD_PER_MILLION = 4.00
GPT_5_6_CACHED_INPUT_USD_PER_MILLION = 0.40
GPT_5_6_OUTPUT_USD_PER_MILLION = 20.00
MAX_TEXT_READ_BYTES = 240_000
MAX_TOOL_OUTPUT_CHARS = 80_000
MAX_IMAGE_BYTES = 12 * 1024 * 1024
MAX_RESPONSE_ROUNDS = 60

ResponseFunction = Callable[..., Awaitable[object]]
ToolReporter = Callable[[str, str], Awaitable[None]]


@dataclass(frozen=True)
class OpenAICouncilMetrics:
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    turns: int
    tool_calls: int

    def as_dict(self) -> dict[str, int | float]:
        return {
            "input_tokens": self.input_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cost_usd": self.cost_usd,
            "turns": self.turns,
            "tool_calls": self.tool_calls,
        }


class OpenAICouncilError(RuntimeError):
    """A GPT Council role failed before its artifact contract was satisfied."""


def _safe_workspace_path(
    root: Path,
    raw: str,
    *,
    must_exist: bool = False,
    writable: bool = False,
    write_roots: tuple[Path, ...] = (),
) -> Path:
    value = str(raw or "").strip()
    if not value or "\x00" in value:
        raise ValueError("A non-empty workspace-relative path is required.")
    candidate = Path(value)
    if candidate.is_absolute():
        resolved = candidate.resolve(strict=must_exist)
    else:
        resolved = (root / candidate).resolve(strict=must_exist)
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("Path must stay inside the Council workspace.") from exc
    if writable:
        approved = tuple(path.resolve() for path in write_roots) or (
            (root / "outputs").resolve(),
        )
        if not any(
            resolved == allowed or resolved.is_relative_to(allowed)
            for allowed in approved
        ):
            labels = ", ".join(
                str(path.relative_to(root.resolve()))
                if path.is_relative_to(root.resolve())
                else str(path)
                for path in approved
            )
            raise ValueError(
                f"Council agent may write only inside its commissioned artifact roots: {labels}."
            )
    return resolved


def _tool_schema(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        },
        "strict": True,
    }


def _tools_for(agent: Agent) -> list[dict[str, Any]]:
    declared = {item.casefold() for item in agent.tools}
    # The historical Deep Research seat returned one remote API response and
    # therefore declared no workspace tools. In a coherent-model run it is a
    # normal independent researcher and owes the same brief/evidence artifacts.
    if agent.is_research and not declared:
        declared = {"websearch", "webfetch", "read", "write"}
    tools: list[dict[str, Any]] = []
    if declared & {"websearch", "webfetch"}:
        tools.append({"type": "web_search"})
    if "read" in declared:
        tools.extend(
            (
                _tool_schema(
                    "workspace_read",
                    "Read one UTF-8 text file from the local Council workspace.",
                    {"path": {"type": "string"}},
                    ["path"],
                ),
                _tool_schema(
                    "workspace_glob",
                    "List workspace files matching a relative glob pattern.",
                    {"pattern": {"type": "string"}},
                    ["pattern"],
                ),
                _tool_schema(
                    "workspace_view_image",
                    "Inspect one PNG, JPEG, GIF, or WebP image from the workspace.",
                    {"path": {"type": "string"}},
                    ["path"],
                ),
            )
        )
    if "write" in declared or "edit" in declared:
        tools.append(
            _tool_schema(
                "workspace_write",
                "Atomically write a UTF-8 artifact inside outputs/.",
                {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                ["path", "content"],
            )
        )
    if "bash" in declared:
        tools.append(
            _tool_schema(
                "workspace_shell",
                "Run one non-shell trusted Python or rendering command in the workspace.",
                {
                    "command": {"type": "string"},
                    "timeout_seconds": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 300,
                    },
                },
                ["command", "timeout_seconds"],
            )
        )
    return tools


def _read_text(root: Path, args: dict[str, Any]) -> str:
    path = _safe_workspace_path(root, str(args.get("path", "")), must_exist=True)
    if not path.is_file():
        raise ValueError("Requested path is not a regular file.")
    if path.stat().st_size > MAX_TEXT_READ_BYTES:
        raise ValueError(
            f"File is larger than {MAX_TEXT_READ_BYTES:,} bytes; use a trusted "
            "workspace_shell parser to extract only what you need."
        )
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("File is not UTF-8 text; use a parser or image tool.") from exc


def _glob_files(root: Path, args: dict[str, Any]) -> str:
    pattern = str(args.get("pattern", "")).strip()
    if not pattern or Path(pattern).is_absolute() or ".." in Path(pattern).parts:
        raise ValueError("Glob must be a workspace-relative pattern without '..'.")
    matches: list[str] = []
    for path in sorted(root.glob(pattern)):
        try:
            resolved = path.resolve(strict=True)
            relative = resolved.relative_to(root.resolve()).as_posix()
        except (OSError, ValueError):
            continue
        if resolved.is_file():
            matches.append(relative)
        if len(matches) >= 500:
            matches.append("… truncated at 500 files")
            break
    return "\n".join(matches) if matches else "No matching files."


def _write_text(
    root: Path,
    args: dict[str, Any],
    write_roots: tuple[Path, ...],
) -> str:
    path = _safe_workspace_path(
        root,
        str(args.get("path", "")),
        writable=True,
        write_roots=write_roots,
    )
    content = args.get("content")
    if not isinstance(content, str):
        raise ValueError("content must be text.")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.openai-tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)
    return f"Wrote {len(content.encode('utf-8')):,} bytes to {path.relative_to(root)}."


def _clean_subprocess_environment() -> dict[str, str]:
    sensitive = ("KEY", "TOKEN", "SECRET", "PASSWORD", "CREDENTIAL")
    return {
        name: value
        for name, value in os.environ.items()
        if not any(marker in name.upper() for marker in sensitive)
    }


def _shell(
    root: Path,
    args: dict[str, Any],
    write_roots: tuple[Path, ...],
) -> str:
    command = str(args.get("command", "")).strip()
    timeout = max(1, min(300, int(args.get("timeout_seconds", 120))))
    try:
        argv = shlex.split(command)
    except ValueError as exc:
        raise ValueError("Command could not be parsed.") from exc
    if not argv:
        raise ValueError("Command is empty.")
    executable = argv[0]
    resolved_executable = shutil.which(executable) if not Path(executable).is_absolute() else executable
    if not resolved_executable:
        raise ValueError(f"Executable is unavailable: {executable}")
    allowed = {"python", "python3", "soffice", "libreoffice", "pdftoppm"}
    executable_path = Path(resolved_executable).resolve()
    workspace_python = (root / ".venv" / "bin" / "python").resolve()
    if executable_path != workspace_python and executable_path.name not in allowed:
        raise ValueError(
            "Only the workspace Python runtime and approved Office/PDF renderers "
            "may run. Use read/write/glob tools for file operations."
        )
    if executable_path.name.startswith("python") or executable_path == workspace_python:
        if "-c" in argv:
            raise ValueError("Inline Python is disabled; write a script under outputs/ first.")
        if "-m" in argv:
            index = argv.index("-m")
            module = argv[index + 1] if index + 1 < len(argv) else ""
            if not module.startswith("cli."):
                raise ValueError("Only trusted cli.* modules may run with python -m.")
        elif len(argv) > 1 and not argv[1].startswith("-"):
            script = _safe_workspace_path(root, argv[1], must_exist=True)
            approved = tuple(path.resolve() for path in write_roots) or (
                (root / "outputs").resolve(),
            )
            if not any(
                script == allowed or script.is_relative_to(allowed)
                for allowed in approved
            ):
                raise ValueError(
                    "Generated Python scripts must live under a commissioned artifact root."
                )
    try:
        completed = subprocess.run(
            [str(executable_path), *argv[1:]],
            cwd=root,
            env=_clean_subprocess_environment(),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return json.dumps({"outcome": "timeout", "timeout_seconds": timeout})
    stdout = completed.stdout[-MAX_TOOL_OUTPUT_CHARS:]
    stderr = completed.stderr[-MAX_TOOL_OUTPUT_CHARS:]
    return json.dumps(
        {
            "outcome": "exit",
            "exit_code": completed.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "truncated": (
                len(completed.stdout) > MAX_TOOL_OUTPUT_CHARS
                or len(completed.stderr) > MAX_TOOL_OUTPUT_CHARS
            ),
        },
        ensure_ascii=False,
    )


def _view_image(root: Path, args: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    path = _safe_workspace_path(root, str(args.get("path", "")), must_exist=True)
    suffix = path.suffix.casefold()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(suffix)
    if mime is None or not path.is_file():
        raise ValueError("Image must be a PNG, JPEG, GIF, or WebP file.")
    data = path.read_bytes()
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError(f"Image exceeds the {MAX_IMAGE_BYTES // 1024 // 1024} MB inspection limit.")
    relative = path.relative_to(root).as_posix()
    message = {
        "role": "user",
        "content": [
            {"type": "input_text", "text": f"Inspect the requested workspace image: {relative}"},
            {
                "type": "input_image",
                "image_url": f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}",
                "detail": "high",
            },
        ],
    }
    return f"Attached {relative} for visual inspection.", message


def _response_item_dict(item: object) -> dict[str, Any]:
    if isinstance(item, dict):
        return item
    dump = getattr(item, "model_dump", None)
    if callable(dump):
        return dump(mode="json", exclude_none=True)
    kind = str(getattr(item, "type", "") or "")
    if kind == "function_call":
        return {
            "type": kind,
            "name": getattr(item, "name", ""),
            "call_id": getattr(item, "call_id", ""),
            "arguments": getattr(item, "arguments", "{}"),
        }
    raise OpenAICouncilError(f"OpenAI returned an unsupported response item: {kind or type(item).__name__}")


def _usage(response: object) -> tuple[int, int, int]:
    usage = getattr(response, "usage", None)
    input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
    details = getattr(usage, "input_tokens_details", None)
    cached_tokens = int(getattr(details, "cached_tokens", 0) or 0)
    if min(input_tokens, output_tokens, cached_tokens) < 0 or cached_tokens > input_tokens:
        raise OpenAICouncilError("OpenAI returned invalid token usage metadata.")
    return input_tokens, cached_tokens, output_tokens


def _retryable(exc: BaseException) -> bool:
    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    if isinstance(status, int) and (status == 429 or status >= 500):
        return True
    folded = str(exc).casefold()
    return any(token in folded for token in ("timed out", "timeout", "connection reset", "temporarily unavailable"))


async def _response_with_retries(call: ResponseFunction, kwargs: dict[str, Any]) -> object:
    last: BaseException | None = None
    for attempt, delay in enumerate((0, 20, 45, 90), start=1):
        if delay:
            await asyncio.sleep(delay)
        try:
            return await call(**kwargs)
        except Exception as exc:  # noqa: BLE001 - provider exceptions are normalized
            last = exc
            if attempt == 4 or not _retryable(exc):
                raise OpenAICouncilError(
                    f"OpenAI Responses call failed ({type(exc).__name__})."
                ) from exc
    raise OpenAICouncilError("OpenAI Responses call failed.") from last


async def run_openai_council_agent(
    *,
    agent: Agent,
    user_prompt: str,
    model: str,
    cwd: Path,
    max_turns: int,
    response_fn: ResponseFunction | None = None,
    on_tool: ToolReporter | None = None,
    write_roots: tuple[Path, ...] = (),
) -> OpenAICouncilMetrics:
    """Execute one agent charter with GPT-5.6 Sol.

    Live runs use ``codex exec`` and the person's saved ChatGPT subscription
    login. ``response_fn`` retains a model-free Responses-shaped test seam.
    """

    tools = _tools_for(agent)
    approved_write_roots = tuple(path.resolve() for path in write_roots) or (
        (cwd / "outputs").resolve(),
    )
    approved_write_labels = ", ".join(
        path.relative_to(cwd.resolve()).as_posix()
        if path.is_relative_to(cwd.resolve())
        else str(path)
        for path in approved_write_roots
    )
    instructions = (
        agent.system_prompt
        + "\n\n## Council execution environment\n\n"
        + "You are the sole model executing this Council role. Use the supplied workspace "
        "tools to read exact inputs and write every requested artifact. Work only inside "
        "the current Council repository; write only inside these commissioned artifact "
        f"roots: {approved_write_labels}. Do not edit prompts, "
        "agent charters, source material, application code, or prior release folders. "
        "Do not merely describe the artifact in chat: create it at the exact requested path. "
        "Any charter sentence claiming this role alone uses another model or provider is "
        "legacy routing metadata; the run-level model selection is authoritative."
    )

    if response_fn is None:
        from cli.codex_subscription import run_codex_exec

        execution_root = Path(
            os.path.commonpath([str(path) for path in approved_write_roots])
        )
        subscription_prompt = (
            instructions
            + "\n\n## Repository boundary\n\n"
            + f"The Council repository read root is `{cwd.resolve()}`. Resolve every "
            "relative input or output path in the assignment against that repository "
            "root, even though your process starts inside a narrower commissioned "
            "write directory. Use absolute paths when invoking repository scripts.\n\n"
            + "## Current assignment\n\n"
            + user_prompt
        )
        try:
            result = await run_codex_exec(
                prompt=subscription_prompt,
                model=model,
                execution_cwd=execution_root,
                sandbox="workspace-write",
                on_tool=on_tool,
                # The commissioned files are the result. The orchestrator
                # validates their type, completeness, and dependency receipt;
                # a redundant final chat sentence is not a success criterion.
                require_final_text=False,
            )
        except Exception as exc:  # noqa: BLE001 - normalize the provider boundary
            raise OpenAICouncilError(str(exc)) from exc
        return OpenAICouncilMetrics(
            input_tokens=result.input_tokens,
            cached_input_tokens=result.cached_input_tokens,
            output_tokens=result.output_tokens,
            total_tokens=(
                result.input_tokens
                + result.output_tokens
                + result.reasoning_output_tokens
            ),
            # ChatGPT-plan use is not API-key token billing.
            cost_usd=0.0,
            turns=result.turns,
            tool_calls=result.tool_calls,
        )

    client = None
    call = response_fn
    history: list[dict[str, Any]] = [{"role": "user", "content": user_prompt}]
    totals = {"input": 0, "cached": 0, "output": 0}
    tool_calls = 0
    turns = 0
    try:
        for _ in range(max(1, min(MAX_RESPONSE_ROUNDS, int(max_turns)))):
            turns += 1
            response = await _response_with_retries(
                call,
                {
                    "model": model,
                    "instructions": instructions,
                    "input": history,
                    "reasoning": {"effort": "high"},
                    "max_output_tokens": 32_768,
                    "tools": tools,
                    "parallel_tool_calls": True,
                    "store": False,
                },
            )
            input_tokens, cached_tokens, output_tokens = _usage(response)
            totals["input"] += input_tokens
            totals["cached"] += cached_tokens
            totals["output"] += output_tokens
            output = list(getattr(response, "output", ()) or ())
            custom_calls = [
                item
                for item in output
                if str(getattr(item, "type", "") or (item.get("type") if isinstance(item, dict) else "")) == "function_call"
            ]
            history.extend(_response_item_dict(item) for item in output)
            if not custom_calls:
                status = str(getattr(response, "status", "") or "").casefold()
                if status != "completed" or getattr(response, "error", None) is not None:
                    raise OpenAICouncilError(
                        f"OpenAI ended the role with status {status or 'unknown'}."
                    )
                break

            for item in custom_calls:
                name = str(getattr(item, "name", "") or (item.get("name") if isinstance(item, dict) else ""))
                call_id = str(getattr(item, "call_id", "") or (item.get("call_id") if isinstance(item, dict) else ""))
                raw_arguments = getattr(item, "arguments", None)
                if raw_arguments is None and isinstance(item, dict):
                    raw_arguments = item.get("arguments", "{}")
                args: dict[str, Any] = {}
                try:
                    args = json.loads(raw_arguments) if isinstance(raw_arguments, str) else dict(raw_arguments or {})
                except (json.JSONDecodeError, TypeError, ValueError) as exc:
                    result = f"Tool error: invalid JSON arguments ({type(exc).__name__})."
                    image_message = None
                else:
                    image_message = None
                    try:
                        if name == "workspace_read":
                            result = _read_text(cwd, args)
                        elif name == "workspace_glob":
                            result = _glob_files(cwd, args)
                        elif name == "workspace_write":
                            result = _write_text(cwd, args, write_roots)
                        elif name == "workspace_shell":
                            result = await asyncio.to_thread(
                                _shell, cwd, args, write_roots
                            )
                        elif name == "workspace_view_image":
                            result, image_message = _view_image(cwd, args)
                        else:
                            result = f"Tool error: unknown or unavailable tool {name!r}."
                    except Exception as exc:  # noqa: BLE001 - tool errors return to the model
                        result = f"Tool error: {exc}"
                tool_calls += 1
                target = str(
                    args.get("path")
                    or args.get("pattern")
                    or args.get("command")
                    or ""
                )
                if on_tool is not None:
                    await on_tool(name, target[:500])
                history.append(
                    {
                        "type": "function_call_output",
                        "call_id": call_id,
                        "output": str(result)[:MAX_TOOL_OUTPUT_CHARS],
                    }
                )
                if image_message is not None:
                    history.append(image_message)
        else:
            raise OpenAICouncilError(
                f"GPT-5.6 Sol exhausted its {max_turns}-turn tool budget."
            )
    finally:
        if client is not None:
            await client.close()

    uncached = totals["input"] - totals["cached"]
    cost = round(
        (
            uncached * GPT_5_6_INPUT_USD_PER_MILLION
            + totals["cached"] * GPT_5_6_CACHED_INPUT_USD_PER_MILLION
            + totals["output"] * GPT_5_6_OUTPUT_USD_PER_MILLION
        )
        / 1_000_000,
        6,
    )
    return OpenAICouncilMetrics(
        input_tokens=totals["input"],
        cached_input_tokens=totals["cached"],
        output_tokens=totals["output"],
        total_tokens=totals["input"] + totals["output"],
        cost_usd=cost,
        turns=turns,
        tool_calls=tool_calls,
    )


__all__ = [
    "OpenAICouncilError",
    "OpenAICouncilMetrics",
    "run_openai_council_agent",
]
