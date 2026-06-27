"""Four-stage Council orchestrator built on the Claude Agent SDK.

Stage 1: parallel research briefs (Opus 4.8, the selected research agents;
         the Deep Research agent routes to OpenAI instead).
Stage 2: Strategist v1 → Red Team v1 → Strategist v2 → Red Team v2 → Strategist v3
         (all on Opus 4.8).
Stage 3: Editor → Humanizer → Fact-checker (all on Opus 4.8).
         The Fact-checker runs LAST so verification covers the humanized text.
Stage 4: handed off to docx_builder.py; optional companion PowerPoint
         (presentation-designer on Opus 4.8); archive done in archive.py.

Human checkpoints between Stage 2/3 and Stage 3/4 are in checkpoints.py.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import questionary
from rich.console import Console

from cli.agents import Agent, load_all_agents
from cli.config import get_config
from cli.events import emit
from cli.interactive import RunSpec

console = Console()

# Model assignments live in council.toml (see cli/config.py for defaults and
# the Settings menu for editing). Role keys: research, synthesis (Strategist),
# critique (Red Team), editor, humanizer, factcheck, presentation,
# openai_deep_research. The Fact-checker defaults to a different model family
# than the ones that write and polish — verification benefits from fresh eyes.


def _model(role: str) -> str:
    return get_config().model(role)


class RunBudgetExceeded(RuntimeError):
    """Raised between steps when the run's cost ceiling has been reached."""


@dataclass
class CostTally:
    by_step: dict[str, float] = field(default_factory=dict)
    budget_usd: float | None = None  # run-level ceiling, checked between steps

    def add(self, step: str, cost: float) -> None:
        self.by_step[step] = self.by_step.get(step, 0.0) + cost

    @property
    def total(self) -> float:
        return sum(self.by_step.values())

    def check_budget(self, next_step: str) -> None:
        if self.budget_usd is not None and self.total >= self.budget_usd:
            raise RunBudgetExceeded(
                f"Budget ceiling reached: ${self.total:.2f} spent of the "
                f"${self.budget_usd:.2f} limit, with '{next_step}' still pending. "
                f"Work so far is saved — relaunch and choose Resume to continue "
                f"with a higher ceiling."
            )


