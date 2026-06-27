"""The Council's interactive hub — everything runs from here.

`./council` with no flags lands on a branded menu that detects interrupted
runs, walks the operator through new runs with a single pre-flight screen,
and closes every loop (publish, decks, revisions, audit, settings) without
requiring a single flag. Flags still exist as deep links for scripting.
"""
from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cli.agents import (
    load_all_agents,
    research_agents,
    standard_research_agents,
    supplemental_agents,
)
from cli.config import MODEL_CHOICES, get_config, save_config
from cli.sources import (
    DROPZONE,
    attach_sources,
    discover_dropzone,
    format_size,
)

console = Console()
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = REPO_ROOT / "outputs"

FORMAT_TITLES = {
    "report": "Full Research Report",
    "article": "Long-Form Article",
    "brief": "Brief",
    "recommendations": "Concise Recommendations",
}


# ----------------------------------------------------------------------------
# Banner and status.
# ----------------------------------------------------------------------------

def _archive_stats() -> tuple[int, str | None]:
    runs_dir = REPO_ROOT / "runs"
    if not runs_dir.is_dir():
        return 0, None
    archives = sorted(
        p.name for p in runs_dir.iterdir()
        if p.is_dir() and p.name[:4].isdigit()
    )
    return len(archives), (archives[-1] if archives else None)


def banner() -> None:
    agents = load_all_agents()
    n_standard = len(standard_research_agents(agents))
    n_suppl = len(supplemental_agents(agents))
    n_archives, last = _archive_stats()
    body = Text()
    body.append("THE AI COUNCIL\n", style="bold white")
    body.append("Transform Airports — research, argued.\n\n", style="dim")
    body.append(f"{n_standard} research lenses (+{n_suppl} supplemental) · "
                f"6 process agents · {n_archives} completed runs", style="cyan")
    if last:
        body.append(f"\nlatest: {last}", style="dim")
    dropped = discover_dropzone()
    if dropped:
        body.append(
            f"\n📎  {len(dropped)} source file{'s' if len(dropped) != 1 else ''} "
            f"staged in sources/ — included in the next New run",
            style="green",
        )
    console.print(Panel(body, border_style="blue", padding=(1, 4)))


# ----------------------------------------------------------------------------
# Interrupted-run detection.
# ----------------------------------------------------------------------------

def detect_interrupted_run() -> dict | None:
    """Return info about a partially-completed run sitting in outputs/, or None.

    A run is "interrupted" if either:
      - there are partial artifacts under outputs/stage*, OR
      - the .active-run.json marker exists (a run was launched but never
        reached archive — covers the case where Stage 1 died so early that
        no briefs wrote, e.g. an immediate model-not-found error).
    """
    from cli.orchestrator import read_run_marker

    stage_counts: dict[str, int] = {}
    newest = 0.0
    for sub in ("stage1", "stage2", "stage3", "stage4"):
        d = OUTPUTS_DIR / sub
        files = [p for p in d.glob("*") if p.is_file()] if d.is_dir() else []
        stage_counts[sub] = len(files)
        for p in files:
            try:
                newest = max(newest, p.stat().st_mtime)
            except OSError:
                pass

    marker = read_run_marker(OUTPUTS_DIR) or {}
    has_any_artifact = any(stage_counts.values())
    has_marker = bool(marker)

    if not has_any_artifact and not has_marker:
        return None

    if stage_counts["stage3"]:
        where = "died during Stage 3–4"
    elif stage_counts["stage2"]:
        where = f"died during Stage 2 ({stage_counts['stage2']} of 5 drafts done)"
    elif stage_counts["stage1"]:
        where = f"died during Stage 1 ({stage_counts['stage1']} briefs done)"
    else:
        where = "died at Stage 1 startup (no briefs written yet)"

    # Use the marker's start time when there are no files to read mtime from.
    if not newest and marker.get("started"):
        try:
            newest = datetime.fromisoformat(marker["started"]).timestamp()
        except (ValueError, TypeError):
            pass
    age = ""
    if newest:
        hours = (datetime.now() - datetime.fromtimestamp(newest)).total_seconds() / 3600
        age = f"{hours:.0f}h ago" if hours >= 1 else f"{hours * 60:.0f}m ago"

    return {
        "slug": marker.get("slug"),
        "title": marker.get("title") or marker.get("slug") or "unknown run",
        "where": where,
        "age": age,
        "has_expensive_work": bool(stage_counts["stage2"] or stage_counts["stage3"]),
        "stage_counts": stage_counts,
    }


