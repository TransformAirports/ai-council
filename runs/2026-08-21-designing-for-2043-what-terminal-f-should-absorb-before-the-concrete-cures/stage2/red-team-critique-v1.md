# Red Team Critique v1 — Evidence Prosecution Brief

**Run:** `designing-for-2043-what-terminal-f-should-absorb-before-the-concrete-cures`
**Target:** `outputs/stage2/strategist-draft-v1.md` (Strategist v1, 2026-08-20)
**Reviewer:** evidence-prosecutor
**Basis:** run manifest roster (12 selected research agents), all 12 Stage 1 briefs, `outputs/stage1/evidence-map.md`, `outputs/evidence-ledger.jsonl` (257 records), targeted ledger pulls quoted below.

Standing note: this draft is better than most v1s. It resists AA's self-reported 50% missed-connection figure, names denominators on the connecting-share dispute, and labels the under-scoping multiplier as professional judgment. The findings below are where it does not hold itself to that same standard. Findings are ordered by damage to the thesis, not by page.

---

## Part 1 — Findings

### F1. The modular change-cost quantification is an unledgered construction stated as fact

- **Location:** Executive summary #2: "A 5% late scope change on a conventional site costs roughly its share of the work; on a modular fabrication line the same change consumes 15–25% of the change budget because it triggers resequencing across pods."
- **Charge:** Invented construction, presented as fact; also a units mismatch.
- **Evidence:** No record in `evidence-ledger.jsonl` contains "15–25" or any variant (grep confirmed zero hits). The figure appears only in evidence-map §6, itself unattributed to a ledger record. The map's own §9 do-not-claim list: "Do not claim retrofit-vs-greenfield cost multipliers as sourced numbers... professional judgment or analyst construction... Present as directional."
- **Compounding problem:** the comparison is incoherent as written. "Costs roughly its share of the work" (a fraction of project cost) is set against "consumes 15–25% of the change budget" (a fraction of a different, undefined base). These are not the same denominator; the sentence reads as a 3–5× multiplier but does not actually state one.
- **Why it matters:** This is the quantitative spine of the report's central reframe (claim #2 of eight). If the fact-checker strikes it, the reframe survives only on the seven-agent qualitative convergence — which is fine, but then the draft must say so.
- **Remedy:** Recalculate or cut the numbers. Either source the multiplier to a named record/engineering reference with a defined denominator, or restate as: "the Chief Engineer, Quantitative Analyst, Operations Analyst, Contrarian, and three other agents converge on the qualitative judgment that post-release changes propagate across the fabrication sequence" — judgment, labeled.

### F2. "The tenant has already told the airport what Terminal F is not" overstates what the Provisions record supports

- **Location:** Executive summary #3; "What the tenant has actually said" ("Read that as a revealed preference... has spent its premium capital at C and D and told the airport what F is for").
- **Charge:** Overstated; missing counterevidence.
- **Evidence:** The Provisions posture is real and heavily corroborated (records 5, 38, 53, 55, 68, 92, 107, 136, 159, 191, 217, 232, 241, 254). But the ledger records carry an explicit caveat the draft's argument body never surfaces: "Whether the Provisions designation is a placeholder or a settled long-term decision is flagged as a known evidence gap" (quantitative-analyst record; same caveat on chief-engineer and technology-scout records; evidence-map §1.2 weakness, §3: "a live signal, not settled fact"). Two omitted alternative readings: (a) timing — Terminal F does not open until 2027, so C and D are the only places AA *could* site premium capital in July 2026; the announcements are equally consistent with sequencing as with tiering; (b) Virtual Chris's ledgered reframe (map §6) that Skylink is becoming AA's premium *spine* and F's premium role may be Arrivals rather than Departures — a reading under which the C-club siting says nothing about F's ceiling.
- **Why it matters:** "Revealed preference" is the draft's single strongest pillar. As written it converts a designation the ledger calls unsettled into a settled instruction, then builds the design brief on it. Decision #4 (get AA's written statement on the U&L lounge obligation) tacitly admits the fact is not in evidence — the executive summary should not assert what decision #4 concedes is unknown.
- **Remedy:** Qualify in the summary and body: "American's announced posture" / "strongest available signal, unconfirmed as a settled U&L commitment." State the placeholder gap where the argument is made, not only in the decision list. Engage the sequencing and Arrivals-premium alternatives explicitly.

