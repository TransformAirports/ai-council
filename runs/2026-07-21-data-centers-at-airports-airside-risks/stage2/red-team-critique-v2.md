# Red Team Critique — Strategist Draft v2

**Target:** `outputs/stage2/strategist-draft-v2.md`
**Prior critique:** `outputs/stage2/red-team-critique-v1.md`
**Verified against:** all 14 Stage 1 briefs in `outputs/stage1/`

---

## Verdict

v2 is a real revision, not a cosmetic one. The geography disaggregation, the two-stage configuration-first screen, the two-instrument jurisdiction split, the casebook, and the fourth rebuttal all answer v1 directly. Section E at the bottom lists what is fixed so the Strategist does not re-litigate solved items.

But the revision introduced **at least five new factual errors**, and — worse — the **revision notes themselves contain two demonstrably false claims about what the Stage 1 record contains**. A revision-notes section that misstates the source record is a process failure, not a prose failure. The fact-checker will catch some of these; the ones it won't catch (the invented installed/permitted reconciliation, the misattributed cites) are the dangerous ones.

Priority order for v3: items 1–5 (new errors), then 6–9 (revision-notes integrity), then 12–13 (screen gaps), then 20–22 (missed evidence), then the rest.

---

## A. New errors v2 introduced

### 1. "27-gigawatt-class backup fleet" — a ~78x single-facility inflation

- **Location:** "Why the Counter-Case Is Insufficient," third rebuttal.
- **Issue:** The sentence reads: "A warehouse does not run a 27-gigawatt-class backup fleet during the ice storm that already closed your runway." The 27 GW figure is Virginia's **statewide** permitted backup-generation capacity (Operations-Analyst, citing Virginia Mercury). No single campus approaches it. The largest single-campus fleet in the record is ~345 MW (COO brief, the 138-generator Colorado campus); the Contrarian brief puts typical hyperscale campuses at 150–250 MW. You have taken a state-level aggregate and hung it on a hypothetical single facility in a rhetorical comparison with a warehouse. That is a 78-to-100x inflation, in the exact paragraph whose job is to prove the draft is more careful than its critics. If the Contrarian were reviewing this draft, this sentence is the one he would read aloud.
- **Recommendation:** "A warehouse does not run a 345-megawatt-class backup fleet" — or, if you want the honest typical case, "a fleet of diesel generators measured in the hundreds of megawatts." Keep the 27 GW where it belongs: as the statewide aggregate that shows how big the cumulative problem is.

### 2. The 240,000-gallon diesel figure sits on a gallons/liters contradiction inside its own source

- **Location:** "The tenant the airport did not staff for," fuel-storage paragraph: "store from roughly 25,000 up to 240,000-plus gallons under NFPA 30 [Director-of-Public-Safety brief, citing PowerMag]."
- **Issue:** The DPS brief contradicts itself. Its key-findings line says "240,000+ gallons"; its own evidence section says a 10 MW Tier-IV plant needs "~240,000 **liters** (~63,400 gallons)." Same number, different units, a 3.8x spread — and the draft picked the larger, internally contradicted figure without flagging the conflict. The fact-checker will trip on this, and if it slips through, any reader who knows diesel logistics will do the arithmetic.
- **Recommendation:** Use "roughly 25,000 to 63,400 gallons for a 10 MW plant, scaling with campus size" and add a bracketed note for the fact-checker that the DPS brief's key-findings line appears to have converted liters to gallons incorrectly. Or verify against PowerMag directly and state which unit is right.

### 3. The "installed vs. permitted" generator reconciliation is invented

- **Location:** Executive Summary, point 2: "roughly 4,700 **installed** backup generators in Loudoun County [Chief-Engineer brief, citing VPM]; statewide, Virginia has **permitted** more than 10,500 [Operations-Analyst brief, citing Virginia Mercury]."
- **Issue:** No brief makes the installed/permitted distinction. The Chief-Engineer/VPM figure is "about 9,000 backup generators statewide, ~4,700 in Loudoun alone" — no label at all. The Emergency-Management brief (citing Environment America) explicitly describes Loudoun's 4,700 as "**permitted** at 12 gigawatts" — directly contradicting the "installed" label the draft assigns. And the CE brief's 9,000-statewide figure has been silently dropped rather than reconciled with the Ops brief's 10,500. The draft manufactured a tidy taxonomy to dissolve a source conflict, then presented the taxonomy as sourced. This is v1 item 6's sin in new clothes: the numbers now *look* reconciled, which is worse than looking contradictory.
- **Recommendation:** State the conflict plainly: "Counts vary by source and vintage — 4,700 generators in Loudoun alone [CE, EM briefs], and between 9,000 [CE, citing VPM] and 10,500+ [Ops, citing Virginia Mercury] statewide." Three sources, one honest range. Do not assign installed/permitted labels no source supports.

