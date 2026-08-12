# Editor notes — Stage 3 edit of strategist-draft-v3

*Run: quiet-by-design-standards-for-mwaa-terminals-2 · 2026-08-11*

**Input:** `outputs/stage2/strategist-draft-v3.md` (per run-manifest declared input for `stage3/edited-draft.md`).
**Output:** `outputs/stage3/edited-draft.md`.

## Length compliance

- Article body (between the article heading and the Airport Decision Card): **1,912 words** (measured with `wc -w`, FC-CHECK tags included), inside the run contract's 1,500–2,000 range. Cut from ~2,750 in v3 — roughly 31% off the body, achieved by removing restatement, not evidence. Every citation, number, and named requirement in v3 survives.
- Executive summary: **~430 words** against the "~400-word" spec, including bracketed FC-CHECK tags. Cut from ~560.
- Airport Decision Card and footnotes retained in full (the decision output is a run success criterion; footnotes untouched except that all 32 definitions carry over verbatim). Note: [^24] (Part 139) was orphaned in v3; I attached it to the Part 139 dependency line in the decision card.

## Major changes

1. **Removed the "Handoff notes" section.** Internal Strategist-to-Editor material, not reader-facing. Its nine residual weaknesses are converted to inline `[FC-CHECK: …]` tags (below) so the Fact-checker inherits them without the reader seeing scaffolding.
2. **Executive summary restructured** from four long paragraphs to four tighter ones; the naming convention, safety framing, and three-proposition case are intact. Redundant restatement of DSCR scoping logic (it appeared in both the summary and ¶10) trimmed in the summary, kept in full in the body.
3. **Cut consultant reflexes:** "The counter-case deserves an honest hearing," "That reframing makes the tenant question tractable, but not closed," "The vehicle exists; the window is narrow" (as a topic-sentence announcement — the content moved into the financial paragraph). Transitions now run through the argument ("Which raises the tenant question") rather than announcing topics.
4. **Merged the three "smaller objections"** at the end of v3 ¶13 into the counter-case paragraph where each was already answered elsewhere; kept the premature-specification objection in full because it is the serious one.
5. **Voice preserved deliberately:** the ICU open and close, "the alarm no one hears," "MWAA does not need to import their brand. It needs to out-engineer them," "Review without a specification is a review of nothing," "the first Wednesday afternoon of gate holds," and the paired closer "whether to write the paragraph." These are the piece, not the bloat.
6. **Buzzword scan:** none of the banned list present in v3 or in the edit. No vague quantifiers left where a number existed in the draft.
7. **Decision card lightly tightened** (~10%): duplicate committee names, restated cure-notice mechanics, and filler ("as much as," "documented" doubling) trimmed. No mechanics, dates, thresholds, or stop conditions changed.

## Flags for the Fact-checker (inline as [FC-CHECK] tags)

1. **771 alarms/bed/day** (fn 10) — primary Johns Hopkins study unresolved; trade-press figure.
2. **2×–4× design-vs-retrofit and $12M–$40M stack** (fn 7) — analyst construction from non-airport pricing; tagged in summary, body, and decision card.
3. **2025 AUL majority-in-interest text** (fn 1, 8, 15) — not verified from primary AUL; tenant tier written as contingent.
4. **DCA Terminal 1 phase status** — unverified; branch logic depends on it.
5. **SFO Quiet Airport outcomes** (fn 19) — SFO-reported, no published methodology.
6. **Cranky Flier CPE figures** ($90.64 vs. $12.88, fn 16) — attributed commentary, methodology unverified.
7. **United/American share and gate counts** (fn 28) — trade press, not primary disclosure.
8. **±3 dB lease-line concessions figure** — analyst placeholder pending Design Manual verification.
9. **NFPA 72 edition in force at each AHJ** (fn 4) — flagged in the decision card verification step rather than inline; the amendment is written as an MWAA floor atop the AHJ-adopted edition.

## Not changed

Thesis, evidence base, conclusions, tiering, stop conditions, and all 32 footnotes. The IAD composite scene (¶2) retains its "operating pattern, not dated observation" hedge per the v2 red-team fix.
