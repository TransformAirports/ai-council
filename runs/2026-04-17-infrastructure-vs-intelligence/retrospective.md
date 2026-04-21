# Retrospective — 2026-04-17 — Infrastructure vs. Operational Intelligence

## The run at a glance

- **Run file:** `prompts/runs/infrastructure-vs-intelligence.md`
- **Thesis:** The discretionary portion of the next billion in airport CapEx should have to clear a defeat test against a much smaller operational intelligence investment.
- **Wall-clock:** ~1h 25m (Stage 1 parallel)
- **Cumulative agent runtime:** ~1h 45m across 11 invocations
- **Final outputs:** 11,578-word report, 1,150-word executive summary, both as .docx

## What worked

- **The two-round adversarial loop did real work.** The Red Team's v1 critique surfaced a buried logical gap (the Strategist had quietly redefined A-CDM as "not AI" to duck the Gartner base rate). The v2 critique caught the opposite pattern — the v2 fix introduced specific dollar envelopes in Section 6 that were over-attributed to the Technology Scout brief. Neither issue would have been caught without the adversarial structure. Both were fixed in v3.
- **The Fact-checker's veto held.** Ten analyst-derived figures in Section 6 were correctly tagged `[UNVERIFIED — HUMAN REVIEW]` and survived into the final .docx with disclosure intact. Zero fabricated numbers.
- **Independent Stage 1 research produced genuinely different briefs.** No echo. The Contrarian brief was strong enough to force real concessions in Section 5 rather than a dismissive rebuttal.
- **Executive summary as a standalone deliverable** was added after the main run and used the same source material without re-running any agents. The modular structure supported this cleanly.

## What didn't

- **The Strategist drifted toward vague MWAA recommendations.** The v1 Section 6 was the weakest part of the first draft and needed two full rounds of critique plus an explicit rebuild instruction to produce specific projects, envelopes, KPIs, and defeat tests. The agent file should probably specify what "Implications for {{org}}" means before the first draft.
- **The Editor ran 37 minutes.** Outlier of the run. The Editor made 91 tool calls (two full reads of a 13,400-word draft plus targeted edits). A tighter Editor prompt — maybe a pass-budget cap or a split between "buzzword/hedge pass" and "compression pass" — might cut this significantly.
- **Dollar-envelope construction was fragile.** The Strategist invented a "1:10 ratio at large US hubs" figure in v1 that had no brief source. The Red Team caught it. A stricter rule — "no derived ratio appears unless both numerator and denominator are brief-cited" — might prevent this class of error upstream.
- **Word count overran on v3.** Target was 8,000-10,500. v3 came in at 13,400 because the Red Team demanded more specific arithmetic in Section 6. The Editor cut it back to 11,397. Not a failure per se — the extra length was load-bearing — but it means length targets in the run prompt are soft.

## Agent files to consider revising

Candidates for PRs after a second run confirms the pattern:

- **`.claude/agents/strategist.md`** — add a specification for the Implications section that forces named projects, envelopes, KPIs, and defeat tests on the first pass. V1 of this run had a generic Section 6; the quality was only recovered in v3 after two critique rounds.
- **`.claude/agents/editor.md`** — consider a pass-budget or multi-pass split. 37 minutes on a single draft is a lot.
- **`.claude/agents/strategist.md`** — add a rule prohibiting derived ratios unless both components are brief-cited.

Hold these until a second run shows the same defects. One run is a data point, not a pattern.

## Cost estimate

Approximately $35-45 in API spend (Sonnet for Stage 1 research, Opus for Stages 2-3, negligible for Stage 4). Not line-item accurate.

## Notes for the next run

- The orchestration prompt is now in `prompts/orchestration.md` as a template with `{{RUN_FILE}}` and `{{RUN_SLUG}}` slots. Run prompts are copied from `prompts/runs/_template.md`.
- This run's full artifact set is preserved in this directory for reference. The `outputs/` working directory has been cleared for the next run.
