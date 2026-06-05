# Technology Scout Brief: Wayfinding Technology in Airport Terminals
**Run:** Indoor Signage Best Practices  
**Stage:** 1 — Independent Research  
**Date:** June 3, 2026  

---

## 1. Taxonomy: What Counts as Wayfinding Technology

Before evaluating what works, we need to be precise about the category boundary. Airport wayfinding technology spans several distinct layers that are routinely conflated:

**Core wayfinding infrastructure**
Static overhead signs, Flight Information Display Systems (FIDS), digital directory kiosks, indoor positioning systems (Bluetooth beacons, Wi-Fi RTT), and content management systems that control what displays say. These are the tools that answer the question: *Where do I go next?*

**Passenger-managed wayfinding**
Mobile apps, AR navigation overlays, and QR-code-triggered directions. These require the passenger to actively participate. They perform differently from fixed infrastructure because adoption is voluntary.

**Supporting analytics**
Passenger flow heat maps, dwell-time analysis, and eye-tracking studies. These are not wayfinding systems themselves but are the validation tools used to evaluate whether the systems above work. Eye tracking in particular has moved from academic research tool to operational practice at Heathrow and Munich — a meaningful shift in the last five years.

**What doesn't belong in this taxonomy**
Advertising screens, retail directories, and entertainment displays are sometimes architected into signage systems and call themselves "wayfinding." They aren't. Their content optimization logic — maximize dwell, maximize impressions — runs directly counter to wayfinding logic, which is: get passengers moving in the right direction as fast as possible. When these systems share infrastructure and compete for screen time with navigational content, wayfinding degrades. This tension is poorly managed at most US hub airports.

---

## 2. Key Findings