def _clear_outputs_dir() -> None:
    from cli.archive import _clear_outputs

    _clear_outputs(OUTPUTS_DIR)


def _guard_clear(info: dict) -> bool:
    """Make destroying Opus-stage work require intent, not a stray Enter."""
    if not info["has_expensive_work"]:
        return bool(questionary.confirm(
            f"outputs/ holds Stage 1 work from '{info['title']}'. Clear it?",
            default=False,
        ).ask())
    console.print(
        f"[yellow]outputs/ holds synthesis work from '{info['title']}' "
        f"({info['where']}). Clearing deletes paid Opus output.[/yellow]"
    )
    typed = questionary.text("Type CLEAR to confirm (anything else cancels):").ask()
    return (typed or "").strip().upper() == "CLEAR"


# ----------------------------------------------------------------------------
# Pre-flight.
# ----------------------------------------------------------------------------

_auth_probe_cache: tuple[bool, str] | None = None


def check_claude_auth(force: bool = False) -> tuple[bool, str]:
    """Verify Claude can actually authenticate, by probing the real CLI.

    The only reliable check is to run a tiny `claude -p` call and see if it
    succeeds — credentials may live in the macOS Keychain, a file, or an env
    key, and inferring from any one location gives false answers (an expired
    file with a valid Keychain token, or vice versa). We test the ground truth.

    Returns (ok, human_message). Result is cached for the session so the
    pre-flight screen can redraw without re-probing. Pass force=True to re-probe
    after a `claude login`.

    Philosophy: block ONLY on a confirmed failure (a 401, or no CLI at all).
    Never block on an inconclusive probe — that would be as bad as the bug it
    replaces. If the probe is ambiguous, allow the run; Stage 1 will surface a
    real problem with a clear message.
    """
    global _auth_probe_cache
    if _auth_probe_cache is not None and not force:
        return _auth_probe_cache

    if os.environ.get("ANTHROPIC_API_KEY"):
        _auth_probe_cache = (True, "API key (pay-as-you-go)")
        return _auth_probe_cache

    import subprocess

    claude = shutil.which("claude")
    if not claude:
        _auth_probe_cache = (
            False,
            "⚠ Claude CLI not found — install Claude Code or set ANTHROPIC_API_KEY",
        )
        return _auth_probe_cache

    try:
        with console.status("[dim]Checking Claude authentication…[/dim]"):
            proc = subprocess.run(
                [claude, "-p", "Reply with exactly: PONG", "--max-turns", "1"],
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=90,
            )
        blob = f"{proc.stdout}\n{proc.stderr}"
        if "PONG" in blob:
            _auth_probe_cache = (True, "authenticated (verified just now)")
        elif "401" in blob or "authenticat" in blob.lower():
            _auth_probe_cache = (
                False,
                "⚠ authentication failed (401) — run `claude login`",
            )
        else:
            # Reached the model but got an unexpected reply — not an auth
            # problem; let the run proceed.
            _auth_probe_cache = (True, "reachable (probe reply unexpected; proceeding)")
    except subprocess.TimeoutExpired:
        _auth_probe_cache = (
            True,
            "auth probe timed out — proceeding (Stage 1 will report any real issue)",
        )
    except OSError as e:
        _auth_probe_cache = (True, f"auth probe could not run ({e}); proceeding")
    return _auth_probe_cache


def _auth_lines(spec) -> list[tuple[str, str]]:
    ok, msg = check_claude_auth()
    lines: list[tuple[str, str]] = [("Claude", msg)]
    if "deep-research" in spec.selected_research_agents:
        if os.environ.get("OPENAI_API_KEY"):
            lines.append(("OpenAI", "API key set (Deep Research bills to OpenAI)"))
        else:
            lines.append(("OpenAI", "⚠ OPENAI_API_KEY missing — Deep Research will fail"))
    return lines


