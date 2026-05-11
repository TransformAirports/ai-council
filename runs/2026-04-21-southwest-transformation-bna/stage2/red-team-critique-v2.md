# Red Team Critique: Strategist Draft v2
## Southwest Transformation at BNA — Second Round

**Draft critiqued:** `/Users/christiankessleriv/Repos/ai-council-mwaa/outputs/stage2/strategist-draft-v2.md`
**Prior critique:** `/Users/christiankessleriv/Repos/ai-council-mwaa/outputs/stage2/red-team-critique-v1.md`
**Critique version:** v2
**Date:** 2026-04-21
**Reviewer:** Red Team (skeptical senior analyst)

---

## Summary before enumeration

v2 fixes most of the v1 credibility disasters. Bill Franklin is gone. The named flight (WN 1442) is gone. The "two seconds per boarding pass" training figure is gone. The crew-base range is reconciled across briefs (650–950 instead of 650–1,300). The 19.5-departures-per-gate math error is gone. The unit mistake on "55 basis points" has been explicitly flagged. The US Airways / America West framing is appropriately caveated. Continental at Denver is now in. The Historian's "mechanical interlocking parts" phrase is used with quotes. The "55-basis-points" unit issue is called out in-text. The Chief Engineer's DEN Great Hall cautionary case appears in Section VI. The closing-disclosure paragraph lists five analyst calculations instead of one.

What v2 got wrong or introduced as new problems is narrower but real. (1) The Continental/Denver paragraph in Section V cites a case the Airline brief does contain but adds a sentence of analyst framing ("The subtler version — growth diversion at the margin, rather than full dehubbing — is available to a Southwest that wants to signal without breaking any contract") that no brief supports. (2) The 215 × 3 ÷ 60 = 10.75 gate-hour figure is arithmetically defensible but is compounded on top of an assumption (the 3-minute boarding-time delta from Southwest's 2006 test) that Southwest itself has been mitigating for 20 months, and the draft does not flag this stacking. (3) The United Club Infinite $695 figure is flagged in the handoff disclosure at the bottom but is presented in the body text (Section I, paragraph 5) as if it were known — a reader encountering the sentence has no signal that this number came from outside the brief library until they reach the italic coda. That is not transparent; it is footnoted self-exculpation. (4) Section V has grown from seven to eight sub-arguments, and at least two of them (Sixth, Seventh) now read as bulleted consultant prose with boldface leads and parallel sentence-starts — the narrative voice that was the point of the assignment is the first casualty of the expansion. (5) The Section VII close on Dallas Love Field is marginally weaker than the v1 version I am critiquing from memory — it opens with a definitional sentence ("The Dallas Love Field precedent is the quiet one") rather than a scene, and the essay ends on a restatement of the central question for what is now roughly the fourth time.

**Total issues in v2:** 22, of which 8 are material and 14 are minor or voice-level.

**Top three to fix before v3:**
1. The Continental/Denver sub-argument's analyst extrapolation (item 3 below) needs either a citation or a trim.
2. The United Club Infinite $695 figure needs a visible-in-prose flag, not a footnote-style coda (item 6).
3. Section V's expansion has flattened from narrative into boldface-led bullet prose (items 9, 10, 11). At least two sub-arguments need to be re-written in the voice the prompt specified.

**Verdict:** v2 is substantially stronger than v1 on factual integrity and materially stronger on rebuttal substance. It is marginally weaker on narrative voice, particularly in Section V and Section VII. Net: v2 is substantially stronger overall.

---

## A. Verification of v1 items (which were actually fixed, which were cosmetically fixed, which regressed)

### 1. Bill Franklin (v1 item 1). FIXED.
The name no longer appears in v2. Section III.a now attributes the 10-minute turn anonymously ("ground crew") and uses the Historian's "mechanical interlocking parts" phrase with quotes. Clean fix.

### 2. The invented opening scene (v1 item 2). MOSTLY FIXED.
WN 1442, the 5:47 block-in time, the specific departure times, the ramp lead's tablet-check, and the 44-minute ground-time specifics are gone. The scene is now framed as illustrative rather than reported: "Picture a Tuesday morning at Gate D6." Good. One residual issue: the specific description of what happens "By Group 2, the forward bin is full. Two rows of passengers who have not yet boarded will try to stow carry-ons above rows they do not sit in, walk forward against the boarding stream, and produce the bin congestion..." is presented in declarative voice as if observed. No brief establishes this specific bin-full-at-Group-2 sequence. The Technology Scout brief establishes the bin congestion phenomenon generally. The Group-2 specificity is analyst inference. Minor. Flagged below as item 12.

### 3. "Two seconds per boarding pass" (v1 item 3). FIXED.
The fabricated training-material figure is removed.

### 4. TWU grievance specifics (v1 item 4). FIXED.
v2 Section I now quotes the grievance correctly as being about crew bag stowage and distinguishes that from passenger bin congestion: "The grievance is about space. The space is the symptom." Clean.

### 5. Contrarian points 1 and 2 not actually defeated (v1 item 5). FIXED, with caveat.
v2's Section V has been expanded from seven to eight sub-arguments and the first two now engage the Contrarian directly: First argues the demand-versus-carrier-specification distinction collapses at the physical design level (good); Second argues the lounge is a proof-of-concept bet not unconditional commitment (good, and drawn from the Airline brief's own framing). These are substantively better rebuttals than v1 offered. The caveat is voice — see items 9–11 below.

