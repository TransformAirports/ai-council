"""Revision mode — produce a revised version of an existing report.

A reader gives additional feedback on a published report. Rather than re-running
the full Council (new research, ten agents, hours), a revision reuses the
original Stage 1 research briefs and runs a tight adversarial loop on the
existing draft plus the new feedback:

    Strategist (revise) → Red Team (critique) → Strategist (finalize)
    → Editor → Fact-checker

Revisions chain: v2 revises v1's output, not the original. Each lives under
`runs/<run>/revisions/vN/`, and the polished output is
`reports/<slug>-revised-vN.docx`, stamped "Revised — Version N" on the cover.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel

from cli.publish import ReportSource, discover_reports

console = Console()

REVISION_DIR_PATTERN = re.compile(r"^v(\d+)$")


@dataclass
class RevisionRequest:
    source: ReportSource
    feedback: str
    version: int


def _completed_revisions(archive_dir: Path) -> list[int]:
    """Version numbers of revisions that finished (have a final-draft.md)."""
    rd = archive_dir / "revisions"
    if not rd.is_dir():
        return []
    out: list[int] = []
    for p in rd.iterdir():
        m = REVISION_DIR_PATTERN.match(p.name)
        if m and (p / "final-draft.md").is_file():
            out.append(int(m.group(1)))
    return sorted(out)


def next_revision_version(archive_dir: Path) -> int:
    completed = _completed_revisions(archive_dir)
    return (max(completed) + 1) if completed else 1


def latest_draft_path(archive_dir: Path) -> Path:
    """The most recent draft to revise from — newest revision, else the original."""
    completed = _completed_revisions(archive_dir)
    if completed:
        return archive_dir / "revisions" / f"v{max(completed)}" / "final-draft.md"
    return archive_dir / "stage3" / "final-draft.md"


def _title_for(source: ReportSource) -> str:
    if source.run_file is not None:
        text = source.run_file.read_text(encoding="utf-8", errors="ignore")
        for line in text.splitlines():
            if line.startswith("# Run:"):
                return line[len("# Run:"):].strip()
    return source.slug.replace("-", " ").title()


def revisable_reports() -> list[ReportSource]:
    """Archived runs that have a body to revise."""
    return [s for s in discover_reports() if s.final_md is not None]


def collect_revision_request(only_slug: str | None = None) -> RevisionRequest | None:
    """Interactive: pick a report, capture feedback. Returns None if cancelled."""
    sources = revisable_reports()
    if not sources:
        console.print("[yellow]No revisable reports found under runs/. Run a report first.[/yellow]")
        return None

    if only_slug:
        match = next((s for s in sources if s.slug == only_slug), None)
        if match is None:
            console.print(f"[red]No archived report with slug '{only_slug}'.[/red]")
            return None
        source = match
    else:
        console.print(
            Panel.fit(
                "[bold]Revise an existing report[/bold]\n"
                "Pick the report a reader gave feedback on, then type the feedback.",
                border_style="cyan",
            )
        )
        choices = []
        for s in sources:
            completed = _completed_revisions(s.archive_dir)
            ver_note = f"  (currently at v{max(completed)})" if completed else ""
            choices.append(
                questionary.Choice(
                    title=f"{_title_for(s)}  —  {s.slug}{ver_note}",
                    value=s.slug,
                )
            )
        picked = questionary.select(
            "Which report?  (scroll with arrow keys)",
            choices=choices,
        ).ask()
        if picked is None:
            raise KeyboardInterrupt
        source = next(s for s in sources if s.slug == picked)

    version = next_revision_version(source.archive_dir)
    console.print()
    console.print(
        f"[bold]Feedback for[/bold] {_title_for(source)} "
        f"[dim](this will become Revised v{version})[/dim]"
    )
    feedback = questionary.text(
        "Additional feedback  (paste OK; press Esc then Enter to submit):",
        multiline=True,
    ).ask()
    if feedback is None:
        raise KeyboardInterrupt
    feedback = feedback.strip()
    if not feedback:
        console.print("[yellow]No feedback entered. Nothing to revise.[/yellow]")
        return None

    return RevisionRequest(source=source, feedback=feedback, version=version)
