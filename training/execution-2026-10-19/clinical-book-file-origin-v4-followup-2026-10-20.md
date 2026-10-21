# Clinical-book local-file lineage follow-up — 2026-10-20

Rechecked the 18 v4 rows previously marked ambiguous against all 47 local
`books_distilled` JSONL files using exact ordered user/assistant content pairs.
Twelve candidate rows now have an exact match to one local file, although the
same pair occurs multiple times within that file and the exact line remains
ambiguous. Six candidate rows still match two separate local files and remain
file-level ambiguous. No row was normalized or guessed into a match.

This narrows local file provenance for 12/18 rows but does not establish the
source book's edition, acquisition history, rights, privacy status, clinical
suitability, or permission to transfer to a provider. No v4 candidate or
training payload changed, and no rights/clearance disposition was inferred.

Private reproducibility evidence is stored with mode 0600 under
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`:

- Sidecar: `clinical-book-file-origin-v4-followup-20261020.jsonl` (18 rows;
  SHA-256 `304d9f10ab6da8fdb3bd529a9620e920bc829547352c012204d6f8f94cafaebc`)
- Report: `clinical-book-file-origin-v4-followup-20261020-report.json`
- Reproducer: `scripts/training/audit_clinical_book_file_origin_v4.py`

The candidate hash is
`f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`.
The private sidecar binds each candidate row hash to exact local file SHA-256s
and matching line numbers without storing message text.
