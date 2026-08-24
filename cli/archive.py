"""Post-run archive: copy outputs/ to runs/YYYY-MM-DD-<slug>/ and clear outputs/.

Matches the workflow described in `prompts/orchestration.md` and `CLAUDE.md`.
A `retrospective.md` is written automatically alongside the staged artifacts.
"""
from __future__ import annotations

import json
import hashlib
import os
import re
import shutil
import tempfile
from datetime import date
from pathlib import Path

from cli.orchestrator import CostTally

STAGE_DIRS: tuple[str, ...] = ("stage1", "stage2", "stage3", "stage4")
RUN_DIRS: tuple[str, ...] = ("context", "evaluation", "release")
RUN_ARTIFACTS: tuple[str, ...] = (
    "run-manifest.json",
    "evidence-ledger.jsonl",
    "claim-lineage.jsonl",
    "quality-gate.json",
    "publishing-quality.json",
    "run-events.jsonl",
)


def _bind_event_journal(
    archive_dir: Path,
    *,
    preserve_existing: bool,
) -> None:
    """Finish the optional event journal after the archive commits."""

    from cli.events import get_sink

    sink = get_sink()
    if sink is not None:
        sink.archive_to(
            archive_dir / "run-events.jsonl",
            preserve_existing=preserve_existing,
        )


def _write_retrospective(archive_dir: Path, slug: str, tally: CostTally) -> None:
    def jsonl_count(path: Path) -> int | None:
        if not path.is_file():
            return None
        count = 0
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.strip():
                continue
            try:
                if isinstance(json.loads(line), dict):
                    count += 1
            except json.JSONDecodeError:
                continue
        return count

    evidence_count = jsonl_count(archive_dir / "evidence-ledger.jsonl")
    lineage_count = jsonl_count(archive_dir / "claim-lineage.jsonl")
    gate_status = "not recorded"
    gate_path = archive_dir / "quality-gate.json"
    if gate_path.is_file():
        try:
            gate = json.loads(gate_path.read_text(encoding="utf-8"))
            gate_status = str(gate.get("status") or gate.get("result") or "recorded")
        except (OSError, json.JSONDecodeError):
            gate_status = "unreadable"
    lines = [
        f"# Retrospective — {slug}",
        "",
        f"Archived: {date.today().isoformat()}",
        "",
        "## Cost",
        "",
        (
            f"Tracked Council model total: **${tally.total:.2f}**"
        ),
        "",
        "| Council step | Cost (USD) |",
        "| --- | ---: |",
    ]
    for step, cost in sorted(tally.by_step.items()):
        lines.append(f"| {step} | ${cost:.2f} |")
    lines += [
        "",
        "## Automated quality record",
        "",
        f"- Evidence records commissioned and curated: **{evidence_count if evidence_count is not None else 'not available'}**",
        f"- Final claims with structured lineage: **{lineage_count if lineage_count is not None else 'not available'}**",
        f"- Publishing quality gate: **{gate_status}**",
        "",
        "## Follow-up",
        "",
        (
            "- Review any warnings in `quality-gate.json`, the Fact-checker's "
            "unverified list, and the evidence map's gaps before the next run."
        ),
        (
            "- Human rubric scores, when supplied, are preserved under "
            "`evaluation/reviews/` and included in the Council audit."
        ),
        "",
    ]
    (archive_dir / "retrospective.md").write_text("\n".join(lines), encoding="utf-8")


def _clear_outputs(outputs_dir: Path) -> None:
    for sub in STAGE_DIRS + RUN_DIRS:
        target = outputs_dir / sub
        if target.is_dir():
            shutil.rmtree(target)
    # Keep the run manifest until every other cleanup has succeeded. If a
    # filesystem error interrupts cleanup, the archived commit can be
    # positively identified and cleanup retried without risking a new run.
    for filename in (
        item for item in RUN_ARTIFACTS if item != "run-manifest.json"
    ):
        target = outputs_dir / filename
        if target.is_file():
            target.unlink()
    src_dir = outputs_dir / "sources"
    if src_dir.is_dir():
        shutil.rmtree(src_dir)
    scope_dir = outputs_dir / "scope"
    if scope_dir.is_dir():
        shutil.rmtree(scope_dir)
    marker = outputs_dir / ".active-run.json"
    if marker.exists():
        marker.unlink()
    manifest = outputs_dir / "run-manifest.json"
    if manifest.is_file():
        manifest.unlink()
    keep = outputs_dir / ".gitkeep"
    if not keep.exists():
        keep.touch()