### 6. III.d premature concession (v1 item 6). FIXED.
The explicit "the Contrarian brief's strongest point is correct" concession in III.d is gone from v2. Section III.e (now "The banking hub Southwest will not call a hub") ends with a cleaner setup line: "That mismatch is the banking-hub argument in its unresolved form. It is not conceded here; it is set up for the rebuttal that will arrive in Section V." That is the right structural move.

### 7. "Bill Franklin's operational miracle" framing (v1 item 7). FIXED.
Mythologizing softened. v2's III.a calls it "an operational expedient that became a cost-structure discipline," which is exactly the Historian brief's phrasing.

### 8. "Mechanical component of a machine" paraphrase (v1 item 8). FIXED.
The Historian's language is now in direct quotes with attribution.

### 9. Bag fee date sequencing (v1 item 9). FIXED.
v2 Executive Summary bullet 1 now states the two-step sequence explicitly: "$35/$45 in May 2025, rising to $45/$55 by late 2025."

### 10. "166 → 215" collapse of 190 interim (v1 item 10). FIXED.
Executive Summary bullet 2 now names all three numbers: "166 daily departures today, 190 in spring 2026, and a planned 215 by fall 2026."

### 11. "19.5 departures per gate" arithmetic error (v1 item 11). FIXED — sort of.
The 19.5 number is gone. The per-gate calculation is gone. v2 has replaced it with a different analyst calculation (166 × 3 ÷ 60 = 8.3 gate-hours; 215 × 3 ÷ 60 = 10.75). These are flagged as analyst calculations. However, see item 4 below — the 10.75 figure stacks assumptions in a way that could mislead.

### 12. Crew base range 650–1,300 (v1 item 12). FIXED.
v2 consistently uses the reconciled range: 500–700 FAs, 150–250 pilots, 650–950 combined. Executive Summary bullet 2 and Section III.e both use these numbers. Good.

### 13. BNA Vision 25% escalation context (v1 item 13). FIXED.
v2 Section III.c now says "modest by global airport-megaproject standards (Berlin Brandenburg ran triple; LAX APM is on track for roughly double)" — which is what the Economist brief supports.

### 14. "MNAA spent years trying to exit" (v1 item 14). PARTIALLY FIXED.
v2 Section III.h softens to "MNAA had sought to renegotiate it for a long time." Acceptable.

### 15. Tennessee governance retroactive / consolidation expansion (v1 item 15). FIXED.
Section III.i now includes the retroactive-unsettling language from the Regulatory brief and explicitly names the Metro Council size case consolidation. Well handled.

### 16. Debt coverage 19.11x to 1.80x, pandemic-relief effect (v1 item 16). FIXED.
Executive Summary bullet 5 and Section III.g now explicitly flag the pandemic-relief inflation of FY2024 and reframe the cleaner comparison as FY2025 5.95x vs. FY2030 1.80x. Good.

### 17. CPE 106% vs 91% framing (v1 item 17). FIXED.
Executive Summary bullet 4 and Section III.g acknowledge both framings with the base years explicit.

### 18. United Club Infinite fee loose attribution (v1 item 18). PARTIALLY FIXED — see item 6 below.
v2 adds the $695 figure, but the transparency of the citation in prose is the issue. The coda flag does not solve the problem of the body-text reader.

### 19. 25–30% carry-on-to-check behavioral assumption (v1 item 19). FIXED.
Section VI now flags this as "a rule of thumb the Engineer brief offers in its own analytic judgment, not a settled industry finding." Good fix.

