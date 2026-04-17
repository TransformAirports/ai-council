# How to Run the Council

A practical operator's guide. Assumes you've already set up the repo and read `claude-code-setup.md`.

## Prerequisites

- Claude Code installed and authenticated
- Repository cloned locally with all 8 agent files present in `.claude/agents/`
- A run prompt in `prompts/runs/` that defines the thesis, audience, tone, and length
- 3-4 hours of soft monitoring time (you do not need to watch it; check in at checkpoints)
- Rough API budget of $30-100 depending on research depth

## The Four Stages

The Council runs in four stages with **two human checkpoints**. The checkpoints exist so you can redirect the argument before the agents spend hours polishing the wrong draft.

### Stage 1 — Research (parallel)

Four agents research independently. They do not read each other's work. This is on purpose — independent evidence collection beats coordinated evidence collection.

- `infrastructure-economist` — airport CapEx trends, cost overruns, debt service
- `operations-analyst` — delay causes, gate utilization, where the real bottleneck is
- `technology-scout` — what "operational intelligence" actually means in deployment
- `contrarian` — the strongest case **against** the thesis

**Kick off:** "Invoke the four Stage 1 agents in parallel and wait for all four briefs to land in `outputs/stage1/`."

**What to look for:** Four briefs, each 1,500-2,500 words, each with inline source citations. If any brief is shorter, has no sources, or reads like a summary of a summary, stop and re-run that agent.

### Stage 2 — Synthesis & Debate

The Strategist reads all four briefs and writes a draft. The Red Team attacks it. The Strategist revises. Repeat twice.

- Strategist produces `strategist-draft-v1.md`
- Red Team produces `red-team-critique-v1.md`
- Strategist produces `strategist-draft-v2.md` (incorporating critique)
- Red Team produces `red-team-critique-v2.md`
- Strategist produces `strategist-draft-v3.md`

**Human checkpoint #1:** Read v3, read both critiques, decide whether to continue.

Questions to ask yourself at this checkpoint:
- Is the thesis still sharp, or has the argument softened into mush?
- Did the Strategist actually address the Contrarian's strongest points, or did it steamroll them?
- Are there any numerical claims that raise an eyebrow? (Flag them for the Fact-checker.)
- Is the MWAA section specific enough, or is it generic consultant-speak?

If anything is off, do **not** proceed. Rewrite the run prompt, update the relevant agent file, and re-run from Stage 2 with the existing briefs.

### Stage 3 — Polish

After your approval:
- Editor produces `edited-draft.md` (cut 15-25% of word count, kill buzzwords, tighten prose)
- Fact-checker produces `fact-check-report.md` and `final-draft.md` (verify every number against Stage 1 briefs; flag or remove what can't be verified)

**Human checkpoint #2:** Read the fact-check report. Decide whether to proceed to Word generation or push back for another revision.

### Stage 4 — Word Document

Use the `docx` skill to produce the final Word document. It should include:
- Cover page
- Executive summary
- Main argument
- Counter-case and rebuttal
- Implications section
- **Methodology appendix** (this is not optional — see `methodology.md`)

## What Good Looks Like

- **Four genuinely different briefs.** If two of them are saying the same thing, the research phase failed.
- **A Contrarian brief you actually have to wrestle with.** If the Strategist can dismiss it in a paragraph, the Contrarian agent is broken or the thesis is too weak to publish.
- **Numerical specificity.** "12 of the 30 large US hubs," not "many airports." If the Editor and Fact-checker can't deliver this, they're not working.
- **A finished document that a skeptical executive would not dismiss in the first 500 words.** This is the real bar.

## What Bad Looks Like

- **Agent echo.** All four Stage 1 briefs citing the same three sources and reaching the same conclusion.
- **Polite Red Team.** Critiques that say "consider adding" instead of "this claim is unsupported, cut it."
- **Hedged Strategist.** "It is important to note that many factors contribute to..." — kill this before it spreads.
- **Vague implications.** "MWAA should consider adopting operational intelligence tools." Useless. The implications must be specific.

## Kill Criteria

Stop the run and fix the agent files (not the output) if you see:

- An agent refuses to take a position
- An agent invents statistics (Fact-checker will catch this, but you should too)
- The Strategist ignores the Contrarian
- The Editor adds new content instead of cutting
- The Fact-checker rubber-stamps unverified claims

In all these cases, the fix is in the markdown, not the prose.

## After the Run

See `docs/how-to-propose-an-agent-change.md`. Every run should produce at least one PR against at least one agent file, or you are not learning anything.
