"""Four-stage Council orchestrator built on the Claude Agent SDK.

Stage 1: parallel research briefs (Sonnet, the selected research agents).
Stage 2: Strategist v1 → Red Team v1 → Strategist v2 → Red Team v2 → Strategist v3 (Opus).
Stage 3: Editor → Fact-checker (Opus).
Stage 4: handed off to docx_builder.py; archive done in archive.py.

Human checkpoints between Stage 2/3 and Stage 3/4 are in checkpoints.py.
"""
from __future__ import annotations

import asyncio
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import questionary
from rich.console import Console

from cli.agents import Agent, load_all_agents
from cli.interactive import RunSpec

console = Console()

SONNET = "claude-sonnet-4-6"
OPUS = "claude-opus-4-8"


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
        "fact-checker": (
            "Read `outputs/stage3/edited-draft.md` and every brief in `outputs/stage1/`. "
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
        tasks.append(
            _run_agent(
                agent=agent,
                user_prompt=prompt,
                model=SONNET,
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
        ("strategist-v1", strategist),
        ("red-team-v1", red_team),
        ("strategist-v2", strategist),
        ("red-team-v2", red_team),
        ("strategist-v3", strategist),
    ]
    started = False
    for step_id, agent in sequence:
        if not started and step_id != start_from:
            continue
        started = True
        await _run_agent(
            agent=agent,
            user_prompt=prompts[step_id],
            model=OPUS,
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
    fact_checker = by_name["fact-checker"]
    prompts = _stage3_prompts(run_file)
    await _run_agent(
        agent=editor,
        user_prompt=prompts["editor"],
        model=OPUS,
        cwd=outputs_dir.parent,
        step_label="stage3/editor",
        tally=tally,
        output_path=outputs_dir / "stage3" / "edited-draft.md",
    )
    await _run_agent(
        agent=fact_checker,
        user_prompt=prompts["fact-checker"],
        model=OPUS,
        cwd=outputs_dir.parent,
        step_label="stage3/fact-checker",
        tally=tally,
        output_path=outputs_dir / "stage3" / "final-draft.md",
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

    console.rule("[bold]Archive[/bold]")
    archive_path = archive_run(repo_root=repo_root, slug=spec.slug, tally=tally)
    console.print(f"[green]Archived to:[/green] {archive_path}")
    return tally