### 4. The 25–35% power penalty is misattributed to the Technology-Scout

- **Location:** "Why the market will always argue 'yes,'" the reconciliation paragraph: "still burns 25–35% more power [Technology-Scout brief]."
- **Issue:** The 25–35% figure appears only in the Infrastructure-Economist brief (DOE, via Data Center Knowledge). The Technology-Scout says dry cooling "uses more power" with no number. The draft's *first* use of the figure, earlier in the same section, cites Infrastructure-Economist correctly — so this is a copy-edit failure, but it is exactly the kind the fact-checker exists to veto.
- **Recommendation:** Change the second cite to [Infrastructure-Economist brief].

### 5. "On short final" is an invented scene detail, and the 45° splice is unflagged

- **Location:** "The wrong day," WACAZ paragraph: "a wing has been thrown past 45 degrees of bank on short final by exactly this mechanism."
- **Issue:** Two problems in one clause. First, the Technology-Scout/WACAZ record documents a 50–60° roll upset at ~550 ft AGL over cooling towers — nothing in any brief says "short final." That is novelistic dressing, the same class of error as the CID scene v1 item 14 flagged. Second, "past 45 degrees of bank" splices the MITRE upset threshold (45°, from the Ops brief) onto the WACAZ event as though 45° were the reported figure, when the reported figure (50–60°) is actually *stronger*. You weakened your own evidence while decorating it.
- **Recommendation:** "a wing has been rolled 50 to 60 degrees at 550 feet by exactly this mechanism [Technology-Scout brief]" — the true number beats the borrowed one, and the altitude is more concrete than the invented phase of flight.

---

## B. The revision notes contain false claims about the source record

### 6. The $207M "could not source to any brief" claim is false

- **Location:** Revision notes, sourcing bullet: "$207 million net… I could not source to any brief."
- **Issue:** Three briefs carry it. Infrastructure-Economist: "~$200–207M net of costs." Airline-Commercial-Strategist: "net ~$207M." Airport-CEO: "netting ~$207M." Standardizing on the $236.5M gross figure is a defensible editorial call — but the stated reason is factually wrong, and it deprives the reader of the more damning number: MWAA *netted* about $207M for land that foreclosed a runway option forever.
- **Recommendation:** Restore the net figure with its three-brief citation: "sold for $236.5 million, netting roughly $207 million after costs [Infrastructure-Economist, Airline-Commercial-Strategist, Airport-CEO briefs]." Correct or delete the revision-note claim.

### 7. The KCI/Kestrel "no brief documents it in usable detail" claim is false

- **Location:** Revision notes: "no Stage 1 brief documents it in usable detail; I will not manufacture a case the panel did not research."
- **Issue:** The Emergency-Management brief documents Kestrel specifically: a ~380-acre, six-building, 1.8-million-square-foot data-center project immediately north of Kansas City International, part of a $100B corridor [KCTV5]. The Contrarian brief carries the ~380-acre program too. That is more documentation than the draft's Inyokern entry rests on. The high-minded refusal ("I will not manufacture a case") is built on not having read the record.
- **Recommendation:** Either add Kestrel to the casebook with the EM-brief sourcing, or drop the revision-note claim. Do not leave a false statement about the record in a document the fact-checker will audit against that record.

### 8. "Name the cost honestly" survives its own claimed deletion

- **Location:** Revision notes claim the imperative asides were "deleted ('Read that sequence again,' 'Name the cost honestly')" — but "Implications for MWAA," the "Choose the lease" bullet, still opens: "Name the cost honestly: the covenant-heavy lease is the slower, lower-upfront-cash instrument."
- **Issue:** Minor as prose, major as process: the revision notes assert an edit that was not made. Combined with items 6 and 7, that is three false statements in one revision-notes section.
- **Recommendation:** Delete the phrase ("The covenant-heavy lease is the slower, lower-upfront-cash instrument" stands fine alone), or keep it and correct the note.

### 9. "Walk the five operating states" is an overclaim; and should revision notes ship at all?

