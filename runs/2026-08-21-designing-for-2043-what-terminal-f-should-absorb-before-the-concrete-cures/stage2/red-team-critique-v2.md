# Red Team Critique v2 — Airport Executive Review

**Run:** `designing-for-2043-what-terminal-f-should-absorb-before-the-concrete-cures`
**Target:** `outputs/stage2/strategist-draft-v2.md` (Strategist v2, 2026-08-20)
**Reviewer:** airport-executive-reviewer
**Basis:** Strategist v2, evidence-prosecutor v1, airport-context.md, evidence-map.md, run manifest (12 selected agents; regulatory-political-analyst, airport-procurement-expert, director-of-public-safety, airport-emergency-management-director, virtual-pat excluded), run prompt.
**Chair simulated:** DFW-equivalent CEO reading a board-facing memorandum drafted for the Airport Board and the CEO's office, weeks before a bond pricing and a fabrication-release milestone.

Standing note. The draft is analytically strong. It handled the evidence prosecution honestly, engaged its own counter-case, and lands on a defensible design instruction — hub-generic bones plus a small number of priced, conditioned premium shells, with a written reversibility register as the governance artifact. What follows is the airport-executive layer the evidence pass did not test: whether this document can be assigned, funded, approved, built, and operated as written. Findings are ordered by damage to executability, not by page. Fifteen numbered findings. Each is tagged **FATAL** (blocks board approval as written), **CONDITION** (fixable in v3 without disturbing the thesis), or **NOTE** (raises the ceiling on quality).

---

## Part 1 — Findings

### E1. The register is the whole product, and the draft does not name who owns it, funds it, or is accountable for it inside DFW. **FATAL**

- **Location:** Executive summary #8; "Implications for the operator," Decision #1 ("Owner: CEO's office, with the Terminal F program team").
- **Charge:** The single most valuable governance artifact the report proposes is orphaned. "CEO's office" is not an executive owner in the sense a board memorandum requires; it is a mailroom. A recurring standing board item needs a named Vice President, a permanent staffing charge inside the Terminal F program, an integration point with the Chief Development Officer's monthly capital reports, and a written escalation path when the register and the design-build JV disagree.
- **What the evidence pass did not test:** Whether the DFW org chart contains a role — VP Terminal Development, VP Capital Programs, VP Airline Affairs — that can carry a standing register-review workload alongside the existing Innovation Next+ delivery obligations. Chris McLaughlin is a first-year CEO with an operations background (context §2); handing him personal ownership of a standing board artifact is a governance error, not a governance strength.
- **Why it matters:** A board that adopts an unmanned artifact watches it die inside two agenda cycles. "Register becomes a decoration on the strategy deck" is named in the draft as the failure mode of Decision #1; the draft's own remedy — "if three consecutive modules ship without the register being consulted, retire it" — accepts the failure it describes. That is not a stop condition. It is a resignation.
- **Remedy:** Name the accountable executive (VP-level, not CEO). State the staffing charge (an assigned program manager and a design-build JV liaison). Route the standing item through the Board's Operations, Safety, and Security Committee or Finance and Audit Committee — not directly to the full board on first appearance. Give the register a budget line, however small.

### E2. First-90-day action on Decision #1 is retrospective, not prospective. **FATAL**

- **Location:** Decision #1, first-90-day action: "the program team publishes the per-module release-for-fabrication dates and a first version of the register."
- **Charge:** The draft's own reframe is that release-for-fabrication is the operative deadline and that for the six August 2026 modules the deadline has already passed. A first-90-day action that begins with the program team publishing dates the CEO's office does not currently hold is documentation, not governance. If the next module locks in fewer than 90 days, the register is late by design.
- **What the evidence pass did not test:** The actual fabrication-release schedule inside the Innovation Next+ JV's factory. The map flags per-module release dates as a gap (§8) requiring documents held by DFW and the JV, not a web search. Without them, the register's cadence cannot be set.
- **Why it matters:** The draft's decision-making promise — "the register enforces the discipline that generic-geometry design is not a shopping list" — is conditioned on catching decisions before they lock. A retrospective register documents decisions that have already locked. That is a change log, not a reversibility register.
- **Remedy:** Split Decision #1 into two acts. Day-0-to-30: obtain the per-module release-for-fabrication schedule from the JV (contractually required disclosure, not a request). Day-30-to-90: name the next module inside the fabrication window, publish its pour-locked and still-open decision list, and hold the first board briefing against that specific module. Do not attempt a program-wide register in 90 days; deliver one module's worth of discipline and expand from there.

