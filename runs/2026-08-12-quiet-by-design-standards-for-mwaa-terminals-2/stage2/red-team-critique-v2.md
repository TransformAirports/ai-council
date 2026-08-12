# Red Team Critique v2 — Airport-Executive Review of Strategist Draft v2

**Run:** `quiet-by-design-standards-for-mwaa-terminals-2`
**Reviewer:** airport-executive-reviewer
**Target:** `outputs/stage2/strategist-draft-v2.md`
**Prior pass:** `outputs/stage2/red-team-critique-v1.md` (evidence-prosecutor)
**Basis:** `outputs/run-manifest.json`, `outputs/stage1/evidence-map.md`, `outputs/context/airport-context.md`, `prompts/runs/quiet-by-design-standards-for-mwaa-terminals-2.md`

## What this review is

The evidence pass has been run. Fabrications are struck, denominators fixed,
citations traced. This review reads the same draft from a different chair —
the seat of an MWAA executive who has to walk the amendment into the Office
of Engineering on Monday, defend it at the Airport Airlines Affairs
Committee on Wednesday, and put it in front of a Board committee before the
next capital-plan update. The question is not "is the argument true." It is
"can this be assigned, funded, approved, procured, staffed, commissioned,
and operated without a board resolution being amended on the floor."

Findings are numbered. Each one is tagged **[FATAL]** (the recommendation
cannot go to the Board as written), **[CONDITION]** (must be resolved before
adoption but does not kill the recommendation), or **[REFINEMENT]** (would
tighten the case; not required for readiness).

---

## Findings

### 1. Decision block does not name the decision the Board is being asked to make [FATAL]

