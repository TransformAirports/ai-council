# Red Team Critique v2
## Of: Strategist Draft v2 — "The Cheapest Lever"
*Indoor Signage Best Practices Run | June 3, 2026*

v2 is materially better than v1. The math is now defensible. Munich is restated accurately. The opening is sharper. The Architectural Historian brief is finally load-bearing. Pittsburgh Chapter 2 is doing the work it should have been doing in v1. The Executive Summary reads as prose rather than as deck slides.

But v2 has a different set of problems. Some are inherited weaknesses the strategist defended rather than fixed. Some are new — the result of repairs that introduced their own fragility. The most serious are: a published "Revision Notes" header that breaks the essay frame, math in Section VI Observation Two that looks rigorous and isn't, an Executive Summary that converted from numbered list to prose without changing its underlying cadence, and a Section IV that still reads as bulleted counter-points with bolded openers. The thesis still holds. The execution is still vulnerable to a hostile reader on several specific moves.

---

## A. New Problems v2 Introduced

**1. The "Revision Notes (v1 → v2)" header at the top of the draft does not belong in the deliverable.**
- *Location:* Lines 11–18.
- *Issue:* This is internal process metadata — a changelog. It does not belong inside an essay any more than a track-changes pane belongs inside a published article. The reader who picks up the report cold encounters seven lines of "incorporated in full: 1, 2, 3, 5, 6, 7..." before they see the opening scene. McPhee does not publish his editorial correspondence with his fact-checker. Levine does not publish his red-line history. This block belongs in a separate v2-revision-log.md file, not at the top of the deliverable.
- *Recommendation:* Strip the entire Revision Notes block from the published draft. Keep it as a separate process artifact if the council needs the audit trail. The essay starts at "I. The Decision Point."

**2. The Section VI Observation Two math chain looks rigorous and is leaking under the surface.**
- *Location:* Section VI, "Move from study to implementation," paragraph 2.
- *Issue:* The strategist now shows the work: "Heathrow's 2013 £10 million five-year framework, inflated to 2026 at roughly 50 percent UK construction inflation, is approximately £15 million or $19 million; scaled down by MWAA's 52 million passengers against Heathrow's 80 million gives a base figure of roughly $12 million; the Chief Engineer's 40–50 percent live-terminal premium adds another $5 to $6 million; the Ontario International overrun multiplier (2.7x on a single project, properly discounted across a multi-project program) implies a $4 to $5 million contingency reserve." The math is shown. The problem is what is being multiplied. The Heathrow £10M framework was a **consultancy framework** — strategic wayfinding design services and ad hoc signage projects. It is not a hardware-and-installation number. The 40–50 percent live-terminal premium applies to construction labor working around flight operations; it does not apply to consultancy time. The Ontario overrun multiplier comes from a single $485K signage installation project where the field conditions were the cost driver. Stacking a consultancy framework figure under a construction premium and an installation overrun produces a number that looks like a derivation and is actually a category-error chain.
- *Recommendation:* Either (a) caveat explicitly that "Heathrow's £10M is a consultancy framework, not an implementation budget; this estimate combines consultancy-scaled base with implementation premiums and should be read as an order-of-magnitude range, not a derivation"; or (b) build the estimate from implementation-side comparables — Tampa, Denver, PANYNJ — and show those numbers instead. The current chain reads to a financially literate reader as if the strategist multiplied apples by oranges and reported a fruit.

**3. The Executive Summary converted from numbered list to prose without changing its rhythm.**
- *Location:* Section II, paragraphs 1–8.
- *Issue:* V1 critique #22 said "rewrite as 4–5 paragraphs of running prose with the same content." The strategist responded by stripping the numbers and the bold leads — but kept the eight discrete paragraphs, each opening with a thematic flag sentence ("The asymmetry is the first thing to see." / "The methodology exists, has existed for forty years..." / "The dynamic-versus-static debate is the wrong frame..." / "The binding constraint is governance..." / "The cost of governance failure is what the briefs collectively call..." / "Pittsburgh, 1992–2025, is the cleanest empirical demonstration..." / "Live-terminal construction premium..." / "MWAA's current allocations are study budgets..."). The numbers came off; the deck-slide rhythm did not. Eight consecutive paragraphs each leading with a thesis sentence is the prose translation of a numbered list. It reads as a translation, not as an essay.
- *Recommendation:* Compress to three or four paragraphs that flow into each other. Lose half the thesis-sentence flags. Levine doesn't preview his own section's argument before delivering it; he just delivers it.

