# Red Team Critique — Strategist Draft v2

**Council Run:** Baggage Handling Best Practices
**Stage 2 — Red Team Critique of Strategist Draft v2**
**Date:** June 3, 2026

This is a critique of `strategist-draft-v2.md`. The Strategist responded to v1 item-by-item and pushed back on three. Some pushbacks are defensible. Others rationalize problems that are still there. And the revision introduced its own weaknesses. The job here is to find them.

The piece is closer than v1. It is not done.

---

## A. Items the Strategist Claimed to Fix But Did Not Fully Fix

**A1. The Revision Notes preamble has become the new opening.**
Location: Lines 9–23 (top of document).
Issue: The first thing the reader sees is a meta-commentary block titled "Revision Notes" that catalogues which Red Team items were addressed and which were rejected. This is editorial scaffolding addressed to the Red Team, not the reader. McPhee does not open a piece with a memo to his editor. The Heathrow scene, which was the strongest part of v1, no longer comes first — it is buried under a block of bureaucratic self-justification.
Recommendation: Strip the Revision Notes entirely. They belong in a cover letter to the Council, not in the manuscript. The piece should begin with "Early on the morning of March 27, 2008..."

**A2. The Executive Summary is still board-deck voice, just without the bolding.**
Location: Section II, lines 43–61.
Issue: The Strategist accepted v1 item A.22 partially — dropped the bolded sub-headers — but kept eight numbered paragraphs of ~100 words each totalling roughly 1,200 words of upfront recap. The Strategist's defense ("the orchestration prompt explicitly specifies 5–8 numbered claims") punts the actual problem: the *length* and *density* of the claims, not their existence. Five-to-eight numbered claims can fit in 300 words. They do not have to be 8 mini-paragraphs that summarize every section that follows. The current version still kills momentum after a strong opening scene.
Recommendation: Compress to half the current length. Each claim becomes 25–50 words, not 100–180. The prompt asks for claims; it does not ask for advance-paragraphs of the argument.

**A3. The Vaughan/normalization-of-deviance frame is named but then over-explained.**
Location: Section III, paragraph beginning "There is a name for the institutional pattern..." (line 81).
Issue: v1 item A.19 recommended using the frame to *replace* several paragraphs of structural argument with one well-placed comparison. The v2 names Vaughan, then proceeds with 90+ words defining normalization of deviance ("An organization repeatedly accepts a signal that something is off — a warning from the engineers, a missed milestone, a degraded test result — and treats the acceptance as evidence that the deviation is tolerable. With each acceptance, the next acceptance is easier..."). This is the very expository tic Vaughan's frame was supposed to compress. McPhee's reader can be trusted to either know Challenger or to look it up.
Recommendation: One sentence on the frame, one specific Challenger detail (the O-ring engineers were on record, the launch happened anyway), and trust the reader. The current 200-word block is doing the opposite of what the frame was for.

