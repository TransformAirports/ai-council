"""Human-in-the-loop checkpoints between stages.

The orchestrator pauses here after Stage 2 (drafts + critiques) and Stage 3
(edited + fact-checked draft). When `auto_approve=True` (the `--no-review`
CLI flag), checkpoints log what would be shown and continue immediately.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any, Iterable

import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from cli.events import get_sink, request_checkpoint
from cli.run_manifest import build_dependency_fingerprint

console = Console()

STAGE2_CHECKPOINT_INPUTS: tuple[str, ...] = (
    "stage2/strategist-draft-v3.md",
    "stage2/red-team-critique-v2.md",
    "stage2/red-team-critique-v1.md",
)
STAGE3_CHECKPOINT_INPUTS: tuple[str, ...] = (
    "stage3/final-draft.md",
    "stage3/fact-check-report.md",
    "claim-lineage.jsonl",
    "quality-gate.json",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


@dataclass
class CheckpointResult:
    approved: bool
    redo_from: str | None = None  # optional name of a step to redo
    notes: str = ""               # operator notes to inject into the redo prompt
    ratings: dict[str, int] | None = None
    # Exact dependency receipt captured around the reads presented for review.
    # The orchestrator passes this back when it records the decision, closing
    # the gap where a draft could change while the operator was deciding.
    reviewed_fingerprint: dict[str, Any] | None = None


def _show_file_excerpt(
    path: Path,
    max_lines: int = 60,
    *,
    content: str | None = None,
) -> None:
    if content is None and not path.is_file():
        console.print(f"[red]Missing: {path}[/red]")
        return
    text = content if content is not None else path.read_text(encoding="utf-8")
    lines = text.splitlines()
    excerpt = "\n".join(lines[:max_lines])
    suffix = (
        f"\n\n[dim]…({len(lines) - max_lines} more lines in "
        f"{path.name})[/dim]"
        if len(lines) > max_lines
        else ""
    )
    console.print(
        Panel(Markdown(excerpt + suffix), title=str(path), border_style="cyan")
    )


def _capture_review_snapshot(
    outputs_dir: Path,
    declared_inputs: Iterable[str],
) -> tuple[dict[str, str], dict[str, Any]]:
    """Read checkpoint inputs once and bind those bytes to a stable receipt.

    The dependency receipt is computed both before and after the display bytes
    are read. Matching receipts plus an explicit hash check prove that the
    cached text is the same version represented by the returned fingerprint.
    """

    manifest_path = outputs_dir / "run-manifest.json"
    declarations = tuple(dict.fromkeys(str(item) for item in declared_inputs))
    before = build_dependency_fingerprint(manifest_path, declarations)
    if before.get("complete") is not True:
        raise RuntimeError(
            "Cannot open checkpoint: one or more review inputs are missing "
            "or unsafe."
        )

    contents: dict[str, str] = {}
    content_hashes: dict[str, str] = {}
    for declaration in declarations:
        relative = Path(declaration)
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or any(character in declaration for character in "*?[")
        ):
            raise RuntimeError(
                "Cannot open checkpoint: review input is not an exact safe "
                f"path: {declaration}"
            )
        path = outputs_dir / relative
        try:
            raw = path.read_bytes()
            contents[declaration] = raw.decode("utf-8")
        except (OSError, UnicodeError) as error:
            raise RuntimeError(
                f"Cannot open checkpoint review input {declaration}: {error}"
            ) from error
        content_hashes[declaration] = hashlib.sha256(raw).hexdigest()

    after = build_dependency_fingerprint(manifest_path, declarations)
    if (
        after.get("complete") is not True
        or before.get("sha256") != after.get("sha256")
    ):
        raise RuntimeError(
            "Checkpoint inputs changed while the review snapshot was being "
            "captured. Open the checkpoint again."
        )

    recorded_hashes: dict[str, str] = {}
    for record in after.get("inputs", []):
        if not isinstance(record, dict):
            continue
        for entry in record.get("files", []):
            if (
                isinstance(entry, dict)
                and entry.get("kind") == "file"
                and isinstance(entry.get("path"), str)
                and isinstance(entry.get("sha256"), str)
            ):
                recorded_hashes[entry["path"]] = entry["sha256"]
    if any(
        recorded_hashes.get(declaration) != digest
        for declaration, digest in content_hashes.items()
    ):
        raise RuntimeError(
            "Checkpoint inputs changed while the review snapshot was being "
            "captured. Open the checkpoint again."
        )
    return contents, deepcopy(after)


async def checkpoint_after_stage2(
    outputs_dir: Path,
    auto_approve: bool = False,
) -> CheckpointResult:
    console.rule("[bold]Human checkpoint #1 — after Stage 2[/bold]")
    contents, reviewed_fingerprint = _capture_review_snapshot(
        outputs_dir, STAGE2_CHECKPOINT_INPUTS
    )
    for relative in STAGE2_CHECKPOINT_INPUTS:
        _show_file_excerpt(
            outputs_dir / relative,
            max_lines=40,
            content=contents[relative],
        )

    if auto_approve:
        console.print(
            "[yellow]--no-review: auto-approving Stage 2 → Stage 3.[/yellow]"
        )
        return CheckpointResult(
            approved=True,
            reviewed_fingerprint=reviewed_fingerprint,
        )

    # Web UI path: send the drafts to the browser and await its decision.
    if get_sink() is not None:
        decision = await request_checkpoint(
            "stage2",
            {
                "title": "Checkpoint 1 — synthesis & debate",
                "subtitle": (
                    "Review the third Strategist draft and both Red Team "
                    "critiques."
                ),
                "documents": [
                    {
                        "name": "Strategist draft v3",
                        "content": contents[STAGE2_CHECKPOINT_INPUTS[0]],
                    },
                    {
                        "name": "Red Team critique v2",
                        "content": contents[STAGE2_CHECKPOINT_INPUTS[1]],
                    },
                    {
                        "name": "Red Team critique v1",
                        "content": contents[STAGE2_CHECKPOINT_INPUTS[2]],
                    },
                ],
                "actions": ["continue", "redo", "abort"],
                "rubric": [
                    {"key": "originality", "label": "Originality"},
                    {
                        "key": "airport_specificity",
                        "label": "Airport specificity",
                    },
                    {
                        "key": "decision_usefulness",
                        "label": "Decision usefulness",
                    },
                ],
            },
        ) or {"action": "abort"}
        action = decision.get("action", "abort")
        if action == "continue":
            return CheckpointResult(
                approved=True,
                ratings=_clean_ratings(decision.get("ratings")),
                reviewed_fingerprint=reviewed_fingerprint,
            )
        if action == "redo":
            return CheckpointResult(
                approved=False,
                redo_from="strategist-v3",
                notes=str(decision.get("notes", "")).strip(),
                ratings=_clean_ratings(decision.get("ratings")),
                reviewed_fingerprint=reviewed_fingerprint,
            )
        return CheckpointResult(
            approved=False,
            reviewed_fingerprint=reviewed_fingerprint,
        )

    answer = await questionary.select(
        "Proceed to Stage 3 (Editor + Fact-checker)?",
        choices=[
            "Yes — continue to Stage 3",
            "No — redo Strategist v3 with my notes",
            "Abort the run",
        ],
    ).ask_async()
    if answer is None or answer.startswith("Abort"):
        return CheckpointResult(
            approved=False,
            reviewed_fingerprint=reviewed_fingerprint,
        )
    if answer.startswith("No"):
        notes = await questionary.text(
            "Your notes for the redo (what should v3 do differently?) "
            "— press Esc then Enter to submit:",
            multiline=True,
        ).ask_async()
        return CheckpointResult(
            approved=False,
            redo_from="strategist-v3",
            notes=(notes or "").strip(),
            reviewed_fingerprint=reviewed_fingerprint,
        )
    return CheckpointResult(
        approved=True,
        reviewed_fingerprint=reviewed_fingerprint,
    )


async def checkpoint_after_stage3(
    outputs_dir: Path,
    auto_approve: bool = False,
) -> CheckpointResult:
    console.rule("[bold]Human checkpoint #2 — after Stage 3[/bold]")
    contents, reviewed_fingerprint = _capture_review_snapshot(
        outputs_dir, STAGE3_CHECKPOINT_INPUTS
    )
    for relative in STAGE3_CHECKPOINT_INPUTS[:2]:
        _show_file_excerpt(
            outputs_dir / relative,
            max_lines=60,
            content=contents[relative],
        )

    if auto_approve:
        console.print(
            "[yellow]--no-review: auto-approving Stage 3 → Stage 4.[/yellow]"
        )
        return CheckpointResult(
            approved=True,
            reviewed_fingerprint=reviewed_fingerprint,
        )

    if get_sink() is not None:
        decision = await request_checkpoint(
            "stage3",
            {
                "title": "Checkpoint 2 — final review",
                "subtitle": (
                    "The edited, humanized, fact-checked draft. Approve to "
                    "produce documents."
                ),
                "documents": [
                    {
                        "name": "Final draft",
                        "content": contents[STAGE3_CHECKPOINT_INPUTS[0]],
                    },
                    {
                        "name": "Fact-check report",
                        "content": contents[STAGE3_CHECKPOINT_INPUTS[1]],
                    },
                ],
                "actions": ["approve", "abort"],
                "rubric": [
                    {"key": "writing", "label": "Writing quality"},
                    {
                        "key": "airport_specificity",
                        "label": "Airport specificity",
                    },
                    {
                        "key": "decision_usefulness",
                        "label": "Decision usefulness",
                    },
                ],
            },
        ) or {"action": "abort"}
        return CheckpointResult(
            approved=decision.get("action") == "approve",
            ratings=_clean_ratings(decision.get("ratings")),
            reviewed_fingerprint=reviewed_fingerprint,
        )

    answer = await questionary.confirm(
        "Generate the Word documents and archive the run?",
        default=True,
    ).ask_async()
    return CheckpointResult(
        approved=bool(answer),
        reviewed_fingerprint=reviewed_fingerprint,
    )


def _clean_ratings(value: object) -> dict[str, int]:
    """Keep only integer 1–5 rubric scores from an untrusted UI payload."""
    if not isinstance(value, dict):
        return {}
    cleaned: dict[str, int] = {}
    for key, raw in value.items():
        if not isinstance(key, str) or not isinstance(raw, int):
            continue
        if 1 <= raw <= 5:
            cleaned[key] = raw
    return cleaned
