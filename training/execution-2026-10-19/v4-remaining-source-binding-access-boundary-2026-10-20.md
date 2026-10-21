# v4 remaining source-binding boundary — 2026-10-20

Update 2026-10-20: the prior PsychEval access boundary is resolved for
technical row matching. The configured object store exposes the declared
`whitebat` bucket through remote `r2`; a private local snapshot of all 369 raw
JSON files now binds all 1,977 candidate rows uniquely (1,968 exact,
9 normalized-only) with zero exact-locator split crossings. The snapshot has
no immutable upstream version, and the adapter-declared current public GitHub
tree remains unrelated; see the [PsychEval upstream-origin binding
audit](psycheval-v4-upstream-origin-binding-2026-10-20.md). The remaining
largest unresolved family is `counseling_conversations` (1,415). The R2
snapshot's `combined_dataset.json` is byte-bound by Git blob SHA-1 to the
pinned Amod revision. After verifying that JSON and JSONL copies have
identical ordered rows and removing the duplicate representation from the
join, 151 rows bind exactly and 311 bind after normalization; 369 remain
unmatched. Of those 369, 361 are prompt-only, 7 response-only, and 1 neither.
The R2 bucket has no acquisition receipt; the declared Hugging Face source
remains manually gated. See the corrected [Counseling Conversations origin
audit](counseling-conversations-v4-upstream-origin-binding-2026-10-20.md).
`daic_woz` has 129 rows and its USC source is controlled-access; the public
mirror is not treated as authorization. No candidate, manifest, release
payload, or provider job changed.

After the corrected Counseling Conversations join, its source file is pinned but 369 candidate pairs still have no normalized full-pair match; 735 normalized matches remain ambiguous because the pinned source contains repeated pairs. A hash-only scan found no exact full-pair matches for those 369 rows among other current candidate source families. `daic_woz` has 129 rows and its USC source is controlled-access; the public mirror is not treated as authorization.

The current frozen candidate and internal manifest were re-counted and re-hashed: each has 190,244 lines. Candidate SHA-256 is `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`; manifest SHA-256 is `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`. The available current-v4 pinned rowref families with local source evidence already have origin and prompt/locator split reports, including the recently completed Mitch Hamidi audit. An older `other-family-local-binding` artifact is tied to a different 190,139-row candidate hash and is not transferable as current-v4 evidence.

Next technical action is to trace the 369 unmatched pairs to their actual transformation/acquisition records and assess the Amod terms for the 1,046 rows that match; preserve the frozen candidate and current training payload while doing so. The exact file-to-revision binding is now proven, but the R2 acquisition receipt is absent. PsychEval is technically row-bound to a private snapshot, but exact acquisition-time lineage is unverified. Rights, privacy, consent, clinical suitability, training eligibility, and provider-transfer permission remain unresolved. No candidate, manifest, release payload, or provider job changed.

Supporting evidence: [PsychEval availability audit](psycheval-v4-source-availability-prompt-crosssplit-2026-10-20.md), [Counseling Conversations access audit](counseling-conversations-v4-source-availability-crosssplit-2026-10-20.md), [source locator metadata audit](source-locator-public-metadata-audit-2026-10-19.md), and [public source-row binding summary](public-source-row-binding-summary.md).
