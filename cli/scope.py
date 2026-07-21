"""Scope-fulfillment mode — turn a client scope of work into its deliverables.

The single-report pipeline answers a question. This pipeline fulfills an
engagement: drop a scope document (RFP, SOW, emailed scope) into sources/,
and the Council plans the deliverables, researches the regulatory and
professional grounding once, then builds every required artifact — Word
documents and PowerPoint decks — with an acceptance-review QA pass at the end.

Stages (custom rail): Plan → Research → Build → Package.
Checkpoints: plan approval (before money is spent on production) and final
QA review (before packaging). Both honor auto_approve.

Every artifact build is resumable: re-running the same engagement title skips
any deliverable whose file already exists with content.
"""
from __future__ import annotations

import asyncio
import json
import re
import shutil
import zipfile
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from rich.console import Console
from slugify import slugify

from cli.agents import load_all_agents
from cli.events import emit, get_sink, request_checkpoint
from cli.orchestrator import (
    CostTally,
    RunBudgetExceeded,
    _model,
    _notify_done,
    _run_agent,
    write_run_marker,
)

console = Console()
REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "reports"


@dataclass
class ScopeResult:
    tally: CostTally
    slug: str = ""
    archive_path: Path | None = None
    package_dir: Path | None = None
    zip_path: Path | None = None
    completed: bool = False


# ----------------------------------------------------------------------------
# Plan handling.
# ----------------------------------------------------------------------------

VALID_KINDS = {"docx", "pptx"}


def parse_plan(raw: str) -> dict:
    """Parse and validate the planner's JSON. Raises ValueError with a
    message suitable for feeding back to the planner on retry."""
    text = raw.strip()
    # Strip a markdown fence if the model wrapped one despite instructions.
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    try:
        plan = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"plan.json is not valid JSON: {e}") from e

    if not isinstance(plan.get("deliverables"), list) or not plan["deliverables"]:
        raise ValueError("plan must contain a non-empty 'deliverables' list")
    seen_ids: set[str] = set()
    for d in plan["deliverables"]:
        for key in ("id", "title", "kind", "filename", "instructions"):
            if not d.get(key):
                raise ValueError(f"deliverable missing '{key}': {d}")
        if d["kind"] not in VALID_KINDS:
            raise ValueError(f"deliverable {d['id']}: kind must be docx or pptx")
        if d["id"] in seen_ids:
            raise ValueError(f"duplicate deliverable id {d['id']}")
        seen_ids.add(d["id"])
        d.setdefault("depends_on", [])
        d["filename"] = Path(d["filename"]).name  # no path tricks
    for d in plan["deliverables"]:
        for dep in d["depends_on"]:
            if dep not in seen_ids:
                raise ValueError(f"deliverable {d['id']} depends on unknown id {dep}")
    if not isinstance(plan.get("research_questions"), list):
        plan["research_questions"] = []
    for i, r in enumerate(plan["research_questions"]):
        r.setdefault("id", f"R{i + 1}")
    plan.setdefault("gaps", [])
    return plan


def order_deliverables(plan: dict) -> list[dict]:
    """Topological order; raises ValueError on dependency cycles."""
    items = {d["id"]: d for d in plan["deliverables"]}
    ordered: list[dict] = []
    state: dict[str, int] = {}  # 0 unvisited, 1 visiting, 2 done

    def visit(did: str) -> None:
        if state.get(did) == 2:
            return
        if state.get(did) == 1:
            raise ValueError(f"dependency cycle involving {did}")
        state[did] = 1
        for dep in items[did]["depends_on"]:
            visit(dep)
        state[did] = 2
        ordered.append(items[did])

    for did in items:
        visit(did)
    return ordered


def render_plan_markdown(plan: dict) -> str:
    lines = [f"# Engagement plan — {plan.get('engagement', 'Untitled')}", ""]
    lines += [plan.get("summary", ""), ""]
    if plan.get("client_context"):
        lines += [f"**Client context:** {plan['client_context']}", ""]
    lines += ["## Deliverables", "",
              "| # | Deliverable | Type | Depends on | Scope basis |",
              "|---|---|---|---|---|"]
    for d in plan["deliverables"]:
        deps = ", ".join(d["depends_on"]) or "—"
        lines.append(f"| {d['id']} | {d['title']} | {d['kind']} | {deps} | {d.get('scope_basis', '—')} |")
    lines += ["", f"**{len(plan['deliverables'])} artifacts**", ""]
    if plan["research_questions"]:
        lines += ["## Research questions", ""]
        for r in plan["research_questions"]:
            lines.append(f"- **{r['id']}** — {r.get('topic', '')}: {r.get('questions', '')}")
        lines.append("")
    if plan["gaps"]:
        lines += ["## Gaps — material not supplied", ""]
        for g in plan["gaps"]:
            lines.append(f"- ⚠ {g}")
        lines += ["", "_Builders will use marked `[AUTHORITY-SPECIFIC — INSERT: …]` "
                  "placeholders for these — never invented client content._"]
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# The pipeline.
# ----------------------------------------------------------------------------

