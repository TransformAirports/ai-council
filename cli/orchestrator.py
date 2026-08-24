"""Manifest-driven Council v2 orchestration on the Claude Agent SDK.

The public flow is context/research/curation, creative and adversarial
synthesis, editorial polish plus source verification, then art-directed Office
production. Model choices come from ``council.toml`` rather than this module.
Every handoff has a typed artifact contract; final claims bind to exact
footnotes, evidence IDs, and final-draft bytes before publication. Two human
checkpoints remain between synthesis, verification, and production.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable

import questionary
from rich.console import Console

from cli.agents import Agent, load_all_agents
from cli.artifacts import ArtifactContract, contract_for_path, validate_artifact
from cli.config import get_config
from cli.council_models import GPT_5_6_SOL, CouncilModel, council_model
from cli.evidence import (
    bind_claim_lineage_to_draft,
    build_evidence_ledger,
    ensure_claim_lineage,
    file_sha256,
    normalise_evidence_ledger,
    write_jsonl,
)
from cli.events import emit, get_sink, request_checkpoint
from cli.interactive import RunSpec
from cli.quality_gate import PublicationQualityError, run_publication_quality_gate
from cli.run_manifest import (
    CheckpointInputsChanged,
    assert_manifest_complete,
    build_dependency_fingerprint,
    build_execution_contract_fingerprint,
    checkpoint_approval_matches,
    create_run_manifest,
    dependency_fingerprint_matches,
    manifest_prompt_block,
    record_checkpoint_decision,
    update_artifact,
    update_stage,
)
from cli.revision_state import (
    STATE_NAME as REVISION_STATE_NAME,
    RevisionDependency,
    assert_revision_state_current,
    build_revision_dependency_fingerprint,
    record_revision_step,
    repo_relative as revision_repo_relative,
    revision_step_matches,
)

console = Console()

# New reports bind every role to the run-level model selected during setup.
# Older prompt files without that field retain the historical council.toml
# role routing so interrupted runs remain reproducible and safe to resume.


_ACTIVE_COUNCIL_MODEL: ContextVar[CouncilModel | None] = ContextVar(
    "active_council_model", default=None
)


def _model(role: str) -> str:
    selected = _ACTIVE_COUNCIL_MODEL.get()
    return selected.id if selected is not None else get_config().model(role)


def _effective_provider(agent: Agent) -> str:
    selected = _ACTIVE_COUNCIL_MODEL.get()
    return selected.provider if selected is not None else agent.provider


def _uses_coherent_run_model() -> bool:
    return _ACTIVE_COUNCIL_MODEL.get() is not None


def _legacy_openai_agent(agent: Agent) -> bool:
    return not _uses_coherent_run_model() and agent.provider == "openai"


class RunBudgetExceeded(RuntimeError):
    """Raised between steps when the run's cost ceiling has been reached."""


def report_runtime_preflight(
    repo_root: Path,
    outputs_dir: Path,
    *,
    selected_research_agents: tuple[str, ...] = (),
    council_model_id: str = "",
) -> dict[str, str]:
    """Fail before paid research if final-package tooling cannot succeed."""

    tools = {
        "office": shutil.which("soffice") or shutil.which("libreoffice"),
        "pdf_renderer": shutil.which("pdftoppm"),
    }
    issues: list[str] = []
    if tools["office"] is None:
        issues.append("LibreOffice (`soffice`) is not installed")
    if tools["pdf_renderer"] is None:
        issues.append("Poppler (`pdftoppm`) is not installed")
    if not outputs_dir.is_dir() or not os.access(outputs_dir, os.W_OK):
        issues.append(f"the output directory is not writable: {outputs_dir}")
    selected_model = council_model(council_model_id)
    if (
        (selected_model is not None and selected_model.provider == "openai")
        or (
            selected_model is None
            and "deep-research" in selected_research_agents
        )
    ):
        from cli.codex_subscription import codex_subscription_status

        codex_status = codex_subscription_status()
        if not codex_status.authenticated:
            issues.append(
                "GPT-5.6 Sol requires a ChatGPT subscription session; run `codex login`"
            )
    try:
        free_bytes = shutil.disk_usage(repo_root).free
    except OSError as exc:
        issues.append(f"free disk space could not be checked: {exc}")
    else:
        if free_bytes < 512 * 1024 * 1024:
            issues.append("less than 512 MB of free disk space remains")
    if issues:
        raise RuntimeError(
            "Run preflight failed before any model call: "
            + "; ".join(issues)
            + ". Fix the local dependency, then retry (choose Resume only if "
            "the app shows saved work)."
        )
    return {name: str(path) for name, path in tools.items() if path is not None}


@dataclass
class CostTally:
    by_step: dict[str, float] = field(default_factory=dict)
    budget_usd: float | None = None  # run-level ceiling, checked between steps
    _reservations: dict[str, float] = field(
        default_factory=dict, init=False, repr=False
    )
    _planned_call_units: int = field(default=0, init=False, repr=False)

    def add(self, step: str, cost: float) -> None:
        charged = max(0.0, float(cost))
        self.by_step[step] = self.by_step.get(step, 0.0) + charged
        # A reservation is the most this invocation may still spend. Once an
        # attempt reports a cost, convert that portion from reserved dollars to
        # actual dollars. Retries can use only the unspent balance instead of
        # receiving the original per-call allowance again.
        if step in self._reservations:
            self._reservations[step] = max(
                0.0, self._reservations[step] - charged
            )

    @property
    def total(self) -> float:
        return sum(self.by_step.values())

    @property
    def remaining(self) -> float | None:
        if self.budget_usd is None:
            return None
        return max(
            0.0,
            self.budget_usd
            - self.total
            - sum(self._reservations.values()),
        )

    def check_budget(self, next_step: str) -> None:
        if self.budget_usd is not None and (
            self.total + sum(self._reservations.values())
        ) >= self.budget_usd:
            raise RunBudgetExceeded(
                f"Budget ceiling reached: ${self.total:.2f} spent of the "
                f"${self.budget_usd:.2f} limit, with '{next_step}' still pending. "
                f"Work so far is saved — relaunch and choose Resume to continue "
                f"with a higher ceiling."
            )

    def reserve(
        self, step: str, requested_usd: float | None = None
    ) -> float | None:
        """Atomically reserve one call's spend from the shared run ceiling.

        All Council tasks share one event loop, so this synchronous mutation
        cannot interleave. The returned amount is also passed to the Claude
        SDK's per-call ``max_budget_usd`` guard.
        """

        if self.budget_usd is None:
            return None
        self.check_budget(step)
        available = self.remaining or 0.0
        planned_units = max(1, self._planned_call_units)
        allocation = (
            available / planned_units
            if requested_usd is None
            else min(available, max(0.0, requested_usd))
        )
        if allocation <= 0:
            self.check_budget(step)
            raise RunBudgetExceeded(
                f"No budget remains for '{step}' under the "
                f"${self.budget_usd:.2f} ceiling."
            )
        if self._planned_call_units:
            self._planned_call_units -= 1
        self._reservations[step] = allocation
        return allocation

    def release(self, step: str) -> None:
        self._reservations.pop(step, None)

    def reservation(self, step: str) -> float | None:
        """Return the unspent reservation for one in-flight invocation."""

        return self._reservations.get(step)

    def plan_calls(self, count: int) -> None:
        self._planned_call_units = max(0, int(count))

    def consume_skipped_call(self) -> None:
        if self._planned_call_units:
            self._planned_call_units -= 1


@dataclass
class RunResult:
    tally: CostTally
    archive_path: Path | None = None
    published_path: Path | None = None
    deck_path: Path | None = None
    completed: bool = False


@dataclass(frozen=True)
class PipelineStep:
    """Inspectable execution contract consumed by the v2 orchestrator."""

    id: str
    phase: str
    agent: str
    model_role: str
    output: str
    inputs: tuple[str, ...]
    quality_gate: str = "typed_artifact"


PIPELINE_DEFINITION: tuple[PipelineStep, ...] = (
    PipelineStep(
        "airport-context",
        "context",
        "airport-context-builder",
        "context",
        "context/airport-context.md",
        ("run-manifest.json",),
    ),
    PipelineStep(
        "evidence-curation",
        "evidence",
        "evidence-curator",
        "curation",
        "stage1/evidence-map.md",
        (
            "run-manifest.json",
            "evidence-ledger.jsonl",
            "context/airport-context.md",
            "stage1/*-brief.md",
        ),
    ),
    PipelineStep(
        "creative-director",
        "synthesis",
        "creative-director",
        "creative",
        "stage2/narrative-options.md",
        (
            "run-manifest.json",
            "context/airport-context.md",
            "evidence-ledger.jsonl",
            "stage1/evidence-map.md",
        ),
    ),
    PipelineStep(
        "strategist-v1",
        "synthesis",
        "strategist",
        "synthesis",
        "stage2/strategist-draft-v1.md",
        (
            "run-manifest.json",
            "context/airport-context.md",
            "stage1/*-brief.md",
            "stage2/narrative-options.md",
            "stage1/evidence-map.md",
            "evidence-ledger.jsonl",
        ),
    ),
    PipelineStep(
        "evidence-prosecutor",
        "synthesis",
        "evidence-prosecutor",
        "critique",
        "stage2/red-team-critique-v1.md",
        (
            "run-manifest.json",
            "stage1/*-brief.md",
            "stage1/evidence-map.md",
            "stage2/strategist-draft-v1.md",
            "evidence-ledger.jsonl",
        ),
    ),
    PipelineStep(
        "strategist-v2",
        "synthesis",
        "strategist",
        "synthesis",
        "stage2/strategist-draft-v2.md",
        (
            "run-manifest.json",
            "stage1/*-brief.md",
            "stage1/evidence-map.md",
            "evidence-ledger.jsonl",
            "stage2/narrative-options.md",
            "stage2/strategist-draft-v1.md",
            "stage2/red-team-critique-v1.md",
        ),
    ),
    PipelineStep(
        "airport-executive-review",
        "synthesis",
        "airport-executive-reviewer",
        "executive_review",
        "stage2/red-team-critique-v2.md",
        (
            "run-manifest.json",
            "stage2/strategist-draft-v2.md",
            "stage2/red-team-critique-v1.md",
            "context/airport-context.md",
            "stage1/evidence-map.md",
        ),
    ),
    PipelineStep(
        "strategist-v3",
        "synthesis",
        "strategist",
        "synthesis",
        "stage2/strategist-draft-v3.md",
        (
            "run-manifest.json",
            "stage1/*-brief.md",
            "stage1/evidence-map.md",
            "evidence-ledger.jsonl",
            "stage2/narrative-options.md",
            "stage2/strategist-draft-v2.md",
            "stage2/red-team-critique-v2.md",
        ),
    ),
    PipelineStep(
        "editor",
        "polish",
        "editor",
        "editor",
        "stage3/edited-draft.md",
        ("run-manifest.json", "stage2/strategist-draft-v3.md"),
    ),
    PipelineStep(
        "humanizer",
        "polish",
        "humanizer",
        "humanizer",
        "stage3/humanized-draft.md",
        ("run-manifest.json", "stage3/edited-draft.md"),
    ),
    PipelineStep(
        "fact-checker",
        "verification",
        "fact-checker",
        "factcheck",
        "stage3/final-draft.md",
        (
            "run-manifest.json",
            "stage1/*-brief.md",
            "stage1/evidence-map.md",
            "stage3/humanized-draft.md",
            "evidence-ledger.jsonl",
            "context/airport-context.md",
            "context/context-sources.jsonl",
        ),
        quality_gate="primary_source_verification",
    ),
    PipelineStep(
        "art-director",
        "production",
        "art-director",
        "art_direction",
        "stage4/visual-brief.json",
        (
            "stage3/final-draft.md",
            "stage3/fact-check-report.md",
            "run-manifest.json",
            "stage1/evidence-map.md",
            "evidence-ledger.jsonl",
            "claim-lineage.jsonl",
            "context/airport-context.md",
        ),
    ),
    PipelineStep(
        "word-visual-inspection",
        "production",
        "art-director",
        "art_direction",
        "stage4/{slug}-word-visual-inspection.json",
        (
            "stage4/{slug}.docx",
            "stage4/qa/{slug}/*.png",
        ),
        quality_gate="rendered_page_inspection",
    ),
    PipelineStep(
        "presentation",
        "production",
        "presentation-designer",
        "presentation",
        "stage4/{slug}.pptx",
        (
            "stage4/visual-brief.json",
            "stage3/final-draft.md",
            "stage3/fact-check-report.md",
            "claim-lineage.jsonl",
            "evidence-ledger.jsonl",
            "context/airport-context.md",
            "run-manifest.json",
        ),
        quality_gate="office_package",
    ),
)

    # Standards bodies paywall their text: there is no free URL that resolves to
    # NFPA 72 §18.4.11.2 or IEC 60268-16. Demanding one pressures an agent into
    # inventing a plausible link, which is worse for the reader than an honest
    # offline citation. `source_citation` is that honest third form — and it is
    # accepted only with a locator, so it cannot become a way to skip sourcing.
RESEARCH_EVIDENCE_CONTRACT = ArtifactContract(
    "jsonl",
    min_records=1,
    required_keys=("claim", "source_title", "source_type", "confidence"),
    required_any=(("source_url", "source_path", "source_citation"),),
    requires_with=(("source_citation", ("page_or_section",)),),
    optional=True,
)

CONTEXT_SOURCES_CONTRACT = ArtifactContract(
    "jsonl",
    min_records=0,
    required_keys=(
        "source",
        "source_url",
        "source_type",
        "is_primary",
        "locator",
        "date",
        "context_supported",
    ),
)

EVIDENCE_LEDGER_CONTRACT = ArtifactContract(
    "jsonl",
    min_records=1,
    required_keys=(
        "evidence_id",
        "agent_id",
        "claim",
        "source_title",
        "source_type",
        "is_primary",
        "confidence",
    ),
    required_any=(("source_url", "source_path", "source_citation"),),
    # The ledger normalizes page_or_section into `locator`.
    requires_with=(("source_citation", ("locator",)),),
)

CLAIM_LINEAGE_CONTRACT = ArtifactContract(
    "jsonl",
    min_records=1,
    required_keys=(
        "claim_id",
        "claim",
        "citation",
        "footnote_id",
        "evidence_ids",
        "verification_status",
        "primary_source_checked",
        "retained",
        "draft_sha256",
    ),
)

CLAIM_LINEAGE_AGENT_CONTRACT = ArtifactContract(
    "jsonl",
    min_records=1,
    required_keys=(
        "claim_id",
        "claim",
        "citation",
        "footnote_id",
        "evidence_ids",
        "verification_status",
        "primary_source_checked",
        "retained",
    ),
)


def _pipeline_steps(phase: str) -> tuple[PipelineStep, ...]:
    return tuple(step for step in PIPELINE_DEFINITION if step.phase == phase)


def _has_content(
    path: Path,
    min_bytes: int = 200,
    *,
    contract: ArtifactContract | None = None,
) -> bool:
    """Return whether an artifact satisfies its typed completion contract.

    ``min_bytes`` remains in the signature for compatibility with callers from
    older extensions, but completion is no longer based on byte size.
    """

    del min_bytes
    return validate_artifact(path, contract or contract_for_path(path)).valid


def _required_outputs_complete(
    outputs: tuple[tuple[Path, ArtifactContract], ...],
) -> bool:
    return bool(outputs) and all(
        validate_artifact(path, contract).valid for path, contract in outputs
    )


def _required_outputs_match_manifest(
    outputs: tuple[tuple[Path, ArtifactContract], ...],
    manifest_path: Path | None,
    dependency_inputs: tuple[str, ...] = (),
) -> bool:
    """Confirm resumable outputs and their declared upstream inputs still match."""

    if manifest_path is None:
        return True
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    by_path = {
        str(item.get("path")): item
        for item in manifest.get("artifacts", [])
        if isinstance(item, dict)
    }
    outputs_dir = manifest_path.parent
    for path, contract in outputs:
        validation = validate_artifact(path, contract)
        try:
            relative = path.resolve().relative_to(outputs_dir.resolve()).as_posix()
        except ValueError:
            return False
        record = by_path.get(relative)
        if (
            not record
            or record.get("status") != "complete"
            or not validation.sha256
            or record.get("sha256") != validation.sha256
        ):
            return False
        if dependency_inputs:
            recorded_dependencies = record.get("dependencies")
            recorded_declarations = tuple(
                str(item.get("declared_input") or "")
                for item in (
                    recorded_dependencies.get("inputs", [])
                    if isinstance(recorded_dependencies, dict)
                    else []
                )
                if isinstance(item, dict)
            )
            if (
                recorded_declarations != dependency_inputs
                or not dependency_fingerprint_matches(
                    manifest_path, recorded_dependencies
                )
            ):
                return False
    return True


def _checkpoint_outputs_match_manifest(
    manifest_path: Path,
    declared_inputs: tuple[str, ...],
) -> bool:
    """Confirm checkpoint files and their upstream receipts remain current."""

    outputs_dir = manifest_path.parent
    outputs = tuple(
        (outputs_dir / relative, contract_for_path(outputs_dir / relative))
        for relative in declared_inputs
    )
    if not _required_outputs_match_manifest(outputs, manifest_path):
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    by_path = {
        str(item.get("path")): item
        for item in manifest.get("artifacts", [])
        if isinstance(item, dict)
    }
    for relative in declared_inputs:
        dependencies = by_path.get(relative, {}).get("dependencies")
        if dependencies is not None and not dependency_fingerprint_matches(
            manifest_path, dependencies
        ):
            return False
    return True


def _validated_stage3_package_matches_manifest(
    outputs_dir: Path,
    manifest_path: Path,
) -> bool:
    """Recognize a completed, gate-passed Stage 3 package on resume.

    A publication-gate remediation legitimately rebinds the final draft,
    fact-check report, and lineage to the remediation snapshots rather than to
    the Humanizer inputs consumed by the initial Fact-Checker call. Requiring
    the original Fact-Checker dependency declaration would therefore rerun the
    verifier on every resume after a successful remediation. The passed gate
    is the stronger resume boundary: all four exact artifacts must match their
    manifest hashes and each artifact's own dependency receipt must still
    match current bytes.
    """

    package = (
        (
            outputs_dir / "stage3" / "final-draft.md",
            contract_for_path(outputs_dir / "stage3" / "final-draft.md"),
        ),
        (
            outputs_dir / "stage3" / "fact-check-report.md",
            contract_for_path(outputs_dir / "stage3" / "fact-check-report.md"),
        ),
        (outputs_dir / "claim-lineage.jsonl", CLAIM_LINEAGE_CONTRACT),
        (
            outputs_dir / "quality-gate.json",
            contract_for_path(outputs_dir / "quality-gate.json"),
        ),
    )
    if not _required_outputs_match_manifest(package, manifest_path):
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        gate = json.loads(
            (outputs_dir / "quality-gate.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return False
    if gate.get("passed") is not True or gate.get("error_count") != 0:
        return False
    by_path = {
        str(item.get("path")): item
        for item in manifest.get("artifacts", [])
        if isinstance(item, dict)
    }
    for path, _contract in package:
        try:
            relative = path.resolve().relative_to(
                outputs_dir.resolve()
            ).as_posix()
        except ValueError:
            return False
        dependencies = by_path.get(relative, {}).get("dependencies")
        if not isinstance(dependencies, dict) or not dependency_fingerprint_matches(
            manifest_path, dependencies
        ):
            return False
    return True


def _sequester_unsourced_evidence(
    path: Path, contract: ArtifactContract
) -> list[tuple[int, str]]:
    """Move records that fail the provenance rule into a sidecar file.

    Research agents periodically write a professional-judgment line into the
    evidence file — an honest claim they cannot attribute to any retrievable
    document. It does not belong in the ledger (the fact-checker would treat it
    as sourced), but discarding an entire agent's paid output over two lines out
    of twenty-five is wildly disproportionate, and it has now killed two runs.

    The unsourced records move to ``<name>.unsourced.jsonl`` so nothing is lost
    and the operator can see exactly what was set aside. Only records failing
    the *provenance* requirement are moved; a record that is malformed JSON or
    missing required keys is a genuine defect and stays put, so the contract
    still fails loudly for real breakage.
    """

    if contract.kind != "jsonl" or not path.is_file():
        return []
    groups = [g for g in contract.required_any if "source_url" in g]
    if not groups:
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []

    keep: list[str] = []
    moved: list[tuple[int, str]] = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            keep.append(line)
            continue
        if not isinstance(record, dict):
            keep.append(line)
            continue
        if [k for k in contract.required_keys if k not in record]:
            keep.append(line)  # a real structural defect; let it fail
            continue
        if all(
            any(record.get(key) not in (None, "") for key in group)
            for group in groups
        ):
            keep.append(line)
            continue
        moved.append((number, str(record.get("claim") or "")[:120]))

    if not moved or not keep:
        # Nothing to do, or everything failed — the latter is a real failure and
        # must surface as one rather than silently emptying the evidence file.
        return []

    sidecar = path.with_suffix(path.suffix + ".unsourced.jsonl")
    kept_records = [json.loads(line) for line in lines if line.strip()]
    unsourced = [
        r for r in kept_records
        if isinstance(r, dict)
        and not all(
            any(r.get(key) not in (None, "") for key in group) for group in groups
        )
    ]
    sidecar.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in unsourced),
        encoding="utf-8",
    )
    path.write_text("\n".join(keep) + "\n", encoding="utf-8")
    return moved


def _quarantine_partial_output(path: Path | None) -> None:
    """Keep failed generated output for diagnosis without letting resume skip it."""

    if path is None or not path.is_file():
        return
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    partial = path.with_name(f"{path.name}.partial-{stamp}")
    os.replace(path, partial)


_TRANSIENT_MODEL_ERROR_TOKENS: tuple[str, ...] = (
    "timed out",
    "timeout",
    "connection reset",
    "connection closed",
    "connection refused",
    "temporarily unavailable",
    "rate limit",
    "overloaded",
    "internal server error",
    "service unavailable",
    "socket hang up",
    "broken pipe",
    "http 429",
    "status 429",
    "status: 429",
    "http 500",
    "http 502",
    "http 503",
    "http 504",
    "status 500",
    "status 502",
    "status 503",
    "status 504",
)
_MAX_MODEL_ATTEMPTS = 4
_RATE_LIMIT_RETRY_SPACING_SECONDS = 8
_next_rate_limit_retry_slot = 0.0


def _retry_delay_seconds(
    attempt: int,
    *,
    rate_limited: bool = False,
    step_label: str = "",
) -> int:
    """Return a bounded retry delay, with longer staggered waits for 429s.

    A normal transport wobble usually clears in seconds. Provider rate limits
    need a materially longer cooling-off period, and parallel Stage 1 agents
    must not all wake up on the same second and recreate the same 429 wave.
    The stable per-step jitter keeps tests and event journals reproducible.
    """

    if not rate_limited:
        return min(5 * (2 ** max(0, attempt - 1)), 30)
    base = min(30 * (2 ** max(0, attempt - 1)), 120)
    digest = hashlib.sha256(
        f"{step_label}:{attempt}".encode("utf-8")
    ).digest()
    return base + digest[0] % 16


def _is_rate_limit_failure(
    *,
    api_status: object = None,
    messages: tuple[object, ...] = (),
) -> bool:
    """Recognize a 429 even when the SDK exposes it only in result text."""

    if api_status == 429:
        return True
    detail = " ".join(str(message) for message in messages).casefold()
    return any(
        token in detail
        for token in ("rate limit", "http 429", "status 429", "status: 429")
    )


def _reserve_rate_limit_retry_delay(attempt: int, step_label: str) -> int:
    """Reserve one staggered retry slot across concurrent Claude agents."""

    global _next_rate_limit_retry_slot
    now = asyncio.get_running_loop().time()
    candidate = now + _retry_delay_seconds(
        attempt, rate_limited=True, step_label=step_label
    )
    scheduled = max(candidate, _next_rate_limit_retry_slot)
    _next_rate_limit_retry_slot = (
        scheduled + _RATE_LIMIT_RETRY_SPACING_SECONDS
    )
    # Round up without adding another dependency. A zero-second 429 retry is
    # never useful, even if a test event loop has a coarse monotonic clock.
    return max(1, int(scheduled - now + 0.999))


def _is_transient_model_failure(
    *,
    api_status: object = None,
    messages: tuple[object, ...] = (),
) -> bool:
    """Classify transport/rate-limit failures that are safe to retry."""

    if isinstance(api_status, int) and (
        api_status in {408, 425, 429} or 500 <= api_status <= 599
    ):
        return True
    detail = " ".join(str(message) for message in messages).casefold()
    return any(token in detail for token in _TRANSIENT_MODEL_ERROR_TOKENS)


async def _run_coherent_openai_agent(
    *,
    agent: Agent,
    user_prompt: str,
    model: str,
    cwd: Path,
    step_label: str,
    tally: CostTally,
    output_path: Path | None,
    output_contract: ArtifactContract | None,
    completion_outputs: tuple[tuple[Path, ArtifactContract], ...],
    max_turns: int,
    manifest_path: Path | None,
    artifact_id: str | None,
    dependency_inputs: tuple[str, ...],
    emit_completion: bool,
    cost_journal: Callable[[CostTally], None] | None,
) -> dict[str, object]:
    """Execute and commit one GPT-backed role using the normal artifact gate."""

    from cli.openai_council import run_openai_council_agent

    console.print(
        f"[cyan]▶ {step_label}[/cyan] "
        f"({agent.display_name}, {model} via ChatGPT subscription)"
    )
    await emit(
        "agent_start",
        step=step_label,
        agent=agent.name,
        display=agent.display_name,
        model=model,
        provider="openai",
        billing="chatgpt_subscription",
        billed_separately=False,
    )

    async def report_tool(tool: str, target: str) -> None:
        if target:
            console.print(f"  [dim]{tool}: {target}[/dim]")
        await emit(
            "agent_tool",
            step=step_label,
            tool=tool,
            target=target,
            provider="openai",
            billing="chatgpt_subscription",
        )

    try:
        metrics = await run_openai_council_agent(
            agent=agent,
            user_prompt=user_prompt,
            model=model,
            cwd=cwd,
            max_turns=max_turns,
            on_tool=report_tool,
            write_roots=tuple(
                dict.fromkeys(path.parent for path, _ in completion_outputs)
            ),
        )
        tally.add(step_label, metrics.cost_usd)
        if cost_journal is not None:
            cost_journal(tally)
        tally.release(step_label)
    except Exception as exc:
        tally.release(step_label)
        for candidate_path, _ in completion_outputs:
            _quarantine_partial_output(candidate_path)
        await emit(
            "agent_error",
            step=step_label,
            agent=agent.name,
            error_type=type(exc).__name__,
            message=str(exc),
            provider="openai",
        )
        raise

    if (
        output_path is not None
        and output_contract is not None
        and not _has_content(output_path, contract=output_contract)
    ):
        validation = validate_artifact(output_path, output_contract)
        if manifest_path is not None:
            update_artifact(
                manifest_path,
                output_path,
                validation,
                artifact_id=artifact_id,
                producer=agent.name,
            )
        await emit("artifact_validated", step=step_label, **validation.to_dict())
        raise RuntimeError(
            f"{step_label} (GPT-5.6 Sol) finished without a valid "
            f"{output_path.name}: {'; '.join(validation.errors)}"
        )

    for candidate_path, candidate_contract in completion_outputs:
        sequestered = _sequester_unsourced_evidence(
            candidate_path, candidate_contract
        )
        if sequestered:
            await emit(
                "agent_warning",
                step=step_label,
                agent=agent.name,
                message=(
                    f"{candidate_path.name}: moved {len(sequestered)} unsourced "
                    "record(s) out of the evidence ledger."
                ),
            )
    incomplete = [
        (path, validate_artifact(path, contract))
        for path, contract in completion_outputs
        if not validate_artifact(path, contract).valid
    ]
    if incomplete:
        detail = "; ".join(
            f"{path.name}: {', '.join(validation.errors)}"
            for path, validation in incomplete
        )
        for path, _ in completion_outputs:
            _quarantine_partial_output(path)
        raise RuntimeError(
            f"{step_label} did not complete its atomic artifact set: {detail}"
        )

    dependencies = (
        build_dependency_fingerprint(manifest_path, dependency_inputs)
        if manifest_path is not None and dependency_inputs
        else None
    )
    if dependencies is not None and dependencies.get("complete") is not True:
        for path, _ in completion_outputs:
            _quarantine_partial_output(path)
        raise RuntimeError(
            f"{step_label} cannot bind its output because a declared upstream "
            "input is missing or unsafe."
        )
    if manifest_path is not None:
        for companion_path, companion_contract in completion_outputs:
            if companion_path == output_path:
                continue
            update_artifact(
                manifest_path,
                companion_path,
                validate_artifact(companion_path, companion_contract),
                producer=agent.name,
                dependencies=dependencies,
            )
    if output_path is not None and output_contract is not None:
        validation = validate_artifact(output_path, output_contract)
        if manifest_path is not None:
            update_artifact(
                manifest_path,
                output_path,
                validation,
                artifact_id=artifact_id,
                producer=agent.name,
                dependencies=dependencies,
            )
        await emit("artifact_validated", step=step_label, **validation.to_dict())

    if emit_completion:
        console.print(
            f"  [green]✓ {step_label} done[/green] "
            f"[dim](ChatGPT plan, {metrics.turns} turns)[/dim]"
        )
        await emit(
            "agent_done",
            step=step_label,
            agent=agent.name,
            cost=metrics.cost_usd,
            turns=metrics.turns,
            total=tally.total,
            provider="openai",
            billing="chatgpt_subscription",
            billed_separately=False,
            usage=metrics.as_dict(),
        )
    return {
        "skipped": False,
        "provider": "openai",
        "cost": metrics.cost_usd,
        "turns": metrics.turns,
        "usage": metrics.as_dict(),
        "billing": "chatgpt_subscription",
        "billed_separately": False,
    }


