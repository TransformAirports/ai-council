# Orchestration — Transform Airports AI Council

<!--
This file is the canonical four-stage sequence. It's read by Claude Code, not
pasted by the user. The user triggers a run by saying "run <filename>" — see
CLAUDE.md for how that's wired.

If you need to edit the stage sequence itself, open a PR against this file so
the change is versioned.
-->

You are running the Council on the thesis described in a run-prompt file in `prompts/runs/`. The user has pointed you at that file. Your job is to execute the four-stage sequence below end-to-end, with two human checkpoints, and archive the result.

## Preconditions

Before Stage 1:

1. Read the run prompt file the user named. Confirm it has no `{{...}}` placeholders, all required sections are filled, and the thesis is a sharp claim (not a topic). If anything is missing, stop and tell the user what's unfilled.
2. Derive the slug from the filename (basename without `.md`).
3. Confirm with the user in one sentence: the thesis as you understand it, estimated wall-clock (2-4 hours), estimated cost ($40-60). Proceed on their confirmation.
4. If `outputs/` contains artifacts from a previous incomplete run, move them aside or clear them — each run starts clean.

## Stage 1 — Research (parallel)

Invoke these eight research agents concurrently. Each agent's full system prompt is in `.claude/agents/<name>.md` — invoke via the Agent tool with `subagent_type: general-purpose` and pass the agent's full prompt in the task prompt, plus: (a) the path to the run file for framing, and (b) an instruction not to read other Stage 1 agents' output (independent evidence is a design feature).

- `infrastructure-economist` → `outputs/stage1/infrastructure-economist-brief.md`
- `operations-analyst` → `outputs/stage1/operations-analyst-brief.md`
- `technology-scout` → `outputs/stage1/technology-scout-brief.md`
- `contrarian` → `outputs/stage1/contrarian-brief.md`
- `chief-engineer` → `outputs/stage1/chief-engineer-brief.md`
- `airline-commercial-strategist` → `outputs/stage1/airline-commercial-strategist-brief.md`
- `regulatory-political-analyst` → `outputs/stage1/regulatory-political-analyst-brief.md`
- `aviation-historian` → `outputs/stage1/aviation-historian-brief.md`

Use Sonnet for Stage 1 research agents (research-heavy, cost-efficient).

Wait for all eight briefs. Confirm each file exists and has material content before proceeding.

## Stage 2 — Synthesis & Debate

Sequential:

1. Invoke `strategist` → `outputs/stage2/strategist-draft-v1.md`
2. Invoke `red-team` → `outputs/stage2/red-team-critique-v1.md`
3. Invoke `strategist` → `strategist-draft-v2.md` (revised per critique; agent must address every v1 critique item)
4. Invoke `red-team` → `red-team-critique-v2.md`
5. Invoke `strategist` → `strategist-draft-v3.md`

Use Opus for Strategist and Red Team (reasoning quality matters most here).

**★ Stop. Human checkpoint #1.**

Present v3 and both critiques to the user. Summarize: what changed across the three drafts, which Red Team issues the Strategist pushed back on and why, any weaknesses the Strategist explicitly disclosed in the v3 handoff. Do not proceed to Stage 3 without the user's explicit approval. If they ask for targeted revisions, loop back to the appropriate step.

## Stage 3 — Polish

After user approval:

1. Invoke `editor` → `outputs/stage3/edited-draft.md` and `editor-notes.md` (cut 15-25% of word count; kill buzzwords; flag hedges for the Fact-checker).
2. Invoke `fact-checker` → `outputs/stage3/fact-check-report.md` and `final-draft.md` (verify every number against Stage 1 briefs; tag unverifiable claims with `[UNVERIFIED — HUMAN REVIEW]`; has veto power over unsourced claims).

Use Opus for both (the Editor makes judgment calls; the Fact-checker needs to reason carefully about whether a number matches).

**★ Stop. Human checkpoint #2.**

Present the final draft and fact-check report. Do not proceed to Stage 4 without the user's explicit approval.

## Stage 4 — Word documents

After user approval, use the `docx` skill to produce two files in `outputs/stage4/`:

1. **Full report:** `<slug>.docx` — cover page (title and subtitle derived from the thesis, "Transform Airports AI Council", today's date, DRAFT notice), table of contents, full body of `final-draft.md`, and the methodology appendix from `docs/methodology.md` with bracketed fields left blank for the human reviewer to fill in.
2. **Executive summary:** `<slug>-executive-summary.docx` — a ~1,100-word, three-page standalone distillation. Calibri typography, elegant layout, centered title block, letter-spaced section headers. Preserve every `[UNVERIFIED — HUMAN REVIEW]` tag. Every claim must trace to the full final draft.

Preserve inline source citations (e.g., `[Economist brief, Finding 3]`) in the full report. Strip them from the executive summary unless the user asks to keep them.

Validate both .docx files before returning.

## After Stage 4 — archive

Without being asked:

1. Create `runs/YYYY-MM-DD-<slug>/` using today's date.
2. Copy all four stage subdirectories from `outputs/` into that folder.
3. Write a short `retrospective.md` in the archive folder: what worked, what didn't, which agent file behaviors to watch for in the next run, approximate cost and runtime.
4. Clear `outputs/` — remove the four stage subdirectories so the next run starts clean. Preserve `outputs/.gitkeep`.
5. Tell the user: archive path, both .docx filenames, one sentence on total cost and runtime.

## Rules that apply through the whole run

- Every numerical claim cites a source, either a Stage 1 brief or a clearly labeled analyst construction.
- Every unverified or analyst-derived claim in the final draft carries a `[UNVERIFIED — HUMAN REVIEW]` tag.
- No banned words (see `CLAUDE.md`).
- No hedging qualifiers when a specific number exists.
- Short paragraphs. Active voice. Specific examples over abstractions.
- Agents never edit each other's files. Agents never edit themselves. Behavior changes go through human PRs against `.claude/agents/`.

## Model guidance summary

| Stage | Agents | Model |
|---|---|---|
| 1 | 8 research agents | Sonnet |
| 2 | Strategist, Red Team | Opus |
| 3 | Editor, Fact-checker | Opus |
| 4 | docx skill driver | whatever is needed |
