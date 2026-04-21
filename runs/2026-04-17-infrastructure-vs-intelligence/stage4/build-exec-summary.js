// Build the 3-page Executive Summary Word document.
// Standalone version of the argument, tuned for a sophisticated reader.

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType,
  LevelFormat, PageBreak, PageNumber, BorderStyle, TabStopType, TabStopPosition,
  HeadingLevel,
} = require('docx');

const OUT = '/Users/christiankessleriv/Repos/ai-council-mwaa/outputs/stage4/infrastructure-vs-intelligence-executive-summary.docx';

// Light helpers ---------------------------------------------------------------
const body = (text, opts = {}) => new Paragraph({
  spacing: { after: 160, line: 300 }, // 1.25x line spacing
  alignment: AlignmentType.LEFT,
  children: [new TextRun({ text, size: 22, font: 'Calibri', ...opts })],
});

const runs = (parts, spacingAfter = 160) => new Paragraph({
  spacing: { after: spacingAfter, line: 300 },
  alignment: AlignmentType.LEFT,
  children: parts.map(p => {
    if (typeof p === 'string') return new TextRun({ text: p, size: 22, font: 'Calibri' });
    return new TextRun({ size: 22, font: 'Calibri', ...p });
  }),
});

const blank = () => new Paragraph({ spacing: { after: 80 }, children: [new TextRun('')] });

// Section header (small caps style via formatting)
const sectionHead = (text) => new Paragraph({
  spacing: { before: 280, after: 140 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 4 } },
  children: [new TextRun({
    text: text.toUpperCase(),
    bold: true, size: 22, font: 'Calibri',
    characterSpacing: 40, // letter-spacing for elegant small-caps feel
    color: '1F2937',
  })],
});

// ---------- title block ------------------------------------------------------
const titleBlock = [
  // top spacer
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
      text: 'Infrastructure vs. Operational Intelligence',
      bold: true, size: 44, font: 'Calibri', color: '111111',
    })],
  }),

  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 160 },
    children: [new TextRun({
      text: 'Why the next billion dollars of airport CapEx deserves a harder test',
      italics: true, size: 26, font: 'Calibri', color: '4B5563',
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
      text: '    MWAA AI Council    \u00B7    April 17, 2026    ',
      size: 18, font: 'Calibri', color: '6B7280', characterSpacing: 30,
    })],
  }),
];

