# The Transform Airports AI Council

**Ask one sharp question about the airport industry. Get back a fascinating,
source-checked narrative built by an independent research swarm, curated
evidence, two different adversarial reviews, primary-source verification, and
visual production QA. Add a formal decision frame only when you need one.**

The Council exists because a single AI, asked to write a long analytical
piece, can produce something fluent and subtly useless: it hedges, flatters the
question, and smooths over objections. The Council is designed to prevent that.
Researchers investigate independently. Their findings become a structured
evidence ledger. One reviewer prosecutes the evidence; another tests whether
the recommendations survive airport governance and operating reality. A source
verifier checks the final reader-facing draft. Deterministic gates stop
publishing defects.

The default deliverable is a 1,500–2,000-word Narrative Feature: one continuous,
enjoyable argument with no decision-card catalog or technical appendix. The
operator can instead choose a full report, brief, or recommendations and can
opt into a named decision frame. PowerPoint remains optional.

---

## Start it on a new machine

The shortest safe path is:

```bash
git clone https://github.com/TransformAirports/ai-council.git
cd ai-council
./council --doctor
./council
```

Before the doctor can pass, install Python 3.11+, Claude Code, LibreOffice, and
Poppler, then sign in with `claude auth login` (or configure an Anthropic API
key). The first launch creates the local virtual environment automatically.
The doctor is read-only and makes no model call.

Follow the copy-and-paste macOS and Ubuntu path in
**[Get the AI Council running](docs/getting-started.md)**. It covers Claude
subscription versus API billing, optional OpenAI Deep Research, first-run
expectations, output locations, resuming failures, and Office-rendering fixes.

---

## How a run works

1. **Frame the decision.** State a contested thesis, the airport decision it
   should inform, the likely owner, horizon, approval route, and definition of
   success.
2. **Assemble current airport context.** The Context Builder reads supplied
   material and authoritative public records before the swarm begins.
3. **Run the independent research swarm.** Every seated researcher writes a
   brief and structured evidence records without reading the others.
4. **Curate and challenge the evidence.** The Evidence Curator deduplicates,
   ranks, and reconciles the record, then closes only load-bearing gaps.
5. **Choose a creative frame.** The Creative Director proposes board-ready,
   counterintuitive, and operational narrative options grounded in the same
   evidence.
6. **Write, prosecute, and revise.** The Strategist drafts; the Evidence
   Prosecutor attacks source use and reasoning; the Strategist revises; the
   Airport Executive Reviewer attacks feasibility; the Strategist revises
   again.
7. **Edit and verify.** The Editor and Humanizer refine the prose. The Source
   Verifier checks the underlying evidence and primary sources, then creates
   claim lineage.
8. **Produce and inspect.** Publishing gates block internal labels,
   placeholders, citation defects, and release errors. The Art Director and
   production agents build the executive packet and render it for QA.

The web app streams agent, artifact, evidence, cost, and quality-gate telemetry.
A refreshed browser can reconnect to a live run.

In plain English, the architecture uses:

- **Parallel research swarm** — independent specialists investigate the same
  decision at the same time, without copying one another.
- **Adversarial synthesis loop** — the argument is written, attacked from two
  different directions, and rewritten after each attack.
- **Multi-model orchestration** — different model families are assigned to
  research, writing, critique, and verification so one model does not grade
  all of its own work.
- **Live agent telemetry** — the operator sees who is working, what passed
  validation, where evidence is thin, and what has been spent while the run is
  happening.

---

## Meet the Council

The repository defines 54 agents: 20 airport research lenses, 18 supplemental
thinkers, and 16 process agents for context, curation, writing, review,
verification, design, production, revision, and scope fulfillment.

### The writing & quality team — on every report

