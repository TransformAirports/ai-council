"""Operator-supplied source material — the file-drop workflow.

The repo's `sources/` folder is a drop zone. When the operator launches a
new run, the hub detects what's there, optionally moves the files into the
run's outputs/sources/<slug>/ folder, and converts office formats to plain
markdown sidecars so every agent (including the OpenAI-hosted Deep Research
lens, which has no file tools) can read them.

Supported formats:
  - .md, .txt, .csv, .json, .yaml → pass through; agents read directly
  - .pdf                          → pass through; Claude SDK's Read handles it
  - .docx, .pptx, .xlsx           → extracted to a .extracted.md sidecar
  - other                         → kept but flagged; agents see path only
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DROPZONE = REPO_ROOT / "sources"

EXTRACTABLE_OFFICE = {".docx", ".pptx", ".xlsx", ".pdf"}
NATIVELY_READABLE = {".md", ".txt", ".csv", ".json", ".yaml", ".yml"}
IGNORE_NAMES = {".ds_store", ".gitkeep"}

# Cap extracted text so a single tool-result can never exceed the SDK's stdout
# buffer or balloon token cost. 600k chars ≈ 150k words ≈ a 400-page document.
MAX_EXTRACT_CHARS = 600_000


@dataclass
class SourceFile:
    original: Path        # path of the file in outputs/sources/<slug>/
    readable: Path        # path agents should read (sidecar or original)
    description: str
    size_bytes: int
    extracted: bool


# ----------------------------------------------------------------------------
# Discovery.
# ----------------------------------------------------------------------------

def discover_dropzone(dropzone: Path = DROPZONE) -> list[Path]:
    """Files currently in the drop zone, ready to attach to a new run."""
    if not dropzone.is_dir():
        return []
    return sorted(
        p for p in dropzone.rglob("*")
        if p.is_file()
        and p.name.lower() not in IGNORE_NAMES
        and not p.name.startswith(".")
    )


def format_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.1f} MB"


# ----------------------------------------------------------------------------
# Attach: move + extract.
# ----------------------------------------------------------------------------

def attach_sources(
    slug: str,
    files: list[Path],
    outputs_dir: Path,
) -> list[SourceFile]:
    """Move dropzone files into outputs/sources/<slug>/ and extract office formats."""
    target_dir = outputs_dir / "sources" / slug
    target_dir.mkdir(parents=True, exist_ok=True)

    out: list[SourceFile] = []
    for src in files:
        dst = target_dir / src.name
        if dst.exists():
            # Don't clobber a previously-attached file with the same name.
            stem, suffix = src.stem, src.suffix
            n = 2
            while (target_dir / f"{stem}-{n}{suffix}").exists():
                n += 1
            dst = target_dir / f"{stem}-{n}{suffix}"
        shutil.move(str(src), str(dst))

        ext = dst.suffix.lower()
        readable = dst
        extracted = False
        description = src.name

        if ext in EXTRACTABLE_OFFICE:
            sidecar = dst.with_suffix(dst.suffix + ".extracted.md")
            try:
                sidecar.write_text(_extract_office(dst), encoding="utf-8")
                readable = sidecar
                extracted = True
            except Exception as e:  # noqa: BLE001 — extraction failure is recoverable
                description = f"{src.name} (extraction failed: {e}; agents see binary path only)"
        elif ext in NATIVELY_READABLE:
            pass
        else:
            description = f"{src.name} (binary; agents see path only)"

        out.append(SourceFile(
            original=dst,
            readable=readable,
            description=description,
            size_bytes=dst.stat().st_size,
            extracted=extracted,
        ))
    return out


# ----------------------------------------------------------------------------
# Format extraction.
# ----------------------------------------------------------------------------

def _extract_office(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".docx":
        text = _extract_docx(path)
    elif ext == ".pptx":
        text = _extract_pptx(path)
    elif ext == ".xlsx":
        text = _extract_xlsx(path)
    elif ext == ".pdf":
        text = _extract_pdf(path)
    else:
        raise ValueError(f"unsupported format: {ext}")
    if len(text) > MAX_EXTRACT_CHARS:
        text = (
            text[:MAX_EXTRACT_CHARS]
            + f"\n\n[…extraction truncated at {MAX_EXTRACT_CHARS:,} characters. "
            f"The source file is longer; the remainder is omitted to keep the "
            f"document within processing limits.]"
        )
    return text


def _extract_pdf(path: Path) -> str:
    """Extract text from a PDF to markdown, page by page.

    Reading a large PDF through Claude's native Read tool returns the file as
    base64 — which blows the SDK's 1 MB stdout buffer and burns huge token
    cost. Extracting text first keeps the tool-result small, cheap, and
    readable by every agent (including the OpenAI Deep Research lens).
    """
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    out: list[str] = [f"# Extracted from {path.name}", ""]
    total_chars = 0
    for i, page in enumerate(reader.pages, 1):
        try:
            page_text = (page.extract_text() or "").strip()
        except Exception:  # noqa: BLE001 — a single bad page shouldn't kill extraction
            page_text = ""
        if not page_text:
            continue
        out.append(f"## Page {i}")
        out.append(page_text)
        out.append("")
        total_chars += len(page_text)

    if total_chars < 100:
        # Almost no extractable text — very likely a scanned/image-only PDF.
        out.append(
            "\n[NOTE: this PDF yielded almost no extractable text. It is likely "
            "a scanned or image-only document. OCR is not available in this "
            "pipeline — if its contents matter, supply a text-based version "
            "(searchable PDF, .docx, or pasted .md).]"
        )
    return "\n".join(out)


def _extract_docx(path: Path) -> str:
    from docx import Document
    doc = Document(str(path))
    out: list[str] = [f"# Extracted from {path.name}", ""]
    for para in doc.paragraphs:
        t = para.text.strip()
        if not t:
            continue
        style = (para.style.name if para.style else "") or ""
        if style.startswith("Heading "):
            level_str = "".join(c for c in style if c.isdigit()) or "1"
            depth = min(int(level_str) + 1, 6)
            out.append(f"{'#' * depth} {t}")
        else:
            out.append(t)
        out.append("")
    for i, table in enumerate(doc.tables, 1):
        out.append(f"## Table {i}")
        for row in table.rows:
            cells = " | ".join((c.text.strip() or "—") for c in row.cells)
            out.append(f"| {cells} |")
        out.append("")
    return "\n".join(out)


def _extract_pptx(path: Path) -> str:
    from pptx import Presentation
    prs = Presentation(str(path))
    out: list[str] = [f"# Extracted from {path.name}", ""]
    for i, slide in enumerate(prs.slides, 1):
        out.append(f"## Slide {i}")
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for para in shape.text_frame.paragraphs:
                t = para.text.strip()
                if t:
                    out.append(t)
        try:
            notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        except Exception:  # noqa: BLE001 — some decks have malformed notes parts
            notes = ""
        if notes:
            out.append(f"*Speaker notes:* {notes}")
        out.append("")
    return "\n".join(out)


def _extract_xlsx(path: Path) -> str:
    from openpyxl import load_workbook
    wb = load_workbook(str(path), data_only=True, read_only=True)
    out: list[str] = [f"# Extracted from {path.name}", ""]
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        out.append(f"## Sheet: {sheet_name}")
        rows_written = 0
        for row in ws.iter_rows(values_only=True):
            if all(c is None for c in row):
                continue
            cells = " | ".join(("" if c is None else str(c)) for c in row)
            out.append(f"| {cells} |")
            rows_written += 1
            if rows_written >= 1000:
                out.append(f"| … truncated at 1,000 rows |")
                break
        out.append("")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Run-prompt section + agent prompt preamble + OpenAI inlining.
# ----------------------------------------------------------------------------

def render_for_run_prompt(sources: list[SourceFile], repo_root: Path = REPO_ROOT) -> str:
    """Body of the `## Source material` section written into the run prompt."""
    if not sources:
        return ""
    lines = [
        "The following operator-supplied files are the starting point for "
        "this run. Read them before conducting your own research. Where the "
        "source material conflicts with your default evidence base, name "
        "the conflict in your brief.",
        "",
    ]
    for s in sources:
        rel = s.readable.relative_to(repo_root).as_posix()
        size = format_size(s.size_bytes)
        if s.extracted:
            orig = s.original.relative_to(repo_root).as_posix()
            lines.append(f"- `{rel}` — extracted from `{orig}` ({size})")
        else:
            lines.append(f"- `{rel}` ({size}) — {s.description}")
    return "\n".join(lines)


def stage1_preamble(source_paths: list[str]) -> str:
    """The instruction injected into every Stage 1 agent's prompt."""
    if not source_paths:
        return ""
    lines = [
        "",
        "**BEFORE you research anything:** the operator attached the following "
        "source material to this run. Read every file listed below first, "
        "treat it as the primary starting point, and quote and engage with it "
        "directly in your brief. Where the source material conflicts with "
        "your default evidence base, name the conflict openly:",
    ]
    for p in source_paths:
        lines.append(f"  - `{p}`")
    return "\n".join(lines)


