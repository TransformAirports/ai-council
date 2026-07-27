"""Structured evaluation artifacts for Council runs.

The evaluator deliberately consumes records rather than attempting to recover
provenance from prose.  A final report is expected *not* to name the research
agents that informed it, so searching the report for an agent's display name is
neither a valid contribution metric nor a safe fallback.

Canonical artifact names (all relative to an archived run) are:

```
run-manifest.json
evidence-ledger.jsonl
claim-lineage.jsonl
evaluation/reviews/<review-id>.json
```

The readers also accept JSON arrays/containers, common underscore variants,
locations under ``metadata/`` or ``evaluation/``, and paths declared in the run
manifest.  This tolerance keeps old archives readable while the pipeline moves
to the canonical contracts.

A human quality-review record looks like:

```
{
  "schema_version": "1.0",
  "review_id": "board-review-1",
  "reviewer": {"type": "human", "name": "Reviewer name"},
  "reviewed_at": "2026-07-23T15:30:00+00:00",
  "rubric": {
    "originality": {"score": 4, "scale_min": 1, "scale_max": 5},
    "airport_specificity": {"score": 5, "scale_min": 1, "scale_max": 5},
    "decision_usefulness": {"score": 4, "scale_min": 1, "scale_max": 5},
    "writing": {"score": 4, "scale_min": 1, "scale_max": 5},
    "visual_quality": {"score": 3, "scale_min": 1, "scale_max": 5}
  },
  "notes": "Optional review notes."
}
```

Only structured IDs connect claims, evidence, and agents.  Unknown or malformed
fields remain unavailable; the module never manufactures a numeric score.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


RUBRIC_DIMENSIONS: tuple[str, ...] = (
    "originality",
    "airport_specificity",
    "decision_usefulness",
    "writing",
    "visual_quality",
)

_RUBRIC_ALIASES: dict[str, str] = {
    "originality": "originality",
    "creativity": "originality",
    "airport_specificity": "airport_specificity",
    "airport_specific": "airport_specificity",
    "specificity": "airport_specificity",
    "decision_usefulness": "decision_usefulness",
    "decision_utility": "decision_usefulness",
    "usefulness": "decision_usefulness",
    "writing": "writing",
    "writing_quality": "writing",
    "prose_quality": "writing",
    "visual_quality": "visual_quality",
    "design_quality": "visual_quality",
    "visuals": "visual_quality",
}

_PRIMARY_SOURCE_TYPES: set[str] = {
    "primary",
    "primary_source",
    "official_record",
    "official_document",
    "government_record",
    "regulation",
    "statute",
    "audited_financial",
    "audited_financial_statement",
    "airport_document",
    "airport_record",
    "original_dataset",
    "dataset",
    "interview",
    "testimony",
}

_VERIFIED_STATUSES: set[str] = {
    "verified",
    "supported",
    "confirmed",
    "accepted",
    "pass",
    "passed",
}
_REMOVED_STATUSES: set[str] = {
    "removed",
    "rejected",
    "deleted",
    "unsupported",
    "failed",
}
_UNVERIFIED_STATUSES: set[str] = {
    "unverified",
    "needs_review",
    "needs_human_review",
    "inconclusive",
    "pending",
    "flagged",
    "not_checked",
    "not_verified",
    "matched_to_evidence_ledger",
    "cited_not_matched_to_ledger",
    "source_matched_not_verified",
}
_QUALIFIED_STATUSES: set[str] = {
    "qualified",
    "narrowed",
    "conditioned",
}
_CORRECTED_STATUSES: set[str] = {
    "corrected",
    "revised",
    "modified",
    "fixed",
}


def _normalise_key(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _nested_get(raw: Mapping[str, Any], *paths: Sequence[str]) -> Any:
    for path in paths:
        value: Any = raw
        for part in path:
            if not isinstance(value, Mapping) or part not in value:
                break
            value = value[part]
        else:
            return value
    return None


def _as_string(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return None


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalised = _normalise_key(value)
        if normalised in {"true", "yes", "y", "1", "primary"}:
            return True
        if normalised in {"false", "no", "n", "0", "secondary"}:
            return False
    if isinstance(value, (int, float)) and value in {0, 1}:
        return bool(value)
    return None


def _as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    agent_id: str | None
    is_primary: bool | None
    source_type: str | None
    source_path: Path
    raw: Mapping[str, Any] = field(repr=False)


@dataclass(frozen=True)
class ClaimRecord:
    claim_id: str
    evidence_ids: tuple[str, ...]
    verification_status: str
    primary_source_checked: bool | None
    corrected: bool
    source_path: Path
    raw: Mapping[str, Any] = field(repr=False)


@dataclass(frozen=True)
class RubricScore:
    dimension: str
    score: float
    scale_min: float = 1.0
    scale_max: float = 5.0
    notes: str | None = None

    @property
    def score_on_five_point_scale(self) -> float | None:
        if self.scale_max <= self.scale_min:
            return None
        if not (self.scale_min <= self.score <= self.scale_max):
            return None
        return 1.0 + 4.0 * (
            (self.score - self.scale_min) / (self.scale_max - self.scale_min)
        )


@dataclass(frozen=True)
class QualityReview:
    review_id: str
    reviewer_type: str
    reviewer_name: str | None
    reviewed_at: str | None
    rubric: Mapping[str, RubricScore]
    notes: str | None
    source_path: Path

    @property
    def is_human(self) -> bool:
        return _normalise_key(self.reviewer_type) in {
            "human",
            "operator",
            "executive",
            "board_member",
            "subject_matter_expert",
        }


@dataclass(frozen=True)
class ArtifactDiscovery:
    manifest_path: Path | None
    manifest: Mapping[str, Any] | None
    evidence_paths: tuple[Path, ...]
    lineage_paths: tuple[Path, ...]
    review_paths: tuple[Path, ...]
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class RecordLoad:
    records: tuple[Mapping[str, Any], ...]
    warnings: tuple[str, ...] = ()


def _read_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"Could not read structured artifact `{path.name}`: {exc}"


def _records_from_json_value(
    value: Any,
    *,
    container_keys: Iterable[str],
) -> list[Mapping[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, Mapping)]
    if not isinstance(value, Mapping):
        return []
    normalised_keys = {_normalise_key(k): k for k in value}
    for candidate in container_keys:
        actual = normalised_keys.get(_normalise_key(candidate))
        if actual is None:
            continue
        nested = value[actual]
        if isinstance(nested, list):
            return [item for item in nested if isinstance(item, Mapping)]
        if isinstance(nested, Mapping):
            return [
                item for item in nested.values()
                if isinstance(item, Mapping)
            ]
    # A single record is accepted when no container key is present.
    return [value]


def read_records(
    path: Path,
    *,
    container_keys: Iterable[str],
) -> RecordLoad:
    warnings: list[str] = []
    records: list[Mapping[str, Any]] = []
    if path.suffix.lower() == ".jsonl":
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            return RecordLoad((), (f"Could not read `{path.name}`: {exc}",))
        for line_number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                warnings.append(
                    f"`{path.name}` line {line_number} is invalid JSON: {exc.msg}"
                )
                continue
            if isinstance(value, Mapping):
                records.append(value)
            else:
                warnings.append(
                    f"`{path.name}` line {line_number} is not a JSON object"
                )
    else:
        value, warning = _read_json(path)
        if warning:
            warnings.append(warning)
        elif value is not None:
            records.extend(
                _records_from_json_value(value, container_keys=container_keys)
            )
    return RecordLoad(tuple(records), tuple(warnings))


def _candidate_manifest_paths(run_dir: Path) -> list[Path]:
    return [
        run_dir / "run-manifest.json",
        run_dir / "run_manifest.json",
        run_dir / "manifest.json",
        run_dir / "metadata" / "run-manifest.json",
        run_dir / "metadata" / "run_manifest.json",
        run_dir / "evaluation" / "run-manifest.json",
    ]


def _collect_declared_paths(
    value: Any,
    *,
    run_dir: Path,
    wanted_keys: set[str],
    current_key: str = "",
) -> list[Path]:
    found: list[Path] = []
    key_matches = _normalise_key(current_key) in wanted_keys
    if isinstance(value, Mapping):
        if key_matches:
            for path_key in ("path", "file", "uri"):
                if path_key in value and isinstance(value[path_key], str):
                    candidate = Path(value[path_key])
                    found.append(
                        candidate if candidate.is_absolute() else run_dir / candidate
                    )
        # Common artifact declaration: {"kind": "evidence_ledger",
        # "path": "metadata/evidence-ledger.jsonl"}.
        kind = _normalise_key(
            value.get("kind")
            or value.get("type")
            or value.get("name")
            or ""
        )
        if kind in wanted_keys:
            for path_key in ("path", "file", "uri"):
                if path_key in value and isinstance(value[path_key], str):
                    candidate = Path(value[path_key])
                    found.append(
                        candidate if candidate.is_absolute() else run_dir / candidate
                    )
        for key, nested in value.items():
            found.extend(
                _collect_declared_paths(
                    nested,
                    run_dir=run_dir,
                    wanted_keys=wanted_keys,
                    current_key=str(key),
                )
            )
    elif isinstance(value, list):
        for item in value:
            found.extend(
                _collect_declared_paths(
                    item,
                    run_dir=run_dir,
                    wanted_keys=wanted_keys,
                    current_key=current_key,
                )
            )
    elif key_matches and isinstance(value, str):
        candidate = Path(value)
        found.append(candidate if candidate.is_absolute() else run_dir / candidate)
    return found


def _unique_existing(paths: Iterable[Path]) -> tuple[Path, ...]:
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        try:
            resolved = path.resolve()
        except OSError:
            resolved = path
        if resolved in seen or not path.is_file():
            continue
        seen.add(resolved)
        unique.append(path)
    return tuple(unique)


def _structured_files_only(paths: Iterable[Path]) -> tuple[Path, ...]:
    return _unique_existing(
        path for path in paths if path.suffix.lower() in {".json", ".jsonl"}
    )


def discover_artifacts(run_dir: Path) -> ArtifactDiscovery:
    warnings: list[str] = []
    manifest_path = next(
        (path for path in _candidate_manifest_paths(run_dir) if path.is_file()),
        None,
    )
    manifest: Mapping[str, Any] | None = None
    if manifest_path is not None:
        value, warning = _read_json(manifest_path)
        if warning:
            warnings.append(warning)
        elif isinstance(value, Mapping):
            manifest = value
        else:
            warnings.append(f"`{manifest_path.name}` is not a JSON object")

    evidence_candidates = [
        run_dir / "evidence-ledger.jsonl",
        run_dir / "evidence-ledger.json",
        run_dir / "evidence_ledger.jsonl",
        run_dir / "evidence_ledger.json",
        run_dir / "metadata" / "evidence-ledger.jsonl",
        run_dir / "metadata" / "evidence-ledger.json",
        run_dir / "evaluation" / "evidence-ledger.jsonl",
        run_dir / "evaluation" / "evidence-ledger.json",
        run_dir / "stage1" / "evidence-ledger.jsonl",
        run_dir / "stage1" / "evidence-ledger.json",
    ]
    lineage_candidates = [
        run_dir / "claim-lineage.jsonl",
        run_dir / "claim-lineage.json",
        run_dir / "claim_lineage.jsonl",
        run_dir / "claim_lineage.json",
        run_dir / "metadata" / "claim-lineage.jsonl",
        run_dir / "metadata" / "claim-lineage.json",
        run_dir / "evaluation" / "claim-lineage.jsonl",
        run_dir / "evaluation" / "claim-lineage.json",
        run_dir / "stage3" / "claim-lineage.jsonl",
        run_dir / "stage3" / "claim-lineage.json",
    ]
    review_candidates = [
        run_dir / "quality-review.json",
        run_dir / "quality-reviews.json",
        run_dir / "quality-reviews.jsonl",
        run_dir / "human-review.json",
        run_dir / "human-reviews.json",
        run_dir / "human-reviews.jsonl",
        run_dir / "evaluation" / "quality-reviews.jsonl",
        run_dir / "evaluation" / "human-reviews.jsonl",
    ]
    for review_dir in (run_dir / "reviews", run_dir / "evaluation" / "reviews"):
        if review_dir.is_dir():
            review_candidates.extend(sorted(review_dir.glob("*.json")))
            review_candidates.extend(sorted(review_dir.glob("*.jsonl")))

    if manifest is not None:
        evidence_candidates.extend(
            _collect_declared_paths(
                manifest,
                run_dir=run_dir,
                wanted_keys={
                    "evidence",
                    "evidence_ledger",
                    "evidence_records",
                },
            )
        )
        lineage_candidates.extend(
            _collect_declared_paths(
                manifest,
                run_dir=run_dir,
                wanted_keys={
                    "claim_lineage",
                    "lineage",
                    "claim_records",
                },
            )
        )
        review_candidates.extend(
            _collect_declared_paths(
                manifest,
                run_dir=run_dir,
                wanted_keys={
                    "quality_review",
                    "quality_reviews",
                    "human_review",
                    "human_reviews",
                    "review_records",
                },
            )
        )

    evidence_paths = _structured_files_only(evidence_candidates)
    canonical_evidence = run_dir / "evidence-ledger.jsonl"
    if canonical_evidence in evidence_paths:
        # ``stage1/evidence-ledger.jsonl`` is a byte-for-byte compatibility
        # mirror in Council v2, not a second commissioned evidence set.
        evidence_paths = tuple(
            path
            for path in evidence_paths
            if path != run_dir / "stage1" / "evidence-ledger.jsonl"
        )

    return ArtifactDiscovery(
        manifest_path=manifest_path,
        manifest=manifest,
        evidence_paths=evidence_paths,
        lineage_paths=_structured_files_only(lineage_candidates),
        review_paths=_structured_files_only(review_candidates),
        warnings=tuple(warnings),
    )


def _evidence_primary_classification(raw: Mapping[str, Any]) -> tuple[bool | None, str | None]:
    explicit = _nested_get(
        raw,
        ("is_primary",),
        ("primary_source",),
        ("source", "is_primary"),
        ("source", "primary"),
    )
    explicit_bool = _as_bool(explicit)

    source_type_value = _nested_get(
        raw,
        ("source_type",),
        ("source", "source_type"),
        ("source", "type"),
        ("classification", "source_type"),
    )
    source_type = _as_string(source_type_value)
    if explicit_bool is not None:
        return explicit_bool, source_type

    tier = _nested_get(raw, ("source_tier",), ("source", "tier"))
    if isinstance(tier, (int, float)) and not isinstance(tier, bool):
        if int(tier) == 1:
            return True, source_type
        if int(tier) > 1:
            return False, source_type

    if source_type is None:
        return None, None
    normalised = _normalise_key(source_type)
    if normalised in _PRIMARY_SOURCE_TYPES:
        return True, source_type
    if normalised in {
        "secondary",
        "secondary_source",
        "news",
        "trade_press",
        "analysis",
        "consultant_report",
        "literature_review",
    }:
        return False, source_type
    return None, source_type


def load_evidence(paths: Iterable[Path]) -> tuple[tuple[EvidenceRecord, ...], tuple[str, ...]]:
    evidence: list[EvidenceRecord] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    for path in paths:
        loaded = read_records(
            path,
            container_keys=("evidence", "records", "items", "ledger"),
        )
        warnings.extend(loaded.warnings)
        for index, raw in enumerate(loaded.records, 1):
            evidence_id = _as_string(
                _nested_get(raw, ("evidence_id",), ("id",), ("record_id",))
            )
            if evidence_id is None:
                evidence_id = f"{path.name}#{index}"
                warnings.append(
                    f"`{path.name}` record {index} has no evidence ID; assigned "
                    f"`{evidence_id}` for counting only"
                )
            if evidence_id in seen_ids:
                warnings.append(
                    f"Duplicate evidence ID `{evidence_id}`; later record ignored"
                )
                continue
            seen_ids.add(evidence_id)
            agent_id = _as_string(
                _nested_get(
                    raw,
                    ("agent_id",),
                    ("agent",),
                    ("agent_name",),
                    ("researcher",),
                    ("produced_by",),
                    ("provenance", "agent_id"),
                    ("provenance", "agent"),
                )
            )
            is_primary, source_type = _evidence_primary_classification(raw)
            evidence.append(
                EvidenceRecord(
                    evidence_id=evidence_id,
                    agent_id=agent_id,
                    is_primary=is_primary,
                    source_type=source_type,
                    source_path=path,
                    raw=raw,
                )
            )
    return tuple(evidence), tuple(warnings)


def _extract_reference_ids(value: Any) -> list[str]:
    refs: list[str] = []
    if isinstance(value, str):
        if value.strip():
            refs.append(value.strip())
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        refs.append(str(value))
    elif isinstance(value, Mapping):
        ref = _as_string(
            _nested_get(value, ("evidence_id",), ("source_id",), ("id",), ("ref",))
        )
        if ref is not None:
            refs.append(ref)
    elif isinstance(value, list):
        for item in value:
            refs.extend(_extract_reference_ids(item))
    return refs


def _normalise_verification_status(raw: Mapping[str, Any]) -> str:
    value = _as_string(
        _nested_get(
            raw,
            ("verification_status",),
            ("fact_check_status",),
            ("status",),
            ("outcome",),
            ("verification", "status"),
        )
    )
    normalised = _normalise_key(value or "")
    if normalised in _VERIFIED_STATUSES:
        return "verified"
    if normalised in _REMOVED_STATUSES:
        return "removed"
    if normalised in _UNVERIFIED_STATUSES:
        return "unverified"
    if normalised in _QUALIFIED_STATUSES:
        return "qualified"
    if normalised in _CORRECTED_STATUSES:
        return "corrected"
    return "unknown"


def _record_was_corrected(raw: Mapping[str, Any], status: str) -> bool:
    explicit = _nested_get(
        raw,
        ("corrected",),
        ("was_corrected",),
        ("changed",),
        ("verification", "corrected"),
    )
    explicit_bool = _as_bool(explicit)
    if explicit_bool is not None:
        return explicit_bool
    action = _as_string(
        _nested_get(raw, ("action",), ("disposition",), ("verification", "action"))
    )
    if _normalise_key(action or "") in _CORRECTED_STATUSES:
        return True
    return status == "corrected"


def load_claim_lineage(
    paths: Iterable[Path],
) -> tuple[tuple[ClaimRecord, ...], tuple[str, ...]]:
    claims: list[ClaimRecord] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()
    for path in paths:
        loaded = read_records(
            path,
            container_keys=("claims", "lineage", "records", "items"),
        )
        warnings.extend(loaded.warnings)
        for index, raw in enumerate(loaded.records, 1):
            claim_id = _as_string(
                _nested_get(raw, ("claim_id",), ("id",), ("record_id",))
            )
            if claim_id is None:
                claim_id = f"{path.name}#{index}"
                warnings.append(
                    f"`{path.name}` record {index} has no claim ID; assigned "
                    f"`{claim_id}` for counting only"
                )
            if claim_id in seen_ids:
                warnings.append(
                    f"Duplicate claim ID `{claim_id}`; later record ignored"
                )
                continue
            seen_ids.add(claim_id)
            reference_value = _nested_get(
                raw,
                ("evidence_ids",),
                ("evidence_refs",),
                ("source_ids",),
                ("evidence",),
                ("sources",),
                ("citations",),
                ("provenance", "evidence_ids"),
            )
            evidence_ids = tuple(dict.fromkeys(_extract_reference_ids(reference_value)))
            status = _normalise_verification_status(raw)
            primary_source_checked = _as_bool(
                _nested_get(
                    raw,
                    ("primary_source_checked",),
                    ("verification", "primary_source_checked"),
                )
            )
            claims.append(
                ClaimRecord(
                    claim_id=claim_id,
                    evidence_ids=evidence_ids,
                    verification_status=status,
                    primary_source_checked=primary_source_checked,
                    corrected=_record_was_corrected(raw, status),
                    source_path=path,
                    raw=raw,
                )
            )
    return tuple(claims), tuple(warnings)


def _parse_rubric_score(
    dimension: str,
    value: Any,
    *,
    default_scale_min: float,
    default_scale_max: float,
) -> RubricScore | None:
    notes: str | None = None
    scale_min = default_scale_min
    scale_max = default_scale_max
    score_value = value
    if isinstance(value, Mapping):
        score_value = value.get("score", value.get("value"))
        scale_min = _as_float(value.get("scale_min", value.get("min"))) or scale_min
        scale_max = _as_float(value.get("scale_max", value.get("max"))) or scale_max
        notes = _as_string(value.get("notes", value.get("comment")))
    score = _as_float(score_value)
    if score is None or scale_max <= scale_min or not (scale_min <= score <= scale_max):
        return None
    return RubricScore(
        dimension=dimension,
        score=score,
        scale_min=scale_min,
        scale_max=scale_max,
        notes=notes,
    )


def load_quality_reviews(
    paths: Iterable[Path],
) -> tuple[tuple[QualityReview, ...], tuple[str, ...]]:
    reviews: list[QualityReview] = []
    warnings: list[str] = []
    for path in paths:
        loaded = read_records(
            path,
            container_keys=("reviews", "records", "items"),
        )
        warnings.extend(loaded.warnings)
        for index, raw in enumerate(loaded.records, 1):
            review_id = _as_string(
                _nested_get(raw, ("review_id",), ("id",), ("record_id",))
            ) or f"{path.stem}#{index}"
            reviewer_type = _as_string(
                _nested_get(
                    raw,
                    ("reviewer_type",),
                    ("reviewer", "type"),
                    ("reviewer", "kind"),
                )
            )
            if reviewer_type is None and "human" in _normalise_key(path.name):
                reviewer_type = "human"
            reviewer_type = reviewer_type or "unknown"
            reviewer_name = _as_string(
                _nested_get(raw, ("reviewer_name",), ("reviewer", "name"))
            )
            reviewed_at = _as_string(
                _nested_get(raw, ("reviewed_at",), ("created_at",), ("timestamp",))
            )
            rubric_value = _nested_get(
                raw,
                ("rubric",),
                ("scores",),
                ("quality_scores",),
                ("review", "rubric"),
            )
            rubric: dict[str, RubricScore] = {}
            default_min = _as_float(raw.get("scale_min")) or 1.0
            default_max = _as_float(raw.get("scale_max")) or 5.0
            if isinstance(rubric_value, Mapping):
                for key, value in rubric_value.items():
                    dimension = _RUBRIC_ALIASES.get(_normalise_key(key))
                    if dimension is None:
                        continue
                    parsed = _parse_rubric_score(
                        dimension,
                        value,
                        default_scale_min=default_min,
                        default_scale_max=default_max,
                    )
                    if parsed is not None:
                        rubric[dimension] = parsed
                    else:
                        warnings.append(
                            f"`{path.name}` review `{review_id}` has an invalid "
                            f"score for `{dimension}`"
                        )
            if not rubric:
                warnings.append(
                    f"`{path.name}` review `{review_id}` contains no valid rubric scores"
                )
            reviews.append(
                QualityReview(
                    review_id=review_id,
                    reviewer_type=reviewer_type,
                    reviewer_name=reviewer_name,
                    reviewed_at=reviewed_at,
                    rubric=rubric,
                    notes=_as_string(raw.get("notes", raw.get("comments"))),
                    source_path=path,
                )
            )
    return tuple(reviews), tuple(warnings)


def manifest_agents(manifest: Mapping[str, Any] | None) -> list[str]:
    if manifest is None:
        return []
    value = _nested_get(
        manifest,
        ("selected_agents",),
        ("seated_agents",),
        ("research_agents",),
        ("selected_research_agents",),
        ("run", "selected_agents"),
        ("run", "agents"),
    )
    if value is None and isinstance(manifest.get("agents"), list):
        value = manifest["agents"]
    names: list[str] = []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item.strip():
                names.append(item.strip())
            elif isinstance(item, Mapping):
                name = _as_string(
                    _nested_get(item, ("agent_id",), ("name",), ("id",))
                )
                role = _normalise_key(item.get("role", item.get("type", "research")))
                if name and role not in {
                    "strategist",
                    "editor",
                    "fact_checker",
                    "humanizer",
                    "red_team",
                    "presentation_designer",
                    "process",
                }:
                    names.append(name)
    return list(dict.fromkeys(names))


def manifest_cost_total(manifest: Mapping[str, Any] | None) -> float | None:
    if manifest is None:
        return None
    value = _nested_get(
        manifest,
        ("cost_total_usd",),
        ("total_cost_usd",),
        ("cost_usd",),
        ("cost", "total_usd"),
        ("cost", "total"),
        ("run", "cost_total_usd"),
        ("telemetry", "cost_total_usd"),
    )
    parsed = _as_float(value)
    return parsed if parsed is not None and parsed >= 0 else None


def manifest_stage_statuses(
    manifest: Mapping[str, Any] | None,
) -> dict[str, str]:
    if manifest is None:
        return {}
    value = _nested_get(
        manifest,
        ("stages",),
        ("stage_completion",),
        ("run", "stages"),
    )
    statuses_by_stage: dict[str, list[str]] = {}
    if isinstance(value, Mapping):
        items = value.items()
    elif isinstance(value, list):
        items = []
        for item in value:
            if isinstance(item, Mapping):
                name = _as_string(
                    _nested_get(item, ("stage_id",), ("name",), ("id",), ("stage",))
                )
                if name:
                    items.append((name, item))
    else:
        items = []

    stage_aliases = {
        "context": "stage1",
        "research": "stage1",
        "evidence": "stage1",
        "synthesis": "stage2",
        "critique": "stage2",
        "polish": "stage3",
        "verification": "stage3",
        "fact_check": "stage3",
        "factcheck": "stage3",
        "production": "stage4",
        "publishing": "stage4",
        "publication": "stage4",
    }
    for raw_name, raw_status in items:
        normalised_name = _normalise_key(raw_name)
        match = re.search(r"(?:stage_?)?([1-4])", normalised_name)
        if match is not None:
            stage_name = f"stage{match.group(1)}"
        else:
            stage_name = stage_aliases.get(normalised_name)
        if stage_name is None:
            continue
        if isinstance(raw_status, Mapping):
            status_value = _as_string(
                _nested_get(
                    raw_status,
                    ("status",),
                    ("state",),
                    ("completion_status",),
                )
            )
            if status_value is None:
                complete = _as_bool(raw_status.get("completed"))
                status_value = "complete" if complete else None
        else:
            status_value = _as_string(raw_status)
            if isinstance(raw_status, bool):
                status_value = "complete" if raw_status else "not_complete"
        status = _normalise_key(status_value or "")
        if status in {"complete", "completed", "done", "success", "succeeded", "passed"}:
            normalised_status = "complete"
        elif status in {"running", "in_progress", "active", "started"}:
            normalised_status = "in_progress"
        elif status in {"failed", "error", "blocked", "cancelled", "canceled"}:
            normalised_status = status
        elif status in {"not_started", "not_complete", "pending", "skipped"}:
            normalised_status = status
        elif status:
            normalised_status = "unknown"
        else:
            continue
        statuses_by_stage.setdefault(stage_name, []).append(normalised_status)

    # When a manifest has not yet recorded coarse stage states, use its
    # required artifact contracts. This remains stronger than filesystem
    # presence because each artifact status comes from contract validation.
    artifacts = manifest.get("artifacts")
    if isinstance(artifacts, list):
        for item in artifacts:
            if not isinstance(item, Mapping) or item.get("required") is False:
                continue
            manifest_stage = _normalise_key(item.get("stage", ""))
            stage_name = stage_aliases.get(manifest_stage)
            if stage_name is None:
                match = re.search(r"(?:stage_?)?([1-4])", manifest_stage)
                stage_name = f"stage{match.group(1)}" if match else None
            if stage_name is None:
                continue
            artifact_status = _normalise_key(item.get("status", "pending"))
            if artifact_status in {
                "complete",
                "completed",
                "done",
                "success",
                "succeeded",
                "passed",
            }:
                normalised_status = "complete"
            elif artifact_status in {"invalid", "failed", "error", "blocked"}:
                normalised_status = "failed"
            elif artifact_status in {"running", "in_progress", "active", "started"}:
                normalised_status = "in_progress"
            elif artifact_status in {"pending", "not_started", "not_complete"}:
                normalised_status = "pending"
            else:
                normalised_status = "unknown"
            statuses_by_stage.setdefault(stage_name, []).append(normalised_status)

    severity = {
        "failed": 6,
        "error": 6,
        "blocked": 6,
        "in_progress": 5,
        "running": 5,
        "pending": 4,
        "not_started": 4,
        "not_complete": 4,
        "unknown": 3,
        "skipped": 2,
        "cancelled": 2,
        "canceled": 2,
        "complete": 1,
    }
    return {
        stage: max(stage_statuses, key=lambda item: severity.get(item, 3))
        for stage, stage_statuses in statuses_by_stage.items()
        if stage_statuses
    }


def write_human_review(
    run_dir: Path,
    scores: Mapping[str, float],
    *,
    reviewer_name: str | None = None,
    notes: str | None = None,
    review_id: str | None = None,
    reviewed_at: str | None = None,
) -> Path:
    """Write a canonical machine-readable human review.

    Scores use a 1–5 scale.  Partial reviews are allowed, but every supplied
    dimension must be one of :data:`RUBRIC_DIMENSIONS`.
    """
    unknown = sorted(set(scores) - set(RUBRIC_DIMENSIONS))
    if unknown:
        raise ValueError(f"Unknown rubric dimension(s): {', '.join(unknown)}")
    if not scores:
        raise ValueError("At least one rubric score is required")
    for dimension, score in scores.items():
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"`{dimension}` must be numeric")
        if not 1 <= float(score) <= 5:
            raise ValueError(f"`{dimension}` must be between 1 and 5")

    timestamp = reviewed_at or datetime.now(timezone.utc).isoformat()
    safe_timestamp = re.sub(r"[^0-9A-Za-z]+", "-", timestamp).strip("-")
    identifier = review_id or f"human-{safe_timestamp}"
    safe_identifier = re.sub(r"[^0-9A-Za-z._-]+", "-", identifier).strip("-")
    if not safe_identifier:
        raise ValueError("review_id must contain at least one safe filename character")
    review_dir = run_dir / "evaluation" / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    path = review_dir / f"{safe_identifier}.json"
    payload = {
        "schema_version": "1.0",
        "review_id": identifier,
        "reviewer": {
            "type": "human",
            **({"name": reviewer_name} if reviewer_name else {}),
        },
        "reviewed_at": timestamp,
        "rubric": {
            dimension: {
                "score": float(score),
                "scale_min": 1,
                "scale_max": 5,
            }
            for dimension, score in scores.items()
        },
        **({"notes": notes} if notes else {}),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def record_quality_review(
    outputs_dir: Path,
    checkpoint: str,
    ratings: dict[str, int],
    notes: str = "",
    approved: bool = True,
) -> Path:
    """Persist the five-dimension checkpoint rubric for later evaluation.

    This intentionally small interface is suitable for both the terminal and
    web checkpoint handlers. ``outputs_dir`` may be the live ``outputs/``
    directory or an archived run root. The archive workflow should preserve
    its ``evaluation/`` child alongside the stage directories.
    """
    missing = sorted(set(RUBRIC_DIMENSIONS) - set(ratings))
    extra = sorted(set(ratings) - set(RUBRIC_DIMENSIONS))
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unknown: {', '.join(extra)}")
        raise ValueError(
            "Quality review requires exactly the five rubric dimensions "
            f"({'; '.join(details)})"
        )
    if not isinstance(approved, bool):
        raise ValueError("approved must be a boolean")
    if not isinstance(checkpoint, str) or not checkpoint.strip():
        raise ValueError("checkpoint is required")

    timestamp = datetime.now(timezone.utc).isoformat()
    checkpoint_key = _normalise_key(checkpoint)
    review_id = f"human-{checkpoint_key}-{timestamp}"
    path = write_human_review(
        outputs_dir,
        ratings,
        notes=notes or None,
        review_id=review_id,
        reviewed_at=timestamp,
    )
    payload, warning = _read_json(path)
    if warning or not isinstance(payload, dict):
        raise OSError(warning or f"Could not update review record `{path}`")
    payload["checkpoint"] = checkpoint
    payload["approved"] = approved
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path
