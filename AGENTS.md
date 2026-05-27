# Repo guidance for Codex

This is the **Transform Airports AI Council** — a multi-agent system that produces executive-grade analytical reports on the airport industry. Eight specialized research agents, one Strategist, one Red Team, one Editor, one Fact-checker. Four stages. Two human checkpoints. See `README.md` for the full explanation.

## Treat this repo like a Codex app

The user writes a run-prompt markdown file in `prompts/runs/` and then triggers a run by telling you the filename. Everything else — research, synthesis, adversarial revision, polish, fact-checking, Word document generation, archiving — is your job.

### When the user says "run <filename>"

If the user says anything that looks like:

- `run airline-consolidation`
- `run prompts/runs/biometric-risk.md`
- `let's run the cargo-revenue file`
- `kick off <name>`
- `execute <name>`

...treat it as a trigger to start a full Council run on that file.

1. Resolve the filename to a path in `prompts/runs/` (add `.md` if missing; accept with or without the directory prefix).
2. Read the file. If any `{{...}}` placeholders remain or required sections are missing/empty, stop and tell the user what's unfilled. Do not proceed with a half-written run prompt.
3. Confirm you understood: "Running `<slug>`. Thesis: <1-sentence paraphrase>. This will take 2-4 hours and cost roughly $40-60. Ready?"
4. On confirmation, execute the four-stage sequence defined in [`prompts/orchestration.md`](prompts/orchestration.md). You already have the run file path and the slug. The user does not need to paste anything further.

### When the user asks for a new run but has no file yet

If they describe a thesis in conversation without pointing to a file (e.g. "let's do a new run on cargo revenue"), follow [`prompts/start-a-run.md`](prompts/start-a-run.md) — it walks you through gathering the thesis, writing the run file for them, and kicking off the run. This is the conversational path for users who don't want to edit files themselves.

### After a run completes

After Stage 4 (Word documents generated), automatically:

1. Copy the full contents of `outputs/` to `runs/YYYY-MM-DD-<slug>/` using today's date.
2. Write a short `retrospective.md` in that folder (what worked, what didn't, which agent file behaviors to watch in the next run).
3. Clear `outputs/` back to an empty state so the next run starts clean.
4. Tell the user the archive path and a one-line summary of the deliverables.

Do NOT require the user to do the archiving themselves. The archive and clean-up is part of the run.

## Tone rules — apply to every deliverable the Council produces, and to your own prose about the Council

- No buzzwords: "absolutely," "leverage," "synergy," "holistic," "best-in-class," "paradigm shift," "ecosystem" (unless literal), "game-changer," "mission-critical" (unless genuinely so), "in today's rapidly evolving landscape."
- No vague quantifiers ("many," "often," "increasingly") when a specific number exists.
- Short paragraphs. Active voice. Specific examples over abstractions.
- Write for sophisticated, skeptical peer readers — airport executives, planners, and policy leaders.

## What the user should NEVER have to do

- Check out a git branch to run a new thesis
- Copy or edit `orchestration.md`
- Paste the four-stage sequence into Codex
- Manually archive outputs to `runs/`
- Clear `outputs/` between runs
- Remember slug conventions or date formats

Branches are only needed for editing the 12 agent-and-process files in `.Codex/agents/` and `prompts/` themselves — see [`docs/how-to-propose-an-agent-change.md`](docs/how-to-propose-an-agent-change.md).

## Key files

- [`prompts/runs/_template.md`](prompts/runs/_template.md) — the template the user copies and renames
- [`prompts/orchestration.md`](prompts/orchestration.md) — the canonical four-stage orchestration (you read this; the user does not)
- [`prompts/start-a-run.md`](prompts/start-a-run.md) — conversational entry point for users who want to dictate a thesis instead of writing a file
- [`.Codex/agents/`](.Codex/agents/) — the twelve agent definitions
- [`runs/2026-04-17-infrastructure-vs-intelligence/`](runs/2026-04-17-infrastructure-vs-intelligence/) — first run's complete archive; use as a reference for what a good run looks like end-to-end
