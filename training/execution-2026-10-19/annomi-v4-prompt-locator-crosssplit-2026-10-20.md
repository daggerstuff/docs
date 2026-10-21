# AnnoMI v4 prompt and locator split audit (2026-10-20)

Audited all 98 `annomi` rows in frozen v4: 92 train, 5 validation, and 1 test. Candidate and internal manifest each contain 190,244 rows; SHA-256 digests are `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349` and `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

All 98 exact prompt hashes and all 98 normalized prompt hashes (NFKC, casefold, whitespace collapse) are distinct. All 98 manifest content groups are distinct. No prompt or content group repeats across splits.

The pinned prior origin audit for `uccollab/AnnoMI` commit `42936645ec3857a9c84ab296a36a3c34b779ef49` found no exact adapter-projection match for any of the 98 candidate rows. That unmatched status transfers to current v4 by candidate-record hash for all 98 rows. Thus the audit has zero upstream row locators available to test for uniqueness or split reuse; it does not treat zero references as evidence that source records are globally disjoint. The prior audit recorded immutable hashes for `AnnoMI-full.csv` and `AnnoMI-simple.csv`; only the full CSV is currently cached locally. It did not verify a license grant.

This was the largest remaining family with a pinned source-projection record after the families already covered; larger remaining families such as PsychEval and counseling conversations only have adapter-declared locators and no local source-row bindings. The hash-only sidecar contains 98 candidate/prompt/content-group hashes, split labels, unmatched statuses, and empty upstream-locator lists. Its SHA-256 is `4b7eced6d868fc3ce580b7894e501b192e092eb5dfb189d1257736c2af9e883b`; it and the aggregate report are mode 0600 under `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`.

This is technical prompt/split evidence only; origin remains unbound. Rights, privacy/consent, clinical suitability, training eligibility, and provider-transfer permission are unresolved. No candidate, manifest, release payload, or provider job was changed.