### 20. Bin retrofit under-use (v1 item 20). FIXED.
Section III.f now gives the retrofit two paragraphs and notes explicitly that 30% of the fleet will not receive the larger bins and that the operational problem will persist into 2027 on those aircraft. Section V sub-argument Fourth uses it as a counter to the Contrarian's turn-time-recovery optimism.

### 21. DEN Great Hall under-use (v1 item 21). FIXED.
Section VI now includes a full paragraph on DEN Great Hall and multi-prime coordination risk, citing the Engineer brief Key Finding 7. The specific recommendation — a single point of authority for utility routing, operational impact, and change-order adjudication that does not run through three separate project teams — is the brief's actual recommendation, used correctly.

### 22. Historian's "no clean precedent" honesty (v1 item 22). FIXED.
Executive Summary bullet 7 now reads almost verbatim what the critique recommended.

### 23. Voice tics — "in this analysis," "on the ledger," "at the analytical level" (v1 item 23). MOSTLY FIXED.
"In this analysis" is gone. "On the ledger" and "at the analytical level" are gone. New tics have crept in — see items 9–11 below.

### 24. III.g "same quarter" timing error (v1 item 24). FIXED.
v2 Section III.h now correctly says "a year before Elliott Management's stake became public and fifteen months before the September 2024 Investor Day."

### 25. VI 2031 renegotiation under-argued (v1 item 25). FIXED.
Section VI now identifies the minimum gate activity mechanism, the fixed-rate pass-through constraint, and the calibration question. Specific enough.

### 26. VII closing scene vague quantifiers (v1 item 26). PARTIALLY FIXED / REGRESSED — see item 13 below.
"Many" and "some" are gone. But the Section VII close is weaker than a clean excision would have been. The Dallas Love Field scene is fine as content; the framing is flat.

### 27. Analyst-derived numbers underdisclosed (v1 item 27). FIXED.
The closing coda now lists five analyst calculations and flags the unit mismatch on 55 basis points explicitly in the body text as well. Honest disclosure.

### 28. Section IV too long relative to Section V (v1 item 28). FIXED — maybe overcorrected.
Section V is now longer than Section IV, as recommended. But the expansion has cost narrative voice (items 9–11).

### 29. Compression risk missing (v1 item 29). FIXED.
Section III.b is now titled "The compression question" and takes on the Airline brief's Key Finding 6 explicitly: Delta's 15-year trajectory vs. Southwest's 18–36-month compression, without Delta's structural advantages, under activist pressure, simultaneously rather than sequentially. This is one of v2's strongest additions.

### 30. Continental at Denver missing (v1 item 30). FIXED, but with overreach — see item 3 below.

### 31. Concourse D Extension $229.6M / $247M discrepancy (v1 item 31). FIXED.
v2 Section III.c now includes both figures and flags the delta as soft cost or non-contract scope: "$247 million all-in (within which $229.6 million is the Hensel Phelps progressive design-build contract) [the $17.4M delta is soft cost or non-contract scope]."

### 32. "Defensive punctuation" framing (v1 item 32). PARTIALLY FIXED.
The "Southwest. Even Better." defensive-punctuation observation appears to have been dropped entirely from v2. Acceptable.

### 33. Gary Kelly "institutional memory" framing (v1 item 33). FIXED.
v2 Section III.a now reads "The longest-tenured member of Southwest's senior leadership, Executive Chairman Gary Kelly, left the same day" — exactly the recommended phrasing.

### 34. Bullet 8 framed as finding vs. research question (v1 item 34). FIXED.
Executive Summary bullet 8 now reads "the single most important finding of this analysis is what the public record does not show" — exactly what was recommended.

### 35. Per-gate math (v1 item 35). OBVIATED.
The 19.5-departures-per-gate calculation that drove this item has been removed entirely. The replacement calculation has its own issues but this specific math error is gone.

### 36. "Half its connecting passengers through a lounge" (v1 item 36). FIXED.
Section VI final paragraph now reads "operates a 30,000-square-foot premium lounge above the lobby" — exactly the recommended phrasing. No invented 50% figure.

**Net on v1 items:** 30 of 36 fully fixed, 4 partially fixed or overcorrected, 2 obviated. No regressions of the specific v1 issues. The regressions are in new territory — see Section B.

---

## B. New issues introduced by the v2 revision

### 1. The Continental/Denver sub-argument contains an analyst extrapolation presented as brief finding.
**Location:** Section V, Fifth sub-argument, final paragraph.