def estimate_cost(spec) -> tuple[float, float]:
    """Rough range calibrated against archived runs' actual tallies."""
    n = len([a for a in spec.selected_research_agents if a != "deep-research"])
    low = 1.5 * n + 7
    high = 4.0 * n + 19
    if getattr(spec, "want_pptx", False):
        low += 1
        high += 4
    return round(low), round(high)


def preflight(spec) -> dict | None:
    """One screen, sensible defaults, single keystroke to launch.

    Returns {"auto_approve": bool, "budget_usd": float|None} or None to cancel.
    """
    cfg = get_config()
    checkpoints_on = True
    budget: float | None = cfg.default_budget_usd or None

    # Hard gate: dead Claude auth makes every agent 401 at "1 turn / $0.00".
    # Catch it here, before a single dollar or minute is spent.
    auth_ok, auth_msg = check_claude_auth()
    if not auth_ok:
        console.print(Panel(
            f"[bold]Claude isn't authenticated, so the run can't proceed.[/bold]\n\n"
            f"{auth_msg}\n\n"
            f"Fix it in one step:\n"
            f"  [cyan]claude login[/cyan]\n\n"
            f"Verify with:  [cyan]claude -p \"say PONG\" --max-turns 1[/cyan]\n"
            f"Then relaunch [cyan]./council[/cyan] and choose Resume.",
            border_style="red", title="Authentication required",
        ))
        return None

    # Hard gate: Deep Research seated without a key fails an hour in. Fix now.
    if "deep-research" in spec.selected_research_agents and not os.environ.get("OPENAI_API_KEY"):
        action = questionary.select(
            "Deep Research is seated but OPENAI_API_KEY is not set:",
            choices=["Unseat Deep Research and continue", "Cancel the run"],
        ).ask()
        if action is None or action.startswith("Cancel"):
            return None
        spec.selected_research_agents.remove("deep-research")

    while True:
        low, high = estimate_cost(spec)
        t = Table(show_header=False, box=None, padding=(0, 2))
        t.add_row("[bold]Title[/bold]", spec.title)
        t.add_row("[bold]Format[/bold]", FORMAT_TITLES.get(spec.output_format, spec.output_format))
        roster = ", ".join(spec.selected_research_agents[:6])
        extra = len(spec.selected_research_agents) - 6
        if extra > 0:
            roster += f"  +{extra} more"
        t.add_row(f"[bold]Council[/bold] ({len(spec.selected_research_agents)})", roster)
        t.add_row(
            "[bold]Models[/bold]",
            f"research {cfg.model('research')} · synthesis {cfg.model('synthesis')} · "
            f"critique/edit {cfg.model('critique')}",
        )
        t.add_row("[bold]Estimated cost[/bold]", f"${low}–${high}" + (
            "  (+ Deep Research on OpenAI)" if "deep-research" in spec.selected_research_agents else ""))
        t.add_row("[bold]Checkpoints[/bold]", "on — pause for your review twice" if checkpoints_on else "off — fully autonomous")
        t.add_row("[bold]Budget ceiling[/bold]", f"${budget:.0f}" if budget else "none")
        t.add_row("[bold]Companion deck[/bold]", "yes" if getattr(spec, "want_pptx", False) else "no")
        if getattr(spec, "source_paths", None):
            srcs = spec.source_paths
            preview = ", ".join(Path(p).name for p in srcs[:3])
            if len(srcs) > 3:
                preview += f"  +{len(srcs) - 3} more"
            t.add_row(f"[bold]📎 Sources[/bold] ({len(srcs)})", preview)
        for label, value in _auth_lines(spec):
            style = "red" if "⚠" in value else ""
            t.add_row(f"[bold]{label}[/bold]", f"[{style}]{value}[/{style}]" if style else value)
        console.print(Panel(t, title="[bold]Pre-flight[/bold]", border_style="green"))

        choice = questionary.select(
            "Ready?",
            choices=["🚀  Launch", "⚙  Adjust (checkpoints / budget / deck)", "✕  Cancel"],
        ).ask()
        if choice is None or choice.startswith("✕"):
            return None
        if choice.startswith("🚀"):
            return {"auto_approve": not checkpoints_on, "budget_usd": budget}

        checkpoints_on = bool(questionary.confirm(
            "Pause at the two human checkpoints?", default=checkpoints_on
        ).ask())
        raw = questionary.text(
            f"Budget ceiling in USD (Enter for {f'${budget:.0f}' if budget else 'none'}, 0 for none):",
        ).ask()
        if raw and raw.strip():
            try:
                val = float(raw.strip().lstrip("$"))
                budget = val if val > 0 else None
            except ValueError:
                pass
        spec.want_pptx = bool(questionary.confirm(
            "Generate a companion executive deck?", default=getattr(spec, "want_pptx", False)
        ).ask())


