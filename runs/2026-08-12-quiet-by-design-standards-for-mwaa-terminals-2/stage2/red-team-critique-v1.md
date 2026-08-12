# Red Team Critique v1 — Evidence Prosecution of Strategist Draft v1

**Run:** `quiet-by-design-standards-for-mwaa-terminals-2`
**Reviewer:** evidence-prosecutor
**Target:** `outputs/stage2/strategist-draft-v1.md` ("The Loud Terminal Is the Unintelligible One")
**Basis:** `outputs/run-manifest.json` (14-agent roster), `outputs/stage1/evidence-map.md`, `outputs/evidence-ledger.jsonl` (256 records), selected Stage 1 briefs, quantitative-analysis exhibits.

The draft is unusually disciplined for a v1 — it obeys most of the curator's do-not-claim list and caveats SFO correctly. That discipline makes the remaining violations easier to see. The findings below are ordered by damage to the thesis, not by location in the draft.

---

## Findings

### F-1. The draft fabricates a scholarly citation the research pass explicitly failed to resolve

- **Location:** Footnote 10: "Sendelbach, S., and Funk, M., 'Alarm Fatigue: A Patient Safety Concern,' *AACN Advanced Critical Care* 24, no. 4 (2013): 378–86; Johns Hopkins ICU alarm-count referenced." Supporting the opening claim: "a single Johns Hopkins ICU study found an average of 771 alarms per bed per day."
- **Charge:** Invented construction / citation mismatch.
- **Evidence:** The only ledger record carrying the 771 figure is `virtual-christian::ev-4ded8693a914` — medium confidence, secondary, with the caveat: "primary Johns Hopkins study citation not resolved in this brief." No ledger record contains Sendelbach & Funk, the journal, the volume, or the page range. The draft supplied a fully formed academic citation the swarm never produced.
- **Why it matters:** This is the article's opening image and closing frame. If the fact-checker later finds the citation wrong in any particular, the entire lateral analogy — and the reader's trust — goes down with it. A fabricated-looking citation in footnote 10 taints footnotes 1–30.
- **Remedy:** Source or cut. Either verify the Sendelbach & Funk citation against the actual paper (WebFetch, one lookup) and add it to the ledger, or revert to what the ledger supports: "a Johns Hopkins ICU study reported by secondary sources," attributed as illustrative magnitude per the evidence map §9.

### F-2. "Order of magnitude cheaper" contradicts the draft's own numbers three paragraphs later

- **Location:** Executive Summary: "acoustic treatment premiums for the concourse-scale envelope at design time run an order of magnitude cheaper than at retrofit."[^7] Versus body ¶ "The window and the vehicle": "$5–$15 per square foot in new construction and $18–$45 per square foot as retrofit — a 2× to 4× premium."
- **Charge:** Overstated + internal contradiction.
- **Evidence:** `quantitative-analyst::ev-ff8f080c67c3` ($5–$15/ft² new) and `ev-aeed0d967d98` ($18–$45/ft² retrofit). The quantitative-analyst brief itself states "a 2× to 4× premium." An order of magnitude is 10×. The draft's own cited range supports at most ~3×–4× at the midpoints.
- **Why it matters:** The cost-avoidance argument is Proposition One of the three that "carry the case." A board member who divides 18 by 15 will conclude the author inflates, and will then discount the accurate numbers too.
- **Remedy:** Recalculate. Use "roughly two to four times" consistently, and see F-3 before doing so.

### F-3. The 2×–4× premium is a ratio between two different products from two different vendor blogs

- **Location:** Same passage; footnote 7.
- **Charge:** Source-quality failure / denominator error.
- **Evidence:** The numerator and denominator come from different sources describing different scopes: `ev-ff8f080c67c3` is "basic acoustic ceiling tile installation" from a contractor pricing guide (designtransitionstudio.com); `ev-aeed0d967d98` is "retrofit acoustic panel treatment" from a vendor blog (acousticmod.com). Both are medium confidence, non-primary, explicitly not airport-specific; the ledger caveats note airside badging/escort/night-work premiums are uncaptured. Dividing one vendor's panel price by another vendor's tile price is not a retrofit premium — it is an artifact.
- **Why it matters:** The financial proposition rests on the design-time-versus-retrofit differential. Right now that differential is constructed, not measured.
- **Remedy:** Qualify. Present the two ranges as separate directional benchmarks ("commercial pricing guides put new-construction acoustic treatment at $5–15/ft² and retrofit at $18–45/ft²; airport airside conditions raise both") and drop the derived multiplier, or anchor the premium in the CII rework literature the infrastructure-economist logged (with its own restated-source caveat, evidence map §6).

