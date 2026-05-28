// Build the Transform Airports AI Council Word document.
// Reads outputs/stage3/final-draft.md + docs/methodology.md and writes a .docx
// with cover page, TOC, body, and methodology appendix.

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType,
  LevelFormat, PageBreak, PageNumber, TabStopType, TabStopPosition,
  TableOfContents, HeadingLevel, BorderStyle, PageOrientation
} = require('docx');

const REPO = '/Users/cgkiv/Documents/GitHub/ai-council';
const SRC = path.join(REPO, 'outputs/stage3/final-draft.md');
const OUT = path.join(REPO, 'outputs/stage4/sterile-corridor-resilience.docx');

// ---------- inline formatting ----------
function parseInline(line) {
  const runs = [];
  let i = 0;
  while (i < line.length) {
    if (line.startsWith('**', i)) {
      const end = line.indexOf('**', i + 2);
      if (end === -1) { runs.push(new TextRun(line.slice(i))); break; }
      runs.push(new TextRun({ text: line.slice(i + 2, end), bold: true }));
      i = end + 2;
    } else if (line[i] === '`') {
      const end = line.indexOf('`', i + 1);
      if (end === -1) { runs.push(new TextRun(line.slice(i))); break; }
      runs.push(new TextRun({
        text: line.slice(i + 1, end),
        font: 'Consolas',
        size: 20,
        shading: { fill: 'F2F2F2', type: 'clear' }
      }));
      i = end + 1;
    } else if (line[i] === '*') {
      const end = line.indexOf('*', i + 1);
      if (end === -1) { runs.push(new TextRun(line.slice(i))); break; }
      runs.push(new TextRun({ text: line.slice(i + 1, end), italics: true }));
      i = end + 1;
    } else {
      let next = line.length;
      for (const tok of ['**', '*', '`']) {
        const p = line.indexOf(tok, i);
        if (p !== -1 && p < next) next = p;
      }
      runs.push(new TextRun(line.slice(i, next)));
      i = next;
    }
  }
  return runs.length ? runs : [new TextRun('')];
}

// ---------- markdown → docx children ----------
function bodyFromMarkdown(md) {
  const children = [];
  const lines = md.split('\n');

  // Skip the H1 title + the draft metadata block.
  // Resume at the first "## I." (Roman-numeral section).
  let start = 0;
  for (let i = 0; i < lines.length; i++) {
    if (/^## [IVX]+\./.test(lines[i])) { start = i; break; }
  }

  let i = start;
  while (i < lines.length) {
    let line = lines[i];

    // Horizontal rule — skip
    if (line.trim() === '---') { i++; continue; }

    // Trailing italic metadata line at end of doc — skip
    if (line.trim().startsWith('*Stage 3 final draft')) { i++; continue; }

    // Blank line — skip
    if (line.trim() === '') { i++; continue; }

    // Heading 1 (## ...)
    if (line.startsWith('## ')) {
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_1,
        pageBreakBefore: true,
        children: parseInline(line.slice(3)),
      }));
      i++; continue;
    }

    // Heading 2 (### ...)
    if (line.startsWith('### ')) {
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: parseInline(line.slice(4)),
      }));
      i++; continue;
    }

    // Heading 3 (#### ...)
    if (line.startsWith('#### ')) {
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: parseInline(line.slice(5)),
      }));
      i++; continue;
    }

    // Bulleted list
    if (line.startsWith('- ')) {
      while (i < lines.length && lines[i].startsWith('- ')) {
        children.push(new Paragraph({
          numbering: { reference: 'bullets', level: 0 },
          children: parseInline(lines[i].slice(2)),
        }));
        i++;
      }
      continue;
    }

    // Numbered list (1. ..., 2. ..., etc.)
    if (/^\d+\.\s/.test(line)) {
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        const m = lines[i].match(/^\d+\.\s(.*)$/);
        children.push(new Paragraph({
          numbering: { reference: 'numbers', level: 0 },
          children: parseInline(m[1]),
        }));
        i++;
      }
      continue;
    }

    // Default: paragraph (one line per paragraph in the source)
    children.push(new Paragraph({
      spacing: { after: 160 },
      children: parseInline(line),
    }));
    i++;
  }

  return children;
}

// ---------- cover page ----------
function coverPage() {
  const out = [];

  for (let k = 0; k < 8; k++) out.push(new Paragraph(''));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 240 },
    children: [new TextRun({
      text: 'Sterile Corridor Design as a Resilience Problem',
      bold: true, size: 52, font: 'Arial'
    })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 720 },
    children: [new TextRun({
      text: 'Why throughput and recovery — not code compliance — should govern the next generation of sterile circulation at IAD',
      italics: true, size: 28, font: 'Arial'
    })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({ text: 'Transform Airports AI Council', size: 28, font: 'Arial' })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 720 },
    children: [new TextRun({ text: 'May 28, 2026', size: 24, font: 'Arial' })],
  }));

  for (let k = 0; k < 6; k++) out.push(new Paragraph(''));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    border: {
      top: { style: BorderStyle.SINGLE, size: 6, color: '888888', space: 6 },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: '888888', space: 6 },
    },
    children: [new TextRun({
      text: 'DRAFT — For internal review. Not for external distribution until human review is complete.',
      bold: true, size: 22, font: 'Arial', color: '333333'
    })],
  }));

  out.push(new Paragraph({ children: [new PageBreak()] }));
  return out;
}