def _sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _safe_archive_path(archive_dir: Path, relative: str, *, label: str) -> Path:
    """Resolve one manifest path without allowing archive escapes or symlinks."""

    lexical = Path(relative)
    if not relative or lexical.is_absolute():
        raise RuntimeError(
            f"Committed archive has an unsafe {label} path: {relative!r}"
        )
    root = archive_dir.resolve()
    cursor = archive_dir
    for part in lexical.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise RuntimeError(
                f"Committed archive {label} may not be a symlink: {relative}"
            )
    candidate = (root / lexical).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(
            f"Committed archive {label} escapes the archive: {relative}"
        ) from exc
    return candidate


def _verify_committed_archive(
    archive_dir: Path,
    manifest_payload: dict,
    *,
    slug: str,
    expected_manifest_sha256: str | None,
) -> None:
    """Revalidate a complete archive before it can authorize output cleanup.

    This deliberately verifies the archived bytes, rather than the possibly
    half-cleaned ``outputs/`` tree. It applies the same prompt, source,
    generated-artifact, QA, visual-inspection, and release-bundle contracts
    used during a fresh archive commit.
    """

    from cli.artifacts import (
        ArtifactContract,
        contract_for_path,
        validate_artifact,
    )

    if archive_dir.is_symlink() or not archive_dir.is_dir():
        raise RuntimeError(
            f"Committed archive is not a regular directory: {archive_dir}"
        )

    archived_manifest = _safe_archive_path(
        archive_dir,
        "run-manifest.json",
        label="run manifest",
    )
    if (
        not expected_manifest_sha256
        or not archived_manifest.is_file()
        or _sha256(archived_manifest) != expected_manifest_sha256
    ):
        raise RuntimeError(
            "Committed archive run manifest does not match the active run."
        )

    run_data = manifest_payload.get("run", {})
    manifest_slug = str(run_data.get("slug") or "")
    if manifest_slug and manifest_slug != slug:
        raise RuntimeError(
            "Committed archive run manifest names a different run: "
            f"{manifest_slug!r}."
        )

    def require_fingerprint(
        path: Path,
        *,
        expected_hash: object,
        expected_size: object,
        label: str,
    ) -> None:
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"Committed archive is missing {label}: {path}")
        if not expected_hash or _sha256(path) != expected_hash:
            raise RuntimeError(
                f"Committed archive {label} does not match its SHA-256."
            )
        if expected_size is not None:
            try:
                size = int(expected_size)
            except (TypeError, ValueError) as exc:
                raise RuntimeError(
                    f"Committed archive has an invalid size for {label}."
                ) from exc
            if path.stat().st_size != size:
                raise RuntimeError(
                    f"Committed archive {label} does not match its size."
                )

    if run_data:
        prompt = _safe_archive_path(
            archive_dir,
            "run-prompt.md",
            label="run prompt",
        )
        require_fingerprint(
            prompt,
            expected_hash=run_data.get("run_prompt_sha256"),
            expected_size=run_data.get("run_prompt_size"),
            label="run prompt",
        )

    expected_sources: dict[str, object] = {}
    for index, source in enumerate(run_data.get("source_material", []), 1):
        relative = str(source.get("archive_path") or "")
        archived_source = _safe_archive_path(
            archive_dir,
            relative,
            label=f"source material {index}",
        )
        require_fingerprint(
            archived_source,
            expected_hash=source.get("sha256"),
            expected_size=source.get("size_bytes"),
            label=f"source material {index}",
        )
        expected_sources[Path(relative).as_posix()] = source.get("sha256")

    for index, source in enumerate(run_data.get("source_library", []), 1):
        relative = (
            Path("sources") / str(source.get("path") or "")
        ).as_posix()
        archived_source = _safe_archive_path(
            archive_dir,
            relative,
            label=f"source-library file {index}",
        )
        require_fingerprint(
            archived_source,
            expected_hash=source.get("sha256"),
            expected_size=source.get("size_bytes"),
            label=f"source-library file {index}",
        )
        expected_sources[relative] = source.get("sha256")

    sources_dir = archive_dir / "sources"
    if sources_dir.exists() and (
        sources_dir.is_symlink() or not sources_dir.is_dir()
    ):
        raise RuntimeError(
            "Committed archive sources path is not a regular directory."
        )
    if sources_dir.is_dir():
        symlinks = [
            path
            for path in sources_dir.rglob("*")
            if path.is_symlink()
        ]
        if symlinks:
            raise RuntimeError(
                "Committed archive source tree contains a symlink: "
                f"{symlinks[0].relative_to(archive_dir)}"
            )
    current_sources = {
        path.relative_to(archive_dir).as_posix(): _sha256(path)
        for path in (
            sorted(sources_dir.rglob("*")) if sources_dir.is_dir() else []
        )
        if path.is_file() and not path.is_symlink()
    }
    if current_sources != expected_sources:
        raise RuntimeError(
            "Committed archive source file set differs from the executable "
            "source contract."
        )

    failures: list[str] = []
    release_expected = False
    for item in manifest_payload.get("artifacts", []):
        required = bool(item.get("required", True))
        artifact_id = str(item.get("id") or item.get("path") or "artifact")
        relative = str(item.get("path") or "")
        if Path(relative).parts[:1] == ("release",):
            release_expected = release_expected or item.get("status") == "complete"
        try:
            candidate = _safe_archive_path(
                archive_dir,
                relative,
                label=f"artifact {artifact_id}",
            )
        except RuntimeError as exc:
            failures.append(str(exc))
            continue
        if (
            not required
            and not candidate.exists()
            and item.get("status") in {"pending", "skipped", None}
        ):
            continue
        if item.get("status") != "complete":
            failures.append(
                f"{artifact_id}: manifest status is "
                f"{item.get('status', 'missing')!r}"
            )
            continue
        if candidate.is_symlink() or not candidate.is_file():
            failures.append(f"{artifact_id}: archived artifact is missing")
            continue
        raw_contract = item.get("contract") or {}
        try:
            contract = ArtifactContract(
                str(
                    raw_contract.get("kind")
                    or contract_for_path(candidate).kind
                ),
                min_words=int(raw_contract.get("min_words") or 0),
                min_records=int(raw_contract.get("min_records") or 0),
                required_keys=tuple(raw_contract.get("required_keys") or ()),
                required_any=tuple(
                    tuple(group)
                    for group in (raw_contract.get("required_any") or ())
                ),
                optional=bool(raw_contract.get("optional", False)),
            )
        except (TypeError, ValueError) as exc:
            failures.append(f"{artifact_id}: invalid artifact contract ({exc})")
            continue
        validation = validate_artifact(candidate, contract)
        if not validation.valid:
            failures.append(
                f"{artifact_id}: "
                f"{'; '.join(validation.errors) or 'invalid'}"
            )
            continue
        if not item.get("sha256") or validation.sha256 != item.get("sha256"):
            failures.append(
                "Archived generated artifact does not match its validated "
                f"bytes: {relative}"
            )
            continue

        role = str(item.get("role") or "")
        if role in {
            "word_visual_inspection",
            "executive_summary_visual_inspection",
            "release_word_visual_inspection",
            "release_executive_summary_visual_inspection",
        }:
            from cli.publishing_quality import (
                qa_word_visual_inspection_receipt,
            )

            word_name = candidate.name.removesuffix(
                "-word-visual-inspection.json"
            )
            word_artifact = candidate.with_name(f"{word_name}.docx")
            inspection_report = qa_word_visual_inspection_receipt(
                candidate,
                artifact=word_artifact,
            )
            if not inspection_report.ok:
                failures.append(
                    f"{artifact_id}: "
                    + "; ".join(
                        f"{issue.code}: {issue.message}"
                        for issue in inspection_report.errors[:8]
                    )
                )
                continue

        if candidate.suffix.lower() == ".json" and (
            role.endswith("_qa")
            or role in {"publishing_quality", "presentation_qa"}
        ):
            try:
                quality = json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(
                    f"{artifact_id}: unreadable QA payload ({exc})"
                )
                continue
            if quality.get("ok") is not True:
                failures.append(
                    f"{artifact_id}: QA payload is not releaseable"
                )

    if failures:
        raise RuntimeError(
            "Committed archive is not releaseable:\n- "
            + "\n- ".join(failures)
        )

    release_dir = archive_dir / "release"
    if release_expected and not release_dir.is_dir():
        raise RuntimeError(
            "Committed archive is missing its required release bundle."
        )
    if release_dir.is_dir():
        from cli.publish import verify_release_bundle

        verify_release_bundle(release_dir)

    retrospective = _safe_archive_path(
        archive_dir,
        "retrospective.md",
        label="retrospective",
    )
    if retrospective.is_symlink() or not retrospective.is_file():
        raise RuntimeError(
            "Committed archive is missing its retrospective."
        )


