// Build the 3-page Executive Summary .docx for the Southwest/BNA run.
// Standalone narrative distillation of final-draft.md.

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType,
  LevelFormat, PageBreak, PageNumber, BorderStyle,
} = require('docx');

const OUT = '/Users/christiankessleriv/Repos/ai-council-mwaa/outputs/stage4/southwest-transformation-bna-executive-summary.docx';

// ---------- helpers ----------
const runs = (parts, spacingAfter = 180) => new Paragraph({
  spacing: { after: spacingAfter, line: 320 },
  alignment: AlignmentType.LEFT,
  children: parts.map(p => {
    if (typeof p === 'string') return new TextRun({ text: p, size: 22, font: 'Calibri' });
    return new TextRun({ size: 22, font: 'Calibri', ...p });
  }),
});

const sectionHead = (text) => new Paragraph({
  spacing: { before: 280, after: 160 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 4 } },
  children: [new TextRun({
    text: text.toUpperCase(),
    bold: true, size: 22, font: 'Calibri',
    characterSpacing: 40, color: '1F2937',
  })],
});

// ---------- title block ----------
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
    spacing: { after: 80 },
    children: [new TextRun({
      text: 'The Airport Southwest Was,',
      bold: true, size: 40, font: 'Calibri', color: '111111',
    })],
  }),

  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 140 },
    children: [new TextRun({
      text: 'The Airport Southwest Is Becoming',
      bold: true, size: 40, font: 'Calibri', color: '111111',
    })],
  }),

  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 160 },
    children: [new TextRun({
      text: 'Nashville\u2019s Capital Program and a Carrier in Mid-Transformation',
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
      text: '    Transform Airports AI Council    \u00B7    April 21, 2026    ',
      size: 18, font: 'Calibri', color: '6B7280', characterSpacing: 30,
    })],
  }),
];