### F-4. The executive summary conflates the provisional $20B announcement with the committed AUL program

- **Location:** Executive Summary, first sentence: "MWAA is about to scope, procure, and commission more than $20 billion of terminal space at IAD and another $2.39 billion at DCA under a new fifteen-year Airline Use and Lease Agreement."[^1]
- **Charge:** Denominator error / overstated.
- **Evidence:** `infrastructure-economist::ev-525ee186f14c` (high, primary): the AUL at execution carries ~$6.99B IAD and ~$2.39B DCA. The $20B+ is the July 29, 2026 announcement — and `quantitative-analyst::ev-6d299a264850` carries the explicit caveat: "treat July 29, 2026 announcement paraphrases as provisional until underlying Board action, program budget amendment, and airline-consent documents are located." The sentence yokes a provisional announcement number and a contractual number under one "under the AUL" construction. The body (¶3) gets this right; the summary does not.
- **Why it matters:** Two ways. First, the 0.06%–0.20% cost ratio in ¶ "The window and the vehicle" uses the $20B provisional figure as its denominator — the largest available number, which minimizes the ratio. Against the committed $6.99B IAD program, the same $12M–$40M is 0.17%–0.57%. Still small; but the draft chose the flattering denominator. Second, the closing counter-response "start now, before design freeze on the projects the money is already committed to" is only true of the $9B AUL program, not the $20B program.
- **Remedy:** Recalculate and qualify. State both denominators or use the committed one; separate "committed under the AUL ($6.99B IAD / $2.39B DCA)" from "announced July 2026 ($20B+, provisional pending Board action)."

### F-5. The Part 382 kiosk claim (25%, December 2016) has no ledger support and inverts the direction of the mandate

- **Location:** Body ¶ "The people who most need to hear": "mandates accessible airport kiosks at up to 25% of installed machines under the December 2016 rulemaking";[^22] repeated in the mandatory-tier specification.
- **Charge:** Unsupported + citation mismatch.
- **Evidence:** The sole Part 382 ledger record, `regulatory-political-analyst::ev-48c339c22ad1`, contains no kiosk provision, no 25% figure, and no December 2016 date. The detail entered via the evidence map's E-09 summary, which the ledger record does not substantiate. Separately, "up to 25%" states a ceiling; the DOT accessible-kiosk rule imposes a floor (at least 25% accessible until full accessibility). As written, the draft describes a cap on accessibility as an accessibility mandate.
- **Why it matters:** The accessibility section is the draft's strongest defensive armor ("the people who most need to hear are the test"). A regulatory misstatement inside that exact section — in a document addressed to policy readers — is the most exposed possible location for one.
- **Remedy:** Source or cut. Verify against the eCFR text of the DOT kiosk rule (14 CFR 382.57) before retaining any percentage or date; otherwise cite Part 382's general accessible-information obligations only, which `ev-48c339c22ad1` supports.

### F-6. "Listed on the National Register (1978)" contradicts the ledger's primary federal source