**A4. Section VI is still a list of seven bolded subsections.**
Location: Section VI throughout.
Issue: The Strategist claimed to "cut two subsections" in response to v1 item A.36. The text counts: bond schedule pressure, contractual testing protection, architecture, EBS, three-party gap, constructability, governance gate. Seven bolded subsections. The Strategist folded cybersecurity into the architecture paragraph and the federal funding window into the schedule paragraph — but the subsection count and the cadence are unchanged. The "Picture the conditions of an early-morning planning meeting in the next quarter" line is the lone attempt to vary opening cadence; it lands as contrived ("Picture the conditions of..." is a writing-school cliché). Every other subsection opens with the same noun-verb declarative cadence v1 critique flagged.
Recommendation: Two options. Either reduce to three subsections (the Strategist's pushback notwithstanding — the audience makes better decisions on three well-developed implications than seven listed ones), or genuinely vary the cadence: open one with a specific person, one with a number, one with a piece of dialogue from the use agreement. "Picture the conditions of..." is not varied cadence; it is one cliché trying to substitute for another.

**A5. The Hong Kong anniversary framing is technically corrected but reads worse than v1.**
Location: Section III, paragraph on HKG (line 75) and Section I (line 35).
Issue: v1 said HKG opened "on the first anniversary of the territory's handover" (factually wrong). v2 says "on a politically immovable timetable set around the territory's handover anniversary five days earlier." The "five days earlier" attaches grammatically to "anniversary," not to the opening, so the reader parses this as "the handover anniversary [which occurred] five days earlier" — meaning five days before the opening on July 6, 1998, which would put the anniversary on July 1, 1998 (correct). But the reading is hostile. A reader who does not stop to do the math will think "the handover happened five days earlier" — which is wrong (handover was 1997). The correction has produced a sentence that requires close reading to parse correctly.
Recommendation: Rewrite plainly. "Hong Kong's Chek Lap Kok opened July 6, 1998, five days after the first anniversary of the territory's handover to the People's Republic, on a calendar the political authorities had set and the engineering schedule could not catch."

**A6. The chiastic closes were not actually cut.**
Location: Section VII Coda, final paragraph (line 215).
Issue: v1 item A.32 flagged closing chiasmus as overused. v2 ends with: "It is the difference between Munich and Denver, between Changi and Heathrow, between the building that opens on time with bags moving and the one whose name becomes a case study. The capital is the easy part. The capital is approved. The discipline that decides what the capital buys is the variable still in play." That is one chiastic structure ("between X and Y, between W and Z, between A and B") followed immediately by three identical-shape declaratives ("The capital is X. The capital is Y. The discipline... is Z"). Both are exactly the cadences v1 flagged. The Strategist's claim in the Revision Notes that chiastic closes were "cut" is not borne out by the actual text.
Recommendation: The penultimate paragraph (lines 213–214 — "At Dulles, the morning that matters has not arrived yet... rooms that do not yet contain the operator who will inherit the consequence") is the strongest closing in the draft. End there. Cut the final paragraph entirely. Or if it must stay, replace the three "The capital is..." lines with one sentence that does the same work without the McKinsey cadence.

**A7. "As the X brief notes" was removed, but the substitute is worse in one place.**
Location: Section III, line 83.
Issue: The line "This is what an org chart looks like when nobody owns the operational mission across the boundary between commissioning and live operations — a point this report develops at length in the section on three-party accountability below." The "a point this report develops at length in the section on... below" is the report-on-itself voice the prompt explicitly bans. It is the same family of consultant-tic as "as the X brief notes." It signals the writer thinking about the writer's outline.
Recommendation: Cut the back-reference. The reader will encounter the three-party argument when they get to it. They do not need to be told it is coming.

---

## B. New Problems Introduced by the Revision

**B1. The Denver delay-cost breakdown looks precise but it contradicts other briefs.**
Location: Section III, paragraph 71 ("approximately $360 million in direct delay costs: $230 million in operating deficits, $37 million in foregone income, $86 million for the parallel conventional system Denver had to build as a backup, and $8.3 million in emergency bond issuance fees.").
Issue: These four numbers come from the Chief Engineer brief (it cites them to GAO RCED-95-35BR). They are sourced. The problem is that two other briefs cite the parallel conventional system at $51 million, not $86 million (Operations Analyst, Regulatory & Political). The Strategist picked the higher number without flagging the inter-brief inconsistency. This is the same pattern v1 critique A.8 flagged for the Denver total: silent selection from inconsistent briefs. The Strategist fixed the *total* per v1 A.8 by showing the $520–600M range — and then immediately repeated the underlying behavior on the line-item breakdown.
Recommendation: Either flag the inconsistency (Chief Engineer cites GAO at $86M for the parallel system; Operations Analyst and Regulatory cite $51M for the manual backup), or pick the most defensible figure and note the range. Do not present a number that two other briefs contradict without acknowledgment.

**B2. The Munich-Denver warning year (1992) is invented.**
Location: Section II point 5 (line 55) and Section III paragraph on Denver (line 71).
Issue: "Munich Airport advised Denver in 1992 that a system Munich had taken two years to build and six months of 24/7 to test could not be safely commissioned in Denver's compressed schedule." None of the briefs put a year on the Munich-Denver communication. The Aviation Historian brief says only "When Munich airport authorities warned that [Denver's] approach was destined to fail" — undated. The Operations Analyst brief says the same. The 1992 date is plausible (BAE was contracted that year) but it is the Strategist's reconstruction, not the briefs'. The pattern matches v1 item A.2 (the invented 4:30 a.m. time) which the Strategist fixed — but reintroduced the same problem in a different specific.
Recommendation: Either source the 1992 date or strip it. "A delegation from Munich Airport... told the city the schedule was a fantasy" reads fine without the year. If a year is wanted, "early in the project" or "during the design phase."

**B3. The "transatlantic bags carry the highest direct liability exposure" claim is wrong on its face.**
Location: Section II point 7 (line 59).
Issue: "Connecting transatlantic bags carry the highest direct liability exposure in the U.S. industry — Montreal Convention caps near $2,175 per passenger, plus rebooking and reputational costs." The Airline Strategist brief documents the statutory caps: domestic flights covered to $4,700 per passenger; Montreal Convention international caps at ~$2,175. So per-passenger statutory exposure is *higher* on domestic flights, not international. The Strategist's framing inverts the cap relationship. The legitimate point — that international connection bags carry higher *practical* cost because re-accommodation is on an expensive international ticket and the loyalty damage falls on premium customers — is not made; it is left for the reader to construct.
Recommendation: Rewrite. "Connecting transatlantic bags carry exposure that is small per-bag at law but large in practice: the Montreal Convention cap of ~$2,175 per passenger is below domestic exposure, but a missed international connection compounds with re-accommodation on an expensive ticket and reputational damage to United's highest-margin customers." Or drop the "highest direct liability exposure" framing.

**B4. The "$5.5 billion in new bonds" and "$6.99 billion IAD program" coexist in the same paragraph without a bridge.**
Location: Section II point 7 (line 59) and Section II point 8 (line 61).
Issue: Point 7 cites $5.5B in new bonds through 2028. Point 8 cites the $6.99B IAD program. These are different things (the bonds are the funding mechanism for a subset of the program; the program also includes grants, PFC, and prior funding). A reader who tries to reconcile them will be confused. Section VI repeats both numbers and adds "$5.5 billion in new bonds through 2028" while also saying "MWAA's $6.99 billion IAD program" and "$9 billion-plus capital program" without explaining how they relate.
Recommendation: One paragraph somewhere — Section II or Section VI — that lays out the funding stack: $9.4B total MWAA program ($6.99B IAD + $2.39B DCA), of which $5.5B is new bond issuance through 2028, with the remainder coming from prior bonds, PFC, AIP, and BIL/ATP grants. Without that frame, the numbers float.

**B5. The logical sequence in Section II point 7 is broken.**
Location: Section II point 7, last three sentences.
Issue: "A BHS commissioning failure at Concourse E does not first hit MWAA's income statement; it hits United's, the same way T5 first hit BA's. The carrier's commercial pressure to open Concourse E early is the most predictable risk in the program." If the carrier bears the first-order cost of failure, why would the carrier pressure for an early opening? The Airline Strategist brief addresses this — the carrier's business case for the facility depends on occupying it, and the cost of *not opening* (delay penalties, foregone revenue, network plan disruption) is more visible to the carrier than the probabilistic cost of opening with a system that may fail. But the Strategist's paragraph asserts both facts and lets them contradict each other.
Recommendation: Bridge the logic. The carrier bears the failure cost *if* the system fails, which it might. The carrier bears the delay cost *certainly* if the opening slips. The certain visible cost dominates the probabilistic invisible one. This is the actual mechanism. Write it.

**B6. The Pittsburgh comparison is now in the draft but is not load-bearing.**
Location: Section IV, point 9 (line 155); Section V, concession block (line 171).
Issue: v1 item A.18 recommended Pittsburgh as a calibration warning that deepens the implications section. The Strategist incorporated it in Section IV as counter-argument 9 and conceded it in Section V — but stopped there. The implications section (VI) does not return to Pittsburgh at the point where the schematic-design recommendations are made. The lesson "design for carrier-agnostic flexibility because the dominant hub carrier of 2026 may not be the dominant hub carrier of 2050" appears in Section V (line 171) and then disappears. Section VI's EBS-sized-for-flow and three-party-ownership-gap recommendations could carry the Pittsburgh lesson forward but do not name it. The case is included; it is not made load-bearing.
Recommendation: In Section VI, the EBS paragraph or the three-party paragraph should explicitly reference Pittsburgh as the reason flow-sized EBS matters more than a network-specific BHS — because the network might change.

**B7. "Honestly Presented" and "honest accounting" are defensive qualifiers.**
Location: Section IV title (line 135) and Section V opening (line 161, 163).
Issue: Section IV is titled "The Counter-Case, Honestly Presented." Section V opens "Some of those counter-arguments are genuinely conceded. Some are dissolved. The honest accounting is worth setting out plainly..." Section IV closes "These objections deserve to be taken seriously. The next section does so honestly." Three instances of "honest/honestly" in close range. Each is the Strategist reassuring the reader that *this* counter-case treatment is on the level. The reader notices: why does the writer need to insist on honesty? In a piece that argued in v1's voice without these qualifiers, their introduction in v2 weakens rather than strengthens.
Recommendation: Cut all three "honest/honestly" qualifiers. Let the substance demonstrate honesty. Naming it performs it; performing it undermines it.

**B8. The "Picture the conditions of an early-morning planning meeting" scene is invented and weak.**
Location: Section VI, paragraph on architecture (line 195).
Issue: "Picture the conditions of an early-morning planning meeting in the next quarter: a schematic-design package on the table, a tunnel section showing the new dedicated baggage runs between the Main Terminal and the concourses, a vendor presentation queued for after lunch." This is an attempt to break the "noun-phrase declarative" cadence of Section VI's openers per v1 item A.28. It does not land. The scene is generic ("an early-morning planning meeting," "a schematic-design package," "a vendor presentation queued for after lunch") — there is no specific person, no specific room, no specific decision. McPhee would have a name, a location, an artifact. The Strategist invented a scene rather than reporting one. The "picture this" framing signals the gap.
Recommendation: Either find a specific real moment to anchor — a date the schematic-design package was discussed, a person who is presenting, a number on a slide — or cut the scene-setting attempt and just make the architectural argument. A bad scene is worse than no scene.

**B9. The "five days" reference in the HKG paragraph repeats inside the same sentence.**
Location: Section III, line 75.
Issue: "Hong Kong's Chek Lap Kok opened July 6, 1998, on a politically immovable timetable set around the territory's handover anniversary five days earlier." Then later in the same paragraph: "The systems worked individually. They had not been tested together under real operational load. They had not been tested together because there was no time, because the calendar had decided that early July would happen no matter what the calendar of testing said." The "calendar" repetition is intentional (it is the rhetorical figure). The "five days" reference is at the start of the paragraph and goes unused. The paragraph would land harder if the "five days" framing were either built into the rhetorical move or removed.
Recommendation: Either work the five-day gap into the narrative ("five days between the anniversary the politicians wanted to mark and the morning the engineers were trying to delay") or drop it.

**B10. The Berlin Brandenburg paragraph attributes the engineer's credential issue but inverts the smoke-extraction claim.**
Location: Section III, paragraph 79 ("a smoke extraction system designed by a man whose business card claimed an engineering credential he did not hold, drawn up to draw smoke downward against the physics of hot gas.").
Issue: The Tech Scout brief says "Smoke extractors were designed to draw smoke downward — physically impossible given that hot gases rise." That is correct. The Strategist's v2 phrasing — "drawn up to draw smoke downward against the physics of hot gas" — is fine, but the sequencing ("designed by a man whose business card claimed an engineering credential he did not hold, drawn up to draw smoke downward") leaves "drawn up" grammatically attached to "credential," not "system." The sentence rewards an attentive reader but trips a fast one.
Recommendation: Split the sentence. "The primary failure mode at BER was fire suppression. The smoke extraction system had been designed to draw smoke downward, against the physics of hot gas. Its designer — a draughtsman whose business cards claimed an engineering credential he did not hold — had been the lead consultant on the design."

---

## C. Unsupported Claims Still Present

**C1. "The single most consistent precursor to failure" is a comparative claim no brief makes.**
Location: Section II point 5 (line 55).
Issue: "Fifth, the integrated testing window is the single most consistent precursor to failure." The Operations Analyst and Aviation Historian briefs identify *three* recurring causes: testing compression, optimistic throughput assumptions, and an owner unwilling to delay. The Strategist's selection of one as "the single most consistent" is editorial. The same paragraph then walks through Munich's advice, the T5 paper, Changi T3/T4, and Newark — which support testing compression as *a* consistent factor, not necessarily *the most* consistent one.
Recommendation: Soften to "Fifth, integrated testing is the precursor most consistently compressed in failures and most consistently honored in successes" — defensible from the briefs. Or just "Fifth, the integrated testing window..." and let the evidence make the case.

**C2. "Most predictable risk in the program" is also a comparative claim.**
Location: Section II point 7 (line 59).
Issue: "The carrier's commercial pressure to open Concourse E early is the most predictable risk in the program." The Airline Strategist brief identifies multiple structural risks: CPE inflation, MII veto, carrier dehubbing, network reallocation. "Most predictable" requires a comparison the Strategist did not make.
Recommendation: "A predictable risk" rather than "the most predictable risk." Or pick a different formulation that does not invite the comparative-ranking challenge.

**C3. "No measurable wear on the original carriers" — the Strategist hedged Munich figures but still asserts this one as fact.**
Location: Section II point 2 (line 49) and Section III, paragraph 89.
Issue: v1 item A.11 flagged that all Munich T2 performance figures are vendor-self-reported. v2 partially addresses this — "vendor- and operator-self-disclosed 99.9% availability and no measurable wear on the original carriers (BEUMER Group operational reference; no independent post-installation audit is in public literature)." Good. But the "no measurable wear" claim is the most extraordinary of the Munich figures (a 22-year-old conveyor system with no measurable wear is a claim that, if true, would be worth a peer-reviewed paper). The hedge "vendor- and operator-self-disclosed" applies to the availability number. It does not visibly attach to the "no measurable wear" assertion. The reader processes 99.9% as caveated and "no measurable wear" as fact.
Recommendation: Distribute the caveat. "BEUMER's operational reporting describes... the carrier belts as showing no measurable wear after twenty-two years. Each figure is operator-self-disclosed and unaudited in public literature." Two sentences making clear the caveat covers both numbers.

**C4. "Tens of thousands of catalogued defects at BER" in the exec summary is now both vague and partly invented.**
Location: Section II point 1 (line 47).
Issue: "tens of thousands of catalogued defects at BER (TÜV's 2014 inspection counted 75,000; the count rose toward 120,000 by opening day in 2020, per Contrarian and Airport CEO brief sourcing)." The 75,000 figure is in the Operations Analyst brief and TÜV's 2014 inspection. The 120,000 figure is in the Contrarian brief as "approximately 120,000 defects." Good. But "rose toward 120,000 by opening day in 2020" implies a documented trajectory between the two numbers. Neither brief provides that trajectory. The two numbers are snapshots six years apart, by different inspectors, using potentially different counting methodologies. The Strategist's "rose toward 120,000" is an implied causal narrative.
Recommendation: "TÜV's 2014 inspection identified 75,000 individual defects; subsequent inspections through opening day in 2020 had catalogued approximately 120,000." This conveys the numbers without implying a monotonic count.

**C5. The "63%" reduction claim is missing — but the figures cited for Asia-Pacific mishandling do not match brief sourcing.**
Location: Section IV, paragraph 9 (line 147).
Issue: "IATA's 2024 mishandling data shows Asia-Pacific at 3.1 bags per 1,000 passengers, North and South America at 5.5, Europe at 12.3 — a four-to-one spread between Asia and Europe." Operations Analyst brief: "Asia-Pacific... 3.1 per 1,000 passengers" — supported. Contrarian brief: "Asia at 3.1 mishandled bags per 1,000 passengers; North and South America at 5.5; Europe at 12.3" — supported. The 4-to-1 spread (12.3/3.1 = 3.97) is mathematically defensible. Not an error. But the comparative "four-to-one" is Strategist-derived; it would benefit from a "roughly four-to-one" or just "roughly 4x."
Recommendation: Soft fix — "roughly four times" or "nearly fourfold" reads more honest than "a four-to-one spread."

**C6. The "$400–500 million BHS at IAD with deferred integrated testing... delivers the Denver outcome at the upper bound" sentence is doing a lot of unsourced work.**
Location: Section VI, closing paragraph (line 205).
Issue: "A $241.5 million Austin-Bergstrom-scale BHS at IAD, properly designed and commissioned, would deliver roughly $0.40–0.55 per passenger in annual debt service — a defensible figure. A $400–500 million BHS at IAD with deferred integrated testing and optimistic throughput assumptions delivers the Denver outcome at the upper bound." First, where does $400–500M come from? Section II point 8 sized the envelope at $280–560M. Section VI rephrases this as $400–500M without bridge. Second, "delivers the Denver outcome" — Denver's total documented cost was $520–600M including a decade of post-opening maintenance, not a single $400–500M commissioning event. Third, the $0.40–0.55 per passenger annual debt service figure is an analyst calculation that does not appear in the briefs. It looks derived (Austin-Bergstrom's $241.5M ÷ ~22M annual passengers = $11/passenger amortized; or some other math), but the derivation is not shown.
Recommendation: Either source the $0.40–0.55 figure or strip it. The "$400–500M" range needs reconciliation with the $280–560M envelope. "The Denver outcome at the upper bound" should be qualified — Denver's $520–600M was the total cost across a decade including the system that never functioned; a $400–500M commissioning failure is a different event.

