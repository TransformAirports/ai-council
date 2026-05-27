# Red Team Critique v2
## Attack on Strategist Draft v2 — "The Architecture of Silence"

**Date:** 2026-05-21
**Critique target:** `outputs/stage2/strategist-draft-v2.md`
**Posture:** Adversarial. The v2 revision genuinely fixed the worst of v1 — Kansas City is gone, the invented Year 1 percentages are gone, the Munich "letter" framing is softened, the BER passenger figure is now honest. The piece reads better. But it still has new arithmetic errors, residual fabricated specifics, an opening that miscounts its own evidence, and at least three structural tics the v1 critique flagged and the revision pretended to address by reshuffling rather than rewriting.

The draft is closer to publishable than v1. It is also still not publishable.

---

## A. New problems introduced by v2

**1. Arithmetic inconsistency between Executive Summary #3 and Implications Directive #1.**
- **Location:** Executive Summary #3 vs. Implications, Directive One.
- **Issue:** Executive Summary #3 says: "widen spreads by 30–60 basis points on the next issuance — **roughly $9–18 million annually on a $1.5 billion deal**, with a 30-year tail." Implications #1 says: "a 30–60 basis point spread widening on a $1.5 billion bond issuance is **$4.5 to $9 million annually** over a 30-year tail." Both numbers cannot be right. The arithmetic is 30 bps × $1.5B = $4.5M/yr; 60 bps × $1.5B = $9M/yr. So the Implications figure ($4.5–9M) is correct and the Executive Summary figure ($9–18M) is exactly double. The Executive Summary appears to have moved a decimal or doubled the spread. A reader who reaches the Implications section will catch this. So will the fact-checker.
- **Recommendation:** Pick one. The math says $4.5–9M. Fix the Executive Summary.

**2. The opening cannot count its own warnings.**
- **Location:** Paragraph 3 of the opening; restated in The Munich Warning section.
- **Issue:** Paragraph 3 lists: Munich's warning (1) + "the warnings of three contractors" (3) + "the assessment of an outside consultant" (1) = **five** independent warnings. The sentence then calls it "**Four** independent, technically qualified warnings." The Munich Warning section repeats the error: "Munich Airport... formally communicated... Three bidders for the contract said the same thing... The independent evaluator the city hired called the plan too complex... The warning was not delivered once; it was delivered **four times by four separate parties**." That count again sums to five (Munich + 3 bidders + consultant). The math fails twice, in the most load-bearing scene of the essay. If the bidders are being collapsed into "the bidders" as a single warning, say so explicitly — but then the count is three, not four.
- **Recommendation:** Fix the count. It is either three (Munich + bidders-collective + consultant) or five (Munich + bidder + bidder + bidder + consultant). It is not four. The error is in the most heavily-leaned-on scene of the piece.

**3. MWAA-to-comparable-program math is broken.**
- **Location:** Implications, opening paragraph ("Three reasons").
- **Issue:** "Current cost estimates approach $22 billion, larger than O'Hare's $11.5 billion expansion and **within the range of JFK NTO's $9.5 billion plus JFK Terminal 6's $4.2 billion combined**." $9.5B + $4.2B = $13.7B. $22B is 60% larger than $13.7B, not "within the range of" it. The comparison is rhetorically gestural and mathematically wrong. A skeptical reader of an MWAA audience will spot it.
- **Recommendation:** Either drop the JFK comparison entirely or rewrite as "materially larger than the combined JFK programs." The piece is comparing a $22B program to a $13.7B benchmark and calling them comparable.

**4. "Eighteen terminal lifts were jammed" is too specific to be in any brief.**
- **Location:** "Six Months Was What Was Agreed," paragraph 4 (T5 opening day scene).
- **Issue:** No Stage 1 brief documents the number 18 for jammed lifts at T5. The chief-engineer brief mentions "broken lifts" without count. The infrastructure-economist mentions "broken lifts, and parking failures" without count. The Strategist appears to have imported a specific number from outside the brief base — the same failure mode v1 was attacked for with Kansas City and "Year 1 demand realization averaging 70%." If the figure has a primary source the Strategist read, it needs to be disclosed. If it does not, it needs to be cut.
- **Recommendation:** Cut or source. Fact-checker will flag this.

