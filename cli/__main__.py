"""`council` CLI entry point.

Running `./council` with no flags opens the interactive hub — the intended
way to use the tool. Every capability (new run, resume, revise, decks,
publish, audit, settings) lives in the menu; flags are deep links into the
same flows for scripting and muscle memory.
"""
from __future__ import annotations

import argparse
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

console = Console()
REPO_ROOT = Path(__file__).resolve().parent.parent

# Load API keys from .env at the repo root (see .env.example). Shell exports
# take precedence — load_dotenv never overrides an existing environment var.
load_dotenv(REPO_ROOT / ".env")


# When ./council is launched from inside an active Claude Code session (a
# common case while developing this very tool!), env vars like CLAUDECODE=1,
# CLAUDE_CODE_CHILD_SESSION, and ANTHROPIC_BASE_URL get inherited by every
# `claude` subprocess the SDK spawns. The children detect the parent and
# refuse to do real work — they return immediately with the spurious
# `is_error: true / subtype: success` envelope, every turn, every agent,
# deterministically. Strip the inherited markers so child sessions boot as
# top-level invocations.
_PARENT_CLAUDE_ENV_VARS = (
    "CLAUDECODE",
    "CLAUDE_CODE_SESSION_ID",
    "CLAUDE_CODE_CHILD_SESSION",
    "CLAUDE_CODE_ENTRYPOINT",
    "CLAUDE_CODE_EXECPATH",
    "CLAUDE_CODE_OAUTH_SCOPES",
    "CLAUDE_CODE_ENABLE_ASK_USER_QUESTION_TOOL",
    "CLAUDE_CODE_EMIT_TOOL_USE_SUMMARIES",
    "CLAUDE_CODE_DISABLE_CRON",
    "CLAUDE_CODE_SDK_HAS_OAUTH_REFRESH",
    "CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH",
    "CLAUDE_AGENT_SDK_VERSION",
    "CLAUDE_EFFORT",
    "ANTHROPIC_BASE_URL",
)
_stripped_parent_env = [v for v in _PARENT_CLAUDE_ENV_VARS if v in os.environ]
for _v in _stripped_parent_env:
    os.environ.pop(_v, None)
if _stripped_parent_env:
    console.print(
        f"[dim]Detected a parent Claude Code session; stripped "
        f"{len(_stripped_parent_env)} inherited env var(s) so child sessions "
        f"boot cleanly.[/dim]"
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="council",
        description="Transform Airports AI Council. Run with no flags for the "
        "interactive hub; flags are deep links into the same flows.",
    )
    p.add_argument("--no-review", action="store_true",
                   help="Deep link: run autonomously (no checkpoints) where applicable.")
    p.add_argument("--dry-run", action="store_true",
                   help="Deep link: collect a new run spec, write the run file, stop.")
    p.add_argument("--skip-prompts", action="store_true", help="Alias for --dry-run.")
    p.add_argument("--resume", nargs="?", const="__detect__", metavar="SLUG",
                   help="Deep link: resume an interrupted run (auto-detected if no slug).")
    p.add_argument("--audit", action="store_true", help="Deep link: council audit.")
    p.add_argument("--publish", nargs="?", const="__all__", metavar="SLUG",
                   help="Deep link: re-publish archived runs (all, or one slug).")
    p.add_argument("--pptx", nargs="?", const="__pick__", metavar="SLUG",
                   help="Deep link: build an executive deck for a finished run.")
    p.add_argument("--revise", nargs="?", const="__pick__", metavar="SLUG",
                   help="Deep link: revise an existing report from reader feedback.")
    p.add_argument("--terminal", action="store_true",
                   help="Use the headless terminal menu instead of the web app "
                   "(for SSH / no-browser environments).")
    return p.parse_args(argv)


def _friendly_failure(exc: Exception) -> int:
    """Save the technical detail, show the human what to do next."""
    log_dir = REPO_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    log_path = log_dir / "last-error.log"
    log_path.write_text(
        f"{datetime.now().isoformat()}\n\n{traceback.format_exc()}",
        encoding="utf-8",
    )
    console.print(Panel(
        f"[bold]The run hit an error — your completed work is safe.[/bold]\n\n"
        f"{type(exc).__name__}: {exc}\n\n"
        f"Relaunch [cyan]./council[/cyan] and choose [bold]Resume[/bold] — "
        f"finished steps are skipped automatically.\n"
        f"[dim]Technical details: {log_path.relative_to(REPO_ROOT)}[/dim]",
        border_style="red",
        title="Run interrupted",
    ))
    return 1


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    from cli import menu

    try:
        if args.audit:
            menu.audit_flow()
            return 0

        if args.publish:
            menu.publish_flow(only_slug=None if args.publish == "__all__" else args.publish)
            return 0

        if args.pptx:
            menu.deck_flow()
            return 0

        if args.revise:
            menu.revise_flow(
                only_slug=None if args.revise == "__pick__" else args.revise,
                auto_approve=args.no_review,
            )
            return 0

        if args.resume:
            if args.resume != "__detect__":
                info = menu.detect_interrupted_run() or {}
                info["slug"] = args.resume
                menu.resume_flow(info if info.get("slug") else None)
            else:
                menu.resume_flow()
            return 0

        if args.dry_run or args.skip_prompts:
            from cli.agents import load_all_agents
            from cli.interactive import collect_run_spec
            from cli.runfile import ensure_unique_slug, write_run_file

            spec = collect_run_spec(load_all_agents())
            spec.slug = ensure_unique_slug(spec.slug)
            run_file = write_run_file(spec)
            console.print(
                f"[green]Run file written:[/green] {run_file.relative_to(REPO_ROOT)} "
                f"[dim](--dry-run: no model calls)[/dim]"
            )
            return 0

        if args.terminal:
            # Headless fallback: the old questionary hub, for SSH / no-browser.
            return menu.hub()

        # Default: launch the web app and open the browser.
        from cli.server import serve

        console.print(
            "[bold cyan]The AI Council[/bold cyan] is starting at "
            "[bold]http://127.0.0.1:8723[/bold] — opening your browser…\n"
            "[dim]Leave this terminal running. Press Ctrl-C to stop the server.[/dim]"
        )
        serve()
        return 0

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled.[/yellow]")
        return 130
    except Exception as e:  # noqa: BLE001 — translate to operator language
        from cli.orchestrator import RunBudgetExceeded

        if isinstance(e, RunBudgetExceeded):
            console.print(Panel(str(e), border_style="yellow", title="Budget ceiling"))
            return 3
        return _friendly_failure(e)


if __name__ == "__main__":
    sys.exit(main())