| Agent | Role |
|---|---|
| **Airport Context Builder** | Assembles current governance, finance, capital, airline, regulatory, and operating facts from supplied and authoritative sources. |
| **Evidence Curator** | Normalizes the swarm's structured evidence, ranks what is load-bearing, preserves disagreement, and closes targeted gaps. |
| **Creative Director** | Develops three truthful narrative and visual approaches before the report's structure hardens. |
| **The Strategist** | Builds the argument from curated evidence and revises it after each specialized adversarial review. |
| **Evidence Prosecutor** | Attacks source quality, arithmetic, causal claims, stale data, cherry-picking, and missing counterevidence. |
| **Airport Executive Reviewer** | Tests ownership, approvals, funding, airline response, procurement, delivery, and peak-hour operating reality. |
| **The Editor** | Cuts 15–25% of the word count, kills jargon and filler, sharpens every sentence. Adds nothing. |
| **The Humanizer** | Rewrites the edited draft to the standard of a Harvard Business Review feature — so the final piece reads like one excellent writer produced it, not a committee. |
| **The Source Verifier** | Verifies the final draft against the evidence ledger and underlying primary sources. Anything unsupported gets cut, qualified, or flagged. |
| **The Art Director** | Defines the visual argument, signature exhibit, slide density, report visuals, sources, and accessibility checks. |
| **The Presentation Designer** | On request, distills the finished report into an elegant executive slide deck. |

### The research lenses — you choose who sits

**Economics & industry**

| Agent | What they bring |
|---|---|
| **Infrastructure Economist** | Airport capital spending, project economics, cost overruns, and what infrastructure investment actually returns. |
| **Airline Commercial Strategist** | How airlines think: hub economics, route networks, cost sensitivity, and how carriers respond to airport decisions. |
| **Aviation Historian** | The long arcs — deregulation, consolidation waves, boom-and-bust construction cycles — and which past moments genuinely rhyme with today. |
| **The Contrarian** | Builds the strongest possible case *against* your thesis. If the argument survives the Contrarian, it's ready for skeptical readers. |

**Operations & engineering**

| Agent | What they bring |
|---|---|
| **Operations Analyst** | Throughput, delays, gate utilization — and whether the real bottleneck is infrastructure or how it's operated. |
| **Quantitative Analyst** | Reproducible calculations, scenarios, sensitivity tests, and chart-ready airport data with explicit inputs and formulas. |
| **Chief Engineer** | Twenty-five years of program delivery: constructability, lifecycle cost, design standards, and how megaprojects actually fail. |
| **Technology Scout** | What airport technology — sensors, biometrics, predictive analytics — actually costs and actually returns once deployed, versus what the brochure said. |
| **Architectural Historian** | Airport terminals as architecture: the design intent behind the great buildings, and what gets lost when operations forget it. |

**Executive leadership**

| Agent | What they bring |
|---|---|
| **Airport CEO** | The chief executive's chair: board accountability, bond ratings, airline agreements, and the politics above operations. |
| **Airport COO** | The operator's chair: airfield, terminals, maintenance, airline relations — whether the plan works at 5:45 AM on a Monday, not just on paper. |
| **Airport Procurement Expert** | The discipline that turns a board vote into a signed contract: federal grant rules, delivery methods, protest risk, and the schedule math master plans understate. |
| **Regulatory & Political Analyst** | The FAA, TSA, Congress, and local politics — which constraints are actually binding and on what timeline anything can change. |

**Public safety & emergency management**

| Agent | What they bring |
|---|---|
| **Director of Public Safety** | Airport police, fire/rescue, and 911 dispatch under one command — response capability, staffing reality, and federal certification. |
| **Airport EM Director** | Decades of real emergency activations: what actually happens in the operations center during the first 30 minutes, versus what the plan says. |

**Out-of-the-box thinkers**

| Agent | What they bring |
|---|---|
| **The Slacker** | Deliberately unprepared. Writes a gut reaction first, then gets exactly ten minutes of research to test it — and reports honestly what survived. The gap between instinct and evidence is signal no other agent produces. |
| **Virtual Christian** | Modeled on the Council's human operator: a free-thinking airport operations leader who connects dots across domains and reframes the question until you say "huh — I hadn't thought of it that way." |
| **Virtual Chris** | The executive connector — finds the alliances, adjacencies, and openings others miss, drawing on history, politics, culture, and science. The council's optimist. |
| **Virtual Pat** | A modern-day MacGyver: unconventional, low-cost, highly practical solutions built from things the airport already owns. Always has the "here's the version that costs 2% as much" answer. |

**Extended research**

| Agent | What they bring |
|---|---|
| **Deep Research** | Runs on OpenAI's deep-research model instead of Claude — a second AI family's independent, exhaustive read of the same question. Optional; requires an OpenAI account. |

### The supplemental council — eighteen great minds, on call

