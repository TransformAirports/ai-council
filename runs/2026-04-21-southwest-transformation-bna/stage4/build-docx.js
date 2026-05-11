// Build the full report .docx for the Southwest/BNA run.
// Reads outputs/stage3/final-draft.md + docs/methodology.md and writes a .docx
// with cover page, TOC, body, and methodology appendix.

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType,
  LevelFormat, PageBreak, PageNumber, TableOfContents, HeadingLevel,
  BorderStyle,
} = require('docx');

const REPO = '/Users/christiankessleriv/Repos/ai-council-mwaa';
const SRC = path.join(REPO, 'outputs/stage3/final-draft.md');
const OUT = path.join(REPO, 'outputs/stage4/southwest-transformation-bna.docx');

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
        font: 'Consolas', size: 20,
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

  // Skip the opening H1 + H2 subtitle + metadata block; resume at first "## I. ..."
  let start = 0;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].startsWith('## I. ')) { start = i; break; }
  }

  let i = start;
  while (i < lines.length) {
    const line = lines[i];

    if (line.trim() === '---') { i++; continue; }
    if (line.trim() === '') { i++; continue; }

    // H1 (Roman-numeral section) — page break before
    if (line.startsWith('## ')) {
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_1,
        pageBreakBefore: true,
        children: parseInline(line.slice(3)),
      }));
      i++; continue;
    }

    // H2 (lettered subsection)
    if (line.startsWith('### ')) {
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: parseInline(line.slice(4)),
      }));
      i++; continue;
    }

    // H3
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

    // Numbered list
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

    // Default: paragraph — narrative prose, slightly more line spacing for readability
    children.push(new Paragraph({
      spacing: { after: 200, line: 320 },
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
    spacing: { after: 200 },
    children: [new TextRun({
      text: 'The Airport Southwest Was,',
      bold: true, size: 48, font: 'Calibri', color: '111111'
    })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 360 },
    children: [new TextRun({
      text: 'The Airport Southwest Is Becoming',
      bold: true, size: 48, font: 'Calibri', color: '111111'
    })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 720 },
    children: [new TextRun({
      text: 'Nashville\u2019s Capital Program and a Carrier in Mid-Transformation',
      italics: true, size: 30, font: 'Calibri', color: '4B5563'
    })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [new TextRun({
      text: 'Transform Airports AI Council',
      size: 26, font: 'Calibri', color: '374151'
    })],
  }));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 720 },
    children: [new TextRun({ text: 'April 21, 2026', size: 22, font: 'Calibri', color: '6B7280' })],
  }));

  for (let k = 0; k < 6; k++) out.push(new Paragraph(''));

  out.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    border: {
      top: { style: BorderStyle.SINGLE, size: 6, color: '888888', space: 6 },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: '888888', space: 6 },
    },
    children: [new TextRun({
      text: 'DRAFT \u2014 For internal review. Not for external distribution until human review is complete.',
      bold: true, size: 20, font: 'Calibri', color: '333333'
    })],
  }));

  out.push(new Paragraph({ children: [new PageBreak()] }));
  return out;
}

// ---------- TOC ----------
function tocPage() {
  return [
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      children: [new TextRun('Table of Contents')],
    }),
    new Paragraph({
      children: [new TextRun({
        text: 'Right-click and select "Update Field" in Word to populate section headings and page numbers.',
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
    children: [new TextRun('Methodology')],
  }));

  out.push(new Paragraph({
    spacing: { after: 160, line: 320 },
    children: parseInline('This document was produced by the Transform Airports AI Council, a multi-agent system operated by ________________ [name / role]. The Council consists of twelve specialized agents running on Anthropic\u2019s Claude platform:'),
  }));

  const bullets = [
    'Eight research agents \u2014 Infrastructure Economist, Operations Analyst, Technology Scout, Contrarian, Chief Engineer, Airline Commercial Strategist, Regulatory/Political Analyst, and Aviation Historian \u2014 that independently gathered evidence without reading each other\u2019s work.',
    'A Strategist that synthesized the eight briefs into a single argumentative draft.',
    'A Red Team that attacked the Strategist\u2019s drafts across multiple revision rounds.',
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
    spacing: { before: 240, after: 160, line: 320 },
    children: parseInline('Total agent runtime: ________ hours. Human review occurred at two checkpoints: after the third Strategist draft and after the Fact-checker\u2019s report. Agent definitions are maintained as versioned markdown files and are edited only by human reviewers via pull request \u2014 agents do not modify themselves or each other.'),
  }));

  out.push(new Paragraph({
    spacing: { after: 240, line: 320 },
    children: parseInline('The final text was reviewed and approved by ________________ [name] before release. AI-assisted production does not reduce human accountability for the arguments and claims in this document.'),
  }));

  return out;
}

// ---------- assemble ----------
const md = fs.readFileSync(SRC, 'utf8');
const bodyChildren = bodyFromMarkdown(md);

const doc = new Document({
  creator: 'Transform Airports AI Council',
  title: 'The Airport Southwest Was, The Airport Southwest Is Becoming',
  description: 'Nashville\u2019s Capital Program and a Carrier in Mid-Transformation',
  styles: {
    default: { document: { run: { font: 'Calibri', size: 23 } } }, // 11.5pt body — narrative long-form likes a touch more space
    paragraphStyles: [
      {
        id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal',
        quickFormat: true,
        run: { size: 36, bold: true, font: 'Calibri', color: '111111' },
        paragraph: { spacing: { before: 360, after: 220 }, outlineLevel: 0 },
      },
      {
        id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal',
        quickFormat: true,
        run: { size: 26, bold: true, italics: true, font: 'Calibri', color: '1F2937' },
        paragraph: { spacing: { before: 240, after: 140 }, outlineLevel: 1 },
      },
      {
        id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal',
        quickFormat: true,
        run: { size: 23, bold: true, font: 'Calibri', color: '1F2937' },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: 'bullets',
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: '\u2022',
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
    // Cover page
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
    // TOC + body + methodology
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
