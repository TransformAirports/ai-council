# Red Team Critique — Strategist Draft v1

*From Compliance to Capability: A Strategic Review of the MWAA Contracting Manual*
*Adversarial QC pass. Every item numbered. No diplomacy.*

---

## Summary judgment

This is a strong draft — better sourced and better written than most. The prose has genuine McPhee texture (the 5:45 a.m. jet bridge, the carousel motor, the curb re-strip), the counter-case is steelmanned at real strength, and the citation discipline is mostly honest. **But it has one load-bearing logical crack, two overclaims that contradict the briefs' own caveats, an arithmetic error that scrambles the recommendation ranking, a propagated currency error, and at least three load-bearing brief findings it dropped.** Fix the crack (Item 1) before anything else; it threatens the spine.

---

## A. Logical gaps and the central vulnerability

**1. The thesis names two different "binding constraints" and never reconciles them. This is the single biggest vulnerability.**
- **Location:** Section I (¶3) vs. Section V, fifth point (¶109).
- **Issue:** Section I plants the flag: "MWAA's binding constraint is not what the manual forbids… The constraint is what the manual fails to measure, to presume, and to instrument." The entire clock/default/instrument argument flows from that. Then Section V concedes — quoting the procurement-expert approvingly — that "the federal review stack, **not the manual**, is the long pole," with a board-to-NTP figure of 24–48 months driven by NEPA, Section 106, and FAA concurrence. These are not the same diagnosis. If the dominant delay is the federal stack *outside* the manual, then re-instrumenting the manual's internal clock is, by the draft's own admission, optimizing the minor pole. The lead anecdote (a 9-month award) and the cycle-time crusade are about manual-internal latency; the most expensive delay is external and unfixable by manual reform. The draft gestures at reconciliation ("the manual is built for the wrong half of it") but never resolves whether cycle-time reform is actually high-leverage given the 24–48-month federal pole dominates.
- **Recommendation:** Resolve this explicitly and early. Either (a) scope the thesis honestly to "the manual governs the recoverable interval, which is a minority of total elapsed time but the only interval MWAA controls," or (b) re-rank so the FAA-chapter / federal-stack work (currently rec 13, Priority 16) rises to reflect that it addresses the actual long pole. Right now Section V quietly demolishes Section I's framing and the reader will notice.

**2. The lead anecdote carries the whole argument on n=1.**
- **Location:** Section I, ¶1.
- **Issue:** The $4.9M / 9-month award is real and checks out against the deep-research brief (issued 8/25/2025, closed 12/10/2025, awarded 5/22/2026). But it is a *single observation*, and the only other data point the deep-research brief offers is the April 2026 post-Board clustering. The draft builds "that asymmetry is the whole argument" on one procurement without noting it is one procurement. A skeptical reader (the stated audience) will ask: is this representative or cherry-picked?
- **Recommendation:** Add the April 2026 clustering (15 contracts awarded post-Board, including $6M/$4.8M/$2.5M items — deep-research brief) as corroboration so the lead rests on a pattern, not an anecdote. Or explicitly concede it is illustrative, not a dataset.

**3. The narrative reconstruction of the 9-month award is invented detail presented as fact.**
- **Location:** Section I, ¶1 ("Somewhere in that interval a proposal sat through an evaluation committee, then a consensus meeting, then reference checks, then a negotiation, then an internal approval chain, then the wait for a Board meeting").
- **Issue:** No brief documents the internal steps of *this specific* procurement. The steps are lifted from the generic EC sequence (ops-analyst §3.6.7) and projected onto the example. "Somewhere in that interval" hedges it, but a fact-checker will flag it as reconstruction dressed as reporting.
- **Recommendation:** Keep the hedge but make the inference visible — "the manual's own process implies a proposal would pass through…" rather than asserting it happened.

---

## B. Overclaims that contradict the briefs' own caveats

