# Evidence Map — Designing for 2043: What Terminal F Should Absorb Before the Concrete Cures

**Run:** `designing-for-2043-what-terminal-f-should-absorb-before-the-concrete-cures`
**Curator:** evidence-curator
**Compiled:** 2026-08-19 · **Reviewed and gap-filled:** 2026-08-20
**Ledger:** `outputs/evidence-ledger.jsonl` — 257 records (255 from 12 research agents + 2 curator gap-fill records)
**Companion:** `outputs/context/airport-context.md`

This is the Strategist's briefing binder. It ranks the load-bearing evidence, preserves disagreements the swarm surfaced, flags what the record does not actually support, and lists the gaps a $4B decision would want closed. The underlying ledger is the source of truth; this map exists to keep the Strategist from having to re-derive judgment about which lines to lean on.

**Curator review pass (2026-08-20):** The prior curation pass produced this map and normalized the 255-record ledger; that work was audited and adopted rather than redone. One targeted gap-fill was executed against a load-bearing public question — the FY2026 CPE projection — upgrading the ledger's sourcing from a third-party aggregator alone to the DFW 2025 A/B bond Official Statement (records `evidence-curator::ev-cpe-fy26-os`, `evidence-curator::ev-cpe-fy26-board`). See §6 and §8 for the resulting shift. Every other gap in §8 was left open because either (a) the required record is confidential (MII thresholds, per-module fabrication-release dates, designed Terminal F FIS booth count) or (b) it needs a documents pull from DFW/AA that no public search will resolve. Downstream stages should route those to the operator or to the fact-checker.

---

## 1. The ten most load-bearing evidence points, ranked

Each item names the claim, the ledger record(s) that carry it, why it decides the Terminal F design brief, and where the sourcing is soft.

### 1. Terminal F scope moved from $1.6B/15 gates to $4B/31 gates in May 2025, with the U&L extended to 2043

- **Anchor records:** `infrastructure-economist::ev-9df5b63ec5a6`, `airline-commercial-strategist::ev-d7a668bca9ed`, `contrarian::ev-*`, and the joint DFW/AA press release cited by ten agents.
- **Why it decides the brief:** This is the frame of the entire run. The decision window is set by the timeline (Phase 1 in 2027, program complete 2030) and the lease runway (2043). Everything else in the map serves this fact.
- **Weakness:** The scope split by function (widebody gate count, FIS floor plate, lounge SF) is not disclosed in the joint press release. Every downstream cost-per-function inference is bracketed by that unknown.

### 2. American's revealed premium posture at DFW is tiered geographically, and Terminal F is not the top tier

