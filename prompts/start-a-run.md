# Start a new Council run — conversational entry point

A human just asked you to kick off a new MWAA AI Council run. Handle this like a colleague doing the paperwork for them, not like a bureaucrat handing them a form.

The goal: they describe what they want in plain English, you do the file mechanics, they confirm, you run. They should not have to open `_template.md` or `orchestration.md` or edit anything manually.

---

## Step 1 — Ask once, in plain English

Ask one question. Short. Something like:

> "What do you want to write about? Give me the sharp version of the claim — the thing you'd argue at a dinner table. Unless you want to set audience, tone, or length yourself, I'll use the same defaults as the last run."

If they give you just a topic ("something on airline consolidation"), push once for the sharper claim. Frame it as helpful, not interrogative:

> "A good thesis is a claim you could lose an argument about. What's the version of this you'd actually defend?"

If they resist being pushed, pick a sharp thesis on their behalf from what they said, show it to them, and ask whether you nailed it. Do not run a generic "topic-level" piece — the Council produces bad output from vague inputs.

## Step 2 — Defaults (use silently unless the user specifies otherwise)

- **Audience:** MWAA leadership, airport planners, and policy readers. Assume sophistication and skepticism.
- **Tone:** Direct. Evidence-dense. Intellectually honest about the counter-argument. Slightly provocative but not polemical. Think Matt Levine on aviation, not a consultant deck.
- **Length:** 8,000-10,000 words for the full report; ~1,100-word executive summary.
- **Research agent overrides:** none (use the defaults in `.claude/agents/`).

Ask about these only if the user asks first, or if the thesis falls outside the Council's core airport-industry specialization (in which case: flag the mismatch and ask whether to proceed anyway or edit the agent files).

## Step 3 — Write the run file

Pick a short kebab-case slug based on the thesis (e.g. `airline-consolidation`, `biometric-risk`, `cargo-revenue-collapse`). Write the run file to `prompts/runs/<slug>.md` using the same section structure as the template (thesis, audience, tone, length, what it is NOT, what it IS, success criteria) — but in clean prose, not `{{...}}` placeholder syntax. The file should read like a finished brief, not a fill-in-the-blanks form.

## Step 4 — Confirm, then run

Show a 4-6 line summary (not the whole file — a human should be able to read this in 15 seconds):

```
Thesis:    <1-2 sentence version>
Audience:  <short>
Tone:      <short>
Length:    <short>
Slug:      <kebab-case>
```

Ask: "Ready to run?"

On confirmation, execute the standard four-stage sequence from [`prompts/orchestration.md`](orchestration.md). You already have the run file path and slug — you wrote them. The user does not need to paste anything further.

## Standard four-stage execution (reminder)

- **Stage 1:** Four research agents (`infrastructure-economist`, `operations-analyst`, `technology-scout`, `contrarian`) invoked in parallel. Outputs to `outputs/stage1/`. Use Sonnet.
- **Stage 2:** `strategist` v1 → `red-team` v1 → `strategist` v2 → `red-team` v2 → `strategist` v3. Outputs to `outputs/stage2/`. Use Opus. **Stop for human checkpoint.**
- **Stage 3:** `editor` → `fact-checker`. Outputs to `outputs/stage3/`. Use Opus for editor, Sonnet or Opus for fact-checker. **Stop for human checkpoint.**
- **Stage 4:** `docx` skill produces `outputs/stage4/<slug>.docx` (full report with cover, TOC, body, methodology appendix) and `<slug>-executive-summary.docx` (3-page standalone distillation).

After Stage 4: remind the user to archive the run to `runs/YYYY-MM-DD-<slug>/` and write a brief retrospective.

## Rules that apply to any run

- Every numerical claim cites a source from a Stage 1 brief or is clearly tagged `[UNVERIFIED — HUMAN REVIEW]`.
- No buzzwords in output prose (see `CLAUDE.md` for the banned list).
- Agents never edit each other's files or their own files. Behavior changes go through human PRs against `.claude/agents/`.

## What the user should not have to do

- Check out a git branch
- Copy `_template.md`
- Edit `orchestration.md`
- Remember slug conventions
- Paste the full orchestration prompt

You handle all of that.
