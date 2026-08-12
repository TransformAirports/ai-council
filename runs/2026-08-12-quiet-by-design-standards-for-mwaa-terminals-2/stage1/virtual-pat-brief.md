# Virtual-Pat Brief — Quiet-by-Design Standards at IAD and DCA

**Run:** `quiet-by-design-standards-for-mwaa-terminals-2`
**Author lens:** solution-oriented, asset-recombining, MacGyver-with-a-P.E.-stamp.
**One-sentence thesis of this brief:** MWAA does not need a nine-figure program to reach the outcome the run prompt is chasing; it needs to insert a small number of measurable requirements into apparatus it already owns — the Design Manual, the AODB, the DC Airports app, the Sunflower program, and a fleet of mobile lounges it is about to throw away — before the next three RFPs go out the door.

The Strategist will hear, from other agents, some version of "adopt an SFO-style Quiet Airport program" or "commission a new acoustic standard." That is the right instinct. It is also the expensive, slow, and easy-to-defer version. This brief is here so the Strategist has the other version available in the same report: the one that starts on a Monday, costs 2 percent of a capital line, and generates real evidence before Concourse C/D design freezes.

## 1. The asset inventory read — what MWAA already owns that bears on this problem

- **The MWAA Design Manual (seven volumes, 2020) and MASTERSPEC-derived Specifications library.** MWAA describes the Manual as "mandatory guide with the force of law on the airport property," updated annually, edited from MASTERSPEC by the Office of Engineering, with airport-specific supplementary volumes at IAD and DCA. This is the enforcement vehicle. Any "standard" not written into these documents is a memo. Any acoustic or PA requirement written into them binds every consultant, contractor, and tenant.
- **The DC Airports mobile app (Fly2DCA/Fly2IAD, "DC Airports," built by MWAA Labs).** It already pushes gate-change and delay notifications, offers turn-by-turn wayfinding, and integrates security wait times. The redundant channel that makes a quiet policy defensible on accessibility grounds already exists and is already in the app stores. The question is whether MWAA extends what the app *does*, not whether MWAA needs a new app.
- **The Sunflower Hidden Disabilities Program at both DCA and IAD.** Rolled out at pre-security, baggage claim, and USO lounge information desks. This is a live, staffed, cross-terminal accessibility channel with a passenger-recognition mechanism. Any "quiet zone" or low-stimulation service designed without leveraging Sunflower is inventing infrastructure that is already on the property.
- **A retiring fleet of mobile lounges at IAD.** The $20B+ transformation announcement explicitly retires them once AeroTrain extension is complete. These are HVAC-equipped, enclosed, movable rooms on aircraft-tug chassis. In the current framing they are salvage. In this brief, they are a family of pre-fab quiet cells with wheels, and a free acoustic mock-up chamber for Concourse C/D design decisions that would otherwise have to build $500K-plus wooden mockups.
- **The existing PA zoning and gate podium microphones.** Every gate in current MWAA terminals already has local gate audio hardware and a microphone at the podium. "Localize announcements to the gate" is a policy and firmware change on top of hardware MWAA has already paid for — not a new build.
- **AODB and FIDS.** The airport operations database that already drives flight information displays is the same feed an automated announcement system would use. The integration risk that airline PMOs cite ("we would have to build all new data plumbing") is largely already retired. AviaVox, the vendor most airlines already run in Europe, is CUPPS-compliant and rides existing PA or PABX.
- **The airline club and USO footprint.** Enclosed, acoustically-separated, privately-funded quiet space already exists in every concourse — MWAA just does not benefit from it because access is gated by fare class or veteran status. This is an asset the standard should acknowledge and, in one solution below, borrow from.

## 2. Five unconventional solutions, ordered from most to least achievable

### Solution 1 — Ship the Design Manual amendment before Concourse C/D 60 percent design

**Problem attacked:** Every quiet-airport failure story in the literature is a story about specifying acoustics *after* the design was frozen. If MWAA does not insert measurable acoustic, PA, and FIDS-density requirements into the Manual and MASTERSPEC library in the next two to three quarters, the IAD $20B+ program and DCA Terminal 1 replacement will each argue those requirements later as change orders at 3–8x cost.