@dataclass
class RunResult:
    tally: CostTally
    archive_path: Path | None = None
    published_path: Path | None = None
    deck_path: Path | None = None
    completed: bool = False


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
    max_turns: int | None = None,
) -> None:
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

    if output_path is not None and _has_content(output_path):
        console.print(
            f"[dim]↷ {step_label} skipped — {output_path.relative_to(cwd)} already exists[/dim]"
        )
        return

    tally.check_budget(step_label)

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
        # Defense in depth: the SDK reads stdout as newline-delimited JSON with
        # a 1 MB default line limit. A single large tool-result (e.g. an agent
        # reading a big file) crashes the reader. Source PDFs are extracted to
        # text before agents see them, but raise the ceiling generously so an
        # incidental large read can't take down a run.
        max_buffer_size=64 * 1024 * 1024,
    )

    # Retry the spurious-success SDK race. When many subprocesses spawn in
    # parallel, some sessions fail to establish and the SDK reports it as
    # "Claude Code returned an error result: success" — usually one turn,
    # zero cost, no output. A single retry with backoff almost always wins,
    # so don't fail the whole batch over a flaky session start.
    SPURIOUS = "Claude Code returned an error result: success"
    attempts_left = 2
    last_exc: Exception | None = None
    while attempts_left > 0:
        attempts_left -= 1
        saw_result = False
        try:
            console.print(f"[cyan]▶ {step_label}[/cyan] ({agent.display_name}, {model})")
            await emit("agent_start", step=step_label, agent=agent.name,
                       display=agent.display_name, model=model)
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
                    # Spurious success: SDK reports ResultMessage but the
                    # agent did effectively no work AND wrote no file. Treat
                    # as a retryable race.
                    if (
                        attempts_left > 0
                        and turns <= 1
                        and cost == 0.0
                        and output_path is not None
                        and not _has_content(output_path)
                    ):
                        console.print(
                            f"  [yellow]↻ {step_label} returned 1 turn / $0 — "
                            f"subprocess race; retrying in 5s[/yellow]"
                        )
                        await asyncio.sleep(5)
                        last_exc = RuntimeError("spurious-success retry")
                        break
                    tally.add(step_label, cost)
                    console.print(
                        f"  [green]✓ {step_label} done[/green] "
                        f"[dim](${cost:.2f}, {turns} turns)[/dim]"
                    )
                    await emit("agent_done", step=step_label, agent=agent.name,
                               cost=cost, turns=turns, total=tally.total)
            else:
                # async-for completed cleanly without our break — done.
                break
            # We broke out for a retry; loop continues.
            continue
        except Exception as e:  # noqa: BLE001 — translate the SDK's spurious-success into a retry
            last_exc = e
            if SPURIOUS in str(e) and not saw_result and attempts_left > 0:
                console.print(
                    f"  [yellow]↻ {step_label} hit subprocess startup race "
                    f"({type(e).__name__}); retrying in 5s[/yellow]"
                )
                await asyncio.sleep(5)
                continue
            raise

    # Catch the "agent completed its turn budget without writing" silent failure.
    # The SDK reports cost and turn count even when Claude Code marks the result
    # is_error=true with subtype=success (the signature of a max_turns exhaustion).
    if output_path is not None and not _has_content(output_path):
        if last_exc and "spurious-success" not in str(last_exc):
            # The last attempt threw something other than our retry signal; re-raise.
            raise last_exc
        # A 1-turn / $0 result with no output almost always means the Claude
        # Code subprocess could not authenticate (expired `claude login` token
        # is the usual culprit). The pre-flight auth check should catch this
        # first, but if a token expires mid-run, point at the real cause.
        raise RuntimeError(
            f"{step_label} produced no output (the agent ran 0–1 turns at $0). "
            f"This is almost always a Claude authentication failure — your "
            f"`claude login` token may have expired. Run `claude login`, verify "
            f"with `claude -p \"say PONG\" --max-turns 1`, then relaunch and "
            f"choose Resume."
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

    model = agent.model_override or _model("openai_deep_research")
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
    from cli.sources import stage1_preamble, inline_for_openai

    source_paths = list(getattr(spec, "source_paths", []) or [])
    preamble = stage1_preamble(source_paths)
    by_name = {a.name: a for a in all_agents}

    # Cap concurrent Claude Code subprocesses. Spawning 10+ sessions in
    # parallel causes a real startup race: some sessions fail to authenticate
    # cleanly and the SDK reports them as spurious "error: success" results.
    # Four-wide is the sweet spot — meaningful parallelism without overloading
    # the SDK or hitting concurrent API ceilings.
    stage1_semaphore = asyncio.Semaphore(4)

    async def _bounded_run(coro):
        async with stage1_semaphore:
            return await coro

    tasks = []
    for name in spec.selected_research_agents:
        agent = by_name[name]
        out = outputs_dir / "stage1" / f"{name}-brief.md"
        override = spec.agent_overrides.get(name, "")
        prompt = _stage1_prompt(agent, run_file, out, override) + preamble
        if agent.provider == "openai":
            # OpenAI agents have no file tools — inline the run prompt and any
            # source-material text the operator attached.
            prompt += (
                "\n\n--- RUN PROMPT FILE (inlined; you cannot read files) ---\n"
                + run_file.read_text(encoding="utf-8", errors="ignore")
            )
            prompt += inline_for_openai(source_paths, repo_root=outputs_dir.parent)
        tasks.append(_bounded_run(
            _run_agent(
                agent=agent,
                user_prompt=prompt,
                model=_model("research"),
                cwd=outputs_dir.parent,
                step_label=f"stage1/{name}",
                tally=tally,
                output_path=out,
            )
        ))
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
    v3_note: str = "",
) -> None:
    by_name = {a.name: a for a in all_agents}
    strategist = by_name["strategist"]
    red_team = by_name["red-team"]
    prompts = _stage2_prompts(run_file)
    if v3_note:
        prompts["strategist-v3"] += (
            "\n\nThe human operator reviewed the previous v3 and asked for this "
            "redo with the following notes. Address them directly — they take "
            "precedence over anything they conflict with:\n"
            f"{v3_note}"
        )
    output_paths = {
        "strategist-v1": outputs_dir / "stage2" / "strategist-draft-v1.md",
        "red-team-v1": outputs_dir / "stage2" / "red-team-critique-v1.md",
        "strategist-v2": outputs_dir / "stage2" / "strategist-draft-v2.md",
        "red-team-v2": outputs_dir / "stage2" / "red-team-critique-v2.md",
        "strategist-v3": outputs_dir / "stage2" / "strategist-draft-v3.md",
    }
    sequence = [
        ("strategist-v1", strategist, _model("synthesis")),
        ("red-team-v1", red_team, _model("critique")),
        ("strategist-v2", strategist, _model("synthesis")),
        ("red-team-v2", red_team, _model("critique")),
        ("strategist-v3", strategist, _model("synthesis")),
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
        model=_model("editor"),
        cwd=outputs_dir.parent,
        step_label="stage3/editor",
        tally=tally,
        output_path=outputs_dir / "stage3" / "edited-draft.md",
    )
    await _run_agent(
        agent=humanizer,
        user_prompt=prompts["humanizer"],
        model=_model("humanizer"),
        cwd=outputs_dir.parent,
        step_label="stage3/humanizer",
        tally=tally,
        output_path=outputs_dir / "stage3" / "humanized-draft.md",
    )
    await _run_agent(
        agent=fact_checker,
        user_prompt=prompts["fact-checker"],
        model=_model("factcheck"),
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
        model=_model("presentation"),
        cwd=outputs_dir.parent,
        step_label="stage4/presentation",
        tally=tally,
        output_path=out_path,
    )