**Issue:** The paragraph closes with: "The subtler version — growth diversion at the margin, rather than full dehubbing — is available to a Southwest that wants to signal without breaking any contract, and the letter is the early form of that signal." This is the Strategist's own construction. The Airline brief's Continental/Denver case study does not discuss "growth diversion at the margin" as a gradient of the full-dehubbing mechanism. The brief says: "capital investment in airport infrastructure does not lock in carrier behavior when the carrier's cost-benefit calculation changes." The Strategist has extended this cleanly-stated mechanism into a gradient (full dehubbing / marginal growth diversion) that the brief does not itself articulate. Not a huge stretch but not in the brief. The paragraph's first five sentences are brief-supported; the sixth and seventh are analyst synthesis presented in the same authoritative register.

**Recommendation:** Flag the gradient explicitly as analyst framing: "The Strategist's reading of the January 2025 letter is that the carrier is signaling a subtler version of the Denver mechanism — growth diversion at the margin rather than full dehubbing — though the briefs do not frame it this way." Or cut the final sentence and let the Denver case carry its own weight without the extrapolation.

### 2. The 10.75 gate-hour figure stacks the 3-minute boarding-time delta on top of itself across fleet growth.
**Location:** Section V, Third sub-argument.

**Issue:** The arithmetic is correct: 215 × 3 ÷ 60 = 10.75. The problem is the assumption being carried forward. The 3-minute delta comes from Southwest's 2006 internal testing of assigned-vs-open boarding (Operations brief, Key Finding 3). Southwest is actively mitigating against that delta with RIDS, paperless turns, larger overhead bins on 70% of the fleet, and an 8-group boarding sequence designed specifically to regularize the process. The Strategist applies the full 2006 delta to a 2026-fall departure count without adjusting for any mitigation. This is defensible but one-sided. The Contrarian's 16-aircraft turn-time-recovery argument is in part a direct offset to this same calculation, and v2 addresses it in the Fourth sub-argument — but the Third sub-argument presents 10.75 gate-hours as if the mitigation were zero. A sophisticated reader will notice the analyst is using the worst-case on the thesis side of the ledger and then treating the mitigation as a separate uncertainty on the Contrarian side of the ledger rather than netting them.

**Recommendation:** Either net them in the Third sub-argument ("at full 3-minute delta with no mitigation, the consumption is 10.75 gate-hours; at Southwest's target of 5-minute net recovery, the calculation reverses to a net gain") or acknowledge explicitly that the 10.75 figure is before any mitigation and that the Fourth sub-argument addresses the offset. Right now the two figures sit in adjacent paragraphs and point in opposite directions without being reconciled.

### 3. "Continental at Denver is the cleanest precedent" — Contrarian never engaged the case, so framing it as "the precedent the Contrarian's framing excludes" overstates the rhetorical move.
**Location:** Section V, Fifth sub-argument, opening.

**Issue:** The Contrarian brief actually names Continental at Denver by mechanism — not by name, but by effect. The Contrarian's meta-argument ("Airport capital plans should not be built around carrier product strategy") is the generalization that covers the Denver case. The Contrarian brief specifically discusses Pittsburgh, CVG, Memphis, America West — and Continental/Denver is notably absent from the Contrarian's list. But the framing "the precedent the Contrarian's framing excludes" implies an intentional exclusion by the Contrarian when in fact the Airline brief brought the case in. This is a minor characterization issue, not a factual error.

**Recommendation:** "Continental at Denver is the precedent the dehubbing analogy framework does not capture." Less rhetorically punchy but more accurate.

### 4. The "Sixth" sub-argument's tranche enumeration is accurate but reads as consultant-report prose.
**Location:** Section V, Sixth sub-argument.

**Issue:** The paragraph reads: "What remains discretionary is the Concourse A reconstruction ($855 million, 16 gates, July 2028) in its detailed design scope; the baggage handling system ($3 miles of conveyor, October 2028) in its specification for priority bag handling and post-bag-fee mix; the central ramp expansion (seven positions, September 2027) in its hookup configuration for power, data, and preconditioned air; and the Central Core Enhancement ($40 million, December 2027) in its passenger flow assumptions." This is a four-part parallel construction with the same semicolon-and-parenthetical rhythm four times. It is perfectly clear and it is also perfectly lifeless. It reads as a due-diligence memo, not as the McPhee/Lewis/Kidder narrative the prompt specifies.

**Recommendation:** Break the list. Give each project one sentence in its own voice. "The Concourse A reconstruction — 16 gates, $855 million, targeted July 2028 — is in detailed design. The baggage handling system is not yet specified for a world where Southwest charges for bags. The central ramp's hookup configuration — power, data, preconditioned air — has not been reconciled with a carrier whose aircraft now sit overnight. The Central Core Enhancement is flowing passengers through a mezzanine that is about to host a lounge." Something with rhythm.