**4. "MWAA cannot say where it falls… because it does not track it" overclaims the operations-analyst's explicit caveat.**
- **Location:** Section II, point 2; Section III "The clock"; Section I.
- **Issue:** The operations-analyst's methodological note says plainly: the no-cycle-time-standard finding is "inferred from the *absence* of any such provision in the manual text; it should be confirmed against MWAA's internal OSCM metrics before the Strategist treats it as established fact." The manual not *mandating* a KPI does not prove OSCM doesn't *measure* cycle time internally. The draft converts "the manual is silent" into "MWAA does not track it" — a different, stronger, unverified claim — and repeats it three times.
- **Recommendation:** Soften to what's supported: "the manual sets no cycle-time standard, and no public evidence shows MWAA measures one." Flag the open question rather than asserting the negative.

**5. The federal-lease date is cherry-picked to maximize the rhetorical effect, even though disclosed.**
- **Location:** Section VI concluding vision ("$22 billion decade"), and the closing footnote.
- **Issue:** The footnote honestly flags that the ceo brief says June 2067 and the reg-political brief says a 2024 extension to ~2100, and admits "this draft uses the longer horizon to make the planning-mismatch point." Disclosure is good — but choosing the figure that best serves the argument *because* it best serves the argument is still cherry-picking. The "75-year planning horizon vs. transaction-by-transaction controls" mismatch is rhetorically juiced by the 2100 number.
- **Recommendation:** The mismatch argument survives at 2067 (still 40+ years). Either make the point at the conservative figure, or state both and note the argument holds regardless — don't lean on the more favorable number.

**6. Denver Great Hall dollar figure conflicts across briefs and the draft silently picks the bigger one.**
- **Location:** Section IV, fourth-from-last ¶ ("a $1.8 billion design-build-finance-operate-maintain concession").
- **Issue:** The chief-engineer brief says "$1.8 billion." The airport-ceo brief says "$650M+ Great Hall P3." That is a 2.7x discrepancy between two of the draft's own sources, unflagged. The $1.8B is almost certainly the full DBFOM concession value over life; $650M+ the construction scope — but the draft doesn't say so and uses the larger, more dramatic figure.
- **Recommendation:** Reconcile and footnote (DBFOM lifecycle value vs. construction value), or the fact-checker will pull the thread.

---

## C. Invented / mis-stated numbers

**7. Arithmetic error in the recommendations matrix scrambles the ranking.**
- **Location:** Section VI, medium-term table, row 6 (TCO/ops-seat/acceptance-gate).
- **Issue:** The stated formula is Priority = Impact + Innovation + (10 − Effort). Row 6 is Impact 8, Effort 3, Innovation 7 → 8 + 7 + (10−3) = **22**, not the 21 printed. This isn't cosmetic: 22 would make row 6 the **highest-priority item in the entire document**, outranking every quick win and M1 (21). The draft's narrative says the quick wins lead the agenda; the corrected math says a medium-term reform tops the list. Every other row I recomputed is correct — this is the only error, which makes it more glaring, not less.
- **Recommendation:** Fix the cell to 22 and re-examine whether the agenda's framing ("quick wins first") survives, or adjust the input scores deliberately and say so.

**8. The "thirteen months" FTA-circular gap is wrong and propagates a brief's internal inconsistency.**
- **Location:** Section II, point 6 ("superseded by 4220.1G effective January 2025 — thirteen months before this edition issued").
- **Issue:** 4220.1G effective January 2025; manual effective May 20, 2026 = **~16 months**, not thirteen. The reg-political brief is itself inconsistent (says both "more than a year" and "thirteen months"); the draft inherited the wrong one. This is precisely the kind of currency/arithmetic slip the draft mocks the manual for — embarrassing if a reviewer catches it.
- **Recommendation:** Change to "more than a year" or recompute to ~16 months.

**9. Pedantic but real: an RFP is not "worth" a dollar value.**
- **Location:** Section I, ¶1 ("a request for proposals worth about $4.9 million").
- **Issue:** The *contract* was ~$4.9M; an RFP has no intrinsic value. Minor imprecision in an opening sentence that wants to be airtight.
- **Recommendation:** "a request for proposals for work worth about $4.9 million" or "that led to a ~$4.9M award."

---

## D. Missed / dropped load-bearing findings

