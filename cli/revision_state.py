"""Durable, hash-bound resume state for focused Council revisions.

Revision inputs span the dated archive, the active ``revisions/vN`` directory,
agent charters, and repository-level publishing contracts.  The normal run
manifest is rooted at ``outputs/`` and intentionally cannot fingerprint those
paths.  This module provides the same fail-closed guarantee for revision mode
without weakening the normal-run path boundary.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from cli.artifacts import ArtifactContract, validate_artifact


SCHEMA_VERSION = "1.0"
STATE_NAME = "revision-execution.json"


@dataclass(frozen=True)
class RevisionDependency:
    """One repo-relative file or glob consumed by a revision step."""

    declaration: str
    required: bool = True


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_relative(repo_root: Path, path: Path) -> str:
    """Return a normalized repo-relative path or fail closed."""

    root = repo_root.resolve()
    candidate = path.resolve(strict=False)
    try:
        return candidate.relative_to(root).as_posix()
    except ValueError as exc:
        raise ValueError(
            f"Revision dependency is outside the repository: {path}"
        ) from exc


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _object_without_duplicate_keys(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    """Reject JSON objects whose apparent mapping hides duplicate records."""

    payload: dict[str, Any] = {}
    for key, value in pairs:
        if key in payload:
            raise ValueError(f"duplicate JSON key: {key}")
        payload[key] = value
    return payload


def load_revision_state(state_path: Path) -> dict[str, Any]:
    """Read revision state; malformed or legacy state is never trusted."""

    try:
        payload = json.loads(
            state_path.read_text(encoding="utf-8"),
            object_pairs_hook=_object_without_duplicate_keys,
        )
    except (OSError, ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return {
            "schema_version": SCHEMA_VERSION,
            "created_at": _now(),
            "updated_at": _now(),
            "steps": {},
        }
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != SCHEMA_VERSION
        or not isinstance(payload.get("steps"), dict)
    ):
        return {
            "schema_version": SCHEMA_VERSION,
            "created_at": _now(),
            "updated_at": _now(),
            "steps": {},
        }
    return payload


def build_revision_dependency_fingerprint(
    *,
    repo_root: Path,
    dependencies: Iterable[RevisionDependency],
    values: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Hash exact input bytes, glob membership, and non-file call settings."""

    root = repo_root.resolve()
    declarations = list(dict.fromkeys(dependencies))
    records: list[dict[str, Any]] = []
    complete = True

    for dependency in declarations:
        declaration = str(dependency.declaration)
        record: dict[str, Any] = {
            "declaration": declaration,
            "required": bool(dependency.required),
            "files": [],
        }
        relative = Path(declaration)
        if (
            not declaration
            or relative.is_absolute()
            or ".." in relative.parts
        ):
            complete = False
            record["error"] = "dependency path escapes the repository"
            records.append(record)
            continue

        has_glob = any(character in declaration for character in "*?[")
        try:
            candidates = (
                sorted(root.glob(declaration))
                if has_glob
                else [root / relative]
            )
        except (OSError, ValueError):
            candidates = []

        unsafe_match = False
        for candidate in candidates:
            if candidate.is_dir() and not candidate.is_symlink():
                continue
            try:
                if candidate.is_symlink():
                    unsafe_match = True
                    continue
                resolved = candidate.resolve(strict=True)
                resolved.relative_to(root)
            except (OSError, ValueError):
                unsafe_match = True
                continue
            if not resolved.is_file():
                unsafe_match = True
                continue
            try:
                size_bytes = resolved.stat().st_size
                digest = _sha256(resolved)
            except OSError:
                unsafe_match = True
                continue
            record["files"].append(
                {
                    "path": resolved.relative_to(root).as_posix(),
                    "sha256": digest,
                    "size_bytes": size_bytes,
                }
            )
        record["files"].sort(key=lambda item: str(item["path"]))
        if unsafe_match:
            complete = False
            record["error"] = "dependency contains an unsafe or unreadable match"
        elif dependency.required and not record["files"]:
            complete = False
            record["error"] = "required dependency matched no regular files"
        records.append(record)

    canonical_values = dict(values or {})
    fingerprint: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "complete": complete,
        "inputs": records,
        "values": canonical_values,
    }
    fingerprint["sha256"] = hashlib.sha256(
        json.dumps(
            fingerprint,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()
    return fingerprint


def _contract_payload(contract: ArtifactContract) -> dict[str, Any]:
    return asdict(contract)


def revision_step_matches(
    *,
    state_path: Path,
    repo_root: Path,
    step_id: str,
    dependencies: Iterable[RevisionDependency],
    values: dict[str, Any],
    outputs: tuple[tuple[Path, ArtifactContract], ...],
) -> tuple[bool, dict[str, Any]]:
    """Return whether one completed step still matches every current byte."""

    fingerprint = build_revision_dependency_fingerprint(
        repo_root=repo_root,
        dependencies=dependencies,
        values=values,
    )
    if fingerprint.get("complete") is not True:
        return False, fingerprint

    payload = load_revision_state(state_path)
    record = payload.get("steps", {}).get(step_id)
    if not isinstance(record, dict):
        return False, fingerprint
    recorded_fingerprint = record.get("dependencies")
    if (
        not isinstance(recorded_fingerprint, dict)
        or recorded_fingerprint.get("sha256") != fingerprint.get("sha256")
    ):
        return False, fingerprint

    expected_paths = [repo_relative(repo_root, path) for path, _ in outputs]
    recorded_outputs = record.get("outputs")
    if not isinstance(recorded_outputs, list) or [
        str(item.get("path") or "")
        for item in recorded_outputs
        if isinstance(item, dict)
    ] != expected_paths:
        return False, fingerprint

    for (path, contract), item in zip(
        outputs, recorded_outputs, strict=True
    ):
        if not isinstance(item, dict):
            return False, fingerprint
        validation = validate_artifact(path, contract)
        if (
            not validation.valid
            or not validation.sha256
            or item.get("sha256") != validation.sha256
            or item.get("size_bytes") != validation.size_bytes
        ):
            return False, fingerprint
    return True, fingerprint


def record_revision_step(
    *,
    state_path: Path,
    repo_root: Path,
    step_id: str,
    dependencies: Iterable[RevisionDependency],
    values: dict[str, Any],
    outputs: tuple[tuple[Path, ArtifactContract], ...],
    dependency_fingerprint: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Atomically commit one step only after all inputs and outputs validate."""

    fingerprint = dependency_fingerprint or build_revision_dependency_fingerprint(
        repo_root=repo_root,
        dependencies=dependencies,
        values=values,
    )
    if fingerprint.get("complete") is not True:
        raise RuntimeError(
            f"Revision step {step_id!r} cannot bind missing or unsafe inputs."
        )

    output_records: list[dict[str, Any]] = []
    for path, contract in outputs:
        validation = validate_artifact(path, contract)
        if not validation.valid or not validation.sha256:
            raise RuntimeError(
                f"Revision step {step_id!r} has an invalid output "
                f"{path.name}: {'; '.join(validation.errors)}"
            )
        output_records.append(
            {
                "path": repo_relative(repo_root, path),
                "sha256": validation.sha256,
                "size_bytes": validation.size_bytes,
                "contract": _contract_payload(contract),
            }
        )

    payload = load_revision_state(state_path)
    payload["schema_version"] = SCHEMA_VERSION
    payload.setdefault("created_at", _now())
    payload["updated_at"] = _now()
    payload.setdefault("steps", {})[step_id] = {
        "status": "complete",
        "completed_at": _now(),
        "dependencies": fingerprint,
        "outputs": output_records,
        "metadata": dict(metadata or {}),
    }
    _atomic_write_json(state_path, payload)
    return payload["steps"][step_id]


def assert_revision_step_outputs_current(
    *,
    state_path: Path,
    repo_root: Path,
    required_steps: Iterable[str],
) -> dict[str, Any]:
    """Verify released step outputs without re-evaluating historical inputs.

    A terminal revision must remain usable after the Council's own code and
    charters evolve, so historical verification cannot require today's input
    fingerprint to equal the one captured at release. It still requires every
    release-critical receipt and every output byte named by those receipts.
    """

    if not state_path.is_file() or state_path.is_symlink():
        raise RuntimeError("Revision execution state is missing or unsafe.")
    payload = load_revision_state(state_path)
    steps = payload.get("steps")
    if not isinstance(steps, dict):
        raise RuntimeError("Revision execution state has no step receipts.")
    required = set(required_steps)
    missing = sorted(required - set(steps))
    if missing:
        raise RuntimeError(
            "Revision execution state is missing required step receipts: "
            + ", ".join(missing)
        )

    failures: list[str] = []
    root = repo_root.resolve()
    for step_id in sorted(required):
        record = steps.get(step_id)
        if not isinstance(record, dict) or record.get("status") != "complete":
            failures.append(f"{step_id}: receipt is not complete")
            continue
        recorded_dependencies = record.get("dependencies")
        if not isinstance(recorded_dependencies, dict):
            failures.append(f"{step_id}: dependency receipt is malformed")
            continue
        dependency_hash = recorded_dependencies.get("sha256")
        unsigned_dependencies = {
            key: value
            for key, value in recorded_dependencies.items()
            if key != "sha256"
        }
        canonical_dependency_hash = hashlib.sha256(
            json.dumps(
                unsigned_dependencies,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode("utf-8")
        ).hexdigest()
        if (
            recorded_dependencies.get("schema_version") != SCHEMA_VERSION
            or recorded_dependencies.get("complete") is not True
            or not isinstance(recorded_dependencies.get("inputs"), list)
            or not isinstance(recorded_dependencies.get("values"), dict)
            or not isinstance(dependency_hash, str)
            or len(dependency_hash) != 64
            or dependency_hash != canonical_dependency_hash
        ):
            failures.append(f"{step_id}: dependency receipt is malformed")
            continue

        raw_outputs = record.get("outputs")
        if not isinstance(raw_outputs, list) or not raw_outputs:
            failures.append(f"{step_id}: output receipt is missing")
            continue
        seen_outputs: set[str] = set()
        for output in raw_outputs:
            if not isinstance(output, dict):
                failures.append(f"{step_id}: output receipt is malformed")
                continue
            raw_relative = output.get("path")
            if not isinstance(raw_relative, str) or not raw_relative:
                failures.append(f"{step_id}: output path is missing")
                continue
            if raw_relative in seen_outputs:
                failures.append(
                    f"{step_id}: duplicate output receipt {raw_relative}"
                )
                continue
            seen_outputs.add(raw_relative)
            relative = Path(raw_relative)
            if relative.is_absolute() or ".." in relative.parts:
                failures.append(f"{step_id}: output path escapes the repository")
                continue
            unresolved = root / relative
            candidate = unresolved.resolve(strict=False)
            try:
                candidate.relative_to(root)
            except ValueError:
                failures.append(f"{step_id}: output path escapes the repository")
                continue
            if unresolved.is_symlink():
                failures.append(f"{step_id}: output path is a symlink")
                continue
            raw_contract = output.get("contract")
            if not isinstance(raw_contract, dict):
                failures.append(f"{step_id}: output contract is missing")
                continue
            try:
                contract = ArtifactContract(
                    kind=str(raw_contract.get("kind") or "binary"),
                    min_words=int(raw_contract.get("min_words") or 0),
                    min_records=int(raw_contract.get("min_records") or 0),
                    required_keys=tuple(raw_contract.get("required_keys") or ()),
                    required_any=tuple(
                        tuple(group)
                        for group in (raw_contract.get("required_any") or ())
                    ),
                    optional=bool(raw_contract.get("optional", False)),
                )
            except (TypeError, ValueError):
                failures.append(f"{step_id}: output contract is malformed")
                continue
            validation = validate_artifact(candidate, contract)
            if (
                not validation.valid
                or not validation.sha256
                or validation.sha256 != output.get("sha256")
                or validation.size_bytes != output.get("size_bytes")
            ):
                failures.append(
                    f"{step_id}: output {relative.as_posix()} changed"
                )
    if failures:
        raise RuntimeError(
            "Released revision receipt validation failed: "
            + "; ".join(failures)
        )
    return payload


def assert_revision_state_current(
    *,
    state_path: Path,
    repo_root: Path,
    required_steps: Iterable[str],
) -> dict[str, Any]:
    """Revalidate every receipt from live disk immediately before release."""

    if not state_path.is_file() or state_path.is_symlink():
        raise RuntimeError("Revision execution state is missing or unsafe.")
    payload = load_revision_state(state_path)
    steps = payload.get("steps")
    if not isinstance(steps, dict):
        raise RuntimeError("Revision execution state has no step receipts.")
    required = set(required_steps)
    missing = sorted(required - set(steps))
    if missing:
        raise RuntimeError(
            "Revision release is missing required step receipts: "
            + ", ".join(missing)
        )

    failures: list[str] = []
    root = repo_root.resolve()
    for step_id in sorted(required):
        record = steps[step_id]
        if not isinstance(record, dict) or record.get("status") != "complete":
            failures.append(f"{step_id}: receipt is not complete")
            continue
        recorded_dependencies = record.get("dependencies")
        if not isinstance(recorded_dependencies, dict):
            failures.append(f"{step_id}: dependency receipt is missing")
            continue
        raw_inputs = recorded_dependencies.get("inputs")
        values = recorded_dependencies.get("values")
        if not isinstance(raw_inputs, list) or not isinstance(values, dict):
            failures.append(f"{step_id}: dependency receipt is malformed")
            continue
        dependencies: list[RevisionDependency] = []
        malformed_input = False
        for item in raw_inputs:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("declaration"), str)
            ):
                malformed_input = True
                break
            dependencies.append(
                RevisionDependency(
                    item["declaration"],
                    required=bool(item.get("required", True)),
                )
            )
        if malformed_input:
            failures.append(f"{step_id}: dependency declarations are malformed")
            continue
        current = build_revision_dependency_fingerprint(
            repo_root=root,
            dependencies=dependencies,
            values=values,
        )
        if (
            current.get("complete") is not True
            or current.get("sha256")
            != recorded_dependencies.get("sha256")
        ):
            failures.append(
                f"{step_id}: a declared input, model contract, or charter changed"
            )
            continue

        raw_outputs = record.get("outputs")
        if not isinstance(raw_outputs, list) or not raw_outputs:
            failures.append(f"{step_id}: output receipt is missing")
            continue
        for output in raw_outputs:
            if not isinstance(output, dict):
                failures.append(f"{step_id}: output receipt is malformed")
                continue
            relative = Path(str(output.get("path") or ""))
            if relative.is_absolute() or ".." in relative.parts:
                failures.append(f"{step_id}: output path escapes the repository")
                continue
            candidate = (root / relative).resolve(strict=False)
            try:
                candidate.relative_to(root)
            except ValueError:
                failures.append(f"{step_id}: output path escapes the repository")
                continue
            if (root / relative).is_symlink():
                failures.append(f"{step_id}: output path is a symlink")
                continue
            raw_contract = output.get("contract")
            if not isinstance(raw_contract, dict):
                failures.append(f"{step_id}: output contract is missing")
                continue
            contract = ArtifactContract(
                kind=str(raw_contract.get("kind") or "binary"),
                min_words=int(raw_contract.get("min_words") or 0),
                min_records=int(raw_contract.get("min_records") or 0),
                required_keys=tuple(raw_contract.get("required_keys") or ()),
                required_any=tuple(
                    tuple(group)
                    for group in (raw_contract.get("required_any") or ())
                ),
                optional=bool(raw_contract.get("optional", False)),
            )
            validation = validate_artifact(candidate, contract)
            if (
                not validation.valid
                or not validation.sha256
                or validation.sha256 != output.get("sha256")
                or validation.size_bytes != output.get("size_bytes")
            ):
                failures.append(
                    f"{step_id}: output {relative.as_posix()} changed"
                )
    if failures:
        raise RuntimeError(
            "Revision release pre-commit validation failed: "
            + "; ".join(failures)
        )
    return payload
