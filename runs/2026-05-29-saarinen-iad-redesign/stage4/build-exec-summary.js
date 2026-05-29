// Build the 3-page Executive Summary Word document.
// Standalone distillation of the full report. ~1,100 words.

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType,
  LevelFormat, PageBreak, PageNumber, BorderStyle, HeadingLevel,
} = require('docx');

const OUT = '/Users/cgkiv/Documents/GitHub/ai-council/outputs/stage4/saarinen-iad-redesign-executive-summary.docx';

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
      text: 'If Saarinen Were Designing Dulles Today',
      bold: true, size: 40, font: 'Calibri', color: '111111',
    })],
  }),

  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 160 },
    children: [new TextRun({
      text: 'A position paper on what a faithful reinterpretation of Saarinen’s design philosophy would, and would not, ask of MWAA’s $22 billion revitalization program',
      italics: true, size: 22, font: 'Calibri', color: '4B5563',
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
      text: '    Transform Airports AI Council    ·    May 29, 2026    ',
      size: 18, font: 'Calibri', color: '6B7280', characterSpacing: 30,
    })],
  }),
];

// ---------- content ----------------------------------------------------------
const content = [
  runs([
    'In 1959, Eero Saarinen carried a stopwatch. So did his staff. They flew to other airports and timed themselves walking from curb to gate, and came back with a number: 900 feet was the average walk at comparable airports of the period. The Civil Aeronautics Administration had calculated that a conventional terminal sized to the projected build-out at Chantilly would require concourses more than 8,000 feet end to end — a mile and a half of finger pier. Saarinen’s response was engineered substitution: bring the aircraft to the passenger by vehicle, keep the building short enough that 900 feet became 200. The mobile lounge was the conclusion of empirical research, not formal experiment. The stopwatch was the philosophy.',
  ]),

  runs([
    { text: 'The thesis. ', bold: true },
    'Saarinen’s IAD encoded design principles — separable from his catenary roof and his mobile lounge — that are partially correct in 2026 and partially obsolete. The compact single-building principle is obsolete: at IAD’s 30-million-passenger scale, a faithful Saarinenian response is a new building, not a renovated 1962 one. Modal clarity, midfield apron flexibility, the deliberate-arrival sequence, and — above all — the empirical method that produced them remain valid and have been systematically violated by every subsequent IAD capital decision. MWAA’s $22 billion revitalization concept, presented to airlines in May 2026 with no confirmed federal funding mechanism, will lock in IAD’s sterile-circulation architecture for thirty years. A faithful reinterpretation of Saarinen’s design philosophy would make materially different choices than the current master plan, in specific identifiable ways, before the bond schedule forecloses them.',
  ]),

  sectionHead('The case'),

  runs([
    { text: 'Saarinen’s design was operationally derived, not aesthetically imposed. ', bold: true },
    'More than a year of stopwatch-timed passenger-flow studies preceded the mobile-lounge concept. The Saarinen office reviewed over 100 program alternatives. The catenary roof was the visible signature of the building; the empirical method was its design philosophy. The two are analytically separable. Treating them as one is the category error the architectural-philosophical conversation has been making for sixty years.',
  ]),

  runs([
    { text: 'The mobile lounge worked for 23 years and broke arithmetically in 1985. ', bold: true },
    'It was operationally coherent for a terminating-passenger airport at 2 to 3 million annual passengers, the regulated-era traffic Saarinen designed for. It failed when United’s 1986 hub launch made simultaneous multi-gate dispatch necessary. The lesson is not that Saarinen was wrong about modal separation. The lesson is that he was right about the principle and wrong about the vehicle. The AeroTrain is the correct architecture, improperly completed.',
  ]),

  runs([
    { text: 'TWA and Dulles are opposite buildings by the same architect. ', bold: true },
    'TWA at JFK optimized for emotional experience and failed operationally, closing in 2001. Dulles optimized for correct problem-solving and has operated for 64 years. Any claim that "Saarinen’s principles" guide the current debate must specify which Saarinen — the expressionist of TWA or the problem-solver of Dulles. The expressionist Saarinen does not generalize. The problem-solver Saarinen does, and that is the version the thesis rescues.',
  ]),

  runs([
    { text: 'The current $22 billion plan repeats the documented Pittsburgh 1992 failure pattern, moderated. ', bold: true },
    'Pittsburgh built a $1 billion hub terminal for US Airways at 80% market share; the carrier dehubbed in 2004; enplanements fell 57% by 2013 and 12 of 25 Concourse B gates were boarded up. IAD’s $22 billion plan designs four new linear concourses around United at roughly 70% landed weight. The Washington-region traffic base, the Lufthansa joint venture, the DCA slot constraint, and IAD’s diplomatic-gateway role moderate the risk. They do not eliminate it. The plan moves IAD in the wrong direction on the dimension that matters most.',
  ]),

  runs([
    { text: 'The cost-per-enplanement math is the binding financial constraint. ', bold: true },
    'IAD’s signatory CPE in 2025 is $11.17. The $22 billion concept implies $90.64 by 2035 — a roughly seven-fold increase. United abandoned IAD as a competitive hub in the early 2000s at $26.47 CPE. MWAA’s debt-service coverage ratio is projected to compress toward 1.3x against a 1.25x covenant under the existing $9 billion capital program alone. The financial envelope for adding design-philosophical ambition to the program is small. It exists. It is shrinking.',
  ]),

  sectionHead('The counter-case, honestly'),

  runs([
    'The strongest objection is that the entire framing is sophisticated nostalgia: Saarinen’s mobile-lounge concept failed; his TWA building was preserved only by abandoning its function; the architectural-philosophical conversation about airports has been displaced by infrastructure-engineering because the building type changed, not because architects got worse. The Journal of Architecture argued in 2005 that reevaluating Saarinen risks "heroicisation, compensation, and coronation" — the architectural-history community already identified the romanticization risk. The Calatrava Oculus is the cautionary tale of civic-monumental ambition with the empirical-research discipline removed: $4 billion against a $2 billion budget, an $80 million architect fee, a skylight that opens once per year. Civic ambition without the stopwatch is the documented failure mode of the field this paper is asking MWAA to enter.',
  ]),

  runs([
    'These objections are real and partially win. The compact-single-building principle is genuinely obsolete — the chief engineer’s assessment is that the existing structural type cannot be internally reorganized for jetbridge operations; that is a new-building question stated in the language of renovation. What survives is narrower: the empirical method that produced Saarinen’s design choices is the most transferable element, and the part the current $22 billion plan most conspicuously lacks. Modal clarity remains valid as a principle; mobile lounges do not as a mechanism. The AeroTrain, properly extended and completed, is the more faithful Saarinenian vehicle than the mobile lounge it replaced — not because Saarinen would have endorsed it, but because the underlying structural logic of modal separation survives only when its vehicle scales.',
  ]),

  sectionHead('What MWAA should do'),

  runs([
    { text: 'Commission a 60-to-90-day empirical study before bond commitment. ', bold: true },
    'A focused study of named flows — curb to checkpoint to AeroTrain to gate; international arrivals through CBP through baggage to landside; specific United and Star Alliance connect-bank micro-sequences — is the operational instrument that makes the Saarinen-philosophy claim concrete. The cost is rounding error against the $22 billion envelope. The output conditions every subsequent move. This is the methodological precondition for a faithful reinterpretation, not a substitute for one.',
  ]),

  runs([
    { text: 'Negotiate design-quality obligations into the project-specific Programmatic Agreement. ', bold: true },
    'The PA being developed for the terminal/concourse redevelopment Environmental Assessment can embed design-quality obligations in a legally binding document if MWAA negotiates for it. The 300-foot terminal extensions’ interior organization is the most accessible entry point in the live program for the Saarinen-philosophy frame. The PA is the lever. It is currently being pulled too gently.',
  ]),

  runs([
    { text: 'Treat the FIS facility as the most-Saarinenian move in the program. ', bold: true },
    'International arrivals — the transition between systems of governance, the longest dwell, the highest probability of a first impression — is the location where the civic-arrival principle has the most operational room to land in 2026. CBP’s Airport Technical Design Standards specify a default. The default produces a generic FIS hall. A specific Saarinen-philosophy alternative, designed against the default rather than into it, is achievable inside the existing program scope.',
  ]),

  runs([
    { text: 'Lock the C/D demolition date in the Use and Lease Agreement amendment. ', bold: true },
    'The temporary Concourses C and D have operated for 40+ years. The November 2025 mobile-lounge collision injuring eighteen is the moment heritage stopped being viable as an argument for retention. A specific demolition date — written into the U&amp;L Agreement amendment, not deferred to subsequent program phases — is the cleanest way to convert a 40-year operational liability into a committed schedule.',
  ]),

  runs([
    { text: 'Add a carrier-concentration cap as a board-policy condition on the $22 billion program. ', bold: true },
    'The Pittsburgh 1992 failure mode is structural, not contingent. A non-binding board policy committing MWAA to evaluate the program scope against a sensitivity case where United’s share falls below 50% over the bond amortization period is the cheapest available risk control. The U&amp;L Agreement is the legally binding instrument; a board policy is the available substitute when the carrier counterparty will not negotiate the binding version.',
  ]),

  runs([
    { text: 'Engage the Calatrava Oculus comparison on the record. ', bold: true },
    'The risk that a $22 billion program produces a building like the Oculus — civic-monumental in form, operationally compromised, expensive to maintain, eventually colonized by retail — is real and named. Engaging the comparison explicitly in the program’s design brief is the discipline that reduces the probability of producing it.',
  ], 240),

  new Paragraph({
    spacing: { before: 240, line: 280 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 8 } },
    children: [new TextRun({
      text: 'Executive summary of a 9,400-word position paper produced by the Transform Airports AI Council. Every numerical claim traces to a primary research brief or a disclosed analyst construction. The full report and methodology appendix are available under separate cover.',
      italics: true, size: 18, font: 'Calibri', color: '6B7280',
    })],
  }),
];

// ---------- document ---------------------------------------------------------
const doc = new Document({
  creator: 'Transform Airports AI Council',
  title: 'If Saarinen Were Designing Dulles Today — Executive Summary',
  description: 'Three-page executive summary of the full position paper',
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
