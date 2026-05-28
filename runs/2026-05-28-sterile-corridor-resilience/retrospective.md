# Retrospective — sterile-corridor-resilience

Run date: 2026-05-28
Approximate wall-clock: ~6 hours (with a ~1-hour pause for the permission fix)
Approximate cost: ~$50

## The thesis

Sterile corridor design at major US hub airports is treated as a code-compliance problem when it should be treated as a throughput and resilience problem. The specific MWAA framing: IAD's midfield concourses (A/B 1997, C/D 2000) and the AeroTrain handoffs are at an inflection point, and the next eighteen months of Tier 2 design development will set the geometry for thirty years.

## Council composition

Twelve agents seated, not eight:
- The eight standard research agents
- airport-ceo, airport-coo, virtual-christian, slacker

The four additional agents earned their seats. virtual-christian surfaced the "lifecycle accountability gap" reframe and the international-to-international flow case. slacker surfaced the bidirectional-flow / LOS-table critique that turned out to be the empirical hook of the entire piece. airport-coo gave the operator-chair texture (the 6:45 a.m. scene) that the Strategist used as the narrative anchor.

## What worked

- **The bidirectional-flow finding.** Slacker's gut-pass hunch ("is Fruin's LOS framework right for bidirectional flow") was confirmed by operations-analyst's retry with a 2018 PLOS One meta-analysis quantifying the 25% capacity reduction. This became the empirical spine of the argument. The structured-versus-unstructured-agents synergy is exactly the design intent of seating both.
- **The strategist's labeling discipline.** Every analyst construction in the draft was labeled as such (pulse arithmetic, mid-life cost multiplier, instrumentation cost estimate), with the underlying components traced to specific briefs. Result: zero `[UNVERIFIED — HUMAN REVIEW]` tags in the final draft. That's unusually clean.
- **Red Team v1 catching the over-spin.** Strategist v1 said the pulse arithmetic "exactly matches" corridor capacity. Red Team caught that the brief actually flagged the calculation as analyst-constructed and required field verification. The correction landed in v2 and held through v3.
- **The DCA Project Journey rebuttal evolution.** v1's response to the contrarian was a redirect. v2 rebuilt it as a financial-multiplier argument ("the window reopens, but only once per generation, because the cost of opening it more often is what the financial system will not tolerate"). That's a sharper version of path dependence than the v1 framing.
- **The 12-agent → 6-movement synthesis at 9,800 words.** No padding, no list-form fallback, no dropped lenses. The historical-arc movement carried Pittsburgh and LGA and JFK T1 cleanly; the IAD-specific implications section named specific dollar figures.

## What didn't work the first time

- **Three Stage 1 agents bailed on a permission denial** (operations-analyst, technology-scout, regulatory-political-analyst) instead of falling back to training-data with caveats the way the other agents did. Their system prompts told them not to fabricate sources, and they read "don't fabricate" as "don't write." This is an agent-definition gap — see "Watch for next run" below.
- **Strategist v1 hit a network socket error** mid-task and produced no output. Had to re-launch. No fix needed; just a transient network issue.
- **Red Team v2 reported it couldn't read the Stage 1 brief files directly** in its session. It worked from the v1 critique's characterization of the briefs plus the v2 prose itself. Items it flagged as "verify against brief" became explicit Fact-checker handoffs. The Fact-checker subsequently verified them cleanly. No lasting damage, but the Red Team's verification was thinner than ideal.

## Watch for the next run

- **Agent definitions should explicitly tell research agents to fall back to training-data with `[from training-data, requires primary-source verification]` labels rather than bail when web access is denied.** Five of the twelve agents did this correctly on their first attempt; three did not and had to be re-launched. The behavior should be the default, not a per-run instruction in the orchestration prompt.
- **The strategist agent's system prompt lists eight briefs.** This run seated twelve. The orchestration prompt has to remind the strategist (and red-team, and fact-checker) about the additional four briefs. Worth considering whether the agent definitions should dynamically reference whichever briefs exist in `outputs/stage1/` rather than hard-coding the eight.
- **The Red Team file-read failure** is worth a closer look. It happened in the second round only. If reproducible, the agent definition or the orchestration framing should ensure file access is stable across both rounds.
- **Permission gating.** The project had no `.claude/settings.local.json` at run start; web tools defaulted to denied. Adding `WebSearch` and `WebFetch` to the project's settings is now done — the file is checked in. Future runs should not hit this same wall, but the user-facing behavior when web tools are unavailable is still something to harden in the agent definitions.

## Files of note

- `stage1/operations-analyst-brief.md` — 90 tool calls in the retry, the most thorough Stage 1 brief. Empirically validated the bidirectional-flow finding.
- `stage1/slacker-brief.md` — the gut-pass that produced the empirical hook the structured agents then quantified. Good case for keeping slacker seated when the thesis is methodological.
- `stage2/strategist-draft-v3.md` — the approved version. Notably, every analyst construction is labeled inline, which is what produced the clean fact-check.
- `stage3/fact-check-report.md` — 64 verified, 3 corrected, 0 `[UNVERIFIED]` tags.
- `stage4/sterile-corridor-resilience.docx` — full report.
- `stage4/sterile-corridor-resilience-executive-summary.docx` — three-page distillation.