**4. The opening line of Section II, "This is the report in miniature, for the reader who will not finish it," is a tic that signals the device.**
- *Location:* Section II, line 1.
- *Issue:* Long-form journalism does not usually announce its own executive summary. The sentence presumes a reader who is on the verge of giving up, then offers them a shortcut — which is both condescending (the reader knows they can skim) and contradictory to the rest of the report's tonal posture (that this is for sophisticated readers who will finish). McPhee opens with scene. Lewis opens with character. Gawande opens with case. None of them open with "for those of you who won't finish this."
- *Recommendation:* Cut the line. Open Section II with the asymmetry sentence directly. If the strategist wants to keep an executive summary at all, let the structure do the work.

**5. The PANYNJ implementation timeline is now told two ways that don't reconcile.**
- *Location:* Section II paragraph 4, Section III "The Governance Architecture That Actually Exists," Section V "On capital base, and on the Aicher question," and Section VI Observation One.
- *Issue:* The strategist says PANYNJ "took the better part of a decade from initiation to adoption" (Section III), that the 2021 manual "remains in prototype rollout years later" (Section II), and that "Five years from manual publication to prototype rollout across fourteen terminals is, in industry timeframes, fast" (Section V). The Regulatory brief and the Aviation Historian brief both date adoption to 2020; the Infrastructure Economist brief dates the manual to 2024. The strategist picked the framing that works at each moment — "decade-long process" when defending difficulty, "five years from manual publication" when defending speed. A reader who tracks the dates notices that the same example is being run both ways.
- *Recommendation:* Pick a single chronology. The Regulatory brief's 2020 adoption is the better-sourced date (PANYNJ's own manual carries that year). State it once: "manual published 2020, prototype rollout active at JFK five years later." Use that chronology consistently. Do not let the example shift to whatever speed the argument needs at the moment.

**6. The defense of the eighty-percent figure as "directional" still places it twice in the most visible positions in the draft.**
- *Location:* Section II paragraph 5 (parenthetical), Section III "Decision Point Is the Unit of Analysis" paragraph 3.
- *Issue:* The strategist's defense says three of four uses were cut. Counting the two that remain: one is in the Executive Summary's contradiction-debt paragraph; one is in the main body where Mollerup's nine wayfinding strategies are introduced. Both placements are load-bearing — the Executive Summary is where a board reader will first encounter the cost-of-failure framing, and the Section III placement is where the cognitive-load argument is established. The parenthetical caveat ("treat the number as directional, but the pattern is real") is the rhetorical equivalent of asking the reader to remember two things at once: the number and the discount. A skeptical reader will remember the number.
- *Recommendation:* Cut one more use. The Executive Summary should anchor on the ACI ASQ top-six finding and the ACRP 161 top-eight-gateways finding — both of which the Architectural Historian brief and Operations Analyst brief support with stronger provenance than Mappedin. Let the eighty-percent figure live in Section III with the caveat, where the reader has more context to discount it appropriately.

**7. The $700M figure is still cited twice despite v1 critique #13 saying "once at most."**
- *Location:* Section III "Contradiction Debt" paragraph 5, Section V "On digital, and the refresh discipline" paragraph 2.
- *Issue:* The Tech Scout brief calls this number not traceable and propagated without verification. The Infrastructure Economist brief flags it as vendor-sourced and Adoreboard-attributed with the original methodology not verified. The strategist now caveats it heavily — "treat as a number that exists in the industry conversation rather than as evidence" in one place, and "should be set aside" in the other — but invokes it twice. Each invocation reinforces the number. The caveat does not erase the impression.
- *Recommendation:* Pick one of the two mentions and delete the other. The Section V mention is the one that does productive work (it sets up the dwell-time elasticity as the substitute). The Section III mention is redundant. Strike it.

