"""Council evaluation — evidence lineage, quality, cost, and completion.

The original audit estimated an agent's contribution by searching final prose
for its display name.  That was misleading: clean public reports intentionally
do not name internal agents, and common words produced false matches.  This
module attributes evidence only when structured records explicitly connect an
evidence ID to both an agent and a claim.

Legacy archives remain readable.  They report observable facts such as brief
presence, word count, artifact-based stage completion, cost recorded in the
retrospective, and literal ``[UNVERIFIED]`` tags.  Metrics that require a run
manifest, evidence ledger, claim lineage, or human review say "data
unavailable" instead of presenting fake precision.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from statistics import mean
from typing import Iterable

from cli.agents import Agent, load_all_agents
from cli.evaluation import (
    RUBRIC_DIMENSIONS,
    ClaimRecord,
    EvidenceRecord,
    QualityReview,
    discover_artifacts,
    load_claim_lineage,
    load_evidence,
    load_quality_reviews,
    manifest_agents,
    manifest_cost_total,
    manifest_stage_statuses,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "runs"

ARCHIVE_DIR_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")
UNVERIFIED_TAG = re.compile(r"\[UNVERIFIED[^\]]*\]")
STAGE_NAMES: tuple[str, ...] = ("stage1", "stage2", "stage3", "stage4")


@dataclass
class RunRecord:
    slug: str
    archive_dir: Path
    seated_agents: list[str]
    brief_word_counts: dict[str, int]
    final_word_count: int
    unverified_count: int
    completed_stage4: bool
    cost_total: float | None
    stage_statuses: dict[str, str] = field(default_factory=dict)
    stage_status_source: str = "legacy artifact presence"
    manifest_path: Path | None = None
    manifest_valid: bool = False
    evidence_paths: tuple[Path, ...] = ()
    lineage_paths: tuple[Path, ...] = ()
    review_paths: tuple[Path, ...] = ()
    evidence_records: tuple[EvidenceRecord, ...] = ()
    claim_records: tuple[ClaimRecord, ...] = ()
    quality_reviews: tuple[QualityReview, ...] = ()
    evidence_data_available: bool = False
    lineage_data_available: bool = False
    warnings: tuple[str, ...] = ()

    @property
    def has_evidence_ledger(self) -> bool:
        return self.evidence_data_available

    @property
    def has_claim_lineage(self) -> bool:
        return self.lineage_data_available

    @property
    def human_reviews(self) -> tuple[QualityReview, ...]:
        return tuple(
            review
            for review in self.quality_reviews
            if review.is_human and review.rubric
        )

    @property
    def evidence_commissioned(self) -> int | None:
        if not self.has_evidence_ledger:
            return None
        return len(self.evidence_records)

    @property
    def used_evidence_ids(self) -> set[str] | None:
        if not self.has_claim_lineage:
            return None
        return {
            evidence_id
            for claim in self.claim_records
            for evidence_id in claim.evidence_ids
        }

    @property
    def evidence_used(self) -> int | None:
        ids = self.used_evidence_ids
        return len(ids) if ids is not None else None

    @property
    def matched_evidence_used(self) -> int | None:
        ids = self.used_evidence_ids
        if ids is None or not self.has_evidence_ledger:
            return None
        ledger_ids = {record.evidence_id for record in self.evidence_records}
        return len(ids & ledger_ids)

    @property
    def missing_evidence_references(self) -> int | None:
        ids = self.used_evidence_ids
        if ids is None or not self.has_evidence_ledger:
            return None
        ledger_ids = {record.evidence_id for record in self.evidence_records}
        return len(ids - ledger_ids)

    @property
    def verified_claims(self) -> int | None:
        if not self.has_claim_lineage:
            return None
        return sum(
            claim.verification_status == "verified"
            for claim in self.claim_records
        )

    @property
    def removed_claims(self) -> int | None:
        if not self.has_claim_lineage:
            return None
        return sum(
            claim.verification_status == "removed"
            for claim in self.claim_records
        )

    @property
    def unverified_claims(self) -> int | None:
        if not self.has_claim_lineage:
            return None
        return sum(
            claim.verification_status == "unverified"
            for claim in self.claim_records
        )

    @property
    def corrected_claims(self) -> int | None:
        """Records showing a correction, including legacy overlay flags."""
        if not self.has_claim_lineage:
            return None
        return sum(claim.corrected for claim in self.claim_records)

    @property
    def corrected_outcome_claims(self) -> int | None:
        if not self.has_claim_lineage:
            return None
        return sum(
            claim.verification_status == "corrected"
            for claim in self.claim_records
        )

    @property
    def qualified_claims(self) -> int | None:
        if not self.has_claim_lineage:
            return None
        return sum(
            claim.verification_status == "qualified"
            for claim in self.claim_records
        )

    @property
    def claims_with_unknown_outcome(self) -> int | None:
        if not self.has_claim_lineage:
            return None
        return sum(
            claim.verification_status not in {
                "verified",
                "qualified",
                "corrected",
                "removed",
                "unverified",
            }
            for claim in self.claim_records
        )

    @property
    def correction_rate(self) -> float | None:
        corrected = self.corrected_claims
        if corrected is None or not self.claim_records:
            return None
        return corrected / len(self.claim_records)

    @property
    def primary_source_claims(self) -> int | None:
        primary, denominator, _ = self._primary_source_counts()
        return primary if denominator is not None else None

    @property
    def primary_source_evaluable_claims(self) -> int | None:
        _, denominator, _ = self._primary_source_counts()
        return denominator

    @property
    def primary_source_unclassified_claims(self) -> int | None:
        _, denominator, unclassified = self._primary_source_counts()
        return unclassified if denominator is not None else None

    @property
    def primary_source_coverage(self) -> float | None:
        primary, denominator, _ = self._primary_source_counts()
        if denominator in {None, 0}:
            return None
        return primary / denominator

    def _primary_source_counts(self) -> tuple[int, int | None, int]:
        if not self.has_evidence_ledger or not self.has_claim_lineage:
            return 0, None, 0
        by_id = {record.evidence_id: record for record in self.evidence_records}
        primary = 0
        evaluable = 0
        unclassified = 0
        for claim in self.claim_records:
            # Removed claims are not part of the published claim set whose
            # source coverage the operator needs to understand.
            if claim.verification_status == "removed":
                continue
            classifications = [
                by_id[evidence_id].is_primary
                for evidence_id in claim.evidence_ids
                if evidence_id in by_id
            ]
            if claim.primary_source_checked is False:
                evaluable += 1
                continue
            if claim.primary_source_checked is not True or not classifications:
                unclassified += 1
                continue
            if True in classifications:
                primary += 1
                evaluable += 1
            elif all(classification is False for classification in classifications):
                evaluable += 1
            else:
                # No primary record and at least one unknown classification.
                # Excluding the claim is more honest than treating unknown as
                # secondary.
                unclassified += 1
        return primary, evaluable, unclassified


@dataclass
class AgentScore:
    """Structured evidence contribution for one agent.

    ``evidence_*`` counts are meaningful only for ``structured_runs``.  They
    are never derived from final prose.
    """

    runs_seated: int = 0
    total_brief_words: int = 0
    runs_completed: int = 0
    structured_runs: int = 0
    evidence_commissioned: int = 0
    evidence_used: int = 0

    @property
    def avg_brief_words(self) -> int:
        if not self.runs_seated:
            return 0
        return self.total_brief_words // self.runs_seated

    @property
    def evidence_use_rate(self) -> float | None:
        if not self.structured_runs or not self.evidence_commissioned:
            return None
        return self.evidence_used / self.evidence_commissioned


def _count_words(text: str) -> int:
    return len(text.split())


def _list_archived_runs(runs_dir: Path) -> list[Path]:
    if not runs_dir.is_dir():
        return []
    return sorted(
        path
        for path in runs_dir.iterdir()
        if path.is_dir() and ARCHIVE_DIR_PATTERN.match(path.name)
    )


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _parse_cost_from_retrospective(retro_path: Path) -> float | None:
    text = _read_text(retro_path)
    if not text:
        return None
    match = re.search(
        r"(?:total\s+(?:estimated\s+)?cost|cost\s+total)[^$\n]*"
        r"\$\s*([\d,]+(?:\.\d+)?)",
        text,
        re.IGNORECASE,
    )
    if match is None:
        return None
    try:
        return float(match.group(1).replace(",", ""))
    except ValueError:
        return None


def _legacy_stage_statuses(archive_dir: Path) -> dict[str, str]:
    stage1 = archive_dir / "stage1"
    stage2 = archive_dir / "stage2"
    stage3 = archive_dir / "stage3"
    stage4 = archive_dir / "stage4"
    return {
        "stage1": (
            "complete"
            if stage1.is_dir() and any(stage1.glob("*-brief.md"))
            else "not_observed"
        ),
        "stage2": (
            "complete"
            if (
                (stage2 / "strategist-draft-v3.md").is_file()
                or (stage2 / "strategist-draft.md").is_file()
            )
            else "not_observed"
        ),
        "stage3": (
            "complete"
            if (stage3 / "final-draft.md").is_file()
            else "not_observed"
        ),
        "stage4": (
            "complete"
            if stage4.is_dir()
            and any(
                path.suffix.lower() in {".docx", ".pptx", ".pdf"}
                for path in stage4.iterdir()
                if path.is_file()
            )
            else "not_observed"
        ),
    }


def _structured_records_available(
    paths: tuple[Path, ...],
    records: tuple[object, ...],
    warnings: Iterable[str],
) -> bool:
    if not paths:
        return False
    if records:
        return True
    blocking_phrases = (
        "could not read",
        "invalid json",
        "is not a json object",
        "is not a json",
    )
    return not any(
        any(phrase in warning.lower() for phrase in blocking_phrases)
        for warning in warnings
    )


def load_run(archive_dir: Path) -> RunRecord:
    match = ARCHIVE_DIR_PATTERN.match(archive_dir.name)
    slug = match.group(1) if match else archive_dir.name

    discovery = discover_artifacts(archive_dir)
    evidence, evidence_warnings = load_evidence(discovery.evidence_paths)
    claims, claim_warnings = load_claim_lineage(discovery.lineage_paths)
    reviews, review_warnings = load_quality_reviews(discovery.review_paths)

    stage1 = archive_dir / "stage1"
    brief_word_counts: dict[str, int] = {}
    if stage1.is_dir():
        for brief in sorted(stage1.glob("*-brief.md")):
            agent_name = brief.name[: -len("-brief.md")]
            brief_word_counts[agent_name] = _count_words(_read_text(brief))

    manifest_seated = manifest_agents(discovery.manifest)
    seated_agents = list(
        dict.fromkeys([*manifest_seated, *sorted(brief_word_counts)])
    )

    final_path = archive_dir / "stage3" / "final-draft.md"
    final_text = _read_text(final_path)

    manifest_stages = manifest_stage_statuses(discovery.manifest)
    legacy_stages = _legacy_stage_statuses(archive_dir)
    if manifest_stages:
        stage_statuses = {
            stage: manifest_stages.get(stage, legacy_stages[stage])
            for stage in STAGE_NAMES
        }
        stage_status_source = "run manifest; artifact fallback for undeclared stages"
    else:
        stage_statuses = legacy_stages
        stage_status_source = "legacy artifact presence (not schema validation)"

    cost_total = manifest_cost_total(discovery.manifest)
    if cost_total is None:
        cost_total = _parse_cost_from_retrospective(
            archive_dir / "retrospective.md"
        )

    warnings = (
        *discovery.warnings,
        *evidence_warnings,
        *claim_warnings,
        *review_warnings,
    )
    return RunRecord(
        slug=slug,
        archive_dir=archive_dir,
        seated_agents=seated_agents,
        brief_word_counts=brief_word_counts,
        final_word_count=_count_words(final_text),
        unverified_count=len(UNVERIFIED_TAG.findall(final_text)),
        completed_stage4=stage_statuses.get("stage4") == "complete",
        cost_total=cost_total,
        stage_statuses=stage_statuses,
        stage_status_source=stage_status_source,
        manifest_path=discovery.manifest_path,
        manifest_valid=discovery.manifest is not None,
        evidence_paths=discovery.evidence_paths,
        lineage_paths=discovery.lineage_paths,
        review_paths=discovery.review_paths,
        evidence_records=evidence,
        claim_records=claims,
        quality_reviews=reviews,
        evidence_data_available=_structured_records_available(
            discovery.evidence_paths,
            evidence,
            evidence_warnings,
        ),
        lineage_data_available=_structured_records_available(
            discovery.lineage_paths,
            claims,
            claim_warnings,
        ),
        warnings=tuple(warnings),
    )


def _structured_agent_counts(
    run: RunRecord,
) -> tuple[dict[str, int], dict[str, int]]:
    if not run.has_evidence_ledger:
        return {}, {}
    commissioned: dict[str, set[str]] = defaultdict(set)
    for evidence in run.evidence_records:
        if evidence.agent_id:
            commissioned[evidence.agent_id].add(evidence.evidence_id)

    used: dict[str, set[str]] = defaultdict(set)
    used_ids = run.used_evidence_ids
    if used_ids is not None:
        for evidence in run.evidence_records:
            if evidence.agent_id and evidence.evidence_id in used_ids:
                used[evidence.agent_id].add(evidence.evidence_id)
    return (
        {agent: len(ids) for agent, ids in commissioned.items()},
        {agent: len(ids) for agent, ids in used.items()},
    )


def audit_runs(
    runs_dir: Path = RUNS_DIR,
    agents: list[Agent] | None = None,
) -> dict:
    if agents is None:
        agents = load_all_agents()

    runs = [load_run(path) for path in _list_archived_runs(runs_dir)]
    scores: dict[str, AgentScore] = defaultdict(AgentScore)

    for run in runs:
        for agent_name in run.seated_agents:
            score = scores[agent_name]
            score.runs_seated += 1
            score.total_brief_words += run.brief_word_counts.get(agent_name, 0)
            if run.completed_stage4:
                score.runs_completed += 1

        commissioned, used = _structured_agent_counts(run)
        if run.has_evidence_ledger and run.has_claim_lineage:
            for agent_name in set(commissioned) | set(used):
                score = scores[agent_name]
                score.structured_runs += 1
                score.evidence_commissioned += commissioned.get(agent_name, 0)
                score.evidence_used += used.get(agent_name, 0)

    return {"runs": runs, "scores": dict(scores)}


def _format_optional_count(value: int | None) -> str:
    return str(value) if value is not None else "data unavailable"


def _format_cost(value: float | None) -> str:
    return f"${value:,.2f}" if value is not None else "data unavailable"


def _format_rate(value: float | None) -> str:
    return f"{value:.0%}" if value is not None else "data unavailable"


def _stage_summary(run: RunRecord) -> str:
    icons = {
        "complete": "✓",
        "in_progress": "…",
        "running": "…",
        "failed": "✗",
        "error": "✗",
        "blocked": "!",
        "cancelled": "–",
        "canceled": "–",
        "skipped": "–",
        "not_started": "–",
        "not_observed": "?",
        "unknown": "?",
    }
    return " ".join(
        f"{stage[-1]}{icons.get(run.stage_statuses.get(stage, 'unknown'), '?')}"
        for stage in STAGE_NAMES
    )


def _verification_summary(run: RunRecord) -> str:
    if not run.has_claim_lineage:
        return "data unavailable"
    return (
        f"{run.verified_claims} verified / {run.qualified_claims} qualified / "
        f"{run.corrected_outcome_claims} corrected / "
        f"{run.removed_claims} removed / "
        f"{run.unverified_claims} unverified"
    )


def _human_rubric_summary(
    runs: Iterable[RunRecord],
) -> dict[str, tuple[float, int]]:
    by_dimension: dict[str, list[float]] = defaultdict(list)
    for run in runs:
        for review in run.human_reviews:
            for dimension, score in review.rubric.items():
                normalised = score.score_on_five_point_scale
                if normalised is not None:
                    by_dimension[dimension].append(normalised)
    return {
        dimension: (mean(values), len(values))
        for dimension, values in by_dimension.items()
        if values
    }


def _render_data_availability(run: RunRecord) -> str:
    available: list[str] = []
    missing: list[str] = []
    for label, present in (
        ("run manifest", run.manifest_valid),
        ("evidence ledger", run.has_evidence_ledger),
        ("claim lineage", run.has_claim_lineage),
        ("human quality review", bool(run.human_reviews)),
    ):
        (available if present else missing).append(label)
    if not missing:
        return "all structured evaluation inputs available"
    if not available:
        return "legacy archive; all structured evaluation inputs unavailable"
    return (
        f"available: {', '.join(available)}; "
        f"unavailable: {', '.join(missing)}"
    )


def render_audit_report(result: dict, agents: list[Agent]) -> str:
    runs: list[RunRecord] = result["runs"]
    scores: dict[str, AgentScore] = result["scores"]
    agents_by_name = {agent.name: agent for agent in agents}

    lines: list[str] = [f"# Council Evaluation — {date.today().isoformat()}", ""]
    if not runs:
        lines.extend(
            [
                "No archived runs found under `runs/`. Run a Council job first, "
                "then evaluate it.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(
        [
            (
                f"Scanned **{len(runs)}** archived run(s). Contribution is counted "
                "only when structured evidence IDs connect a research record to a "
                "claim. The evaluator never searches final prose for agent names."
            ),
            "",
            "Stage key: `1✓` means Stage 1 completed; `?` means completion could "
            "only be inferred from missing/present legacy artifacts and was not "
            "declared by a manifest.",
            "",
            "| Run | Stages | Cost | Evidence commissioned | Evidence used | "
            "Primary-source claim coverage | Verification | Human reviews |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |",
        ]
    )
    for run in runs:
        primary = (
            f"{run.primary_source_claims}/{run.primary_source_evaluable_claims} "
            f"({_format_rate(run.primary_source_coverage)})"
            if run.primary_source_coverage is not None
            else "data unavailable"
        )
        lines.append(
            f"| `{run.slug}` | {_stage_summary(run)} | "
            f"{_format_cost(run.cost_total)} | "
            f"{_format_optional_count(run.evidence_commissioned)} | "
            f"{_format_optional_count(run.evidence_used)} | {primary} | "
            f"{_verification_summary(run)} | {len(run.human_reviews)} |"
        )
    lines.append("")

    lines.extend(["## Run detail", ""])
    for run in runs:
        lines.extend(
            [
                f"### `{run.slug}`",
                "",
                f"- **Stage completion:** {_stage_summary(run)}. Source: "
                f"{run.stage_status_source}.",
                f"- **Cost:** {_format_cost(run.cost_total)}.",
                f"- **Structured inputs:** {_render_data_availability(run)}.",
            ]
        )
        if run.has_evidence_ledger:
            unattributed = sum(
                evidence.agent_id is None for evidence in run.evidence_records
            )
            lines.append(
                f"- **Evidence:** {run.evidence_commissioned} commissioned; "
                f"{_format_optional_count(run.evidence_used)} referenced by claims; "
                f"{unattributed} record(s) lack structured agent attribution."
            )
        else:
            lines.append(
                "- **Evidence:** data unavailable. Stage 1 brief files show which "
                "agents ran, but not which evidence reached the report."
            )
        if run.has_claim_lineage:
            lines.append(
                f"- **Claim outcomes:** {_verification_summary(run)}; "
                f"{run.corrected_claims} record(s) show a correction "
                f"({_format_rate(run.correction_rate)} of lineage records); "
                f"{run.claims_with_unknown_outcome} unknown outcome."
            )
            if run.has_evidence_ledger:
                lines.append(
                    f"- **Lineage integrity:** {run.matched_evidence_used} used "
                    f"evidence ID(s) match the ledger; "
                    f"{run.missing_evidence_references} reference(s) do not."
                )
                if run.primary_source_coverage is None:
                    lines.append(
                        "- **Primary-source claim coverage:** data unavailable. "
                        "No claims had enough structured source classification to "
                        "form an honest denominator."
                    )
                else:
                    lines.append(
                        f"- **Primary-source claim coverage:** "
                        f"{run.primary_source_claims}/"
                        f"{run.primary_source_evaluable_claims} "
                        f"({_format_rate(run.primary_source_coverage)}); "
                        f"{run.primary_source_unclassified_claims} claim(s) excluded "
                        f"because source classification was missing."
                    )
        elif run.unverified_count:
            lines.append(
                f"- **Legacy verification signal:** {run.unverified_count} literal "
                "`[UNVERIFIED]` tag(s) remain in the final draft. Verified, removed, "
                "and corrected claim counts are data unavailable without lineage."
            )
        else:
            lines.append(
                "- **Verification outcomes:** data unavailable. The absence of "
                "`[UNVERIFIED]` tags in a legacy draft is not proof that every claim "
                "was verified."
            )
        if run.human_reviews:
            lines.append(
                f"- **Human review:** {len(run.human_reviews)} machine-readable "
                "review record(s)."
            )
        else:
            lines.append("- **Human rubric:** data unavailable.")
        if run.warnings:
            lines.append(
                f"- **Structured-data warnings:** {len(run.warnings)}. "
                "See the data-quality section below."
            )
        lines.append("")

    lines.extend(
        [
            "## Structured evidence contribution",
            "",
            (
                "Brief volume and seating are observable for legacy archives. "
                "Evidence contribution is shown only for runs containing both an "
                "evidence ledger and claim lineage; it is never inferred from names "
                "appearing in the report."
            ),
            "",
            "| Agent | Runs seated | Avg brief words | Lineage runs | "
            "Evidence commissioned | Evidence used | Use rate |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for name, score in sorted(
        scores.items(),
        key=lambda item: (
            -item[1].structured_runs,
            -item[1].evidence_used,
            -item[1].runs_seated,
            item[0],
        ),
    ):
        commissioned = (
            str(score.evidence_commissioned)
            if score.structured_runs
            else "data unavailable"
        )
        used = str(score.evidence_used) if score.structured_runs else "data unavailable"
        use_rate = (
            _format_rate(score.evidence_use_rate)
            if score.structured_runs
            else "data unavailable"
        )
        lines.append(
            f"| `{name}` | {score.runs_seated} | {score.avg_brief_words:,} | "
            f"{score.structured_runs} | {commissioned} | {used} | {use_rate} |"
        )
    lines.append("")

    research_names = {agent.name for agent in agents if agent.is_research}
    never_seated = sorted(research_names - set(scores))
    if never_seated:
        lines.extend(["## Available but never seated", ""])
        for name in never_seated:
            display = agents_by_name[name].display_name if name in agents_by_name else name
            lines.append(f"- `{name}` ({display})")
        lines.append("")

    lines.extend(["## Human quality rubric", ""])
    rubric = _human_rubric_summary(runs)
    if not rubric:
        lines.extend(
            [
                (
                    "Data unavailable. Add machine-readable human review records "
                    "under `evaluation/reviews/` to measure originality, airport "
                    "specificity, decision usefulness, writing, and visual quality."
                ),
                "",
            ]
        )
    else:
        lines.extend(
            [
                (
                    "Scores below are normalized to a five-point scale only when a "
                    "review record supplies a valid scale. `n` is the number of human "
                    "scores, not the number of runs."
                ),
                "",
                "| Dimension | Mean / 5 | n |",
                "| --- | ---: | ---: |",
            ]
        )
        for dimension in RUBRIC_DIMENSIONS:
            if dimension not in rubric:
                lines.append(
                    f"| {dimension.replace('_', ' ').title()} | "
                    "data unavailable | 0 |"
                )
                continue
            average, count = rubric[dimension]
            lines.append(
                f"| {dimension.replace('_', ' ').title()} | "
                f"{average:.1f} | {count} |"
            )
        lines.append("")

    known_costs = [run.cost_total for run in runs if run.cost_total is not None]
    lines.extend(["## Portfolio telemetry", ""])
    if known_costs:
        lines.append(
            f"- **Known cost:** ${sum(known_costs):,.2f} across "
            f"{len(known_costs)}/{len(runs)} run(s)."
        )
    else:
        lines.append("- **Cost:** data unavailable for every archived run.")
    structured_runs = [
        run for run in runs if run.has_evidence_ledger and run.has_claim_lineage
    ]
    lines.append(
        f"- **Full lineage coverage:** {len(structured_runs)}/{len(runs)} run(s)."
    )
    reviewed_runs = [run for run in runs if run.human_reviews]
    lines.append(
        f"- **Human rubric coverage:** {len(reviewed_runs)}/{len(runs)} run(s)."
    )
    manifest_runs = [run for run in runs if run.manifest_valid]
    lines.append(
        f"- **Manifest coverage:** {len(manifest_runs)}/{len(runs)} run(s)."
    )
    stage4_complete = [
        run for run in runs if run.stage_statuses.get("stage4") == "complete"
    ]
    lines.append(
        f"- **Stage 4 completion observed or declared:** "
        f"{len(stage4_complete)}/{len(runs)} run(s)."
    )
    lines.append("")

    warning_runs = [run for run in runs if run.warnings]
    if warning_runs:
        lines.extend(["## Structured-data quality", ""])
        for run in warning_runs:
            lines.append(f"### `{run.slug}`")
            lines.append("")
            for warning in run.warnings:
                lines.append(f"- {warning}")
            lines.append("")

    lines.extend(
        [
            "---",
            "",
            "### Methodology",
            "",
            "- **Agent contribution requires structured lineage.** An evidence "
            "record must name an agent ID, and a claim-lineage record must reference "
            "that evidence ID. Final-text name matching is never used.",
            "- **Primary-source coverage is claim-level.** A claim counts as "
            "primary-supported only when the lineage marks primary-source checking "
            "complete and at least one linked evidence record is explicitly classified "
            "as primary. Removed claims are excluded; claims with missing checking or "
            "ambiguous classification are reported separately.",
            "- **Correction rate is an overlay.** It is the share of lineage records "
            "marked as corrected; verified, qualified, corrected, removed, and "
            "unverified remain distinct recorded outcomes.",
            "- **Legacy stage completion is observational.** Artifact presence can "
            "show that work exists, but only a run manifest can declare validated "
            "completion.",
            "- **Missing data stays missing.** Zero means a structured record was "
            "available and the counted event did not occur. `Data unavailable` means "
            "the required structured artifact was absent.",
            "",
            (
                "_Generated by `council --audit`. Re-run after each archive to track "
                "evidence use, factual outcomes, human judgment, cost, and completion._"
            ),
        ]
    )
    return "\n".join(lines)


def write_audit_report(report: str, runs_dir: Path = RUNS_DIR) -> Path:
    runs_dir.mkdir(parents=True, exist_ok=True)
    out_path = runs_dir / f"_audit-{date.today().isoformat()}.md"
    out_path.write_text(report, encoding="utf-8")
    return out_path