### E3. Cost-recovery MOU with American is treated as a signable instrument the draft does not describe. **FATAL**

- **Location:** Executive summary #8; Decision #2 ("Route the premium-adjacent options through American under signed cost-recovery language"); "Why the counter-case is insufficient."
- **Charge:** A signed AA cost-recovery MOU is the load-bearing mechanism that turns the register from a shopping list into "discipline." The draft describes the mechanism nowhere. Cost-recovery inside an exclusive-use terminal under a residual-hybrid Use and Lease Agreement is not a standing instrument; it is either (a) a side letter to the U&L amendment, which requires American's capital committee and DFW General Counsel, or (b) a tenant improvement recovery inside the rate base, which raises CPE and pulls MII into the room. Neither is a memo the Chief Development Officer countersigns with an SVP of Hub Operations in a fabrication cycle.
- **What the evidence pass did not test:** The actual contract vehicle. The evidence map's do-not-claim list is explicit: "Do not claim MII thresholds are known ... Every characterization of 'AA veto' is professional judgment from the concentration percentage." The draft's Decision #4 concedes that the run does not know the MII trigger thresholds — yet Decision #2 assumes those thresholds do not bind the option-preservation instrument. That is an inconsistency inside the recommendation set.
- **Why it matters:** If the cost-recovery mechanism is a side letter to the U&L, the register's tempo (per module, every 30–60 days) is inconsistent with U&L amendment cadence (annual or event-driven, negotiated). If it is a rate-base tenant-improvement recovery, every option added is a CPE event with an MII test that has to run before the pour, not after. The draft's discipline collapses if the instrument does not exist or exists on the wrong clock.
- **Remedy:** Before v3, either (a) name a real contract vehicle DFW and American can execute inside a fabrication cycle — a Terminal F Reversibility Side Letter with a schedule of pre-priced options, referenced in and permitted by the 2025 U&L amendment, executed once and refreshed annually — or (b) drop the "signed cost-recovery MOU" language and say plainly that the register's premium items are conditional on the next U&L amendment. Do not present a mechanism the run does not carry.

### E4. The procurement path for register-driven changes is absent from every recommendation. **FATAL**

- **Location:** Decisions #1, #2, and #5 (module template scope change under Innovation Next+ delivery contract).
- **Charge:** The airport-procurement-expert agent was excluded from this run (manifest confirmed). It shows. Every register item that becomes a scope change is a procurement action against a signed design-build contract with the Innovation Next+ JV (Archer Western–Turner–Phillips May–H.J. Russell, per footnote 1). The draft treats these as internal directives. In practice they are change orders on a federally-touched capital project with DBE goals, Buy America obligations (if AIP or discretionary FAA grants touch), and a bid-protest surface.
- **What the evidence pass did not test:** Whether the JV's contract type (fixed-price, GMP, IPD-adjacent) permits owner-directed template modifications at repeat-part cost, or whether every template change triggers a re-price cycle that erodes the 30% dividend the draft cites in the same sentence. Decision #5 ("finalize a written spec ... ship it through the factory once") assumes template modification is a costless owner right. That is a procurement claim the run cannot substantiate.
- **Why it matters:** A CEO reading Decision #5 asks the Chief Procurement Officer, "what is our change-order posture on Innovation Next+?" If the answer is anything other than "the contract accommodates the template as an owner-furnished baseline," the recommendation is unfunded.
- **Remedy:** Before v3, insert a Decision #0: "Confirm with the Chief Procurement Officer that the Innovation Next+ JV contract permits template-level owner-directed changes at repeat-part cost within the current change-order envelope, and identify the earliest module release for which template changes can still be absorbed under the base contract." Without this, Decision #5 is a design directive with no procurement path.

### E5. City-council approval, bond authorization envelope, and issuance window are unengaged. **CONDITION**

- **Location:** Executive summary #7; Decision #2 (Airport Board memorandum); Decision #5 (modular-manufacturer scope change).
- **Charge:** Context §2 establishes that Dallas and Fort Worth city councils must approve DFW's annual budget and bond sales. The 70th Supplemental Bond Ordinance authorizes up to $3.0B in new debt between March 1, 2025 and February 28, 2026 (evidence map §7). The draft treats board approval as sufficient and treats bond capacity as a background variable, not a scheduling constraint. It is not.
- **What the evidence pass did not test:** Whether register-driven option premiums (shells, MEP oversizing, MARS provisioning) fall inside the current bond authorization or require a new supplemental ordinance and two city-council approvals. The 2025 A/B bond series is priced; the next new-money authorization for Terminal F is the register's actual funding source and no recommendation names its window.
- **Why it matters:** A CEO who approves a preserved shell before the next supplemental ordinance is authorized has to carry the option premium on interim financing or defer it and lose the fabrication release. A board recommendation that ignores the bond calendar reads to the audit committee as incomplete.
- **Remedy:** Add a funding-source column to the register. State, for each option, whether it is funded from the current 70th Supplemental Bond Ordinance, PFC (unlikely — $4.50 cap unchanged, evidence map §2 bench), a future supplemental ordinance requiring city-council action by a named date, or American under cost-recovery. Route the bond-adjacent items through the Finance and Audit Committee before the full board.

