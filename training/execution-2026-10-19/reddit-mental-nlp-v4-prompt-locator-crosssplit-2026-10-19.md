# Reddit Mental NLP prompt and source-locator split audit — 2026-10-19

This hash-only audit reuses the existing adapter/source binding for the 70,968-row `reddit_mental_nlp` family and checks the current v4 candidate's train/validation/test assignments. The checked-in adapter SHA-256 is `fb224f3d380e7380367642ca7aa6bae6e636ec6077829a7aa060a1493c20c6a5`. The current candidate SHA-256 is `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`; the v4 internal manifest SHA-256 is `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

The pinned source binding is Kaggle `kamaruladha/mental-disorders-identification-reddit-nlp`, platform version 2, file `mental_disorders_reddit.csv` (701,787 data rows; SHA-256 `7529dd554c83a3bb781df91405a40262451d6b98b4bd4725e5711c0a06a42ef7`; archive SHA-256 `e0b99acbbb0ab9603191848a144e491741ad76a5a24b271e57ccea3b55a0bace`). The curation-time Kaggle version remains unknown. This audit reuses the existing unique row-reference sidecar and does not fetch or independently replay the source file.

| Split | Candidate rows | Exact unique source bindings | Normalized unique source bindings | No unique locator in sidecar |
|---|---:|---:|---:|---:|
| Train | 63,813 | 25,976 | 26,551 | 11,286 |
| Validation | 3,641 | 1,508 | 1,483 | 650 |
| Test | 3,514 | 1,410 | 1,481 | 623 |
| Total | 70,968 | 28,894 | 29,515 | 12,559 |

The final column includes ambiguous matches, unmatched rows, and the one user-text match with a label mismatch; it does not mean every such row is unmatched. The earlier source-binding audit separately reports 244 exact-tier ambiguous rows, 192 normalized-tier ambiguous rows, and 12,122 unmatched rows. Exact and normalized tiers are distinct matching rules, and normalized matches are not exact-origin evidence.

Prompt overlap is computed from stripped user-message content. Exact prompt keys hash the UTF-8 text after adapter stripping; normalized keys additionally case-fold and collapse whitespace. Seven exact prompt keys (14 rows: 7 train, 3 validation, 4 test) occur across splits. Under case/whitespace normalization, nine keys (18 rows: 9 train, 4 validation, 5 test) cross splits. These are potential prompt-generalization leakage signals; they do not establish duplicate source rows. The v4 manifest contains 70,927 distinct content groups for this family, with zero groups crossing splits.

Across the existing unique source-row bindings, none of the 28,894 exact-tier locators or 29,515 normalized-tier locators is reused across candidate rows or assigned to multiple splits. The corresponding 28,894 exact-tier and 29,515 normalized-tier source-record hashes are also all distinct, with zero cross-split repeats. Ambiguous and unmatched candidates have no unique locator in that sidecar and are excluded from this locator check. The ignored private hash-only sidecar is `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/reddit-mental-nlp-v4-prompt-locator-crosssplit.jsonl` (70,968 rows, 45,538,334 bytes, SHA-256 `1e7d3cbc78245b286acfb057c8875fa12e85a3f100d57873ec15c04ffaf43c0e`, mode `0600` in a mode `0700` directory). It stores prompt hashes, candidate row/group hashes, split labels, and unique source-row locators/hashes only.

The existing Kaggle metadata names Reddit API Terms. Rights, privacy, consent, permitted training/provider use, and curation-time snapshot identity remain unresolved. This audit is not a clearance decision, and no corpus, release payload, or provider run was changed.
