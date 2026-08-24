"""Read-only self-service diagnostics for a Council installation."""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Callable, Mapping, Sequence

from rich.console import Console
from rich.table import Table


REPO_ROOT = Path(__file__).resolve().parent.parent
MINIMUM_FREE_BYTES = 512 * 1024 * 1024


@dataclass(frozen=True)
class DoctorCheck:
    key: str
    label: str
    ok: bool
    required: bool
    detail: str
    fix: str = ""


Which = Callable[[str], str | None]
Runner = Callable[..., subprocess.CompletedProcess[str]]


def _python_check(version: Sequence[int]) -> DoctorCheck:
    value = ".".join(str(part) for part in version[:3])
    ok = tuple(version[:2]) >= (3, 11)
    return DoctorCheck(
        "python",
        "Python 3.11+",
        ok,
        True,
        value,
        "Install Python 3.11 or newer, then run ./council again.",
    )


def _tool_check(
    key: str,
    label: str,
    candidates: tuple[str, ...],
    fix: str,
    *,
    which: Which,
) -> DoctorCheck:
    path = None
    for name in candidates:
        candidate = which(name)
        if candidate:
            path = candidate
            break
    return DoctorCheck(
        key,
        label,
        path is not None,
        True,
        str(path) if path else "not found",
        fix,
    )


def _claude_auth_check(
    claude: str | None,
    *,
    environment: Mapping[str, str],
    runner: Runner,
) -> DoctorCheck:
    if claude is None:
        return DoctorCheck(
            "claude-auth",
            "Claude authentication",
            False,
            True,
            "cannot check subscription access without the Claude CLI",
            "Install Claude Code, then run: claude auth login",
        )
    try:
        completed = runner(
            [claude, "auth", "status", "--json"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
            env={
                key: value
                for key, value in environment.items()
                if key not in {"ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN"}
            },
        )
        payload = json.loads(completed.stdout or "{}")
        logged_in = completed.returncode == 0 and payload.get("loggedIn") is True
        method = str(payload.get("authMethod") or "authenticated session")
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError, TypeError):
        logged_in = False
        method = "status could not be verified"
    return DoctorCheck(
        "claude-auth",
        "Claude authentication",
        logged_in,
        True,
        (
            f"{method} session present; live model access is checked when Council opens"
            if logged_in
            else "not signed in"
        ),
        "Run: claude auth login",
    )


def _codex_auth_check(
    codex: str | None,
    *,
    environment: Mapping[str, str],
    runner: Runner,
) -> DoctorCheck:
    if codex is None:
        return DoctorCheck(
            "codex-auth",
            "ChatGPT subscription",
            False,
            False,
            "cannot check without the Codex CLI",
            "Install Codex, then run: codex login",
        )
    try:
        completed = runner(
            [codex, "login", "status"],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
            env={
                key: value
                for key, value in environment.items()
                if key not in {"OPENAI_API_KEY", "CODEX_API_KEY"}
            },
        )
        detail = " ".join(
            part.strip()
            for part in (completed.stdout, completed.stderr)
            if part.strip()
        )
        logged_in = completed.returncode == 0 and "chatgpt" in detail.casefold()
    except (OSError, subprocess.SubprocessError):
        logged_in = False
    return DoctorCheck(
        "codex-auth",
        "ChatGPT subscription",
        logged_in,
        False,
        "ChatGPT session present" if logged_in else "not signed in with ChatGPT",
        "Run: codex login",
    )


def _workspace_check(repo_root: Path) -> DoctorCheck:
    problems: list[str] = []
    for name in ("outputs", "reports", "runs"):
        path = repo_root / name
        probe = path if path.exists() else path.parent
        if not probe.is_dir() or not os.access(probe, os.W_OK):
            problems.append(name)
    return DoctorCheck(
        "workspace",
        "Writable work folders",
        not problems,
        True,
        "outputs/, reports/, and runs/ are writable" if not problems else "not writable: " + ", ".join(problems),
        "Give your user write access to this repository; do not run the Council with sudo.",
    )


def _disk_check(repo_root: Path, disk_usage: Callable[[Path], object]) -> DoctorCheck:
    try:
        free = int(getattr(disk_usage(repo_root), "free"))
    except (OSError, TypeError, ValueError, AttributeError):
        return DoctorCheck(
            "disk",
            "Free disk space",
            False,
            True,
            "could not be measured",
            "Confirm that at least 512 MB is free on the repository volume.",
        )
    gib = free / (1024 ** 3)
    return DoctorCheck(
        "disk",
        "Free disk space",
        free >= MINIMUM_FREE_BYTES,
        True,
        f"{gib:.1f} GB available",
        "Free at least 512 MB before starting a report.",
    )


def _package_check() -> DoctorCheck:
    packages = {
        "claude_agent_sdk": "Claude Agent SDK",
        "fastapi": "FastAPI",
        "docx": "python-docx",
        "pptx": "python-pptx",
        "pypdf": "pypdf",
        "openpyxl": "openpyxl",
    }
    missing = [label for module, label in packages.items() if importlib.util.find_spec(module) is None]
    return DoctorCheck(
        "python-packages",
        "Council Python packages",
        not missing,
        True,
        "installed" if not missing else "missing: " + ", ".join(missing),
        "Run ./council once to create or repair the local virtual environment.",
    )