**5. "Baggage handlers... arrived two hours late" is also too specific.**
- **Location:** Same paragraph as item 4.
- **Issue:** The briefs document that baggage handlers could not access the staff car park. They do not document the specific "two hours late" figure. The Strategist is constructing scene detail that the brief base does not support.
- **Recommendation:** Either find the source or rewrite as "Baggage handlers could not access the staff car park; many arrived late, and ID systems did not recognize their badges" — making the imprecision honest.

**6. The Wowereit quote is unsupported and possibly attributing the wrong person.**
- **Location:** Berlin's Draughtsman, paragraph 4.
- **Issue:** "Its chairman, Klaus Wowereit, publicly acknowledged that no one on the board had been selected for construction competency." Two problems. First, no Stage 1 brief contains this quote or the substance of it attributed to Wowereit. The closest the briefs come is Prof. Genia Kostka of the Free University of Berlin (chief-engineer brief): "The supervisory board was full of politicians who had no idea how to supervise the project. They were in charge of key decisions." That is an academic, not Wowereit. Second, the regulatory-political brief specifically names **Michael Müller** as the 2015 supervisory board chairman who insisted on a 2017 opening. Wowereit was Berlin's mayor and the supervisory board chair earlier in the program — he resigned in 2013 over BER — but the briefs do not document him making this acknowledgment. This is either an unsourced quote or attributed to the wrong man.
- **Recommendation:** Either source the Wowereit quote or replace with the Kostka quote and attribute it correctly. The Strategist appears to have transposed a real characterization of the board into a fabricated direct attribution.

**7. "Carousel of CEOs" attributed to "Berlin's investigative press" — no brief supports the phrase.**
- **Location:** Berlin's Draughtsman, paragraph 5.
- **Issue:** "What Berlin's investigative press called 'a carousel of CEOs.'" No Stage 1 brief uses this phrase or attributes it to Berlin journalism. The chief-engineer brief says "Four CEOs cycled through the project between 2013 and 2017." The historian brief refers to a "carousel of CEOs between 2012 and 2016" (paraphrased). The phrase reads as Strategist coinage with a manufactured journalistic attribution. The v1 critique attacked the Strategist for inventing a Munich "letter" the briefs did not describe. The Strategist appears to have substituted one literary invention for another.
- **Recommendation:** Either find the source for "carousel of CEOs" in Berlin press, or strike the attribution and own the phrase as authorial.

**8. The FIFA World Cup framing is the Strategist's analytical reach, not a brief claim.**
- **Location:** "The Concession Trap," final paragraph on JFK NTO.
- **Issue:** "And the World Cup is sitting on the timeline. FIFA matches in June and July 2026 create exactly the political opening date that BER's supervisory board kept committing to and that the actual systems work could not meet." This is a plausible analytical inference. But no Stage 1 brief makes this connection. Operations-analyst, technology-scout, and aviation-historian all note JFK NTO's slip from summer to November 2026 — none of them tie that slip to FIFA pressure. The Strategist is asserting a causal mechanism (FIFA → political opening date pressure → testing compression) that the briefs do not document. It may be correct. It is presented as if known.
- **Recommendation:** Either source it (FIFA host city pressure on transit infrastructure is documented elsewhere, even if not in these briefs) or frame as Strategist hypothesis ("The FIFA matches in June and July 2026 sit directly on the testing window — exactly the kind of political opening-date pressure that broke BER's schedule discipline").

**9. "Changi T4 ran twenty-four months" overstates the briefs.**
- **Location:** Implications, Directive Three.
- **Issue:** "Istanbul and Changi T4 ran twenty-four months." Operations-analyst documents Istanbul's ORAT as "more than two years." For Changi T4, operations-analyst says "more than 100 trials" with "a testing program that extended across multiple months." Tech-scout brief does not give a duration figure for T4. "Multiple months" is not 24 months. The Strategist generalizes Istanbul's duration to Changi T4 without evidence.
- **Recommendation:** Separate the two: "Istanbul ran ORAT for more than two years; Changi T4 ran 100+ trials with 2,500 staff and 7,500 volunteers across multiple months." The latter is also impressive. The Strategist did not need to inflate it.