# ----------------------------------------------------------------------------
# Flows.
# ----------------------------------------------------------------------------

def _open(path: Path) -> None:
    try:
        subprocess.run(["open", str(path)], check=False)
    except OSError:
        console.print(f"[yellow]Could not open {path}[/yellow]")


def post_run_menu(spec, result) -> None:
    """Close the loop after a completed run instead of dead-ending."""
    from cli.orchestrator import run_presentation_for_archive

    while True:
        choices = []
        if result.published_path:
            choices.append("📄  Open the published report")
        if result.deck_path:
            choices.append("📊  Open the deck")
        elif result.archive_path:
            choices.append("📊  Generate a companion deck")
        if result.archive_path:
            choices.append("🗂   Open the archive folder")
        choices += ["✎  Start a revision of this report", "←  Back to menu"]
        choice = questionary.select("What next?", choices=choices).ask()
        if choice is None or choice.startswith("←"):
            return
        if choice.startswith("📄"):
            _open(result.published_path)
        elif "Open the deck" in choice:
            _open(result.deck_path)
        elif "Generate" in choice:
            result.deck_path = asyncio.run(run_presentation_for_archive(
                archive_dir=result.archive_path, slug=spec.slug,
                title=spec.title, repo_root=REPO_ROOT,
            ))
        elif choice.startswith("🗂"):
            _open(result.archive_path)
        elif choice.startswith("✎"):
            revise_flow(only_slug=spec.slug)
            return


def _prompt_sources() -> list[Path]:
    """Detect dropzone contents and ask whether to attach them.

    Returns the list of files the operator wants to include (possibly empty).
    """
    dropped = discover_dropzone()
    if not dropped:
        return []
    t = Table(show_header=False, box=None, padding=(0, 2))
    for p in dropped:
        try:
            size = format_size(p.stat().st_size)
        except OSError:
            size = "—"
        t.add_row(f"  • {p.name}", f"[dim]{size}[/dim]")
    console.print(Panel(
        t,
        title="[bold]📎  Source material detected in sources/[/bold]",
        border_style="green",
    ))
    answer = questionary.select(
        "Include these as source material for this run?",
        choices=[
            "Yes — attach all and use them as the starting point",
            "No — ignore them this run (they stay in sources/)",
            "Cancel the new run",
        ],
    ).ask()
    if answer is None or answer.startswith("Cancel"):
        raise KeyboardInterrupt
    return dropped if answer.startswith("Yes") else []


def new_run_flow() -> None:
    from cli.interactive import collect_run_spec
    from cli.orchestrator import run_pipeline
    from cli.runfile import ensure_unique_slug, write_run_file

    interrupted = detect_interrupted_run()
    if interrupted:
        console.print(
            f"[yellow]Heads up: an interrupted run ('{interrupted['title']}', "
            f"{interrupted['where']}) is sitting in outputs/.[/yellow]"
        )
        if not _guard_clear(interrupted):
            console.print("[dim]Keeping it. Use Resume from the main menu instead.[/dim]")
            return
        _clear_outputs_dir()

    # Detect source material BEFORE the thesis flow — so the operator's
    # thesis answer can refer to the files they just attached.
    sources_to_attach = _prompt_sources()

    agents = load_all_agents()
    spec = collect_run_spec(agents)
    unique = ensure_unique_slug(spec.slug)
    if unique != spec.slug:
        console.print(f"[dim]Slug '{spec.slug}' exists — using '{unique}'.[/dim]")
        spec.slug = unique

    # Now that the slug is settled, move sources into outputs/sources/<slug>/
    # and extract office formats. The drop zone is left empty for the next run.
    if sources_to_attach:
        attached = attach_sources(spec.slug, sources_to_attach, REPO_ROOT / "outputs")
        spec.source_paths = [
            s.readable.relative_to(REPO_ROOT).as_posix() for s in attached
        ]
        console.print(
            f"[green]📎  Attached {len(attached)} source file"
            f"{'s' if len(attached) != 1 else ''} to '{spec.slug}'.[/green]"
        )
        for s in attached:
            tag = " [dim](extracted)[/dim]" if s.extracted else ""
            console.print(f"   • {s.original.name}{tag}")

    launch = preflight(spec)
    if launch is None:
        console.print("[yellow]Cancelled. Nothing written, nothing spent.[/yellow]")
        return

    run_file = write_run_file(spec)
    console.print(f"[green]Run file:[/green] {run_file.relative_to(REPO_ROOT)}")
    result = asyncio.run(run_pipeline(
        spec=spec, run_file=run_file, repo_root=REPO_ROOT,
        auto_approve=launch["auto_approve"], budget_usd=launch["budget_usd"],
    ))
    console.print(f"[bold green]Done. Total cost: ${result.tally.total:.2f}[/bold green]")
    if result.completed:
        post_run_menu(spec, result)