- **Location:** Revision notes; "The wrong day," first paragraph.
- **Issue:** The notes claim the draft now "walk[s] the five operating states the run file asked for." The draft lists them in one sentence — "normal cooling, peak demand, generator testing, utility outage, and prolonged emergency generation. They do not share a controlling envelope" — and then analyzes two of them. Listing is not walking. Separately: a revision-notes section is process metadata. It has no place in an executive deliverable; it exists to talk to me, and I am not the audience of record.
- **Recommendation:** Either genuinely walk the five states (two to three sentences each: which hazard peaks, in which weather) or drop the claim. Move revision notes to a separate file or strip them before the Editor pass.

---

## C. v1 items only partially fixed

### 10. The screen still omits the hot-day turbulence envelope the draft's own prose concedes

- **Location:** "Implications for MWAA," Stage 2 plume-study bullet, vs. "The wrong day," second paragraph.
- **Issue:** The prose now correctly concedes (per the Ops brief) that "turbulence peaks at peak sensible-heat rejection — the hottest day." But the screen — the operational instrument the whole document exists to deliver — requires modeling only "the full islanded-generation load case under calm, cold, stable conditions for turbulence, and the cold-humid evaporative case for visible obscuration." The hottest-day dry-cooler case, acknowledged as a peak in the body, is absent from the tool. This is the identical prose-vs-tool gap v1 item 2 flagged on tiering: the argument learns, the checklist doesn't.
- **Recommendation:** Add the third envelope to the bullet: peak-ambient, full-IT-load, dry-cooler operation for buoyant turbulence. Three envelopes, one sentence.

### 11. The briefs disagree on which day is the controlling turbulence case, and the draft picks a side silently

- **Location:** Executive Summary, point 2 ("turbulence… peaks on the hot dry day"); "The wrong day."
- **Issue:** The Ops brief says turbulence peaks at maximum sensible-heat rejection (hottest day, full IT load). The Deep-Research brief says "the most critical scenario is a cold, still day with full IT load: the large temperature delta causes strong updrafts." These are physically different claims about the same hazard. The draft adopts Ops without acknowledging Deep-Research disagrees — and adds "dry" to "hot day" on its own authority. A draft whose thesis is "model the envelopes, don't assume the controlling case" should not itself assume the controlling case.
- **Recommendation:** Note the disagreement explicitly — it *strengthens* the argument: "the panel's own sources disagree on which day is worst, which is precisely why the screen requires modeling all three envelopes rather than trusting anyone's intuition about the controlling case."

### 12. 424 vs. 433 acres — still no variance note

- **Location:** Throughout (Western Lands passages).
- **Issue:** v1 item 8 asked for a fact-checker note: five briefs say 424 acres, the Airport-CEO brief says 433. The draft uses 424 with no note. Correct choice, undocumented.
- **Recommendation:** One bracketed note at first use: "[424 acres per five briefs; CEO brief says 433 — using majority figure]."

### 13. Executive Summary point 7 ships the inflammatory version; the fairness arrives 1,400 words later

- **Location:** Executive Summary, point 7, vs. "The risk you cannot un-build."
- **Issue:** The summary says the tract was "assembled in 2005–2007 for a fourth runway" and sold — full stop. The body's caveats (the fourth runway was built in 2008; the parcel was "runway-adjacent, not runway-critical"; the live fifth-runway alignment is on the south side) arrive well over a thousand words later. An executive who reads only the summary — most of them — gets a version the Strategist's own body text says is unfair. That is cherry-picking your own draft.
- **Recommendation:** One clause in point 7: "…assembled in 2005–2007 during the fourth-runway program — runway-adjacent, not runway-critical — and sold in 2018…" The claim survives the honesty; that is the test of a claim worth making.

### 14. "Materially impacts the safe and efficient operation of aircraft" appears four times

- **Location:** Executive Summary point 5; §743 section (twice); "Implications for MWAA."
- **Issue:** v1 item 24, unfixed. A quoted statutory phrase is a scalpel; the fourth use is a butter knife. By the last occurrence the reader has stopped hearing it.
- **Recommendation:** Quote it once, in the §743 section, in full. Thereafter: "the §743 standard" or "the materially-impacts test."

### 15. The glare bullet miscites its language and drops the Ops brief's sharpest instrument

