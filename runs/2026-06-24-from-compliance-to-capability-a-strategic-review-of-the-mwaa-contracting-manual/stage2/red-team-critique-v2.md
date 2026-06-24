# Red Team Critique — Strategist Draft v2

*From Compliance to Capability: A Strategic Review of the MWAA Contracting Manual*
*Second adversarial pass. Focus: what v2 did NOT fix, what it fixed only on paper, and the new weaknesses the revision introduced. No diplomacy.*

---

## Summary judgment

v2 did real work. The arithmetic error (rec 6 = 22), the currency slip ("more than a year"), the RFP-"worth" imprecision, the strawman flourish, and the banned word are all genuinely fixed. The four dropped findings — collaborative-front/adversarial-back, category management, de facto OEM lock-in, IROPS standing vehicles — are back, and the matrix math now checks out top to bottom. Good.

**But the central fix is over-engineered, and it created two new problems bigger than most of what it solved.** To close the Item-1 crack, the Strategist conceded that the manual governs "a minority of total elapsed time" — and then applied that concession globally, including to a lead exhibit (a $4.9M services award) that has no federal-review pole at all. The same re-scoping introduced a flat non-sequitur in the executive summary (the FAA chapter "addresses the delay that actually dominates" — it does not). On top of that: a new unsupported claim (LaGuardia "on time and on budget"), a reconciliation asserted as fact that no brief states (Denver), a revision-notes block that overstates its own fixes and does not belong in the deliverable, and a body that has ballooned to ~7,600 words — well past the 4,000–6,000 ceiling v1 worried it might undershoot.

Fix items 1 and 2 first. They are on the spine.

---

## A. The Item-1 crack is papered, not closed — and the patch over-concedes

**1. The "minority of total elapsed time" concession is globalized, and it guts the lead anecdote.**
- **Location:** Section I, ¶3 (the bolded scoping sentence) vs. Section I, ¶1 (the $4.9M / 9-month lead) and Section VI quick-win #1.
- **Issue:** The scoping sentence — "the manual governs the recoverable interval — a minority of total elapsed time, but the only interval MWAA controls outright" — is true for a *major Dulles capital action on new ground*, where NEPA (6–24 mo) and Section 106 (+12–24 mo) dominate the 24–48-month board-to-NTP figure [airport-procurement-expert §2.3]. It is **false for the lead exhibit.** The $4.9M, 9-month award is a services/goods buy with no environmental review; for that class the procurement gauntlet *is* essentially the whole clock, and the manual governs nearly all of the recoverable time. By stating the concession globally, the draft tells the skeptical reader: "by my own admission, my opening exhibit optimizes a minority interval." It conflates two procurement regimes — small/non-capital (manual governs ~all elapsed time) and major capital on new ground (manual governs a minority) — and applies the major-capital concession to a non-capital anecdote.
- **Recommendation:** Split the regimes explicitly. The cycle-time crusade is *strongest* on the sub-$3M, non-grant, non-capital band — exactly where the lead anecdote and the April clustering live, and exactly where the COO locates the real pain ("$350K–$3M band," the carousel motor, the curb re-strip). Reserve the "minority of total elapsed time" concession for major federally-funded capital, and say so in the same breath. Right now the concession is laundered across both and undersells the case.

**2. Section II point 7 contains a flat non-sequitur the rest of the draft knows is wrong.**
- **Location:** Section II, point 7 ("the reform that equips MWAA for the FAA half of that stack addresses the delay that actually dominates") vs. Section V, fifth point.
- **Issue:** The dominant external delays are NEPA and Section 106 — "largely outside the manual and outside MWAA's unilateral control" (Section V says this correctly). The FAA chapter the draft wants to build covers FAA *grant concurrence* (30–90 days within the procurement phase), BABA domestic-content workflows, and sole-source prior approval [airport-procurement-expert §2.1, §2.3]. Those are real, but they are **not** "the delay that actually dominates." Section V's fifth point states the honest version ("a meaningful slice of that federal stack *is* the manual's to shape"). Section II point 7 overclaims it into "the delay that actually dominates" and directly contradicts V. A reader who reads both will catch the seam.
- **Recommendation:** Rewrite II point 7 to match V: the FAA chapter shortens the *slice of the federal stack MWAA can touch* (grant concurrence, BABA, sole-source prior approval), not the dominant NEPA/106 poles. Do not let the executive summary claim more than the argument delivers.

**3. The "dominates" rhetoric and the rec-15 priority score (19) contradict each other.**
- **Location:** Section II point 7 / Section VI rec 15 (priority 19, mid-pack) / Section VI fourth observation.
- **Issue:** If the FAA chapter addresses "the delay that actually dominates," it should top the matrix, not sit at 19 tied with four other items. v1 Item 1 offered two exits — scope honestly (option a) *or* re-rank the FAA work to the top (option b). The draft took option (a) in the prose but then borrowed option (b)'s rhetoric ("addresses the delay that actually dominates," "should not stay a low-priority afterthought") without moving the score. Pick one. Either the FAA chapter is the long-pole reform (score it top, above rec 6) or it is one mid-pack structural fix (drop the "dominates" language).
- **Recommendation:** Given #2, keep rec 15 at mid-pack and strip the "dominates" framing. Consistency beats a second dramatic claim.