def resume_flow(info: dict | None = None) -> None:
    from cli.orchestrator import run_pipeline
    from cli.runfile import RUNS_DIR, parse_run_file

    info = info or detect_interrupted_run()
    if info is None:
        console.print("[yellow]No interrupted run found in outputs/.[/yellow]")
        return
    slug = info.get("slug")
    if not slug:
        # Pre-marker interruption: ask which run file it belongs to.
        candidates = sorted(p.stem for p in RUNS_DIR.glob("*.md") if p.stem != "_template")
        slug = questionary.select(
            "Which run does the interrupted work belong to?", choices=candidates
        ).ask()
        if slug is None:
            return
    spec = parse_run_file(slug)
    run_file = RUNS_DIR / f"{slug}.md"
    console.print(
        f"[cyan]Resuming '{spec.title}'[/cyan] [dim]— completed steps are skipped, "
        f"only missing work re-runs.[/dim]"
    )
    launch = preflight(spec)
    if launch is None:
        return
    result = asyncio.run(run_pipeline(
        spec=spec, run_file=run_file, repo_root=REPO_ROOT,
        auto_approve=launch["auto_approve"], budget_usd=launch["budget_usd"],
        resume=True,
    ))
    console.print(f"[bold green]Done. Total cost this session: ${result.tally.total:.2f}[/bold green]")
    if result.completed:
        post_run_menu(spec, result)


def revise_flow(only_slug: str | None = None, auto_approve: bool = False) -> None:
    from cli.orchestrator import run_revision_pipeline
    from cli.revise import collect_revision_request

    request = collect_revision_request(only_slug=only_slug)
    if request is None:
        return
    out_path, tally = asyncio.run(run_revision_pipeline(
        request=request, repo_root=REPO_ROOT, auto_approve=auto_approve,
    ))
    if out_path is not None:
        console.print(
            f"[bold green]Revision v{request.version} complete "
            f"(${tally.total:.2f}).[/bold green]"
        )
        if questionary.confirm("Open the revised document?", default=True).ask():
            _open(out_path)


def deck_flow() -> None:
    from cli.orchestrator import run_presentation_for_archive
    from cli.publish import discover_reports

    sources = [s for s in discover_reports() if s.final_md is not None]
    if not sources:
        console.print("[yellow]No archived runs available.[/yellow]")
        return
    pick = questionary.select(
        "Build an executive deck for which report?",
        choices=[s.slug for s in sources],
    ).ask()
    if pick is None:
        return
    src = next(s for s in sources if s.slug == pick)
    title = pick.replace("-", " ").title()
    if src.run_file is not None:
        for line in src.run_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("# Run:"):
                title = line[len("# Run:"):].strip()
                break
    deck = asyncio.run(run_presentation_for_archive(
        archive_dir=src.archive_dir, slug=pick, title=title, repo_root=REPO_ROOT,
    ))
    if questionary.confirm("Open the deck?", default=True).ask():
        _open(deck)


