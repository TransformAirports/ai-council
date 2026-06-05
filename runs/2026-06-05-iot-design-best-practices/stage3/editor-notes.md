# Editor Notes — "The Sensor Outlives the System"

Stage 3 edit of `outputs/stage2/strategist-draft-v3.md` → `outputs/stage3/edited-draft.md`.

## Word count

| | Words |
|---|---|
| Strategist v3 as delivered | 11,196 |
| — of which "Handoff Notes" meta-section (instructions to editor/fact-checker, not report content) | ~430 |
| v3 actual report content | ~10,766 |
| **Edited draft** | **9,937** |

Reduction from the full v3 file: **11.2%** (1,259 words). Reduction from actual report content: 7.7%.

This lands below the 15–25% target. That is a deliberate, documented editorial judgment, not an incomplete pass — see "Why not 15%" below. The draft is unusually dense: nearly every sentence carries an argument step or a named piece of evidence, the run **mandates** a 6–10 case catalog (the draft runs the full 10), and the executive summary is already **947 words, under its ~1,100-word spec**. Reaching 15% by trimming prose alone is not possible without stripping evidence the brief forbids me to remove (rule 9).

## What I changed

**1. Removed the "Handoff Notes — weaknesses knowingly left in" section (~430 words).** This was meta-commentary addressed to the editor and fact-checker ("weaknesses knowingly left in"), not part of the report. It does not belong in a reader-facing draft. The substantive honesty it flagged is already carried in the body (the unobservable-stranding-rate concession, the "two network upgrades is aspirational" qualification, the staffing constraint).

**2. Buzzwords — eliminated.** The only banned word present was "leverage," in four places. Replacements:
- "highest-leverage decision" → "most consequential decision"
- "the vendor's leverage is absolute" → "the vendor holds every card"
- "the practical leverage points the same way" → "the practical power points the same way"
- "the most leverage it will ever have" → "the most bargaining power it will ever have"

Confirmed clean on a full sweep: no leverage / synergy / holistic / best-in-class / paradigm shift / game-changer / mission-critical / absolutely / ecosystem / seamless / robust / world-class.

**3. Cut restatement closers and cross-section duplications** (the bulk of the legitimate trim):
- Removed "because no credible stranding rate exists in the public record" — restated the sentence's own opening.
- Removed "The record of what endures does not obviously favor the report's recommendation" — restated the two sentences before it.
- Removed the duplicated procurement-officers/incumbent-vendors explanation in the MWAA section (the same clause appears in full in the contract-sentences section; kept it there, trimmed the echo).
- Trimmed the "concede everything by name" clause-list in the Counter-Case rebuttal (it previewed points the following paragraphs then make in full).
- Collapsed the "cheapest moment is now / before the slab is poured / cheaper in design than retrofit" triple in the MWAA opener to a single statement.
- Tightened the executive-summary point 2 tail (it restated the same point's own bolded lead about the unobservable rate).

**4. Fixed announce-y transitions.** "A reader who came in skeptical should, at this point, feel the case has been made fairly. It has. Now it has to be answered." → "A reader who came in skeptical should feel the case has been made fairly. Now to answer it."

**5. Rhythm.** Split the longest paragraph (the Rotterdam/Schiphol/Barcelona "well-resourced public entity" objection, ~10 sentences) at its natural seam — the objection, then the narrower prescription. Left the narrative case-study paragraphs (3G open, Pearson, Orly, Sigfox) intact as deliberate story-units; chopping them into uniform declaratives would flatten the voice the run wants (Matt Levine, not a consultant deck).

**6. Active voice and minor tightening** throughout, preserving the rhetorical short paragraphs ("That is the shape of the problem. Not the sensor.") and the poetic close.

## What I deliberately did NOT cut

- **The 10-case catalog.** The run mandates 6–10; the draft runs 10 (Pearson, Orly, Sigfox, Cisco Kinetic, 3G sunset, Charlotte Douglas, Dallas Love Field, Denver, iFlow, AirAsia/klia2). Every case names the specific architectural decision that doomed it — this is the report's core evidence, not bloat.
- **The repeated through-line** ("decouple at the schema and broker; name an accountable owner with a defined successor; write exit cost into the contract"). It recurs by design as a drumbeat across the argument, counter-case rebuttal, and MWAA sections. Thinning it would soften the conclusion (rule 9).
- **The executive summary**, already under spec at 947 words.

## Flags for the Fact-checker

1. **`[FACT-CHECK: which airport ran iFlow?]`** — inline at the iFlow case (the 400+ Wi-Fi AP / 130 people-counter / 50 Bluetooth deployment). The draft says "a major hub" but never names it. The Stage 1 brief should identify the airport; if it can't, this case is weakened and may need the hedge made explicit. This is the only place I left a hedge ("a major hub") standing because the specific is not in the draft.
2. **Cross-check the recurring numbers** the argument leans on hardest, several of which appear in multiple sections and must agree: 3G shutdown completed Dec 2022; Sigfox €91M loss on €24M revenue, acquired €25M; Denver Great Hall settled $183.6M at 30% design; Denver baggage $193M → $360–400M; license fees 20–40% of 3-yr TCO; 75% of US private 5G on CBRS; Delta Baggage AI 99.9% scan / 120M+ bags; United ~$2B AWS savings; PFC frozen at $4.50 since 2001 (= ~$7.85 in 2026 dollars); IIJA Airport Terminal Program window closed Jan 15, 2026; MWAA $9B program / $6.99B at Dulles / United Concourse E $500M+, 14 gates, 435,000 sq ft, announced Dec 2024; airfield-lighting gateway 43 ms vs. 500 ms stop-bar limit. I changed none of these; flagging the load-bearing ones for verification against the briefs.

## Decision for the human checkpoint

If a reduction closer to 15% is required, the only lever that does not strip evidence the brief protects is **the run's own latitude on catalog length**: the spec asks for "6–10" cases, and the draft uses 10. Dropping the two **"stranding-in-waiting"** cases (Charlotte Douglas pavement sensors and Dallas Love Field's Boingo CBRS network) — the only two that are *predictions* rather than documented casualties — would remove ~300–400 words and still satisfy the catalog requirement at 8 cases. I did **not** make that cut on my own authority because it removes named deployments (an argument/evidence decision that belongs to the Strategist or the human), and because Love Field is later reused as the live example of spectrum-allocation risk in the network section, so cutting it would require a second edit there. Recommend treating this as a checkpoint decision rather than an editor's call.