**10. "Most current US business cases — including those for the seven mega-programs now executing simultaneously — model 30-year amortization without modeling 30-year maintenance reality."**
- **Location:** The Failure Clock That Keeps Running, final paragraph.
- **Issue:** This is a sweeping factual claim about how seven specific named programs actually do their financial modeling. The chief-engineer brief argues that "lifecycle cost thinking is structurally absent from most mega-terminal business cases" — a general claim. The Strategist has narrowed this to a specific assertion about the current US wave that the briefs do not establish. No brief examines the financial models of the seven programs and confirms they omit maintenance reality.
- **Recommendation:** Soften to "Lifecycle cost thinking is structurally absent from most mega-terminal business cases, per the chief-engineer brief — and there is no public evidence that the current US wave has corrected for it." Don't claim what the briefs cannot prove.

---

## B. What the v2 revision did not fix

**11. The "Concede" tic was compressed, not eliminated.**
- **Location:** Why the Counter-Case Is Insufficient.
- **Issue:** The v1 critique flagged the six-paragraph "Concede the Nth objection..." rhythm as sermonic. The v2 compresses it to three paragraphs, each still opening with the same construction: "Concede the first objection at full strength." "Concede the second objection and adjust the argument." "Concede the third objection and recognize what it forces." The reader still feels the McKinsey scaffolding. Three "Concede X" openers in 800 words is the same rhetorical move repeated three times. Cutting from six to three reduced the duration of the irritation; it did not change the irritation's nature.
- **Recommendation:** Break the pattern. One "Concede" opener is fine. The second move should be syntactically different: a scene, a quote, an "And yet," anything that breaks the rhythm. Right now the section announces its own structure.

**12. The Executive Summary is still numbered and still pre-empts the essay.**
- **Location:** Executive Summary.
- **Issue:** The v1 critique recommended "cut the Executive Summary to four sharper points OR convert it into a 3-paragraph prose preface." V2 cut from eight points to five, which is progress on length but not on form. The summary still reads as deck slides 1 through 5. Point #1 in particular ("The four leading indicators...") is 158 words long and contains the entire sharpened thesis — which then has to be argued out from scratch in the Counter-Case section as if the reader had not just read it. A reader who reads the summary has consumed the essay's conclusions; the body becomes appendix. The v1 critique said this. V2 reshuffled rather than rebuilt.
- **Recommendation:** Convert to prose preface OR cut Points #4 and #5 (which are factual setup, not findings) into a "Context" paragraph and leave three findings.

**13. The "case-name declarative" subsection opener is still the dominant rhythm.**
- **Location:** Subsection headers throughout The Argument.
- **Issue:** V1 critique recommended at least three subsections open with scene rather than case-name declarative. V2 result, openers by section:
  - **The Munich Warning** — opens "Return to Denver." Improved.
  - **Berlin's Draughtsman** — opens with Schwarz firing scene. Improved.
  - **The American Echo** — opens "BER's business-case failure has a US precedent..." Still declarative.
  - **Six Months Was What Was Agreed** — opens "Heathrow Terminal 5 refines the argument by isolating a single failure variable. T5 cost £4.2 billion..." Still case-name declarative.
  - **The Concession Trap** — opens "Denver's Great Hall is the case where the contracting structure itself produced the institutional gap." Still declarative.
  - **The 482-Foot Walk** — opens "LaGuardia Terminal B introduces a failure mode..." Still declarative.
  - **Two Years of Trials** — opens "Istanbul Airport opened in October 2018." Still declarative.
  - **The Failure Clock That Keeps Running** — opens with abstract statement. Worst opener in the piece.
  
  Two of eight subsections open with a scene. Six of eight still announce themselves like deck slides. The v1 critique was substantive on this point; the v2 fix is cosmetic.
- **Recommendation:** Rewrite at least two more openers around a specific moment. The T5 section could open with Booker's quote. The Concession Trap could open with the August 2019 termination announcement. The 482-Foot Walk could open inside the 22-minute connecting walk itself — a passenger making the actual transit. The Failure Clock could open at a Year 12 BHS replacement decision at a real airport.

**14. The "institutional standing" thesis is restated at least six times.**
- **Location:** Throughout.
- **Issue:** "What predicts outcome is whether the institution receiving the signal has the standing to act on it." A version of this sentence appears in the opening (paragraph 6), Executive Summary #1, the close of The Munich Warning section, the close of Berlin's Draughtsman, the Counter-Case section ("the institution receiving the signal"), and the closing photograph paragraph. By the third repetition it loses force. By the sixth, the reader is being lectured. McPhee, Lewis, Gawande do not repeat their thesis as if the reader cannot hold it.
- **Recommendation:** Cut at least three of these restatements. Trust the reader to carry the thesis from one section to the next. The piece is approximately 6,500 words; it does not need a thesis reminder every 1,000 words.

