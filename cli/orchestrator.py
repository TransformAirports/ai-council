"""Four-stage Council orchestrator built on the Claude Agent SDK.

Stage 1: parallel research briefs (Opus 4.8, the selected research agents;
         the Deep Research agent routes to OpenAI instead).
Stage 2: Strategist v1 → Red Team v1 → Strategist v2 → Red Team v2 → Strategist v3
         (Strategist on Opus 4.8; Red Team on Fable 5).
Stage 3: Editor (Fable 5) → Humanizer (Fable 5) → Fact-checker (Opus 4.8).
         The Fact-checker runs LAST so verification covers the humanized text.
Stage 4: handed off to docx_builder.py; optional companion PowerPoint
         (presentation-designer on Fable 5); archive done in archive.py.

Human checkpoints between Stage 2/3 and Stage 3/4 are in checkpoints.py.
"""
from __future__ import annotations

import asyncio
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import questionary
from rich.console import Console

from cli.agents import Agent, load_all_agents
from cli.interactive import RunSpec

console = Console()

# Role-based model assignments. Research and synthesis run on Opus 4.8;
# critique and editorial passes run on Fable 5 (stronger critique/synthesis/
# editorial performance). The Fact-checker stays on Opus 4.8 deliberately —
# verification benefits from a different model family than the one that wrote
# and polished the text it is checking.
RESEARCH_MODEL = "claude-opus-4-8"
SYNTHESIS_MODEL = "claude-opus-4-8"      # Strategist
CRITIQUE_MODEL = "claude-fable-5"        # Red Team
EDITOR_MODEL = "claude-fable-5"          # Editor
HUMANIZER_MODEL = "claude-fable-5"       # Humanizer
FACTCHECK_MODEL = "claude-opus-4-8"      # Fact-checker
PRESENTATION_MODEL = "claude-fable-5"    # Companion PowerPoint

# Default model for the OpenAI-hosted Deep Research agent. An agent file can
# override this via a `model:` frontmatter key. NOTE: verify this model ID is
# enabled on your OpenAI account before seating the agent.
OPENAI_DEEP_RESEARCH_MODEL = "gpt-5.5-pro-deep-research"


@dataclass
class CostTally:
    by_step: dict[str, float] = field(default_factory=dict)

    def add(self, step: str, cost: float) -> None:
        self.by_step[step] = self.by_step.get(step, 0.0) + cost

    @property
    def total(self) -> float:
        return sum(self.by_step.values())


def _has_content(path: Path, min_bytes: int = 200) -> bool:
    try:
        return path.is_file() and path.stat().st_size >= min_bytes
    except OSError:
        return False


async def _run_agent(
    *,
    agent: Agent,
    user_prompt: str,
    model: str,
    cwd: Path,
    step_label: str,
    tally: CostTally,
    output_path: Path | None = None,
    max_turns: int = 80,
) -> None:
    """Invoke one agent end-to-end via the Claude Agent SDK.

    If `output_path` is set and already exists with material content, the
    invocation is skipped — supports `--resume` after a partial run.

    After completion, if `output_path` is set but the file is missing or empty,
    raises a clear error. Otherwise an exhausted-turn-budget run can look like
    success in the trace ("done, $X, N turns") even though no file was written.

    `max_turns` is generous by default (80) because synthesis agents have to
    read many briefs before writing. Stage 1 doesn't strictly need this much
    headroom; Stage 2 and Stage 3 do.
    """
    if output_path is not None and _has_content(output_path):
        console.print(
            f"[dim]↷ {step_label} skipped — {output_path.relative_to(cwd)} already exists[/dim]"
        )
        return

    if agent.provider == "openai":
        await _run_openai_deep_research(
            agent=agent,
            user_prompt=user_prompt,
            step_label=step_label,
            tally=tally,
            output_path=output_path,
        )
        if output_path is not None and not _has_content(output_path):
            raise RuntimeError(
                f"{step_label} (OpenAI) finished without producing {output_path}."
            )
        return

    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ResultMessage,
        TextBlock,
        ToolUseBlock,
        query,
    )

    options = ClaudeAgentOptions(
        system_prompt=agent.system_prompt,
        allowed_tools=list(agent.tools) if agent.tools else None,
        permission_mode="bypassPermissions",
        model=model,
        cwd=str(cwd),
        max_turns=max_turns,
    )

    console.print(f"[cyan]▶ {step_label}[/cyan] ({agent.display_name}, {model})")

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
        elif isinstance(msg, ResultMessage):
            cost = getattr(msg, "total_cost_usd", None) or 0.0
            tally.add(step_label, cost)
            console.print(
                f"  [green]✓ {step_label} done[/green] "
                f"[dim](${cost:.2f}, {getattr(msg, 'num_turns', '?')} turns)[/dim]"
            )

    # Catch the "agent completed its turn budget without writing" silent failure.
    # The SDK reports cost and turn count even when Claude Code marks the result
    # is_error=true with subtype=success (the signature of a max_turns exhaustion).
    if output_path is not None and not _has_content(output_path):
        raise RuntimeError(
            f"{step_label} finished without writing {output_path.relative_to(cwd)}. "
            f"This usually means the agent exhausted its turn budget on reads "
            f"before getting to the Write step. Try raising max_turns or "
            f"reducing how many files the agent has to read."
        )