**10. The chief-engineer's "collaborative front end bolted onto an adversarial back end" is dropped entirely.**
- **Location:** Should appear in Section III "The default" and/or the rebuttal; currently absent.
- **Issue:** This is finding #3 *and* a verbatim pull-quote in the chief-engineer brief: the manual authorizes progressive design-build and CMAR (which require open-book trust) while the disputes chapter prohibits total-cost claims, prohibits anticipatory-profit claims, and waives jury trials — "MWAA has bolted a collaborative front end onto an adversarial back end." The draft recommends *inverting to alternative delivery as the default* (rec 8) but never notes that the claims/disputes posture actively fights that delivery model. You can't make PDB presumptive and leave the adversarial claims chapter untouched — that's an internal contradiction the chief engineer handed you and you skipped.
- **Recommendation:** Add to "The default" or to rec 8/10: re-tooling the disputes posture (or at least the ADR/DRB layer) is a precondition for the alternative-delivery default to work.

**11. Federal category management / enterprise sourcing — the slacker's strongest evidence-backed lever — is entirely missing.**
- **Location:** Should be in Section VI medium-term; absent.
- **Issue:** The slacker brief calls enterprise/strategic sourcing (federal category management: "$27.3B saved over 3 years; $16.9B cost avoidance in 2024") "the single best evidence-backed medium-term reform, stronger than any new procurement *method*." The draft has cooperative-purchasing (rec 2) but never addresses category management / strategic sourcing as an enterprise discipline. That's the highest-evidence reform in the slacker's sprint, dropped.
- **Recommendation:** Add a category-management / strategic-sourcing recommendation, or explain why it's out of scope for a manual review (it may be — but say so).

**12. De facto sole-source / OEM lock-in on airport technology is unaddressed.**
- **Location:** Should appear near the technology section (III "The instrument") or the sole-source discussion; absent.
- **Issue:** The procurement-expert (§2.6) flags that the manual's sole-source rules are disciplined on paper but silent on the *de facto* sole sources that dominate airport tech — BHS controls, CUPPS/CUTE common-use, airfield lighting controls, access control — and that the DOT IG's 2016 audit found controls failing in *documentation discipline* (24 of 34 sole-source contracts missing the required COI agreement). This is a live procurement vulnerability for the $6.99B Dulles program and it's missing.
- **Recommendation:** Add a line in "The instrument" or rec set: identify which Dulles technology procurements are already de facto sole-source before they reach an RFP "dressed as competitive."

**13. The COO's IROPS / standing-vehicle point is under-weighted.**
- **Location:** Section VI; appears only obliquely.
- **Issue:** The airport-coo brief's fourth named reform — "require standing emergency vehicles (MACCs, IDIQs, BPAs) for the systems that fail — power, snow, IT, BHS — so the urgent/critical clause is the exception, not the plan" — with Atlanta 2017 and Southwest 2022 as evidence, doesn't get its own recommendation. Rec 11 (MACC pool) is capital-program-oriented, not IROPS-oriented.
- **Recommendation:** Either add an IROPS standing-vehicle rec or fold it explicitly into rec 11/12 with the operational-continuity framing.

---

## E. Rhetorical / structural issues

**14. The 2012 scandal is explained three times, nearly verbatim.**
- **Location:** Section II point 4, Section IV opening, Section V point 1.
- **Issue:** The $200K trigger / $83.6M / "poster child for corruption" / 117-of-190 package recurs three times. Some restatement is needed (counter-case must restate to rebut), but the *facts* are re-litigated each time rather than referenced. It bloats an already long IV+V block.
- **Recommendation:** State the scandal once at full strength (Section IV), then refer back ("the 2012 controls named above") in II and V rather than re-citing the figures.