### E6. FAA design-standard concurrence, NEPA class-of-action, and CBP FIS staffing MOU are absent as dependencies. **CONDITION**

- **Location:** "What generic geometry actually means" (invokes FAA AC 150/5300-13B and CBP Airport Technical Design Standard without treating them as approval paths); Decision #3 (FIS queue depth re-run).
- **Charge:** The draft cites the technical standards but treats them as design inputs, not as federal approval dependencies. AC 150/5300-13B concurrence for MARS-capable stands at Airplane Design Group V–VI positions requires modification-of-standard requests where geometry departs from the AC; NEPA class-of-action for the expanded 31-gate/$4B scope is flagged as unconfirmed in context §8; CBP staffing for a Terminal F FIS at the sized throughput requires an executed Reimbursable Services Program agreement or a CBP staffing memo, which is a two-year negotiation, not a design directive.
- **What the evidence pass did not test:** The current status of any of these federal dependencies. Dallas Resolution 25-1461 (evidence map §7) is the earliest procedural signal that CBP FIS reimbursement is a live conversation; the draft cites nothing about NEPA or FAA modification-of-standard status.
- **Why it matters:** Sizing the FIS to CBP standard is necessary but not sufficient. If CBP will not staff the sized hall, the shell is a moot preservation. If NEPA is not cleared for the expanded scope, several register items — apron-side MARS geometry, additional international gates — are exposed to a federal-side stop.
- **Remedy:** Add a dependency column to the register listing FAA (AC 150/5300-13B concurrence or MOS letter), NEPA (class-of-action status), CBP (RSP or MOU status), and TSA (checkpoint layout concurrence) for every item where federal approval binds. Route unresolved dependencies to Decision #4 (General Counsel) rather than leaving them implicit.

### E7. The Fort Worth board seats and the 2043 U&L renewal politics are entirely absent. **CONDITION**

- **Location:** No location. The Terminal F recommendation does not engage the split-city governance the evidence map flagged as an insight (§6).
- **Charge:** DFW's 11 voting board seats split 7 Dallas / 4 Fort Worth, with Fort Worth's council appointing the four (context §2). Evidence map §6 flagged this explicitly: "The Fort Worth 4-of-11 board seats introduce political risk that doesn't materialize until the 2043 U&L renewal. A council member who feels Terminal F was designed as a Dallas project will find leverage to say so in the run-up to renewal." American's headquarters are in Fort Worth. The draft is a board-facing memorandum that says nothing to the four seats whose leverage grows as the 2043 renewal approaches.
- **What the evidence pass did not test:** Whether any of the register items — Fort Worth-facing landside access, Fort Worth-based DBE participation, tenant improvement structures that visibly benefit Fort Worth firms — is available at low marginal cost and would materially reduce 2043 renewal risk.
- **Why it matters:** A board memorandum from the CEO's office that reads as a Dallas-side design instruction, addressed to a board where four seats can hold up a bond sale, is a political read the draft cannot afford to skip. This is not gratuitous politics; it is credit risk on the 2043 renewal that Fitch and Moody's methodology sheets will eventually price.
- **Remedy:** Add one sentence to the executive summary and one bullet to the register: intentional Fort Worth-facing considerations (landside access, DBE, cargo-side ramp geometry if a 787-9P dual-purpose stand is registered) as items whose political value exceeds their marginal cost. The evidence map already surfaced this; the draft dropped it.

### E8. Labor and concurrent-construction contention are unmodeled. **CONDITION**