- **Anchor records:** `airline-commercial-strategist::ev-d063ac6892ae`, `contrarian::ev-e0e801801c25`, `contrarian::ev-43f712ba50d6`, plus records 92, 107, 136, 159, 191, 217, 232, 241, 242, 254 (11 corroborating records across 8 agents).
- **What the record says:** 37,000 sf Admirals Club in Terminal C (AA's largest ever); Flagship Check-In in Terminal D near D30; a Provisions by Admirals Club grab-and-go in Terminal F.
- **Why it decides the brief:** This is the tenant's own signal about Terminal F's role in the premium hierarchy. It is the single strongest counterweight to the run-prompt thesis that Terminal F must absorb a premium repositioning; it is also the strongest argument for buying the shell (structural, MEP, curtainwall) that lets American change its mind by 2032 without a retrofit.
- **Weakness:** Whether the Provisions designation is a settled U&L obligation or a placeholder is unknown (context §9). No agent found a document that answers the question. The airport should insist on knowing before the modules affecting a Flagship-conversion envelope are locked.

### 3. Two-thirds of American's DFW customers connect, but the connecting-share number is contested

- **Anchor records:** `airline-commercial-strategist::ev-d3646f7a1477` (60% airport-level), context §4 (~two-thirds carrier-level asserted in run prompt), record 69 (Contrarian's reconciliation), record 152, record 253.
- **Why it decides the brief:** The connecting-vs-originating ratio drives every landside/airside size — curb, ticketing, TSA, retail, gate hold, walk distances. The 55–70% band the Quantitative Analyst uses swings O&D throughput by ~50% at peak.
- **Weakness:** The two-thirds figure has no primary AA document in the ledger. The 60% figure is aggregator-sourced (Deep Arrival citing DFW statistics). The Strategist should cite both and name the denominator whenever using either.

### 4. American restructured DFW from 9 to 13 daily banks starting April 2026, driving denser peak connectivity, not flatter

- **Anchor records:** `airline-commercial-strategist::ev-e4842e2ba510`, `contrarian::ev-21d97f31e691`, `operations-analyst::ev-c330a5acbfca`, `operations-analyst::ev-0f74c40d0b6e`, record 153.
- **Why it decides the brief:** The bank geometry sets the operational template Terminal F must serve. AA's own framing ("Doubling down on DFW... further strengthens its Flagship hub") is a signal to expect *more* connecting bank pressure, not less. The Airline Strategist estimates ~52 departures at 9am peak vs ~110 previously — meaning gate concurrency at Terminal F is set by bank contiguity, not by an old peak-hour surge.
- **Weakness:** The 50% missed-connection improvement number (record `airline-commercial-strategist::ev-c8d187d1b0ba`, and simple-flying trade press) is AA-reported two weeks post-launch. Operations Analyst evidence (record 70, `ev-6ad1dbdb3363`) shows DFW's Q2 2026 departure rate up only ~1% YoY and still second-worst among busy US airports, and AA lengthened scheduled block times +6 min on 145 markets — which mechanically inflates scheduled OTP. The Strategist should not overstate the rebank's proven benefit.

### 5. Delta's premium strategy crossed a threshold in Q4 2025 that American is chasing — and that changes the physical brief American faces

- **Anchor records:** `airline-commercial-strategist::ev-ed425c651135` (Q4 2025 premium $5.70B > main cabin $5.62B; FY2025 premium $22.1B), `airline-commercial-strategist::ev-9b47fcf1b976` (AA target: narrowbody premium seat share 25% → 40%; +50% lie-flat by end of decade), `airline-commercial-strategist::ev-afc6a59128bd` (787-9P / retrofitted 777-300ER configurations), record 190 (787-9 goes from 285 to 244 seats), record 219 (51 Flagship Suites on 787-9P), record 222 (Isom framing).
- **Why it decides the brief:** These are the numbers that turn "premium repositioning" from marketing into a physical demand signal — larger lounge seat pitch, wider premium check-in envelope, and a widebody gate mix that supports Flagship-capacity aircraft.
- **Weakness:** These are Delta's numbers and AA's targets. AA's balance sheet ($34.7B debt at Q1 2026, per record 60; 0.2% net margin in 2025 per record 249) is the constraint on execution. The Strategist must engage the Contrarian argument that AA's cost-discipline / high-leverage posture is inconsistent with a fully-funded premium platform in every terminal.

### 6. DFW's CPE trajectory is spending down its arbitrage during the ramp

- **Anchor records:** `infrastructure-economist::ev-6a303334efb7` (FY20-FY25 CPE), `airline-commercial-strategist::ev-9783f6e95c10` (DWU FY26 projection $16.99), `airline-commercial-strategist::ev-fcb92bc5fb30` (FY2025 proposed budget CPE $13.56), `evidence-curator::ev-cpe-fy26-os` (2025 A/B Official Statement — DFW FY25 actual $13.59, FY26 projected $16.99), `evidence-curator::ev-cpe-fy26-board` (Fort Worth Report Documenters, June 2025 board briefing — FY26 CPE $16.39 vs FY25 outlook $14.56), record 175 (PIT CPE ~doubled by 2011 after US Airways dehub), record 148 (Moody's Aa3+ US airport medians ~72 days cash on hand in 2024).
- **Why it decides the brief:** CPE is the airline veto lever inside the U&L. DFW came in at $13.59 actual for FY25 and is projected to $16.99 in FY26 in the 2025 A/B bond Official Statement — a 25% jump in one year, disclosed to bondholders. A June 2025 board briefing showed a slightly softer $16.39 projection against a $14.56 FY25 outlook; the delta is directional (Official Statements typically include debt-service coverage that mid-cycle board briefings may exclude), not contradictory. DFW is still $10–20 below JFK/EWR/LAX/ORD comps (record 25) and DWU peer-table 2025 places DFW 2nd lowest among top-10 large hubs at $13.59. But debt is scheduled to grow from $7.2B (2024) to $12.4B by FY29 (record `infrastructure-economist::ev-85be22c1fe28`) before the full $4B Terminal F stack is fully debt-financed. The Airline Strategist's professional judgment is that CPE breaching $20-22 changes carrier behavior at connecting hubs.
- **Weakness:** Post-scope-acceleration rating-agency remodeling has not been published (KBRA affirmed AA in Aug 2025 before the $4B scope was fully layered). The Official Statement figure was pulled via DWU's aggregation, not the underlying OS PDF itself — a fact-checker should retrieve the primary document if any recommendation quantitatively rests on the $16.99. The gap-fill closes the "third-party aggregator only" concern from the prior curation pass but does not close the primary-document verification step.

### 7. Modular construction saves ~30% in cost and time, and moves the reversibility deadline earlier

- **Anchor records:** `infrastructure-economist::ev-56a69208d46e`, `contrarian::ev-3cd6d9a7b69b`, `contrarian::ev-18d0e99795f7`, record 89 (Terminal C 9-gate modular pier, six pre-fitted megastructure modules), record 156 (Phase 1 six modules, largest 278×136 ft, 3,320 tons at ~¾-inch survey tolerance), record 192, record 227, record 228, record 243.
- **Why it decides the brief:** The modular method reshapes the reversibility map. Chief Engineer and Quantitative Analyst emphasize the operative deadline is **release-for-fabrication per module**, not concrete-cure — weeks-to-months earlier than the run-prompt phrasing suggests. Post-fabrication modular is *more* change-hostile than stick-built. The savings are not the design story; the accelerated design-lock is.
- **Weakness:** The 30% cost saving and 30-35% time saving are DFW-supplied and moved through trade press (Airport Improvement, Dallas Innovates). No independent audit against a stick-built counterfactual is in the record. "Largest modular airport project ever undertaken" is uncontested but also unaudited.

### 8. FIS geometry sizing and MARS-capable gate provisioning are the pour-locked decisions with the largest downstream cost of being wrong

- **Anchor records:** record 199 (CBP Airport Technical Design Standard: ~100 pax/hr per double booth, 50–75 ft primary queue), record 200 (2021 edition governing FIS design), record 234 (Dallas Resolution 25-1461 — CBP FIS reimbursement resolution), record 151 (CBP Reimbursable Services Program under Cross-Border Trade Enhancement Act 2016), record 80–81 (MARS at ORD T5), record 203 (MARS engineering), record 251 (MARS definition).
- **Why it decides the brief:** FIS floor plate, sterile corridor width, escalator core count, and exit-corridor geometry are pour-locked and directly cap 2043 international arrivals capacity. MARS-capable stands are the highest-value pour-locked flex — they let a Terminal F gate serve either a widebody premium routing or two narrowbody bank turns. AA is publicly moving international capacity from LHR to DFW (record `airline-commercial-strategist::ev-6f157cc0ecd1`: DFW +6% Q3 2026 while LHR -13%) and adding six new international routes (record `airline-commercial-strategist::ev-5b76a2fb6b0f`).
- **Weakness:** Terminal F's designed FIS booth count, sterile corridor width, and gate mix are not in the public record. Whether the CBP reimbursement resolution covers full Terminal F FIS or only equipment install is not detailed.

### 9. History repeats itself in this exact building type — and the design lesson is generic geometry, not carrier-specific geometry

- **Anchor records:** PIT Midfield $1B/US Airways dehub 2004/debt to 2019: records 41, 174–177; STL/TWA: records 45, 180–181; CVG/Delta: records 43–44, 178–179; CLE/United 2014: records 182–183; DTW/McNamara: record 184; ATL Concourse F: record 185; JFK T5/JetBlue: records 186–187; Aviation Historian brief (which frames all six).
- **Why it decides the brief:** Four of the six post-1978 purpose-built hub terminals failed after their carrier de-hubbed. The one that aged well — DTW McNamara — did so because it encoded a hub *form* (linear midfield with satellite concourses), not a Northwest form. This is a design lesson available at essentially zero incremental cost: prefer generic hub geometry inside carrier-specific finishes. This is the design signal that most cleanly cuts across the Contrarian and majority framings.
- **Weakness:** Sample size six. Historical rhyme, not law. PIT was a much smaller two-carrier situation without a genuine two-city O&D floor. DFW's 82.6% AA share sits on a real Dallas–Fort Worth economy that PIT never had.

### 10. DFW's Skylink node inside Terminal F is a pour-locked failure point during the morning connecting bank

- **Anchor records:** record 87 (Skylink 2-min headway, 9-min max transit), record 161 (Skylink out of service 22:00–06:00 for maintenance, ~15 min transit on single loop), record 162 (Jan 2023 winter storm: 1,100+ cancellations day 1, 600+ day 2 at DFW), COO brief §1.
- **Why it decides the brief:** The Terminal F Skylink station is included in Phase 1 (records 113, 229). The 6:15 AM connecting bank starts before Skylink's second loop resumes normal service. If the Skylink node lacks a second platform edge, redundant vertical circulation, and queuing capacity sized to a single-loop morning failure, the failure mode is the connecting bank collapsing — the operational metric the airport and airline both need to defend.
- **Weakness:** The current Terminal F Skylink station design (platform edge count, vertical circulation redundancy, queue depth) is not in the public record. COO's recommendation for redundancy is professional judgment, not a documented scope.

---

## 2. Bench: five more evidence points the Strategist should keep close

11. **A-CDM / operational intelligence benefits are audit-able at European scale, not yet at US scale.** Records 77–79, 117–121 (A-CDM taxi-out savings 0.25–3 min, 18–23% network delay reduction potential, 34% of ECAC departures from CDM airports), records 122–124 (Assaia YYZ 44% taxi-in reduction; Alaska/SEA 12% turn / 17% excess-hold reduction). Load-bearing because the cheap pour-preserved options (conduit, PoE++, mounts, cabling to tower sightlines) hedge the *deployment*, not the *benefit*. Vendor-published ROI numbers should be treated as directional.

12. **DFW debt trajectory $7.2B (2024) → $12.4B projected (FY29); DSCR 1.43–1.51× stable through pandemic; KBRA AA/Stable Aug 2025.** Records `infrastructure-economist::ev-85be22c1fe28`, `infrastructure-economist::ev-5ada50c866d0`, `infrastructure-economist::ev-032b2c3b3fb1`, record 148. Defines credit headroom for premium capex; frames the CPE debate.

13. **Heathrow T5 delivered on time and on budget under the T5 Agreement relational contract** (record `infrastructure-economist::ev-70c2c7cae06f`, record 209) — but opened with a 42,000-bag failure (records 132–133, 248). Both facts are load-bearing: T5's governance model is the closest parallel to Terminal F's single-airline structure, and its commissioning failure is the closest parallel to the operational risk in a rushed 2027 Phase 1 opening.

14. **Denver Great Hall terminated at ~$311M overrun, $184M paid to end P3, ~$2.1B completion path with Hensel Phelps; expected 2028.** Records 205–207. The most recent, most citable US airport-terminal governance failure. It anchors "under-scoping is the more expensive error" without requiring the Strategist to cite BER or DIA baggage.

15. **PFC has been $4.50 since 2001 (AIR-21 / Wendell H. Ford Act) and was unchanged in the 2024 FAA Reauthorization (PL 118-63); airport-side construction costs have roughly tripled since 2001.** Records 143, 188, 189. Explains why federal money is not the Terminal F funding story and why bond issuance + rate covenants do the work — which is why the CPE / MII arithmetic in #6 is decisive.

---

## 3. Agreements across the swarm — themes the Strategist should carry forward

Nine or more agents converged on these frames. Preserving them is not a matter of counting votes; it is a matter of naming the areas where independent readings of the record produced the same answer.

- **Publish a written reversibility register — module by module — as a governance artifact.** Airport CEO, Chief Engineer, Rams, Operations Analyst, Quantitative Analyst, Technology Scout, Infrastructure Economist, and Virtual Chris all land here. Eight of twelve. Contrarian does not disagree; he sharpens it into "buy specific options with signed AA cost-recovery."
- **Preserve a Flagship-convertible lounge shell without building the Flagship lounge American hasn't asked for.** Airline Strategist, Airport CEO, Airport COO, Chief Engineer, Rams, Virtual Chris, Quantitative Analyst all recommend the shell (25,000–40,000 sf structural allowance, MEP risers, curtainwall breaks). Contrarian is the disciplining dissent — see §4.
- **MARS-capable stands at a defined minority of positions.** Chief Engineer, Operations Analyst, Rams, Airline Strategist, COO. Cheap to preserve at fabrication; unavailable after.
- **FIS geometry is pour-locked and load-bearing on 2043 international growth.** Airline Strategist, Chief Engineer, Operations Analyst, CEO, Virtual Chris, Rams. Six agents.
- **AA's Provisions posture is a live signal, not settled fact, and must be tested against U&L language.** All twelve agents cite the Provisions posture; the read on what it means is what divides them.
- **Modular is a tolerance regime, not a permission slip.** Chief Engineer, Operations Analyst, Quantitative Analyst, Contrarian, Rams, COO, Aviation Historian. Seven agents. "Modular = flexible" is marketing.
- **Under-scoping is the more expensive error than over-scoping (2–4× retrofit premium, professional judgment).** CEO, Infrastructure Economist (IAD Concourse D → $3.75B AeroTrain extension; DIA >$100M in terminal design changes), Chief Engineer, Quantitative Analyst, Operations Analyst, Aviation Historian, Virtual Chris. Seven agents.
- **82.6% AA share + MII architecture = single-carrier veto in practice.** Airline Strategist, CEO, COO, Quantitative Analyst, Aviation Historian, Contrarian. Six agents. Any scope change inside Terminal F needs AA consent; MII trigger thresholds are confidential.
- **The Skylink node is under-appreciated.** COO, Rams, Operations Analyst, Virtual Chris, CEO. Five agents.
- **Terminal C and Terminal A modular renovations concurrent with Terminal F create craft-labor, fabrication-yard, and airside-window competition.** Chief Engineer, records 89–90, 116, 244. Rarely surfaced but decisive for schedule risk.

---

## 4. Contradictions and tensions the Strategist must preserve

These are the honest disagreements. A clean synthesis that erases them is a bad synthesis. Each is named so the Strategist can engage rather than paper over.

**Tension A — How aggressively to design against the Provisions signal.**
Contrarian: design honestly to the announced Provisions; refuse everything else except two or three specific low-cost options with signed AA cost-recovery. Airline Strategist, CEO, COO, Chief Engineer, Rams, Virtual Chris, Quantitative Analyst: preserve the Flagship-convertible shell. This is the single sharpest disagreement in the swarm. The Contrarian's option-premium discipline — "options accumulate into a shopping list no future budget funds" — is a real constraint the majority frame needs to survive.

**Tension B — Airport-level 60% or carrier-level ~66% connecting share?**
Airline Strategist accepts either ("within 5 points, design implications are consistent"). Quantitative Analyst treats the range as an active sensitivity that swings O&D count by ~50%. Contrarian argues the direction of travel is *more* connecting because of the 13-bank restructure. Aviation Historian implicitly warns that A321XLR-scale ultra-long narrowbody flying could later erode connecting share. Not a solved question.

**Tension C — Is the modular method a schedule/cost tool or a flexibility tool?**
Operations Analyst says modular arbitrage collapses the flex premium — spend it. Chief Engineer and Quantitative Analyst say post-fabrication modular is *more* change-hostile than stick-built. Contrarian says 30% savings are a repetition dividend killed by bespoke premium modules. All three positions are compatible in principle but produce different recommendations about how far to push per-module variation for premium features.

**Tension D — Does the 13-bank restructure flatten the profile (COO's read) or thicken the peak (Operations Analyst's read)?**
COO reads AA's messaging as a flatter, mid-day-loaded operation. Operations Analyst Q2 2026 data (record 70, `ev-6ad1dbdb3363`) show departure rate up only ~1% and lengthened block times inflating scheduled OTP. Airline Strategist notes bank contiguity amplifies peak simultaneity. Terminal F sizing depends on which is correct.

**Tension E — What is the operative reversibility deadline?**
CEO, Rams, and the run-prompt language say concrete-cure. Chief Engineer says factory design-lock — for some modules, already passed. Quantitative Analyst says release-for-fabrication per module, weeks-to-months earlier. This is a factual disagreement about the deadline that changes the urgency of every recommendation. **The Strategist should name the release-for-fabrication reality and stop using the "before the concrete cures" phrasing as though it captured the operative deadline.**

**Tension F — CUPPS/common-use readiness in an exclusive-use terminal.**
COO recommends CUPPS-capable gate hardware as IROPS insurance. Airline Strategist frames it as a contractual question needing pre-approved rate treatment or exclusive-use envelope carve-outs. Contrarian's option-premium logic cuts implicitly against it. Live tension between operator instinct and use-and-lease reality.

**Tension G — Is Terminal F a connecting-heavy building with premium options, or something else?**
Airline Strategist: connecting-heavy with preserved options. Rams: honest connecting building; don't pretend. Contrarian: widebody feeder and bank pressure valve. Virtual Chris: Arrivals premium, not Departures premium — a portfolio role AA doesn't yet cover. Multiple framings the Strategist may need to hold simultaneously.

---

## 5. The strongest evidence against the thesis

Synthesized from the Contrarian brief and the counter-evidence buried across five other briefs. This is the case the Strategist must engage.

American — the party with the most information about its own 2043 network — has publicly designated Terminal F's flagship-adjacent offering as Provisions by Admirals Club, placed its largest-ever 37,000 sf Admirals Club in Terminal C, and put Flagship Check-In in Terminal D. The airport is being asked to override the tenant's own signal with premium bones AA did not request. American is simultaneously *expanding* the connecting bank from 9 to 13 (record `airline-commercial-strategist::ev-e4842e2ba510`) — denser peak throughput, tighter minimum connect times, more simultaneous gate demand — which is the opposite physical implication of a premium-shift design brief. The acknowledged premium leader, Delta, has delayed a Delta One Lounge at its own ATL mega-hub to 2028 (record `contrarian::ev-bbfb17e8f0b1`) because the economics at connecting hubs are unsettled; designing Terminal F today around a premium anchor for the industry's *follower* asks the airport to bet on an answer the leader has not published.

AA's premium history includes hard retrenchment inside the last five years — every Flagship Lounge except JFK closed in March 2020 for 18 months (record `contrarian::ev-02c3980fc7b3`). AA's balance sheet still constrains the pivot (Q1 2026 total debt $34.7B, record 60; 0.2% net margin in 2025, record 249). Isom has publicly framed premium as the vehicle to close a $3B profit gap to United and $5B to Delta (record 61, record 222) — gaps that have persisted a decade. Modular's 30% saving is a repetition dividend, not an infrastructure dividend; every bespoke MEP tree or double-height structural allowance off-standard modules do not clear the factory at repeat-part cost. The industry finance model puts premium features on the *carrier's* side of the line (Delta One JFK T4 is a 40,000 sf carrier-funded fit-out on Port Authority base building, record `contrarian::ev-c90731082056`). DFW paying now for AA-branded premium space AA has not asked for inverts the customary allocation of premium risk. AMR/AA §365 real property lease record (record `contrarian::ev-80e5b480748b`: 554 assumed / 12 rejected in 2013) makes lease-rejection legally cheap and renegotiation leverage high. Every preserved option carries an option premium; options accumulate into shopping lists no future budget funds.

The Contrarian's concession — buy two or three specific low-cost options on two or three named gate positions, contingent on a signed AA cost-recovery MOU, refuse everything else — is a materially smaller recommendation than the run prompt implies. The Strategist must genuinely engage this version, not dismiss it.

---

## 6. Non-obvious insights

Things that would surprise a sophisticated executive who has already read the DFW press releases:

- **The operative reversibility deadline is release-for-fabrication per module — weeks to months earlier than concrete-cure.** (Chief Engineer, Quantitative Analyst.) The run-prompt phrasing is technically wrong for a modular build; some module design-lock dates have already passed. This alone reframes the urgency.
- **Post-fabrication modular is more change-hostile than stick-built.** A 5% late change on a conventional site costs ~5%; on a modular fabrication line it commonly consumes 15–25% of the change budget because it triggers resequencing across pods. "Modular = flexible" is marketing.
- **Skylink is quietly becoming AA's premium spine at DFW.** The Terminal C 37,000 sf Admirals Club sits near the Skylink station; Terminal F includes a centralized Skylink station in Phase 1; together they begin a distribution spine. Reframing Terminal F premium as *Arrivals* rather than Departures (Virtual Chris) resolves the competitive conflict with Terminal C and slots F into a portfolio role AA does not have covered.
- **The one terminal that survived a strategy shift did so by encoding *generic* hub geometry, not carrier-specific geometry.** DTW McNamara absorbed the Delta/NWA merger without material retrofit because it was a hub form, not a Northwest form (Aviation Historian; record 184).
- **DFW's airfield-side latent capacity is nearly booked; the terminal-side is the frontier.** Wake RECAT delivered 22 additional arrivals/hr at Memphis (record 74); MIT Lincoln Lab quantified +3.5 arrivals/hr on 35C worth $4.7M/year (record 75). The next 10–15% of DFW throughput comes from gate reuse, connection reliability, and checkpoint modernization — which all route through Terminal F decisions.
- **DFW's Q2 2026 departure rate is still second-worst among busy US airports** (record `operations-analyst::ev-6ad1dbdb3363`), and AA lengthened block times +6 min on 145 markets to help scheduled OTP. Forever Forward isn't yet delivering what the press release implied.
- **The MII architecture at 82% activity is a single-carrier veto in practice.** Anything AA does not want inside its exclusive-use terminal will not be built at DFW's discretion; anything the airport wants the right to add later must be either contractually pre-approved with agreed rate treatment or housed outside AA's exclusive-use envelope. This is a legal-architecture question, not a design question — and it has to be answered before the concrete cures.
- **The Fort Worth 4-of-11 board seats introduce political risk that doesn't materialize until the 2043 U&L renewal.** A council member who feels Terminal F was designed as a Dallas project will find leverage to say so in the run-up to renewal. Intentional Fort Worth-facing concessions are cheap insurance no other agent surfaced.
- **CBP Simplified Arrival and AA biometric boarding are already live at DFW** (records 127–128). Terminal F should be scoped to the mature version of the stack, not the pilot version.
- **Dallas Resolution 25-1461 (CBP FIS reimbursement, record 234) is the earliest public procedural signal that Terminal F international throughput is a live design conversation.** No other agent surfaces this.
- **AA Cargo has not been invited to the design table.** (Virtual Chris §1.7.) Ramp geometry that lets a 787-9P work a passenger turn and a cargo turn without repositioning is a quiet operating-margin play.
- **The lifecycle O&M bill (BHS 15-year cycle at ~10% purchase cost/year; HVAC 15–20 years; apron PCI-driven rehab 10–15 years) is a nine-figure deferred-maintenance liability if Terminal F is capitalized at $4B and O&M is underfunded even 15%.** (Chief Engineer §2.5; records 201, 202.)

---

## 7. Airport-specific constraints that bind the Terminal F design decision

- **Use-and-Lease architecture.** Residual-hybrid, base term Oct 1, 2023 – Sep 30, 2033, April 2025 offer letter option through Sep 30, 2043; extension amends FY2034–2043 revenue sharing to eliminate the Upper Threshold and split net revenue 45/55 DFW/airlines (record `airline-commercial-strategist::ev-854a1201ffed`, record 146). AA sole occupant of Terminal F; AA consent required for scope changes.
- **MII (majority-in-interest).** Requires majority-by-number and majority-by-activity of signatories to consent to major capital additions. At 82% activity, AA has effective single-carrier veto. Trigger thresholds confidential.
- **FIS / CBP.** CBP Airport Technical Design Standard: ~100 pax/hr per double booth, 50–75 ft primary queue depth (records 199–200). CBP Reimbursable Services Program (record 151). Dallas Resolution 25-1461 approved CBP reimbursement for FIS equipment (record 234).
- **TSA.** DHS S&T target 300 pax/hr/lane; live CT lanes at ~200 avg, 330 peak (records 84–85). Room dimensions pour-locked; casework swappable.
- **Structural pours and MEP shafts.** Column grid, floor-to-floor height inside module, primary baggage tunnel alignment/depth, apron column-and-jetway grid (Code C vs E vs MARS), hydrant fuel loop, primary electrical service, standby generator sizing, 400 Hz and PCA at stand — all pour-locked. Vertical MEP risers and grease-waste rough-ins to potential lounge and premium F&B locations — cheap to preserve at factory, punitive to retrofit.
- **Skylink node.** Overnight single-loop 22:00–06:00, ~15 min transit (record 161); Terminal F node must survive a 6:15 AM rail failure during morning arrival wave.
- **Board governance.** 12 members, 11 voting (7 Dallas, 4 Fort Worth), plus rotating non-voting neighbor seat (record 145, 236). Board approves capital changes; city councils approve annual budget and bond sales.
- **CEO tenure.** Chris McLaughlin appointed by unanimous board vote April 2025, assumed role May 19 2025 (record 144). Operations background.
- **Debt authorization envelope.** 70th Supplemental Bond Ordinance authorizes up to $3.0B in new debt March 2025–Feb 2026 (records 110, `airline-commercial-strategist::ev-83ce3618d87b`). Total CIP $11.3B through FY30 (records 111, 218, 252). Outstanding debt projected $7.2B → $12.4B by FY29 (`infrastructure-economist::ev-85be22c1fe28`).
- **PFC ceiling.** $4.50 unchanged since 2001; 2024 FAA Reauthorization (PL 118-63) left cap unchanged (records 143, 188). Federal grants are not the Terminal F funding story.
- **Concurrent construction competition.** Terminal C 9-gate modular pier delivered June 2026 (records 89, 90); Terminal C targeted 32 gates across >1 million sf; Terminal A renewal using same modular method (records 116, 138, 244) — competing for craft labor, fabrication yards, crane/SPMT windows, and airside impact windows.
- **NEPA.** Class-of-action status for the expanded 31-gate/$4B scope not confirmed in the record (context §8).

---

## 8. Gap list

Facts the swarm needed but did not have. Each is a candidate for closure before the Strategist commits to a specific recommendation.

Quantitative denominators still open:
- Terminal F widebody vs. narrowbody gate mix, and preserved flex / MARS-capable positions. Named by every agent.
- Terminal F floor-plate square footage (total, and by function: lounge, retail, ticketing, FIS, baggage). Quant Analyst's arithmetic is bracketed on this.
- AA-controlled gate count at DFW today (Quant §2 bracketed 130–160).
- Per-module release-for-fabrication dates. The operative reversibility deadline.
- Terminal F BHS spine capacity (bags/hr), FIS booth count, sterile-corridor width as designed.
- Post-scope-acceleration rating-agency remodeling. **Partial gap-fill 2026-08-20:** DWU dashboard now cites the FY26 $16.99 CPE projection to the 2025 A/B bond Official Statement, and a June 2025 board briefing surfaced a $16.39 board-level FY26 projection. A fact-checker should pull the OS itself and any post-May-2025 rating-agency letters if a quantitative recommendation rests on either figure.
- Airport-level vs. carrier-level connecting share as filed by DFW and AA (primary sources).
- Terminal F architect of record and any published design-intent statement beyond the joint press release (Innovation Next+ JV named at record 158, 215 — designers are PGAL, Gensler, Muller2).

Confidential U&L terms:
- MII trigger thresholds for capital additions.
- Any Terminal-F-specific rate treatment carve-outs.
- Whether the 2025 U&L amendment obligates AA to a Flagship-tier lounge at Terminal F at any point before 2043. Determines whether the reversibility discussion is design or contract.

Regulatory / operating:
- CBP staffing model committed for Terminal F international arrivals.
- Design and permitting status of Terminal F FIS.
- NEPA class-of-action status for the expanded scope.
- Cybersecurity posture segregating third-party check-in vendor from AODB (Tech Scout notes 2025 BER failure mode, record 135).
- Whether Terminal F module template already includes Assaia-ready gate camera mounts and PoE++ budget.

Curator note (original pass): I did not conduct targeted external gap fills in this pass. The remaining budget is small relative to the value of a full report to the operator, and the highest-leverage gaps (confidential U&L economics, per-module release-for-fabrication dates, designed FIS booth count) cannot be closed by web search — they require documents held by DFW and AA. The Strategist should treat these as open gaps and route them to the human checkpoint for operator disclosure or to the fact-checker to challenge any claim that depends on them.

Curator note (2026-08-20 review pass): One targeted gap-fill executed. FY26 CPE trajectory upgraded from DWU-projection sourcing to a DWU aggregation of the DFW 2025 A/B bond Official Statement plus a June 2025 board-briefing figure (Fort Worth Report Documenters). Both were added to the ledger as `evidence-curator::ev-cpe-fy26-os` and `evidence-curator::ev-cpe-fy26-board`. Two attempts to pull primary documents directly (Fort Worth Report article, City of Fort Worth-hosted DFW FY26 proposed budget PDF) returned HTTP 403 and should be retried by the fact-checker with an authenticated fetch path. No other gap on this list was closed — the remaining items require either confidential DFW/AA documents (MII thresholds, per-module release dates, FIS booth count, U&L Flagship-lounge obligation) or an authenticated primary-document pull that the curator budget cannot justify at this stage.

---

## 9. "Do not claim" list

Things the swarm reached for that the evidence does not actually support. The Strategist should not write these; the fact-checker will veto them.

- **Do not claim "modular = flexible."** Multiple agents refute; modular is a tolerance regime, and after fabrication release it is *more* change-hostile than stick-built.
- **Do not claim American has committed to a Flagship-tier lounge at Terminal F.** Every agent that touches this notes American's announced posture is a Provisions grab-and-go. Whether the U&L obligates AA to more before 2043 is a gap.
- **Do not claim Terminal F opens with two-thirds connecting share as a settled fact.** Airport-level 60% is secondary-aggregator sourced; carrier-level ~two-thirds is a run-prompt assertion without a primary AA document.
- **Do not claim the 13-bank restructure has demonstrably improved DFW OTP.** Q2 2026 data show ~1% departure-rate improvement; DFW still second-worst among busy US airports; AA lengthened block times +6 min on 145 markets. The 50% missed-connection improvement figure is AA-reported two weeks post-launch.
- **Do not claim the modular method saves ~30% independently.** The figure is DFW-supplied and moved through trade press; no independent audit against a stick-built counterfactual is in the record.
- **Do not claim MII thresholds are known.** Confidential. Every characterization of "AA veto" is professional judgment from the concentration percentage.
- **Do not claim vendor ROI figures as fact.** Assaia's YYZ 44% taxi-in reduction and Alaska/SEA 12% turn reduction are Assaia-published; HKIA digital-twin capex is non-public; any single-source ROI figure is a hypothesis.
- **Do not claim European A-CDM benefits transfer 1:1 to a US Surface-CDM deployment at DFW.** Ecosystem is not the same animal; no equivalent to EUROCONTROL as network manager.
- **Do not claim retrofit-vs-greenfield cost multipliers as sourced numbers.** CEO's "2–4× retrofit premium," Chief Engineer's Category A/B/C multipliers, Quant Analyst's 5–100× table, and Ops Analyst's "MEP oversizing 3–5% at construction, 40–60% as retrofit" are professional judgment or analyst construction, not from a single citable dataset. Present as directional.
- **Do not claim eVTOL vertiport arrives at Terminal F by any specific date.** Virtual Chris flags as hypothesis.
- **Do not claim AA's ~$3B/$5B profit-gap-closure via premium as an executed strategy.** It is Isom's public framing; the gap has persisted a decade; execution risk is unreduced.
- **Do not claim McKinsey / consultant-adjacent language.** Run prompt explicitly excludes ("no 'flexible, future-proof' unless you name the specific option and what it costs"). The Council tone rules ban buzzwords.
- **Do not claim the Terminal F Skylink station has a "second platform edge" as designed.** COO recommends it; no source confirms it.
- **Do not claim CUPPS-capable gate hardware is in the current Terminal F scope.** COO recommends it; no source confirms it.
- **Do not claim NEPA clearance for the expanded 31-gate / $4B scope is complete.** Airport context §8 flags as unconfirmed.
- **Do not claim the announced Terminal F amenity list constitutes the full program.** The joint press release names amenities but does not commit to a Flagship-tier lounge or a specific widebody gate count (record 169).

---

## 10. Candidate airport cases and quantitative exhibits

The Strategist can lean on these — each is anchored in the ledger and each closes off a specific argumentative move.

**Positive design lessons (build these into the argument):**
- **DTW McNamara (2002)** — generic hub geometry absorbed the Delta/NWA merger without material retrofit. Record 184; Aviation Historian brief. The single cleanest example of design outlasting carrier strategy.
- **LGA Terminal C (Delta, 2022–2024)** — $4B four-concourse program delivered two years ahead of schedule under a single-airline delivery model (record `infrastructure-economist::ev-3ad44367f57d`, record 211–212). The commissioning-and-delivery counter-example that says single-airline governance can work — if the airline treats it like Delta did.
- **Heathrow T5 (BAA/BA, 2008)** — delivered on time within £4.3B budget under the T5 Agreement relational contract (record `infrastructure-economist::ev-70c2c7cae06f`, record 209). Governance geometry parallel; buy the model, not just the outcome.

**Negative lessons (what Terminal F must avoid):**
- **PIT Midfield (1992) — ~$1B, US Airways dehub 2004, stranded debt to 2019** (records 41, 174–177). The dehub cautionary tale; also a warning that a landside replacement can be the recovery path (record 177 — $1.75B new landside opened 2025).
- **CVG (Delta, 22.7M pax 2005 → <6M pax 2013)** — records 43–44, 178–179. Speed of the collapse.
- **STL (TWA/AA, 500+ flights 2001 → 207 by 2003)** — records 45, 180–181. AA's own historical willingness to walk after a merger.
- **CLE (United, 2014)** — Concourse D empty since May 2014 (record 183). Concourse-level obsolescence.
- **Denver Great Hall (2018 termination, $184M paid to end P3, $2.1B completion path)** — records 205–207. Most recent US airport-terminal governance failure; useful because it does not require narrating BER or DIA baggage to make the point.
- **BER (2020 opening, €6.5B vs €2.83B budget, 9 years late, 2025 cyber attack via check-in vendor)** — records 3, 134, 135, 208. The system-integration and cyber-supply-chain lesson.
- **DIA original baggage** — $193M budget → $311M + $80M manual backup + $100M design changes; abandoned by United 2005 — records 6–8. Cited sparingly.
- **JFK T5 / JetBlue** — $875M in 2008, $200M T5i extension 2014, ~$100M premium refresh 2025–26 (records 186, 187). Terminal-scale carrier strategy shift is a real, recent, US phenomenon.

**Quantitative exhibits the swarm has already assembled** (the Strategist should not re-derive these):
- CPE peer comparison table for 2024: DFW $13.44 vs peer large hubs ATL $3.94, CLT $4.74, ORD $29.56, LAX $30.16, JFK $36.01, EWR $31.67, MIA $16.83, PHL $15.03, IAH $10.66, DTW $9.20, MSP $11.06, SEA $18.24, DEN $12.76 (record `airline-commercial-strategist::ev-37a6763aa555`).
- Cost-per-gate arithmetic: $106.7M (15 gates/$1.6B) → $129M (31 gates/$4B); incremental 16 gates ~$150M each (Quantitative Analyst brief).
- A Flagship-tier lounge in Terminal F displaces 1.6–4.0 gate positions = $207–600M in foregone gate value alone (Quantitative Analyst brief). This is the arithmetic that quantifies the "buy the shell, not the lounge" recommendation.
- Modular module dimensions and moves: six mega-modules placed, largest 278×136 ft at 3,320 tons, ~¾-inch survey tolerance, moved during a two-week overnight window in August 2026 (records 156, 192, 227, 243). This is the fact that anchors "release-for-fabrication is the real deadline."

---

## 11. Curator's note on the ledger

The ledger now sits at 257 records: 255 from the research swarm, preserved in place, plus 2 curator gap-fill records appended during the 2026-08-20 review pass (`evidence-curator::ev-cpe-fy26-os`, `evidence-curator::ev-cpe-fy26-board`). Records are valid JSONL and use the research-contract schema (fields include `evidence_id`, `agent_id`, `claim`, `source`, `source_url`, `source_type`, `date`, `data_vintage`, `airport`, `quote`, `caveat`, `units`, `denominator`, `confidence`, `is_primary`, `status`, `corroborated_by`, `contradicted_by`, `discovered_by`). Field names differ slightly from the field names the curator-prompt requests (`source_title`, `supporting_excerpt`, `source_date`, `airport_or_entity`) but carry the same content; the Strategist and downstream agents already consume the ledger in this shape and no upstream tool depends on rename. Rewriting 255 records to swap field names would have cost more than it added.

Duplication is heavy in three clusters that the Strategist should be aware of:
- **AA 82.6% passenger share / 82% departures** (records 30, 68, 93, 108, 170, 237, 253) — cite once, do not stack.
- **Provisions by Admirals Club as the Terminal F posture** (records 5, 38, 53, 55, 68, 92, 107, 136, 159, 191, 217, 232, 241, 254) — this is the most-corroborated single claim in the ledger. Twelve records across eight agents.
- **Modular ~30% cost/time savings** (records 16, 17, 51, 62, 63, 103, 138, 193, 228, 243) — treated as sourced but not audited.

Independent corroboration in these clusters is real (multiple agents found the primary source independently), so the duplicates should be read as strong signal, not as noise. The Strategist should cite one anchor record per cluster and treat the rest as corroboration.

No targeted external gap fill was performed in this curation pass; the remaining budget was reserved for downstream stages. The highest-leverage open questions (confidential U&L economics, per-module release-for-fabrication dates, designed FIS booth count) cannot be closed by web search — they require documents held by DFW and AA — and are named in §8 for the operator to route.
