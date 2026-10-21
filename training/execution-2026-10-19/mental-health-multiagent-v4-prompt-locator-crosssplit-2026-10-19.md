# Mental Health Multiagent prompt and locator split audit — 2026-10-19

This audit hashes prompt context and source locators for the v4 `mental_health_multiagent` family. The candidate contains 190,244 lines with SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`. I independently counted 190,244 lines in its internal manifest and computed SHA-256 `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

The family has 5,606 rows: 5,064 train, 272 validation, and 270 test. Prompt context is the ordered non-system sequence before the final assistant target after the adapter's whitespace stripping. Normalized context additionally case-folds and collapses whitespace while preserving roles and turn order.

| Prompt context tier | Distinct hashes | Repeated hashes | Rows in repeated hashes | Hashes crossing splits |
|---|---:|---:|---:|---:|
| Exact | 5,601 | 2 | 7 | 0 |
| Case/whitespace normalized | 5,601 | 2 | 7 | 0 |

All 5,606 v4 content groups are distinct across splits; zero groups cross splits. The existing pinned public comparison has 24 unique rowrefs and 5,582 unmatched rows. The 24 referenced public repository file locators and projected record hashes are each unique and none cross splits.

The existing public snapshot is `mithatco/mental_health_multiagent` at commit `3473e6afa3b8da9a2dd8f5c71ea22ea60a0b4099`; its file-hash manifest SHA-256 is `2d7e3179a5cd1d34273838a4739ef3a29afb08a173a7467c3bd1ff608c69af6b`. The prior rowref sidecar SHA-256 is `986338249b05f8d1c1497e1e9a589f6c2964c30bd21ceffbd273ed76b81744a4`. The checked-in adapter declares a different GitHub owner/path and private S3 as its source, so the public snapshot comparison does not establish the candidate's actual S3 origin.

The new ignored private sidecar contains hashes, split labels, row numbers, and public source locators only: `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/mental-health-multiagent-v4-prompt-locator-crosssplit.jsonl` (5,606 rows, 3,224,573 bytes, SHA-256 `659b15d6d8549ab51ade6252f160f9a359a09cfd7280b8b2a4c0c412f762748e`, mode `0600` under a `0700` directory). The private aggregate report is stored beside it, mode `0600`.

These are technical split and lineage checks only. Rights, privacy, consent, clinical suitability, license terms, and provider-transfer permission remain unresolved. No corpus, payload, or provider job changed.
