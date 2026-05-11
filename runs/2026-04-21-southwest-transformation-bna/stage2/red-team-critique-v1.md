# Red Team Critique: Strategist Draft v1
## Southwest Transformation at BNA

**Draft critiqued:** `/Users/christiankessleriv/Repos/ai-council-mwaa/outputs/stage2/strategist-draft-v1.md`
**Critique version:** v1
**Date:** 2026-04-21
**Reviewer:** Red Team (skeptical senior analyst)

---

## Summary assessment before the enumeration

This is a strong draft at the level of macro-architecture, but it is riddled with small-to-medium integrity problems that will embarrass the Council if they reach a Southwest network planner or an MNAA finance committee. The most serious problems: (1) the named-character opening ("Bill Franklin" plus a specific flight and gate agent and ramp lead) is not supported by the briefs and reads as narrative invention; (2) the Contrarian's two strongest points are paraphrased but not actually defeated; (3) several analyst-derived numbers are presented as brief-cited when they are not, and the draft's own closing disclosure undersells the count; (4) the piece misses live, load-bearing findings from the Regulatory and Technology Scout briefs (overhead-bin TWU grievance specifics, the bin-retrofit timeline, the Trump-era penalty waiver, the 1.8% Q4 2025 EBIT-ahead-of-guidance validation number) that would actually sharpen the argument.

---

## 1. The opening names "Bill Franklin" as a historical person. Unsupported.

**Location:** Section I, paragraph 4 ("Two decades earlier...")  and again in Section III.a, paragraph 3 ("The 10-minute turn, invented in 1972 by Bill Franklin and a ground crew...").

**Issue:** The Historian brief references the 1972 ten-minute turn and cites Southwest's own history page at southwest50.com, but nowhere in the Historian brief, the Airline brief, or the Operations brief is any individual named "Bill Franklin" identified as the inventor of the ten-minute turn. The Historian brief attributes the turn to "a ground crew" anonymously. The Operations brief repeats "Bill Franklin's 1972 '10-minute turn' concept" but with no source beyond the same southwest50.com link. The attribution may be accurate in Southwest corporate lore, but neither Stage 1 brief establishes it with a citation naming the individual. The Strategist has accepted a name from one brief's prose without verifying it, and then embellished it into a character ("Bill Franklin's operational miracle, three planes flying a four-plane schedule through Texas") that invites readers to treat it as a documented historical figure.

**Recommendation:** Either (a) verify the attribution against the Southwest 50 source and add the citation explicitly in prose ("the ramp supervisor Bill Franklin, according to Southwest's official history"), or (b) cut the name entirely and keep it anonymous ("a ramp crew at Dallas Love Field in 1972"). Narrative license does not extend to elevating a name in a secondary source to a protagonist. If you do keep the name, say where it comes from in the sentence itself.

---

## 2. The opening scene invents specific unnamed characters and a specific flight. Soft invention.

**Location:** Section I, paragraphs 1–3 ("On a Tuesday in April 2026, Gate D6... WN 1442 to Baltimore... 175 seats, all sold... A ramp lead checked a tablet. A gate agent in the new uniform... Eleven minutes late. Ground time from block-in to pushback, 44 minutes.").

**Issue:** None of the Stage 1 briefs establishes WN 1442 as a real flight on a specific April 2026 Tuesday, or the specific 5:47 block-in and 6:31 departure times, or that the forward bin filled at Group 2, or the 44-minute ground time on this specific turn. The run prompt asks for narrative in the McPhee/Lewis/Kidder tradition, but McPhee does not invent scenes — he reports them. Lewis does not invent dialogue — he gets it from people. The draft opens by asking the reader to trust a scene that is, on the evidence of the briefs, a composite or an illustrative fabrication. Airport executives will notice.

**Recommendation:** Two clean options. (a) Mark the scene as illustrative in the prose itself — "A typical morning at Gate D6 looks something like this" — which costs a little narrative punch but preserves honesty. (b) Keep the concrete scene but strip the invented specifics: drop the flight number, drop the exact times, drop the gate agent's scan-sequence training estimate. Ground the opening in things the briefs actually establish: 49-minute average turns, 175-seat MAX 8s, eight groups, TWU grievance filed, Concourse D has 11 gates. The scene can still land without inventing a flight. If you want a specific flight, pick one the historian already documented: the Concourse D opening on "Southwest flight WN2086 to Denver from gate D1" (Historian brief, Evidence section) is real and dramatic.

---

## 3. The "two seconds per boarding pass" and "old sequence, closer to one" detail is unsourced.

**Location:** Section I, paragraph 2 ("a scan sequence that the carrier's training material estimates at two seconds per boarding pass; the old sequence, under open seating, ran closer to one").

**Issue:** No Stage 1 brief contains this figure. The Operations brief cites the 1–4 minute boarding-time increase from Southwest's own 2006 testing, but does not break the per-pass scan time down to seconds, and certainly does not reference Southwest training material. The Technology Scout discusses the stanchion-to-digital transition but not scan sequence timing.

**Recommendation:** Delete the sentence or substitute the sourced figure. The 1–4 minute boarding increase from the Operations brief is vivid enough without fabricating a per-pass second count.

---

## 4. The TWU grievance is cited but the specifics are thinner than the draft implies.

**Location:** Section I, paragraph 2 ("the bin-stow congestion that the Transport Workers Union had filed a formal grievance about two months earlier").