def publish_flow(only_slug: str | None = None) -> None:
    from cli.publish import publish_all

    results = publish_all(only_slug=only_slug)
    if not results:
        console.print("[yellow]No matching archived runs found.[/yellow]")
        return
    for slug, out_path, status in results:
        if status == "ok" and out_path is not None:
            console.print(f"  [green]✓[/green] {slug} → {out_path.relative_to(REPO_ROOT)}")
        else:
            console.print(f"  [red]✗[/red] {slug} — {status}")


def audit_flow() -> None:
    from cli.audit import audit_runs, render_audit_report, write_audit_report

    agents = load_all_agents()
    result = audit_runs(agents=agents)
    report = render_audit_report(result, agents)
    console.print(report)
    if result["runs"]:
        out = write_audit_report(report)
        console.print(f"\n[green]Saved:[/green] {out.relative_to(REPO_ROOT)}")


def settings_menu() -> None:
    while True:
        cfg = get_config()
        t = Table(show_header=False, box=None, padding=(0, 2))
        for role in ("research", "synthesis", "critique", "editor", "humanizer",
                     "factcheck", "presentation", "openai_deep_research"):
            t.add_row(f"[bold]{role}[/bold]", cfg.model(role))
        t.add_row("[bold]max_turns[/bold]", str(cfg.max_turns))
        t.add_row("[bold]default budget[/bold]", f"${cfg.default_budget_usd:g}")
        t.add_row("[bold]default format[/bold]", cfg.default_format)
        console.print(Panel(t, title="[bold]Settings — council.toml[/bold]", border_style="blue"))

        choice = questionary.select(
            "Change:",
            choices=["A model assignment", "Turn budget (max_turns)",
                     "Default budget ceiling", "←  Back"],
        ).ask()
        if choice is None or choice.startswith("←"):
            return
        if choice.startswith("A model"):
            role = questionary.select(
                "Which role?",
                choices=["research", "synthesis", "critique", "editor",
                         "humanizer", "factcheck", "presentation"],
            ).ask()
            if role is None:
                continue
            model = questionary.select(
                f"Model for {role}:", choices=MODEL_CHOICES + ["custom…"]
            ).ask()
            if model == "custom…":
                model = (questionary.text("Model ID:").ask() or "").strip()
            if model:
                cfg.models[role] = model
                save_config(cfg)
        elif choice.startswith("Turn"):
            raw = questionary.text(f"max_turns (now {cfg.max_turns}):").ask()
            if raw and raw.strip().isdigit() and int(raw) > 0:
                cfg.max_turns = int(raw)
                save_config(cfg)
        elif choice.startswith("Default budget"):
            raw = questionary.text(
                f"Default ceiling in USD (now ${cfg.default_budget_usd:g}, 0 = none):"
            ).ask()
            try:
                cfg.default_budget_usd = max(0.0, float((raw or "").strip().lstrip("$")))
                save_config(cfg)
            except ValueError:
                pass


# ----------------------------------------------------------------------------
# The hub.
# ----------------------------------------------------------------------------

def hub() -> int:
    banner()
    while True:
        interrupted = detect_interrupted_run()
        choices = []
        if interrupted:
            tag = f" — '{interrupted['title']}' ({interrupted['where']}"
            tag += f", {interrupted['age']})" if interrupted["age"] else ")"
            choices.append(f"⟳  Resume interrupted run{tag}")
        choices += [
            "✦  New report",
            "✎  Revise a report",
            "📊  Build a deck for a finished report",
            "⇪  Re-publish reports",
            "◎  Audit the council",
            "⚙  Settings",
            "→  Exit",
        ]
        choice = questionary.select("", choices=choices).ask()
        if choice is None or choice.startswith("→"):
            return 0
        try:
            if choice.startswith("⟳"):
                resume_flow(interrupted)
            elif choice.startswith("✦"):
                new_run_flow()
            elif choice.startswith("✎"):
                revise_flow()
            elif choice.startswith("📊"):
                deck_flow()
            elif choice.startswith("⇪"):
                publish_flow()
            elif choice.startswith("◎"):
                audit_flow()
            elif choice.startswith("⚙"):
                settings_menu()
        except KeyboardInterrupt:
            console.print("\n[yellow]Back to menu.[/yellow]")
        console.print()