**15. "The architecture of silence" is named but still mostly asserted.**
- **Location:** Title, opening, Berlin's Draughtsman.
- **Issue:** V1 critique said: stage it as a scene. V2 adds the Schwarz 90%/56% scene, which is genuinely good — that paragraph works. But the phrase is then invoked five additional times across the piece as concept rather than scene. The reader gets one scene's worth of architecture-of-silence and four invocations. The scene-to-invocation ratio is still wrong.
- **Recommendation:** One more scene. Booker's "I remember suggesting nine months, but six months was what was agreed" is already in the piece — it is itself an architecture-of-silence scene (the warning was given, recorded, and overridden). Tie that scene explicitly to the metaphor in T5 the way the Schwarz scene ties to it in BER. Two staged scenes carry the metaphor; six invocations do not.

**16. Selection bias — the contrarian's strongest objection — is still not addressed directly.**
- **Location:** The Counter-Case, Honestly Presented.
- **Issue:** The contrarian brief's most forceful argument is item #2 in its strongest-version list: "Selection bias corrupts the sample. The brief studies BER, T5, LGA, and JFK T1 — four projects that entered public consciousness as troubled. It does not study the fifty terminal programs in the same era that had identical organizational complexity and opened without triggering a CNN headline." V2 acknowledges the universality objection ("the signals appear in 91.5% of megaprojects") and uses it as the springboard for the institutional-standing reformulation. But the selection-bias objection is different and harder: the failure cases the essay studies may be the worst-of-N from a much larger N of programs with comparable governance pathology that opened acceptably. The Strategist has not engaged this. The institutional-standing reformulation is itself vulnerable to selection bias unless the success cases (Istanbul, Changi T4) and failure cases (BER, Denver) can be distinguished by something other than hindsight.
- **Recommendation:** Add a paragraph in the Counter-Case section that engages selection bias directly. The honest concession: "We are studying four publicly-known failure cases. There are many comparable programs of the same era that opened without becoming famous failures. Our case for institutional standing as the discriminating variable depends on the comparison being valid — and we have not, in this essay, proven that it is." Then argue what makes the comparison still useful despite the bias.

**17. Mirabel is still missing.**
- **Location:** Should be in the historical-arc framing or The American Echo.
- **Issue:** Aviation historian's brief presents Mirabel as "the cleanest historical case of what Bent Flyvbjerg calls 'optimism bias' in its pure form" — Canadian gateway sized for 20M, never exceeded 3M, demolished 2014. This is the purest demand-failure case in the entire brief base. V2 mentions Pittsburgh, Memphis, Cincinnati, St. Louis, and Cleveland in The American Echo. It still does not mention Mirabel. The historian's most useful single example is omitted.
- **Recommendation:** Add Mirabel to The American Echo (it is North American, not American — that is the only reason to keep the section title) or to the historical-arc paragraph in the opening. The Aerotrain section in Implications is the natural place if Mirabel is reframed as "the demand assumption that died on contact with technology change" — refueling stops obsoleted by longer-range jets, exactly the kind of business-case shock the essay argues for. Currently the historian lens is being paid for and not used.

---

## C. Cherry-picking and overreach the v2 added or left intact