**Issue:** The Technology Scout brief documents the TWU filing "formal complaints about crew bag stowage areas being relocated to accommodate passenger bin overflow" (Evidence section, citing aviationa2z.com from February 2026). The draft's phrase "two months earlier" is chronologically plausible against an April 2026 scene but is not established in the briefs as a specific grievance date. More important: the actual grievance was specifically about crew bag stowage, not about passenger bin-stow congestion per se. The draft blurs the two.

**Recommendation:** Either quote the grievance's actual subject (crew bag stowage) or drop the "two months earlier" precision. The bin-stow congestion claim is defensible on its own without attaching it to a specific labor filing that was about a different, adjacent issue.

---

## 5. Contrarian's strongest points are paraphrased in Section IV but not actually defeated in Section V.

**Location:** Sections IV and V. Specifically, the "BNA built to demand, not to carrier specification" argument (Contrarian brief, Key Finding 2) and "Southwest is setting departure records" (Contrarian brief, Key Finding 1) are both reproduced at length in IV and then addressed in V.

**Issue:** Section V's responses to these two points are the weakest prose in the essay and they do not fully defeat the Contrarian's position.

- On "demand vs. carrier specification," V's argument is that "Southwest is the mechanism through which more than half of BNA's demand reaches the airport." That is true but it is not a response to the Contrarian's actual claim, which is that demand projections drove BNA Vision and New Horizon, not Southwest's operating model. The fact that Southwest delivers most of the demand does not refute the claim that the capital was scaled to the demand. The draft needs to show that BNA's specific design decisions — hold room sizing, BHS specification, gate podium configuration — were in fact calibrated to carrier-specific assumptions, not just demand totals. The Engineer brief has the ammunition (ACRP 25 hold room factor; BHS bag-mix question flagged UNVERIFIED) but the draft does not actually marshal it against the Contrarian in V. It asserts the conclusion.

- On "Southwest is setting departure records," V concedes "The 190 peak-day departures rising to 215 are real" and then pivots to dwell-time compositional shift. This is competent but under-argued. The Contrarian specifically says airlines do not commit $53M to lounge fit-outs at airports they are retrenching from — and the draft never directly answers that. The Airline brief's framing ("Nashville is the proof of concept. If it fails, Nashville absorbs a $53 million write-off.") is actually the tool that cuts against the Contrarian here — a proof-of-concept bet is not the same as a retrenchment signal — but it is also not the same as "Southwest is unambiguously embedding." The draft should use that finer distinction instead of conceding the point and changing subject.

**Recommendation:** Rewrite Section V's first and second sub-arguments to engage the Contrarian on their own terms. Cite the Engineer brief specifically on whether the hold rooms at the Concourse D Extension (which opened July 2025) were sized against the new or old throughput model — that question is unresolved in the public record, per the Engineer brief, and that unresolved-ness is the actual refutation of "BNA built to demand." On the lounge: make the proof-of-concept argument explicit. The lounge is a strategic bet whose failure scenario is a $53M write-off in a live terminal, not unconditional commitment evidence.

---

## 6. The "Contrarian's strongest point... is correct" admission in Section III.d is jarring against the thesis.

**Location:** Section III.d, final paragraph ("The Contrarian brief's strongest point — that a banking structure will make Southwest a more intensive user of BNA facilities, not a lighter one — is correct.").

**Issue:** Conceding the Contrarian's point in the middle of the argument section, without then showing what the Contrarian missed, is a rhetorical sag. The next sentence — "The question is whether the facility was designed for intensive use of this particular kind" — is the right move but reads as a pivot rather than a rebuttal. And placing the concession in III.d before the full counter-case is even presented in IV means the reader encounters the same concession twice, with the second time (in V) doing the analytical work the first one gestured at.

**Recommendation:** Cut the explicit concession from III.d. Let the section state the banking-hub mismatch argument on its own merits and save the Contrarian engagement for IV/V where the structure supports it. Or, if you want to keep the concession, move it to V and do the analytical work in one place.

---

## 7. The "Bill Franklin" / "three planes flying a four-plane schedule" framing is cleaner than the Historian brief supports.

**Location:** Section III.a, paragraph 3 ("a ground crew that actually achieved 22 minutes on a schedule designed for four aircraft flown by three").

**Issue:** The Historian brief says "In 1972, Southwest was operating with three planes on a schedule designed for four. To maintain the schedule, ground crews turned a 737 in 10 minutes. The airline's official history records the crew achieved 22 minutes — which was enough." The draft cleans this into a near-mythic origin narrative. The Historian brief itself is careful to note the 22 minutes "was enough" — which is a different narrative than the draft's heroic framing. A sophisticated reader of Southwest history will know the airline was operationally ad-hoc in 1972, not launching a load-bearing cost-structure vision.

**Recommendation:** Soften the mythologizing. "The ten-minute turn was an operational expedient that became a cost-structure discipline" is more accurate than "Bill Franklin's operational miracle." The Historian brief Key Finding 1 calls it "the mechanical interlocking parts of a cost structure" — use that phrasing.

---

## 8. The claim that "Every piece of Southwest's commercial model... was a mechanical component of a machine" is the Historian's prose lightly rewritten.

**Location:** Section III.a, paragraph 3.

