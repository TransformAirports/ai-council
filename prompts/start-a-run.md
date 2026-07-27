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

## Step 2 — Infer the decision frame and defaults

From the user's description, infer:

- The airport, authority, program, or industry segment
- The decision the work should enable
- The likely executive owner
- The useful time horizon
- The approvals or external parties likely to matter
- The measurable definition of success

Do not interrogate the user for fields you can reasonably infer. Mark unknown
operator-specific facts as research questions in the run file; never invent
them.

Use these defaults silently unless the user specifies otherwise:

- **Audience:** MWAA leadership, airport planners, and policy readers. Assume sophistication and skepticism.
- **Tone:** Direct. Evidence-dense. Intellectually honest about the counter-argument. Slightly provocative but not polemical. Think Matt Levine on aviation, not a consultant deck.
- **Length:** 8,000-10,000 words for the full report; ~1,100-word executive summary.
- **Council:** balanced airport council unless the thesis clearly requires a
  specialist roster.
- **Research agent overrides:** none.
- **Deck mode:** board decision when a deck is requested.

Ask about these only if the user asks first, or if the thesis falls outside the Council's core airport-industry specialization (in which case: flag the mismatch and ask whether to proceed anyway or edit the agent files).

## Step 3 — Write the run file

Pick a short kebab-case slug based on the thesis. Write the run file to
`prompts/runs/<slug>.md` using the template's current structure, including the
decision frame and selected council. Write clean prose, not placeholder syntax.
The file should read like a finished commission.

## Step 4 — Confirm, then run

Show a 4-6 line summary (not the whole file — a human should be able to read this in 15 seconds):

```
Thesis:    <1-2 sentence version>
Audience:  <short>
Tone:      <short>
Length:    <short>
Decision:  <decision and owner, or "to be established by the research">
Slug:      <kebab-case>
```

Ask: "Ready to run?"

On confirmation, execute the canonical Council v2 pipeline from
[`prompts/orchestration.md`](orchestration.md) through
`./council --run <run-file-path>`. You already have the run file path and slug
— you wrote them. The user does not need to paste anything further.

Execute the canonical Council v2 pipeline from
[`prompts/orchestration.md`](orchestration.md). Do not copy an older roster or
stage sequence into the conversation. The CLI owns model routing, manifests,
resume behavior, quality gates, archiving, and publishing.

## Rules that apply to any run

- Every load-bearing claim traces through the claim-lineage file to a structured
  evidence record and an underlying source.
- Reader-facing citations name primary sources, never agents or briefs.
- Every recommendation identifies an owner, approval path, first 90-day move,
  dependencies, leading measure, failure mode, and stop condition—or explicitly
  labels the missing operator fact.
- No buzzwords in output prose (see `CLAUDE.md` for the banned list).
- Agents never edit each other's files or their own files. Behavior changes go through human PRs against `.claude/agents/`.

## What the user should not have to do

- Check out a git branch
- Copy `_template.md`
- Edit `orchestration.md`
- Remember slug conventions
- Paste the full orchestration prompt

You handle all of that.
