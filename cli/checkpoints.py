"""Human-in-the-loop checkpoints between stages.

The orchestrator pauses here after Stage 2 (drafts + critiques) and Stage 3
(edited + fact-checked draft). When `auto_approve=True` (the `--no-review`
CLI flag), checkpoints log what would be shown and continue immediately.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


@dataclass
class CheckpointResult:
    approved: bool
    redo_from: str | None = None  # optional name of a step to redo


def _show_file_excerpt(path: Path, max_lines: int = 60) -> None:
    if not path.is_file():
        console.print(f"[red]Missing: {path}[/red]")
        return
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    excerpt = "\n".join(lines[:max_lines])
    suffix = f"\n\n[dim]…({len(lines) - max_lines} more lines in {path.name})[/dim]" if len(lines) > max_lines else ""
    console.print(Panel(Markdown(excerpt + suffix), title=str(path), border_style="cyan"))


def checkpoint_after_stage2(
    outputs_dir: Path,
    auto_approve: bool = False,
) -> CheckpointResult:
    console.rule("[bold]Human checkpoint #1 — after Stage 2[/bold]")
    stage2 = outputs_dir / "stage2"
    files = [
        stage2 / "strategist-draft-v3.md",
        stage2 / "red-team-critique-v2.md",
        stage2 / "red-team-critique-v1.md",
    ]
    for f in files:
        _show_file_excerpt(f, max_lines=40)

    if auto_approve:
        console.print("[yellow]--no-review: auto-approving Stage 2 → Stage 3.[/yellow]")
        return CheckpointResult(approved=True)

    answer = questionary.select(
        "Proceed to Stage 3 (Editor + Fact-checker)?",
        choices=[
            "Yes — continue to Stage 3",
            "No — redo Strategist v3 with my notes",
            "Abort the run",
        ],
    ).ask()
    if answer is None or answer.startswith("Abort"):
        return CheckpointResult(approved=False)
    if answer.startswith("No"):
        return CheckpointResult(approved=False, redo_from="strategist-v3")
    return CheckpointResult(approved=True)


def checkpoint_after_stage3(
    outputs_dir: Path,
    auto_approve: bool = False,
) -> CheckpointResult:
    console.rule("[bold]Human checkpoint #2 — after Stage 3[/bold]")
    stage3 = outputs_dir / "stage3"
    files = [
        stage3 / "final-draft.md",
        stage3 / "fact-check-report.md",
    ]
    for f in files:
        _show_file_excerpt(f, max_lines=60)

    if auto_approve:
        console.print("[yellow]--no-review: auto-approving Stage 3 → Stage 4.[/yellow]")
        return CheckpointResult(approved=True)

    answer = questionary.confirm(
        "Generate the Word documents and archive the run?",
        default=True,
    ).ask()
    return CheckpointResult(approved=bool(answer))