- **Location:** Not addressed. Evidence map §7 flagged concurrent Terminal C and Terminal A modular renovations as competing for craft labor, fabrication yards, and airside windows.
- **Charge:** The draft treats the modular factory as an infinite-throughput resource. Terminal C's nine-gate pier opened June 2026 using the same method; Terminal A renewal is queued. Craft labor for MEP first-fit inside modules, SPMT operators and windows, crane-and-erection windows, and the Innovation Next+ JV's yard capacity are shared across three concurrent programs. Every template change registered against Terminal F competes for the same fabrication line.
- **What the evidence pass did not test:** Whether the fabrication line has resequencing capacity for the register's expected volume of option-driven changes, or whether adding conduit and PoE++ backbone to every module (Decision #5) extends the fabrication cycle beyond what Terminal C and Terminal A can absorb without their own schedule slip.
- **Why it matters:** A COO reading Decision #5 asks the program director: "Does this slow C or A?" If yes, the register's benefit at F is paid for by schedule slip elsewhere. That is a real trade the draft does not price.
- **Remedy:** Add to Decision #5 an explicit check with the JV: confirm the template modification is absorbable inside the current fabrication cadence for all three concurrent projects (C, A, F) without a schedule impact greater than a defined threshold. If not, phase the template rollout.

### E9. The 6:15 a.m. scenario is a design test but not an operating test — IROPS, staffing, and CUPPS are dropped. **CONDITION**

- **Location:** "The 6:15 a.m. sizing case"; Decision #3.
- **Charge:** The draft adopts the 6:15 a.m. Skylink-degraded morning as the formal sizing scenario for pour-locked geometry. Correct decision. But an operating scenario is more than geometry. What staffing model absorbs the surge — DFW's own Guest Experience staff, AA station personnel, TSA officers, CBP officers, ARFF and airport police? None appear. CUPPS-capable gate hardware (evidence map Tension F) is a COO recommendation the draft dropped — under a single-carrier disruption, F cannot bleed passengers to other terminals without common-use hardware or a manual reassignment protocol. Public safety is not engaged (director-of-public-safety and airport-emergency-management-director were excluded from this run; evidence map flagged the gap; the draft did not).
- **What the evidence pass did not test:** The IROPS behavior of Terminal F under a real ground stop with AA as sole occupant. The January 2023 winter event cited as the demand curve is a DFW-wide event; the draft loads it onto Terminal F geometry without loading it onto Terminal F staffing.
- **Why it matters:** A COO reading Decision #3 sees the sizing scenario and asks: "Did we run a tabletop with AA station operations, TSA, and CBP against this?" If the answer is no, the sizing is engineering-only and the operational commitment does not exist.
- **Remedy:** Add to Decision #3 an explicit tabletop exercise against the 6:15 scenario, participants named (AA DFW Hub Ops, TSA FSD, CBP Port Director, DFW COO, ARFF, airport police, Skylink operations). Add CUPPS-capable gate hardware to the register with the disposition explicit (COO recommends; Airline Strategist and Contrarian have a view; the draft picks one). Do not leave Tension F unresolved.

### E10. The affordability envelope has no CPE governance rule the register must live inside. **CONDITION**

- **Location:** Executive summary #7; "Why the counter-case is insufficient" (affordability paragraph).
- **Charge:** The draft acknowledges FY26 CPE at $16.99 (aggregator-sourced, primary-document verification pending), acknowledges debt trajectory to $12.4B by FY29 pre-expansion and higher post-expansion, and acknowledges the Airline Strategist's professional judgment that low-$20s CPE begins to change carrier behavior. It then omits the operational consequence: the register itself needs a CPE governance rule. What CPE trajectory must the aggregate register premiums live inside? What triggers a mandatory register value-engineering pass? What is the interaction between the register and the KBRA AA/Stable methodology's coverage and liquidity thresholds?
- **What the evidence pass did not test:** Whether a bounded CPE-trajectory rule (for example, "the aggregate register premium may not raise projected CPE above a defined ceiling in any FY through FY30") is achievable given the current forecast. The Airline Strategist can compute this from the debt-service schedule; the run did not commission it.
- **Why it matters:** A Finance and Audit Committee that adopts the register without a CPE governance rule is buying an unbounded option premium. The Contrarian's objection ("options accumulate into a shopping list no future budget funds") lives inside this omission.
- **Remedy:** Add to Decision #2 a governance rule: the aggregate register-driven option premium at each fabrication release, expressed as a projected CPE contribution, must sit inside a Finance and Audit Committee-set ceiling. Publish the ceiling. Route the CPE bridge to the Quantitative Analyst before v3 or in the fact-checker pass.

### E11. The MII architecture is treated as a Decision #4 question, but several register items assume its answer. **CONDITION**