**Issue:** Compare to Historian brief Key Finding 1: "They were the mechanical interlocking parts of a cost structure that let Southwest earn money in markets where legacy carriers bled." The draft has "a mechanical component of a machine designed to generate more flying hours per aircraft per day than any competitor could match." This is close enough to the brief's phrasing to read as a paraphrase without citation credit and not close enough to be a proper quote. It is in the gray zone where the Strategist is re-using a brief author's vivid framing without attribution.

**Recommendation:** Either quote the Historian directly ("the Historian brief called them 'the mechanical interlocking parts of a cost structure'") or re-phrase further into the Strategist's own voice. The current version is too close for comfort.

---

## 9. "Bag fees... now $45/$55" is slightly sloppy on the date sequencing.

**Location:** Section II, bullet 1 and Section III.e.

**Issue:** The Airline brief is careful: "In July 2024, CEO Bob Jordan told investors... Nine months later, on March 11, 2025, the carrier announced it would begin charging $35/$45 for first/second bags effective May 28, 2025. By late 2025, those fees rose further to $45/$55." The draft in III.e says "Southwest's first-checked-bag fee went into effect May 28, 2025, at $35. It rose to $45 later the same year, and the second-bag fee to $55." That is right. But the Executive Summary in Section II says "introduced checked-bag fees (now $45/$55)" — which compresses the 2025 sequencing and misses the initial $35/$45 structure. The Chief Engineer brief also says "$35, then raised to $45 effective April 2026." That is a different date.

**Recommendation:** Reconcile the dates across the draft. The Engineer brief's "effective April 2026" is either wrong or it is a second increase the draft hasn't accounted for. Flag the discrepancy to the Fact-checker. In prose, be explicit about the two-step sequence: $35/$45 in May 2025, $45/$55 by late 2025.

---

## 10. "166 daily departures rising to a planned 215 by fall 2026" in Executive Summary bullet 2 is correct but buries the 190 peak-day spring 2026 interim.

**Location:** Section II, bullet 2.

**Issue:** The Airline and Contrarian briefs both establish 190 peak-day departures in spring 2026 rising to 215 by fall 2026. The draft says "operates up to 166 daily departures rising to a planned 215 by fall 2026," which collapses the intermediate step and implies a jump from 166 to 215. This is directionally accurate but numerically imprecise.

**Recommendation:** "Operates up to 166 daily departures today, 190 in spring 2026, and a planned 215 by fall 2026." The three numbers tell the actual growth story.

---

## 11. "19.5 departures per gate per day" — analyst-constructed, partially disclosed, but calculation base is also analyst-selected.

**Location:** Section V, sub-argument 2 ("Eleven gates cycling 215 departures requires 19.5 departures per gate per day...").

**Issue:** The draft's closing note (line 224) flags 19.5 as analyst-constructed: "constructed transparently from the 215-departure figure in the Contrarian brief and the 11-gate figure in the Airline brief." Good. But the prose itself does not flag it as analyst-constructed — the reader encounters "19.5 departures per gate per day" as if it were a known quantity. A diligent airport ops reader will also note: 215 is a peak-day figure, not an average-day figure, so dividing 215 by 11 to generate a per-gate cycle rate conflates peak with average. The real average may be lower; the real peak may be higher because aircraft do not distribute evenly across gates. Additionally, Southwest does not operate all its BNA flights from Concourse D — the Airline brief specifies "Southwest also operates from gates in Concourse C — C4, C7, C9, C16, C18, C19, C20, C21, C22, and C25, some of which require a shuttle bus connection from the main terminal." The denominator 11 is therefore wrong; the actual Southwest gate count at BNA includes Concourse C gates.

**Recommendation:** Either (a) rework the calculation against the correct total Southwest gate count at BNA (11 on D plus some number on C) and flag it in prose as "a back-of-envelope estimate: 215 divided by total Southwest gate positions at BNA," or (b) drop the per-gate number and argue from total gate-hours instead. And add "(analyst calculation)" or equivalent in the sentence itself, not only in the closing note.

---

## 12. "Crew base... housing 650 to 1,300 pilots and flight attendants" — range is wider than the briefs support.

**Location:** Section III.d, paragraph 2.

**Issue:** The Airline brief says "650-1,300 pilots and flight attendants based there." The Historian brief says "500-700 flight attendants and 150-200 pilots to Nashville." The Economist brief says "approximately 500–700 flight attendants and 150–200 pilots." The Contrarian brief says "150-250 pilots and 500-700 flight attendants, with explicit growth targets." The consistent set is 500–700 FAs + 150–250 pilots = 650–950 total. The 1,300 upper bound comes from only the Airline brief, and the Technology Scout brief casually mentions "approximately 1,000 employees based at BNA" as a separate total. The draft's "650 to 1,300" uses only the Airline brief's outer range without flagging the wider range of estimates.

**Recommendation:** Use a tighter range ("roughly 700–950 combined pilots and flight attendants") or, if you want to preserve the upper bound, flag the range disparity: "estimates range from 650 to 1,300 depending on source and whether growth targets are included."

---

## 13. Section III.b collapses BNA Vision cost history in a way the Economist brief would not.

**Location:** Section III.b, paragraph 1 ("BNA Vision — the predecessor program to New Horizon — launched in 2017 with a $1.2 billion budget and delivered in February 2024 at $1.5 billion, a 25% escalation that the Authority has not publicly characterized as overrun.").

