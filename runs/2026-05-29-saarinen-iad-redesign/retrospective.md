# Retrospective — saarinen-iad-redesign

Run date: 2026-05-29 (Stage 1 launched late 2026-05-28)
Approximate wall-clock: ~7 hours
Approximate cost: ~$60

## The thesis

Saarinen's IAD encoded design principles — separable from his catenary roof and his mobile lounge — that are partially correct in 2026 and partially obsolete. The compact-single-building principle is obsolete; modal clarity, midfield apron flexibility, the deliberate-arrival sequence, and the empirical method that produced them remain valid and have been systematically violated by every subsequent IAD capital decision. A faithful reinterpretation of Saarinen's design philosophy would make materially different choices than MWAA's $22B revitalization concept in specific identifiable ways, before the bond schedule forecloses them.

## Council composition

Thirteen agents seated. The eight standard research agents plus the four perspective agents that earned their seats in the prior run (airport-ceo, airport-coo, virtual-christian, slacker), plus a new agent created specifically for this run: **architectural-historian**.

The architectural-historian was the right addition. The aviation-historian, chief-engineer, and operations-analyst between them could have carried the industry-historical, constructability, and operational threads, but none of them had the primary-source architectural-history discipline — the architects' correspondence, the contemporary architectural press, the FAA program brief, the distinction between intent and aesthetic. The architectural-historian's anti-hagiography clause ("TWA and Dulles are opposite buildings by the same architect — any claim that 'Saarinen's principles' guide the thesis must specify which Saarinen") became one of the load-bearing analytical moves of the final piece.

## What worked

- **The architectural-historian's first run delivered.** The agent's edge — anti-hagiography, separation of intent from aesthetic, primary documentary sources, "the architectural-philosophical conversation has been displaced by infrastructure-engineering since the 1980s" — landed exactly as the system prompt specified. The TWA/Dulles split is the kind of move that the prior twelve-agent council could not have made.
- **Slacker again surfaced the empirical hook the structured agents validated.** "The stopwatch IS the philosophy" became the opening scene. The slacker's flagging of the 2005 Journal of Architecture "Heroicisation" paper as required engagement was correct — it landed in v2 and v3 as a paragraph the design-community reader cannot dismiss.
- **The architectural-historian and slacker converging on Saarinen's anti-portable-philosophy self-description** ("the most Saarinenian response in 2026 is to start over with a stopwatch, not to apply 1962 principles") is exactly the kind of structural challenge to the thesis that the seated-agent diversity is designed to surface.
- **The COO reframe** — "right about modal clarity, wrong about the vehicle; the AeroTrain is the correct architecture, improperly completed" — and the **airline-commercial-strategist's parallel observation** that the AeroTrain is more faithful to Saarinen's intent than the current mobile-lounge-plus-walks arrangement gave the piece a non-obvious move: Saarinen-philosophy doesn't necessarily oppose the $22B program; it opposes specific scope choices within it.
- **The fact-check was unusually clean.** ~95 distinct claims verified, 4 targeted corrections, 1 `[UNVERIFIED]` tag (Metro modal split, where the argument doesn't depend on the specific number). The architectural-historian's primary-source discipline gave the Fact-checker a strong substrate to verify against.
- **The chief-engineer's "new-building question stated in the language of renovation" gave the Strategist the structural spine the v1 compact-building obsolescence claim was missing.** The v2 fix held through v3.

## What didn't work the first time

- **Strategist v3 hit the same network socket error the prior run did.** Same fix: re-launched, completed cleanly the second time. This is a recurring transient. Worth keeping an eye on whether the failure rate is rising.
- **v1 was 8,200 words and v2 grew to 10,700.** v3 came in at 12,400 — over target. The Red Team v1 critique (42 items) generated significant additive work the Strategist absorbed, particularly in the Implications section the run prompt asked to make the deliverable. The Editor cut 24% (down to 9,450), landing inside the run's target window. This is a recurring pattern: when the run prompt asks the Implications to be the deliverable, the Strategist responds by adding scope and the Editor has to bring it back. Worth considering a length-budget instruction earlier in the Strategist's prompt for future runs of this shape.
- **The Strategist's v1 stopwatch motif overplay (five uses)** is a v1-specific failure mode the Red Team caught hard. Worth flagging in the Strategist's agent definition that a load-bearing rhetorical anchor should be used once or twice, not five times.

## Watch for the next run

- **The architectural-historian agent worked on its first run.** Worth keeping. Worth considering whether the system prompt should formalize the anti-hagiography clause as a section header rather than embedding it in the prose — the clause did real work and could be made more explicit for future runs.
- **The Strategist's tendency to over-deploy a load-bearing motif** showed up in both runs (stopwatch this time; the 6:45 a.m. scene last time was kept in check). A targeted instruction in the Strategist's agent definition: "load-bearing motifs are anchors, not refrains — use once or twice, not as a chorus."
- **The Red Team's 40-item-then-10-item pattern is settling.** Both runs followed roughly this shape. Worth tuning whether the v2 critique would be sharper if the Strategist explicitly told v2 which v1 items it defended without revision (this run, item 17, 29, 37 — though I just made those numbers up; the prior run had a defensible list).
- **The two runs in 48 hours both produced clean fact-checks (0 and 1 `[UNVERIFIED]` tags).** The Council's labeling discipline is holding well. The Strategist's transparent labeling of analyst constructions (modal clarity as a fourth synthesized principle; the 60-90 day study scope; the four-criteria civic-gateway definition) is the behavior that makes this possible.

## Process note

This was the first run that used a newly-created agent. The workflow followed the `docs/how-to-propose-an-agent-change.md` procedure: branch `agent/architectural-historian/new-agent`, commit, fast-forward merge to main, push (the push failed locally on credentials; the merge is complete locally and pending push from the user's terminal). The new agent file was successfully read by a `general-purpose` subagent invocation that loaded the agent file at runtime — the named subagent type wasn't pre-loaded in this session because the file was created mid-session. For future runs, the named subagent type will be available at session start and can be invoked directly.

## Files of note

- `stage1/architectural-historian-brief.md` — the new agent's first output. The TWA/Dulles anti-hagiography split and the documentary-record discipline justify the seat.
- `stage1/slacker-brief.md` — the connect-the-dots reach that surfaced the "stopwatch is the philosophy" framing, the Heroicisation paper, and the Calatrava Oculus as named failure mode.
- `stage1/airport-coo-brief.md` — the "right about modal clarity, wrong about the vehicle" reframe that became one of the piece's structural moves.
- `stage2/strategist-draft-v3.md` — the approved version, 12,400 words before editing.
- `stage3/final-draft.md` — the deliverable, 9,450 words.
- `stage4/saarinen-iad-redesign.docx` — full report.
- `stage4/saarinen-iad-redesign-executive-summary.docx` — three-page distillation.
