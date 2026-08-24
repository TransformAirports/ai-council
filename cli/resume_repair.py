"""Audited re-baseline for a resume contract that failed on a false positive.

``ResumeContractMismatch`` is correct to fail closed: paid artifacts must never
be silently reused under a changed contract. But the guard hashes some things
that carry no contract meaning (historically, the order the operator clicked
agents), and legitimate maintenance to the identity code itself changes the
execution-contract fingerprint. Both refuse resumes that are actually safe.

This module is the sanctioned escape hatch. It refuses to touch anything unless
the *semantic* contract is provably identical — same run, same seated agents,
same agent instructions byte-for-byte, same model routing, same run prompt,
same source material. Code drift must be acknowledged explicitly and is
recorded in the manifest. Every re-baseline writes an audit entry, so a
re-baselined run is never indistinguishable from an untouched one.

Usage:
    python -m cli.resume_repair                     # inspect only
    python -m cli.resume_repair --apply             # re-baseline
    python -m cli.resume_repair --apply --accept-code-changes
    python -m cli.resume_repair --apply --redo-agent fact-checker
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cli.run_manifest import (
    EXECUTION_CONTRACT_PATTERNS,
    MANIFEST_NAME,
    build_execution_contract_fingerprint,
    create_run_manifest,
    refresh_dependency_fingerprint_sha256,
)
from cli.council_models import council_model

REPO_ROOT = Path(__file__).resolve().parent.parent


def _effective_model_for_resume(spec: Any, agent: Any, role: str) -> str:
    """Mirror the orchestrator's run-level-over-legacy model precedence."""

    selected = council_model(getattr(spec, "council_model", ""))
    if selected is not None:
        return selected.id
    from cli.orchestrator import _model

    return agent.model_override or _model(role)


@dataclass
class RepairReport:
    slug: str = ""
    stored_identity: str = ""
    current_identity: str = ""
    blocking: list[str] = field(default_factory=list)
    benign: list[str] = field(default_factory=list)
    code_changes: list[str] = field(default_factory=list)

    @property
    def already_matches(self) -> bool:
        return bool(self.stored_identity) and self.stored_identity == self.current_identity

    @property
    def safe_to_rebaseline(self) -> bool:
        return not self.blocking