**Issue:** The Economist brief Key Finding 6 is explicit: "No public documentation attributes the increase to specific scope changes versus construction inflation versus schedule-related carrying costs; the authority has not characterized the increase as a 'cost overrun' and the program was completed in February 2024." The Strategist's phrasing "that the Authority has not publicly characterized as overrun" is correct but drops the preceding "no public documentation attributes" caveat. The effect is to imply MNAA is suppressing an overrun disclosure, which is stronger than what the Economist brief actually supports. Global precedents (Berlin, LAX APM) in the Economist brief establish that 25% escalation is modest by sector standards — the Economist brief explicitly calls it "modest by sector standards." The draft does not.

**Recommendation:** Add the context the Economist brief provides. Something like: "a 25% escalation that is modest by global airport-megaproject standards (Berlin Brandenburg ran triple; LAX APM is on track to run double) but that the Authority has not publicly characterized as scope change, inflation, or overrun." That tells the reader the number is unremarkable in sector terms without burying the transparency question.

---

## 14. The claim "MNAA spent years trying to exit it" (the MII structure) is directionally supported but phrased too strongly.

**Location:** Section III.g, paragraph 2.

**Issue:** The Regulatory brief establishes that the new agreement ended "28 years of financial control by the airlines" and "MNAA secured it in mid-2023 and executed the new seven-year agreement July 1, 2023." Nothing in the briefs specifies "years of trying to exit" — that is an interpretive leap. The negotiation may have been intensive and long; it may have been resolved quickly once Southwest was ready. The brief does not say.

**Recommendation:** Soften to "that MNAA had sought to renegotiate for a long time" or similar, and drop the editorializing sentiment ("a genuine generational win, and the fact that the New Horizon program is proceeding at scale is the direct consequence of it"). That last clause is an analyst opinion — correct but not cited.

---

## 15. Section III.h (Tennessee governance) understates and misses a live element flagged in the Regulatory brief.

**Location:** Section III.h.

**Issue:** The Regulatory brief explicitly flags that the Supreme Court's ruling, "expected in 2026," could "retroactively unsettle the governance structure under which New Horizon was authorized and the 2023 airline use agreement was executed." The draft captures the forward-looking board-appointment risk but drops the retroactive unsettling point, which is the more serious capital-planning exposure. The Regulatory brief also documents that the Supreme Court consolidated the MNAA case with a parallel Metro Council size case — the draft mentions consolidation in passing but does not engage with why that matters (it widens the legal question beyond airport governance specifically).

**Recommendation:** Expand III.h by roughly 40%. Include (a) the retroactive risk to New Horizon authorization, (b) the consolidation with the Metro Council case, and (c) the specific rating-agency disclosure that governance risk is a priced consideration. Currently the section reads like a footnote; the Regulatory brief treats it as material.

---

## 16. "Senior debt service coverage is projected to fall from 19.11x in FY2024 to 1.80x in FY2030" — the draft omits FY2025 5.95x and does not flag the federal pandemic-relief effect.

**Location:** Section II bullet 5; Section III.f, paragraph 4.

**Issue:** The Economist brief Evidence section says FY2024's 19.11x is "inflated by $30–40 million in annual federal pandemic relief funds applied to debt service," and FY2025's 5.95x is the "last year of meaningful federal relief application, approximately $5.5 million." The draft presents the 19.11x-to-1.80x trajectory as if it were a pure debt-program story, which it is not — half the apparent collapse is the roll-off of federal relief. Sophisticated bond readers will see the framing as misleading.

**Recommendation:** Flag the federal-relief effect in the prose. "The trajectory from 19.11x to 1.80x is partly an artifact of federal pandemic-relief funds rolling off after FY2025; a cleaner comparison is FY2025's 5.95x against the 2030 trough." That framing is both more honest and, if anything, more analytically useful — it is the difference between 5.95 and 1.80 that matters, and the ratio 3.3x is still dramatic.

---

## 17. "The Authority's own rate-of-return and cost study projects the trajectory continuing to $17.48 by FY2032 — a 106% increase over eight years" is arithmetic the draft should double-check.

**Location:** Section II, bullet 4; Section III.f, paragraph 2.

**Issue:** Economist brief says "FY2024: $8.49 / FY2032: ~$17.48 (projected)." $17.48 / $8.49 = 2.06, a 106% increase. That is correct. But the Economist brief's own Quotable Data Point 2 says "a 91% increase in seven years" from $9.16 (FY2025) to $17.48 (FY2032). The draft chooses the larger percentage (106% across FY2024–FY2032) rather than the Economist's preferred framing (91% across FY2025–FY2032). Both are defensible, but the draft should disclose which base year it uses and why.

**Recommendation:** Either stick with the Economist brief's 91% seven-year framing, or keep 106% and add "from FY2024 to FY2032" explicitly so the reader can see the base.

---

## 18. "The lounge is... being built for a Chase co-branded credit card projected at $500–$600 per year, competing directly with the Delta Reserve card's $650 and United Club's Infinite tier."

**Location:** Section I, paragraph 5.

**Issue:** The Airline brief establishes the $500–$600 projection and the Delta Reserve $650 comparison. The Technology Scout brief puts the figure at "approximately $595 annual fee." The draft is fine on the numbers but "competing directly with... United Club's Infinite tier" is a little loose — the Technology Scout brief references "United Club Infinite" without pricing. If you're comparing against Delta Reserve at $650, give the United number too or drop the United reference.