async def run_presentation_for_archive(
    *,
    archive_dir: Path,
    slug: str,
    title: str,
    repo_root: Path,
) -> Path:
    """Generate a companion deck for an already-archived run.

    The deck is written into the archive's stage4/ and copied to reports/
    for distribution. Returns the reports/ path.
    """
    from cli.publish import REPORTS_DIR

    all_agents = load_all_agents()
    by_name = {a.name: a for a in all_agents}
    designer = by_name["presentation-designer"]
    tally = CostTally()

    stage4 = archive_dir / "stage4"
    stage4.mkdir(parents=True, exist_ok=True)
    out_path = stage4 / f"{slug}.pptx"
    final_rel = (archive_dir / "stage3" / "final-draft.md").relative_to(repo_root).as_posix()
    factcheck_rel = (archive_dir / "stage3" / "fact-check-report.md").relative_to(repo_root).as_posix()
    prompt = (
        f"Build the companion executive presentation for the report titled "
        f"\"{title}\".\n\n"
        f"Source material:\n"
        f"- Final draft: `{final_rel}`\n"
        f"- Fact-check report: `{factcheck_rel}` (read if present)\n"
        f"- Run prompt: `prompts/runs/{slug}.md` (read if present)\n\n"
        f"Save the finished deck to: `{out_path}`\n"
        f"The repo's Python interpreter with python-pptx installed is at "
        f"`.venv/bin/python` — use it for your build script, and validate the "
        f"deck opens cleanly before finishing."
    )
    await _run_agent(
        agent=designer,
        user_prompt=prompt,
        model=_model("presentation"),
        cwd=repo_root,
        step_label=f"deck/{slug}",
        tally=tally,
        output_path=out_path,
    )
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    deck_dst = REPORTS_DIR / f"{slug}.pptx"
    shutil.copy2(out_path, deck_dst)
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
        "want_pptx": getattr(spec, "want_pptx", False),
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


