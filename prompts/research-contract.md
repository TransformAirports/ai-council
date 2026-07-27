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
- `source_url` or `source_path`
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
- Distinguish observation, source-supported inference, and professional
  judgment.
- Record evidence against the thesis as carefully as evidence for it.
- If a claim lacks a usable source, keep it out of the evidence file and label
  it clearly as an evidence gap in the brief.
- Quantitative records must state units, denominator, geography, and vintage
  whenever those facts affect interpretation.