- **Location:** Body ¶ "The people who most need to hear" and footnote 24: "IAD's Saarinen Main Terminal is listed on the National Register (1978)."
- **Charge:** Citation mismatch / source-quality failure.
- **Evidence:** The ledger contains a live contradiction the draft silently resolved toward the weaker source. `regulatory-political-analyst::ev-02b64dc7bbda` (high, primary — FAA report to the ACHP): the Main Terminal was "determined eligible for the National Register in March 1978" and its caveat states "the terminal was determined eligible but has not been formally added to the National Register." Against that: Wikipedia (`virtual-christian::ev-0310472f48f9`) and the context packet (`virtual-chris::ev-99e27d3fdd37`) say "listed 1978." The draft adopted the Wikipedia/packet version over the federal primary without flagging the conflict — exactly the substitution the evidence map §6 warns against for load-bearing claims.
- **Why it matters:** Marginally for the argument — Section 106 attaches to eligible properties as well as listed ones, so the compliance point survives either way. Materially for credibility: this is a checkable fact about the reader's own airport, and the draft's version disagrees with the FAA's own filing in the ledger.
- **Remedy:** Replace with the formulation both sources support: "determined eligible for the National Register in 1978 as part of the Dulles Airport Historic District; Section 106 consultation attaches to eligible properties." If the Strategist believes listing occurred, verify against the NPS database and update the ledger — do not out-vote a primary with an encyclopedia.

### F-7. The Schiphol characterization is wrong on its face and weakens the "category error" argument it serves

- **Location:** Body ¶ "The peer set": "They are single-terminal, short-haul, high-English-proficiency operations with traveler mixes that were quieter in the first place... IAD's 36%-plus international share and DCA's slot-constrained peaks are not their problems."
- **Charge:** Overstated / unsupported.
- **Evidence:** No ledger record describes Schiphol's traffic structure, terminal count, or haul mix (grep across 256 records: zero hits). The evidence map hedges — "three of the four are single-terminal, business-traveler-heavy" — and the contrarian brief distinguishes Schiphol as "a genuinely dense FIDS-plus-app model against a passenger base that expects it," not as short-haul. Schiphol is an intercontinental transfer hub whose international share exceeds IAD's; presenting IAD's 36% international share as a problem the peers don't have is untrue for at least AMS, and the draft flattens the map's "three of the four" into all four.
- **Why it matters:** The peer-dismissal is load-bearing: it licenses "MWAA does not need to import their brand. It needs to out-engineer them." A sophisticated reader who knows Schiphol will catch the error in one line, and the entire category-error argument — which is otherwise sound — inherits the discount.
- **Remedy:** Qualify. Keep the structural-difference argument but state it accurately: the shared claim the ledger supports (E-07) is that none of the peers has published intelligibility, missed-boarding, or channel-redundancy data, and that the transferability question is open. Differentiate LCY/HEL/CPH (small, point-to-point, single-terminal) from AMS (large transfer hub whose difference from IAD is design-and-app density, not traffic mix).

### F-8. The draft asserts tenant-audio reach the ledger says is unverified — then concedes the opposite in its own dependencies

- **Location:** ¶ "Governance is the technology": "A standard that specifies platform behavior... reaches through the tenant technology standards and the AUL to the microphone at the podium." Also Executive Summary Proposition Two: the Design Manual "bind[s] consultants, contractors, and tenants today," and ¶ "The window and the vehicle": "binds... through tenant technology standards and MASTERSPEC-derived specifications — the airlines and concessionaires whose systems set the soundscape today."
- **Charge:** Overstated / hidden assumption.
- **Evidence:** Evidence map §7 do-not-claim: "Do not claim that airline hold-room PA at IAD or DCA is subject to MWAA design authority today." `airline-commercial-strategist::ev-bbe86adff5f4`: at preferential-use gates the holdroom and podium PA are the airline's leased premises; "MWAA-specific gate arrangement... not confirmed here from an MWAA document." `airport-ceo::ev-e36d706a5fbe` caveat: "specific enforcement mechanics against tenants are not detailed." `quantitative-analyst::ev-41d72e9a58cc` caveat: standards touching airline hold-room audio "engage majority-in-interest and consultation." The draft's own Dependencies section admits MII provisions are unverified — while the body affirms present-tense reach.
- **Why it matters:** The contrarian's Scenario A is the thesis's sharpest failure mode: a standard that binds the base building while the actual noise sources sit inside the tenant envelope produces "cost imposed on the authority, noise unchanged for the passenger." If tenant reach is unverified, the draft's claim that the standard "reaches... to the microphone" is the single most consequential overstatement in the document.
- **Remedy:** Qualify throughout. Present tenant reach as the design objective of the standard, contingent on the AUL/tenant-technology-standards verification the draft itself lists as step one — not as an existing property of the Design Manual. Make the "binds tenants today" claim conditional in the Executive Summary, not just in the fine print.

