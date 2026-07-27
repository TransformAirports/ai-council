"""Shared Markdown claim-unit parsing for lineage and publication gates."""
from __future__ import annotations

import re


FOOTNOTE_MARKER_RE = re.compile(r"\[\^([^\]]+)\]")
_PROTECTED_PERIOD = "\ue000"
_ABBREVIATION_RE = re.compile(
    r"\b(?:mr|mrs|ms|dr|prof|sr|jr|st|vs|etc|no|fig|sec|ch|vol|pp|"
    r"dept|inc|co|corp|ltd|approx)\.",
    re.IGNORECASE,
)
_INITIALISM_RE = re.compile(r"\b(?:[A-Za-z]\.){2,}")


def _protect_nonterminal_periods(text: str) -> str:
    """Mask periods that cannot end a sentence without changing offsets."""

    protected = re.sub(
        r"(?<=\d)\.(?=\d)",
        _PROTECTED_PERIOD,
        text,
    )
    protected = _INITIALISM_RE.sub(
        lambda match: match.group(0).replace(".", _PROTECTED_PERIOD),
        protected,
    )
    protected = _ABBREVIATION_RE.sub(
        lambda match: match.group(0).replace(".", _PROTECTED_PERIOD),
        protected,
    )
    return protected


def split_claim_units(text: str) -> list[str]:
    """Split prose into cited sentence units while preserving abbreviations.

    The output uses slices from the original text.  Masking therefore affects
    only boundary detection and never changes reader-facing bytes.
    """

    protected = _protect_nonterminal_periods(text)
    units: list[str] = []
    for match in re.finditer(
        r".*?[.!?](?:\[\^[^\]]+\])?(?=\s+|$)|.+$",
        protected,
        flags=re.DOTALL,
    ):
        unit = text[match.start() : match.end()].strip()
        if unit:
            units.append(unit)
    return units


def marker_claim_contexts(body: str) -> dict[str, list[str]]:
    """Map footnote labels to the raw sentence or table row each marker cites."""

    contexts: dict[str, list[str]] = {}
    for marker in FOOTNOTE_MARKER_RE.finditer(body):
        prefix = body[: marker.start()].rstrip()
        if not prefix:
            continue
        paragraph = re.split(r"\n\s*\n", prefix)[-1]
        lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
        if lines and lines[-1].startswith("|"):
            context = lines[-1]
        else:
            candidates = split_claim_units(paragraph)
            context = candidates[-1] if candidates else paragraph
        if context.strip():
            contexts.setdefault(marker.group(1), []).append(context)
    return contexts