def _configuration_checks(repo_root: Path, environment: Mapping[str, str]) -> list[DoctorCheck]:
    from cli.config import inspect_config

    inspection = inspect_config(repo_root / "council.toml")
    cfg = inspection.config
    if inspection.parse_error:
        configured = DoctorCheck(
            "models",
            "Model routing",
            False,
            True,
            f"council.toml could not be parsed: {inspection.parse_error}",
            "Correct or remove the malformed council.toml, then rerun ./council --doctor.",
        )
    elif inspection.blocked_models:
        selections = "; ".join(
            f"{item.role}: {item.configured} → {item.replacement}"
            for item in inspection.blocked_models
        )
        configured = DoctorCheck(
            "models",
            "Model routing",
            False,
            True,
            f"blocked model selection{'s' if len(inspection.blocked_models) != 1 else ''}: {selections}",
            "Replace the blocked model IDs in council.toml with the suggested values.",
        )
    else:
        configured = DoctorCheck(
            "models",
            "Model routing",
            bool(cfg.models),
            True,
            f"{len(cfg.models)} roles resolved; default ceiling ${cfg.default_budget_usd:g}",
            "Restore council.toml or use the built-in defaults.",
        )
    env_path = repo_root / ".env"
    credentials = DoctorCheck(
        "optional-credentials",
        "Subscription-only authentication",
        True,
        False,
        (
            ".env found; provider keys are ignored for model execution"
            if env_path.is_file()
            else "saved Claude and ChatGPT sign-ins; no API key required"
        ),
        "Use `claude auth login` and `codex login` for subscription access.",
    )
    return [configured, credentials]


def collect_doctor_checks(
    repo_root: Path = REPO_ROOT,
    *,
    environment: Mapping[str, str] | None = None,
    which: Which = shutil.which,
    runner: Runner = subprocess.run,
    disk_usage: Callable[[Path], object] = shutil.disk_usage,
    python_version: Sequence[int] | None = None,
) -> list[DoctorCheck]:
    """Inspect local prerequisites without a model call or filesystem write."""

    env = os.environ if environment is None else environment
    version = sys.version_info if python_version is None else python_version
    python = _python_check(version)
    claude_path = which("claude")
    codex_path = which("codex")
    claude_cli = DoctorCheck(
        "claude-cli",
        "Claude Code CLI",
        claude_path is not None,
        False,
        str(claude_path) if claude_path else "not found",
        "Install Claude Code: curl -fsSL https://claude.ai/install.sh | bash",
    )
    claude_auth = _claude_auth_check(
        claude_path, environment=env, runner=runner
    )
    claude_auth = replace(claude_auth, required=False)
    codex_cli = DoctorCheck(
        "codex-cli",
        "Codex CLI",
        codex_path is not None,
        False,
        str(codex_path) if codex_path else "not found",
        "Install Codex: curl -fsSL https://chatgpt.com/codex/install.sh | sh",
    )
    codex_auth = _codex_auth_check(
        codex_path, environment=env, runner=runner
    )
    provider = DoctorCheck(
        "report-provider",
        "Report model provider",
        claude_auth.ok or codex_auth.ok,
        True,
        (
            "Claude Fable 5 and GPT-5.6 Sol subscription sessions are ready"
            if claude_auth.ok and codex_auth.ok
            else "GPT-5.6 Sol ChatGPT subscription verified"
            if codex_auth.ok
            else "Claude Fable 5 authentication verified"
            if claude_auth.ok
            else "neither Claude nor ChatGPT subscription authentication is ready"
        ),
        "Run `claude auth login` or `codex login`.",
    )
    office = _tool_check(
        "libreoffice",
        "LibreOffice renderer",
        ("soffice", "libreoffice"),
        "macOS: brew install --cask libreoffice · Ubuntu: sudo apt install libreoffice",
        which=which,
    )
    poppler = _tool_check(
        "poppler",
        "Poppler PDF renderer",
        ("pdftoppm",),
        "macOS: brew install poppler · Ubuntu: sudo apt install poppler-utils",
        which=which,
    )
    return [
        python,
        claude_cli,
        claude_auth,
        codex_cli,
        codex_auth,
        provider,
        office,
        poppler,
        _package_check(),
        _workspace_check(repo_root),
        _disk_check(repo_root, disk_usage),
        *_configuration_checks(repo_root, env),
    ]


def render_doctor(checks: Sequence[DoctorCheck], *, console: Console) -> None:
    table = Table(title="Council doctor", show_lines=False, pad_edge=False)
    table.add_column("", width=2)
    table.add_column("Check", style="bold")
    table.add_column("Result")
    for check in checks:
        if check.ok:
            icon, style = "✓", "green"
        elif check.required:
            icon, style = "✗", "red"
        else:
            icon, style = "!", "yellow"
        detail = check.detail
        if not check.ok and check.fix:
            detail += f"\n[dim]{check.fix}[/dim]"
        table.add_row(f"[{style}]{icon}[/{style}]", check.label, detail)
    console.print(table)


def run_doctor(repo_root: Path = REPO_ROOT, *, console: Console | None = None) -> int:
    output = console or Console()
    checks = collect_doctor_checks(repo_root)
    render_doctor(checks, console=output)
    blockers = [check for check in checks if check.required and not check.ok]
    if blockers:
        output.print(
            f"\n[red]{len(blockers)} required check{'s' if len(blockers) != 1 else ''} failed.[/red] "
            "Fix the items above, then rerun [cyan]./council --doctor[/cyan]."
        )
        return 1
    output.print("\n[green]Ready for a Council report run.[/green]")
    return 0


__all__ = ["DoctorCheck", "collect_doctor_checks", "render_doctor", "run_doctor"]