### F-9. The counter-case paragraph omits the contrarian's two strongest objections

- **Location:** ¶ "The counter-case deserves an honest hearing" — lists four objections (IEC fluctuating noise, SFO methodology, peer structure, Design Manual latency/AUL uncertainty).
- **Charge:** Missing counterevidence.
- **Evidence:** The contrarian brief (selected per manifest; `outputs/stage1/contrarian-brief.md`) leads with two arguments the draft never engages: (a) **Redundancy** — NFPA 72, ADA §219, and ACRP 175 already set the intelligibility and assistive-listening floors that matter most; a new MWAA standard "will primarily regulate the discretionary space above the floor — passenger comfort — where the case for uniform prescription is weakest" (§1, bullet 1). (b) **Premature-specification risk** — "the economics literature on airport capital delivery does not support the axiom that earlier specificity is cheaper"; rigid overlays written before program-brief maturity are themselves a change-order driver (§1, bullet 7), plus Scenario B: STI commissioning gates on the critical path blocking TCO at Concourse C/D and triggering airline recovery disputes in the tightest DSCR window. The contrarian also offers a concrete smaller alternative — a mandatory 30%-design Communications-Environment Design Review with no new bi-airport thresholds — that the draft neither adopts nor rebuts.
- **Why it matters:** (a) attacks the draft's central identity claim (that MWAA needs a *new* standard rather than enforcement of existing floors); (b) attacks Proposition One directly (early = cheap) with the same rework logic the draft uses, pointed the other way; and the unaddressed alternative is precisely what a skeptical board asks for. An "honest hearing" that skips the two hardest questions is not one.
- **Remedy:** Defend. Add both objections to the counter-case and answer them — e.g., the standard's new content is the ADS map, representative-traffic commissioning, governance/audit logging, and channel-redundancy floors, which the existing codes do not require; and the commissioning gate should be specified as verification-with-cure-period, not a TCO condition. If the Strategist cannot beat the contrarian's smaller alternative on the merits, the recommendation should shrink toward it.

### F-10. The draft suppresses the United-posture contradiction while leaning on the July 2026 announcement

- **Location:** ¶3 ("On July 29, 2026, the President, the U.S. Transportation Secretary, United's CEO, and MWAA jointly announced...") and the closing counter-response ("the projects the money is already committed to").
- **Charge:** Cherry-picking / missing counterevidence.
- **Evidence:** Evidence map §3 contradiction 5, `airline-commercial-strategist::ev-25589088b745`: Cranky Flier characterizes Kirby's posture at the announcement as reluctant ("There is no world where he wants to pay to operate at this kind of palace") and describes United as prepared to shelve elements under a future administration. Companion record `ev-ae855a6678ab`: an airline briefing put transformation-scenario CPE at $90.64 versus $12.88 current. The map instructs: "The article should not present United as unambiguously enthusiastic." The draft presents the announcement's cast list without the ambivalence, and its "window" argument assumes program durability.
- **Why it matters:** The urgency case ("the window is finite") depends on the program actually proceeding on the announced arc. If the anchor carrier is positioned to shelve components, the correct framing is that the *standard* is cheap insurance either way — which is actually a stronger argument than the one the draft makes, because a Design Manual amendment survives program shrinkage while a program-contingent pitch does not.
- **Remedy:** Add one sentence acknowledging the analyst read of United's posture (attributed as commentary, per map §6) and reframe the urgency argument to be robust to program re-scoping.

### F-11. The 5:30 p.m. September 2025 IAD vignette is an invented scene wearing the costume of reportage

- **Location:** ¶2: "Cross to IAD at 5:30 p.m. on a weekday in September 2025, in the international connecting bank. A gate change at Concourse C paged overhead. A TSA advisory. Two boarding calls at adjacent gates..."
- **Charge:** Invented construction.
- **Evidence:** No ledger record documents any observed announcement sequence at IAD — no PA logs, no announcement-frequency measurement, no dated observation. The specificity (date-month precision, gate locations, announcement inventory) implies an evidentiary basis that does not exist. The draft's own "What would change this recommendation" section concedes MWAA has published no PA telemetry.
- **Why it matters:** The run prompt bans "unverified claims without operational data." A reader who asks "who logged this?" gets no answer, and the passage sits immediately before the draft's genuine traffic statistics, borrowing their authority.
- **Remedy:** Qualify or cut. Either mark it explicitly as a composite/hypothetical ("picture the international bank at 5:30 p.m....") or replace it with the airport-coo brief's operator vignettes, which are at least attributed to a named persona's professional experience rather than staged as observation.

