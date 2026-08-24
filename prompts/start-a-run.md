# Start a new Council run — conversational entry point

A human just asked you to kick off a new MWAA AI Council run. Handle this like a colleague doing the paperwork for them, not like a bureaucrat handing them a form.

The goal: they describe what they want in plain English, you do the file mechanics, they confirm, you run. They should not have to open `_template.md` or `orchestration.md` or edit anything manually.

---

## Step 1 — Ask once, in plain English

Ask one question. Short. Something like:

> "What do you want to write about? Give me the sharp version of the claim — the thing you'd argue at a dinner table. Unless you say otherwise, I'll shape it as a fascinating narrative feature."

If they give you just a topic ("something on airline consolidation"), push once for the sharper claim. Frame it as helpful, not interrogative:

> "A good thesis is a claim you could lose an argument about. What's the version of this you'd actually defend?"

If they resist being pushed, pick a sharp thesis on their behalf from what they said, show it to them, and ask whether you nailed it. Do not run a generic "topic-level" piece — the Council produces bad output from vague inputs.

## Step 2 — Use the narrative defaults

From the user's description, infer:

- The airport, authority, program, or industry segment
- The tension, mechanism, cases, places, or people likely to make the story move
- The strongest counter-case

Do not infer a decision frame. Include one only when the user explicitly says
the work must support a named decision or opts into it after seeing the choice.
Unknown operator-specific facts remain research questions; never invent them.

Use these defaults silently unless the user specifies otherwise:

- **Audience:** MWAA leadership, airport planners, and policy readers. Assume sophistication and skepticism.
- **Tone:** Fascinating, vivid, and argument-led. Open with a scene, case, or surprise. Write like an excellent magazine feature, not a consulting assignment or technical paper.
- **Length:** A 1,500–2,000-word narrative feature, with no appendices or separate executive summary.
- **Output format:** article.
- **Council model:** claude-fable-5, unless the operator chooses gpt-5.6-sol.
- **Council:** balanced airport council unless the thesis clearly requires a
  specialist roster.
- **Research agent overrides:** none.
- **Deck mode:** board decision when a deck is requested.

Ask about these only if the user asks first, or if the thesis falls outside the Council's core airport-industry specialization (in which case: flag the mismatch and ask whether to proceed anyway or edit the agent files).

## Step 3 — Write the run file

Pick a short kebab-case slug based on the thesis. Write the run file to
`prompts/runs/<slug>.md` using the template's current structure, omitting the
Decision frame unless the user opted in, and including the selected council.
Write clean prose, not placeholder syntax.
The file should read like a finished commission.

## Step 4 — Confirm, then run

Show a 4-6 line summary (not the whole file — a human should be able to read this in 15 seconds):

```
Thesis:    <1-2 sentence version>
Audience:  <short>
Tone:      <short>
Length:    <short>
Mode:      <"narrative feature" or the opted-in decision and owner>
Slug:      <kebab-case>
```

Ask: "Ready to run?"

On confirmation, execute the canonical Council v2 pipeline from
[`prompts/orchestration.md`](orchestration.md) through
`./council --run <run-file-path>`. You already have the run file path and slug
— you wrote them. The user does not need to paste anything further.

Execute the canonical Council v2 pipeline from
[`prompts/orchestration.md`](orchestration.md). Do not copy an older roster or
stage sequence into the conversation. The CLI owns the run-level model route, manifests,
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