**Recommendation:** Either add the United Club Infinite card's current annual fee (publicly available — $695 as of 2024) with the source, or drop the clause.

---

## 19. Section III.e invents a behavioral assumption and presents it as brief-supported.

**Location:** Section VI, second decision point ("(b) a 25–30% passenger shift from carry-on to check").

**Issue:** The Engineer brief says "Even a conservative behavioral assumption — say, 25-30% of passengers who previously carried on now check bags — materially increases..." That is the Engineer's own conservative assumption, not an established behavioral finding. The draft picks up "(b) a 25–30% passenger shift from carry-on to check" in a load-case specification that reads as if it were a settled research input. It isn't. It's the Engineer's rule-of-thumb.

**Recommendation:** Flag it in the prose. "A behavioral assumption in the engineer's own judgment (25–30% carry-on to checked shift)" or similar. The shift is plausible but the source matters if MNAA is going to use this as a load case specification.

---

## 20. The Technology Scout's overhead-bin-retrofit timeline is load-bearing and under-used.

**Location:** Section III.e, paragraph 3.

**Issue:** The Technology Scout brief's most specific finding is that Southwest is "retrofit seven of every ten aircraft with larger overhead bins (50% increased capacity) by end of 2026." The draft mentions this in passing ("Southwest is retrofitting seven of every ten aircraft with 50%-larger bins to absorb by end of 2026") but does not use it to its full analytical weight. The bin retrofit is the specific mitigation for the bin-stow congestion, and it is the kind of detail that tells a sophisticated reader the Strategist understands the transformation's operational ecology. It should be a named counter to the Contrarian's turn-time-recovery optimism: even with RIDS and paperless turns, the physical cause of bin congestion (smaller bins than the checked-to-carry-on shift demands) is only being addressed on 70% of the fleet, on a multi-year schedule.

**Recommendation:** Expand the bin retrofit detail in III.e and use it in V's sub-argument 3 (the turn-time recovery section). The current draft treats it as a grace note; it should be a paragraph-level piece of evidence.

---

## 21. The draft under-uses the Chief Engineer's DEN Great Hall cautionary case.

**Location:** The DEN case is absent from the draft entirely.

**Issue:** The Engineer brief Key Finding 7 establishes that DIA terminated a $1.8B DBFOM contract in 2019 after $288M in projected overruns, with the after-action report identifying unclear owner decision-making as the root cause. The brief argues: "BNA's program is better structured — CM at Risk versus a P3 DBFOM — but the interface between the Concourse A reconstruction, the simultaneous BHS installation, and the Central Core Enhancement still creates a multi-prime coordination problem." This is a constructability lens that directly supports the draft's Section VI recommendations about stress-testing remaining tranches. The Strategist has skipped it.

**Recommendation:** Add a paragraph in Section VI (before the 2031 use-agreement negotiating-position discussion) on governance/multi-prime coordination risk. Use the DEN precedent as the cautionary case. This is the Chief Engineer's on-constructability lens being under-used, exactly the kind of gap the critique spec calls out.

---

## 22. The Historian brief's "No clean historical precedent... and the brief should say so" honesty is partially honored but partially collapsed.

**Location:** Section II bullet 7; Section V sub-argument 4.

**Issue:** The Historian brief Key Finding 8 is explicit: "No US carrier-airport pair offers a clean template for what is happening at BNA... Southwest at 54% of BNA seat capacity is a different order of concentration than jetBlue at JFK or America West at Phoenix... The concentration at BNA... has no clean historical parallel among US carrier-airport relationships outside the fortress hub cases, and those cases all ended in dehubbing, which is not what is happening here."

The draft's Section V sub-argument 4 does acknowledge this ("the historical analogies that fit are not the ones the Contrarian brief or the thesis relies upon") and names US Airways / America West as the closer analog. Good. But the Executive Summary bullet 7 presents the US Airways / America West case more confidently than the Historian warrants — "the strongest warning is the US Airways / America West case" reads as if the Historian has blessed this as the load-bearing precedent. The Historian's actual position is closer to: US Airways/America West is the closest-in-kind, but no clean precedent exists, and Midway-under-Southwest is the closest-in-kind-but-not-scale alternative. The draft collapses that subtlety.

**Recommendation:** Revise Executive Summary bullet 7 to: "The historical analogies are imperfect, and the Historian explicitly notes no clean precedent exists. The closest in kind is US Airways / America West (2005–2013), where the LCC-to-legacy drift was visible only in retrospect. The closest in the other direction is what Midway absorbed as Southwest grew through the 1980s–90s, but at a different scale and in the opposite direction of change." That is more faithful to the Historian brief.

---

## 23. Voice — "It is worth noting that" / "As we have seen" instances.

**Location:** Several spots, mostly moderate rather than egregious.

**Issue:** The draft is largely disciplined on hedging, but some weak phrases have slipped in:

- Section III.f, paragraph 1: "That letter is the revealed-preference data point that matters most in this analysis." The phrase "in this analysis" is filler; the sentence is stronger as "That letter is the revealed-preference data point that matters most."
- Section III.g, final paragraph: "Both sides got what they wanted. One side knew more about what was coming." This is good. But earlier in the same section: "Southwest negotiated those rates during the same quarter it was finalizing its Investor Day transformation internally." "The same quarter" is loose — the brief says July 2023 agreement, September 2024 Investor Day, which is five quarters apart. The draft is wrong on the timing.
- Section V sub-argument 2, final paragraph: "The math is not impossible. The math is narrow. And the narrower it gets, the more each one of Southwest's initiatives — lounge space, premium queuing, priority bag handling — has to fit inside the existing concrete rather than require new concrete that the program has not funded." This paragraph is strong — short sentences, active voice. Good rhythm. Preserve this voice across the rest of the document.
- Section V sub-argument 7, final sentence: "Demand-robust alone is not sufficient when one carrier produces more than half the demand and is mid-transformation on the operational side of the ledger." The phrase "on the operational side of the ledger" is mild consultant-speak. Cut to "mid-transformation operationally."

**Recommendation:** Do a voice pass. Specifically hunt for "in this analysis," "on the ledger," "at the analytical level," and similar consultant tics. The run prompt specified McPhee/Lewis/Kidder — none of them write "at the analytical level."

---

## 24. The transformation timing in Section III.g is wrong.

**Location:** Section III.g, final paragraph ("Southwest negotiated those rates during the same quarter it was finalizing its Investor Day transformation internally.").

**Issue:** The airline use agreement was signed July 1, 2023. Investor Day was September 26, 2024. These are not the same quarter. They are fifteen months apart. The Regulatory brief says Southwest "negotiated those rates in mid-2023, precisely as the airline was working through its Elliott-driven transformation planning internally" — but Elliott's stake was disclosed in June 2024, a year after the use agreement. So the Regulatory brief's "working through its Elliott-driven transformation planning internally" is itself already slightly anachronistic, and the draft compounds the error.

**Recommendation:** Rewrite: "Southwest signed the agreement in mid-2023, a year before Elliott's stake became public and fifteen months before Investor Day. The airline that negotiated fixed rental rates is not the airline that emerged from the September 2024 transformation." That preserves the "one side knew more about what was coming" punch without the factually incorrect "same quarter" claim.

---

## 25. Section VI's 2031 use-agreement paragraph introduces a new implication that is under-argued.

**Location:** Section VI, "The 2031 use agreement renegotiation."

**Issue:** The paragraph is strong conceptually but makes a large claim ("The airport should start positioning for that renegotiation now") without showing the reader what that positioning looks like. The Regulatory brief specifies that the minimum gate activity recapture mechanism is contractual — that could be highlighted. The brief also notes fixed rental rates through 2031 mean MNAA cannot pass through debt service through the contract term — that is the specific financial mechanism that makes positioning urgent. The draft gestures; the brief has the specifics.

**Recommendation:** Expand by one or two sentences with specific positioning actions: calibrating gate activity thresholds on the lounge lease, sequencing rate-setting methodology discussions before bond-market windows, preserving lease-term optionality on any Concourse A Southwest-adjacent space.

---

## 26. Section VII (closing scene) reuses Gate D6 without adding new narrative weight.

**Location:** Section VII ("A few hundred yards north of Gate D6, across the apron, the concrete for the Concourse A reconstruction will be poured starting this summer.").

**Issue:** The closing scene tries to bookend Section I, but it is mostly declarative rather than observational. "Some of them will have come from a lounge upstairs. Many of them will have checked a bag." — "many" and "some" are exactly the vague quantifiers the tone rules forbid. And "The question is whether it was designed knowing what that gate would be asked to do" is the third restatement of the essay's central question in the final 200 words. The closing should do something the body did not.

**Recommendation:** Either (a) find a genuinely new observational detail to close on — something specific from one of the briefs that has not been used (the Dallas Love Field precedent from the Engineer brief, the Midway historical analog from the Historian brief, the rating agency "buffer is being consumed" language from the Regulatory brief), or (b) cut Section VII and let Section VI's "every element of that sentence is a fact already established" paragraph close the essay. Section VI's final paragraph is stronger than Section VII. Do not dilute it.

---

## 27. The draft's closing disclosure undersells the count of analyst-derived calculations.

**Location:** Final italicized note (line 224).

**Issue:** The note says "One analyst-derived calculation — the 19.5 departures per gate..." In fact the draft contains multiple analyst calculations that should be disclosed:

- "A 3-minute average increase across 166 daily Concourse D departures consumes roughly eight gate-hours per day" (Section II bullet 3). The 8-hour figure is Operations brief Key Finding 1's derivation, not a brief data point — 166 × 3 / 60 = 8.3. Analyst math.
- "$1,766 per square foot" (Section III.c). $53M / 30,000 sqft. Analyst math derived from two brief figures. The Engineer brief does this calculation explicitly; the Technology Scout gives $1,767. Minor, but it is analyst-derived and the brief's own value should be cited, not re-derived.
- The "55 basis points above covenant" phrasing (Executive Summary bullet 5). The Economist brief says 1.80x vs 1.25x floor = 0.55x margin. 55 "basis points" is the wrong unit — basis points are used for interest-rate or percentage-yield metrics; a debt service coverage ratio margin of 0.55x is 55 hundredths of a coverage ratio, not 55 basis points. The Economist brief itself says "55 basis points above covenant" — so the brief has the same error — but the Strategist should not repeat a unit mistake.
- "Approximately 22% increase in passengers per gate cycle" (Section II bullet 3, Section III.b). This is derived: 175/143 = 22.4% per the Engineer brief. Brief-supported but still a calculated ratio.

