# Council Research Artifact Contract

Every Stage 1 researcher produces two artifacts:

1. A readable analytical brief at the path assigned by the orchestrator.
2. A JSON Lines evidence file at the assigned `*-evidence.jsonl` path.

The evidence file contains one valid JSON object per line and no markdown
fences. Each record represents the smallest defensible claim supported by one
source.

Required fields:

- `claim`
- `source_title`
- one of `source_url`, `source_path`, or `source_citation`
- `source_type`
- `source_date` when known
- `data_vintage` when different from the publication date
- `airport_or_entity`
- `page_or_section`
- `supporting_excerpt`
- `units` and `denominator` for quantitative claims
- `caveat`
- `confidence`: high, medium, or low

Rules:

- The brief is analysis; it is never the source.
- Prefer primary documents, regulations, datasets, audited financials,
  official statements, airport records, and authoritative research.
- Never invent a URL, document title, page, quotation, number, or date.
- Paywalled and print-only works are legitimate evidence. When a source has no
  free URL that resolves to the cited text — NFPA, IEC, ANSI, ICAO, ACRP
  monographs, textbooks, printed board minutes — set `source_citation` to the
  full citation a librarian could act on (issuing body, designation, edition or
  year, title) and set `page_or_section` to where in the work the claim lives.
  Leave `source_url` null. Do not manufacture a link to satisfy the schema: a
  fabricated URL is a worse failure than an honest offline citation.
- Use `source_citation` only when no public URL exists. If the work is on the
  open web, cite the URL.
- Distinguish observation, source-supported inference, and professional
  judgment.
- Record evidence against the thesis as carefully as evidence for it.
- If a claim lacks a usable source, keep it out of the evidence file and label
  it clearly as an evidence gap in the brief.
- **Professional judgment never goes in the evidence file.** Your expert read —
  what a procurement cycle really costs, how long hiring actually takes, what
  breaks first in practice — is the most valuable thing you produce, and the
  brief is where it belongs. State it there in prose, in your own voice, marked
  as judgment. The evidence file holds only claims a reader could go and verify
  against a document. A record whose `source_type` is `professional_judgment`,
  or whose excerpt says it is "not sourced to a single publication," is by
  definition a brief sentence, not a ledger entry.
- Every record needs a real source. Do not manufacture one, and do not stretch
  a loosely related document to cover a claim it does not actually support.
- Quantitative records must state units, denominator, geography, and vintage
  whenever those facts affect interpretation.