### F-12. The ACI-NA "guidance" is a vendor-context advocacy post promoted to institutional authority

- **Location:** ¶ "Governance is the technology": "The Airports Council International – North America has framed the newer generation of automated announcement platforms in terms MWAA's Design Manual can actually enforce..." Footnote 25: "published guidance."
- **Charge:** Source-quality failure / overstated.
- **Evidence:** `operations-analyst::ev-08af28494c7c` — medium confidence, with the ledger caveat "industry advocacy piece with vendor context; directional rather than measurement-grade." It is a February 2026 ACI-NA website article, not ACI-NA guidance, a recommended practice, or a standard. The only corroborating record is a vendor website (`virtual-pat::ev-7b1cb65b62df`, AviaVox self-reported claims).
- **Why it matters:** "Governance is the technology" is a full load-bearing paragraph — the draft's answer to how announcement policy becomes enforceable. Its evidentiary base is one advocacy post plus one vendor page. The governance argument itself (audit logs, template control, centralized management) is sound engineering logic; it should stand on the requirements framework, not on a borrowed institutional imprimatur.
- **Remedy:** Requalify the attribution ("an ACI-NA-published industry article describes...") and let the enforcement logic carry its own weight as MWAA's specification choice, which needs no ACI-NA endorsement.

### F-13. The DCA Terminal 1 sequencing rests on a project status the run never established

- **Location:** ¶ "Exercise it first where the friction is lowest" and the Decision block: "in time to govern the scope documents for the DCA Terminal 1 replacement."
- **Charge:** Hidden assumption / stale-or-absent data.
- **Evidence:** Evidence map gap §5.e: "The Council could not confirm whether Terminal 1 is in design phase, procurement phase, or funded programming only. This changes the 'when'..." No ledger record establishes that scope documents are forthcoming, or that the standard can be adopted "in time." The draft discloses the AUL and Design Manual gaps in its failure-mode section but never discloses this one.
- **Why it matters:** The pilot-first sequencing is the recommendation's implementation spine. If Terminal 1 is already in design, the "specify before designs harden" logic partially inverts for the very project chosen as the proof case.
- **Remedy:** Qualify. Add Terminal 1 phase verification to the 90-day list alongside the Design Manual review, and add a branch to the failure-mode section: if Terminal 1 is past scope-definition, the reference application shifts to the IAD C/D program elements still in programming.

---

## Claim-to-evidence coverage summary

Of the draft's 30 footnotes: **22 trace cleanly** to ledger clusters or the quantitative-analyst exhibits (the standards stack fn4–6, 20–21, 23, 27–29; the financials fn9, 15; traffic fn12–13; peers fn16–17; SFO fn18–19 with correct caveats; Design Manual fn2, 8; collision fn3; Concourse E fn30; airline shares fn26 with the directional caveat carried). **Four are supported but misused** (fn7 — supported by quant exhibits but contradicted in the exec summary and built on cross-source vendor benchmarks, F-2/F-3; fn1 — conflated denominators, F-4; fn25 — authority inflation, F-12; fn24 — resolved against the primary, F-6). **Two are unsupported in the ledger** (fn10 — fabricated-form citation, F-1; the fn22 kiosk detail, F-5). The un-footnoted September 2025 vignette is invented (F-11). The $12M–$40M figure, which I initially suspected was invented, in fact traces to `outputs/stage1/quantitative-analysis/calculations.json` and the quantitative-analyst brief, which labels it "not a bid estimate" — the draft carries that caveat adequately in fn7.

## The five most load-bearing claims