**Finding 1: FIDS are the undisputed technology win; everything else is contested.**  
Dynamic flight information displays — gate assignments, boarding times, delay status, baggage claim carousel — have fully replaced static flip-boards and printed schedules without meaningful controversy. Changi Terminal 2 retired its iconic split-flat boards in February 2024 after 21 years. The FIDS market was $527M globally in 2024, growing at 7% CAGR [Source: https://www.globalgrowthinsights.com/market-reports/flight-information-display-systems-fids-market-101925]. This is settled technology with settled value. Every other category on the dynamic-signage spectrum has a less clear case.

**Finding 2: Eye tracking is now operational, not just academic — and what it reveals is embarrassing.**  
Heathrow ran a formal eye-tracking study of Terminal 5 passengers from December 2022 through January 2023 using Tobii Pro Glasses 3 across 108 participants. The study identified two specific failure modes: signs that passengers simply didn't notice, and areas where oversaturation of signs created cognitive overload and additional confusion. The T5 wayfinding satisfaction score had declined during the COVID period (when operational necessity prompted sign proliferation) and reversed after Heathrow acted on the eye-tracking data to declutter. Munich Airport's parallel study found that "passengers largely ignored information on navigation signage that wasn't relevant to their journey" — meaning information overload doesn't just confuse, it trains passengers to stop reading signs entirely. [Sources: https://www.tobii.com/resource-center/customer-stories/heathrow-uses-eye-tracking-to-improve-wayfinding; https://www.tobii.com/resource-center/customer-stories/munich-airport-wayfinding-study]

**Finding 3: Airport apps have a 7% ceiling, and the entire mobile-app wayfinding category is overinvested.**  
Independent analysis finds only 7% of airport passengers use mobile apps from their departure airport; airline apps reach 5x more passengers than airport apps [Source: https://tnmt.com/airport-apps-are-dying-out/]. The fundamental problem is what one analysis calls the "active role" problem: passengers will not install or open an app to solve a wayfinding problem that the terminal should solve for them with fixed signs. The airports that have achieved higher digital engagement — Schiphol, Changi, Hong Kong — did so with features that address genuine non-wayfinding pain points (baggage tracking, arrival notifications) and bundled wayfinding in. Gatwick committed to a system of approximately 2,000 navigation beacons as part of a "£2.5bn technology plan" and produced no documented outcome data [Source: https://travelwayfinding.com/indoor-positioning-gatwick-airport/].

**Finding 4: The decision-point is a testable technology discipline, not a design instinct.**  
Romedi Passini's 1992 framework (spatial decision-making: where people must choose, what information is available at that moment, and what they do with it) has been operationalized in ACRP Report 52's three principles — continuity (no passenger loses sight of a cue), connectivity (cues link to each other), and consistency (same system at every decision point) [Source: https://crp.trb.org/acrpwebresource2/acrp-report-52-wayfinding-and-signing-guidelines-for-airport-terminals-and-landside/]. What eye-tracking adds is *empirical validation* of where decision-points actually are versus where planners think they are. The Heathrow data found that the moments that matter are "transitional points" — entering large halls, exiting escalators, encountering multiple path options — not the mid-corridor sections where most airports put their biggest signs.

**Finding 5: Governance technology without governance authority is worthless.**  
The best wayfinding CMS implementation in the industry is functionally useless if airlines, TSA, and retail tenants can bypass it. Philadelphia International's Gresham Smith engagement documented a terminal where accumulated one-off renovations had made signage "disjointed and difficult for passengers to use" [Source: https://www.greshamsmith.com/projects/philadelphia-international-airport-phl-wayfinding-and-signage-upgrade/]. The recommended fix wasn't better technology — it was a GIS-based signage inventory and a standards manual that governs future changes. Manchester Airport's documented improvement in wayfinding came from concentrating authority: a single "Head of Visual Environment" with a clear directive to reduce sign volume, not add to it. [Source: https://www.airport-technology.com/features/feature41491/]

**Finding 6: The leading airports (Schiphol, Changi, Zurich) treat wayfinding as a system, not a product.**  
Paul Mijksenaar's work at Schiphol — which began in the 1990s and produced what is probably the most studied airport wayfinding system in the world — was grounded in two ergonomic research reports that studied how travelers relate to signage before any design work began: field of vision, sightlines, visibility, color contrasts, routing, decision points [Source: https://www.mijksenaar.com/project/amsterdam-schiphol-airport/]. The iconic yellow-on-black color system was not an aesthetic choice; it was a contrast solution for terminal lighting conditions. Zurich Airport's Burri system, designed by Grimshaw, was briefed explicitly for "bold, clear, practical and internationally understandable" wayfinding [Source: Grimshaw/Burri system documentation]. What distinguishes these systems from most US airports is not the technology; it is the pre-existing commitment to a performance criterion that technology has to meet.

**Finding 7: The "$700M in lost revenue" figure is not an audited number.**  
This figure appears repeatedly in vendor materials, trade press, and technology pitch decks as evidence that wayfinding failure has a quantifiable cost. The original source is not traceable to an independent study. It appears to be a secondary citation that has propagated without verification. Strategists should not use it in attributable claims. The structurally valid point underneath it — that passengers who are confused spend less, arrive at gates anxious, and are more likely to complain — has independent support, including the J.D. Power and MTT finding that "happiest passengers spend up to twice as much money in the airport" [Source: https://www.tobii.com/blog/so-many-signs-so-little-time], but that's a satisfaction-revenue correlation, not a wayfinding-specific cost quantification.

---

## 3. Evidence Section

### 3.1 Eye-Tracking Research

The most rigorous source of empirical data on airport signage behavior is now the Tobii case studies, which document actual passenger gaze behavior rather than surveys or simulations.

**Heathrow Terminal 5 (2022-23):** 108 participants tracked at arrival, departure, and connection touchpoints. Key finding: failures concentrated at "transitional points" — escalator exits, entries to large halls, multi-path junctions. Satisfaction metric reversed post-intervention. Note: Heathrow retained Tobii, a vendor; the research is applied rather than independent, but methodology (actual gaze data vs. surveys) is sound. [Source: https://www.tobii.com/resource-center/customer-stories/heathrow-uses-eye-tracking-to-improve-wayfinding]

**Munich Airport:** Airport used Tobii Pro Glasses 3 to study passenger engagement with navigation signs. Finding: passengers filtered out information irrelevant to their journey, which means sign overload doesn't just confuse — it causes passengers to stop reading navigation content altogether. The airport redesigned floor signage based on findings and validated dynamic digital displays for contextually relevant content. [Source: https://www.tobii.com/resource-center/customer-stories/munich-airport-wayfinding-study]

**Shanghai Pudong (PVG) satellite terminal (published 2021):** Laboratory-plus-field eye-tracking study documented that passengers demonstrate "reconfirmation behavior" — re-reading a sign they've already acted on — and tend to scan signs in a clockwise pattern. High information density and text-only formats increased cognitive load and reduced decision confidence; text-plus-graphic formats improved performance. [Source: https://www.researchgate.net/publication/354763265_From_Visual_Behavior_to_Signage_Design_A_Wayfinding_Experiment_with_Eye-Tracking_in_Satellite_Terminal_of_PVG_Airport]

A 2025 study published in the *Journal of Asian Architecture and Building Engineering* conducted a controlled laboratory experiment with 60 participants using combinations of information density and coding formats, with time pressure as a moderator. Outcome: "high information density and text-only formats increased cognitive load and reduced decision confidence, while text + graphic formats improved performance." This is peer-reviewed evidence, not vendor material. [Source: https://www.tandfonline.com/doi/full/10.1080/13467581.2025.2589544]

### 3.2 Technology Standards and Governance

**ACRP Report 52 (TRB, 2011):** The authoritative US standard. Establishes three wayfinding principles: continuity (directional cue visible within 30 meters at all times), connectivity (signs chain to each other across the entire journey), consistency (same system, same language, same hierarchy throughout). The report's guidance on technology is deliberately platform-agnostic; it establishes performance criteria that any sign system — static or digital — must meet. The FAA's Advisory Circular 150/5360-12F aligns with this standard. [Source: https://crp.trb.org/acrpwebresource2/acrp-report-52-wayfinding-and-signing-guidelines-for-airport-terminals-and-landside/]

**Port Authority of New York and New Jersey (PANYNJ) Wayfinding Manual:** Post-9/11 security additions, terminal expansions, and volume growth progressively degraded a system that had been built on a single standard. The PANYNJ manual attempt to re-establish system-wide coherence across multiple airports is the clearest US-side governance case study — both as a model and as evidence of how quickly entropy wins without active stewardship. [Source: https://wayfinding.panynj.gov/]

**ACRP Research Report 177 (TRB):** Covers wayfinding for aging travelers and persons with disabilities; documents that the populations most harmed by wayfinding failure are also the populations airports serve at increasing rates. Relevant for any technology evaluation that must account for baseline accessibility. [Source: https://crp.trb.org/acrpwebresource2/enhancing-airport-wayfinding-for-aging-travelers-and-persons-with-disabilities/]

### 3.3 Dynamic vs. Static: The Evidence Position

The industry literature does not have a clean randomized controlled trial comparing dynamic and static wayfinding systems at scale, and this matters when evaluating claims. What the evidence actually supports:

- **Dynamic is clearly better** for time-variant information: gate assignments, delay status, security wait times, baggage carousel assignments. These are use cases where static signs fail by definition.
- **Static is clearly better** for fixed spatial orientation: which direction is Terminal C, where are the elevators, which way is ground transportation. These facts don't change, and the research (Munich, Heathrow) demonstrates passengers learn to filter content that changes unpredictably.
- **The adversarial dynamic:** When digital displays show a mix of navigation and advertising content, the advertising logic undermines the wayfinding function. A screen that rotates between "Gates A1-A30 →" and a car rental ad trains passengers to discount it as a navigation resource. Manchester's documented improvement came from explicitly choosing not to use signage real estate for advertising in navigation-critical locations. [Source: https://www.airport-technology.com/features/feature41491/]

### 3.4 Cost Landscape

Direct cost data on airport wayfinding technology is difficult to obtain from public sources. What is documented:

- **Digital signage hardware per screen:** $1,000–$5,000 depending on size and specification; ongoing maintenance $100–$500/year per screen [Source: https://www.lookdigitalsignage.com/blog/digital-signage-cost]
- **Philadelphia International Airport:** ~1,500 digital displays across 3M sq ft of terminal space; managed through 900+ media players (planned consolidation to single CMS by 2026) [Source: https://statetechmagazine.com/article/2025/04/airports-leverage-displays-keep-passengers-moving]
- **Denver International Airport:** Structural analysis of existing overhead sign structures before replacement found foundations still sound, yielding an estimated $3–4M in avoided replacement costs [Source: https://www.greshamsmith.com/projects/denver-international-airport-den-comprehensive-signage-upgrade/]
- **Unplanned maintenance cost multiplier:** Emergency display replacements and vendor callouts cost 4.8x more than scheduled maintenance cycles [Source: https://oxmaint.com/industries/aviation-management/airport-signage-wayfinding-system-maintenance]
- **FIDS market (global):** $527M in 2024, projected $1.06B by 2034 [Source: https://www.globalgrowthinsights.com/market-reports/flight-information-display-systems-fids-market-101925]

No independently audited, airport-specific ROI studies on wayfinding technology investments exist in the public domain. Vendor-supplied figures should be treated as marketing materials.

---

## 4. Maturity Assessment: Real vs. Hype

**Mature, evidence-backed:**
- FIDS and baggage information displays (BIDS): fully mature, clear value, standard infrastructure
- Static overhead directional signage per ACRP 52 / FAA AC standards: proven; the challenge is governance, not technology
- Eye-tracking validation studies: methodologically sound, now affordable at operational scale (~$50,000 for a terminal study), and producing actionable data at Heathrow and Munich
- GIS-based signage inventory and standards manuals: underutilized but proven (Gresham Smith/PHL model)

**Functional but oversold:**
- Interactive directory kiosks: useful at key decision points (pre-security, post-security junctions), but adoption data is sparse and deployment without maintenance plan creates broken-display problems within 18 months
- Bluetooth beacon systems for analytics (heatmaps, dwell time): works, delivers value for sign placement decisions, but requires installation and ongoing calibration
- Digital queue-status displays at security checkpoints: documented in PHL and ATL; reduces passenger anxiety at a measurable decision point

**Overhyped, no documented scale outcomes:**
- AR navigation overlays: impressive demos, no published adoption data at hub-scale airports; Gatwick's "2,000-beacon" commitment produced no outcomes documentation
- Airport standalone wayfinding apps: 7% passenger adoption ceiling; investment rarely recovers
- "AI-powered" wayfinding kiosks: mostly re-branded FIDS integration with voice or touch interfaces; no evidence of performance superiority over well-designed static systems at navigation decision points
- Delta Parallel Reality (DTW, June 2022): technically interesting; no published outcome data two years post-launch; appears to remain a limited-deployment novelty

**Unresolved:**
- Passenger-face recognition for personalized wayfinding (Incheon tested guide robots in 2017; Prague deploys 6-language content adapted to passenger nationality composition): technically feasible, privacy constraint in US context creates deployment ceiling
- Integrated FIDS-to-mobile pass-through (gate change notification via airline app): real value in flight management, but requires airline cooperation and doesn't address primary wayfinding failure modes

---

## 5. Direct Quotes for Strategist Use

**On information overload as the actual problem:**
> "We're vastly reducing the number of signs on site." — Jacqueline Neville, Head of Visual Environment, Manchester Airport [Source: https://www.airport-technology.com/features/feature41491/]

**On what wayfinding failure actually costs operationally:**
> "The number one question we encounter at LAX is passengers asking for assistance to find an airline." — Terri Mestas, Los Angeles World Airports [Source: https://www.passengerterminaltoday.com/features/exclusive-feature-how-are-airports-transforming-their-wayfinding-programs.html]

**On where attention actually matters:**
> "Moments generally occurred at transitional points on their journey...Attention data in these few seconds were crucial to understanding what was causing confusion." — Tobii/Heathrow T5 research summary [Source: https://www.tobii.com/resource-center/customer-stories/heathrow-uses-eye-tracking-to-improve-wayfinding]

**On the limit of pleasing multiple stakeholders:**
> "Trying to please all of the people all of the time will only create the problem we're attempting to move away from." — Jacqueline Neville, Manchester Airport [Source: https://www.airport-technology.com/features/feature41491/]

**On the failure mode of signage designed for airports that haven't learned to ignore their tenants:**
> "Passengers largely ignored information on navigation signage that wasn't relevant to their journey." — Munich Airport / Tobii eye-tracking study finding [Source: https://www.tobii.com/resource-center/customer-stories/munich-airport-wayfinding-study]

---

## 6. Specific Notes for the Indoor Signage Run

**The dynamic-vs.-static question is a false choice in the wrong frame.** The better frame is: *what question is the passenger asking at this decision point, and which medium answers it most reliably under stress?* FIDS answers "has my gate changed?" Static signage answers "which direction is Terminal B?" Mixing these in the same display is not a technology decision; it's a governance failure. The strategist should push back hard on any recommendation that defaults to "more digital" as an upgrade path.

**The technology that matters most for the MWAA thesis is governance technology, not display technology.** The problem the run file describes — decades of accumulated, contradictory signage decisions — is not solved by installing better screens. It is solved by establishing who owns the standard, giving them veto authority over tenant and agency additions, and building a cataloging system (GIS-based) that makes it possible to enforce the standard across renovations. PHL's Gresham Smith engagement is the closest documented precedent: the deliverable was a standards manual and a database, not hardware.

**Eye tracking should be specified as a validation tool, not a research curiosity.** A terminal-scale eye-tracking study using Tobii Pro Glasses 3 runs roughly $40,000–$80,000 (based on Heathrow study scope). That is a rounding error against the capital cost of a signage renovation. Any airport installing a new wayfinding system that doesn't budget for a pre/post eye-tracking validation study is forgoing the only tool that tells them whether the system actually works.

**App-based wayfinding is not a substitute for a functional physical sign system.** The 7% adoption rate is decisive. Designing for the passenger who has installed the airport app is designing for a very small minority — and that minority is, by definition, already comfortable with airport navigation. The passengers who most need wayfinding help are the ones least likely to use an app.

---

*Sources cited inline using [Source: URL] format throughout. All vendor-supplied performance figures are noted as such and should not be used as independent evidence in the final report.*
