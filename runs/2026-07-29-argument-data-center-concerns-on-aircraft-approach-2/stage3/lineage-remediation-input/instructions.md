# Argument verification remediation

The first verification pass did not satisfy the deterministic release contract. Repair the final argument and rebuild its lineage.

## Blocking findings

- numeric_claims_without_footnotes: numerical claims lack a footnote in the same sentence or table row
- memo_paragraph_too_long: the executive memo contains prose paragraphs longer than 90 words
- word_count_out_of_range: the final argument has 601 reader-facing words; the run contract requires 350–550
- claim_lineage_schema: C3 is missing: draft_sha256
- stale_claim_lineage: C3 is not bound to the current final-draft bytes
- lineage_claim_footnote_mismatch: C3 does not appear in the sentence or table row cited by [^2]
- claim_not_supported_by_evidence_record: C3's cited evidence records do not collectively support the reader-facing assertion
- claim_lineage_schema: C7b is missing: draft_sha256
- stale_claim_lineage: C7b is not bound to the current final-draft bytes
- lineage_footnote_not_in_draft: C7b does not name a footnote marker used in the final draft
- claim_not_supported_by_evidence_record: C7b's cited evidence records do not collectively support the reader-facing assertion
- claim_not_supported_by_evidence_record: C16's cited evidence records do not collectively support the reader-facing assertion
- claim_lineage_schema: C19 is missing: draft_sha256
- stale_claim_lineage: C19 is not bound to the current final-draft bytes
- lineage_claim_footnote_mismatch: C19 does not appear in the sentence or table row cited by [^2]
- claim_not_supported_by_evidence_record: C19's cited evidence records do not collectively support the reader-facing assertion
- claim_without_evidence: C20 is retained but has no evidence IDs
- lineage_contract: line 3 missing required keys: draft_sha256
- lineage_contract: line 7 missing required keys: draft_sha256
- lineage_contract: line 13 missing required keys: draft_sha256