**Recommendation:** Expand the closing disclosure to list all analyst calculations, or inline-flag each as "(author calculation)" the first time it appears. On the 55-basis-points unit error, either change to "0.55x above the covenant floor" or "55 hundredths of a coverage ratio above covenant." Do not inherit the Economist brief's unit mistake.

---

## 28. Structural: Section IV is too long relative to Section V.

**Location:** Sections IV and V.

**Issue:** Section IV (the counter-case) runs roughly 1,000 words and presents the Contrarian case with generosity. Section V (the rebuttal) runs roughly 1,400 words but half of it concedes points and the specifically analytical refutation is thinner than the counter-case presentation. For a skeptical reader, this ratio is wrong. The counter-case should be presented cleanly; the rebuttal should dominate.

**Recommendation:** Tighten Section IV by about 25%. Every Contrarian argument in IV should have a one-sentence strongest-form statement, not a paragraph-long presentation. The Strategist has already made the Contrarian case as strong as the Contrarian did; there is no reason to go further. Then use the reclaimed words in V to do the specific analytical work that the current draft asserts but does not show (see items 5, 6, and 20 above).

---

## 29. Missing lens: the Airline Commercial Strategist's Delta-template compression argument is the most important one missing.

**Location:** Not in the draft.

**Issue:** The Airline brief Key Finding 6 makes the single strongest "why Southwest's transformation is high-risk" argument: "Delta's trajectory is the relevant comparison... Delta, compressing this same transformation into 15 years... Southwest is attempting to compress that same trajectory into 18-36 months, under activist pressure, with a narrowbody-only fleet, without international joint ventures, and while simultaneously managing the operational disruption of the transformation itself." The brief calls this "the core analytical uncertainty" and the "strategic risk."

The draft never engages with compression risk specifically. The Investor Day $4B EBIT / 15% ROIC targets are cited as commitments, but the analytical question — can Southwest execute in 18-36 months what took Delta 15 years? — is never asked. This is a load-bearing lens that the Airline brief surfaces and the draft skips.

**Recommendation:** Add a paragraph (ideally in Section III.a or a new sub-section before Section III.b) engaging the compression question. Short form: the transformation risk for BNA is not just that Southwest is changing, but that Southwest is changing faster than Delta or United did, without their structural advantages, under activist pressure, and while the operational changes and revenue gains arrive simultaneously rather than sequentially. If the compression fails, the cost pressure doesn't go away. The CPE trajectory at BNA becomes more binding, not less.

---

## 30. Missing lens: Continental at Denver (1995) is the single cleanest precedent for CPE-triggered hub decisions, and it is entirely absent.

**Location:** Not in the draft.

**Issue:** The Airline brief's Specific Case Studies section opens with "Continental at Denver (DIA, 1995): Denver had just completed a $4.8 billion new airport... Continental had reduced Denver from hub to spoke status, citing higher landing fees and facility costs... capital investment in airport infrastructure does not lock in carrier behavior when the carrier's cost-benefit calculation changes." The Economist brief also references Continental Denver. This is the cleanest historical precedent in the whole case library for "capital investment does not prevent cost-driven dehubbing decisions."

The draft engages with Pittsburgh, CVG, Memphis, and America West. It does not engage with Continental/Denver. This is a missed opportunity because Continental/Denver is the only case in the library where a carrier reduced service at an airport specifically because of airport costs rather than because of network consolidation — which is exactly the mechanism the draft is arguing is live at BNA via the January 2025 cost-restraint letter.

**Recommendation:** Add Continental/Denver to Section III.f or V sub-argument 6. The precedent directly supports the draft's cost-trajectory argument and undercuts the Contrarian's "dehubbing is the only historical mechanism" framing.

---

## 31. Minor factual slip: Concourse D opened at six gates, extended to eleven; draft treats this correctly but timing prose is imprecise.

**Location:** Section III.b, paragraph 1 ("Eleven gates now, after the July 2025 extension added five more at $229.6 million").

**Issue:** The Engineer brief says the Concourse D Extension was $229.6M per the Hensel Phelps contract value. The Economist brief says "$247 million contract." These two figures appear in different briefs and differ by $17.4M. The draft picks $229.6M without noting the discrepancy. The Operations brief also uses $247M.

**Recommendation:** Resolve the discrepancy — the $229.6M appears to be the Hensel Phelps contract value and $247M may include additional scope or soft costs. Flag to the Fact-checker. In prose, the cleanest move is to use the higher, more frequently cited figure with a footnote or parenthetical: "$247 million all-in ($229.6 million in the Hensel Phelps contract)."

---

## 32. "Investor Day's defensive punctuation was not an accident. 'Southwest. Even Better.'" — this rhetorical move is appealing but worth checking.

**Location:** Section III.a, paragraph 5.

**Issue:** The Airline brief uses similar framing: "The title's defensive punctuation was not accidental." The draft is following the Airline brief's lead. But "defensive punctuation" is an interpretive characterization; the period might equally have been chosen for rhythm or branding simplicity. The draft treats the interpretation as established. If a Southwest network planner reads this, they may find the psychoanalyzing of a press-release period unpersuasive.

**Recommendation:** Either cut the observation or make it explicit analytical commentary ("one could read the period as defensive punctuation"). The current prose presents it as self-evident; it isn't.

---

## 33. The "Gary Kelly... left the same day" framing is factually correct but dramatic in a way that oversells.