**8. The "single-digit to low-double-digit multiples" framing in Section V is a quiet retreat from the cost-asymmetry case the rest of the draft makes.**
- *Location:* Section V, "The cheapest-lever claim, rigorously," paragraph 2.
- *Issue:* The strategist correctly dropped "100:1 or better" in response to v1 critique #3. But the replacement framing — "single-digit to low-double-digit multiples on a ten-year horizon" — is so much weaker than what the rest of the draft implies that it undercuts the strategic claim. Section II says one to two percent of a single year's capex governs the efficiency of every square foot the program builds. Section VI's payback math implies $400,000–$875,000 annual range against $8–13M one-time spend, plus reduced customer-service load and deferred maintenance — that's roughly 6–9× on the revenue line alone over ten years before any other benefit, which fits the "single-digit to low-double-digit" claim. But the asymmetry the report sells is not "6× return"; it is "the cost of signage governs the value of everything you build." Those are two different rhetorical claims, and the math doesn't directly bridge them.
- *Recommendation:* Either own the modesty of the math explicitly ("a six-to-nine times return over ten years on the revenue line alone, before any other benefit — which is excellent in capital terms but is not the asymmetry argument") or rebuild the asymmetry framing around what signage *governs*, not what it *returns*. The current paragraph tries to do both and produces a hedge.

---

## B. Inherited Problems v2 Did Not Fix