async def _run_openai_deep_research(
    *,
    agent: Agent,
    user_prompt: str,
    step_label: str,
    tally: CostTally,
    output_path: Path | None,
) -> None:
    """Run a research brief through an OpenAI deep-research model.

    OpenAI agents cannot use our file tools, so the prompt must carry all
    context inline and we write the response to `output_path` ourselves.
    Requires OPENAI_API_KEY in the environment and the `openai` package.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            f"{step_label}: the Deep Research agent needs OPENAI_API_KEY set. "
            "Export it or deselect the agent."
        )
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError(
            f"{step_label}: the `openai` package is not installed. "
            "Run `pip install -e .` to pick up the new dependency."
        ) from e

    model = agent.model_override or OPENAI_DEEP_RESEARCH_MODEL
    console.print(f"[cyan]▶ {step_label}[/cyan] ({agent.display_name}, {model} via OpenAI)")

    def _call() -> str:
        client = OpenAI(timeout=3600.0)
        resp = client.responses.create(
            model=model,
            instructions=agent.system_prompt,
            input=user_prompt,
            tools=[{"type": "web_search_preview"}],
        )
        return resp.output_text

    text = await asyncio.to_thread(_call)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    # OpenAI usage is billed on the OpenAI account; not added to the Claude tally.
    tally.add(step_label, 0.0)
    console.print(
        f"  [green]✓ {step_label} done[/green] [dim](billed to OpenAI account, "
        f"not in Claude tally)[/dim]"
    )


def _stage1_prompt(agent: Agent, run_file: Path, output_path: Path, override: str) -> str:
    parts = [
        f"You are producing an independent research brief for the Council run defined in `{run_file}`.",
        f"Read that file first for the thesis, audience, tone, and any per-agent override.",
        "",
        f"Write your brief to: `{output_path}`",
        "",
        "Critical rule: do NOT read any other agent's output in `outputs/stage1/`. "
        "Independent evidence is a design feature — Stage 2 needs your distinct lens.",
    ]
    if override:
        parts += [
            "",
            f"This run's override for your agent: {override}",
        ]
    return "\n".join(parts)


def _stage2_prompts(run_file: Path) -> dict[str, str]:
    return {
        "strategist-v1": (
            "Read the run prompt at "
            f"`{run_file}` and all eight (or fewer) briefs in `outputs/stage1/`.\n\n"
            "Produce the first argumentative draft of the Council's main piece.\n"
            "Write to: `outputs/stage2/strategist-draft-v1.md`"
        ),
        "red-team-v1": (
            "Read the run prompt at "
            f"`{run_file}` and the Strategist's draft at `outputs/stage2/strategist-draft-v1.md`.\n\n"
            "Attack the draft: weak claims, logical gaps, unsupported assertions, places the argument is vulnerable. "
            "Number every critique item so the Strategist can address each one.\n"
            "Write to: `outputs/stage2/red-team-critique-v1.md`"
        ),
        "strategist-v2": (
            "Read `outputs/stage2/strategist-draft-v1.md` and `outputs/stage2/red-team-critique-v1.md`. "
            f"Read the run prompt at `{run_file}` for ongoing framing.\n\n"
            "Revise the draft to address every item in the v1 critique. Where you push back rather than incorporate, "
            "say so explicitly in a brief revision-notes section at the top.\n"
            "Write the revised draft to: `outputs/stage2/strategist-draft-v2.md`"
        ),
        "red-team-v2": (
            "Read `outputs/stage2/strategist-draft-v2.md` and your previous critique at "
            "`outputs/stage2/red-team-critique-v1.md`.\n\n"
            "Attack again. Focus on what the v2 revision did NOT fix, and on new weaknesses the revision introduced.\n"
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


def _stage3_prompts(run_file: Path) -> dict[str, str]:
    return {
        "editor": (
            "Read the run prompt at "
            f"`{run_file}` and `outputs/stage2/strategist-draft-v3.md`.\n\n"
            "Cut 15-25% of word count. Kill buzzwords (see CLAUDE.md). Flag any hedge or "
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
            "Read `outputs/stage3/humanized-draft.md` and every brief in `outputs/stage1/`. "
            f"Also read the run prompt at `{run_file}`.\n\n"
            "Verify every numerical claim, attributed quote, and specific assertion against the Stage 1 briefs. "
            "Tag claims you cannot verify with `[UNVERIFIED — HUMAN REVIEW]` in the final draft. You have veto "
            "power over any claim that cannot be sourced.\n"
            "Write the fact-check report to: `outputs/stage3/fact-check-report.md`\n"
            "Write the final draft to: `outputs/stage3/final-draft.md`"
        ),
    }


STAGE_SUBDIRS: tuple[str, ...] = ("stage1", "stage2", "stage3", "stage4")


def _existing_artifacts(outputs_dir: Path) -> list[Path]:
    """Return any pre-existing files under outputs/stage*/ that would conflict."""
    found: list[Path] = []
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

    for sub in STAGE_SUBDIRS:
        (outputs_dir / sub).mkdir(parents=True, exist_ok=True)
    (outputs_dir / ".gitkeep").touch(exist_ok=True)


async def run_stage1(
    spec: RunSpec,
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
) -> None:
    by_name = {a.name: a for a in all_agents}
    tasks = []
    for name in spec.selected_research_agents:
        agent = by_name[name]
        out = outputs_dir / "stage1" / f"{name}-brief.md"
        override = spec.agent_overrides.get(name, "")
        prompt = _stage1_prompt(agent, run_file, out, override)
        if agent.provider == "openai":
            # OpenAI agents have no file tools — inline the run prompt.
            prompt += (
                "\n\n--- RUN PROMPT FILE (inlined; you cannot read files) ---\n"
                + run_file.read_text(encoding="utf-8", errors="ignore")
            )
        tasks.append(
            _run_agent(
                agent=agent,
                user_prompt=prompt,
                model=RESEARCH_MODEL,
                cwd=outputs_dir.parent,
                step_label=f"stage1/{name}",
                tally=tally,
                output_path=out,
            )
        )
    await asyncio.gather(*tasks)
    missing = [
        name
        for name in spec.selected_research_agents
        if not (outputs_dir / "stage1" / f"{name}-brief.md").is_file()
    ]
    if missing:
        raise RuntimeError(f"Stage 1 agents did not write their briefs: {missing}")


async def run_stage2(
    spec: RunSpec,
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
    start_from: str = "strategist-v1",
) -> None:
    by_name = {a.name: a for a in all_agents}
    strategist = by_name["strategist"]
    red_team = by_name["red-team"]
    prompts = _stage2_prompts(run_file)
    output_paths = {
        "strategist-v1": outputs_dir / "stage2" / "strategist-draft-v1.md",
        "red-team-v1": outputs_dir / "stage2" / "red-team-critique-v1.md",
        "strategist-v2": outputs_dir / "stage2" / "strategist-draft-v2.md",
        "red-team-v2": outputs_dir / "stage2" / "red-team-critique-v2.md",
        "strategist-v3": outputs_dir / "stage2" / "strategist-draft-v3.md",
    }
    sequence = [
        ("strategist-v1", strategist, SYNTHESIS_MODEL),
        ("red-team-v1", red_team, CRITIQUE_MODEL),
        ("strategist-v2", strategist, SYNTHESIS_MODEL),
        ("red-team-v2", red_team, CRITIQUE_MODEL),
        ("strategist-v3", strategist, SYNTHESIS_MODEL),
    ]
    started = False
    for step_id, agent, model in sequence:
        if not started and step_id != start_from:
            continue
        started = True
        await _run_agent(
            agent=agent,
            user_prompt=prompts[step_id],
            model=model,
            cwd=outputs_dir.parent,
            step_label=f"stage2/{step_id}",
            tally=tally,
            output_path=output_paths[step_id],
        )


async def run_stage3(
    run_file: Path,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
) -> None:
    by_name = {a.name: a for a in all_agents}
    editor = by_name["editor"]
    humanizer = by_name["humanizer"]
    fact_checker = by_name["fact-checker"]
    prompts = _stage3_prompts(run_file)
    await _run_agent(
        agent=editor,
        user_prompt=prompts["editor"],
        model=EDITOR_MODEL,
        cwd=outputs_dir.parent,
        step_label="stage3/editor",
        tally=tally,
        output_path=outputs_dir / "stage3" / "edited-draft.md",
    )
    await _run_agent(
        agent=humanizer,
        user_prompt=prompts["humanizer"],
        model=HUMANIZER_MODEL,
        cwd=outputs_dir.parent,
        step_label="stage3/humanizer",
        tally=tally,
        output_path=outputs_dir / "stage3" / "humanized-draft.md",
    )
    await _run_agent(
        agent=fact_checker,
        user_prompt=prompts["fact-checker"],
        model=FACTCHECK_MODEL,
        cwd=outputs_dir.parent,
        step_label="stage3/fact-checker",
        tally=tally,
        output_path=outputs_dir / "stage3" / "final-draft.md",
    )


async def run_presentation(
    spec: RunSpec,
    outputs_dir: Path,
    all_agents: list[Agent],
    tally: CostTally,
) -> None:
    """Generate the companion executive PowerPoint via the presentation agent."""
    by_name = {a.name: a for a in all_agents}
    designer = by_name["presentation-designer"]
    out_path = outputs_dir / "stage4" / f"{spec.slug}.pptx"
    prompt = (
        f"Build the companion executive presentation for the report titled "
        f"\"{spec.title}\".\n\n"
        f"Source material (read all three):\n"
        f"- Final draft: `outputs/stage3/final-draft.md`\n"
        f"- Fact-check report: `outputs/stage3/fact-check-report.md`\n"
        f"- Run prompt: `prompts/runs/{spec.slug}.md`\n\n"
        f"Save the finished deck to: `{out_path}`\n"
        f"The repo's Python interpreter with python-pptx installed is at "
        f"`.venv/bin/python` — use it for your build script, and validate the "
        f"deck opens cleanly before finishing."
    )
    await _run_agent(
        agent=designer,
        user_prompt=prompt,
        model=PRESENTATION_MODEL,
        cwd=outputs_dir.parent,
        step_label="stage4/presentation",
        tally=tally,
        output_path=out_path,
    )


async def run_pipeline(
    *,
    spec: RunSpec,
    run_file: Path,
    repo_root: Path,
    auto_approve: bool,
    resume: bool = False,
) -> CostTally:
    from cli.checkpoints import checkpoint_after_stage2, checkpoint_after_stage3
    from cli.docx_builder import build_documents
    from cli.archive import archive_run

    outputs_dir = repo_root / "outputs"
    await prepare_outputs(outputs_dir, auto_approve=auto_approve, resume=resume)
    all_agents = load_all_agents()
    tally = CostTally()

    console.rule("[bold]Stage 1 — parallel research briefs[/bold]")
    await run_stage1(spec, run_file, outputs_dir, all_agents, tally)

    console.rule("[bold]Stage 2 — synthesis & adversarial revision[/bold]")
    await run_stage2(spec, run_file, outputs_dir, all_agents, tally)

    while True:
        result = await checkpoint_after_stage2(outputs_dir, auto_approve=auto_approve)
        if result.approved:
            break
        if result.redo_from == "strategist-v3":
            v3_path = outputs_dir / "stage2" / "strategist-draft-v3.md"
            if v3_path.exists():
                v3_path.unlink()
            await run_stage2(
                spec, run_file, outputs_dir, all_agents, tally, start_from="strategist-v3"
            )
            continue
        console.print("[yellow]Stopping at Stage 2.[/yellow]")
        return tally

    console.rule("[bold]Stage 3 — edit & fact-check[/bold]")
    await run_stage3(run_file, outputs_dir, all_agents, tally)

    result = await checkpoint_after_stage3(outputs_dir, auto_approve=auto_approve)
    if not result.approved:
        console.print("[yellow]Stopping at Stage 3. No Word docs generated.[/yellow]")
        return tally

    console.rule("[bold]Stage 4 — Word documents[/bold]")
    build_documents(
        slug=spec.slug,
        title=spec.title,
        final_draft=outputs_dir / "stage3" / "final-draft.md",
        methodology=repo_root / "docs" / "methodology.md",
        out_dir=outputs_dir / "stage4",
    )

    if getattr(spec, "want_pptx", False):
        console.rule("[bold]Companion PowerPoint[/bold]")
        await run_presentation(spec, outputs_dir, load_all_agents(), tally)

    console.rule("[bold]Archive[/bold]")
    archive_path = archive_run(repo_root=repo_root, slug=spec.slug, tally=tally)
    console.print(f"[green]Archived to:[/green] {archive_path}")
    return tally


# ----------------------------------------------------------------------------
# Revision pipeline — produce a revised version of an existing report from
# reader feedback, reusing the original Stage 1 research briefs.
# ----------------------------------------------------------------------------

def _revision_prompts(base_rel: str, src_draft_rel: str, briefs_rel: str) -> dict[str, str]:
    return {
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
            f"Write the edited draft to: `{base_rel}/edited-draft.md`"
        ),
        "humanizer": (
            f"Read `{base_rel}/edited-draft.md`. Refine tone, readability, and overall "
            "writing quality per your charter. Do not add, remove, or alter any factual "
            "claim, number, citation, or bracketed tag — the Fact-checker verifies your "
            "output next.\n"
            f"Write the refined draft to: `{base_rel}/humanized-draft.md`"
        ),
        "fact-checker": (
            f"Read `{base_rel}/humanized-draft.md` and the original briefs in "
            f"`{briefs_rel}/`. Verify every numerical and attributed claim against the "
            "briefs. Tag anything you cannot verify with `[UNVERIFIED — HUMAN REVIEW]`. "
            "You have veto power over unsourced claims.\n"
            f"Write the final revised draft to: `{base_rel}/final-draft.md`"
        ),
    }


async def run_revision_pipeline(
    *,
    request,  # cli.revise.RevisionRequest
    repo_root: Path,
    auto_approve: bool,
) -> tuple[Path | None, CostTally]:
    """Run the focused revision loop and build the polished revised report."""
    import questionary as _q

    from cli.checkpoints import _show_file_excerpt
    from cli.publish import ReportSource, build_polished_report

    source = request.source
    version = request.version
    archive_dir = source.archive_dir

    from cli.revise import latest_draft_path

    base = archive_dir / "revisions" / f"v{version}"
    base.mkdir(parents=True, exist_ok=True)
    (base / "feedback.md").write_text(
        f"# Reader feedback — Revised v{version}\n\n{request.feedback}\n",
        encoding="utf-8",
    )

    src_draft = latest_draft_path(archive_dir)
    briefs_dir = archive_dir / "stage1"
    base_rel = base.relative_to(repo_root).as_posix()
    src_draft_rel = src_draft.relative_to(repo_root).as_posix()
    briefs_rel = briefs_dir.relative_to(repo_root).as_posix()

    all_agents = load_all_agents()
    by_name = {a.name: a for a in all_agents}
    tally = CostTally()
    prompts = _revision_prompts(base_rel, src_draft_rel, briefs_rel)

    console.rule(f"[bold]Revising '{source.slug}' → v{version}[/bold]")
    console.print(f"[dim]Revising from: {src_draft_rel}[/dim]")

    steps = [
        ("strategist-a", by_name["strategist"], base / "revised-draft-a.md", SYNTHESIS_MODEL),
        ("red-team", by_name["red-team"], base / "red-team-critique.md", CRITIQUE_MODEL),
        ("strategist-b", by_name["strategist"], base / "revised-draft-b.md", SYNTHESIS_MODEL),
        ("editor", by_name["editor"], base / "edited-draft.md", EDITOR_MODEL),
        ("humanizer", by_name["humanizer"], base / "humanized-draft.md", HUMANIZER_MODEL),
        ("fact-checker", by_name["fact-checker"], base / "final-draft.md", FACTCHECK_MODEL),
    ]
    for step_id, agent, out_path, model in steps:
        await _run_agent(
            agent=agent,
            user_prompt=prompts[step_id],
            model=model,
            cwd=repo_root,
            step_label=f"revision-v{version}/{step_id}",
            tally=tally,
            output_path=out_path,
        )

    final_draft = base / "final-draft.md"
    if not auto_approve:
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

    # Build the polished docx, stamped with the revision label.
    revised_source = ReportSource(
        slug=source.slug,
        archive_dir=archive_dir,
        stage4_docx=source.stage4_docx,
        final_md=final_draft,
        run_file=source.run_file,
    )
    out_path = build_polished_report(
        revised_source,
        by_name,
        revision_label=f"Revised — Version {version}",
        out_name=f"{source.slug}-revised-v{version}.docx",
    )
    console.print(f"[green]Revised report built:[/green] {out_path.relative_to(repo_root)}")
    return out_path, tally