**Location:** Section III.a, paragraph 4 ("The long-serving Executive Chairman Gary Kelly — the carrier's institutional memory — left the same day.").

**Issue:** The Regulatory brief says "Executive Chairman Gary Kelly, the longest-serving custodian of Southwest's institutional identity, departed the same day." That is what the draft is paraphrasing. But "institutional memory" elevates Kelly beyond what the briefs establish — Kelly was CEO from 2004 to 2022, and Executive Chairman after, which is "longest-serving custodian" not the carrier's entire institutional memory. Herb Kelleher, who died in 2019, is the actual institutional-memory figure in Southwest's mythology.

**Recommendation:** Tighten to "The longest-tenured member of Southwest's senior leadership — Executive Chairman Gary Kelly — left the same day." That is accurate without over-dramatizing.

---

## 34. Executive Summary bullet 8 is phrased as a finding but reads as a research question.

**Location:** Section II, bullet 8.

**Issue:** "The uncommitted tranches of New Horizon... were scoped before the carrier's transformation. Whether their design assumptions still hold against a Southwest that turns aircraft in 49 minutes, charges for bags, stocks a lounge, and schedules connecting banks is a question the public record does not answer. That is the single most important finding of this analysis." The last sentence is doing a lot of work. The "finding" is really "there is a question and it is unanswered" — that is a diligence observation, not a finding in the traditional sense. The draft acknowledges this honestly, which is good, but the executive-summary framing elevates an unanswered question to the status of a conclusion.

**Recommendation:** Rephrase: "The single most important finding of this analysis is what the public record does not show: whether the uncommitted tranches' design assumptions were re-analyzed against the post-transformation Southwest." That is both more honest and more useful to a board reader.

---

## 35. "19.5 departures per gate per day... at 45-minute turns consumes almost all of the 16-hour operational day in gate occupancy alone."

**Location:** Section V, sub-argument 2.

**Issue:** 19.5 × 45 minutes = 877.5 minutes = 14.6 hours. A 16-hour operational day is a reasonable assumption. But 14.6 hours is 91% of 16 hours, not "almost all." More important, the 45-minute figure is Southwest's TARGET, not current — the draft has already established the current average is 49 minutes. At 49 minutes, 19.5 × 49 = 955.5 minutes = 15.9 hours = 99% of a 16-hour day, which is genuinely "almost all." The draft switches between the target and current turn times across the calculation without tracking which it is using.

**Recommendation:** Pick current (49 min) and show the math explicitly: "at 49-minute average turns, 19.5 × 49 = 955 minutes, consuming 15.9 of a 16-hour operational day per gate. Even at the target 44-minute turn, 19.5 × 44 = 858 minutes, or 14.3 hours — 89% of the operational day. The headroom is real but narrow." That also engages the Contrarian's turn-time optimism directly — if Southwest hits its target, the math works; if it does not, the math does not.

---

## 36. "The airline's 2030 operation runs 49-minute turns on 175-seat aircraft, banks four connections daily at Nashville, sends half its connecting passengers through a 30,000-square-foot lounge above the lobby, and charges $55 for a checked bag" — "half its connecting passengers" is invented.

**Location:** Section VI, final paragraph.

**Issue:** No brief supports "half its connecting passengers" will use the lounge. The Airline brief discusses lounge access as a Chase co-brand feature, not as a 50% connecting-passenger usage rate. This is an analyst estimate inserted into a sentence the Strategist is presenting as a factual projection.

**Recommendation:** Drop "sends half its connecting passengers through a..." and replace with "operates a 30,000-square-foot premium lounge above the lobby." The sentence's power is in the aggregate picture, not in any single attendance ratio.

---

## Final tally

**Invented or unsupported specifics:** 5 (items 1, 2, 3, 19, 36).
**Cherry-picked or under-caveated evidence:** 5 (items 4, 9, 13, 16, 32).
**Logical gaps or under-argued moves:** 4 (items 5, 6, 22, 34).
**Voice / flat prose / consultant tics:** 3 (items 8, 23, 26).
**Missed counter-arguments or lenses:** 4 (items 15, 20, 29, 30).
**Invented derived numbers:** 3 (items 11, 27, 35).
**Structural issues:** 2 (items 21, 28).
**Factual / attribution errors:** 4 (items 7, 10, 12, 14, 17, 24, 25, 31, 33).

(Some items sit in multiple categories; total distinct items: 36.)

**Most serious three, ranked:**

1. **Item 1 (Bill Franklin as named protagonist).** Narrative prose cannot invent or elevate named historical individuals. If the attribution is corporate-lore from southwest50.com, say so in the sentence. This is the single most damaging credibility risk in the draft for a Southwest-network-planner reader.

2. **Items 5 and 6 (Contrarian not actually defeated).** The counter-case is presented with more generosity than the rebuttal marshals specific refutation. Section V concedes and pivots rather than refutes. The Engineer brief, the Airline brief (on compression risk), and the Regulatory brief (on recapture mechanism specifics) all contain ammunition the draft does not fire.

3. **Item 27 (analyst-derived numbers underdisclosed).** The closing note acknowledges one analyst calculation. There are at least four in the draft (items 11, 27a-d, 35). A fact-checker will flag these. A skeptical board reader will notice. Disclosure is free; opacity costs credibility.

---

*Red Team critique complete. Recommendations are prescriptive. The Strategist is not required to accept all of them, but each should be explicitly addressed or consciously overridden in v2.*
