// Build the 3-page Executive Summary Word document.
// Standalone distillation of the full report. ~1,100 words.

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType,
  LevelFormat, PageBreak, PageNumber, BorderStyle, HeadingLevel,
} = require('docx');

const OUT = '/Users/cgkiv/Documents/GitHub/ai-council/outputs/stage4/sterile-corridor-resilience-executive-summary.docx';

const runs = (parts, spacingAfter = 160) => new Paragraph({
  spacing: { after: spacingAfter, line: 300 },
  alignment: AlignmentType.LEFT,
  children: parts.map(p => {
    if (typeof p === 'string') return new TextRun({ text: p, size: 22, font: 'Calibri' });
    return new TextRun({ size: 22, font: 'Calibri', ...p });
  }),
});

const sectionHead = (text) => new Paragraph({
  spacing: { before: 280, after: 140 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 4 } },
  children: [new TextRun({
    text: text.toUpperCase(),
    bold: true, size: 22, font: 'Calibri',
    characterSpacing: 40,
    color: '1F2937',
  })],
});

// ---------- title block ------------------------------------------------------
const titleBlock = [
  new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: '', size: 16 })] }),

  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [new TextRun({
      text: 'EXECUTIVE SUMMARY',
      size: 18, font: 'Calibri', characterSpacing: 60,
      color: '6B7280', bold: true,
    })],
  }),

  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({
      text: 'Sterile Corridor Design as a Resilience Problem',
      bold: true, size: 40, font: 'Calibri', color: '111111',
    })],
  }),

  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 160 },
    children: [new TextRun({
      text: 'Why throughput and recovery — not code compliance — should govern the next generation of sterile circulation at IAD',
      italics: true, size: 24, font: 'Calibri', color: '4B5563',
    })],
  }),

  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 320 },
    border: {
      top: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 8 },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 8 },
    },
    children: [new TextRun({
      text: '    Transform Airports AI Council    ·    May 28, 2026    ',
      size: 18, font: 'Calibri', color: '6B7280', characterSpacing: 30,
    })],
  }),
];

