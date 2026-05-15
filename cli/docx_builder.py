"""Stage 4 — produce the full report and executive summary as Word documents.

Replicates what the Claude Code `docx` skill would otherwise do, but as plain
Python so the CLI does not depend on Claude Code being present at runtime.

The markdown→docx conversion is intentionally minimal — it handles the
constructs the Strategist and Fact-checker actually emit (headings, paragraphs,
bullet lists, inline bold/italic, blockquotes). Tables and code fences are
rendered as monospaced blocks.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^[\-\*]\s+(.*)$")
ORDERED_RE = re.compile(r"^\d+\.\s+(.*)$")
BLOCKQUOTE_RE = re.compile(r"^>\s?(.*)$")
INLINE_BOLD = re.compile(r"\*\*(.+?)\*\*")
INLINE_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
INLINE_CODE = re.compile(r"`([^`]+)`")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def _add_inline(paragraph, text: str, base_size: int = 11) -> None:
    """Add a text run, parsing **bold**, *italic*, and `code` segments."""
    if not text:
        return
    pos = 0
    tokens: list[tuple[str, str]] = []
    pattern = re.compile(r"\*\*(.+?)\*\*|(?<!\*)\*([^*]+?)\*(?!\*)|`([^`]+)`")
    for m in pattern.finditer(text):
        if m.start() > pos:
            tokens.append(("plain", text[pos : m.start()]))
        if m.group(1) is not None:
            tokens.append(("bold", m.group(1)))
        elif m.group(2) is not None:
            tokens.append(("italic", m.group(2)))
        elif m.group(3) is not None:
            tokens.append(("code", m.group(3)))
        pos = m.end()
    if pos < len(text):
        tokens.append(("plain", text[pos:]))

    for kind, value in tokens:
        run = paragraph.add_run(value)
        run.font.size = Pt(base_size)
        run.font.name = "Calibri"
        if kind == "bold":
            run.bold = True
        elif kind == "italic":
            run.italic = True
        elif kind == "code":
            run.font.name = "Consolas"


def _strip_comments(text: str) -> str:
    return HTML_COMMENT.sub("", text)


def _markdown_to_docx(doc: Document, markdown: str, body_size: int = 11) -> None:
    text = _strip_comments(markdown)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i].rstrip()
        if not raw.strip():
            i += 1
            continue

        m = HEADING_RE.match(raw)
        if m:
            level = min(len(m.group(1)), 4)
            heading = doc.add_heading(level=level)
            _add_inline(heading, m.group(2), base_size=18 - level * 2)
            i += 1
            continue

        m = BULLET_RE.match(raw)
        if m:
            while i < len(lines):
                line = lines[i].rstrip()
                bm = BULLET_RE.match(line)
                if not bm:
                    break
                p = doc.add_paragraph(style="List Bullet")
                _add_inline(p, bm.group(1), base_size=body_size)
                i += 1
            continue

        m = ORDERED_RE.match(raw)
        if m:
            while i < len(lines):
                line = lines[i].rstrip()
                om = ORDERED_RE.match(line)
                if not om:
                    break
                p = doc.add_paragraph(style="List Number")
                _add_inline(p, om.group(1), base_size=body_size)
                i += 1
            continue

        m = BLOCKQUOTE_RE.match(raw)
        if m:
            buf: list[str] = []
            while i < len(lines):
                line = lines[i].rstrip()
                bm = BLOCKQUOTE_RE.match(line)
                if not bm:
                    break
                buf.append(bm.group(1))
                i += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(24)
            _add_inline(p, " ".join(buf), base_size=body_size)
            for run in p.runs:
                run.italic = True
            continue

        # Plain paragraph: collect until blank line.
        buf = [raw]
        i += 1
        while i < len(lines) and lines[i].strip():
            if HEADING_RE.match(lines[i]) or BULLET_RE.match(lines[i]) or ORDERED_RE.match(lines[i]):
                break
            buf.append(lines[i].rstrip())
            i += 1
        p = doc.add_paragraph()
        _add_inline(p, " ".join(buf), base_size=body_size)


def _set_default_font(doc: Document, name: str = "Calibri", size: int = 11) -> None:
    style = doc.styles["Normal"]
    style.font.name = name
    style.font.size = Pt(size)


def _add_cover_page(doc: Document, title: str, subtitle: str) -> None:
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(28)
    run.font.name = "Calibri"

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(subtitle)
    run.font.size = Pt(14)
    run.font.name = "Calibri"
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    for _ in range(2):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Transform Airports AI Council")
    run.font.size = Pt(12)
    run.font.name = "Calibri"

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(date.today().strftime("%B %d, %Y"))
    run.font.size = Pt(11)
    run.font.name = "Calibri"

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("DRAFT — for review")
    run.italic = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0xAA, 0x33, 0x33)

    doc.add_page_break()


def _add_table_of_contents(doc: Document) -> None:
    p = doc.add_paragraph()
    run = p.add_run()
    fld_begin = run._element.makeelement(qn("w:fldChar"), {qn("w:fldCharType"): "begin"})
    run._element.append(fld_begin)
    instr = run._element.makeelement(qn("w:instrText"), {qn("xml:space"): "preserve"})
    instr.text = 'TOC \\o "1-3" \\h \\z \\u'
    run._element.append(instr)
    fld_sep = run._element.makeelement(qn("w:fldChar"), {qn("w:fldCharType"): "separate"})
    run._element.append(fld_sep)
    fld_end = run._element.makeelement(qn("w:fldChar"), {qn("w:fldCharType"): "end"})
    run._element.append(fld_end)
    doc.add_paragraph(
        "(Right-click → Update Field in Word to populate the table of contents.)"
    ).runs[0].italic = True
    doc.add_page_break()


def _build_full_report(
    title: str,
    final_draft_md: str,
    methodology_md: str,
    out_path: Path,
) -> None:
    doc = Document()
    _set_default_font(doc, "Calibri", 11)
    _add_cover_page(doc, title=title, subtitle="A Council Argument")
    _add_table_of_contents(doc)
    _markdown_to_docx(doc, final_draft_md, body_size=11)
    doc.add_page_break()
    doc.add_heading("Appendix: Methodology", level=1)
    _markdown_to_docx(doc, methodology_md, body_size=11)
    doc.save(out_path)


def _build_executive_summary(
    title: str,
    final_draft_md: str,
    out_path: Path,
) -> None:
    """Three-page distillation. Compresses the full draft to ~1,100 words.

    Keeps top-level headings, the first paragraph after each, and any
    [UNVERIFIED — HUMAN REVIEW] tags exactly as-is. Strips bracketed source
    citations like `[Economist brief, Finding 3]`.
    """
    doc = Document()
    _set_default_font(doc, "Calibri", 11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title.upper())
    run.bold = True
    run.font.size = Pt(20)
    run.font.name = "Calibri"
    run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    # Letter-spaced header effect via wide tracking on the title only.

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("EXECUTIVE  SUMMARY")
    run.font.size = Pt(11)
    run.font.name = "Calibri"
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(date.today().strftime("%B %Y") + "  ·  Transform Airports AI Council")
    run.font.size = Pt(10)
    run.font.name = "Calibri"
    run.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    doc.add_paragraph()

    citation_re = re.compile(r"\[(?:[A-Z][a-z]+ (?:brief|note)|Stage \d+)[^\]]*\]")
    distilled = _distill_for_summary(final_draft_md, citation_re)
    _markdown_to_docx(doc, distilled, body_size=11)

    doc.save(out_path)


def _distill_for_summary(markdown: str, citation_re: re.Pattern) -> str:
    """Keep H1/H2 headings, first paragraph under each, preserve UNVERIFIED tags."""
    text = _strip_comments(markdown)
    text = citation_re.sub("", text)
    out: list[str] = []
    paragraphs: list[str] = []
    keep_next_paragraph = True
    paragraph_lines: list[str] = []

    def flush_paragraph(force_keep: bool = False) -> None:
        nonlocal keep_next_paragraph
        joined = " ".join(paragraph_lines).strip()
        paragraph_lines.clear()
        if not joined:
            return
        if keep_next_paragraph or force_keep or "[UNVERIFIED" in joined:
            out.append(joined)
            out.append("")
            keep_next_paragraph = False

    for line in text.splitlines():
        stripped = line.rstrip()
        m = HEADING_RE.match(stripped)
        if m:
            flush_paragraph()
            level = len(m.group(1))
            if level <= 2:
                out.append(stripped)
                out.append("")
                keep_next_paragraph = True
            continue
        if not stripped:
            flush_paragraph()
            continue
        paragraph_lines.append(stripped)
    flush_paragraph()
    return "\n".join(out)


def build_documents(
    *,
    slug: str,
    title: str,
    final_draft: Path,
    methodology: Path,
    out_dir: Path,
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    final_draft_md = final_draft.read_text(encoding="utf-8")
    methodology_md = methodology.read_text(encoding="utf-8") if methodology.is_file() else ""

    full_path = out_dir / f"{slug}.docx"
    exec_path = out_dir / f"{slug}-executive-summary.docx"

    _build_full_report(title, final_draft_md, methodology_md, full_path)
    _build_executive_summary(title, final_draft_md, exec_path)

    return full_path, exec_path