// ---------- content ----------
const content = [
  // Opening
  runs([
    'On January 26, 2026, Southwest Airlines flight 1971 landed in Los Angeles. The gate agents applauded. A flight attendant told CNBC she was so happy she wanted to cry. Flight 1971 was the last Southwest flight to operate under open seating, the policy the carrier had held for fifty-four years and that every competitor had tried to replicate and failed. The applause was genuine. The policy ended anyway.',
  ]),

  runs([
    'The end of open seating is one of six transformations Southwest compressed into eighteen months. Checked-bag fees now run $45 for the first bag and $55 for the second. Basic economy fares have replaced Wanna Get Away. The carrier joined the online travel agency distribution network it had refused for two decades. It committed to premium extra-legroom seats on a third of its fleet. It filed permits in February 2026 for a 30,000-square-foot, $53 million airport lounge in the central mezzanine at Nashville International \u2014 the largest lounge in its corporate pipeline and the physical evidence that the airline whose name still hangs above Concourse D is no longer the airline that designed it.',
  ]),

  runs([
    { text: 'This essay argues three things. ', bold: true },
    'First, Southwest is completing a decade-compressed transformation from the highest-productivity point-to-point carrier in U.S. aviation history to a hybrid revenue-optimization carrier, and the transformation is structurally irreversible. Second, Nashville International\u2019s capital program \u2014 $4.5 billion committed since 2017, with the uncommitted tranches of the New Horizon program still to be design-locked \u2014 was scoped against the Southwest that existed when ground broke, not the Southwest that will be flying in 2030. Third, the gap between those two airlines is narrow enough to be invisible from a glance at the gate chart, and wide enough that the Metropolitan Nashville Airport Authority\u2019s next three capital decisions should be pressure-tested against the new model before they are committed, not after.',
  ]),

  sectionHead('The evidence'),

  runs([
    { text: 'Southwest\u2019s presence at BNA is deepening even as its character changes. ', bold: true },
    'The carrier holds 54% of total BNA traffic and 60% of seat capacity. It opened its twelfth crew base at BNA in May 2024 \u2014 somewhere between 650 and 950 employees. It operated 166 daily departures last year, 190 this spring, and is scheduled for 215 by fall 2026. Nashville is one of four coordinating connection banks in Southwest\u2019s new schedule architecture. This is the opposite of a departure signal. It is also the opposite of the high-frequency, quick-turn, point-to-point relationship that Concourse D was designed around.',
  ]),

  runs([
    { text: 'The operational math runs against gate productivity in the short term. ', bold: true },
    'Southwest\u2019s own 2006 internal testing showed assigned seating adds one to four minutes of boarding time. A three-minute average increase across 166 daily Concourse D departures consumes roughly eight gate-hours per day. The fleet is simultaneously upgauging from 143-seat 737-700s to 175-seat MAX 8s \u2014 a 22% increase in passengers per gate cycle on infrastructure sized before the shift. The system-average turn that had sat at 25 minutes for most of the carrier\u2019s history was 49 minutes by 2024. The company\u2019s own target is 44.',
  ]),

  runs([
    { text: 'The airport\u2019s financials are tightening in the same window. ', bold: true },
    'BNA\u2019s cost per enplanement is projected to rise from $8.49 in FY2024 to $17.48 by FY2032, nearly doubling. The increase is driven almost entirely by debt service on New Horizon. Senior debt service coverage is projected to fall from 5.95x in FY2025 to 1.80x in FY2030 against a covenant floor of 1.25x. Southwest\u2019s January 2025 letter to MNAA asking the Authority to keep cost increases to a reasonable level is the revealed-preference data point that matters. Carriers send letters like that eighteen months before they begin diverting growth to cheaper stations.',
  ]),

  runs([
    { text: 'The airline use agreement executed in July 2023 is the hinge. ', bold: true },
    'It eliminated Southwest\u2019s majority-in-interest veto over terminal capital \u2014 a generational shift for MNAA \u2014 but locked terminal rental rates through June 30, 2031. Southwest signed it a year before Elliott Management\u2019s stake became public and fifteen months before the September 2024 Investor Day announced the transformation. Both sides got what they wanted from the negotiation. One side knew more about what was coming.',
  ]),

  sectionHead('The counter-case, honestly'),

  runs([
    'The strongest version of the opposing view is that BNA Vision was scaled to metropolitan demand growth, not to any specific carrier\u2019s boarding process, and that Southwest\u2019s transformation is a revenue-side phenomenon that should not move airport capital decisions. Nashville remains one of the fastest-growing mid-size markets in the country. Southwest is setting departure records, not reducing them. Historical airport bets on carrier behavior \u2014 at Memphis, at Cincinnati, at Pittsburgh \u2014 produced abandoned terminals; historical bets on demand held their value through the next carrier\u2019s arrival.',
  ]),

  runs([
    'That argument is honest, and it is not sufficient. Demand volume is one planning input. The per-passenger infrastructure profile is a second \u2014 larger aircraft, longer dwell, more checked bags, more premium square footage \u2014 and it has changed. Continental\u2019s 1995 reduction of service at Denver after a CPE spike is the cleaner precedent than the dehubbings: a carrier with network commitment shifting where growth went once the cost curve crossed a threshold. The January 2025 letter suggests Southwest\u2019s finance team is already watching that curve.',
  ]),

  sectionHead('What this means for MNAA'),

  runs([
    'Three capital decisions carry load-bearing weight before 2028. The Concourse A reconstruction \u2014 16 gates, 374,000 square feet, $855 million, target July 2028 \u2014 has not fully locked its design. Hold room sizing, podium configuration, premium queuing geometry, and lounge adjacencies are each still adjustable within the Hensel Phelps contract. The baggage handling system expansion commissions in October 2028; its load case against a checked-bag mix reflecting the new fee structure, a behavioral shift of 25 to 30 percent of carry-on passengers to the hold, and a 215-departure peak is a load case the systems integrator should already have in its model \u2014 and if it has not been re-run since the May 2025 bag-fee rollout, it needs to be. The Central Ramp Expansion\u2019s September 2027 hookup configuration for seven remain-overnight and deicing positions is the hardest decision to reverse: concrete pours last forty years, and the power, data, preconditioned-air, and ground-power-unit density for a carrier running a redeye fleet with premium passenger expectations is different from the density for a carrier that turned aircraft quickly and kept overnight counts low.',
  ]),

  runs([
    'Underneath these three, the 2031 use agreement renewal is the pressure point. The fixed rental rate through 2031 means the airport cannot pass through rising debt service to Southwest during the contract term. The leverage for 2031 is built between now and 2030, in how Concourse A lands, in how Southwest\u2019s CPE at BNA compares to peer airports the carrier has added capacity to, and in whether the Oasis lounge is meeting its traffic and revenue targets two years into operation. MNAA should start positioning for that renegotiation now, not in 2030. The lounge terms already under discussion are the leading edge.',
  ]),

  sectionHead('The question, stated once'),

  runs([
    'The question MNAA\u2019s planners should ask at their next capital planning meeting is not whether Southwest will still be at BNA in 2030. That has an easy answer. The question is this: what does each remaining New Horizon tranche look like if Southwest\u2019s 2030 operation runs 49-minute turns on 175-seat aircraft, banks four connections daily at Nashville, operates a 30,000-square-foot premium lounge above the lobby, and charges $55 for a checked bag? Every element of that sentence is a fact already established by Southwest\u2019s own filings and operating record. None of them requires a forecast.',
  ], 240),

  // Closing
  new Paragraph({
    spacing: { before: 240, line: 300 },
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: 'BFBFBF', space: 8 } },
    children: [new TextRun({
      text: 'Executive summary of an 8,200-word report produced by the Transform Airports AI Council. Every numerical claim traces to a primary research brief or a disclosed analyst construction. The full report and methodology appendix are available under separate cover.',
      italics: true, size: 18, font: 'Calibri', color: '6B7280',
    })],
  }),
];

// ---------- document ----------
const doc = new Document({
  creator: 'Transform Airports AI Council',
  title: 'The Airport Southwest Was, The Airport Southwest Is Becoming \u2014 Executive Summary',
  description: 'Three-page executive summary of the full report',
  styles: {
    default: { document: { run: { font: 'Calibri', size: 22 } } },
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