**15. Sections IV + V together dwarf the affirmative case in Section III.**
- **Location:** Sections III / IV / V proportions.
- **Issue:** The counter-case (IV, five bolded movements) plus rebuttal (V, five numbered points + conclusion) are roughly the heart of the piece, while the actual affirmative argument (III, three short sub-sections) is comparatively thin. The architecture is thesis → big antithesis → big synthesis, which is intellectually honest but leaves the reader feeling the *defense* of the idea is larger than the idea. Momentum sags in the middle of V's five-point march.
- **Recommendation:** Either tighten V from five points to three (merge the credit and out-of-scope points; they're related), or thicken III so the affirmative case carries more of its own weight before the long defensive passage.

**16. "The counter-case never mentions it" is a strawman flourish — the Strategist wrote the counter-case.**
- **Location:** Section V, fifth point, final sentence ("the counter-case never mentions it").
- **Issue:** The Strategist authored *both* the steelman (IV) and the rebuttal (V). Claiming the counter-case "never mentions" the FAA-chapter gap is rhetorical theater — you chose what went in the counter-case. It reads as scoring a point against your own setup.
- **Recommendation:** Cut the flourish. Just make the FAA-gap point on its merits.

**17. Banned word: "leverage."**
- **Location:** Section V, fourth point ("Faster, disciplined delivery is leverage MWAA can spend at the table").
- **Issue:** CLAUDE.md tone rules explicitly ban "leverage." One use here.
- **Recommendation:** "negotiating power," "a card MWAA can play," etc.

**18. The "Executive summary" is short of target and isn't actually an executive summary.**
- **Location:** Section II.
- **Issue:** The run prompt asks for a ~1,100-word executive summary. Section II reads as eight key *findings* — it never summarizes the ranked roadmap, the quick wins, or the concluding vision, which is what an exec for this audience needs from a standalone summary. It also appears short of 1,100 words.
- **Recommendation:** Extend Section II to preview the agenda (the three or four highest-priority reforms by name) and the bottom line, and check the word count against the brief.

**19. No discrete "benchmark observations" section; transportation-agency benchmarking is thin.**
- **Location:** Whole-document structure vs. success criteria.
- **Issue:** The run's success criteria list benchmarking against (a) airport authorities, (b) transportation agencies, (c) public-sector best practice, (d) P3 frameworks. Airport (San Antonio, St. Louis, Sea-Tac, LAWA, Denver) and public-sector (eVA, Tulsa) are covered; *transportation-agency* (state DOT / transit procurement reform) benchmarking is essentially absent, and the P3 benchmark leans only on Denver's failure — the LaGuardia CTB P3 (procurement-expert §2.9) is available as a counter-example and unused. Weaving benchmarks into the narrative is fine stylistically, but a skeptical reader checking the brief against deliverables will see a gap.
- **Recommendation:** Add a transportation-agency benchmark (or name the omission), and use LaGuardia CTB to balance the Denver Great Hall cautionary tale in M4.

---

## F. Smaller verification notes (fix or confirm)

**20. "$3M threshold puts the Board in the critical path of routine change orders."**
- **Location:** Section V, second point.
- **Issue:** The $3M reservation is for contract *award*; whether routine *change orders/modifications* independently trip a fresh Board vote depends on modification rules the draft doesn't cite. The chief-engineer brief supports the substance ("a large share of material change orders will clear [$3M]"; "no expedited lane for time-critical construction modifications"), but the draft states the mechanism more confidently than it shows it.
- **Recommendation:** Cite the modification mechanism or soften to "contract actions, including large modifications, that cross $3M."

**21. "Federal practice routinely takes three to six months… before the 57-day clock starts" applied to MWAA without noting MWAA isn't federal.**
- **Location:** Section III "The clock."
- **Issue:** The 3–6-month pre-solicitation figure is MITRE/federal (ops-analyst). MWAA is explicitly *not* a federal agency. Directionally fine, but applying a federal benchmark to a non-federal authority without a caveat invites the "apples to oranges" objection from the skeptical audience.
- **Recommendation:** Add a half-sentence acknowledging it's a federal proxy used for directional scale.

**22. Confirm overall word count against the 4,000–6,000 target.**
- **Location:** Whole document.
- **Issue:** I did not count, but the draft may be near or under the floor once the tables are excluded from prose. Worth a hard count.
- **Recommendation:** Verify; if light, the affirmative case in III (Item 15) is the natural place to add.

---

## What to keep (so the Strategist doesn't over-correct)

- The clock/default/instrument triad is a clean, memorable spine. Keep it — just reconcile it with Item 1.
- The Tampa $100K comparison is handled *exactly* right: used, then caveated as a single-point directional claim per the slacker's own flag. Model for the rest.
- The DBIA / eVA / vendor-ROI figures are all correctly discounted as trade-association or vendor-reported. Honest and consistent.
- Section IV is a genuinely strong steelman — it would persuade me if I hadn't read V. Don't weaken it.
- The "stop paying a conservatism tax you were never charged" framing is the sharpest line in the piece. Keep it.