async def _run_agent(
    *,
    agent: Agent,
    user_prompt: str,
    model: str,
    cwd: Path,
    step_label: str,
    tally: CostTally,
    output_path: Path | None = None,
    max_turns: int | None = None,
    artifact_contract: ArtifactContract | None = None,
    manifest_path: Path | None = None,
    artifact_id: str | None = None,
    budget_allocation_usd: float | None = None,
    required_outputs: tuple[tuple[Path, ArtifactContract], ...] = (),
    dependency_inputs: tuple[str, ...] = (),
    emit_completion: bool = True,
    cost_journal: Callable[[CostTally], None] | None = None,
) -> dict[str, object]:
    """Invoke one agent end-to-end via the Claude Agent SDK.

    If `output_path` is set and already exists with material content, the
    invocation is skipped — supports resume after a partial run.

    After completion, if `output_path` is set but the file is missing or empty,
    raises a clear error. Otherwise an exhausted-turn-budget run can look like
    success in the trace ("done, $X, N turns") even though no file was written.

    `max_turns` defaults from council.toml (generous, because synthesis agents
    read many briefs before writing). The run-level budget ceiling is checked
    here, between steps — completed work is never interrupted mid-call.
    """
    if max_turns is None:
        max_turns = get_config().max_turns
    effective_provider = _effective_provider(agent)

    output_contract = (
        artifact_contract
        or (contract_for_path(output_path) if output_path is not None else None)
    )
    completion_outputs = tuple(required_outputs)
    if output_path is not None and output_contract is not None:
        completion_outputs = (
            (output_path, output_contract),
            *tuple(
                item for item in completion_outputs if item[0] != output_path
            ),
        )
    if (
        completion_outputs
        and _required_outputs_complete(completion_outputs)
        and _required_outputs_match_manifest(
            completion_outputs,
            manifest_path,
            dependency_inputs,
        )
    ):
        if not _legacy_openai_agent(agent):
            tally.consume_skipped_call()
        console.print(
            f"[dim]↷ {step_label} skipped — {output_path.relative_to(cwd)} already exists[/dim]"
        )
        validation = validate_artifact(output_path, output_contract)
        if manifest_path is not None:
            update_artifact(
                manifest_path,
                output_path,
                validation,
                artifact_id=artifact_id,
                producer=agent.name,
            )
        await emit(
            "agent_skipped",
            step=step_label,
            agent=agent.name,
            path=str(output_path),
            reason="validated artifact already complete",
        )
        await emit(
            "artifact_validated",
            step=step_label,
            **validation.to_dict(),
        )
        return {
            "skipped": True,
            "provider": effective_provider,
            "billed_separately": _legacy_openai_agent(agent),
        }

    if manifest_path is not None:
        for candidate_path, candidate_contract in completion_outputs:
            if (
                validate_artifact(candidate_path, candidate_contract).valid
                and not _required_outputs_match_manifest(
                    ((candidate_path, candidate_contract),),
                    manifest_path,
                    dependency_inputs,
                )
            ):
                _quarantine_partial_output(candidate_path)

    coherent_openai = effective_provider == "openai" and _uses_coherent_run_model()
    if coherent_openai:
        # Subscription usage has no API-dollar reservation. Keep the planner's
        # call count accurate without applying the Claude SDK spend ceiling.
        tally.consume_skipped_call()
    call_budget = (
        None
        if _legacy_openai_agent(agent) or coherent_openai
        else tally.reserve(step_label, budget_allocation_usd)
    )

    if coherent_openai:
        return await _run_coherent_openai_agent(
            agent=agent,
            user_prompt=user_prompt,
            model=model,
            cwd=cwd,
            step_label=step_label,
            tally=tally,
            output_path=output_path,
            output_contract=output_contract,
            completion_outputs=completion_outputs,
            max_turns=max_turns,
            manifest_path=manifest_path,
            artifact_id=artifact_id,
            dependency_inputs=dependency_inputs,
            emit_completion=emit_completion,
            cost_journal=cost_journal,
        )

    if _legacy_openai_agent(agent):
        openai_metrics = await _run_openai_deep_research(
            agent=agent,
            user_prompt=user_prompt,
            step_label=step_label,
            tally=tally,
            output_path=output_path,
            cwd=cwd,
        )
        if (
            output_path is not None
            and output_contract is not None
            and not _has_content(output_path, contract=output_contract)
        ):
            await emit(
                "agent_error",
                step=step_label,
                agent=agent.name,
                error_type="ArtifactContractError",
                message=f"OpenAI finished without a valid {output_path.name}.",
                provider="openai",
                billing="chatgpt_subscription",
                billed_separately=False,
            )
            raise RuntimeError(
                f"{step_label} (OpenAI) finished without producing {output_path}."
            )
        if output_path is not None and output_contract is not None:
            validation = validate_artifact(output_path, output_contract)
            if manifest_path is not None:
                dependencies = (
                    build_dependency_fingerprint(
                        manifest_path, dependency_inputs
                    )
                    if dependency_inputs
                    else None
                )
                if (
                    dependencies is not None
                    and dependencies.get("complete") is not True
                ):
                    _quarantine_partial_output(output_path)
                    raise RuntimeError(
                        f"{step_label} cannot bind its output because a declared "
                        "upstream input is missing or unsafe."
                    )
                update_artifact(
                    manifest_path,
                    output_path,
                    validation,
                    artifact_id=artifact_id,
                    producer=agent.name,
                    dependencies=dependencies,
                )
            await emit(
                "artifact_validated",
                step=step_label,
                **validation.to_dict(),
            )
        if emit_completion:
            await emit(
                "agent_done",
                step=step_label,
                agent=agent.name,
                cost=None,
                turns=None,
                total=tally.total,
                provider="openai",
                billing="chatgpt_subscription",
                billed_separately=False,
                usage=openai_metrics,
            )
        return {
            "skipped": False,
            "provider": "openai",
            "cost": 0.0,
            "turns": 1,
            "usage": openai_metrics,
            "billing": "chatgpt_subscription",
            "billed_separately": False,
        }

    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ResultMessage,
        TextBlock,
        ToolUseBlock,
        query,
    )

    # Retry spurious SDK races and normal transient provider failures. When
    # many subprocesses spawn in
    # parallel, some sessions fail to establish and the SDK reports it as
    # "Claude Code returned an error result: success" — usually one turn,
    # zero cost, no output. Four bounded attempts with backoff cover a short
    # provider wobble without turning contract/auth failures into retry loops.
    SPURIOUS = "Claude Code returned an error result: success"
    attempts_left = _MAX_MODEL_ATTEMPTS
    last_exc: Exception | None = None
    completed_cost: float | None = None
    completed_turns: int | None = None

    def remaining_attempt_budget() -> float | None:
        if tally.budget_usd is None:
            return call_budget
        remaining = tally.reservation(step_label)
        if remaining is None or remaining <= 0:
            raise RunBudgetExceeded(
                f"The retry allowance for '{step_label}' was consumed by "
                "earlier attempts. Work so far is saved; Resume with a higher "
                "run ceiling if this step still needs to run."
            )
        return remaining

    while attempts_left > 0:
        attempts_left -= 1
        attempt = _MAX_MODEL_ATTEMPTS - attempts_left
        saw_result = False
        try:
            system_prompt = agent.system_prompt
            if _uses_coherent_run_model():
                system_prompt += (
                    "\n\nThe run-level Council model selection is authoritative. "
                    "Ignore any legacy charter sentence claiming this role alone "
                    "uses a different model or provider."
                )
            options = ClaudeAgentOptions(
                system_prompt=system_prompt,
                allowed_tools=list(agent.tools) if agent.tools else None,
                permission_mode="bypassPermissions",
                model=model,
                cwd=str(cwd),
                max_turns=max_turns,
                max_budget_usd=remaining_attempt_budget(),
                # The SDK reads stdout as newline-delimited JSON with a 1 MB
                # default line limit. A large tool result must not crash it.
                max_buffer_size=64 * 1024 * 1024,
                # Empty values override inherited shell credentials in the SDK
                # subprocess. Claude therefore uses the `claude auth login`
                # subscription session even if a key was exported elsewhere.
                env={
                    "ANTHROPIC_API_KEY": "",
                    "CLAUDE_CODE_OAUTH_TOKEN": "",
                },
            )
            console.print(
                f"[cyan]▶ {step_label}[/cyan] "
                f"({agent.display_name}, {model} via Claude subscription)"
            )
            await emit("agent_start", step=step_label, agent=agent.name,
                       display=agent.display_name, model=model,
                       provider="anthropic", billing="claude_subscription",
                       attempt=attempt, max_attempts=_MAX_MODEL_ATTEMPTS)
            async for msg in query(prompt=user_prompt, options=options):
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, ToolUseBlock):
                            tool = block.name
                            target = ""
                            if isinstance(block.input, dict):
                                target = (
                                    block.input.get("file_path")
                                    or block.input.get("path")
                                    or block.input.get("url")
                                    or ""
                                )
                            if target:
                                console.print(f"  [dim]{tool}: {target}[/dim]")
                                await emit("agent_tool", step=step_label, tool=tool, target=target)
                elif isinstance(msg, ResultMessage):
                    saw_result = True
                    cost = getattr(msg, "total_cost_usd", None) or 0.0
                    turns = getattr(msg, "num_turns", 0) or 0
                    result_text = str(
                        getattr(msg, "result", None) or ""
                    ).strip()
                    result_errors = list(getattr(msg, "errors", None) or [])
                    permission_denials = list(
                        getattr(msg, "permission_denials", None) or []
                    )
                    stop_reason = str(
                        getattr(msg, "stop_reason", None) or ""
                    ).strip()
                    subtype = str(getattr(msg, "subtype", "") or "").strip()
                    api_status = getattr(msg, "api_error_status", None)
                    fatal_stop = any(
                        token in stop_reason.casefold()
                        for token in (
                            "refus",
                            "error",
                            "max_token",
                            "max_budget",
                            "context_window",
                        )
                    )
                    failed_result = (
                        bool(getattr(msg, "is_error", False))
                        or bool(result_errors)
                        or bool(permission_denials)
                        or (
                            isinstance(api_status, int)
                            and api_status >= 400
                        )
                        or subtype.casefold().startswith("error")
                        or fatal_stop
                    )
                    result_messages = (result_text, *result_errors)
                    rate_limited = _is_rate_limit_failure(
                        api_status=api_status,
                        messages=result_messages,
                    )
                    transient_failure = _is_transient_model_failure(
                        api_status=api_status,
                        messages=result_messages,
                    )
                    failed_result = failed_result or transient_failure
                    # Spurious success: SDK reports ResultMessage but the
                    # agent did effectively no work AND wrote no file. Treat
                    # as a retryable race. Inspect the result first: the SDK
                    # also reports zero-turn / zero-cost 429s, which are real
                    # provider limits and need a much longer staggered wait.
                    if (
                        attempts_left > 0
                        and not failed_result
                        and not transient_failure
                        and turns <= 1
                        and cost == 0.0
                        and output_path is not None
                        and (
                            output_contract is None
                            or not _has_content(
                                output_path, contract=output_contract
                            )
                        )
                    ):
                        delay = _retry_delay_seconds(attempt)
                        console.print(
                            f"  [yellow]↻ {step_label} returned 1 turn / $0 — "
                            f"subprocess race; retrying in {delay}s[/yellow]"
                        )
                        await emit(
                            "agent_retry",
                            step=step_label,
                            agent=agent.name,
                            reason="subprocess startup race",
                            attempt=attempt + 1,
                            max_attempts=_MAX_MODEL_ATTEMPTS,
                            delay_seconds=delay,
                        )
                        await asyncio.sleep(delay)
                        last_exc = RuntimeError("spurious-success retry")
                        break
                    # A session-level flag with no concrete fault behind it:
                    # the CLI marked the session unsuccessful (is_error, or an
                    # unusual stop such as `stop_sequence`) yet reported no
                    # error text, no denial, no API status, and a benign
                    # subtype. Seen live when a sampled draft matched a harness
                    # stop sequence mid-write. The artifacts are the ground
                    # truth for whether work finished; when they are incomplete
                    # this is worth a bounded retry, not a dead run.
                    benign_session_flag = (
                        failed_result
                        and not result_errors
                        and not permission_denials
                        and not (
                            isinstance(api_status, int) and api_status >= 400
                        )
                        and not result_text
                        and not subtype.casefold().startswith("error")
                        and not fatal_stop
                    )
                    if failed_result:
                        tally.add(step_label, cost)
                        if cost_journal is not None:
                            cost_journal(tally)
                        if benign_session_flag:
                            if completion_outputs and _required_outputs_complete(
                                completion_outputs
                            ):
                                completed_cost = float(cost)
                                completed_turns = int(turns)
                                console.print(
                                    f"  [yellow]↻ {step_label} ended with a "
                                    f"session flag (stop reason: "
                                    f"{stop_reason or 'none'}), but its complete "
                                    "validated artifact set was accepted[/yellow]"
                                )
                                await emit(
                                    "agent_session_flag_recovered",
                                    step=step_label,
                                    agent=agent.name,
                                    stop_reason=stop_reason,
                                    cost=completed_cost,
                                    turns=completed_turns,
                                    total=tally.total,
                                )
                                continue
                            if attempts_left > 0:
                                remaining_attempt_budget()
                                delay = _retry_delay_seconds(attempt)
                                for candidate_path, _c in completion_outputs:
                                    _quarantine_partial_output(candidate_path)
                                if output_path is not None:
                                    _quarantine_partial_output(output_path)
                                console.print(
                                    f"  [yellow]↻ {step_label} stopped early "
                                    f"(stop reason: {stop_reason or 'none'}, "
                                    f"no error detail) — retrying in {delay}s[/yellow]"
                                )
                                await emit(
                                    "agent_retry",
                                    step=step_label,
                                    agent=agent.name,
                                    reason="session stopped without error detail",
                                    attempt=attempt + 1,
                                    max_attempts=_MAX_MODEL_ATTEMPTS,
                                    delay_seconds=delay,
                                )
                                await asyncio.sleep(delay)
                                last_exc = RuntimeError("spurious-success retry")
                                break
                        if attempts_left > 0 and transient_failure:
                            remaining_attempt_budget()
                            delay = (
                                _reserve_rate_limit_retry_delay(
                                    attempt, step_label
                                )
                                if rate_limited
                                else _retry_delay_seconds(attempt)
                            )
                            for candidate_path, _c in completion_outputs:
                                _quarantine_partial_output(candidate_path)
                            _quarantine_partial_output(output_path)
                            retry_reason = (
                                "provider rate limit (429)"
                                if rate_limited
                                else "transient provider or network error"
                            )
                            console.print(
                                f"  [yellow]↻ {step_label} hit {retry_reason} "
                                f"— retrying in {delay}s[/yellow]"
                            )
                            await emit(
                                "agent_retry",
                                step=step_label,
                                agent=agent.name,
                                reason=retry_reason,
                                attempt=attempt + 1,
                                max_attempts=_MAX_MODEL_ATTEMPTS,
                                delay_seconds=delay,
                            )
                            await asyncio.sleep(delay)
                            last_exc = RuntimeError("transient model retry")
                            break
                        turn_limit_exhausted = (
                            subtype.casefold() == "error_max_turns"
                            or any(
                                "maximum number of turns" in str(error).casefold()
                                for error in result_errors
                            )
                        )
                        non_turn_errors = [
                            error
                            for error in result_errors
                            if "maximum number of turns"
                            not in str(error).casefold()
                        ]
                        recoverable_turn_limit = bool(
                            turn_limit_exhausted
                            and completion_outputs
                            and _required_outputs_complete(completion_outputs)
                            and not non_turn_errors
                            and not permission_denials
                            and not (
                                isinstance(api_status, int)
                                and api_status >= 400
                            )
                        )
                        if recoverable_turn_limit:
                            completed_cost = float(cost)
                            completed_turns = int(turns)
                            console.print(
                                f"  [yellow]↻ {step_label} reached {turns} turns, "
                                "but its complete validated artifact set was "
                                "accepted[/yellow]"
                            )
                            await emit(
                                "agent_turn_limit_recovered",
                                step=step_label,
                                agent=agent.name,
                                cost=completed_cost,
                                turns=completed_turns,
                                total=tally.total,
                            )
                            continue
                        _quarantine_partial_output(output_path)
                        matched_stop = str(
                            getattr(msg, "stop_sequence", None) or ""
                        ).strip()
                        details = [
                            *result_errors[:3],
                            result_text,
                            (
                                f"permission denials: {len(permission_denials)}"
                                if permission_denials
                                else ""
                            ),
                            f"API status: {api_status}" if api_status else "",
                            (
                                "session flagged is_error"
                                if getattr(msg, "is_error", False)
                                else ""
                            ),
                            f"stop reason: {stop_reason}" if stop_reason else "",
                            (
                                f"matched stop sequence: {matched_stop!r}"
                                if matched_stop
                                else ""
                            ),
                            f"subtype: {subtype}" if subtype else "",
                        ]
                        detail = "; ".join(item for item in details if item)
                        raise RuntimeError(
                            f"{step_label} returned an unsuccessful model result"
                            + (f": {detail}" if detail else "")
                        )
                    else:
                        tally.add(step_label, cost)
                        if cost_journal is not None:
                            cost_journal(tally)
                        tally.release(step_label)
                        completed_cost = float(cost)
                        completed_turns = int(turns)
            else:
                # async-for completed cleanly without our break — done.
                break
            # We broke out for a retry; loop continues.
            continue
        except Exception as e:  # noqa: BLE001 — translate the SDK's spurious-success into a retry
            last_exc = e
            # Claude Code emits an error ResultMessage at max_turns and the SDK
            # may then raise the same condition again while closing the stream.
            # If the ResultMessage was already accepted because every required
            # artifact is complete, the duplicate close-time exception must not
            # turn that successful recovery back into a failed run.
            completed_result_cleanup = bool(
                completed_cost is not None
                and (
                    not completion_outputs
                    or _required_outputs_complete(completion_outputs)
                )
            )
            if completed_result_cleanup:
                await emit(
                    "agent_stream_cleanup_recovered",
                    step=step_label,
                    agent=agent.name,
                    error_type=type(e).__name__,
                    cost=completed_cost,
                    turns=completed_turns,
                    total=tally.total,
                )
                break
            if SPURIOUS in str(e) and not saw_result and attempts_left > 0:
                delay = _retry_delay_seconds(attempt)
                console.print(
                    f"  [yellow]↻ {step_label} hit subprocess startup race "
                    f"({type(e).__name__}); retrying in {delay}s[/yellow]"
                )
                await emit(
                    "agent_retry",
                    step=step_label,
                    agent=agent.name,
                    reason="subprocess startup race",
                    attempt=attempt + 1,
                    max_attempts=_MAX_MODEL_ATTEMPTS,
                    delay_seconds=delay,
                )
                await asyncio.sleep(delay)
                continue
            if attempts_left > 0 and _is_transient_model_failure(
                messages=(e,)
            ):
                delay = _retry_delay_seconds(attempt)
                for candidate_path, _c in completion_outputs:
                    _quarantine_partial_output(candidate_path)
                _quarantine_partial_output(output_path)
                console.print(
                    f"  [yellow]↻ {step_label} hit a transient "
                    f"{type(e).__name__} — retrying in {delay}s[/yellow]"
                )
                await emit(
                    "agent_retry",
                    step=step_label,
                    agent=agent.name,
                    reason=str(e),
                    attempt=attempt + 1,
                    max_attempts=_MAX_MODEL_ATTEMPTS,
                    delay_seconds=delay,
                )
                await asyncio.sleep(delay)
                continue
            await emit(
                "agent_error",
                step=step_label,
                agent=agent.name,
                error_type=type(e).__name__,
                message=str(e),
            )
            tally.release(step_label)
            raise

    # Catch the "agent completed its turn budget without writing" silent failure.
    # The SDK reports cost and turn count even when Claude Code marks the result
    # is_error=true with subtype=success (the signature of a max_turns exhaustion).
    if (
        output_path is not None
        and output_contract is not None
        and not _has_content(output_path, contract=output_contract)
    ):
        tally.release(step_label)
        validation = validate_artifact(output_path, output_contract)
        if manifest_path is not None:
            update_artifact(
                manifest_path,
                output_path,
                validation,
                artifact_id=artifact_id,
                producer=agent.name,
            )
        await emit(
            "artifact_validated",
            step=step_label,
            **validation.to_dict(),
        )
        if output_path.is_file() and validation.size_bytes:
            raise RuntimeError(
                f"{step_label} wrote {output_path}, but it failed the artifact "
                f"contract: {'; '.join(validation.errors)}"
            )
        if last_exc and "spurious-success" not in str(last_exc):
            # The last attempt threw something other than our retry signal; re-raise.
            raise last_exc
        # A 1-turn / $0 result with no output almost always means the Claude
        # Code subprocess could not authenticate (expired `claude auth login` token
        # is the usual culprit). The pre-flight auth check should catch this
        # first, but if a token expires mid-run, point at the real cause.
        raise RuntimeError(
            f"{step_label} produced no output (the agent ran 0–1 turns at $0). "
            f"This is almost always a Claude authentication failure — your "
            f"`claude auth login` token may have expired. Run `claude auth login`, verify "
            f"with `claude -p \"say PONG\" --max-turns 1`, then relaunch and "
            f"choose Resume."
        )
    tally.release(step_label)
    for candidate_path, candidate_contract in completion_outputs:
        sequestered = _sequester_unsourced_evidence(candidate_path, candidate_contract)
        if sequestered:
            await emit(
                "agent_warning",
                step=step_label,
                agent=agent.name,
                message=(
                    f"{candidate_path.name}: moved {len(sequestered)} unsourced "
                    f"record(s) to {candidate_path.name}.unsourced.jsonl "
                    f"(lines {', '.join(str(n) for n, _ in sequestered)}). "
                    "Professional judgment belongs in the brief, not the ledger."
                ),
            )
    incomplete_companions = [
        (path, validate_artifact(path, contract))
        for path, contract in completion_outputs
        if not validate_artifact(path, contract).valid
    ]
    if incomplete_companions:
        detail = "; ".join(
            f"{path.name}: {', '.join(validation.errors)}"
            for path, validation in incomplete_companions
        )
        # The outputs form one commit unit. Preserve every member as a
        # quarantined diagnostic, including a valid-looking primary file,
        # rather than allowing a later resume to mix artifacts from different
        # attempts.
        for path, _ in completion_outputs:
            _quarantine_partial_output(path)
        await emit(
            "agent_error",
            step=step_label,
            agent=agent.name,
            error_type="ArtifactContractError",
            message=detail,
        )
        raise RuntimeError(
            f"{step_label} did not complete its atomic artifact set: {detail}"
        )
    dependencies = (
        build_dependency_fingerprint(manifest_path, dependency_inputs)
        if manifest_path is not None and dependency_inputs
        else None
    )
    if dependencies is not None and dependencies.get("complete") is not True:
        for path, _ in completion_outputs:
            _quarantine_partial_output(path)
        raise RuntimeError(
            f"{step_label} cannot bind its output because a declared upstream "
            "input is missing or unsafe."
        )
    if manifest_path is not None:
        for companion_path, companion_contract in completion_outputs:
            if companion_path == output_path:
                continue
            companion_validation = validate_artifact(
                companion_path, companion_contract
            )
            update_artifact(
                manifest_path,
                companion_path,
                companion_validation,
                producer=agent.name,
                dependencies=dependencies,
            )
    if output_path is not None and output_contract is not None:
        validation = validate_artifact(output_path, output_contract)
        if manifest_path is not None:
            update_artifact(
                manifest_path,
                output_path,
                validation,
                artifact_id=artifact_id,
                producer=agent.name,
                dependencies=dependencies,
            )
        await emit(
            "artifact_validated",
            step=step_label,
            **validation.to_dict(),
        )
    if completed_cost is None or completed_turns is None:
        await emit(
            "agent_error",
            step=step_label,
            agent=agent.name,
            error_type="MissingResultMessage",
            message="Agent stream ended without a successful ResultMessage.",
            provider="anthropic",
            billing="claude_subscription",
        )
        raise RuntimeError(
            f"{step_label} ended without a successful model result."
        )
    if emit_completion:
        console.print(
            f"  [green]✓ {step_label} done[/green] "
            f"[dim](Claude plan, {completed_turns} turns)[/dim]"
        )
        await emit(
            "agent_done",
            step=step_label,
            agent=agent.name,
            cost=completed_cost,
            turns=completed_turns,
            total=tally.total,
            provider="anthropic",
            billing="claude_subscription",
            billed_separately=False,
        )
    return {
        "skipped": False,
        "provider": "anthropic",
        "cost": completed_cost,
        "turns": completed_turns,
        "billing": "claude_subscription",
        "billed_separately": False,
    }


async def _run_openai_deep_research(
    *,
    agent: Agent,
    user_prompt: str,
    step_label: str,
    tally: CostTally,
    output_path: Path | None,
    cwd: Path,
) -> dict[str, int | None]:
    """Run the legacy cross-model research seat on the ChatGPT subscription.

    The prompt already carries source material inline. Codex returns the brief
    as its final message and the Council commits it to the contracted path.
    """
    from cli.codex_subscription import run_codex_exec

    model = GPT_5_6_SOL
    console.print(
        f"[cyan]▶ {step_label}[/cyan] "
        f"({agent.display_name}, {model} via ChatGPT subscription)"
    )
    await emit(
        "agent_start",
        step=step_label,
        agent=agent.name,
        display=agent.display_name,
        model=model,
        provider="openai",
        billing="chatgpt_subscription",
        billed_separately=False,
    )

    try:
        result = await run_codex_exec(
            prompt=agent.system_prompt + "\n\n## Current assignment\n\n" + user_prompt,
            model=model,
            execution_cwd=cwd,
            sandbox="read-only",
        )
    except Exception as exc:
        await emit(
            "agent_error",
            step=step_label,
            agent=agent.name,
            error_type=type(exc).__name__,
            message=str(exc),
            provider="openai",
            billing="chatgpt_subscription",
            billed_separately=False,
        )
        raise
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.final_text, encoding="utf-8")
    metrics = {
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "total_tokens": (
            result.input_tokens
            + result.output_tokens
            + result.reasoning_output_tokens
        ),
    }
    console.print(
        f"  [green]✓ {step_label} done[/green] [dim](ChatGPT plan)[/dim]"
    )
    return metrics


def _stage1_prompt(agent: Agent, run_file: Path, output_path: Path, override: str) -> str:
    parts = [
        f"You are producing an independent research brief for the Council run defined in `{run_file}`.",
        f"Read that file first for the thesis, audience, tone, and any per-agent override.",
        "Read `prompts/research-contract.md` and follow its brief/evidence artifact "
        "schema exactly.",
        "Read `outputs/run-manifest.json` for the authoritative run contract and "
        "`outputs/context/airport-context.md` for airport-specific constraints, "
        "governance, plans, and operator-supplied context. Treat context sources as "
        "starting evidence, not as conclusions.",
        "",
        f"Write your brief to: `{output_path}`",
        "",
        "Critical rule: do NOT read any other agent's output in `outputs/stage1/`. "
        "Independent evidence is a design feature — Stage 2 needs your distinct lens.",
    ]
    if not _legacy_openai_agent(agent):
        evidence_path = output_path.with_name(
            output_path.name.replace("-brief.md", "-evidence.jsonl")
        )
        parts += [
            "",
            f"Also write a structured evidence companion to: `{evidence_path}`",
            "Write one valid JSON object per line, with no markdown fence. Each record "
            "must contain `claim`, `source_title`, one of `source_url`, `source_path`, or `source_citation` (use `source_citation` plus `page_or_section` for paywalled or print-only standards such as NFPA, IEC, or ANSI, and never invent a URL to satisfy the schema), "
            "`source_type`, `is_primary`, `page_or_section`, "
            "`supporting_excerpt`, `source_date`, `data_vintage`, "
            "`airport_or_entity`, `units`, `denominator`, `caveat`, and "
            "`confidence`. Omit or use null for "
            "unknown optional fields; never invent metadata. The brief remains the "
            "readable analysis and the JSONL is its claim-level evidence trail. "
            "Professional judgment goes in the BRIEF, never in the evidence file: "
            "if a claim rests on your expert read rather than a document a reader "
            "could go and verify, write it in the brief's prose and leave it out "
            "of the JSONL entirely. Every evidence record must carry a real "
            "source.",
        ]
    if override:
        parts += [
            "",
            f"This run's override for your agent: {override}",
        ]
    return "\n".join(parts)


def _stage2_prompts(
    run_file: Path,
    manifest_path: Path | None = None,
    repo_root: Path | None = None,
) -> dict[str, str]:
    prompts = {
        "creative-director": (
            f"Read the run prompt at `{run_file}`, `outputs/run-manifest.json`, "
            "`outputs/context/airport-context.md`, "
            "`outputs/stage1/evidence-map.md`, and "
            "`outputs/evidence-ledger.jsonl`.\n\n"
            "Develop three genuinely different narrative spines for the report: "
            "(1) conservative and board-ready, (2) counterintuitive, and "
            "(3) operationally grounded in a specific airport moment. For each, "
            "provide the thesis, opening scene, signature evidence visual, strongest "
            "objection, memorable comparison, and why it matters to the decision "
            "owner. Rank the options using truth, originality, airport specificity, "
            "and decision usefulness; recommend one without inventing facts.\n"
            "Write to: `outputs/stage2/narrative-options.md`"
        ),
        "strategist-v1": (
            "Read the run prompt at "
            f"`{run_file}`, `outputs/run-manifest.json`, every brief declared in the "
            "manifest, `outputs/context/airport-context.md`, "
            "`outputs/stage1/evidence-map.md`, "
            "`outputs/stage2/narrative-options.md`, and "
            "`outputs/evidence-ledger.jsonl`.\n\n"
            "Produce the first argumentative draft of the Council's main piece. Use "
            "the strongest narrative spine, preserve meaningful disagreement, and "
            "cite primary sources through markdown footnotes rather than internal "
            "agent or brief names.\n"
            "Write to: `outputs/stage2/strategist-draft-v1.md`"
        ),
        "evidence-prosecutor": (
            "Read the run prompt at "
            f"`{run_file}`, `outputs/run-manifest.json`, the Strategist's draft at "
            "`outputs/stage2/strategist-draft-v1.md`, every selected research brief, "
            "`outputs/stage1/evidence-map.md`, and "
            "`outputs/evidence-ledger.jsonl`.\n\n"
            "Act as an evidence prosecutor. Attack source quality, numerical support, "
            "causal leaps, cherry-picking, stale data, missing denominators, hidden "
            "assumptions, and any counterevidence the draft suppresses. Trace each "
            "load-bearing critique to evidence IDs or primary sources. Number every "
            "item so the Strategist can answer it.\n"
            "Write to: `outputs/stage2/red-team-critique-v1.md`"
        ),
        "strategist-v2": (
            "Read `outputs/stage2/strategist-draft-v1.md` and `outputs/stage2/red-team-critique-v1.md`. "
            f"Read the run prompt at `{run_file}` for ongoing framing.\n\n"
            "Revise the draft to address every item in the v1 critique. Where you push back rather than incorporate, "
            "say so explicitly in a brief revision-notes section at the top.\n"
            "Write the revised draft to: `outputs/stage2/strategist-draft-v2.md`"
        ),
        "airport-executive-review": (
            "Read `outputs/stage2/strategist-draft-v2.md`, "
            "`outputs/stage2/red-team-critique-v1.md`, "
            "`outputs/context/airport-context.md`, "
            "`outputs/stage1/evidence-map.md`, `outputs/run-manifest.json`, and "
            f"the decision framing in `{run_file}`.\n\n"
            "Review from the chair of a skeptical airport executive. Test operational "
            "feasibility, owner and authority, airline response, use-and-lease terms, "
            "procurement path, board and political realities, bond and funding impact, "
            "FAA constraints, staffing, first-90-day action, leading metrics, and stop "
            "conditions. Focus on what the evidence pass did not test. Number every "
            "item and distinguish a fatal flaw from an implementation condition.\n"
            "Write to: `outputs/stage2/red-team-critique-v2.md`"
        ),
        "strategist-v3": (
            "Read `outputs/stage2/strategist-draft-v2.md` and `outputs/stage2/red-team-critique-v2.md`. "
            f"Read the run prompt at `{run_file}`.\n\n"
            "Produce the final pre-edit draft. Address every v2 critique. At the very top, write a short "
            "'Handoff notes' section listing any weaknesses you are knowingly leaving in, and why.\n"
            "Write to: `outputs/stage2/strategist-draft-v3.md`"
        ),
    }
    if manifest_path is not None and repo_root is not None:
        contract = manifest_prompt_block(manifest_path, repo_root=repo_root)
        prompts = {name: prompt + contract for name, prompt in prompts.items()}
    return prompts