### 5. The "Seventh" sub-argument restates the essay's thesis instead of making a new point.
**Location:** Section V, Seventh sub-argument.

**Issue:** This paragraph argues "the January 2025 cost-restraint letter is not a threat, but it is a signal that the counter-case's 'Southwest is embedding' framing does not accommodate." The argument is already made in Section III.g. Repeating it as its own sub-argument in Section V adds words without adding analytical weight. The paragraph's single new observation — that the peak debt service coverage stress (FY2030) and the use agreement expiration (June 30, 2031) are not a coincidence — is real and worth keeping, but it is one sentence, not a whole sub-argument.

**Recommendation:** Collapse Seventh into Sixth as a one-sentence addition, or fold the "FY2030 debt trough and June 2031 renewal are not a coincidence" observation into Section III.g where it naturally lives. Eight sub-arguments is already too many for Section V to carry narrative momentum; seven would be better, six better still.

### 6. The United Club Infinite $695 figure is not transparently flagged in the body text.
**Location:** Section I, paragraph 5 ("a product competing with Delta's Reserve card at $650 and United's Club Infinite tier, which retails at $695").

**Issue:** The in-text parenthetical says "[United Club Infinite annual fee — analyst cross-reference to publicly disclosed Chase card schedule, not sourced in Stage 1 briefs]." That does appear in the draft. Good. But the parenthetical is in the citation bracket, where readers consuming the essay for narrative — not for fact-check audit — will skim past it. The United $695 figure appears in the sentence as an equivalent kind of fact to the Delta $650 figure (which is in the Airline brief). A reader cannot tell, from reading the prose, that one of these numbers is brief-sourced and the other is analyst research outside the brief library.

The bigger concern: the closing coda paragraph repeats the disclosure ("The United Club Infinite card's $695 annual fee referenced in Section I is a publicly disclosed Chase product schedule figure not present in the Stage 1 briefs, flagged accordingly. The Fact-checker should verify it"). This is transparent to a fact-checker reading handoff notes. It is not transparent to the narrative reader.

**Recommendation:** Either (a) bring the disclosure into the sentence itself — "United's Club Infinite tier, which publicly lists a $695 annual fee per Chase's card schedule, a figure cited here from outside the brief library"; or (b) drop the United comparison entirely and let the Delta Reserve $650 comparison carry. Option (b) is cleaner. The three-card comparison is not load-bearing for the Oasis argument.

### 7. The Section I scene's "By Group 2, the forward bin is full" is analyst reconstruction.
**Location:** Section I, paragraph 2.

**Issue:** Declarative voice — "By Group 2, the forward bin is full. Two rows of passengers who have not yet boarded will try to stow carry-ons above rows they do not sit in, walk forward against the boarding stream, and produce the bin congestion that has plagued Southwest since the bag-fee and assigned-seat rollouts collided in mid-2025." The bin-congestion phenomenon generally is documented (Technology Scout brief). The "Group 2, forward bin full" sequence specifically is not in any brief. It is an analyst reconstruction of the phenomenon's mechanics. Not a fabrication, but not reported either.

**Recommendation:** Re-cast as mechanism rather than scene: "The bin-stow problem has a predictable geography. Forward bins fill first as boarding Groups 1 and 2 load. Later groups then walk forward through the boarding stream to stow carry-ons above rows they do not sit in. The result is the congestion that Southwest has been publicly working through since mid-2025." Slightly longer, but it is mechanism-level description instead of reported-scene voice. Or: keep the current prose and open it with a signal — "The mechanics of the bin problem, as widely reported, go roughly like this..."

### 8. "Sixteen phantom aircraft of flying through process, not concrete" is rhetorical but citation-loose.
**Location:** Section IV, "Operational changes being actively offset."

**Issue:** The phrase "Sixteen phantom aircraft of flying through process, not concrete" appears in Section IV as part of the Contrarian paraphrase, and then the Contrarian's number (16) is used in Section V Fourth sub-argument as "the sixteen-phantom-aircraft figure is real." That is accurate — both the Operations brief Key Finding 1 and the Contrarian brief Evidence section confirm it. But "phantom aircraft" is the Strategist's coinage. The briefs use "equivalent to adding 16 aircraft." A sophisticated reader may find "phantom aircraft" slightly too clever. Not wrong; just a voice judgment call.

**Recommendation:** Keep the first instance; on the second reference in Section V, say "the sixteen-aircraft-equivalent figure." Save the coinage for one appearance.

