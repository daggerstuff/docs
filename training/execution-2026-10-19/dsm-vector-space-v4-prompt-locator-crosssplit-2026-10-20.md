# DSM vector-space v4 prompt and source-locator split audit (2026-10-20)

Audited all 116 `dsm_vector_space` rows in frozen v4: 106 train, 6 validation, and 4 test. Candidate and internal manifest both contain 190,244 rows; their SHA-256 digests are `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349` and `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

The audit used non-system turns except the final assistant target for prompt keys. All 116 exact and normalized prompt hashes are distinct; manifest content-group hashes are also all distinct. None repeat or cross splits.

The pinned public-repository row binding remains ambiguous for every candidate row: each maps to two upstream rows, with no candidate arbitrarily resolved. All 232 source locator references are unique and none cross splits. The comparison is against `savelee/dsm-in-vector-space` commit `c61599906a386bae33d81fac42a8acc26f6a29ef`; the adapter's original acquisition declaration names private S3, so this public content correspondence does not establish which S3 object supplied the candidate.

The private sidecar contains 116 rows of candidate/prompt/content-group hashes, split assignments, retained ambiguity status, and hashed locator references. Its SHA-256 is `a0419964c6b25a7f334e898abc1f72731461787cb28c25e3c934d30b0fd501d8`; both it and the aggregate JSON report are mode 0600 under `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`.

These are technical lineage and split findings only. They do not establish license rights, privacy or consent, clinical suitability, benchmark-leakage acceptability, or provider-transfer permission. Underlying DSM material rights require separate review. No candidate, manifest, release payload, or provider job was changed.