- **Location:** Decision #4 (obtain the MII trigger thresholds); Decisions #1, #2, #5 (all of which propose actions inside American's exclusive-use envelope).
- **Charge:** The draft correctly routes the MII thresholds to General Counsel. But the register in Decision #1, the cost-recovery mechanism in Decision #2, and the template modifications in Decision #5 all assume DFW retains unilateral discretion inside the exclusive-use envelope. If MII trigger thresholds are low, the register becomes a set of items that require American's consent to preserve, which changes its character entirely. If MII trigger thresholds are high, the register is procedurally clean but the "cost-recovery MOU" mechanism is not the right instrument.
- **What the evidence pass did not test:** The sequencing. Decision #4's outcome must precede Decisions #1, #2, and #5, not run in parallel with them.
- **Why it matters:** Board memoranda that assume contract facts pending confirmation are the ones the General Counsel's office quietly redlines.
- **Remedy:** Reorder the Decisions. Decision #4 becomes Decision #1, on a compressed timeline (30 days, not 90). The register work follows the answer.

### E12. The "shell at pennies on the base dollar" claim carries no arithmetic. **CONDITION**

- **Location:** Executive summary #6; "What generic geometry actually means"; "The counter-case, honestly presented" (Contrarian objection); Decision #2.
- **Charge:** The draft repeatedly asserts that generic-geometry provisions and shells cost "pennies on the base dollar at fabrication and multiples in retrofit." The evidence map's do-not-claim list is explicit: retrofit-vs-greenfield cost multipliers are professional judgment, not sourced numbers. The draft respects this in the general form and then imports the informal version into the recommendation. A CFO reading "small option premium" and "pennies on the dollar" for a $4B program asks for the number, and the register has none.
- **What the evidence pass did not test:** The dollar cost, per module, of the register's proposed provisions (MEP riser oversizing, structural allowance for a lounge shell, curtain-wall breaks, PoE++ backbone, dense sensor conduit, MARS apron geometry, FIS floor-plate oversizing). The Quantitative Analyst brief carries a $207–600M figure for a Flagship-tier lounge displacing 1.6–4.0 gate positions (evidence map §10), which is a displacement cost, not a provision cost.
- **Why it matters:** Every recommendation the audit committee approves needs a number. "Small" is not a number. Publishing the register with prices was the draft's own Decision #1 language; it is asserted, not delivered.
- **Remedy:** Commission the Quantitative Analyst to publish, in v3 or in the fact-checker pass, a per-item cost range for the register's top ten items. Not audit-grade — order-of-magnitude with stated assumptions. The register cannot be published to the board without them.

### E13. Leading indicators are named as compliance items, not as decision-triggers. **NOTE**

- **Location:** Decisions #1–#5, "Success measure" fields.
- **Charge:** Every success measure in the Decisions is a process compliance measure ("every board vote on a module change order is preceded by a written finding against the register"), not a leading indicator that changes an executive decision. A leading indicator for the Terminal F decision brief is different: is the AA connecting share trending up or down inside the 60%–two-thirds band; is the 13-bank restructure's peak-flattening claim corroborated in the next two operating quarters; is AA's premium-share build-out on schedule (narrowbody 25% → 40%; lie-flat +50% by end of decade); is DFW CPE tracking above or below the Finance and Audit Committee's ceiling.
- **What the evidence pass did not test:** Whether the run's own leading indicators can be reported quarterly to the board against the register.
- **Why it matters:** A register that survives value engineering and board turnover does so because it re-tests its own assumptions on a schedule the board can see. Compliance measures do not do this work.
- **Remedy:** Add a "Leading indicators" section to the Implications, five or six items, each with a quarterly reporting owner. The COO's annual re-test of the peak-density reading (Decision #3) is the model; extend it.

### E14. Stop conditions are named for the register but not for the recommendations. **NOTE**

- **Location:** Decisions #1–#5, "Stop condition" fields.
- **Charge:** Each Decision has a stop condition for its own execution (register consulted three times; AA not countersigned after two cycles; template does not clear repeat-part cost). None has a stop condition for the recommendation itself. The draft names two 2035 conditions that would make the recommendations look wrong (A321XLR erosion of connecting share; AA physical Flagship build-out at F). Those are honest exposure statements. They are not stop conditions.
- **What the evidence pass did not test:** What signal, observable in FY27–FY30, would cause the CEO's office to unwind the register or retire a class of preserved options.
- **Why it matters:** A board wants to know when to stop as clearly as when to start. Without an explicit stop condition at the recommendation level, the register is a permanent artifact — which is exactly what the Contrarian warns against.
- **Remedy:** Add one paragraph: named signals (AA formal Flagship build-out at F on a published schedule; connecting share erosion below a defined band across two consecutive years; U&L renewal negotiations opened earlier than 2043) that trigger a register unwind, and the executive who is authorized to unwind on each signal.

