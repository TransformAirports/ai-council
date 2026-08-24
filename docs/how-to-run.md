# How to run the Council

The Council turns a contested airport question into a sourced executive
decision package. You frame the decision, choose the research lenses, and
review two checkpoints. The system handles research, synthesis, challenge,
source verification, document production, visual QA, archiving, and cleanup.

## Start with a decision, not a topic

A useful run prompt answers six questions:

1. What claim should the Council test?
2. What airport decision should the work inform?
3. Who owns that decision?
4. What is the time horizon?
5. What approvals or stakeholders can change the outcome?
6. What observable result would count as success?

“Airport biometrics” is a topic. “Large hubs should stop treating biometrics as
a checkpoint project and fund it as shared passenger-processing
infrastructure” is a thesis. The second gives researchers something to test and
executives something to decide.

Use the guided **New report** flow in the web app, copy
[`prompts/runs/_template.md`](../prompts/runs/_template.md), or describe the
question conversationally and ask Codex to create a run.

Place useful source files in `sources/` before launch. The Airport Context
Builder will use them as the starting record and distinguish supplied facts
from public-source research.

## Launch

From the repository root:

```bash
./council
```

The browser app guides framing, council selection, cost estimation, launch,
live monitoring, checkpoint review, and download.

To trigger a prepared run conversationally, say:

> `run <filename>`

The filename may include or omit `prompts/runs/` and `.md`. The system validates
the prompt before it spends money. The direct headless equivalent is:

```bash
./council --run prompts/runs/<name>.md --budget 80
```

`--budget` is an execution guardrail in USD-equivalent units for Claude calls
across the parallel swarm and downstream process. GPT-5.6 Sol runs use the
ChatGPT plan's own usage limits and do not reserve API dollars. `--dry-run` is
a different mode: it creates a new run file interactively without model calls
and cannot be combined with `--run`.

## What happens during a run

### 1. Context, research, and evidence curation

The Airport Context Builder assembles the decision environment: governance,
capital program, airline agreements, finance, regulation, procurement,
operating constraints, and supplied facts.

The selected researchers then run as a **parallel research swarm**. That means
several specialists investigate the same question at the same time, from
different professional viewpoints, without reading one another’s conclusions.
Each produces a narrative brief and structured evidence records.

The Evidence Curator combines those records into an evidence ledger,
deduplicates sources, preserves genuine disagreement, scores source strength,
and commissions only targeted gap-filling research.

### 2. Creative framing and adversarial synthesis

The Creative Director proposes several truthful ways to tell the story,
including a counterintuitive frame, an airport-operating frame, and a
board-decision frame.

The **adversarial synthesis loop** then develops the report:

1. The Strategist drafts from the context and curated evidence.
2. The Evidence Prosecutor attacks source quality, arithmetic, causal logic,
   and omitted counterevidence.
3. The Strategist revises.
4. The Airport Executive Reviewer attacks feasibility: authority, airline
   response, funding, procurement, staffing, approvals, and peak-hour
   operations.
5. The Strategist revises again.

This is adversarial because the reviewers are assigned to find failure, not to
agree politely. It is a loop because the writer must answer the findings in a
new draft.

**Human checkpoint 1:** review the argument before editorial polish. Score
originality, airport specificity, decision usefulness, and writing. Ask:

- Is the recommendation a decision, or merely an aspiration?
- Does the evidence change what an airport executive should do?
- Did the report preserve the strongest counterargument?
- Are owner, approval route, timing, operating consequence, and success
  measure explicit?

### 3. Editing, source verification, and release gate

The Editor cuts repetition and consultant language. The Humanizer makes the
piece read as one authoritative writer rather than a committee transcript.

The Source Verifier checks reader-facing claims against the evidence ledger and
the underlying primary sources. It records claim-to-evidence lineage and marks
each claim verified, qualified, removed, or unresolved.

A deterministic publication gate then blocks unresolved placeholders, leaked
internal filenames, broken footnotes, unsupported numeric claims, and other
release defects.

**Human checkpoint 2:** review the final argument, source-verification report,
and remaining limitations before approving production.

### 4. Executive production and visual QA

The Art Director creates a visual contract: information hierarchy, signature
exhibit, source treatment, chart plan, accessibility, and slide-density rules.
The production layer builds the Word package and, when requested, a PowerPoint
in board-decision, executive-briefing, or technical-read-ahead mode.

Every generated Office file is reopened and structurally checked. Rendered
pages and slides are inspected for overflow, clipping, weak hierarchy,
unreadable density, and accidental internal content. A release fails when a
hard defect remains.

## Live agent telemetry

The run screen shows **live agent telemetry**: which agent is working, which
artifact it is producing, how the evidence ledger is changing, current cost,
and the state of each quality gate. It is the Council’s instrument panel. If
the browser refreshes, it reconnects to the active run without restarting
completed work.

Each new report uses **one model across many separated roles**. At setup, choose
Claude Fable 5 or GPT-5.6 Sol. That same model performs research, synthesis,
adversarial review, source verification, and production. The run manifest
records the selection, provider, and prompt hash for every commissioned agent.

## What good looks like

- Independent briefs disagree for intelligible reasons.
- The evidence ledger distinguishes primary evidence, secondary reporting,
  calculations, and analyst judgment.
- The strongest objection changes the final recommendation.
- Airport authority, airline behavior, financing, procurement, regulation,
  and day-of-operations consequences are named where they matter.
- Recommendations identify an owner, approval route, first action, time
  horizon, measure, and stop or reconsider condition.
- Visuals explain a comparison, sequence, tradeoff, or decision; they do not
  merely decorate the page.
- Every consequential number reaches a primary source or is explicitly
  qualified.

## What bad looks like

- Multiple agents repeat the same source and conclusion.
- Critiques say “consider adding” without naming the defect and remedy.
- The report offers generic “airports should” advice with no accountable owner.
- A chart lacks a source, unit, date, or decision point.
- The prose names agents, briefs, stages, or internal files.
- The deck is a document pasted onto slides.

## After completion

The Council automatically archives the complete internal record under
`runs/YYYY-MM-DD-<slug>/`, publishes distribution-ready files to `reports/`,
writes a retrospective, and clears the working output area.

Published downloads come from a hash-verified, immutable release bundle. If a
deck is added later, its Art Director brief, package, rendered QA, and release
record are staged durably under `logs/deck-backfills/<slug>/`; a failed build
resumes there under the same budget and does not partially rewrite the archive.
Pre-v2 archives without this release record are refused by default. Use
`--allow-legacy-publish` only when you intentionally want the system to render
and QA an older Office file again.

Before external release, a named human remains accountable for the argument,
source choices, redactions, and recommendations. Record the five quality
ratings—originality, airport specificity, decision usefulness, writing, and
visual quality—so the audit can show whether the system is improving across
runs.

Use `./council --audit` to review evidence use, primary-source coverage,
verification outcomes, corrections, cost, completion, and human quality scores.
