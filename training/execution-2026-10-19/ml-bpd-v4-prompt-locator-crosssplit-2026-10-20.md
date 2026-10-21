# ML-BPD v4 prompt and source-locator split audit (2026-10-20)

Audited the 100 `ml_bpd` rows transferred into frozen v4 by exact candidate-record SHA-256 from the prior source-binding sidecar. All 100 row hashes verified in the current candidate; the older binding report's candidate digest is retained as provenance, not assumed to be the current v4 digest. The candidate and aligned internal manifest each contain 190,244 rows, with SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349` and `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

The family has 86 train, 11 validation, and 3 test rows. Prompt hashes use all non-system turns except the final assistant target; normalized keys apply NFKC, casefolding, and whitespace collapse. All 100 exact prompts, all 100 normalized prompts, and all 100 manifest content groups are distinct; none repeat or cross splits.

Prior source statuses were preserved: 56 unique upstream user-content matches and 44 duplicate-content ambiguous matches. All 144 candidate-to-source-row locator references (including all alternatives for ambiguous rows) are unique, with no cross-split locator reuse. The pinned upstream is `saidejp/machine_learning_BPD` commit `41a6535acbd5389766d18882e9b9b20ca89660ea`; the prior row-binding report records hashes for four source CSVs. The private sidecar hashes candidate/prompt values and each `(commit, file hash, row number)` locator; it stores no message text or score values.

The hash-only private sidecar has 100 rows and SHA-256 `9320bb308f971d3fa901edc83b6c582226f4becac54d1c3b4066331f559d33e8`; its paired aggregate report is mode 0600 under `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`.

The prior source audit notes sensitive clinical assessment measures and no repository license file; privacy, consent, clinical validity, training permission, and provider transfer remain unresolved. Technical lineage is not clearance. No candidate, manifest, release payload, or provider job was changed.
