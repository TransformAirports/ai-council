"""Revision mode — produce a revised version of an existing report.

A reader gives additional feedback on a published report. Rather than re-running
the full Council (new research, ten agents, hours), a revision reuses the
original Stage 1 research briefs and runs a tight adversarial loop on the
existing draft plus the new feedback:

    Strategist (revise) → Red Team (critique) → Strategist (finalize)
    → Editor → Humanizer → Source Verifier → release gate → Art Director
    → rendered Word packet → exact-byte release

Revisions chain: v2 revises v1's output, not the original. Each lives under
`runs/<run>/revisions/vN/`, and the polished output is
`reports/<slug>-revised-vN.docx`, stamped "Revised — Version N" on the cover.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import questionary
from rich.console import Console
from rich.panel import Panel

from cli.publish import ReportSource, discover_reports
from cli.revision_state import assert_revision_step_outputs_current

console = Console()

REVISION_DIR_PATTERN = re.compile(r"^v(\d+)$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
RELEASE_CRITICAL_REVISION_STEPS = frozenset(
    {
        "strategist-a",
        "red-team",
        "strategist-b",
        "editor",
        "humanizer",
        "fact-checker",
        "word-production",
        "word-visual-inspection",
    }
)


@dataclass
class RevisionRequest:
    source: ReportSource
    feedback: str
    version: int


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_object_without_duplicates(path: Path) -> dict[str, Any]:
    def reject_duplicates(
        pairs: list[tuple[str, Any]],
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for key, value in pairs:
            if key in payload:
                raise ValueError(f"duplicate JSON key: {key}")
            payload[key] = value
        return payload

    payload = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
    )
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return payload


def _assert_terminal_file_hash(
    path: Path,
    expected: object,
    *,
    label: str,
) -> str:
    if (
        not isinstance(expected, str)
        or SHA256_PATTERN.fullmatch(expected) is None
    ):
        raise RuntimeError(
            f"Revision terminal manifest has no valid {label} hash."
        )
    if path.is_symlink() or not path.is_file():
        raise RuntimeError(f"Released revision {label} is missing or unsafe.")
    actual = _sha256(path)
    if actual != expected:
        raise RuntimeError(f"Released revision {label} hash does not match.")
    return actual


def _repo_root_for_archive(archive_dir: Path) -> Path:
    """Resolve the repository root for repo-relative execution receipts."""

    archive = archive_dir.resolve()
    if archive.parent.name == "runs":
        return archive.parent.parent
    for ancestor in archive.parents:
        runs_dir = ancestor / "runs"
        try:
            archive.relative_to(runs_dir.resolve())
        except (OSError, ValueError):
            continue
        return ancestor
    # Test and embedding fallback. Production archives always live in runs/.
    return archive.parent


def _terminal_required_steps(
    *,
    manifest: dict[str, Any],
    revision_dir: Path,
    final_draft_sha256: str,
) -> set[str]:
    raw_steps = manifest.get("required_steps")
    if raw_steps is None:
        required = set(RELEASE_CRITICAL_REVISION_STEPS)
    else:
        if (
            not isinstance(raw_steps, list)
            or any(not isinstance(step, str) or not step for step in raw_steps)
            or len(raw_steps) != len(set(raw_steps))
        ):
            raise RuntimeError(
                "Revision terminal manifest has malformed required steps."
            )
        required = set(raw_steps)
        missing_core = RELEASE_CRITICAL_REVISION_STEPS - required
        if missing_core:
            raise RuntimeError(
                "Revision terminal manifest omits release-critical steps: "
                + ", ".join(sorted(missing_core))
            )

    visual_hash = manifest.get("visual_brief_sha256")
    if visual_hash is not None:
        if (
            not isinstance(visual_hash, str)
            or SHA256_PATTERN.fullmatch(visual_hash) is None
        ):
            raise RuntimeError(
                "Revision terminal manifest has an invalid visual brief hash."
            )
        required.add("art-direction")
    elif "art-direction" in required:
        raise RuntimeError(
            "Revision terminal manifest requires art direction without a "
            "released visual brief."
        )

    remediated = revision_dir / "final-draft-remediated.md"
    remediation_is_active = (
        remediated.is_file()
        and not remediated.is_symlink()
        and _sha256(remediated) == final_draft_sha256
    )
    if remediation_is_active:
        required.add("fact-check-remediation")
    elif "fact-check-remediation" in required:
        raise RuntimeError(
            "Revision terminal manifest requires remediation whose promoted "
            "draft is not the released final draft."
        )
    return required


def verify_terminal_revision(
    revision_dir: Path,
    *,
    archive_dir: Path,
    expected_version: int,
    expected_source_draft: Path,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Fail closed unless every byte in a receipt-aware release still agrees."""

    base = revision_dir.resolve()
    archive = archive_dir.resolve()
    if base.parent != (archive / "revisions").resolve():
        raise RuntimeError("Revision directory is outside its source archive.")
    if base.name != f"v{expected_version}":
        raise RuntimeError("Revision directory and expected version disagree.")

    manifest_path = base / "revision-manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise RuntimeError("Receipt-aware revision has no safe terminal manifest.")
    try:
        manifest = _json_object_without_duplicates(manifest_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError("Revision terminal manifest is malformed.") from exc

    slug = manifest.get("slug")
    if (
        manifest.get("schema_version") != "1.0"
        or manifest.get("status") != "released"
        or manifest.get("revision") != expected_version
        or manifest.get("source_archive") != archive.name
        or not isinstance(slug, str)
        or not slug.strip()
    ):
        raise RuntimeError("Revision terminal identity is incomplete or invalid.")

    source_hash = _assert_terminal_file_hash(
        expected_source_draft,
        manifest.get("source_draft_sha256"),
        label="source draft",
    )
    if source_hash != manifest.get("source_draft_sha256"):
        raise RuntimeError("Revision source draft identity does not match.")

    feedback = base / "feedback.md"
    final_draft = base / "final-draft.md"
    lineage = base / "claim-lineage.jsonl"
    gate = base / "quality-gate.json"
    visual_brief = base / "visual-brief.json"
    execution_state = base / "revision-execution.json"
    release_dir = base / "release"
    release_manifest = release_dir / "release-manifest.json"
    release_slug = f"{slug}-revised-v{expected_version}"
    stage4_report = base / "stage4" / f"{release_slug}.docx"
    stage4_summary = (
        base
        / "stage4"
        / f"{release_slug}-executive-summary.docx"
    )

    _assert_terminal_file_hash(
        feedback,
        manifest.get("feedback_sha256"),
        label="feedback",
    )
    final_hash = _assert_terminal_file_hash(
        final_draft,
        manifest.get("final_draft_sha256"),
        label="final draft",
    )
    _assert_terminal_file_hash(
        lineage,
        manifest.get("claim_lineage_sha256"),
        label="claim lineage",
    )
    _assert_terminal_file_hash(
        gate,
        manifest.get("quality_gate_sha256"),
        label="quality gate",
    )
    _assert_terminal_file_hash(
        stage4_report,
        manifest.get("word_report_sha256"),
        label="Word report",
    )
    _assert_terminal_file_hash(
        release_manifest,
        manifest.get("release_manifest_sha256"),
        label="release manifest",
    )
    _assert_terminal_file_hash(
        execution_state,
        manifest.get("revision_execution_sha256"),
        label="revision execution state",
    )

    try:
        gate_payload = _json_object_without_duplicates(gate)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError("Released revision quality gate is malformed.") from exc
    if gate_payload.get("passed") is not True:
        raise RuntimeError("Released revision quality gate is not passing.")

    visual_hash = manifest.get("visual_brief_sha256")
    if visual_hash is not None:
        _assert_terminal_file_hash(
            visual_brief,
            visual_hash,
            label="visual brief",
        )
    elif visual_brief.exists() or visual_brief.is_symlink():
        raise RuntimeError(
            "Released revision has an unbound visual brief beside its terminal "
            "manifest."
        )

    summary_hash = manifest.get("executive_summary_sha256")
    if summary_hash is not None:
        _assert_terminal_file_hash(
            stage4_summary,
            summary_hash,
            label="executive summary",
        )
    elif stage4_summary.exists() or stage4_summary.is_symlink():
        raise RuntimeError(
            "Released revision has an unbound executive summary beside its "
            "terminal manifest."
        )

    try:
        from cli.publish import verify_release_bundle

        strict_release_payload = _json_object_without_duplicates(
            release_manifest
        )
        release_payload = verify_release_bundle(release_dir)
    except (
        AttributeError,
        FileNotFoundError,
        KeyError,
        OSError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
        RuntimeError,
    ) as exc:
        raise RuntimeError("Released revision bundle is invalid.") from exc
    if release_payload != strict_release_payload:
        raise RuntimeError(
            "Released revision bundle changed while it was being verified."
        )
    if release_payload.get("slug") != release_slug:
        raise RuntimeError("Released revision bundle has the wrong slug.")
    artifacts = release_payload.get("artifacts")
    if not isinstance(artifacts, list):
        raise RuntimeError("Released revision bundle has no artifact inventory.")
    by_role = {
        str(item.get("role") or ""): item
        for item in artifacts
        if isinstance(item, dict)
    }
    word_artifact = by_role.get("word_report")
    if (
        not isinstance(word_artifact, dict)
        or word_artifact.get("sha256") != manifest.get("word_report_sha256")
    ):
        raise RuntimeError(
            "Released revision Word report disagrees with its release bundle."
        )
    summary_artifact = by_role.get("executive_summary")
    if summary_hash is None:
        if summary_artifact is not None:
            raise RuntimeError(
                "Released revision bundle contains an unbound executive summary."
            )
    elif (
        not isinstance(summary_artifact, dict)
        or summary_artifact.get("sha256") != summary_hash
    ):
        raise RuntimeError(
            "Released revision executive summary disagrees with its bundle."
        )

    required_steps = _terminal_required_steps(
        manifest=manifest,
        revision_dir=base,
        final_draft_sha256=final_hash,
    )
    assert_revision_step_outputs_current(
        state_path=execution_state,
        repo_root=repo_root or _repo_root_for_archive(archive),
        required_steps=required_steps,
    )
    # Re-read every terminal-bound byte after the deeper bundle and receipt
    # checks. A concurrent mutation cannot be accepted in the gap between an
    # early hash check and the function's successful return.
    final_bindings: list[tuple[Path, object, str]] = [
        (
            expected_source_draft,
            manifest.get("source_draft_sha256"),
            "source draft",
        ),
        (feedback, manifest.get("feedback_sha256"), "feedback"),
        (final_draft, manifest.get("final_draft_sha256"), "final draft"),
        (lineage, manifest.get("claim_lineage_sha256"), "claim lineage"),
        (gate, manifest.get("quality_gate_sha256"), "quality gate"),
        (
            stage4_report,
            manifest.get("word_report_sha256"),
            "Word report",
        ),
        (
            release_manifest,
            manifest.get("release_manifest_sha256"),
            "release manifest",
        ),
        (
            execution_state,
            manifest.get("revision_execution_sha256"),
            "revision execution state",
        ),
    ]
    if visual_hash is not None:
        final_bindings.append((visual_brief, visual_hash, "visual brief"))
    if summary_hash is not None:
        final_bindings.append(
            (stage4_summary, summary_hash, "executive summary")
        )
    for bound_path, bound_hash, label in final_bindings:
        _assert_terminal_file_hash(bound_path, bound_hash, label=label)
    try:
        final_manifest = _json_object_without_duplicates(manifest_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(
            "Revision terminal manifest changed during verification."
        ) from exc
    if final_manifest != manifest:
        raise RuntimeError(
            "Revision terminal manifest changed during verification."
        )
    return manifest


def _completed_revisions(archive_dir: Path) -> list[int]:
    """Version numbers of released revisions.

    Legacy revisions predate execution receipts, so their final draft remains
    the compatibility completion marker. Receipt-aware revisions advance only
    after the terminal release manifest is committed; a crash after
    fact-checking must resume the same version instead of silently becoming a
    new revision.
    """
    rd = archive_dir / "revisions"
    if not rd.is_dir():
        return []
    revision_dirs: dict[int, Path] = {}
    for path in rd.iterdir():
        match = REVISION_DIR_PATTERN.match(path.name)
        if match and path.is_dir() and not path.is_symlink():
            revision_dirs[int(match.group(1))] = path

    out: list[int] = []
    expected_version = 1
    expected_source = archive_dir / "stage3" / "final-draft.md"
    while expected_version in revision_dirs:
        path = revision_dirs[expected_version]
        final_draft = path / "final-draft.md"
        if final_draft.is_symlink() or not final_draft.is_file():
            break
        execution_state = path / "revision-execution.json"
        if not execution_state.exists() and not execution_state.is_symlink():
            # Compatibility: legacy revisions predate execution receipts.
            out.append(expected_version)
            expected_source = final_draft
            expected_version += 1
            continue
        if execution_state.is_symlink() or not execution_state.is_file():
            # A dangling link, directory, or other non-file marker is
            # receipt-aware corruption, not evidence of a legacy revision.
            break
        try:
            verify_terminal_revision(
                path,
                archive_dir=archive_dir,
                expected_version=expected_version,
                expected_source_draft=expected_source,
            )
        except (OSError, RuntimeError, ValueError):
            break
        out.append(expected_version)
        expected_source = final_draft
        expected_version += 1
    return out


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
