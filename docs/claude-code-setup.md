# MWAA AI Council — Setup & Run Instructions

## Context

You are helping build and operate a multi-agent AI system (internally called "the Council") that produces rigorous, executive-grade analytical reports on airport industry topics. The Council consists of specialized agents that research independently, debate, critique each other, and produce a final polished Word document.

The first run will produce a provocative thought piece with the working thesis: **"Airports are over-investing in infrastructure and under-investing in operational intelligence."** This thesis was proposed by MWAA leadership and should be treated as the sharp angle to pursue, while honestly steelmanning the counter-argument.

## Principles (read before building)

1. **Runtime is not quality.** The goal is depth of disagreement between agents, not clock time. A well-orchestrated 90-minute run beats a sloppy 6-hour one. If agents are echoing each other, something is wrong.

2. **Steelman the counter-argument.** A provocative piece that only stacks evidence for the thesis is a polemic. The best version presents the strongest case against, then dismantles it. That's what makes it credible to sophisticated readers.

3. **Versioned human editing is the improvement loop.** Agents get better through committed PRs against their markdown files after each run — not through self-modification. Never let an agent edit another agent's file.

4. **Every numerical claim must be sourced.** The Fact-checker has veto power. Unsourced numbers get flagged or removed.

5. **No buzzwords, no hedging, no motivational language.** The user (Christian) is an experienced airport operations leader. Output should be tight, plain, and direct. "Absolutely" is banned. So is "leverage synergies" and similar.

6. **Disclose the methodology.** Every final output carries a methodology appendix explaining the multi-agent process.

## Repository Structure

```
mwaa-ai-council/
├── .claude/
│   └── agents/
│       ├── infrastructure-economist.md
│       ├── operations-analyst.md
│       ├── technology-scout.md
│       ├── contrarian.md
│       ├── strategist.md
│       ├── red-team.md
│       ├── editor.md
│       └── fact-checker.md
├── prompts/
│   └── runs/
│       └── infrastructure-vs-intelligence.md
├── outputs/                    # gitignored
├── runs/                       # manually curated notable runs
├── docs/
│   ├── claude-code-setup.md    # this file
│   ├── how-to-run.md
│   ├── how-to-propose-an-agent-change.md
│   └── methodology.md
├── .gitignore
└── README.md
```

## Orchestration — How to Actually Run It

Once all agent files are committed to the repo, here's the run sequence. You can kick this off from Claude Code with a top-level prompt:

The orchestration prompt is now maintained as a modular template at [`prompts/orchestration.md`](../prompts/orchestration.md). To kick off a run:

1. Copy [`prompts/runs/_template.md`](../prompts/runs/_template.md) to `prompts/runs/<your-slug>.md` and fill in the sections.
2. Open `prompts/orchestration.md` and replace the two values at the top: `{{RUN_FILE}}` (path to your new run file) and `{{RUN_SLUG}}` (used for the archive folder name).
3. Copy the orchestration body (from "I'm ready to execute..." to the end) and paste into a fresh Claude Code session in the repo root.

The orchestration file is the source of truth for the four-stage sequence, the model guidance, and the rules for the whole run. If you need to edit the sequence itself, open a PR against `prompts/orchestration.md` so the change is versioned.

## Methodology Appendix (to include in the final Word doc)

Every final output should include an appendix along these lines:

> **Methodology**
>
> This document was produced by a multi-agent AI system operated by [name/role]. The system consisted of eight specialized agents running on Anthropic's Claude platform: four research agents (Infrastructure Economist, Operations Analyst, Technology Scout, Contrarian) that independently gathered evidence; a Strategist that synthesized their findings into a draft argument; a Red Team agent that critiqued the draft across multiple revision rounds; an Editor that tightened the final prose; and a Fact-checker that verified numerical claims against source briefs.
>
> Total agent runtime: [X] hours. Human review occurred at two checkpoints. All numerical claims were verified against primary research briefs or flagged for human review. Agent definitions are maintained as versioned markdown files in a private repository and are edited by human reviewers via pull request.
>
> The final text was reviewed and approved by [name] before release. AI-assisted production does not reduce human accountability for the arguments and claims in this document.

## Before You Run

Checklist:
- [ ] All 8 agent files committed to `.claude/agents/`
- [ ] Run prompt committed to `prompts/runs/`
- [ ] `outputs/` directory exists and is in `.gitignore`
- [ ] You have API budget — estimate $30-100 for a full run depending on research depth
- [ ] You have 3-4 hours of soft monitoring time available (you don't need to watch it, but you should check in at checkpoints)
- [ ] You've read the thesis carefully and are prepared to push back on the Strategist if the argument goes somewhere you disagree with

## After the Run

- [ ] Commit notable intermediate artifacts to `runs/YYYY-MM-DD-<slug>/` for archival
- [ ] Write 3-5 sentences of post-run notes in `runs/YYYY-MM-DD-<slug>/retrospective.md`: what worked, what didn't, which agent files should be revised
- [ ] Open PRs against the agent files for any refinements identified in the retrospective
- [ ] Do a final human pass on the Word doc before sending anywhere — AI output is 85%, your judgment is the last 15%