### 9. Section V's boldface sub-argument leads are consultant-report voice.
**Location:** Section V, sub-arguments First through Eighth.

**Issue:** Every one of the eight sub-arguments opens with a boldface lead sentence that summarizes the argument before the argument is made. "**First, the demand-versus-carrier-specification distinction collapses at the level of physical design.**" "**Second, the lounge is not unconditional commitment evidence. It is a proof-of-concept bet.**" "**Third, 'Southwest is adding' is not the same as 'Southwest is adding the same thing.'**" And so on, eight times. This is the formatting of a board memo, not a long-form essay. Lewis does not write this way. McPhee does not write this way. The prompt specifically bans this pattern ("no paragraph that reads as five identical declaratives in a row"; the closest cousin to five identical declarative openings is eight identical boldface-lead sub-arguments).

**Recommendation:** Remove the boldface lead-sentences. Rework at least half the sub-arguments to open in scene, observation, or specific detail. The argument of each sub-section will still be clear; the section will stop reading like a bulleted memo. Seven sub-arguments would be even better (see item 5 above).

### 10. Section V's sub-arguments all run the same rhetorical shape — concession, pivot, specific evidence, conclusion.
**Location:** Section V, throughout.

**Issue:** First: "The Contrarian is right that... But..." Second: "That is true at the direction-of-commitment level and incomplete at the type-of-commitment level..." Third: "The 190 peak-day departures rising to 215 are real. They are also..." Fourth: "The sixteen-phantom-aircraft figure is real. It is also a best case..." Fifth: "The Contrarian is right that Pittsburgh, Cincinnati, and Memphis are dehubbing stories..." Sixth: "What remains discretionary is..." Seventh: "The letter was sent by a carrier..." Eighth: "The strategist who accepts it without reservation concludes..."

Six of eight sub-arguments open with a concession-and-pivot structure. At this density, the rebuttal stops feeling like a rebuttal and starts feeling like a repeated verbal tic: "Yes, but actually..." eight times in a row. Each individual sub-argument is competent. The cumulative rhythm is enervating.

**Recommendation:** Vary the openings. Start at least two sub-arguments with a specific detail or a scene instead of a concession. Start at least one with a question. The Strategist should be unafraid to disagree with the Contrarian without first agreeing with the Contrarian.

### 11. The bolded summary before each Section V sub-argument duplicates the argument in the paragraph that follows.
**Location:** Section V.

**Issue:** Related to item 9 but distinct. The boldface lead is usually a single sentence. The paragraph that follows then says the same thing again in longer form. A reader who reads the bold lines can skip the paragraphs and miss nothing. A reader who reads the paragraphs has already seen the punch line. This structure is suited to executives scanning for decisions, not to readers following an argument.

**Recommendation:** If boldface leads remain (recommend against — see item 9), they should be scene-setting or question-raising rather than argument-summarizing. "The lounge is not unconditional commitment evidence. It is a proof-of-concept bet." is just saying the paragraph's thesis twice.

### 12. Section VII opens with a definitional sentence instead of a scene.
**Location:** Section VII, paragraph 1.

**Issue:** "The Dallas Love Field precedent is the quiet one." Then the next sentence: "Southwest controls 90% of gates there." This is definitional-first, observational-second — the opposite of the scene-in, argument-out structure the prompt specifies. The Love Field material is all brief-supported (Engineer brief); the voice is what is weak. Compare to an actual McPhee opening of a closing: there would be a specific moment, place, or image that carries the abstraction.

**Recommendation:** Open Section VII with a specific detail. "In Dallas, on Love Field's concourse, the walls begin coming down in 2027." Or "Southwest's home airport — Dallas Love Field, 90% Southwest gates — will start construction on a $1 billion terminal renovation in 2027. The walls are being pushed outward by 50 feet." Either is more scene-first than "The Dallas Love Field precedent is the quiet one."

### 13. Section VII closes on the essay's fourth restatement of the central question.
**Location:** Section VII, final two paragraphs.

**Issue:** The question "whether the Southwest arriving at each new Nashville gate in 2029 is the Southwest the gate was designed to hold, or the Southwest that will ask the gate to do a little more than it was built for" is the essay's central question. It has already been stated in Section I ("the gap between those two airlines is narrow enough to be invisible from a glance at the gate chart, and wide enough..."), in Executive Summary bullet 8, in Section III.b opening ("The Investor Day targets matter..."), and in Section VI's final paragraph ("What does each remaining New Horizon tranche look like if Southwest's 2030 operation runs 49-minute turns..."). Asking it a fifth time in Section VII, after the Love Field paragraph, is one restatement too many.