// ---------- content ----------------------------------------------------------
const content = [
  runs([
    'At 6:45 a.m. on a Tuesday in February, the Concourse C escalator bank at Dulles is doing the work it does most mornings — moving roughly two hundred passengers from an AeroTrain that arrived at 6:39 up to the sterile concourse level. One of the two escalators is running rough. A cleaning crew is past their scheduled clearance window. TSA is at three of four lanes. Nothing is broken. Everything is marginal. This is the baseline. The thesis is about what the baseline looks like in 2036.',
  ]),

  runs([
    { text: 'The thesis. ', bold: true },
    'Sterile corridor design at major US hub airports is governed by code minimums and a fifty-year-old pedestrian flow framework that was never built for what these corridors are now asked to do. The specific failure modes worth worrying about are not slow congestion at peak but binary vertical-circulation failures at automated people mover (APM) handoffs, whose 1990s installed base is now reaching end-of-life simultaneously across the midfield generation of US hubs. MWAA, with the Tier 2 program in active construction and a $22 billion revitalization concept under DOT review with no confirmed federal funding mechanism, has perhaps eighteen months before the next generation of sterile circulation at IAD locks in for thirty years.',
  ]),

  sectionHead('The empirical case'),

  runs([
    { text: 'The Level of Service framework lies under load. ', bold: true },
    'A 2018 PLOS One synthesis found bidirectional pedestrian flow capacity clusters around 1.5 persons per meter per second versus roughly 2.0 for unidirectional flow — a 25 percent reduction. A corridor rated LOS C on a design drawing is operating at functional LOS D during the dominant directional surge of an AeroTrain discharge. Add a parallel cleaning-cart obstacle (16 percent density concentration, per a 2019 Physica A controlled study) and roll-aboard luggage (3 to 8 percent walking-speed reduction, per Seth Young’s 1999 TRB study), and the design grade becomes a fictional one.',
  ]),

  runs([
    { text: 'The industry has formally disavowed its own design dataset. ', bold: true },
    'ACRP Problem Statement 24-1058 (FY2024) states that the pedestrian-flow formulas underlying current design "were created in the 1970s" and "do not account for demographic trends or increased prevalence of roll-aboard luggage." FAA Advisory Circular 150/5360-13A continues to reference the unflagged tables as the design starting point. The empirical foundation of the design conversation is a 1970s framework that the industry’s own research program has acknowledged is no longer valid.',
  ]),

  runs([
    { text: 'No airport has validated its design simulations against measured operations. ', bold: true },
    'A 2025 ACM literature review found no published post-occupancy comparison anywhere between pre-opening pedestrian simulation predictions and measured corridor throughput. MassMotion, AnyLogic, and SimWalk are used to certify designs and then never reopened. The industry designs to a model it has never validated.',
  ]),

  runs([
    { text: 'Denver is confessing the previous generation’s mistake at three-quarters of a billion dollars. ', bold: true },
    'DEN announced in May 2026 a $300 to $700 million pedestrian-walkway program to add redundancy to its underground APM after 31 years of single-mode operation. CEO Phil Washington described the program as breaking "the airport’s dangerous over-reliance on aging train networks." The 1995 decision to build without pedestrian redundancy was a design choice. It is now being corrected at three-quarters of a billion dollars exclusive of three decades of distributed operational cost that never appeared in any capital line. IAD’s AeroTrain opened in 2010. The clock is running.',
  ]),

  sectionHead('The IAD-specific stakes'),

  runs([
    'The IAD midfield concourses (A/B 1997, C/D 2000) were sized for late-1990s United hub operations, and the AeroTrain was retrofit onto a sterile envelope already a decade old when it opened in 2010 — the handoff geometry was not designed as a whole. Vertical circulation installed between 1997 and 2004 is now at or past practical service life. The next capital cycle, roughly 2027 to 2035 in MWAA’s CIP framing, is the window. If it closes without resetting corridor geometry and vertical-circulation redundancy at the AeroTrain handoffs, the next opportunity is 2040-plus.',
  ]),

  runs([
    'The cleanest version of the resilience question is not daily peak performance. It is what happens when the AeroTrain fails for four hours — weather, mechanical, propulsion-system, fire-alarm cascade. The bus alternative is designed to bridge a brief gap. It is not designed for four-hour duration. The single-mode APM is the failure mode DEN is now spending its way out of. IAD has not yet bought.',
  ]),

  sectionHead('The counter-case, honestly'),

  runs([
    'The path-dependence argument is the strongest objection and partially succeeds. DCA Project Journey (2019-2021) reconfigured sterile corridor geometry in an occupied concourse without a day of full closure. Corridors are not physically immutable. What in-place renovation cannot change at any cost the rate base will tolerate is the structural envelope itself — the column grid, the inherited MEP chase, the bay spacing. The bounded version of the thesis is a financial claim, not a structural one: in-place renovation costs roughly 1.5 to 2.5 times greenfield per ACRP Report 25, and 3 to 5 times for the narrower category of mid-life vertical circulation replacement at sterile-side handoffs where construction windows are tightest. The window reopens, but only once per generation, because the cost of opening it more often is what the political and financial system will not tolerate.',
  ]),

  runs([
    'The checkpoint-trade-off objection is correct in the middle of the failure distribution and wrong at the tail. Checkpoint capital moves the median; corridor and vertical-circulation capital compresses the tail. Both are valid. Neither substitutes for the other. The political objection — a $22 billion proposal absorbs the conversation, the PFC cap will not move, MWAA leadership has institutional reasons to avoid invisible-infrastructure capital — is real and unfavorable but does not change the underlying physics.',
  ]),

  sectionHead('What MWAA should do'),

  runs([
    { text: 'Instrument Tier 2 East at opening. ', bold: true },
    'Xovis 3D stereo-optical sensors at the vertical circulation nodes; Veovo or BlipTrack flow tracking through the connector segments. Likely low single-digit millions against a concourse program in the hundreds of millions. The value is the first published post-occupancy throughput baseline for an AeroTrain handoff at IAD against the simulation predictions that justified the design. Without it, the next capital request for handoff capacity has no empirical foundation.',
  ]),

  runs([
    { text: 'Fund the Concourse C escalator now. ', bold: true },
    'A third escalator or a second elevator bank at the AeroTrain connection is the cheapest legible capital intervention against the documented failure mode. The figures in the briefs bracket $3 to $12 million depending on scope — small enough to fit inside a state-of-good-repair allocation rather than requiring a discrete MII vote.',
  ]),

  runs([
    { text: 'Bundle corridor resilience scope into the $22 billion program. ', bold: true },
    'A freestanding corridor resilience investment will not survive the political moment. The $3.75 billion central-spine concept under DOT review should expand to include vertical circulation at handoff points and parallel sterile-side pedestrian paths between concourses, structured as a hub-efficiency investment with explicit connect-time analysis United’s network planning team will credit. Hub efficiency is the framing that produced United’s buy-in at DEN. It is the framing that survives.',
  ]),

  runs([
    { text: 'Use the lease renewal window to restructure how corridor capital is classified. ', bold: true },
    'Sterile circulation that follows preferential gate clusters should be treated as preferential infrastructure rather than common-use — the only structural change that aligns the carrier whose banking operation drives the demand with the cost of meeting that demand. Instrumentation makes the conversation possible.',
  ]),

  sectionHead('The question, stated once'),

  runs([
    'The Tier 2 East concourse opens in September 2026 with corridor geometry that will be the corridor geometry of IAD for thirty years. The smallest, cheapest, and most consequential decision left in the program is whether to instrument that geometry on opening day, against the simulations that justified it. The 7:39 bank ten years from now is the one that should be on the board’s mind. The 6:45 a.m. scene is the one already on the operator’s.',
  ], 240),

  new Paragraph({
    spacing: { before: 240, line: 280 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 8 } },
    children: [new TextRun({
      text: 'Executive summary of an 8,200-word report produced by the Transform Airports AI Council. Every numerical claim traces to a primary research brief or a disclosed analyst construction. The full report and methodology appendix are available under separate cover.',
      italics: true, size: 18, font: 'Calibri', color: '6B7280',
    })],
  }),
];

// ---------- document ---------------------------------------------------------
const doc = new Document({
  creator: 'Transform Airports AI Council',
  title: 'Sterile Corridor Design as a Resilience Problem — Executive Summary',
  description: 'Three-page executive summary of the full report',
  styles: {
    default: {
      document: { run: { font: 'Calibri', size: 22 } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1296, right: 1440, bottom: 1296, left: 1440 },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: 'Executive Summary  ·  ',
              size: 16, font: 'Calibri', color: '9CA3AF',
            }),
            new TextRun({ children: [PageNumber.CURRENT], size: 16, font: 'Calibri', color: '9CA3AF' }),
            new TextRun({ text: ' / ', size: 16, font: 'Calibri', color: '9CA3AF' }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, font: 'Calibri', color: '9CA3AF' }),
          ],
        })],
      }),
    },
    children: [...titleBlock, ...content],
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUT, buffer);
  const stat = fs.statSync(OUT);
  console.log(`Wrote ${OUT}`);
  console.log(`Size: ${(stat.size / 1024).toFixed(1)} KB`);
}).catch(err => {
  console.error('Pack error:', err);
  process.exit(1);
});
