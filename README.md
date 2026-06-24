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
| **Humanizer** | Post-editing pass that refines tone, readability, and writing quality — smooths the seams of multi-agent assembly without touching a single claim, number, or tag. |
| **Fact-checker** | Verifies every numerical and attributed claim against the research briefs — running **after** the Humanizer, so verification covers the final text. Has veto power over anything that cannot be sourced. |

All process agents run on Claude Opus 4.8. Model assignments per role live in `council.toml` and are editable from the hub's Settings menu — point any role at Sonnet for a cheap draft pass, then switch back.

#### The writer

The Strategist is the agent that turns whatever research lenses you seated into a single argumentative draft. There is one Strategist; it always runs once research is in.

| Agent | What it does |
| --- | --- |
| **Strategist** | Reads every research brief, writes the argumentative draft, and revises it in response to each Red Team pass. |

#### Pick your council — the research lenses

Nineteen research lenses are available. Seat as few or as many as the thesis warrants. Each one is biased by design — none are neutral — and each writes an independent brief without seeing the others. Fewer seats means a tighter scope and a cheaper run; more seats means more variance for the Strategist to argue against. Research briefs run on Claude Opus 4.8; the Deep Research lens routes to OpenAI instead and requires `OPENAI_API_KEY`.

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
| Airport Procurement Expert | Federal grant procurement, delivery-method selection, DBE, protest risk, the schedule arithmetic that turns a board vote into a buildable contract |
| Director of Public Safety | Airport police, ARFF, dispatch under one command; Part 139 and 1542 reality |
| Airport EM Director | Long-tenured airport EM perspective; real EOC activations and exercises |
| The Slacker | Gut thesis first, then a strict ten-minute research sprint, then a revised position — the intuition-vs-evidence delta no other agent generates |
| Virtual Christian | The operator's free-thinker voice modeled on the council's human; reframes the question instead of answering it head-on |
| Virtual Chris | Executive connector — maps the stakeholder lattice, initiative adjacencies, and cross-disciplinary patterns others miss; the council's optimist |
| Virtual Pat | Modern-day MacGyver — unconventional, low-cost, highly practical solutions built from assets the airport already owns |
| Deep Research (GPT-5.5 Pro) | Long-horizon, citation-dense research pass on OpenAI's deep-research model — a second model family's independent read (requires `OPENAI_API_KEY`) |

---

## 2. How to use it

A run starts with a sharp thesis. The sharper the thesis, the sharper the output. "An overview of regional airline trends" produces a summary. "Regional airline consolidation has gone far enough that the next wave of mergers will strand infrastructure the industry just built" produces an argument.