async def run_scope_pipeline(
    *,
    title: str,
    notes: str = "",
    repo_root: Path = REPO_ROOT,
    auto_approve: bool = False,
    budget_usd: float | None = None,
) -> ScopeResult:
    from cli.interactive import RunSpec
    from cli.sources import attach_sources, discover_dropzone

    slug = slugify(title) or "scope-engagement"
    base = repo_root / "outputs" / "scope" / slug
    (base / "research").mkdir(parents=True, exist_ok=True)
    (base / "deliverables").mkdir(parents=True, exist_ok=True)
    scripts_dir = base / "_scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    # Keep the deliverables folder clean — only real artifacts belong there.
    for stray in (base / "deliverables").glob("*.py"):
        stray.rename(scripts_dir / stray.name)

    tally = CostTally(budget_usd=budget_usd)
    result = ScopeResult(tally=tally, slug=slug)
    agents = {a.name: a for a in load_all_agents()}

    # Attach scope documents from the drop zone (or reuse ones already
    # attached to this engagement on a previous, interrupted attempt).
    dropped = discover_dropzone()
    if dropped:
        attached = attach_sources(slug, dropped, repo_root / "outputs")
        source_paths = [s.readable.relative_to(repo_root).as_posix() for s in attached]
    else:
        existing = repo_root / "outputs" / "sources" / slug
        source_paths = sorted(
            p.relative_to(repo_root).as_posix()
            for p in existing.glob("*")
            if p.is_file() and (p.suffix in (".md", ".txt") or p.name.endswith(".extracted.md"))
        ) if existing.is_dir() else []
    if not source_paths:
        raise RuntimeError(
            "No scope documents found. Drop the scope (PDF, Word, or text) into "
            "sources/ and relaunch."
        )

    spec = RunSpec(title=title, slug=slug, thesis=f"Scope engagement: {title}",
                   output_format="report", source_paths=source_paths)
    marker_spec = spec
    write_run_marker(repo_root / "outputs", marker_spec)
    # Tag the marker so resume routes back into scope mode.
    marker_path = repo_root / "outputs" / ".active-run.json"
    marker = json.loads(marker_path.read_text())
    marker["mode"] = "scope"
    marker_path.write_text(json.dumps(marker, indent=2))

    await emit("run_start", slug=slug, title=title, mode="scope",
               agents=["scope-planner", "scope-researcher", "scope-builder", "scope-qa"],
               stages=["Plan", "Research", "Build", "Package"])

    src_list = "\n".join(f"- `{p}`" for p in source_paths)

    # ─── Stage 1: Plan ───
    await emit("stage_start", stage=1, label="Reading the scope & planning deliverables")
    console.rule("[bold]Scope — planning[/bold]")
    plan_path = base / "plan.json"
    plan: dict | None = None
    planner_note = f"\n\nOperator notes for this engagement:\n{notes}" if notes.strip() else ""

    for attempt in range(3):
        if plan_path.is_file():
            try:
                plan = parse_plan(plan_path.read_text(encoding="utf-8"))
                break
            except ValueError as e:
                plan_path.unlink()
                planner_note += (
                    f"\n\nYour previous plan.json was invalid and has been deleted. "
                    f"The error: {e}. Produce corrected, valid JSON."
                )
        await _run_agent(
            agent=agents["scope-planner"],
            user_prompt=(
                "Read the client scope document(s) and any supporting material:\n"
                f"{src_list}\n\n"
                f"Write the engagement plan as JSON to: `{plan_path.relative_to(repo_root).as_posix()}`"
                f"{planner_note}"
            ),
            model=_model("synthesis"),
            cwd=repo_root,
            step_label="scope/plan",
            tally=tally,
            output_path=plan_path,
        )
    if plan is None:
        plan = parse_plan(plan_path.read_text(encoding="utf-8"))

    # Plan checkpoint.
    while not auto_approve:
        decision = await request_checkpoint("scope-plan", {
            "title": "Engagement plan — approve before production",
            "subtitle": f"{len(plan['deliverables'])} artifacts. Nothing below has been built or billed yet.",
            "documents": [{"name": "The plan", "content": render_plan_markdown(plan)}],
            "actions": ["continue", "redo", "abort"],
        }) or {"action": "abort"}
        action = decision.get("action")
        if action == "continue":
            break
        if action == "redo":
            plan_path.unlink(missing_ok=True)
            note = str(decision.get("notes", "")).strip()
            await _run_agent(
                agent=agents["scope-planner"],
                user_prompt=(
                    "Read the client scope document(s) and any supporting material:\n"
                    f"{src_list}\n\n"
                    f"Write the engagement plan as JSON to: `{plan_path.relative_to(repo_root).as_posix()}`"
                    f"{planner_note}\n\nThe operator reviewed your previous plan and asked for "
                    f"this redo with the following notes — address them directly:\n{note}"
                ),
                model=_model("synthesis"),
                cwd=repo_root,
                step_label="scope/plan-redo",
                tally=tally,
                output_path=plan_path,
            )
            plan = parse_plan(plan_path.read_text(encoding="utf-8"))
            continue
        console.print("[yellow]Stopped at plan review.[/yellow]")
        return result

    (base / "plan.md").write_text(render_plan_markdown(plan), encoding="utf-8")

    # ─── Stage 2: Research ───
    await emit("stage_start", stage=2, label=f"Researching — {len(plan['research_questions'])} questions in parallel")
    console.rule("[bold]Scope — research[/bold]")
    sem = asyncio.Semaphore(4)
    brief_paths: list[Path] = []

    async def _research(rq: dict) -> None:
        out = base / "research" / f"{rq['id']}-brief.md"
        brief_paths.append(out)
        async with sem:
            await _run_agent(
                agent=agents["scope-researcher"],
                user_prompt=(
                    f"Engagement: {plan.get('engagement', title)}\n"
                    f"Context: {plan.get('summary', '')}\n\n"
                    f"Your assigned research question ({rq['id']}): {rq.get('topic', '')}\n"
                    f"{rq.get('questions', '')}\n\n"
                    f"The scope documents, for context:\n{src_list}\n\n"
                    f"Write your brief to: `{out.relative_to(repo_root).as_posix()}`"
                ),
                model=_model("research"),
                cwd=repo_root,
                step_label=f"scope/research-{rq['id']}",
                tally=tally,
                output_path=out,
            )

    if plan["research_questions"]:
        await asyncio.gather(*(_research(rq) for rq in plan["research_questions"]))

    briefs_list = "\n".join(
        f"- `{p.relative_to(repo_root).as_posix()}`" for p in brief_paths
    ) or "(none commissioned)"
    gaps_text = "\n".join(f"- {g}" for g in plan.get("gaps", [])) or "(none identified)"

    # ─── Stage 3: Build ───
    ordered = order_deliverables(plan)
    await emit("stage_start", stage=3, label=f"Building {len(ordered)} deliverables")
    console.rule(f"[bold]Scope — building {len(ordered)} deliverables[/bold]")
    built: dict[str, Path] = {}
    build_sem = asyncio.Semaphore(2)
    done_ids: set[str] = set()

    async def _build(d: dict) -> None:
        out = base / "deliverables" / d["filename"]
        deps_list = "\n".join(
            f"- {dep}: `{built[dep].relative_to(repo_root).as_posix()}`"
            for dep in d["depends_on"] if dep in built
        ) or "(none)"
        async with build_sem:
            await _run_agent(
                agent=agents["scope-builder"],
                user_prompt=(
                    f"Engagement: {plan.get('engagement', title)}\n"
                    f"Client context: {plan.get('client_context', '')}\n\n"
                    f"YOUR ASSIGNED DELIVERABLE — {d['id']}: {d['title']} ({d['kind']})\n"
                    f"Scope basis: {d.get('scope_basis', '')}\n\n"
                    f"Build instructions:\n{d['instructions']}\n\n"
                    f"Scope documents:\n{src_list}\n\n"
                    f"Research briefs:\n{briefs_list}\n\n"
                    f"Completed dependencies (binding — align with them):\n{deps_list}\n\n"
                    f"Known gaps (use marked placeholders, never invent):\n{gaps_text}\n\n"
                    f"Write any build scripts into: "
                    f"`{scripts_dir.relative_to(repo_root).as_posix()}/` "
                    f"(never into the deliverables folder).\n"
                    f"Remember: do NOT open .docx/.pptx dependencies with Read — "
                    f"extract their headings/slide titles with a short script instead, "
                    f"and keep every command's output under ~150 lines.\n\n"
                    f"Save the finished {d['kind']} to exactly: "
                    f"`{out.relative_to(repo_root).as_posix()}`"
                ),
                model=_model("editor"),
                cwd=repo_root,
                step_label=f"scope/build-{d['id']}",
                tally=tally,
                output_path=out,
            )
        built[d["id"]] = out
        done_ids.add(d["id"])
        await emit("deliverable_done", id=d["id"], title=d["title"],
                   file=d["filename"], done=len(done_ids), total=len(ordered))

    # Build in dependency waves: everything whose deps are satisfied runs
    # concurrently (bounded by the semaphore); the next wave follows.
    remaining = list(ordered)
    while remaining:
        wave = [d for d in remaining if all(dep in built for dep in d["depends_on"])]
        if not wave:
            raise RuntimeError("dependency deadlock in plan — check depends_on")
        await asyncio.gather(*(_build(d) for d in wave))
        remaining = [d for d in remaining if d["id"] not in built]

    # ─── QA + final checkpoint ───
    qa_path = base / "qa-report.md"
    files_list = "\n".join(
        f"- {d['id']} ({d['title']}): `{built[d['id']].relative_to(repo_root).as_posix()}`"
        for d in ordered
    )
    await _run_agent(
        agent=agents["scope-qa"],
        user_prompt=(
            f"Engagement: {plan.get('engagement', title)}\n\n"
            f"Original scope documents:\n{src_list}\n\n"
            f"The engagement plan: `{(base / 'plan.md').relative_to(repo_root).as_posix()}`\n\n"
            f"Produced deliverables:\n{files_list}\n\n"
            f"Write your acceptance review to: `{qa_path.relative_to(repo_root).as_posix()}`"
        ),
        model=_model("factcheck"),
        cwd=repo_root,
        step_label="scope/qa",
        tally=tally,
        output_path=qa_path,
    )

    if not auto_approve:
        decision = await request_checkpoint("scope-final", {
            "title": "Acceptance review — final checkpoint",
            "subtitle": "The QA agent's deliverable-by-deliverable audit against the scope.",
            "documents": [
                {"name": "QA report", "content": qa_path.read_text(encoding="utf-8", errors="ignore")},
                {"name": "The plan", "content": render_plan_markdown(plan)},
            ],
            "actions": ["approve", "abort"],
        }) or {"action": "abort"}
        if decision.get("action") != "approve":
            console.print("[yellow]Stopped at final review. Deliverables remain in outputs/scope/.[/yellow]")
            return result

    # ─── Stage 4: Package ───
    await emit("stage_start", stage=4, label="Packaging & archiving")
    console.rule("[bold]Scope — packaging[/bold]")

    package_dir = REPORTS_DIR / f"scope-{slug}"
    package_dir.mkdir(parents=True, exist_ok=True)
    for d in ordered:
        shutil.copy2(built[d["id"]], package_dir / d["filename"])
    shutil.copy2(qa_path, package_dir / "qa-report.md")
    (package_dir / "MANIFEST.md").write_text(
        render_plan_markdown(plan) + "\n\n---\n\nProduced by the Transform Airports "
        "AI Council. AI-generated engagement materials — subject-matter-expert "
        "review required before client delivery.\n", encoding="utf-8")

    zip_path = REPORTS_DIR / f"{slug}-deliverables.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(package_dir.iterdir()):
            zf.write(f, f.name)

    # Archive the working tree.
    archive_dir = repo_root / "runs" / f"{date.today().isoformat()}-scope-{slug}"
    if not archive_dir.exists():
        shutil.copytree(base, archive_dir)
        src_dir = repo_root / "outputs" / "sources" / slug
        if src_dir.is_dir():
            shutil.copytree(src_dir, archive_dir / "sources")
        (archive_dir / "retrospective.md").write_text(
            f"# Scope engagement — {title}\n\nArchived {date.today().isoformat()}. "
            f"{len(ordered)} deliverables, total cost ${tally.total:.2f}.\n",
            encoding="utf-8")
    from cli.archive import _clear_outputs
    _clear_outputs(repo_root / "outputs")

    result.archive_path = archive_dir
    result.package_dir = package_dir
    result.zip_path = zip_path
    result.completed = True
    await emit("run_complete", slug=slug, title=title, mode="scope",
               total=tally.total,
               deliverables=[{"id": d["id"], "title": d["title"], "file": d["filename"]}
                             for d in ordered],
               zip=f"/download/{zip_path.name}")
    _notify_done("AI Council", f"Scope engagement complete: {title} (${tally.total:.2f})")
    return result
