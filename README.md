# The Transform Airports AI Council

A multi-agent system that produces executive-grade analytical reports on the airport industry. This page explains what it is, how to use it, and how to install the CLI.

**On this page**

1. [What the AI Council is](#1-what-the-ai-council-is)
2. [How to use it](#2-how-to-use-it)
3. [Install and start the CLI](#3-install-and-start-the-cli)

---

## 1. What the AI Council is

The Council is a roster of specialized agents working in sequence to produce a single long-form analytical document on a thesis you supply. A group of research lenses you choose work in parallel, each through a different stance. One synthesizes their work into an argument. One attacks that argument. The first revises, the second attacks again. An editor tightens the prose. A fact-checker verifies every number against the underlying briefs. You review the result at two checkpoints. The final deliverables are two Word documents — a full report and a three-page executive summary — with a methodology appendix.

The point is to avoid the failure mode of asking a single model to write a long analytical piece: fluent prose that hedges where it shouldn't, cherry-picks its own evidence, smooths over objections, and flatters whatever thesis was handed in. The Council enforces three things a solo model will not do on its own.

- **Independent evidence.** The research agents you seat do not see each other's work. Each argues from a different default stance. You get variance instead of convergence.
- **Adversarial pressure.** The Red Team agent's only job is to break the Strategist's draft. Three rounds of attack-and-revise strip out the weak claims.
- **A hard stop on unverifiable numbers.** Every numerical claim in the final draft has to trace back to a Stage 1 brief. If it can't, the Fact-checker cuts it or flags it for human review.

### How you compose the council

You assemble each run yourself. The CLI presents the research lenses as a checklist; you seat the ones whose perspective the thesis actually needs. Three quality guardrails — the Red Team, the Editor, and the Fact-checker — run on every job and are not optional. Everything else is a pick-and-choose decision about what kind of council you want at this table for this thesis.

#### Required — the quality guardrails

These three are not selectable. They protect the output regardless of which research lenses you seat.

| Agent | What it does |
| --- | --- |
| **Red Team** | Attacks the Strategist's draft across two critique rounds. Finds weak claims, logical gaps, and unsupported assertions. |
| **Editor** | Cuts 15–25% of word count. Kills buzzwords. Adds nothing. |
| **Fact-checker** | Verifies every numerical and attributed claim against the research briefs. Has veto power over anything that cannot be sourced. |

#### The writer

The Strategist is the agent that turns whatever research lenses you seated into a single argumentative draft. There is one Strategist; it always runs once research is in.

| Agent | What it does |
| --- | --- |
| **Strategist** | Reads every research brief, writes the argumentative draft, and revises it in response to each Red Team pass. |

#### Pick your council — the research lenses

Sixteen research lenses are available. Seat as few or as many as the thesis warrants. Each one is biased by design — none are neutral — and each writes an independent brief without seeing the others. Fewer seats means a tighter scope and a cheaper run; more seats means more variance for the Strategist to argue against.

| Lens | What it brings to the table |
| --- | --- |
| Infrastructure Economist | Airport CapEx economics, cost overruns, debt service |
| Operations Analyst | Delay causes, throughput, gate utilization |
| Technology Scout | What operational technology actually costs and returns |
| Contrarian | The strongest possible case against the thesis |
| Chief Engineer | Constructability, lifecycle cost, megaproject failure modes |
| Airline Commercial Strategist | Hub economics, CPE sensitivity, carrier responses |
| Regulatory & Political Analyst | FAA, TSA, CBP, Congress, and the binding political constraints |
| Aviation Historian | Long-cycle industry arcs, deregulation, consolidation waves |
| Architectural Historian | Terminal architecture as a building type; design intent the operational record forgets |
| Airport CEO | Board accountability, bond rating, use-and-lease, long-horizon politics |
| Airport COO | The operator's chair: airfield, terminal, maintenance, airline relations |
| Director of Public Safety | Airport police, ARFF, dispatch under one command; Part 139 and 1542 reality |
| Airport EM Director | Long-tenured airport EM perspective; real EOC activations and exercises |
| EM Consultant (external) | Outside-in preparedness diagnosis; cross-sector pattern matching |
| The Slacker | Unstructured gut take plus wandering web searches; surfaces what the structured agents miss |
| Virtual Christian | The operator's free-thinker voice modeled on the council's human; reframes the question instead of answering it head-on |

---

## 2. How to use it

A run starts with a sharp thesis. The sharper the thesis, the sharper the output. "An overview of regional airline trends" produces a summary. "Regional airline consolidation has gone far enough that the next wave of mergers will strand infrastructure the industry just built" produces an argument.

You can start a run two ways:

- **The CLI (recommended).** Run `council` in the terminal. It walks you through the thesis, audience, tone, length, and which agents to seat on the Council, writes the run file for you, and drives the four stages end-to-end. Installation is in the next section.
- **Claude Code.** Write a run-prompt file in `prompts/runs/` by hand, then say "run \<filename\>" inside Claude Code. The conversational flow handles the same four stages.

Either path produces the same artifacts and the same archive layout. You can switch between them between runs.

### The four stages

**Stage 1 — Research** &nbsp;·&nbsp; *Parallel · Claude Sonnet · ~30–60 minutes*
The selected research agents work concurrently. Each produces an independent brief (typically 1,500–2,500 words) with inline source citations. They cannot read each other's output.

**Stage 2 — Synthesis and debate** &nbsp;·&nbsp; *Sequential · Claude Opus · ~60–90 minutes*
Strategist drafts v1, Red Team critiques v1, Strategist revises to v2, Red Team critiques v2, Strategist produces v3 with explicit handoff notes about anything it knowingly left in.

> **Human checkpoint #1.** The CLI shows you v3 and both critiques and asks whether to continue, redo the final draft with your notes, or stop. Pass `--no-review` to skip.

**Stage 3 — Edit and fact-check** &nbsp;·&nbsp; *Sequential · Claude Opus · ~30–45 minutes*
The Editor cuts roughly a fifth of the word count, removes buzzwords, and flags hedges. The Fact-checker verifies every numerical and attributed claim against the Stage 1 briefs. Unverifiable claims get cut or tagged `[UNVERIFIED — HUMAN REVIEW]`.

> **Human checkpoint #2.** The CLI shows you the final draft and the fact-check report. Pass `--no-review` to skip.

**Stage 4 — Word documents** &nbsp;·&nbsp; *Local generation · ~10 seconds*
The CLI builds two `.docx` files: a full report with cover page, table of contents placeholder, body, and methodology appendix; and a three-page executive summary distilled from the same final draft.

### After the run

The CLI archives everything to `runs/YYYY-MM-DD-<slug>/` with the four stage subfolders intact and writes a `retrospective.md` that includes the cost breakdown. Then it clears `outputs/` so the next run starts fresh.

A typical full run takes 2–4 hours of wall-clock time and costs roughly $40–60 in API spend. Reducing the number of research agents brings both down proportionally.

### An example you can read

The archived run at `runs/2026-04-17-infrastructure-vs-intelligence/` is the first complete Council deliverable. It tested the thesis that airports are over-investing in infrastructure and under-investing in operational intelligence, produced an 11,600-word report and a three-page executive summary, and verified 118 numerical claims against the briefs. Read it as a worked example of what a finished run looks like end-to-end.

---

## 3. Install and start the CLI

### Prerequisites

- macOS or Linux with Python 3.11 or newer (`python3 --version` to check)
- Either a Claude.ai subscription with Opus access **or** an Anthropic API key — see [Authenticate Claude](#authenticate-claude) below
- This repository cloned locally

### Install and run

One step. From the repository root:

```bash
./council
```

The first invocation creates a virtual environment, installs the Claude Agent SDK and the Word-document builder, and launches the CLI. Every subsequent invocation skips the install and goes straight to running. No `pip install`, no `source .venv/bin/activate`.

### Authenticate Claude

The CLI runs on the Claude Agent SDK, which uses the Claude Code CLI binary under the hood. That gives you two ways to pay for runs.

| Option | How to set it up |
| --- | --- |
| **Subscription credits** (Claude.ai Pro, Max, Team, or Enterprise) | Sign into Claude Code once with `claude login`. Leave `ANTHROPIC_API_KEY` unset. Runs draw against your Claude.ai plan's usage allowance. |
| **Pay-as-you-go API key** (Anthropic API console) | Export `ANTHROPIC_API_KEY="sk-ant-..."` in your shell. Runs draw against your API console balance and the CLI reports per-step USD cost. |

> **Subscription caveats.** Stages 2 and 3 use Claude Opus, so your subscription needs Opus access (Max, or Team and Enterprise with Opus enabled; Pro alone is generally Sonnet-only and will not complete a full run). The Council also fires many calls in close succession — a 13-agent run can approach the 5-hour rolling window on a Max plan. If you hit a rate limit mid-run, the SDK pauses until the window resets.

### Start a run

```bash
./council
```

The CLI asks for three things plus a council pick:

1. **Title** — one short headline. The slug is auto-derived.
2. **Thesis** — one to three sentences, sharp and falsifiable. Multi-line paste is fine.
3. **Scope** *(optional)* — paste a bulleted list of what the council should address. Skip to let the council scope itself from the thesis.
4. **Avoid** *(optional)* — paste a list of what the piece should refuse to be. Skip for the standard guardrails.
5. **Council composition** — pick a preset:
   - **All sixteen lenses** — every research agent
   - **Default seven (audit-tuned)** — the agents that consistently surface in synthesis, per [`council --audit`](#auditing-the-council): Tech Scout, Contrarian, Airport CEO, Airport COO, Infra Economist, Ops Analyst, Airline Commercial Strategist
   - **Operational focus** — Ops Analyst, Chief Engineer, COO, Public Safety, EM Director, Tech Scout
   - **Strategic focus** — CEO, COO, Regulatory, Airline Commercial, Infra Econ, Aviation Historian
   - **Custom** — grouped checklist where you toggle individual agents

Audience, tone (analytical sharp), and length (~9k-word report) use sensible defaults you can override by editing `prompts/runs/<slug>.md` before confirming. The CLI writes the run file, confirms the spec, clears any stale artifacts from `outputs/`, and starts Stage 1.

### Flags

| Flag | Effect |
| --- | --- |
| `--no-review` | Skip the initial spec confirmation and both human checkpoints. Runs fully autonomously. |
| `--resume SLUG` | Resume a previously interrupted run. Reads `prompts/runs/<SLUG>.md`, keeps existing `outputs/` artifacts, and re-runs only the steps whose output files are missing. |
| `--audit` | Scan all archived runs and produce a council-audit report. See [Auditing the council](#auditing-the-council). |
| `--publish [SLUG]` | Format archived full reports into polished, distribution-ready documents under `reports/`. See [Publishing reports](#publishing-reports). |
| `--dry-run` | Write the run file from your answers and stop without calling the model. Useful for previewing. |
| `--skip-prompts` | Alias for `--dry-run`. |
| `--help` | Print usage and exit. |

### Auditing the council

```bash
./council --audit
```

Scans every archived run under `runs/`, extracts objective signals (citation counts in the final draft, fact-check rejection counts, brief word volume, completion status), and produces a markdown report at `runs/_audit-YYYY-MM-DD.md`. The report ranks each agent by **citations per 1,000 brief words** — how often the Strategist surfaced an agent's work relative to how much that agent wrote — and flags agents that are underused, that produce a disproportionate share of fact-check rejections, or that have never been seated. Findings include actionable next steps pointing at specific `.claude/agents/*.md` files to edit.

The audit-tuned **Default seven** preset is derived directly from this signal. Re-run the audit after every few new archives and update [cli/interactive.py](cli/interactive.py)'s `PRESET_DEFAULT` to keep it aligned with reality.

### Publishing reports

```bash
./council --publish              # every archived run
./council --publish <slug>       # just one run
```

Takes the full report from each `runs/*/stage4/` folder (executive summaries are excluded) and produces a polished, distribution-ready `.docx` under a top-level `reports/` folder. The body is rebuilt cleanly from the run's `stage3/final-draft.md` so the published version doesn't inherit the stage4 file's own cover page and appendix. Each published report gets:

- A branded cover page — the logo at `assets/council-logo.png`, the report title, the subheading "An Analytical Report Generated by the AI Research Council", and a **FINAL — FOR DISTRIBUTION** mark. Typeset in Georgia with MWAA brand-navy headings.
- An **Abstract** page (drawn from the run's thesis and scope)
- A **How This Report Was Produced** page — the four-stage process, the exact research agents that were seated for that run (read from the run's `stage1/` brief filenames, so it reflects what actually ran), and a pointer to the full agent specifications at the [agents directory on GitHub](https://github.com/TransformAirports/ai-council/tree/main/.claude/agents)
- **Page numbers** in the footer
- An **AI-generation disclaimer** as the final section

To change the cover logo, replace `assets/council-logo.png` with a horizontal logo of your own (the build also accepts `assets/logo.png`). If neither exists, the cover renders cleanly without a logo. Typography and brand color are set at the top of [cli/publish.py](cli/publish.py) (`BODY_FONT`, `HEADING_FONT`, `BRAND_NAVY`).

Re-running is safe: it overwrites the polished file for each run in place. The `reports/` folder is yours to hand out; nothing else in the pipeline writes to it.

### Troubleshooting

- **Claude is not authenticated.** Either run `claude login` to use subscription credits, or export `ANTHROPIC_API_KEY` for API billing — you need one or the other in the shell session you run `council` in.
- **"Rate limit reached"** mid-run on a subscription plan. The SDK pauses until your Claude.ai rolling window resets. To finish faster, switch to an API key or deselect a few research lenses to shorten the run.
- **"outputs/ contains files from a previous run."** The CLI offers to clear them. Without `--no-review` it asks; with the flag it clears silently. To pick up where a crash left off, run `council --resume <slug>` instead.
- **An agent "completed" but did not write its output.** The orchestrator catches this and reports it clearly. It almost always means the agent exhausted its `max_turns` budget on file reads before reaching the Write step. Raising `max_turns` in `cli/orchestrator.py` or seating fewer research lenses resolves it.
- **The Word document looks rough.** The built-in markdown-to-docx is intentionally minimal — open the file in Word and apply your preferred styles, or polish the markdown in `outputs/stage3/final-draft.md` and rerun Stage 4 manually.

### Where the source files live

- `.claude/agents/` — the twenty agent definitions (sixteen research lenses plus the Strategist, Red Team, Editor, and Fact-checker)
- `cli/` — the Python CLI (entry point: `cli/__main__.py`)
- `prompts/runs/` — run-prompt files, one per thesis
- `prompts/orchestration.md` — the canonical four-stage sequence Claude Code reads
- `docs/methodology.md` — the methodology appendix attached to every published report
- `runs/` — archived deliverables, one folder per completed run
- `scripts/build_it_memo.py` — generator for the IT-department-facing memo