### E15. The recommendation set is written to five chairs and does not address the board as a body. **NOTE**

- **Location:** "Implications for the operator" (opens with "each addressed to a specific chair").
- **Charge:** The draft addresses the CEO's office, the Chief Development Officer, the COO, the General Counsel, and the CIO. It does not address the Board as a body. A board-facing memorandum needs a "What we ask of the Board" paragraph naming (a) the specific action requested at the next meeting (adopt the register as a standing item; delegate approval of the Terminal F Reversibility Side Letter to the Finance and Audit Committee; note the CPE governance rule for the FY27 budget); (b) the specific action requested at the meeting after that; and (c) the reporting cadence the Board will see against the register.
- **What the evidence pass did not test:** Whether the recommendation set, as written, is executable by the CEO's office alone or whether board action is on any critical path.
- **Why it matters:** An executive reader reads for the board ask. The draft has one embedded in Decision #1 and one embedded in Decision #4, and does not consolidate them.
- **Remedy:** Add a short "Board actions requested" section — three items, dated to the next two board meetings, each with the committee route.

---

## Part 2 — Airport Decision Cards

Every recommendation the draft carries as a "Decision" is restated below in the format an airport executive needs. Where the draft is silent on a field, the field is marked **(not in draft)**. This is the layer v3 must supply if the report is to be board-ready.

### Card A — Publish the module-by-module reversibility register as a standing governance artifact (Decision #1)

- **Executive owner:** VP Terminal Development (or equivalent) — **not in draft** (draft names "CEO's office," which is not an executive owner).
- **Decision and approval route:** Adoption of standing register as recurring item on Operations, Safety, and Security Committee agenda, escalating to full Board on material changes — **not in draft** (draft routes directly to full Board with no committee stage).
- **First 90-day action:** Day-0-to-30: obtain per-module release-for-fabrication schedule from Innovation Next+ JV under contract disclosure. Day-30-to-90: publish register for the next module in the fabrication window. **Draft's first-90-day action is retrospective (see E2).**
- **Cost order of magnitude:** **Not in draft.** Range: register staffing $250K–$500K annual loaded cost; register-driven option premiums TBD (see E12).
- **Funding source:** **Not in draft.** Staffing from operating budget; option premiums from current 70th Supplemental Bond Ordinance where inside envelope, otherwise from next supplemental (requires Dallas + Fort Worth city-council approval).
- **Airline dependency:** Signed Terminal F Reversibility Side Letter with American, or clarity that register items are conditional on the next U&L amendment (see E3, E11).
- **Board dependency:** Board committee assignment; standing item adoption.
- **Federal dependency:** None at register level; per-item federal dependencies (FAA, NEPA, CBP, TSA) surfaced per option (see E6).
- **Procurement dependency:** Innovation Next+ JV contract accommodates owner-directed template changes at repeat-part cost (see E4).
- **Labor dependency:** Fabrication capacity absorbs template changes without slipping Terminal C or Terminal A (see E8).
- **Operational dependency:** Program team staffing bandwidth.
- **Leading indicator:** Percentage of fabrication releases preceded by a written register finding; count of preserved options exercised vs. retired; CPE contribution of aggregate preserved options against the Finance and Audit Committee ceiling.
- **Failure mode:** Register accumulates preserved options without American cost recovery; option premium falls to DFW rate base.
- **Stop condition:** Register formally retired if AA formal Flagship build-out at F is announced on a schedule the airport can see, or connecting-share erodes below a defined band across two consecutive years, or U&L renewal opens earlier than 2043. **Not in draft (see E14).**
- **What evidence would change the recommendation:** Publication of MII trigger thresholds; primary-document CPE projection through FY30; American's written statement on the Flagship-at-F question.

### Card B — Route the premium-adjacent options through American under signed cost-recovery language (Decision #2)