---

## B. New unsupported / invented content introduced in v2

**4. The LaGuardia counter-example is not in any brief — the persuasive details are invented.**
- **Location:** Section VI, M4 ("the counter-example is LaGuardia Terminal B, delivered on time and on budget under a 35-year private-lease P3").
- **Issue:** This was added to answer v1 Item 19 (balance Denver's failure with a P3 success). But the load-bearing specifics — "on time and on budget" and "35-year private-lease" — appear in **no brief**. The airport-procurement-expert brief (§2.9) cites LaGuardia CTB only as a "$4B Central Terminal B" P3, with no outcome and no lease term. The deep-research brief discusses P3 success generically (an Australian PPP study), never LaGuardia's delivery record. M4 cites "deep-research; airport-procurement-expert" — neither supports the claim. This is external knowledge smuggled in, and it is exactly what the fact-checker has veto power over.
- **Recommendation:** Cut "delivered on time and on budget under a 35-year private-lease" unless a brief substantiates it. "The Port Authority's $4B LaGuardia Central Terminal B P3" is the most the briefs support. Make the contrast on what's sourced.

**5. The Denver $650M-vs-$1.8B reconciliation is asserted as settled fact; no brief states it.**
- **Location:** Section IV ("The two figures are not in conflict: the larger is the DBFOM concession over its life, the smaller the construction scope") and the closing footnote.
- **Issue:** v1 Item 6 asked the Strategist to reconcile the 2.7x discrepancy between the chief-engineer's "$1.8 billion" and the ceo's "$650M+." The draft did — but invented the reconciliation. The chief-engineer brief calls the entire $1.8B "a design-build-finance-operate-maintain Great Hall concession"; the ceo brief says "$650M+ Great Hall P3." **Neither brief says $1.8B is the lifecycle value and $650M is the construction scope.** The split is a plausible analyst inference, but it is stated as fact ("are not in conflict") rather than as inference.
- **Recommendation:** Hedge it — "the figures most likely measure different things: the larger the DBFOM concession over its life, the smaller the construction scope" — or footnote it as analyst reconciliation, not brief-cited fact. Don't hand the fact-checker a fact that isn't in the source set.

---

## C. Revision claims that were not actually honored

**6. The revision note claims the scandal is "stated once at full strength in Section IV." It is stated at full strength twice, and the key figure three times.**
- **Location:** Revision notes (line 16) vs. Section II point 4, Section IV opening, Section V point 1.
- **Issue:** Section II point 4 carries the *full* package — "117 of 190 contracts, about $225 million... an estimated $83.6 million... poster child for corruption." Section IV restates the full package. Section V point 1 repeats "$83.6 million that never reached the Board." So the full treatment appears twice (II + IV), and $83.6M appears three times — exactly the bloat v1 Item 14 flagged. The revision note's claim that it's now "once at full strength" is **false**, and the draft's own pushback ("I kept a compact, figure-bearing version in the executive summary") is contradicted by II point 4, which is not compact — it's the whole thing.
- **Recommendation:** Either actually compress II point 4 to a one-line figure-light pointer ("the controls are scar tissue from a 2012 IG corruption finding — see Section IV"), or stop claiming the redundancy is fixed. Right now the self-report and the text disagree.

**7. The revision-notes block itself does not belong in the deliverable, and it manufactures a false record.**
- **Location:** Lines 7–22 ("Revision notes (v1 → v2)").
- **Issue:** This is process scaffolding — a changelog addressed to me, not to an airport executive. It will read as bizarre in a board-facing report, and worse, it asserts fixes that are partial (Item 14, above) or rhetorical (Item 1, which is scoped but not resolved — see Item 1 here). Leaving it in bakes an inaccurate "all 22 items addressed" claim into the document of record.
- **Recommendation:** Strip the entire block before this advances. If a change-log is wanted, it lives in a separate note to the council, not in Section 0 of the report. And don't claim "addresses all 22 items" — several are partial.

---

## D. Structural problems, including one v2 created

**8. The body blew past the word ceiling. v1 feared it was light; v2 over-corrected hard.**
- **Location:** Whole document (Section I onward ≈ 7,600 words, including tables).
- **Issue:** The success criteria target 4,000–6,000 words. The restored findings + thickened Section III + the retained five-point Section V have pushed the body ~1,600+ words over the ceiling. This is not polish — it is over the contractual limit, and the Editor will have to cut aggressively, which risks re-breaking the things v2 just fixed.
- **Recommendation:** Cut 1,500–2,000 words now, deliberately, while the Strategist controls the scalpel. Natural cuts: collapse Section V from five points to three (merge the credit point and the out-of-scope point — both resolve to "disciplined throughput is a competitiveness and credit asset"); tighten the scandal to one full statement (Item 6 above buys back ~150 words); trim the executive summary's eight findings, several of which Section III restates in full.

**9. Section V's five-point march still sags, and v2 chose not to fix it.**
- **Location:** Section V.
- **Issue:** v1 Item 15 flagged the momentum sag through five rebuttal points; the draft pushed back and thickened III instead. Fine as far as it goes, but the consequence is a piece that is now both too long (Item 8) *and* still drags through the middle. Points 2 (credit) and 4 (out-of-scope) are the merge candidates — both end at "faster, disciplined delivery is a credit/competitiveness asset."
- **Recommendation:** Merge V2 and V4. Three rebuttal points (control≠pre-approval; disciplined-throughput-is-credit-and-competitiveness; technology-sequencing) is tighter and answers every counter the steelman raised.

**10. The quick/medium/moonshot tiers fight the priority scores, and the medium table isn't sorted.**
- **Location:** Section VI tables.
- **Issue:** If "Priority" is the sort key, the tiers scramble it. M1 (21, "moonshot") outranks every medium-term reform except rec 6. Rec 6 (22, "medium") tops the whole document. And the medium table rows run 22, 20, 20, 20, 19, 19, 19, 19, 17, 19, 16 — rec 15 (19) sits *below* rec 14 (17). A skeptical reader who trusts the column will see it isn't honored and conclude the scoring is decorative.
- **Recommendation:** Either sort each table by descending priority, or add one sentence stating that the tiers reflect *effort/political-risk class*, not priority, and that priority cuts across tiers. Don't leave the column and the order contradicting each other.

**11. Rec 6's #1 ranking hangs on a soft Innovation score.**
- **Location:** Section VI rec 6 (Impact 8, Effort 3, Innovation 7 → 22) and the "A note on what the math now says" paragraph.
- **Issue:** The draft now stakes a headline ("the single highest-priority reform in the matrix") on rec 6 topping the list at 22. That margin exists only because Innovation is scored 7 — higher than the delivery-method framework (6) and the threshold re-index (5). But the COO brief calls TCO scoring and the ops seat *standard, off-the-shelf ACRP practice* (ACRP 172/252/267) — which reads more like Innovation 5 than 7. Drop Innovation to 5 and rec 6 falls to 20, tied with three others and no longer uniquely first. The "the math now says X" framing is therefore fragile: it's the Strategist's own soft input doing the work, dressed as a result.
- **Recommendation:** Either defend Innovation 7 explicitly (what's *innovative*, as opposed to merely high-value, about requiring an ops seat?), or accept that rec 6 ties at the top and stop staging it as a clean arithmetic verdict. The substantive point — fix the moment of award — survives without the manufactured #1.

**12. With the manual conceded to govern a minority of elapsed time, quick-win #1 (cycle-time KPI) needs a bridge it doesn't have.**
- **Location:** Section I ¶3 (concession) → Section VI quick-win #1 (cycle-time standard, ranked first to start).
- **Issue:** Section I concedes the recoverable interval is small; Section VI then leads the action agenda with the reform that times that small interval, with no sentence connecting the two. The reader is owed the argument: *timing the recoverable minority is the first move because it is free, it is the band where most transactions actually live (sub-$3M, non-capital), and you cannot manage what you never measure.* That bridge exists in pieces across the draft but never lands where the tension is.
- **Recommendation:** Add one connective sentence at quick-win #1 tying it to the regime split from Item 1 — the KPI governs the non-capital band where the manual owns nearly all the clock, which is most of MWAA's transaction volume.

---

## E. What v2 genuinely fixed — do not re-break these

- **Arithmetic:** every matrix row now computes correctly under Impact + Innovation + (10 − Effort). Rec 6 = 22, named as top. Verified all 20 rows.
- **Currency:** "more than a year" replaces "thirteen months." Correct and safe.
- **RFP "worth":** now "a request for proposals for work worth about $4.9 million." Fixed.
- **n=1 lead:** the April 2026 fifteen-award post-Board cluster is added and checks out against the deep-research brief. The lead now rests on a pattern.
- **Invented internal steps:** reframed as the manual's *implied* process ("the manual's own process implies the rest of the wait is spent in series"). Honest now.
- **Lease date:** the planning-horizon point is now made at the conservative 2067 figure and explicitly holds at either date. Cherry-pick neutralized.
- **Federal proxy:** the 3–6-month pre-solicitation figure now carries "a non-federal proxy, used here only for directional scale." Good.
- **Restored findings:** collaborative-front/adversarial-back (Section III + rec 10), category management (rec 13, figures match slacker), de facto OEM lock-in (Section III + rec 15), IROPS standing vehicles (rec 12). All four back and correctly sourced.
- **Strawman flourish** cut; **"leverage"** gone from the body (it survives only inside the revision-notes block, which should be deleted anyway — Item 7).

Don't sacrifice any of these to hit the word count. The cuts in Item 8 come from Section V, the scandal restatements, and the executive summary — not from the fixes above.
