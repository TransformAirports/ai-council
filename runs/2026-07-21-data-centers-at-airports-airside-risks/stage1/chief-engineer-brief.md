# Chief Engineer Brief — Data Centers Near Airfields: The Constructability and Lifecycle Reality

**Run:** Data Centers at Airports: Airside Risks
**Lens:** Program delivery, constructability, lifecycle cost, FAA design standards, asset-condition and interdependency risk
**Date:** 2026-07-21

---

## Framing: what an engineer sees that a land-use review does not

A Part 77 obstruction review answers one question: does the building's static geometry pierce an imaginary surface? That is a survey problem. A data center near an approach or departure corridor is not a survey problem — it is a **process plant** that runs 24/7, sheds hundreds of megawatts of heat, stores and burns diesel, moves large volumes of water, and radiates RF. The airfield risk lives in the *operating envelope* of that plant, not in its roofline. The FAA's own obstruction-evaluation machinery was not built to catch a thermal plume that peaks 1,000+ feet above a cooling tower that itself never comes close to a Part 77 surface.

That is the structural gap the thesis correctly identifies. My job here is to tell you what the physics, the standards, and the build sequence actually look like — and to hold both sides honest. The data-center advocates understate the operating-scenario risk; reflexive opponents overstate the routine-cooling case and ignore that the controlling scenario is the *generator plant under prolonged islanded operation*, not the steam wisp on a cold morning.

---

## 1. Key Findings

- **The controlling scenario is prolonged emergency generation, not normal cooling.** Under normal water- or air-cooled operation, a hyperscale campus is a warm-but-modest buoyancy source. The design-controlling event is a grid outage that forces dozens of Tier 4 diesel generators — a small power plant, 50–200+ MW of prime movers — into simultaneous sustained operation. That combines a concentrated hot exhaust column, degraded local visibility, and NOₓ/PM emissions in exactly the low-altitude band where approach and departure corridors live. Any compatibility finding that models only "normal cooling" has tested the wrong load case.

- **Thermal-plume turbulence is a documented, FAA-recognized hazard — and it extends far above the structure.** FAA/MITRE work concluded that significant turbulent effects of an exhaust plume "can extend to heights of over 1,000 feet above the height of the top of the stack or cooling tower," and that the worst conditions are calm winds, low temperatures, and stable stratification — i.e., a still cold morning over a runway [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html]. A structure that clears every Part 77 surface can still launch a hazard column into protected airspace.