- **Executive owner:** Chief Development Officer, with General Counsel — draft names CDO alone.
- **Decision and approval route:** Board memorandum + American internal capital committee — draft names this but does not name the contract vehicle (see E3).
- **First 90-day action:** Draft a Terminal F Reversibility Side Letter with schedule of pre-priced options, executed once and refreshed annually against U&L amendment.
- **Cost order of magnitude:** **Not in draft** (see E12).
- **Funding source:** American cost recovery for premium shells; DFW residual for generic geometry.
- **Airline dependency:** American capital committee sign-off; SVP Hub Operations plus American CFO office, not SVP Hub Ops alone.
- **Board dependency:** Delegation of side-letter execution to Finance and Audit Committee.
- **Federal dependency:** None at instrument level.
- **Procurement dependency:** Innovation Next+ JV contract accommodates option execution against a signed schedule.
- **Labor dependency:** As Card A.
- **Operational dependency:** General Counsel bandwidth on U&L instruments concurrent with 2025 amendment implementation.
- **Leading indicator:** Number of premium-conditioned shells with countersigned option memos at each fabrication release; ratio of options exercised to preserved.
- **Failure mode:** As draft.
- **Stop condition:** Draft's "drop from register after two fabrication cycles without AA countersign" is acceptable; add a lifecycle-cost trigger (see E10).
- **What evidence would change the recommendation:** American's written statement on the Flagship-at-F question; publication of MII trigger thresholds; a change in American's premium-share build-out schedule.

### Card C — Adopt the 6:15 a.m. degraded-morning stress case (Decision #3)

- **Executive owner:** COO, with Chief Engineer and AA DFW Hub Ops.
- **Decision and approval route:** Internal program directive; concurrent tabletop with TSA FSD, CBP Port Director, ARFF, airport police — **tabletop not in draft** (see E9).
- **First 90-day action:** As draft, plus a tabletop against the January 2023 demand curve with named federal partners.
- **Cost order of magnitude:** Sizing changes bounded by geometry decisions already inside the register; incremental cost per pour-locked change stated as a range.
- **Funding source:** Inside base Terminal F scope.
- **Airline dependency:** AA participation in the tabletop.
- **Board dependency:** None at directive level; results reported to Operations, Safety, and Security Committee.
- **Federal dependency:** TSA and CBP participation and buy-in on staffing implications of sized geometry.
- **Procurement dependency:** None at scenario level; downstream register items carry procurement.
- **Labor dependency:** DFW Guest Experience, ARFF, airport police staffing under the surge condition.
- **Operational dependency:** Annual re-test as draft describes.
- **Leading indicator:** Quarterly reporting of AA rebank peak profile against the 13-bank flatness vs. density question (Tension D); Skylink single-loop transit performance during 22:00–06:00.
- **Failure mode:** As draft, plus: tabletop reveals CBP or TSA staffing model cannot absorb the sized throughput and the sizing is engineering-only.
- **Stop condition:** As draft.
- **What evidence would change the recommendation:** Two consecutive full-year operating cycles corroborating the COO's flatter-profile reading of the rebank; A321XLR-scale flying erodes connecting share materially.

### Card D — Close the two contract questions the design cannot answer (Decision #4)

- **Executive owner:** General Counsel, with airline-affairs office. **This card should be executed first, on a 30-day timeline, not 90 (see E11).**
- **Decision and approval route:** Internal disclosure to Finance and Audit Committee.
- **First 30-day action:** Obtain from American a written statement of (a) whether the current U&L amendment obligates a Flagship-tier lounge at Terminal F at any point before 2043 and (b) the MII trigger thresholds for capital additions inside the exclusive-use envelope.
- **Cost order of magnitude:** Legal and airline-affairs staff time; nominal.
- **Funding source:** Operating budget.
- **Airline dependency:** American General Counsel willingness to state.
- **Board dependency:** Disclosure to Finance and Audit Committee before the next module's release.
- **Federal dependency:** None.
- **Procurement dependency:** None.
- **Labor dependency:** None.
- **Operational dependency:** None.
- **Leading indicator:** Disclosure received / not received before named fabrication-release milestones.
- **Failure mode:** Register makes recommendations that assume contract facts not in evidence — the draft says this exactly.
- **Stop condition:** If American declines to state, escalate to airline-affairs at CEO-to-CEO level; if still unstated, treat the register's premium items as design questions bounded by conservative MII assumptions.
- **What evidence would change the recommendation:** The answers themselves.

### Card E — Fix the sensor, cabling, and data-plane schedule at the module template (Decision #5)

