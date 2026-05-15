"""`council` CLI entry point.

Interactive run-spec capture → write `prompts/runs/<slug>.md` →
drive the four-stage Council pipeline via the Claude Agent SDK →
write Word documents → archive to `runs/YYYY-MM-DD-<slug>/`.

Flags:
    --no-review     Skip both human checkpoints AND the initial spec-confirm.
                    Runs fully autonomously end-to-end.
    --dry-run       Build the run-spec and write the run file, then stop.
                    Useful for previewing the prompt without spending money.
    --skip-prompts  (Phase 1 behavior) Don't execute the pipeline; just write
                    the run file. Implied by --dry-run.
"""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

from rich.console import Console

from cli.agents import load_all_agents
from cli.interactive import collect_run_spec, confirm_spec
from cli.runfile import write_run_file

console = Console()
REPO_ROOT = Path(__file__).resolve().parent.parent


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="council",
        description="Transform Airports AI Council — interactive multi-agent runner.",
    )
    p.add_argument(
        "--no-review",
        action="store_true",
        help="Skip human checkpoints and the initial spec confirmation. Runs end-to-end without prompts.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Write the run file from your answers and stop. Does not call the model.",
    )
    p.add_argument(
        "--skip-prompts",
        action="store_true",
        help="Alias for --dry-run.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        agents = load_all_agents()
        spec = collect_run_spec(agents)

        if args.no_review:
            console.print("[dim]--no-review: skipping spec confirmation.[/dim]")
        elif not confirm_spec(spec):
            console.print("[yellow]Aborted. No file written.[/yellow]")
            return 1

        run_file = write_run_file(spec)
        rel = run_file.relative_to(REPO_ROOT)
        console.print(f"[green]Wrote run file:[/green] {rel}")

        if args.dry_run or args.skip_prompts:
            console.print("[dim]--dry-run: stopping before model calls.[/dim]")
            return 0

        from cli.orchestrator import run_pipeline

        tally = asyncio.run(
            run_pipeline(
                spec=spec,
                run_file=run_file,
                repo_root=REPO_ROOT,
                auto_approve=args.no_review,
            )
        )
        console.print(f"[green]Run complete. Total estimated cost: ${tally.total:.2f}[/green]")
        return 0
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled.[/yellow]")
        return 130
    except FileExistsError as e:
        console.print(f"[red]{e}[/red]")
        return 2
    except Exception as e:
        console.print(f"[red]Unhandled error: {e}[/red]")
        raise


if __name__ == "__main__":
    sys.exit(main())
