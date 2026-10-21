# ARC corpus v4 prompt and source-locator split audit (2026-10-20)

Audited all 1,085 `arc_corpus` rows in frozen v4: 981 train, 58 validation, and 46 test. The 190,244-row candidate SHA-256 is `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`; the 190,244-row internal manifest SHA-256 is `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

Using non-system turns except the final assistant target, all 1,085 exact prompt hashes and all 1,085 normalized prompt hashes (NFKC, casefold, whitespace collapse) are distinct. All 1,085 manifest content-group hashes are distinct. None repeat or cross splits. The previously established source binding remains exact for all 1,085 candidate rows by canonical session rendering and unique `(arc_id, session_n)` key; the row locators are unique with no cross-split reuse.

The private hash-only sidecar has 1,085 rows and SHA-256 `f0d108bb558608675ecf25341486b7a1918b9a2de0284a38625584de2de665c3`; its paired report is also mode 0600 in `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`. The source binding used the protected ARC archive snapshot SHA-256 `8d5b53b9ea9d2c6e157f072bd3542550d7f0caaa5e4cdfb585d4751746f19936` and prior rowref sidecar SHA-256 `23b6e6eed9f9bb3af22c7ff1605aac1c59414e7ec7b6b77c22ddf5e7cc1a5e12`.

This is technical lineage and split evidence only. The archive's machine acceptance verdict does not establish clinician review, clinical quality, rights, privacy or consent, generation-provider terms, training eligibility, or permission to transfer the records. No candidate, manifest, release payload, or provider job was changed.