- **Executive owner:** CIO with Chief Engineer.
- **Decision and approval route:** Innovation Next+ JV scope-change instrument (not "modular-manufacturer scope change" — this is a JV, not a single manufacturer).
- **First 90-day action:** Confirm with Chief Procurement Officer that the JV contract permits template-level owner-directed changes at repeat-part cost (see E4); then finalize the written spec.
- **Cost order of magnitude:** **Not in draft.** Conduit and pull-boxes on 20-foot centers; fiber and PoE++ backbone at 3–5× current sensor count — priceable, not priced.
- **Funding source:** Terminal F base scope if inside change-order envelope; supplemental if not.
- **Airline dependency:** AA IT participation in factory witness testing against a live A-CDM, biometric, and CBP stack.
- **Board dependency:** None at template level; reported to Operations, Safety, and Security Committee.
- **Federal dependency:** CBP biometric stack integration (already live per evidence map §6); TSA CT lane integration.
- **Procurement dependency:** As E4.
- **Labor dependency:** Fabrication schedule absorbs template modification without slipping C or A (see E8).
- **Operational dependency:** DFW IT integration bandwidth.
- **Leading indicator:** Factory witness test pass/fail against integrated stack; per-gate variance from template.
- **Failure mode:** As draft.
- **Stop condition:** As draft.
- **What evidence would change the recommendation:** Factory witness test reveals template will not clear repeat-part cost.

---

## Part 3 — What the evidence pass did not test

The evidence-prosecutor v1 did honest work on evidence integrity, source quality, and internal consistency. It did not test the following, which are the airport-executive layer this critique focuses on:

1. **Governance mechanics.** Whether the register has a real owner, a real staffing charge, a real committee route, and a real cadence. (E1, E15.)
2. **Contract instruments.** Whether the "signed cost-recovery MOU" exists as an executable instrument inside the U&L architecture. (E3, E11.)
3. **Procurement path.** Whether register-driven template changes are permissible owner actions inside the Innovation Next+ JV contract. (E4.)
4. **Bond and city-council calendar.** Whether register-driven option premiums fall inside the current 70th Supplemental Bond Ordinance authorization window or require a new supplemental with two city-council approvals. (E5.)
5. **Federal partner dependencies.** FAA modification-of-standard, NEPA class-of-action, CBP RSP/MOU, TSA concurrence — as decision paths, not as design inputs. (E6.)
6. **Split-city board politics and 2043 U&L renewal.** Whether the recommendation set addresses Fort Worth's four votes and reduces 2043 renewal risk. (E7.)
7. **Concurrent construction and labor contention.** Whether F's register-driven template changes can be executed without slipping C or A. (E8.)
8. **IROPS and public-safety operating layer.** Whether the 6:15 scenario has been tabletopped with staffing, not just sized with geometry. (E9.)
9. **CPE governance rule.** What ceiling the aggregate register premium must live inside. (E10.)
10. **Register arithmetic.** Per-item cost, per-item CPE contribution. (E12.)
11. **Leading indicators.** Board-reportable metrics that trigger decisions, not compliance. (E13.)
12. **Stop conditions at the recommendation level.** Not just at the tool level. (E14.)

---

## Part 4 — Which findings are fatal and which are conditions

- **FATAL (4):** E1 (register owner), E2 (retrospective first-90-day action), E3 (unnamed contract vehicle for cost-recovery), E4 (procurement path).
- **CONDITION (7):** E5 (bond/city-council calendar), E6 (federal dependencies), E7 (Fort Worth politics), E8 (labor and concurrent construction), E9 (IROPS tabletop and CUPPS resolution), E10 (CPE governance rule), E11 (MII sequencing), E12 (register arithmetic).
- **NOTE (3):** E13 (leading indicators), E14 (recommendation-level stop conditions), E15 (board actions requested paragraph).

The four fatal findings are the ones that render the recommendation unassignable, unfundable, unapprovable through the correct instrument, or unexecutable inside the current construction contract. Each is repairable in v3 without disturbing the thesis. None require the argument to move; each requires the recommendation to acquire an airport-executive layer the evidence pass did not test for.

---

## Verdict

**READY WITH NAMED CONDITIONS.**

The argument is sound. The evidence pass has been honored. The recommendation set — hub-generic bones, a small number of priced and conditioned premium shells, a written reversibility register, the 6:15 sizing case as a formal scenario, template-level instrumentation, and two contract questions routed to General Counsel — is the recommendation that survives its own strongest counter-case.

It is not yet the recommendation an airport board can adopt. Four fatal findings must be closed before v3 goes to the board: the register needs a named executive owner (E1); the first-90-day action must be prospective, not retrospective (E2); the cost-recovery instrument must be named as a real contract vehicle (E3); and the procurement path for template changes must be confirmed with the Chief Procurement Officer against the Innovation Next+ JV contract (E4).

Close those four and the seven implementation conditions in v3, and the report is board-ready. Publish it as written, and the CEO's office will spend the first meeting explaining what "CEO's office, with the Terminal F program team" means and why a document titled "the register is the deadline" arrived without dates the register can be tied to.

The concrete is a decoy. The register is the deadline. The airport-executive layer is the recommendation.
