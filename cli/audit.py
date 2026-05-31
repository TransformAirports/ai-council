"""Council audit — scan archived runs and surface which agents to revise.

For every run under `runs/YYYY-MM-DD-<slug>/`, the audit pulls objective
signals from the artifacts on disk:

  - Which research agents were seated (filename presence in stage1/)
  - Brief word count per agent
  - Citation count per agent in the final draft (display-name search)
  - Fact-check rejections traceable to each agent (UNVERIFIED tag with the
    agent's name in nearby context)
  - Total run cost and completion status (presence of stage4 .docx files)

It rolls those signals up across runs into per-agent scores and produces a
markdown report with patterns worth acting on and a checklist of specific
agent files to edit. The current state of `.claude/agents/` is the source of
truth for which lenses exist and what their display names are; agents that
exist but have never been seated are flagged separately.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from cli.agents import Agent, load_all_agents

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = REPO_ROOT / "runs"

ARCHIVE_DIR_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")
UNVERIFIED_TAG = re.compile(r"\[UNVERIFIED[^\]]*\]")


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


@dataclass
class AgentScore:
    runs_seated: int = 0
    total_brief_words: int = 0
    times_cited_in_final: int = 0
    times_rejected_traceable: int = 0
    runs_completed: int = 0

    @property
    def avg_brief_words(self) -> int:
        if not self.runs_seated:
            return 0
        return self.total_brief_words // self.runs_seated

    @property
    def citation_rate(self) -> float:
        if not self.runs_seated:
            return 0.0
        return self.times_cited_in_final / self.runs_seated

    @property
    def citations_per_1k_brief_words(self) -> float:
        """The signal that actually matters: synthesis return on brief volume."""
        if not self.total_brief_words:
            return 0.0
        return self.times_cited_in_final / (self.total_brief_words / 1000.0)


def _count_words(text: str) -> int:
    return len(text.split())


def _list_archived_runs(runs_dir: Path) -> list[Path]:
    if not runs_dir.is_dir():
        return []
    return sorted(
        p for p in runs_dir.iterdir()
        if p.is_dir() and ARCHIVE_DIR_PATTERN.match(p.name)
    )


def _parse_cost_from_retrospective(retro_path: Path) -> float | None:
    if not retro_path.is_file():
        return None
    try:
        text = retro_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = re.search(r"[Tt]otal[^$\n]*\$\s*([\d,]+\.\d{2})", text)
    if m:
        try:
            return float(m.group(1).replace(",", ""))
        except ValueError:
            pass
    return None


def load_run(archive_dir: Path) -> RunRecord:
    match = ARCHIVE_DIR_PATTERN.match(archive_dir.name)
    slug = match.group(1) if match else archive_dir.name

    stage1 = archive_dir / "stage1"
    seated_agents: list[str] = []
    brief_word_counts: dict[str, int] = {}
    if stage1.is_dir():
        for brief in sorted(stage1.glob("*-brief.md")):
            name = brief.name[: -len("-brief.md")]
            seated_agents.append(name)
            try:
                brief_word_counts[name] = _count_words(
                    brief.read_text(encoding="utf-8", errors="ignore")
                )
            except OSError:
                brief_word_counts[name] = 0

    final_path = archive_dir / "stage3" / "final-draft.md"
    final_text = ""
    if final_path.is_file():
        try:
            final_text = final_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            pass
    final_word_count = _count_words(final_text)
    unverified_count = len(UNVERIFIED_TAG.findall(final_text))

    stage4 = archive_dir / "stage4"
    completed_stage4 = stage4.is_dir() and any(stage4.glob("*.docx"))

    cost_total = _parse_cost_from_retrospective(archive_dir / "retrospective.md")

    return RunRecord(
        slug=slug,
        archive_dir=archive_dir,
        seated_agents=seated_agents,
        brief_word_counts=brief_word_counts,
        final_word_count=final_word_count,
        unverified_count=unverified_count,
        completed_stage4=completed_stage4,
        cost_total=cost_total,
    )


def _agent_search_patterns(agent: Agent) -> set[str]:
    """Names to look for when attributing citations to an agent."""
    patterns: set[str] = set()
    if agent.display_name:
        patterns.add(agent.display_name)
    # Also accept the kebab-case name expanded into a phrase
    patterns.add(agent.name.replace("-", " "))
    # Common reference forms used in drafts (e.g., "Economist brief")
    if "-" in agent.name:
        head = agent.name.split("-")[0]
        patterns.add(head)
    return {p for p in patterns if len(p) >= 4}


def _score_agent_in_text(agent: Agent, text: str) -> tuple[int, int]:
    """Return (citations_in_final, rejections_traceable_to_agent)."""
    if not text:
        return 0, 0
    patterns = _agent_search_patterns(agent)
    citations = 0
    for p in patterns:
        try:
            citations += len(re.findall(r"\b" + re.escape(p) + r"\b", text, re.IGNORECASE))
        except re.error:
            continue

    rejections = 0
    for m in UNVERIFIED_TAG.finditer(text):
        ctx_start = max(0, m.start() - 150)
        context = text[ctx_start:m.start()]
        for p in patterns:
            if re.search(r"\b" + re.escape(p) + r"\b", context, re.IGNORECASE):
                rejections += 1
                break

    return citations, rejections


def audit_runs(
    runs_dir: Path = RUNS_DIR,
    agents: list[Agent] | None = None,
) -> dict:
    if agents is None:
        agents = load_all_agents()
    agents_by_name = {a.name: a for a in agents}

    run_paths = _list_archived_runs(runs_dir)
    runs: list[RunRecord] = [load_run(p) for p in run_paths]
    scores: dict[str, AgentScore] = defaultdict(AgentScore)

    for run in runs:
        final_path = run.archive_dir / "stage3" / "final-draft.md"
        final_text = ""
        if final_path.is_file():
            try:
                final_text = final_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                pass

        for agent_name in run.seated_agents:
            score = scores[agent_name]
            score.runs_seated += 1
            score.total_brief_words += run.brief_word_counts.get(agent_name, 0)
            if run.completed_stage4:
                score.runs_completed += 1

            agent = agents_by_name.get(agent_name)
            if agent is None:
                continue
            citations, rejections = _score_agent_in_text(agent, final_text)
            score.times_cited_in_final += citations
            score.times_rejected_traceable += rejections

    return {"runs": runs, "scores": dict(scores)}


def _diagnose(score: AgentScore) -> str:
    """Diagnose an agent's signal using citations-per-1k-brief-words.

    The metric is "how many times did the Strategist surface this agent's
    work, per 1,000 words of brief the agent wrote." This penalizes long
    briefs that nobody cites and rewards short briefs that get used a lot.
    """
    if score.runs_seated == 0:
        return "—"
    if score.times_rejected_traceable >= 3:
        return "**HIGH REJECTION**"
    rate = score.citations_per_1k_brief_words
    if score.runs_seated >= 2 and rate < 1.5:
        return "**UNDERUSED**"
    if rate >= 8.0:
        return "Strong contributor"
    if rate >= 3.0:
        return "Solid"
    return "Adequate"


def _extract_findings(
    scores: dict[str, AgentScore],
    runs: list[RunRecord],
    agents_by_name: dict[str, Agent],
) -> list[str]:
    findings: list[str] = []

    for name, score in sorted(scores.items()):
        if score.runs_seated >= 2 and score.citations_per_1k_brief_words < 1.5:
            findings.append(
                f"**{name}** has a low return on brief volume: "
                f"{score.citations_per_1k_brief_words:.1f} citations per 1k brief words "
                f"({score.times_cited_in_final} citations across {score.runs_seated} runs "
                f"of ~{score.avg_brief_words:,}-word briefs). Strong contributors land 8+. "
                f"The synthesis is paying for variance the Strategist isn't using. "
                f"Tighten the prompt to a shorter, more pointed brief — or drop the agent "
                f"from default presets and only seat it when the thesis specifically needs the lens."
            )

    total_rejections = sum(s.times_rejected_traceable for s in scores.values())
    if total_rejections >= 3:
        for name, score in sorted(scores.items()):
            if score.times_rejected_traceable >= 2:
                share = score.times_rejected_traceable / total_rejections
                if share >= 0.25:
                    findings.append(
                        f"**{name}** accounts for {share:.0%} of traceable fact-check "
                        f"rejections ({score.times_rejected_traceable} of {total_rejections}). "
                        f"The prompt may be encouraging confident assertion over verifiable "
                        f"evidence. Add stricter sourcing language."
                    )

    completed = [r for r in runs if r.completed_stage4]
    incomplete = [r for r in runs if not r.completed_stage4]
    if incomplete and completed:
        findings.append(
            f"{len(incomplete)} of {len(runs)} runs did not reach Stage 4. The incomplete "
            f"runs averaged {sum(len(r.seated_agents) for r in incomplete) / len(incomplete):.1f} "
            f"agents seated; the completed ones averaged "
            f"{sum(len(r.seated_agents) for r in completed) / len(completed):.1f}. "
            f"If incomplete runs trend toward larger councils, the pipeline cost (turn "
            f"budgets, rate limits) is correlating with breadth."
        )

    # Unverified-tag spread: which runs left a lot of unsourced claims for human review?
    if len(runs) >= 2:
        unverified = [(r.slug, r.unverified_count) for r in runs]
        max_run = max(unverified, key=lambda x: x[1])
        min_run = min(unverified, key=lambda x: x[1])
        if max_run[1] >= 5 and max_run[1] >= 3 * max(1, min_run[1]):
            findings.append(
                f"Run `{max_run[0]}` left {max_run[1]} unverified tags in its final draft, "
                f"versus {min_run[1]} for `{min_run[0]}`. Either the Fact-checker is more "
                f"aggressive on certain theses, or some research agents are producing claims "
                f"that don't survive verification on certain topics. Worth diffing the briefs."
            )

    return findings


def _generate_next_steps(
    scores: dict[str, AgentScore],
    agents: list[Agent],
) -> list[str]:
    steps: list[str] = []
    seen: set[str] = set()

    for name, score in sorted(scores.items()):
        if score.runs_seated >= 2 and score.citations_per_1k_brief_words < 1.5:
            target = f".claude/agents/{name}.md"
            if target not in seen:
                steps.append(
                    f"Tighten `{target}` — {score.citations_per_1k_brief_words:.1f} "
                    f"citations per 1k brief words (strong contributors land 8+)."
                )
                seen.add(target)
        if score.times_rejected_traceable >= 3:
            target = f".claude/agents/{name}.md"
            if target not in seen:
                steps.append(
                    f"Add stricter sourcing rules to `{target}` — high traced rejection count."
                )
                seen.add(target)

    research_names = {a.name for a in agents if a.is_research}
    never_seated = sorted(research_names - set(scores.keys()))
    if never_seated:
        steps.append(
            f"Decide whether {', '.join('`' + n + '`' for n in never_seated)} "
            f"belongs in a preset or should be retired."
        )

    return steps


def render_audit_report(result: dict, agents: list[Agent]) -> str:
    runs: list[RunRecord] = result["runs"]
    scores: dict[str, AgentScore] = result["scores"]
    agents_by_name = {a.name: a for a in agents}

    lines: list[str] = []
    lines.append(f"# Council Audit — {date.today().isoformat()}")
    lines.append("")

    if not runs:
        lines.append("No archived runs found under `runs/`. Run a Council job first, then audit.")
        lines.append("")
        return "\n".join(lines)

    lines.append(f"Scanned **{len(runs)}** archived run(s):")
    lines.append("")
    for run in runs:
        cost = f"${run.cost_total:.2f}" if run.cost_total is not None else "cost unknown"
        status = "completed" if run.completed_stage4 else "**incomplete**"
        lines.append(
            f"- `{run.slug}` — {len(run.seated_agents)} agents seated, {cost}, "
            f"{status}, {run.final_word_count:,} words in final, {run.unverified_count} unverified tag(s)"
        )
    lines.append("")

    if len(runs) < 3:
        lines.append(
            "> _Note: with fewer than three runs scanned, every signal below is "
            "preliminary. Patterns emerge across runs, not within one._"
        )
        lines.append("")

    lines.append("## Agent performance")
    lines.append("")
    lines.append(
        "Sorted by **citations per 1k brief words** — how often the Strategist "
        "surfaced each agent's work relative to how much that agent wrote. "
        "Strong contributors land 8+. Under 1.5 is a signal the prompt needs work "
        "or the agent doesn't belong in default presets."
    )
    lines.append("")
    lines.append(
        "| Agent | Runs | Avg brief words | Cited | Rejections | Cites / 1k words | Signal |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")

    sorted_scores = sorted(
        scores.items(),
        key=lambda kv: (-kv[1].citations_per_1k_brief_words, -kv[1].runs_seated, kv[0]),
    )
    for name, score in sorted_scores:
        lines.append(
            f"| `{name}` | {score.runs_seated} | {score.avg_brief_words:,} | "
            f"{score.times_cited_in_final} | {score.times_rejected_traceable} | "
            f"{score.citations_per_1k_brief_words:.1f} | {_diagnose(score)} |"
        )
    lines.append("")

    research_names = {a.name for a in agents if a.is_research}
    never_seated = sorted(research_names - set(scores.keys()))
    if never_seated:
        lines.append("## Available but never seated")
        lines.append("")
        for name in never_seated:
            agent = agents_by_name.get(name)
            disp = agent.display_name if agent else name
            lines.append(f"- `{name}` ({disp})")
        lines.append("")

    findings = _extract_findings(scores, runs, agents_by_name)
    if findings:
        lines.append("## Patterns worth acting on")
        lines.append("")
        for i, finding in enumerate(findings, 1):
            lines.append(f"{i}. {finding}")
            lines.append("")

    next_steps = _generate_next_steps(scores, agents)
    if next_steps:
        lines.append("## What to do next")
        lines.append("")
        for step in next_steps:
            lines.append(f"- [ ] {step}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("### Methodology notes")
    lines.append("")
    lines.append(
        "- **Citation counts are approximate.** The audit searches the final draft for "
        "each agent's display name and a few common reference forms. Agents whose display "
        "names are common English words (e.g. \"Slacker\", \"Virtual Christian\") may be "
        "undercounted because the Strategist doesn't always name-drop them when it uses "
        "their content."
    )
    lines.append(
        "- **Rejections are attributed by proximity.** An `[UNVERIFIED]` tag with an "
        "agent's name in the 150 chars before it is counted against that agent. False "
        "positives are possible when multiple agents are named near the same passage."
    )
    lines.append(
        "- **The audit only sees what's in `runs/`.** Runs you deleted or archived "
        "elsewhere are invisible to this scan."
    )
    lines.append("")
    lines.append(
        f"_Generated by `council --audit`. Re-run after each new archive to track how "
        f"the agent roster is performing across runs._"
    )

    return "\n".join(lines)


def write_audit_report(report: str, runs_dir: Path = RUNS_DIR) -> Path:
    runs_dir.mkdir(parents=True, exist_ok=True)
    out_path = runs_dir / f"_audit-{date.today().isoformat()}.md"
    out_path.write_text(report, encoding="utf-8")
    return out_path