---

## D. Counter-Arguments Still Not Fully Engaged

**D1. The PGDS-in-flight problem is acknowledged but not actually addressed.**
Location: Section V (line 181) and Section IV item 8 (line 153).
Issue: v1 item A.40 flagged the PGDS revision cycle as a counter-argument the Strategist did not engage. The v2 mentions it in Section IV ("PGDS v8.0 is current; v9.0 is in development. A BHS designed today to v8.0 may need re-engineering to v9.0 before iSAT") and again in Section V ("The PGDS-in-flight problem is real..."). But the implications section (VI) does not return to PGDS. The recommendation should be: how should MWAA's BHS design hedge against a PGDS revision arriving mid-project? Design margin for v9.0 anticipated requirements? Engage TSA early on draft v9.0? The counter-argument is acknowledged but not converted into design discipline.
Recommendation: Section VI's architecture paragraph or testing paragraph should include a PGDS-hedging recommendation. Otherwise the counter-argument is conceded and then forgotten.

**D2. The Contrarian's redundant-path argument is now mentioned but treated as conceded — and the implications section does not return to it.**
Location: Section V (line 167) and Section VI (no clear callback).
Issue: v1 item A.39 flagged the redundant-path argument as unaddressed. The v2 concedes it in Section V: "the redundant-path question is the most important schematic-phase decision for the IAD program and is currently in the eighteen-month window where it can still be specified." Strong concession. But Section VI's architecture paragraph discusses tunnel geometry, makeup-room geometry, EBS, and cybersecurity — and only obliquely names the redundant-path question ("makeup-room geometry, EBS footprint, sortation architecture — set the BHS performance envelope"). If the redundant secondary sortation path is "the most important schematic-phase decision," it should have its own paragraph in Section VI with the specific recommendation: write the redundant-path requirement into the schematic-design RFP before tunnel cross-sections are fixed.
Recommendation: Promote the redundant-path argument to its own Section VI subsection, or at minimum a dedicated paragraph. It is the cleanest, most actionable schematic-phase recommendation in the file and currently gets one phrase.