For questions that deserve a perspective from outside aviation, you can seat legendary thinkers — each one a faithful rendering of how that mind worked, adapted from the open-source [Council of High Intelligence](https://github.com/0xNyk/council-of-high-intelligence).

| Thinker | The way they see |
|---|---|
| **Ada Lovelace** | The first to see computation as abstraction, not just arithmetic. |
| **Aristotle** | The taxonomist who insists understanding begins with classification. |
| **Marcus Aurelius** | Emperor and philosopher, who governs himself before governing others. |
| **Richard Feynman** | The physicist who won't accept what he can't explain simply. |
| **Daniel Kahneman** | Proved judgment is systematically irrational; names the biases. |
| **Andrej Karpathy** | The neural-net whisperer who knows how AI actually learns and fails. |
| **Lao Tzu** | The sage who sees the problem is often the intervention itself. |
| **Machiavelli** | The realist who reads how people and institutions actually behave. |
| **Donella Meadows** | The systems thinker who finds the leverage points others miss. |
| **Charlie Munger** | The polymath who triangulates truth across many mental models, by inversion. |
| **Miyamoto Musashi** | The undefeated swordsman who reads timing, position, and rhythm. |
| **Dieter Rams** | The designer who believes good design is as little design as possible. |
| **Socrates** | The gadfly who destroys false certainty by testing every premise. |
| **Sun Tzu** | The strategist who sees position, timing, and information in any contest. |
| **Ilya Sutskever** | The researcher at the frontier between capability and catastrophe. |
| **Nassim Taleb** | The scholar of fragility, robustness, and antifragility under uncertainty. |
| **Linus Torvalds** | The engineer who builds things that work and ships them. |
| **Alan Watts** | The philosopher who dissolves problems by reframing how we see them. |

---

## What you get

- **Executive read-ahead** (Word) — the polished argument, cases, citations,
  decision cards, and methodology.
- **Decision brief** (Word) — the decision, evidence, recommendation, risks,
  owner, approval route, first 90 days, and measures.
- **Technical evidence appendix** (Word) — sources, assumptions, evidence gaps,
  calculations, and verification record.
- **Companion deck** (PowerPoint, optional) — board decision, executive
  briefing, or technical read-ahead mode.
- **Full internal provenance** — run manifest, airport context, briefs,
  evidence ledger, narrative options, drafts, critiques, claim lineage,
  verification, quality gates, human scores, and cost.

Every report ends with a clear disclaimer that it was produced by AI, and every number in it traces to a source or is flagged for human review.

---

## Using it

From the project folder, run:

```bash
./council
```

Your browser opens to the Council's web app. From there, everything is guided:

- **Home** — your library of finished reports, and a one-click resume if a run was ever interrupted.
- **New report** — a three-step wizard: frame the question (with a built-in writing guide and tips under every field), choose your council (with a live cost estimate as you pick), review and launch.
- **The live run** — watch the council work as a constellation: agents light up as they research, evidence streams toward the center, the cost ticks in real time. When it's your turn to review, the draft and critiques appear side by side for your decision.
- **The result** — read the finished report right in the app, download the documents, revise it from feedback, or build the deck.

The app estimates cost from the selected council before launch and enforces the
budget ceiling between steps. Council v2 spends more of the budget on
curation, verification, and production instead of simply adding research
volume.

**The one skill worth learning:** how you frame the question determines everything. The short version — make a claim someone could disagree with, not a topic. The full craft is in [Writing effective run prompts](docs/writing-effective-run-prompts.md), and the same guidance is built into the app.

---

<details>
<summary><b>⚙️ Setup & technical reference</b> (for whoever administers this)</summary>

### Prerequisites

- macOS or Linux with Python 3.11+ (`python3 --version` to check)
- A Claude subscription with Opus access (sign in once with `claude auth login`) **or** an `ANTHROPIC_API_KEY`
- LibreOffice (`soffice`) and Poppler (`pdftoppm`) for mandatory rendered QA
- `OPENAI_API_KEY` for the GPT-5.6 Sol Prompt Coach; also used when you seat the Deep Research lens
- This repository cloned locally

The first `./council` creates a virtual environment and installs everything automatically. No manual `pip install`.

Run `./council --doctor` before the first report. The complete installation
path is in [docs/getting-started.md](docs/getting-started.md).

### API keys

Copy `.env.example` to `.env` at the repo root and fill in what you use. The CLI loads it automatically; shell exports win over `.env` values. `.env` is gitignored.

### Model routing

Every process role has an explicit model assignment in `council.toml`: context,
research, curation, creative framing, synthesis, evidence critique, executive
review, editing, humanization, source verification, art direction, and
presentation. The defaults deliberately vary model families across writing and
verification. The optional Deep Research lens runs on OpenAI's
`o3-deep-research`.

### Command-line deep links

`./council` with no flags opens the web app. Every flow is also reachable headless:

| Flag | Effect |
|---|---|
| `--doctor` | Read-only setup check for Python, Claude authentication, LibreOffice, Poppler, packages, writable folders, disk, and model configuration. Makes no model call. |
| `--run FILE` | Validate and execute a prepared file inside `prompts/runs/` through the canonical pipeline. |
| `--budget USD` | Set a finite Claude-spend ceiling for `--run` or `--pptx`; zero permits no Claude calls. OpenAI Deep Research is billed separately. |
| `--terminal` | The full menu in the terminal instead of the browser (SSH / no-browser use). |
| `--resume [SLUG]` | Resume an interrupted run; auto-detects if no slug given. Completed steps are never re-run or re-billed. |
| `--revise [SLUG]` | Revise an existing report from reader feedback. |
| `--publish [SLUG]` | Re-publish the exact QA-approved Office artifacts from the latest matching archive. |
| `--allow-legacy-publish` | With `--publish`, explicitly permit a pre-v2 archive with no hash-bound release; the Office file is rendered and QA'd again before publication. |
| `--pptx [SLUG]` | Build an executive deck for a finished run. Failed deck builds resume from durable, input-bound staging instead of repeating completed paid work. |
| `--audit` | Evaluate evidence lineage, primary-source coverage, verification outcomes, cost, completion, and human quality scores across archived runs. |
| `--dry-run` | Create a new run file interactively and stop before any AI calls. It cannot be combined with `--run`. |

### Source material

Drop PDFs, Word docs, decks, or spreadsheets into `sources/` before launching. The app detects them, moves them into the durable `sources/runs/<slug>/` library, converts them to text the agents can read, and instructs every researcher to treat them as the primary starting point. Symlinks and path escapes are rejected. The same source bytes are fingerprinted, rechecked before release, and copied into the archive, so the saved run prompt remains rerunnable after `outputs/` is cleared.

### Scope mode — fulfilling an entire engagement

Beyond single reports, the Council can fulfill a full scope of work. Drop the scope document (an RFP, SOW, or emailed scope) into `sources/`, open **Fulfill a scope** in the app, and:

1. A **Scope Planner** reads the scope and produces a deliverables plan — every required artifact enumerated with type, dependencies, and build instructions, plus an honest list of client materials the scope assumes but that weren't supplied.
2. **You approve the plan** before production spends anything (redo-with-notes supported).
3. **Scope Researchers** answer the plan's regulatory and best-practice questions in parallel, citation-first.
4. **Scope Builders** produce every artifact — Word documents and PowerPoint decks — in dependency order, aligning each with the artifacts it builds on. Missing client-specific material becomes marked `[AUTHORITY-SPECIFIC — INSERT: …]` placeholders, never invented content.
5. A **Scope QA** agent audits the finished set against the original scope — a requirement-by-requirement acceptance trace — and you review it before packaging.

Everything lands in `reports/scope-<name>/` plus a single zip, with a manifest
and the QA report. The app authorizes that ZIP through a dedicated hash-bound
Scope pointer and keeps the engagement in the Library after reload; it never
opens a general ZIP download path. Re-running the same engagement title safely
resumes paid work only when the exact source bytes, operator notes, plan,
research, dependent artifacts, model route, agent charter, and execution
contract still match. A changed input quarantines and rebuilds only the
affected work; packaging and archiving are hash-verified before `outputs/` is
cleared. Headless: `./council --scope "Engagement name" --no-review`.

Scope engagements are large runs — budget accordingly (the default ceiling for scope mode is $250) and treat the output as consultant-grade *drafts*: AI-produced engagement materials that need subject-matter-expert review before client delivery.

### Argument mode — strengthening a focused case

Open **Strengthen an argument** in the app when the desired outcome is a
concise case rather than a long-form report. Paste the existing argument,
attach supporting documents, or do both; describe what needs stronger proof;
then choose the research agents whose lenses fit the question. The Council
runs one focused research wave, then ranks the evidence and rewrites the case
in a single synthesis pass. The fast default seats four lenses in one parallel
wave; the balanced and full rosters remain available. The release is an exact
one-page, source-checked Word memo (350–550 words), with the verified Markdown
kept in the app reader.

A six-slide PowerPoint is selected by default and can be turned off or changed
to any exact count from 3 to 30. Its claim-stakes-mechanism-proof-objection-ask
sequence uses assertion headlines, one visual idea per slide, and a lower text
density than the full report decks. The presentation contract, production
checks, and release gate enforce the requested count. Argument releases are
hash-bound, archived, and kept in the Library alongside report and scope
releases.

### The pipeline, precisely

Four public stages, with typed artifacts between them:

1. **Context, research, and curation:** Airport Context Builder → parallel
   independent research briefs plus per-agent evidence JSONL → evidence ledger
   and evidence map.
2. **Creative synthesis and two adversarial reviews:** Creative Director →
   Strategist v1 → Evidence Prosecutor → Strategist v2 → Airport Executive
   Reviewer → Strategist v3 → **human checkpoint #1**.
3. **Edit and source verification:** Editor → Humanizer → Source Verifier →
   claim lineage and publishing quality gate → **human checkpoint #2**.
4. **Production and release:** Art Director → Word executive packet → full-size
   Word page and sequence inspection with a hash-bound receipt → optional
   PowerPoint → mode-specific structural QA → canonical signature-slide,
   full-size slide, and montage inspection with a hash-bound receipt → exact-byte release staging
   and hash verification → archive-destination reservation → immutable,
   hash-named release bundle plus an atomic current-release manifest →
   atomic archive and retry-safe workspace cleanup.

The run manifest records every selected agent, model, input, output,
validation result, dependency receipt, and stage status. It also fingerprints
the Council code, agent charters, research contract, and visual design system
that shaped the run. Budget ceilings are enforced between calls; interrupted
runs resume only when both the artifact bytes and the exact upstream bytes
still match. A partial run cannot silently combine outputs from two Council
versions.

### Revising a report

A revision doesn't re-run the research swarm. It reuses the archived evidence
and runs a focused loop—Strategist revision, adversarial review,
Editor/Humanizer, fresh source verification, deterministic release gate, new
Art Director brief, rendered Word QA, and exact-byte release—producing
`reports/<slug>-revised-vN.docx` and, for full reports, a revised executive
summary. Revisions chain: v2 builds on v1. Each released version appears as its
own Library entry with its revised reader-facing draft and hash-verified
downloads; the **Revise** action still targets the original archive so the
next version follows the verified revision chain.

### The council audit

`--audit` never searches public prose for agent names. It attributes an agent's
contribution only when an evidence ID connects that agent's record to a final
claim. It reports commissioned and used evidence, primary-source-checked claim
coverage, verified/qualified/removed/unverified outcomes, correction rate,
cost, stage completion, and human scores for originality, airport specificity,
decision usefulness, writing, and visual quality. Legacy runs remain visible
and say "data unavailable" where they lack structured provenance.

### Where things live

| Path | Contents |
|---|---|
| `.claude/agents/` | All 54 agent definitions — versioned markdown, human-edited source of truth |
| `.codex/agents/` | Generated Codex-native mirrors of the same definitions |
| `cli/` | The engine and web app (`cli/server.py`, `cli/webapp/`) |
| `prompts/runs/` | One run-prompt file per question |
| `docs/` | The [writing guide](docs/writing-effective-run-prompts.md) and the [methodology](docs/methodology.md) that appears in every report |
| `runs/` | Complete archives: manifest, context, evidence, lineage, reviews, drafts, critiques, verification, QA, and documents |
| `reports/` | Polished, distribution-ready documents (regenerated on demand; not committed) |
| `council.toml` | Operator config: models per role, budgets, defaults |

### Governance

Agents never edit themselves or each other. Behavior changes go through human-reviewed edits to the files in `.claude/agents/` — see [how to propose an agent change](docs/how-to-propose-an-agent-change.md). The methodology appendix in every published report discloses exactly how the document was produced.

</details>

---

*Built by the Office of Strategy and Operational Performance, Metropolitan Washington Airports Authority. Reports are AI-produced drafts for human review — AI assistance does not reduce human accountability for what gets published.*
