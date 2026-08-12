"""Typed artifact validation for Council pipeline outputs.

The original orchestrator treated any file larger than 200 bytes as complete.
That made resume convenient, but it also accepted truncated markdown, invalid
JSON, and corrupt Office files.  This module provides lightweight, deterministic
contracts that are strict enough to catch broken handoffs without requiring a
model call.
"""
from __future__ import annotations

import hashlib
import json
import re
import zipfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


_WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
_PLACEHOLDER_RE = re.compile(r"\{\{[^{}\n]+\}\}")


@dataclass(frozen=True)
class ArtifactContract:
    """Minimum structural expectations for one pipeline artifact."""

    kind: str
    min_words: int = 0
    min_records: int = 0
    required_keys: tuple[str, ...] = ()
    required_any: tuple[tuple[str, ...], ...] = ()
    # (trigger_field, (fields that must then be present, ...)). Lets one
    # provenance form carry a stricter burden than another: an offline citation
    # is accepted only when it also names where in the work the claim lives.
    requires_with: tuple[tuple[str, tuple[str, ...]], ...] = ()
    optional: bool = False


@dataclass
class ArtifactValidation:
    """Serializable result of applying an :class:`ArtifactContract`."""

    path: str
    valid: bool
    kind: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    size_bytes: int = 0
    word_count: int = 0
    record_count: int = 0
    sha256: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def contract_for_path(path: Path, *, optional: bool = False) -> ArtifactContract:
    """Infer a sensible contract from a pipeline filename.

    The thresholds intentionally validate structure, not editorial quality.
    Quality is handled later by the publication gate and human checkpoints.
    """

    name = path.name.lower()
    suffix = path.suffix.lower()

    if suffix == ".md":
        if name.endswith("-brief.md"):
            minimum = 100
        elif "strategist-draft" in name or name in {
            "edited-draft.md",
            "humanized-draft.md",
            "final-draft.md",
        }:
            minimum = 250
        elif any(
            token in name
            for token in (
                "critique",
                "review",
                "curation",
                "evidence-map",
                "narrative-options",
                "airport-context",
            )
        ):
            minimum = 60
        elif "fact-check" in name:
            minimum = 40
        else:
            minimum = 20
        return ArtifactContract("markdown", min_words=minimum, optional=optional)

    if suffix == ".json":
        return ArtifactContract("json", optional=optional)
    if suffix == ".jsonl":
        return ArtifactContract("jsonl", min_records=1, optional=optional)
    if suffix == ".pptx":
        return ArtifactContract("pptx", optional=optional)
    if suffix == ".docx":
        return ArtifactContract("docx", optional=optional)
    return ArtifactContract("binary", optional=optional)


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_markdown(path: Path, contract: ArtifactContract) -> tuple[list[str], list[str], int, int]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ["not valid UTF-8 text"], warnings, 0, 0

    words = len(_WORD_RE.findall(text))
    if words < contract.min_words:
        errors.append(
            f"contains {words} words; contract requires at least {contract.min_words}"
        )
    if _PLACEHOLDER_RE.search(text):
        errors.append("contains an unresolved {{placeholder}}")
    if text.rstrip().endswith(("…", "...", "TODO", "TBD")):
        warnings.append("content may be truncated or unfinished")
    return errors, warnings, words, 0


def _validate_json(path: Path, contract: ArtifactContract) -> tuple[list[str], list[str], int, int]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"invalid JSON: {exc}"], [], 0, 0
    if not isinstance(payload, (dict, list)):
        errors.append("JSON root must be an object or array")
    if contract.required_keys and isinstance(payload, dict):
        missing = [key for key in contract.required_keys if key not in payload]
        if missing:
            errors.append(f"missing required keys: {', '.join(missing)}")
        for group in contract.required_any:
            if not any(payload.get(key) not in (None, "") for key in group):
                errors.append(
                    "requires at least one of: " + ", ".join(group)
                )
        for trigger, dependents in contract.requires_with:
            if payload.get(trigger) in (None, ""):
                continue
            absent = [k for k in dependents if payload.get(k) in (None, "")]
            if absent:
                errors.append(
                    f"uses {trigger} and must also set: " + ", ".join(absent)
                )
    return errors, [], 0, len(payload) if isinstance(payload, list) else 1


def _validate_jsonl(path: Path, contract: ArtifactContract) -> tuple[list[str], list[str], int, int]:
    errors: list[str] = []
    records = 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return ["not valid UTF-8 text"], [], 0, 0

    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number} is invalid JSON: {exc.msg}")
            continue
        if not isinstance(record, dict):
            errors.append(f"line {number} must contain a JSON object")
            continue
        missing = [key for key in contract.required_keys if key not in record]
        if missing:
            errors.append(
                f"line {number} missing required keys: {', '.join(missing)}"
            )
        for group in contract.required_any:
            if not any(record.get(key) not in (None, "") for key in group):
                errors.append(
                    f"line {number} requires at least one of: {', '.join(group)}"
                )
        for trigger, dependents in contract.requires_with:
            if record.get(trigger) in (None, ""):
                continue
            absent = [k for k in dependents if record.get(k) in (None, "")]
            if absent:
                errors.append(
                    f"line {number} uses {trigger} and must also set: "
                    + ", ".join(absent)
                )
        records += 1
    if records < contract.min_records:
        errors.append(
            f"contains {records} records; contract requires at least {contract.min_records}"
        )
    return errors, [], 0, records


def _validate_office_zip(
    path: Path, *, member: str
) -> tuple[list[str], list[str], int, int]:
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"invalid Office package: {exc}"], [], 0, 0
    errors: list[str] = []
    for required in ("[Content_Types].xml", member):
        if required not in names:
            errors.append(f"Office package is missing {required}")
    return errors, [], 0, 0


def validate_artifact(
    path: Path, contract: ArtifactContract | None = None
) -> ArtifactValidation:
    """Validate ``path`` and return a detailed, serializable result."""

    contract = contract or contract_for_path(path)
    result = ArtifactValidation(path=str(path), valid=False, kind=contract.kind)
    try:
        if not path.is_file():
            if contract.optional:
                result.valid = True
                result.warnings.append("optional artifact is not present")
            else:
                result.errors.append("file does not exist")
            return result
        result.size_bytes = path.stat().st_size
        if result.size_bytes == 0:
            result.errors.append("file is empty")
            return result
    except OSError as exc:
        result.errors.append(f"cannot inspect file: {exc}")
        return result

    if contract.kind == "markdown":
        errors, warnings, words, records = _validate_markdown(path, contract)
    elif contract.kind == "json":
        errors, warnings, words, records = _validate_json(path, contract)
    elif contract.kind == "jsonl":
        errors, warnings, words, records = _validate_jsonl(path, contract)
    elif contract.kind == "pptx":
        errors, warnings, words, records = _validate_office_zip(
            path, member="ppt/presentation.xml"
        )
    elif contract.kind == "docx":
        errors, warnings, words, records = _validate_office_zip(
            path, member="word/document.xml"
        )
    else:
        errors, warnings, words, records = [], [], 0, 0

    result.errors.extend(errors)
    result.warnings.extend(warnings)
    result.word_count = words
    result.record_count = records
    result.valid = not result.errors
    if result.valid:
        try:
            result.sha256 = _hash_file(path)
        except OSError as exc:
            result.valid = False
            result.errors.append(f"cannot hash file: {exc}")
    return result
