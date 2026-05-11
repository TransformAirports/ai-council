# The Transform Airports AI Council

**A multi-agent system that produces executive-grade analytical reports on the airport industry.**

Twelve specialized agents. Eight run in parallel to research a thesis independently, each through a different lens: economics, operations, technology, opposition, engineering, airline commercial strategy, regulation and politics, and aviation history. One synthesizes their briefs into an argument. One attacks that argument. The author revises, the attacker hits it again. An editor tightens. A fact-checker verifies every number. A human reviews the result twice. The final deliverables are two Word documents — a full report and a three-page executive summary — with a methodology appendix, ready to share.

This repository is the source of truth for the agents and the process. The agents live as versioned markdown files in [`.claude/agents/`](.claude/agents/). Runs are triggered with a single command in Claude Code.

---

## Hit run

Treat the repo like a Claude Code app. There are two ways in.

**Option A — you know what you want to write.** Copy [`prompts/runs/_template.md`](prompts/runs/_template.md), rename the copy to describe your thesis (e.g. `airline-consolidation.md`), fill in the sections in your editor of choice, and in Claude Code say:

> **run airline-consolidation**

Claude confirms the thesis with you in one sentence, kicks off the four-stage sequence, and a few hours later hands you back two Word documents and an archived run folder.

**Option B — you want to dictate the thesis.** In Claude Code, say:

> **Let's do a new Council run.**

Claude will ask what you want to write about in plain English, write the run file for you, and kick off the same sequence.

Either way: no git branches, no copy-pasting orchestration prompts, no remembering where files go. Running a new thesis adds a markdown file; nothing gets "deployed."

Branches are only needed for editing the agent files themselves — see [`docs/how-to-propose-an-agent-change.md`](docs/how-to-propose-an-agent-change.md).

---

## Why this exists

A single LLM, asked to write a long analytical piece, produces prose that is fluent and subtly wrong. It hedges where it shouldn't, cherry-picks its own evidence, smooths over objections, and flatters whatever thesis you handed it. The output reads like every other AI-generated document you've seen.

The Council is an answer to that failure mode. It builds in the three things a solo model cannot do on its own:

1. **Genuinely independent evidence.** Eight research agents gather data without seeing each other's work. You get variance, not convergence.
2. **Adversarial pressure on the draft.** A Red Team agent exists only to break the argument. The Strategist has to defend it. Two rounds of this strip out the weak claims.
3. **A hard stop on unverifiable numbers.** A Fact-checker cross-references every number in the final draft against the research briefs. If it can't trace a claim, the claim goes.

The result is a document a sophisticated reader will still disagree with — but not one they can dismiss.

---

## Example: a finished report

To see what the Council produces end-to-end, look at the archived run in [`runs/2026-04-17-infrastructure-vs-intelligence/`](runs/2026-04-17-infrastructure-vs-intelligence/).

**The thesis:**

> **Airports are over-investing in infrastructure and under-investing in operational intelligence.**

The run file is at [`prompts/runs/infrastructure-vs-intelligence.md`](prompts/runs/infrastructure-vs-intelligence.md). The Council produced an 11,600-word final report and a three-page executive summary from it, with 118 numerical claims verified against the research briefs and 10 analyst-derived figures tagged for human review.

**What's in the archive folder:**

- [`stage1/`](runs/2026-04-17-infrastructure-vs-intelligence/stage1/) — four independent research briefs (this run used the prior four-agent roster; current runs will produce eight)
- [`stage2/`](runs/2026-04-17-infrastructure-vs-intelligence/stage2/) — three Strategist drafts and two Red Team critiques, showing how the argument evolved across the adversarial loop
- [`stage3/`](runs/2026-04-17-infrastructure-vs-intelligence/stage3/) — the Editor's cut, the Fact-checker's verification report, and the final text
- [`stage4/`](runs/2026-04-17-infrastructure-vs-intelligence/stage4/) — the full report and executive summary as Word documents
- [`retrospective.md`](runs/2026-04-17-infrastructure-vs-intelligence/retrospective.md) — what worked, what didn't, and which agent-file behaviors to watch next time

The point of the piece was not to confirm its thesis. It was to present the claim sharply, steelman the counter-argument, and let the evidence decide whether the thesis survived. Read the archive as a worked example of that pattern.

---

## The twelve agents

All live in [`.claude/agents/`](.claude/agents/) as markdown files with YAML frontmatter. Each has an edge — a default stance they argue from. None are neutral.

### Research (Stage 1 — eight agents, run in parallel)

