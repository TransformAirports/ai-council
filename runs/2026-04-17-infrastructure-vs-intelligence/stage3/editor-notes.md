# Editor's Notes — Draft v3 Edit

**Date:** April 17, 2026
**Editor pass on:** `outputs/stage2/strategist-draft-v3.md`
**Output:** `outputs/stage3/edited-draft.md`

---

## Word count

- **Before:** 13,382 words
- **After:** 11,397 words
- **Cut:** 1,985 words
- **Percentage cut:** 14.8%
- **Target range (task spec):** ~10,000–11,400 words. Final lands at the top of the range.

---

## Major structural or rhetorical changes

1. **No structural reorganization.** The argument, section order, and numbered claims are intact. The Strategist's scaffold was already disciplined; the cut is line-by-line rather than reorganizational.

2. **Thesis section split.** Section 1 was a single 200-word paragraph. Broke it into two shorter paragraphs so the narrow-scope definition separates from the opening diagnosis. No wording change to the thesis itself.

3. **Citation-sentence compression.** Many citation tails appeared twice in the same paragraph. Dropped the second reference where unambiguous.

4. **Self-references simplified.** "Section 6.2 of this paper" → "6.2." "The Stage 3 fact-checker should verify" → "Fact-checker should verify." Dozens of these across Section 6.

5. **Short emphatic sentences used for pivots.** "Not inflation. Optimism bias embedded in planning." "Not 5%. Not 50%." "Scoped, not universal." Replacing longer concessive constructions.

6. **Removed meta-commentary about the Strategist's own process where it duplicated what the draft already showed.** Lines like "The honest framing is..." kept where load-bearing, trimmed where they just throat-cleared.

7. **Preserved everything load-bearing:** every number, every citation, every defeat-test threshold, every analyst-derived envelope, every caveat, every Red Team concession and withdrawal, the V2-vs-V3 commentary about prior-draft corrections, and every piece of the Section 6 implementation specification.

---

## Buzzwords and hedges killed

The Strategist's v3 draft was already remarkably clean on the task spec's banned-word list. Grep for `leverage`, `synergy`, `holistic`, `best-in-class`, `paradigm shift`, `ecosystem`, `absolutely`, `game-changer`, `mission-critical`, `in today's rapidly evolving` returned **zero hits in the source**. Nothing from that list to kill.

What I actually cut (hedges, passive voice, and throat-clearing):

- "Some portion of the current capital program" → "Part of the current capital program" (in 1–2 spots)
- "Airports are being asked to finance" → "Airports finance" (3.7, passive → active)
- "This paragraph speaks only to..." → "This speaks only to..." (3.3)
- "It is worth noting that" → deleted where it appeared
- "The Strategist notes that" / "The brief states that" tails trimmed when the citation already carried the load
- "Effectively places" → "places straight" / "puts" (6.1)
- "Rhetorical fig leaf" (jargon-adjacent) → deleted, replaced with direct language
- Multiple instances of "rather than" → em-dash pivot where it preserved meaning
- "Mathematically fixed throughput maxima" kept (technical, load-bearing); "fundamentally" / "arguably" / "essentially" were not present to cut
- "Meaningfully more accountable" kept in 5.2.4 because the qualifier is the argument; would not trim without weakening the point
- Doubled qualifiers stripped: "very" / "genuinely very" / "actually" where the sentence carried without them

Passive voice converted to active where the actor mattered:
- "...are being asked to finance an expanding capital envelope" → "Airports finance..."
- "A bad concourse is a balance-sheet obligation" kept (the actor genuinely does not matter; concourse qua concourse)
- "Bond covenants require debt service" kept (actor = the covenant, literal and correct)

---

## Specifics the draft didn't have — flagged for the Fact-checker