def archive_path_for(repo_root: Path, slug: str) -> Path:
    """Return the canonical dated archive destination for a run."""

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,127}", slug):
        raise ValueError(f"Unsafe archive slug: {slug!r}")
    return repo_root / "runs" / f"{date.today().isoformat()}-{slug}"


def reserve_archive_path(
    *,
    repo_root: Path,
    slug: str,
    manifest_path: Path | None = None,
) -> Path:
    """Reject an archive collision before distribution is modified.

    An existing archive is accepted only as an idempotent cleanup retry when
    its run manifest is byte-identical to the active run manifest.
    """

    archive_dir = archive_path_for(repo_root, slug)
    if not archive_dir.exists():
        return archive_dir
    archived_manifest = archive_dir / "run-manifest.json"
    if (
        manifest_path is not None
        and manifest_path.is_file()
        and archived_manifest.is_file()
        and _sha256(manifest_path) == _sha256(archived_manifest)
    ):
        from cli.run_manifest import load_run_manifest

        manifest_sha256 = _sha256(manifest_path)
        _verify_committed_archive(
            archive_dir,
            load_run_manifest(archived_manifest),
            slug=slug,
            expected_manifest_sha256=manifest_sha256,
        )
        return archive_dir
    raise FileExistsError(
        f"Archive already exists: {archive_dir}. Pick a different slug."
    )