**Mechanism:** A single addendum volume — call it Volume 8, "Acoustic and Passenger-Communications Design." It states, in a page or two of hard numbers: unoccupied ambient limit (target LAeq ≤ 55 dBA in holdrooms, ≤ 60 dBA in main circulation), reverberation ceiling (RT60 ≤ 1.2 s in holdrooms, ≤ 1.6 s in main hall), STI floor per ACRP Research Report 175 (STI ≥ 0.50 in passenger-processing zones, ≥ 0.45 minimum with 10 dB(A) SNR), PA zoning granularity (individual holdroom addressable, plus concourse-wide emergency), adjacent-zone spillover limit, FIDS density per linear foot, tenant sound-footprint cap, and a commissioning STIPA verification protocol tied to substantial completion. Every threshold is drawn from a document the industry already accepts (ACRP 175, IEC 60268-16 for STI methodology, IEC 60849 / EN 54-16 for voice alarm intelligibility). Nothing here is invented.

**Existing assets recombined:** the Manual itself, MASTERSPEC editing capacity in the Office of Engineering, and ACRP 175 as the source document.

**Cost order-of-magnitude:** $50K–$150K for consultant editing and internal review. This is a document, not a project.

**Implementation path:** Board-approved as an annual Manual update, not as a standalone policy — that is the vehicle MWAA already uses and the one airlines already expect. Applies to all new work at RFP release after adoption date; grandfathers projects past 60 percent design.

**Who resists and why:** designers and contractors bidding on the IAD program will resist adding a commissioning gate at substantial completion because it moves punchlist risk onto them. Airline design reps will resist per-gate PA addressability if they think it constrains boarding practice. Both are manageable if the requirement is written before their bids are priced.

**Failure mode:** the amendment gets diluted in Manual review into aspirational language ("designers *should consider* intelligibility") and ceases to bind. Prevent by writing every threshold as a numeric acceptance criterion, tied to a test method, tied to a substantial-completion checkpoint.

### Solution 2 — Push the boarding call to the app the airport already ships

**Problem attacked:** The concourse-wide PA is the loudest single contributor to terminal ambient noise, and roughly 70 percent of what it carries at IAD and DCA on any given hour is boarding calls that the boarding passenger already has on a device. SFO cut daily announcement time by 90 minutes (paging occurrences 492 → 261; duration 145 min → 58 min, a 60 percent reduction in cumulative duration) not by silencing anything safety-critical but by moving boarding calls to gate-local audio and pushing the redundant channel elsewhere. MWAA already ships the elsewhere.