These are places the Strategist used a non-specific claim because the number isn't in any Stage 1 brief. I did not invent substitutes; I preserved the Strategist's disclosures and flag them here for the Fact-checker to resolve against primary sources (MWAA's published capital plan, ACFR, bond filings, authority procurement records).

1. **Project Journey discretionary sub-tranche dollar value.** The draft uses an analyst-estimated **$350–750M (15–30% of $2.4B)** constructed by analogy to the AIP ratio. The brief does not disclose the mandatory/discretionary split of Project Journey. The Fact-checker should verify this against MWAA's capital plan line items for Terminal B/C redevelopment. (Sec 6.1)

2. **Concourse E sub-project cost.** Stage 1 briefs do not disclose a Concourse E sub-project cost; only that Concourse E is within the $9B program. The draft uses an analyst-estimated demand-contingent tranche of **$200M–$600M**. Fact-checker should pull the figure from the authority's published plan. (Sec 6.2)

3. **DCA operational intelligence stack envelope ($15–50M).** Analyst-derived from the digital twin $15–40M benchmark. The brief provides no integrated-stack cost anchor for a US large hub. Fact-checker should attempt to anchor to MWAA or peer-airport procurement records. (Sec 6.1)

4. **IAD operational intelligence envelope including A-CDM ($20–60M).** Analyst-derived from the digital twin benchmark with additional data-governance weighting. Munich SESAR DMAN installation-level cost is not disclosed in the brief. Fact-checker should attempt to anchor to Frequentis, Indra, or Thales published deployment costs at comparable hubs. (Sec 6.2)

5. **APOC envelope ($15–40M combined).** Analyst-derived from the digital twin benchmark plus facility allowance. No brief-cited APOC cost exists. SFO's January 2026 facility is described without a dollar figure. Fact-checker should try to obtain SFO's capital cost and any comparable European benchmarks. (Sec 6.5)

6. **MWAA $1–3B discretionary tranche estimate.** Constructed by analogy to AIP's 50%+ mandatory pavement/safety ratio. No authority-level disclosure of the mandatory/discretionary split. Fact-checker should verify against ACFR, bond filings, and published capital plan. (Sec 3.7)

7. **Five-condition test for other US large hubs (ATL, MCO, IAH, DTW/MSP, IAD).** Conditions (a) peak-hour utilization and (d) DSCR trajectory require airport-specific disclosures neither Stage 1 brief compiles. The draft identifies these as candidates only; Fact-checker should verify against each hub's published data before any citation outside this paper. (Sec 5.2.6)

8. **"Orlando's JetBlue 25% turn variance"** — the draft attributes this to OAG data cited in the Operations brief (Finding 3). Worth double-checking the brief carries the exact figure and the exact carrier attribution before quoting externally.

9. **"15 candidate" vs. "19 candidate" runway-expansion populations (Bilotkach/Mueller).** Draft is clear that the Operations brief does not state mutual exclusivity of the two subsets. The Fact-checker should check the underlying Bilotkach/Mueller paper itself to determine whether the 15 and 19 groups overlap. If they overlap, it strengthens the thesis; if they do not, the combined "34 of 55 / 62%" headline the draft withdrew may be recoverable. Either way, the underlying paper should be re-consulted rather than relying on the brief's silence.

10. **"DSCR covenants typically 1.10x–1.50x depending on indenture"** — the parenthetical qualifier is analyst knowledge, not brief-sourced. Fact-checker should confirm the typical MWAA indenture covenant.

---

## Places the Strategist was weakest — Fact-checker should pay special attention

1. **Section 6.1 DCA defeat-test formula.** "For every 10% sustained 95th-percentile wait-time reduction, one increment of discretionary hold-room square footage is deferred or cancelled." The "increment" is undefined. This is a pre-registration contract term; it needs a concrete definition (square feet per increment, or a formula that maps wait-time reduction to specific cancelled line items). Currently analytical but not operationally pre-registered. Fact-checker and Red Team should flag.

2. **Section 6.2 IAD one-for-one formula.** "A 7% throughput gain yields at least a 3.5% gate-count reduction; a 10% gain yields 5%." The ratio is not half-derived, and the mapping from throughput-gain-percentage to gate-count-percentage has no stated analytical foundation. It is mechanistically plausible but the coefficient is a choice. The Fact-checker should either verify this is a reasonable operational rule-of-thumb or request a Strategist justification.

3. **Section 3.4's A-CDM paragraph structure.** The draft stacks the EUROCONTROL 17-airport finding, then the network-effect caveat, then the Munich single-airport resolution. It reads cleanly now, but the "Munich was inside the European network, so it is itself an inexact proxy — but it is the closest single-airport anchor the brief evidence provides" sentence is the place the thesis is most fragile. If the Fact-checker can find any single-airport A-CDM evidence outside the European network (e.g., Australian, Middle Eastern, or Asian deployments), that would materially strengthen Section 6.2.

4. **Section 5.2.1's three-part categorical distinction from NextGen.** The arguments (airport-level vs. national, COTS vs. custom federal, years vs. decades) are correct but the draft does not provide a direct counterexample of a US airport-level commercial operational intelligence deployment that succeeded on a disclosed basis. Munich is the closest, but Munich is European and partly federal (SESAR). The Fact-checker should look for a US airport-level success case — Philadelphia's surface-metering pilot, or any Charlotte TFDM follow-on data — to anchor this section harder.

5. **Section 3.5 price-tag ratio.** The draft says "single-digit-percentage-of-IT-spend category" for narrow-sense operational intelligence but does not footnote the share explicitly. The Fact-checker could estimate this from the SITA survey's cybersecurity-at-100% and passenger-processing-at-95% figures to put a more defensible floor on what share of the $8.9B is in the narrow operational intelligence category. Currently a directional claim.

6. **Section 3.7's PFC cap figure.** "$4.50 has declined to the equivalent of $2.72 in year-2000 dollars indexed to construction prices — a 40% real loss." The 40% figure should tie cleanly to the $2.72 / $4.50 arithmetic (which would be ~39.6% real loss). Fact-checker should confirm the precise RAND-study figure and whether the 40% is construction-price-indexed or CPI-indexed.

7. **Section 5.2.5 Alaska Airlines and CrowdStrike framing.** "The Alaska Airlines hardware failure produced 150 cancellations at a carrier with approximately 1,300 daily flights — a bad day, not a systemic failure." The 1,300 daily flights is analyst context, not brief-sourced. Fact-checker should confirm Alaska's daily schedule size as of 2025 before this framing is used externally.

---

## What I did not change

- Every dollar figure and percentage in the draft.
- Every citation tag.
- The order of sections and subsections.
- Any defeat-test threshold (20%, 9%, 7%, 4%, 0.5-minute, etc.).
- Any envelope range ($1–3B, $50–150M, $15–50M, $20–60M, $15–40M, $350–750M, $200–600M, $550M–$1.35B).
- Any verbatim quotation from a Stage 1 brief.
- Any place the Strategist explicitly withdrew a V1 or V2 claim (the withdrawals are governance, not prose, and preserved exactly).
- Any part of Section 4 that presents the Contrarian's argument. Counter-case fairness must survive the edit.

---

## Summary

The v3 draft arrived clean of the banned buzzwords and tightly argued. The cut is 14.8% — the top end of the target range — achieved by compressing citation tails, trimming meta-commentary, shortening long paragraphs into their load-bearing claims, and converting passive constructions where the actor was visible. Every substantive argument, number, and citation is intact. The Fact-checker should focus on the ten specifics flagged above, with Section 6 the priority because it is where the paper makes its concrete recommendations and where the analyst-derived envelopes need external anchors.
