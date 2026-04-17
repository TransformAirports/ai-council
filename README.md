# The MWAA AI Council

**A multi-agent system that produces executive-grade analytical reports on the airport industry.**

Eight specialized agents. Four run in parallel to research a topic independently. One synthesizes. One attacks that synthesis. The author revises, the attacker hits it again. An editor tightens. A fact-checker verifies every number. A human reviews the result twice. The final product is a Word document with a methodology appendix, ready to share.

This repository is the source of truth for the agents and the process. The agents live as versioned markdown files in [`.claude/agents/`](.claude/agents/). The runs that produce real documents are kicked off with Claude Code.

---

## Why this exists

A single LLM, asked to write a long analytical piece, produces prose that is fluent and subtly wrong. It hedges where it shouldn't, cherry-picks its own evidence, smooths over objections, and flatters whatever thesis you handed it. The output reads like every other AI-generated document you've seen.

The Council is an answer to that failure mode. It builds in the three things a solo model cannot do on its own:

1. **Genuinely independent evidence.** Four research agents gather data without seeing each other's work. You get variance, not convergence.
2. **Adversarial pressure on the draft.** A Red Team agent exists only to break the argument. The Strategist has to defend it. Two rounds of this strip out the weak claims.
3. **A hard stop on unverifiable numbers.** A Fact-checker cross-references every number in the final draft against the research briefs. If it can't trace a claim, the claim goes.

The result is a document a sophisticated reader will still disagree with — but not one they can dismiss.

---

## The first run

The Council's first run is a thought piece with the working thesis:

> **Airports are over-investing in infrastructure and under-investing in operational intelligence.**

The run prompt, full framing, and audience notes live at [`prompts/runs/infrastructure-vs-intelligence.md`](prompts/runs/infrastructure-vs-intelligence.md). The target output is an 8,000-10,000 word Word document for MWAA leadership and airport industry readers.

The point is not to confirm the thesis. The point is to present it sharply, honestly steelman the counter-argument, and let the evidence decide whether it survives.

---

## The eight agents

All live in [`.claude/agents/`](.claude/agents/) as markdown files with YAML frontmatter.

### Research (Stage 1 — parallel)

| Agent | Role |
|---|---|
| [`infrastructure-economist`](.claude/agents/infrastructure-economist.md) | Airport CapEx trends, cost overruns, debt service, opportunity cost |
| [`operations-analyst`](.claude/agents/operations-analyst.md) | Delay causes, gate utilization, latent throughput in existing infrastructure |
| [`technology-scout`](.claude/agents/technology-scout.md) | What "operational intelligence" means concretely; what it has cost and returned |
| [`contrarian`](.claude/agents/contrarian.md) | The strongest possible case **against** the thesis |

### Synthesis & Debate (Stage 2)

| Agent | Role |
|---|---|
| [`strategist`](.claude/agents/strategist.md) | Reads all four briefs; writes the argumentative draft; revises after Red Team |
| [`red-team`](.claude/agents/red-team.md) | Attacks the Strategist's draft; finds unsupported claims and logical gaps |

### Polish (Stage 3)

| Agent | Role |
|---|---|
| [`editor`](.claude/agents/editor.md) | Cuts 15-25% of the word count; kills buzzwords; tightens prose. Adds nothing. |
| [`fact-checker`](.claude/agents/fact-checker.md) | Verifies every number against the Stage 1 briefs. Has veto power. |

---

## How a run works

```
Stage 1: Research (parallel, ~60-90 min)
  infrastructure-economist ─┐
  operations-analyst ───────┼──► 4 briefs in outputs/stage1/
  technology-scout ─────────┤
  contrarian ───────────────┘

Stage 2: Synthesis & Debate (~60-90 min)
  strategist v1 ──► red-team critique ──► strategist v2
                 ──► red-team critique ──► strategist v3
                                           │
                                           ▼
                                    ★ Human checkpoint

Stage 3: Polish (~30 min)
  editor ──► fact-checker ──► final-draft.md
                              │
                              ▼
                       ★ Human checkpoint

Stage 4: Word Document
  docx skill ──► .docx with cover, summary, and methodology appendix
```

Two human checkpoints. The first is after the Strategist's third draft — this is where you decide whether the argument is going somewhere worth finishing. The second is after the Fact-checker — this is where you confirm the numbers hold up.

Full operator's guide: [`docs/how-to-run.md`](docs/how-to-run.md).

---

## Principles

These are the rules the Council plays by. They are also the rules the prose plays by — each agent is instructed to refuse them.

1. **Runtime is not quality.** A well-orchestrated 90-minute run beats a sloppy 6-hour one. Depth of disagreement between agents matters more than time on the clock.
2. **Steelman the counter-argument.** A thesis that cannot survive its strongest objection should not be published.
3. **Versioned human editing is the improvement loop.** Agents get better through pull requests against their markdown files. Agents never edit themselves. Agents never edit each other.
4. **Every numerical claim must be sourced.** The Fact-checker has veto power. No exceptions.
5. **No buzzwords. No hedging. No motivational language.** "Leverage," "synergy," "paradigm shift," "in today's rapidly evolving landscape" — all banned. The reader is sophisticated; write for that reader.
6. **Disclose the methodology.** Every final document carries the methodology appendix. AI assistance does not reduce human accountability.

---

## How the agents get better

After every run, the operator writes a brief retrospective — what worked, what didn't, which agent file needs editing. Pattern defects (the Red Team is too polite; the Contrarian softens in the last section; the Editor misses hedge words) become PRs against the relevant markdown file. A second human reviews. The next run uses the updated agent.

This is deliberately slow. It is also the only way to keep the system accountable across many runs.

See [`docs/how-to-propose-an-agent-change.md`](docs/how-to-propose-an-agent-change.md).

---

## Repository layout

```
mwaa-ai-council/
├── .claude/agents/              # the eight agent definitions
├── prompts/runs/                # run-specific thesis and framing files
├── outputs/                     # agent output (gitignored)
├── runs/                        # curated archives of notable runs
├── docs/                        # operator and contributor docs
│   ├── claude-code-setup.md     # canonical setup instructions
│   ├── how-to-run.md            # operator's guide
│   ├── how-to-propose-an-agent-change.md
│   └── methodology.md           # the canonical methodology appendix
├── .gitignore
└── README.md
```

---

## Getting started

1. Install [Claude Code](https://docs.claude.com/en/docs/claude-code).
2. Clone this repository.
3. Read [`docs/claude-code-setup.md`](docs/claude-code-setup.md) and [`docs/how-to-run.md`](docs/how-to-run.md).
4. Decide on a thesis. Write a run prompt in `prompts/runs/<slug>.md` using [`infrastructure-vs-intelligence.md`](prompts/runs/infrastructure-vs-intelligence.md) as a template.
5. Kick off the run from Claude Code with the orchestration prompt in `claude-code-setup.md`.
6. Be present at the two human checkpoints.

Budget roughly $30-100 in API cost per full run and 3-4 hours of soft monitoring time.

---

## A note on scope

The Council is tuned for airport industry analysis. The pattern — four independent researchers, adversarial synthesis, editor, fact-checker, human checkpoints — generalizes. But the value is in the specialization. Edit the agents for your domain. Don't use them as a generic "write me a report" framework.

---

## Accountability

AI output is 85%. The last 15% is the judgment of the human whose name goes on the document. Every final piece the Council produces carries that human's name, reviewed and approved before release. The methodology appendix discloses how the document was made. The disclosure is not a disclaimer — it is a statement of process.
