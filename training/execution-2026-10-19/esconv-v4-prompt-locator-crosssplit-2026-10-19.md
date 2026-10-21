# ESConv v4 prompt and source-locator split audit (2026-10-19)

Audited all 892 `esconv` rows in frozen v4: 811 train, 46 validation, 35 test. The candidate and internal manifest each contain 190,244 rows, with SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349` and `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`, respectively.

Prompt keys cover non-system turns except the final assistant target. Exact keys use compact Unicode JSON role/content sequences; normalized keys apply NFKC, casefolding, and whitespace collapse. All 892 exact and all 892 normalized prompt hashes are distinct, with no cross-split repeats. Manifest `content_group_sha256` values are also all distinct, with no cross-split group reuse.

The existing pinned adapter-projection binding statuses were retained: 13 exact-unique, 16 normalized-unique, 863 unmatched, and no ambiguous rows. The 29 bound upstream locators are unique and none cross splits. The source is `thu-coai/Emotional-Support-Conversation` commit `f262d062ad74cb39b17ea476facc81568ddcba24`; `ESConv.json` SHA-256 is `aa0556c5b330562ba009c1cd5137486bfa2a7255f33225a6524cd58f7efdd9af`. The sidecar contains only hashes, split, status, and hashed file/record locators.

Private hash-only evidence (892 rows; SHA-256 `e2ad047ba95a03c0c25a90f911fec57ed0fb6956a182a97d66add05cdce63152`) and its aggregate JSON report are mode 0600 under `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`.

This is technical provenance and split evidence only. It does not establish licensing, privacy or consent, clinical review, training eligibility, provider-transfer permission, or redistribution rights. No candidate, manifest, release payload, or provider job was changed.