// ---------- TOC page ----------
function tocPage() {
  return [
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      children: [new TextRun('Table of Contents')],
    }),
    new Paragraph({
      children: [new TextRun({
        text: 'Section headings link to their page. Right-click and select "Update Field" in Word to populate.',
        italics: true, size: 20, color: '555555'
      })],
      spacing: { after: 240 },
    }),
    new TableOfContents('Contents', {
      hyperlink: true,
      headingStyleRange: '1-2',
    }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// ---------- methodology appendix ----------
function methodologyAppendix() {
  const out = [];

  out.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: true,
    children: [new TextRun('Methodology Appendix')],
  }));

  out.push(new Paragraph({
    spacing: { after: 160 },
    children: [new TextRun({
      text: 'This document was produced by the Transform Airports AI Council, a multi-agent system operated by ________________ [name / role]. The Council consists of twelve specialized agents running on Anthropic’s Claude platform:',
    })],
  }));

  const bullets = [
    'Eight research agents — Infrastructure Economist, Operations Analyst, Technology Scout, Contrarian, Chief Engineer, Airline Commercial Strategist, Regulatory/Political Analyst, and Aviation Historian — that independently gathered evidence without reading each other’s work.',
    'Four additional perspective agents seated for this run — Airport CEO, Airport COO, Virtual Christian (the operator’s intuition pass), and Slacker (the unstructured adjacency scan).',
    'A Strategist that synthesized the twelve briefs into a single argumentative draft.',
    'A Red Team that attacked the Strategist’s drafts across two revision rounds.',
    'An Editor that tightened the final prose without adding new content or claims.',
    'A Fact-checker that verified every numerical and attributed claim against the research briefs. Unverifiable claims were removed or flagged for human review.',
  ];
  for (const b of bullets) {
    out.push(new Paragraph({
      numbering: { reference: 'bullets', level: 0 },
      children: parseInline(b),
    }));
  }

  out.push(new Paragraph({
    spacing: { before: 240, after: 160 },
    children: parseInline('Total agent runtime: ________ hours. Human review occurred at two checkpoints: after the third Strategist draft and after the Fact-checker’s report. Agent definitions are maintained as versioned markdown files and are edited only by human reviewers via pull request — agents do not modify themselves or each other.'),
  }));

  out.push(new Paragraph({
    spacing: { after: 240 },
    children: parseInline('The final text was reviewed and approved by ________________ [name] before release. AI-assisted production does not reduce human accountability for the arguments and claims in this document.'),
  }));

  return out;
}

// ---------- assemble ----------
const md = fs.readFileSync(SRC, 'utf8');
const bodyChildren = bodyFromMarkdown(md);

const doc = new Document({
  creator: 'Transform Airports AI Council',
  title: 'Sterile Corridor Design as a Resilience Problem',
  description: 'Why throughput and recovery should govern the next generation of sterile circulation at IAD',
  styles: {
    default: {
      document: { run: { font: 'Arial', size: 22 } },
    },
    paragraphStyles: [
      {
        id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal',
        quickFormat: true,
        run: { size: 36, bold: true, font: 'Arial', color: '000000' },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 },
      },
      {
        id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal',
        quickFormat: true,
        run: { size: 28, bold: true, font: 'Arial', color: '000000' },
        paragraph: { spacing: { before: 240, after: 140 }, outlineLevel: 1 },
      },
      {
        id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal',
        quickFormat: true,
        run: { size: 24, bold: true, italics: true, font: 'Arial', color: '000000' },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: 'bullets',
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: '•',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
      {
        reference: 'numbers',
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: '%1.',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } },
        }],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
        titlePage: true,
      },
      children: coverPage(),
    },
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
          pageNumbers: { start: 1 },
        },
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ children: [PageNumber.CURRENT], size: 18, color: '777777' }),
            ],
          })],
        }),
      },
      children: [
        ...tocPage(),
        ...bodyChildren,
        ...methodologyAppendix(),
      ],
    },
  ],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(OUT, buffer);
  const stat = fs.statSync(OUT);
  console.log(`Wrote ${OUT}`);
  console.log(`Size: ${(stat.size / 1024).toFixed(1)} KB`);
  console.log(`Body paragraphs: ${bodyChildren.length}`);
}).catch(err => {
  console.error('Pack error:', err);
  process.exit(1);
});