| Agent | Lens |
|---|---|
| [`infrastructure-economist`](.claude/agents/infrastructure-economist.md) | Airport CapEx economics, cost overruns, debt service, opportunity cost |
| [`operations-analyst`](.claude/agents/operations-analyst.md) | Delay causes, gate utilization, latent throughput in existing infrastructure |
| [`technology-scout`](.claude/agents/technology-scout.md) | What operational technology actually costs and returns in deployment |
| [`contrarian`](.claude/agents/contrarian.md) | The strongest possible case **against** the thesis |
| [`chief-engineer`](.claude/agents/chief-engineer.md) | Constructability, lifecycle cost, design standards, megaproject failure modes |
| [`airline-commercial-strategist`](.claude/agents/airline-commercial-strategist.md) | Hub economics, CPE sensitivity, dehubbing warnings, carrier responses |
| [`regulatory-political-analyst`](.claude/agents/regulatory-political-analyst.md) | FAA, TSA, CBP, Congress, and local political constraints that are actually binding |
| [`aviation-historian`](.claude/agents/aviation-historian.md) | Long-cycle industry arcs, deregulation, consolidation waves, pattern-matching |

### Synthesis & Debate (Stage 2)

| Agent | Role |
|---|---|
| [`strategist`](.claude/agents/strategist.md) | Reads all eight briefs; writes the argumentative draft; revises after each Red Team pass |
| [`red-team`](.claude/agents/red-team.md) | Attacks the Strategist's draft; finds unsupported claims, logical gaps, missed lenses |

### Polish (Stage 3)

| Agent | Role |
|---|---|
| [`editor`](.claude/agents/editor.md) | Cuts 15-25% of word count; kills buzzwords; tightens prose. Adds nothing. |
| [`fact-checker`](.claude/agents/fact-checker.md) | Verifies every number against the Stage 1 briefs. Has veto power. |

---

## How a run works

```
Stage 1: Research (parallel, ~60-90 min)
  infrastructure-economist      ─┐
  operations-analyst            ─┤
  technology-scout              ─┤
  contrarian                    ─┼──► 8 briefs in outputs/stage1/
  chief-engineer                ─┤
  airline-commercial-strategist ─┤
  regulatory-political-analyst  ─┤
  aviation-historian            ─┘

Stage 2: Synthesis & Debate (~60-90 min)
  strategist v1 ──► red-team critique ──► strategist v2
                 ──► red-team critique ──► strategist v3
                                           │
                                           ▼
                                    ★ Human checkpoint #1

Stage 3: Polish (~30-60 min)
  editor ──► fact-checker ──► final-draft.md
                              │
                              ▼
                       ★ Human checkpoint #2

Stage 4: Word documents (~5 min)
  docx skill ──► full report .docx (cover, TOC, body, methodology appendix)
              ──► 3-page executive summary .docx

Auto-archive
  outputs/ ──► runs/YYYY-MM-DD-<slug>/ (with retrospective)
```

Two human checkpoints. The first is after the Strategist's third draft — this is where you decide whether the argument is going somewhere worth finishing. The second is after the Fact-checker — this is where you confirm the numbers hold up.

Full operator's guide: [`docs/how-to-run.md`](docs/how-to-run.md).

---

## Principles

These are the rules the Council plays by. They are also the rules the prose plays by — each agent is instructed to refuse them.

1. **Runtime is not quality.** A well-orchestrated 90-minute run beats a sloppy 6-hour one. Depth of disagreement between agents matters more than time on the clock.
2. **Steelman the counter-argument.** A thesis that cannot survive its strongest objection should not be published.
3. **Versioned human editing is the improvement loop.** Agents get better through pull requests against their markdown files. Agents never edit themselves. Agents never edit each other.
4. **Every numerical claim must be sourced.** The Fact-checker has veto power. No exceptions.
5. **No buzzwords. No hedging. No motivational language.** "Leverage," "synergy," "paradigm shift," "in today's rapidly evolving landscape" — all banned. The reader is sophisticated; write for that reader.
6. **Disclose the methodology.** Every final document carries the methodology appendix. AI assistance does not reduce human accountability.

---

## How the agents get better

After every run, the operator writes a brief retrospective — what worked, what didn't, which agent file needs editing. Pattern defects (the Red Team is too polite; the Contrarian softens in the last section; the Editor misses hedge words) become PRs against the relevant markdown file. A second human reviews. The next run uses the updated agent.

This is deliberately slow. It is also the only way to keep the system accountable across many runs.