### F3. Corroboration of a fact is passed off as corroboration of an interpretation

- **Location:** "The single most-corroborated fact in the entire evidence base is that American is not asking DFW to build a premium anchor at F."
- **Charge:** Overstated; conflation.
- **Evidence:** What twelve records across eight agents corroborate is the *announcement* (Provisions at F; 37,000 sf club at C; Flagship Check-In at D). The interpretation — what it means for F's design brief — is the sharpest disagreement in the swarm (map §4, Tensions A and G: Contrarian vs. seven shell-preserving agents vs. Virtual Chris's Arrivals frame). Also note: the twelve agents corroborated by independently finding the *same* joint press release; that is convergence on one primary source, not twelve independent observations.
- **Why it matters:** The sentence launders the run's most contested judgment through the run's most corroborated fact.
- **Remedy:** Recalculate the wording: "The most corroborated fact in the ledger is the announcement itself. What it means is the swarm's sharpest disagreement, and here is why this draft resolves it the way it does."

### F4. The historical universe drops its sixth case — the one that argues against the draft

- **Location:** Executive summary #5 and "The historical spine": "Four of the six post-deregulation purpose-built hub terminals were dehubbed... The one that aged well, Detroit McNamara..." and the opening's "the only post-1978 purpose-built hub terminal that outlived a strategy shift."
- **Charge:** Cherry-picking; denominator error; missing counterevidence.
- **Evidence:** The aviation-historian brief (line 12) defines the universe: "roughly six times... Four ended badly (Pittsburgh 1992, St. Louis 1998, Cincinnati 1994, Cleveland 1999). One aged well (Detroit McNamara 2002). **One is instructive but inconclusive (JetBlue T5 at JFK, 2008).**" The draft counts four failures plus DTW and never accounts for the sixth. Worse, the T5 case (historian brief Case 3; records 186–187, aviation-historian::ev-94d92992ae9c) is the historian's *strongest argument for the run-prompt thesis*: $875M terminal, $200M T5i retrofit in 2014, ~$100M premium refresh 2025–26 — "total post-opening retrofit spend approaching one-third of original construction cost... pricing [the premium shift] into the 2027 scope is dramatically cheaper than pricing it into 2033 retrofit." The historian brief calls T5 "the strongest available analogue to the Terminal F decision." The draft, which argues generic bones and deferred premium, omits it entirely. ATL's Maynard Jackson / Concourse F (2012, purpose-built premium international floor plate, record 185; historian brief line 61) is also in the ledger and also unaccounted, and it too complicates "the only one that aged well."
- **Why it matters:** The historical spine is claim #5 of eight and supplies the report's design instruction ("generic bones now"). A universe curated to exclude the analogue the source discipline itself ranked strongest is the kind of omission the airport-executive reviewer will find in one read.
- **Remedy:** Restore T5 and ATL Concourse F to the spine and defend the thesis against them — the draft's shell-preservation recommendation can absorb T5's lesson, but it must do so on the page. Correct "the only post-1978 purpose-built hub terminal that outlived a strategy shift."

### F5. "Dehubbed within a business cycle" is false for three of the four failure cases

- **Location:** Executive summary #5.
- **Charge:** Overstated.
- **Evidence:** Terminal-to-dehub intervals from the draft's own citations and the historian brief: PIT 1992→2004 (12 years), CVG 1994→2005–2013 (11–19 years), CLE 1999→2014 (15 years). Only STL (1998→2001–03) fits inside anything a reader would call a business cycle.
- **Why it matters:** The compression makes the historical warning look faster-acting than the record shows; a skeptical reader who checks one date discounts the whole spine.
- **Remedy:** Cut the phrase. "Within roughly a decade to fifteen years of opening" is still a devastating fact against a 2043 lease horizon — use the true number.

### F6. The ATL Delta One delay is given a cause the source does not state, from a 2024-vintage record

