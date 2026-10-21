# Counseling Conversations v4 prompt split audit and source gate (2026-10-20)

Audited 1,415 `counseling_conversations` v4 rows by current candidate-record hash transfer: 1,278 train, 62 validation, 75 test. The 190,244-row candidate SHA-256 is `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`; the aligned internal manifest SHA-256 is `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

Exact prompt hashes have 674 distinct values, 285 repeated hashes across 1,026 rows, and 79 hashes spanning splits (424 rows in those groups: 325 train, 44 validation, 55 test). NFKC/casefold/whitespace-normalized prompt hashes yield the same counts. All 1,415 manifest content-group hashes are distinct with no split crossing.

The original public-metadata-only status is superseded by the corrected private-snapshot binding below: 151 records have exact unique locators and 311 have unique locators after normalization. The adapter declares `Amod/mental_health_counseling_conversations`, file `combined_dataset.json`; its revision is now confirmed by the local Git blob hash. Hugging Face still reports a manual gate, and the source terms require separate rights/consent assessment.

Private hash-only sidecar (1,415 rows; SHA-256 `f886d1c0a9aab431f15a8c7d093229c145fa1bf6dea19600f41a9ca0ed042b0c`) and paired report are mode 0600 in `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`.

## Superseding private-snapshot binding update

The earlier statement that no source join was possible is superseded for
technical matching. A private R2 snapshot at
`whitebat/training/raw/counseling_conversations/` contains two raw Q&A files
(3,512 rows each) and one derived ChatML output. The JSON and JSONL raw files
have the same ordered records; the JSON file's Git blob hash matches
`combined_dataset.json` at pinned Amod revision
`d7e86f0813c5690181b41f97403c3674aa55dcef`. The corrected audit indexes that
source once, excluding the duplicate serialization from locator counts. The
R2 bucket itself has no version history or acquisition receipt.

Against the frozen 1,415-row candidate, the corrected exact ordered
user/assistant pair join yields 151 unique, 276 ambiguous, and 988 unmatched
rows; NFKC/casefold/space normalization yields 311 unique, 735 ambiguous, and
369 unmatched. Earlier ambiguity counts were inflated by indexing two
identical raw-file representations. Exact and normalized source-locator split
crossings are both zero. Of the 369 normalized pair-unmatched rows, 361 have a
prompt match without a response match, 7 have a response match without a
prompt match, and 1 has neither. The 369 also fail to match the public Sulav
mirror at pinned revision `66316a6dd209fb6cf95e1ba1b77e9ffc96b69efa`.

This establishes partial technical content correspondence, not source
license, consent, or transfer rights. The declared Amod dataset card
is gated and its current terms prohibit rewriting individual question-answer
pairs; the separate Sulav mirror provides no verified license. Do not treat
the 369 as ordinary formatting differences or silently rewrite them. Keep the
candidate frozen while applicable authorization is resolved and the 369
unmatched records are traced. See [private-snapshot origin-binding audit](counseling-conversations-v4-upstream-origin-binding-2026-10-20.md)
for hashes and aggregate evidence. No candidate, manifest, release payload, or
provider job was changed.

These are candidate-only prompt/content split findings, not source-origin, license, privacy/consent, clinical suitability, or provider-transfer clearance. No candidate, manifest, release payload, or provider job was changed.
