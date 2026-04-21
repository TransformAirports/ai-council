# How to Run the Council

A practical operator's guide. Two or three minutes to read before your first run.

## The mental model

Treat the repo like a Claude Code app. You write a run-prompt file describing what you want to think about. You tell Claude Code to run it. It runs for 2-4 hours. You show up twice to review and approve. It hands you back two Word documents and a fully archived run folder.

Everything else — research, adversarial revision, editing, fact-checking, Word generation, archiving — is the Council's job, not yours.

## The flow, end to end

### Step 1. Write the run-prompt file

Copy [`prompts/runs/_template.md`](../prompts/runs/_template.md). Rename the copy to something short and descriptive: `airline-consolidation.md`, `biometric-risk.md`, `cargo-revenue-collapse.md`. Fill in every section in your editor of choice. The sections are: thesis, audience, tone, length, what it is NOT, what it IS, optional operator-specific framing, success criteria, optional research-agent overrides.

The most important field is the **thesis**. A sharp falsifiable claim produces a sharp argument. A topic produces a generic summary. If you find yourself writing "an overview of..." or "trends in...", stop and sharpen.

If you'd rather dictate the thesis conversationally instead of editing a file, skip step 1 and say "let's do a new Council run" in Claude Code. Claude will interview you and write the file for you.

### Step 2. Trigger the run

In Claude Code in this repo, say:

> `run <your-filename>`

You can write it with or without the `.md` extension, with or without the `prompts/runs/` prefix. All of these work:

- `run airline-consolidation`
- `run prompts/runs/airline-consolidation.md`
- `let's run the airline-consolidation file`

Claude confirms the thesis in one sentence and an estimate of time and cost, then kicks off Stage 1.

### Step 3. Stage 1 runs (parallel research, ~60-90 min)

Eight agents research independently — they do not read each other's work.

- `infrastructure-economist` — airport CapEx, cost overruns, debt service
- `operations-analyst` — delay data, throughput, latent capacity
- `technology-scout` — what operational technology actually costs and returns
- `contrarian` — the strongest case against the thesis
- `chief-engineer` — constructability, lifecycle cost, design standards
- `airline-commercial-strategist` — carrier economics, hub decisions, CPE sensitivity
- `regulatory-political-analyst` — FAA, TSA, CBP, Congress, local politics
- `aviation-historian` — long-cycle industry arcs, pattern-matching

**What to look for:** eight briefs, each 1,500-2,500 words, each with inline source citations. If any brief is shorter, has no sources, or reads like a summary of a summary, Claude should re-run that agent before proceeding.

### Step 4. Stage 2 runs (synthesis and adversarial debate, ~60-90 min)

- Strategist produces draft v1
- Red Team critiques v1
- Strategist revises to v2
- Red Team critiques v2
- Strategist produces v3

**★ Human checkpoint #1.** Read v3. Read both critiques. Decide whether to continue.

Questions to ask yourself at this checkpoint:

- Is the thesis still sharp, or has the argument softened into mush?
- Did the Strategist actually address the Contrarian's strongest points, or did it steamroll them?
- Are there any numerical claims that raise an eyebrow? (Flag them for the Fact-checker.)
- Is the operator-specific implications section specific enough, or is it generic consultant-speak?

If anything is off, redirect before approving. Tell Claude what to change and it will loop back to the right step.

### Step 5. Stage 3 runs (polish, ~30-60 min)

- Editor cuts 15-25% and kills buzzwords
- Fact-checker verifies every number, tags `[UNVERIFIED — HUMAN REVIEW]` on analyst-derived claims

**★ Human checkpoint #2.** Read the fact-check report. Decide whether to proceed to Word generation or push back for another revision.

### Step 6. Stage 4 runs (Word documents, ~5 min)

Two deliverables land in `outputs/stage4/`:

- `<slug>.docx` — full report with cover page, table of contents, body, methodology appendix
- `<slug>-executive-summary.docx` — three-page standalone distillation

### Step 7. Archive (automatic)

Claude copies `outputs/` to `runs/YYYY-MM-DD-<slug>/`, writes a short `retrospective.md`, and clears `outputs/` for the next run. You don't have to do any of this manually.

## What good looks like

- **Eight genuinely different briefs.** If two briefs are saying the same thing, the research phase failed.
- **A Contrarian brief you actually have to wrestle with.** If the Strategist can dismiss it in a paragraph, the Contrarian agent is broken or the thesis is too weak to publish.
- **Numerical specificity.** "12 of the 30 large US hubs," not "many airports." If the Editor and Fact-checker can't deliver this, they're not working.
- **A finished document a skeptical executive would not dismiss in the first 500 words.** This is the real bar.

## What bad looks like

- **Agent echo.** Multiple Stage 1 briefs citing the same sources and reaching the same conclusion.
- **Polite Red Team.** Critiques that say "consider adding" instead of "this claim is unsupported, cut it."
- **Hedged Strategist.** "It is important to note that many factors contribute to..." — kill this before it spreads.
- **Vague implications.** "The operator should consider adopting operational intelligence tools." Useless.

## Kill criteria

Stop the run and fix the agent files (not the output) if you see:

- An agent refusing to take a position
- An agent inventing statistics
- The Strategist ignoring the Contrarian or the Regulatory/Political analyst
- The Editor adding new content instead of cutting
- The Fact-checker rubber-stamping unverified claims

In all these cases, the fix is in the markdown in `.claude/agents/`, not in the prose. See [`how-to-propose-an-agent-change.md`](how-to-propose-an-agent-change.md).

## After the run

- Read the auto-generated retrospective in `runs/YYYY-MM-DD-<slug>/retrospective.md`. Add anything the Council missed about what worked or didn't.
- Fill the blanks in the Word document's methodology appendix (operator name/role, total runtime, your name as reviewer).
- Verify the `[UNVERIFIED — HUMAN REVIEW]` tagged claims against authoritative sources before anything goes external.
- Open PRs against agent files for any patterns you noticed across runs. Every run should produce at least one improvement to the system, or you're not learning anything.
