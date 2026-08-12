"""Scope-fulfillment mode — turn a client scope of work into its deliverables.

The single-report pipeline answers a question. This pipeline fulfills an
engagement: supply a scope document (RFP, SOW, or emailed scope), and the
Council plans the deliverables, researches the regulatory and
professional grounding once, then builds every required artifact — Word
documents and PowerPoint decks — with an acceptance-review QA pass at the end.

Stages (custom rail): Plan → Research → Build → Package.
Checkpoints: plan approval (before money is spent on production) and final
QA review (before packaging). Both honor auto_approve.

Every paid step is resumable only when its artifact hash and step-scoped
dependency receipt still match the exact source library, plan, research,
dependent deliverables, model route, agent charter, and executable contract.
Stale work is quarantined rather than silently mixed into a new package.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from rich.console import Console
from slugify import slugify

from cli.agents import load_all_agents
from cli.artifacts import contract_for_path
from cli.events import emit, request_checkpoint
from cli.orchestrator import (
    CostTally,
    _model,
    _notify_done,
    _required_outputs_match_manifest,
    _run_agent,
    write_run_marker,
)

console = Console()
REPO_ROOT = Path(__file__).resolve().parent.parent
SCOPE_STATE_SCHEMA_VERSION = "1.0"
SCOPE_STEP_CONTRACT_VERSION = "1.0"
SCOPE_PACKAGE_RECEIPT_VERSION = "1.0"
SCOPE_ARCHIVE_RECEIPT_VERSION = "1.0"
SCOPE_DISTRIBUTION_POINTER_VERSION = "1.0"
SCOPE_EXECUTION_FILES: tuple[str, ...] = (
    "AGENTS.md",
    "CLAUDE.md",
    "cli/scope.py",
    "cli/orchestrator.py",
    "cli/artifacts.py",
    "cli/run_manifest.py",
    "cli/sources.py",
    "council.toml",
    "package.json",
    "pyproject.toml",
)
SCOPE_EXECUTION_PATTERNS: tuple[str, ...] = ("assets/brand/**/*",)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _relative_regular_file(path: Path, repo_root: Path) -> dict[str, Any]:
    """Return a hash record for one trusted, non-symlink repository file."""

    candidate = Path(path)
    if candidate.is_symlink():
        raise RuntimeError(f"Scope input may not be a symlink: {candidate}")
    try:
        resolved = candidate.resolve(strict=True)
        relative = resolved.relative_to(repo_root.resolve())
    except (OSError, ValueError) as exc:
        raise RuntimeError(
            f"Scope input must be a regular file inside the repository: {candidate}"
        ) from exc
    if not resolved.is_file():
        raise RuntimeError(f"Scope input is not a regular file: {candidate}")
    return {
        "path": relative.as_posix(),
        "sha256": _file_sha256(resolved),
        "size_bytes": resolved.stat().st_size,
    }


def _scope_source_library(repo_root: Path, slug: str) -> list[Path]:
    """Return the complete immutable input set attached to one engagement."""

    source_dir = repo_root / "sources" / "runs" / slug
    if source_dir.is_symlink():
        raise RuntimeError(f"Scope source library may not be a symlink: {source_dir}")
    if not source_dir.is_dir():
        return []
    files: list[Path] = []
    for path in sorted(source_dir.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"Scope source files may not be symlinks: {path}")
        if path.is_file():
            files.append(path)
    return files


def _scope_readable_sources(repo_root: Path, slug: str) -> list[Path]:
    """Resolve the files agents should read from the durable source library."""

    files = _scope_source_library(repo_root, slug)
    extracted_originals = {
        path.with_name(path.name[: -len(".extracted.md")])
        for path in files
        if path.name.endswith(".extracted.md")
    }
    readable: list[Path] = []
    for path in files:
        if path in extracted_originals:
            continue
        if path.name.endswith(".extracted.md") or path.suffix.lower() in {
            ".md",
            ".txt",
            ".csv",
            ".json",
            ".yaml",
            ".yml",
            ".pdf",
            ".docx",
            ".pptx",
            ".xlsx",
        }:
            readable.append(path)
    return readable


def _scope_state_path(base: Path) -> Path:
    return base / "scope-state.json"


def _prepare_scope_state(
    *, base: Path, slug: str, title: str, operator_notes: str = ""
) -> Path:
    """Create or repair the manifest used by ``_run_agent`` for safe resume."""

    path = _scope_state_path(base)
    prior: dict[str, Any] | None = None
    if path.is_symlink():
        raise RuntimeError(f"Scope state may not be a symlink: {path}")
    if path.is_file():
        try:
            candidate = json.loads(path.read_text(encoding="utf-8"))
            if (
                candidate.get("schema_version") == SCOPE_STATE_SCHEMA_VERSION
                and isinstance(candidate.get("artifacts"), list)
                and candidate.get("run", {}).get("slug") == slug
            ):
                prior = candidate
        except (OSError, json.JSONDecodeError):
            prior = None
        if prior is None:
            _quarantine_scope_path(path)

    payload = prior or {
        "schema_version": SCOPE_STATE_SCHEMA_VERSION,
        "created_at": _now(),
        "artifacts": [],
    }
    payload["updated_at"] = _now()
    payload["run"] = {
        "slug": slug,
        "title": title,
        "operator_notes": operator_notes,
    }
    _atomic_json(path, payload)
    return path


def _scope_step_contract_path(base: Path, step_id: str) -> Path:
    safe = slugify(step_id, separator="-") or "step"
    identity = hashlib.sha256(step_id.encode("utf-8")).hexdigest()[:10]
    return base / "_state" / "inputs" / f"{safe}-{identity}.json"


def _write_scope_step_contract(
    *,
    repo_root: Path,
    base: Path,
    step_id: str,
    model: str,
    agent_path: Path | None,
    input_paths: Iterable[Path],
    membership_roots: Iterable[Path] = (),
    virtual_inputs: dict[str, Any] | None = None,
) -> Path:
    """Write the canonical, step-scoped dependency snapshot used for resume.

    The contract is refreshed before every possible skip. Its own bytes encode
    exact input membership and hashes, so a source, plan, brief, dependency,
    model route, agent charter, or executable contract change invalidates only
    the affected output and all stages that explicitly consume it.
    """

    paths = [Path(path) for path in input_paths]
    paths.extend(repo_root / relative for relative in SCOPE_EXECUTION_FILES)
    for pattern in SCOPE_EXECUTION_PATTERNS:
        paths.extend(
            path for path in sorted(repo_root.glob(pattern)) if path.is_file()
        )
    if agent_path is not None:
        paths.append(agent_path)

    records: dict[str, dict[str, Any]] = {}
    for path in paths:
        record = _relative_regular_file(path, repo_root)
        records[record["path"]] = record

    membership_sets: list[dict[str, Any]] = []
    for root in membership_roots:
        root = Path(root)
        if root.is_symlink() or not root.is_dir():
            raise RuntimeError(f"Scope membership root is unsafe or missing: {root}")
        try:
            relative_root = root.resolve().relative_to(repo_root.resolve())
        except ValueError as exc:
            raise RuntimeError(
                f"Scope membership root escapes the repository: {root}"
            ) from exc
        members = []
        for member in sorted(root.rglob("*")):
            if member.is_symlink():
                raise RuntimeError(f"Scope inputs may not contain symlinks: {member}")
            if member.is_file():
                members.append(member.resolve().relative_to(repo_root.resolve()).as_posix())
        membership_sets.append(
            {"root": relative_root.as_posix(), "files": members}
        )

    execution_patterns = []
    for pattern in SCOPE_EXECUTION_PATTERNS:
        execution_patterns.append(
            {
                "pattern": pattern,
                "files": [
                    path.resolve().relative_to(repo_root.resolve()).as_posix()
                    for path in sorted(repo_root.glob(pattern))
                    if path.is_file()
                ],
            }
        )

    payload = {
        "schema_version": SCOPE_STEP_CONTRACT_VERSION,
        "pipeline_contract": "scope-v2-hash-bound-resume",
        "step": step_id,
        "model": model,
        "virtual_inputs": virtual_inputs or {},
        "files": [records[key] for key in sorted(records)],
        "membership_sets": membership_sets,
        "execution_patterns": execution_patterns,
    }
    path = _scope_step_contract_path(base, step_id)
    _atomic_json(path, payload)
    return path


def _scope_step_contract_is_current(path: Path, repo_root: Path) -> bool:
    """Recheck the real upstream bytes encoded in one dependency contract."""

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != SCOPE_STEP_CONTRACT_VERSION:
            return False
        expected_files = payload.get("files")
        if not isinstance(expected_files, list):
            return False
        for expected in expected_files:
            if not isinstance(expected, dict):
                return False
            current = _relative_regular_file(
                repo_root / str(expected.get("path") or ""), repo_root
            )
            if current != expected:
                return False
        for membership in payload.get("membership_sets", []):
            root = repo_root / str(membership.get("root") or "")
            if root.is_symlink() or not root.is_dir():
                return False
            current_members = []
            for member in sorted(root.rglob("*")):
                if member.is_symlink():
                    return False
                if member.is_file():
                    current_members.append(
                        member.resolve().relative_to(repo_root.resolve()).as_posix()
                    )
            if current_members != membership.get("files"):
                return False
        for declaration in payload.get("execution_patterns", []):
            pattern = str(declaration.get("pattern") or "")
            current_members = [
                member.resolve().relative_to(repo_root.resolve()).as_posix()
                for member in sorted(repo_root.glob(pattern))
                if member.is_file()
            ]
            if current_members != declaration.get("files"):
                return False
        return True
    except (OSError, RuntimeError, TypeError, ValueError, json.JSONDecodeError):
        return False


def _assert_scope_outputs_current(
    *,
    repo_root: Path,
    base: Path,
    state_path: Path,
    outputs: Iterable[Path],
) -> None:
    """Final fail-closed gate for every paid Scope artifact and dependency."""

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("Scope resume state is missing or invalid.") from exc
    records = {
        str(item.get("path") or ""): item
        for item in state.get("artifacts", [])
        if isinstance(item, dict)
    }
    failures: list[str] = []
    for output in outputs:
        try:
            relative = output.resolve().relative_to(base.resolve()).as_posix()
        except ValueError:
            failures.append(f"{output}: output escapes the Scope workspace")
            continue
        record = records.get(relative)
        dependencies = record.get("dependencies") if record else None
        declarations = tuple(
            str(item.get("declared_input") or "")
            for item in (
                dependencies.get("inputs", [])
                if isinstance(dependencies, dict)
                else []
            )
            if isinstance(item, dict)
        )
        if (
            not record
            or not declarations
            or not _required_outputs_match_manifest(
                ((output, contract_for_path(output)),),
                state_path,
                declarations,
            )
        ):
            failures.append(f"{relative}: artifact or dependency receipt is stale")
            continue
        for declaration in declarations:
            contract_path = base / declaration
            if not _scope_step_contract_is_current(contract_path, repo_root):
                failures.append(
                    f"{relative}: upstream bytes changed after the step completed"
                )
    if failures:
        raise RuntimeError(
            "Scope release integrity check failed; outputs were preserved: "
            + "; ".join(failures)
        )


def _scope_dependency_declaration(path: Path, base: Path) -> tuple[str, ...]:
    try:
        relative = path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError as exc:
        raise RuntimeError(f"Scope dependency contract escapes {base}: {path}") from exc
    return (relative,)


def _quarantine_scope_path(path: Path) -> Path | None:
    """Move stale work aside without making it eligible for a resume skip."""

    if not path.exists() and not path.is_symlink():
        return None
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    stale = path.with_name(f"{path.name}.stale-{stamp}")
    os.replace(path, stale)
    return stale


def _quarantine_unplanned_outputs(
    *, research_dir: Path, deliverables_dir: Path, plan: dict[str, Any]
) -> None:
    expected_briefs = {
        f"{question['id']}-brief.md" for question in plan["research_questions"]
    }
    for path in research_dir.glob("*-brief.md"):
        if path.name not in expected_briefs:
            _quarantine_scope_path(path)

    expected_deliverables = {
        deliverable["filename"] for deliverable in plan["deliverables"]
    }
    for path in deliverables_dir.iterdir():
        if (
            path.is_file()
            and path.suffix.lower() in {".docx", ".pptx"}
            and path.name not in expected_deliverables
        ):
            _quarantine_scope_path(path)


def _tree_inventory(root: Path, *, exclude: set[str] | None = None) -> list[dict[str, Any]]:
    """Hash-bind exact tree membership; reject links and non-regular entries."""

    excluded = exclude or set()
    if root.is_symlink() or not root.is_dir():
        raise RuntimeError(f"Expected a regular directory: {root}")
    inventory: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"Packaged Scope outputs may not contain symlinks: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative in excluded:
            continue
        inventory.append(
            {
                "path": relative,
                "sha256": _file_sha256(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return inventory


def _scope_package_matches(
    *,
    receipt_path: Path,
    package_dir: Path,
    zip_path: Path,
    contract_sha256: str,
) -> bool:
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if (
            receipt.get("schema_version") != SCOPE_PACKAGE_RECEIPT_VERSION
            or receipt.get("dependency_contract_sha256") != contract_sha256
            or receipt.get("files") != _tree_inventory(package_dir)
            or receipt.get("zip", {}).get("sha256") != _file_sha256(zip_path)
            or receipt.get("zip", {}).get("size_bytes") != zip_path.stat().st_size
        ):
            return False
        with zipfile.ZipFile(zip_path) as archive:
            names = sorted(info.filename for info in archive.infolist())
        return names == sorted(item["path"] for item in receipt["files"])
    except (
        OSError,
        RuntimeError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ):
        return False


def _scope_distribution_matches(
    *,
    pointer_path: Path,
    receipt_path: Path,
    package_dir: Path,
    zip_path: Path,
    contract_sha256: str,
    slug: str,
) -> bool:
    """Verify the exact current Scope package exposed by the local UI."""

    try:
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
        if (
            pointer.get("schema_version")
            != SCOPE_DISTRIBUTION_POINTER_VERSION
            or pointer.get("status") != "current"
            or pointer.get("mode") != "scope"
            or pointer.get("slug") != slug
            or pointer.get("receipt", {}).get("path") != receipt_path.name
            or pointer.get("receipt", {}).get("sha256")
            != _file_sha256(receipt_path)
            or pointer.get("zip", {}).get("path") != zip_path.name
            or pointer.get("zip", {}).get("sha256") != _file_sha256(zip_path)
            or pointer.get("zip", {}).get("size_bytes")
            != zip_path.stat().st_size
            or pointer.get("package", {}).get("path") != package_dir.name
            or pointer.get("package", {}).get("files")
            != _tree_inventory(package_dir)
        ):
            return False
        return _scope_package_matches(
            receipt_path=receipt_path,
            package_dir=package_dir,
            zip_path=zip_path,
            contract_sha256=contract_sha256,
        )
    except (OSError, RuntimeError, TypeError, ValueError, json.JSONDecodeError):
        return False


def _publish_scope_distribution_pointer(
    *,
    repo_root: Path,
    base: Path,
    slug: str,
    title: str,
    archive_dir: Path,
    package_dir: Path,
    zip_path: Path,
    package_receipt: Path,
    ordered: list[dict[str, Any]],
) -> Path:
    """Atomically expose one hash-bound Scope ZIP without broad ZIP access."""

    reports_dir = (repo_root / "reports").resolve()
    receipt_copy = reports_dir / f"scope-{slug}-package-receipt.json"
    pointer_path = reports_dir / f"scope-{slug}-package-manifest.json"
    package_contract = _scope_step_contract_path(base, "package")
    contract_sha256 = _file_sha256(package_contract)
    if not _scope_package_matches(
        receipt_path=package_receipt,
        package_dir=package_dir,
        zip_path=zip_path,
        contract_sha256=contract_sha256,
    ):
        raise RuntimeError(
            "Scope package changed before distribution; download was withheld."
        )

    receipt_payload = json.loads(package_receipt.read_text(encoding="utf-8"))
    _atomic_json(receipt_copy, receipt_payload)
    pointer_payload = {
        "schema_version": SCOPE_DISTRIBUTION_POINTER_VERSION,
        "status": "current",
        "mode": "scope",
        "slug": slug,
        "title": title,
        "date": date.today().isoformat(),
        "archive_path": archive_dir.resolve().relative_to(
            repo_root.resolve()
        ).as_posix(),
        "receipt": {
            "path": receipt_copy.name,
            "sha256": _file_sha256(receipt_copy),
        },
        "zip": {
            "path": zip_path.resolve().relative_to(reports_dir).as_posix(),
            "sha256": _file_sha256(zip_path),
            "size_bytes": zip_path.stat().st_size,
        },
        "package": {
            "path": package_dir.resolve().relative_to(reports_dir).as_posix(),
            "files": _tree_inventory(package_dir),
        },
        "deliverables": [
            {
                "id": deliverable["id"],
                "title": deliverable["title"],
                "filename": deliverable["filename"],
            }
            for deliverable in ordered
        ],
    }
    _atomic_json(pointer_path, pointer_payload)
    if not _scope_distribution_matches(
        pointer_path=pointer_path,
        receipt_path=receipt_copy,
        package_dir=package_dir,
        zip_path=zip_path,
        contract_sha256=contract_sha256,
        slug=slug,
    ):
        raise RuntimeError(
            "Scope distribution pointer failed its exact-byte verification."
        )
    return pointer_path


def _promote_scope_package(
    *,
    repo_root: Path,
    base: Path,
    slug: str,
    plan: dict[str, Any],
    ordered: list[dict[str, Any]],
    built: dict[str, Path],
    qa_path: Path,
) -> tuple[Path, Path, Path]:
    """Build or safely reuse an exact, hash-bound client package."""

    reports_dir = repo_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    package_dir = reports_dir / f"scope-{slug}"
    zip_path = reports_dir / f"{slug}-deliverables.zip"
    receipt_path = base / "package-receipt.json"
    plan_markdown = render_plan_markdown(plan)
    manifest_text = (
        plan_markdown
        + "\n\n---\n\nProduced by the Transform Airports AI Council. "
        "AI-generated engagement materials — subject-matter-expert review "
        "required before client delivery.\n"
    )
    package_contract = _write_scope_step_contract(
        repo_root=repo_root,
        base=base,
        step_id="package",
        model="deterministic",
        agent_path=None,
        input_paths=[
            base / "plan.json",
            base / "plan.md",
            qa_path,
            *(built[deliverable["id"]] for deliverable in ordered),
        ],
        membership_roots=[repo_root / "sources" / "runs" / slug],
        virtual_inputs={
            "slug": slug,
            "deliverables": [
                {
                    "id": deliverable["id"],
                    "filename": deliverable["filename"],
                }
                for deliverable in ordered
            ],
            "manifest_text": manifest_text,
        },
    )
    contract_sha256 = _file_sha256(package_contract)
    if _scope_package_matches(
        receipt_path=receipt_path,
        package_dir=package_dir,
        zip_path=zip_path,
        contract_sha256=contract_sha256,
    ):
        return package_dir, zip_path, receipt_path

    staging_root = Path(
        tempfile.mkdtemp(prefix=f".scope-{slug}-", dir=reports_dir)
    )
    staged_package = staging_root / package_dir.name
    staged_zip = staging_root / zip_path.name
    try:
        staged_package.mkdir()
        for deliverable in ordered:
            shutil.copy2(
                built[deliverable["id"]],
                staged_package / deliverable["filename"],
            )
        shutil.copy2(qa_path, staged_package / "qa-report.md")
        (staged_package / "MANIFEST.md").write_text(
            manifest_text, encoding="utf-8"
        )
        files = _tree_inventory(staged_package)
        with zipfile.ZipFile(staged_zip, "w", zipfile.ZIP_DEFLATED) as archive:
            for item in files:
                archive.write(staged_package / item["path"], item["path"])
        receipt = {
            "schema_version": SCOPE_PACKAGE_RECEIPT_VERSION,
            "created_at": _now(),
            "slug": slug,
            "dependency_contract": package_contract.relative_to(base).as_posix(),
            "dependency_contract_sha256": contract_sha256,
            "files": files,
            "zip": {
                "path": zip_path.name,
                "sha256": _file_sha256(staged_zip),
                "size_bytes": staged_zip.stat().st_size,
            },
        }

        if package_dir.exists() or package_dir.is_symlink():
            _quarantine_scope_path(package_dir)
        if zip_path.exists() or zip_path.is_symlink():
            _quarantine_scope_path(zip_path)
        os.replace(staged_package, package_dir)
        os.replace(staged_zip, zip_path)
        _atomic_json(receipt_path, receipt)
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)

    if not _scope_package_matches(
        receipt_path=receipt_path,
        package_dir=package_dir,
        zip_path=zip_path,
        contract_sha256=contract_sha256,
    ):
        raise RuntimeError("Scope package failed its post-promotion hash check.")
    return package_dir, zip_path, receipt_path


def _scope_archive_matches(
    archive_dir: Path, *, package_receipt_sha256: str
) -> bool:
    receipt_path = archive_dir / "archive-receipt.json"
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        return bool(
            receipt.get("schema_version") == SCOPE_ARCHIVE_RECEIPT_VERSION
            and receipt.get("package_receipt_sha256") == package_receipt_sha256
            and receipt.get("files")
            == _tree_inventory(archive_dir, exclude={"archive-receipt.json"})
        )
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError):
        return False


def _archive_scope_run(
    *,
    repo_root: Path,
    base: Path,
    slug: str,
    title: str,
    deliverable_count: int,
    total_cost: float,
    package_receipt: Path,
) -> Path:
    """Commit an exact archive, reusing only a byte-for-byte matching retry."""

    package_receipt_sha256 = _file_sha256(package_receipt)
    runs_dir = repo_root / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{date.today().isoformat()}-scope-{slug}"
    first = runs_dir / stem
    if first.is_dir() and _scope_archive_matches(
        first, package_receipt_sha256=package_receipt_sha256
    ):
        return first

    archive_dir = first
    suffix = 2
    while archive_dir.exists() or archive_dir.is_symlink():
        archive_dir = runs_dir / f"{stem}-{suffix}"
        if archive_dir.is_dir() and _scope_archive_matches(
            archive_dir, package_receipt_sha256=package_receipt_sha256
        ):
            return archive_dir
        suffix += 1

    # Validate both trees before copytree can follow an unexpected link.
    _tree_inventory(base)
    source_dir = repo_root / "sources" / "runs" / slug
    if source_dir.is_dir():
        _tree_inventory(source_dir)

    staging_root = Path(tempfile.mkdtemp(prefix=f".{stem}-", dir=runs_dir))
    staged_archive = staging_root / archive_dir.name
    try:
        shutil.copytree(base, staged_archive)
        if source_dir.is_dir():
            shutil.copytree(source_dir, staged_archive / "sources")
        (staged_archive / "retrospective.md").write_text(
            f"# Scope engagement — {title}\n\n"
            f"Archived {date.today().isoformat()}. {deliverable_count} "
            f"deliverables, total cost ${total_cost:.2f}.\n",
            encoding="utf-8",
        )
        _atomic_json(
            staged_archive / "archive-receipt.json",
            {
                "schema_version": SCOPE_ARCHIVE_RECEIPT_VERSION,
                "created_at": _now(),
                "slug": slug,
                "package_receipt_sha256": package_receipt_sha256,
                "files": _tree_inventory(staged_archive),
            },
        )
        os.replace(staged_archive, archive_dir)
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)

    if not _scope_archive_matches(
        archive_dir, package_receipt_sha256=package_receipt_sha256
    ):
        raise RuntimeError("Scope archive failed its post-promotion hash check.")
    return archive_dir


@dataclass
class ScopeResult:
    tally: CostTally
    slug: str = ""
    archive_path: Path | None = None
    package_dir: Path | None = None
    zip_path: Path | None = None
    completed: bool = False


# ----------------------------------------------------------------------------
# Plan handling.
# ----------------------------------------------------------------------------

VALID_KINDS = {"docx", "pptx"}
SAFE_SCOPE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")


def parse_plan(raw: str) -> dict:
    """Parse and validate the planner's JSON. Raises ValueError with a
    message suitable for feeding back to the planner on retry."""
    text = raw.strip()
    # Strip a markdown fence if the model wrapped one despite instructions.
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    try:
        plan = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"plan.json is not valid JSON: {e}") from e

    if not isinstance(plan, dict):
        raise ValueError("plan.json must contain one JSON object")
    if not isinstance(plan.get("deliverables"), list) or not plan["deliverables"]:
        raise ValueError("plan must contain a non-empty 'deliverables' list")
    seen_ids: set[str] = set()
    seen_filenames: set[str] = set()
    for d in plan["deliverables"]:
        if not isinstance(d, dict):
            raise ValueError(f"deliverable must be an object: {d!r}")
        for key in ("id", "title", "kind", "filename", "instructions"):
            if not d.get(key):
                raise ValueError(f"deliverable missing '{key}': {d}")
        if d["kind"] not in VALID_KINDS:
            raise ValueError(f"deliverable {d['id']}: kind must be docx or pptx")
        if not SAFE_SCOPE_ID.fullmatch(str(d["id"])):
            raise ValueError(f"unsafe deliverable id {d['id']!r}")
        if d["id"] in seen_ids:
            raise ValueError(f"duplicate deliverable id {d['id']}")
        seen_ids.add(d["id"])
        d.setdefault("depends_on", [])
        if not isinstance(d["depends_on"], list) or any(
            not isinstance(dependency, str) for dependency in d["depends_on"]
        ):
            raise ValueError(
                f"deliverable {d['id']}: depends_on must be a list of ids"
            )
        raw_filename = str(d["filename"])
        d["filename"] = Path(raw_filename).name
        if d["filename"] != raw_filename or d["filename"].startswith("."):
            raise ValueError(f"unsafe deliverable filename {raw_filename!r}")
        if d["filename"] in seen_filenames:
            raise ValueError(f"duplicate deliverable filename {d['filename']}")
        seen_filenames.add(d["filename"])
        if Path(d["filename"]).suffix.lower() != f".{d['kind']}":
            raise ValueError(
                f"deliverable {d['id']}: filename extension must match kind "
                f"{d['kind']}"
            )
    for d in plan["deliverables"]:
        for dep in d["depends_on"]:
            if dep not in seen_ids:
                raise ValueError(f"deliverable {d['id']} depends on unknown id {dep}")
    if not isinstance(plan.get("research_questions"), list):
        plan["research_questions"] = []
    seen_research_ids: set[str] = set()
    for i, r in enumerate(plan["research_questions"]):
        if not isinstance(r, dict):
            raise ValueError(f"research question must be an object: {r!r}")
        r.setdefault("id", f"R{i + 1}")
        if not SAFE_SCOPE_ID.fullmatch(str(r["id"])):
            raise ValueError(f"unsafe research question id {r['id']!r}")
        if r["id"] in seen_research_ids:
            raise ValueError(f"duplicate research question id {r['id']}")
        seen_research_ids.add(r["id"])
    plan.setdefault("gaps", [])
    return plan


def order_deliverables(plan: dict) -> list[dict]:
    """Topological order; raises ValueError on dependency cycles."""
    items = {d["id"]: d for d in plan["deliverables"]}
    ordered: list[dict] = []
    state: dict[str, int] = {}  # 0 unvisited, 1 visiting, 2 done

    def visit(did: str) -> None:
        if state.get(did) == 2:
            return
        if state.get(did) == 1:
            raise ValueError(f"dependency cycle involving {did}")
        state[did] = 1
        for dep in items[did]["depends_on"]:
            visit(dep)
        state[did] = 2
        ordered.append(items[did])

    for did in items:
        visit(did)
    return ordered


def render_plan_markdown(plan: dict) -> str:
    lines = [f"# Engagement plan — {plan.get('engagement', 'Untitled')}", ""]
    lines += [plan.get("summary", ""), ""]
    if plan.get("client_context"):
        lines += [f"**Client context:** {plan['client_context']}", ""]
    lines += ["## Deliverables", "",
              "| # | Deliverable | Type | Depends on | Scope basis |",
              "|---|---|---|---|---|"]
    for d in plan["deliverables"]:
        deps = ", ".join(d["depends_on"]) or "—"
        lines.append(f"| {d['id']} | {d['title']} | {d['kind']} | {deps} | {d.get('scope_basis', '—')} |")
    lines += ["", f"**{len(plan['deliverables'])} artifacts**", ""]
    if plan["research_questions"]:
        lines += ["## Research questions", ""]
        for r in plan["research_questions"]:
            lines.append(f"- **{r['id']}** — {r.get('topic', '')}: {r.get('questions', '')}")
        lines.append("")
    if plan["gaps"]:
        lines += ["## Gaps — material not supplied", ""]
        for g in plan["gaps"]:
            lines.append(f"- ⚠ {g}")
        lines += ["", "_Builders will use marked `[AUTHORITY-SPECIFIC — INSERT: …]` "
                  "placeholders for these — never invented client content._"]
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# The pipeline.
# ----------------------------------------------------------------------------

async def run_scope_pipeline(
    *,
    title: str,
    notes: str | None = None,
    source_files: Iterable[Path] | None = None,
    repo_root: Path = REPO_ROOT,
    auto_approve: bool = False,
    budget_usd: float | None = None,
) -> ScopeResult:
    from cli.interactive import RunSpec
    from cli.sources import attach_sources, discover_dropzone

    slug = slugify(title) or "scope-engagement"
    base = repo_root / "outputs" / "scope" / slug
    (base / "research").mkdir(parents=True, exist_ok=True)
    (base / "deliverables").mkdir(parents=True, exist_ok=True)
    scripts_dir = base / "_scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    # Keep the deliverables folder clean — only real artifacts belong there.
    for stray in (base / "deliverables").glob("*.py"):
        stray.rename(scripts_dir / stray.name)

    tally = CostTally(budget_usd=budget_usd)
    result = ScopeResult(tally=tally, slug=slug)
    agents = {a.name: a for a in load_all_agents()}
    if notes is None:
        try:
            prior_state = json.loads(
                _scope_state_path(base).read_text(encoding="utf-8")
            )
            notes = str(prior_state.get("run", {}).get("operator_notes") or "")
        except (OSError, json.JSONDecodeError):
            notes = ""

    # Browser runs pass an explicit, isolated selection. Terminal runs retain
    # the source-folder workflow when no explicit selection is provided.
    supplied = (
        discover_dropzone(repo_root / "sources")
        if source_files is None
        else [Path(path) for path in source_files]
    )
    if supplied:
        attach_sources(slug, supplied, repo_root / "outputs")
    source_inventory = _scope_source_library(repo_root, slug)
    source_paths = [
        path.relative_to(repo_root).as_posix()
        for path in _scope_readable_sources(repo_root, slug)
    ]
    if not source_paths:
        if source_files is None:
            raise RuntimeError(
                "No scope documents found. Drop the scope (PDF, Word, or text) "
                "into sources/ and relaunch."
            )
        raise RuntimeError("No scope documents found. Add at least one document and relaunch.")
    state_path = _prepare_scope_state(
        base=base, slug=slug, title=title, operator_notes=notes
    )

    async def _scope_call(
        *,
        agent_name: str,
        step_id: str,
        user_prompt: str,
        model_role: str,
        output_path: Path,
        input_paths: Iterable[Path],
        virtual_inputs: dict[str, Any],
    ) -> dict[str, object]:
        agent = agents[agent_name]
        model_id = _model(model_role)
        contract_path = _write_scope_step_contract(
            repo_root=repo_root,
            base=base,
            step_id=step_id,
            model=model_id,
            agent_path=agent.path,
            input_paths=input_paths,
            membership_roots=[repo_root / "sources" / "runs" / slug],
            virtual_inputs=virtual_inputs,
        )
        return await _run_agent(
            agent=agent,
            user_prompt=user_prompt,
            model=model_id,
            cwd=repo_root,
            step_label=f"scope/{step_id}",
            tally=tally,
            output_path=output_path,
            manifest_path=state_path,
            artifact_id=f"scope/{step_id}",
            dependency_inputs=_scope_dependency_declaration(contract_path, base),
        )

    spec = RunSpec(title=title, slug=slug, thesis=f"Scope engagement: {title}",
                   output_format="report", source_paths=source_paths)
    marker_spec = spec
    write_run_marker(repo_root / "outputs", marker_spec)
    # Tag the marker so resume routes back into scope mode.
    marker_path = repo_root / "outputs" / ".active-run.json"
    marker = json.loads(marker_path.read_text())
    marker["mode"] = "scope"
    marker["scope_notes"] = notes
    marker_path.write_text(json.dumps(marker, indent=2))

    await emit("run_start", slug=slug, title=title, mode="scope",
               agents=["scope-planner", "scope-researcher", "scope-builder", "scope-qa"],
               stages=["Plan", "Research", "Build", "Package"])

    src_list = "\n".join(f"- `{p}`" for p in source_paths)

    # ─── Stage 1: Plan ───
    await emit("stage_start", stage=1, label="Reading the scope & planning deliverables")
    console.rule("[bold]Scope — planning[/bold]")
    plan_path = base / "plan.json"
    plan: dict | None = None
    planner_note = f"\n\nOperator notes for this engagement:\n{notes}" if notes.strip() else ""

    for attempt in range(3):
        await _scope_call(
            agent_name="scope-planner",
            step_id="plan",
            user_prompt=(
                "Read the client scope document(s) and any supporting material:\n"
                f"{src_list}\n\n"
                f"Write the engagement plan as JSON to: `{plan_path.relative_to(repo_root).as_posix()}`"
                f"{planner_note}"
            ),
            model_role="synthesis",
            output_path=plan_path,
            input_paths=source_inventory,
            virtual_inputs={
                "title": title,
                "operator_notes": notes,
                "source_paths": source_paths,
            },
        )
        try:
            plan = parse_plan(plan_path.read_text(encoding="utf-8"))
            break
        except ValueError as e:
            _quarantine_scope_path(plan_path)
            planner_note += (
                f"\n\nYour previous plan.json was invalid and has been quarantined. "
                f"The error: {e}. Produce corrected, valid JSON."
            )
    if plan is None:
        plan = parse_plan(plan_path.read_text(encoding="utf-8"))

    # Plan checkpoint.
    while not auto_approve:
        decision = await request_checkpoint("scope-plan", {
            "title": "Engagement plan — approve before production",
            "subtitle": f"{len(plan['deliverables'])} artifacts. Nothing below has been built or billed yet.",
            "documents": [{"name": "The plan", "content": render_plan_markdown(plan)}],
            "actions": ["continue", "redo", "abort"],
        }) or {"action": "abort"}
        action = decision.get("action")
        if action == "continue":
            break
        if action == "redo":
            _quarantine_scope_path(plan_path)
            note = str(decision.get("notes", "")).strip()
            await _scope_call(
                agent_name="scope-planner",
                step_id="plan",
                user_prompt=(
                    "Read the client scope document(s) and any supporting material:\n"
                    f"{src_list}\n\n"
                    f"Write the engagement plan as JSON to: `{plan_path.relative_to(repo_root).as_posix()}`"
                    f"{planner_note}\n\nThe operator reviewed your previous plan and asked for "
                    f"this redo with the following notes — address them directly:\n{note}"
                ),
                model_role="synthesis",
                output_path=plan_path,
                input_paths=source_inventory,
                virtual_inputs={
                    "title": title,
                    "operator_notes": notes,
                    "operator_redo_notes": note,
                    "source_paths": source_paths,
                },
            )
            plan = parse_plan(plan_path.read_text(encoding="utf-8"))
            continue
        console.print("[yellow]Stopped at plan review.[/yellow]")
        return result

    (base / "plan.md").write_text(render_plan_markdown(plan), encoding="utf-8")
    _quarantine_unplanned_outputs(
        research_dir=base / "research",
        deliverables_dir=base / "deliverables",
        plan=plan,
    )

    # ─── Stage 2: Research ───
    await emit("stage_start", stage=2, label=f"Researching — {len(plan['research_questions'])} questions in parallel")
    console.rule("[bold]Scope — research[/bold]")
    sem = asyncio.Semaphore(4)
    brief_paths = [
        base / "research" / f"{question['id']}-brief.md"
        for question in plan["research_questions"]
    ]
    briefs_by_id = {
        question["id"]: path
        for question, path in zip(plan["research_questions"], brief_paths)
    }

    async def _research(rq: dict) -> None:
        out = briefs_by_id[rq["id"]]
        async with sem:
            await _scope_call(
                agent_name="scope-researcher",
                step_id=f"research-{rq['id']}",
                user_prompt=(
                    f"Engagement: {plan.get('engagement', title)}\n"
                    f"Context: {plan.get('summary', '')}\n\n"
                    f"Your assigned research question ({rq['id']}): {rq.get('topic', '')}\n"
                    f"{rq.get('questions', '')}\n\n"
                    f"The scope documents, for context:\n{src_list}\n\n"
                    f"Write your brief to: `{out.relative_to(repo_root).as_posix()}`"
                ),
                model_role="research",
                output_path=out,
                input_paths=[*source_inventory, plan_path],
                virtual_inputs={
                    "title": title,
                    "engagement": plan.get("engagement", title),
                    "summary": plan.get("summary", ""),
                    "research_question": rq,
                    "source_paths": source_paths,
                },
            )

    if plan["research_questions"]:
        await asyncio.gather(*(_research(rq) for rq in plan["research_questions"]))

    briefs_list = "\n".join(
        f"- `{p.relative_to(repo_root).as_posix()}`" for p in brief_paths
    ) or "(none commissioned)"
    gaps_text = "\n".join(f"- {g}" for g in plan.get("gaps", [])) or "(none identified)"

    # ─── Stage 3: Build ───
    ordered = order_deliverables(plan)
    await emit("stage_start", stage=3, label=f"Building {len(ordered)} deliverables")
    console.rule(f"[bold]Scope — building {len(ordered)} deliverables[/bold]")
    built: dict[str, Path] = {}
    build_sem = asyncio.Semaphore(2)
    done_ids: set[str] = set()

    async def _build(d: dict) -> None:
        out = base / "deliverables" / d["filename"]
        deps_list = "\n".join(
            f"- {dep}: `{built[dep].relative_to(repo_root).as_posix()}`"
            for dep in d["depends_on"] if dep in built
        ) or "(none)"
        async with build_sem:
            await _scope_call(
                agent_name="scope-builder",
                step_id=f"build-{d['id']}",
                user_prompt=(
                    f"Engagement: {plan.get('engagement', title)}\n"
                    f"Client context: {plan.get('client_context', '')}\n\n"
                    f"YOUR ASSIGNED DELIVERABLE — {d['id']}: {d['title']} ({d['kind']})\n"
                    f"Scope basis: {d.get('scope_basis', '')}\n\n"
                    f"Build instructions:\n{d['instructions']}\n\n"
                    f"Scope documents:\n{src_list}\n\n"
                    f"Research briefs:\n{briefs_list}\n\n"
                    f"Completed dependencies (binding — align with them):\n{deps_list}\n\n"
                    f"Known gaps (use marked placeholders, never invent):\n{gaps_text}\n\n"
                    f"Write any build scripts into: "
                    f"`{scripts_dir.relative_to(repo_root).as_posix()}/` "
                    f"(never into the deliverables folder).\n"
                    f"Remember: do NOT open .docx/.pptx dependencies with Read — "
                    f"extract their headings/slide titles with a short script instead, "
                    f"and keep every command's output under ~150 lines.\n\n"
                    f"Save the finished {d['kind']} to exactly: "
                    f"`{out.relative_to(repo_root).as_posix()}`"
                ),
                model_role="editor",
                output_path=out,
                input_paths=[
                    *source_inventory,
                    plan_path,
                    *brief_paths,
                    *(built[dependency] for dependency in d["depends_on"]),
                ],
                virtual_inputs={
                    "title": title,
                    "engagement": plan.get("engagement", title),
                    "client_context": plan.get("client_context", ""),
                    "deliverable": d,
                    "gaps": plan.get("gaps", []),
                    "source_paths": source_paths,
                    "research_briefs": [
                        path.relative_to(repo_root).as_posix()
                        for path in brief_paths
                    ],
                    "completed_dependencies": {
                        dependency: built[dependency].relative_to(
                            repo_root
                        ).as_posix()
                        for dependency in d["depends_on"]
                    },
                },
            )
        built[d["id"]] = out
        done_ids.add(d["id"])
        await emit("deliverable_done", id=d["id"], title=d["title"],
                   file=d["filename"], done=len(done_ids), total=len(ordered))

    # Build in dependency waves: everything whose deps are satisfied runs
    # concurrently (bounded by the semaphore); the next wave follows.
    remaining = list(ordered)
    while remaining:
        wave = [d for d in remaining if all(dep in built for dep in d["depends_on"])]
        if not wave:
            raise RuntimeError("dependency deadlock in plan — check depends_on")
        await asyncio.gather(*(_build(d) for d in wave))
        remaining = [d for d in remaining if d["id"] not in built]

    # ─── QA + final checkpoint ───
    qa_path = base / "qa-report.md"
    files_list = "\n".join(
        f"- {d['id']} ({d['title']}): `{built[d['id']].relative_to(repo_root).as_posix()}`"
        for d in ordered
    )
    await _scope_call(
        agent_name="scope-qa",
        step_id="qa",
        user_prompt=(
            f"Engagement: {plan.get('engagement', title)}\n\n"
            f"Original scope documents:\n{src_list}\n\n"
            f"The engagement plan: `{(base / 'plan.md').relative_to(repo_root).as_posix()}`\n\n"
            f"Produced deliverables:\n{files_list}\n\n"
            f"Write your acceptance review to: `{qa_path.relative_to(repo_root).as_posix()}`"
        ),
        model_role="factcheck",
        output_path=qa_path,
        input_paths=[
            *source_inventory,
            plan_path,
            base / "plan.md",
            *(built[deliverable["id"]] for deliverable in ordered),
        ],
        virtual_inputs={
            "title": title,
            "engagement": plan.get("engagement", title),
            "source_paths": source_paths,
            "deliverables": [
                {
                    "id": deliverable["id"],
                    "title": deliverable["title"],
                    "path": built[deliverable["id"]].relative_to(
                        repo_root
                    ).as_posix(),
                }
                for deliverable in ordered
            ],
        },
    )

    if not auto_approve:
        decision = await request_checkpoint("scope-final", {
            "title": "Acceptance review — final checkpoint",
            "subtitle": "The QA agent's deliverable-by-deliverable audit against the scope.",
            "documents": [
                {"name": "QA report", "content": qa_path.read_text(encoding="utf-8", errors="ignore")},
                {"name": "The plan", "content": render_plan_markdown(plan)},
            ],
            "actions": ["approve", "abort"],
        }) or {"action": "abort"}
        if decision.get("action") != "approve":
            console.print("[yellow]Stopped at final review. Deliverables remain in outputs/scope/.[/yellow]")
            return result

    # ─── Stage 4: Package ───
    paid_outputs = [
        plan_path,
        *brief_paths,
        *(built[deliverable["id"]] for deliverable in ordered),
        qa_path,
    ]
    _assert_scope_outputs_current(
        repo_root=repo_root,
        base=base,
        state_path=state_path,
        outputs=paid_outputs,
    )
    await emit("stage_start", stage=4, label="Packaging & archiving")
    console.rule("[bold]Scope — packaging[/bold]")

    package_dir, zip_path, package_receipt = _promote_scope_package(
        repo_root=repo_root,
        base=base,
        slug=slug,
        plan=plan,
        ordered=ordered,
        built=built,
        qa_path=qa_path,
    )
    archive_dir = _archive_scope_run(
        repo_root=repo_root,
        base=base,
        slug=slug,
        title=title,
        deliverable_count=len(ordered),
        total_cost=tally.total,
        package_receipt=package_receipt,
    )

    package_contract = _scope_step_contract_path(base, "package")
    if not _scope_package_matches(
        receipt_path=package_receipt,
        package_dir=package_dir,
        zip_path=zip_path,
        contract_sha256=_file_sha256(package_contract),
    ):
        raise RuntimeError(
            "Scope package changed after archiving; outputs were preserved."
        )
    if not _scope_archive_matches(
        archive_dir,
        package_receipt_sha256=_file_sha256(package_receipt),
    ):
        raise RuntimeError(
            "Scope archive changed before cleanup; outputs were preserved."
        )
    _assert_scope_outputs_current(
        repo_root=repo_root,
        base=base,
        state_path=state_path,
        outputs=paid_outputs,
    )
    _publish_scope_distribution_pointer(
        repo_root=repo_root,
        base=base,
        slug=slug,
        title=title,
        archive_dir=archive_dir,
        package_dir=package_dir,
        zip_path=zip_path,
        package_receipt=package_receipt,
        ordered=ordered,
    )
    from cli.archive import _clear_outputs
    _clear_outputs(repo_root / "outputs")

    result.archive_path = archive_dir
    result.package_dir = package_dir
    result.zip_path = zip_path
    result.completed = True
    await emit("run_complete", slug=slug, title=title, mode="scope",
               total=tally.total,
               deliverables=[{"id": d["id"], "title": d["title"], "file": d["filename"]}
                             for d in ordered],
               zip=f"/download/{zip_path.name}")
    _notify_done("AI Council", f"Scope engagement complete: {title} (${tally.total:.2f})")
    return result
