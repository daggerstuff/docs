# Crisis Benchmark prompt and source-locator split audit — 2026-10-19

This hash-only audit uses the existing pinned Crisis Benchmark rowrefs and independently counts and hashes the current v4 candidate and internal manifest. Both contain 190,244 rows. Candidate SHA-256: `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`. Manifest SHA-256: `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

The `crisis_benchmark` family has 1,522 rows: 1,374 train, 79 validation, and 69 test. Exact user-prompt hashes (after stripping) and case-folded, whitespace-normalized user-prompt hashes each yielded 1,522 distinct hashes, with no duplicate prompt and no cross-split prompt overlap. All 1,522 candidate content groups are split-disjoint.

The adapter-declared HF mirror is `arnaiztech/llms-mental-health-crisis-benchmark` at revision `7f0a0d31bb8309b0e52e670d535d954d6fa7a386`. Pinned source files: `test.parquet`, 1,239,532 bytes, SHA-256 `1342f5166b6862afbc88acf27a6e719230d4f1478b4cee7b6b1ce42ebf7547d9`; and `validation.parquet`, 143,221 bytes, SHA-256 `109251c85d96e4a50fe70e8700417a79df9e6f3f5b5dafdbaafdea3bf4e5d57d`. The previous adapter-projection join found 1,370 exact unique rows, 36 exact ambiguous rows, 22 normalized-only unique rows, and 94 unmatched rows. It found zero complete adapter-render matches.

Across the 1,465 unique referenced upstream row locators and corresponding source-row hashes (including all references retained for ambiguous candidates), none is reused across candidate rows or crosses splits. The prior ambiguity is preserved: the 36 ambiguous candidate rows refer to duplicate upstream rows. The 94 unmatched rows have no locator in the prior sidecar and are excluded from that locator check.

The new private sidecar records candidate row/group hashes, exact and normalized user-prompt hashes, split labels, binding tier, and pinned upstream locators/hashes only: `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/crisis-benchmark-v4-prompt-locator-crosssplit.jsonl` (1,522 rows, 935,449 bytes, SHA-256 `4062f748901bd7d4b8dca73ce6c36849d5b7f7df9d761ab81079d3357f4a59c5`, mode `0600` under a mode `0700` directory). The private aggregate report is stored beside it, also mode `0600`.

The source is a crisis evaluation benchmark, so row or prompt correspondence does not settle evaluation contamination or appropriate SFT use. Rights, privacy, consent, clinical suitability, and provider-transfer permission remain unresolved. No dataset, release payload, or provider job changed.
