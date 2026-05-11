# Retrospective — 2026-04-21 — Southwest Transformation at BNA

## The run at a glance

- **Run file:** `prompts/runs/southwest-transformation-bna.md`
- **Thesis:** BNA's capital program was designed for the Southwest that existed when ground broke, not the Southwest that will be flying through Nashville in 2030. The remaining uncommitted tranches of New Horizon need to be pressure-tested against the new operating model before they are committed, not after.
- **Wall-clock:** ~80 minutes (Stage 1 parallel + sequential Stages 2-4 + archive)
- **Cumulative agent runtime:** ~95 minutes across 13 agent invocations
- **Final outputs:** 8,227-word report; ~1,150-word executive summary; both as .docx

## What worked

- **Eight lenses produced genuinely distinct evidence.** No echo. The Airline Commercial Strategist's deep dive on Southwest's CASM/PRASM trajectory, the Chief Engineer's Dallas Love Field retrofit comparable, the Regulatory/Political analyst's discovery of the live Tennessee Supreme Court case over MNAA governance, and the Aviation Historian's honest framing that no clean precedent exists — each contributed load-bearing material the Strategist used distinctly.
- **The narrative register held.** The Red Team caught the "Bill Franklin" invention in v1 — an invented named character from a secondary source. The Strategist cut it cleanly in v2 without losing the scene. By v3 the opening still opened on Gate D6 at 6:14 a.m., with the Acme Feed & Seed mezzanine contrast, the bin-stow geography, and the closing "the concrete is still being poured" — narrative long-form, not consultant report.
- **The Red Team's pattern observation landed.** "McPhee and Kidder get their vividness from observation, not from invention." That single sentence in the v1 critique shaped the entire v2 revision and the Strategist's approach to narrative authority through v3.
- **Fact-checker verdict cleaner than the first run.** ~140 claims checked, 128 verified, one suspected error corrected (the 36% Southwest-operating-revenue attribution), zero `[UNVERIFIED — HUMAN REVIEW]` tags surviving to the final draft. The Strategist avoided inventing analyst-derived sub-tranche figures — Section VI argues about the actual disclosed New Horizon components ($855M Concourse A, October 2028 BHS commissioning, the seven ramp positions) using the Engineer brief's sourced numbers.
- **Structural discipline.** The Red Team v2 caught that Section V had flattened into boldface-led bullets after v2's rebuttal expansion. The Strategist's v3 revision collapsed eight sub-arguments to seven natural movements, removed boldface leads, varied rhetorical shape. Voice restored within the same revision pass.

## What didn't

- **Section VI Implications were argumentative rather than directive.** The first run had pre-registered defeat tests with numeric thresholds. This one doesn't — the Strategist argued for specific diligence steps (request the carrier-mix hold-room sizing case in writing; re-run the BHS load case after the May 2025 fee rollout) but stopped short of naming a specific test that would gate a specific tranche. Defensible for this thesis (the operator is the one with the capital plan details; the piece asks them to use them), but it's a softer landing than the first run's.
- **The Editor ran fast (~8 min)** compared to the first run's 37 minutes, but the shorter runtime may reflect deliberately lighter cuts to preserve narrative voice. The result was a 15% cut at the conservative end of the 15-25% target range. This is probably correct for narrative long-form but worth watching — if future runs see the Editor consistently at 15%, a tighter system-prompt budget or a deeper second pass might be warranted.
- **One Red Team v2 item was softened rather than fully resolved.** The Strategist kept the boarding-group names list in-prose with an added flag rather than cutting it. Defensible (the list does scene-level work), but the Fact-checker noted that the specific ordering is a Strategist choice. A more conservative resolution would have been to generalize ("eight boarding groups, ordered by fare class and status") rather than enumerate.
- **Narrative specifics flagged but preserved.** Gate D6, "Tuesday morning," the boarding group names, the "three floors up" mezzanine description — these are illustrative rather than observational and the Fact-checker correctly let them stand. But a stricter reading of the brief material would have preserved the scene's mechanism without naming a specific gate. Worth discussing with the human reviewer whether narrative long-form's license for illustrative specifics is the right line for this system, or whether the line should sit closer to "only names and times that appear in the briefs."

## Agent files to consider revising

Holding these until a third run confirms the pattern:

- **`.claude/agents/strategist.md`** — consider a clearer rule on what counts as permissible narrative detail. The current guidance ("use character and place... let specificity do the work") allowed the Bill Franklin invention; the tightening in v2-v3 recovered from it but only after a Red Team round. A pre-stated rule like "any named individual must be sourced to a brief" might prevent the initial overreach.
- **`.claude/agents/editor.md`** — the 15% cut at the conservative end of target may become a recurring pattern if the Editor is instructed to preserve narrative voice aggressively. If that's the right trade-off, the target range should be narrowed (e.g., 12-18%) rather than the current 15-25%.
- **`.claude/agents/strategist.md` again** — the Section VI implications in this run were softer than the first run's pre-registered defeat tests. For runs where operator-specific decisions need to land with force, a stronger Section VI directive might help. But it may also be correct that this thesis didn't call for pre-registered defeat tests in the same way — worth human judgment.

## Cost estimate

Approximately $40-50 in API spend. Stage 1 (Sonnet × 8): ~$15. Stage 2 (Opus × 5): ~$25. Stage 3 (Opus × 2): ~$8. Stage 4: ~$2. Not line-item accurate; total inferred from prior run + model mix.

## Notes for the next run

- Template edits, orchestration, and the conversational entry point all worked as designed. The "run southwest-transformation-bna" trigger produced the expected confirmation, the expected four-stage execution, and the expected archive behavior. No machinery changes needed.
- This run's full artifact set is preserved in this directory for reference. The `outputs/` working directory has been cleared for the next run.