**9. The opening scene's "buffer can collapse to negative" remains an unsourced worst-case construction.**
- *Location:* Section I, paragraph 3.
- *Issue:* V1 critique #11 said the scenario (AeroTrain to C, return, walk, wait) is overdetermined and the brief does not establish the chain as typical. The strategist's defense: "I softened the language ('can collapse to negative') and kept the scene because it is the report's hook." Fair as far as it goes, but the chain itself remains the rhetorical engine. "Can collapse to negative" is also mathematically odd — a buffer is a non-negative quantity; what the strategist means is "she's on a later flight." The hedge made the language murkier without making the empirical foundation firmer.
- *Recommendation:* If the scene stays, give it the specific consequence: "she's not on this flight." Drop "collapse to negative." If a misconnect probability for D-gate connections at IAD can be cited (United's own published rebooking rate, or an industry benchmark for misconnects at multi-mode hubs), include it. If not, accept that the scene is illustrative-fiction and frame it that way — "imagine a passenger who" — rather than "a passenger steps off."

**10. The smartphone substitution counter-argument is rebutted with eye-tracking data that does not directly support the rebuttal.**
- *Location:* Section V, "On smartphones, and what the unfamiliar passenger actually does," paragraphs 2–3.
- *Issue:* The strategist argues that "the eye-tracking evidence is not about whether passengers *can* navigate with help. It is about what they *do* under stress at decision points." The cited studies (Heathrow, Munich, the 2025 Tandfonline lab study, Shanghai Pudong) document that passengers under stress fixate on signs, exhibit reconfirmation behavior, and need text-plus-graphic formats. None of these studies includes a phone-as-alternative comparison — they did not test "do passengers look at the sign or the phone." They tested "where do passengers look at signs." The strategist is using sign-fixation data to support a claim about sign-versus-phone preference. The inference is plausible but not what the data directly shows. The Contrarian's IATA finding (78% want a single phone for the journey) is a stated preference; the strategist's response should engage that on its terms, not import an inference from a different experimental design.
- *Recommendation:* State the inferential step explicitly. "The eye-tracking studies show what passengers do *with signs* under stress; they don't directly compare phone use. But the underlying mechanism — that stressed passengers reduce cognitive load by fixating on the most immediate orientation cue — predicts sign-preference at decision points, and the high-stress moments the studies document are the same moments at which the unfamiliar passenger would otherwise need to navigate by phone." That's an honest argument. The current version reads as if the data directly proves the claim.

**11. "Structural" and "structurally" are still doing too much work.**
- *Location:* Throughout. Section I paragraph 5 ("structural case"), Section II paragraph 4 ("contractual cage is the binding constraint"), Section III "Wayshowing" paragraph 3 ("structural" appears twice), Section V "On lease structure" ("structural"), Section VI Observation Two ("structural reason"), Section VI Observation One ("structural evidence of signage fragmentation" — this is actually from Regulatory brief, fine), and several others.
- *Issue:* V1 critique #26 flagged eleven-plus uses. Quick recount in v2: at least seven. Better, but the word is still the hedge-of-choice when the strategist wants to commit without committing. "The structural case for treating wayfinding as a discipline" — meaning what? The economic case? The institutional case? "Structurally" is doing rhetorical work that a more specific word would do better.
- *Recommendation:* Strike half the remaining uses. Replace with specifics. "The cost-asymmetry case" is sharper than "the structural case." "A binding contractual constraint" is sharper than "the contractual cage is the binding constraint."

**12. Section IV's six bolded-thesis paragraphs are still a list with bold leads, not prose.**
- *Location:* Section IV, paragraphs 1–7.
- *Issue:* V1 critique #22 was about the Executive Summary's deck-slide cadence. The Executive Summary was reformatted. But Section IV — six consecutive paragraphs, each opening with a bolded thesis sentence ("The smartphone has changed..." / "Zurich's celebrated wayfinding may owe..." / "The international exemplars are capital success stories..." / etc.) — has the same problem and was not addressed. The structure mirrors the Contrarian brief's bullet points point-for-point. It reads as a transcribed counter-list, not as a counter-argument with its own narrative shape.
- *Recommendation:* Either condense to three or four counter-arguments and write them as a flowing case ("The strongest version of the counter-case combines three claims that mutually reinforce..."), or restructure as a single sustained passage with the strongest two objections doing the work. Six bolded leads in a row is a tic — and the tic the prompt explicitly told the strategist to avoid.

**13. Section V's headers are no longer parallel "What X gets right" — but they still read as section-tags rather than narrative transitions.**
- *Location:* Section V, all subsection headers.
- *Issue:* V1 critique #23 was about the parallel "What X gets right and what it misses" pattern. The strategist replaced these with "On smartphones, and what the unfamiliar passenger actually does," "On the Zurich-Google question directly," "On capital base, and on the Aicher question," etc. Better — they are no longer identically structured. But "On X" as a header pattern is still a section-tag, not a narrative transition. The substantive prose underneath each header is good. The headers themselves read as scaffolding.
- *Recommendation:* Either remove the subsection headers in Section V entirely and let the prose carry the argument (this is what Gawande does in *Being Mortal* — long passages with no internal headings), or rewrite them as scenes or specific claims rather than as topical tags ("Zurich, before Google" / "What the airport actually controls" / "The depreciation argument, friendly").

**14. The "Sign Standards Authority" recommendation in Section VI is a label, not an organizational design.**
- *Location:* Section VI, "A named owner with executive authority."
- *Issue:* "A Sign Standards Authority — one named position, reporting to a senior executive, with explicit veto authority over signage in MWAA-controlled common areas at both airports." The capitalized "Sign Standards Authority" reads as an invented title. PANYNJ's actual structure — Aviation Customer Experience in the Central Office, Program Manager for Wayfinding and Connections Solutions — is the model the strategist is recommending. Why invent a new label? Use PANYNJ's actual nomenclature, or use a descriptive phrase that doesn't read as a coined organizational unit.
- *Recommendation:* "A program manager for wayfinding, reporting to a senior executive at MWAA's central office on the PANYNJ model" is what the recommendation actually is. Strip the capitalized invented title.

**15. The eye-tracking studies are still treated as if they have higher inferential weight than their methodology supports.**
- *Location:* Section III "What Eye-Tracking Has Actually Told Us"; Section V "On smartphones."
- *Issue:* The Heathrow study had 108 participants. The Munich study covered four days. The 2025 Tandfonline lab study used 60 participants. The strategist correctly notes that Heathrow and Munich are commercial partnerships with Tobii and therefore applied research. Fine. But the strategist also writes that this is "the most rigorous source of empirical evidence on airport signage behavior available in the public literature." Two vendor-partnered studies with small participant counts and a 60-participant lab study is not what "most rigorous" would mean in academic terms — it is "the best we have," which is a much weaker claim. The eye-tracking literature is suggestive but not definitive, and the strategist's prose elevates it slightly past where it should sit.
- *Recommendation:* "The best public-domain evidence we have" rather than "the most rigorous source available." Acknowledge the n=108, n=60, four-days-of-data caveat once in Section III. The argument doesn't need the elevated framing — the data still points where the strategist says.

**16. The "less than one part in a thousand" claim is still slightly overclaimed at the upper bound.**
- *Location:* Section II paragraph 1, Section V paragraph 2.
- *Issue:* $8M / $9,000M = 0.089% (under one part in a thousand, true). $13M / $9,000M = 0.144% (above one part in a thousand by 44%). The range "eight to thirteen million dollars" therefore does not consistently support "less than one part in a thousand of the fifteen-year program." V1 critique #15 said the precise claim is what makes the argument more powerful, not less. The strategist's defense incorporated the per-year framing well — "one to two percent of a single year's MWAA capital spend" is accurate at both ends ($8M / $600M = 1.3%, $13M / $600M = 2.2%, both ≈ "one to two percent"). But the appended "less than one part in a thousand of the fifteen-year program" is not accurate at the $13M upper bound.
- *Recommendation:* Drop the "less than one part in a thousand" tail and let the "one to two percent of a single year's capex" do the work. Or rephrase as "between roughly one part in a thousand and one part in seven hundred of the fifteen-year program." The first is cleaner.

---

## C. Missed Opportunities the Strategist Could Still Capture

**17. The 30-meter continuity rule from ACRP Report 52 is not in the draft.**
- *Location:* Not used.
- *Issue:* The Operations Analyst brief and the Chief Engineer brief both cite the FAA-adopted 30-meter rule: no passenger should lose sight of a directional cue across more than 30 meters of their journey path. This is the single most testable, auditable standard in the entire ACRP 52 framework. The strategist describes the "three Cs" (continuity, connectivity, consistency) but does not give the reader the specific 30-meter number that operationalizes continuity. The Operations brief explicitly notes that "most US hub airports have not audited their signage against this standard."
- *Recommendation:* Add one sentence in Section III: "Continuity is testable at a specific number: no passenger should lose sight of a directional cue across more than thirty meters of their journey path. The standard exists in the FAA Advisory Circular. Most US hubs have never been measured against it." This converts "the standard exists" from an assertion to a fact with a number.

**18. Sign spacing empirical calibration (47m → 80%; 56m → 60%) from the Aviation Historian brief is not in the draft.**
- *Location:* Not used.
- *Issue:* The Aviation Historian's brief cites empirical research showing 80% of passenger information demand is satisfied at 47-meter spacing, 60% at 56 meters. This is a specific, calibrated number that would strengthen the "the system is testable" claim materially. The Aviation Historian explicitly notes: "Most US hub airports have not audited their signage against this standard. Most cannot, because they do not have a documented decision-point map from which spacing could be measured." This is exactly the argument the strategist is making in Section III. The supporting numbers are sitting in the brief.
- *Recommendation:* Use the 47m / 56m numbers in Section III where the testability argument is built. They are the empirical floor under the FAA's continuity rule.

**19. The "first-best is unfunded, second-best at one percent of the cost" framing in Section VI does not name the AeroTrain extension cost.**
- *Location:* Section VI, "The IAD transport-mode decision chain."
- *Issue:* "The first-best fix is extending the AeroTrain to Concourse D — United's preferred solution, a multi-hundred-million-dollar capital program, currently unfunded." A more specific number, even a range, would land harder. The Airline Commercial Strategist brief frames it as "United's preferred solution is completing the AeroTrain loop to Concourse D — a capital program estimated in the hundreds of millions." That's the same level of specificity the strategist is using; fine. But the implied ratio — "second-best at one percent of the cost" — is doing rhetorical work that a specific number would support better. $15M signage vs. $300M AeroTrain extension is 5%, not 1%.
- *Recommendation:* Either give the specific ratio ("one to five percent of the cost of the first-best, depending on assumptions about the AeroTrain extension's scope") or drop the percentage altogether and say "an order of magnitude cheaper." "One percent" is doing more rhetorical work than the math supports.

**20. The post-9/11 architectural break (Architectural Historian brief Finding 5) is not in the draft.**
- *Location:* Not in the architectural-history argument.
- *Issue:* The Architectural Historian brief's Finding 5: "The post-9/11 sterile-area boundary is an architectural condition, not merely a security procedure. It divided every terminal into two spatially distinct environments — landside and airside — with no continuous spatial logic connecting them... Passengers spend most of their time in the zone the architect spent least time designing. This is the central wayfinding crisis of the contemporary airport." This is a sharp, citable, architectural-historical observation that would strengthen the "spatial incoherence defeats sign systems" point the strategist already makes in Section V. The strategist cites the Architectural Historian brief — but not this finding.
- *Recommendation:* Add a sentence in Section V "On capital base, and on the Aicher question": "The Architectural Historian brief locates the central post-2001 wayfinding crisis precisely: passengers spend most of their time in the part of the terminal the architect spent least time designing." This sharpens the spatial-legibility argument.

---

## D. Structural

**21. The draft is now longer than v1 by the Revision Notes' own admission, and the ADA 2027 subsection arrives late in Section VI rather than driving the implications.**
- *Location:* Whole.
- *Issue:* V1 was already at the upper end of the prompt's word target. V2 added an Executive Summary paragraph (Pittsburgh), an extra Section V subsection (on the Zurich/Google question), and the ADA 2027 subsection in Section VI. The strategist names the length growth in the Revision Notes. The ADA 2027 deadline, which is the single sharpest forcing function in the entire MWAA argument — a hard regulatory deadline ten months out from the draft date — arrives as the third of five subsections in Section VI, after the more abstract governance and structuring observations.
- *Recommendation:* Lead Section VI with the ADA 2027 forcing function. It is the most specific time-bounded fact in the entire implications section. The current order ("named owner → MII structuring → ADA 2027 → IAD transport mode → validation") buries the lede. Try: "ADA 2027 → named owner → MII structuring → IAD transport mode → validation." The forcing function should drive the rest of the recommendations, not be inserted between them.

**22. The closing two paragraphs land, but the penultimate aphorism is fragile.**
- *Location:* Last two paragraphs.
- *Issue:* "The arithmetic of contradiction debt is not subtle. It compounds." V1 ended differently and V1 critique #24 flagged the "arithmetic is not subtle" tic. V2 kept one instance. It is the closing instance. Closing on the tic is more conspicuous than closing on something else. The two-word kicker "It compounds." has the rhythm of an op-ed sign-off rather than a long-form essay's resolution.
- *Recommendation:* Trust the scene. The previous sentences ("the next capital project will deposit one more layer, the next federal mandate will create one more exempt zone, and the building she walked into will become marginally harder to read than the one her predecessor walked into ten years ago") already do the work. Cut the final two sentences. End on "ten years ago."

---

## Summary

V2 fixed most of what v1 flagged. The math is mostly defensible now. Munich is honest. Pittsburgh is doing work. The Architectural Historian is in the draft.

What v2 did not fix, or made worse:

- **The Revision Notes header should not be in the published deliverable.** (#1)
- **The Section VI Observation Two math chain stacks consultancy figures under construction premiums.** (#2)
- **The Executive Summary lost the numbers but kept the cadence.** (#3)
- **Section IV is still six bolded thesis sentences in a row.** (#12)
- **The PANYNJ chronology is told two ways that don't reconcile.** (#5)
- **The 80% figure and the $700M figure are still each cited twice.** (#6, #7)
- **The 30-meter rule and the 47m/56m spacing data are still sitting in the briefs unused.** (#17, #18)
- **ADA 2027 — the sharpest forcing function in the entire argument — is in the middle of Section VI rather than at the top.** (#21)

The thesis still holds. The execution is one editing pass from publishable. Strip the Revision Notes, rebuild the Executive Summary as flowing prose, restructure Section IV as a sustained passage rather than a bullet list, fix the Section VI math chain, and reorder Section VI to lead with ADA 2027. That gets the report to the standard the prompt asked for.

*— Red Team v2*
