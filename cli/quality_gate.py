"""Deterministic publication gate for final Council drafts."""
from __future__ import annotations

import json
import os
import re
import hashlib
import unicodedata
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from cli.artifacts import validate_artifact
from cli.claim_text import marker_claim_contexts, split_claim_units


FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.+)$", re.MULTILINE)
FOOTNOTE_BLOCK_RE = re.compile(
    r"^\[\^[^\]]+\]:[^\n]*(?:\n[ \t]{2,}[^\n]*)*",
    re.MULTILINE,
)
FOOTNOTE_MARKER_RE = re.compile(r"\[\^([^\]]+)\]")
URL_RE = re.compile(r"https?://[^\s)\]}>]+", re.IGNORECASE)
NUMERIC_CLAIM_RE = re.compile(
    r"(?:"
    r"\$\s?\d[\d,.]*"
    r"|\b\d+(?:\.\d+)?\s?%"
    r"|\b\d+(?:\.\d+)?\s+(?i:percent|percentage\s+points?)\b"
    r"|\b\d+(?:\.\d+)?\s*:\s*\d+(?:\.\d+)?\b"
    r"|\b(?:19|20)\d{2}\b"
    r"|\b\d+(?:\.\d+)?\s?(?i:"
    r"thousand|million|billion|trillion|"
    r"passengers?|gates?|flights?|operations?|bags?|aircraft|"
    r"seconds?|minutes?|hours?|days?|weeks?|months?|years?|"
    r"lanes?|checkpoints?|positions?|employees?|fte|acres?|"
    r"square\s+feet|sq\.?\s*ft\.?|feet|meters?|miles?|"
    r"megawatts?|mw|mwh|tons?|basis\s+points?"
    r")\b"
    r"|\b\d+(?:\.\d+)?\s?[x×]\b"
    r")"
)
ATTRIBUTED_CLAIM_RE = re.compile(
    r"\b(?:according to|reported|reports|stated|states|found|finds|"
    r"estimated|estimates|projected|projects|forecast|forecasts|said|says)\b",
    re.IGNORECASE,
)
SUPPORT_STOPWORDS = {
    "about",
    "after",
    "again",
    "against",
    "airport",
    "because",
    "before",
    "between",
    "could",
    "from",
    "have",
    "into",
    "million",
    "more",
    "should",
    "than",
    "that",
    "their",
    "there",
    "these",
    "they",
    "this",
    "through",
    "were",
    "will",
    "with",
    "would",
}
DEFAULT_WORD_COUNT_BOUNDS: dict[str, tuple[int, int]] = {
    "report": (4_000, 6_000),
    "article": (1_500, 2_000),
    "brief": (700, 1_000),
    "recommendations": (400, 700),
}
EXECUTIVE_MEMO_HEADINGS: tuple[str, ...] = (
    "bottom line",
    "why it holds",
    "strongest objection",
    "what to do now",
)
ACADEMIC_MEMO_PHRASES: dict[str, str] = {
    "this paper": r"\bthis paper\b",
    "this report": r"\bthis report\b",
    "the literature": r"\bthe literature\b",
    "it is important to note": r"\bit is important to note\b",
    "in conclusion": r"\bin conclusion\b",
    "a review of": r"\ba review of\b",
}
WORD_COUNT_RANGE_RE = re.compile(
    r"(?<!\d)(\d[\d,]*)\s*[–—-]\s*(\d[\d,]*)"
    r"\s*(?:-\s*)?words?\b",
    re.IGNORECASE,
)
WORD_COUNT_SINGLE_RE = re.compile(
    r"(?P<approx>~|about\s+|approximately\s+|approx\.?\s+)?"
    r"(?<!\d)(?P<count>\d[\d,]*)\s*(?:-\s*)?words?\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class QualityIssue:
    severity: str
    code: str
    message: str
    count: int = 1


class PublicationQualityError(RuntimeError):
    """Raised when the final draft contains a deterministic release blocker."""

    def __init__(self, report_path: Path, issues: Iterable[QualityIssue]):
        errors = [issue for issue in issues if issue.severity == "error"]
        summary = "; ".join(issue.message for issue in errors[:5])
        super().__init__(
            f"Publication quality gate failed ({len(errors)} blocker(s)): {summary}. "
            f"See {report_path}."
        )
        self.report_path = report_path
        self.issues = list(issues)


def resolve_word_count_bounds(
    output_format: str,
    length_instruction: str | None = None,
) -> tuple[int, int]:
    """Resolve the final reader-facing word-count contract.

    A numeric range in the run prompt is authoritative. A single requested
    count receives a deterministic tolerance: ten percent for explicitly
    approximate language and five percent otherwise. Format defaults cover
    legacy run prompts without a parseable numeric instruction.
    """

    instruction = str(length_instruction or "")
    range_match = WORD_COUNT_RANGE_RE.search(instruction)
    if range_match:
        lower = int(range_match.group(1).replace(",", ""))
        upper = int(range_match.group(2).replace(",", ""))
        if 100 <= lower <= upper:
            return lower, upper

    single_match = WORD_COUNT_SINGLE_RE.search(instruction)
    if single_match:
        requested = int(single_match.group("count").replace(",", ""))
        if requested >= 100:
            tolerance = 0.10 if single_match.group("approx") else 0.05
            return (
                max(100, round(requested * (1 - tolerance))),
                round(requested * (1 + tolerance)),
            )

    return DEFAULT_WORD_COUNT_BOUNDS.get(
        str(output_format or "").strip().lower(),
        DEFAULT_WORD_COUNT_BOUNDS["report"],
    )


def publication_word_count(text: str) -> int:
    """Count reader-facing Markdown prose, excluding citation definitions."""

    body = FOOTNOTE_BLOCK_RE.sub("", text)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = FOOTNOTE_MARKER_RE.sub("", body)
    body = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = URL_RE.sub("", body)
    return len(re.findall(r"\b[\w'’.-]+\b", body, flags=re.UNICODE))


def inspect_executive_memo_markdown(text: str) -> list[QualityIssue]:
    """Enforce the short, plain-English shape used by Strengthen an argument.

    This is intentionally a narrow release profile, not a general-purpose
    readability score. It catches the failure modes that make an executive
    memo feel like a compressed academic article: missing decision structure,
    long blocks, long sentence runs, and scholarly throat-clearing.
    """

    issues: list[QualityIssue] = []
    body = FOOTNOTE_BLOCK_RE.sub("", text)
    headings = {
        re.sub(r"\s+", " ", match.group(1)).strip().casefold()
        for match in re.finditer(r"(?m)^##\s+(.+?)\s*$", body)
    }
    missing = [heading for heading in EXECUTIVE_MEMO_HEADINGS if heading not in headings]
    if missing:
        _issue(
            issues,
            severity="error",
            code="memo_structure_missing",
            message="the executive memo is missing required sections: " + ", ".join(missing),
            count=len(missing),
        )

    prose_paragraphs: list[str] = []
    for paragraph in re.split(r"\n\s*\n", body):
        paragraph = paragraph.strip()
        if not paragraph or paragraph.startswith("#"):
            continue
        paragraph_lines = [line for line in paragraph.splitlines() if line.strip()]
        if paragraph_lines and all(
            line.lstrip().startswith(("- ", "* ", "> "))
            for line in paragraph_lines
        ):
            prose_paragraphs.extend(
                re.sub(r"^\s*[-*>]\s+", "", line).strip()
                for line in paragraph_lines
            )
            continue
        prose_paragraphs.append(re.sub(r"\s+", " ", paragraph))
    oversized = [
        paragraph
        for paragraph in prose_paragraphs
        if len(re.findall(r"\b[\w'’.-]+\b", paragraph)) > 90
    ]
    if oversized:
        _issue(
            issues,
            severity="error",
            code="memo_paragraph_too_long",
            message="the executive memo contains prose paragraphs longer than 90 words",
            count=len(oversized),
        )

    sentences = [
        sentence
        for paragraph in prose_paragraphs
        for sentence in split_claim_units(paragraph)
        if sentence.strip()
    ]
    sentence_lengths = [
        len(re.findall(r"\b[\w'’.-]+\b", sentence)) for sentence in sentences
    ]
    if sentence_lengths:
        average = sum(sentence_lengths) / len(sentence_lengths)
        long_count = sum(length > 36 for length in sentence_lengths)
        if average > 26 or long_count > max(1, len(sentence_lengths) // 5):
            _issue(
                issues,
                severity="error",
                code="memo_sentence_density",
                message=(
                    "the executive memo is too syntactically dense "
                    f"(average {average:.1f} words per sentence; "
                    f"{long_count} sentence(s) exceed 36 words)"
                ),
                count=max(long_count, 1),
            )

    for label, pattern in ACADEMIC_MEMO_PHRASES.items():
        count = len(re.findall(pattern, body, re.IGNORECASE))
        if count:
            _issue(
                issues,
                severity="error",
                code="memo_academic_register",
                message=f"replace academic framing phrase '{label}' with direct English",
                count=count,
            )
    return issues


def _issue(
    issues: list[QualityIssue],
    *,
    severity: str,
    code: str,
    message: str,
    count: int = 1,
) -> None:
    issues.append(QualityIssue(severity, code, message, count))


def _normalise_for_identity(value: object) -> str:
    """Normalize Markdown prose for deterministic claim/citation identity."""

    text = unicodedata.normalize("NFKC", str(value or ""))
    text = FOOTNOTE_MARKER_RE.sub("", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"[`*_>#|~]", " ", text)
    text = re.sub(r"[^\w$%]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip().casefold()


def _numeric_claim_segments(body: str) -> list[str]:
    """Return sentence/table-row units that make a material numeric assertion."""

    segments: list[str] = []
    for paragraph in re.split(r"\n\s*\n", body):
        paragraph = paragraph.strip()
        if not paragraph or paragraph.startswith("#"):
            continue
        lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
        if lines and all(line.startswith("|") for line in lines):
            candidates = lines
        else:
            candidates = split_claim_units(paragraph)
        for candidate in candidates:
            candidate = candidate.strip()
            if candidate and NUMERIC_CLAIM_RE.search(candidate):
                segments.append(candidate)
    return segments


def _marker_contexts(body: str) -> dict[str, list[str]]:
    """Map each footnote label to the sentence or table row it actually cites."""

    return {
        label: [
            identity
            for context in raw_contexts
            if (identity := _normalise_for_identity(context))
        ]
        for label, raw_contexts in marker_claim_contexts(body).items()
    }


_SOURCE_TOKEN_STOPWORDS = {
    "and",
    "for",
    "from",
    "into",
    "near",
    "of",
    "on",
    "over",
    "the",
    "to",
    "with",
}


def _source_tokens(value: object) -> set[str]:
    return {
        token
        for token in re.findall(r"\b[\w'-]+\b", _normalise_for_identity(value))
        if token not in _SOURCE_TOKEN_STOPWORDS
        and (len(token) >= 3 or any(character.isdigit() for character in token))
    }


def _source_identifiers(value: object) -> set[str]:
    identity = _normalise_for_identity(value)
    patterns = (
        r"\bpart\s+\d+\b",
        r"\bsection\s+\d+[a-z]?\b",
        r"\b\d+\s+cfr\s+(?:part\s+)?\d+\b",
        r"\b\d+\s+u\s+s\s+c\s+\d+\b",
        r"\b(?:form\s+)?7460\s+1\b",
        r"\b(?:ac\s+)?150\s+\d{4}\s+\d+[a-z]?\b",
    )
    return {
        match.group(0)
        for pattern in patterns
        for match in re.finditer(pattern, identity)
    }


def _evidence_matches_citation(record: dict, citation: str) -> bool:
    """Require a lineage evidence ID to identify the source readers can see."""

    citation_urls = {
        url.rstrip(".,;").casefold() for url in URL_RE.findall(citation)
    }
    source_url = str(record.get("source_url") or "").rstrip(".,;").casefold()
    if source_url and source_url in citation_urls:
        return True

    citation_identity = _normalise_for_identity(citation)
    source_candidates = (
        record.get("source_title"),
        record.get("source"),
        # Paywalled standards carry their full written citation here instead of
        # a URL; it is the only string that identifies them to a reader.
        record.get("source_citation"),
        Path(str(record.get("source_path") or "")).name,
    )
    for candidate in source_candidates:
        source_identity = _normalise_for_identity(candidate)
        if (
            len(source_identity) >= 8
            and (
                source_identity in citation_identity
                or citation_identity in source_identity
            )
        ):
            return True
        for fragment in re.split(r"\s*(?:[;/]|\(|\)|—|--)\s*", str(candidate or "")):
            fragment_identity = _normalise_for_identity(fragment)
            if len(fragment_identity) >= 8 and fragment_identity in citation_identity:
                return True
        source_tokens = _source_tokens(candidate)
        citation_tokens = _source_tokens(citation)
        overlap = source_tokens & citation_tokens
        if source_tokens and (
            len(overlap) >= 3
            and len(overlap) / len(source_tokens) >= 0.50
        ):
            return True
        if _source_identifiers(candidate) & _source_identifiers(citation):
            return True
    return False


def _support_text_supports_claim(support_text: str, claim: str) -> bool:
    support_text = " ".join(
        support_text.split()
    )
    claim_identity = _normalise_for_identity(claim)
    support_identity = _normalise_for_identity(support_text)
    if not claim_identity or not support_identity:
        return False
    if claim_identity in support_identity:
        return True

    def material_numbers(value: str) -> set[float]:
        without_times = re.sub(
            r"\b\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)\b",
            " ",
            value,
            flags=re.IGNORECASE,
        )
        numbers: set[float] = set()
        scale_by_suffix = {
            "": 1.0,
            "k": 1_000.0,
            "thousand": 1_000.0,
            "m": 1_000_000.0,
            "million": 1_000_000.0,
            "b": 1_000_000_000.0,
            "billion": 1_000_000_000.0,
            "t": 1_000_000_000_000.0,
            "trillion": 1_000_000_000_000.0,
        }
        for match in re.finditer(
            r"(?<![\w])(?P<number>\d[\d,]*(?:\.\d+)?)"
            r"\s*(?P<suffix>thousand|million|billion|trillion|[kmbt])?\b",
            without_times,
            flags=re.IGNORECASE,
        ):
            number = float(match.group("number").replace(",", ""))
            suffix = str(match.group("suffix") or "").casefold()
            numbers.add(number * scale_by_suffix[suffix])
        return numbers

    claim_numbers = material_numbers(claim)
    support_numbers = material_numbers(support_text)
    approximate = bool(
        re.search(
            r"(?:~|≈|\babout\b|\bapproximately\b|\baround\b|\bbarely\b|"
            r"\bnearly\b|\broughly\b)",
            claim,
            flags=re.IGNORECASE,
        )
    )
    for number in claim_numbers:
        if number in support_numbers:
            continue
        if approximate and any(
            abs(candidate - number) <= max(1.0, abs(number) * 0.10)
            for candidate in support_numbers
        ):
            continue
        return False

    def meaningful_tokens(value: str) -> set[str]:
        return {
            token
            for token in re.findall(r"\b[\w'-]{4,}\b", value)
            if token not in SUPPORT_STOPWORDS and not token.isdigit()
        }

    claim_tokens = meaningful_tokens(claim_identity)
    support_tokens = meaningful_tokens(support_identity)
    if not claim_tokens:
        return bool(claim_numbers and claim_numbers.issubset(support_numbers))
    overlap = claim_tokens & support_tokens
    return len(overlap) >= 3 and (
        len(overlap) / len(claim_tokens) >= 0.25
        or len(overlap) / max(1, len(support_tokens)) >= 0.25
    )


def _evidence_supports_claim(record: dict, claim: str) -> bool:
    """Require one evidence record to support this claim's substance."""

    support_text = " ".join(
        str(record.get(key) or "")
        for key in ("claim", "quote", "supporting_excerpt")
    )
    return _support_text_supports_claim(support_text, claim)


def _evidence_records_support_claim(records: Iterable[dict], claim: str) -> bool:
    """Evaluate a compound claim against the cited evidence records together."""

    support_text = " ".join(
        str(record.get(key) or "")
        for record in records
        for key in ("claim", "quote", "supporting_excerpt")
    )
    return _support_text_supports_claim(support_text, claim)


def inspect_publication_markdown(
    text: str, *, agent_names: Iterable[str] = ()
) -> list[QualityIssue]:
    issues: list[QualityIssue] = []
    checks = (
        (
            r"\[Source:\s*",
            "internal_source_tag",
            "internal [Source: ...] tags must be converted to reader-facing footnotes",
        ),
        (
            r"\[UNVERIFIED[^\]]*\]",
            "unverified_claim",
            "unverified claims remain in the final draft",
        ),
        (
            r"\{\{[^{}\n]+\}\}",
            "unresolved_placeholder",
            "an unresolved {{placeholder}} remains",
        ),
        (
            r"`?outputs/(?:context|stage[1-4])/",
            "internal_path",
            "an internal pipeline path is visible to the reader",
        ),
        (
            r"\bStage\s+[1234]\s+(?:final|draft|output|report|fact[- ]checked)",
            "internal_stage_label",
            "an internal Council stage label is visible to the reader",
        ),
        (
            r"\b(?:research|agent|analyst|strategist|red[- ]team)[-_ ]brief\b",
            "internal_brief_reference",
            "an internal agent or brief reference is visible to the reader",
        ),
    )
    for pattern, code, message in checks:
        count = len(re.findall(pattern, text, flags=re.IGNORECASE))
        if count:
            _issue(
                issues,
                severity="error",
                code=code,
                message=message,
                count=count,
            )

    for name in agent_names:
        # Exact slugs are unambiguously internal; natural role phrases such as
        # "operations analyst" are not blocked because they can be legitimate.
        count = len(re.findall(rf"\b{re.escape(name)}-brief\b", text, re.IGNORECASE))
        if count:
            _issue(
                issues,
                severity="error",
                code="named_internal_brief",
                message=f"internal brief name '{name}-brief' is visible",
                count=count,
            )

    definitions = FOOTNOTE_DEF_RE.findall(text)
    definition_labels = [label for label, _ in definitions]
    body = FOOTNOTE_DEF_RE.sub("", text)
    marker_labels = FOOTNOTE_MARKER_RE.findall(body)
    marker_set = set(marker_labels)
    definition_set = set(definition_labels)

    duplicate_defs = {
        label for label in definition_labels if definition_labels.count(label) > 1
    }
    if duplicate_defs:
        _issue(
            issues,
            severity="error",
            code="duplicate_footnote_definition",
            message=f"duplicate footnote definitions: {', '.join(sorted(duplicate_defs))}",
            count=len(duplicate_defs),
        )
    missing_defs = marker_set - definition_set
    if missing_defs:
        _issue(
            issues,
            severity="error",
            code="missing_footnote_definition",
            message=f"footnote markers lack definitions: {', '.join(sorted(missing_defs))}",
            count=len(missing_defs),
        )
    orphan_defs = definition_set - marker_set
    if orphan_defs:
        _issue(
            issues,
            severity="error",
            code="orphan_footnote_definition",
            message=f"footnote definitions are never used: {', '.join(sorted(orphan_defs))}",
            count=len(orphan_defs),
        )

    nonnumeric_labels = {
        label
        for label in marker_set | definition_set
        if not label.isdigit()
    }
    if nonnumeric_labels:
        _issue(
            issues,
            severity="error",
            code="nonnumeric_footnote_label",
            message=(
                "Word production requires numeric footnote labels: "
                + ", ".join(sorted(nonnumeric_labels))
            ),
            count=len(nonnumeric_labels),
        )

    first_use = list(dict.fromkeys(marker_labels))
    if first_use and all(label.isdigit() for label in first_use):
        expected = [str(number) for number in range(1, len(first_use) + 1)]
        if first_use != expected:
            _issue(
                issues,
                severity="error",
                code="footnote_sequence",
                message="numeric footnotes are not sequential in order of first use",
            )

    uncited_numeric_segments = [
        segment
        for segment in _numeric_claim_segments(body)
        if not FOOTNOTE_MARKER_RE.search(segment)
    ]
    if uncited_numeric_segments:
        examples = " | ".join(
            re.sub(r"\s+", " ", segment).strip()[:220]
            for segment in uncited_numeric_segments[:5]
        )
        _issue(
            issues,
            severity="error",
            code="numeric_claims_without_footnotes",
            message=(
                "numerical claims lack a footnote in the same sentence or table "
                f"row. First affected passages: {examples}"
            ),
            count=len(uncited_numeric_segments),
        )

    uncited_attributed_segments = [
        segment
        for paragraph in re.split(r"\n\s*\n", body)
        if paragraph.strip() and not paragraph.lstrip().startswith("#")
        for segment in split_claim_units(paragraph)
        if ATTRIBUTED_CLAIM_RE.search(segment)
        and not FOOTNOTE_MARKER_RE.search(segment)
    ]
    if uncited_attributed_segments:
        examples = " | ".join(
            re.sub(r"\s+", " ", segment).strip()[:220]
            for segment in uncited_attributed_segments[:5]
        )
        _issue(
            issues,
            severity="error",
            code="attributed_claims_without_footnotes",
            message=(
                "attributed claims lack a footnote in the same sentence. "
                f"First affected passages: {examples}"
            ),
            count=len(uncited_attributed_segments),
        )

    substantive_words = len(
        re.findall(
            r"\b[\w'-]+\b",
            re.sub(r"(?m)^\s*#+.*$", "", body),
        )
    )
    required_citations = max(1, (substantive_words + 599) // 600)
    if len(marker_labels) < required_citations:
        _issue(
            issues,
            severity="error",
            code="insufficient_citation_coverage",
            message=(
                f"the draft has {substantive_words} substantive words but only "
                f"{len(marker_labels)} citation marker(s); at least "
                f"{required_citations} are required"
            ),
        )

    buzzwords = {
        "best-in-class": r"\bbest-in-class\b",
        "paradigm shift": r"\bparadigm shift\b",
        "in today's rapidly evolving landscape": (
            r"\bin today['’]s rapidly evolving landscape\b"
        ),
        "synergy": r"\bsynerg(?:y|ies)\b",
    }
    for label, pattern in buzzwords.items():
        count = len(re.findall(pattern, text, re.IGNORECASE))
        if count:
            _issue(
                issues,
                severity="warning",
                code="tone_buzzword",
                message=f"tone review: remove or justify '{label}'",
                count=count,
            )
    return issues


def run_publication_quality_gate(
    *,
    final_draft: Path,
    report_path: Path,
    evidence_ledger_path: Path,
    agent_names: Iterable[str] = (),
    claim_lineage_path: Path | None = None,
    output_format: str | None = None,
    length_instruction: str | None = None,
    readability_profile: str | None = None,
    raise_on_failure: bool = True,
) -> dict:
    """Inspect and persist a release-gate report.

    The report is always written, including on failure, so operators and resume
    runs have an exact remediation list.
    """

    validation = validate_artifact(final_draft)
    issues: list[QualityIssue] = []
    for error in validation.errors:
        _issue(
            issues,
            severity="error",
            code="invalid_final_artifact",
            message=error,
        )
    text = ""
    word_count: int | None = None
    word_count_bounds: tuple[int, int] | None = None
    if final_draft.is_file():
        text = final_draft.read_text(encoding="utf-8", errors="replace")
        issues.extend(
            inspect_publication_markdown(text, agent_names=agent_names)
        )
        if readability_profile == "executive_memo":
            issues.extend(inspect_executive_memo_markdown(text))
        if output_format is not None or length_instruction:
            word_count = publication_word_count(text)
            word_count_bounds = resolve_word_count_bounds(
                output_format or "report",
                length_instruction,
            )
            lower, upper = word_count_bounds
            if word_count < lower or word_count > upper:
                _issue(
                    issues,
                    severity="error",
                    code="word_count_out_of_range",
                    message=(
                        f"the final {output_format or 'report'} has "
                        f"{word_count:,} reader-facing words; the run contract "
                        f"requires {lower:,}–{upper:,}"
                    ),
                )

    evidence_ids: set[str] = set()
    evidence_by_id: dict[str, dict] = {}
    if not evidence_ledger_path.is_file():
        _issue(
            issues,
            severity="error",
            code="missing_evidence_ledger",
            message="evidence-ledger.jsonl is missing",
        )
    else:
        for line_number, line in enumerate(
            evidence_ledger_path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines(),
            start=1,
        ):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                _issue(
                    issues,
                    severity="error",
                    code="invalid_evidence_ledger_json",
                    message=f"evidence-ledger line {line_number} is invalid JSON",
                )
                continue
            evidence_id = (
                str(record.get("evidence_id") or "")
                if isinstance(record, dict)
                else ""
            )
            if not evidence_id:
                _issue(
                    issues,
                    severity="error",
                    code="evidence_without_id",
                    message=f"evidence-ledger line {line_number} has no evidence_id",
                )
            elif evidence_id in evidence_ids:
                _issue(
                    issues,
                    severity="error",
                    code="duplicate_evidence_id",
                    message=f"evidence ID '{evidence_id}' appears more than once",
                )
            else:
                evidence_ids.add(evidence_id)
                if isinstance(record, dict):
                    evidence_by_id[evidence_id] = record
    if not evidence_ids:
        _issue(
            issues,
            severity="error",
            code="empty_evidence_ledger",
            message="the evidence ledger contains no usable evidence IDs",
        )

    lineage_records: list[dict] = []
    if claim_lineage_path is None or not claim_lineage_path.is_file():
        _issue(
            issues,
            severity="error",
            code="missing_claim_lineage",
            message="claim-lineage.jsonl is missing",
        )
    else:
        for line_number, line in enumerate(
            claim_lineage_path.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines(),
            start=1,
        ):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                _issue(
                    issues,
                    severity="error",
                    code="invalid_claim_lineage_json",
                    message=f"claim-lineage line {line_number} is invalid JSON",
                )
                continue
            if not isinstance(record, dict):
                _issue(
                    issues,
                    severity="error",
                    code="invalid_claim_lineage_record",
                    message=f"claim-lineage line {line_number} is not an object",
                )
                continue
            lineage_records.append(record)

    lineage_required = {
        "claim_id",
        "claim",
        "citation",
        "footnote_id",
        "evidence_ids",
        "verification_status",
        "primary_source_checked",
        "retained",
        "draft_sha256",
    }
    allowed_statuses = {
        "verified",
        "qualified",
        "corrected",
        "removed",
        "unverified",
    }
    draft_hash = (
        hashlib.sha256(final_draft.read_bytes()).hexdigest()
        if final_draft.is_file()
        else None
    )
    draft_text = (
        final_draft.read_text(encoding="utf-8", errors="replace")
        if final_draft.is_file()
        else ""
    )
    definitions = {
        label: citation for label, citation in FOOTNOTE_DEF_RE.findall(draft_text)
    }
    body = FOOTNOTE_DEF_RE.sub("", draft_text)
    body_identity = _normalise_for_identity(body)
    body_markers = set(FOOTNOTE_MARKER_RE.findall(body))
    marker_contexts = _marker_contexts(body)
    covered_markers: set[str] = set()
    claim_ids: set[str] = set()
    for index, record in enumerate(lineage_records, start=1):
        claim_id = str(record.get("claim_id") or f"lineage record {index}")
        if claim_id in claim_ids:
            _issue(
                issues,
                severity="error",
                code="duplicate_claim_id",
                message=f"claim ID '{claim_id}' appears more than once",
            )
        claim_ids.add(claim_id)
        missing = sorted(lineage_required - set(record))
        if missing:
            _issue(
                issues,
                severity="error",
                code="claim_lineage_schema",
                message=f"{claim_id} is missing: {', '.join(missing)}",
            )
        if not isinstance(record.get("retained"), bool):
            _issue(
                issues,
                severity="error",
                code="claim_lineage_retained_type",
                message=f"{claim_id} has a non-boolean retained value",
            )
            continue
        status = str(record.get("verification_status") or "")
        if status not in allowed_statuses:
            _issue(
                issues,
                severity="error",
                code="claim_lineage_status",
                message=f"{claim_id} has unknown verification status '{status}'",
            )
            continue
        retained = record["retained"]
        if status in {"verified", "qualified", "corrected"} and not retained:
            _issue(
                issues,
                severity="error",
                code="claim_status_retention_mismatch",
                message=f"{claim_id} is {status} but marked as excluded",
            )
        if status in {"removed", "unverified"} and retained:
            _issue(
                issues,
                severity="error",
                code="claim_status_retention_mismatch",
                message=f"{claim_id} is {status} but marked as retained",
            )
        if not draft_hash or record.get("draft_sha256") != draft_hash:
            _issue(
                issues,
                severity="error",
                code="stale_claim_lineage",
                message=f"{claim_id} is not bound to the current final-draft bytes",
            )

        claim_identity = _normalise_for_identity(record.get("claim"))
        claim_appears = bool(
            claim_identity and claim_identity in body_identity
        )
        if retained and not claim_appears:
            _issue(
                issues,
                severity="error",
                code="lineage_claim_not_in_draft",
                message=(
                    f"{claim_id} is retained but its exact normalized claim "
                    "does not appear in the final draft"
                ),
            )
        if not retained and claim_appears:
            _issue(
                issues,
                severity="error",
                code="excluded_claim_still_in_draft",
                message=(
                    f"{claim_id} is marked as excluded but still appears in "
                    "the final draft"
                ),
            )

        if retained:
            footnote_id = str(record.get("footnote_id") or "").strip()
            if not footnote_id or footnote_id not in body_markers:
                _issue(
                    issues,
                    severity="error",
                    code="lineage_footnote_not_in_draft",
                    message=(
                        f"{claim_id} does not name a footnote marker used in "
                        "the final draft"
                    ),
                )
            elif footnote_id not in definitions:
                _issue(
                    issues,
                    severity="error",
                    code="lineage_footnote_without_definition",
                    message=f"{claim_id} footnote [^{footnote_id}] has no definition",
                )
            else:
                covered_markers.add(footnote_id)
                localized_claim = any(
                    claim_identity and claim_identity in context
                    for context in marker_contexts.get(footnote_id, [])
                )
                if not localized_claim:
                    _issue(
                        issues,
                        severity="error",
                        code="lineage_claim_footnote_mismatch",
                        message=(
                            f"{claim_id} does not appear in the sentence or "
                            f"table row cited by [^{footnote_id}]"
                        ),
                    )
                if _normalise_for_identity(record.get("citation")) != (
                    _normalise_for_identity(definitions[footnote_id])
                ):
                    _issue(
                        issues,
                        severity="error",
                        code="lineage_citation_mismatch",
                        message=(
                            f"{claim_id} citation does not equal the "
                            f"[^{footnote_id}] reader-facing footnote"
                        ),
                    )

            claim_evidence_ids = record.get("evidence_ids")
            if not isinstance(claim_evidence_ids, list) or not claim_evidence_ids:
                _issue(
                    issues,
                    severity="error",
                    code="claim_without_evidence",
                    message=f"{claim_id} is retained but has no evidence IDs",
                )
            else:
                missing_refs = sorted(
                    {
                        str(evidence_id)
                        for evidence_id in claim_evidence_ids
                        if str(evidence_id) not in evidence_ids
                    }
                )
                if missing_refs:
                    _issue(
                        issues,
                        severity="error",
                        code="claim_references_missing_evidence",
                        message=(
                            f"{claim_id} references unknown evidence IDs: "
                            + ", ".join(missing_refs)
                        ),
                        count=len(missing_refs),
                    )
                known_refs = [
                    str(evidence_id)
                    for evidence_id in claim_evidence_ids
                    if str(evidence_id) in evidence_by_id
                ]
                matched_refs = [
                    evidence_id
                    for evidence_id in known_refs
                    if _evidence_matches_citation(
                        evidence_by_id[evidence_id],
                        str(record.get("citation") or ""),
                    )
                ]
                if known_refs and not matched_refs:
                    _issue(
                        issues,
                        severity="error",
                        code="claim_evidence_citation_mismatch",
                        message=(
                            f"{claim_id} has no evidence ID that identifies "
                            "its reader-facing source: "
                            + ", ".join(known_refs)
                        ),
                        count=len(known_refs),
                    )
                supporting_records = [
                    evidence_by_id[evidence_id]
                    for evidence_id in matched_refs
                ]
                if matched_refs and not _evidence_records_support_claim(
                    supporting_records,
                    str(record.get("claim") or ""),
                ):
                    _issue(
                        issues,
                        severity="error",
                        code="claim_not_supported_by_evidence_record",
                        message=(
                            f"{claim_id}'s cited evidence records do not collectively "
                            "support the reader-facing assertion"
                        ),
                    )
            if record.get("primary_source_checked") is not True:
                _issue(
                    issues,
                    severity="error",
                    code="primary_source_not_checked",
                    message=(
                        f"{claim_id} is retained but its primary source was not checked"
                    ),
                )

    if not lineage_records:
        _issue(
            issues,
            severity="error",
            code="empty_claim_lineage",
            message="claim-lineage.jsonl contains no canonical claim records",
        )
    elif not any(
        record.get("retained") is True
        and record.get("verification_status")
        in {"verified", "qualified", "corrected"}
        for record in lineage_records
    ):
        _issue(
            issues,
            severity="error",
            code="no_retained_verified_claims",
            message=(
                "the final draft has no retained verified, qualified, or "
                "corrected claim lineage"
            ),
        )
    elif body_markers - covered_markers:
        uncovered = sorted(body_markers - covered_markers)
        _issue(
            issues,
            severity="error",
            code="incomplete_claim_lineage",
            message=(
                "reader-facing footnotes lack retained claim lineage: "
                + ", ".join(f"[^{label}]" for label in uncovered)
            ),
            count=len(uncovered),
        )

    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]
    payload = {
        "schema_version": "1.0",
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "final_draft": str(final_draft),
        "passed": not errors,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "artifact_validation": validation.to_dict(),
        "reader_word_count": word_count,
        "word_count_bounds": (
            {"minimum": word_count_bounds[0], "maximum": word_count_bounds[1]}
            if word_count_bounds is not None
            else None
        ),
        "readability_profile": readability_profile,
        "evidence_records": len(evidence_ids),
        "claim_lineage_records": len(lineage_records),
        "issues": [asdict(issue) for issue in issues],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = report_path.with_name(f".{report_path.name}.tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, report_path)
    if errors and raise_on_failure:
        raise PublicationQualityError(report_path, issues)
    return payload