**Recommendation:** Either (a) close on Love Field itself ("What Love Field is committing to in 2027 is what Nashville quietly decided in 2017 it had already done") and stop there; or (b) cut Section VII entirely and let Section VI's Dallas-Love-Field-adjacent close carry. The essay does not need a separate Section VII coda if Section VI is doing the closing work.

### 14. The v2 close is marginally weaker than the essay's strongest available close.
**Location:** Section VII, final paragraph vs. Section VI, final paragraph.

**Issue:** The v1 critique flagged that Section VI's final paragraph (the "every element of that sentence is a fact already established" paragraph) was stronger than Section VII's close. That observation is preserved in v2. Section VI's final paragraph remains the strongest close in the essay: "The question MNAA's planners should ask at their next capital planning meeting is not 'will Southwest still be here in 2030?' That has an easy answer. The question to ask is this: 'What does each remaining New Horizon tranche look like if Southwest's 2030 operation runs 49-minute turns on 175-seat aircraft, banks four connections daily at Nashville, operates a 30,000-square-foot premium lounge above the lobby, and charges $55 for a checked bag?' Every element of that sentence is a fact already established by Southwest's own filings and operating record. None of them requires a forecast." That close defines the thesis by the post-transformation state and makes the question unanswerable only by facts. Section VII dilutes it with a second close that restates rather than extends.