- **Do not conflate the four plume phenomena.** Visible vapor (condensation), hot exhaust (buoyant, low-oxygen), heat haze (optical/refractive), and aerodynamic turbulence (the vertical-gust hazard) are distinct. Only the last reliably upsets aircraft; the MITRE model sizes it against four aircraft classes (light-sport, light GA, business jet, large jet), and light aircraft feel it at higher altitude than heavy jets [Source: https://www.mitre.org/our-impact/intellectual-property/exhaust-plume-analyzer]. A rigorous review measures the vertical-velocity field, not the visible steam.

- **The facility is effectively permanent and un-phaseable.** Unlike a terminal or an apron you can build in stages and modify, a commissioned data center is a 20–30 year fixed asset with contractual uptime obligations to tenants who will litigate before they accept an operating restriction. There is no "phase 2 removal." Whatever airfield-capacity envelope it forecloses is foreclosed for a generation. This is the interface-risk trap: the airport carries the operational constraint forever; the developer carries only the construction period.

- **Evaporative cooling and stormwater features are wildlife and icing attractants under existing FAA guidance.** AC 150/5200-33C treats open water as a hazardous wildlife attractant and recommends detention basins stay "totally dry between rainfalls," with a 5-statute-mile separation standard where an attractant could move hazardous wildlife across approach/departure airspace [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf]. A large cooling-water/stormwater footprint near a runway can create standing water and vegetation the airport is otherwise obligated to eliminate.

- **The build itself is a grid and utility program, not a real-estate deal — and its schedule is governed by lead times the airport does not control.** Substation transformer lead times now exceed **160 weeks** in 2026, substation build plus long-lead gear runs **36–60 months**, and Northern Virginia grid-connection waits exceed **seven years** [Source: https://www.constructionowners.com/insights/how-long-it-actually-takes-to-power-a-data-center-in-2026-a-u-s-market-by-market-reality-check]. That matters airside two ways: (a) it explains why developers push generators to run longer and more often — the on-site diesel plant is the *interim primary source*, not a rare backup — and (b) it means any "24–36 month" compatibility-and-build story is optimistic before the first drawing is stamped.

- **EMI is plausible but must be tested, not assumed.** Data centers are dense RF and switching environments (high-frequency power electronics, cooling VFDs, wireless building systems) sited near ILS, radar, and 4.2–4.4 GHz radar-altimeter operations. The 5G altimeter saga proved the aviation altimeter band is "dependent on a sanitized RF environment" and vulnerable to adjacent-band emitters [Source: https://www.remcom.com/resources/articles-and-papers/assessing-5g-radar-altimeter-interference-for-realistic-instrument-landing-system-approaches]. I have **not** found a documented case of a data center degrading a nav aid, and I will not assert one. The point is that EMI is a testable engineering question with an established methodology — it should be in scope, not assumed benign.

---

## 2. Evidence

### 2.1 Thermal plume — the FAA already treats this as a real hazard

The FAA did not invent a rule for data centers; it built one for power plants and cooling towers, and a data center's generator hall behaves like a small power plant. The Aeronautical Information Manual, §7-6-16, "Avoid Flight in the Vicinity of Exhaust Plumes (Smoke Stacks and Cooling Towers)," warns pilots that turbulent effects can extend **over 1,000 feet above the top of the stack or cooling tower**, that smaller aircraft feel effects at higher altitude than heavier aircraft, and that hazards are "most critical during low altitude flight" in "calm and cold air, especially in and around approach and departure corridors" [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html].

The technical basis is the FAA Airport Obstruction Standards Committee (AOSC) Plume Study (2008–2010) and the MITRE verification (September 2012), which produced the Exhaust Plume Analyzer: a convective-flow model of the mean plume, two aircraft-response models sizing the vertical gust needed to cause severe turbulence or aircraft upset, and a turbulence model computing the probability of encountering such a gust — parameterized for four aircraft classes [Source: https://www.mitre.org/our-impact/intellectual-property/exhaust-plume-analyzer]. **Honesty note:** I did not confirm a single universal "X m/s = upset" threshold from primary FAA text; the model produces class-specific gust thresholds and probabilities, and any brief that cites one round number as *the* threshold is overstating the science. The defensible statement is qualitative and quantitative on *height* (>1,000 ft above source) and on *conditions* (calm, cold, stable) [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html].

FAA has a companion screening product, the "Technical Guidance Assessment Tool — Thermal Exhaust Plume Impact," referenced in its environmental/land-use library — the correct instrument for a data-center review, though the airport should require the developer to run it on the *generator plant at full islanded load*, not the chillers [Source: https://www.faa.gov/sites/faa.gov/files/airports/environmental/land_use/Technical-Guidance-Assessment-Tool-Thermal-Exhaust-Plume-Impact.pdf].

### 2.2 The generator plant is the real thermal and air-quality source

Virginia's "Data Center Alley" is the working case study, and it sits in the Dulles flight environment. Loudoun County holds roughly **200 data centers across ~50 million square feet**, concentrated along the Dulles Greenway corridor near IAD, with departures routinely overflying facilities [Source: https://www.city-journal.org/article/loudoun-county-virginia-data-centers-construction]. Virginia has about **9,000 backup generators statewide, ~4,700 in Loudoun alone** [Source: https://www.vpm.org/news/2025-12-17/virginia-data-centers-diesel-backup-generators-deq-loudoun-turner-dowd].

Two facts define the controlling scenario. First, in routine operation these generators run only "10 to 30 minutes per month" for testing, and most sites reported zero-to-two minor outages over two years [Source: https://www.vpm.org/news/2025-12-17/virginia-data-centers-diesel-backup-generators-deq-loudoun-turner-dowd]. Second — and this is the risk pivot — Virginia DEQ has been asked to *expand permitted generator run-time* precisely because grid supply cannot keep up, and the state set a **Tier 4 emissions baseline** amid community pushback [Source: https://www.datacenterknowledge.com/build-design/virginia-deq-revises-data-center-generator-rules-as-community-pushback-builds]. Permitted pollutants include NOₓ, PM10/PM2.5, CO, and VOCs [Source: https://www.vpm.org/news/2025-12-17/virginia-data-centers-diesel-backup-generators-deq-loudoun-turner-dowd]. The airside implication: the frequency and duration of the worst-case thermal/emissions event is not a fixed engineering constant — it is a regulatory variable that is trending *up* under grid pressure. Approve against today's 20-minutes-a-month profile and you may be living with tomorrow's extended-runtime variance.

### 2.3 Wildlife, water, and stormwater — an existing FAA obligation collides with data-center design

AC 150/5200-33C is unambiguous that open and standing water is a hazardous wildlife attractant. It recommends detention basins "remain totally dry between rainfalls," requires paved bottoms where flow or wetness is anticipated to suppress nesting vegetation, and applies a **5-statute-mile** separation concept where an attractant could push wildlife across approach/departure airspace [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf]. Evaporative cooling towers, makeup-water ponds, and large impervious-roof stormwater systems all push against this guidance. An airport that spends real money each year on wildlife-hazard management under Part 139 cannot casually approve a neighbor that engineers in the exact standing-water and vegetation conditions it is obligated to eliminate.

### 2.4 EMI — in scope, unproven, testable

The radar altimeter operates at 4.2–4.4 GHz and, per the 5G experience, is "dependent on a sanitized RF environment" during the landing phase when terrain separation is critical [Source: https://www.remcom.com/resources/articles-and-papers/assessing-5g-radar-altimeter-interference-for-realistic-instrument-landing-system-approaches]. Recognized external EMI sources include communication towers, high-voltage transmission lines, and improperly shielded electronic equipment [Source: https://www.remcom.com/resources/articles-and-papers/assessing-5g-radar-altimeter-interference-for-realistic-instrument-landing-system-approaches]. A hyperscale campus brings all three: on-site high-voltage feeds, dense switching electronics, and its own microwave/wireless links. I found **no documented instance** of a data center degrading an ILS or altimeter, and I will not manufacture one. The correct posture is a required EMI/EMC study and coordination with the FAA spectrum office — a solvable engineering item if scoped early, an expensive surprise if discovered at commissioning.

### 2.5 The build is a utility megaproject with lead times the airport cannot compress

Even setting airside physics aside, a hyperscale build is not "just a big box." Substation transformer lead times run **~160+ weeks in 2026** (up from ~50 weeks in 2021); substation construction is **18–36 months** but stretches to **36–60 months** once switchgear and breakers are counted; median interconnection-to-operation is approaching **five years**, and Northern Virginia connection waits exceed **seven years** [Source: https://www.constructionowners.com/insights/how-long-it-actually-takes-to-power-a-data-center-in-2026-a-u-s-market-by-market-reality-check]. PJM reported **>21 GW in engineering-procurement and 8.2 GW under construction** as of early 2026 [Source: https://www.datacenterknowledge.com/energy-power-supply/why-ai-data-center-projects-face-years-of-delays-after-approval]. This is the same optimism-bias pattern I have watched sink airfield programs: the first schedule assumes the utility interface is somebody else's problem. It never is. And the grid-delay gap is exactly what converts "emergency backup" diesel into de-facto primary generation — the airside hazard and the schedule risk share a root cause.

---

## 3. Cost and Schedule Reality (comparables)

- **Grid/substation interface:** 36–60 months for on-site substation and long-lead gear; 5–7+ years to firm grid supply in constrained markets like Northern Virginia [Source: https://www.constructionowners.com/insights/how-long-it-actually-takes-to-power-a-data-center-in-2026-a-u-s-market-by-market-reality-check]. Translation: any coupled "site-approval-to-operational-compatibility" timeline under ~4 years is optimistic.
- **Generator fleet scale:** ~4,700 backup generators in Loudoun County alone; a single large campus can field dozens of Tier 4 units totaling well into the tens-to-hundreds of MW of prime movers [Source: https://www.vpm.org/news/2025-12-17/virginia-data-centers-diesel-backup-generators-deq-loudoun-turner-dowd]. Airside review must model that fleet running together, not one set testing.
- **Regulatory variance drift:** Virginia DEQ actively weighing *expanded* generator run-hours because the grid cannot supply the load [Source: https://insideclimatenews.org/news/15122025/virginia-regulators-weigh-expanded-use-of-data-centers-polluting-generators/]. The worst-case operating envelope is not static; it moves against the airport over time.
- **Plume hazard height:** >1,000 ft above the source structure — a value that can place a hazard column inside approach/departure airspace even when the building clears every Part 77 surface [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html].
- **Wildlife separation benchmark:** 5 statute miles for attractants capable of moving wildlife across approach/departure airspace [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf].

---

## 4. Data Points a Strategist Can Use Verbatim

1. **"A data center that clears every Part 77 surface can still fire a turbulence column more than 1,000 feet above its cooling towers — into exactly the calm, cold, low-altitude air where approach and departure corridors live."** [Source: https://faraim.org/faa/aim/chapter-7/section-7-6-16.html]

2. **"The controlling airside scenario is not normal cooling. It is a grid outage forcing a fleet of Tier 4 diesels — a small on-site power plant — into sustained simultaneous operation. Loudoun County alone hosts roughly 4,700 backup generators."** [Source: https://www.vpm.org/news/2025-12-17/virginia-data-centers-diesel-backup-generators-deq-loudoun-turner-dowd]

3. **"The worst-case operating envelope is a moving target: Virginia DEQ is being asked to *increase* permitted generator run-hours because the grid can't keep up. Approve against today's 20-minutes-a-month test profile and you inherit tomorrow's extended-runtime variance."** [Source: https://www.datacenterknowledge.com/build-design/virginia-deq-revises-data-center-generator-rules-as-community-pushback-builds]

4. **"Northern Virginia grid-connection waits exceed seven years and substation transformers alone run 160-plus weeks. That delay is why 'emergency backup' quietly becomes primary generation — and it is why any 24–36 month compatibility-and-build timeline is optimistic before the first drawing is stamped."** [Source: https://www.constructionowners.com/insights/how-long-it-actually-takes-to-power-a-data-center-in-2026-a-u-s-market-by-market-reality-check]

5. **"FAA already obligates the airport to eliminate standing water and nesting vegetation near runways; a data center's evaporative cooling ponds and stormwater basins engineer those attractants back in — inside the 5-statute-mile screening distance."** [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf]

---

## 5. Screening Framework — studies MWAA should require before approval (public-information basis)

An engineer's approval gate, layered on top of (not instead of) the Part 77 review:

1. **Thermal-plume assessment on the controlling load case.** Require the FAA Thermal Exhaust Plume tool run for *full islanded generator operation* under calm/cold/stable atmospherics, mapping the vertical-velocity field against the four MITRE aircraft classes and against actual approach/departure track geometry — not a normal-cooling steam analysis [Source: https://www.faa.gov/sites/faa.gov/files/airports/environmental/land_use/Technical-Guidance-Assessment-Tool-Thermal-Exhaust-Plume-Impact.pdf].
2. **Generator-fleet emissions and visibility study.** All units simultaneous, worst-case duration matching the *permitted maximum* run-hours (with a sensitivity case for a future variance increase), quantifying NOₓ/PM and any localized visibility reduction over the corridor.
3. **Wildlife-attractant and stormwater compliance review** against AC 150/5200-33C — dry-basin design, paved bottoms, no makeup-water ponding, vegetation control [Source: https://www.faa.gov/documentLibrary/media/Advisory_Circular/150-5200-33C.pdf].
4. **EMI/EMC study and FAA spectrum coordination** covering ILS, surveillance radar, and the 4.2–4.4 GHz altimeter band, with a shielding/siting mitigation plan [Source: https://www.remcom.com/resources/articles-and-papers/assessing-5g-radar-altimeter-interference-for-realistic-instrument-landing-system-approaches].
5. **Lighting and glare study** for security/obstruction lighting and roof/glazing reflectivity along night and low-visibility approaches.
6. **Airfield-capacity-preservation finding.** An explicit demonstration that the facility does not foreclose a planned or foreseeable future runway, taxiway, RPZ, or NAVAID siting — because the facility is permanent and the constraint is permanent.
7. **Grant-assurance and ALP consistency check** — confirm the use is compatible with the sponsor's federal obligations and reflected on the Airport Layout Plan before, not after, entitlement.
8. **Emergency-response and fuel-storage review** — on-site diesel inventory (often hundreds of thousands of gallons), ARFF implications, and mutual-aid load, coordinated with airport public safety.

**Decision rule the thesis is right to insist on:** the burden of proof runs the other way. The developer must produce independent evidence of compatibility across *all* operating scenarios and of preserved future capacity — not merely a survey showing the roofline stays below an imaginary surface.

---

## Engineer's bottom line

Neither the concrete nor the compatibility case is as easy as its advocates claim. The routine-cooling risk is real but modest and manageable; opponents who hang the argument on a morning steam wisp will lose the technical fight. The defensible, controlling risk is the **generator plant under prolonged islanded operation** — a hazard whose worst case is being made *worse* by the very grid shortage driving these projects, and whose thermal column FAA already recognizes can reach 1,000+ feet above a structure that never trips a Part 77 surface. Combine that with an un-phaseable, generation-length asset that can quietly foreclose future airfield capacity, and the standard of review the thesis proposes — independent, all-scenario, capacity-preserving evidence — is not precautionary overreach. It is ordinary engineering diligence applied to a process plant that happens to sit under a flight path.