def archive_run(
    *,
    repo_root: Path,
    slug: str,
    tally: CostTally,
    run_file: Path | None = None,
    manifest_path: Path | None = None,
) -> Path:
    outputs_dir = repo_root / "outputs"
    runs_dir = repo_root / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = reserve_archive_path(
        repo_root=repo_root,
        slug=slug,
        manifest_path=manifest_path,
    )
    if archive_dir.exists():
        # ``reserve_archive_path`` has revalidated the exact committed prompt,
        # sources, generated artifacts, receipts, and release bundle. Cleanup
        # is idempotent and the manifest is deleted last, so retrying here is
        # both safe and recoverable.
        _bind_event_journal(archive_dir, preserve_existing=True)
        _clear_outputs(outputs_dir)
        return archive_dir
    manifest_payload: dict | None = None
    manifest_sha256: str | None = None
    if manifest_path is not None:
        from cli.run_manifest import assert_manifest_complete

        manifest_payload = assert_manifest_complete(manifest_path)
        manifest_sha256 = _sha256(manifest_path)
        if not manifest_sha256:
            raise RuntimeError("Could not fingerprint the active run manifest.")
        if run_file is None:
            raw_prompt = Path(
                str(manifest_payload.get("run", {}).get("run_prompt") or "")
            )
            run_file = (
                raw_prompt
                if raw_prompt.is_absolute()
                else repo_root / raw_prompt
            )
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{archive_dir.name}-", dir=runs_dir)
    )
    try:
        for sub in STAGE_DIRS:
            src = outputs_dir / sub
            if src.is_dir():
                shutil.copytree(src, temporary / sub)
        for sub in RUN_DIRS:
            src = outputs_dir / sub
            if src.is_dir():
                shutil.copytree(src, temporary / sub)
        for filename in RUN_ARTIFACTS:
            src = outputs_dir / filename
            if src.is_file():
                shutil.copy2(src, temporary / filename)

        # Preserve the exact executable prompt, not merely a mutable live path.
        if run_file is not None and run_file.is_file():
            shutil.copy2(run_file, temporary / "run-prompt.md")

        # Source material attached to this run (if any) lands in the archive
        # alongside the stages, so revisions and audits can still see it.
        from cli.sources import archive_sources

        archive_sources(
            slug,
            outputs_dir,
            temporary,
            source_material=(
                manifest_payload.get("run", {}).get("source_material", [])
                if manifest_payload is not None
                else None
            ),
        )

        _write_retrospective(temporary, slug, tally)
        if manifest_payload is not None:
            # Recheck the complete staged transaction after copying. This
            # closes the assert→copy race and gives cleanup retries exactly the
            # same archive-side validation contract as the fresh commit.
            _verify_committed_archive(
                temporary,
                manifest_payload,
                slug=slug,
                expected_manifest_sha256=manifest_sha256,
            )
        os.replace(temporary, archive_dir)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    # Clearing happens only after the complete archive directory has been
    # atomically promoted into place. The live sink mirrors the final
    # run-complete and stream-end events into the committed optional journal.
    _bind_event_journal(archive_dir, preserve_existing=False)
    _clear_outputs(outputs_dir)
    return archive_dir