async def run_pipeline(
    *,
    spec: RunSpec,
    run_file: Path,
    repo_root: Path,
    auto_approve: bool,
    resume: bool = False,
    budget_usd: float | None = None,
) -> RunResult:
    from cli.checkpoints import checkpoint_after_stage2, checkpoint_after_stage3
    from cli.docx_builder import build_documents
    from cli.archive import archive_run

    outputs_dir = repo_root / "outputs"
    await prepare_outputs(outputs_dir, auto_approve=auto_approve, resume=resume)
    write_run_marker(outputs_dir, spec)
    all_agents = load_all_agents()
    tally = CostTally(budget_usd=budget_usd)
    result_out = RunResult(tally=tally)

    await emit("run_start", slug=spec.slug, title=spec.title,
               agents=list(spec.selected_research_agents),
               output_format=getattr(spec, "output_format", "report"),
               resume=resume)

    await emit("stage_start", stage=1, label="Research — parallel briefs")
    console.rule("[bold]Stage 1 — parallel research briefs[/bold]")
    await run_stage1(spec, run_file, outputs_dir, all_agents, tally)

    await emit("stage_start", stage=2, label="Synthesis & adversarial revision")
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
                spec, run_file, outputs_dir, all_agents, tally,
                start_from="strategist-v3", v3_note=result.notes,
            )
            continue
        console.print("[yellow]Stopping at Stage 2.[/yellow]")
        return result_out

    await emit("stage_start", stage=3, label="Edit, humanize & fact-check")
    console.rule("[bold]Stage 3 — edit, humanize & fact-check[/bold]")
    await run_stage3(run_file, outputs_dir, all_agents, tally)

    result = await checkpoint_after_stage3(outputs_dir, auto_approve=auto_approve)
    if not result.approved:
        console.print("[yellow]Stopping at Stage 3. No Word docs generated.[/yellow]")
        return result_out

    await emit("stage_start", stage=4, label="Produce documents")
    console.rule("[bold]Stage 4 — Word documents[/bold]")
    build_documents(
        slug=spec.slug,
        title=spec.title,
        final_draft=outputs_dir / "stage3" / "final-draft.md",
        methodology=repo_root / "docs" / "methodology.md",
        out_dir=outputs_dir / "stage4",
        output_format=getattr(spec, "output_format", "report"),
    )

    if getattr(spec, "want_pptx", False):
        console.rule("[bold]Companion PowerPoint[/bold]")
        await run_presentation(spec, outputs_dir, all_agents, tally)

    console.rule("[bold]Archive[/bold]")
    archive_path = archive_run(repo_root=repo_root, slug=spec.slug, tally=tally)
    console.print(f"[green]Archived to:[/green] {archive_path}")
    result_out.archive_path = archive_path

    # Final step: publish the polished, distribution-ready document. The run
    # is complete without a separate `council --publish` invocation; that flag
    # remains for re-publishing or backfilling older archives.
    console.rule("[bold]Publish[/bold]")
    from cli.publish import REPORTS_DIR, publish_all

    for slug, out_path, status in publish_all(only_slug=spec.slug):
        if status == "ok" and out_path is not None:
            console.print(
                f"[green]Published:[/green] {out_path.relative_to(repo_root)}"
            )
            result_out.published_path = out_path
        else:
            console.print(f"[yellow]Publish issue for {slug}: {status}[/yellow]")

    # A companion deck archived with the run also belongs in reports/.
    deck_src = archive_path / "stage4" / f"{spec.slug}.pptx"
    if deck_src.is_file():
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        deck_dst = REPORTS_DIR / f"{spec.slug}.pptx"
        shutil.copy2(deck_src, deck_dst)
        console.print(f"[green]Deck:[/green] {deck_dst.relative_to(repo_root)}")
        result_out.deck_path = deck_dst

    result_out.completed = True
    await emit(
        "run_complete",
        slug=spec.slug,
        title=spec.title,
        total=tally.total,
        archive=str(archive_path),
        published=str(result_out.published_path) if result_out.published_path else None,
        deck=str(result_out.deck_path) if result_out.deck_path else None,
    )
    _notify_done("AI Council", f"Run complete: {spec.title} (${tally.total:.2f})")
    return result_out


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

    from cli.checkpoints import _read, _show_file_excerpt
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
    await emit("run_start", slug=source.slug, title=f"{source.slug} — Revision v{version}",
               agents=["strategist", "red-team", "editor", "humanizer", "fact-checker"],
               mode="revise")
    await emit("stage_start", stage=2, label=f"Revising to v{version}")

    steps = [
        ("strategist-a", by_name["strategist"], base / "revised-draft-a.md", _model("synthesis")),
        ("red-team", by_name["red-team"], base / "red-team-critique.md", _model("critique")),
        ("strategist-b", by_name["strategist"], base / "revised-draft-b.md", _model("synthesis")),
        ("editor", by_name["editor"], base / "edited-draft.md", _model("editor")),
        ("humanizer", by_name["humanizer"], base / "humanized-draft.md", _model("humanizer")),
        ("fact-checker", by_name["fact-checker"], base / "final-draft.md", _model("factcheck")),
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
