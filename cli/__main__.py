"""`council` CLI entry point.

Running `./council` with no flags opens the interactive hub — the intended
way to use the tool. Every capability (new run, resume, revise, decks,
publish, audit, settings) lives in the menu; flags are deep links into the
same flows for scripting and muscle memory.
"""
from __future__ import annotations

import argparse
import math
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()
REPO_ROOT = Path(__file__).resolve().parent.parent

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
    # Council model execution is subscription-only. Removing these prevents a
    # forgotten shell export from changing the billing route.
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
)
_stripped_parent_env = [v for v in _PARENT_CLAUDE_ENV_VARS if v in os.environ]
for _v in _stripped_parent_env:
    os.environ.pop(_v, None)
if _stripped_parent_env:
    console.print(
        f"[dim]Removed {len(_stripped_parent_env)} inherited session or API-key "
        f"environment variable(s); Council model calls use saved subscription "
        f"sign-ins.[/dim]"
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
    p.add_argument("--run", metavar="FILE",
                   help="Run an existing prompt from prompts/runs/ through the canonical pipeline.")
    p.add_argument("--budget", type=float, metavar="USD",
                   help="Budget ceiling for --run; defaults to council.toml.")
    p.add_argument("--resume", nargs="?", const="__detect__", metavar="SLUG",
                   help="Deep link: resume an interrupted run (auto-detected if no slug).")
    p.add_argument("--audit", action="store_true", help="Deep link: council audit.")
    p.add_argument(
        "--doctor",
        action="store_true",
        help="Check authentication, renderers, disk, configuration, and local dependencies without a model call.",
    )
    p.add_argument("--publish", nargs="?", const="__all__", metavar="SLUG",
                   help="Deep link: re-publish archived runs (all, or one slug).")
    p.add_argument(
        "--allow-legacy-publish",
        action="store_true",
        help="Allow --publish to re-QA and publish a pre-v2 archive that has "
        "no hash-bound release bundle.",
    )
    p.add_argument("--pptx", nargs="?", const="__pick__", metavar="SLUG",
                   help="Deep link: build an executive deck for a finished run.")
    p.add_argument("--revise", nargs="?", const="__pick__", metavar="SLUG",
                   help="Deep link: revise an existing report from reader feedback.")
    p.add_argument("--terminal", action="store_true",
                   help="Use the headless terminal menu instead of the web app "
                   "(for SSH / no-browser environments).")
    p.add_argument("--scope", metavar="TITLE",
                   help="Deep link: fulfill a client scope of work headlessly. "
                   "Drop the scope document into sources/ first. Combine with "
                   "--no-review to run without checkpoints; without it, use the "
                   "web app so the plan-approval checkpoint has a UI.")
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

    try:
        if args.doctor:
            from cli.doctor import run_doctor

            return run_doctor(REPO_ROOT, console=console)

        from cli import menu

        if args.run and (args.dry_run or args.skip_prompts):
            console.print(
                "[red]--run cannot be combined with --dry-run or "
                "--skip-prompts.[/red] No model calls were made."
            )
            return 2

        if args.audit:
            menu.audit_flow()
            return 0

        if args.publish:
            published = menu.publish_flow(
                only_slug=None if args.publish == "__all__" else args.publish,
                allow_legacy=args.allow_legacy_publish,
            )
            return 0 if published else 1

        if args.allow_legacy_publish:
            console.print(
                "[red]--allow-legacy-publish is valid only with --publish.[/red]"
            )
            return 2

        if args.run:
            import asyncio

            from cli.config import get_config
            from cli.orchestrator import run_pipeline
            from cli.runfile import (
                parse_run_file,
                resolve_run_file,
                validate_run_file,
            )

            try:
                run_file = resolve_run_file(args.run)
            except (FileNotFoundError, ValueError) as exc:
                console.print(
                    Panel(
                        str(exc),
                        border_style="red",
                        title="Run prompt not found",
                    )
                )
                return 2
            errors = validate_run_file(run_file)
            if errors:
                console.print(Panel(
                    "\n".join(f"• {error}" for error in errors),
                    border_style="red",
                    title="Run prompt is not ready",
                ))
                return 2
            spec = parse_run_file(run_file.stem, runs_dir=run_file.parent)
            from cli.codex_subscription import codex_subscription_status
            from cli.council_models import council_model

            selected_model = council_model(getattr(spec, "council_model", ""))
            if selected_model is not None and selected_model.provider == "openai":
                codex_status = codex_subscription_status()
                if not codex_status.authenticated:
                    console.print(
                        Panel(
                            "Run `codex login`, complete the ChatGPT browser sign-in, "
                            "then relaunch ./council.",
                            border_style="red",
                            title="ChatGPT authentication required",
                        )
                    )
                    return 2
            elif (
                "deep-research" in spec.selected_research_agents
                and not codex_subscription_status().authenticated
            ):
                console.print(
                    "[red]This legacy prompt seats Deep Research, but Codex is not "
                    "signed in with ChatGPT. Run `codex login`.[/red]"
                )
                return 2
            if selected_model is None or selected_model.provider == "anthropic":
                auth_ok, auth_message = menu.check_claude_auth()
                if not auth_ok:
                    console.print(
                        Panel(auth_message, border_style="red", title="Authentication required")
                    )
                    return 2
            ceiling = args.budget
            if ceiling is None:
                ceiling = get_config().default_budget_usd
            if ceiling is not None and (
                not math.isfinite(ceiling) or ceiling < 0
            ):
                console.print(
                    "[red]--budget must be a finite number, zero or greater.[/red]"
                )
                return 2
            result = asyncio.run(run_pipeline(
                spec=spec,
                run_file=run_file,
                repo_root=REPO_ROOT,
                auto_approve=args.no_review,
                budget_usd=ceiling,
            ))
            return 0 if result.completed else 1

        if args.pptx:
            from cli.config import get_config

            ceiling = args.budget
            if ceiling is None:
                ceiling = get_config().default_budget_usd
            if ceiling is not None and (
                not math.isfinite(ceiling) or ceiling < 0
            ):
                console.print(
                    "[red]--budget must be a finite number, zero or greater.[/red]"
                )
                return 2
            built = menu.deck_flow(
                only_slug=None if args.pptx == "__pick__" else args.pptx,
                budget_usd=ceiling,
            )
            return 0 if built else 1

        if args.revise:
            menu.revise_flow(
                only_slug=None if args.revise == "__pick__" else args.revise,
                auto_approve=args.no_review,
            )
            return 0

        if args.resume:
            if args.resume != "__detect__":
                info = menu.detect_interrupted_run()
                if info is None:
                    console.print("[yellow]No interrupted run found in outputs/.[/yellow]")
                    return 2
                active_slug = info.get("slug")
                if active_slug != args.resume:
                    console.print(
                        "[red]Resume refused:[/red] outputs/ belongs to "
                        f"`{active_slug or 'an unidentified legacy run'}`, not "
                        f"`{args.resume}`. Existing artifacts were left untouched."
                    )
                    return 2
                menu.resume_flow(
                    info,
                    auto_approve=args.no_review,
                    budget_usd=args.budget,
                )
            else:
                menu.resume_flow(
                    auto_approve=args.no_review,
                    budget_usd=args.budget,
                )
            return 0

        if args.scope:
            import asyncio

            if not args.no_review:
                console.print(
                    "[yellow]--scope without --no-review needs the web app for the "
                    "plan-approval checkpoint. Launch ./council and use 'Fulfill a "
                    "scope', or add --no-review to run fully autonomously.[/yellow]"
                )
                return 1
            from cli.scope import run_scope_pipeline

            result = asyncio.run(run_scope_pipeline(
                title=args.scope, auto_approve=True,
            ))
            if result.completed:
                console.print(
                    f"[green]Engagement complete — {result.zip_path} "
                    f"(${result.tally.total:.2f})[/green]"
                )
            return 0 if result.completed else 1

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