**18. The Denver Great Hall section omits that the project was repackaged and is being delivered.**
- **Location:** The Concession Trap, paragraph 2.
- **Issue:** "The project was repackaged and ultimately approved at approximately $2.35 billion, with completion now scheduled for 2028 — seven years beyond the original schedule." This is technically accurate. But the chief-engineer brief notes the project is now being delivered under a different contract structure, and the failure mode the essay diagnoses (P3 mismatch with airport's operating capacity) is being actively addressed by the airport. The Strategist does not say so. The frame leaves the reader thinking Denver still has not figured this out, which is incomplete.
- **Recommendation:** One sentence acknowledging that the repackaged delivery is happening under a structure aligned with what the post-mortem recommended would be honest.

**19. The LGA "design that traded operational performance for architectural achievement" framing is sharper than the operations-analyst brief supports.**
- **Location:** The 482-Foot Walk, paragraph 2.
- **Issue:** Operations-analyst documents the 22-minute international connection, the 25% rise in transfer times, the AirTrain cancellation, the 20-minute drop-off zone waits. The brief frames these as "the landside assumption embedded in the original Terminal B business case did not survive contact with cost estimating." The Strategist's framing — "a design that traded operational performance for architectural achievement" — implies an architect-vs-operator value tradeoff that the brief does not directly establish. The brief argues the airside geometry was a real gain and the landside was a cost-estimating failure. The Strategist has converted "cost estimating failed" into "design prioritized architecture over operations." Those are different indictments.
- **Recommendation:** Either source the design-versus-operations framing (it is plausible and may be defensible from the contrarian brief, which notes LGA won architectural awards but does not say the architecture compromised operations) or soften to: "the operational performance the building enables is worse on multiple dimensions than what it replaced, and the landside assumption that would have offset that was cancelled when its cost rose 433%."

**20. The Denver $360 million was finally fixed in v2 — but the Munich Warning section still says "$33 million per month."**
- **Location:** The Munich Warning, paragraph 4.
- **Issue:** Chief-engineer brief documents the monthly operating deficit range as **$13.35 million to $18.75 million** — not $33 million per month. The opening paragraph of v2 correctly states "Monthly operating deficits ran between $13.35 million and $18.75 million." The Munich Warning section then says "delay cost the GAO measured at $33 million per month." Both numbers cannot describe the same thing. If $33M/month is meant to include all delay costs (operating deficits + lost income + alternative system spend), the math still does not work — $33M × 16 months = $528M, well above the $360M total. The figure appears unsourced or wrong.
- **Recommendation:** Either drop "$33 million per month" or source it. The brief gives a defensible monthly range, and the cumulative figure ($360M) is sourced. The Strategist is constructing a number.

**21. "Five US airports — Pittsburgh, Memphis, Cincinnati, St. Louis, and Cleveland" — claim about all five having signaled financial distress before formal dehub.**
- **Location:** The American Echo, paragraph 1.
- **Issue:** "Each of these airports had their primary carrier signal financial distress before the formal dehub announcement." Airline-commercial-strategist brief makes this claim about "the pattern across all five dehubbed airports" — so it is sourced. But the specifics are documented in the brief only for Pittsburgh (US Airways' two bankruptcies 2002–2004) and implicitly for Memphis (Northwest acquired by Delta 2008). The brief does not specifically document financial-distress signaling for CVG, STL, or CLE pre-dehub. The Strategist is generalizing from two documented cases to five.
- **Recommendation:** Either lean on the two documented cases or acknowledge that the pattern is consistent across the five without claiming each individual one signaled distress. The "each of these" construction implies a documented per-case finding that the briefs do not establish.

---

## D. Missed lenses still missing

**22. The Chief Engineer's CSPP / Part 139 lens — flagged in v1 — is still not in the piece.**
- **Location:** Should be somewhere in The Concession Trap or Implications.
- **Issue:** Chief-engineer brief presents Part 139 / CSPP as a regulatory floor: "A schedule 'optimization' made in the project office does not automatically become executable on the airfield." This is the forcing function that bounds what owners can do under schedule pressure. The lifecycle cost piece was added per v1 critique. The CSPP piece was not. It is the more useful lens for the Implications section, because it explains why MWAA cannot simply compress its construction window even if the political layer wants it to.
- **Recommendation:** Add one paragraph in The Failure Clock section or Implications #1 acknowledging that Part 139 itself imposes constraints that compression cannot overcome. Right now the essay treats schedule pressure as if it were unbounded by federal regulation.

**23. The historian's "stakes" framing (largest wave since 1989–1998) is now in Executive Summary #2 but is not load-bearing in the body.**
- **Location:** Executive Summary #2 and the opening; not developed in the body.
- **Issue:** V1 critique recommended opening or closing the essay with the historical-arc point. V2 adds it to the executive summary and the opening paragraph, but the body of the essay does not return to it. The reader is told it is the largest wave since 1989–1998, then never reminded what that earlier wave produced or what it broke. Pittsburgh appears in The American Echo. Denver is everywhere. Atlanta's international terminal — the success case from the earlier wave per the historian brief — appears nowhere. The historical arc is asserted at the front and then dropped.
- **Recommendation:** Either build a paragraph in The American Echo that puts the current wave alongside its 1989–1998 predecessor and lists what the earlier wave produced (Denver, Pittsburgh, Atlanta's international terminal, plus the demand failures like Mirabel that predated it), or move the framing to the closing photograph so it does work at the end. Right now it is throat-clearing in the executive summary.

---

## E. Structural and rhetorical

**24. The Failure Clock section is too short and entirely abstract.**
- **Location:** The Failure Clock That Keeps Running.
- **Issue:** Two paragraphs. No scene. No specific airport. Opens "There is a fifth signal the standard framework does not name, and it has nothing to do with the opening day." Closes "That is its own architecture of silence." In between: lifecycle cost percentages and an unsupported claim about US programs' financial models. This is the new section added per v1 critique #26. It reads as a bullet point inflated to a paragraph, not as a part of the essay. The point is correct and worth making. The execution is not.
- **Recommendation:** Find one airport where deferred maintenance bit at Year 10–15 and stage it. The DIA baggage system being decommissioned in 2005 after $1M/month maintenance costs is one candidate. The original LGA terminal as the case for "deferred renewal becomes mandatory replacement" is another. A specific airport, a specific year, a specific maintenance decision — then the abstraction lands.

**25. The closing photograph paragraph is now four sentences of literary reflection on a fact the piece already established.**
- **Location:** Final paragraph.
- **Issue:** V1 critique said either let the photograph end the piece or give it one more beat. V2 added several beats and ended on a thesis restatement ("The signals had arrived. The institution had not been built to act on them."). The middle sentences are good — "There was no one there to see it. Somewhere in Berlin, the planners who had committed to a 2011 opening, then 2012, then 2013, then 2014, then 2017 — the people who had received the warnings and let them pass — would have looked at that photograph and recognized something that took them nine years to admit." That sentence lands. The final two sentences ("The signals had arrived. The institution had not been built to act on them.") are the sixth restatement of the thesis. They blunt the image.
- **Recommendation:** End on "would have looked at that photograph and recognized something that took them nine years to admit." Cut the thesis-restatement coda. The image is doing the work; let it.

**26. "Italics not allowed" is not actually a rule, but the piece uses italics three times for emphasis where the sentence should carry the weight.**
- **Location:** Counter-Case ("*and* no compensating institutional check exists"; "*not* a feature lifted from..."); the body uses italics for emphasis in moments where stronger verb choice or rewrite would do the work without typographic crutches.
- **Issue:** Minor. But Lewis, McPhee, Kidder, Gawande almost never italicize for emphasis in long-form prose. Italic emphasis is a consultant tic — it tells the reader where to put the stress because the prose has not.
- **Recommendation:** Run a pass and remove italics where the sentence can be rewritten to make the emphasis structural rather than typographic.

---

## F. Bottom line for the Strategist

V2 made real progress. The Kansas City case is gone. The invented Year 1 percentages are gone. The OECD / World Bank fabrication is corrected. The BER passenger figure is now defensible. The Munich "letter" framing is honest. The Executive Summary is shorter. The Counter-Case section is no longer six stacked concessions. The Aerotrain framing acknowledges both reads. The success cases got scene-level treatment. Sean Donohue and the DFW use-and-lease example appear. Lifecycle cost made it in. The dehub pattern made it in. The regulatory chain (PFC → financing → governance) is now load-bearing.

That said, v2 introduces four new factual problems the fact-checker will flag:

- Arithmetic error in Executive Summary #3 ($9–18M should be $4.5–9M).
- Counting error in the opening paragraph (four warnings vs. five sources, repeated in Munich Warning section).
- MWAA-comparison error in Implications opening ($22B is not "within range of" $13.7B).
- $33M/month figure in Munich Warning is inconsistent with the $13.35–18.75M monthly range used in the opening.

And four new specifics that read as outside-the-brief inventions:

- "Eighteen terminal lifts were jammed."
- "Baggage handlers... arrived two hours late."
- Wowereit's "construction competency" quote (likely either fabricated or misattributed).
- "Berlin's investigative press called 'a carousel of CEOs'" — phrase has no documented source.
- The FIFA World Cup pressure causal chain.
- Changi T4's "twenty-four months" of trials.

And four structural fixes the v1 critique recommended that v2 only partially executed:

- Executive Summary is shorter but still numbered and still pre-empts the body.
- "Concede the Nth objection" rhythm compressed from six paragraphs to three, but the rhythm itself was not broken.
- Subsection openers — two of eight now open with scene; six still declare themselves like deck headers.
- The institutional-standing thesis is restated six times. It should appear twice.

The piece is closer to what the run prompt asked for. It is not yet what the run prompt asked for. Another revision is warranted before Editor handoff.

The thesis is publishable. The draft is not yet.