**Mechanism:** Automate boarding-call generation from AODB events (boarding-open, group calls, final-call, gate change) into two parallel channels: a gate-local audio call at podium volume (with the human agent's mic still overriding), and a targeted push notification through the DC Airports app to passengers with that flight in "My Trip." Concourse-wide PA reserves itself for exception announcements (irregular ops, security, weather diversions, emergency). Use an AviaVox-class automated engine — the vendor is CUPPS-compliant, integrates with existing PA/PABX, is already the standard at 130+ airlines, and supports 35+ languages, which is the accessibility answer to the international traffic profile at IAD.

**Existing assets recombined:** AODB, gate podium hardware, the DC Airports app, the airline gate agent workforce (freed for passenger contact), and the Sunflower program (as the recognized channel for passengers who need staffed announcement equivalence).

**Cost order-of-magnitude:** Software-and-integration heavy. Rough envelope: $80K–$180K per gate for the automation engine (vendor list price varies by scope), $200K–$400K for AODB integration and app push extension, plus internal PMO. Deployed across ~50 IAD/DCA gates over 24 months, the terminal-wide envelope lands in the low-single-digit millions — a rounding error on the $20B+ transformation and cheaper than any capital "quiet lounge" wing.

**Implementation path:** Pilot on three DCA gates during a low-traffic operational window with one carrier's consent. Measure boarding time (AviaVox claims up to 20 percent efficiency; even 5 percent is a real airline number), missed-boarding rate, and STIPA-verified concourse ambient. Roll out by carrier and concourse based on the pilot data, not on universal fiat.

**Who resists and why:** Gate agents worry it takes work away — it does the opposite; it takes routine scripting away and leaves them free to handle exceptions. Legal will worry about ADA. Answer: the app push, the visual FIDS, the staffed Sunflower channel, and the gate-local audio together form the redundant channel set the ADA analysis actually requires. Airlines with legacy CUTE/CUPPS platforms will drag; contract enforcement through the Use and Lease common-use provisions is the lever.

**Failure mode:** MWAA rolls out automation without the app-push and Sunflower redundancy, and effectively re-runs the London City Airport model on a passenger mix that is not London City's. The redundant-channel design is what makes this defensible.

### Solution 3 — Convert two retired mobile lounges into rolling low-stimulation cells and an acoustic mock-up chamber

**Problem attacked:** MWAA is about to scrap or auction an asset that solves two adjacent problems: (a) IAD has no dedicated sensory-friendly quiet room; the Sunflower program is a lanyard without a destination. (b) Concourse C/D replacement design will make ceiling-and-floor finish decisions that determine RT60 for the next 40 years, and those decisions are conventionally made from spec sheets, not from a full-scale mock-up.

**Mechanism:** Reserve two of the retiring mobile lounges. Convert one to a mobile "Sunflower Quiet Cell" — internal fit-out with acoustically absorptive lining, dimmable lighting, no PA speaker feed, a mother's-room-grade seating configuration, and a Sunflower-recognized staffing tie-in. Park it curbside or airside near IAD's Concourse A/B intersection or Concourse C, or roll it into surge positions during irregular ops. Convert the second to a fitted-out acoustic mock-up shell used by the Concourse C/D design team to A/B test finish assemblies before any spec is issued for pricing. When the design phase closes, refit it as a second quiet cell or offer it to Loudoun County for community use.

**Existing assets recombined:** the mobile-lounge chassis (asset value being written down), IAD Fire and Rescue's existing curbside vehicle management, Sunflower staffing, the Office of Engineering's acoustic consultant bench, and rented STIPA/tapping-machine metrology (~$8K for a two-week rental window).

**Cost order-of-magnitude:** $80K–$200K per unit for fit-out, versus roughly the same for a purpose-built mock-up MWAA would otherwise buy and throw away, and versus the multi-million-dollar cost of a permanent airside quiet wing.

**Implementation path:** Ninety-day proof — decommission one mobile lounge to a spec-writing team, do the fit-out in the existing MWAA maintenance shop, publish the acoustic test results. Loudoun press picks this up as reuse; sensory-access groups pick it up as accessibility. The audacity is the point: it is a $150K answer to a problem the industry usually solves with a $30M lounge.

**Who resists and why:** MWAA's own asset-disposal process may prefer auction proceeds. Fire and rescue will require access certification. Airline operations will want assurance the vehicle does not clog airside choreography — solved by parking curbside or in landside pre-security zones where mobile-lounge chassis already have operating history.

**Failure mode:** The retiring lounges get auctioned before this proposal reaches the board. This is a timing solution. It expires.

### Solution 4 — Amend the tenant lease and concession handbook to cap sound footprint before the next RFP cycle

**Problem attacked:** Concession TVs, retail music, and airline club audio contribute a large fraction of concourse ambient sound and are almost entirely uncontrolled by MWAA today. Retrofitting them after leases are signed is politically expensive; specifying them at RFP is nearly free. SFO's Quiet Airport policy explicitly leaned on tenant rules limiting sound footprint and restricting music use, and reported the tenant piece as a meaningful contributor to the 40 percent overall onsite noise reduction.

**Mechanism:** Insert three requirements into the standard tenant lease and concession handbook: (a) sound-level cap measured at the lease line (e.g., ≤ 65 dBA at 1 m from lease-line at any hour), (b) prohibition on TV audio in unenclosed premises (visual-only with closed captions on), (c) equipment procurement compliance list for any airline gate-agent audio and airline club PA that ties into MWAA infrastructure. This is a document change with a 12–24 month tenant transition window.

**Existing assets recombined:** the tenant lease apparatus, MWAA's real-estate compliance function, and the same STIPA/SPL measurement kit used for Solution 1 acceptance testing.

**Cost order-of-magnitude:** Effectively zero direct capital. Enforcement staffing is a fraction of an FTE in the real-estate compliance function.

**Implementation path:** Amend the tenant handbook first (does not require re-execution of existing leases; applies at renewal and at any premises alteration), then insert into the next RFP cycle for DCA Terminal 1 replacement concessions. Tie enforcement to existing tenant coordination meetings.

**Who resists and why:** Concessionaires argue TV audio drives dwell and spend. The counter is airline experience at SFO: reported concession spend went up, not down, once ambient stress dropped. Sports bars are the honest exception; carve them out by category, not by pleading.

**Failure mode:** MWAA writes the cap but does not measure. A sound-level cap without a monitoring protocol is a suggestion. Attach a spot-check regime to the same instrumentation Solution 1 already funds.

### Solution 5 — A "Sunflower Silent Lane" through TSA at scheduled windows, with no new hardware

**Problem attacked:** Even a perfect terminal-side quiet-by-design outcome breaks at the security checkpoint, which is the loudest, most stressful, and most cognitively demanding zone in the passenger journey. Every neurodivergent, deaf/HoH, and infrequent-traveler focus group in the accessibility literature identifies checkpoint as the acute pinch point.

**Mechanism:** Use an existing lane at defined off-peak windows (early morning at DCA between the 5:00–5:30 slot bank, mid-day at IAD international pre-departure) as a Sunflower Silent Lane — visual-only announcements at the divest belt, TSOs briefed on low-stimulation protocol (no clap-through, no shouting, calm hand-signal repertoire), tactile signage at bin drop. No new equipment. Signage change, a Sunflower staffing tie-in, and a schedule.

**Existing assets recombined:** existing TSA lanes and staffing (MWAA works this through the TSA Federal Security Director schedule), the Sunflower lanyard as the recognized channel, and the airport ambassador program at both airports.

**Cost order-of-magnitude:** Under $30K for signage, tactile kit, and staff training in the first 90 days.

**Implementation path:** Pilot at DCA (single lane, one operational window) inside a 60-day window with the FSD's cooperation. Publish outcome data — throughput, complaints, use rate — before proposing IAD extension.

**Who resists and why:** TSA can argue that specialized lane management dilutes throughput. Counter: this runs in a low-demand window where lane utilization is already sub-optimal. Union coordination is real but small.

**Failure mode:** No passenger uses the lane because MWAA never told them. This is a marketing failure; solve by tying it to the Sunflower onboarding and the DC Airports app.

## 3. Precedents — operations already running some version of this

- **San Francisco International (SFO) Quiet Airport Program, 2018–2020.** Documented reductions: paging occurrences from 492 to 261 (–47 percent), cumulative duration from 145 to 58 minutes (–60 percent), self-reported ~40 percent reduction in onsite noise. Program leaned on gate-local audio, elimination of concourse-wide final-call, tenant sound-footprint rules, and music-volume policy. [Source: https://www.airport-technology.com/features/san-francisco-quiet-airport/] [Source: https://www.gensler.com/blog/designing-the-quiet-airport-at-sfo] [Source: https://www.thetravel.com/san-francisco-airports-quiet-airport-policy/]
- **London City Airport silent terminal, since 2008.** No routine PA in the departure lounge; passengers rely on FIDS and, more recently, real-time flight updates pushed via Facebook Messenger and Twitter. Announcements are made only for weather delays or emergencies. [Source: https://www.londoncityairport.com/at-the-airport/need-to-know/airport-policies/silent-policy]
- **Boston Medical Center telemetry alarm reduction, 2011–2013.** 89 percent reduction in weekly audible cardiac alarms (62,793 → 3,970); noise floor fell from 90 dB to 72 dB. Achieved by reclassifying self-resetting alarms as crisis alarms requiring nurse action, rolled from a single pilot unit to 310 of 332 beds in 18 months. The hospital-industry precedent for MWAA: measurable acoustic outcomes are reachable in occupied 24/7 environments through policy rather than construction. [Source: https://www.sciencedaily.com/releases/2014/01/140115172938.htm] [Source: https://www.patientcarelink.org/boston-medical-center-tackles-alarm-fatigue-and-noise/]
- **AviaVox automated passenger announcement platform, deployed at 130+ airlines and airports in 35+ languages.** CUPPS-compliant; integrates with existing PA/PABX and AODB. Vendor claims up to 20 percent boarding efficiency improvement; even discounted heavily, the throughput gain is on the same order as the ambient-noise gain. [Source: https://aviavox.com/for-airlines/]
- **Schiphol Buitenschot Land Art Park, 2013.** 80-acre landscape acoustic diffraction system that cut ground noise near the airport in half using earthworks in a pattern originally derived from Ernst Chladni's acoustic figures. Cited here not as a directly transferable IAD solution but as the industry's cleanest example of a low-tech recombination that outperformed a nine-figure engineered alternative. [Source: https://www.smithsonianmag.com/innovation/crazy-land-art-deflects-noise-from-amsterdams-airport-180955398/]

## 4. The 90-day pilot tier — three things MWAA could start on Monday for under $100K total

1. **Baseline STIPA + LAeq survey at one IAD holdroom and one DCA holdroom.** Two-week metrology rental (~$8K), two-week acoustician time (~$25K), one MWAA engineer as escort. Deliverable: a defensible ambient-noise and intelligibility baseline that every subsequent standards conversation cites. This is the "before" number the entire program depends on.
2. **AODB → DC Airports app boarding-call push at three DCA gates, one carrier.** Software integration only — the AODB, the app, and gate podium audio all exist. Deliverable: a two-week A/B test comparing missed-boarding rate, boarding time, and concourse PA volume between control and pilot gates. Under $50K if built in-house against the existing app.
3. **Reserve two retiring mobile lounges from disposition and fit out one as a quiet-cell prototype.** Requires a decision on the disposition schedule before it becomes irreversible. Fit-out at ~$40K–$60K in MWAA's own maintenance shop within the 90-day window. Deliverable: a demonstrable low-stimulation space at IAD by end of quarter — the physical artifact that turns the standards conversation from abstract to argue-able.

All three combined ship real evidence before any capital committee meeting on Concourse C/D or DCA Terminal 1 has to make a design decision.

## 5. The kill list — clever-sounding ideas rejected, one sentence each

- **Terminal-wide beam-steered directional loudspeaker deployment.** Impressive on demo day; $2–4M per concourse; still fails ACRP 175 STI targets if the room's RT60 is wrong, which is the actual problem.
- **White-noise / sound-masking installations across public zones.** Solves the office-privacy problem MWAA does not have; adds ambient noise to a terminal we are trying to make quieter.
- **App-only communication.** ~15–20 percent of IAD passengers are international/non-English/first-time-flyers; an app-only design is a Title II ADA and Title VI language-access risk MWAA does not need.
- **A new "quiet wing" or dedicated sensory terminal.** A decade to build, a nine-figure line, and by the time it opens the standard belongs in every concourse anyway.
- **Retrofitting the Saarinen Main Terminal for acoustic performance.** Historic-protection restrictions are prohibitive, and the acoustic problem is in the concourses, not the head-house.
- **Total ban on PA announcements.** SFO tried variants of this and rolled back to gate-local + exception; the missed-boarding and safety-messaging tails are non-negotiable.
- **Waiting for the DCA T1 replacement to "get this right in the new terminal."** The T1 design freezes long before the standard can be argued in that program; if MWAA does not standardize now, it re-argues every requirement inside a change-order fight.

**Bottom line for the Strategist:** the version of this argument that costs 2 percent as much and ships 20x sooner is a Design Manual amendment, a software integration on infrastructure MWAA already owns, and one repurposed mobile lounge. Everything else is the follow-through.