When you launch `./council`, it first asks whether you want to **create a new report** or **revise an existing one**. The new-report path is below; the revise path is in [Revising a report](#revising-a-report).

You can start a new run two ways:

- **The CLI (recommended).** Run `council` in the terminal. It walks you through the thesis, audience, tone, length, and which agents to seat on the Council, writes the run file for you, and drives the four stages end-to-end. Installation is in the next section.
- **Claude Code.** Write a run-prompt file in `prompts/runs/` by hand, then say "run \<filename\>" inside Claude Code. The conversational flow handles the same four stages.

Either path produces the same artifacts and the same archive layout. You can switch between them between runs.

### The four stages

**Stage 1 — Research** &nbsp;·&nbsp; *Parallel · Claude Opus 4.8 (Deep Research lens on OpenAI) · ~30–60 minutes*
The selected research agents work concurrently. Each produces an independent brief (typically 1,500–2,500 words) with inline source citations. They cannot read each other's output.

**Stage 2 — Synthesis and debate** &nbsp;·&nbsp; *Sequential · Opus 4.8 · ~60–90 minutes*
Strategist drafts v1, Red Team critiques v1, Strategist revises to v2, Red Team critiques v2, Strategist produces v3 with explicit handoff notes about anything it knowingly left in.

> **Human checkpoint #1.** The CLI shows you v3 and both critiques and asks whether to continue, redo the final draft with your notes, or stop. Pass `--no-review` to skip.

**Stage 3 — Edit, humanize, and fact-check** &nbsp;·&nbsp; *Sequential · Opus 4.8 · ~30–60 minutes*
The Editor cuts roughly a fifth of the word count, removes buzzwords, and flags hedges. The Humanizer then refines tone, readability, and writing quality without touching any claim, number, or tag. The Fact-checker runs last — verifying every numerical and attributed claim in the humanized text against the Stage 1 briefs. Unverifiable claims get cut or tagged `[UNVERIFIED — HUMAN REVIEW]`.

> **Human checkpoint #2.** The CLI shows you the final draft and the fact-check report. Pass `--no-review` to skip.

**Stage 4 — Word documents** &nbsp;·&nbsp; *Local generation · ~10 seconds*
The CLI builds two `.docx` files: a full report with cover page, table of contents placeholder, body, and methodology appendix; and a three-page executive summary distilled from the same final draft.

### After the run

The CLI archives everything to `runs/YYYY-MM-DD-<slug>/` with the four stage subfolders intact and writes a `retrospective.md` that includes the cost breakdown. It then clears `outputs/` so the next run starts fresh — and finishes by automatically publishing the polished, distribution-ready document to `reports/<slug>.docx`, styled for whichever output format the run used. One command in, finished document out.

A typical full run takes 2–4 hours of wall-clock time and costs roughly $40–60 in API spend. Reducing the number of research agents brings both down proportionally.

### An example you can read

The archived run at `runs/2026-04-17-infrastructure-vs-intelligence/` is the first complete Council deliverable. It tested the thesis that airports are over-investing in infrastructure and under-investing in operational intelligence, produced an 11,600-word report and a three-page executive summary, and verified 118 numerical claims against the briefs. Read it as a worked example of what a finished run looks like end-to-end.

---

## 3. Install and start the CLI

### Prerequisites

- macOS or Linux with Python 3.11 or newer (`python3 --version` to check)
- Either a Claude.ai subscription with Opus access **or** an Anthropic API key — see [Authenticate Claude](#authenticate-claude) below
- *(Optional)* `OPENAI_API_KEY` — only needed if you seat the Deep Research lens, which runs on OpenAI's deep-research model
- This repository cloned locally

### Install and run

One step. From the repository root:

```bash
./council
```

The first invocation creates a virtual environment, installs the Claude Agent SDK and the Word-document builder, and launches the CLI. Every subsequent invocation skips the install and goes straight to running. No `pip install`, no `source .venv/bin/activate`.

### Authenticate Claude

The CLI runs on the Claude Agent SDK, which uses the Claude Code CLI binary under the hood. That gives you two ways to pay for runs.

The easiest place to put keys: copy `.env.example` to `.env` at the repo root and fill in what you use. The CLI loads it automatically at startup (shell exports still win). `.env` is gitignored, so keys never end up in the repo.

| Option | How to set it up |
| --- | --- |
| **Subscription credits** (Claude.ai Pro, Max, Team, or Enterprise) | Sign into Claude Code once with `claude login`. Leave `ANTHROPIC_API_KEY` unset. Runs draw against your Claude.ai plan's usage allowance. |
| **Pay-as-you-go API key** (Anthropic API console) | Export `ANTHROPIC_API_KEY="sk-ant-..."` in your shell. Runs draw against your API console balance and the CLI reports per-step USD cost. |

> **Subscription caveats.** Stages 2 and 3 use Claude Opus, so your subscription needs Opus access (Max, or Team and Enterprise with Opus enabled; Pro alone is generally Sonnet-only and will not complete a full run). The Council also fires many calls in close succession — a 13-agent run can approach the 5-hour rolling window on a Max plan. If you hit a rate limit mid-run, the SDK pauses until the window resets.

### Start a run

```bash
./council
```

The CLI asks for:

1. **Title** — one short headline. The slug is auto-derived.
2. **Thesis** — one to three sentences, sharp and falsifiable. Multi-line paste is fine.
3. **Scope** *(optional)* — paste a bulleted list of what the council should address. Skip to let the council scope itself from the thesis.
4. **Avoid** *(optional)* — paste a list of what the piece should refuse to be. Skip for the standard guardrails.
5. **Output format** — the shape of the final deliverable:
   - **Full Research Report** (4,000–6,000 words)
   - **Long-Form Article** (1,500–2,000 words)
   - **Brief** (700–1,000 words)
   - **Concise recommendations** (numbered and actionable, 400–700 words)
6. **Council composition** — pick a preset:
   - **All standard lenses** — every Claude-native research agent
   - **Default seven (audit-tuned)** — the agents that consistently surface in synthesis, per [`council --audit`](#auditing-the-council): Tech Scout, Contrarian, Airport CEO, Airport COO, Infra Economist, Ops Analyst, Airline Commercial Strategist
   - **Operational focus** — Ops Analyst, Chief Engineer, COO, Public Safety, EM Director, Tech Scout
   - **Strategic focus** — CEO, COO, Regulatory, Airline Commercial, Infra Econ, Aviation Historian
   - **Custom** — grouped checklist where you toggle individual agents, including the OpenAI-hosted Deep Research lens
7. **Companion PowerPoint** *(yes/no)* — optionally generate an executive deck alongside the Word documents (or pass `--pptx`).

Audience and tone (analytical sharp) use sensible defaults you can override by editing `prompts/runs/<slug>.md` before confirming. The CLI writes the run file, confirms the spec, clears any stale artifacts from `outputs/`, and starts Stage 1.

### Source material

Drop files into the `sources/` folder at the repo root before launching a new run — PDFs, Word docs, PowerPoint decks, Excel sheets, markdown, plain text. The hub shows a `📎` badge as soon as files appear, and the first prompt in **New report** asks whether to attach them.

On accept, the CLI moves each file into the run's `outputs/sources/<slug>/` folder, converts `.docx` / `.pptx` / `.xlsx` to plain markdown sidecars (so every agent — including the OpenAI-hosted Deep Research lens, which has no file tools — can read them), and injects a preamble into every Stage 1 agent's prompt: *"Before you research anything, read these files first — treat them as the primary starting point and quote them directly."* The Stage 1 research is now grounded in your material, not just the open web.

The sources move out of the drop zone (it's free for the next run) and travel into the run archive at completion (`runs/<dated>/sources/`), so future revisions, audits, and re-publishes can still see what the Council was given.

Two limits worth knowing:
- **Scanned PDFs without a text layer** read as pixels, not words. Most modern PDFs are searchable and work fine; if Deep Research is seated and a scanned PDF is in the mix, convert it first.
- **Deep Research** can't read files directly — its prompt has the source text inlined, truncated at 30,000 characters per file. For very long documents, it sees the first portion.

### The hub

`./council` with no flags opens the interactive hub — the intended way to use the tool. It greets you with the Council's status (lenses, archives, latest run), **detects interrupted runs automatically** and offers to resume them first, and routes everything from one menu:

- **Resume interrupted run** — shown only when one is detected, with the stage it died at and how long ago. Completed steps are never re-run or re-billed. Clearing an interrupted run that contains synthesis work requires typing `CLEAR` — a stray Enter can't destroy paid output.
- **New report** — the five-question flow, then a single **pre-flight screen**: council roster, models, estimated cost range, auth status for both providers, checkpoint mode, budget ceiling, and deck option, all visible with one keystroke to launch and one place to adjust.
- **Revise a report**, **Build a deck for a finished report**, **Re-publish**, **Audit**, **Settings**.

After a run completes, a **what-next menu** closes the loop: open the published document, open or generate the executive deck, open the archive, or start a revision on the spot. Long runs end with a macOS notification.

Every run accepts a **budget ceiling** (default in Settings): the orchestrator checks spend between steps and halts cleanly with resume instructions if the ceiling is hit — completed work is never interrupted mid-call.

If a run fails, the CLI saves the technical detail to `logs/last-error.log` and tells you exactly what to do: relaunch and choose Resume.

### Settings — council.toml

Model assignments per role (research, synthesis, critique, editor, humanizer, fact-check, presentation), the per-agent turn budget, and the default cost ceiling live in `council.toml` at the repo root — created and edited from the hub's Settings menu, no Python required. Want a cheap draft run? Point `research` at Sonnet in Settings and switch it back after.

### Flags (deep links)

Every flag is a shortcut into the same flows the menu offers — nothing is flag-only.

| Flag | Effect |
| --- | --- |
| `--resume [SLUG]` | Jump to resume; auto-detects the interrupted run if no slug is given. |
| `--audit` | Jump to the council audit. |
| `--publish [SLUG]` | Jump to re-publish (all archives, or one slug). |
| `--revise [SLUG]` | Jump to revision (picker, or a specific report). |
| `--pptx` | Jump to deck-building for a finished run. |
| `--no-review` | Run autonomously where applicable (combined with `--revise`). |
| `--dry-run` / `--skip-prompts` | Collect a new run spec, write the run file, stop before any model call. |
| `--help` | Print usage and exit. |

### Auditing the council

```bash
./council --audit
```

Scans every archived run under `runs/`, extracts objective signals (citation counts in the final draft, fact-check rejection counts, brief word volume, completion status), and produces a markdown report at `runs/_audit-YYYY-MM-DD.md`. The report ranks each agent by **citations per 1,000 brief words** — how often the Strategist surfaced an agent's work relative to how much that agent wrote — and flags agents that are underused, that produce a disproportionate share of fact-check rejections, or that have never been seated. Findings include actionable next steps pointing at specific `.claude/agents/*.md` files to edit.

The audit-tuned **Default seven** preset is derived directly from this signal. Re-run the audit after every few new archives and update [cli/interactive.py](cli/interactive.py)'s `PRESET_DEFAULT` to keep it aligned with reality.

### Publishing reports

Publishing happens **automatically at the end of every run** — the pipeline's final step writes the polished document to `reports/`. The flag exists for re-publishing and backfill:

```bash
./council --publish              # re-publish every archived run
./council --publish <slug>       # re-publish one run
```

The treatment adapts to the run's output format:

| Format | Treatment |
| --- | --- |
| Full Research Report | Cover page, abstract page, methodology page, body, full-page disclaimer |
| Long-Form Article | Cover page, body, compact production colophon, inline disclaimer |
| Brief | Compact page-one title block (no cover), body, colophon, inline disclaimer |
| Concise recommendations | Same compact treatment as Brief |

All formats get Georgia typography, brand-navy headings, page numbers, and the AI-generation disclaimer. The publisher rebuilds the body from each run's `stage3/final-draft.md` (executive summaries are excluded) and writes to a top-level `reports/` folder. The body is rebuilt cleanly from the run's `stage3/final-draft.md` so the published version doesn't inherit the stage4 file's own cover page and appendix. Each published report gets:

- A branded cover page — the logo at `assets/council-logo.png`, the report title, the subheading "An Analytical Report Generated by the AI Research Council", and a **FINAL — FOR DISTRIBUTION** mark. Typeset in Georgia with MWAA brand-navy headings.
- An **Abstract** page (drawn from the run's thesis and scope)
- A **How This Report Was Produced** page — the four-stage process, the exact research agents that were seated for that run (read from the run's `stage1/` brief filenames, so it reflects what actually ran), and a pointer to the full agent specifications at the [agents directory on GitHub](https://github.com/TransformAirports/ai-council/tree/main/.claude/agents)
- **Page numbers** in the footer
- An **AI-generation disclaimer** as the final section

To change the cover logo, replace `assets/council-logo.png` with a horizontal logo of your own (the build also accepts `assets/logo.png`). If neither exists, the cover renders cleanly without a logo. Typography and brand color are set at the top of [cli/publish.py](cli/publish.py) (`BODY_FONT`, `HEADING_FONT`, `BRAND_NAVY`).

### Revising a report

When a reader gives feedback on a finished report, you don't re-run the whole Council. A revision reuses the original research and applies a focused pass.

```bash
./council                  # then choose "Revise an existing report"
./council --revise         # jump straight to the report picker
./council --revise <slug>  # revise a specific report
```

You pick the report the feedback is about (a scrollable list), type the feedback, and the Council runs a tight loop on the **existing draft plus your feedback**:

> Strategist (revise) → Red Team (critique) → Strategist (finalize) → Editor → Fact-checker

It reuses the original Stage 1 research briefs — no new research, no ten-agent run — so a revision is a handful of Opus calls rather than a multi-hour job. The result is a polished `reports/<slug>-revised-vN.docx`, stamped **Revised — Version N** on the cover.

Revisions chain: the first is v1, the next is v2, and each one revises the previous version's output rather than the original. The intermediate drafts, the critique, and the feedback that prompted each revision are preserved under `runs/<run>/revisions/vN/` for provenance. Add `--no-review` to skip the pre-build review of the revised draft.

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
