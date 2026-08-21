"""Run-manifest contract for dynamic Council orchestration.

``outputs/run-manifest.json`` is the single source of truth for which research
agents were seated and which artifacts every downstream stage must consume.
Process prompts may evolve, but they no longer need to hard-code a roster or a
list of brief filenames.
"""
from __future__ import annotations

from copy import deepcopy
import json
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from cli.artifacts import (
    ArtifactContract,
    ArtifactValidation,
    contract_for_path,
    validate_artifact,
)


SCHEMA_VERSION = "2.0"
MANIFEST_NAME = "run-manifest.json"
DEPENDENCY_FINGERPRINT_VERSION = "1.0"
EXECUTION_CONTRACT_PATTERNS: tuple[str, ...] = (
    "AGENTS.md",
    "CLAUDE.md",
    "council.toml",
    "pyproject.toml",
    "prompts/orchestration.md",
    "prompts/research-contract.md",
    "assets/brand/README.md",
    "assets/brand/*.json",
    "cli/*.py",
)

# Modules that carry a run to the operator but do not generate its content.
#
# The contract exists to stop a resume from stitching together artifacts that
# no two versions of the code would ever produce together. Transport and UI
# code cannot cause that: a WebSocket reconnect fix, a terminal menu tweak, or
# a change to the audit reader has no path to the text of a brief or the bytes
# of a .docx. Hashing them as blocking meant every edit to this app bricked
# resume for whatever was mid-flight — the tripwire fired on its own authors.
#
# These are still fingerprinted and still recorded in the manifest, so the
# receipt stays complete and an investigator can see exactly what moved. They
# just don't refuse the resume.
#
# The list is a DENYLIST on purpose. A new module added to cli/ is blocking
# until someone deliberately declares it inert, so the failure mode of
# forgetting is a loud false refusal, never a silently corrupt resume.
#
# server.py builds a spec for NEW runs (_build_spec), which does shape output —
# but a resume reads its spec from the manifest, where it is hashed separately.
APP_SHELL_PATHS: frozenset[str] = frozenset(
    {
        "cli/__main__.py",     # argv parsing
        "cli/audit.py",        # post-hoc retrospective reader
        "cli/events.py",       # event sink and transport
        "cli/interactive.py",  # terminal prompts
        "cli/menu.py",         # terminal UI
        "cli/resume_repair.py",  # the repair tool itself
        "cli/server.py",       # HTTP/WebSocket transport and dispatch
    }
)


