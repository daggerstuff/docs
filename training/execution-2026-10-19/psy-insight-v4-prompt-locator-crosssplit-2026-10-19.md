# Psy-Insight v4 prompt and source-locator split audit (2026-10-19)

Audited all 673 `psy_insight` rows in the frozen v4 candidate. The candidate has 190,244 JSONL rows (SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`); the aligned internal manifest has 190,244 rows (SHA-256 `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`). Family split counts are 588 train, 39 validation, and 46 test.

Prompt keys cover every non-system turn except the final assistant target. Exact keys hash compact Unicode JSON role/content sequences. Normalized keys apply NFKC, casefolding, and whitespace collapse before hashing. All 673 prompt hashes are distinct under both methods; there are no repeated prompts or cross-split prompt overlaps.

The prior exact-origin sidecar was replay-checked against current candidate row hashes: 518 rows have one unique public source dialogue locator and 155 remain unmatched; there are no ambiguous statuses in that sidecar. The 518 source locators are unique and none cross splits. The public comparison is against `ckqqqq/Psy-Insight` commit `0a5bd3f011dd8fdb8d6b7c0081b3510e4a478f5a`; the checked-in adapter declares a private S3 acquisition path and a different GitHub owner/name, so this public comparison does not establish the original S3 object revision.

Separately, all 50 repair-overlay rows with generated continuations have unique source-excerpt locators from `xi1019/counseling-psy-insight` revision `dd6f2e582377ddb71e976ec8f45ad48b5c5fc57a` (44 train, 2 validation, 4 test); none of those excerpt locators repeat or cross splits. These locators identify source excerpts used in repair, not upstream response targets. Generated responses remain distinct from source-origin evidence.

The private hash-only sidecar has 673 records and SHA-256 `2f0cb3753cb9426a834dafebb14105af6db145d5afd38eb6427af73b9b1e5176`; its paired machine-readable report and sidecar are mode 0600 under `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`. The sidecar stores candidate/prompt hashes, split labels, existing binding statuses, and hashed source locators only.

This is technical lineage and split evidence only. It does not establish dataset licensing, privacy or consent, clinical review, training suitability, provider-transfer permission, or rights to distribute model weights. No candidate, manifest, release payload, or provider job was modified.