- **Location:** "What the tenant has actually said": Delta "has publicly delayed the ATL Delta One Lounge to 2028 because the physical economics of a premium anchor at a mega-connecting-hub are not settled."
- **Charge:** Causal leap; stale data.
- **Evidence:** `contrarian::ev-bbfb17e8f0b1` (confidence: medium, date 2024): Delta "publicly deferred a Delta One Lounge at Atlanta... until a 2028 target opening, and industry observers note Delta has not yet solved premium lounge execution at its major connecting hubs." Caveat on the record itself: "Combines Delta's public announcement with industry commentary." Delta stated a target date; the "because economics are unsettled" clause is industry commentary promoted to Delta's motive. The record is also two years old in a fast-moving lounge program; its 2026 status is unverified.
- **Why it matters:** The draft uses the leader's supposed hesitation as proof the premium-at-connecting-hub question "the industry has not answered." If Delta's delay is a construction-sequencing story, the inference collapses.
- **Remedy:** Qualify ("a delay industry observers attribute to...") and route to the fact-checker to verify the ATL lounge's status as of August 2026 before this survives to v3.

### F7. The IAD AeroTrain claim contradicts its own ledger record

- **Location:** "Why the counter-case is insufficient": "IAD's $3.75 billion AeroTrain extension made necessary by a 1962 routing decision at pour."
- **Charge:** Citation mismatch; invented construction.
- **Evidence:** `infrastructure-economist::ev-818ffbf1eab8`: AeroTrain opened January 2010 without a Concourse D station — the routing decision dates to the 2000s design of the AeroTrain, not to 1962 (1962 is the Saarinen terminal / mobile-lounge era). Second record: the "$3.75 billion" is the budget for the AeroTrain extension *and underground tunnel* inside a $22.5B, 2028–2033 renovation program — not the price of fixing a single omitted stop, and not a committed construction cost ("trade press reporting of MWAA program direction; not a construction contract," per the record's caveat).
- **Why it matters:** This is one of three anchors for "under-scoping is the more expensive error." A wrong date plus an inflated attribution in the same clause invites the reader to discount the other two anchors.
- **Remedy:** Correct to what the records support: a 2000s-era routing decision omitted the Concourse D stop; mobile-lounge operations continued 16 years; the remedy is now folded into a ~$3.75B extension-and-tunnel budget inside a $22.5B program.

### F8. The ratings-slip arithmetic has no ledger record

- **Location:** Counter-case #4: "every 15–30 basis-point ratings slip on the next issuance is a $60–120 million lifetime interest event on the next $2 billion of new-money par."
- **Charge:** Invented construction.
- **Evidence:** No ledger record contains this calculation or its inputs (grep: zero hits on "basis point," "60–120"). The arithmetic is internally plausible (2B × 15–30bp × ~20-year average life) but it is an analyst construction with unstated assumptions about tenor and structure, presented inside a section the draft then endorses ("Each is real. Each survives.").
- **Why it matters:** Endorsed counter-case claims carry the same evidentiary burden as thesis claims. The fact-checker will have nothing to check this against.
- **Remedy:** Either attribute to the quantitative analyst with the assumptions stated (par, average life, level-debt structure), or cut and let the CPE trajectory carry the affordability objection — it is strong enough alone.

### F9. The CPE behavior threshold is judgment stated as law, and the breach prediction is unsupported

- **Location:** Counter-case #4: "airline signatories start changing behavior when connecting-hub CPE crosses the low $20s. Terminal F is likely to breach that band inside the ramp."
- **Charge:** Unsupported (both sentences); the second is an extrapolation with no ledgered projection behind it.
- **Evidence:** The $20–22 threshold is the Airline Strategist's professional judgment (map §1.6: "The Airline Strategist's professional judgment is that CPE breaching $20-22 changes carrier behavior"). No record projects DFW CPE above $16.99 (FY26). The ledger contains no CPE forecast for FY27–FY30, the years "inside the ramp."
- **Why it matters:** "Likely to breach" is doing real work — it is the factual hinge of the affordability objection the draft says "survives."
- **Remedy:** Label the threshold as the Airline Strategist's judgment. For the breach claim: either have the quantitative analyst build the FY27–30 CPE bridge from the debt-service schedule (transparent scenario, stated assumptions) or soften to "the trajectory points toward that band; no public projection confirms it."

### F10. The $12.4B FY29 debt projection predates the scope it is used to characterize

- **Location:** Executive summary #7; counter-case #4. Footnote 15: *The Bond Buyer*, August 2024.
- **Charge:** Stale data, unlabeled.
- **Evidence:** `infrastructure-economist::ev-85be22c1fe28` dates to the August 2024 rating action — nine months before the May 2025 expansion of Terminal F from $1.6B/15 gates to $4B/31 gates (footnote 17). The draft half-acknowledges this ("before the full $4B Terminal F debt stack is layered") but presents $12.4B as the current trajectory. If the pre-expansion projection was $12.4B, the post-expansion number is higher; the map itself flags "post-scope-acceleration rating-agency remodeling has not been published" (§1.6 weakness).
- **Why it matters:** The draft's affordability arithmetic runs on a floor value presented as a forecast.
- **Remedy:** Label the vintage explicitly: "projected $12.4B by FY29 as of the August 2024 rating action, before the Terminal F scope grew by $2.4B — the post-expansion figure has not been published and is higher."

### F11. The $16.99 CPE figure is attributed to the Official Statement, but the OS itself was never retrieved

- **Location:** Executive summary #7; footnote 14 ("in the 2025 A/B bond Official Statement").
- **Charge:** Source-quality failure (provenance, not accuracy).
- **Evidence:** `evidence-curator::ev-cpe-fy26-os` — curator's own note (map §1.6 weakness, §8): "The Official Statement figure was pulled via DWU's aggregation, not the underlying OS PDF itself — a fact-checker should retrieve the primary document if any recommendation quantitatively rests on the $16.99." Two attempts to pull primary documents returned HTTP 403. The draft's footnote 14 asserts direct OS provenance and treats the $16.39 board-briefing delta as "directional, not contradictory" — language lifted from the map without the map's accompanying verification caveat.
- **Why it matters:** The "25% single-year jump" is quoted in the executive summary of a board-facing document and attributed to a bondholder disclosure nobody in this run has opened.
- **Remedy:** Keep the figure; fix the provenance ("per the 2025 A/B Official Statement as aggregated by DWU Consulting; primary document verification pending") and flag footnote 14 for a mandatory fact-checker primary pull.

### F12. The U&L consent requirement is asserted as contract fact the run does not possess

- **Location:** "What the tenant has actually said": "the party whose consent is required under the Use and Lease Agreement for any scope change inside its exclusive-use terminal."
- **Charge:** Unsupported; internally inconsistent with the draft's own decision #4.
- **Evidence:** No ledger record states the U&L consent mechanics (grep "consent": zero substantive hits). The map's do-not-claim list: "Do not claim MII thresholds are known... Every characterization of 'AA veto' is professional judgment from the concentration percentage." The draft's own decision #4 instructs General Counsel to obtain the MII trigger thresholds because they are "load-bearing on whether the reversibility discussion is design or contract" — i.e., the draft elsewhere admits it does not know what it asserts here.
- **Why it matters:** If the consent architecture is softer than asserted, the "revealed preference" argument weakens (the airport has more unilateral room); if harder, several register items may be contractually moot. Either way, stating it as fact pre-answers decision #4.
- **Remedy:** Qualify: "AA's 82% activity share makes its consent a practical requirement under any standard MII architecture; the actual trigger thresholds are confidential and are the subject of decision #4."

### F13. Tension D is resolved silently: the draft asserts one side of a documented internal disagreement

- **Location:** "Bank density, not bank flatness": "Bank contiguity — banks overlapping in time — amplifies gate concurrency; it does not reduce it."
- **Charge:** Missing counterevidence (the run's own).
- **Evidence:** Map §4, Tension D: the COO brief reads AA's 13-bank messaging as a *flatter, mid-day-loaded* operation; the Operations Analyst and Airline Strategist read denser peaks. The map states: "Terminal F sizing depends on which is correct." The draft adopts the denser-peak reading as physics, without acknowledging the COO's read exists — while elsewhere citing the COO's own Skylink scenario as an anchor.
- **Why it matters:** The 6:15 sizing case, the connecting-geometry emphasis, and the register's priorities all descend from the denser-peak read. If the COO is right, the sizing case is over-conservative and the affordability critique bites harder.
- **Remedy:** Name the disagreement and defend the choice (the Q2 2026 data and bank-contiguity logic are defensible grounds — use them as an argument, not as an omission).

### F14. The +6-minute block-time figure is network-wide, deployed as DFW-specific evidence

- **Location:** Executive summary #4 and "Bank density" section: "American also lengthened scheduled block times +6 minutes on 145 markets, which mechanically improves scheduled on-time performance."
- **Charge:** Denominator error.
- **Evidence:** The airport-coo ledger record: "adding an average of 6 minutes of block time across 145 markets (CLT +17, DCA +10, MIA +9) alongside the DFW re-bank." The three named examples are Charlotte, Washington National, and Miami — the 145 markets are a network measure, not a DFW measure. Using it in a DFW-OTP paragraph implies DFW schedules were padded +6 minutes; the record does not say that.
- **Why it matters:** It is used twice, including in the executive summary, to discount the rebank — a discount the draft's thesis depends on.
- **Remedy:** Name the denominator: "network-wide, across 145 markets including CLT, DCA, and MIA."

### F15. Cluster of unsourced specifics presented as fact

- **Location / items:**
  1. "DFW is on its third modular concourse and the Terminal C nine-gate pier was delivered two years after design lock" — neither "third" nor "two years after design lock" appears in any ledger record (Terminal C pier records confirm the pier and the June 2026 opening only).
  2. "At 6:15 a.m., the first arrival bank of American's 13-bank day is on the ground" — no record establishes the 13-bank structure's first-bank timing; the 6:15 case is the COO's constructed scenario (map §1.10 weakness: "professional judgment, not a documented scope"). Present it as the constructed stress case it is.
  3. Decision #1: "monthly standing item at the first-Thursday meeting" — board meeting cadence is not in the ledger.
  4. "The reopening was fall 2021" — the contrarian record says AA "did not *begin* reopening the network until fall 2021"; the network did not reopen at once.
  5. "narrowbody premium share moving from 25% to 40% by 2030" — the record (`airline-commercial-strategist::ev-9b47fcf1b976`) dates the lie-flat growth "by end of decade"; the ledger does not attach "2030" to the 40% narrowbody target. Footnote 21's own text says "by end of decade."
  6. "Chief Engineer, Quantitative Analyst, Operations Analyst, and the Contrarian all converged on the same reading — seven of the twelve independent research agents": four names, then a count of seven. The map's seven are CE, OA, QA, Contrarian, Rams, COO, Aviation Historian. Name all seven or say four.
- **Charge:** Unsupported (items 1–3, 5); overstated (4); internal inconsistency (6).
- **Remedy:** Source or soften each. None is load-bearing alone; together they are the texture a hostile reader uses to impeach the load-bearing material.

### F16. Narrative flourishes that outrun the record

- **Items:**
  1. "the module template ships thirty-one identical, forensically instrumented gates — the one thing DFW gets almost free that no stick-built terminal in the US can match." Three claims — identical, almost free, unmatched in the US — none sourced. The gates are not identical (Code C vs. E vs. MARS mix is a run-level open gap, map §8), instrumentation is not free (draft's own decision #5 contemplates it failing repeat-part cost), and the US-superlative is unverifiable.
  2. "It also names — for the first time in the public conversation about this project — the reader's actual customer." The run has not surveyed the public conversation; "first time" is unverifiable.
  3. "American shifted strategy twice in eighteen months" — used twice as a load-bearing rebuttal premise. The rebank (announced December 2025) and the premium-tier siting (July 2026) are eight months apart, and both are arguably execution moves inside one continuous strategy, not two strategy shifts. The "strategy-shift insurance" rebuttal in "Why the counter-case is insufficient" leans on this characterization; state it as "moved twice on hub structure and premium siting inside eight months" and let the reader weigh it.
- **Charge:** Flourish exceeding factual record.
- **Remedy:** Trim items 1–2; recalibrate item 3.

---

## Part 2 — Claim-to-evidence coverage summary

The draft carries 33 footnotes. Approximately 26 trace cleanly to ledger records with vintages and caveats intact (spot-checked: module move [record 156], Provisions cluster, rebank [ev-e4842e2ba510], Q2 2026 OTP [ev-6ad1dbdb3363], Delta Q4 2025 premium [ev-ed425c651135], Flagship closures [ev-02c3980fc7b3], CBP/TSA geometry [records 199–200, 84–85], Skylink single-loop [record 161], Jan 2023 storm [record 162], §365 record [ev-80e5b480748b], CPE peer table [ev-37a6763aa555], Denver [205–207], T5 Heathrow [209, 132–133], LGA [211–212], 930/100k peak-day [ev-0f74c40d0b6e, which itself pairs the two figures]).

Claims with **no ledger record**: the 15–25% change-budget multiplier (F1), the $60–120M ratings arithmetic (F8), the CPE-breach prediction (F9), the U&L consent mechanics (F12), "third modular concourse" / "two years after design lock" / first-Thursday board cadence / 6:15 first-bank timing (F15). Claims **contradicting or exceeding their record**: IAD 1962 (F7), ATL delay causation (F6), block-time denominator (F14), "reopening was fall 2021" (F15.4).

## Part 3 — The five most load-bearing claims, and whether each survives

1. **Release-for-fabrication is the operative deadline; post-release modular is change-hostile.** Survives — on the seven-agent qualitative convergence. Does not survive with the 15–25% quantification as written (F1).
2. **The Provisions posture means Terminal F is not the premium anchor.** Survives only in qualified form. The announcement is the ledger's most corroborated fact; the "revealed preference" interpretation is contested inside the run, carries an unsettled-placeholder caveat on the records themselves, and has two unengaged alternative readings (F2, F3).
3. **The rebank densifies the peak; size to the connecting geometry.** Survives as a defended judgment, not as fact — Tension D must appear on the page (F13), and the block-time evidence must be re-denominated (F14).
4. **The historical spine: generic geometry outlives carrier strategy.** Survives in corrected form. The universe must include JFK T5 and ATL Concourse F, "within a business cycle" must go, and the draft must answer T5's pro-provisioning lesson directly (F4, F5). Properly handled, the corrected spine is *stronger* — a thesis that survives its best counterexample is worth more than one that hides it.
5. **The affordability trajectory constrains the register.** Survives directionally; every number in it needs its vintage and provenance label ($16.99 via aggregator, F11; $12.4B pre-dates the scope expansion, F10; the breach-of-$20s prediction is currently unsupported, F9).

## Part 4 — Counterevidence minimized or omitted

- **JFK T5's retrofit arc** — the historian's declared "strongest available analogue," arguing premium should be priced into the 2027 scope. Omitted entirely (F4).
- **ATL Maynard Jackson / Concourse F (2012)** — a purpose-built premium international floor plate at a mega-connecting-hub that works; in the ledger (record 185); complicates both "only DTW aged well" and "premium at connecting hubs is unsettled." Omitted.
- **Virtual Chris's Arrivals-premium / Skylink-spine reframe** — a ledger-anchored alternative under which the C-club siting does not demote F. Omitted (F2).
- **COO's flatter-profile reading of the rebank** — the other side of Tension D (F13).
- **Operations Analyst's Tension C position** ("modular arbitrage collapses the flex premium — spend it") — the draft presents the change-hostility consensus without acknowledging the one selected agent who draws the opposite spending conclusion from the same facts.

## Part 5 — Acquittals: claims that are well supported and honestly handled

- The **50% missed-connection figure** is correctly quarantined as AA-reported, two weeks post-launch, and set against the sober Q2 2026 audit. Exemplary.
- The **connecting-share denominator discipline** (60% airport-level vs. ~two-thirds carrier-level, both cited, denominators named) follows the map's instruction to the letter.
- The **under-scoping multiplier** is explicitly labeled "a professional judgment held by seven of the twelve independent research agents." This is the standard F1, F8, and F9 should be brought up to.
- The **August 2026 module move facts** (six modules, 278×136 ft, 3,320 tons, ¾-inch tolerance) match record 156 exactly.
- **Delta's Q4 2025 premium-over-main-cabin crossing** and FY totals match `ev-ed425c651135`.
- The **Flagship closure history** (March 2020, ~18 months, JFK excepted) matches the contrarian record, save the reopening nuance (F15.4).
- The **counter-case section as a structure** is genuinely adversarial — the four objections are the strongest available and are not strawmen. The problem is not the section's honesty; it is that two of its quantitative planks (F8, F9) are unsourced.

---

## Instruction to the Strategist

Fifteen of sixteen findings are repairable without moving the thesis. The exception is F2/F3/F4 taken together: if the Provisions interpretation is qualified honestly and T5 is allowed on the page, the draft's conclusion ("generic bones, conditioned premium shells, priced register") still stands — but the *route* to it must run through the counterexamples, not around them. That version is more durable and, for this audience, more persuasive. Answer each finding by number in v2.