**D3. The "single common pathway" claim still does some of the work the v1 critique flagged.**
Location: Section III, line 81; Section V, line 173.
Issue: v1 item A.24 (separately, A.6's "taxonomy" objection from Contrarian brief) flagged that the four canonical cases are not the same failure. v2 addresses this — the taxonomy paragraph in Section III names four distinct failure modes (scope creep, testing compression, cascading IT, envelope failure) and Section V partially concedes the taxonomy objection ("the report should treat them with more precision than a single label"). Good. But the same paragraph then asserts: "They share a final common pathway: an opening date the institution cannot move, accountability that dies at organizational boundaries, and warning signs treated as background once they have arrived enough times to feel normal." This "common pathway" framing carries most of the analytical weight. The reader thinks: if each failure mode has a different upstream cause but they "share a final common pathway," is the common pathway actually a useful unit of analysis, or is it just the trivially-true observation that all delayed-opening disasters share the feature that the opening was not delayed? The argument needs to explain *why* the common pathway is causal rather than tautological.
Recommendation: The common-pathway claim needs a sentence on why the pathway is itself the intervention point — because the upstream causes are diverse and difficult to prevent in any one project, the downstream gate (opening date authority) is the leverage point. Without that bridge, the taxonomy concession undermines the synthesis.

---

## E. Structural and Prose Issues

**E1. The opening still does the dramatic restatement that v1 had.**
Location: Section I, paragraph 1.
Issue: "It carried no checked bags. None." The "None." sentence-fragment is the same rhetorical move v1 had. It performs emphasis the previous sentence has already earned. McPhee's tradition does not need to repeat itself in italics-of-meaning.
Recommendation: Drop "None." One sentence does the work.

**E2. "Preparing a £10 million invoice to BAA" is editorial.**
Location: Section I, paragraph 3 (line 33).
Issue: The Airline Strategist brief says BA "publicly demanded £10 million." "Preparing an invoice" reads more colorful but the brief does not document an invoice as the form of the demand. This is a minor editorial reshaping that introduces a small fictional detail.
Recommendation: "publicly demanding £10 million from BAA" matches the brief.

**E3. "By Day Five" capitalized is a tic.**
Location: Section I, paragraph 3 (line 33).
Issue: "By Day Five, 500 flights had been cancelled..." Capitalizing "Day Five" performs corporate-crisis-timeline voice ("Day Five of the BP crisis," "Day Three of the negotiation"). The case study uses an industrial register that does not fit the McPhee opening.
Recommendation: "by the fifth day" or "within five days."

**E4. The Coda has a strong penultimate paragraph and a weak final one.**
Location: Section VII, lines 213–215.
Issue: Already covered in A6. The penultimate paragraph ("At Dulles, the morning that matters has not arrived yet...") is the strongest closing in the file. The final paragraph dilutes it with the three "It is" declaratives and the three "The capital is" declaratives. The piece would end stronger one paragraph earlier.
Recommendation: End the piece at line 213. Cut line 215.

**E5. "These observations are recommendations, and naming them as such is the honest thing to do."**
Location: Section VI, line 205.
Issue: This sentence is another instance of "honest" as defensive qualifier (see B7). It also concedes a v1 critique (A.25 — "own the recommendation") with a self-conscious aside rather than just owning it. Owning a recommendation means writing recommendations; it does not mean noting that one is being honest about writing recommendations.
Recommendation: Cut the sentence. The list of "Spend on X" recommendations that follows does the work without preamble.

**E6. The "Where I push back, briefly" section in Revision Notes invites the reader to litigate v1 disagreements.**
Location: Lines 19–23.
Issue: Even granting the Revision Notes should exist (they should not — see A1), the "Where I push back, briefly" section explicitly invites the reader to engage with the prior critique. The reader of the manuscript does not have the prior critique. They have only the assertions that things were pushed back on. This is the writer reading their email in front of the reader.
Recommendation: Already covered by A1. Strip the entire preamble.

---

## F. The Two-Paragraph Summary

The v2 is a substantial improvement over v1 on the line-level numbers and citations. The Heathrow scene works. The deregulation framing is in. Pittsburgh is in. Vaughan is named. The Munich figures are caveated. The Hong Kong date is corrected. The "as the X brief notes" tic is largely gone. The exec summary has lost its bolded headers. Most of the substantive v1 critique was responded to in good faith.

The piece still has three structural problems that the line-level fixes do not solve. First, the Revision Notes preamble has displaced the opening scene and turned the manuscript into a document about a previous draft. Second, the Executive Summary is still board-deck voice at length — the bolded headers were the visible symptom, not the disease. Third, the Coda still ends on the chiastic and triple-declarative cadence v1 flagged, despite the Revision Notes' claim that those constructions were cut. The next revision needs to address these three at the structural level, not by adding language about how they have been addressed. Cut the preamble. Halve the exec summary. End the piece one paragraph earlier.

---

*Red Team critique v2 prepared June 3, 2026. The Strategist should treat A1–A7 as items the previous critique already raised that v2 did not fully resolve; B1–B10 as new weaknesses introduced by the revision; C1–C6 as residual brief-sourcing problems; D1–D3 as counter-arguments still under-engaged; and E1–E5 as prose-level issues. Items with the highest leverage for the next revision are A1, A2, A4, B1, B5, B8, and the structural items in the closing summary.*