def _stage3_prompts(
    run_file: Path,
    manifest_path: Path | None = None,
    repo_root: Path | None = None,
) -> dict[str, str]:
    prompts = {
        "editor": (
            "Read the run prompt at "
            f"`{run_file}` and `outputs/stage2/strategist-draft-v3.md`.\n\n"
            "Honor the output format and keep the reader-facing draft inside the "
            "numeric range in `## Length`; publication checks that range "
            "deterministically. Cut repetition and excess—up to 25% when the draft "
            "has room—but never cut below the requested floor. Kill buzzwords (see "
            "CLAUDE.md). Flag any hedge or "
            "numerical claim that needs Fact-checker verification with a bracketed inline tag.\n"
            "Write the edited draft to: `outputs/stage3/edited-draft.md`\n"
            "Write your editor notes to: `outputs/stage3/editor-notes.md`"
        ),
        "humanizer": (
            "Read the run prompt at "
            f"`{run_file}` and the edited draft at `outputs/stage3/edited-draft.md`.\n\n"
            "Refine tone, readability, and overall writing quality per your charter. "
            "Do not add, remove, or alter any factual claim, number, citation, or "
            "bracketed tag — the Fact-checker verifies your output next, and any "
            "drift you introduce will be caught and cut.\n"
            "Write the refined draft to: `outputs/stage3/humanized-draft.md`"
        ),
        "fact-checker": (
            "Read `outputs/stage3/humanized-draft.md`, `outputs/run-manifest.json`, "
            "every brief declared in the manifest, "
            "`outputs/stage1/evidence-map.md`, `outputs/evidence-ledger.jsonl`, "
            "`outputs/context/airport-context.md`, and "
            "`outputs/context/context-sources.jsonl`. "
            f"Also read the run prompt at `{run_file}`.\n\n"
            "Verify every numerical claim, attributed quote, and specific assertion "
            "against the underlying primary source—not merely against another agent's "
            "brief. Open the cited URL or local source when tools permit; confirm the "
            "exact number, denominator, date, page or section, attribution, and that "
            "the source supports the draft's wording. A brief can help locate evidence "
            "but cannot certify it. Correct or remove claims that fail. Do not release "
            "an `[UNVERIFIED — HUMAN REVIEW]` tag in the final draft. Preserve the "
            "requested output format and keep reader-facing prose inside the numeric "
            "range in the run prompt's `## Length` section.\n"
            "Write the fact-check report to: `outputs/stage3/fact-check-report.md`\n"
            "Write the final draft to: `outputs/stage3/final-draft.md`\n"
            "Write claim-level verification to `outputs/claim-lineage.jsonl`, one "
            "JSON object per line with: `claim_id`, `claim` (exact reader-facing "
            "claim text), `footnote_id` (the marker label without `[^ ]`), "
            "`citation` (exactly equal to that footnote's definition), "
            "`evidence_ids`, `retained` (boolean), "
            "`verification_status` (verified, qualified, corrected, removed, or "
            "unverified), `primary_source_checked`, and "
            "`correction` when applicable. Every `evidence_ids` value must be an "
            "exact `evidence_id` copied from `outputs/evidence-ledger.jsonl`; never "
            "invent, transform, or synthesize an ID. No markdown fence."
        ),
    }
    if manifest_path is not None and repo_root is not None:
        contract = manifest_prompt_block(manifest_path, repo_root=repo_root)
        prompts = {name: prompt + contract for name, prompt in prompts.items()}
    return prompts


STAGE_SUBDIRS: tuple[str, ...] = (
    "context",
    "evaluation",
    "stage1",
    "stage2",
    "stage3",
    "stage4",
)
RUN_ROOT_ARTIFACTS: tuple[str, ...] = (
    "run-manifest.json",
    "evidence-ledger.jsonl",
    "claim-lineage.jsonl",
    "quality-gate.json",
)


def _existing_artifacts(outputs_dir: Path) -> list[Path]:
    """Return any pre-existing files under outputs/stage*/ that would conflict."""
    found: list[Path] = [
        outputs_dir / name
        for name in RUN_ROOT_ARTIFACTS
        if (outputs_dir / name).is_file()
    ]
    for sub in STAGE_SUBDIRS:
        stage_dir = outputs_dir / sub
        if not stage_dir.is_dir():
            continue
        for p in stage_dir.rglob("*"):
            if p.is_file():
                found.append(p)
    return found


async def prepare_outputs(outputs_dir: Path, auto_approve: bool, resume: bool = False) -> None:
    """Ensure outputs/ is laid out for a run.

    Default behavior: if prior-run artifacts are present, either confirm with the
    user (interactive) or wipe silently (--no-review). Always preserves
    outputs/.gitkeep.

    With `resume=True`: leave existing artifacts in place. The per-step skip
    logic in _run_agent will pick up where the previous run stopped.
    """
    outputs_dir.mkdir(parents=True, exist_ok=True)
    existing = _existing_artifacts(outputs_dir)
    if resume:
        console.print(
            f"[cyan]Resume mode: keeping {len(existing)} existing file(s) in outputs/.[/cyan]"
        )
    elif existing:
        if auto_approve:
            console.print(
                f"[yellow]Clearing {len(existing)} stale file(s) from outputs/ before this run.[/yellow]"
            )
        elif get_sink() is not None:
            preview = "\n".join(
                f"- `{path.relative_to(outputs_dir)}`" for path in existing[:12]
            )
            if len(existing) > 12:
                preview += f"\n- …and {len(existing) - 12} more file(s)"
            decision = await request_checkpoint(
                "output_cleanup",
                {
                    "title": "Existing run work is in outputs/",
                    "subtitle": (
                        "Starting a different report will clear this working "
                        "set. Completed Library reports are not affected."
                    ),
                    "documents": [
                        {
                            "name": "Files to clear",
                            "content": preview,
                        }
                    ],
                    "actions": ["clear", "abort"],
                },
            ) or {"action": "abort"}
            if decision.get("action") != "clear":
                raise RuntimeError("Aborted: existing outputs were not cleared.")
        else:
            console.print(
                f"[yellow]Found {len(existing)} file(s) in outputs/ from a previous run.[/yellow]"
            )
            preview = "\n".join(f"  • {p.relative_to(outputs_dir)}" for p in existing[:8])
            console.print(f"[dim]{preview}{'…' if len(existing) > 8 else ''}[/dim]")
            answer = await questionary.confirm(
                "Clear outputs/ and start fresh?", default=True
            ).ask_async()
            if not answer:
                raise RuntimeError("Aborted: outputs/ not cleared.")
        for sub in STAGE_SUBDIRS:
            target = outputs_dir / sub
            if target.is_dir():
                shutil.rmtree(target)
        for name in RUN_ROOT_ARTIFACTS:
            target = outputs_dir / name
            if target.is_file():
                target.unlink()

    for sub in STAGE_SUBDIRS:
        (outputs_dir / sub).mkdir(parents=True, exist_ok=True)
    (outputs_dir / ".gitkeep").touch(exist_ok=True)


async def run_airport_context(
    *,
    spec: RunSpec,
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path,
) -> None:
    """Build the shared airport context packet before independent research."""

    step = next(item for item in PIPELINE_DEFINITION if item.id == "airport-context")
    by_name = {agent.name: agent for agent in all_agents}
    agent = by_name.get(step.agent)
    context_path = outputs_dir / step.output
    sources_path = outputs_dir / "context" / "context-sources.jsonl"
    decision_frame_enabled = bool(
        getattr(spec, "decision_frame_enabled", False)
        or str(getattr(spec, "decision_required", "") or "").strip()
    )
    await emit(
        "phase_start",
        phase="context",
        label=(
            "Build airport and decision context"
            if decision_frame_enabled
            else "Build airport and reporting context"
        ),
    )
    update_stage(manifest_path, "context", "running")

    if agent is None:
        # Compatibility for installations that resume before the v2 process
        # agent files have been installed. This is intentionally a factual
        # handoff, not a synthetic airport profile.
        source_lines = "\n".join(
            f"- `{path}`" for path in list(getattr(spec, "source_paths", []) or [])
        ) or "- No operator-supplied source files were attached."
        context_path.parent.mkdir(parents=True, exist_ok=True)
        decision_sections = (
            f"## Decision\n\n{getattr(spec, 'decision_required', '') or 'Not specified.'}\n\n"
            f"## Decision owner\n\n{getattr(spec, 'decision_owner', '') or 'Not specified.'}\n\n"
            if decision_frame_enabled
            else ""
        )
        context_path.write_text(
            "# Airport and reporting context\n\n"
            "The dedicated airport-context builder is not installed in this "
            "environment. Researchers must use the run prompt and attached sources "
            "without assuming a specific airport, governance model, airline "
            "agreement, approval path, capital plan, or operating constraint.\n\n"
            f"{decision_sections}"
            f"## Operator context\n\n{getattr(spec, 'operator_context', '') or 'Not specified.'}\n\n"
            f"## Attached sources\n\n{source_lines}\n",
            encoding="utf-8",
        )
        sources_path.write_text("\n", encoding="utf-8")
    else:
        framing_instruction = (
            "Identify the decision owner, decision required, time horizon, "
            "approval path, and any unresolved decision dependencies."
            if decision_frame_enabled
            else "This run has no Decision frame. Do not invent a decision owner, "
            "approval path, action plan, or success measure. Identify the factual "
            "setting, institutions, places, people, tensions, and source limitations "
            "that will help independent researchers tell the story accurately."
        )
        prompt = (
            f"Read the authoritative run contract at `outputs/run-manifest.json` "
            f"and the run prompt at `{run_file}`. Build a concise airport context "
            "packet before the research swarm begins.\n\n"
            f"{framing_instruction} Identify the named airport/operator, governance, "
            "airline/use-and-lease context, "
            "capital and financial constraints, operating conditions, relevant plans, "
            "and source limitations. Read every operator-supplied source declared in "
            "the manifest. If no airport or operator is named, do not conduct broad "
            "airport web research or invent a local profile; summarize only the "
            "operator framing and attached-source context, and label what remains "
            "unknown.\n\n"
            "Write the readable packet to `outputs/context/airport-context.md`. "
            "Write one JSON object per line to "
            "`outputs/context/context-sources.jsonl` for every source actually used, "
            "with `source`, `source_url`, `source_type`, `is_primary`, `locator`, "
            "`date`, and `context_supported`. If no source was used, still create "
            "the file as newline-only valid empty JSONL. Do not wrap JSONL in "
            "markdown."
        )
        await _run_agent(
            agent=agent,
            user_prompt=prompt,
            model=_model(step.model_role),
            cwd=outputs_dir.parent,
            step_label="context/airport-context",
            tally=tally,
            output_path=context_path,
            manifest_path=manifest_path,
            artifact_id="context/airport-context",
            required_outputs=(
                (sources_path, CONTEXT_SOURCES_CONTRACT),
            ),
            dependency_inputs=step.inputs,
        )

    context_validation = validate_artifact(context_path)
    update_artifact(
        manifest_path,
        context_path,
        context_validation,
        artifact_id="context/airport-context",
        producer=step.agent if agent is not None else "orchestrator",
        dependencies=build_dependency_fingerprint(
            manifest_path, step.inputs
        ),
    )
    source_validation = validate_artifact(
        sources_path, CONTEXT_SOURCES_CONTRACT
    )
    update_artifact(
        manifest_path,
        sources_path,
        source_validation,
        artifact_id="context/sources",
        producer=step.agent if agent is not None else "orchestrator",
        required=True,
        dependencies=build_dependency_fingerprint(
            manifest_path, step.inputs
        ),
    )
    update_stage(
        manifest_path,
        "context",
        "complete",
        context_sources=source_validation.record_count,
    )


async def run_stage1(
    spec: RunSpec,
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path,
) -> None:
    from cli.sources import stage1_preamble, inline_for_openai

    source_paths = list(getattr(spec, "source_paths", []) or [])
    preamble = stage1_preamble(source_paths)
    by_name = {a.name: a for a in all_agents}

    # GPT-5.6 Sol has a ChatGPT-plan request/token window. Two concurrent
    # research calls preserve parallel independence without making the local
    # Codex session collide with its own top-tier-model limits. Claude keeps
    # the proven four-subprocess ceiling.
    stage1_concurrency = (
        2
        if (
            _ACTIVE_COUNCIL_MODEL.get() is not None
            and _ACTIVE_COUNCIL_MODEL.get().provider == "openai"
        )
        else 4
    )
    stage1_semaphore = asyncio.Semaphore(stage1_concurrency)

    async def _bounded_run(coro):
        async with stage1_semaphore:
            return await coro

    await emit(
        "research_swarm_start",
        agents=list(spec.selected_research_agents),
        total=len(spec.selected_research_agents),
        concurrency=stage1_concurrency,
    )
    update_stage(
        manifest_path,
        "research",
        "running",
        agents=len(spec.selected_research_agents),
        concurrency=stage1_concurrency,
    )
    tasks = []
    for name in spec.selected_research_agents:
        agent = by_name[name]
        out = outputs_dir / "stage1" / f"{name}-brief.md"
        override = spec.agent_overrides.get(name, "")
        prompt = _stage1_prompt(agent, run_file, out, override) + preamble
        if _legacy_openai_agent(agent):
            # OpenAI agents have no file tools — inline the run prompt and any
            # source-material text the operator attached.
            prompt += (
                "\n\n--- RUN PROMPT FILE (inlined; you cannot read files) ---\n"
                + run_file.read_text(encoding="utf-8", errors="ignore")
            )
            prompt += inline_for_openai(source_paths, repo_root=outputs_dir.parent)
        required_outputs: list[tuple[Path, ArtifactContract]] = []
        if not _legacy_openai_agent(agent):
            required_outputs.append(
                (
                    outputs_dir / "stage1" / f"{name}-evidence.jsonl",
                    ArtifactContract(
                        "jsonl",
                        min_records=1,
                        required_keys=RESEARCH_EVIDENCE_CONTRACT.required_keys,
                        required_any=RESEARCH_EVIDENCE_CONTRACT.required_any,
                    ),
                )
            )
        if name == "quantitative-analyst":
            required_outputs.extend(
                (
                    (
                        outputs_dir
                        / "stage1"
                        / "quantitative-analysis"
                        / "calculations.json",
                        contract_for_path(
                            outputs_dir
                            / "stage1"
                            / "quantitative-analysis"
                            / "calculations.json"
                        ),
                    ),
                    (
                        outputs_dir
                        / "stage1"
                        / "quantitative-analysis"
                        / "README.md",
                        contract_for_path(
                            outputs_dir
                            / "stage1"
                            / "quantitative-analysis"
                            / "README.md"
                        ),
                    ),
                )
            )
        tasks.append(_bounded_run(
            _run_agent(
                agent=agent,
                user_prompt=prompt,
                model=_model("research"),
                cwd=outputs_dir.parent,
                step_label=f"stage1/{name}",
                tally=tally,
                output_path=out,
                manifest_path=manifest_path,
                artifact_id=f"stage1/{name}/brief",
                required_outputs=tuple(required_outputs),
                dependency_inputs=(
                    "run-manifest.json",
                    "context/airport-context.md",
                ),
            )
        ))
    task_results = await asyncio.gather(*tasks, return_exceptions=True)
    task_failures = [
        (name, result)
        for name, result in zip(spec.selected_research_agents, task_results)
        if isinstance(result, BaseException)
    ]
    if task_failures:
        update_stage(
            manifest_path,
            "research",
            "failed",
            failed_agents=[name for name, _ in task_failures],
            completed_agents=sum(
                not isinstance(result, BaseException)
                for result in task_results
            ),
        )
        detail = "; ".join(
            f"{name}: {type(error).__name__}: {error}"
            for name, error in task_failures
        )
        raise RuntimeError(
            "Stage 1 finished the remaining parallel work but could not "
            f"complete {len(task_failures)} agent(s). Resume will reuse every "
            f"successful brief. {detail}"
        )
    missing = [
        name
        for name in spec.selected_research_agents
        if not (outputs_dir / "stage1" / f"{name}-brief.md").is_file()
    ]
    if missing:
        raise RuntimeError(f"Stage 1 agents did not write their briefs: {missing}")
    for name in spec.selected_research_agents:
        evidence_path = outputs_dir / "stage1" / f"{name}-evidence.jsonl"
        required_evidence = not _legacy_openai_agent(by_name[name])
        evidence_contract = (
            ArtifactContract(
                "jsonl",
                min_records=1,
                required_keys=RESEARCH_EVIDENCE_CONTRACT.required_keys,
                required_any=RESEARCH_EVIDENCE_CONTRACT.required_any,
            )
            if required_evidence
            else RESEARCH_EVIDENCE_CONTRACT
        )
        evidence_validation = validate_artifact(evidence_path, evidence_contract)
        update_artifact(
            manifest_path,
            evidence_path,
            evidence_validation,
            artifact_id=f"stage1/{name}/evidence",
            producer=name,
            required=required_evidence,
        )
        if not evidence_validation.valid:
            raise RuntimeError(
                f"{name} did not produce a valid evidence companion: "
                + "; ".join(evidence_validation.errors)
            )
        await emit(
            "artifact_validated",
            step=f"stage1/{name}/evidence",
            **evidence_validation.to_dict(),
        )
    if "quantitative-analyst" in set(spec.selected_research_agents):
        quantitative_artifacts = (
            (
                outputs_dir
                / "stage1"
                / "quantitative-analysis"
                / "calculations.json",
                "stage1/quantitative/calculations",
            ),
            (
                outputs_dir / "stage1" / "quantitative-analysis" / "README.md",
                "stage1/quantitative/readme",
            ),
        )
        for quantitative_path, artifact_id in quantitative_artifacts:
            validation = validate_artifact(quantitative_path)
            update_artifact(
                manifest_path,
                quantitative_path,
                validation,
                artifact_id=artifact_id,
                producer="quantitative-analyst",
            )
            await emit(
                "artifact_validated",
                step=artifact_id,
                **validation.to_dict(),
            )
            if not validation.valid:
                raise RuntimeError(
                    "Quantitative Analyst did not produce a reproducible "
                    f"{quantitative_path.name}: {'; '.join(validation.errors)}"
                )
    update_stage(
        manifest_path,
        "research",
        "complete",
        agents=len(spec.selected_research_agents),
    )
    await emit(
        "research_swarm_complete",
        agents=list(spec.selected_research_agents),
        total=len(spec.selected_research_agents),
    )


async def run_evidence_curation(
    *,
    spec: RunSpec,
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path,
) -> None:
    """Build the ledger, close load-bearing gaps, and rank the evidence."""

    await emit(
        "phase_start",
        phase="evidence",
        label="Curate evidence, disagreements, and research gaps",
    )
    update_stage(manifest_path, "evidence", "running")
    ledger_path = outputs_dir / "evidence-ledger.jsonl"
    compatibility_path = outputs_dir / "stage1" / "evidence-ledger.jsonl"
    curation_path = outputs_dir / "stage1" / "evidence-map.md"
    by_name = {agent.name: agent for agent in all_agents}
    dependency_inputs = [
        "run-manifest.json",
        "context/airport-context.md",
    ]
    for name in spec.selected_research_agents:
        dependency_inputs.append(f"stage1/{name}-brief.md")
        agent = by_name.get(name)
        if agent is None or not _legacy_openai_agent(agent):
            dependency_inputs.append(f"stage1/{name}-evidence.jsonl")
        if name == "quantitative-analyst":
            dependency_inputs.extend(
                (
                    "stage1/quantitative-analysis/calculations.json",
                    "stage1/quantitative-analysis/README.md",
                )
            )
    curation_dependencies = tuple(dependency_inputs)
    curation_outputs = (
        (ledger_path, EVIDENCE_LEDGER_CONTRACT),
        (compatibility_path, EVIDENCE_LEDGER_CONTRACT),
        (curation_path, contract_for_path(curation_path)),
    )
    existing_ledger = validate_artifact(
        ledger_path, EVIDENCE_LEDGER_CONTRACT
    )
    existing_curation = validate_artifact(curation_path)
    if (
        existing_ledger.valid
        and existing_curation.valid
        and _required_outputs_match_manifest(
            curation_outputs,
            manifest_path,
            curation_dependencies,
        )
    ):
        # Resume must preserve Curator-added gap-fill evidence rather than
        # rebuilding the ledger from the pre-curation agent companions.
        curated_result = normalise_evidence_ledger(ledger_path)
        write_jsonl(compatibility_path, curated_result.records)
        update_artifact(
            manifest_path,
            ledger_path,
            validate_artifact(ledger_path, EVIDENCE_LEDGER_CONTRACT),
            artifact_id="evidence/ledger",
            producer="evidence-curator",
            dependencies=build_dependency_fingerprint(
                manifest_path, curation_dependencies
            ),
        )
        update_artifact(
            manifest_path,
            compatibility_path,
            validate_artifact(compatibility_path, EVIDENCE_LEDGER_CONTRACT),
            artifact_id="evidence/ledger-compatibility",
            producer="evidence-curator",
            required=False,
            dependencies=build_dependency_fingerprint(
                manifest_path, curation_dependencies
            ),
        )
        update_artifact(
            manifest_path,
            curation_path,
            existing_curation,
            artifact_id="evidence/curation",
            producer="evidence-curator",
            dependencies=build_dependency_fingerprint(
                manifest_path, curation_dependencies
            ),
        )
        await emit(
            "evidence_update",
            ledger_path=str(ledger_path),
            record_count=curated_result.record_count,
            structured_records=curated_result.structured_records,
            legacy_records=curated_result.legacy_records,
            agents_without_evidence=[],
            invalid_record_count=len(curated_result.invalid_records),
            resumed=True,
        )
        update_stage(
            manifest_path,
            "evidence",
            "complete",
            evidence_records=curated_result.record_count,
            resumed=True,
        )
        return

    for stale_path, stale_contract in curation_outputs:
        if validate_artifact(stale_path, stale_contract).valid:
            _quarantine_partial_output(stale_path)

    ledger_result = build_evidence_ledger(
        selected_agents=spec.selected_research_agents,
        stage1_dir=outputs_dir / "stage1",
        output_path=ledger_path,
        compatibility_path=compatibility_path,
    )
    # An evidence-free ledger remains a valid legacy handoff: the curator can
    # still inspect briefs and explicitly report that the run lacks usable
    # claim-level sources. Publication verification remains strict later.
    ledger_contract = ArtifactContract("jsonl", min_records=0)
    ledger_validation = validate_artifact(ledger_path, ledger_contract)
    update_artifact(
        manifest_path,
        ledger_path,
        ledger_validation,
        artifact_id="evidence/ledger",
        producer="orchestrator",
        dependencies=build_dependency_fingerprint(
            manifest_path, curation_dependencies
        ),
    )
    compatibility_validation = validate_artifact(
        compatibility_path, ledger_contract
    )
    update_artifact(
        manifest_path,
        compatibility_path,
        compatibility_validation,
        artifact_id="evidence/ledger-compatibility",
        producer="orchestrator",
        required=False,
        dependencies=build_dependency_fingerprint(
            manifest_path, curation_dependencies
        ),
    )
    await emit(
        "evidence_update",
        ledger_path=str(ledger_path),
        record_count=ledger_result.record_count,
        structured_records=ledger_result.structured_records,
        legacy_records=ledger_result.legacy_records,
        agents_without_evidence=ledger_result.agents_without_evidence,
        invalid_record_count=len(ledger_result.invalid_records),
    )
    step = next(item for item in PIPELINE_DEFINITION if item.id == "evidence-curation")
    curator = by_name.get(step.agent) or by_name["strategist"]
    curation_path = outputs_dir / step.output
    prompt = (
        f"Read `{run_file}`, `outputs/run-manifest.json`, every selected Stage 1 "
        "brief declared there, `outputs/evidence-ledger.jsonl`, and "
        "`outputs/context/airport-context.md`.\n\n"
        "Act as the Council's evidence editor. Deduplicate findings; rank the "
        "load-bearing evidence; identify contradictions, stale or weak sources, "
        "missing denominators, and claims that are inference rather than fact. "
        "Distinguish obvious observations from non-obvious insights. Produce an "
        "argument kit containing the ten strongest evidence points, the strongest "
        "counter-case, disagreements the Strategist must preserve, airport-specific "
        "constraints, and a gap analysis.\n\n"
        "For a small number of genuinely load-bearing gaps, conduct targeted research "
        "against primary sources using your available tools. Normalize, deduplicate, "
        "and update the canonical ledger in place at "
        "`outputs/evidence-ledger.jsonl`, including any targeted evidence you find. "
        "Never fill a gap with conjecture. Clearly list any gap that remains open.\n\n"
        "Write the complete evidence curation and gap analysis to "
        "`outputs/stage1/evidence-map.md`."
    )
    prompt += manifest_prompt_block(manifest_path, repo_root=outputs_dir.parent)
    await _run_agent(
        agent=curator,
        user_prompt=prompt,
        model=_model(step.model_role),
        cwd=outputs_dir.parent,
        step_label="evidence/evidence-curation",
        tally=tally,
        output_path=curation_path,
        manifest_path=manifest_path,
        artifact_id="evidence/curation",
        dependency_inputs=curation_dependencies,
    )

    # The curator owns the final normalization and targeted gap-fill pass.
    # Normalize aliases into the public v2 schema, then refresh the Stage 1
    # compatibility mirror used by older prompts and archived tooling.
    curated_result = normalise_evidence_ledger(ledger_path)
    write_jsonl(compatibility_path, curated_result.records)
    ledger_result.records = curated_result.records
    ledger_result.structured_records = curated_result.structured_records
    ledger_result.legacy_records = curated_result.legacy_records
    ledger_result.invalid_records.extend(curated_result.invalid_records)
    ledger_validation = validate_artifact(
        ledger_path, EVIDENCE_LEDGER_CONTRACT
    )
    update_artifact(
        manifest_path,
        ledger_path,
        ledger_validation,
        artifact_id="evidence/ledger",
        producer="evidence-curator",
        dependencies=build_dependency_fingerprint(
            manifest_path, curation_dependencies
        ),
    )
    update_artifact(
        manifest_path,
        compatibility_path,
        validate_artifact(compatibility_path, EVIDENCE_LEDGER_CONTRACT),
        artifact_id="evidence/ledger-compatibility",
        producer="evidence-curator",
        required=False,
        dependencies=build_dependency_fingerprint(
            manifest_path, curation_dependencies
        ),
    )
    await emit(
        "evidence_update",
        ledger_path=str(ledger_path),
        record_count=ledger_result.record_count,
        structured_records=ledger_result.structured_records,
        legacy_records=ledger_result.legacy_records,
        agents_without_evidence=ledger_result.agents_without_evidence,
        invalid_record_count=len(ledger_result.invalid_records),
    )
    if not ledger_validation.valid:
        raise RuntimeError(
            "Evidence curation produced no valid claim-level ledger. "
            + "; ".join(ledger_validation.errors)
        )
    update_stage(
        manifest_path,
        "evidence",
        "complete",
        evidence_records=ledger_result.record_count,
        open_agent_gaps=len(ledger_result.agents_without_evidence),
    )


async def run_stage2(
    spec: RunSpec,
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path,
    start_from: str = "creative-director",
    v3_note: str = "",
) -> None:
    by_name = {a.name: a for a in all_agents}
    prompts = _stage2_prompts(
        run_file, manifest_path=manifest_path, repo_root=outputs_dir.parent
    )
    if v3_note:
        prompts["strategist-v3"] += (
            "\n\nThe human operator reviewed the previous v3 and asked for this "
            "redo with the following notes. Address them directly — they take "
            "precedence over anything they conflict with:\n"
            f"{v3_note}"
        )
    artifact_ids = {
        "creative-director": "stage2/narrative-options",
        "strategist-v1": "stage2/strategist-v1",
        "evidence-prosecutor": "stage2/evidence-prosecutor",
        "strategist-v2": "stage2/strategist-v2",
        "airport-executive-review": "stage2/airport-executive-review",
        "strategist-v3": "stage2/strategist-v3",
    }
    update_stage(manifest_path, "synthesis", "running")
    started = False
    for step in _pipeline_steps("synthesis"):
        if not started and step.id != start_from:
            continue
        started = True
        agent = by_name.get(step.agent)
        if agent is None and step.id == "creative-director":
            agent = by_name["strategist"]
        elif agent is None and step.id in {
            "evidence-prosecutor",
            "airport-executive-review",
        }:
            agent = by_name["red-team"]
        if agent is None:
            raise RuntimeError(
                f"Pipeline step {step.id} requires missing agent {step.agent}."
            )
        await _run_agent(
            agent=agent,
            user_prompt=prompts[step.id],
            model=_model(step.model_role),
            cwd=outputs_dir.parent,
            step_label=f"stage2/{step.id}",
            tally=tally,
            output_path=outputs_dir / step.output,
            manifest_path=manifest_path,
            artifact_id=artifact_ids[step.id],
            dependency_inputs=step.inputs,
        )
    update_stage(manifest_path, "synthesis", "complete")