def generation_contract_records(
    records: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """The subset of the contract whose bytes can change a run's output."""

    return [r for r in records if str(r.get("path", "")) not in APP_SHELL_PATHS]


class ResumeContractMismatch(RuntimeError):
    """Raised when paid artifacts no longer match the executable run contract."""


class CheckpointInputsChanged(RuntimeError):
    """Raised when checkpoint inputs no longer match the reviewed snapshot."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _contract_dict(contract: ArtifactContract) -> dict[str, Any]:
    return {
        "kind": contract.kind,
        "min_words": contract.min_words,
        "min_records": contract.min_records,
        "required_keys": list(contract.required_keys),
        "required_any": [list(group) for group in contract.required_any],
        "requires_with": [
            [trigger, list(dependents)]
            for trigger, dependents in contract.requires_with
        ],
        "optional": contract.optional,
    }


def _file_fingerprint(path: Path) -> tuple[str | None, int | None]:
    try:
        if not path.is_file():
            return None, None
        return hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_size
    except OSError:
        return None, None


def build_execution_contract_fingerprint(
    repo_root: Path,
) -> list[dict[str, Any]]:
    """Fingerprint the local code, prompts, and design rules that shape a run."""

    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for pattern in EXECUTION_CONTRACT_PATTERNS:
        for path in sorted(repo_root.glob(pattern)):
            if not path.is_file():
                continue
            relative = path.relative_to(repo_root).as_posix()
            if relative in seen:
                continue
            if path.is_symlink():
                raise ResumeContractMismatch(
                    f"Execution-contract file may not be a symlink: {relative}"
                )
            sha256, size_bytes = _file_fingerprint(path)
            records.append(
                {
                    "path": relative,
                    "sha256": sha256,
                    "size_bytes": size_bytes,
                }
            )
            seen.add(relative)
    records.sort(key=lambda item: str(item["path"]))
    return records


def build_dependency_fingerprint(
    manifest_path: Path,
    declared_inputs: Iterable[str],
) -> dict[str, Any]:
    """Bind one artifact generation to the exact upstream bytes it consumed.

    ``run-manifest.json`` is represented by the stable executable run identity
    rather than its mutable file bytes. Other declarations may be exact
    output-relative paths or glob patterns. Glob membership is part of the
    receipt, so adding or removing a selected upstream artifact invalidates a
    downstream resume just as changing its bytes does.
    """

    payload = load_run_manifest(manifest_path)
    outputs_dir = manifest_path.parent.resolve()
    declarations = list(dict.fromkeys(str(item) for item in declared_inputs))
    input_records: list[dict[str, Any]] = []
    complete = True

    for declaration in declarations:
        record: dict[str, Any] = {
            "declared_input": declaration,
            "files": [],
        }
        if declaration == MANIFEST_NAME:
            run_identity = str(
                payload.get("run", {}).get("resume_identity_sha256") or ""
            )
            if len(run_identity) != 64:
                complete = False
                record["error"] = "run identity is missing"
            else:
                record["files"] = [
                    {
                        "path": MANIFEST_NAME,
                        "kind": "run_identity",
                        "sha256": run_identity,
                        "size_bytes": None,
                    }
                ]
            input_records.append(record)
            continue

        relative = Path(declaration)
        if relative.is_absolute() or ".." in relative.parts:
            complete = False
            record["error"] = "input path escapes outputs/"
            input_records.append(record)
            continue

        has_glob = any(character in declaration for character in "*?[")
        try:
            candidates = (
                sorted(outputs_dir.glob(declaration))
                if has_glob
                else [outputs_dir / relative]
            )
        except (OSError, ValueError):
            candidates = []

        for candidate in candidates:
            try:
                resolved = candidate.resolve(strict=True)
                resolved.relative_to(outputs_dir)
            except (OSError, ValueError):
                complete = False
                continue
            if candidate.is_symlink() or not resolved.is_file():
                complete = False
                continue
            sha256, size_bytes = _file_fingerprint(resolved)
            if not sha256 or size_bytes is None:
                complete = False
                continue
            record["files"].append(
                {
                    "path": resolved.relative_to(outputs_dir).as_posix(),
                    "kind": "file",
                    "sha256": sha256,
                    "size_bytes": size_bytes,
                }
            )
        record["files"].sort(key=lambda item: str(item["path"]))
        if not record["files"]:
            complete = False
            record["error"] = "no regular input files matched"
        input_records.append(record)

    fingerprint: dict[str, Any] = {
        "schema_version": DEPENDENCY_FINGERPRINT_VERSION,
        "complete": complete,
        "inputs": input_records,
    }
    fingerprint["sha256"] = dependency_fingerprint_sha256(fingerprint)
    return fingerprint


def dependency_fingerprint_sha256(fingerprint: object) -> str:
    """Return the canonical digest for a dependency receipt body.

    A dependency fingerprint is written in more than one place: normal
    artifact completion, resume-manifest refresh, and the audited re-baseline
    tool.  Keeping the serializer here prevents one writer from changing the
    receipt body without refreshing the digest that validates it.
    """

    if not isinstance(fingerprint, dict):
        raise TypeError("Dependency fingerprint must be a mapping.")
    body = {
        key: value
        for key, value in fingerprint.items()
        if key != "sha256"
    }
    return hashlib.sha256(
        json.dumps(
            body,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


def refresh_dependency_fingerprint_sha256(fingerprint: object) -> bool:
    """Refresh a stored receipt digest in place; return whether it was valid."""

    if not isinstance(fingerprint, dict):
        return False
    try:
        fingerprint["sha256"] = dependency_fingerprint_sha256(fingerprint)
    except (TypeError, ValueError):
        return False
    return True


def _repair_audited_rebaseline_dependency_digest(
    fingerprint: object,
    *,
    prior_manifest: dict[str, Any],
    artifact_path: str,
) -> bool:
    """Repair only the historical, audited re-baseline digest defect.

    Older versions of ``resume_repair`` moved an embedded run identity without
    recomputing the receipt's outer digest.  An arbitrary stale digest must
    remain invalid: otherwise a resume could turn receipt tampering into a
    trusted record.  We therefore repair only when reversing the recorded
    re-baseline transitions reconstructs the exact body covered by the stale
    digest, and only for an artifact named in those audit entries.
    """

    if not isinstance(fingerprint, dict):
        return False
    recorded_digest = fingerprint.get("sha256")
    if not isinstance(recorded_digest, str) or len(recorded_digest) != 64:
        return False
    try:
        if recorded_digest == dependency_fingerprint_sha256(fingerprint):
            return False
    except (TypeError, ValueError):
        return False

    audits = prior_manifest.get("resume_rebaselines")
    if not isinstance(audits, list):
        return False
    historical = deepcopy(fingerprint)
    for audit in reversed(audits):
        if not isinstance(audit, dict):
            continue
        restamped = audit.get("restamped_dependency_receipts")
        if not isinstance(restamped, list) or artifact_path not in restamped:
            continue
        previous = audit.get("previous_identity_sha256")
        current = audit.get("new_identity_sha256")
        if (
            not isinstance(previous, str)
            or not isinstance(current, str)
            or len(previous) != 64
            or len(current) != 64
        ):
            continue
        changed = False
        inputs = historical.get("inputs")
        if not isinstance(inputs, list):
            return False
        for record in inputs:
            if not isinstance(record, dict):
                continue
            files = record.get("files")
            if not isinstance(files, list):
                continue
            for entry in files:
                if (
                    isinstance(entry, dict)
                    and entry.get("kind") == "run_identity"
                    and entry.get("sha256") == current
                ):
                    entry["sha256"] = previous
                    changed = True
        if not changed:
            continue
        try:
            reconstructed_digest = dependency_fingerprint_sha256(historical)
        except (TypeError, ValueError):
            return False
        if reconstructed_digest == recorded_digest:
            return refresh_dependency_fingerprint_sha256(fingerprint)
    return False


def dependency_fingerprint_matches(
    manifest_path: Path,
    recorded: object,
) -> bool:
    """Return whether a recorded upstream receipt still matches current bytes."""

    if not isinstance(recorded, dict) or recorded.get("complete") is not True:
        return False
    inputs = recorded.get("inputs")
    if not isinstance(inputs, list):
        return False
    declarations = [
        str(item.get("declared_input") or "")
        for item in inputs
        if isinstance(item, dict)
    ]
    if (
        len(declarations) != len(inputs)
        or any(not declaration for declaration in declarations)
    ):
        return False
    try:
        recorded_digest = dependency_fingerprint_sha256(recorded)
    except (TypeError, ValueError):
        return False
    if recorded.get("sha256") != recorded_digest:
        return False
    current = build_dependency_fingerprint(manifest_path, declarations)
    return bool(
        current.get("complete") is True
        and current.get("sha256") == recorded.get("sha256")
    )


def _artifact(
    artifact_id: str,
    path: str,
    *,
    stage: str,
    producer: str,
    role: str,
    optional: bool = False,
    contract: ArtifactContract | None = None,
) -> dict[str, Any]:
    contract = contract or contract_for_path(Path(path), optional=optional)
    return {
        "id": artifact_id,
        "path": path,
        "stage": stage,
        "producer": producer,
        "role": role,
        "required": not optional,
        "status": "pending",
        "contract": _contract_dict(contract),
    }


def _expected_artifacts(spec: Any) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = [
        _artifact(
            "context/airport-context",
            "context/airport-context.md",
            stage="context",
            producer="airport-context-builder",
            role="airport_context",
        ),
        _artifact(
            "context/sources",
            "context/context-sources.jsonl",
            stage="context",
            producer="airport-context-builder",
            role="context_sources",
            contract=ArtifactContract(
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
            ),
        ),
    ]
    for name in list(getattr(spec, "selected_research_agents", []) or []):
        artifacts.extend(
            (
                _artifact(
                    f"stage1/{name}/brief",
                    f"stage1/{name}-brief.md",
                    stage="research",
                    producer=name,
                    role="research_brief",
                ),
                _artifact(
                    f"stage1/{name}/evidence",
                    f"stage1/{name}-evidence.jsonl",
                    stage="research",
                    producer=name,
                    role="agent_evidence",
                    optional=name == "deep-research",
                    contract=ArtifactContract(
                        "jsonl",
                        min_records=1,
                        required_keys=(
                            "claim",
                            "source_title",
                            "source_type",
                            "confidence",
                        ),
                        required_any=(("source_url", "source_path", "source_citation"),),
                    requires_with=(("source_citation", ("page_or_section",)),),
                        optional=name == "deep-research",
                    ),
                ),
            )
        )
    if "quantitative-analyst" in set(
        getattr(spec, "selected_research_agents", []) or []
    ):
        artifacts.extend(
            (
                _artifact(
                    "stage1/quantitative/calculations",
                    "stage1/quantitative-analysis/calculations.json",
                    stage="research",
                    producer="quantitative-analyst",
                    role="reproducible_calculations",
                ),
                _artifact(
                    "stage1/quantitative/readme",
                    "stage1/quantitative-analysis/README.md",
                    stage="research",
                    producer="quantitative-analyst",
                    role="reproduction_instructions",
                ),
            )
        )
    artifacts.extend(
        (
            _artifact(
                "evidence/ledger",
                "evidence-ledger.jsonl",
                stage="evidence",
                producer="orchestrator",
                role="evidence_ledger",
                contract=ArtifactContract(
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
                ),
            ),
            _artifact(
                "evidence/ledger-compatibility",
                "stage1/evidence-ledger.jsonl",
                stage="evidence",
                producer="orchestrator",
                role="evidence_ledger_compatibility",
                optional=True,
            ),
            _artifact(
                "evidence/curation",
                "stage1/evidence-map.md",
                stage="evidence",
                producer="evidence-curator",
                role="evidence_curation_and_gap_analysis",
            ),
            _artifact(
                "stage2/narrative-options",
                "stage2/narrative-options.md",
                stage="synthesis",
                producer="creative-director",
                role="creative_framing",
            ),
            _artifact(
                "stage2/strategist-v1",
                "stage2/strategist-draft-v1.md",
                stage="synthesis",
                producer="strategist",
                role="draft",
            ),
            _artifact(
                "stage2/evidence-prosecutor",
                "stage2/red-team-critique-v1.md",
                stage="synthesis",
                producer="evidence-prosecutor",
                role="evidence_review",
            ),
            _artifact(
                "stage2/strategist-v2",
                "stage2/strategist-draft-v2.md",
                stage="synthesis",
                producer="strategist",
                role="draft",
            ),
            _artifact(
                "stage2/airport-executive-review",
                "stage2/red-team-critique-v2.md",
                stage="synthesis",
                producer="airport-executive-reviewer",
                role="airport_execution_review",
            ),
            _artifact(
                "stage2/strategist-v3",
                "stage2/strategist-draft-v3.md",
                stage="synthesis",
                producer="strategist",
                role="draft",
            ),
            _artifact(
                "stage3/edited",
                "stage3/edited-draft.md",
                stage="polish",
                producer="editor",
                role="edited_draft",
            ),
            _artifact(
                "stage3/editor-notes",
                "stage3/editor-notes.md",
                stage="polish",
                producer="editor",
                role="editor_notes",
            ),
            _artifact(
                "stage3/humanized",
                "stage3/humanized-draft.md",
                stage="polish",
                producer="humanizer",
                role="humanized_draft",
            ),
            _artifact(
                "stage3/final",
                "stage3/final-draft.md",
                stage="verification",
                producer="fact-checker",
                role="final_draft",
            ),
            _artifact(
                "stage3/fact-check",
                "stage3/fact-check-report.md",
                stage="verification",
                producer="fact-checker",
                role="fact_check_report",
            ),
            _artifact(
                "verification/claim-lineage",
                "claim-lineage.jsonl",
                stage="verification",
                producer="fact-checker",
                role="claim_lineage",
                contract=ArtifactContract(
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
                ),
            ),
            _artifact(
                "verification/quality-gate",
                "quality-gate.json",
                stage="verification",
                producer="orchestrator",
                role="publication_quality_gate",
            ),
        )
    )
    output_format = str(getattr(spec, "output_format", "report"))
    want_pptx = bool(getattr(spec, "want_pptx", False))
    needs_visual_brief = want_pptx or output_format not in {
        "brief",
        "recommendations",
    }
    visual_artifact = _artifact(
        "stage4/visual-brief",
        "stage4/visual-brief.json",
        stage="production",
        producer="art-director",
        role="visual_brief",
        optional=not needs_visual_brief,
    )
    if not needs_visual_brief:
        visual_artifact["status"] = "skipped"
        visual_artifact["skip_reason"] = (
            "short output format without a companion presentation"
        )
    artifacts.append(visual_artifact)
    slug = str(getattr(spec, "slug", "council-report"))
    artifacts.append(
        _artifact(
            "stage4/word-report",
            f"stage4/{slug}.docx",
            stage="production",
            producer="orchestrator",
            role="word_report",
        )
    )
    artifacts.append(
        _artifact(
            "stage4/word-visual-inspection",
            f"stage4/{slug}-word-visual-inspection.json",
            stage="production",
            producer="art-director",
            role="word_visual_inspection",
            contract=ArtifactContract(
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
            ),
        )
    )
    executive_artifact = _artifact(
        "stage4/executive-summary",
        f"stage4/{slug}-executive-summary.docx",
        stage="production",
        producer="orchestrator",
        role="executive_summary",
        optional=output_format in {"brief", "recommendations"},
    )
    if output_format in {"brief", "recommendations"}:
        executive_artifact["status"] = "skipped"
        executive_artifact["skip_reason"] = (
            "short output format is already an executive-length deliverable"
        )
    artifacts.append(executive_artifact)
    executive_inspection = _artifact(
        "stage4/executive-summary-visual-inspection",
        f"stage4/{slug}-executive-summary-word-visual-inspection.json",
        stage="production",
        producer="art-director",
        role="executive_summary_visual_inspection",
        optional=output_format in {"brief", "recommendations"},
        contract=ArtifactContract(
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
            optional=output_format in {"brief", "recommendations"},
        ),
    )
    if output_format in {"brief", "recommendations"}:
        executive_inspection["status"] = "skipped"
        executive_inspection["skip_reason"] = (
            "short output format has no executive-summary document"
        )
    artifacts.append(executive_inspection)
    artifacts.append(
        _artifact(
            "stage4/publishing-quality",
            "publishing-quality.json",
            stage="production",
            producer="orchestrator",
            role="publishing_quality",
            contract=ArtifactContract(
                "json",
                required_keys=("artifact", "kind", "ok", "issues"),
            ),
        )
    )
    if want_pptx:
        artifacts.extend(
            (
                _artifact(
                    "stage4/presentation",
                    f"stage4/{slug}.pptx",
                    stage="production",
                    producer="presentation-designer",
                    role="presentation",
                ),
                _artifact(
                    "stage4/presentation-qa",
                    f"stage4/{slug}-qa.json",
                    stage="production",
                    producer="orchestrator",
                    role="presentation_qa",
                    contract=ArtifactContract(
                        "json",
                        required_keys=("artifact", "kind", "ok", "issues"),
                    ),
                ),
                _artifact(
                    "stage4/visual-inspection",
                    f"stage4/{slug}-visual-inspection.json",
                    stage="production",
                    producer="presentation-designer",
                    role="visual_inspection",
                    contract=ArtifactContract(
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
                    ),
                ),
            )
        )
    artifacts.extend(
        (
            _artifact(
                "release/word-report",
                f"release/{slug}.docx",
                stage="release",
                producer="orchestrator",
                role="release_word_report",
            ),
            _artifact(
                "release/word-qa",
                f"release/qa/{slug}.docx.qa.json",
                stage="release",
                producer="orchestrator",
                role="release_word_qa",
                contract=ArtifactContract(
                    "json",
                    required_keys=("artifact", "kind", "ok", "issues"),
                ),
            ),
            _artifact(
                "release/word-visual-inspection",
                f"release/{slug}-word-visual-inspection.json",
                stage="release",
                producer="orchestrator",
                role="release_word_visual_inspection",
                contract=ArtifactContract(
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
                ),
            ),
        )
    )
    release_executive = _artifact(
        "release/executive-summary",
        f"release/{slug}-executive-summary.docx",
        stage="release",
        producer="orchestrator",
        role="release_executive_summary",
        optional=output_format in {"brief", "recommendations"},
    )
    release_executive_qa = _artifact(
        "release/executive-summary-qa",
        f"release/qa/{slug}-executive-summary.docx.qa.json",
        stage="release",
        producer="orchestrator",
        role="release_executive_summary_qa",
        optional=output_format in {"brief", "recommendations"},
        contract=ArtifactContract(
            "json",
            required_keys=("artifact", "kind", "ok", "issues"),
            optional=output_format in {"brief", "recommendations"},
        ),
    )
    release_executive_inspection = _artifact(
        "release/executive-summary-visual-inspection",
        f"release/{slug}-executive-summary-word-visual-inspection.json",
        stage="release",
        producer="orchestrator",
        role="release_executive_summary_visual_inspection",
        optional=output_format in {"brief", "recommendations"},
        contract=ArtifactContract(
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
            optional=output_format in {"brief", "recommendations"},
        ),
    )
    if output_format in {"brief", "recommendations"}:
        for item in (
            release_executive,
            release_executive_qa,
            release_executive_inspection,
        ):
            item["status"] = "skipped"
            item["skip_reason"] = (
                "short output format is already an executive-length deliverable"
            )
    artifacts.extend(
        (
            release_executive,
            release_executive_qa,
            release_executive_inspection,
        )
    )
    if want_pptx:
        artifacts.extend(
            (
                _artifact(
                    "release/presentation",
                    f"release/{slug}.pptx",
                    stage="release",
                    producer="orchestrator",
                    role="release_presentation",
                ),
                _artifact(
                    "release/presentation-qa",
                    f"release/qa/{slug}.pptx.qa.json",
                    stage="release",
                    producer="orchestrator",
                    role="release_presentation_qa",
                    contract=ArtifactContract(
                        "json",
                        required_keys=("artifact", "kind", "ok", "issues"),
                    ),
                ),
                _artifact(
                    "release/visual-inspection",
                    f"release/{slug}-visual-inspection.json",
                    stage="release",
                    producer="orchestrator",
                    role="release_visual_inspection",
                    contract=ArtifactContract(
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
                    ),
                ),
            )
        )
    artifacts.append(
        _artifact(
            "release/manifest",
            "release/release-manifest.json",
            stage="release",
            producer="orchestrator",
            role="release_manifest",
            contract=ArtifactContract(
                "json",
                required_keys=("schema_version", "slug", "artifacts"),
            ),
        )
    )
    return artifacts


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def load_run_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def create_run_manifest(
    *,
    spec: Any,
    run_file: Path,
    outputs_dir: Path,
    all_agents: Iterable[Any],
    resume: bool = False,
    pipeline_steps: Iterable[Any] = (),
    model_assignments: dict[str, str] | None = None,
) -> Path:
    """Create or refresh the canonical manifest and return its path."""

    path = outputs_dir / MANIFEST_NAME
    selected_names = list(getattr(spec, "selected_research_agents", []) or [])
    agents_by_name = {agent.name: agent for agent in all_agents}
    model_assignments = model_assignments or {}

    def agent_contract(
        name: str, *, model_role: str, override: str = ""
    ) -> dict[str, Any]:
        agent = agents_by_name.get(name)
        prompt_path = getattr(agent, "path", None)
        prompt_sha256 = None
        prompt_rel = None
        if isinstance(prompt_path, Path) and prompt_path.is_file():
            prompt_rel = _relative(prompt_path, repo_root)
            prompt_sha256, _ = _file_fingerprint(prompt_path)
        return {
            "name": name,
            "display_name": getattr(agent, "display_name", name),
            "provider": getattr(agent, "provider", "unknown"),
            "prompt_path": prompt_rel,
            "prompt_sha256": prompt_sha256,
            "model_role": model_role,
            "model_id": (
                getattr(agent, "model_override", None)
                or model_assignments.get(model_role)
            ),
            "override": override,
        }

    repo_root = outputs_dir.parent
    source_material: list[dict[str, Any]] = []
    source_root = (
        repo_root / "sources" / "runs" / str(getattr(spec, "slug", ""))
    )
    for source_component in (
        repo_root / "sources",
        repo_root / "sources" / "runs",
        source_root,
    ):
        if source_component.is_symlink():
            raise ResumeContractMismatch(
                "Run source library may not traverse symlinks: "
                f"{source_component}"
            )
    source_root_resolved = (
        source_root.resolve(strict=True)
        if source_root.exists()
        else source_root.resolve(strict=False)
    )
    for raw_path in list(getattr(spec, "source_paths", []) or []):
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        try:
            resolved_candidate = candidate.resolve(strict=True)
            relative_source = resolved_candidate.relative_to(
                source_root_resolved
            )
            lexical_relative = candidate.absolute().relative_to(
                source_root.absolute()
            )
        except (OSError, ValueError) as exc:
            raise ResumeContractMismatch(
                "Executable source paths must be regular files inside "
                f"sources/runs/{getattr(spec, 'slug', '')}/: {raw_path}"
            ) from exc
        cursor = source_root.absolute()
        if candidate.is_symlink():
            raise ResumeContractMismatch(
                f"Executable source path may not be a symlink: {raw_path}"
            )
        for part in lexical_relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ResumeContractMismatch(
                    "Executable source path may not traverse symlinks: "
                    f"{raw_path}"
                )
        if not resolved_candidate.is_file():
            raise ResumeContractMismatch(
                f"Executable source path is not a regular file: {raw_path}"
            )
        archive_path = (Path("sources") / relative_source).as_posix()
        source_sha256, source_size = _file_fingerprint(resolved_candidate)
        source_material.append(
            {
                "runtime_path": _relative(resolved_candidate, repo_root),
                "archive_path": archive_path,
                "sha256": source_sha256,
                "size_bytes": source_size,
            }
        )
    source_library: list[dict[str, Any]] = []
    if source_root.is_dir() and source_material:
        for library_file in sorted(source_root.rglob("*")):
            if library_file.is_symlink():
                raise ResumeContractMismatch(
                    "Run source library may not contain symlinks: "
                    f"{library_file}"
                )
            if not library_file.is_file():
                continue
            library_sha256, library_size = _file_fingerprint(library_file)
            source_library.append(
                {
                    "path": library_file.relative_to(source_root).as_posix(),
                    "sha256": library_sha256,
                    "size_bytes": library_size,
                }
            )
    selected_agents = []
    for name in selected_names:
        contract = agent_contract(
            name,
            model_role="research",
            override=dict(getattr(spec, "agent_overrides", {}) or {}).get(name, ""),
        )
        contract["brief_path"] = f"stage1/{name}-brief.md"
        contract["evidence_path"] = f"stage1/{name}-evidence.jsonl"
        selected_agents.append(contract)

    pipeline_steps = tuple(pipeline_steps)
    process_agents: list[dict[str, Any]] = []
    seen_process: set[str] = set()
    for step in pipeline_steps:
        name = str(getattr(step, "agent", ""))
        role = str(getattr(step, "model_role", ""))
        if not name or name in seen_process:
            continue
        seen_process.add(name)
        process_agents.append(agent_contract(name, model_role=role))

    run_prompt_sha256, run_prompt_size = _file_fingerprint(run_file)
    execution_contract = build_execution_contract_fingerprint(repo_root)
    identity_payload = {
        "schema_version": SCHEMA_VERSION,
        "run": {
            "slug": str(getattr(spec, "slug", "")),
            "title": str(getattr(spec, "title", "")),
            "thesis": str(getattr(spec, "thesis", "")),
            "audience": str(getattr(spec, "audience", "")),
            "tone": str(getattr(spec, "tone", "")),
            "length": str(getattr(spec, "length", "")),
            "output_format": str(getattr(spec, "output_format", "report")),
            "want_pptx": bool(getattr(spec, "want_pptx", False)),
            "deck_mode": str(getattr(spec, "deck_mode", "board") or "board"),
            "decision_required": str(
                getattr(spec, "decision_required", "") or ""
            ),
            "decision_owner": str(getattr(spec, "decision_owner", "") or ""),
            "time_horizon": str(getattr(spec, "time_horizon", "") or ""),
            "approval_path": str(getattr(spec, "approval_path", "") or ""),
            "success_measure": str(getattr(spec, "success_measure", "") or ""),
            "operator_context": str(getattr(spec, "operator_context", "") or ""),
            "is_not": list(getattr(spec, "is_not", []) or []),
            "is_yes": list(getattr(spec, "is_yes", []) or []),
            "success_criteria": list(
                getattr(spec, "success_criteria", []) or []
            ),
            "run_prompt_sha256": run_prompt_sha256,
            "run_prompt_size": run_prompt_size,
        },
        "source_material": source_material,
        "source_library": source_library,
        # Only generation code binds the identity. App-shell modules are still
        # recorded in the manifest for the receipt; see APP_SHELL_PATHS.
        "execution_contract": generation_contract_records(execution_contract),
        # Identity is order-insensitive for the roster. WHICH agents are seated
        # is the contract; the order the operator happened to click them is not.
        # The web form records selection order while the run prompt normalizes
        # to registry order, so an order-sensitive hash refuses legitimate
        # resumes. Execution order is unchanged — this sorts the hashed copy only.
        "selected_research_agents": sorted(
            selected_agents, key=lambda item: str(item.get("name", ""))
        ),
        "process_agents": process_agents,
        "pipeline": [
            {
                "id": str(getattr(step, "id", "")),
                "phase": str(getattr(step, "phase", "")),
                "agent": str(getattr(step, "agent", "")),
                "model_role": str(getattr(step, "model_role", "")),
                "model_id": model_assignments.get(
                    str(getattr(step, "model_role", ""))
                ),
                "inputs": list(getattr(step, "inputs", ())),
                "output": str(getattr(step, "output", "")),
                "quality_gate": str(
                    getattr(step, "quality_gate", "typed_artifact")
                ),
            }
            for step in pipeline_steps
        ],
    }
    resume_identity_sha256 = hashlib.sha256(
        json.dumps(
            identity_payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()

    prior: dict[str, Any] | None = None
    if resume:
        if path.is_file():
            try:
                candidate = load_run_manifest(path)
                if candidate.get("run", {}).get("slug") == getattr(
                    spec, "slug", ""
                ):
                    prior = candidate
            except (OSError, json.JSONDecodeError):
                prior = None
        if prior is None:
            raise ResumeContractMismatch(
                "Cannot resume safely: the prior run manifest is missing, "
                "invalid, or names a different run. Existing artifacts were "
                "left untouched."
            )
        if (
            prior.get("run", {}).get("resume_identity_sha256")
            != resume_identity_sha256
        ):
            raise ResumeContractMismatch(
                "Cannot resume safely because the run prompt, source files, "
                "roster, agent instructions, model routing, pipeline contract, "
                "or local code, prompts, or design rules changed since these "
                "artifacts were produced. Existing artifacts were left untouched; "
                "start a new run so stale paid work is not silently reused."
            )

    artifacts = _expected_artifacts(spec)
    if prior:
        previous_by_path = {
            item.get("path"): item for item in prior.get("artifacts", [])
        }
        for item in artifacts:
            old = previous_by_path.get(item["path"])
            if old and old.get("status") in {"complete", "invalid"}:
                preserved = {
                    key: deepcopy(old[key])
                    for key in (
                        "status",
                        "validation",
                        "sha256",
                        "size_bytes",
                        "word_count",
                        "record_count",
                        "completed_at",
                        "dependencies",
                    )
                    if key in old
                }
                # Repair the one known historical receipt defect only when its
                # audit trail proves exactly which identity bytes were moved.
                # Arbitrary stale digests remain stale and force a safe re-run.
                if "dependencies" in preserved:
                    _repair_audited_rebaseline_dependency_digest(
                        preserved["dependencies"],
                        prior_manifest=prior,
                        artifact_path=str(item["path"]),
                    )
                item.update(preserved)

    now = _now()
    run_payload: dict[str, Any] = {
        "slug": str(getattr(spec, "slug", "")),
        "title": str(getattr(spec, "title", "")),
        "thesis": str(getattr(spec, "thesis", "")),
        "run_prompt": _relative(run_file, repo_root),
        "run_prompt_sha256": run_prompt_sha256,
        "run_prompt_size": run_prompt_size,
        "resume_identity_sha256": resume_identity_sha256,
        "output_format": str(getattr(spec, "output_format", "report")),
        "want_pptx": bool(getattr(spec, "want_pptx", False)),
        "deck_mode": str(getattr(spec, "deck_mode", "board") or "board"),
        "decision_required": str(
            getattr(spec, "decision_required", "") or ""
        ),
        "decision_owner": str(getattr(spec, "decision_owner", "") or ""),
        "time_horizon": str(getattr(spec, "time_horizon", "") or ""),
        "approval_path": str(getattr(spec, "approval_path", "") or ""),
        "success_measure": str(getattr(spec, "success_measure", "") or ""),
        "operator_context": str(getattr(spec, "operator_context", "") or ""),
        "source_paths": list(getattr(spec, "source_paths", []) or []),
        "source_material": source_material,
        "source_library": source_library,
        "execution_contract": execution_contract,
        "resume": resume,
    }
    if prior and isinstance(prior.get("run"), dict):
        for key, value in prior["run"].items():
            if key not in run_payload:
                run_payload[key] = deepcopy(value)

    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "created_at": prior.get("created_at", now) if prior else now,
        "updated_at": now,
        "run": run_payload,
        "selected_research_agents": selected_agents,
        "process_agents": process_agents,
        "pipeline": {
            "schema_version": SCHEMA_VERSION,
            "definition_version": "council-v2",
            "steps": [
                {
                    "id": str(getattr(step, "id", "")),
                    "phase": str(getattr(step, "phase", "")),
                    "agent": str(getattr(step, "agent", "")),
                    "model_role": str(getattr(step, "model_role", "")),
                    "model_id": model_assignments.get(
                        str(getattr(step, "model_role", ""))
                    ),
                    "inputs": list(getattr(step, "inputs", ())),
                    "output": str(getattr(step, "output", "")),
                    "quality_gate": str(
                        getattr(step, "quality_gate", "typed_artifact")
                    ),
                }
                for step in pipeline_steps
            ],
        },
        "contracts": {
            "manifest": MANIFEST_NAME,
            "airport_context": "context/airport-context.md",
            "context_sources": "context/context-sources.jsonl",
            "evidence_ledger": "evidence-ledger.jsonl",
            "evidence_ledger_compatibility": "stage1/evidence-ledger.jsonl",
            "evidence_map": "stage1/evidence-map.md",
            "evidence_curation": "stage1/evidence-map.md",
            "creative_framing": "stage2/narrative-options.md",
            "quality_reviews": [
                "stage2/red-team-critique-v1.md",
                "stage2/red-team-critique-v2.md",
            ],
            "claim_lineage": "claim-lineage.jsonl",
            "quality_gate": "quality-gate.json",
            "visual_brief": "stage4/visual-brief.json",
        },
        "artifacts": artifacts,
        "stages": prior.get("stages", {}) if prior else {},
    }
    if prior:
        # Resume refreshes the fields it owns but must not erase audit trails
        # or extension state it does not understand.  This specifically keeps
        # resume_rebaselines and persisted human-checkpoint approvals intact.
        for key, value in prior.items():
            if key not in payload:
                payload[key] = deepcopy(value)
    _atomic_write_json(path, payload)
    return path


def update_artifact(
    manifest_path: Path,
    artifact_path: Path,
    validation: ArtifactValidation,
    *,
    artifact_id: str | None = None,
    producer: str | None = None,
    role: str | None = None,
    required: bool | None = None,
    dependencies: dict[str, Any] | None = None,
) -> None:
    """Record validation and completion metadata for one artifact."""

    if not manifest_path.is_file():
        return
    payload = load_run_manifest(manifest_path)
    outputs_dir = manifest_path.parent
    relative_path = _relative(artifact_path, outputs_dir)
    artifacts = payload.setdefault("artifacts", [])
    item = next(
        (
            entry
            for entry in artifacts
            if entry.get("path") == relative_path
            or (artifact_id and entry.get("id") == artifact_id)
        ),
        None,
    )
    if item is None:
        item = {
            "id": artifact_id or relative_path.replace("/", ":"),
            "path": relative_path,
            "stage": "unknown",
            "producer": producer or "orchestrator",
            "role": role or "artifact",
            "required": True if required is None else required,
            "contract": _contract_dict(contract_for_path(artifact_path)),
        }
        artifacts.append(item)
    if producer:
        item["producer"] = producer
    if role:
        item["role"] = role
    if required is not None:
        item["required"] = required
    item["status"] = "complete" if validation.valid else "invalid"
    item["validation"] = validation.to_dict()
    item["size_bytes"] = validation.size_bytes
    item["word_count"] = validation.word_count
    item["record_count"] = validation.record_count
    item["sha256"] = validation.sha256
    if dependencies is not None:
        item["dependencies"] = dependencies
    item["completed_at"] = _now()
    payload["updated_at"] = _now()
    _atomic_write_json(manifest_path, payload)


def update_stage(
    manifest_path: Path, stage: str, status: str, **metrics: Any
) -> None:
    """Update a coarse lifecycle stage without rewriting orchestration code."""

    if not manifest_path.is_file():
        return
    payload = load_run_manifest(manifest_path)
    stage_data = payload.setdefault("stages", {}).setdefault(stage, {})
    stage_data["status"] = status
    stage_data["updated_at"] = _now()
    stage_data.update(metrics)
    payload["updated_at"] = _now()
    _atomic_write_json(manifest_path, payload)


def checkpoint_approval_matches(
    manifest_path: Path,
    checkpoint_id: str,
    declared_inputs: Iterable[str],
) -> bool:
    """Return whether an approval still covers the exact checkpoint inputs."""

    try:
        payload = load_run_manifest(manifest_path)
    except (OSError, TypeError, json.JSONDecodeError):
        return False
    record = payload.get("checkpoints", {}).get(checkpoint_id)
    if not isinstance(record, dict) or record.get("approved") is not True:
        return False
    expected = tuple(dict.fromkeys(str(item) for item in declared_inputs))
    dependencies = record.get("dependencies")
    recorded_inputs = tuple(
        str(item.get("declared_input") or "")
        for item in (
            dependencies.get("inputs", [])
            if isinstance(dependencies, dict)
            else []
        )
        if isinstance(item, dict)
    )
    return bool(
        recorded_inputs == expected
        and dependency_fingerprint_matches(manifest_path, dependencies)
    )


def record_checkpoint_decision(
    manifest_path: Path,
    checkpoint_id: str,
    *,
    approved: bool,
    action: str,
    declared_inputs: Iterable[str],
    auto_approved: bool = False,
    reviewed_fingerprint: object | None = None,
) -> None:
    """Persist a human decision against the bytes the operator reviewed."""

    if not manifest_path.is_file():
        return
    expected = tuple(dict.fromkeys(str(item) for item in declared_inputs))
    if reviewed_fingerprint is None:
        # Compatibility path for callers that have not yet captured the review
        # snapshot. New checkpoint flows should always supply it.
        dependencies = build_dependency_fingerprint(manifest_path, expected)
    else:
        dependencies = deepcopy(reviewed_fingerprint)
        if not isinstance(dependencies, dict):
            raise CheckpointInputsChanged(
                f"Cannot persist {checkpoint_id}: the reviewed snapshot is "
                "missing or malformed."
            )
        inputs = dependencies.get("inputs")
        recorded_inputs = tuple(
            str(item.get("declared_input") or "")
            for item in (inputs if isinstance(inputs, list) else [])
            if isinstance(item, dict)
        )
        if recorded_inputs != expected:
            raise CheckpointInputsChanged(
                f"Cannot persist {checkpoint_id}: the reviewed snapshot does "
                "not cover the declared checkpoint inputs."
            )
    if dependencies.get("complete") is not True:
        raise CheckpointInputsChanged(
            f"Cannot persist {checkpoint_id}: one or more reviewed artifacts "
            "are missing or unsafe."
        )
    if reviewed_fingerprint is not None and not dependency_fingerprint_matches(
        manifest_path, dependencies
    ):
        raise CheckpointInputsChanged(
            f"Cannot persist {checkpoint_id}: reviewed artifacts changed "
            "while the checkpoint was awaiting a decision. Review them again."
        )
    payload = load_run_manifest(manifest_path)
    payload.setdefault("checkpoints", {})[checkpoint_id] = {
        "approved": bool(approved),
        "action": str(action),
        "auto_approved": bool(auto_approved),
        "decided_at": _now(),
        "dependencies": dependencies,
    }
    payload["updated_at"] = _now()
    # Recheck immediately before the atomic manifest write. This catches a
    # concurrent writer that moved an input while the decision record itself
    # was being assembled.
    if reviewed_fingerprint is not None and not dependency_fingerprint_matches(
        manifest_path, dependencies
    ):
        raise CheckpointInputsChanged(
            f"Cannot persist {checkpoint_id}: reviewed artifacts changed "
            "while the checkpoint was awaiting a decision. Review them again."
        )
    _atomic_write_json(manifest_path, payload)


def assert_manifest_complete(manifest_path: Path) -> dict[str, Any]:
    """Refuse release unless every required artifact still matches its record.

    This is the final deterministic commit check. It protects against a file
    being edited, replaced, or deleted after its stage-level validation but
    before distribution and archiving.
    """

    payload = load_run_manifest(manifest_path)
    outputs_dir = manifest_path.parent.resolve()
    repo_root = outputs_dir.parent
    failures: list[str] = []

    def verify_input(
        label: str,
        path: Path,
        expected_hash: str | None,
        expected_size: int | None,
    ) -> None:
        actual_hash, actual_size = _file_fingerprint(path)
        if (
            not expected_hash
            or actual_hash != expected_hash
            or (
                expected_size is not None
                and actual_size != int(expected_size)
            )
        ):
            failures.append(
                f"{label}: current bytes do not match the executable input"
            )

    run_data = payload.get("run", {})
    run_prompt_raw = str(run_data.get("run_prompt") or "")
    if run_prompt_raw:
        run_prompt_path = Path(run_prompt_raw)
        if not run_prompt_path.is_absolute():
            run_prompt_path = repo_root / run_prompt_path
        verify_input(
            "run prompt",
            run_prompt_path,
            run_data.get("run_prompt_sha256"),
            run_data.get("run_prompt_size"),
        )
    elif run_data:
        failures.append("run prompt: path is missing from the manifest")

    # Current Council manifests own an explicit lifecycle. Artifacts alone are
    # not enough: an interrupted production step must never be promoted merely
    # because its files happen to look complete on disk. Minimal legacy/test
    # manifests that predate the ``stages`` field retain their old behavior.
    if "stages" in payload:
        stages = payload.get("stages")
        if not isinstance(stages, dict):
            failures.append("stages: lifecycle record is missing or malformed")
        else:
            for stage in (
                "context",
                "research",
                "evidence",
                "synthesis",
                "polish",
                "verification",
                "production",
                "release",
            ):
                record = stages.get(stage)
                status = record.get("status") if isinstance(record, dict) else None
                if status != "complete":
                    failures.append(
                        f"stage {stage}: lifecycle status is {status or 'missing'!r}"
                    )

    for index, source in enumerate(run_data.get("source_material", []), 1):
        raw_path = Path(str(source.get("runtime_path") or ""))
        if not raw_path.is_absolute():
            raw_path = repo_root / raw_path
        verify_input(
            f"source material {index}",
            raw_path,
            source.get("sha256"),
            source.get("size_bytes"),
        )

    source_root = (
        repo_root / "sources" / "runs" / str(run_data.get("slug") or "")
    )
    expected_library = {
        str(item.get("path")): (
            item.get("sha256"),
            item.get("size_bytes"),
        )
        for item in run_data.get("source_library", [])
    }
    current_library = {
        path.relative_to(source_root).as_posix(): _file_fingerprint(path)
        for path in (
            sorted(source_root.rglob("*")) if source_root.is_dir() else []
        )
        if path.is_file()
    }
    if (
        (run_data.get("source_material") or expected_library)
        and current_library != expected_library
    ):
        failures.append(
            "source library: file set or bytes changed after the run began"
        )

    recorded_execution_contract = run_data.get("execution_contract")
    if recorded_execution_contract is not None:
        try:
            current_execution_contract = build_execution_contract_fingerprint(
                repo_root
            )
        except ResumeContractMismatch as exc:
            failures.append(f"execution contract: {exc}")
        else:
            # Compare generation code only. A recorded contract may predate the
            # app-shell split and still carry transport modules, so filter both
            # sides rather than assuming the stored list is already narrow.
            if generation_contract_records(
                current_execution_contract
            ) != generation_contract_records(recorded_execution_contract):
                failures.append(
                    "execution contract: code, prompts, or design rules changed "
                    "after the run began"
                )

    for item in payload.get("artifacts", []):
        required = bool(item.get("required", True))
        artifact_id = str(item.get("id") or item.get("path") or "artifact")
        relative = Path(str(item.get("path") or ""))
        candidate = (outputs_dir / relative).resolve()
        try:
            candidate.relative_to(outputs_dir)
        except ValueError:
            failures.append(f"{artifact_id}: path escapes outputs/")
            continue
        if (
            not required
            and not candidate.exists()
            and item.get("status") in {"pending", "skipped", None}
        ):
            continue
        if item.get("status") != "complete":
            failures.append(
                f"{artifact_id}: manifest status is {item.get('status', 'missing')!r}"
            )
            continue
        raw_contract = item.get("contract") or {}
        contract = ArtifactContract(
            str(raw_contract.get("kind") or contract_for_path(candidate).kind),
            min_words=int(raw_contract.get("min_words") or 0),
            min_records=int(raw_contract.get("min_records") or 0),
            required_keys=tuple(raw_contract.get("required_keys") or ()),
            required_any=tuple(
                tuple(group)
                for group in (raw_contract.get("required_any") or ())
            ),
            requires_with=tuple(
                (str(trigger), tuple(dependents))
                for trigger, dependents in (
                    raw_contract.get("requires_with") or ()
                )
            ),
            optional=bool(raw_contract.get("optional", False)),
        )
        validation = validate_artifact(candidate, contract)
        if not validation.valid:
            failures.append(
                f"{artifact_id}: {'; '.join(validation.errors) or 'invalid'}"
            )
            continue
        expected_hash = item.get("sha256")
        if not expected_hash or validation.sha256 != expected_hash:
            failures.append(
                f"{artifact_id}: current bytes do not match the validated SHA-256"
            )
            continue
        dependencies = item.get("dependencies")
        if dependencies is not None and not dependency_fingerprint_matches(
            manifest_path, dependencies
        ):
            failures.append(
                f"{artifact_id}: declared upstream inputs changed or are missing"
            )
            continue
        if item.get("role") in {
            "word_visual_inspection",
            "executive_summary_visual_inspection",
            "release_word_visual_inspection",
            "release_executive_summary_visual_inspection",
        }:
            from cli.publishing_quality import (
                qa_word_visual_inspection_receipt,
            )

            word_name = candidate.name.removesuffix(
                "-word-visual-inspection.json"
            )
            word_artifact = candidate.with_name(f"{word_name}.docx")
            inspection_report = qa_word_visual_inspection_receipt(
                candidate,
                artifact=word_artifact,
            )
            if not inspection_report.ok:
                failures.append(
                    f"{artifact_id}: "
                    + "; ".join(
                        f"{issue.code}: {issue.message}"
                        for issue in inspection_report.errors[:8]
                    )
                )
                continue
        if candidate.suffix.lower() == ".json" and (
            str(item.get("role", "")).endswith("_qa")
            or item.get("role") in {"publishing_quality", "presentation_qa"}
        ):
            try:
                quality = json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                failures.append(f"{artifact_id}: unreadable QA payload ({exc})")
                continue
            if quality.get("ok") is not True:
                failures.append(f"{artifact_id}: QA payload is not releaseable")
    if failures:
        raise RuntimeError(
            "Run manifest is not releaseable:\n- " + "\n- ".join(failures)
        )
    return payload


def manifest_prompt_block(manifest_path: Path, *, repo_root: Path) -> str:
    """Return the authoritative, step-scoped handoff injected into prompts."""

    manifest_rel = _relative(manifest_path, repo_root)
    return (
        "\n\n## Authoritative run contract\n\n"
        f"Read `{manifest_rel}` as the authoritative roster and artifact map for "
        "this run; any static roster or filename list in older instructions is "
        "obsolete. Use it to resolve the inputs named in this step's prompt. When "
        "the step calls for every selected brief, include every brief listed in the "
        "manifest and do not silently omit supplemental agents. Keep this handoff "
        "step-scoped: do not reread unrelated upstream artifacts unless a targeted "
        "verification requires one."
    )