def inline_for_openai(
    source_paths: list[str],
    repo_root: Path = REPO_ROOT,
    max_chars_per_file: int = 30000,
) -> str:
    """Inline source-file text for the OpenAI-hosted Deep Research agent.

    OpenAI agents have no file tools — they only see the prompt text. Each
    file's readable form is inlined; PDFs are referenced by name only because
    we can't extract their text without adding another dep.
    """
    if not source_paths:
        return ""
    chunks: list[str] = [
        "\n\n--- OPERATOR-SUPPLIED SOURCE MATERIAL (inlined; you cannot read files) ---",
    ]
    for rel in source_paths:
        path = (repo_root / rel) if not Path(rel).is_absolute() else Path(rel)
        chunks.append(f"\n\n=== FILE: {path.name} ===")
        if not path.is_file():
            chunks.append(f"\n[File not found at {rel}]")
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            chunks.append(f"\n[Read failed: {e}]")
            continue
        if len(text) > max_chars_per_file:
            text = text[:max_chars_per_file] + f"\n\n[…truncated at {max_chars_per_file:,} chars]"
        chunks.append("\n" + text)
    return "".join(chunks)


# ----------------------------------------------------------------------------
# Archive.
# ----------------------------------------------------------------------------

def archive_sources(slug: str, outputs_dir: Path, archive_dir: Path) -> Path | None:
    """Copy outputs/sources/<slug>/ into the archive at completion."""
    src = outputs_dir / "sources" / slug
    if not src.is_dir():
        return None
    dst = archive_dir / "sources"
    if dst.exists():
        return dst
    shutil.copytree(src, dst)
    return dst
