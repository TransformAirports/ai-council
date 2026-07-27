"""Focused Council workflow for strengthening an existing argument.

Unlike a normal Council run, this mode does not produce a Word report. It takes
an existing argument (pasted text, uploaded source material, or both), runs a
selected research swarm, reconciles the evidence, and releases a concise,
fact-checked Markdown argument. An optional presentation is built to an exact
operator-supplied slide count.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from slugify import slugify

from cli.agents import load_all_agents, research_agents
from cli.artifacts import ArtifactContract, contract_for_path, validate_artifact
from cli.evidence import (
    bind_claim_lineage_to_draft,
    build_evidence_ledger,
    ensure_claim_lineage,
    normalise_evidence_ledger,
)
from cli.events import emit
from cli.orchestrator import (
    CLAIM_LINEAGE_AGENT_CONTRACT,
    CLAIM_LINEAGE_CONTRACT,
    CostTally,
    RESEARCH_EVIDENCE_CONTRACT,
    _model,
    _notify_done,
    _required_outputs_complete,
    _required_outputs_match_manifest,
    _run_agent,
    _validate_visual_brief,
    _visual_brief_contract,
    _visual_inspection_contract,
)
from cli.publishing_quality import assert_quality


REPO_ROOT = Path(__file__).resolve().parent.parent
ARGUMENT_SLIDE_MIN = 3
ARGUMENT_SLIDE_MAX = 30
ARGUMENT_TEXT_MAX_CHARS = 200_000
ARGUMENT_RELEASE_SCHEMA_VERSION = "1.0"
ARGUMENT_PIPELINE_SCHEMA_VERSION = "strengthen-v5"
SAFE_SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


@dataclass
class StrengthenRequest:
    title: str
    argument_text: str = ""
    research_goal: str = ""
    audience: str = "Airport executives and sophisticated aviation readers"
    selected_agents: list[str] = field(default_factory=list)
    want_pptx: bool = False
    slide_count: int | None = None
    source_tokens: list[str] = field(default_factory=list)
    slug: str = ""

    @classmethod
    def from_payload(
        cls,
        payload: object,
        *,
        allowed_agents: Iterable[str],
    ) -> "StrengthenRequest":
        """Validate the browser contract before any paid work starts."""

        if not isinstance(payload, dict):
            raise ValueError("Argument request must be an object.")
        title = str(payload.get("title") or "").strip()
        if not title:
            raise ValueError("Give the argument a title.")
        if len(title) > 160:
            raise ValueError("Argument title must be 160 characters or fewer.")

        argument_text = str(payload.get("argument_text") or "").strip()
        if len(argument_text) > ARGUMENT_TEXT_MAX_CHARS:
            raise ValueError(
                f"Pasted argument is longer than {ARGUMENT_TEXT_MAX_CHARS:,} characters."
            )
        research_goal = str(payload.get("research_goal") or "").strip()
        if len(research_goal) > 4_000:
            raise ValueError("Research direction must be 4,000 characters or fewer.")
        audience = str(payload.get("audience") or "").strip()
        if len(audience) > 1_000:
            raise ValueError("Audience must be 1,000 characters or fewer.")
        if not audience:
            audience = "Airport executives and sophisticated aviation readers"

        raw_tokens = payload.get("source_tokens") or []
        if not isinstance(raw_tokens, list) or any(
            not isinstance(item, str) for item in raw_tokens
        ):
            raise ValueError("Uploaded source tokens must be a list of filenames.")
        source_tokens = list(dict.fromkeys(item.strip() for item in raw_tokens if item.strip()))
        if not argument_text and not source_tokens:
            raise ValueError("Paste an argument, attach at least one document, or do both.")

        raw_agents = payload.get("agents") or []
        if not isinstance(raw_agents, list) or any(
            not isinstance(item, str) for item in raw_agents
        ):
            raise ValueError("Selected agents must be a list.")
        selected_agents = list(dict.fromkeys(item.strip() for item in raw_agents if item.strip()))
        if not selected_agents:
            raise ValueError("Seat at least one research agent.")
        allowed = set(allowed_agents)
        unknown = [name for name in selected_agents if name not in allowed]
        if unknown:
            raise ValueError("Unknown or non-research agents: " + ", ".join(unknown))

        raw_want_pptx = payload.get("want_pptx", False)
        if not isinstance(raw_want_pptx, bool):
            raise ValueError("PowerPoint selection must be true or false.")
        want_pptx = raw_want_pptx
        slide_count: int | None = None
        if want_pptx:
            raw_count = payload.get("slide_count")
            if isinstance(raw_count, bool):
                raise ValueError("Slide count must be a whole number.")
            if isinstance(raw_count, float) and not raw_count.is_integer():
                raise ValueError("Slide count must be a whole number.")
            if isinstance(raw_count, str) and not re.fullmatch(r"[0-9]+", raw_count.strip()):
                raise ValueError("Slide count must be a whole number.")
            try:
                slide_count = int(raw_count)
            except (TypeError, ValueError) as exc:
                raise ValueError("Enter the exact number of slides to build.") from exc
            if not ARGUMENT_SLIDE_MIN <= slide_count <= ARGUMENT_SLIDE_MAX:
                raise ValueError(
                    f"Slide count must be between {ARGUMENT_SLIDE_MIN} and "
                    f"{ARGUMENT_SLIDE_MAX}."
                )

        slug = str(payload.get("slug") or "").strip()
        if slug and not SAFE_SLUG.fullmatch(slug):
            raise ValueError(f"Unsafe argument slug: {slug!r}")
        return cls(
            title=title,
            argument_text=argument_text,
            research_goal=research_goal,
            audience=audience,
            selected_agents=selected_agents,
            want_pptx=want_pptx,
            slide_count=slide_count,
            source_tokens=source_tokens,
            slug=slug,
        )


@dataclass
class StrengthenResult:
    tally: CostTally
    slug: str = ""
    public_slug: str = ""
    archive_path: Path | None = None
    argument_path: Path | None = None
    deck_path: Path | None = None
    completed: bool = False


def _unique_slug(title: str, repo_root: Path) -> str:
    base = slugify(title) or "strengthened-argument"
    slug = base
    number = 2
    while (
        (repo_root / "reports" / f"argument-{slug}-release.json").exists()
        or (repo_root / "sources" / "runs" / slug).exists()
    ):
        slug = f"{base}-{number}"
        number += 1
    return slug


def _readable_source_library(repo_root: Path, slug: str) -> list[Path]:
    root = repo_root / "sources" / "runs" / slug
    if root.is_symlink():
        raise RuntimeError(f"Argument source library may not be a symlink: {root}")
    if not root.is_dir():
        return []
    files = [path for path in sorted(root.rglob("*")) if path.is_file()]
    if any(path.is_symlink() for path in files):
        raise RuntimeError("Argument source library may not contain symlinks.")
    extracted_originals = {
        path.with_name(path.name[: -len(".extracted.md")])
        for path in files
        if path.name.endswith(".extracted.md")
    }
    readable: list[Path] = []
    for path in files:
        if path in extracted_originals:
            continue
        if path.name.endswith(".extracted.md") or path.suffix.lower() in {
            ".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".pdf",
        }:
            readable.append(path)
    return readable


def _request_markdown(request: StrengthenRequest, source_paths: list[str]) -> str:
    material = request.argument_text or (
        "The source documents contain the argument to strengthen; no separate text "
        "was pasted."
    )
    sources = "\n".join(f"- `{path}`" for path in source_paths) or "- None"
    goal = request.research_goal or (
        "Find the strongest evidence, counterevidence, mechanism, and examples that "
        "make this argument more defensible without turning it into a long-form report."
    )
    return (
        f"# Strengthen an argument: {request.title}\n\n"
        f"## Audience\n\n{request.audience}\n\n"
        f"## What the research should strengthen\n\n{goal}\n\n"
        f"## Current argument\n\n{material}\n\n"
        f"## Supplemental material\n\n{sources}\n\n"
        "## Output contract\n\n"
        "Return one concise, standalone argument—not a report, methodology, research "
        "summary, or memo. Preserve the author's point of view while improving the "
        "logic, evidence, specificity, and treatment of the strongest counter-case.\n"
    )


def load_strengthen_request(path: Path, allowed_agents: Iterable[str]) -> StrengthenRequest:
    payload = json.loads(path.read_text(encoding="utf-8"))
    # Persisted requests use the dataclass field name; browser payloads use agents.
    if "selected_agents" in payload and "agents" not in payload:
        payload["agents"] = payload["selected_agents"]
    return StrengthenRequest.from_payload(payload, allowed_agents=allowed_agents)


def _write_active_marker(
    outputs_dir: Path, request: StrengthenRequest, *, preserve_started: bool = False
) -> None:
    path = outputs_dir / ".active-run.json"
    started = _now()
    if preserve_started and path.is_file():
        try:
            started = str(json.loads(path.read_text()).get("started") or started)
        except (OSError, json.JSONDecodeError):
            pass
    _atomic_json(
        path,
        {
            "slug": request.slug,
            "title": request.title,
            "started": started,
            "format": "strengthened argument",
            "mode": "strengthen",
            "want_pptx": request.want_pptx,
            "slide_count": request.slide_count,
            "request": "context/argument-request.json",
            "pipeline_version": "strengthen-v1",
        },
    )


def _archive_inventory(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"Argument archive may not contain symlinks: {path}")
        if path.is_file():
            records.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "sha256": _sha256(path),
                    "size_bytes": path.stat().st_size,
                }
            )
    return records


def _rebind_argument_dependency_identity(
    manifest: dict[str, Any], identity_sha256: str
) -> bool:
    """Rebind only the stable run-identity token in existing step receipts."""

    changed = False
    for artifact in manifest.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        dependencies = artifact.get("dependencies")
        if not isinstance(dependencies, dict):
            continue
        rebound = False
        for declared in dependencies.get("inputs", []):
            if (
                not isinstance(declared, dict)
                or declared.get("declared_input") != "run-manifest.json"
            ):
                continue
            files = declared.get("files")
            if not isinstance(files, list) or len(files) != 1:
                continue
            record = files[0]
            if (
                isinstance(record, dict)
                and record.get("kind") == "run_identity"
                and record.get("sha256") != identity_sha256
            ):
                record["sha256"] = identity_sha256
                rebound = True
        if rebound:
            dependencies.pop("sha256", None)
            dependencies["sha256"] = hashlib.sha256(
                json.dumps(
                    dependencies,
                    sort_keys=True,
                    separators=(",", ":"),
                    ensure_ascii=False,
                ).encode("utf-8")
            ).hexdigest()
            changed = True
    return changed


def _rebind_argument_curator_dependencies(manifest_path: Path) -> bool:
    """Move legacy Curator receipts off the ledger they own and rewrite."""

    from cli.run_manifest import build_dependency_fingerprint, update_artifact

    outputs_dir = manifest_path.parent
    evidence_map = outputs_dir / "stage1" / "evidence-map.md"
    ledger_path = outputs_dir / "evidence-ledger.jsonl"
    outputs = (
        (evidence_map, contract_for_path(evidence_map)),
        (ledger_path, ArtifactContract("jsonl", min_records=0)),
    )
    if not _required_outputs_complete(outputs):
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
    for path, contract in outputs:
        validation = validate_artifact(path, contract)
        relative = path.relative_to(outputs_dir).as_posix()
        record = by_path.get(relative)
        if (
            not record
            or record.get("status") != "complete"
            or not validation.sha256
            or record.get("sha256") != validation.sha256
        ):
            return False
    dependencies = build_dependency_fingerprint(
        manifest_path,
        (
            "run-manifest.json",
            "context/argument-request.md",
            "stage1/*-brief.md",
            "stage1/*-evidence.jsonl",
        ),
    )
    if dependencies.get("complete") is not True:
        return False
    update_artifact(
        manifest_path,
        evidence_map,
        validate_artifact(evidence_map, contract_for_path(evidence_map)),
        artifact_id="argument/evidence-map",
        producer="evidence-curator",
        dependencies=dependencies,
    )
    update_artifact(
        manifest_path,
        ledger_path,
        validate_artifact(ledger_path, ArtifactContract("jsonl", min_records=0)),
        artifact_id="argument/evidence-ledger",
        producer="evidence-curator",
        dependencies=dependencies,
    )
    return True


def _rebind_argument_downstream_dependencies(manifest_path: Path) -> bool:
    """Bind legacy downstream receipts to the normalized Curator artifacts."""

    from cli.run_manifest import build_dependency_fingerprint, update_artifact

    outputs_dir = manifest_path.parent
    evidence_map = outputs_dir / "stage1" / "evidence-map.md"
    ledger_path = outputs_dir / "evidence-ledger.jsonl"
    strategist_draft = outputs_dir / "stage2" / "strategist-draft.md"
    final_draft = outputs_dir / "stage3" / "final-draft.md"
    fact_report = outputs_dir / "stage3" / "fact-check-report.md"
    lineage_path = outputs_dir / "claim-lineage.jsonl"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    by_path = {
        str(item.get("path")): item
        for item in manifest.get("artifacts", [])
        if isinstance(item, dict)
    }

    strategist_validation = validate_artifact(
        strategist_draft,
        ArtifactContract("markdown", min_words=250),
    )
    strategist_record = by_path.get("stage2/strategist-draft.md")
    if (
        not strategist_record
        or strategist_record.get("status") != "complete"
        or not strategist_validation.valid
        or strategist_record.get("sha256") != strategist_validation.sha256
    ):
        return False
    strategist_dependencies = build_dependency_fingerprint(
        manifest_path,
        (
            "run-manifest.json",
            "context/argument-request.md",
            "stage1/*-brief.md",
            "stage1/evidence-map.md",
            "evidence-ledger.jsonl",
        ),
    )
    if strategist_dependencies.get("complete") is not True:
        return False
    update_artifact(
        manifest_path,
        strategist_draft,
        strategist_validation,
        artifact_id="argument/strategist-draft",
        producer="strategist",
        dependencies=strategist_dependencies,
    )

    fact_outputs = (
        (final_draft, ArtifactContract("markdown", min_words=250)),
        (fact_report, contract_for_path(fact_report)),
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    by_path = {
        str(item.get("path")): item
        for item in manifest.get("artifacts", [])
        if isinstance(item, dict)
    }
    for path, contract in fact_outputs:
        validation = validate_artifact(path, contract)
        record = by_path.get(path.relative_to(outputs_dir).as_posix())
        if (
            not record
            or record.get("status") != "complete"
            or not validation.valid
            or record.get("sha256") != validation.sha256
        ):
            return False
    bind_claim_lineage_to_draft(
        final_draft=final_draft,
        output_path=lineage_path,
    )
    lineage_validation = validate_artifact(lineage_path, CLAIM_LINEAGE_CONTRACT)
    if not lineage_validation.valid:
        return False
    fact_dependencies = build_dependency_fingerprint(
        manifest_path,
        (
            "run-manifest.json",
            "context/argument-request.md",
            "stage1/evidence-map.md",
            "evidence-ledger.jsonl",
            "stage2/strategist-draft.md",
        ),
    )
    if fact_dependencies.get("complete") is not True:
        return False
    update_artifact(
        manifest_path,
        final_draft,
        validate_artifact(final_draft, ArtifactContract("markdown", min_words=250)),
        artifact_id="argument/final-draft",
        producer="fact-checker",
        dependencies=fact_dependencies,
    )
    update_artifact(
        manifest_path,
        fact_report,
        validate_artifact(fact_report, contract_for_path(fact_report)),
        producer="fact-checker",
        dependencies=fact_dependencies,
    )
    update_artifact(
        manifest_path,
        lineage_path,
        lineage_validation,
        producer="fact-checker",
        dependencies=fact_dependencies,
    )
    return True


def _prepare_argument_manifest(
    *,
    request: StrengthenRequest,
    repo_root: Path,
    outputs_dir: Path,
    readable_sources: list[Path],
    agents: dict[str, Any],
    process_names: list[str],
    resume: bool,
) -> Path:
    """Bind resumable paid work to the complete argument execution contract."""

    from cli.run_manifest import (
        ResumeContractMismatch,
        build_execution_contract_fingerprint,
    )

    role_models = {
        **{
            name: agents[name].model_override or _model("research")
            for name in request.selected_agents
        },
        "evidence-curator": _model("curation"),
        "strategist": _model("synthesis"),
        "fact-checker": _model("factcheck"),
    }
    if request.want_pptx:
        role_models.update(
            {
                "art-director": _model("art_direction"),
                "presentation-designer": _model("presentation"),
            }
        )

    agent_contracts: list[dict[str, Any]] = []
    for name in [*request.selected_agents, *process_names]:
        agent = agents[name]
        prompt_path = getattr(agent, "path", None)
        prompt_sha256: str | None = None
        prompt_name: str | None = None
        if isinstance(prompt_path, Path) and prompt_path.is_file():
            if prompt_path.is_symlink():
                raise ResumeContractMismatch(
                    f"Argument agent definition may not be a symlink: {prompt_path}"
                )
            prompt_sha256 = _sha256(prompt_path)
            try:
                prompt_name = prompt_path.relative_to(repo_root).as_posix()
            except ValueError:
                prompt_name = prompt_path.resolve().as_posix()
        agent_contracts.append(
            {
                "name": name,
                "provider": agent.provider,
                "model": role_models[name],
                "prompt_path": prompt_name,
                "prompt_sha256": prompt_sha256,
            }
        )

    sources: list[dict[str, Any]] = []
    source_root = repo_root / "sources" / "runs" / request.slug
    for path in sorted(source_root.rglob("*")):
        if path.is_symlink():
            raise ResumeContractMismatch(
                f"Argument source library may not contain symlinks: {path}"
            )
        if path.is_file():
            sources.append(
                {
                    "path": path.relative_to(source_root).as_posix(),
                    "sha256": _sha256(path),
                    "size_bytes": path.stat().st_size,
                    "readable": path in readable_sources,
                }
            )

    identity = {
        "schema_version": ARGUMENT_PIPELINE_SCHEMA_VERSION,
        "request": asdict(request),
        "sources": sources,
        "agents": agent_contracts,
        "execution_contract": build_execution_contract_fingerprint(repo_root),
    }
    identity_sha256 = hashlib.sha256(
        json.dumps(
            identity,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()
    manifest_path = outputs_dir / "run-manifest.json"
    if resume:
        try:
            prior = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ResumeContractMismatch(
                "Cannot resume the argument safely because its run manifest is missing "
                "or invalid. Existing work was left untouched."
            ) from exc
        prior_identity = prior.get("argument_identity")
        prior_hash = prior.get("run", {}).get("resume_identity_sha256")
        if (
            prior.get("mode") != "strengthen"
            or prior.get("run", {}).get("slug") != request.slug
        ):
            raise ResumeContractMismatch(
                "Cannot resume the argument safely because its request, source bytes, "
                "agent instructions, model routing, or local execution contract changed. "
                "Existing work was left untouched; start a new argument run."
            )
        if prior_hash != identity_sha256:
            migration_allowed = False
            changed_execution: set[str] = set()
            prior_schema = (
                str(prior_identity.get("schema_version") or "")
                if isinstance(prior_identity, dict)
                else ""
            )
            if isinstance(prior_identity, dict):
                prior_semantic = {
                    key: value
                    for key, value in prior_identity.items()
                    if key not in {"schema_version", "execution_contract"}
                }
                current_semantic = {
                    key: value
                    for key, value in identity.items()
                    if key not in {"schema_version", "execution_contract"}
                }
                prior_execution = {
                    str(item.get("path")): item
                    for item in prior_identity.get("execution_contract", [])
                    if isinstance(item, dict) and item.get("path")
                }
                current_execution = {
                    str(item.get("path")): item
                    for item in identity.get("execution_contract", [])
                    if isinstance(item, dict) and item.get("path")
                }
                changed_execution = {
                    path
                    for path in set(prior_execution) | set(current_execution)
                    if prior_execution.get(path) != current_execution.get(path)
                }
                is_lineage_migration_followup = bool(
                    prior_schema == ARGUMENT_PIPELINE_SCHEMA_VERSION
                    and not prior.get("dependency_identity_rebound")
                    and any(
                        isinstance(item, dict)
                        and item.get("reason")
                        == "lineage-remediation compatibility fix"
                        for item in prior.get("resume_migrations", [])
                    )
                )
                is_verifier_v4_migration = bool(
                    prior_schema == "strengthen-v2"
                    and changed_execution
                    and changed_execution
                    <= {
                        "cli/claim_text.py",
                        "cli/evidence.py",
                        "cli/quality_gate.py",
                        "cli/strengthen.py",
                    }
                )
                is_curator_v4_migration = bool(
                    prior_schema == "strengthen-v3"
                    and changed_execution
                    and changed_execution <= {"cli/strengthen.py"}
                )
                is_downstream_v5_migration = bool(
                    prior_schema == "strengthen-v4"
                    and changed_execution
                    and changed_execution <= {"cli/strengthen.py"}
                )
                migration_allowed = bool(
                    prior_semantic == current_semantic
                    and changed_execution
                    and (
                        (
                            prior_schema == "strengthen-v1"
                            and changed_execution <= {"cli/strengthen.py"}
                        )
                        or is_lineage_migration_followup
                        or is_verifier_v4_migration
                        or is_curator_v4_migration
                        or is_downstream_v5_migration
                    )
                )
            if not migration_allowed:
                raise ResumeContractMismatch(
                    "Cannot resume the argument safely because its request, source bytes, "
                    "agent instructions, model routing, or local execution contract changed. "
                    "Existing work was left untouched; start a new argument run."
                )
            prior["argument_identity"] = identity
            prior["run"]["resume_identity_sha256"] = identity_sha256
            _rebind_argument_dependency_identity(prior, identity_sha256)
            prior["dependency_identity_rebound"] = True
            prior.setdefault("resume_migrations", []).append(
                {
                    "at": _now(),
                    "from": prior_schema,
                    "to": ARGUMENT_PIPELINE_SCHEMA_VERSION,
                    "reason": (
                        "claim-verifier receipt migration"
                        if prior_schema == "strengthen-v2"
                        else "curator receipt migration"
                        if prior_schema in {"strengthen-v3", "strengthen-v4"}
                        else "lineage-remediation receipt migration"
                    ),
                    "changed_execution_files": sorted(changed_execution),
                }
            )
            _atomic_json(manifest_path, prior)
            if prior_schema in {"strengthen-v2", "strengthen-v3", "strengthen-v4"}:
                curator_rebound = _rebind_argument_curator_dependencies(manifest_path)
                downstream_rebound = (
                    _rebind_argument_downstream_dependencies(manifest_path)
                    if curator_rebound
                    else False
                )
                prior = json.loads(manifest_path.read_text(encoding="utf-8"))
                prior["curator_dependency_rebound"] = bool(curator_rebound)
                prior["downstream_dependency_rebound"] = bool(downstream_rebound)
                _atomic_json(manifest_path, prior)
        elif _rebind_argument_dependency_identity(prior, identity_sha256):
            prior["dependency_identity_rebound"] = True
            _atomic_json(manifest_path, prior)
        return manifest_path

    _atomic_json(
        manifest_path,
        {
            "schema_version": "2.0",
            "mode": "strengthen",
            "created_at": _now(),
            "run": {
                "slug": request.slug,
                "title": request.title,
                "resume_identity_sha256": identity_sha256,
            },
            "argument_identity": identity,
            "artifacts": [],
        },
    )
    return manifest_path


def _archive_strengthen_run(
    *, repo_root: Path, request: StrengthenRequest, tally: CostTally
) -> Path:
    outputs_dir = repo_root / "outputs"
    runs_dir = repo_root / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{date.today().isoformat()}-argument-{request.slug}"
    archive_dir = runs_dir / stem
    suffix = 2
    while archive_dir.exists() or archive_dir.is_symlink():
        archive_dir = runs_dir / f"{stem}-{suffix}"
        suffix += 1
    staging_root = Path(tempfile.mkdtemp(prefix=".argument-archive-", dir=runs_dir))
    staged = staging_root / archive_dir.name
    try:
        shutil.copytree(outputs_dir, staged)
        source_dir = repo_root / "sources" / "runs" / request.slug
        if source_dir.is_dir():
            shutil.copytree(source_dir, staged / "sources")
        (staged / "retrospective.md").write_text(
            "\n".join(
                [
                    f"# Retrospective — strengthened argument: {request.title}",
                    "",
                    f"Archived: {date.today().isoformat()}",
                    f"Claude API total: **${tally.total:.2f}**",
                    "",
                    "The focused workflow produced a concise verified argument"
                    + (" and an exact-length presentation." if request.want_pptx else "."),
                    "Review the fact-check report and evidence map before external use.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        _atomic_json(
            staged / "argument-archive.json",
            {
                "schema_version": ARGUMENT_RELEASE_SCHEMA_VERSION,
                "mode": "strengthen",
                "slug": request.slug,
                "title": request.title,
                "created_at": _now(),
                "cost_by_step": tally.by_step,
                "files": _archive_inventory(staged),
            },
        )
        os.replace(staged, archive_dir)
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)
    if archive_dir.is_symlink() or not archive_dir.is_dir():
        raise RuntimeError("Strengthened-argument archive promotion failed.")
    return archive_dir


def _publish_strengthen_release(
    *,
    repo_root: Path,
    request: StrengthenRequest,
    final_argument: Path,
    deck: Path | None,
    archive_dir: Path,
) -> tuple[Path, Path | None]:
    reports_dir = repo_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    public_slug = f"argument-{request.slug}"
    argument_target = reports_dir / f"{public_slug}.md"
    deck_target = reports_dir / f"{public_slug}.pptx" if deck is not None else None
    pointer_target = reports_dir / f"{public_slug}-release.json"
    staging_root = Path(tempfile.mkdtemp(prefix=".argument-release-", dir=reports_dir))
    try:
        staged_argument = staging_root / argument_target.name
        shutil.copy2(final_argument, staged_argument)
        staged_deck: Path | None = None
        if deck is not None and deck_target is not None:
            staged_deck = staging_root / deck_target.name
            shutil.copy2(deck, staged_deck)
        artifacts = [
            {
                "role": "argument",
                "path": argument_target.name,
                "sha256": _sha256(staged_argument),
                "size_bytes": staged_argument.stat().st_size,
            }
        ]
        if staged_deck is not None and deck_target is not None:
            artifacts.append(
                {
                    "role": "presentation",
                    "path": deck_target.name,
                    "sha256": _sha256(staged_deck),
                    "size_bytes": staged_deck.stat().st_size,
                    "slide_count": request.slide_count,
                }
            )
        staged_pointer = staging_root / pointer_target.name
        _atomic_json(
            staged_pointer,
            {
                "schema_version": ARGUMENT_RELEASE_SCHEMA_VERSION,
                "status": "current",
                "mode": "strengthen",
                "slug": public_slug,
                "source_slug": request.slug,
                "title": request.title,
                "date": date.today().isoformat(),
                "archive_path": archive_dir.relative_to(repo_root).as_posix(),
                "artifacts": artifacts,
            },
        )
        os.replace(staged_argument, argument_target)
        if staged_deck is not None and deck_target is not None:
            os.replace(staged_deck, deck_target)
        # The pointer is the commit record and is always promoted last.
        os.replace(staged_pointer, pointer_target)
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)
    return argument_target, deck_target


async def _build_argument_deck(
    *,
    request: StrengthenRequest,
    repo_root: Path,
    outputs_dir: Path,
    agents: dict[str, Any],
    tally: CostTally,
    manifest_path: Path,
) -> Path:
    assert request.slide_count is not None
    art_director = agents["art-director"]
    designer = agents["presentation-designer"]
    visual_path = outputs_dir / "stage4" / "visual-brief.json"
    visual_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path = repo_root / "assets" / "brand" / "visual-brief.schema.json"
    art_prompt = (
        "Read `outputs/context/argument-request.md`, "
        "`outputs/stage1/evidence-map.md`, `outputs/evidence-ledger.jsonl`, "
        "`outputs/claim-lineage.jsonl`, `outputs/stage3/final-draft.md`, and "
        "`outputs/stage3/fact-check-report.md`.\n\n"
        f"Create the canonical visual brief for an `argument_brief` presentation "
        f"of exactly {request.slide_count} slides. This deck strengthens and presents "
        "the argument; it is not a report placed on slides. Use one claim per slide, "
        "a genuine counter-case, an evidence-bearing signature visual, and a final "
        "implication or ask. The `slides` array must contain exactly "
        f"{request.slide_count} entries numbered 1 through {request.slide_count}.\n\n"
        "Write valid JSON to `outputs/stage4/visual-brief.json` and validate it "
        "against `assets/brand/visual-brief.schema.json`. Use `argument_brief` as "
        "the exact `deck_mode`; keep `report_visuals` as an empty array."
    )
    await _run_agent(
        agent=art_director,
        user_prompt=art_prompt,
        model=_model("art_direction"),
        cwd=repo_root,
        step_label="argument/art-direction",
        tally=tally,
        output_path=visual_path,
        artifact_contract=_visual_brief_contract(),
        manifest_path=manifest_path,
        artifact_id="argument/visual-brief",
        dependency_inputs=(
            "run-manifest.json",
            "context/argument-request.md",
            "stage1/evidence-map.md",
            "evidence-ledger.jsonl",
            "claim-lineage.jsonl",
            "stage3/final-draft.md",
            "stage3/fact-check-report.md",
        ),
    )
    visual_validation = _validate_visual_brief(
        out_path=visual_path,
        schema_path=schema_path,
        evidence_ledger=outputs_dir / "evidence-ledger.jsonl",
        requested_mode="argument_brief",
    )
    try:
        visual_payload = json.loads(visual_path.read_text(encoding="utf-8"))
        actual_slides = len(visual_payload.get("slides", []))
    except (OSError, TypeError, json.JSONDecodeError):
        actual_slides = 0
    if actual_slides != request.slide_count:
        visual_validation.valid = False
        visual_validation.errors.append(
            f"slides: expected exactly {request.slide_count}, got {actual_slides}"
        )
    await emit(
        "artifact_validated",
        step="argument/visual-brief",
        **visual_validation.to_dict(),
    )
    if not visual_validation.valid:
        raise RuntimeError(
            "Argument visual brief failed validation: "
            + "; ".join(visual_validation.errors[:8])
        )

    out_path = outputs_dir / "stage4" / f"argument-{request.slug}.pptx"
    inspection_dir = outputs_dir / "stage4" / "inspection" / request.slug
    receipt_path = outputs_dir / "stage4" / f"argument-{request.slug}-visual-inspection.json"
    qa_path = outputs_dir / "stage4" / f"argument-{request.slug}-qa.json"
    prompt = (
        f"Build an executive presentation of exactly {request.slide_count} slides "
        f"for \"{request.title}\".\n\n"
        "Read the final verified argument at `outputs/stage3/final-draft.md`, the "
        "fact-check report, evidence ledger, claim lineage, argument request, and "
        "the exact slide contract at `outputs/stage4/visual-brief.json`. Follow the "
        "brand system in `assets/brand/`.\n\n"
        f"Save the finished deck to `{out_path.relative_to(repo_root).as_posix()}`. "
        f"It must contain exactly {request.slide_count} slides—no title-slide or "
        "appendix additions beyond the canonical slide contract.\n\n"
        "After building, run this exact QA and inspection command:\n\n"
        f"`.venv/bin/python -m cli.presentation_qa \"{out_path}\" "
        f"--mode argument_brief --slide-count {request.slide_count} "
        f"--visual-brief \"{visual_path}\" --json \"{inspection_dir / 'designer-qa.json'}\" "
        f"--render-dir \"{inspection_dir}\" --prepare-inspection \"{receipt_path}\"`\n\n"
        "Inspect every rendered slide at full size and the montage. Fix all defects. "
        "Then edit only the receipt's `inspection` object to attest the exact final "
        "bytes, signature exhibit, and resolved findings as required by your charter."
    )
    await _run_agent(
        agent=designer,
        user_prompt=prompt,
        model=_model("presentation"),
        cwd=repo_root,
        step_label="argument/presentation",
        tally=tally,
        output_path=out_path,
        required_outputs=((receipt_path, _visual_inspection_contract()),),
        manifest_path=manifest_path,
        artifact_id="argument/presentation",
        dependency_inputs=(
            "run-manifest.json",
            "context/argument-request.md",
            "stage3/final-draft.md",
            "stage3/fact-check-report.md",
            "evidence-ledger.jsonl",
            "claim-lineage.jsonl",
            "stage4/visual-brief.json",
        ),
    )

    from cli.presentation_qa import (
        PresentationQAConfig,
        qa_presentation,
        qa_visual_inspection_receipt,
    )

    qa_report = qa_presentation(
        out_path,
        config=PresentationQAConfig.for_argument(request.slide_count),
        render_dir=outputs_dir / "stage4" / "qa" / request.slug,
        deck_mode="argument_brief",
        visual_brief=visual_path,
    )
    inspection = qa_visual_inspection_receipt(
        receipt_path,
        artifact=out_path,
        visual_brief=visual_path,
        deck_mode="argument_brief",
    )
    qa_report.issues.extend(inspection.issues)
    qa_report.metadata["visual_inspection"] = inspection.metadata
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
    assert_quality(qa_report)
    return out_path


async def run_strengthen_pipeline(
    *,
    request: StrengthenRequest,
    source_files: Iterable[Path] = (),
    repo_root: Path = REPO_ROOT,
    budget_usd: float | None = None,
    resume: bool = False,
) -> StrengthenResult:
    """Run the focused research, rewrite, verification, and optional deck path."""

    all_agents = load_all_agents()
    by_name = {agent.name: agent for agent in all_agents}
    allowed = {agent.name for agent in research_agents(all_agents)}
    # Revalidate persisted or programmatic requests at the paid-work boundary.
    payload = asdict(request)
    payload["agents"] = payload.pop("selected_agents")
    request = StrengthenRequest.from_payload(payload, allowed_agents=allowed)
    if resume:
        if not request.slug:
            raise ValueError("A resumed argument run must preserve its slug.")
    else:
        request.slug = _unique_slug(request.title, repo_root)

    outputs_dir = repo_root / "outputs"
    for folder in ("context", "stage1", "stage2", "stage3", "stage4"):
        (outputs_dir / folder).mkdir(parents=True, exist_ok=True)
    tally = CostTally(budget_usd=budget_usd)
    # Research calls run concurrently; reserve an honest share for all remaining
    # sequential calls as well.
    tally.plan_calls(len(request.selected_agents) + 4 + (2 if request.want_pptx else 0))
    result = StrengthenResult(
        tally=tally,
        slug=request.slug,
        public_slug=f"argument-{request.slug}",
    )

    request_json = outputs_dir / "context" / "argument-request.json"
    if not resume or not request_json.is_file():
        persisted = asdict(request)
        _atomic_json(request_json, persisted)
    _write_active_marker(outputs_dir, request, preserve_started=resume)

    from cli.sources import attach_sources, inline_for_openai

    supplied = [Path(path) for path in source_files]
    if supplied:
        attach_sources(request.slug, supplied, outputs_dir)
    source_dir = repo_root / "sources" / "runs" / request.slug
    source_dir.mkdir(parents=True, exist_ok=True)
    if request.argument_text:
        pasted = source_dir / "pasted-argument.md"
        expected = "# Pasted argument\n\n" + request.argument_text.rstrip() + "\n"
        if not pasted.is_file():
            pasted.write_text(expected, encoding="utf-8")
        elif pasted.read_text(encoding="utf-8") != expected:
            raise RuntimeError(
                "The persisted pasted argument differs from this resume request."
            )

    readable_sources = _readable_source_library(repo_root, request.slug)
    if not readable_sources:
        raise RuntimeError("No readable argument material was attached.")
    source_paths = [path.relative_to(repo_root).as_posix() for path in readable_sources]
    request_md = outputs_dir / "context" / "argument-request.md"
    request_md.write_text(_request_markdown(request, source_paths), encoding="utf-8")

    process_names = ["evidence-curator", "strategist", "fact-checker"]
    if request.want_pptx:
        process_names.extend(["art-director", "presentation-designer"])
    manifest_path = _prepare_argument_manifest(
        request=request,
        repo_root=repo_root,
        outputs_dir=outputs_dir,
        readable_sources=readable_sources,
        agents=by_name,
        process_names=process_names,
        resume=resume,
    )
    from cli.run_manifest import build_dependency_fingerprint, update_artifact

    await emit(
        "run_start",
        slug=result.public_slug,
        title=request.title,
        mode="strengthen",
        agents=[*request.selected_agents, *process_names],
        stages=[
            "Research",
            "Strengthen",
            "Verify",
            "Build deck" if request.want_pptx else "Release",
        ],
    )

    # Stage 1 — independent research swarm.
    await emit("stage_start", stage=1, label="Researching the argument from selected lenses")
    await emit(
        "research_swarm_start",
        agents=request.selected_agents,
        total=len(request.selected_agents),
        concurrency=4,
    )
    semaphore = asyncio.Semaphore(4)

    async def research_one(name: str) -> None:
        agent = by_name[name]
        brief = outputs_dir / "stage1" / f"{name}-brief.md"
        evidence = outputs_dir / "stage1" / f"{name}-evidence.jsonl"
        prompt = (
            "Read `outputs/context/argument-request.md` and every supplemental "
            "source listed there. Research only what will materially strengthen, "
            "qualify, or disprove the supplied argument. Preserve independent "
            "judgment; do not read other researchers' outputs. Identify the strongest "
            "mechanism, primary-source evidence, named cases, quantitative anchors, "
            "and counterevidence.\n\n"
            f"Write a focused research brief to `{brief.relative_to(repo_root).as_posix()}`. "
            "Keep it useful to a writer rather than expanding into a general report."
        )
        required: tuple[tuple[Path, ArtifactContract], ...] = ()
        if agent.provider != "openai":
            prompt += (
                f"\n\nAlso write claim-level evidence to "
                f"`{evidence.relative_to(repo_root).as_posix()}` as JSONL. Each record "
                "must contain `claim`, `source_title`, `source_url` or `source_path`, "
                "`source_type`, `is_primary`, `page_or_section`, "
                "`supporting_excerpt`, `source_date`, `data_vintage`, "
                "`airport_or_entity`, `units`, `denominator`, `caveat`, and "
                "`confidence`. Never invent missing metadata."
            )
            required = (
                (
                    evidence,
                    ArtifactContract(
                        "jsonl",
                        min_records=1,
                        required_keys=RESEARCH_EVIDENCE_CONTRACT.required_keys,
                        required_any=RESEARCH_EVIDENCE_CONTRACT.required_any,
                    ),
                ),
            )
        else:
            prompt += "\n\n" + request_md.read_text(encoding="utf-8")
            prompt += inline_for_openai(source_paths, repo_root=repo_root)
        async with semaphore:
            await _run_agent(
                agent=agent,
                user_prompt=prompt,
                model=agent.model_override or _model("research"),
                cwd=repo_root,
                step_label=f"argument/research/{name}",
                tally=tally,
                output_path=brief,
                required_outputs=required,
                manifest_path=manifest_path,
                artifact_id=f"argument/research/{name}",
                dependency_inputs=(
                    "run-manifest.json",
                    "context/argument-request.md",
                ),
            )

    await asyncio.gather(*(research_one(name) for name in request.selected_agents))
    await emit(
        "research_swarm_complete",
        agents=request.selected_agents,
        total=len(request.selected_agents),
    )

    ledger_path = outputs_dir / "evidence-ledger.jsonl"
    evidence_map = outputs_dir / "stage1" / "evidence-map.md"
    curator_dependencies = (
        "run-manifest.json",
        "context/argument-request.md",
        "stage1/*-brief.md",
        "stage1/*-evidence.jsonl",
    )
    curator_outputs = (
        (evidence_map, contract_for_path(evidence_map)),
        (ledger_path, ArtifactContract("jsonl", min_records=0)),
    )
    curator_can_resume = bool(
        resume
        and _required_outputs_complete(curator_outputs)
        and _required_outputs_match_manifest(
            curator_outputs,
            manifest_path,
            curator_dependencies,
        )
    )
    if not curator_can_resume:
        ledger = build_evidence_ledger(
            selected_agents=request.selected_agents,
            stage1_dir=outputs_dir / "stage1",
            output_path=ledger_path,
        )
        update_artifact(
            manifest_path,
            ledger_path,
            validate_artifact(ledger_path, ArtifactContract("jsonl", min_records=0)),
            artifact_id="argument/evidence-ledger",
            producer="orchestrator",
        )
        await emit(
            "evidence_update",
            ledger_path=str(ledger_path),
            record_count=ledger.record_count,
            agents_without_evidence=ledger.agents_without_evidence,
            invalid_record_count=len(ledger.invalid_records),
        )
    curator_prompt = (
        "Read the argument request, all selected research briefs in "
        "`outputs/stage1/`, and `outputs/evidence-ledger.jsonl`. Reconcile duplicate "
        "findings, disagreements, primary-source quality, and the strongest "
        "counter-case. Use targeted web research only for a small number of "
        "load-bearing gaps. Update the canonical evidence ledger in place with any "
        "new verified evidence.\n\nWrite a compact argument kit—not a report—to "
        "`outputs/stage1/evidence-map.md`. Rank the evidence the strategist should "
        "use, state what not to claim, and identify any unresolved limits."
    )
    await _run_agent(
        agent=by_name["evidence-curator"],
        user_prompt=curator_prompt,
        model=_model("curation"),
        cwd=repo_root,
        step_label="argument/evidence-curation",
        tally=tally,
        output_path=evidence_map,
        required_outputs=((ledger_path, ArtifactContract("jsonl", min_records=0)),),
        manifest_path=manifest_path,
        artifact_id="argument/evidence-map",
        dependency_inputs=curator_dependencies,
    )
    ledger = normalise_evidence_ledger(ledger_path)
    curator_fingerprint = build_dependency_fingerprint(
        manifest_path, curator_dependencies
    )
    update_artifact(
        manifest_path,
        evidence_map,
        validate_artifact(evidence_map, contract_for_path(evidence_map)),
        artifact_id="argument/evidence-map",
        producer="evidence-curator",
        dependencies=curator_fingerprint,
    )
    update_artifact(
        manifest_path,
        ledger_path,
        validate_artifact(ledger_path, ArtifactContract("jsonl", min_records=0)),
        artifact_id="argument/evidence-ledger",
        producer="evidence-curator",
        dependencies=curator_fingerprint,
    )
    await emit(
        "evidence_update",
        ledger_path=str(ledger_path),
        record_count=ledger.record_count,
        agents_without_evidence=[],
        invalid_record_count=len(ledger.invalid_records),
    )

    # Stage 2 — write only the strengthened argument.
    await emit("stage_start", stage=2, label="Rebuilding the argument around the evidence")
    strategist_draft = outputs_dir / "stage2" / "strategist-draft.md"
    strategist_prompt = (
        "Read `outputs/context/argument-request.md`, every selected research brief, "
        "`outputs/stage1/evidence-map.md`, and `outputs/evidence-ledger.jsonl`.\n\n"
        "Rewrite the supplied argument into one concise, standalone, evidence-driven "
        "argument for the named audience. Preserve the author's intended position, "
        "but sharpen the thesis, causal mechanism, quantitative anchors, named cases, "
        "and strongest counter-case. Change or narrow the claim when the evidence "
        "requires it. Do not describe the research process, agents, briefs, or Council. "
        "Do not write an executive summary, table of contents, methodology, appendix, "
        "or report sections. Aim for 600–1,200 words and never exceed 1,500 words. "
        "Use reader-facing numeric Markdown footnotes for every material factual claim.\n\n"
        "Write the complete argument to `outputs/stage2/strategist-draft.md`."
    )
    await _run_agent(
        agent=by_name["strategist"],
        user_prompt=strategist_prompt,
        model=_model("synthesis"),
        cwd=repo_root,
        step_label="argument/strategist",
        tally=tally,
        output_path=strategist_draft,
        artifact_contract=ArtifactContract("markdown", min_words=250),
        manifest_path=manifest_path,
        artifact_id="argument/strategist-draft",
        dependency_inputs=(
            "run-manifest.json",
            "context/argument-request.md",
            "stage1/*-brief.md",
            "stage1/evidence-map.md",
            "evidence-ledger.jsonl",
        ),
    )

    # Stage 3 — independent source verification and publication text gate.
    await emit("stage_start", stage=3, label="Verifying every load-bearing claim")
    final_draft = outputs_dir / "stage3" / "final-draft.md"
    fact_report = outputs_dir / "stage3" / "fact-check-report.md"
    lineage_path = outputs_dir / "claim-lineage.jsonl"
    fact_prompt = (
        "Verify the reader-facing draft at `outputs/stage2/strategist-draft.md` "
        "against `outputs/evidence-ledger.jsonl`, the underlying primary sources, "
        "the research briefs, and the supplied argument material. Check every number, "
        "named example, attribution, causal claim, date, denominator, and footnote. "
        "Remove or narrow anything you cannot verify. Preserve a concise argument; do "
        "not expand it into a report. The released text may contain no internal Council "
        "language or unverified tags.\n\n"
        "Write the verified argument to `outputs/stage3/final-draft.md`, the verification "
        "log to `outputs/stage3/fact-check-report.md`, and claim lineage to "
        "`outputs/claim-lineage.jsonl` using your charter's JSONL schema. For each "
        "reader-facing footnote marker, use one retained lineage record whose `claim` "
        "copies the complete cited sentence or table row verbatim and whose `citation` "
        "copies that footnote definition verbatim. Consolidate multiple facts in one "
        "cited sentence into that record's evidence ID list. Do not create retained "
        "records for dates, revisions, or other source metadata that the reader-facing "
        "draft does not actually assert. The release gate rejects every retained record "
        "whose `primary_source_checked` is not true. If you cannot actually check the "
        "primary source or the primary inputs to a disclosed calculation, remove the "
        "claim from the final draft; a copied excerpt, a brief, a prior verification "
        "note, or an inaccessible URL does not satisfy this rule."
    )
    fact_dependencies = (
        "run-manifest.json",
        "context/argument-request.md",
        "stage1/evidence-map.md",
        "evidence-ledger.jsonl",
        "stage2/strategist-draft.md",
    )
    await _run_agent(
        agent=by_name["fact-checker"],
        user_prompt=fact_prompt,
        model=_model("factcheck"),
        cwd=repo_root,
        step_label="argument/fact-check",
        tally=tally,
        output_path=final_draft,
        artifact_contract=ArtifactContract("markdown", min_words=250),
        required_outputs=(
            (fact_report, contract_for_path(fact_report)),
            (lineage_path, CLAIM_LINEAGE_AGENT_CONTRACT),
        ),
        manifest_path=manifest_path,
        artifact_id="argument/final-draft",
        dependency_inputs=fact_dependencies,
    )
    quality_path = outputs_dir / "quality-gate.json"
    from cli.quality_gate import run_publication_quality_gate

    def evaluate_verification() -> tuple[list[dict[str, Any]], Any, dict[str, Any]]:
        current_lineage, _ = ensure_claim_lineage(
            final_draft=final_draft,
            evidence_ledger=ledger_path,
            output_path=lineage_path,
        )
        current_lineage = bind_claim_lineage_to_draft(
            final_draft=final_draft, output_path=lineage_path
        )
        current_validation = validate_artifact(
            lineage_path, CLAIM_LINEAGE_CONTRACT
        )
        current_quality = run_publication_quality_gate(
            final_draft=final_draft,
            report_path=quality_path,
            evidence_ledger_path=ledger_path,
            agent_names=[*request.selected_agents, *process_names],
            claim_lineage_path=lineage_path,
            output_format="argument",
            length_instruction="250–1,500 words",
            raise_on_failure=False,
        )
        return current_lineage, current_validation, current_quality

    lineage, lineage_validation, quality = evaluate_verification()
    verification_dependencies = fact_dependencies
    if not lineage_validation.valid or not quality["passed"]:
        await emit(
            "quality_gate",
            passed=False,
            attempt=1,
            remediation_pending=True,
            error_count=int(quality["error_count"]),
            warning_count=int(quality["warning_count"]),
        )
        remediation_dir = outputs_dir / "stage3" / "lineage-remediation-input"
        remediation_dir.mkdir(parents=True, exist_ok=True)
        remediation_draft = remediation_dir / "final-draft.md"
        remediation_report = remediation_dir / "fact-check-report.md"
        remediation_lineage = remediation_dir / "claim-lineage.jsonl"
        remediation_quality = remediation_dir / "quality-gate.json"
        shutil.copy2(final_draft, remediation_draft)
        shutil.copy2(fact_report, remediation_report)
        shutil.copy2(lineage_path, remediation_lineage)
        shutil.copy2(quality_path, remediation_quality)
        issue_lines = [
            f"- {issue.get('code')}: {issue.get('message')}"
            for issue in quality.get("issues", [])
            if isinstance(issue, dict) and issue.get("severity") == "error"
        ]
        for error in lineage_validation.errors:
            line = f"- lineage_contract: {error}"
            if line not in issue_lines:
                issue_lines.append(line)
        remediation_instructions = remediation_dir / "instructions.md"
        remediation_instructions.write_text(
            "# Argument verification remediation\n\n"
            "The first verification pass did not satisfy the deterministic release "
            "contract. Repair the final argument and rebuild its lineage.\n\n"
            "## Blocking findings\n\n"
            + "\n".join(issue_lines)
            + "\n",
            encoding="utf-8",
        )
        verification_dependencies = (
            *fact_dependencies,
            "stage3/lineage-remediation-input/final-draft.md",
            "stage3/lineage-remediation-input/fact-check-report.md",
            "stage3/lineage-remediation-input/claim-lineage.jsonl",
            "stage3/lineage-remediation-input/quality-gate.json",
            "stage3/lineage-remediation-input/instructions.md",
        )
        remediation_prompt = (
            "Read the immutable first-pass verification files and blocking findings "
            "under `outputs/stage3/lineage-remediation-input/`, together with "
            "`outputs/evidence-ledger.jsonl` and the underlying primary sources. "
            "Perform one bounded release remediation. Preserve the concise argument "
            "unless a factual claim must be removed or narrowed.\n\n"
            "Rebuild claim lineage around the reader-facing draft, not around source "
            "metadata: create exactly one retained record per footnote marker; copy "
            "the complete sentence or table row immediately cited by that marker "
            "verbatim into `claim`; copy the reader-facing footnote definition "
            "verbatim into `citation`; and include every evidence ID needed for the "
            "compound sentence in that one record. Omit records for facts not asserted "
            "in the draft. A retained verified, qualified, or corrected claim may set "
            "`primary_source_checked` true only after the underlying primary source or "
            "primary inputs to a disclosed calculation were actually checked. The "
            "deterministic gate rejects every retained record with that field false: "
            "an HTTP error, a copied ledger excerpt, a secondary article, or a prior "
            "agent's verification note does not count. If the primary source remains "
            "inaccessible, delete the factual assertion and its footnote rather than "
            "reporting it as resolved. Before writing, confirm that every retained JSONL "
            "record will have `primary_source_checked: true`.\n\n"
            "Write the repaired argument to `outputs/stage3/final-draft.md`, the "
            "updated verification log to `outputs/stage3/fact-check-report.md`, and "
            "canonical JSONL to `outputs/claim-lineage.jsonl`."
        )
        await _run_agent(
            agent=by_name["fact-checker"],
            user_prompt=remediation_prompt,
            model=_model("factcheck"),
            cwd=repo_root,
            step_label="argument/fact-check-remediation",
            tally=tally,
            output_path=final_draft,
            artifact_contract=ArtifactContract("markdown", min_words=250),
            required_outputs=(
                (fact_report, contract_for_path(fact_report)),
                (lineage_path, CLAIM_LINEAGE_AGENT_CONTRACT),
            ),
            manifest_path=manifest_path,
            artifact_id="argument/final-draft-remediated",
            dependency_inputs=verification_dependencies,
        )
        lineage, lineage_validation, quality = evaluate_verification()
        if not lineage_validation.valid:
            raise RuntimeError(
                "Strengthened argument claim lineage remains incomplete after the "
                "bounded remediation pass: "
                + "; ".join(lineage_validation.errors)
            )
        quality = run_publication_quality_gate(
            final_draft=final_draft,
            report_path=quality_path,
            evidence_ledger_path=ledger_path,
            agent_names=[*request.selected_agents, *process_names],
            claim_lineage_path=lineage_path,
            output_format="argument",
            length_instruction="250–1,500 words",
            raise_on_failure=True,
        )
    update_artifact(
        manifest_path,
        lineage_path,
        lineage_validation,
        artifact_id="argument/claim-lineage",
        producer="fact-checker",
        dependencies=build_dependency_fingerprint(
            manifest_path, verification_dependencies
        ),
    )
    await emit(
        "evidence_update",
        kind="claim_lineage",
        record_count=len(lineage),
        agents_without_evidence=[],
    )

    update_artifact(
        manifest_path,
        quality_path,
        validate_artifact(quality_path, contract_for_path(quality_path)),
        artifact_id="argument/quality-gate",
        producer="orchestrator",
        dependencies=build_dependency_fingerprint(
            manifest_path,
            (
                "run-manifest.json",
                "stage3/final-draft.md",
                "evidence-ledger.jsonl",
                "claim-lineage.jsonl",
            ),
        ),
    )
    await emit(
        "quality_gate",
        passed=bool(quality["passed"]),
        error_count=int(quality["error_count"]),
        warning_count=int(quality["warning_count"]),
    )

    # Stage 4 — optional exact-length deck, then immutable archive and release.
    await emit(
        "stage_start",
        stage=4,
        label=(
            f"Building an exact {request.slide_count}-slide deck"
            if request.want_pptx
            else "Archiving and releasing the strengthened argument"
        ),
    )
    deck_path: Path | None = None
    if request.want_pptx:
        deck_path = await _build_argument_deck(
            request=request,
            repo_root=repo_root,
            outputs_dir=outputs_dir,
            agents=by_name,
            tally=tally,
            manifest_path=manifest_path,
        )
    archive_dir = _archive_strengthen_run(
        repo_root=repo_root, request=request, tally=tally
    )
    argument_release, deck_release = _publish_strengthen_release(
        repo_root=repo_root,
        request=request,
        final_argument=final_draft,
        deck=deck_path,
        archive_dir=archive_dir,
    )
    from cli.archive import _clear_outputs

    _clear_outputs(outputs_dir)
    result.archive_path = archive_dir
    result.argument_path = argument_release
    result.deck_path = deck_release
    result.completed = True
    await emit(
        "run_complete",
        slug=result.public_slug,
        title=request.title,
        mode="strengthen",
        total=tally.total,
        archive=archive_dir.relative_to(repo_root).as_posix(),
        slide_count=request.slide_count,
    )
    _notify_done(
        "AI Council", f"Strengthened argument complete: {request.title} (${tally.total:.2f})"
    )
    return result
