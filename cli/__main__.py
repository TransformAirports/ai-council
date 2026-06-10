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
from cli.interactive import choose_mode, collect_run_spec, confirm_spec
from cli.runfile import RUNS_DIR, parse_run_file, write_run_file

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
    p.add_argument(
        "--resume",
        metavar="SLUG",
        help="Resume a previously interrupted run. Reads prompts/runs/<SLUG>.md, "
        "keeps existing outputs/ artifacts, and re-runs only the steps whose "
        "output files are missing or empty. Skips the interactive prompts.",
    )
    p.add_argument(
        "--audit",
        action="store_true",
        help="Scan all archived runs under runs/ and produce a council-audit "
        "report identifying which agents are underused, which produce the most "
        "fact-check rejections, and which have never been seated. Writes the "
        "report to runs/_audit-YYYY-MM-DD.md and exits.",
    )
    p.add_argument(
        "--publish",
        nargs="?",
        const="__all__",
        metavar="SLUG",
        help="Format the full reports in runs/*/stage4 into polished, "
        "distribution-ready documents under reports/. Each gets a cover page, "
        "abstract, a page explaining the Council process and the agents used, "
        "page numbers, and an AI-generation disclaimer. Pass a SLUG to publish "
        "just one run; omit it to publish every archived run. Exits when done.",
    )
    p.add_argument(
        "--pptx",
        action="store_true",
        help="Also generate a companion executive PowerPoint after Stage 4 "
        "(presentation-designer agent on Fable 5). The deck lands in the run "
        "archive alongside the Word documents.",
    )
    p.add_argument(
        "--revise",
        nargs="?",
        const="__pick__",
        metavar="SLUG",
        help="Revise an existing report from new reader feedback. Reuses the "
        "original research briefs and runs a focused Strategist/Red Team/Editor/"
        "Fact-checker loop on the existing draft plus your feedback, producing "
        "reports/<slug>-revised-vN.docx. Pass a SLUG to target one report; omit "
        "it to pick from a list.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        if args.audit:
            from cli.audit import audit_runs, render_audit_report, write_audit_report

            agents = load_all_agents()
            result = audit_runs(agents=agents)
            report = render_audit_report(result, agents)
            console.print(report)
            if result["runs"]:
                out_path = write_audit_report(report)
                console.print(
                    f"\n[green]Audit written to:[/green] {out_path.relative_to(REPO_ROOT)}"
                )
            return 0

        if args.publish:
            from cli.publish import publish_all

            only = None if args.publish == "__all__" else args.publish
            scope = f"run '{only}'" if only else "all archived runs"
            console.print(f"[cyan]Publishing polished reports for {scope}…[/cyan]")
            results = publish_all(only_slug=only)
            if not results:
                console.print(
                    "[yellow]No matching reports found under runs/*/stage4.[/yellow]"
                )
                return 1
            ok = 0
            for slug, out_path, status in results:
                if status == "ok" and out_path is not None:
                    console.print(
                        f"  [green]✓[/green] {slug} → {out_path.relative_to(REPO_ROOT)}"
                    )
                    ok += 1
                else:
                    console.print(f"  [red]✗[/red] {slug} — {status}")
            console.print(
                f"[green]Published {ok} of {len(results)} report(s) to reports/.[/green]"
            )
            return 0 if ok else 2

        # Decide between creating a new report and revising an existing one.
        # An explicit --revise flag wins; --resume stays the new-run resume path;
        # otherwise ask interactively.
        do_revise = False
        revise_slug = None
        if args.revise is not None:
            do_revise = True
            revise_slug = None if args.revise == "__pick__" else args.revise
        elif not args.resume:
            do_revise = choose_mode() == "revise"

        if do_revise:
            from cli.orchestrator import run_revision_pipeline
            from cli.revise import collect_revision_request

            request = collect_revision_request(only_slug=revise_slug)
            if request is None:
                return 1
            if args.dry_run or args.skip_prompts:
                console.print(
                    "[dim]--dry-run: feedback captured; stopping before model calls.[/dim]"
                )
                return 0
            out_path, tally = asyncio.run(
                run_revision_pipeline(
                    request=request,
                    repo_root=REPO_ROOT,
                    auto_approve=args.no_review,
                )
            )
            if out_path is None:
                console.print(
                    f"[yellow]Revision stopped. Cost so far: ${tally.total:.2f}[/yellow]"
                )
                return 0
            console.print(
                f"[green]Revision v{request.version} complete. "
                f"Total estimated cost: ${tally.total:.2f}[/green]"
            )
            return 0

        if args.resume:
            spec = parse_run_file(args.resume)
            run_file = RUNS_DIR / f"{args.resume}.md"
            console.print(
                f"[cyan]Resuming run: {args.resume}[/cyan] "
                f"[dim]({len(spec.selected_research_agents)} research agents seated)[/dim]"
            )
        else:
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

        if args.pptx:
            spec.want_pptx = True

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
                resume=bool(args.resume),
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