See [`docs/how-to-propose-an-agent-change.md`](docs/how-to-propose-an-agent-change.md).

---

## Repository layout

```
transform-airports-ai-council/
├── CLAUDE.md                    # repo-root guidance Claude Code auto-loads
├── .claude/agents/              # the twelve agent definitions
├── prompts/
│   ├── orchestration.md         # the canonical 4-stage sequence (Claude reads this; you don't)
│   ├── start-a-run.md           # conversational entry point for dictated runs
│   └── runs/
│       ├── _template.md         # copy this, rename, fill in
│       └── <your-run>.md        # one file per thesis you run
├── outputs/                     # working directory for the current run (gitignored, auto-cleared)
├── runs/                        # archived completed runs (one folder per run, auto-created)
├── docs/                        # operator and contributor docs
│   ├── claude-code-setup.md
│   ├── how-to-run.md            # operator's guide
│   ├── how-to-propose-an-agent-change.md
│   └── methodology.md           # the canonical methodology appendix
├── .gitignore
└── README.md
```

---

## Getting started

1. Install [Claude Code](https://docs.claude.com/en/docs/claude-code) and clone this repository.
2. Read [`docs/how-to-run.md`](docs/how-to-run.md) for the operator's guide and the two human checkpoints to expect.
3. **Decide on a thesis.** Copy [`prompts/runs/_template.md`](prompts/runs/_template.md), rename the copy, and fill in the sections in the editor of your choice. Or skip the file and dictate the thesis to Claude Code (see "Hit run" above).
4. In Claude Code, say **`run <your-filename>`**. Claude confirms, runs the four stages with two human checkpoints, generates the Word documents, and archives the run.

Budget roughly $40-60 in API cost per full run and 2-4 hours of wall-clock time. The actual time at the keyboard is whatever you spend at the two checkpoints.

**Reference example:** [`runs/2026-04-17-infrastructure-vs-intelligence/`](runs/2026-04-17-infrastructure-vs-intelligence/) contains a complete archived run — every intermediate artifact, the final Word document, the three-page executive summary, the fact-check report, and the retrospective. Read it to see what a good run looks like end-to-end.

---

## A note on scope

The Council is tuned for airport industry analysis — airport economics, operations, capital programs, airline commercial dynamics, regulation and politics, and the long arc of US aviation. The pattern (independent researchers → adversarial synthesis → editor → fact-checker → human checkpoints) generalizes. But the value is in the specialization. Edit the agents for your domain. Don't use them as a generic "write me a report" framework.

---

## Accountability

AI output is 85%. The last 15% is the judgment of the human whose name goes on the document. Every final piece the Council produces carries that human's name, reviewed and approved before release. The methodology appendix discloses how the document was made. The disclosure is not a disclaimer — it is a statement of process.

---

## Sync architecture

The agent files in [`.claude/agents/`](.claude/agents/) are the source of truth. A companion Lovable site reads the same agent roster from Supabase. The two stay in sync via a GitHub Action.

```
.claude/agents/*.md  ──push to main──►  GitHub Action  ──upsert──►  Supabase ◄──read──  Lovable site
```

**Required frontmatter on every agent file:**

```yaml
---
name: <kebab-case slug>          # also the Claude Code subagent identifier
display_name: <human-readable>
description: <one-line role>
order: <integer>
tools: <comma-separated list>    # required by Claude Code
---
```

On every push to `main` that touches `.claude/agents/**`, `README.md`, or `scripts/sync-agents.mjs`, the workflow at [`.github/workflows/sync-agents.yml`](.github/workflows/sync-agents.yml) runs [`scripts/sync-agents.mjs`](scripts/sync-agents.mjs). The script parses each agent file with `gray-matter`, upserts a row into the Supabase `agents` table keyed on `slug`, then deletes any rows whose slug is no longer in the repo. Renames and removals therefore propagate without manual cleanup.

The Supabase schema lives at [`supabase/migrations/0001_agents.sql`](supabase/migrations/0001_agents.sql). The `agents` table is publicly readable via RLS; writes require the service role key, which only the GitHub Action holds. The `agent_proposals` table accepts public inserts so the Lovable site can collect modification or addition proposals from readers; those proposals never modify `agents` directly — they become PR candidates against this repo, reviewed by humans before any agent behavior changes.

To run the sync locally for debugging:

```bash
SUPABASE_URL=... SUPABASE_SERVICE_KEY=... GIT_SHA=$(git rev-parse HEAD) npm run sync
```