**Recommendation:** Consider ending at Section VI. The Dallas Love Field material is valuable but could be moved to a single paragraph inside Section V (as a closing note on the Sixth sub-argument, "the tranches are not equally committed") or inside Section VI (as a parenthetical on the 2031 renegotiation's precedent). Reclaiming those 200 words and ending on the Section VI paragraph makes the essay stronger by subtraction.

---

## C. Voice and rhetoric issues remaining

### 15. "Concrete and drywall" and "fit inside the existing concrete" are good phrases, but the essay over-uses concrete-as-metaphor.
**Location:** Section I ("In concrete and drywall"), Section III.c ("every planning assumption embedded in that concrete"), Section V sub-argument Third ("process, not concrete"), Section VII ("The answer is in the concrete, and the concrete is still being poured"). Four instances.

**Issue:** "Concrete" as metaphor for commitment works once, maybe twice. Four appearances turns it into a motif the reader notices as a stylistic decision rather than a substantive claim. The Section VII line in particular — "The answer is in the concrete, and the concrete is still being poured" — is McPhee-ish in aspiration and self-conscious in execution.

**Recommendation:** Cut at least two of the four. The Section I "concrete and drywall" is the strongest; keep it. The Section V "process, not concrete" works as dialectic. Drop Section III.c's "embedded in that concrete" and Section VII's "the concrete is still being poured."

### 16. "Revealed-preference data point" is repeated.
**Location:** Section II bullet 4 ("the revealed-preference data point that matters"); Section III.g paragraph 1 ("That letter is the revealed-preference data point that matters most"); Section V Seventh sub-argument implicitly echoes it.

**Issue:** "Revealed-preference" is economist jargon. It appears three times in the essay. On the second appearance it reads as a tic; on the third as self-parody.

**Recommendation:** Use it once — in Section II bullet 4. Replace the Section III.g instance with plain prose: "The letter is the data point that matters most. A carrier cutting 15% of its corporate workforce and writing to its most profitable station about O&M restraint is an airline already modeling airport cost against its own cost-reduction program."

### 17. "Compression" does a lot of work in Section III.b without being fully defined in its first appearance.
**Location:** Section III.b.

**Issue:** The section is titled "The compression question" and the word "compression" appears seven times in six paragraphs. The concept is clear in context — time-compression of Delta's 15-year transformation into Southwest's 18–36 months — but a reader unfamiliar with the Airline brief's framing may not immediately grasp why "compression" rather than "acceleration" or "speed" is the right word. The first paragraph introduces the idea but does not define the term explicitly.

**Recommendation:** In the opening paragraph's second sentence, make the definition explicit: "Southwest is attempting, in 18 to 36 months, what Delta took 15 years to build — a compression ratio of roughly 8-to-1."

### 18. "The peak debt service coverage stress is FY2030. The use agreement runs to June 30, 2031. These two dates are not a coincidence."
**Location:** Section V, Seventh sub-argument, final three sentences.

**Issue:** This is a strong observation. It is also an interpretive leap the briefs do not make. The Economist brief says FY2030 is the DSC trough. The Regulatory brief says the use agreement runs through June 30, 2031. Neither brief argues these are causally linked or that Southwest signed the 2023 agreement with FY2030 in mind. The Strategist is drawing the connection. That may be correct analysis — but it should be flagged as analyst inference, not stated as established fact.

**Recommendation:** Soften to "The peak debt service coverage stress is FY2030. The use agreement runs to June 30, 2031. Whether the timing is coincidence or revealed preference is a question worth asking." Or flag explicitly: "One reading — not in the briefs, but worth naming — is that these dates are not a coincidence."

### 19. "Carrier-funded capital in airport-controlled real estate" is well phrased.
**Location:** Section I.

**Issue:** None. This is an example of the prose working. Noted for contrast against items 15–17.

---

## D. Operator verification — is it BNA/MNAA throughout, or does MWAA creep in?

### 20. The draft correctly uses BNA and MNAA throughout. No MWAA creep.
**Location:** Section VI title: "Implications for MNAA."

**Issue:** The prompt note ("this run is for BNA/MNAA, not MWAA — verify the Strategist has the right operator throughout") is satisfied. Every operator reference in the essay is to MNAA. The CLAUDE.md project context mentions MWAA as the user's day job (Christian at MWAA), but the run file is for BNA, and the essay keeps the distinction correctly.

---

## E. Remaining questions for the human reviewer

### 21. Is the $1,766/sq ft Oasis figure best-practice or inherited from the brief?
**Location:** Section III.d, paragraph 1; coda disclosure.

**Issue:** The Engineer brief computes $1,766/sq ft and the Technology Scout brief computes $1,767/sq ft. These are the same underlying arithmetic against two sources with slightly different rounding; the draft's $1,766 is brief-cited. Not an issue — flagged only because the coda mentions it as an analyst calculation when it is really a brief-stated figure.

**Recommendation:** The coda's entry (d) is correct as written; the figure is not a new analyst construction, it is the Engineer brief's own computation. The coda's careful disclosure is in fact over-disclosure on this one item. Minor.

### 22. Is the eight-boarding-group list accurate?
**Location:** Section I, paragraph 1.

**Issue:** The eight boarding groups listed in the opening scene — Business Select, Preferred, A-List Preferred, Extra Legroom, A-List, Rapid Rewards cardholders, and the last two groups including Basic fare — is presented as if authoritative. The Operations brief establishes the 8-group structure generally. The specific names of the groups (Business Select, Preferred, A-List Preferred, etc.) are from Southwest's public materials but are not quoted verbatim in any Stage 1 brief. The names are correct per Southwest's public product documentation, but the essay is reaching outside the brief library for them, as it does with the United Club Infinite fee.

**Recommendation:** Either (a) cite "per Southwest's public boarding-group documentation" in the sentence, or (b) simplify: "eight boarding groups that range from Business Select at the front to Basic fare at the back." The Fact-checker should verify the group names against Southwest's current published boarding policy.

---

## Final tally

**Items resolved from v1 (of 36):** 30 fully fixed, 4 partially fixed or acceptably resolved, 2 obviated by structural changes.
**New issues introduced in v2:** 22 total.
- Material (likely to affect a reader's confidence): 8 (items 1, 2, 6, 9, 10, 11, 12, 14).
- Moderate (voice/rhetoric drift): 8 (items 4, 5, 7, 8, 13, 15, 16, 17).
- Minor (flagging, disclosure, small inference): 6 (items 3, 18, 19, 20, 21, 22).

**Most serious three for v3:**
1. **Section V's eight boldface-led sub-arguments (items 9, 10, 11).** The expansion has flattened the essay's voice from narrative into memo. This is the single biggest regression in v2 and it is the most visible to a sophisticated reader. Target: reduce to 6 or 7 sub-arguments, cut boldface leads on at least half, vary the concession-and-pivot rhythm.
2. **The United Club Infinite $695 figure (item 6).** The handoff-note disclosure is not a substitute for in-prose transparency. Either flag in the sentence or cut the comparison.
3. **The Continental/Denver "growth diversion at the margin" extrapolation (item 1).** The Airline brief supports the mechanism; the gradient framing is analyst synthesis presented as brief finding. Trim or flag.

**Verdict:** v2 is substantially stronger than v1 on factual integrity and substantially stronger on the rebuttal section's substance. It is marginally weaker on narrative voice in Section V and Section VII. Net: substantially stronger, but with a voice regression that a voice-pass in v3 can fix without structural rework.

---

*Red Team critique v2 complete. v3 should prioritize voice restoration in Section V, the United Club Infinite disclosure, and a decision on whether Section VII stays or the essay ends at Section VI. All remaining issues are editable within a standard revision pass and none require new research.*
