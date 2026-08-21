"""Safe lifecycle operations for Library entries.

The Council's release and archive receipts are evidence.  Renaming a report by
editing those receipts would destroy that evidence, while deleting only a
Library card would strand the prompt, sources, revisions, and release bundles.
This module keeps display metadata in operator-local sidecars and treats a
report plus all of its revisions as one deletion family.

No public operation accepts a filesystem path.  Every managed path is derived
from a validated ``mode`` and ``slug``, remains under ``repo_root``, and is
moved with ``os.replace`` into an isolated transaction.  A recoverable delete
keeps that transaction in Council Trash; a permanent delete removes the staged
payload only after every owned artifact has moved successfully.  Directory
fingerprinting and moves never follow symlinks.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
import stat
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping


METADATA_SCHEMA_VERSION = "1.0"
OWNERSHIP_SCHEMA_VERSION = "1.0"
BUILTIN_LEGACY_OWNERSHIP_VERSION = "2026-08-21.1"
DELETE_RECEIPT_SCHEMA_VERSION = "1.0"
DELETE_PLAN_TTL_SECONDS = 5 * 60
METADATA_MAX_BYTES = 64 * 1024
TITLE_MAX_CHARS = 200
SUMMARY_MAX_CHARS = 1_000
TAG_MAX_CHARS = 48
TAG_MAX_COUNT = 12

VALID_MODES = frozenset({"report", "revision", "scope", "strengthen"})
TARGET_CATEGORIES = frozenset(
    {
        "distribution_pointer",
        "distribution_file",
        "release_bundle",
        "metadata",
        "ownership_receipt",
        "prompt",
        "source_library",
        "run_archive",
    }
)
MANAGED_TARGET_PREFIXES = (
    ("reports",),
    ("runs",),
    ("prompts", "runs"),
    ("sources", "runs"),
    ("final", "Word"),
    ("final", "PowerPoint"),
    ("final", "PDF"),
    (".council-state", "library", "metadata"),
    (".council-state", "library", "ownership"),
)
SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,191}$")
REVISION_RE = re.compile(r"^(.+)-revised-v([1-9][0-9]*)$")
CLIENT_RE = re.compile(r"^[A-Za-z0-9_-]{16,128}$")
SCOPE_STALE_SUFFIX_RE = re.compile(r"^\d{8}T\d{12}$")

# Human-reviewed one-time migration assertions for the historical exports that
# predate release manifests. These are deliberately exact path + byte bindings,
# not report-number or title patterns. A present file whose bytes drift from
# this table blocks deletion; an already-removed path is simply absent.
BUILTIN_LEGACY_REPORT_OWNERSHIP: Mapping[
    str, tuple[tuple[str, str, int], ...]
] = {
    "infrastructure-vs-intelligence": (
        (
            "final/PDF/AI Report 001 — Infrastructure vs. Operational Intelligence.pdf",
            "c70afb41f8e8dd20098079d87859e2c4221379f0a455efc443877469282574ff",
            581_079,
        ),
    ),
    "mega-terminal-programs-that-underperformed-year-1-3-warning-signs": (
        (
            "final/PDF/AI Report 002 — Mega-Terminal Programs That Underperformed.pdf",
            "eaa3712682b1f3d90a1e70fe3120cd627745ca41cbe1f7c2a4f629fb21a4bb0b",
            466_696,
        ),
    ),
    "sterile-corridor-resilience": (
        (
            "final/PDF/AI Report 003 — Sterile Circulation Best Practices .pdf",
            "8504cbc92c98b3486882adf7822d9ffd27c8ff750f52a3d882cb16ee48231a85",
            504_129,
        ),
    ),
    "saarinen-iad-redesign": (
        (
            "final/PDF/AI Report 004 - If Eero Saarinen Were Designing Dulles Today.pdf",
            "7ff3923570a732de2156201c3faef3fc6d1363d95d01ffed1b480cac84c9b7c4",
            522_141,
        ),
    ),
    "baggage-handling-best-practices": (
        (
            "final/PDF/AI Report 005 — Baggage Handling Best Practices.pdf",
            "c843dd4494ae71b53b53f01ad989fe595125d574f0739992fd13d4cff9462a5b",
            473_448,
        ),
    ),
    "indoor-signage-best-practices": (
        (
            "final/PDF/AI Report 006 — Indoor Signage Best Practices.pdf",
            "aec45c0bb08474be2d0a1f783bc85f12fe3f836a882846085408178a2f539d3c",
            502_030,
        ),
    ),
    "iot-design-best-practices": (
        (
            "final/PDF/AI Report 007 — IoT Design Best Practices.pdf",
            "80bba9ab185f075c1f4d874bfbe5cddcf0c2f98d70068b1d090de126b1f7bdfd",
            485_043,
        ),
    ),
    "from-compliance-to-capability-a-strategic-review-of-the-mwaa-contracting-manual": (
        (
            "final/PDF/AI Report 008 — From Compliance to Capability.pdf",
            "b1b4f7b5944b7509f61d199edc173d5576fa33af3e86d06af4332183b755ae9e",
            503_282,
        ),
        (
            "final/PowerPoint/AI Report 008 — From Compliance to Capability.pptx",
            "efcab70a7b0009f82beef1ff6c5ade55ba87417b7c92a5a51b564fe814c0e457",
            64_486,
        ),
    ),
}

PROTECTED_LIBRARY_PATHS = frozenset(
    {"final/PowerPoint/AI Research Council — How It Works.pptx"}
)


class LibraryLifecycleError(RuntimeError):
    """Base error with a stable API-facing code and suggested HTTP status."""

    code = "library_lifecycle_error"
    http_status = 400


class InvalidLibraryIdentity(LibraryLifecycleError):
    code = "invalid_library_identity"


class LibraryItemNotFound(LibraryLifecycleError):
    code = "library_item_not_found"
    http_status = 404


class MetadataValidationError(LibraryLifecycleError):
    code = "invalid_library_metadata"


class LifecycleSafetyError(LibraryLifecycleError):
    code = "library_safety_error"
    http_status = 409


class MutationBlocked(LibraryLifecycleError):
    code = "library_mutation_blocked"
    http_status = 409


class DeletePlanNotFound(LibraryLifecycleError):
    code = "delete_plan_not_found"
    http_status = 404


class DeletePlanExpired(LibraryLifecycleError):
    code = "delete_plan_expired"
    http_status = 409


class DeletePlanForbidden(LibraryLifecycleError):
    code = "delete_plan_forbidden"
    http_status = 403


class DeletePlanStale(LibraryLifecycleError):
    code = "delete_plan_stale"
    http_status = 409


class ConfirmationMismatch(LibraryLifecycleError):
    code = "delete_confirmation_mismatch"


class LifecycleTransactionError(LibraryLifecycleError):
    code = "library_transaction_failed"
    http_status = 500


class RestoreConflict(LibraryLifecycleError):
    code = "library_restore_conflict"
    http_status = 409


@dataclass(frozen=True)
class PathSnapshot:
    kind: str
    digest: str
    file_count: int
    total_bytes: int
    symlink_count: int

    def as_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "digest": self.digest,
            "file_count": self.file_count,
            "total_bytes": self.total_bytes,
            "symlink_count": self.symlink_count,
        }


@dataclass(frozen=True)
class LifecycleTarget:
    relative_path: str
    category: str
    snapshot: PathSnapshot

    def as_dict(self) -> dict[str, object]:
        return {
            "path": self.relative_path,
            "category": self.category,
            **self.snapshot.as_dict(),
        }


@dataclass(frozen=True)
class ArtifactInventory:
    requested_mode: str
    requested_slug: str
    family_mode: str
    family_slug: str
    public_slug: str
    revision_slugs: tuple[str, ...]
    targets: tuple[LifecycleTarget, ...]

    @property
    def file_count(self) -> int:
        return sum(item.snapshot.file_count for item in self.targets)

    @property
    def total_bytes(self) -> int:
        return sum(item.snapshot.total_bytes for item in self.targets)

    @property
    def symlink_count(self) -> int:
        return sum(item.snapshot.symlink_count for item in self.targets)

    @property
    def digest(self) -> str:
        return _json_digest(
            {
                "requested_mode": self.requested_mode,
                "requested_slug": self.requested_slug,
                "family_mode": self.family_mode,
                "family_slug": self.family_slug,
                "public_slug": self.public_slug,
                "revision_slugs": list(self.revision_slugs),
                "targets": [item.as_dict() for item in self.targets],
            }
        )

    def summary(self) -> dict[str, object]:
        groups: dict[str, dict[str, int]] = {}
        for target in self.targets:
            group = groups.setdefault(
                target.category,
                {"targets": 0, "files": 0, "bytes": 0, "symlinks": 0},
            )
            group["targets"] += 1
            group["files"] += target.snapshot.file_count
            group["bytes"] += target.snapshot.total_bytes
            group["symlinks"] += target.snapshot.symlink_count
        return {
            "requested_mode": self.requested_mode,
            "requested_slug": self.requested_slug,
            "family_mode": self.family_mode,
            "family_slug": self.family_slug,
            "public_slug": self.public_slug,
            "revision_slugs": list(self.revision_slugs),
            "revision_count": len(self.revision_slugs),
            "target_count": len(self.targets),
            "file_count": self.file_count,
            "total_bytes": self.total_bytes,
            "symlink_count": self.symlink_count,
            "groups": groups,
            "inventory_digest": self.digest,
        }


@dataclass(frozen=True)
class DeletePlan:
    plan_id: str
    client_id: str
    created_at: float
    expires_at: float
    confirmation: str
    permanent: bool
    inventory: ArtifactInventory

    def as_dict(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "created_at": _iso_timestamp(self.created_at),
            "expires_at": _iso_timestamp(self.expires_at),
            "confirmation": self.confirmation,
            "permanent": self.permanent,
            "recoverable": not self.permanent,
            **self.inventory.summary(),
            "targets": [target.as_dict() for target in self.inventory.targets],
        }


@dataclass(frozen=True)
class DeletionReceipt:
    receipt_id: str
    deleted_at: str
    trash_path: str
    inventory: ArtifactInventory

    def as_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "deleted_at": self.deleted_at,
            "trash_path": self.trash_path,
            "recoverable": True,
            **self.inventory.summary(),
            "targets": [target.as_dict() for target in self.inventory.targets],
        }


@dataclass(frozen=True)
class PermanentDeletionReceipt:
    receipt_id: str
    deleted_at: str
    cleanup_pending: bool
    inventory: ArtifactInventory

    def as_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "deleted_at": self.deleted_at,
            "recoverable": False,
            "permanent": True,
            "cleanup_pending": self.cleanup_pending,
            "reclaimed_bytes": self.inventory.total_bytes,
            **self.inventory.summary(),
            "targets": [target.as_dict() for target in self.inventory.targets],
        }


@dataclass(frozen=True)
class RestoreReceipt:
    receipt_id: str
    restored_at: str
    target_count: int

    def as_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "restored_at": self.restored_at,
            "target_count": self.target_count,
        }


MutationGuard = Callable[[str, str], str | None]


def _iso_timestamp(epoch: float | None = None) -> str:
    value = time.time() if epoch is None else epoch
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat(
        timespec="seconds"
    )


def _json_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _json_digest(payload: object) -> str:
    return hashlib.sha256(_json_bytes(payload)).hexdigest()


def _lexists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def _validate_identity(mode: object, slug: object) -> tuple[str, str]:
    if not isinstance(mode, str) or mode not in VALID_MODES:
        raise InvalidLibraryIdentity(f"Unsupported Library mode: {mode!r}")
    if not isinstance(slug, str) or SLUG_RE.fullmatch(slug) is None:
        raise InvalidLibraryIdentity(f"Unsafe Library slug: {slug!r}")
    if mode == "revision" and REVISION_RE.fullmatch(slug) is None:
        raise InvalidLibraryIdentity(
            "Revision slugs must end with '-revised-vN'."
        )
    if mode == "strengthen" and not slug.startswith("argument-"):
        raise InvalidLibraryIdentity(
            "Strengthened-argument Library slugs must start with 'argument-'."
        )
    return mode, slug


def _validate_client_id(client_id: object) -> str:
    if not isinstance(client_id, str) or CLIENT_RE.fullmatch(client_id) is None:
        raise DeletePlanForbidden("Invalid Library mutation client ID.")
    return client_id


def _plain_text(value: object, *, field: str, maximum: int, empty: bool) -> str:
    if not isinstance(value, str):
        raise MetadataValidationError(f"{field} must be text.")
    normalized = value.strip()
    if not empty and not normalized:
        raise MetadataValidationError(f"{field} may not be empty.")
    if len(normalized) > maximum:
        raise MetadataValidationError(
            f"{field} may not exceed {maximum:,} characters."
        )
    if any(ord(character) < 32 or ord(character) == 127 for character in normalized):
        raise MetadataValidationError(f"{field} contains a control character.")
    return normalized


def _validated_tags(value: object) -> list[str]:
    if not isinstance(value, list) or len(value) > TAG_MAX_COUNT:
        raise MetadataValidationError(
            f"tags must be a list of no more than {TAG_MAX_COUNT} values."
        )
    tags: list[str] = []
    folded: set[str] = set()
    for raw in value:
        tag = _plain_text(
            raw, field="tag", maximum=TAG_MAX_CHARS, empty=False
        )
        identity = tag.casefold()
        if identity in folded:
            continue
        folded.add(identity)
        tags.append(tag)
    return tags


def _sha256_file_stable(path: Path) -> tuple[str, int]:
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise LifecycleSafetyError(f"Expected a regular file: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    after = path.lstat()
    identity_before = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    identity_after = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if identity_before != identity_after or not stat.S_ISREG(after.st_mode):
        raise DeletePlanStale(f"File changed while it was inventoried: {path}")
    return digest.hexdigest(), after.st_size


def _snapshot_path(path: Path) -> PathSnapshot:
    """Fingerprint one path without following any symlink."""

    try:
        root_stat = path.lstat()
    except OSError as exc:
        raise DeletePlanStale(f"Library artifact disappeared: {path}") from exc

    if stat.S_ISLNK(root_stat.st_mode):
        target = os.readlink(path)
        digest = _json_digest({"type": "symlink", "target": target})
        return PathSnapshot("symlink", digest, 0, 0, 1)
    if stat.S_ISREG(root_stat.st_mode):
        digest, size = _sha256_file_stable(path)
        return PathSnapshot("file", digest, 1, size, 0)
    if not stat.S_ISDIR(root_stat.st_mode):
        raise LifecycleSafetyError(
            f"Library artifacts must be files, directories, or symlinks: {path}"
        )

    records: list[dict[str, object]] = [{"path": "", "type": "directory"}]
    file_count = 0
    total_bytes = 0
    symlink_count = 0

    def walk(directory: Path, prefix: Path) -> None:
        nonlocal file_count, total_bytes, symlink_count
        try:
            with os.scandir(directory) as iterator:
                entries = sorted(list(iterator), key=lambda item: item.name)
        except OSError as exc:
            raise LifecycleSafetyError(
                f"Could not inventory Library directory: {directory}"
            ) from exc
        names_before = [entry.name for entry in entries]
        for entry in entries:
            child = directory / entry.name
            relative = (prefix / entry.name).as_posix()
            try:
                child_stat = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise DeletePlanStale(
                    f"Library artifact changed during inventory: {child}"
                ) from exc
            if stat.S_ISLNK(child_stat.st_mode):
                link_target = os.readlink(child)
                records.append(
                    {"path": relative, "type": "symlink", "target": link_target}
                )
                symlink_count += 1
            elif stat.S_ISDIR(child_stat.st_mode):
                records.append({"path": relative, "type": "directory"})
                walk(child, prefix / entry.name)
            elif stat.S_ISREG(child_stat.st_mode):
                digest, size = _sha256_file_stable(child)
                records.append(
                    {
                        "path": relative,
                        "type": "file",
                        "sha256": digest,
                        "size_bytes": size,
                    }
                )
                file_count += 1
                total_bytes += size
            else:
                raise LifecycleSafetyError(
                    f"Unsupported special file inside Library artifact: {child}"
                )
        try:
            with os.scandir(directory) as iterator:
                names_after = sorted(item.name for item in iterator)
        except OSError as exc:
            raise DeletePlanStale(
                f"Library directory changed during inventory: {directory}"
            ) from exc
        if names_before != names_after:
            raise DeletePlanStale(
                f"Library directory changed during inventory: {directory}"
            )

    walk(path, Path())
    return PathSnapshot(
        "directory",
        _json_digest(records),
        file_count,
        total_bytes,
        symlink_count,
    )


def _target_priority(target: LifecycleTarget) -> tuple[int, str]:
    priorities = {
        "distribution_pointer": 0,
        "distribution_file": 1,
        "release_bundle": 2,
        "metadata": 3,
        "ownership_receipt": 4,
        "prompt": 5,
        "source_library": 6,
        "run_archive": 7,
    }
    return priorities.get(target.category, 50), target.relative_path


class LibraryLifecycle:
    """Repository-scoped metadata, delete-plan, trash, and restore service."""

    def __init__(
        self,
        repo_root: Path,
        *,
        plan_ttl_seconds: int = DELETE_PLAN_TTL_SECONDS,
        clock: Callable[[], float] = time.time,
    ) -> None:
        root = Path(repo_root).resolve()
        if not root.is_dir():
            raise ValueError(f"Repository root is unavailable: {root}")
        self.repo_root = root
        self.plan_ttl_seconds = int(plan_ttl_seconds)
        if self.plan_ttl_seconds <= 0:
            raise ValueError("Delete-plan TTL must be positive.")
        self._clock = clock
        self._plans: dict[str, DeletePlan] = {}
        self._lock = threading.RLock()

    @property
    def state_dir(self) -> Path:
        return self.repo_root / ".council-state"

    @property
    def trash_root(self) -> Path:
        return self.state_dir / "trash" / "library"

    @property
    def purge_journal_root(self) -> Path:
        return self.state_dir / "trash" / "library-purge-journals"

    def _assert_managed_roots(self) -> None:
        """Reject a symlink in any root that could redirect a managed target."""

        self._assert_state_roots()
        managed = (
            self.repo_root / "reports",
            self.repo_root / "runs",
            self.repo_root / "prompts",
            self.repo_root / "prompts" / "runs",
            self.repo_root / "sources",
            self.repo_root / "sources" / "runs",
            self.repo_root / "final",
            self.repo_root / "final" / "Word",
            self.repo_root / "final" / "PowerPoint",
            self.repo_root / "final" / "PDF",
        )
        for path in managed:
            if path.is_symlink():
                raise LifecycleSafetyError(
                    f"Managed Library root may not be a symlink: {path}"
                )
            if path.exists():
                try:
                    path.resolve().relative_to(self.repo_root)
                except ValueError as exc:
                    raise LifecycleSafetyError(
                        f"Managed Library root escapes the repository: {path}"
                    ) from exc

    def _assert_state_roots(self) -> None:
        """Validate only operator-state roots used by metadata reads/writes."""

        paths = [
            self.state_dir,
            self.state_dir / "library",
            self.state_dir / "library" / "metadata",
            self.state_dir / "library" / "ownership",
            self.state_dir / "library" / "ownership" / "report",
            self.state_dir / "trash",
            self.state_dir / "trash" / "library",
            self.state_dir / "trash" / "library-purge-journals",
        ]
        paths.extend(
            self.state_dir / "library" / "metadata" / mode
            for mode in sorted(VALID_MODES)
        )
        for path in paths:
            if path.is_symlink():
                raise LifecycleSafetyError(
                    f"Library state root may not be a symlink: {path}"
                )
            if path.exists():
                try:
                    path.resolve().relative_to(self.repo_root)
                except ValueError as exc:
                    raise LifecycleSafetyError(
                        f"Library state root escapes the repository: {path}"
                    ) from exc

    def _ensure_directory(self, path: Path) -> None:
        try:
            relative = path.relative_to(self.repo_root)
        except ValueError as exc:
            raise LifecycleSafetyError(
                f"Library state path escapes the repository: {path}"
            ) from exc
        cursor = self.repo_root
        for component in relative.parts:
            cursor = cursor / component
            if cursor.is_symlink():
                raise LifecycleSafetyError(
                    f"Library state path may not traverse a symlink: {cursor}"
                )
            if cursor.exists() and not cursor.is_dir():
                raise LifecycleSafetyError(
                    f"Library state parent is not a directory: {cursor}"
                )
            cursor.mkdir(exist_ok=True)

    def _relative(self, path: Path) -> str:
        try:
            relative = path.relative_to(self.repo_root)
        except ValueError as exc:
            raise LifecycleSafetyError(
                f"Library target escapes the repository: {path}"
            ) from exc
        if not relative.parts or ".." in relative.parts:
            raise LifecycleSafetyError(f"Unsafe Library target: {path}")
        return relative.as_posix()

    def _managed_target_relative(self, value: object) -> str:
        """Return one canonical repo-relative path in a Library-owned tree."""

        if not isinstance(value, str) or not value:
            raise LifecycleSafetyError("Library target path is invalid.")
        candidate = self.repo_root / Path(value)
        relative = self._relative(candidate)
        if relative != value:
            raise LifecycleSafetyError(
                f"Library target path is not canonical: {value!r}"
            )
        parts = Path(relative).parts
        if not any(
            len(parts) > len(prefix) and parts[: len(prefix)] == prefix
            for prefix in MANAGED_TARGET_PREFIXES
        ):
            raise LifecycleSafetyError(
                f"Library target is outside managed artifact trees: {relative}"
            )
        return relative

    def _assert_payload_parentage(self, path: Path, payload_root: Path) -> None:
        """Reject a symlink between a Trash payload root and a target leaf.

        The leaf itself may be a symlink: deleting and restoring that link,
        without following its external target, is supported deliberately.
        """

        if payload_root.is_symlink() or not payload_root.is_dir():
            raise LifecycleSafetyError("Library trash payload is unavailable.")
        try:
            relative = path.relative_to(payload_root)
        except ValueError as exc:
            raise LifecycleSafetyError(
                "Library trash target escapes its payload."
            ) from exc
        if not relative.parts or ".." in relative.parts:
            raise LifecycleSafetyError("Library trash target is unsafe.")
        cursor = payload_root
        for component in relative.parts[:-1]:
            cursor = cursor / component
            if cursor.is_symlink():
                raise LifecycleSafetyError(
                    f"Library trash target traverses a symlink: {cursor}"
                )
            if not cursor.exists():
                # An untouched target in an interrupted transaction has no
                # payload parents yet. Its original path will decide whether
                # recovery can safely skip it.
                return
            if not cursor.is_dir():
                raise LifecycleSafetyError(
                    f"Library trash target parent is unavailable: {cursor}"
                )

    def _metadata_path(self, mode: str, slug: str) -> Path:
        _validate_identity(mode, slug)
        return self.state_dir / "library" / "metadata" / mode / f"{slug}.json"

    def _ownership_path(self, slug: str) -> Path:
        """Return the explicit legacy-export ownership receipt for a report.

        Ownership receipts are deliberately separate from editable display
        metadata. They bind an otherwise renamed file to one report by its
        canonical repo-relative path, byte length, and SHA-256 digest.
        """

        _validate_identity("report", slug)
        return (
            self.state_dir
            / "library"
            / "ownership"
            / "report"
            / f"{slug}.json"
        )

    def read_metadata(self, mode: str, slug: str) -> dict[str, object] | None:
        mode, slug = _validate_identity(mode, slug)
        self._assert_state_roots()
        path = self._metadata_path(mode, slug)
        if not _lexists(path):
            return None
        if path.is_symlink() or not path.is_file():
            raise LifecycleSafetyError(
                f"Library metadata is not a regular file: {path}"
            )
        if path.stat().st_size > METADATA_MAX_BYTES:
            raise LifecycleSafetyError("Library metadata exceeds its size limit.")
        try:
            payload = json.loads(path.read_text(encoding="utf-8", errors="strict"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise LifecycleSafetyError("Library metadata is unreadable.") from exc
        if (
            not isinstance(payload, dict)
            or payload.get("schema_version") != METADATA_SCHEMA_VERSION
            or payload.get("mode") != mode
            or payload.get("slug") != slug
        ):
            raise LifecycleSafetyError("Library metadata identity is invalid.")
        # Revalidate stored display values before returning them to a renderer.
        result: dict[str, object] = {
            "schema_version": METADATA_SCHEMA_VERSION,
            "mode": mode,
            "slug": slug,
            "updated_at": str(payload.get("updated_at") or ""),
        }
        if "title" in payload:
            result["title"] = _plain_text(
                payload["title"],
                field="title",
                maximum=TITLE_MAX_CHARS,
                empty=False,
            )
        if "summary" in payload:
            result["summary"] = _plain_text(
                payload["summary"],
                field="summary",
                maximum=SUMMARY_MAX_CHARS,
                empty=True,
            )
        if "tags" in payload:
            result["tags"] = _validated_tags(payload["tags"])
        if not any(field in result for field in {"title", "summary", "tags"}):
            raise LifecycleSafetyError("Library metadata has no display fields.")
        return result

    def update_metadata(
        self,
        mode: str,
        slug: str,
        changes: Mapping[str, object],
    ) -> dict[str, object]:
        """Atomically patch display-only metadata without touching report bytes."""

        mode, slug = _validate_identity(mode, slug)
        if not isinstance(changes, Mapping):
            raise MetadataValidationError("Metadata changes must be an object.")
        allowed = {"title", "summary", "tags"}
        unknown = set(changes) - allowed
        if unknown:
            raise MetadataValidationError(
                "Unknown metadata field(s): " + ", ".join(sorted(unknown))
            )
        if not changes:
            raise MetadataValidationError("No metadata changes were supplied.")
        with self._lock:
            self._assert_state_roots()
            existing = self.read_metadata(mode, slug) or {}
            payload: dict[str, object] = {
                "schema_version": METADATA_SCHEMA_VERSION,
                "mode": mode,
                "slug": slug,
                "updated_at": _iso_timestamp(self._clock()),
            }
            for field in allowed:
                if field in changes:
                    if field == "title":
                        payload[field] = _plain_text(
                            changes[field],
                            field="title",
                            maximum=TITLE_MAX_CHARS,
                            empty=False,
                        )
                    elif field == "summary":
                        payload[field] = _plain_text(
                            changes[field],
                            field="summary",
                            maximum=SUMMARY_MAX_CHARS,
                            empty=True,
                        )
                    else:
                        payload[field] = _validated_tags(changes[field])
                elif field in existing:
                    payload[field] = existing[field]
            path = self._metadata_path(mode, slug)
            self._ensure_directory(path.parent)
            if path.is_symlink():
                raise LifecycleSafetyError("Library metadata may not be a symlink.")
            self._atomic_json(path, payload)
            return payload

    def _atomic_json(self, path: Path, payload: object) -> None:
        self._ensure_directory(path.parent)
        temporary = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
        try:
            with temporary.open("xb") as handle:
                handle.write(
                    json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
                    + b"\n"
                )
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if _lexists(temporary):
                temporary.unlink()

    def _add_target(
        self,
        targets: dict[str, tuple[Path, str]],
        path: Path,
        category: str,
    ) -> None:
        if not _lexists(path):
            return
        relative = self._relative(path)
        self._managed_target_relative(relative)
        prior = targets.get(relative)
        if prior is not None and prior[1] != category:
            raise LifecycleSafetyError(
                f"Library target has conflicting categories: {relative}"
            )
        targets[relative] = (path, category)

    def _safe_json_file(self, path: Path) -> dict[str, Any] | None:
        if path.is_symlink() or not path.is_file():
            return None
        try:
            if path.stat().st_size > 2 * 1024 * 1024:
                return None
            payload = json.loads(path.read_text(encoding="utf-8", errors="strict"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    def _direct_children(self, root: Path) -> list[Path]:
        if not _lexists(root):
            return []
        if root.is_symlink() or not root.is_dir():
            raise LifecycleSafetyError(
                f"Managed Library directory is not a regular directory: {root}"
            )
        try:
            return sorted(root.iterdir(), key=lambda item: item.name)
        except OSError as exc:
            raise LifecycleSafetyError(
                f"Could not inspect managed Library directory: {root}"
            ) from exc

    def _legacy_export_relative(self, value: object) -> str:
        """Validate one explicit ownership path in the legacy final/ tree."""

        relative = self._managed_target_relative(value)
        parts = Path(relative).parts
        allowed = {
            "Word": ".docx",
            "PowerPoint": ".pptx",
            "PDF": ".pdf",
        }
        if (
            len(parts) != 3
            or parts[0] != "final"
            or parts[1] not in allowed
            or Path(parts[2]).suffix.casefold() != allowed[parts[1]]
        ):
            raise LifecycleSafetyError(
                "Legacy ownership receipts may name only a direct Word, "
                "PowerPoint, or PDF export in final/."
            )
        if relative in PROTECTED_LIBRARY_PATHS:
            raise LifecycleSafetyError(
                f"Non-report Council material may not belong to a report: {relative}"
            )
        return relative

    def _builtin_report_ownership_indexes(
        self,
    ) -> dict[str, tuple[tuple[str, str, int], ...]]:
        """Validate the versioned, human-reviewed legacy migration table."""

        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}\.[1-9][0-9]*", BUILTIN_LEGACY_OWNERSHIP_VERSION):
            raise LifecycleSafetyError("Built-in legacy ownership version is invalid.")
        indexes: dict[str, tuple[tuple[str, str, int], ...]] = {}
        claims: dict[str, str] = {}
        for slug, raw_entries in BUILTIN_LEGACY_REPORT_OWNERSHIP.items():
            if not isinstance(slug, str) or SLUG_RE.fullmatch(slug) is None:
                raise LifecycleSafetyError(
                    "Built-in legacy ownership has an unsafe report slug."
                )
            if not isinstance(raw_entries, (list, tuple)):
                raise LifecycleSafetyError(
                    f"Built-in legacy ownership is invalid for: {slug}"
                )
            entries: list[tuple[str, str, int]] = []
            for raw in raw_entries:
                if not isinstance(raw, (list, tuple)) or len(raw) != 3:
                    raise LifecycleSafetyError(
                        f"Built-in legacy ownership has an invalid artifact: {slug}"
                    )
                relative = self._legacy_export_relative(raw[0])
                digest = raw[1]
                size = raw[2]
                if (
                    not isinstance(digest, str)
                    or re.fullmatch(r"[0-9a-f]{64}", digest) is None
                    or not isinstance(size, int)
                    or isinstance(size, bool)
                    or size < 0
                ):
                    raise LifecycleSafetyError(
                        f"Built-in legacy ownership has an invalid byte binding: {slug}"
                    )
                prior = claims.get(relative)
                if prior is not None and prior != slug:
                    raise LifecycleSafetyError(
                        "Built-in legacy export has conflicting owners: "
                        f"{relative} ({prior}, {slug})."
                    )
                claims[relative] = slug
                entries.append((relative, digest, size))
            indexes[slug] = tuple(entries)
        return indexes

    def _report_ownership_indexes(
        self,
    ) -> dict[str, tuple[tuple[str, str, int], ...]]:
        """Load the exact, hash-bound ownership index for legacy exports.

        The index is an escape hatch for old numbered or human-renamed files
        whose original release bytes no longer exist. Invalid or conflicting
        receipts block mutation instead of widening a filename match.
        """

        root = self.state_dir / "library" / "ownership" / "report"
        indexes: dict[str, tuple[tuple[str, str, int], ...]] = {}
        claims = {
            relative: slug
            for slug, entries in self._builtin_report_ownership_indexes().items()
            for relative, _digest, _size in entries
        }
        for path in self._direct_children(root):
            if path.suffix != ".json":
                continue
            slug = path.stem
            if SLUG_RE.fullmatch(slug) is None:
                raise LifecycleSafetyError(
                    f"Legacy ownership receipt has an unsafe name: {path.name}"
                )
            payload = self._safe_json_file(path)
            if (
                payload is None
                or payload.get("schema_version") != OWNERSHIP_SCHEMA_VERSION
                or payload.get("mode") != "report"
                or payload.get("slug") != slug
                or not isinstance(payload.get("artifacts"), list)
            ):
                raise LifecycleSafetyError(
                    f"Legacy ownership receipt is invalid: {path.name}"
                )
            entries: list[tuple[str, str, int]] = []
            for raw in payload["artifacts"]:
                if not isinstance(raw, dict):
                    raise LifecycleSafetyError(
                        f"Legacy ownership receipt has an invalid artifact: {path.name}"
                    )
                relative = self._legacy_export_relative(raw.get("path"))
                digest = raw.get("sha256")
                size = raw.get("size_bytes")
                if (
                    not isinstance(digest, str)
                    or re.fullmatch(r"[0-9a-f]{64}", digest) is None
                    or not isinstance(size, int)
                    or isinstance(size, bool)
                    or size < 0
                ):
                    raise LifecycleSafetyError(
                        f"Legacy ownership receipt has an invalid byte binding: {path.name}"
                    )
                prior = claims.get(relative)
                if prior is not None and prior != slug:
                    raise LifecycleSafetyError(
                        "Legacy export is claimed by more than one report: "
                        f"{relative} ({prior}, {slug})."
                    )
                claims[relative] = slug
                entries.append((relative, digest, size))
            indexes[slug] = tuple(entries)
        return indexes

    def _add_builtin_legacy_exports(
        self,
        targets: dict[str, tuple[Path, str]],
        base_slug: str,
    ) -> None:
        """Add exact historical exports asserted by the built-in migration."""

        entries = self._builtin_report_ownership_indexes().get(base_slug, ())
        for relative, expected_digest, expected_size in entries:
            path = self.repo_root / Path(relative)
            if not _lexists(path):
                continue
            if path.is_symlink() or not path.is_file():
                raise LifecycleSafetyError(
                    f"Built-in legacy export is not a regular file: {relative}"
                )
            digest, size = _sha256_file_stable(path)
            if digest != expected_digest or size != expected_size:
                raise LifecycleSafetyError(
                    "Built-in legacy export no longer matches migration version "
                    f"{BUILTIN_LEGACY_OWNERSHIP_VERSION}: {relative}"
                )
            self._add_target(targets, path, "distribution_file")

    def _add_explicit_legacy_exports(
        self,
        targets: dict[str, tuple[Path, str]],
        base_slug: str,
    ) -> None:
        indexes = self._report_ownership_indexes()
        receipt_path = self._ownership_path(base_slug)
        if base_slug not in indexes:
            return
        for relative, expected_digest, expected_size in indexes[base_slug]:
            path = self.repo_root / Path(relative)
            if not _lexists(path):
                # A manually removed legacy export does not make its ownership
                # receipt dangerous. The receipt itself is still cleaned up.
                continue
            if path.is_symlink() or not path.is_file():
                raise LifecycleSafetyError(
                    f"Owned legacy export is not a regular file: {relative}"
                )
            digest, size = _sha256_file_stable(path)
            if digest != expected_digest or size != expected_size:
                raise LifecycleSafetyError(
                    "Owned legacy export no longer matches its receipt: "
                    f"{relative}"
                )
            self._add_target(targets, path, "distribution_file")
        self._add_target(targets, receipt_path, "ownership_receipt")

    def _iter_export_files(self, root: Path) -> list[Path]:
        """Return Office/PDF files below a trusted root without following links."""

        if root.is_symlink() or not root.is_dir():
            return []
        found: list[Path] = []
        stack = [root]
        while stack:
            directory = stack.pop()
            try:
                with os.scandir(directory) as iterator:
                    entries = sorted(list(iterator), key=lambda item: item.name)
            except OSError as exc:
                raise LifecycleSafetyError(
                    f"Could not inspect verified release artifacts: {directory}"
                ) from exc
            for entry in entries:
                path = directory / entry.name
                try:
                    info = entry.stat(follow_symlinks=False)
                except OSError as exc:
                    raise DeletePlanStale(
                        f"Verified release artifact changed during inventory: {path}"
                    ) from exc
                if stat.S_ISLNK(info.st_mode):
                    continue
                if stat.S_ISDIR(info.st_mode):
                    stack.append(path)
                elif stat.S_ISREG(info.st_mode) and path.suffix.casefold() in {
                    ".docx",
                    ".pptx",
                    ".pdf",
                }:
                    found.append(path)
        return found

    def _add_verified_legacy_exports(
        self,
        targets: dict[str, tuple[Path, str]],
    ) -> None:
        """Migrate renamed final/ exports by exact equality to retained bytes.

        A filename resemblance is never evidence. A legacy final/ file is
        included only when its extension and SHA-256 digest exactly match a
        report artifact retained in this family's selected archive, immutable
        release bundle, or current reports/ distribution file.
        """

        trusted_roots: list[Path] = []
        trusted_files: list[Path] = []
        for path, category in targets.values():
            if category == "run_archive" and not path.is_symlink() and path.is_dir():
                trusted_roots.extend(
                    (
                        path / "stage4",
                        path / "release",
                        path / "outputs" / "release",
                    )
                )
            elif category == "release_bundle":
                trusted_roots.append(path)
            elif (
                category == "distribution_file"
                and path.parent == self.repo_root / "reports"
                and path.suffix.casefold() in {".docx", ".pptx", ".pdf"}
                and not path.is_symlink()
                and path.is_file()
            ):
                trusted_files.append(path)

        for root in trusted_roots:
            trusted_files.extend(self._iter_export_files(root))
        trusted_hashes: dict[str, set[str]] = {
            ".docx": set(),
            ".pptx": set(),
            ".pdf": set(),
        }
        for path in trusted_files:
            digest, _size = _sha256_file_stable(path)
            trusted_hashes[path.suffix.casefold()].add(digest)

        final_roots = (
            self.repo_root / "final" / "Word",
            self.repo_root / "final" / "PowerPoint",
            self.repo_root / "final" / "PDF",
        )
        for root in final_roots:
            for candidate in self._direct_children(root):
                suffix = candidate.suffix.casefold()
                if suffix not in trusted_hashes or candidate.is_symlink():
                    continue
                if not candidate.is_file():
                    continue
                relative = self._relative(candidate)
                if relative in targets:
                    continue
                if relative in PROTECTED_LIBRARY_PATHS:
                    continue
                digest, _size = _sha256_file_stable(candidate)
                if digest in trusted_hashes[suffix]:
                    self._add_target(targets, candidate, "distribution_file")

    def _mode_has_source_claim(self, mode: str, source_slug: str) -> bool:
        """Detect mode-specific artifacts without consulting the shared source."""

        reports = self.repo_root / "reports"
        metadata = self.state_dir / "library" / "metadata"
        if mode == "report":
            markers = (
                self.repo_root / "prompts" / "runs" / f"{source_slug}.md",
                reports / f"{source_slug}.docx",
                reports / f"{source_slug}-executive-summary.docx",
                reports / f"{source_slug}.pptx",
                reports / f"{source_slug}.docx.qa.json",
                reports / f"{source_slug}-executive-summary.docx.qa.json",
                reports / f"{source_slug}.pptx.qa.json",
                reports / f"{source_slug}-release-manifest.json",
                reports / f"{source_slug}-deck-release-manifest.json",
                self.repo_root / "final" / "Word" / f"{source_slug}.docx",
                self.repo_root / "final" / "PowerPoint" / f"{source_slug}.pptx",
                self.repo_root / "final" / "PDF" / f"{source_slug}.pdf",
                metadata / "report" / f"{source_slug}.json",
                self._ownership_path(source_slug),
            )
            archive_re = re.compile(
                rf"^\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(source_slug)}$"
            )
        elif mode == "scope":
            markers = (
                reports / f"scope-{source_slug}",
                reports / f"{source_slug}-deliverables.zip",
                reports / f"scope-{source_slug}-package-receipt.json",
                reports / f"scope-{source_slug}-package-manifest.json",
                metadata / "scope" / f"{source_slug}.json",
            )
            archive_re = re.compile(
                rf"^\d{{4}}-\d{{2}}-\d{{2}}-scope-{re.escape(source_slug)}$"
            )
        else:
            public_slug = f"argument-{source_slug}"
            markers = (
                reports / f"{public_slug}.md",
                reports / f"{public_slug}-memo.docx",
                reports / f"{public_slug}.pptx",
                reports / f"{public_slug}-release.json",
                metadata / "strengthen" / f"{public_slug}.json",
            )
            archive_re = re.compile(
                rf"^\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(public_slug)}$"
            )
        if any(_lexists(path) for path in markers):
            return True
        if mode == "report" and any(
            _lexists(self.repo_root / Path(relative))
            for relative, _digest, _size in self._builtin_report_ownership_indexes().get(
                source_slug, ()
            )
        ):
            return True
        archives = self._direct_children(self.repo_root / "runs")
        if any(archive_re.fullmatch(path.name) is not None for path in archives):
            return True
        if mode == "report":
            revision_marker = re.compile(
                rf"^{re.escape(source_slug)}-revised-v[1-9][0-9]*"
                r"(?:\.docx|-executive-summary\.docx|\.pptx|"
                r"-release-manifest\.json|-deck-release-manifest\.json)$"
            )
            if any(
                revision_marker.fullmatch(path.name) is not None
                for path in self._direct_children(reports)
            ):
                return True
            for bundle in self._direct_children(reports / "releases"):
                manifest = (
                    None
                    if bundle.is_symlink() or not bundle.is_dir()
                    else self._safe_json_file(bundle / "release-manifest.json")
                )
                manifest_slug = str((manifest or {}).get("slug") or "")
                revision = REVISION_RE.fullmatch(manifest_slug)
                if (
                    manifest_slug == source_slug
                    or (revision and revision.group(1) == source_slug)
                    or self._report_bundle_name_match(bundle.name, source_slug)
                    is not None
                ):
                    return True
            return False

        retry_prefix = (
            f"scope-{source_slug}" if mode == "scope" else f"argument-{source_slug}"
        )
        retry_re = re.compile(
            rf"^\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(retry_prefix)}-([2-9][0-9]*)$"
        )
        receipt_name = (
            "archive-receipt.json"
            if mode == "scope"
            else "argument-archive.json"
        )
        for archive in archives:
            if retry_re.fullmatch(archive.name) is None:
                continue
            receipt = (
                None
                if archive.is_symlink() or not archive.is_dir()
                else self._safe_json_file(archive / receipt_name)
            )
            if receipt and receipt.get("slug") == source_slug:
                return True
        if mode == "scope":
            stale_names = (f"scope-{source_slug}", f"{source_slug}-deliverables.zip")
            for path in self._direct_children(reports):
                for base_name in stale_names:
                    prefix = f"{base_name}.stale-"
                    if path.name.startswith(prefix) and SCOPE_STALE_SUFFIX_RE.fullmatch(
                        path.name[len(prefix):]
                    ):
                        return True
        return False

    def _add_exclusive_source_target(
        self,
        targets: dict[str, tuple[Path, str]],
        *,
        owner_mode: str,
        source_slug: str,
    ) -> None:
        """Move a legacy source directory only when one family owns it.

        Old Council modes all used ``sources/runs/<slug>``. If more than one
        still-live family claims that slug, the first deletion preserves the
        shared directory. Once only one family remains, its next inventory can
        safely include the source bytes.
        """

        claimants = {
            mode
            for mode in ("report", "scope", "strengthen")
            if self._mode_has_source_claim(mode, source_slug)
        }
        if len(claimants) > 1 or (claimants and owner_mode not in claimants):
            return
        self._add_target(
            targets,
            self.repo_root / "sources" / "runs" / source_slug,
            "source_library",
        )

    def _report_inventory(self, requested_mode: str, requested_slug: str) -> ArtifactInventory:
        match = REVISION_RE.fullmatch(requested_slug) if requested_mode == "revision" else None
        base_slug = match.group(1) if match else requested_slug
        if SLUG_RE.fullmatch(base_slug) is None:
            raise InvalidLibraryIdentity("Revision has an unsafe base report slug.")

        targets: dict[str, tuple[Path, str]] = {}
        revision_numbers: set[int] = set()
        artifact_revision_numbers: set[int] = set()
        runs = self.repo_root / "runs"
        archive_name_re = re.compile(
            rf"^\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(base_slug)}$"
        )
        for archive in self._direct_children(runs):
            if archive_name_re.fullmatch(archive.name) is None:
                continue
            self._add_target(targets, archive, "run_archive")
            if archive.is_symlink() or not archive.is_dir():
                continue
            revisions = archive / "revisions"
            if revisions.is_symlink():
                # The whole archive is moved as one opaque directory; never
                # traverse an unexpected revisions link merely to find versions.
                continue
            if revisions.is_dir():
                for revision in self._direct_children(revisions):
                    version = re.fullmatch(r"v([1-9][0-9]*)", revision.name)
                    if version:
                        number = int(version.group(1))
                        revision_numbers.add(number)
                        artifact_revision_numbers.add(number)

        reports = self.repo_root / "reports"
        top_level_revision_re = re.compile(
            rf"^{re.escape(base_slug)}-revised-v([1-9][0-9]*)"
            r"(?:\.docx|-executive-summary\.docx|\.pptx|\.docx\.qa\.json|"
            r"-executive-summary\.docx\.qa\.json|\.pptx\.qa\.json|"
            r"-release-manifest\.json|-deck-release-manifest\.json)$"
        )
        for path in self._direct_children(reports):
            version = top_level_revision_re.fullmatch(path.name)
            if version:
                number = int(version.group(1))
                revision_numbers.add(number)
                artifact_revision_numbers.add(number)

        metadata_revisions = self.state_dir / "library" / "metadata" / "revision"
        metadata_revision_re = re.compile(
            rf"^{re.escape(base_slug)}-revised-v([1-9][0-9]*)\.json$"
        )
        for path in self._direct_children(metadata_revisions):
            version = metadata_revision_re.fullmatch(path.name)
            if version:
                revision_numbers.add(int(version.group(1)))

        releases = reports / "releases"
        for bundle in self._direct_children(releases):
            associated = False
            if not bundle.is_symlink() and bundle.is_dir():
                manifest = self._safe_json_file(bundle / "release-manifest.json")
                manifest_slug = str((manifest or {}).get("slug") or "")
                if manifest_slug == base_slug:
                    associated = True
                else:
                    revision_match = REVISION_RE.fullmatch(manifest_slug)
                    if revision_match and revision_match.group(1) == base_slug:
                        number = int(revision_match.group(2))
                        revision_numbers.add(number)
                        artifact_revision_numbers.add(number)
                        associated = True
            name_match = self._report_bundle_name_match(bundle.name, base_slug)
            if name_match is not None:
                associated = True
                if name_match:
                    revision_numbers.add(name_match)
                    artifact_revision_numbers.add(name_match)
            if associated:
                self._add_target(targets, bundle, "release_bundle")

        release_slugs = [base_slug] + [
            f"{base_slug}-revised-v{number}" for number in sorted(revision_numbers)
        ]
        if match and int(match.group(2)) not in artifact_revision_numbers:
            raise LibraryItemNotFound(
                f"Revision is not part of a released Library family: {requested_slug}."
            )
        fixed_suffixes = (
            ".docx",
            "-executive-summary.docx",
            ".pptx",
            ".docx.qa.json",
            "-executive-summary.docx.qa.json",
            ".pptx.qa.json",
        )
        pointer_suffixes = (
            "-release-manifest.json",
            "-deck-release-manifest.json",
        )
        for release_slug in release_slugs:
            for suffix in fixed_suffixes:
                self._add_target(
                    targets,
                    reports / f"{release_slug}{suffix}",
                    "distribution_file",
                )
            for suffix in pointer_suffixes:
                self._add_target(
                    targets,
                    reports / f"{release_slug}{suffix}",
                    "distribution_pointer",
                )
            # Historical operators also copied exact-slug exports into final/.
            # Include only deterministic names; manually renamed PDFs or decks
            # have no receipt that can safely bind them to this family.
            for path in (
                self.repo_root / "final" / "Word" / f"{release_slug}.docx",
                self.repo_root
                / "final"
                / "PowerPoint"
                / f"{release_slug}.pptx",
                self.repo_root / "final" / "PDF" / f"{release_slug}.pdf",
            ):
                self._add_target(targets, path, "distribution_file")

        self._add_target(
            targets,
            self.repo_root / "prompts" / "runs" / f"{base_slug}.md",
            "prompt",
        )
        self._add_exclusive_source_target(
            targets,
            owner_mode="report",
            source_slug=base_slug,
        )
        self._add_target(
            targets, self._metadata_path("report", base_slug), "metadata"
        )
        for release_slug in release_slugs[1:]:
            self._add_target(
                targets,
                self._metadata_path("revision", release_slug),
                "metadata",
            )
        self._add_builtin_legacy_exports(targets, base_slug)
        self._add_explicit_legacy_exports(targets, base_slug)
        self._add_verified_legacy_exports(targets)

        return self._finish_inventory(
            requested_mode=requested_mode,
            requested_slug=requested_slug,
            family_mode="report",
            family_slug=base_slug,
            public_slug=base_slug,
            revision_slugs=tuple(release_slugs[1:]),
            targets=targets,
        )

    @staticmethod
    def _report_bundle_name_match(name: str, base_slug: str) -> int | None:
        """Return revision number, 0 for base, or None for no exact bundle name."""

        escaped = re.escape(base_slug)
        base = re.fullmatch(
            rf"{escaped}(?:-deck)?-([0-9a-f]{{12}})", name
        )
        if base:
            return 0
        revision = re.fullmatch(
            rf"{escaped}-revised-v([1-9][0-9]*)(?:-deck)?-([0-9a-f]{{12}})",
            name,
        )
        return int(revision.group(1)) if revision else None

    def _scope_inventory(self, slug: str) -> ArtifactInventory:
        targets: dict[str, tuple[Path, str]] = {}
        reports = self.repo_root / "reports"
        fixed = (
            (reports / f"scope-{slug}", "distribution_file"),
            (reports / f"{slug}-deliverables.zip", "distribution_file"),
            (
                reports / f"scope-{slug}-package-receipt.json",
                "distribution_file",
            ),
            (
                reports / f"scope-{slug}-package-manifest.json",
                "distribution_pointer",
            ),
        )
        for path, category in fixed:
            self._add_target(targets, path, category)

        stale_names = (f"scope-{slug}", f"{slug}-deliverables.zip")
        for path in self._direct_children(reports):
            for base_name in stale_names:
                prefix = f"{base_name}.stale-"
                if path.name.startswith(prefix) and SCOPE_STALE_SUFFIX_RE.fullmatch(
                    path.name[len(prefix):]
                ):
                    self._add_target(targets, path, "distribution_file")

        primary_re = re.compile(
            rf"^\d{{4}}-\d{{2}}-\d{{2}}-scope-{re.escape(slug)}$"
        )
        retry_re = re.compile(
            rf"^\d{{4}}-\d{{2}}-\d{{2}}-scope-{re.escape(slug)}-([2-9][0-9]*)$"
        )
        for archive in self._direct_children(self.repo_root / "runs"):
            if primary_re.fullmatch(archive.name):
                self._add_target(targets, archive, "run_archive")
                continue
            if retry_re.fullmatch(archive.name) is None:
                continue
            receipt = (
                None
                if archive.is_symlink() or not archive.is_dir()
                else self._safe_json_file(archive / "archive-receipt.json")
            )
            if receipt and receipt.get("slug") == slug:
                self._add_target(targets, archive, "run_archive")

        self._add_exclusive_source_target(
            targets,
            owner_mode="scope",
            source_slug=slug,
        )
        self._add_target(
            targets, self._metadata_path("scope", slug), "metadata"
        )
        return self._finish_inventory(
            requested_mode="scope",
            requested_slug=slug,
            family_mode="scope",
            family_slug=slug,
            public_slug=slug,
            revision_slugs=(),
            targets=targets,
        )

    def _strengthen_inventory(self, public_slug: str) -> ArtifactInventory:
        source_slug = public_slug.removeprefix("argument-")
        if SLUG_RE.fullmatch(source_slug) is None:
            raise InvalidLibraryIdentity(
                "Strengthened-argument source slug is unsafe."
            )
        targets: dict[str, tuple[Path, str]] = {}
        reports = self.repo_root / "reports"
        for suffix in (".md", "-memo.docx", ".pptx"):
            self._add_target(
                targets,
                reports / f"{public_slug}{suffix}",
                "distribution_file",
            )
        self._add_target(
            targets,
            reports / f"{public_slug}-release.json",
            "distribution_pointer",
        )

        primary_re = re.compile(
            rf"^\d{{4}}-\d{{2}}-\d{{2}}-argument-{re.escape(source_slug)}$"
        )
        retry_re = re.compile(
            rf"^\d{{4}}-\d{{2}}-\d{{2}}-argument-{re.escape(source_slug)}-([2-9][0-9]*)$"
        )
        for archive in self._direct_children(self.repo_root / "runs"):
            if primary_re.fullmatch(archive.name):
                self._add_target(targets, archive, "run_archive")
                continue
            if retry_re.fullmatch(archive.name) is None:
                continue
            receipt = (
                None
                if archive.is_symlink() or not archive.is_dir()
                else self._safe_json_file(archive / "argument-archive.json")
            )
            if receipt and receipt.get("slug") == source_slug:
                self._add_target(targets, archive, "run_archive")

        self._add_exclusive_source_target(
            targets,
            owner_mode="strengthen",
            source_slug=source_slug,
        )
        self._add_target(
            targets,
            self._metadata_path("strengthen", public_slug),
            "metadata",
        )
        return self._finish_inventory(
            requested_mode="strengthen",
            requested_slug=public_slug,
            family_mode="strengthen",
            family_slug=source_slug,
            public_slug=public_slug,
            revision_slugs=(),
            targets=targets,
        )

    def _finish_inventory(
        self,
        *,
        requested_mode: str,
        requested_slug: str,
        family_mode: str,
        family_slug: str,
        public_slug: str,
        revision_slugs: tuple[str, ...],
        targets: dict[str, tuple[Path, str]],
    ) -> ArtifactInventory:
        snapshots = tuple(
            LifecycleTarget(relative, category, _snapshot_path(path))
            for relative, (path, category) in sorted(targets.items())
        )
        if not snapshots:
            raise LibraryItemNotFound(
                f"No Library artifacts were found for {requested_mode}:{requested_slug}."
            )
        return ArtifactInventory(
            requested_mode=requested_mode,
            requested_slug=requested_slug,
            family_mode=family_mode,
            family_slug=family_slug,
            public_slug=public_slug,
            revision_slugs=revision_slugs,
            targets=snapshots,
        )

    def inventory(self, mode: str, slug: str) -> ArtifactInventory:
        mode, slug = _validate_identity(mode, slug)
        self._assert_managed_roots()
        if mode in {"report", "revision"}:
            return self._report_inventory(mode, slug)
        if mode == "scope":
            return self._scope_inventory(slug)
        return self._strengthen_inventory(slug)

    def _check_guard(
        self,
        inventory: ArtifactInventory,
        *,
        active_run: bool,
        interrupted_slug: str | None,
        guard: MutationGuard | None,
    ) -> None:
        if active_run:
            raise MutationBlocked(
                "A Council run is active. Wait for it to finish before changing the Library."
            )
        identities = {
            inventory.requested_slug,
            inventory.family_slug,
            inventory.public_slug,
            *inventory.revision_slugs,
        }
        if interrupted_slug and interrupted_slug in identities:
            raise MutationBlocked(
                "This Library family has an interrupted run. Resume or abandon it first."
            )
        if guard is not None:
            message = guard(inventory.family_mode, inventory.family_slug)
            if message:
                raise MutationBlocked(str(message))

    def create_delete_plan(
        self,
        mode: str,
        slug: str,
        *,
        client_id: str,
        active_run: bool = False,
        interrupted_slug: str | None = None,
        guard: MutationGuard | None = None,
        permanent: bool = False,
    ) -> DeletePlan:
        client = _validate_client_id(client_id)
        with self._lock:
            now = self._clock()
            self._plans = {
                key: value
                for key, value in self._plans.items()
                if value.expires_at > now
            }
            inventory = self.inventory(mode, slug)
            self._check_guard(
                inventory,
                active_run=active_run,
                interrupted_slug=interrupted_slug,
                guard=guard,
            )
            plan = DeletePlan(
                plan_id=secrets.token_urlsafe(24),
                client_id=client,
                created_at=now,
                expires_at=now + self.plan_ttl_seconds,
                confirmation=inventory.family_slug,
                permanent=bool(permanent),
                inventory=inventory,
            )
            self._plans[plan.plan_id] = plan
            return plan

    def _load_plan(self, plan_id: str, client_id: str) -> DeletePlan:
        client = _validate_client_id(client_id)
        if not isinstance(plan_id, str) or not plan_id:
            raise DeletePlanNotFound("Delete plan is missing.")
        plan = self._plans.get(plan_id)
        if plan is None:
            raise DeletePlanNotFound("Delete plan was not found.")
        if not secrets.compare_digest(plan.client_id, client):
            raise DeletePlanForbidden("Delete plan belongs to another browser tab.")
        if plan.expires_at <= self._clock():
            self._plans.pop(plan_id, None)
            raise DeletePlanExpired("Delete plan expired; preview the deletion again.")
        return plan

    def commit_delete(
        self,
        plan_id: str,
        *,
        client_id: str,
        confirmation: str,
        active_run: bool = False,
        interrupted_slug: str | None = None,
        guard: MutationGuard | None = None,
    ) -> DeletionReceipt | PermanentDeletionReceipt:
        with self._lock:
            plan = self._load_plan(plan_id, client_id)
            if not isinstance(confirmation, str) or not secrets.compare_digest(
                confirmation, plan.confirmation
            ):
                raise ConfirmationMismatch(
                    "Deletion confirmation did not match the verified plan; "
                    "preview the deletion again."
                )
            current = self.inventory(
                plan.inventory.requested_mode, plan.inventory.requested_slug
            )
            self._check_guard(
                current,
                active_run=active_run,
                interrupted_slug=interrupted_slug,
                guard=guard,
            )
            if current.digest != plan.inventory.digest:
                raise DeletePlanStale(
                    "Library artifacts changed after the preview; preview the deletion again."
                )
            receipt = self._move_to_trash(plan, current)
            self._plans.pop(plan_id, None)
            if not plan.permanent:
                return receipt
            return self._purge_committed_receipt(receipt)

    def _purge_committed_receipt(
        self, receipt: DeletionReceipt
    ) -> PermanentDeletionReceipt:
        """Permanently remove a committed Trash payload with crash recovery.

        The move transaction has already removed every target from the live
        Library and verified its bytes.  A journal outside the receipt tree is
        written before recursive removal so a process death can only leave a
        cleanup job, never a half-live report family.
        """

        self._assert_managed_roots()
        receipt_dir = self.trash_root / receipt.receipt_id
        if receipt_dir.is_symlink() or not receipt_dir.is_dir():
            raise LifecycleSafetyError(
                "The staged Library deletion is unavailable for permanent removal."
            )
        loaded, raw_inventory, _targets = self._load_committed_receipt(
            receipt_dir, receipt.receipt_id
        )
        if (
            raw_inventory.get("inventory_digest") != receipt.inventory.digest
            or loaded.get("receipt_id") != receipt.receipt_id
        ):
            raise LifecycleSafetyError(
                "The staged Library deletion no longer matches its verified inventory."
            )

        self._ensure_directory(self.purge_journal_root)
        journal_path = self.purge_journal_root / f"{receipt.receipt_id}.json"
        self._atomic_json(
            journal_path,
            {
                "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
                "status": "purging",
                "receipt_id": receipt.receipt_id,
                "inventory_digest": receipt.inventory.digest,
                "total_bytes": receipt.inventory.total_bytes,
            },
        )
        cleanup_pending = False
        try:
            shutil.rmtree(receipt_dir)
            if _lexists(receipt_dir):
                raise OSError("staged deletion still exists after cleanup")
            journal_path.unlink()
        except OSError:
            # The Library entry is already gone. Keep the durable marker so
            # startup recovery can finish reclaiming space without guessing.
            cleanup_pending = True
        return PermanentDeletionReceipt(
            receipt_id=receipt.receipt_id,
            deleted_at=receipt.deleted_at,
            cleanup_pending=cleanup_pending,
            inventory=receipt.inventory,
        )

    def _move_to_trash(
        self, plan: DeletePlan, inventory: ArtifactInventory
    ) -> DeletionReceipt:
        self._assert_managed_roots()
        self._ensure_directory(self.trash_root)
        stamp = datetime.fromtimestamp(
            self._clock(), tz=timezone.utc
        ).strftime("%Y%m%dT%H%M%S%fZ")
        safe_family = inventory.family_slug[:96]
        receipt_id = f"{stamp}-{inventory.family_mode}-{safe_family}-{plan.plan_id[:10]}"
        pending = self.trash_root / f".pending-{plan.plan_id}"
        final = self.trash_root / receipt_id
        if _lexists(pending) or _lexists(final):
            raise LifecycleTransactionError("Library trash transaction already exists.")
        pending.mkdir()
        payload_root = pending / "payload"
        payload_root.mkdir()
        ordered = sorted(inventory.targets, key=_target_priority)
        journal: dict[str, object] = {
            "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
            "status": "moving",
            "plan_id": plan.plan_id,
            "client_id": plan.client_id,
            "created_at": _iso_timestamp(plan.created_at),
            "inventory_digest": inventory.digest,
            "targets": [
                {**target.as_dict(), "moved": False} for target in ordered
            ],
        }
        self._atomic_json(pending / "journal.json", journal)
        moved: list[tuple[LifecycleTarget, Path, Path]] = []
        try:
            for index, target in enumerate(ordered):
                source = self.repo_root / Path(target.relative_path)
                destination = payload_root / Path(target.relative_path)
                if not _lexists(source):
                    raise DeletePlanStale(
                        f"Library artifact disappeared before deletion: {target.relative_path}"
                    )
                current = _snapshot_path(source)
                if current != target.snapshot:
                    raise DeletePlanStale(
                        f"Library artifact changed before deletion: {target.relative_path}"
                    )
                self._ensure_directory(destination.parent)
                if _lexists(destination):
                    raise LifecycleTransactionError(
                        f"Trash destination already exists: {target.relative_path}"
                    )
                os.replace(source, destination)
                moved.append((target, source, destination))
                targets_payload = list(journal["targets"])
                targets_payload[index] = {
                    **dict(targets_payload[index]),
                    "moved": True,
                }
                journal["targets"] = targets_payload
                self._atomic_json(pending / "journal.json", journal)

            deleted_at = _iso_timestamp(self._clock())
            receipt_payload = {
                "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
                "status": "deleted",
                "receipt_id": receipt_id,
                "plan_id": plan.plan_id,
                "client_id": plan.client_id,
                "deleted_at": deleted_at,
                "inventory": {
                    **inventory.summary(),
                    "targets": [target.as_dict() for target in ordered],
                },
            }
            self._atomic_json(pending / "receipt.json", receipt_payload)
            journal["status"] = "committed"
            journal["receipt_id"] = receipt_id
            self._atomic_json(pending / "journal.json", journal)
            os.replace(pending, final)
            return DeletionReceipt(
                receipt_id=receipt_id,
                deleted_at=deleted_at,
                trash_path=self._relative(final),
                inventory=inventory,
            )
        except Exception as exc:
            rollback_errors: list[str] = []
            for _target, source, destination in reversed(moved):
                try:
                    self._ensure_directory(source.parent)
                    if _lexists(source):
                        raise RestoreConflict(
                            f"Rollback target already exists: {source}"
                        )
                    os.replace(destination, source)
                except Exception as rollback_exc:  # noqa: BLE001 - preserve journal
                    rollback_errors.append(str(rollback_exc))
            if rollback_errors:
                try:
                    journal["status"] = "rollback_failed"
                    journal["error"] = str(exc)
                    journal["rollback_errors"] = rollback_errors
                    self._atomic_json(pending / "journal.json", journal)
                except Exception:
                    pass
                raise LifecycleTransactionError(
                    "Library deletion failed and automatic rollback was incomplete; "
                    f"the recovery journal is {self._relative(pending)}."
                ) from exc
            shutil.rmtree(pending, ignore_errors=True)
            if isinstance(exc, LibraryLifecycleError):
                raise
            raise LifecycleTransactionError(
                "Library deletion failed; every moved artifact was restored."
            ) from exc

    def _load_committed_receipt(
        self, receipt_dir: Path, receipt_id: str
    ) -> tuple[dict[str, Any], dict[str, Any], list[LifecycleTarget]]:
        receipt = self._safe_json_file(receipt_dir / "receipt.json")
        if (
            receipt is None
            or receipt.get("schema_version") != DELETE_RECEIPT_SCHEMA_VERSION
            or receipt.get("status") != "deleted"
            or receipt.get("receipt_id") != receipt_id
        ):
            raise LifecycleSafetyError("Library deletion receipt is invalid.")
        raw_inventory = receipt.get("inventory")
        raw_targets = (
            raw_inventory.get("targets")
            if isinstance(raw_inventory, dict)
            else None
        )
        if (
            not isinstance(raw_inventory, dict)
            or not isinstance(raw_targets, list)
            or not raw_targets
        ):
            raise LifecycleSafetyError("Library deletion receipt has no targets.")

        targets: list[LifecycleTarget] = []
        for raw in raw_targets:
            if not isinstance(raw, dict):
                raise LifecycleSafetyError("Library deletion target is invalid.")
            relative = self._managed_target_relative(str(raw.get("path") or ""))
            category = str(raw.get("category") or "")
            kind = str(raw.get("kind") or "")
            digest = str(raw.get("digest") or "")
            counts = (
                raw.get("file_count"),
                raw.get("total_bytes"),
                raw.get("symlink_count"),
            )
            if (
                category not in TARGET_CATEGORIES
                or kind not in {"file", "directory", "symlink"}
                or re.fullmatch(r"[0-9a-f]{64}", digest) is None
                or any(
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or value < 0
                    for value in counts
                )
            ):
                raise LifecycleSafetyError("Library deletion target binding is invalid.")
            snapshot = PathSnapshot(
                kind=kind,
                digest=digest,
                file_count=counts[0],
                total_bytes=counts[1],
                symlink_count=counts[2],
            )
            targets.append(LifecycleTarget(relative, category, snapshot))
        return receipt, raw_inventory, targets

    def restore(
        self,
        receipt_id: str,
        *,
        active_run: bool = False,
        guard: MutationGuard | None = None,
    ) -> RestoreReceipt:
        """Restore one committed trash receipt, exposing pointers last."""

        if (
            not isinstance(receipt_id, str)
            or Path(receipt_id).name != receipt_id
            or re.fullmatch(r"[A-Za-z0-9._-]{1,240}", receipt_id) is None
        ):
            raise InvalidLibraryIdentity("Unsafe Library receipt ID.")
        with self._lock:
            self._assert_managed_roots()
            receipt_dir = self.trash_root / receipt_id
            if receipt_dir.is_symlink() or not receipt_dir.is_dir():
                raise LibraryItemNotFound("Library trash receipt was not found.")
            if (receipt_dir / "restore-receipt.json").is_file():
                raise RestoreConflict("This Library deletion was already restored.")
            _receipt, raw_inventory, targets = self._load_committed_receipt(
                receipt_dir, receipt_id
            )
            family_mode = str(raw_inventory.get("family_mode") or "")
            family_slug = str(raw_inventory.get("family_slug") or "")
            if active_run:
                raise MutationBlocked(
                    "A Council run is active. Wait for it to finish before restoring."
                )
            if guard is not None:
                message = guard(family_mode, family_slug)
                if message:
                    raise MutationBlocked(str(message))

            payload_root = receipt_dir / "payload"
            if payload_root.is_symlink() or not payload_root.is_dir():
                raise LifecycleSafetyError("Library trash payload is unavailable.")
            for target in targets:
                source = payload_root / Path(target.relative_path)
                destination = self.repo_root / Path(target.relative_path)
                self._assert_payload_parentage(source, payload_root)
                self._ensure_directory(destination.parent)
                if not _lexists(source) or _snapshot_path(source) != target.snapshot:
                    raise LifecycleSafetyError(
                        f"Trashed Library artifact changed: {target.relative_path}"
                    )
                if _lexists(destination):
                    raise RestoreConflict(
                        f"Cannot restore because a current path exists: {target.relative_path}"
                    )

            # Reversing deletion priority restores archives and supporting bytes
            # before the public current pointer makes downloads discoverable.
            ordered = sorted(targets, key=_target_priority, reverse=True)
            restored: list[tuple[LifecycleTarget, Path, Path]] = []
            journal_path = receipt_dir / "restore-journal.json"
            self._atomic_json(
                journal_path,
                {
                    "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
                    "status": "restoring",
                    "receipt_id": receipt_id,
                    "targets": [target.as_dict() for target in ordered],
                },
            )
            try:
                for target in ordered:
                    source = payload_root / Path(target.relative_path)
                    destination = self.repo_root / Path(target.relative_path)
                    self._ensure_directory(destination.parent)
                    os.replace(source, destination)
                    restored.append((target, source, destination))
                restored_at = _iso_timestamp(self._clock())
                self._atomic_json(
                    receipt_dir / "restore-receipt.json",
                    {
                        "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
                        "status": "restored",
                        "receipt_id": receipt_id,
                        "restored_at": restored_at,
                        "target_count": len(restored),
                    },
                )
                self._atomic_json(
                    journal_path,
                    {
                        "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
                        "status": "restored",
                        "receipt_id": receipt_id,
                    },
                )
                return RestoreReceipt(receipt_id, restored_at, len(restored))
            except Exception as exc:
                rollback_errors: list[str] = []
                for _target, source, destination in reversed(restored):
                    try:
                        self._ensure_directory(source.parent)
                        os.replace(destination, source)
                    except Exception as rollback_exc:  # noqa: BLE001
                        rollback_errors.append(str(rollback_exc))
                self._atomic_json(
                    journal_path,
                    {
                        "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
                        "status": "restore_failed",
                        "receipt_id": receipt_id,
                        "error": str(exc),
                        "rollback_errors": rollback_errors,
                    },
                )
                if rollback_errors:
                    raise LifecycleTransactionError(
                        "Library restore failed and rollback was incomplete."
                    ) from exc
                raise LifecycleTransactionError(
                    "Library restore failed; restored paths were moved back to Trash."
                ) from exc

    def recover_pending_restores(self) -> list[str]:
        """Complete restores interrupted between filesystem moves and receipt.

        Filesystem state is authoritative. For every receipt target, exactly
        one of the Trash payload and original destination must exist, and the
        existing copy must still match the deletion snapshot. Re-running this
        method after any later crash therefore converges on the same fully
        restored state without duplicating or overwriting bytes.
        """

        recovered: list[str] = []
        with self._lock:
            self._assert_managed_roots()
            for receipt_dir in self._direct_children(self.trash_root):
                if receipt_dir.name.startswith(".pending-"):
                    continue
                if receipt_dir.is_symlink() or not receipt_dir.is_dir():
                    raise LifecycleSafetyError(
                        f"Library trash receipt is unsafe: {receipt_dir}"
                    )
                journal_path = receipt_dir / "restore-journal.json"
                if not _lexists(journal_path):
                    continue
                if (receipt_dir / "restore-receipt.json").is_file():
                    # restore() writes the durable receipt before marking the
                    # journal complete, so this is already a committed restore.
                    continue
                journal = self._safe_json_file(journal_path)
                if (
                    journal is None
                    or journal.get("schema_version")
                    != DELETE_RECEIPT_SCHEMA_VERSION
                    or journal.get("receipt_id") != receipt_dir.name
                ):
                    raise LifecycleSafetyError(
                        f"Pending Library restore has an invalid journal: {receipt_dir}"
                    )
                status = journal.get("status")
                if status != "restoring":
                    if status == "restored":
                        raise LifecycleSafetyError(
                            "Library restore journal is complete but its receipt "
                            f"is missing: {receipt_dir.name}"
                        )
                    # A restore_failed journal with a successful rollback is not
                    # pending. The operator may safely try Restore again.
                    continue

                _receipt, _raw_inventory, targets = self._load_committed_receipt(
                    receipt_dir, receipt_dir.name
                )
                payload_root = receipt_dir / "payload"
                if payload_root.is_symlink() or not payload_root.is_dir():
                    raise LifecycleSafetyError(
                        "Pending Library restore has no safe Trash payload."
                    )
                ordered = sorted(targets, key=_target_priority, reverse=True)
                for target in ordered:
                    source = payload_root / Path(target.relative_path)
                    destination = self.repo_root / Path(target.relative_path)
                    self._assert_payload_parentage(source, payload_root)
                    self._ensure_directory(destination.parent)
                    payload_exists = _lexists(source)
                    destination_exists = _lexists(destination)
                    if payload_exists and destination_exists:
                        raise RestoreConflict(
                            "Pending Library restore has two copies of: "
                            f"{target.relative_path}"
                        )
                    if not payload_exists and not destination_exists:
                        raise RestoreConflict(
                            "Pending Library restore is missing both copies of: "
                            f"{target.relative_path}"
                        )
                    existing = source if payload_exists else destination
                    if _snapshot_path(existing) != target.snapshot:
                        raise LifecycleSafetyError(
                            "Pending Library restore artifact changed: "
                            f"{target.relative_path}"
                        )
                    if destination_exists:
                        continue
                    os.replace(source, destination)

                restored_at = _iso_timestamp(self._clock())
                self._atomic_json(
                    receipt_dir / "restore-receipt.json",
                    {
                        "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
                        "status": "restored",
                        "receipt_id": receipt_dir.name,
                        "restored_at": restored_at,
                        "target_count": len(ordered),
                        "recovered_after_crash": True,
                    },
                )
                self._atomic_json(
                    journal_path,
                    {
                        "schema_version": DELETE_RECEIPT_SCHEMA_VERSION,
                        "status": "restored",
                        "receipt_id": receipt_dir.name,
                    },
                )
                recovered.append(receipt_dir.name)
        return recovered

    def recover_pending_purges(self) -> list[str]:
        """Finish permanent deletions interrupted during recursive cleanup."""

        recovered: list[str] = []
        with self._lock:
            self._assert_managed_roots()
            for journal_path in self._direct_children(self.purge_journal_root):
                if journal_path.is_symlink() or not journal_path.is_file():
                    raise LifecycleSafetyError(
                        f"Permanent deletion journal is unsafe: {journal_path}"
                    )
                journal = self._safe_json_file(journal_path)
                receipt_id = str((journal or {}).get("receipt_id") or "")
                if (
                    journal is None
                    or journal.get("schema_version")
                    != DELETE_RECEIPT_SCHEMA_VERSION
                    or journal.get("status") != "purging"
                    or journal_path.name != f"{receipt_id}.json"
                    or Path(receipt_id).name != receipt_id
                    or re.fullmatch(r"[A-Za-z0-9._-]{1,240}", receipt_id) is None
                ):
                    raise LifecycleSafetyError(
                        f"Permanent deletion journal is invalid: {journal_path}"
                    )
                receipt_dir = self.trash_root / receipt_id
                if _lexists(receipt_dir):
                    if receipt_dir.is_symlink() or not receipt_dir.is_dir():
                        raise LifecycleSafetyError(
                            f"Permanent deletion payload is unsafe: {receipt_dir}"
                        )
                    shutil.rmtree(receipt_dir)
                    if _lexists(receipt_dir):
                        raise LifecycleTransactionError(
                            f"Permanent deletion cleanup did not finish: {receipt_id}"
                        )
                journal_path.unlink()
                recovered.append(receipt_id)
        return recovered

    def recover_pending_transactions(self) -> list[str]:
        """Recover incomplete deletes and restores left by a process crash."""

        recovered: list[str] = []
        with self._lock:
            self._assert_managed_roots()
            recovered.extend(self.recover_pending_purges())
            for pending in self._direct_children(self.trash_root):
                if not pending.name.startswith(".pending-"):
                    continue
                if pending.is_symlink() or not pending.is_dir():
                    raise LifecycleSafetyError(
                        f"Pending Library transaction is unsafe: {pending}"
                    )
                journal = self._safe_json_file(pending / "journal.json")
                targets = (journal or {}).get("targets")
                if not isinstance(targets, list):
                    raise LifecycleSafetyError(
                        f"Pending Library transaction has no journal: {pending}"
                    )
                payload_root = pending / "payload"
                if payload_root.is_symlink() or not payload_root.is_dir():
                    raise LifecycleSafetyError(
                        f"Pending Library transaction has no safe payload: {pending}"
                    )
                conflicts: list[str] = []
                for raw in reversed(targets):
                    if not isinstance(raw, dict):
                        raise LifecycleSafetyError(
                            "Pending Library transaction contains an invalid target."
                        )
                    relative = str(raw.get("path") or "")
                    relative = self._managed_target_relative(relative)
                    source = payload_root / Path(relative)
                    destination = self.repo_root / Path(relative)
                    self._assert_payload_parentage(source, payload_root)
                    payload_exists = _lexists(source)
                    original_exists = _lexists(destination)
                    # Inspect actual path state rather than trusting only the
                    # journal flag. A process can die after os.replace succeeds
                    # but before moved=true is durably written.
                    if not payload_exists:
                        if not original_exists:
                            conflicts.append(relative)
                        continue
                    if original_exists:
                        conflicts.append(relative)
                        continue
                    self._ensure_directory(destination.parent)
                    os.replace(source, destination)
                if conflicts:
                    raise RestoreConflict(
                        "Pending Library transaction needs manual recovery: "
                        + ", ".join(conflicts)
                    )
                shutil.rmtree(pending)
                recovered.append(pending.name)
            recovered.extend(self.recover_pending_restores())
        return recovered


__all__ = [
    "ArtifactInventory",
    "ConfirmationMismatch",
    "DeletePlan",
    "DeletePlanExpired",
    "DeletePlanForbidden",
    "DeletePlanNotFound",
    "DeletePlanStale",
    "DeletionReceipt",
    "InvalidLibraryIdentity",
    "LibraryItemNotFound",
    "LibraryLifecycle",
    "LibraryLifecycleError",
    "LifecycleSafetyError",
    "LifecycleTarget",
    "LifecycleTransactionError",
    "MetadataValidationError",
    "MutationBlocked",
    "PermanentDeletionReceipt",
    "RestoreConflict",
    "RestoreReceipt",
]