- **Location:** "Implications for MWAA," NAVAID/lighting bullet: "lighting/glare review to downward-shielded, non-specular standards [Technology-Scout, Chief-Engineer briefs]."
- **Issue:** Two problems. The "downward-shielded, non-specular" formulation is the COO brief's, not Tech-Scout's or the Chief-Engineer's. And the Ops brief hands you the strongest precedent for the entire screen concept — the FAA's solar policy requiring a Sandia Glare Hazard Analysis *before* Form 7460-1 filing — which is a live example of the FAA already demanding a physics study beyond geometry for one facility type. The draft's core claim is "the FAA reviews geometry, not physics"; the solar carve-out is both the exception that proves it and the template for extending it. It appears nowhere.
- **Recommendation:** Fix the cite to [COO brief]. Add one sentence, in the screen or the §743 section: the FAA already requires a quantified glare-hazard analysis for solar farms before airspace filing [Ops brief] — the screen asks for nothing more novel than extending that logic to heat.

### 16. Fire-water cite conditions on a distinction its source doesn't make

- **Location:** "The tenant the airport did not staff for": "an *evaporative* hyperscale campus draws 1 to 5 million gallons a day [DPS brief]."
- **Issue:** The DPS brief gives 1–5M gallons/day without conditioning on cooling type; the evaporative conditioning comes from the Infrastructure-Economist ("Evaporative cooling — the source of… 1–5 million gallons/day"). The follow-on sentence — "a closed-loop or dry-cooled facility… draws a fraction of that" — is uncited entirely (supportable via Tech-Scout's "no water consumed" for dry cooling).
- **Recommendation:** Joint cite the first [DPS, Infrastructure-Economist briefs]; cite the second [Technology-Scout brief].

### 17. "Every unit comes from mutual aid" universalizes a Daejeon-specific fact

- **Location:** "The tenant the airport did not staff for," Daejeon paragraph.
- **Issue:** The DPS brief says every unit **on that fire** came from mutual aid. The draft's present-tense generalization — that any such fire anywhere draws entirely on mutual aid — is not in the record and is not even obviously true for an airport with on-site ARFF.
- **Recommendation:** Past tense, Daejeon-specific: "Every unit on that fire came from mutual aid [DPS brief]." The specific case is scarier than the vague generalization anyway.

### 18. Two small precision drifts

- **Location:** (a) "Why the market will always argue 'yes'": "clearing **near** the FERC cap." (b) Casebook, Manassas entry: "no formal seat."
- **Issue:** (a) The Infrastructure-Economist brief says clearing "**at** the FERC cap of $329.17/MW-day" — the draft softened a hard number. (b) "No formal seat" is a rhetorical extension; the Ops brief documents the Manassas situation but not that phrase or that specific procedural fact.
- **Recommendation:** (a) Restore "at the FERC cap of $329.17 per megawatt-day." (b) Rephrase to what the brief supports, or mark it as inference.

---

## D. Missed evidence and missed lenses

### 19. The dehubbing casebook — the strongest historical-arc material in the record — is unused

- **Location:** "Implications for MWAA" and "The risk you cannot un-build" (absence).
- **Issue:** This run has no aviation-historian brief; the Airline-Commercial-Strategist brief carries the historical load instead, and the draft leaves it on the table. The brief documents five dehubbing collapses — CVG/Delta, PIT/US Airways, STL/TWA-American, CLE/Continental-United, MEM/Northwest-Delta — and draws the mirror-image lesson explicitly: "A data center that eliminates the airfield's growth path does the dehubbing damage pre-emptively — it removes the carrier's option to grow before the carrier has decided whether to." The MWAA section argues United-concentration risk (49.9% of passengers, 62% of seats) with no historical teeth. Five carcasses are the teeth. Also unused from the same brief: the CPE spread ($3.93 at ATL to $36.01 at JFK, median ~$12.88) and the brief's three pre-approval carrier tests, which map directly onto the screen.
- **Recommendation:** Two to three sentences in the MWAA section: name two or three of the five cases, deploy the pre-emptive-dehubbing line, and cite the brief. Consider folding the carrier tests into the Stage 2 study package.

### 20. Dulles Cloud South is missing from a casebook it belongs in

- **Location:** "The casebook."
- **Issue:** The COO brief documents Cloud South's rejection by Prince William County (July 2026) and hands you the thesis on a plate: "It died on local land-use politics, not on an aviation-compatibility finding. That is the tell." Tech-Scout has the scale (~56M sq ft proposed south of IAD); Deep-Research has the flight-path geometry (south of Dulles sits under north-flow departures and south-flow missed approaches). A fifth case, at the draft's own airport, better documented than Manassas, proving the draft's exact claim — that the deciding instrument is never the airside test. Its absence from a casebook that found room for Inyokern is inexplicable.
- **Recommendation:** Add Cloud South as the fifth (or lead) casebook entry. It is the only case in the record where the flight paths, the scale, and the decision mechanism are all documented *for the airport this report is addressed to*.

### 21. The Byron Airport precedent — the mechanism's origin story — is unused

- **Location:** "The wrong day" / "A geometry test for a machinery problem" (absence).
- **Issue:** Virtual-Chris and Deep-Research both document the 2010 Byron, CA fight over a 200 MW plant 2.6 miles out: pilots reporting invisible plumes lofting light aircraft 300–500 feet on final, an AOPA objection, and — critically — this fight is the origin of the MITRE plume study the draft leans on. Right now the draft's turbulence evidence is one WACAZ event plus modeling. Byron converts "the literature warns" into a second documented mechanism-in-action, and it gives the screen a lineage: the FAA's own analytical tooling exists because pilots forced the question once before.
- **Recommendation:** One paragraph, probably in "The wrong day," linking Byron → MITRE → the current gap.

### 22. FAA Order 7400.2K §6-3-3 is the missing federal hook for the §743 argument

- **Location:** §743 section (absence).
- **Issue:** Deep-Research surfaces that under Order 7400.2K §6-3-3 the FAA can rule an object a hazard for "physical, electromagnetic, or line-of-sight interference" with flight operations — existing federal authority that reaches beyond geometry. The draft's §743 argument currently asks Congress-and-FAA to build something; §6-3-3 suggests the authority partly exists and goes unexercised, which is a sharper claim. ACRP Report 108 (energy facilities near airports, plume modeling and setbacks) is likewise unused and would give the study-package bullet a named methodology.
- **Recommendation:** Cite §6-3-3 in the §743 section as existing-but-dormant authority; cite ACRP 108 in the Stage 2 study bullet as the methodological anchor.

### 23. Minor unused material

- **Location:** Various.
- **Issue:** Virtual-Chris's waste-heat/district-energy and shared-standby-generation opportunities (the draft uses only the interconnection-siding point) — relevant to the "advocacy off-fence" instrument, where the airport needs something to offer, not just something to demand. The Procurement brief's MWAA board approval threshold (leases >$3M require board action) would ground the governance bullet in an actual tripwire.
- **Recommendation:** Optional adds; the district-energy point is the better of the two because it converts the screen from pure gatekeeping into a negotiation posture.

---

## E. Prose and structure

### 24. The "not X; it is Y" tic survived the purge

- **Location:** Throughout — at least six instances: "it is not an Iowa problem. It is the order…"; "The question is not whether… The question is whether…"; "not category but scale and correlation"; "procedural, not technological"; "a lease clause, not a law of physics"; the §743 framing.
- **Issue:** Each instance is individually fine; six is a metronome. It is the single most recognizable machine-prose signature in the document, and the humanizer will flag it if I don't.
- **Recommendation:** Keep the two strongest ("a lease clause, not a law of physics" earns its place). Recast the rest as direct assertions.

### 25. What v2 fixed — do not re-litigate

For the record, so v3 effort goes where it's needed: the geography disaggregation (Ashburn-overflown vs. Digital-Dulles-west) is honest and correct; the two-stage configuration-first screen answers v1's central structural objection; the two-instrument split (binding on MWAA land, advocacy off-fence) resolves the jurisdiction confusion using the COO's "commenter, not a decider" line properly; the fourth rebuttal finally answers "lighter than a hotel" on the merits; the study-governance bullet (developer-funded, airport-directed, Brooks Act) closes v1 item 20; the interconnection causal chain, the ¼-acre/5,000-ft bright line, the test-hours reconciliation, the 20-to-30-year-asset/40-to-50-year-lease split cite, the layered bird-strike numbers, and the "fatal"→"decisive" downgrade are all verified against the briefs and correct. The Contrarian quotes are verbatim. The closing paragraph — "It will probably operate, under conditions the airport is now negotiating from weakness" — is the best sentence in the document. Protect it.

---

## Priority for v3

1. **Items 1–5** — new factual errors. The 27 GW inflation (item 1) and the invented installed/permitted taxonomy (item 3) are the two the fact-checker is least likely to catch and the Contrarian most likely to weaponize.
2. **Items 6–9** — revision-notes integrity. Three false process claims in one section. Fix or strip the section.
3. **Items 10–11** — the screen must carry all three plume envelopes, and the Ops/Deep-Research disagreement should be surfaced, not adjudicated silently.
4. **Items 19–22** — the dehubbing casebook and Cloud South are the two highest-value adds in the entire record; both are one-paragraph fixes.
5. **Items 12–18, 23–24** — precision and prose cleanup.