def _sha(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    except OSError:
        return None


def _mirror_repo(sandbox: Path, agents_dir: Path) -> None:
    """Copy the byte-identical inputs the identity hash reads.

    The fingerprint is taken relative to ``outputs_dir.parent``, so identity can
    only be recomputed faithfully inside a directory shaped like the repo.
    """
    for pattern in EXECUTION_CONTRACT_PATTERNS:
        for src in sorted(REPO_ROOT.glob(pattern)):
            if not src.is_file():
                continue
            dst = sandbox / src.relative_to(REPO_ROOT)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    dst_agents = sandbox / agents_dir.relative_to(REPO_ROOT)
    dst_agents.parent.mkdir(parents=True, exist_ok=True)
    if dst_agents.exists():
        shutil.rmtree(dst_agents)
    shutil.copytree(agents_dir, dst_agents)
    src_sources = REPO_ROOT / "sources"
    if src_sources.is_dir():
        shutil.copytree(src_sources, sandbox / "sources", dirs_exist_ok=True)


def compute_current_identity(outputs_dir: Path = REPO_ROOT / "outputs") -> tuple[str, dict[str, Any]]:
    """Recompute the identity the running code would produce, without writing.

    Uses the real ``create_run_manifest`` against a faithful repo mirror so this
    can never drift from the guard it is meant to reconcile.
    """
    from cli.agents import load_all_agents
    from cli.orchestrator import PIPELINE_DEFINITION, _model
    from cli.runfile import RUNS_DIR, parse_run_file

    manifest = json.loads((outputs_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    slug = manifest["run"]["slug"]
    spec = parse_run_file(slug)

    needs_art = bool(getattr(spec, "want_pptx", False)) or any(
        step.id == "art-director" for step in PIPELINE_DEFINITION
    )
    steps = tuple(
        s for s in PIPELINE_DEFINITION
        if (s.id != "art-director" or needs_art)
        and (s.id != "presentation" or bool(getattr(spec, "want_pptx", False)))
    )
    roles = {"research", *(s.model_role for s in steps)}
    selected_model = council_model(getattr(spec, "council_model", ""))
    assignments = {
        role: selected_model.id if selected_model is not None else _model(role)
        for role in sorted(roles)
    }

    agents_dir = REPO_ROOT / ".claude" / "agents"
    with tempfile.TemporaryDirectory() as td:
        sandbox = Path(td) / "repo"
        sandbox.mkdir(parents=True)
        _mirror_repo(sandbox, agents_dir)
        sandbox_outputs = sandbox / "outputs"
        sandbox_outputs.mkdir(parents=True, exist_ok=True)
        run_file = RUNS_DIR / f"{slug}.md"
        sandbox_run = sandbox / run_file.relative_to(REPO_ROOT)
        sandbox_run.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(run_file, sandbox_run)
        path = create_run_manifest(
            spec=spec,
            run_file=sandbox_run,
            outputs_dir=sandbox_outputs,
            all_agents=load_all_agents(sandbox / ".claude" / "agents"),
            resume=False,
            pipeline_steps=steps,
            model_assignments=assignments,
        )
        fresh = json.loads(path.read_text(encoding="utf-8"))
    return fresh["run"]["resume_identity_sha256"], fresh


def inspect(outputs_dir: Path = REPO_ROOT / "outputs") -> RepairReport:
    """Compare stored and current identity, classifying every difference."""
    from cli.agents import load_all_agents
    from cli.runfile import RUNS_DIR, parse_run_file

    report = RepairReport()
    manifest = json.loads((outputs_dir / MANIFEST_NAME).read_text(encoding="utf-8"))
    stored_run = manifest["run"]
    report.slug = stored_run["slug"]
    report.stored_identity = stored_run.get("resume_identity_sha256", "")

    spec = parse_run_file(report.slug)
    agents = {a.name: a for a in load_all_agents()}

    # Run prompt — the durable statement of the question.
    run_file = RUNS_DIR / f"{report.slug}.md"
    if _sha(run_file) != stored_run.get("run_prompt_sha256"):
        report.blocking.append("run prompt bytes changed since the artifacts were produced")

    # Roster: set identity is the contract; order is not.
    stored_roster = [e["name"] for e in manifest.get("selected_research_agents", [])]
    current_roster = list(getattr(spec, "selected_research_agents", []) or [])
    if set(stored_roster) != set(current_roster):
        added = sorted(set(current_roster) - set(stored_roster))
        removed = sorted(set(stored_roster) - set(current_roster))
        report.blocking.append(f"seated roster changed (added={added}, removed={removed})")
    elif stored_roster != current_roster:
        report.benign.append("roster order differs (same agents; seating order is not a contract)")

    # Agent instructions must be byte-identical — they produced the artifacts.
    for entry in manifest.get("selected_research_agents", []) + manifest.get("process_agents", []):
        name = entry.get("name")
        agent = agents.get(name)
        if agent is None:
            report.blocking.append(f"agent no longer exists: {name}")
            continue
        if _sha(agent.path) != entry.get("prompt_sha256"):
            report.blocking.append(f"agent instructions changed: {name}")

    # Model routing per role. An explicit run-level selection is authoritative
    # for every agent, just as it was when create_run_manifest recorded the
    # run. Comparing those entries to legacy council.toml routing would
    # incorrectly block every GPT-selected resume.
    seen: dict[str, str] = {}
    for entry in manifest.get("selected_research_agents", []) + manifest.get("process_agents", []):
        role, stored_model = entry.get("model_role"), entry.get("model_id")
        if not role or role in seen:
            continue
        seen[role] = stored_model
        current_model = _effective_model_for_resume(
            spec, agents[entry["name"]], role
        )
        if current_model != stored_model:
            report.blocking.append(
                f"model routing changed for {role}: {stored_model} → {current_model}"
            )

    # Source material must be byte-identical.
    for src in stored_run.get("source_material") or []:
        if _sha(REPO_ROOT / src["runtime_path"]) != src.get("sha256"):
            report.blocking.append(f"source file changed or missing: {src['runtime_path']}")

    # Code / prompts / design rules — reported, never auto-approved.
    stored_code = {r["path"]: r["sha256"] for r in (stored_run.get("execution_contract") or [])}
    current_code = {r["path"]: r["sha256"] for r in build_execution_contract_fingerprint(REPO_ROOT)}
    report.code_changes = sorted(
        [f"~ {p}" for p in stored_code.keys() & current_code.keys() if stored_code[p] != current_code[p]]
        + [f"+ {p}" for p in current_code.keys() - stored_code.keys()]
        + [f"- {p}" for p in stored_code.keys() - current_code.keys()]
    )

    report.current_identity, _ = compute_current_identity(outputs_dir)
    return report


AGENT_INSTRUCTIONS_CHANGED = "agent instructions changed: "


def _discard_agent_artifacts(manifest: dict, agent_names: set[str]) -> list[str]:
    """Reset one agent's artifacts to pending so its work is redone, not reused.

    An agent whose instructions changed must not have its old output reused —
    that is what the blocking check protects. But the check is whole-run: it
    refuses a resume even when the only artifacts at risk are the ones the
    edited agent produced and which the resume would regenerate anyway.

    Discarding those artifacts makes the guarantee precise instead of coarse.
    Nothing produced under the old instructions survives, so the run stays
    internally consistent, and work by agents whose instructions did not change
    is untouched.
    """

    discarded: list[str] = []
    for artifact in manifest.get("artifacts", []):
        if str(artifact.get("producer") or "") not in agent_names:
            continue
        artifact["status"] = "pending"
        for field_name in ("sha256", "dependencies", "validation", "size_bytes",
                           "word_count", "record_count", "completed_at"):
            artifact.pop(field_name, None)
        discarded.append(str(artifact.get("path", "")))
    return discarded


def _restamp_dependency_identities(
    manifest: dict,
    previous_identity: str,
    new_identity: str,
    outputs_dir: Path | None = None,
) -> list[str]:
    """Re-point completed artifacts' dependency receipts at the new identity.

    Every artifact records the run identity it was bound to. Moving the run's
    identity without moving these leaves each completed artifact pointing at an
    identity that no longer exists — and the orchestrator quarantines and
    re-runs any artifact whose receipt does not match, so a re-baseline would
    silently discard every paid brief in the run.

    Only receipts carrying exactly ``previous_identity`` are moved. A receipt
    bound to some third identity came from a different run and is left alone,
    so this repairs continuity without ever inventing it.

    An artifact is re-stamped only when its bytes still hash to the value the
    manifest recorded. A file that has since changed is genuinely out of sync
    with its receipt, and re-stamping it would launder a real mismatch into an
    apparently-valid one — so it is left for the orchestrator to re-run.
    """

    if not previous_identity or previous_identity == new_identity:
        return []
    touched: list[str] = []
    for artifact in manifest.get("artifacts", []):
        if outputs_dir is not None:
            candidate = outputs_dir / str(artifact.get("path", ""))
            recorded = artifact.get("sha256")
            if not recorded or not candidate.is_file():
                continue
            if hashlib.sha256(candidate.read_bytes()).hexdigest() != recorded:
                continue
        dependencies = artifact.get("dependencies") or {}
        changed = False
        for record in dependencies.get("inputs", []):
            for entry in record.get("files", []):
                if (
                    entry.get("kind") == "run_identity"
                    and entry.get("sha256") == previous_identity
                ):
                    entry["sha256"] = new_identity
                    changed = True
        if changed:
            # The embedded identity is part of the canonical receipt body.
            # Refresh the outer digest in the same mutation so the next resume
            # does not mistake a safe re-baseline for changed upstream work.
            refresh_dependency_fingerprint_sha256(dependencies)
            touched.append(str(artifact.get("path", "")))
    return touched


def rebaseline(
    outputs_dir: Path = REPO_ROOT / "outputs",
    *,
    accept_code_changes: bool = False,
    reason: str = "",
    redo_agents: set[str] | None = None,
) -> RepairReport:
    """Re-point the stored identity at current state, with an audit record."""
    report = inspect(outputs_dir)
    redo = {name.strip() for name in (redo_agents or set()) if name.strip()}
    if redo:
        # An instruction change for an agent whose output we are about to throw
        # away is not a reason to refuse the resume.
        report.blocking = [
            entry for entry in report.blocking
            if not (
                entry.startswith(AGENT_INSTRUCTIONS_CHANGED)
                and entry[len(AGENT_INSTRUCTIONS_CHANGED):].strip() in redo
            )
        ]
    if report.already_matches:
        return report
    if not report.safe_to_rebaseline:
        raise RuntimeError(
            "Refusing to re-baseline — the contract genuinely changed:\n  "
            + "\n  ".join(report.blocking)
            + "\nThese artifacts were produced under different conditions. Start a new run."
        )
    if report.code_changes and not accept_code_changes:
        raise RuntimeError(
            "Local code, prompts, or design rules changed:\n  "
            + "\n  ".join(report.code_changes)
            + "\nRe-run with --accept-code-changes to record and accept them."
        )

    manifest_path = outputs_dir / MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    backup = manifest_path.with_suffix(
        f".json.pre-rebaseline-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}"
    )
    shutil.copy2(manifest_path, backup)

    _, fresh = compute_current_identity(outputs_dir)
    discarded = _discard_agent_artifacts(manifest, redo) if redo else []
    restamped = _restamp_dependency_identities(
        manifest,
        report.stored_identity,
        report.current_identity,
        outputs_dir=outputs_dir,
    )
    manifest["run"]["resume_identity_sha256"] = report.current_identity
    manifest["run"]["execution_contract"] = fresh["run"]["execution_contract"]
    manifest["run"]["source_material"] = fresh["run"].get("source_material")
    manifest["run"]["source_library"] = fresh["run"].get("source_library")
    manifest["selected_research_agents"] = fresh["selected_research_agents"]
    manifest["process_agents"] = fresh["process_agents"]
    manifest.setdefault("resume_rebaselines", []).append(
        {
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "previous_identity_sha256": report.stored_identity,
            "new_identity_sha256": report.current_identity,
            "benign_differences": report.benign,
            "accepted_code_changes": report.code_changes,
            "restamped_dependency_receipts": restamped,
            "redone_agents": sorted(redo),
            "discarded_artifacts": discarded,
            "reason": reason or "operator-approved re-baseline after verified-safe mismatch",
            "backup": backup.name,
        }
    )
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    tmp = manifest_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    tmp.replace(manifest_path)
    return report


def _print(report: RepairReport) -> None:
    print(f"run: {report.slug}")
    print(f"stored identity : {report.stored_identity[:16]}…")
    print(f"current identity: {report.current_identity[:16]}…")
    if report.already_matches:
        print("\n✓ identities match — resume is already safe.")
        return
    print("\nBLOCKING (real contract changes):")
    print("  " + "\n  ".join(report.blocking) if report.blocking else "  none")
    print("\nBENIGN (no contract meaning):")
    print("  " + "\n  ".join(report.benign) if report.benign else "  none")
    print("\nCODE / PROMPT / DESIGN CHANGES:")
    print("  " + "\n  ".join(report.code_changes) if report.code_changes else "  none")
    print(
        "\n"
        + ("✓ safe to re-baseline" if report.safe_to_rebaseline
           else "✗ NOT safe — start a new run")
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="cli.resume_repair",
        description="Inspect or repair a failed resume-contract check.",
    )
    p.add_argument("--apply", action="store_true", help="Write the re-baseline.")
    p.add_argument("--accept-code-changes", action="store_true",
                   help="Acknowledge and record local code/prompt/design changes.")
    p.add_argument("--reason", default="", help="Recorded in the audit entry.")
    p.add_argument(
        "--redo-agent", action="append", default=[], metavar="NAME",
        help=(
            "Accept an instruction change for NAME by DISCARDING every artifact "
            "NAME produced, so the resume regenerates them instead of reusing "
            "work made under the old instructions. Repeatable."
        ),
    )
    args = p.parse_args(argv)

    if not args.apply:
        _print(inspect())
        print("\n(inspection only — pass --apply to re-baseline)")
        return 0
    try:
        report = rebaseline(
            accept_code_changes=args.accept_code_changes,
            reason=args.reason,
            redo_agents=set(args.redo_agent),
        )
    except RuntimeError as exc:
        print(str(exc))
        return 2
    _print(report)
    if args.redo_agent:
        print(
            "\n✓ re-baselined. Discarded all artifacts produced by: "
            + ", ".join(sorted(set(args.redo_agent)))
            + " — the resume will regenerate them. Other agents' work is kept."
        )
    else:
        print(
            "\n✓ re-baselined. Resume from the app; completed artifacts are preserved."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