async def run_stage3(
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path,
) -> None:
    by_name = {a.name: a for a in all_agents}
    prompts = _stage3_prompts(
        run_file, manifest_path=manifest_path, repo_root=outputs_dir.parent
    )
    artifact_ids = {
        "editor": "stage3/edited",
        "humanizer": "stage3/humanized",
        "fact-checker": "stage3/final",
    }
    update_stage(manifest_path, "polish", "running")
    for step in (
        *_pipeline_steps("polish"),
        *_pipeline_steps("verification"),
    ):
        if step.phase == "verification":
            update_stage(manifest_path, "polish", "complete")
            update_stage(manifest_path, "verification", "running")
        agent = by_name[step.agent]
        required_outputs: tuple[tuple[Path, ArtifactContract], ...] = ()
        if step.agent == "editor":
            editor_notes = outputs_dir / "stage3" / "editor-notes.md"
            required_outputs = (
                (editor_notes, contract_for_path(editor_notes)),
            )
        elif step.agent == "fact-checker":
            required_outputs = (
                (
                    outputs_dir / "stage3" / "fact-check-report.md",
                    contract_for_path(
                        outputs_dir / "stage3" / "fact-check-report.md"
                    ),
                ),
                (
                    outputs_dir / "claim-lineage.jsonl",
                    CLAIM_LINEAGE_AGENT_CONTRACT,
                ),
            )
            if _validated_stage3_package_matches_manifest(
                outputs_dir, manifest_path
            ):
                tally.consume_skipped_call()
                final_draft = outputs_dir / "stage3" / "final-draft.md"
                console.print(
                    "[dim]↷ stage3/fact-checker skipped — validated "
                    "publication-gate package already exists[/dim]"
                )
                await emit(
                    "agent_skipped",
                    step="stage3/fact-checker",
                    agent=agent.name,
                    path=str(final_draft),
                    reason="validated publication-gate package already complete",
                )
                await emit(
                    "artifact_validated",
                    step="stage3/fact-checker",
                    **validate_artifact(final_draft).to_dict(),
                )
                continue
        await _run_agent(
            agent=agent,
            user_prompt=prompts[step.id],
            model=_model(step.model_role),
            cwd=outputs_dir.parent,
            step_label=f"stage3/{step.id}",
            tally=tally,
            output_path=outputs_dir / step.output,
            manifest_path=manifest_path,
            artifact_id=artifact_ids[step.id],
            required_outputs=required_outputs,
            dependency_inputs=step.inputs,
        )

    fact_report = outputs_dir / "stage3" / "fact-check-report.md"
    report_validation = validate_artifact(fact_report)
    update_artifact(
        manifest_path,
        fact_report,
        report_validation,
        artifact_id="stage3/fact-check",
        producer="fact-checker",
    )
    await emit(
        "artifact_validated",
        step="stage3/fact-check-report",
        **report_validation.to_dict(),
    )
    if not report_validation.valid:
        raise RuntimeError(
            "Fact-checker did not produce a valid verification report: "
            + "; ".join(report_validation.errors)
        )

    lineage_path = outputs_dir / "claim-lineage.jsonl"
    lineage, generated = ensure_claim_lineage(
        final_draft=outputs_dir / "stage3" / "final-draft.md",
        evidence_ledger=outputs_dir / "evidence-ledger.jsonl",
        output_path=lineage_path,
    )
    lineage = bind_claim_lineage_to_draft(
        final_draft=outputs_dir / "stage3" / "final-draft.md",
        output_path=lineage_path,
    )
    lineage_validation = validate_artifact(lineage_path, CLAIM_LINEAGE_CONTRACT)
    update_artifact(
        manifest_path,
        lineage_path,
        lineage_validation,
        artifact_id="verification/claim-lineage",
        producer="orchestrator" if generated else "fact-checker",
    )
    await emit(
        "evidence_update",
        kind="claim_lineage",
        lineage_path=str(lineage_path),
        record_count=len(lineage),
        generated_fallback=generated,
    )
    update_stage(
        manifest_path,
        "verification",
        "complete",
        claims=len(lineage),
        lineage_fallback=generated,
    )


def _visual_brief_contract() -> ArtifactContract:
    return ArtifactContract(
        "json",
        required_keys=(
            "communication_job",
            "audience",
            "decision",
            "decision_owner",
            "approval_path",
            "first_90_day_action",
            "success_measures",
            "deck_mode",
            "visual_thesis",
            "signature_visual",
            "brand_profile",
            "slides",
            "report_visuals",
            "source_appendix",
            "accessibility_checks",
            "asset_requests",
        ),
    )


def _visual_inspection_contract() -> ArtifactContract:
    return ArtifactContract(
        "json",
        required_keys=(
            "schema_version",
            "artifact",
            "visual_brief",
            "deck_mode",
            "slide_count",
            "rendered_slides",
            "montage",
            "signature_visual",
            "inspection",
        ),
    )


def _word_visual_inspection_contract() -> ArtifactContract:
    return ArtifactContract(
        "json",
        required_keys=(
            "schema_version",
            "inspection_type",
            "artifact",
            "pdf",
            "page_count",
            "rendered_pages",
            "montage",
            "inspection",
        ),
    )


def _validate_visual_brief(
    *,
    out_path: Path,
    schema_path: Path,
    evidence_ledger: Path,
    requested_mode: str,
):
    """Apply the canonical schema and evidence referential-integrity gate."""

    from jsonschema import Draft202012Validator

    contract = _visual_brief_contract()
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    schema_errors = [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: "
        f"{error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(payload),
            key=lambda item: list(item.absolute_path),
        )
    ]
    slides = payload.get("slides", []) if isinstance(payload, dict) else []
    slide_numbers = [
        slide.get("slide_number")
        for slide in slides
        if isinstance(slide, dict)
    ]
    if len(slide_numbers) != len(set(slide_numbers)):
        schema_errors.append("slides: slide_number values must be unique")
    if slide_numbers != list(range(1, len(slide_numbers) + 1)):
        schema_errors.append(
            "slides: slide_number values must be contiguous and ordered from 1"
        )
    if payload.get("deck_mode") != requested_mode:
        schema_errors.append(
            f"deck_mode: expected {requested_mode!r}, got "
            f"{payload.get('deck_mode')!r}"
        )
    signature = (
        payload.get("signature_visual")
        if isinstance(payload, dict)
        else None
    )
    signature_slide_number = (
        signature.get("slide_number")
        if isinstance(signature, dict)
        else None
    )
    slides_by_number = {
        slide.get("slide_number"): slide
        for slide in slides
        if isinstance(slide, dict)
    }
    signature_slide = slides_by_number.get(signature_slide_number)
    if not isinstance(signature_slide_number, int) or signature_slide is None:
        schema_errors.append(
            "signature_visual.slide_number: must identify one canonical slide"
        )
    elif isinstance(signature, dict):
        signature_evidence_values = signature.get("evidence_ids", [])
        slide_evidence_values = signature_slide.get("evidence_ids", [])
        signature_evidence = {
            str(item)
            for item in (
                signature_evidence_values
                if isinstance(signature_evidence_values, list)
                else []
            )
        }
        slide_evidence = {
            str(item)
            for item in (
                slide_evidence_values
                if isinstance(slide_evidence_values, list)
                else []
            )
        }
        missing_signature_evidence = sorted(
            signature_evidence - slide_evidence
        )
        if missing_signature_evidence:
            schema_errors.append(
                "signature_visual.evidence_ids: target slide "
                f"{signature_slide_number} omits "
                + ", ".join(missing_signature_evidence)
            )

    if not evidence_ledger.is_file():
        schema_errors.append(
            f"evidence ledger is missing: {evidence_ledger}"
        )
    ledger_ids: set[str] = set()
    if evidence_ledger.is_file():
        for line in evidence_ledger.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict) and record.get("evidence_id"):
                ledger_ids.add(str(record["evidence_id"]))

    visual_evidence_ids: set[str] = set()

    def collect_evidence_ids(value: object) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "evidence_ids" and isinstance(child, list):
                    visual_evidence_ids.update(str(item) for item in child)
                else:
                    collect_evidence_ids(child)
        elif isinstance(value, list):
            for child in value:
                collect_evidence_ids(child)

    collect_evidence_ids(payload)
    unknown_ids = sorted(visual_evidence_ids - ledger_ids)
    if unknown_ids:
        schema_errors.append(
            "visual evidence IDs are absent from the canonical ledger: "
            + ", ".join(unknown_ids)
        )

    visual_validation = validate_artifact(out_path, contract)
    if schema_errors:
        visual_validation.errors.extend(schema_errors)
        visual_validation.valid = False
    return visual_validation


async def run_art_direction(
    *,
    spec: RunSpec,
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path,
) -> Path | None:
    """Create the visual contract used by both document and slide production."""

    output_format = str(getattr(spec, "output_format", "report"))
    decision_frame_enabled = bool(
        getattr(spec, "decision_frame_enabled", False)
        or any(
            str(getattr(spec, field, "") or "").strip()
            for field in (
                "decision_required",
                "decision_owner",
                "time_horizon",
                "approval_path",
                "success_measure",
            )
        )
    )
    needed = bool(getattr(spec, "want_pptx", False)) or (
        output_format == "report" and decision_frame_enabled
    )
    if not needed:
        await emit(
            "manifest_update",
            path=str(manifest_path),
            artifact="stage4/visual-brief.json",
            status="skipped",
            reason="short output format without a companion presentation",
        )
        return None

    step = next(item for item in PIPELINE_DEFINITION if item.id == "art-director")
    by_name = {agent.name: agent for agent in all_agents}
    art_director = by_name.get(step.agent)
    if art_director is None:
        raise RuntimeError(
            "Council v2 requires the art-director process agent for full reports "
            "and presentations."
        )
    out_path = outputs_dir / step.output
    decision_required = getattr(spec, "decision_required", "") or ""
    decision_owner = getattr(spec, "decision_owner", "") or ""
    approval_path = getattr(spec, "approval_path", "") or ""
    success_measure = getattr(spec, "success_measure", "") or ""
    time_horizon = getattr(spec, "time_horizon", "") or ""
    if decision_frame_enabled:
        decision_contract = (
            "Carry this opted-in run-prompt decision frame into the canonical "
            "top-level fields. Preserve named authorities and thresholds exactly; "
            "qualify a conflict instead of silently replacing it:\n"
            f"- decision: {decision_required or 'Not specified in run prompt.'}\n"
            f"- decision_owner: {decision_owner or 'Establish from verified authority.'}\n"
            f"- approval_path: {approval_path or 'Establish from verified authority.'}\n"
            f"- time horizon for the first action: {time_horizon or 'Not specified in run prompt.'}\n"
            f"- first success measure: {success_measure or 'Establish from verified evidence.'}\n"
            "Derive `first_90_day_action` from the verified draft and evidence. "
            "Write `success_measures` as a non-empty array.\n\n"
        )
    else:
        decision_contract = (
            "This is a narrative commission with no decision frame. Do not invent "
            "an owner, approval path, action plan, or success measure. Keep `decision`, "
            "`decision_owner`, `approval_path`, and `first_90_day_action` as empty "
            "strings and `success_measures` as an empty array. Let `communication_job`, "
            "`visual_thesis`, and evidence-bound report visuals carry the story.\n\n"
        )
    prompt = (
        f"Read `{run_file}`, `outputs/run-manifest.json`, "
        "`outputs/context/airport-context.md`, `outputs/stage1/evidence-map.md`, "
        "`outputs/evidence-ledger.jsonl`, "
        "`outputs/claim-lineage.jsonl`, `outputs/stage3/final-draft.md`, and "
        "`outputs/stage3/fact-check-report.md`.\n\n"
        "Create the visual contract for the Word report and any companion deck. "
        "Visuals must explain evidence rather than decorate it. Specify one signature "
        "visual and bind it to one exact `slide_number`; that target slide must "
        "carry the same evidence IDs and use the signature exhibit as its primary "
        "visual. Specify airport maps or passenger/decision flows where relevant, quantitative "
        "charts with evidence IDs, implementation timelines, recommendation callouts, "
        "tables, section treatments, image/source rights notes, accessibility, and a "
        "density budget. Do not invent a number or visual datum. Every factual visual "
        "must name evidence IDs or verified claims.\n\n"
        f"The requested presentation mode is "
        f"`{getattr(spec, 'deck_mode', 'board') or 'board'}`. "
        "Separate speaker-led board slides from read-ahead/appendix material.\n\n"
        + decision_contract
        + "Write valid JSON—not markdown—to `outputs/stage4/visual-brief.json` with "
        "top-level keys: `communication_job`, `audience`, `decision`, "
        "`decision_owner`, `approval_path`, `first_90_day_action`, "
        "`success_measures`, `deck_mode`, "
        "`visual_thesis`, `signature_visual`, `brand_profile`, `slides`, "
        "`report_visuals`, `source_appendix`, `accessibility_checks`, and "
        "`asset_requests`. Validate it against "
        "`assets/brand/visual-brief.schema.json` before finishing."
    )
    prompt += manifest_prompt_block(manifest_path, repo_root=outputs_dir.parent)
    contract = _visual_brief_contract()
    completion = await _run_agent(
        agent=art_director,
        user_prompt=prompt,
        model=_model(step.model_role),
        cwd=outputs_dir.parent,
        step_label="stage4/art-director",
        tally=tally,
        output_path=out_path,
        artifact_contract=contract,
        manifest_path=manifest_path,
        artifact_id="stage4/visual-brief",
        dependency_inputs=step.inputs,
        emit_completion=False,
    )
    schema_path = (
        outputs_dir.parent / "assets" / "brand" / "visual-brief.schema.json"
    )
    requested_mode = str(getattr(spec, "deck_mode", "board_decision"))
    visual_validation = _validate_visual_brief(
        out_path=out_path,
        schema_path=schema_path,
        evidence_ledger=outputs_dir / "evidence-ledger.jsonl",
        requested_mode=requested_mode,
    )
    update_artifact(
        manifest_path,
        out_path,
        visual_validation,
        artifact_id="stage4/visual-brief",
        producer="art-director",
    )
    await emit(
        "artifact_validated",
        step="stage4/visual-brief-schema",
        **visual_validation.to_dict(),
    )
    if not visual_validation.valid:
        await emit(
            "agent_error",
            step="stage4/art-director",
            agent=art_director.name,
            error_type="VisualBriefContractError",
            message="; ".join(visual_validation.errors[:8]),
        )
        _quarantine_partial_output(out_path)
        raise RuntimeError(
            "Art Director visual brief failed its canonical schema: "
            + "; ".join(visual_validation.errors[:8])
        )
    if not completion.get("skipped"):
        cost = completion.get("cost")
        turns = completion.get("turns")
        console.print(
            f"  [green]✓ stage4/art-director done[/green] "
            f"[dim](${float(cost or 0):.2f}, {turns or 0} turns)[/dim]"
        )
        await emit(
            "agent_done",
            step="stage4/art-director",
            agent=art_director.name,
            cost=cost,
            turns=turns,
            total=tally.total,
            provider=completion.get("provider"),
            billed_separately=bool(completion.get("billed_separately", False)),
        )
    return out_path


