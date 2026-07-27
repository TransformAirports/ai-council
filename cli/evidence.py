"""Structured evidence and claim-lineage support for Council runs.

Research agents are asked to emit companion JSONL records, but older agents and
archived runs only contain inline ``[Source: ...]`` tags.  The builder accepts
both formats and records which path supplied each item, allowing Council v2 to
adopt structured provenance without making resume or legacy research brittle.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from cli.claim_text import marker_claim_contexts


SOURCE_TAG_RE = re.compile(r"\[Source:\s*(.+?)\]", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s)\]}>]+")
FOOTNOTE_MARKER_RE = re.compile(r"\[\^([^\]]+)\]")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.+)$", re.MULTILINE)


@dataclass
class LedgerBuildResult:
    records: list[dict[str, Any]]
    structured_records: int = 0
    legacy_records: int = 0
    invalid_records: list[str] = field(default_factory=list)
    agents_without_evidence: list[str] = field(default_factory=list)

    @property
    def record_count(self) -> int:
        return len(self.records)


def _as_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    values = value if isinstance(value, (list, tuple, set)) else [value]
    return [str(item).strip() for item in values if str(item).strip()]


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def _stable_evidence_id(agent: str, claim: str, source: str) -> str:
    digest = hashlib.sha256(
        f"{agent}\0{claim.strip()}\0{source.strip()}".encode("utf-8")
    ).hexdigest()[:12]
    # Canonical IDs are born namespaced.  This makes normalization idempotent:
    # a ledger record can pass through the curation and verification stages
    # repeatedly without changing the identifier that narrative artifacts cite.
    return f"{agent}::ev-{digest}"


def file_sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.is_file():
        return records, errors
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return [], [f"{path.name}: cannot read: {exc}"]
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}:{number}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path.name}:{number}: record is not an object")
            continue
        records.append(value)
    return records, errors


def _normalise_record(
    raw: dict[str, Any], *, agent: str, ordinal: int
) -> tuple[dict[str, Any] | None, str | None]:
    claim = str(
        raw.get("claim")
        or raw.get("finding")
        or raw.get("assertion")
        or raw.get("summary")
        or ""
    ).strip()
    source_url = str(raw.get("source_url") or raw.get("url") or "").strip()
    source_path = str(raw.get("source_path") or "").strip()
    source = str(
        raw.get("source")
        or raw.get("source_title")
        or raw.get("citation")
        or source_url
        or source_path
        or ""
    ).strip()
    if not claim:
        return None, f"record {ordinal} has no claim"
    if not source:
        return None, f"record {ordinal} has no source or URL"

    confidence_raw = raw.get("confidence", "medium")
    if isinstance(confidence_raw, (int, float)):
        confidence: str | float = max(0.0, min(1.0, float(confidence_raw)))
    else:
        confidence = str(confidence_raw).strip().lower() or "medium"

    source_type = str(raw.get("source_type") or "unspecified").strip()
    primary_raw = raw.get("is_primary")
    if isinstance(primary_raw, bool):
        is_primary: bool | None = primary_raw
    elif primary_raw is not None:
        is_primary = str(primary_raw).strip().lower() in {"1", "true", "yes"}
    else:
        source_type_low = source_type.lower()
        primary_markers = (
            "primary",
            "regulation",
            "statute",
            "official",
            "dataset",
            "audited",
            "airport report",
            "airport document",
            "airport_document",
            "government report",
            "financial statement",
        )
        is_primary = (
            True
            if any(marker in source_type_low for marker in primary_markers)
            else None
        )

    evidence_id = str(raw.get("evidence_id") or raw.get("id") or "").strip()
    if not evidence_id:
        evidence_id = _stable_evidence_id(agent, claim, source)
    elif "::" not in evidence_id:
        # Individual agents commonly start at E-0001. Namespace agent-emitted
        # IDs before aggregation so one agent's record can never overwrite
        # another's in evaluation or claim lineage.
        evidence_id = f"{agent}::{evidence_id}"
    return (
        {
            "evidence_id": evidence_id,
            "claim": claim,
            "source": source,
            "source_title": str(raw.get("source_title") or source).strip(),
            "source_url": source_url or None,
            "source_path": source_path or None,
            "source_type": source_type,
            "is_primary": is_primary,
            "locator": str(
                raw.get("locator")
                or raw.get("page")
                or raw.get("section")
                or raw.get("page_or_section")
                or ""
            ).strip()
            or None,
            "quote": str(
                raw.get("quote")
                or raw.get("excerpt")
                or raw.get("supporting_excerpt")
                or ""
            ).strip()
            or None,
            "airport": str(
                raw.get("airport") or raw.get("airport_or_entity") or ""
            ).strip()
            or None,
            "date": str(
                raw.get("date")
                or raw.get("source_date")
                or raw.get("data_vintage")
                or raw.get("year")
                or ""
            ).strip()
            or None,
            "data_vintage": str(raw.get("data_vintage") or "").strip() or None,
            "units": str(raw.get("units") or "").strip() or None,
            "denominator": str(raw.get("denominator") or "").strip() or None,
            "caveat": str(raw.get("caveat") or raw.get("limitations") or "").strip()
            or None,
            "confidence": confidence,
            "agent_id": str(
                raw.get("agent_id") or raw.get("agent") or agent
            ).strip(),
            "discovered_by": list(
                dict.fromkeys(
                    [
                        str(raw.get("agent_id") or raw.get("agent") or agent).strip(),
                        *_as_string_list(raw.get("discovered_by")),
                    ]
                )
            ),
            "corroborated_by": _as_string_list(raw.get("corroborated_by")),
            "contradicted_by": _as_string_list(raw.get("contradicted_by")),
            "status": str(raw.get("status") or "usable").strip(),
            "provenance_mode": str(
                raw.get("provenance_mode") or "structured"
            ).strip(),
        },
        None,
    )


def _claim_before(text: str, position: int) -> str:
    """Return the nearest useful sentence or line before a source marker."""

    prefix = text[:position].rstrip()
    if not prefix:
        return ""
    paragraph = re.split(r"\n\s*\n", prefix)[-1]
    line = paragraph.splitlines()[-1].strip()
    line = re.sub(r"^[#>*\-\d.\s]+", "", line)
    if len(line) < 20:
        sentences = re.split(r"(?<=[.!?])\s+", paragraph.strip())
        line = sentences[-1].strip() if sentences else line
    return line[:1200]


def _legacy_records(brief_path: Path, *, agent: str) -> list[dict[str, Any]]:
    if not brief_path.is_file():
        return []
    try:
        text = brief_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    records: list[dict[str, Any]] = []
    for ordinal, match in enumerate(SOURCE_TAG_RE.finditer(text), start=1):
        source = match.group(1).strip()
        claim = _claim_before(text, match.start())
        if not claim:
            claim = f"Evidence item recorded in {brief_path.name}"
        urls = URL_RE.findall(source)
        record, _ = _normalise_record(
            {
                "claim": claim,
                "source": source,
                "source_url": urls[0] if urls else "",
                "source_type": "unspecified",
                "confidence": "unrated",
                "provenance_mode": "legacy-source-tag",
            },
            agent=agent,
            ordinal=ordinal,
        )
        if record:
            records.append(record)
    return records


def _deduplicate(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for record in records:
        key = (
            re.sub(r"\s+", " ", str(record.get("claim", "")).lower()).strip(),
            re.sub(
                r"\s+",
                " ",
                str(record.get("source_url") or record.get("source") or "")
                .lower(),
            ).strip(),
        )
        existing = by_key.get(key)
        if existing is None:
            by_key[key] = record
            continue
        discovered = existing.setdefault("discovered_by", [])
        for name in record.get("discovered_by", []):
            if name not in discovered:
                discovered.append(name)
    return list(by_key.values())


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    _atomic_write_text(path, "\n".join(lines) + ("\n" if lines else ""))


def build_evidence_ledger(
    *,
    selected_agents: Iterable[str],
    stage1_dir: Path,
    output_path: Path,
    compatibility_path: Path | None = None,
) -> LedgerBuildResult:
    """Merge structured agent evidence and legacy source tags into one ledger."""

    result = LedgerBuildResult(records=[])
    collected: list[dict[str, Any]] = []
    for agent in selected_agents:
        evidence_path = stage1_dir / f"{agent}-evidence.jsonl"
        structured, errors = _read_jsonl(evidence_path)
        result.invalid_records.extend(errors)
        accepted = 0
        for ordinal, raw in enumerate(structured, start=1):
            record, error = _normalise_record(raw, agent=agent, ordinal=ordinal)
            if error:
                result.invalid_records.append(f"{evidence_path.name}: {error}")
                continue
            assert record is not None
            collected.append(record)
            accepted += 1
            result.structured_records += 1

        # Structured records are authoritative for that agent. Fall back only
        # when the companion file is absent or yielded no usable records.
        if accepted == 0:
            legacy = _legacy_records(stage1_dir / f"{agent}-brief.md", agent=agent)
            collected.extend(legacy)
            result.legacy_records += len(legacy)
            if not legacy:
                result.agents_without_evidence.append(agent)

    result.records = _deduplicate(collected)
    write_jsonl(output_path, result.records)
    if compatibility_path is not None:
        write_jsonl(compatibility_path, result.records)
    return result


def normalise_evidence_ledger(path: Path) -> LedgerBuildResult:
    """Normalize an Evidence Curator-written ledger in place."""

    raw_records, errors = _read_jsonl(path)
    result = LedgerBuildResult(records=[], invalid_records=list(errors))
    normalized: list[dict[str, Any]] = []
    for ordinal, raw in enumerate(raw_records, start=1):
        agent = str(raw.get("agent_id") or raw.get("agent") or "evidence-curator")
        record, error = _normalise_record(raw, agent=agent, ordinal=ordinal)
        if error:
            result.invalid_records.append(f"{path.name}: {error}")
            continue
        assert record is not None
        normalized.append(record)
        if str(record.get("provenance_mode", "")).startswith("legacy"):
            result.legacy_records += 1
        else:
            result.structured_records += 1
    result.records = _deduplicate(normalized)
    write_jsonl(path, result.records)
    return result


def _footnote_claim(body: str, marker_start: int) -> str:
    prefix = body[:marker_start].rstrip()
    paragraph = re.split(r"\n\s*\n", prefix)[-1]
    sentences = re.split(r"(?<=[.!?])\s+", paragraph)
    claim = sentences[-1] if sentences else paragraph
    return re.sub(r"\s+", " ", claim).strip()[-1500:]


def _match_evidence(
    citation: str, ledger: list[dict[str, Any]]
) -> list[str]:
    citation_urls = {url.rstrip(".,;") for url in URL_RE.findall(citation)}
    matches: list[str] = []
    citation_low = citation.lower()
    for record in ledger:
        source_url = str(record.get("source_url") or "").rstrip(".,;")
        source = str(record.get("source") or "").strip()
        if source_url and source_url in citation_urls:
            matches.append(str(record.get("evidence_id")))
        elif source and len(source) >= 18 and source.lower() in citation_low:
            matches.append(str(record.get("evidence_id")))
    return list(dict.fromkeys(matches))


def ensure_claim_lineage(
    *,
    final_draft: Path,
    evidence_ledger: Path,
    output_path: Path,
) -> tuple[list[dict[str, Any]], bool]:
    """Preserve valid agent-written lineage or derive a conservative fallback.

    Returns ``(records, generated)``.  Fallback records deliberately distinguish
    a source match from primary-source verification; the latter remains the
    Fact-checker's responsibility.
    """

    existing, errors = _read_jsonl(output_path)
    required = {
        "claim_id",
        "claim",
        "citation",
        "footnote_id",
        "evidence_ids",
        "verification_status",
        "primary_source_checked",
        "retained",
    }
    allowed_statuses = {
        "verified",
        "qualified",
        "corrected",
        "removed",
        "unverified",
    }
    existing_is_canonical = bool(existing) and not errors and all(
        required.issubset(record)
        and record.get("verification_status") in allowed_statuses
        and isinstance(record.get("evidence_ids"), list)
        and isinstance(record.get("primary_source_checked"), bool)
        for record in existing
    )
    if existing_is_canonical:
        return existing, False

    ledger, ledger_errors = _read_jsonl(evidence_ledger)
    if ledger_errors:
        ledger = []
    try:
        text = final_draft.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        write_jsonl(output_path, [])
        return [], True

    definitions = {key: value for key, value in FOOTNOTE_DEF_RE.findall(text)}
    body = FOOTNOTE_DEF_RE.sub("", text)
    seen: set[str] = set()
    lineage: list[dict[str, Any]] = []
    for marker in FOOTNOTE_MARKER_RE.finditer(body):
        label = marker.group(1)
        if label in seen:
            continue
        seen.add(label)
        citation = definitions.get(label, "")
        evidence_ids = _match_evidence(citation, ledger)
        lineage.append(
            {
                "claim_id": f"claim-{len(lineage) + 1:04d}",
                "claim": _footnote_claim(body, marker.start()),
                "footnote_id": label,
                "citation": citation,
                "evidence_ids": evidence_ids,
                "verification_status": "unverified",
                "primary_source_checked": False,
                "retained": True,
                "verification_note": (
                    "Deterministic fallback matched the citation to the evidence "
                    "ledger but did not open the primary source."
                    if evidence_ids
                    else "Deterministic fallback could not match the citation to "
                    "the evidence ledger or open the primary source."
                ),
                "match_status": (
                    "matched_to_evidence_ledger"
                    if evidence_ids
                    else "cited_not_matched_to_ledger"
                ),
                "lineage_mode": "deterministic-footnote-fallback",
            }
        )
    write_jsonl(output_path, lineage)
    return lineage, True


def bind_claim_lineage_to_draft(
    *, final_draft: Path, output_path: Path
) -> list[dict[str, Any]]:
    """Bind lineage only when retained claims and citations match the draft."""

    records, errors = _read_jsonl(output_path)
    draft_hash = file_sha256(final_draft)
    if errors or not records or not draft_hash:
        return records
    text = final_draft.read_text(encoding="utf-8", errors="replace")
    definitions = {key: value for key, value in FOOTNOTE_DEF_RE.findall(text)}
    body = FOOTNOTE_DEF_RE.sub("", text)

    def normalise(value: object) -> str:
        candidate = unicodedata.normalize("NFKC", str(value or ""))
        candidate = FOOTNOTE_MARKER_RE.sub("", candidate)
        candidate = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", candidate)
        candidate = re.sub(r"[`*_>#|~]", " ", candidate)
        candidate = re.sub(r"[^\w$%]+", " ", candidate, flags=re.UNICODE)
        return re.sub(r"\s+", " ", candidate).strip().casefold()

    body_identity = normalise(body)
    marker_contexts = {
        label: [
            context_identity
            for context in contexts
            if (context_identity := normalise(context))
        ]
        for label, contexts in marker_claim_contexts(body).items()
    }
    for record in records:
        record.pop("draft_sha256", None)
        status = str(record.get("verification_status") or "")
        retained = record.get(
            "retained",
            status not in {"removed", "unverified"},
        )
        if retained:
            claim = normalise(record.get("claim"))
            footnote_id = str(
                record.get("footnote_id") or record.get("footnote") or ""
            ).strip()
            citation = definitions.get(footnote_id)
            if (
                not claim
                or claim not in body_identity
                or not any(
                    claim in context
                    for context in marker_contexts.get(footnote_id, [])
                )
                or citation is None
                or normalise(record.get("citation")) != normalise(citation)
            ):
                continue
        record["draft_sha256"] = draft_hash
    write_jsonl(output_path, records)
    return records
