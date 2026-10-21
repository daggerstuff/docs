# Reddit Mental Health Posts prompt and source-locator split audit — 2026-10-19

This hash-only audit reuses the existing source binding for the 30,444-row `reddit_mental_health_posts` family and checks prompt and locator overlap across v4 train/validation/test. The checked-in adapter SHA-256 is `3e66610594fc48e1137e02f45907a5f584b4c2fdcc1bab4131531060e497016e`. The adapter-declared HF dataset `solomonk/reddit_mental_health_posts` is pinned at revision `48c23354c088c4273b260a877dafa424e1c6cc95`. The five local source files remain available with restrictive permissions; their bytes and SHA-256 values were reverified against the prior pinned-source report.

The candidate SHA-256 is `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`; v4 internal manifest SHA-256 is `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`. Family split counts are train 27,373, validation 1,581, and test 1,490.

Exact prompt keys hash stripped user-message content. Normalized keys additionally case-fold and collapse whitespace.

| Prompt tier | Distinct hashes | Hashes crossing splits | Rows touched | Split distribution |
|---|---:|---:|---:|---|
| Exact | 30,439 | 1 | 2 | train 1, validation 1 |
| Case/whitespace normalized | 30,438 | 2 | 4 | train 2, validation 2 |

Across the existing 10,693 unique source bindings, no upstream file/row locator or projected source-message hash is reused across candidate rows or crosses splits. The family has 30,379 distinct v4 content groups, with zero groups crossing splits. The remaining 19,751 rows have no exact source match in the prior join and remain unbound.

The ignored private hash-only sidecar is `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/reddit-mental-health-posts-v4-prompt-locator-crosssplit.jsonl` (30,444 rows, 16,412,638 bytes, SHA-256 `7d75d2ff63facae0b35e55de4da9ab360429f7d77720586da32d5e888fcadd91`, mode `0600` beneath a mode `0700` directory). It records prompt hashes, candidate row/group hashes, split labels, and upstream locators and hashes only.

The source revision is pinned for this audit, but the candidate's curation-time source revision remains unknown. The HF API had no license value for the repo. Reddit platform terms, author rights, privacy, consent, clinical suitability, and provider-training permission remain unresolved. No corpus, release payload, or provider run changed.