async def run_word_visual_inspection(
    *,
    artifacts: list[Path],
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path | None,
    step_label: str,
    max_turns: int | None = None,
    revision_state_path: Path | None = None,
    revision_repo_root: Path | None = None,
    revision_dependencies: tuple[RevisionDependency, ...] = (),
    revision_receipt_inputs: tuple[Path, ...] = (),
    revision_extra_values: dict[str, object] | None = None,
) -> None:
    """Require full-size visual inspection of every rendered Word page."""

    from cli.publishing_quality import (
        assert_quality,
        qa_word_visual_inspection_receipt,
    )

    if not artifacts:
        raise ValueError("Word visual inspection requires at least one document.")
    art_director = {
        agent.name: agent for agent in all_agents
    }.get("art-director")
    if art_director is None:
        raise RuntimeError(
            "Council production requires the art-director for Word page inspection."
        )
    receipts = [
        artifact.with_name(
            f"{artifact.stem}-word-visual-inspection.json"
        )
        for artifact in artifacts
    ]
    if (
        revision_state_path is not None
        and len(revision_receipt_inputs) != len(receipts)
    ):
        raise RuntimeError(
            "Revision Word inspection requires one immutable input receipt "
            "for every approved output receipt."
        )
    if revision_state_path is not None and revision_repo_root is None:
        raise RuntimeError(
            "Revision Word inspection requires an explicit repository root."
        )

    def inspection_reports():
        return [
            qa_word_visual_inspection_receipt(
                receipt,
                artifact=artifact,
            )
            for artifact, receipt in zip(artifacts, receipts, strict=True)
        ]

    reports = inspection_reports()
    # Normal runs can trust the hash-bound receipt directly. Revisions also
    # require the step-scoped execution receipt (model, charter, prompt, and
    # upstream files), so route even a visually valid receipt through the
    # revision wrapper; it will skip without spend only when both layers match.
    already_complete = (
        revision_state_path is None and all(report.ok for report in reports)
    )
    completion: dict[str, object]
    if already_complete:
        tally.consume_skipped_call()
        completion = {"skipped": True, "provider": art_director.provider}
        await emit(
            "agent_skipped",
            step=step_label,
            agent=art_director.name,
            path=str(receipts[0]),
            reason="hash-bound Word page inspection already complete",
        )
    else:
        if revision_state_path is None:
            packets = "\n".join(
                f"- Word artifact: `{artifact}`\n  Receipt: `{receipt}`"
                for artifact, receipt in zip(
                    artifacts, receipts, strict=True
                )
            )
            receipt_instructions = (
                "Do not edit the Word, PDF, page PNGs, montage, or any "
                "hash/inventory field. If the exact rendered pages are clean, "
                "edit only each receipt's `inspection` object: set "
            )
        else:
            packets = "\n".join(
                f"- Word artifact: `{artifact}`\n"
                f"  Immutable input receipt: `{receipt_input}`\n"
                f"  Approved receipt to write: `{receipt}`"
                for artifact, receipt_input, receipt in zip(
                    artifacts,
                    revision_receipt_inputs,
                    receipts,
                    strict=True,
                )
            )
            receipt_instructions = (
                "Do not edit the Word, PDF, page PNGs, montage, immutable "
                "input receipts, or any hash/inventory field. For each clean "
                "document, write the named approved receipt as an exact copy "
                "of its immutable input receipt except for the `inspection` "
                "object. In that object, set "
            )
        prompt = (
            "Act as the final visual inspector for these airport-executive Word "
            "documents. Each receipt names the exact Word bytes, converted PDF, "
            "every full-size page PNG, and a page-sequence montage:\n\n"
            f"{packets}\n\n"
            "Use Read to inspect every `rendered_pages[].path` image individually "
            "at full size. Then inspect `montage.path` for pacing, page hierarchy, "
            "and accidental blank or stranded pages. Check clipped text, split or "
            "overflowing tables, broken figures, unreadable source notes, awkward "
            "page breaks, inconsistent headers/footers, excessive whitespace, and "
            "anything that would look unfinished to an airport CEO or board. "
            "Do not approve conversion success by itself.\n\n"
            f"{receipt_instructions}`full_size_each_page_inspected`, "
            "`montage_inspected`, and `findings_resolved` to true; set `status` "
            "to `pass`; leave `unresolved_findings` empty; and record observations "
            "or resolved defects in `resolved_findings`. If a defect remains, keep "
            "status pending and name it in `unresolved_findings` so release stops."
        )
        if revision_state_path is None:
            completion = await _run_agent(
                agent=art_director,
                user_prompt=prompt,
                model=_model("art_direction"),
                cwd=outputs_dir.parent,
                step_label=step_label,
                tally=tally,
                output_path=None,
                max_turns=max_turns,
                emit_completion=False,
            )
        else:
            assert revision_repo_root is not None
            art_model = _model("art_direction")
            bound_revision_dependencies = _revision_agent_dependencies(
                repo_root=revision_repo_root,
                agent=art_director,
                inputs=revision_dependencies,
            )
            revision_values = _revision_call_values(
                agent=art_director,
                model=art_model,
                prompt=prompt,
                step_label=step_label,
                extra=revision_extra_values,
            )
            inspection_outputs = (
                (receipts[0], _word_visual_inspection_contract()),
                *tuple(
                    (receipt, _word_visual_inspection_contract())
                    for receipt in receipts[1:]
                ),
            )
            reusable, _ = revision_step_matches(
                state_path=revision_state_path,
                repo_root=revision_repo_root,
                step_id="word-visual-inspection",
                dependencies=bound_revision_dependencies,
                values=revision_values,
                outputs=inspection_outputs,
            )
            if not reusable:
                # The approved receipt is both the inspector's result and a
                # release gate, so never feed a stale approved receipt back to
                # the model. Re-render exact Word bytes and prepare a separate
                # immutable pending receipt for each document.
                from cli.publishing_quality import (
                    prepare_word_visual_inspection_receipt,
                    render_office_artifact,
                )

                for artifact, receipt_input in zip(
                    artifacts,
                    revision_receipt_inputs,
                    strict=True,
                ):
                    rendered, render_issues = render_office_artifact(
                        artifact,
                        artifact.parent / "qa" / artifact.stem,
                        required=True,
                    )
                    if any(
                        issue.severity == "error"
                        for issue in render_issues
                    ):
                        raise RuntimeError(
                            "Revision Word inspection could not prepare a "
                            f"complete render packet for {artifact.name}."
                        )
                    prepare_word_visual_inspection_receipt(
                        artifact=artifact,
                        rendered_files=rendered,
                        receipt_path=receipt_input,
                    )
            completion = await _run_revision_agent(
                state_path=revision_state_path,
                repo_root=revision_repo_root,
                step_id="word-visual-inspection",
                agent=art_director,
                user_prompt=prompt,
                model=art_model,
                step_label=step_label,
                tally=tally,
                output_path=receipts[0],
                artifact_contract=_word_visual_inspection_contract(),
                required_outputs=tuple(
                    (receipt, _word_visual_inspection_contract())
                    for receipt in receipts[1:]
                ),
                dependencies=revision_dependencies,
                emit_completion=False,
                extra_values=revision_extra_values,
            )
        reports = inspection_reports()

    inspection_metadata: list[dict[str, object]] = []
    for artifact, receipt, report in zip(
        artifacts, receipts, reports, strict=True
    ):
        if manifest_path is not None:
            artifact_id = (
                "stage4/executive-summary-visual-inspection"
                if artifact.stem.endswith("-executive-summary")
                else "stage4/word-visual-inspection"
            )
            validation = validate_artifact(
                receipt,
                _word_visual_inspection_contract(),
            )
            if not report.ok:
                validation.valid = False
                validation.errors.extend(
                    f"{issue.code}: {issue.message}"
                    for issue in report.errors
                )
            update_artifact(
                manifest_path,
                receipt,
                validation,
                artifact_id=artifact_id,
                producer="art-director",
            )
            await emit(
                "artifact_validated",
                step=f"{step_label}/{artifact.stem}",
                **validation.to_dict(),
            )
        assert_quality(report)
        inspection_metadata.append(
            {
                "artifact": str(artifact),
                "receipt": str(receipt),
                **report.metadata,
            }
        )

    quality_path = outputs_dir / "publishing-quality.json"
    if quality_path.is_file():
        quality_payload = json.loads(
            quality_path.read_text(encoding="utf-8")
        )
        quality_payload.setdefault("metadata", {})[
            "word_visual_inspections"
        ] = inspection_metadata
        temporary = quality_path.with_name(f".{quality_path.name}.tmp")
        temporary.write_text(
            json.dumps(quality_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, quality_path)

    if not completion.get("skipped"):
        cost = completion.get("cost")
        turns = completion.get("turns")
        console.print(
            f"  [green]✓ {step_label} done[/green] "
            f"[dim](${float(cost or 0):.2f}, {turns or 0} turns)[/dim]"
        )
        await emit(
            "agent_done",
            step=step_label,
            agent=art_director.name,
            cost=cost,
            turns=turns,
            total=tally.total,
            provider=completion.get("provider"),
            billed_separately=bool(completion.get("billed_separately", False)),
        )


async def run_presentation(
    spec: RunSpec,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path,
) -> None:
    """Generate the companion executive PowerPoint via the presentation agent."""
    by_name = {a.name: a for a in all_agents}
    designer = by_name["presentation-designer"]
    out_path = outputs_dir / "stage4" / f"{spec.slug}.pptx"
    receipt_path = (
        outputs_dir / "stage4" / f"{spec.slug}-visual-inspection.json"
    )
    inspection_dir = outputs_dir / "stage4" / "inspection" / spec.slug
    deck_mode = str(getattr(spec, "deck_mode", "board_decision"))
    prompt = (
        f"Build the companion executive presentation for the report titled "
        f"\"{spec.title}\".\n\n"
        f"Source material (read all):\n"
        f"- Final draft: `outputs/stage3/final-draft.md`\n"
        f"- Fact-check report: `outputs/stage3/fact-check-report.md`\n"
        f"- Art direction and slide contract: `outputs/stage4/visual-brief.json`\n"
        f"- Claim lineage: `outputs/claim-lineage.jsonl`\n"
        f"- Evidence ledger: `outputs/evidence-ledger.jsonl`\n"
        f"- Airport context: `outputs/context/airport-context.md`\n"
        f"- Run manifest: `outputs/run-manifest.json`\n"
        f"- Run prompt: `prompts/runs/{spec.slug}.md`\n\n"
        f"Save the finished deck to: `{out_path}`\n"
        f"The repo's Python interpreter with python-pptx installed is at "
        f"`.venv/bin/python` — use it for your build script.\n\n"
        "Your work is not complete when the PPTX merely opens. Run this exact "
        "inspection-packet workflow after building it:\n\n"
        f"`.venv/bin/python -m cli.presentation_qa \"{out_path}\" "
        f"--mode {deck_mode} "
        f"--visual-brief \"{outputs_dir / 'stage4' / 'visual-brief.json'}\" "
        f"--json \"{inspection_dir / 'designer-qa.json'}\" "
        f"--render-dir \"{inspection_dir}\" "
        f"--prepare-inspection \"{receipt_path}\"`\n\n"
        "Then inspect every rendered slide PNG individually at full size and "
        "inspect `montage.png` for narrative rhythm. Fix every defect and rerun "
        "the command if the deck bytes change. Only after the exact final bytes "
        "are clean, confirm that the exact slide named by "
        "`signature_visual.slide_number` contains the primary exhibit and name "
        f"that exhibit or group with the reserved prefix "
        f"`SIGNATURE VISUAL —`. Edit only the receipt's `inspection` object: set "
        "`full_size_each_slide_inspected`, `montage_inspected`, and "
        "`signature_exhibit_present`, `signature_exhibit_matches_brief`, and "
        "`findings_resolved` to true; set `status` to `pass`; leave "
        "`unresolved_findings` empty; and describe material fixes in "
        "`resolved_findings`. The receipt hashes must never be edited by hand."
    )
    completion = await _run_agent(
        agent=designer,
        user_prompt=prompt,
        model=_model("presentation"),
        cwd=outputs_dir.parent,
        step_label="stage4/presentation",
        tally=tally,
        output_path=out_path,
        manifest_path=manifest_path,
        artifact_id="stage4/presentation",
        required_outputs=((receipt_path, _visual_inspection_contract()),),
        dependency_inputs=tuple(
            item.format(slug=spec.slug) for item in next(
                step
                for step in PIPELINE_DEFINITION
                if step.id == "presentation"
            ).inputs
        ),
        emit_completion=False,
    )
    from cli.presentation_qa import (
        qa_presentation,
        qa_visual_inspection_receipt,
    )
    from cli.publishing_quality import assert_quality

    qa_path = outputs_dir / "stage4" / f"{spec.slug}-qa.json"
    qa_report = qa_presentation(
        out_path,
        render_dir=outputs_dir / "stage4" / "qa" / f"{spec.slug}-presentation",
        deck_mode=deck_mode,
        visual_brief=outputs_dir / "stage4" / "visual-brief.json",
    )
    inspection_report = qa_visual_inspection_receipt(
        receipt_path,
        artifact=out_path,
        visual_brief=outputs_dir / "stage4" / "visual-brief.json",
        deck_mode=deck_mode,
    )
    qa_report.issues.extend(inspection_report.issues)
    qa_report.metadata["visual_inspection"] = inspection_report.metadata
    qa_report.write_json(qa_path)
    qa_contract = ArtifactContract(
        "json",
        required_keys=("artifact", "kind", "ok", "issues"),
    )
    qa_validation = validate_artifact(qa_path, qa_contract)
    update_artifact(
        manifest_path,
        qa_path,
        qa_validation,
        artifact_id="stage4/presentation-qa",
        producer="orchestrator",
    )
    await emit(
        "render_qa",
        artifact=str(out_path),
        status="passed" if qa_report.ok else "failed",
        issues=len(qa_report.issues),
        errors=len(qa_report.errors),
        warnings=len(qa_report.warnings),
        rendered_files=qa_report.rendered_files,
    )
    if not qa_report.ok:
        await emit(
            "agent_error",
            step="stage4/presentation",
            agent=designer.name,
            error_type="PresentationQAError",
            message="; ".join(issue.message for issue in qa_report.errors[:8]),
        )
        _quarantine_partial_output(out_path)
        _quarantine_partial_output(receipt_path)
    assert_quality(qa_report)
    if not completion.get("skipped"):
        cost = completion.get("cost")
        turns = completion.get("turns")
        console.print(
            f"  [green]✓ stage4/presentation done[/green] "
            f"[dim](${float(cost or 0):.2f}, {turns or 0} turns)[/dim]"
        )
        await emit(
            "agent_done",
            step="stage4/presentation",
            agent=designer.name,
            cost=cost,
            turns=turns,
            total=tally.total,
            provider=completion.get("provider"),
            billed_separately=bool(completion.get("billed_separately", False)),
        )


def _remove_backfill_path(path: Path) -> None:
    """Remove one transaction target without following directory symlinks."""

    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _backfill_render_hashes(render_dir: Path) -> dict[str, str | None]:
    """Return a deterministic content inventory for a rendered deck."""

    if not render_dir.is_dir():
        return {}
    return {
        path.relative_to(render_dir).as_posix(): file_sha256(path)
        for path in sorted(render_dir.rglob("*"))
        if path.is_file()
    }


def _write_backfill_state(path: Path, payload: dict) -> None:
    """Atomically persist resumable deck-backfill state."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _presentation_backfill_identity(
    *,
    archive_dir: Path,
    slug: str,
    title: str,
    repo_root: Path,
    art_director: Agent,
    designer: Agent,
) -> tuple[dict[str, object], str, dict[str, Path], str]:
    """Recompute the complete deck-backfill identity from live disk."""

    run_prompt = archive_dir / "run-prompt.md"
    if not run_prompt.is_file():
        run_prompt = repo_root / "prompts" / "runs" / f"{slug}.md"
    ledger_path = archive_dir / "evidence-ledger.jsonl"
    if not ledger_path.is_file():
        ledger_path = archive_dir / "stage1" / "evidence-ledger.jsonl"
    source_paths = {
        "run_prompt": run_prompt,
        "final_draft": archive_dir / "stage3" / "final-draft.md",
        "fact_check_report": (
            archive_dir / "stage3" / "fact-check-report.md"
        ),
        "evidence_ledger": ledger_path,
        "claim_lineage": archive_dir / "claim-lineage.jsonl",
        "airport_context": (
            archive_dir / "context" / "airport-context.md"
        ),
        "archived_run_manifest": archive_dir / "run-manifest.json",
    }
    archived_manifest = source_paths["archived_run_manifest"]
    deck_mode = "board_decision"
    if archived_manifest.is_file():
        try:
            deck_mode = str(
                json.loads(archived_manifest.read_text(encoding="utf-8"))
                .get("run", {})
                .get("deck_mode")
                or deck_mode
            )
        except (OSError, json.JSONDecodeError):
            pass
    if deck_mode not in {
        "board_decision",
        "executive_briefing",
        "technical_read_ahead",
    }:
        deck_mode = "board_decision"

    def relative(path: Path) -> str:
        try:
            return path.relative_to(repo_root).as_posix()
        except ValueError:
            return str(path)

    payload: dict[str, object] = {
        "schema_version": "3.0",
        "slug": slug,
        "title": title,
        "archive": str(archive_dir),
        "deck_mode": deck_mode,
        "sources": {
            name: file_sha256(path)
            for name, path in source_paths.items()
        },
        "models": {
            "art_direction": _model("art_direction"),
            "presentation": _model("presentation"),
        },
        "agent_charters": {
            "art-director": {
                "path": relative(art_director.path),
                "sha256": file_sha256(art_director.path),
            },
            "presentation-designer": {
                "path": relative(designer.path),
                "sha256": file_sha256(designer.path),
            },
        },
        "execution_contract": build_execution_contract_fingerprint(
            repo_root
        ),
        "visual_inspection_contract": "1.0",
    }
    identity = hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return payload, identity, source_paths, deck_mode


def _assert_presentation_backfill_precommit(
    *,
    archive_dir: Path,
    slug: str,
    title: str,
    repo_root: Path,
    art_director: Agent,
    designer: Agent,
    expected_payload: dict[str, object],
    expected_identity: str,
    backfill_state: dict[str, object],
    visual_path: Path,
    out_path: Path,
    qa_path: Path,
    receipt_path: Path,
    qa_render_dir: Path,
    inspection_dir: Path,
) -> None:
    """Fail closed if any source, contract, or inspected output changed."""

    current_payload, current_identity, _, _ = (
        _presentation_backfill_identity(
            archive_dir=archive_dir,
            slug=slug,
            title=title,
            repo_root=repo_root,
            art_director=art_director,
            designer=designer,
        )
    )
    if (
        current_identity != expected_identity
        or current_payload != expected_payload
    ):
        raise RuntimeError(
            "Deck backfill source, model, charter, or execution identity "
            "changed before publication."
        )
    expected_outputs = {
        "visual_brief_sha256": file_sha256(visual_path),
        "presentation_sha256": file_sha256(out_path),
        "presentation_qa_sha256": file_sha256(qa_path),
        "visual_inspection_sha256": file_sha256(receipt_path),
        "qa_render_files": _backfill_render_hashes(qa_render_dir),
        "inspection_render_files": _backfill_render_hashes(inspection_dir),
    }
    mismatched = [
        key
        for key, current in expected_outputs.items()
        if backfill_state.get(key) != current
    ]
    if mismatched:
        raise RuntimeError(
            "Deck backfill inspected outputs changed before publication: "
            + ", ".join(mismatched)
        )


def _publish_presentation_backfill_release(
    *,
    archive_dir: Path,
    slug: str,
    title: str,
    repo_root: Path,
    art_director: Agent,
    designer: Agent,
    expected_payload: dict[str, object],
    expected_identity: str,
    backfill_state: dict[str, object],
    stage4: Path,
    visual_path: Path,
    out_path: Path,
    qa_path: Path,
    receipt_path: Path,
    qa_render_dir: Path,
    inspection_dir: Path,
    release_dir: Path,
    deck_mode: str,
    out_dir: Path,
) -> dict[str, Path]:
    """Stage and promote a backfill only while its live identity is stable."""

    from cli.publish import promote_release, stage_release_artifacts

    guard = {
        "archive_dir": archive_dir,
        "slug": slug,
        "title": title,
        "repo_root": repo_root,
        "art_director": art_director,
        "designer": designer,
        "expected_payload": expected_payload,
        "expected_identity": expected_identity,
        "backfill_state": backfill_state,
        "visual_path": visual_path,
        "out_path": out_path,
        "qa_path": qa_path,
        "receipt_path": receipt_path,
        "qa_render_dir": qa_render_dir,
        "inspection_dir": inspection_dir,
    }
    _assert_presentation_backfill_precommit(**guard)
    if not _staged_presentation_release_matches_sources(
        release_dir=release_dir,
        staged_stage4=stage4,
        slug=slug,
    ):
        stage_release_artifacts(
            stage4_dir=stage4,
            slug=slug,
            release_dir=release_dir,
            require_presentation=True,
            include_roles={"presentation"},
            presentation_mode=deck_mode,
            visual_brief=visual_path,
            require_visual_inspection=True,
        )
    _assert_presentation_backfill_precommit(**guard)
    return promote_release(
        release_dir=release_dir,
        out_dir=out_dir,
        release_manifest_name=f"{slug}-deck-release-manifest.json",
        reconcile_roles=False,
    )


def _commit_presentation_backfill_archive(
    *,
    archive_dir: Path,
    slug: str,
    title: str,
    repo_root: Path,
    art_director: Agent,
    designer: Agent,
    expected_payload: dict[str, object],
    expected_identity: str,
    backfill_state: dict[str, object],
    visual_path: Path,
    out_path: Path,
    qa_path: Path,
    receipt_path: Path,
    qa_render_dir: Path,
    inspection_dir: Path,
    staged_stage4: Path,
    archive_stage4: Path,
) -> dict[str, Path]:
    """Recheck the paid work immediately before mutating the run archive."""

    _assert_presentation_backfill_precommit(
        archive_dir=archive_dir,
        slug=slug,
        title=title,
        repo_root=repo_root,
        art_director=art_director,
        designer=designer,
        expected_payload=expected_payload,
        expected_identity=expected_identity,
        backfill_state=backfill_state,
        visual_path=visual_path,
        out_path=out_path,
        qa_path=qa_path,
        receipt_path=receipt_path,
        qa_render_dir=qa_render_dir,
        inspection_dir=inspection_dir,
    )
    return _promote_archive_backfill(
        staged_stage4=staged_stage4,
        archive_stage4=archive_stage4,
        slug=slug,
    )


def _assert_archive_allows_deck_backfill(
    *,
    archive_dir: Path,
    slug: str,
    staged_stage4: Path | None = None,
) -> Path | None:
    """Refuse replacement, while recognizing resumable manifest-last commits.

    Returns the archived deck when a complete durable backfill is already
    committed. A raw deck without its manifest is accepted only when an exact,
    validated staging transaction remains available to finish the interrupted
    commit.
    """

    release_manifest = archive_dir / "release" / "release-manifest.json"
    if release_manifest.is_file():
        try:
            release_payload = json.loads(
                release_manifest.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                "Cannot establish deck-backfill eligibility because the "
                "archived canonical release manifest is invalid."
            ) from exc
        if any(
            str(item.get("role") or "") == "presentation"
            for item in release_payload.get("artifacts", [])
            if isinstance(item, dict)
        ):
            raise RuntimeError(
                "This archive already has a canonical presentation. Deck "
                "backfill only fills a missing deck; replacement requires an "
                "explicit future replacement workflow."
            )

    archived_deck = archive_dir / "stage4" / f"{slug}.pptx"
    if archived_deck.exists() or archived_deck.is_symlink():
        if archived_deck.is_symlink():
            raise RuntimeError(
                "Archived presentation is a symlink; refusing deck recovery."
            )
        archived_backfill = (
            archive_dir / "stage4" / f"{slug}-deck-backfill.json"
        )
        archived_supplement = (
            archive_dir / "release-supplements" / "deck"
        )
        if (
            archived_backfill.is_file()
            and (archived_supplement / "release-manifest.json").is_file()
        ):
            from cli.publish import _verify_archived_deck_supplement_binding

            _verify_archived_deck_supplement_binding(
                archive_dir=archive_dir,
                slug=slug,
                deck_supplement=archived_supplement,
            )
            return archived_deck

        if staged_stage4 is not None:
            try:
                _validate_staged_backfill(
                    staged_stage4=staged_stage4,
                    slug=slug,
                )
            except (OSError, RuntimeError, ValueError):
                pass
            else:
                # Manifest-last archive commit was interrupted. The paid,
                # hash-bound staging transaction is authoritative and can
                # safely replace the partial archive targets on resume.
                return None
        raise RuntimeError(
            "This archive already has a presentation. Deck backfill only "
            "fills a missing deck; replacement requires an explicit future "
            "replacement workflow."
        )
    return None


def _validate_staged_backfill(
    *,
    staged_stage4: Path,
    slug: str,
) -> dict:
    """Verify the hash-bound backfill record before archive mutation."""

    manifest = staged_stage4 / f"{slug}-deck-backfill.json"
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid staged deck backfill manifest: {exc}") from exc

    expected_files = {
        "visual_brief": (
            "stage4/deck-backfill/visual-brief.json",
            staged_stage4 / "deck-backfill" / "visual-brief.json",
        ),
        "presentation": (
            f"stage4/{slug}.pptx",
            staged_stage4 / f"{slug}.pptx",
        ),
        "presentation_qa": (
            f"stage4/{slug}-qa.json",
            staged_stage4 / f"{slug}-qa.json",
        ),
        "visual_inspection": (
            f"stage4/{slug}-visual-inspection.json",
            staged_stage4 / f"{slug}-visual-inspection.json",
        ),
    }
    artifacts = payload.get("artifacts")
    if payload.get("schema_version") != "3.0":
        raise RuntimeError("Backfill manifest schema must be 3.0.")
    if payload.get("slug") != slug or not isinstance(artifacts, dict):
        raise RuntimeError("Backfill manifest has no artifact inventory.")
    for role, (relative, path) in expected_files.items():
        record = artifacts.get(role)
        if (
            not isinstance(record, dict)
            or record.get("path") != relative
            or not path.is_file()
            or record.get("sha256") != file_sha256(path)
        ):
            raise RuntimeError(
                f"Backfill artifact hash mismatch before archive commit: {role}"
            )

    render_dir = staged_stage4 / "qa" / f"{slug}-presentation"
    render_record = artifacts.get("qa_render")
    if (
        not isinstance(render_record, dict)
        or render_record.get("path")
        != f"stage4/qa/{slug}-presentation"
        or render_record.get("files") != _backfill_render_hashes(render_dir)
    ):
        raise RuntimeError(
            "Backfill render inventory mismatch before archive commit."
        )
    inspection_dir = staged_stage4 / "inspection" / slug
    inspection_record = artifacts.get("inspection_render")
    if (
        not isinstance(inspection_record, dict)
        or inspection_record.get("path")
        != f"stage4/inspection/{slug}"
        or inspection_record.get("files")
        != _backfill_render_hashes(inspection_dir)
    ):
        raise RuntimeError(
            "Backfill visual-inspection inventory mismatch before archive "
            "commit."
        )
    from cli.presentation_qa import qa_visual_inspection_receipt

    inspection_report = qa_visual_inspection_receipt(
        staged_stage4 / f"{slug}-visual-inspection.json",
        artifact=staged_stage4 / f"{slug}.pptx",
        visual_brief=(
            staged_stage4 / "deck-backfill" / "visual-brief.json"
        ),
        deck_mode=str(payload.get("deck_mode") or ""),
    )
    if not inspection_report.ok:
        raise RuntimeError(
            "Backfill visual-inspection receipt is not passing: "
            + "; ".join(
                issue.message for issue in inspection_report.errors[:8]
            )
        )
    if payload.get("qa_ok") is not True:
        raise RuntimeError("Backfill manifest does not record passing QA.")
    release_dir = staged_stage4.parent / "release"
    release_record = artifacts.get("release_supplement")
    if (
        not isinstance(release_record, dict)
        or release_record.get("path") != "release-supplements/deck"
        or release_record.get("files")
        != _backfill_render_hashes(release_dir)
    ):
        raise RuntimeError(
            "Backfill release-supplement inventory mismatch before archive "
            "commit."
        )
    from cli.publish import verify_release_bundle

    release_payload = verify_release_bundle(
        release_dir,
        require_word_report=False,
    )
    if (
        str(release_payload.get("slug") or "") != slug
        or {
            str(item.get("role") or "")
            for item in release_payload.get("artifacts", [])
        }
        != {"presentation"}
    ):
        raise RuntimeError(
            "Backfill release supplement is not a deck-only bundle for this "
            "slug."
        )
    return payload


def _staged_presentation_release_matches_sources(
    *,
    release_dir: Path,
    staged_stage4: Path,
    slug: str,
) -> bool:
    """Return whether a durable deck release still binds the exact sources.

    A resumed backfill may have crossed the reports-promotion boundary but not
    the archive-commit boundary. Rebuilding the release manifest in that case
    changes its hash and creates a second immutable bundle for identical work.
    Reuse is safe only when the complete bundle verifies and every
    presentation-inspection source still matches the staged transaction.
    """

    from cli.publish import verify_release_bundle

    try:
        payload = verify_release_bundle(
            release_dir,
            require_word_report=False,
        )
        artifacts = payload.get("artifacts")
        if (
            payload.get("slug") != slug
            or not isinstance(artifacts, list)
            or len(artifacts) != 1
        ):
            return False
        artifact = artifacts[0]
        if (
            not isinstance(artifact, dict)
            or artifact.get("role") != "presentation"
            or artifact.get("source_path") != f"stage4/{slug}.pptx"
        ):
            return False

        presentation = staged_stage4 / f"{slug}.pptx"
        visual_brief = (
            staged_stage4 / "deck-backfill" / "visual-brief.json"
        )
        receipt = (
            staged_stage4 / f"{slug}-visual-inspection.json"
        )
        inspection_dir = staged_stage4 / "inspection" / slug
        if not all(
            path.is_file()
            for path in (presentation, visual_brief, receipt)
        ) or not inspection_dir.is_dir():
            return False
        if artifact.get("source_sha256") != file_sha256(presentation):
            return False

        requirements = payload.get("requirements")
        if not isinstance(requirements, dict) or not (
            requirements.get("presentation") is True
            and requirements.get("visual_inspection") is True
            and requirements.get("word_visual_inspection") is False
        ):
            return False
        inspection = artifact.get("visual_inspection")
        if (
            not isinstance(inspection, dict)
            or inspection.get("type") != "presentation_slides"
            or inspection.get("sha256") != file_sha256(receipt)
            or inspection.get("visual_brief_sha256")
            != file_sha256(visual_brief)
        ):
            return False

        expected_files = {
            (
                Path("inspection")
                / slug
                / path.relative_to(inspection_dir)
            ).as_posix(): (
                file_sha256(path),
                path.stat().st_size,
            )
            for path in sorted(inspection_dir.rglob("*"))
            if path.is_file()
        }
        recorded_files = inspection.get("files")
        if not isinstance(recorded_files, list):
            return False
        actual_files = {
            str(item.get("path") or ""): (
                str(item.get("sha256") or ""),
                item.get("size_bytes"),
            )
            for item in recorded_files
            if isinstance(item, dict)
        }
        return actual_files == expected_files
    except (FileNotFoundError, OSError, RuntimeError, ValueError, TypeError):
        return False


def _promote_archive_backfill(
    *,
    staged_stage4: Path,
    archive_stage4: Path,
    slug: str,
) -> dict[str, Path]:
    """Commit a validated deck backfill to an archive with full rollback.

    Only the deck-specific transaction targets are replaced. Existing Word
    artifacts and all unrelated archived files remain untouched.
    """

    _validate_staged_backfill(staged_stage4=staged_stage4, slug=slug)
    source_operations = [
        (
            "visual_brief",
            staged_stage4 / "deck-backfill" / "visual-brief.json",
            archive_stage4 / "deck-backfill" / "visual-brief.json",
        ),
        (
            "presentation",
            staged_stage4 / f"{slug}.pptx",
            archive_stage4 / f"{slug}.pptx",
        ),
        (
            "presentation_qa",
            staged_stage4 / f"{slug}-qa.json",
            archive_stage4 / f"{slug}-qa.json",
        ),
        (
            "qa_render",
            staged_stage4 / "qa" / f"{slug}-presentation",
            archive_stage4 / "qa" / f"{slug}-presentation",
        ),
        (
            "visual_inspection",
            staged_stage4 / f"{slug}-visual-inspection.json",
            archive_stage4 / f"{slug}-visual-inspection.json",
        ),
        (
            "inspection_render",
            staged_stage4 / "inspection" / slug,
            archive_stage4 / "inspection" / slug,
        ),
        (
            "release_supplement",
            staged_stage4.parent / "release",
            archive_stage4.parent / "release-supplements" / "deck",
        ),
        (
            "backfill_manifest",
            staged_stage4 / f"{slug}-deck-backfill.json",
            archive_stage4 / f"{slug}-deck-backfill.json",
        ),
    ]
    missing = [
        str(source)
        for _, source, _ in source_operations
        if not source.exists()
    ]
    if missing:
        raise FileNotFoundError(
            "Staged deck backfill is incomplete: " + ", ".join(missing)
        )

    archive_stage4.mkdir(parents=True, exist_ok=True)
    transaction = Path(
        tempfile.mkdtemp(prefix=f".{slug}-backfill-commit-", dir=archive_stage4)
    )
    backups = transaction / "backups"
    backups.mkdir()
    commit_staged = transaction / "staged"
    commit_staged.mkdir()
    operations: list[tuple[str, Path, Path]] = []
    promoted: list[Path] = []
    backed_up: list[tuple[Path, Path]] = []
    created_parents: list[Path] = []
    try:
        # Copy every source into the commit transaction before touching the
        # archive. The durable staging tree remains resumable even if the
        # archive commit later fails.
        for index, (role, source, destination) in enumerate(source_operations):
            commit_source = commit_staged / f"{index:02d}-{source.name}"
            if source.is_dir() and not source.is_symlink():
                shutil.copytree(source, commit_source)
                if _backfill_render_hashes(commit_source) != (
                    _backfill_render_hashes(source)
                ):
                    raise RuntimeError(
                        f"Backfill commit staging changed directory bytes: {role}"
                    )
            else:
                shutil.copy2(source, commit_source)
                if file_sha256(commit_source) != file_sha256(source):
                    raise RuntimeError(
                        f"Backfill commit staging changed file bytes: {role}"
                    )
            operations.append((role, commit_source, destination))

        for index, (role, source, destination) in enumerate(operations):
            parent = destination.parent
            if not parent.exists():
                parent.mkdir(parents=True)
                created_parents.append(parent)
            if destination.exists() or destination.is_symlink():
                backup = backups / f"{index:02d}-{destination.name}"
                os.replace(destination, backup)
                backed_up.append((destination, backup))
            os.replace(source, destination)
            promoted.append(destination)

        # Verify the exact committed bytes before the manifest-last operation
        # is considered authoritative.
        for (role, original, _), (_, _, destination) in zip(
            source_operations,
            operations,
            strict=True,
        ):
            if original.is_dir() and not original.is_symlink():
                matches = _backfill_render_hashes(destination) == (
                    _backfill_render_hashes(original)
                )
            else:
                matches = file_sha256(destination) == file_sha256(original)
            if not matches:
                raise RuntimeError(
                    f"Backfill archive commit changed artifact bytes: {role}"
                )

        committed = {
            role: destination
            for role, _, destination in operations
        }
        # A hard process crash can strand a prior transaction directory.
        # Once a complete newer supplement is committed, those backups are no
        # longer authoritative and can be removed safely.
        for stale in archive_stage4.glob(
            f".{slug}-backfill-commit-*"
        ):
            if stale != transaction:
                shutil.rmtree(stale, ignore_errors=True)
        return committed
    except Exception:
        for destination in reversed(promoted):
            if destination.exists() or destination.is_symlink():
                _remove_backfill_path(destination)
        for destination, backup in reversed(backed_up):
            if backup.exists() or backup.is_symlink():
                os.replace(backup, destination)
        for parent in reversed(created_parents):
            try:
                parent.rmdir()
            except OSError:
                pass
        raise
    finally:
        shutil.rmtree(transaction, ignore_errors=True)


def _archived_council_model(archive_dir: Path) -> CouncilModel | None:
    """Recover the immutable run-level route for revisions and deck backfills."""

    manifest = archive_dir / "run-manifest.json"
    if not manifest.is_file():
        return None
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    run = payload.get("run") if isinstance(payload, dict) else None
    model_id = run.get("council_model", "") if isinstance(run, dict) else ""
    return council_model(str(model_id or ""))


async def run_presentation_for_archive(
    *,
    archive_dir: Path,
    slug: str,
    title: str,
    repo_root: Path,
    budget_usd: float | None = None,
) -> Path:
    selected = _archived_council_model(archive_dir)
    token = _ACTIVE_COUNCIL_MODEL.set(selected)
    try:
        return await _run_presentation_for_archive(
            archive_dir=archive_dir,
            slug=slug,
            title=title,
            repo_root=repo_root,
            budget_usd=budget_usd,
        )
    finally:
        _ACTIVE_COUNCIL_MODEL.reset(token)


async def _run_presentation_for_archive(
    *,
    archive_dir: Path,
    slug: str,
    title: str,
    repo_root: Path,
    budget_usd: float | None = None,
) -> Path:
    """Backfill a deck through a durable, resumable staging transaction."""

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,127}", slug):
        raise ValueError(f"Unsafe deck-backfill slug: {slug!r}")
    archive_dir = archive_dir.resolve()
    staging_root = (
        repo_root.resolve() / "logs" / "deck-backfills" / slug
    ).resolve()
    approved_root = (
        repo_root.resolve() / "logs" / "deck-backfills"
    ).resolve()
    try:
        staging_root.relative_to(approved_root)
    except ValueError as exc:
        raise ValueError(f"Unsafe deck-backfill slug: {slug!r}") from exc
    committed_deck = _assert_archive_allows_deck_backfill(
        archive_dir=archive_dir,
        slug=slug,
        staged_stage4=staging_root / "stage4",
    )
    if committed_deck is not None:
        from cli.publish import REPORTS_DIR, promote_release

        published = promote_release(
            release_dir=(
                archive_dir / "release-supplements" / "deck"
            ),
            out_dir=REPORTS_DIR,
            release_manifest_name=f"{slug}-deck-release-manifest.json",
            reconcile_roles=False,
        )
        shutil.rmtree(staging_root, ignore_errors=True)
        return published["presentation"]
    staging_root.mkdir(parents=True, exist_ok=True)
    state_path = staging_root / "state.json"
    try:
        result = await _build_presentation_backfill(
            archive_dir=archive_dir,
            slug=slug,
            title=title,
            repo_root=repo_root.resolve(),
            staging_root=staging_root,
            budget_usd=budget_usd,
        )
    except BaseException as exc:
        try:
            state = (
                json.loads(state_path.read_text(encoding="utf-8"))
                if state_path.is_file()
                else {}
            )
        except (OSError, json.JSONDecodeError):
            state = {}
        state.update(
            {
                "status": "interrupted",
                "error_type": type(exc).__name__,
                "updated_at": datetime.now()
                .astimezone()
                .isoformat(timespec="seconds"),
            }
        )
        _write_backfill_state(state_path, state)
        raise
    shutil.rmtree(staging_root, ignore_errors=True)
    return result


async def _build_presentation_backfill(
    *,
    archive_dir: Path,
    slug: str,
    title: str,
    repo_root: Path,
    staging_root: Path,
    budget_usd: float | None = None,
) -> Path:
    """Build and validate one deck in an isolated staging tree."""

    from cli.presentation_qa import (
        qa_presentation,
        qa_visual_inspection_receipt,
    )
    from cli.publish import (
        REPORTS_DIR,
    )
    from cli.publishing_quality import assert_quality

    all_agents = load_all_agents()
    by_name = {a.name: a for a in all_agents}
    art_director = by_name["art-director"]
    designer = by_name["presentation-designer"]

    def relative(path: Path) -> str:
        try:
            return path.relative_to(repo_root).as_posix()
        except ValueError:
            return str(path)

    identity_payload, identity, source_paths, deck_mode = (
        _presentation_backfill_identity(
            archive_dir=archive_dir,
            slug=slug,
            title=title,
            repo_root=repo_root,
            art_director=art_director,
            designer=designer,
        )
    )
    run_prompt = source_paths["run_prompt"]
    final_path = source_paths["final_draft"]
    factcheck_path = source_paths["fact_check_report"]
    ledger_path = source_paths["evidence_ledger"]
    lineage_path = source_paths["claim_lineage"]
    context_path = source_paths["airport_context"]
    archived_manifest = source_paths["archived_run_manifest"]
    if not final_path.is_file() or not ledger_path.is_file():
        raise FileNotFoundError(
            "Deck backfill requires the archived final draft and canonical "
            f"evidence ledger; missing under {archive_dir}."
        )
    source_fingerprints = dict(identity_payload["sources"])
    captured_art_model = str(
        dict(identity_payload["models"])["art_direction"]
    )
    captured_presentation_model = str(
        dict(identity_payload["models"])["presentation"]
    )
    state_path = staging_root / "state.json"
    try:
        prior_state = (
            json.loads(state_path.read_text(encoding="utf-8"))
            if state_path.is_file()
            else {}
        )
    except (OSError, json.JSONDecodeError):
        prior_state = {}
    existing_staged_work = any(
        (staging_root / name).exists()
        or (staging_root / name).is_symlink()
        for name in ("stage4", "release")
    )
    if (
        existing_staged_work
        and (
            not prior_state
            or prior_state.get("identity_sha256") != identity
        )
    ):
        stale = (
            staging_root
            / "stale"
            / datetime.now().strftime("%Y%m%dT%H%M%S%f")
        )
        stale.mkdir(parents=True, exist_ok=True)
        for name in ("stage4", "release", "state.json"):
            existing = staging_root / name
            if existing.exists() or existing.is_symlink():
                os.replace(existing, stale / name)
        prior_state = {}
    elif prior_state and prior_state.get("identity_sha256") != identity:
        prior_state = {}

    prior_costs = prior_state.get("cost_by_step", {})
    tally = CostTally(
        by_step={
            str(step): float(cost)
            for step, cost in (
                prior_costs.items()
                if isinstance(prior_costs, dict)
                else ()
            )
        },
        budget_usd=budget_usd,
    )
    tally.plan_calls(2)
    stage4 = staging_root / "stage4"
    stage4.mkdir(parents=True, exist_ok=True)
    visual_path = stage4 / "deck-backfill" / "visual-brief.json"
    visual_path.parent.mkdir(parents=True, exist_ok=True)
    out_path = stage4 / f"{slug}.pptx"
    qa_path = stage4 / f"{slug}-qa.json"
    receipt_path = stage4 / f"{slug}-visual-inspection.json"
    inspection_dir = stage4 / "inspection" / slug
    qa_render_dir = stage4 / "qa" / f"{slug}-presentation"

    def invalidate_staged_deck() -> None:
        for path in (out_path, qa_path, receipt_path):
            _quarantine_partial_output(path)
        for directory in (inspection_dir, qa_render_dir):
            if directory.is_dir():
                shutil.rmtree(directory)

    recorded_visual_sha = str(
        prior_state.get("visual_brief_sha256") or ""
    )
    if visual_path.is_file() and (
        not recorded_visual_sha
        or file_sha256(visual_path) != recorded_visual_sha
    ):
        _quarantine_partial_output(visual_path)
        invalidate_staged_deck()

    recorded_presentation_sha = str(
        prior_state.get("presentation_sha256") or ""
    )
    recorded_qa_sha = str(
        prior_state.get("presentation_qa_sha256") or ""
    )
    recorded_receipt_sha = str(
        prior_state.get("visual_inspection_sha256") or ""
    )
    recorded_presentation_dependencies = str(
        prior_state.get("presentation_dependencies_sha256") or ""
    )
    expected_presentation_dependencies = (
        hashlib.sha256(
            json.dumps(
                {
                    "backfill_identity_sha256": identity,
                    "visual_brief_sha256": recorded_visual_sha,
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        if recorded_visual_sha
        else ""
    )
    if any(path.is_file() for path in (out_path, qa_path, receipt_path)):
        state_bound = bool(
            recorded_presentation_sha
            and recorded_qa_sha
            and recorded_receipt_sha
            and file_sha256(out_path) == recorded_presentation_sha
            and file_sha256(qa_path) == recorded_qa_sha
            and file_sha256(receipt_path) == recorded_receipt_sha
            and recorded_presentation_dependencies
            == expected_presentation_dependencies
            and _backfill_render_hashes(qa_render_dir)
            == prior_state.get("qa_render_files")
            and _backfill_render_hashes(inspection_dir)
            == prior_state.get("inspection_render_files")
        )
        if not state_bound:
            invalidate_staged_deck()

    backfill_state = {
        **identity_payload,
        "identity_sha256": identity,
        "status": "running",
        "phase": prior_state.get("phase", "art_direction"),
        "started_at": prior_state.get(
            "started_at",
            datetime.now().astimezone().isoformat(timespec="seconds"),
        ),
        "updated_at": datetime.now()
        .astimezone()
        .isoformat(timespec="seconds"),
        "budget_usd": budget_usd,
        "cost_by_step": tally.by_step,
    }
    _write_backfill_state(state_path, backfill_state)

    def journal_backfill_cost(current_tally: CostTally) -> None:
        backfill_state.update(
            {
                "cost_by_step": dict(current_tally.by_step),
                "claude_cost_usd": current_tally.total,
                "last_billed_at": datetime.now()
                .astimezone()
                .isoformat(timespec="seconds"),
                "updated_at": datetime.now()
                .astimezone()
                .isoformat(timespec="seconds"),
            }
        )
        _write_backfill_state(state_path, backfill_state)

    art_prompt = (
        f"Create the canonical visual contract for the archived Council report "
        f"\"{title}\". Read these exact sources:\n"
        f"- Run prompt: `{relative(run_prompt)}`\n"
        f"- Final draft: `{relative(final_path)}`\n"
        f"- Fact-check report: `{relative(factcheck_path)}` (if present)\n"
        f"- Evidence ledger: `{relative(ledger_path)}`\n"
        f"- Claim lineage: `{relative(lineage_path)}` (if present)\n"
        f"- Airport context: `{relative(context_path)}` (if present)\n"
        f"- Archived run manifest: `{relative(archived_manifest)}` (if present)\n\n"
        f"The required deck mode is `{deck_mode}`. Define the visual argument "
        "before slide production. Use only evidence IDs present in the archived "
        "ledger. Include every field required by "
        "`assets/brand/visual-brief.schema.json` and validate against that schema.\n\n"
        f"Write valid JSON to: `{relative(visual_path)}`"
    )
    art_completion = await _run_agent(
        agent=art_director,
        user_prompt=art_prompt,
        model=captured_art_model,
        cwd=repo_root,
        step_label=f"deck/{slug}/art-direction",
        tally=tally,
        output_path=visual_path,
        artifact_contract=_visual_brief_contract(),
        emit_completion=False,
        cost_journal=journal_backfill_cost,
    )
    visual_validation = _validate_visual_brief(
        out_path=visual_path,
        schema_path=repo_root / "assets" / "brand" / "visual-brief.schema.json",
        evidence_ledger=ledger_path,
        requested_mode=deck_mode,
    )
    await emit(
        "artifact_validated",
        step=f"deck/{slug}/visual-brief",
        **visual_validation.to_dict(),
    )
    if not visual_validation.valid:
        await emit(
            "agent_error",
            step=f"deck/{slug}/art-direction",
            agent=art_director.name,
            error_type="VisualBriefContractError",
            message="; ".join(visual_validation.errors[:8]),
        )
        _quarantine_partial_output(visual_path)
        raise RuntimeError(
            "Backfill Art Director brief failed the canonical contract: "
            + "; ".join(visual_validation.errors[:8])
        )
    if not art_completion.get("skipped"):
        await emit(
            "agent_done",
            step=f"deck/{slug}/art-direction",
            agent=art_director.name,
            cost=art_completion.get("cost"),
            turns=art_completion.get("turns"),
            total=tally.total,
            provider=art_completion.get("provider"),
            billed_separately=False,
        )
    current_visual_sha = file_sha256(visual_path)
    if (
        any(path.is_file() for path in (out_path, qa_path, receipt_path))
        and current_visual_sha != recorded_visual_sha
    ):
        invalidate_staged_deck()
    presentation_dependencies_sha256 = hashlib.sha256(
        json.dumps(
            {
                "backfill_identity_sha256": identity,
                "visual_brief_sha256": current_visual_sha,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    backfill_state.update(
        {
            "phase": "art_direction_complete",
            "updated_at": datetime.now()
            .astimezone()
            .isoformat(timespec="seconds"),
            "cost_by_step": tally.by_step,
            "art_direction_dependencies_sha256": identity,
            "visual_brief_sha256": current_visual_sha,
            "presentation_dependencies_sha256": (
                presentation_dependencies_sha256
            ),
        }
    )
    _write_backfill_state(state_path, backfill_state)

    prompt = (
        f"Build the companion executive presentation for the report titled "
        f"\"{title}\".\n\n"
        f"Source material (read all available files):\n"
        f"- Final draft: `{relative(final_path)}`\n"
        f"- Fact-check report: `{relative(factcheck_path)}`\n"
        f"- Canonical Art Director brief: `{relative(visual_path)}`\n"
        f"- Evidence ledger: `{relative(ledger_path)}`\n"
        f"- Claim lineage: `{relative(lineage_path)}`\n"
        f"- Airport context: `{relative(context_path)}`\n"
        f"- Run prompt: `{relative(run_prompt)}`\n\n"
        "Follow the Art Director brief exactly; do not author a replacement. "
        "Use visible sources for every material number and attributed claim.\n\n"
        f"Save the finished deck to: `{relative(out_path)}`\n"
        f"The repo's Python interpreter with python-pptx installed is at "
        f"`.venv/bin/python` — use it for your build script.\n\n"
        "Your work is not complete when the PPTX merely opens. Run this exact "
        "inspection-packet workflow after building it:\n\n"
        f"`.venv/bin/python -m cli.presentation_qa "
        f"\"{relative(out_path)}\" --mode {deck_mode} "
        f"--visual-brief \"{relative(visual_path)}\" "
        f"--json \"{relative(inspection_dir / 'designer-qa.json')}\" "
        f"--render-dir \"{relative(inspection_dir)}\" "
        f"--prepare-inspection \"{relative(receipt_path)}\"`\n\n"
        "Inspect every rendered slide PNG individually at full size and inspect "
        "`montage.png` for narrative rhythm. Fix every defect and rerun the "
        "command if the deck bytes change. Only after the exact final bytes are "
        "clean, confirm that the exact slide named by "
        "`signature_visual.slide_number` contains the primary exhibit named "
        "`SIGNATURE VISUAL — <concept>`. Edit only the receipt's `inspection` "
        "object: set "
        "`full_size_each_slide_inspected`, `montage_inspected`, and "
        "`signature_exhibit_present`, `signature_exhibit_matches_brief`, and "
        "`findings_resolved` to true; set `status` to `pass`; leave "
        "`unresolved_findings` empty; and record material corrections in "
        "`resolved_findings`. Never edit the receipt hashes by hand."
    )
    design_completion = await _run_agent(
        agent=designer,
        user_prompt=prompt,
        model=captured_presentation_model,
        cwd=repo_root,
        step_label=f"deck/{slug}",
        tally=tally,
        output_path=out_path,
        required_outputs=((receipt_path, _visual_inspection_contract()),),
        emit_completion=False,
        cost_journal=journal_backfill_cost,
    )
    qa_report = qa_presentation(
        out_path,
        render_dir=stage4 / "qa" / f"{slug}-presentation",
        deck_mode=deck_mode,
        visual_brief=visual_path,
    )
    inspection_report = qa_visual_inspection_receipt(
        receipt_path,
        artifact=out_path,
        visual_brief=visual_path,
        deck_mode=deck_mode,
    )
    qa_report.issues.extend(inspection_report.issues)
    qa_report.metadata["visual_inspection"] = inspection_report.metadata
    qa_report.write_json(qa_path)
    await emit(
        "render_qa",
        artifact=str(out_path),
        status="passed" if qa_report.ok else "failed",
        issues=len(qa_report.issues),
        errors=len(qa_report.errors),
        warnings=len(qa_report.warnings),
        rendered_files=qa_report.rendered_files,
    )
    if not qa_report.ok:
        await emit(
            "agent_error",
            step=f"deck/{slug}",
            agent=designer.name,
            error_type="PresentationQAError",
            message="; ".join(issue.message for issue in qa_report.errors[:8]),
        )
        _quarantine_partial_output(out_path)
        _quarantine_partial_output(receipt_path)
    assert_quality(qa_report)
    if not design_completion.get("skipped"):
        await emit(
            "agent_done",
            step=f"deck/{slug}",
            agent=designer.name,
            cost=design_completion.get("cost"),
            turns=design_completion.get("turns"),
            total=tally.total,
            provider=design_completion.get("provider"),
            billed_separately=False,
        )
    backfill_state.update(
        {
            "phase": "presentation_qa_complete",
            "updated_at": datetime.now()
            .astimezone()
            .isoformat(timespec="seconds"),
            "cost_by_step": tally.by_step,
            "presentation_sha256": file_sha256(out_path),
            "presentation_qa_sha256": file_sha256(qa_path),
            "visual_inspection_sha256": file_sha256(receipt_path),
            "qa_render_files": _backfill_render_hashes(
                stage4 / "qa" / f"{slug}-presentation"
            ),
            "inspection_render_files": _backfill_render_hashes(
                inspection_dir
            ),
        }
    )
    _write_backfill_state(state_path, backfill_state)

    release_dir = staging_root / "release"
    # Publishing is the first irreversible boundary. Recompute the complete
    # archived-source/model/charter/execution identity both before staging and
    # immediately before promotion.
    published = _publish_presentation_backfill_release(
        archive_dir=archive_dir,
        slug=slug,
        title=title,
        repo_root=repo_root,
        art_director=art_director,
        designer=designer,
        expected_payload=identity_payload,
        expected_identity=identity,
        backfill_state=backfill_state,
        visual_path=visual_path,
        out_path=out_path,
        qa_path=qa_path,
        receipt_path=receipt_path,
        qa_render_dir=qa_render_dir,
        inspection_dir=inspection_dir,
        release_dir=release_dir,
        stage4=stage4,
        deck_mode=deck_mode,
        out_dir=REPORTS_DIR,
    )
    deck_dst = published["presentation"]
    backfill_state.update(
        {
            "phase": "reports_promoted",
            "updated_at": datetime.now()
            .astimezone()
            .isoformat(timespec="seconds"),
            "cost_by_step": tally.by_step,
            "published_release_manifest_sha256": file_sha256(
                published["release_manifest"]
            ),
        }
    )
    _write_backfill_state(state_path, backfill_state)

    render_dir = stage4 / "qa" / f"{slug}-presentation"
    published_record = {}
    for role, path in sorted(published.items()):
        if path.is_file():
            published_record[role] = {
                "path": relative(path),
                "sha256": file_sha256(path),
            }
        elif path.is_dir():
            published_record[role] = {
                "path": relative(path),
                "files": _backfill_render_hashes(path),
            }
    backfill_record = {
        "schema_version": "3.0",
        "slug": slug,
        "deck_mode": deck_mode,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "identity_sha256": identity,
        "art_direction_dependencies_sha256": identity,
        "presentation_dependencies_sha256": (
            presentation_dependencies_sha256
        ),
        "sources": source_fingerprints,
        "models": identity_payload["models"],
        "agent_charters": identity_payload["agent_charters"],
        "execution_contract": identity_payload["execution_contract"],
        "artifacts": {
            "visual_brief": {
                "path": "stage4/deck-backfill/visual-brief.json",
                "sha256": file_sha256(visual_path),
            },
            "presentation": {
                "path": f"stage4/{out_path.name}",
                "sha256": file_sha256(out_path),
            },
            "presentation_qa": {
                "path": f"stage4/{qa_path.name}",
                "sha256": file_sha256(qa_path),
            },
            "visual_inspection": {
                "path": f"stage4/{receipt_path.name}",
                "sha256": file_sha256(receipt_path),
            },
            "qa_render": {
                "path": f"stage4/qa/{slug}-presentation",
                "files": _backfill_render_hashes(render_dir),
            },
            "inspection_render": {
                "path": f"stage4/inspection/{slug}",
                "files": _backfill_render_hashes(inspection_dir),
            },
            "release_supplement": {
                "path": "release-supplements/deck",
                "files": _backfill_render_hashes(release_dir),
            },
        },
        "published_release": published_record,
        "qa_ok": qa_report.ok,
        "claude_cost_usd": tally.total,
    }
    backfill_manifest = stage4 / f"{slug}-deck-backfill.json"
    temporary_manifest = backfill_manifest.with_name(
        f".{backfill_manifest.name}.tmp"
    )
    temporary_manifest.write_text(
        json.dumps(backfill_record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary_manifest, backfill_manifest)

    _commit_presentation_backfill_archive(
        archive_dir=archive_dir,
        slug=slug,
        title=title,
        repo_root=repo_root,
        art_director=art_director,
        designer=designer,
        expected_payload=identity_payload,
        expected_identity=identity,
        backfill_state=backfill_state,
        visual_path=visual_path,
        out_path=out_path,
        qa_path=qa_path,
        receipt_path=receipt_path,
        qa_render_dir=qa_render_dir,
        inspection_dir=inspection_dir,
        staged_stage4=stage4,
        archive_stage4=archive_dir / "stage4",
    )
    backfill_state.update(
        {
            "status": "complete",
            "phase": "archive_committed",
            "updated_at": datetime.now()
            .astimezone()
            .isoformat(timespec="seconds"),
            "cost_by_step": tally.by_step,
        }
    )
    _write_backfill_state(state_path, backfill_state)
    console.print(
        f"[green]Deck built:[/green] {deck_dst.relative_to(repo_root)} "
        f"[dim](${tally.total:.2f})[/dim]"
    )
    return deck_dst


ACTIVE_RUN_MARKER = ".active-run.json"


def write_run_marker(outputs_dir: Path, spec: RunSpec) -> None:
    """Record which run owns outputs/ so an interrupted run can be detected."""
    marker = {
        "slug": spec.slug,
        "title": spec.title,
        "started": datetime.now().isoformat(timespec="seconds"),
        "format": getattr(spec, "output_format", "report"),
        "council_model": getattr(spec, "council_model", ""),
        "want_pptx": getattr(spec, "want_pptx", False),
        "deck_mode": getattr(spec, "deck_mode", "board"),
        "decision_frame_enabled": bool(
            getattr(spec, "decision_frame_enabled", False)
            or any(
                str(getattr(spec, field, "") or "").strip()
                for field in (
                    "decision_required",
                    "decision_owner",
                    "time_horizon",
                    "approval_path",
                    "success_measure",
                )
            )
        ),
        "decision_required": getattr(spec, "decision_required", ""),
        "decision_owner": getattr(spec, "decision_owner", ""),
        "time_horizon": getattr(spec, "time_horizon", ""),
        "approval_path": getattr(spec, "approval_path", ""),
        "success_measure": getattr(spec, "success_measure", ""),
        "manifest": "run-manifest.json",
        "pipeline_version": "council-v2",
    }
    (outputs_dir / ACTIVE_RUN_MARKER).write_text(
        json.dumps(marker, indent=2), encoding="utf-8"
    )


def read_run_marker(outputs_dir: Path) -> dict | None:
    p = outputs_dir / ACTIVE_RUN_MARKER
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def assert_resume_identity(outputs_dir: Path, expected_slug: str) -> None:
    """Refuse to reuse artifacts unless marker and manifest name the same run."""

    marker = read_run_marker(outputs_dir)
    if not marker or not marker.get("slug"):
        raise RuntimeError(
            "Cannot resume safely: outputs/.active-run.json is missing or invalid. "
            "The existing artifacts were left untouched."
        )
    marker_slug = str(marker["slug"])
    manifest_path = outputs_dir / "run-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_slug = str(manifest["run"]["slug"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        raise RuntimeError(
            "Cannot resume safely: outputs/run-manifest.json is missing or invalid. "
            "The existing artifacts were left untouched."
        ) from None
    if marker_slug != manifest_slug:
        raise RuntimeError(
            "Cannot resume safely: the active-run marker names "
            f"'{marker_slug}', but the manifest names '{manifest_slug}'. "
            "The existing artifacts were left untouched."
        )
    if expected_slug != marker_slug:
        raise RuntimeError(
            f"Cannot resume '{expected_slug}': outputs/ belongs to "
            f"'{marker_slug}'. The existing artifacts were left untouched."
        )


def _notify_done(title: str, message: str) -> None:
    """Best-effort completion signal: macOS notification + terminal bell."""
    try:
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{message}" with title "{title}" sound name "Glass"'],
            capture_output=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        pass
    print("\a", end="", flush=True)


def _persist_checkpoint_ratings(
    outputs_dir: Path, checkpoint_result: object, *, review_id: str
) -> None:
    """Persist partial human rubric scores without coupling to the UI."""

    ratings = getattr(checkpoint_result, "ratings", None)
    if not ratings:
        return
    try:
        from cli.evaluation import write_human_review
    except ImportError:
        console.print(
            f"[yellow]Could not persist {review_id} ratings: "
            "cli.evaluation is unavailable.[/yellow]"
        )
        return
    write_human_review(outputs_dir, ratings, review_id=review_id)


# Bounded remediation attempts after a failed publication gate. Each pass costs
# a fact-checker invocation, so this stays small; three is enough to converge a
# 40-blocker gate in practice while capping the spend.
MAX_REMEDIATION_PASSES = 3


async def run_quality_gate_with_remediation(
    *,
    spec: RunSpec,
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    manifest_path: Path,
    agent_names: list[str],
) -> dict:
    """Run the deterministic gate with bounded verifier remediation passes."""

    final_draft = outputs_dir / "stage3" / "final-draft.md"
    lineage_path = outputs_dir / "claim-lineage.jsonl"
    report_path = outputs_dir / "quality-gate.json"

    def execute_gate() -> dict:
        return run_publication_quality_gate(
            final_draft=final_draft,
            report_path=report_path,
            evidence_ledger_path=outputs_dir / "evidence-ledger.jsonl",
            agent_names=agent_names,
            claim_lineage_path=lineage_path,
            output_format=getattr(spec, "output_format", "report"),
            length_instruction=getattr(spec, "length", ""),
            raise_on_failure=True,
        )

    try:
        payload = execute_gate()
    except PublicationQualityError:
        first_payload = json.loads(report_path.read_text(encoding="utf-8"))
        first_validation = validate_artifact(report_path)
        update_artifact(
            manifest_path,
            report_path,
            first_validation,
            artifact_id="verification/quality-gate",
            producer="orchestrator",
        )
        await emit(
            "quality_gate",
            passed=False,
            attempt=1,
            remediation_pending=True,
            error_count=first_payload.get("error_count", 1),
            warning_count=first_payload.get("warning_count", 0),
            report=str(report_path),
        )

        # A single bounded pass cannot clear a large blocker set: this gate
        # reported 45 errors in one run, and the verifier clears a subset
        # each time. Re-gate after every pass and stop the moment it is
        # clean, so a finished run is not discarded over blockers the next
        # pass would have fixed. Still strictly bounded.
        for _pass in range(1, MAX_REMEDIATION_PASSES + 1):
            is_final_pass = _pass == MAX_REMEDIATION_PASSES
            # Each pass must answer the CURRENT gate output, not the first.
            first_payload = json.loads(report_path.read_text(encoding="utf-8"))
            by_name = {agent.name: agent for agent in all_agents}
            verifier = by_name["fact-checker"]
            remediated_path = outputs_dir / "stage3" / "final-draft-remediated.md"
            remediation_inputs = (
                outputs_dir / "stage3" / "remediation-inputs"
            )
            remediation_inputs.mkdir(parents=True, exist_ok=True)
            snapshot_final = remediation_inputs / "final-draft-before-gate.md"
            snapshot_gate = remediation_inputs / "quality-gate-before-remediation.json"
            snapshot_fact_report = (
                remediation_inputs / "fact-check-report-before-gate.md"
            )
            snapshot_lineage = (
                remediation_inputs / "claim-lineage-before-gate.jsonl"
            )
            fact_report = outputs_dir / "stage3" / "fact-check-report.md"
            for source, snapshot, artifact_id in (
                (
                    final_draft,
                    snapshot_final,
                    "verification/remediation-input/final-draft",
                ),
                (
                    report_path,
                    snapshot_gate,
                    "verification/remediation-input/quality-gate",
                ),
                (
                    fact_report,
                    snapshot_fact_report,
                    "verification/remediation-input/fact-check-report",
                ),
                (
                    lineage_path,
                    snapshot_lineage,
                    "verification/remediation-input/claim-lineage",
                ),
            ):
                shutil.copy2(source, snapshot)
                update_artifact(
                    manifest_path,
                    snapshot,
                    validate_artifact(snapshot),
                    artifact_id=artifact_id,
                    producer="orchestrator",
                    role="remediation_input",
                    required=True,
                )
            remediated_fact_report = (
                outputs_dir / "stage3" / "fact-check-report-remediated.md"
            )
            remediated_lineage = (
                outputs_dir / "stage3" / "claim-lineage-remediated.jsonl"
            )
            remediation_dependencies = (
                "run-manifest.json",
                "stage3/remediation-inputs/final-draft-before-gate.md",
                "stage3/remediation-inputs/quality-gate-before-remediation.json",
                "stage3/remediation-inputs/fact-check-report-before-gate.md",
                "stage3/remediation-inputs/claim-lineage-before-gate.jsonl",
                "evidence-ledger.jsonl",
            )
            blockers = [
                issue
                for issue in first_payload.get("issues", [])
                if issue.get("severity") == "error"
            ]
            prompt = (
                f"Read `{run_file}`, `outputs/run-manifest.json`, "
                "`outputs/stage3/remediation-inputs/final-draft-before-gate.md`, "
                "`outputs/stage3/remediation-inputs/quality-gate-before-remediation.json`, "
                "`outputs/stage3/remediation-inputs/fact-check-report-before-gate.md`, "
                "`outputs/stage3/remediation-inputs/claim-lineage-before-gate.jsonl`, "
                "and `outputs/evidence-ledger.jsonl`.\n\n"
                f"This is bounded remediation pass {_pass} of "
                f"{MAX_REMEDIATION_PASSES} after the deterministic "
                "publication gate. Fix every listed blocker without adding new facts or "
                "weakening a well-supported conclusion. Convert internal source tags to "
                "reader-facing primary-source footnotes; repair footnote structure; "
                "use numeric footnote labels only; "
                "remove or accurately qualify unsupported claims; and re-open primary "
                "sources whenever the lineage says they were not checked. A claim that "
                "cannot be verified must be removed from the reader-facing draft, not "
                "left with an internal tag. If the gate reports a word-count blocker, "
                "restore the requested range using only explanation, implications, and "
                "decision mechanics already supported by verified evidence; do not add "
                "new factual claims.\n\n"
                f"Gate blockers:\n{json.dumps(blockers, indent=2)}\n\n"
                "Write the remediated reader-facing draft to "
                "`outputs/stage3/final-draft-remediated.md`. Write the remediated "
                "lineage to `outputs/stage3/claim-lineage-remediated.jsonl` using "
                "the canonical fields: exact "
                "`claim`, exact `citation`, `footnote_id`, `evidence_ids`, boolean "
                "`retained`, boolean `primary_source_checked`, and statuses verified, "
                "qualified, corrected, removed, or unverified. Every `evidence_ids` "
                "value must be copied exactly from an `evidence_id` already present "
                "in `outputs/evidence-ledger.jsonl`; never invent or synthesize one. "
                "Write the complete "
                "updated fact-check report, including a "
                "`## Publication-gate remediation` section to "
                "`outputs/stage3/fact-check-report-remediated.md` describing every "
                "change. Do not modify the immutable remediation-input snapshots."
            )
            prompt += manifest_prompt_block(
                manifest_path, repo_root=outputs_dir.parent
            )
            await _run_agent(
                agent=verifier,
                user_prompt=prompt,
                model=_model("factcheck"),
                cwd=outputs_dir.parent,
                step_label="stage3/fact-check-remediation",
                tally=tally,
                output_path=remediated_path,
                artifact_contract=contract_for_path(final_draft),
                manifest_path=manifest_path,
                artifact_id="verification/remediated-draft",
                required_outputs=(
                    (
                        remediated_lineage,
                        CLAIM_LINEAGE_AGENT_CONTRACT,
                    ),
                    (
                        remediated_fact_report,
                        contract_for_path(remediated_fact_report),
                    ),
                ),
                dependency_inputs=remediation_dependencies,
            )
            shutil.copy2(remediated_path, final_draft)
            shutil.copy2(remediated_fact_report, fact_report)
            shutil.copy2(remediated_lineage, lineage_path)
            bound_dependencies = build_dependency_fingerprint(
                manifest_path, remediation_dependencies
            )
            final_validation = validate_artifact(final_draft)
            update_artifact(
                manifest_path,
                final_draft,
                final_validation,
                artifact_id="stage3/final",
                producer="fact-checker",
                dependencies=bound_dependencies,
            )
            lineage, generated = ensure_claim_lineage(
                final_draft=final_draft,
                evidence_ledger=outputs_dir / "evidence-ledger.jsonl",
                output_path=lineage_path,
            )
            lineage = bind_claim_lineage_to_draft(
                final_draft=final_draft,
                output_path=lineage_path,
            )
            lineage_validation = validate_artifact(
                lineage_path, CLAIM_LINEAGE_CONTRACT
            )
            update_artifact(
                manifest_path,
                lineage_path,
                lineage_validation,
                artifact_id="verification/claim-lineage",
                producer="orchestrator" if generated else "fact-checker",
                dependencies=bound_dependencies,
            )
            await emit(
                "evidence_update",
                kind="claim_lineage",
                lineage_path=str(lineage_path),
                record_count=len(lineage),
                generated_fallback=generated,
                remediation=True,
            )
            fact_report_validation = validate_artifact(fact_report)
            update_artifact(
                manifest_path,
                fact_report,
                fact_report_validation,
                artifact_id="stage3/fact-check",
                producer="fact-checker",
                dependencies=bound_dependencies,
            )
            await emit(
                "artifact_validated",
                step="stage3/fact-check-report-remediated",
                **fact_report_validation.to_dict(),
            )
            if not fact_report_validation.valid:
                raise RuntimeError(
                    "The remediated fact-check report failed its artifact contract: "
                    + "; ".join(fact_report_validation.errors)
                )
            try:
                payload = execute_gate()
            except PublicationQualityError:
                second_payload = json.loads(report_path.read_text(encoding="utf-8"))
                second_validation = validate_artifact(report_path)
                update_artifact(
                    manifest_path,
                    report_path,
                    second_validation,
                    artifact_id="verification/quality-gate",
                    producer="orchestrator",
                )
                await emit(
                    "quality_gate",
                    passed=False,
                    attempt=_pass + 1,
                    remediation_pending=not is_final_pass,
                    error_count=second_payload.get("error_count", 1),
                    warning_count=second_payload.get("warning_count", 0),
                    report=str(report_path),
                )
                if is_final_pass:
                    raise
                continue
            await emit(
                "quality_gate",
                passed=True,
                attempt=_pass + 1,
                remediated=True,
                error_count=payload.get("error_count", 0),
                warning_count=payload.get("warning_count", 0),
                report=str(report_path),
            )
            break
    else:
        await emit(
            "quality_gate",
            passed=True,
            attempt=1,
            remediated=False,
            error_count=payload.get("error_count", 0),
            warning_count=payload.get("warning_count", 0),
            report=str(report_path),
        )

    validation = validate_artifact(report_path)
    update_artifact(
        manifest_path,
        report_path,
        validation,
        artifact_id="verification/quality-gate",
        producer="orchestrator",
        dependencies=build_dependency_fingerprint(
            manifest_path,
            (
                "run-manifest.json",
                "stage3/final-draft.md",
                "claim-lineage.jsonl",
                "evidence-ledger.jsonl",
            ),
        ),
    )
    return payload


async def run_pipeline(
    *,
    spec: RunSpec,
    run_file: Path,
    repo_root: Path,
    auto_approve: bool,
    resume: bool = False,
    budget_usd: float | None = None,
) -> RunResult:
    """Run a report under its explicit single-model route when present."""

    selected = council_model(getattr(spec, "council_model", ""))
    token = _ACTIVE_COUNCIL_MODEL.set(selected)
    try:
        return await _run_pipeline(
            spec=spec,
            run_file=run_file,
            repo_root=repo_root,
            auto_approve=auto_approve,
            resume=resume,
            budget_usd=budget_usd,
        )
    finally:
        _ACTIVE_COUNCIL_MODEL.reset(token)


async def _run_pipeline(
    *,
    spec: RunSpec,
    run_file: Path,
    repo_root: Path,
    auto_approve: bool,
    resume: bool = False,
    budget_usd: float | None = None,
) -> RunResult:
    from cli.checkpoints import (
        CheckpointResult,
        STAGE2_CHECKPOINT_INPUTS,
        STAGE3_CHECKPOINT_INPUTS,
        checkpoint_after_stage2,
        checkpoint_after_stage3,
    )
    from cli.docx_builder import build_documents
    from cli.archive import archive_run, reserve_archive_path

    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    if resume:
        assert_resume_identity(outputs_dir, spec.slug)
    # Final-package dependencies must be healthy before a new manifest or
    # active-run marker makes an otherwise empty run look resumable. A failed
    # preflight is therefore a clean retry, not an interrupted Council run.
    runtime_tools = report_runtime_preflight(
        repo_root,
        outputs_dir,
        selected_research_agents=tuple(spec.selected_research_agents),
        council_model_id=str(getattr(spec, "council_model", "") or ""),
    )
    await emit("preflight", passed=True, tools=runtime_tools)
    await prepare_outputs(outputs_dir, auto_approve=auto_approve, resume=resume)
    sink = get_sink()
    if sink is not None and sink.journal_path is None:
        sink.bind_journal(outputs_dir / "run-events.jsonl")
    all_agents = load_all_agents()
    tally = CostTally(budget_usd=budget_usd)
    by_agent_name = {agent.name: agent for agent in all_agents}
    planned_research_calls = sum(
        not _legacy_openai_agent(by_agent_name[name])
        for name in spec.selected_research_agents
    )
    output_format = str(getattr(spec, "output_format", "report"))
    has_decision_frame = bool(
        getattr(spec, "decision_frame_enabled", False)
        or any(
            str(getattr(spec, field, "") or "").strip()
            for field in (
                "decision_required",
                "decision_owner",
                "time_horizon",
                "approval_path",
                "success_measure",
            )
        )
    )
    needs_art_direction = bool(getattr(spec, "want_pptx", False)) or (
        output_format == "report" and has_decision_frame
    )
    regular_process_calls = 11
    optional_production_calls = 1 + int(needs_art_direction) + int(
        bool(getattr(spec, "want_pptx", False))
    )
    contingency_calls = 2  # one verifier remediation and one requested v3 redo
    planned_model_calls = (
        planned_research_calls
        + regular_process_calls
        + optional_production_calls
        + contingency_calls
    )
    tally.plan_calls(planned_model_calls)
    result_out = RunResult(tally=tally)
    active_pipeline_steps = tuple(
        step
        for step in PIPELINE_DEFINITION
        if (
            step.id != "art-director" or needs_art_direction
        )
        and (
            step.id != "presentation"
            or bool(getattr(spec, "want_pptx", False))
        )
    )
    model_roles = {"research", *(step.model_role for step in active_pipeline_steps)}
    model_assignments = {role: _model(role) for role in sorted(model_roles)}
    manifest_path = create_run_manifest(
        spec=spec,
        run_file=run_file,
        outputs_dir=outputs_dir,
        all_agents=all_agents,
        resume=resume,
        pipeline_steps=active_pipeline_steps,
        model_assignments=model_assignments,
    )
    # On resume, create_run_manifest re-fingerprints the run prompt, sources,
    # roster, agent instructions, model routing, and pipeline. Do not refresh
    # the active marker until that paid-work identity check has succeeded.
    write_run_marker(outputs_dir, spec)
    await emit(
        "manifest_update",
        path=str(manifest_path),
        selected_agents=len(spec.selected_research_agents),
        artifact_count=len(
            json.loads(manifest_path.read_text(encoding="utf-8")).get(
                "artifacts", []
            )
        ),
    )

    process_agent_names = list(
        dict.fromkeys(step.agent for step in active_pipeline_steps)
    )
    await emit(
        "run_start",
        slug=spec.slug,
        title=spec.title,
        agents=[*spec.selected_research_agents, *process_agent_names],
        output_format=getattr(spec, "output_format", "report"),
        resume=resume,
        manifest=str(manifest_path),
        pipeline_version="council-v2",
        council_model=(
            _ACTIVE_COUNCIL_MODEL.get().id
            if _ACTIVE_COUNCIL_MODEL.get() is not None
            else "legacy-role-routing"
        ),
        provider=(
            _ACTIVE_COUNCIL_MODEL.get().provider
            if _ACTIVE_COUNCIL_MODEL.get() is not None
            else "mixed"
        ),
        billing=(
            "chatgpt_subscription"
            if (
                _ACTIVE_COUNCIL_MODEL.get() is not None
                and _ACTIVE_COUNCIL_MODEL.get().provider == "openai"
            )
            else "claude_subscription"
            if (
                _ACTIVE_COUNCIL_MODEL.get() is not None
                and _ACTIVE_COUNCIL_MODEL.get().provider == "anthropic"
            )
            else "provider_subscriptions"
        ),
    )
    await emit(
        "budget_plan",
        ceiling=budget_usd,
        planned_model_calls=planned_model_calls,
        planned_claude_calls=(
            planned_model_calls
            if (
                _ACTIVE_COUNCIL_MODEL.get() is None
                or _ACTIVE_COUNCIL_MODEL.get().provider == "anthropic"
            )
            else 0
        ),
        openai_calls_excluded=sum(
            _legacy_openai_agent(by_agent_name[name])
            for name in spec.selected_research_agents
        ),
    )

    console.rule("[bold]Context — airport and decision packet[/bold]")
    await run_airport_context(
        spec=spec,
        run_file=run_file,
        outputs_dir=outputs_dir,
        all_agents=all_agents,
        tally=tally,
        manifest_path=manifest_path,
    )

    await emit("stage_start", stage=1, label="Research — parallel briefs")
    console.rule("[bold]Stage 1 — parallel research briefs[/bold]")
    await run_stage1(
        spec, run_file, outputs_dir, all_agents, tally, manifest_path
    )

    console.rule("[bold]Evidence curation & targeted gap analysis[/bold]")
    await run_evidence_curation(
        spec=spec,
        run_file=run_file,
        outputs_dir=outputs_dir,
        all_agents=all_agents,
        tally=tally,
        manifest_path=manifest_path,
    )

    await emit("stage_start", stage=2, label="Synthesis & adversarial revision")
    console.rule("[bold]Stage 2 — synthesis & adversarial revision[/bold]")
    await run_stage2(
        spec, run_file, outputs_dir, all_agents, tally, manifest_path
    )

    stage2_checkpoint_inputs = STAGE2_CHECKPOINT_INPUTS
    while True:
        if not _checkpoint_outputs_match_manifest(
            manifest_path, stage2_checkpoint_inputs
        ):
            console.print(
                "[yellow]Stage 2 changed before approval; rebuilding only "
                "the stale synthesis work before reopening review.[/yellow]"
            )
            await emit(
                "checkpoint_invalidated",
                kind="stage2",
                reason="review inputs or their upstream receipts changed",
            )
            await run_stage2(
                spec, run_file, outputs_dir, all_agents, tally, manifest_path
            )
            continue
        if checkpoint_approval_matches(
            manifest_path, "stage2", stage2_checkpoint_inputs
        ):
            result = CheckpointResult(approved=True)
            console.print(
                "[cyan]↷ Stage 2 checkpoint already approved for these "
                "exact draft bytes.[/cyan]"
            )
            await emit(
                "checkpoint_skipped",
                kind="stage2",
                reason="stored approval matches reviewed artifacts",
            )
        else:
            result = await checkpoint_after_stage2(
                outputs_dir, auto_approve=auto_approve
            )
            action = (
                "continue"
                if result.approved
                else "redo"
                if result.redo_from
                else "abort"
            )
            try:
                record_checkpoint_decision(
                    manifest_path,
                    "stage2",
                    approved=result.approved,
                    action=action,
                    declared_inputs=stage2_checkpoint_inputs,
                    auto_approved=auto_approve,
                    reviewed_fingerprint=result.reviewed_fingerprint,
                )
            except CheckpointInputsChanged as exc:
                console.print(
                    "[yellow]Stage 2 changed while it was open for review; "
                    "rebuilding stale work and reopening the checkpoint.[/yellow]"
                )
                await emit(
                    "checkpoint_invalidated",
                    kind="stage2",
                    reason=str(exc),
                )
                await run_stage2(
                    spec, run_file, outputs_dir, all_agents, tally,
                    manifest_path,
                )
                continue
            _persist_checkpoint_ratings(
                outputs_dir, result, review_id="checkpoint-stage2"
            )
        if not _checkpoint_outputs_match_manifest(
            manifest_path, stage2_checkpoint_inputs
        ):
            await emit(
                "checkpoint_invalidated",
                kind="stage2",
                reason="review inputs changed immediately after the decision",
            )
            await run_stage2(
                spec, run_file, outputs_dir, all_agents, tally, manifest_path
            )
            continue
        if result.approved:
            break
        if result.redo_from == "strategist-v3":
            v3_path = outputs_dir / "stage2" / "strategist-draft-v3.md"
            if v3_path.exists():
                v3_path.unlink()
            await run_stage2(
                spec, run_file, outputs_dir, all_agents, tally,
                manifest_path,
                start_from="strategist-v3", v3_note=result.notes,
            )
            continue
        console.print("[yellow]Stopping at Stage 2.[/yellow]")
        return result_out

    await emit("stage_start", stage=3, label="Edit, humanize & fact-check")
    console.rule("[bold]Stage 3 — edit, humanize & fact-check[/bold]")
    await run_stage3(
        run_file, outputs_dir, all_agents, tally, manifest_path
    )

    await run_quality_gate_with_remediation(
        spec=spec,
        run_file=run_file,
        outputs_dir=outputs_dir,
        all_agents=all_agents,
        tally=tally,
        manifest_path=manifest_path,
        agent_names=[
            *spec.selected_research_agents,
            *process_agent_names,
        ],
    )

    stage3_checkpoint_inputs = STAGE3_CHECKPOINT_INPUTS
    while True:
        if not _checkpoint_outputs_match_manifest(
            manifest_path, stage3_checkpoint_inputs
        ):
            console.print(
                "[yellow]Verified Stage 3 inputs changed before approval; "
                "rerunning fact-check and the publication gate.[/yellow]"
            )
            await emit(
                "checkpoint_invalidated",
                kind="stage3",
                reason="verified inputs or their upstream receipts changed",
            )
            await run_stage3(
                run_file, outputs_dir, all_agents, tally, manifest_path
            )
            await run_quality_gate_with_remediation(
                spec=spec,
                run_file=run_file,
                outputs_dir=outputs_dir,
                all_agents=all_agents,
                tally=tally,
                manifest_path=manifest_path,
                agent_names=[
                    *spec.selected_research_agents,
                    *process_agent_names,
                ],
            )
            continue
        if checkpoint_approval_matches(
            manifest_path, "stage3", stage3_checkpoint_inputs
        ):
            result = CheckpointResult(approved=True)
            console.print(
                "[cyan]↷ Stage 3 checkpoint already approved for these exact "
                "verified draft bytes.[/cyan]"
            )
            await emit(
                "checkpoint_skipped",
                kind="stage3",
                reason="stored approval matches reviewed artifacts",
            )
        else:
            result = await checkpoint_after_stage3(
                outputs_dir, auto_approve=auto_approve
            )
            try:
                record_checkpoint_decision(
                    manifest_path,
                    "stage3",
                    approved=result.approved,
                    action="approve" if result.approved else "abort",
                    declared_inputs=stage3_checkpoint_inputs,
                    auto_approved=auto_approve,
                    reviewed_fingerprint=result.reviewed_fingerprint,
                )
            except CheckpointInputsChanged as exc:
                await emit(
                    "checkpoint_invalidated",
                    kind="stage3",
                    reason=str(exc),
                )
                await run_stage3(
                    run_file, outputs_dir, all_agents, tally, manifest_path
                )
                await run_quality_gate_with_remediation(
                    spec=spec,
                    run_file=run_file,
                    outputs_dir=outputs_dir,
                    all_agents=all_agents,
                    tally=tally,
                    manifest_path=manifest_path,
                    agent_names=[
                        *spec.selected_research_agents,
                        *process_agent_names,
                    ],
                )
                continue
            _persist_checkpoint_ratings(
                outputs_dir, result, review_id="checkpoint-stage3"
            )
        if not _checkpoint_outputs_match_manifest(
            manifest_path, stage3_checkpoint_inputs
        ):
            continue
        break
    if not result.approved:
        console.print("[yellow]Stopping at Stage 3. No Word docs generated.[/yellow]")
        return result_out

    await emit("stage_start", stage=4, label="Produce documents")
    update_stage(manifest_path, "production", "running")
    console.rule("[bold]Stage 4 — art direction & documents[/bold]")
    await run_art_direction(
        spec=spec,
        run_file=run_file,
        outputs_dir=outputs_dir,
        all_agents=all_agents,
        tally=tally,
        manifest_path=manifest_path,
    )
    from cli.publishing_quality import executive_summary_word_target

    executive_summary_target_words = executive_summary_word_target(
        run_file.read_text(encoding="utf-8", errors="ignore")
    )
    report_path, executive_path = build_documents(
        slug=spec.slug,
        title=spec.title,
        final_draft=outputs_dir / "stage3" / "final-draft.md",
        methodology=repo_root / "docs" / "methodology.md",
        out_dir=outputs_dir / "stage4",
        output_format=getattr(spec, "output_format", "report"),
        decision_frame_enabled=has_decision_frame,
        visual_brief=(
            outputs_dir / "stage4" / "visual-brief.json"
            if (outputs_dir / "stage4" / "visual-brief.json").is_file()
            else None
        ),
        decision_context={
            "decision": getattr(spec, "decision_required", ""),
            "decision_owner": getattr(spec, "decision_owner", ""),
            "approval_path": getattr(spec, "approval_path", ""),
            "time_horizon": getattr(spec, "time_horizon", ""),
            "success_measure": getattr(spec, "success_measure", ""),
        },
        executive_summary_target_words=executive_summary_target_words,
    )
    await run_word_visual_inspection(
        artifacts=[
            report_path,
            *([executive_path] if executive_path is not None else []),
        ],
        outputs_dir=outputs_dir,
        all_agents=all_agents,
        tally=tally,
        manifest_path=manifest_path,
        step_label="stage4/word-visual-inspection",
    )
    executive_required = executive_path is not None
    for artifact_path, artifact_id, role, required in (
        (report_path, "stage4/word-report", "word_report", True),
        (
            executive_path,
            "stage4/executive-summary",
            "executive_summary",
            executive_required,
        ),
    ):
        if artifact_path is None:
            continue
        validation = validate_artifact(artifact_path)
        update_artifact(
            manifest_path,
            artifact_path,
            validation,
            artifact_id=artifact_id,
            producer="orchestrator",
            role=role,
            required=required,
        )
        await emit(
            "artifact_validated",
            step=f"stage4/{role}",
            **validation.to_dict(),
        )
        if not validation.valid:
            raise RuntimeError(
                f"{artifact_path.name} failed its Office artifact contract: "
                + "; ".join(validation.errors)
            )

    publishing_quality_path = outputs_dir / "publishing-quality.json"
    publishing_quality_contract = ArtifactContract(
        "json",
        required_keys=("artifact", "kind", "ok", "issues"),
    )
    publishing_quality_validation = validate_artifact(
        publishing_quality_path,
        publishing_quality_contract,
    )
    update_artifact(
        manifest_path,
        publishing_quality_path,
        publishing_quality_validation,
        artifact_id="stage4/publishing-quality",
        producer="orchestrator",
    )
    if not publishing_quality_validation.valid:
        raise RuntimeError(
            "Document publishing QA record is invalid: "
            + "; ".join(publishing_quality_validation.errors)
        )
    publishing_payload = json.loads(
        publishing_quality_path.read_text(encoding="utf-8")
    )
    if publishing_payload.get("ok") is not True:
        raise RuntimeError(
            "Document publishing QA contains release-blocking errors."
        )
    await emit(
        "render_qa",
        artifact=str(report_path),
        status="passed",
        issues=len(publishing_payload.get("issues", [])),
        rendered_files=publishing_payload.get("rendered_files", []),
    )

    if getattr(spec, "want_pptx", False):
        console.rule("[bold]Companion PowerPoint[/bold]")
        await run_presentation(
            spec, outputs_dir, all_agents, tally, manifest_path
        )
    update_stage(manifest_path, "production", "complete")

    # Release is a commit gate, not a best-effort postscript. Stage exact
    # Stage 4 bytes, independently render/inspect them, bind the bundle to
    # hashes in both manifests, and promote the complete set before archiving.
    console.rule("[bold]Release[/bold]")
    from cli.publish import (
        REPORTS_DIR,
        promote_release,
        stage_release_artifacts,
    )

    release_dir = outputs_dir / "release"
    release_payload = stage_release_artifacts(
        stage4_dir=outputs_dir / "stage4",
        slug=spec.slug,
        release_dir=release_dir,
        require_executive_summary=executive_required,
        require_presentation=bool(getattr(spec, "want_pptx", False)),
        presentation_mode=str(
            getattr(spec, "deck_mode", "board_decision")
        ),
        visual_brief=outputs_dir / "stage4" / "visual-brief.json",
        require_visual_inspection=bool(
            getattr(spec, "want_pptx", False)
        ),
        require_word_visual_inspection=True,
    )
    release_ids = {
        "word_report": ("release/word-report", "release/word-qa"),
        "executive_summary": (
            "release/executive-summary",
            "release/executive-summary-qa",
        ),
        "presentation": (
            "release/presentation",
            "release/presentation-qa",
        ),
    }
    for artifact in release_payload.get("artifacts", []):
        role = str(artifact["role"])
        artifact_id, qa_id = release_ids[role]
        released_path = release_dir / str(artifact["path"])
        released_validation = validate_artifact(released_path)
        update_artifact(
            manifest_path,
            released_path,
            released_validation,
            artifact_id=artifact_id,
            producer="orchestrator",
        )
        qa_path = release_dir / str(artifact["qa_path"])
        qa_validation = validate_artifact(
            qa_path,
            ArtifactContract(
                "json",
                required_keys=("artifact", "kind", "ok", "issues"),
            ),
        )
        update_artifact(
            manifest_path,
            qa_path,
            qa_validation,
            artifact_id=qa_id,
            producer="orchestrator",
        )
        if role == "presentation":
            inspection_record = artifact.get("visual_inspection")
            if not isinstance(inspection_record, dict):
                raise RuntimeError(
                    "Presentation release has no hash-bound visual inspection."
                )
            inspection_path = release_dir / str(
                inspection_record.get("path") or ""
            )
            inspection_validation = validate_artifact(
                inspection_path,
                _visual_inspection_contract(),
            )
            update_artifact(
                manifest_path,
                inspection_path,
                inspection_validation,
                artifact_id="release/visual-inspection",
                producer="orchestrator",
            )
        elif role in {"word_report", "executive_summary"}:
            inspection_record = artifact.get("visual_inspection")
            if not isinstance(inspection_record, dict):
                raise RuntimeError(
                    f"{role} release has no hash-bound page inspection."
                )
            inspection_path = release_dir / str(
                inspection_record.get("path") or ""
            )
            inspection_validation = validate_artifact(
                inspection_path,
                _word_visual_inspection_contract(),
            )
            update_artifact(
                manifest_path,
                inspection_path,
                inspection_validation,
                artifact_id=(
                    "release/executive-summary-visual-inspection"
                    if role == "executive_summary"
                    else "release/word-visual-inspection"
                ),
                producer="orchestrator",
            )
        await emit(
            "artifact_validated",
            step=f"release/{role}",
            **released_validation.to_dict(),
        )
    release_manifest_path = release_dir / "release-manifest.json"
    release_manifest_validation = validate_artifact(
        release_manifest_path,
        ArtifactContract(
            "json",
            required_keys=("schema_version", "slug", "artifacts"),
        ),
    )
    update_artifact(
        manifest_path,
        release_manifest_path,
        release_manifest_validation,
        artifact_id="release/manifest",
        producer="orchestrator",
    )
    update_stage(manifest_path, "release", "complete")
    assert_manifest_complete(manifest_path)

    # Reject a same-day slug collision before reports/ is changed. The archive
    # module still repeats this check at commit time.
    reserve_archive_path(
        repo_root=repo_root,
        slug=spec.slug,
        manifest_path=manifest_path,
    )
    published = promote_release(
        release_dir=release_dir,
        out_dir=REPORTS_DIR,
    )
    result_out.published_path = published["word_report"]
    result_out.deck_path = published.get("presentation")
    console.print(
        f"[green]Published:[/green] "
        f"{result_out.published_path.relative_to(repo_root)}"
    )
    if result_out.deck_path is not None:
        console.print(
            f"[green]Deck:[/green] {result_out.deck_path.relative_to(repo_root)}"
        )

    console.rule("[bold]Archive[/bold]")
    archive_path = archive_run(
        repo_root=repo_root,
        slug=spec.slug,
        tally=tally,
        run_file=run_file,
        manifest_path=manifest_path,
    )
    console.print(f"[green]Archived to:[/green] {archive_path}")
    result_out.archive_path = archive_path

    result_out.completed = True
    await emit(
        "run_complete",
        slug=spec.slug,
        title=spec.title,
        total=tally.total,
        archive=str(archive_path),
        published=str(result_out.published_path) if result_out.published_path else None,
        deck=str(result_out.deck_path) if result_out.deck_path else None,
        billing=(
            "chatgpt_subscription"
            if (
                _ACTIVE_COUNCIL_MODEL.get() is not None
                and _ACTIVE_COUNCIL_MODEL.get().provider == "openai"
            )
            else "claude_subscription"
            if (
                _ACTIVE_COUNCIL_MODEL.get() is not None
                and _ACTIVE_COUNCIL_MODEL.get().provider == "anthropic"
            )
            else "provider_subscriptions"
        ),
    )
    _notify_done("AI Council", f"Run complete: {spec.title} (subscription plan)")
    return result_out


# ----------------------------------------------------------------------------
# Revision pipeline — produce a revised version of an existing report from
# reader feedback, reusing the original Stage 1 research briefs.
# ----------------------------------------------------------------------------

REVISION_EXECUTION_CONTRACTS: tuple[str, ...] = (
    "AGENTS.md",
    "CLAUDE.md",
    "council.toml",
    "cli/agents.py",
    "cli/artifacts.py",
    "cli/config.py",
    "cli/orchestrator.py",
    "cli/revision_state.py",
)

# The revision user prompt narrows generic normal-run charter examples to these
# exact archive inputs. Keep this declarative: tests verify that every
# charter-permitted read is both named to the model and hash-bound in the
# corresponding step receipt.
REVISION_SYSTEM_PROMPT_INPUTS: dict[str, tuple[str, ...]] = {
    "strategist-a": (
        "run_prompt",
        "run_manifest",
        "evidence_map",
        "evidence_ledger",
        "narrative_options",
        "briefs",
    ),
    "strategist-b": (
        "run_prompt",
        "run_manifest",
        "evidence_map",
        "evidence_ledger",
        "narrative_options",
        "briefs",
    ),
    "red-team": (
        "run_manifest",
        "evidence_map",
        "evidence_ledger",
        "briefs",
    ),
    "fact-checker": (
        "run_manifest",
        "evidence_map",
        "evidence_ledger",
        "airport_context",
        "context_sources",
        "briefs",
    ),
    "fact-check-remediation": (
        "run_manifest",
        "evidence_ledger",
    ),
    "art-direction": (
        "run_prompt",
        "run_manifest",
        "final_draft",
        "fact_check_report",
        "evidence_map",
        "evidence_ledger",
        "airport_context",
        "context_sources",
    ),
}


def _revision_system_dependencies(
    step_id: str,
    catalog: dict[str, RevisionDependency],
) -> tuple[RevisionDependency, ...]:
    keys = REVISION_SYSTEM_PROMPT_INPUTS[step_id]
    missing = [key for key in keys if key not in catalog]
    if missing:
        raise RuntimeError(
            f"Revision step {step_id!r} has no dependency mapping for: "
            + ", ".join(missing)
        )
    return tuple(catalog[key] for key in keys)


def _revision_system_prompt_block(
    step_id: str,
    catalog: dict[str, RevisionDependency],
) -> str:
    """Narrow normal-run charter examples to an exact revision read set."""

    lines = [
        "\n\n--- REVISION-MODE SYSTEM INPUT CONTRACT ---",
        "For this assignment, the archived Council inputs your system charter "
        "permits are exactly:",
    ]
    for key in REVISION_SYSTEM_PROMPT_INPUTS[step_id]:
        dependency = catalog[key]
        availability = "" if dependency.required else " (read only if present)"
        lines.append(
            f"- {key}: `{dependency.declaration}`{availability}"
        )
    lines.extend(
        (
            "Do not substitute normal-run `outputs/...` examples, discover a "
            "newer draft, or read another archived Council artifact.",
            "--- END REVISION-MODE SYSTEM INPUT CONTRACT ---",
        )
    )
    return "\n".join(lines)


def _revision_dependency(
    repo_root: Path,
    path: Path,
    *,
    required: bool = True,
) -> RevisionDependency:
    return RevisionDependency(
        revision_repo_relative(repo_root, path),
        required=required,
    )


def _revision_glob_dependency(
    repo_root: Path,
    directory: Path,
    pattern: str,
    *,
    required: bool = True,
) -> RevisionDependency:
    relative = revision_repo_relative(repo_root, directory)
    return RevisionDependency(
        f"{relative}/{pattern}",
        required=required,
    )


def _revision_agent_dependencies(
    *,
    repo_root: Path,
    agent: Agent,
    inputs: tuple[RevisionDependency, ...],
) -> tuple[RevisionDependency, ...]:
    """Add the executable and model-charter files every paid call consumes."""

    static = tuple(
        RevisionDependency(path, required=True)
        for path in REVISION_EXECUTION_CONTRACTS
    )
    charter = _revision_dependency(repo_root, agent.path)
    return tuple(dict.fromkeys((*inputs, charter, *static)))


def _revision_call_values(
    *,
    agent: Agent,
    model: str,
    prompt: str,
    step_label: str,
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    values: dict[str, object] = {
        "step_label": step_label,
        "agent": agent.name,
        "agent_provider": _effective_provider(agent),
        "agent_model_override": (
            None if _uses_coherent_run_model() else agent.model_override
        ),
        "agent_tools": list(agent.tools),
        "agent_system_prompt_sha256": hashlib.sha256(
            agent.system_prompt.encode("utf-8")
        ).hexdigest(),
        "model": model,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    }
    values.update(extra or {})
    return values


def _revision_completion_outputs(
    *,
    output_path: Path,
    artifact_contract: ArtifactContract | None,
    required_outputs: tuple[tuple[Path, ArtifactContract], ...],
) -> tuple[tuple[Path, ArtifactContract], ...]:
    primary_contract = artifact_contract or contract_for_path(output_path)
    return (
        (output_path, primary_contract),
        *tuple(
            item for item in required_outputs if item[0] != output_path
        ),
    )


async def _run_revision_agent(
    *,
    state_path: Path,
    repo_root: Path,
    step_id: str,
    agent: Agent,
    user_prompt: str,
    model: str,
    step_label: str,
    tally: CostTally,
    output_path: Path,
    dependencies: tuple[RevisionDependency, ...],
    artifact_contract: ArtifactContract | None = None,
    required_outputs: tuple[tuple[Path, ArtifactContract], ...] = (),
    emit_completion: bool = True,
    extra_values: dict[str, object] | None = None,
) -> dict[str, object]:
    """Run one revision agent only when its exact receipt cannot be reused."""

    bound_dependencies = _revision_agent_dependencies(
        repo_root=repo_root,
        agent=agent,
        inputs=dependencies,
    )
    values = _revision_call_values(
        agent=agent,
        model=model,
        prompt=user_prompt,
        step_label=step_label,
        extra=extra_values,
    )
    completion_outputs = _revision_completion_outputs(
        output_path=output_path,
        artifact_contract=artifact_contract,
        required_outputs=required_outputs,
    )
    reusable, before = revision_step_matches(
        state_path=state_path,
        repo_root=repo_root,
        step_id=step_id,
        dependencies=bound_dependencies,
        values=values,
        outputs=completion_outputs,
    )
    if before.get("complete") is not True:
        for path, _ in completion_outputs:
            _quarantine_partial_output(path)
        missing = [
            str(item.get("declaration") or "")
            for item in before.get("inputs", [])
            if isinstance(item, dict) and item.get("error")
        ]
        raise RuntimeError(
            f"{step_label} cannot start because a declared revision input is "
            "missing or unsafe"
            + (f": {', '.join(missing)}" if missing else ".")
        )
    if not reusable:
        # A revision output set is one paid-work commit. Never let generic
        # file-exists resume mix a stale primary with fresh companions.
        for path, _ in completion_outputs:
            _quarantine_partial_output(path)

    completion = await _run_agent(
        agent=agent,
        user_prompt=user_prompt,
        model=model,
        cwd=repo_root,
        step_label=step_label,
        tally=tally,
        output_path=output_path,
        artifact_contract=artifact_contract,
        required_outputs=required_outputs,
        emit_completion=emit_completion,
    )
    after = build_revision_dependency_fingerprint(
        repo_root=repo_root,
        dependencies=bound_dependencies,
        values=values,
    )
    if (
        after.get("complete") is not True
        or after.get("sha256") != before.get("sha256")
    ):
        for path, _ in completion_outputs:
            _quarantine_partial_output(path)
        raise RuntimeError(
            f"{step_label} inputs changed while the agent was running; its "
            "outputs were quarantined instead of being mixed into the revision."
        )
    if reusable:
        return completion
    record_revision_step(
        state_path=state_path,
        repo_root=repo_root,
        step_id=step_id,
        dependencies=bound_dependencies,
        values=values,
        outputs=completion_outputs,
        dependency_fingerprint=after,
        metadata={
            "agent": agent.name,
            "model": model,
            "provider": _effective_provider(agent),
        },
    )
    return completion


def _record_revision_agent_outputs(
    *,
    state_path: Path,
    repo_root: Path,
    step_id: str,
    agent: Agent,
    prompt: str,
    model: str,
    step_label: str,
    dependencies: tuple[RevisionDependency, ...],
    outputs: tuple[tuple[Path, ArtifactContract], ...],
    extra_values: dict[str, object] | None = None,
    metadata: dict[str, object] | None = None,
) -> None:
    """Refresh a receipt after deterministic canonicalization mutates output."""

    bound_dependencies = _revision_agent_dependencies(
        repo_root=repo_root,
        agent=agent,
        inputs=dependencies,
    )
    values = _revision_call_values(
        agent=agent,
        model=model,
        prompt=prompt,
        step_label=step_label,
        extra=extra_values,
    )
    record_revision_step(
        state_path=state_path,
        repo_root=repo_root,
        step_id=step_id,
        dependencies=bound_dependencies,
        values=values,
        outputs=outputs,
        metadata={
            "agent": agent.name,
            "model": model,
            "provider": _effective_provider(agent),
            **dict(metadata or {}),
        },
    )


def _snapshot_revision_remediation_inputs(
    *,
    base: Path,
    sources: dict[str, Path],
) -> dict[str, Path]:
    """Freeze self-mutating remediation inputs before the paid verifier call."""

    destination_dir = base / "remediation-inputs"
    destination_dir.mkdir(parents=True, exist_ok=True)
    snapshots: dict[str, Path] = {}
    for name, source in sources.items():
        if not source.is_file() or source.is_symlink():
            raise RuntimeError(
                f"Cannot snapshot revision remediation input: {source}"
            )
        destination = destination_dir / name
        temporary = destination.with_name(f".{destination.name}.tmp")
        shutil.copy2(source, temporary)
        os.replace(temporary, destination)
        snapshots[name] = destination
    return snapshots


def _publish_revision_release(
    *,
    state_path: Path,
    repo_root: Path,
    required_steps: set[str],
    stage4_dir: Path,
    slug: str,
    release_dir: Path,
    require_executive_summary: bool,
    out_dir: Path,
) -> dict[str, Path]:
    """Apply live revision receipt barriers around release staging."""

    from cli.publish import promote_release, stage_release_artifacts

    assert_revision_state_current(
        state_path=state_path,
        repo_root=repo_root,
        required_steps=required_steps,
    )
    stage_release_artifacts(
        stage4_dir=stage4_dir,
        slug=slug,
        release_dir=release_dir,
        require_executive_summary=require_executive_summary,
        include_roles={
            "word_report",
            *(
                {"executive_summary"}
                if require_executive_summary
                else set()
            ),
        },
        require_word_visual_inspection=True,
    )
    assert_revision_state_current(
        state_path=state_path,
        repo_root=repo_root,
        required_steps=required_steps,
    )
    return promote_release(release_dir=release_dir, out_dir=out_dir)


def _revision_prompts(
    base_rel: str,
    src_draft_rel: str,
    briefs_rel: str,
    evidence_ledger_rel: str,
    original_lineage_rel: str | None,
    system_input_catalog: dict[str, RevisionDependency],
) -> dict[str, str]:
    prompts = {
        "strategist-a": (
            "You are revising an existing Council report in response to new reader "
            f"feedback. Read the current report draft at `{src_draft_rel}` and the "
            f"reader's feedback at `{base_rel}/feedback.md`. The original research "
            f"briefs are in `{briefs_rel}/` — rely on them for evidence and do NOT "
            "invent new facts or sources.\n\n"
            "Produce a revised draft that incorporates the feedback while preserving "
            "the report's structure, voice, and every well-supported claim the "
            "feedback does not touch. Make the changes the feedback calls for; do not "
            "rewrite wholesale. Where the feedback asks for something the evidence "
            "cannot support, say so in the text rather than fabricating support.\n"
            f"Write the revised draft to: `{base_rel}/revised-draft-a.md`"
        ),
        "red-team": (
            f"Read the revised draft at `{base_rel}/revised-draft-a.md`, the reader "
            f"feedback at `{base_rel}/feedback.md`, and the prior draft at "
            f"`{src_draft_rel}`.\n\n"
            "Critique the revision on two axes: (1) did it actually address the "
            "feedback, point by point; and (2) did the revision introduce new weak "
            "claims, internal contradictions, or breaks in the argument? Number every "
            "item.\n"
            f"Write to: `{base_rel}/red-team-critique.md`"
        ),
        "strategist-b": (
            f"Read `{base_rel}/revised-draft-a.md` and the critique at "
            f"`{base_rel}/red-team-critique.md`. Produce the final revised draft, "
            "addressing every critique item. Keep the report's voice.\n"
            f"Write to: `{base_rel}/revised-draft-b.md`"
        ),
        "editor": (
            f"Read `{base_rel}/revised-draft-b.md`. Tighten for executive tone and "
            "economy without adding content or changing claims. Kill buzzwords (see "
            "CLAUDE.md).\n"
            f"Write the edited draft to `{base_rel}/edited-draft.md` and a concise "
            f"change log to `{base_rel}/editor-notes.md`."
        ),
        "humanizer": (
            f"Read `{base_rel}/edited-draft.md`. Refine tone, readability, and overall "
            "writing quality per your charter. Do not add, remove, or alter any factual "
            "claim, number, citation, or bracketed tag — the Fact-checker verifies your "
            "output next.\n"
            f"Write the refined draft to: `{base_rel}/humanized-draft.md`"
        ),
        "fact-checker": (
            f"Read `{base_rel}/humanized-draft.md`, the original briefs in "
            f"`{briefs_rel}/`, and the canonical evidence ledger at "
            f"`{evidence_ledger_rel}`."
            + (
                f" Read the original claim lineage at `{original_lineage_rel}` "
                "as a starting map, not as proof."
                if original_lineage_rel
                else ""
            )
            + "\n\nVerify every numerical claim, attributed quote, and specific "
            "assertion against the underlying source—not merely against a brief. "
            "Open the cited URL or local source when possible and confirm the "
            "number, denominator, date, locator, and wording. Remove or accurately "
            "qualify anything that cannot be supported. The reader-facing revision "
            "must contain no `[UNVERIFIED]` tag or internal Council path.\n\n"
            f"Write the final revised draft to `{base_rel}/final-draft.md`.\n"
            f"Write a verification log to `{base_rel}/fact-check-report.md`.\n"
            f"Write canonical JSONL to `{base_rel}/claim-lineage.jsonl`, one "
            "record per consequential claim, with exact `claim`, exact `citation`, "
            "`footnote_id`, `evidence_ids`, boolean `retained`, "
            "`verification_status`, boolean `primary_source_checked`, and "
            "`verification_note`. Excluded unverified claims must use "
            "`retained: false`; no markdown fence."
        ),
    }
    for step_id in (
        "strategist-a",
        "red-team",
        "strategist-b",
        "fact-checker",
    ):
        prompts[step_id] += _revision_system_prompt_block(
            step_id, system_input_catalog
        )
    return prompts


async def run_revision_pipeline(
    *,
    request,
    repo_root: Path,
    auto_approve: bool,
) -> tuple[Path | None, CostTally]:
    selected = _archived_council_model(request.source.archive_dir)
    token = _ACTIVE_COUNCIL_MODEL.set(selected)
    try:
        return await _run_revision_pipeline(
            request=request,
            repo_root=repo_root,
            auto_approve=auto_approve,
        )
    finally:
        _ACTIVE_COUNCIL_MODEL.reset(token)


async def _run_revision_pipeline(
    *,
    request,  # cli.revise.RevisionRequest
    repo_root: Path,
    auto_approve: bool,
) -> tuple[Path | None, CostTally]:
    """Run the focused revision loop and build the polished revised report."""
    import questionary as _q

    from cli.checkpoints import _read, _show_file_excerpt
    from cli.docx_builder import build_documents
    from cli.publish import (
        REPORTS_DIR,
        _detect_format,
    )

    source = request.source
    version = request.version
    archive_dir = source.archive_dir
    output_format = _detect_format(source)
    length_instruction = ""
    executive_summary_target_words: int | None = None
    revision_decision_context: dict[str, str] = {}
    revision_decision_frame_enabled = False
    if source.run_file is not None and source.run_file.is_file():
        run_prompt_text = source.run_file.read_text(
            encoding="utf-8", errors="ignore"
        )
        from cli.publishing_quality import executive_summary_word_target

        executive_summary_target_words = executive_summary_word_target(
            run_prompt_text
        )
        length_match = re.search(
            r"(?ms)^## Length(?:\s+\([^)]*\))?\s*$\n"
            r"(?P<body>.*?)(?=^##\s|\Z)",
            run_prompt_text,
        )
        if length_match:
            length_instruction = length_match.group("body").strip()
        try:
            from cli.runfile import parse_run_file

            source_spec = parse_run_file(
                source.run_file.name,
                runs_dir=source.run_file.parent,
            )
        except (FileNotFoundError, ValueError):
            # Legacy archives may predate the structured decision frame. Their
            # verified prose remains publishable without inventing metadata.
            pass
        else:
            revision_decision_frame_enabled = bool(
                getattr(source_spec, "decision_frame_enabled", False)
            )
            revision_decision_context = {
                "decision": source_spec.decision_required,
                "decision_owner": source_spec.decision_owner,
                "approval_path": source_spec.approval_path,
                "time_horizon": source_spec.time_horizon,
                "success_measure": source_spec.success_measure,
            }

    from cli.revise import latest_draft_path

    base = archive_dir / "revisions" / f"v{version}"
    base.mkdir(parents=True, exist_ok=True)
    feedback_path = base / "feedback.md"
    feedback_path.write_text(
        f"# Reader feedback — Revised v{version}\n\n{request.feedback}\n",
        encoding="utf-8",
    )
    revision_state_path = base / REVISION_STATE_NAME

    src_draft = latest_draft_path(archive_dir)
    # A same-version resume must never revise its own partially completed final
    # draft. Pin vN to vN-1 (or the original) even if vN/final-draft.md exists.
    if base.resolve() in src_draft.resolve().parents:
        prior_revision = (
            archive_dir
            / "revisions"
            / f"v{version - 1}"
            / "final-draft.md"
        )
        src_draft = (
            prior_revision
            if version > 1 and prior_revision.is_file()
            else archive_dir / "stage3" / "final-draft.md"
        )
    if not src_draft.is_file():
        raise FileNotFoundError(
            f"Revision source draft is missing: {src_draft}"
        )
    briefs_dir = archive_dir / "stage1"
    evidence_ledger = archive_dir / "evidence-ledger.jsonl"
    if not evidence_ledger.is_file():
        selected_agents = sorted(
            path.name.removesuffix("-brief.md")
            for path in briefs_dir.glob("*-brief.md")
        )
        evidence_ledger = base / "evidence-ledger.jsonl"
        build_evidence_ledger(
            selected_agents=selected_agents,
            stage1_dir=briefs_dir,
            output_path=evidence_ledger,
        )
    original_lineage = archive_dir / "claim-lineage.jsonl"
    base_rel = base.relative_to(repo_root).as_posix()
    src_draft_rel = src_draft.relative_to(repo_root).as_posix()
    briefs_rel = briefs_dir.relative_to(repo_root).as_posix()
    evidence_ledger_rel = evidence_ledger.relative_to(repo_root).as_posix()
    original_lineage_rel = (
        original_lineage.relative_to(repo_root).as_posix()
        if original_lineage.is_file()
        else None
    )

    all_agents = load_all_agents()
    by_name = {a.name: a for a in all_agents}
    tally = CostTally()
    tally.plan_calls(10)
    brief_inputs = _revision_glob_dependency(
        repo_root,
        briefs_dir,
        "*-brief.md",
    )
    source_library = _revision_glob_dependency(
        repo_root,
        archive_dir / "sources",
        "**/*",
        required=False,
    )
    original_lineage_input = _revision_dependency(
        repo_root,
        original_lineage,
        required=False,
    )
    revision_system_catalog: dict[str, RevisionDependency] = {
        "run_prompt": _revision_dependency(
            repo_root,
            (
                source.run_file
                if source.run_file is not None
                else archive_dir / "run-prompt.md"
            ),
            required=(
                source.run_file is not None
                and source.run_file.is_file()
            ),
        ),
        "run_manifest": _revision_dependency(
            repo_root,
            archive_dir / "run-manifest.json",
            required=False,
        ),
        "evidence_map": _revision_dependency(
            repo_root,
            archive_dir / "stage1" / "evidence-map.md",
            required=False,
        ),
        "evidence_ledger": _revision_dependency(
            repo_root,
            evidence_ledger,
        ),
        "narrative_options": _revision_dependency(
            repo_root,
            archive_dir / "stage2" / "narrative-options.md",
            required=False,
        ),
        "airport_context": _revision_dependency(
            repo_root,
            archive_dir / "context" / "airport-context.md",
            required=False,
        ),
        "context_sources": _revision_dependency(
            repo_root,
            archive_dir / "context" / "context-sources.jsonl",
            required=False,
        ),
        "briefs": brief_inputs,
        "final_draft": _revision_dependency(
            repo_root,
            base / "final-draft.md",
        ),
        "fact_check_report": _revision_dependency(
            repo_root,
            base / "fact-check-report.md",
        ),
    }
    prompts = _revision_prompts(
        base_rel,
        src_draft_rel,
        briefs_rel,
        evidence_ledger_rel,
        original_lineage_rel,
        revision_system_catalog,
    )
    revision_dependencies: dict[str, tuple[RevisionDependency, ...]] = {
        "strategist-a": (
            _revision_dependency(repo_root, src_draft),
            _revision_dependency(repo_root, feedback_path),
            *_revision_system_dependencies(
                "strategist-a", revision_system_catalog
            ),
        ),
        "red-team": (
            _revision_dependency(repo_root, base / "revised-draft-a.md"),
            _revision_dependency(repo_root, feedback_path),
            _revision_dependency(repo_root, src_draft),
            *_revision_system_dependencies(
                "red-team", revision_system_catalog
            ),
        ),
        "strategist-b": (
            _revision_dependency(repo_root, base / "revised-draft-a.md"),
            _revision_dependency(repo_root, base / "red-team-critique.md"),
            *_revision_system_dependencies(
                "strategist-b", revision_system_catalog
            ),
        ),
        "editor": (
            _revision_dependency(repo_root, base / "revised-draft-b.md"),
        ),
        "humanizer": (
            _revision_dependency(repo_root, base / "edited-draft.md"),
        ),
        "fact-checker": (
            _revision_dependency(repo_root, base / "humanized-draft.md"),
            original_lineage_input,
            source_library,
            *_revision_system_dependencies(
                "fact-checker", revision_system_catalog
            ),
        ),
    }

    console.rule(f"[bold]Revising '{source.slug}' → v{version}[/bold]")
    console.print(f"[dim]Revising from: {src_draft_rel}[/dim]")
    await emit("run_start", slug=source.slug, title=f"{source.slug} — Revision v{version}",
               agents=[
                   "strategist",
                   "red-team",
                   "editor",
                   "humanizer",
                   "fact-checker",
                   "art-director",
               ],
               mode="revise")
    await emit("stage_start", stage=2, label=f"Revising to v{version}")

    factchecker_model = _model("factcheck")
    steps = [
        (
            "strategist-a",
            by_name["strategist"],
            base / "revised-draft-a.md",
            _model("synthesis"),
        ),
        (
            "red-team",
            by_name["red-team"],
            base / "red-team-critique.md",
            _model("critique"),
        ),
        (
            "strategist-b",
            by_name["strategist"],
            base / "revised-draft-b.md",
            _model("synthesis"),
        ),
        (
            "editor",
            by_name["editor"],
            base / "edited-draft.md",
            _model("editor"),
        ),
        (
            "humanizer",
            by_name["humanizer"],
            base / "humanized-draft.md",
            _model("humanizer"),
        ),
        (
            "fact-checker",
            by_name["fact-checker"],
            base / "final-draft.md",
            factchecker_model,
        ),
    ]
    revision_step_contracts: dict[str, ArtifactContract] = {
        "strategist-a": ArtifactContract("markdown", min_words=250),
        "strategist-b": ArtifactContract("markdown", min_words=250),
    }
    for step_id, agent, out_path, model in steps:
        required_outputs: tuple[tuple[Path, ArtifactContract], ...] = ()
        if step_id == "editor":
            required_outputs = (
                (
                    base / "editor-notes.md",
                    contract_for_path(base / "editor-notes.md"),
                ),
            )
        elif step_id == "fact-checker":
            required_outputs = (
                (
                    base / "fact-check-report.md",
                    contract_for_path(base / "fact-check-report.md"),
                ),
                (
                    base / "claim-lineage.jsonl",
                    CLAIM_LINEAGE_AGENT_CONTRACT,
                ),
            )
        await _run_revision_agent(
            state_path=revision_state_path,
            repo_root=repo_root,
            step_id=step_id,
            agent=agent,
            user_prompt=prompts[step_id],
            model=model,
            step_label=f"revision-v{version}/{step_id}",
            tally=tally,
            output_path=out_path,
            artifact_contract=revision_step_contracts.get(step_id),
            required_outputs=required_outputs,
            dependencies=revision_dependencies[step_id],
            extra_values={
                "revision": version,
                "source_archive": archive_dir.name,
                "output_format": output_format,
            },
        )

    final_draft = base / "final-draft.md"
    revision_lineage = base / "claim-lineage.jsonl"
    revision_gate = base / "quality-gate.json"
    bind_claim_lineage_to_draft(
        final_draft=final_draft,
        output_path=revision_lineage,
    )
    factchecker_outputs = (
        (final_draft, contract_for_path(final_draft)),
        (
            base / "fact-check-report.md",
            contract_for_path(base / "fact-check-report.md"),
        ),
        (revision_lineage, CLAIM_LINEAGE_AGENT_CONTRACT),
    )
    _record_revision_agent_outputs(
        state_path=revision_state_path,
        repo_root=repo_root,
        step_id="fact-checker",
        agent=by_name["fact-checker"],
        prompt=prompts["fact-checker"],
        model=factchecker_model,
        step_label=f"revision-v{version}/fact-checker",
        dependencies=revision_dependencies["fact-checker"],
        outputs=factchecker_outputs,
        extra_values={
            "revision": version,
            "source_archive": archive_dir.name,
            "output_format": output_format,
        },
        metadata={"canonicalized_claim_lineage": True},
    )

    def run_revision_gate() -> dict:
        return run_publication_quality_gate(
            final_draft=final_draft,
            report_path=revision_gate,
            evidence_ledger_path=evidence_ledger,
            agent_names=[agent.name for agent in all_agents],
            claim_lineage_path=revision_lineage,
            output_format=output_format,
            length_instruction=length_instruction,
            raise_on_failure=True,
        )

    try:
        run_revision_gate()
    except PublicationQualityError:
        remediation = base / "final-draft-remediated.md"
        remediation_snapshots = _snapshot_revision_remediation_inputs(
            base=base,
            sources={
                "final-draft.md": final_draft,
                "quality-gate.json": revision_gate,
                "fact-check-report.md": base / "fact-check-report.md",
                "claim-lineage.jsonl": revision_lineage,
            },
        )
        remediation_rel = (
            (base / "remediation-inputs")
            .relative_to(repo_root)
            .as_posix()
        )
        remediation_prompt = (
            f"Read `{remediation_rel}/final-draft.md`, "
            f"`{remediation_rel}/quality-gate.json`, "
            f"`{remediation_rel}/fact-check-report.md`, "
            f"`{remediation_rel}/claim-lineage.jsonl`, "
            f"and `{evidence_ledger_rel}`.\n\n"
            "This is the revision's single publication-gate remediation pass. "
            "Fix every blocker against the underlying source. Do not add facts. "
            "Remove unsupported claims, repair exact footnote-to-claim lineage, "
            "and leave no internal or unverified release tag.\n\n"
            f"Write the remediated draft to `{base_rel}/final-draft-remediated.md`. "
            f"Rewrite `{base_rel}/claim-lineage.jsonl` with exact claim text, "
            "exact citation definitions, footnote IDs, evidence IDs, retained "
            "booleans, source-check booleans, and canonical statuses. Append a "
            f"remediation section to `{base_rel}/fact-check-report.md`."
        )
        remediation_prompt += _revision_system_prompt_block(
            "fact-check-remediation", revision_system_catalog
        )
        remediation_dependencies = (
            *tuple(
                _revision_dependency(repo_root, path)
                for path in remediation_snapshots.values()
            ),
            *_revision_system_dependencies(
                "fact-check-remediation", revision_system_catalog
            ),
        )
        remediation_outputs = (
            (remediation, contract_for_path(final_draft)),
            (revision_lineage, CLAIM_LINEAGE_AGENT_CONTRACT),
            (
                base / "fact-check-report.md",
                contract_for_path(base / "fact-check-report.md"),
            ),
        )
        await _run_revision_agent(
            state_path=revision_state_path,
            repo_root=repo_root,
            step_id="fact-check-remediation",
            agent=by_name["fact-checker"],
            user_prompt=remediation_prompt,
            model=factchecker_model,
            step_label=f"revision-v{version}/fact-check-remediation",
            tally=tally,
            output_path=remediation,
            artifact_contract=contract_for_path(final_draft),
            required_outputs=remediation_outputs[1:],
            dependencies=remediation_dependencies,
            extra_values={
                "revision": version,
                "source_archive": archive_dir.name,
                "output_format": output_format,
            },
        )
        shutil.copy2(remediation, final_draft)
        bind_claim_lineage_to_draft(
            final_draft=final_draft,
            output_path=revision_lineage,
        )
        run_revision_gate()
        # Canonicalization and promotion mutate the verifier's lineage/final
        # bytes after both model calls. Refresh both receipts so a safe resume
        # preserves the paid remediation instead of rerunning the verifier.
        _record_revision_agent_outputs(
            state_path=revision_state_path,
            repo_root=repo_root,
            step_id="fact-check-remediation",
            agent=by_name["fact-checker"],
            prompt=remediation_prompt,
            model=factchecker_model,
            step_label=f"revision-v{version}/fact-check-remediation",
            dependencies=remediation_dependencies,
            outputs=remediation_outputs,
            extra_values={
                "revision": version,
                "source_archive": archive_dir.name,
                "output_format": output_format,
            },
            metadata={
                "canonicalized_claim_lineage": True,
                "promoted_to_final_draft": True,
            },
        )
        _record_revision_agent_outputs(
            state_path=revision_state_path,
            repo_root=repo_root,
            step_id="fact-checker",
            agent=by_name["fact-checker"],
            prompt=prompts["fact-checker"],
            model=factchecker_model,
            step_label=f"revision-v{version}/fact-checker",
            dependencies=revision_dependencies["fact-checker"],
            outputs=factchecker_outputs,
            extra_values={
                "revision": version,
                "source_archive": archive_dir.name,
                "output_format": output_format,
            },
            metadata={
                "canonicalized_claim_lineage": True,
                "superseded_by": "fact-check-remediation",
            },
        )

    if not auto_approve:
        from cli.events import get_sink, request_checkpoint
        if get_sink() is not None:
            decision = await request_checkpoint("revision", {
                "title": f"Revised draft v{version} — review",
                "subtitle": "Approve to build the polished revised document.",
                "documents": [
                    {"name": f"Revised draft v{version}", "content": _read(final_draft)},
                ],
                "actions": ["approve", "abort"],
            }) or {"action": "abort"}
            if decision.get("action") != "approve":
                return None, tally
        else:
            console.rule(f"[bold]Revised draft v{version} — review[/bold]")
            _show_file_excerpt(final_draft, max_lines=50)
            answer = await _q.confirm(
                "Build the polished revised report document?", default=True
            ).ask_async()
            if not answer:
                console.print(
                    f"[yellow]Stopped. Revised draft saved at {base_rel}/final-draft.md "
                    f"but no Word document was built.[/yellow]"
                )
                return None, tally

    release_slug = f"{source.slug}-revised-v{version}"
    title = source.slug.replace("-", " ").title()
    if source.run_file is not None:
        for line in source.run_file.read_text(
            encoding="utf-8", errors="ignore"
        ).splitlines():
            if line.startswith("# Run:"):
                title = line[len("# Run:"):].strip()
                break

    visual_path: Path | None = None
    if output_format == "report" and revision_decision_frame_enabled:
        await emit(
            "stage_start",
            stage=4,
            label=f"Art direction and release for revision v{version}",
        )
        visual_path = base / "visual-brief.json"
        deck_mode = "board_decision"
        archived_manifest = archive_dir / "run-manifest.json"
        if archived_manifest.is_file():
            try:
                deck_mode = str(
                    json.loads(
                        archived_manifest.read_text(encoding="utf-8")
                    )
                    .get("run", {})
                    .get("deck_mode")
                    or deck_mode
                )
            except (OSError, json.JSONDecodeError):
                pass
        if deck_mode not in {
            "board_decision",
            "executive_briefing",
            "technical_read_ahead",
        }:
            deck_mode = "board_decision"
        visual_prompt = (
            f"Create the canonical Word-report visual contract for revision "
            f"v{version} of \"{title}\". Read `{base_rel}/feedback.md`, "
            f"`{base_rel}/final-draft.md`, `{base_rel}/fact-check-report.md`, "
            f"`{base_rel}/claim-lineage.jsonl`, and `{evidence_ledger_rel}`. "
            "Read the original airport context and run prompt from the archive "
            "when present. The revision may have changed the decision, so do not "
            "reuse an old visual plan without checking it against the revised "
            "draft. Use only canonical evidence IDs. Include every field in "
            "`assets/brand/visual-brief.schema.json`; the deck_mode contract is "
            f"`{deck_mode}` even though this revision currently releases Word. "
            f"Write valid JSON to `{base_rel}/visual-brief.json`."
        )
        visual_prompt += _revision_system_prompt_block(
            "art-direction", revision_system_catalog
        )
        art_dependencies: tuple[RevisionDependency, ...] = (
            _revision_dependency(repo_root, feedback_path),
            _revision_dependency(repo_root, revision_lineage),
            *_revision_system_dependencies(
                "art-direction", revision_system_catalog
            ),
            _revision_glob_dependency(
                repo_root,
                repo_root / "assets" / "brand",
                "**/*",
            ),
        )
        if visual_path.is_file():
            try:
                prior_visual = _validate_visual_brief(
                    out_path=visual_path,
                    schema_path=(
                        repo_root
                        / "assets"
                        / "brand"
                        / "visual-brief.schema.json"
                    ),
                    evidence_ledger=evidence_ledger,
                    requested_mode=deck_mode,
                )
            except (OSError, ValueError, json.JSONDecodeError):
                prior_visual = None
            if prior_visual is None or not prior_visual.valid:
                _quarantine_partial_output(visual_path)
        art_model = _model("art_direction")
        art_completion = await _run_revision_agent(
            state_path=revision_state_path,
            repo_root=repo_root,
            step_id="art-direction",
            agent=by_name["art-director"],
            user_prompt=visual_prompt,
            model=art_model,
            step_label=f"revision-v{version}/art-direction",
            tally=tally,
            output_path=visual_path,
            artifact_contract=_visual_brief_contract(),
            dependencies=art_dependencies,
            emit_completion=False,
            extra_values={
                "revision": version,
                "source_archive": archive_dir.name,
                "output_format": output_format,
                "deck_mode": deck_mode,
                "title": title,
            },
        )
        visual_validation = _validate_visual_brief(
            out_path=visual_path,
            schema_path=(
                repo_root / "assets" / "brand" / "visual-brief.schema.json"
            ),
            evidence_ledger=evidence_ledger,
            requested_mode=deck_mode,
        )
        await emit(
            "artifact_validated",
            step=f"revision-v{version}/visual-brief",
            **visual_validation.to_dict(),
        )
        if not visual_validation.valid:
            await emit(
                "agent_error",
                step=f"revision-v{version}/art-direction",
                agent="art-director",
                error_type="VisualBriefContractError",
                message="; ".join(visual_validation.errors[:8]),
            )
            _quarantine_partial_output(visual_path)
            raise RuntimeError(
                "Revision Art Director brief failed the canonical contract: "
                + "; ".join(visual_validation.errors[:8])
            )
        _record_revision_agent_outputs(
            state_path=revision_state_path,
            repo_root=repo_root,
            step_id="art-direction",
            agent=by_name["art-director"],
            prompt=visual_prompt,
            model=art_model,
            step_label=f"revision-v{version}/art-direction",
            dependencies=art_dependencies,
            outputs=((visual_path, _visual_brief_contract()),),
            extra_values={
                "revision": version,
                "source_archive": archive_dir.name,
                "output_format": output_format,
                "deck_mode": deck_mode,
                "title": title,
            },
            metadata={"canonical_schema_validated": True},
        )
        if not art_completion.get("skipped"):
            await emit(
                "agent_done",
                step=f"revision-v{version}/art-direction",
                agent="art-director",
                cost=art_completion.get("cost"),
                turns=art_completion.get("turns"),
                total=tally.total,
                provider=art_completion.get("provider"),
                billed_separately=False,
            )

    stage4_dir = base / "stage4"
    report_path = stage4_dir / f"{release_slug}.docx"
    executive_path = (
        stage4_dir / f"{release_slug}-executive-summary.docx"
        if output_format == "report" and revision_decision_frame_enabled
        else None
    )
    word_outputs = (
        (report_path, contract_for_path(report_path)),
        *(
            ((executive_path, contract_for_path(executive_path)),)
            if executive_path is not None
            else ()
        ),
    )
    word_build_dependencies: tuple[RevisionDependency, ...] = (
        _revision_dependency(repo_root, final_draft),
        *(
            (_revision_dependency(repo_root, visual_path),)
            if visual_path is not None
            else ()
        ),
        *(
            (
                _revision_dependency(
                    repo_root, repo_root / "docs" / "methodology.md"
                ),
            )
            if output_format == "report"
            else ()
        ),
        _revision_glob_dependency(
            repo_root,
            repo_root / "assets" / "brand",
            "**/*",
        ),
        RevisionDependency("cli/docx_builder.py"),
        RevisionDependency("cli/publishing_quality.py"),
    )
    word_build_values: dict[str, object] = {
        "revision": version,
        "source_archive": archive_dir.name,
        "slug": release_slug,
        "title": title,
        "output_format": output_format,
        "decision_frame_enabled": revision_decision_frame_enabled,
        "decision_context": revision_decision_context,
        "revision_label": f"Revised — Version {version}",
        "executive_summary_target_words": executive_summary_target_words,
    }
    word_build_reusable, word_build_fingerprint = revision_step_matches(
        state_path=revision_state_path,
        repo_root=repo_root,
        step_id="word-production",
        dependencies=word_build_dependencies,
        values=word_build_values,
        outputs=word_outputs,
    )
    if word_build_fingerprint.get("complete") is not True:
        raise RuntimeError(
            "Revision Word production cannot bind its source and design "
            "contracts."
        )
    if not word_build_reusable:
        for path, _ in word_outputs:
            _quarantine_partial_output(path)
            _quarantine_partial_output(
                path.with_name(
                    f"{path.stem}-word-visual-inspection.json"
                )
            )
            _quarantine_partial_output(
                path.with_name(
                    f"{path.stem}-word-visual-inspection-input.json"
                )
            )
        report_path, executive_path = build_documents(
            slug=release_slug,
            title=title,
            final_draft=final_draft,
            methodology=repo_root / "docs" / "methodology.md",
            out_dir=stage4_dir,
            output_format=output_format,
            decision_frame_enabled=revision_decision_frame_enabled,
            visual_brief=visual_path,
            decision_context=revision_decision_context,
            revision_label=f"Revised — Version {version}",
            executive_summary_target_words=executive_summary_target_words,
        )
        record_revision_step(
            state_path=revision_state_path,
            repo_root=repo_root,
            step_id="word-production",
            dependencies=word_build_dependencies,
            values=word_build_values,
            outputs=word_outputs,
            metadata={"producer": "orchestrator"},
        )
    word_artifacts = [
        report_path,
        *([executive_path] if executive_path is not None else []),
    ]
    receipt_inputs = tuple(
        artifact.with_name(
            f"{artifact.stem}-word-visual-inspection-input.json"
        )
        for artifact in word_artifacts
    )
    word_inspection_dependencies: tuple[RevisionDependency, ...] = (
        *tuple(
            _revision_dependency(repo_root, artifact)
            for artifact in word_artifacts
        ),
        *tuple(
            _revision_dependency(
                repo_root, receipt_input, required=False
            )
            for receipt_input in receipt_inputs
        ),
        *tuple(
            _revision_glob_dependency(
                repo_root,
                artifact.parent / "qa" / artifact.stem,
                "**/*",
                required=False,
            )
            for artifact in word_artifacts
        ),
        RevisionDependency("cli/docx_builder.py"),
        RevisionDependency("cli/publishing_quality.py"),
    )
    await run_word_visual_inspection(
        artifacts=word_artifacts,
        outputs_dir=base,
        all_agents=all_agents,
        tally=tally,
        manifest_path=None,
        step_label=f"revision-v{version}/word-visual-inspection",
        revision_state_path=revision_state_path,
        revision_repo_root=repo_root,
        revision_dependencies=word_inspection_dependencies,
        revision_receipt_inputs=receipt_inputs,
        revision_extra_values={
            "revision": version,
            "source_archive": archive_dir.name,
            "output_format": output_format,
            "title": title,
        },
    )
    required_revision_steps = {
        "strategist-a",
        "red-team",
        "strategist-b",
        "editor",
        "humanizer",
        "fact-checker",
        "word-production",
        "word-visual-inspection",
    }
    if visual_path is not None:
        required_revision_steps.add("art-direction")
    remediated_draft = base / "final-draft-remediated.md"
    if (
        remediated_draft.is_file()
        and file_sha256(remediated_draft) == file_sha256(final_draft)
    ):
        required_revision_steps.add("fact-check-remediation")
    release_dir = base / "release"
    # Re-read every dependency and output before staging and again before
    # promotion. A mutation cannot hide behind a once-valid receipt or the
    # staged bundle's independent Office QA.
    published = _publish_revision_release(
        state_path=revision_state_path,
        repo_root=repo_root,
        required_steps=required_revision_steps,
        stage4_dir=stage4_dir,
        slug=release_slug,
        release_dir=release_dir,
        require_executive_summary=executive_path is not None,
        out_dir=REPORTS_DIR,
    )
    out_path = published["word_report"]

    revision_manifest = {
        "schema_version": "1.0",
        "slug": source.slug,
        "revision": version,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_archive": archive_dir.name,
        "source_draft_sha256": file_sha256(src_draft),
        "feedback_sha256": file_sha256(base / "feedback.md"),
        "final_draft_sha256": file_sha256(final_draft),
        "claim_lineage_sha256": file_sha256(revision_lineage),
        "quality_gate_sha256": file_sha256(revision_gate),
        "visual_brief_sha256": (
            file_sha256(visual_path) if visual_path is not None else None
        ),
        "word_report_sha256": file_sha256(report_path),
        "executive_summary_sha256": (
            file_sha256(executive_path)
            if executive_path is not None
            else None
        ),
        "release_manifest_sha256": file_sha256(
            release_dir / "release-manifest.json"
        ),
        "revision_execution_sha256": file_sha256(revision_state_path),
        "required_steps": sorted(required_revision_steps),
        "claude_cost_usd": tally.total,
        "status": "released",
    }
    revision_manifest_path = base / "revision-manifest.json"
    temporary_revision_manifest = revision_manifest_path.with_name(
        f".{revision_manifest_path.name}.tmp"
    )
    temporary_revision_manifest.write_text(
        json.dumps(revision_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary_revision_manifest, revision_manifest_path)
    console.print(
        f"[green]Revised report released:[/green] "
        f"{out_path.relative_to(repo_root)}"
    )
    return out_path, tally