- **Location:** "Airport Decision" block, ll. 74–90; Executive Summary ll. 30–36.
- **Charge:** The block names an owner ("MWAA President and CEO; Office of
  Engineering; Board of Directors") and a direction to draft, but no board
  action, no meeting cycle, and no approval instrument. A board reader asks
  three questions and gets none of them answered: **What am I voting on?
  When? Under what delegated authority?** The Design Manual is administered
  by the Office of Engineering; some amendments are internal engineering
  actions, others rise to a Board resolution because they affect airline cost
  recovery, project-delivery method, or federal grant terms. The draft does
  not say which category this amendment falls into or who confirms that. If
  Engineering can adopt it as an internal standards revision, the Board is
  a stakeholder, not the decision-maker. If it changes airline recoverable
  cost, it triggers AUL consultation and — depending on MII text — a formal
  objection process that the Board must be prepared to hear.
- **Remedy:** State the instrument (Design Manual amendment issued by the
  Office of Engineering under delegated standards-setting authority, with a
  Board information item at the next scheduled Business Administration
  Committee, escalating to a Board resolution only if consultation surfaces
  material airline objection or an AUL cost-center change). Name the meeting
  cycle by month, not by "capital cycle." Without that, "Board of Directors
  (adoption)" is aspiration.

### 2. Airline consultation timeline is absent — and it is on the critical path, not a dependency footnote [FATAL]

- **Location:** Dependencies block, l. 84; Executive Summary ll. 30–36; the
  entire body treats airline reach as a design objective without pricing the
  consultation.
- **Charge:** Any standard that touches airline recoverable cost or tenant
  audio must be routed through the AAAC well before it lands in a scope
  document. Under the 2025 AUL, the consultation obligation is procedural
  regardless of whether MII is invoked. The draft lists "airline
  consultation" as one line under Dependencies and treats MII as an unknown
  to be verified. That is upside-down for an executive review. The Council's
  own record is clear: United is publicly reluctant on the July 29
  transformation program, has already circulated a $90.64 CPE scenario, and
  will read a new acoustic and tenant-audio standard as a scope-creep signal
  during CPE negotiations. American at DCA will demand the same treatment
  Terminal-1-side. Neither carrier is asked politely to align with a
  Design Manual amendment mid-negotiation; each will demand cost impact,
  schedule impact, and MII characterization on the record before any scope
  document cites the section.
- **Remedy:** Add an airline-consultation lane to the 90-day plan:
  (a) confidential briefing to United and American executive station managers
  and their capital counsels in weeks 1–3; (b) formal AAAC briefing at the
  next scheduled meeting; (c) 30-day comment window on the draft amendment
  language; (d) written response letter cataloging airline concerns; (e)
  written MWAA position on cost-recovery categorization keyed to the AUL cost
  centers. Nothing goes into a scope document until (e) is on the record.
  Absent that lane the recommendation walks into the AAAC blind.

### 3. First 90 days is a verification list, not a delivery plan — day 91 is undefined [CONDITION]

- **Location:** "First 90 days" block, ll. 80.
- **Charge:** Five verifications are named; no drafting milestones, no
  socialization windows, no target date for a Board information item, no
  Concourse E baseline instrumentation contract, no signing authority for
  the acoustic consultant that will do the STI/ambient baseline. If Terminal
  1 phase turns out to be past scope-definition (Finding 13 in v1), what
  happens on day 91? The draft says the reference application shifts to an
  IAD C/D element, but there is no branch logic in the timeline.
- **Remedy:** Extend the plan through day 180 with two branches — Terminal 1
  in scope-definition (pilot proceeds) versus past scope-definition
  (Concourse E baseline becomes the reference application while a C/D
  element is qualified). Name the acoustic consultant procurement vehicle
  (existing IDIQ, task order, or new solicitation), the target Board
  briefing month, and the target amendment publication date.

### 4. Procurement path for the amendment work is unaddressed [FATAL]

- **Location:** No section addresses procurement of the acoustic engineering,
  commissioning, or platform work that the amendment implies.
- **Charge:** MWAA cannot commission a Concourse E baseline STI/ambient
  measurement or draft technically defensible amendment language without
  hiring acoustic engineering support. That is a professional services
  engagement — a Brooks Act qualifications-based procurement if federally
  funded, an MWAA-policy QBS if not. Either way it is a multi-month
  procurement, not a purchase order. The mobile notification platform in the
  $12M–$40M stack is a technology procurement that would trigger IT
  governance, cyber review, and potentially the Airport Airlines Affairs
  Committee. The FIDS redundancy line item is a capital project with its own
  design and construction procurement stack. None of this is named. A
  reader could adopt the recommendation on Monday and discover on Tuesday
  that nothing can start for six months.
- **Remedy:** Add a procurement path row per line item: acoustic engineering
  support (existing on-call A/E IDIQ if available; if not, new QBS), Concourse
  E baseline measurement (task order under existing commissioning contract if
  possible), platform (evaluate against existing MWAA IT governance
  processes and any active enterprise-notification contract), FIDS redundancy
  (identify existing capital program element it rides inside). Confirm each
  has an available vehicle or name the solicitation.

### 5. Cost stack is a range, not a budget — and it is not tied to a funding source [FATAL]

- **Location:** "Cost order of magnitude" block, l. 82; footnote 7.
- **Charge:** "$12M–$40M one-time across the full stack" tells the CFO
  nothing operational. What is the split between IAD and DCA? What portion
  is capital versus operating? What portion is airline-recoverable under
  the AUL cost centers, and what portion sits on MWAA general airport
  revenue? Which bond series or PFC application does the capital portion
  ride inside? The claim "the standalone CPE effect approaches zero if the
  standard rides inside program financing" is asserted, not shown. If the
  ceiling treatment premium adds to a program cost that is airline-
  recoverable under Terminal Rentals, CPE moves. The magnitude may be
  trivial; that determination is not in the draft. The draft is also silent
  on the operating-cost tail — governance platform annual license, ongoing
  commissioning verification, MWAA staff time to run the audit-log regime.
  A one-time capital range is not a life-cycle cost.
- **Remedy:** Provide (a) a rough allocation IAD/DCA, (b) capital vs.
  operating split, (c) recoverable-vs-non-recoverable characterization keyed
  to the AUL cost-center categories that would apply (Terminal Rentals,
  Landing Fees, etc.), (d) five-year operating tail for platform license,
  audit-log staffing, and commissioning verification, (e) the funding source
  candidate list per line item (existing program contingency, PFC amendment,
  GARB, airline recoverable). A CPE-neutral statement without those
  allocations is a claim, not a finding.

### 6. Debt-service coverage argument runs the wrong direction inside the recommendation [CONDITION]

- **Location:** Executive Summary ll. 34; body ll. 58 ("MWAA's coverage
  window makes the case sharper, not softer").
- **Charge:** DSCR compression from 1.63× to ~1.3× is cited as a reason to
  adopt the standard now — because rework avoidance is the easy sell. That
  argument holds only if the standard demonstrably reduces late-stage
  rework, not merely early-stage specification cost. The evidence prosecutor
  already trimmed the "order of magnitude" overstatement to two-to-four
  times. Even at four times, if the amendment adds cost to programs already
  in design (the committed AUL work), the DSCR argument cuts the other way
  — added specification cost inside a tight coverage window is exactly
  what rating agencies notice. The draft needs to explicitly separate
  "programs still in programming or early scope" (where the argument holds)
  from "programs in design or procurement" (where it does not) and route
  the standard into the first category only. If the Council cannot confirm
  where the committed AUL work sits on that curve, the DSCR framing should
  be softened.
- **Remedy:** Add a program-status table naming each committed AUL project
  by phase and stating which the amendment would apply to. Do not lean on
  DSCR compression as a general urgency argument; lean on it as an argument
  for scoping the amendment to still-in-programming work only.

### 7. Section 106 exposure on any Saarinen-adjacent work is understated [CONDITION]

- **Location:** Dependencies block, l. 84 ("Section 106 consultation on any
  Saarinen-adjacent modification"); body l. 54.
- **Charge:** The draft treats Section 106 as a checkbox. Section 106
  consultation on a Register-eligible district is a 6–18 month process with
  the Virginia State Historic Preservation Office and ACHP that can extend
  further if adverse effect is determined and a Memorandum of Agreement is
  required. Any acoustic treatment inside the Main Terminal head-house — or
  any tenant-audio governance that changes the acoustic character of the
  Saarinen space — is potentially in scope. That is a schedule risk the
  recommendation must own, particularly given the July 29 announcement
  explicitly preserved the Main Terminal. The AeroTrain extension and
  mobile-lounge retirement both touch adjacent-property questions. A
  standard whose reference application is Concourse E or DCA Terminal 1
  avoids most of this, but any later application to C/D or the Main
  Terminal must budget the consultation up front.
- **Remedy:** Add explicit language that the amendment applies to new-build
  and non-Saarinen-adjacent work first, and that any application within the
  eligible-district envelope requires Section 106 scoping as a precedent
  step. Add SHPO consultation to the dependency list, not to a parenthetical.

### 8. IROPS behavior of the standard is undefined — the standard will be violated on the first Nor'easter [FATAL]

- **Location:** Body l. 60 (mandatory-tier language); no IROPS section.
- **Charge:** The Joint Commission analogy is precisely the wrong end of the
  operating envelope. Hospitals set alarm policy for steady-state clinical
  operations. Airports face announcement floods during snow ops, ground
  stops, TSA equipment failures, and gate-hold events, when the passenger
  who needs the information is the passenger who cannot pull out a phone.
  A standard that specifies intelligibility floors, PA zoning, and audit-
  logged governance without explicit IROPS override, override-authority
  identification, and post-event reconciliation requirements will be
  violated the first Wednesday afternoon Concourse C degrades to gate
  holds. When the standard is violated as a normal operating necessity, its
  authority erodes for the events it was meant to govern. Every airport
  operator reading this will pattern-match to their own experience and
  discount the whole document if the IROPS behavior is not specified.
- **Remedy:** Add an IROPS section to the mandatory tier: (a) named override
  authority (typically Airport Duty Manager or equivalent), (b) permitted
  deviations during declared IROPS, (c) audit-log capture of the deviation,
  (d) post-event reconciliation reporting to the governance body. Without
  this the standard is naïve about the environment.

### 9. Ownership of commissioning and ongoing verification is unassigned [CONDITION]

- **Location:** Owner block l. 76 ("Office of Engineering (drafting
  authority)"); no assignment for verification, commissioning, or ongoing
  audit.
- **Charge:** Engineering drafts the standard. Who signs off on
  commissioning under representative traffic? Who owns the audit-log
  governance body the "Governance is the technology" section calls for?
  MWAA has an Operations organization at each airport; there is a
  Communications Center; there is IT; there is a Facilities function. None
  is named. The Joint Commission analogy has a specific institutional
  answer — every hospital has an alarm-management committee reporting to
  patient safety. The draft's airport analogue is unnamed. Without a
  standing owner the standard becomes an artifact rather than a running
  discipline.
- **Remedy:** Name owners: Engineering for standard content and revision;
  Operations (airport by airport) for commissioning acceptance under
  representative traffic; a standing Announcement Governance Committee
  (co-chaired Engineering / Operations / Communications / IT, with a rotating
  air-carrier member) for audit-log review and template control. Add annual
  reporting to the Business Administration Committee of the Board.

### 10. Staffing implication is not scoped [CONDITION]

- **Location:** Not present.
- **Charge:** Audit-logged governance, commissioning verification under
  representative traffic, and tenant-audio compliance oversight are all
  labor. The draft implies but does not name new MWAA workload. If the
  standard adds 0.5 to 1.0 FTE across Engineering, Operations, and IT at
  each airport for governance and verification, that is a real budget line.
  If it adds acoustic-consultant retainer costs, that is another. Neither is
  in the cost stack. A CFO reading the recommendation will ask; a labor
  reader (AFGE and other represented workforce at MWAA) will read carefully
  to see whether new duties are assigned to represented positions without
  bargaining.
- **Remedy:** Add an FTE estimate to the cost stack — a range is fine.
  Identify whether new duties fall inside existing position descriptions or
  trigger reclassification/bargaining. If tenant-audio compliance is added
  to an existing MWAA station manager or airline liaison position, name it.

### 11. FAA and AHJ concurrence is a footnote where it should be a step [CONDITION]

- **Location:** Dependencies l. 84 ("FAA/AHJ concurrence on NFPA 72 edition
  in force").
- **Charge:** The Virginia Statewide Fire Prevention Code and the DC
  building code adopt NFPA 72 on independent cycles. IAD sits in Loudoun/
  Fairfax; DCA sits in DC. The AHJs are different. The edition in force is
  different. The Fire Marshal at each airport is the person who accepts
  commissioning under the emergency-voice provisions. If the amendment
  specifies STI floors above the AHJ-adopted edition, the standard is
  MWAA-imposed and enforceable only under MWAA authority; if below, MWAA is
  in conflict. Neither is discussed. FAA Part 139 emergency-communications
  requirements are similarly named but not walked through — Part 139
  inspection is annual, and any deviation from as-designed emergency PA
  performance is a finding.
- **Remedy:** Confirm the NFPA 72 edition in force at each AHJ before
  drafting mandatory language, and structure the amendment as "MWAA
  requirement, in addition to the AHJ-adopted edition" with a compliance
  matrix. Add Fire Marshal briefings to the 90-day plan and Part 139
  compliance review to the standing verification cycle.

### 12. Leading indicator is a paperwork event, not an outcome signal [REFINEMENT]

- **Location:** Leading indicator block, l. 86 ("First eligible major
  terminal-package scope documents released with mandatory quiet-by-design
  language cited by section").
- **Charge:** That is a document-milestone indicator, useful for tracking
  drafting completion but silent on whether the standard is working. An
  outcome-leading indicator would be commissioned STI and ambient readings
  under representative traffic at Concourse E on opening, compared against
  the ACRP 175 band and the NFPA 72 floor; and, once at least one
  amendment-governed project reaches TCO, the commissioning cure-period
  cost delta relative to a comparable non-amendment project. A CEO who
  reads only the leading indicator on a dashboard should see whether the
  standard is producing the outcome the case was built on.
- **Remedy:** Add two leading indicators alongside the paperwork one:
  (a) Concourse E commissioned STI baseline under representative traffic
  within 90 days of opening; (b) missed-boarding, service-recovery, and
  ADA-effective-communication complaint rates at any facility subject to
  the amendment, benchmarked against non-amendment facilities.

### 13. Stop conditions cover the amendment but not the standard's application [CONDITION]

- **Location:** Failure mode / stop condition block, l. 88.
- **Charge:** All three stop conditions address whether to adopt the
  amendment. None address stopping application once adopted. If the
  Concourse E baseline reading shows existing MWAA design already meets
  ACRP 175 and NFPA 72 under representative traffic, the cost-avoidance
  case collapses for the balance of the program, and the standard's
  application should contract to governance and IROPS behavior only. If an
  early commissioning cure-period triggers unrecoverable MWAA cost above a
  named threshold, the amendment's TCO-adjacent language must be rewritten.
  Neither branch is in the recommendation.
- **Remedy:** Add two application-side stop conditions: (a) Concourse E
  baseline meets ACRP 175 under representative traffic → mandatory
  application contracts to governance and IROPS behavior; the acoustic
  performance section becomes recommended practice pending measured cause.
  (b) First cure-period cost exceeds $X per project (name the threshold) →
  Engineering issues a hold on further application pending amendment
  language revision.

### 14. Political framing understates the "reducing safety broadcasts" attack surface [CONDITION]

- **Location:** Body ll. 32, 42; Executive Summary l. 32.
- **Charge:** The draft correctly refuses the "silent airport" framing and
  argues intelligibility as the variable. That framing works for peer
  executives; it does not survive a 45-second cable-news segment or a
  hostile local reporter's paraphrase after any DCA incident. Two additional
  political armors are needed and are not present: (a) an explicit
  MWAA-communications position that any external reference to the standard
  uses the phrase "communications-integrity standard," never "quiet by
  design," in board and press materials — the internal engineering name and
  the external policy name should be separated; (b) a coordination step
  with the DOT Office of Public Affairs given the July 29 co-brand, so the
  standard is not read as MWAA quietly walking away from the transformation
  scope. Neither is trivial and neither is called out.
- **Remedy:** Add a communications-and-public-affairs step to the 90-day
  plan: name the external framing convention; brief DOT and White House
  liaison at the appropriate seniority given the July 29 stack; brief the
  Airports Council and A4A given cross-industry press interest.

### 15. Tenant-audio governance mechanics remain a design objective without an enforcement architecture [CONDITION]

- **Location:** Body ll. 56, 64; Dependencies l. 84.
- **Charge:** The evidence pass forced honest hedging on tenant reach —
  present-tense claims became design objectives contingent on AUL
  verification. That is correct on evidence. It leaves a governance
  vacuum. Even if the AUL and tenant-technology-standards apparatus does
  reach airline holdroom audio in principle, MWAA still needs a live
  enforcement architecture: an inspection cycle, a violation ladder, a
  consequences schedule that is credible without being punitive on Day 1.
  Airlines will read a standard without those mechanics as a paper
  requirement and will comply nominally. Concessionaires will do the same
  with holdroom-adjacent audio. The Joint Commission analogy again — the
  hospital analogue works because Joint Commission survey findings have
  accreditation consequences. MWAA's analogue is smaller and needs to be
  named.
- **Remedy:** Sketch the enforcement architecture even if the AUL text is
  not yet verified: annual acoustic inspection cycle keyed to lease renewal
  or Tenant Technology Standards audit; violation notice with 30/60/90-day
  cure; escalation to lease-management action only for documented pattern
  noncompliance; annual public MWAA Announcement Governance Report to the
  Board. That framework can be drafted before the AUL text is closed and
  will inform the AUL consultation.

### 16. The recommendation does not address what the standard says about televisions and concessions media [REFINEMENT]

- **Location:** Body ll. 60 (mandatory tier lists PA zoning, ADS mapping,
  intelligibility floors, accessibility, hearing conservation, governance).
- **Charge:** The run prompt lists "televisions and media" as a scope item;
  the airport-context packet flags the same. Concessionaire televisions and
  gate-lounge feeds are among the loudest ambient contributors in a
  terminal. A quiet-by-design standard silent on television and concessions
  media is under-scoped against its own charter. This is not fatal — the
  amendment can be scoped to acoustic and PA-zoning content and defer
  television governance to a follow-on volume — but the scoping decision
  should be explicit.
- **Remedy:** Either add a "televisions and concessions media" line to the
  mandatory-tier list with concrete language (e.g., no ambient television
  audio in holdrooms except captioned displays, concessionaire audio
  contained to lease line ±X dB, closed-captioning required) or state
  explicitly that the amendment defers television governance to a
  subsequent Design Manual volume.

### 17. What-would-change-this-recommendation section is thin against evidence the Council would actually accept [REFINEMENT]

- **Location:** Ll. 90.
- **Charge:** Two evidence branches are named — a measured MWAA STI/ambient
  baseline showing existing spaces already meet the floors, and MWAA-
  published PA telemetry showing announcement density below peer-reduced
  bands. Both are on the MWAA side of the fence. Missing: (a) a peer-airport
  primary methodology (e.g., SFO Airport Commission publishes measured
  baseline showing negligible intelligibility change) — that would collapse
  the "no published methodology" argument and permit direct-copy operating
  patterns rather than fresh engineering; (b) an AUL-consultation outcome
  in which airlines commit to a shorter-form standard as a negotiation
  concession — that would reduce the amendment's marginal content; (c) FAA
  publication of Part 139 amendments touching PA and communications, which
  would move requirements outside MWAA's discretion.
- **Remedy:** Add those three branches to the "what would change" list.

### 18. The recommendation names Concourse E as the baseline site without naming the acoustic consultant, the measurement protocol, or the acceptance authority [CONDITION]

- **Location:** Body ll. 62; First 90 days item 5.
- **Charge:** Commissioning a first ADS map and baseline STI/ambient reading
  at Concourse E within 90 days of opening is a real deliverable. It is
  also a real procurement. Who does the measurement? Under what protocol
  (IEC 60268-16:2020 as measurement method, ACRP 175 as target, NFPA 72 as
  emergency floor)? Who accepts the report? Does the report become a
  Concourse E post-occupancy condition — which would create a live
  regulatory obligation? None of this is closed in the draft.
- **Remedy:** In the same 90-day plan item, name the procurement vehicle,
  the measurement protocol by reference, the acceptance authority (Engineering
  with concurrence from Operations and the Fire Marshal), and confirm the
  report's status (informational baseline, not a Concourse E TCO condition).

---

## What the evidence pass did not test (thematic summary)

- **Instrument and approval route.** Evidence review passed on citations,
  not on how the recommendation becomes an executable board or executive
  action. Findings 1, 2, 3.
- **Procurement.** No procurement path was tested; the amendment carries
  three distinct procurement obligations (professional services,
  technology, capital) each with independent timelines. Finding 4.
- **Funding source and CPE mechanics.** The evidence pass corrected the
  denominator; it did not test whether the cost stack is airline-recoverable,
  bond-financed, or PFC-eligible, or what the CPE motion actually is.
  Findings 5, 6.
- **Section 106, IROPS, and AHJ compliance.** All three are named as
  constraints and none are engineered into the recommendation. Findings 7,
  8, 11.
- **Staffing and standing ownership.** Governance-as-technology needs a
  named committee, an owner, and an FTE line. Findings 9, 10, 15.
- **Outcome leading indicators and application-side stop conditions.** The
  recommendation instruments its own drafting but not its own results.
  Findings 12, 13.
- **External communications and stakeholder posture.** Political framing
  and DOT coordination are load-bearing given the July 29 stack. Finding 14.
- **Scope integrity.** The run prompt lists televisions/media; the
  amendment lists them nowhere. Finding 16.

## Airport decision card — what the recommendation needs to include

The current draft has a decision block. Comparing against the executive
decision card this review requires:

| Card field | Draft status | Required remedy |
|---|---|---|
| Executive owner | Named (CEO, Engineering, Board) | Name the instrument and approval route (Finding 1) |
| Decision and approval route | Direction to draft | Name meeting cycle, Board action or delegation, AAAC consultation lane (Findings 1, 2) |
| First 90-day action | Five-item verification list | Extend to day 180 with branch logic; add airline consultation, procurement, DOT/press coordination (Findings 2, 3, 4, 14) |
| Cost order of magnitude and funding source | $12M–$40M one-time; funding source undefined | Split IAD/DCA, capital/operating, recoverable/non-recoverable, five-year O&M tail, funding candidates (Finding 5) |
| Airline / board / federal / procurement / labor / operational dependencies | Airline consultation and MII named; procurement, labor, IROPS, AHJ, Section 106 mechanics not developed | Findings 2, 4, 7, 8, 10, 11 |
| Leading indicator | Scope-document release | Add outcome indicators keyed to Concourse E baseline and complaint rates (Finding 12) |
| Failure mode / stop condition | Three amendment-side branches | Add two application-side branches (Finding 13) |
| What would change the recommendation | Two MWAA-side evidence branches | Add three external evidence branches (Finding 17) |

---

## Verdict

**NOT READY.**

The argument is unusually well-formed for a v2 draft, and the evidence pass
did its job. But the recommendation as written cannot be assigned, funded,
approved, procured, staffed, or operated without additional work. Five
findings are fatal in the executive sense — meaning a board member or CFO
reading the current text would send it back before voting: **F-1
(instrument and approval route absent), F-2 (airline consultation lane
missing), F-4 (procurement path unaddressed), F-5 (cost stack not a
budget), F-8 (IROPS behavior undefined).** Any one of these is enough to
force a re-work. The other findings are implementation conditions and
refinements that a competent Office of Engineering can absorb in the same
revision cycle.

The Strategist should not weaken the case. The case is sound. What it
needs is the operational scaffolding a chair-level reader will demand
before signing. Add the approval instrument, the airline lane, the
procurement path, a funding-source-aware cost stack, and an IROPS
paragraph — and this recommendation becomes READY WITH NAMED CONDITIONS
(Section 106 scoping, AHJ concurrence, tenant-audio enforcement architecture,
staffing FTE estimate, outcome leading indicators, application-side stop
conditions, external framing convention).

Ship the standard. Ship it as something a Board can adopt on a Wednesday.