1. **The Design Manual is a mandatory enforcement vehicle MWAA already owns (E-04).** Survives — 8 agents, including MWAA's own description. The tenant-reach extension does not survive as stated (F-8).
2. **Intelligibility, not silence, is the engineering variable, with NFPA 72 / ACRP 175 / IEC 60268-16 floors (E-01/02/03).** Survives, including the fluctuating-noise self-caveat, which the draft handles honestly. Note all NFPA/IEC citations are secondary summaries of paywalled codes; the draft's cite-the-adopted-edition instruction (fn4) is the correct hedge. Partially exposed to the contrarian's redundancy objection until F-9 is answered.
3. **Early specification is dramatically cheaper than retrofit (Proposition One).** Does not survive as stated: "order of magnitude" is contradicted by the draft's own 2×–4×, the multiplier is a cross-vendor artifact, and the premature-specification counter is unaddressed (F-2, F-3, F-9).
4. **The financial window (DSCR 1.63×→~1.3×, ~$5.5B new debt) makes now the moment (E-05).** Survives on the numbers (7 agents, rating-agency-derived). The urgency framing is exposed to the United-posture omission (F-10) and cuts both ways per the contrarian (commissioning gates in a tight coverage window are a cost, not only a savings).
5. **The peer set is a policy analogue, not a design precedent (E-07).** The conclusion survives; the supporting characterization does not (F-7). Fix the Schiphol sentence and this becomes one of the draft's strongest sections.

## Counterevidence minimized or omitted

- The contrarian's redundancy argument and 30%-design-review alternative (F-9) — the largest omission.
- Premature-specification change-order risk and the commissioning-blocks-TCO scenario (F-9).
- United's ambivalent posture and the $90.64 airline-side CPE figure (F-10).
- ACRP 239 (2023), which the map identifies as the current source for the accessibility and older-adult case; the draft argues accessibility entirely from regulations and never deploys the stronger, newer research document.
- The FLL 2017 after-action material (director-of-public-safety, primary AAR) on communications failure under emergency reversion — directly relevant to the draft's own "the announcement that matters" framing, unused.

## Narrative flourish outrunning the record

- The September 2025 IAD vignette (F-11).
- "Every standard adopted after design freeze becomes a change order" — an absolute supported only by CII heuristics the map restricts to framing use.
- The ICU analogy used as both opening and closing frame; the map's instruction was "cite it once... only if the article has room." As the structural spine it now carries more weight than a medium-confidence, unresolved-primary record can bear (F-1).
- "MWAA does not need to import their brand. It needs to out-engineer them." Fine as rhetoric; ensure F-7's correction doesn't leave it stranded.

## Acquittals — important claims that are well supported

- **The SFO treatment is exemplary.** The draft quotes the operating model, attributes every outcome number to SFO, states flatly that no methodology exists, and preserves the passenger-complaint counterweight. This is exactly what the map ordered (E-08, §7).
- **The NFPA 72 numbers.** The draft picks the widely corroborated 0.45/0.50 formulation over the outlier trade-source variants and instructs citation of the AHJ-adopted edition — correctly resolving map contradiction §3.2.
- **The fluctuating-noise limitation of IEC 60268-16** is surfaced, credited, and converted into a requirement (representative-traffic commissioning) rather than buried. Honest and constructive.
- **Traffic and financial statistics** (IAD 29.01M/10.53M intl; DCA 24.89M, −5.4% with MWAA's attribution; DSCR trajectory; AUL structure) all trace to high-confidence ledger records.
- **The failure-mode and stop-condition section** — including the concession that the current Design Manual content is unverified and the recommendation may contract — is the kind of honesty the run prompt demanded. Extend it per F-13, don't dilute it.

## Verdict

The argument's skeleton is sound and unusually well-aligned with the curated evidence. The convictions are concentrated in five places: one fabricated-form citation (F-1), one internal numerical contradiction on the core financial proposition (F-2/F-3), one denominator conflation in the opening sentence (F-4), two regulatory-fact errors in the accessibility/preservation armor (F-5, F-6), and a pattern of asserting tenant reach and peer differences beyond what the ledger holds (F-7, F-8). All are repairable in one revision. F-9 is the one that requires new argument rather than repair: the draft must beat the contrarian's smaller alternative, not ignore it.