// ---------- content ----------------------------------------------------------
const content = [
  // Opening
  runs([
    'US airports are spending against a physical problem they diagnosed two decades ago, while a material share of the binding throughput constraint has migrated to coordination, staffing, and software. The industry\u2019s own trade body reports global airport return on invested capital below its weighted average cost of capital. The 2024 Airports Council International outlook calls for $2.4 trillion in global CapEx through 2040 on that basis. Something has to change, or the trajectory underwrites value destruction at scale.',
  ]),

  runs([
    { text: 'The thesis is narrow. ', bold: true },
    'The discretionary portion of the next billion in airport CapEx \u2014 the portion not driven by pavement compliance, safety mandates, or irreducible physical overload \u2014 should have to clear a defeat test. That test: whether a much smaller operational intelligence investment, applied first, could compress apparent demand for the physical project enough to stage, defer, or resize it. Most US hubs do not run that test. This paper argues they should.',
  ]),

  sectionHead('The evidence'),

  runs([
    { text: 'The economics do not work at the top of the stack. ', bold: true },
    'Airport ROIC sits below WACC by the sector\u2019s own reporting. Total 2024 global airport revenue ran 2.1% below pre-pandemic levels in real terms even while traffic was 4% above 2019 \u2014 the industry raised capital faster than it raised margin. Flyvbjerg\u2019s 258-project transport dataset finds 86% of megaprojects overrun, at 28% on average. Berlin Brandenburg ran 132% over and nine years late. The LAX APM is 76% over with no opening date. Denver\u2019s Great Hall is roughly three times original city exposure. Heathrow Terminal 5 is the counter-case, and its lesson is governance, not category feasibility.',
  ]),

  runs([
    { text: 'The current US delay picture is not primarily a runway picture. ', bold: true },
    'FAA data attribute 74% of system-impacting delays to weather and 15% to volume. Flight-level data attribute 39% of delayed minutes to late-arriving aircraft and 35% to carrier causes. Nineteen of the thirty largest ATC facilities operate below 85% of staffing targets and produce 40% of all National Airspace System delays. None of this changes with a new concourse.',
  ]),

  runs([
    { text: 'Operational interventions have delivered independently validated gains. ', bold: true },
    'Wake-turbulence re-categorization at Memphis: a 15%-plus capacity increase, nine added movements per hour, no construction. Time-Based Separation at Heathrow: a 62% first-year reduction in headwind delays. EUROCONTROL\u2019s Airport Collaborative Decision-Making assessment across 17 European airports: 34,000 tonnes of fuel saved annually and 250,000 minutes of flow delay avoided \u2014 independently audited, not vendor-reported. These are not forty-percent marketing figures. They are mid-single-digit to low-double-digit gains at a fraction of megaproject cost.',
  ]),

  runs([
    { text: 'The optionality asymmetry is decisive. ', bold: true },
    'A badly executed A-CDM deployment is recoverable in tens of millions and a few years. A badly sited concourse is a balance-sheet obligation for thirty. Commit operational intelligence first and you learn what physical investment the higher operational baseline actually requires. Commit infrastructure first and you foreclose the test.',
  ]),

  sectionHead('The counter-case, honestly'),

  runs([
    'The strongest objection is that physical ceilings are real and software is not geography. LaGuardia is capped at 71 operations per hour. DCA is at a federal cap of 62 per hour inside a hard physical perimeter. Denver processes 82 million passengers through infrastructure built for 50 million. Where the binding constraint is geometry, infrastructure is the right answer.',
  ]),

  runs([
    'NextGen is the second objection: $15 billion of federal investment, the DOT Inspector General finding 16% of projected benefits delivered. That program is a real warning \u2014 about federal IT governance on a multi-decade scope, not about airport-level commercially productized deployments over 24 to 36 months. The comparison class for airport A-CDM is Munich and Heathrow, not NextGen.',
  ]),

  runs([
    'Most of the $151 billion ACI-NA infrastructure need is mandatory safety, security, accessibility, and asset renewal. The allocation argument does not touch that spend. It applies to the discretionary tranche \u2014 the portion that passes neither a compliance test nor a genuine capacity-ceiling test.',
  ]),

  sectionHead('What this means for MWAA'),

  runs([
    'MWAA operates an airport at a federal-and-physical cap and an airport with physical room but exposed hub economics. The allocation test applies to both, in different forms.',
  ]),

  runs([
    { text: 'DCA. ', bold: true },
    'The $2.4 billion Project Journey program responds to a real constraint \u2014 a terminal designed for 15 million passengers now serving 25 million. Most of that envelope is structural renewal, accessibility, security, and baggage. A residual tranche, sized by the authority\u2019s own capital plan, is discretionary: gate count beyond the slot cap, hold-room footprint beyond federal minimums, concession and amenity build-out. That residual should have to clear a defeat test against a paired operational intelligence program \u2014 queue prediction, biometric flow, predictive gate allocation, and the unified operational data backbone that makes the three cohere.',
  ]),

  runs([
    { text: 'IAD. ', bold: true },
    'Dulles has physical room. It also has a debt service coverage ratio projected to fall from 2.79x in FY2024 to 1.70x by FY2030 under favorable assumptions. The Concourse E demand-contingent tranche \u2014 the portion justified by forecast international growth \u2014 is the second test case. Its test partner is a regional A-CDM deployment paired with DCA, benchmarked to Munich\u2019s 9% taxi-time reduction as a floor.',
  ]),

  runs([
    { text: 'The envelope. ', bold: true },
    'The system-level operational intelligence investment, component-anchored to the research briefs, lands at $50-150M over 36 months. That is 0.6 to 1.7% of MWAA\u2019s $9 billion capital plan, or roughly one-sixth to one-ninth of the discretionary tranche it would condition. Large enough to matter if it succeeds. A rounding error if it does not.',
  ]),

  runs([
    { text: 'The mechanism. ', bold: true },
    'A pre-registered defeat test. If by month 24 a named operational KPI moves by a named amount sustained over six months, a named infrastructure sub-tranche is deferred, resized, or cancelled per a formula signed at contract. If the KPI does not move, an independent adjudicator \u2014 not the authority, not the vendor \u2014 determines whether the failure was architectural, execution, or environmental. Only environmental failure unlocks the infrastructure spend on original terms.',
  ]),

  sectionHead('The question, stated once'),

  runs([
    'The bond market, the rating agencies, and the authority\u2019s own DSCR trajectory now require that the allocation question be answered on the record rather than assumed away. The next roughly $1-3 billion of discretionary MWAA CapEx is going to get decided. It should be decided knowing what $50-150M of operational intelligence would have done first, and knowing the answer is not allowed to be "we didn\u2019t ask."',
  ], 240),

  // Closing italic note
  new Paragraph({
    spacing: { before: 240, line: 280 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 8 } },
    children: [new TextRun({
      text: 'Executive summary of an 11,600-word report produced by the MWAA AI Council. Every numerical claim traces to a primary research brief or a disclosed analyst construction. The full report and methodology appendix are available under separate cover.',
      italics: true, size: 18, font: 'Calibri', color: '6B7280',
    })],
  }),
];

// ---------- document ---------------------------------------------------------
const doc = new Document({
  creator: 'MWAA AI Council',
  title: 'Infrastructure vs. Operational Intelligence \u2014 Executive Summary',
  description: 'Three-page executive summary of the full report',
  styles: {
    default: {
      document: { run: { font: 'Calibri', size: 22 } }, // 11pt
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 }, // US Letter
        margin: { top: 1296, right: 1440, bottom: 1296, left: 1440 }, // 0.9"/1" margins
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({
              text: 'Executive Summary  \u00B7  ',
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
