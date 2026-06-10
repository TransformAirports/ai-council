"""Post-run archive: copy outputs/ to runs/YYYY-MM-DD-<slug>/ and clear outputs/.

Matches the workflow described in `prompts/orchestration.md` and `CLAUDE.md`.
A `retrospective.md` is written automatically alongside the staged artifacts.
"""
from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

from cli.orchestrator import CostTally

STAGE_DIRS: tuple[str, ...] = ("stage1", "stage2", "stage3", "stage4")


def _write_retrospective(archive_dir: Path, slug: str, tally: CostTally) -> None:
    lines = [
        f"# Retrospective — {slug}",
        "",
        f"Archived: {date.today().isoformat()}",
        "",
        "## Cost",
        "",
        f"Total estimated cost: **${tally.total:.2f}**",
        "",
        "| Step | Cost (USD) |",
        "| --- | ---: |",
    ]
    for step, cost in sorted(tally.by_step.items()):
        lines.append(f"| {step} | ${cost:.2f} |")
    lines += [
        "",
        "## Notes",
        "",
        "_Fill in by hand: what worked, what didn't, agent behaviors to watch next run._",
        "",
    ]
    (archive_dir / "retrospective.md").write_text("\n".join(lines), encoding="utf-8")


def _clear_outputs(outputs_dir: Path) -> None:
    for sub in STAGE_DIRS:
        target = outputs_dir / sub
        if target.is_dir():
            shutil.rmtree(target)
    marker = outputs_dir / ".active-run.json"
    if marker.exists():
        marker.unlink()
    keep = outputs_dir / ".gitkeep"
    if not keep.exists():
        keep.touch()


def archive_run(*, repo_root: Path, slug: str, tally: CostTally) -> Path:
    outputs_dir = repo_root / "outputs"
    archive_dir = repo_root / "runs" / f"{date.today().isoformat()}-{slug}"
    if archive_dir.exists():
        raise FileExistsError(
            f"Archive already exists: {archive_dir}. Pick a different slug or remove it."
        )
    archive_dir.mkdir(parents=True)

    for sub in STAGE_DIRS:
        src = outputs_dir / sub
        if src.is_dir():
            shutil.copytree(src, archive_dir / sub)

    _write_retrospective(archive_dir, slug, tally)
    _clear_outputs(outputs_dir)
    return archive_dir
