# Counseling Conversations v4 private-snapshot origin binding (2026-10-20)

This audit compares the frozen v4 `counseling_conversations` family against a
private object-store snapshot. It records aggregate counts and hashes only; no
conversation text or row-level identifiers are included here. **Correction:**
the initial audit counted both `combined_dataset.json` and the equivalent
`combined_dataset.jsonl` as independent source rows, inflating ambiguity. The
corrected v2 sidecar indexes the pinned JSON once after verifying both files
have identical ordered records. Use the v2 counts and sidecar below; the
original sidecar remains as historical audit output.

The 190,244-row candidate SHA-256 is
`f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`; the
internal manifest SHA-256 is
`3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`. The
family contains 1,415 rows (1,278 train, 62 validation, 75 test); the adapter
SHA-256 is `22caf7afa1f971e055dcc1b4bbdc59a34d17799c697428f2a9f1577e1dc56a7e`.

The private snapshot was audited 2026-10-20 from
`r2:whitebat/training/raw/counseling_conversations/`. It contains three
objects. Two raw Q&A files contain 3,512 rows each (7,024 total) and produce
3,508 adapter-valid records each (7,016 as duplicate serialization views).
The two raw files have identical ordered JSON records. The 4,790,520-byte
`raw/combined_dataset.json` file's Git blob SHA-1 matches
`c007b48f6350f2d1493109db168440bfc6d8450f`, the `combined_dataset.json`
object at pinned Hugging Face revision
`d7e86f0813c5690181b41f97403c3674aa55dcef`. Its local SHA-256 is
`e9e1dbb65604b5e41f9a7a6f5c1b5edc57a85de681573be97f14d5730204c7ab`. This
byte-level match binds the local source file to the exact upstream revision.
The combined byte count of both raw representations is
9,588,535 and the source-file manifest SHA-256 is
`ac12f1aba6358c8d3e02de06542f366469c9efd841abd47ae6deeb5eb2a23962`. The
third object is derived ChatML output and was excluded as an input source.

| Join | Unique | Ambiguous | Unmatched | Source-locator split crossings |
|---|---:|---:|---:|---:|
| Exact ordered non-system user/assistant turns (corrected v2) | 151 | 276 | 988 | 0 |
| NFKC + case-fold + collapsed-whitespace turns (corrected v2) | 311 | 735 | 369 | 0 |

Ambiguity is retained rather than broken arbitrarily. Among the 369 normalized
full-pair-unmatched rows, 361 have a normalized prompt match without a response
match, 7 have a response match without a prompt match, and 1 has neither. The
369 rows also fail to match the separate public Sulav mirror pinned at
`66316a6dd209fb6cf95e1ba1b77e9ffc96b69efa`. This is consistent with assistant
responses altered or sourced elsewhere for a substantial subset, but the
available snapshot does not establish which explanation is correct.

## Historical-copy and candidate-lineage cross-check

The candidate's 1,415 ordered user/assistant pairs have exact string equality
with the counseling family in the earlier 190,139-row recovered candidate
(1,415/1,415); the 369 pair mismatches therefore predate the current 190,244
v4 packaging. This is equality of parsed message strings, not a claim that the
serialized JSONL bytes are identical. Additional private historical copies do
not explain them:

| Private historical copy | Rows | Candidate normalized-pair matches | Pair unmatched |
|---|---:|---:|---:|
| `hetzner/acquired/mental_health_counseling.json` | 3,512 | 311 unique + 735 ambiguous | 369 |
| `training_v2/stage1_foundation/Amod_mental_health_counseling_conversations.jsonl` | 500 | 241 unique | 1,174 |
| `training_v3/stage1_foundation/Amod_mental_health_counseling_conversations.jsonl` | 500 | 241 unique | 1,174 |
| Saved ChatML adapter output | 3,508 | 311 unique + 735 ambiguous | 369 |

The 361 prompt-only, 7 response-only, and 1 neither split is unchanged in the
acquired snapshot and saved ChatML output. Historical-copy SHA-256 hashes are
`58d8df2e90e2952396ef464e7a2bd944aa7a3072f6386bd833fda7068b642379`
(`mental_health_counseling.json`),
`2ce1da4f0884c35ab75adc6b74294f497d1d66ffe2f0aa98bbe635bcd0a4ac34`
(training v2), and
`ef622418924a93cb190ed300bc2673eeeb80f371fed9d71079b5b7b12387dc5a`
(training v3). These are private content snapshots and not immutable upstream
release identifiers. Their local copies are mode 0600 under
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/counseling-conversations-historical/`.

The historical adapter output records only the `Amod` URL, a retrieval time,
and the generic `download`, `extract`, `convert_to_chatml`, `validate`
transformation list; it contains no record locator or source revision. The
checked-in adapter strips surrounding whitespace but does not rewrite answer
text. The recovered candidate has no per-row provenance fields beyond its
family label. The exact upstream or intervening transformation that produced
the 369 pairs therefore remains unidentified.

The declared adapter source is
[`Amod/mental_health_counseling_conversations`](https://huggingface.co/datasets/Amod/mental_health_counseling_conversations).
Its current gated card states that individual question-answer pairs must not
be rewritten or altered, and sets separate noncommercial/commercial and
redistribution conditions. The separate Sulav mirror has no verified license.
The R2 raw snapshot file is byte-bound to the pinned Amod revision, though its
acquisition receipt and timing remain unavailable. Technical matching does
not establish rights, consent, privacy, clinical suitability, or provider-
transfer authorization.

Additional read-only checks on 2026-10-20 established the exact source version
while leaving the acquisition receipt unavailable. The R2 bucket reports
versioning `Unversioned`; its objects carry timestamps and content type but no
acquisition receipt. The two raw file modification times are 2026-08-04, while
their R2 creation timestamps are 2026-10-20. Authenticated Hugging Face
metadata at the pinned commit resolves `combined_dataset.json`, but fetching
that file returns HTTP 404 through the current client; no source content was
downloaded from Hugging Face. The local file-to-revision binding instead comes
from the Git blob hash match above. An R2 metadata-only inventory found no
additional Amod-named source copy: it contains the already audited raw
snapshot, derived ChatML output, and same acquired/v2/v3 historical copies
listed above. Their R2 creation dates reflect the 2026-10-20 mirror and add no
acquisition-time evidence. Keep the 369 normalized pair-unmatched rows in the
existing frozen research candidate and training payload as directed; this
provenance finding does not pause or retroactively alter the active full-
corpus job. It remains a source-lineage qualification for later release
decisions.

The candidate, manifest, provider payload, and running jobs were not changed.
Keep the 1,415-row family frozen pending lineage and rights clarification; do
not silently rewrite the 369 pair-unmatched examples. Machine-readable report
and hash-only sidecar are stored privately, mode 0600, under
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`.
The corrected v2 sidecar contains 1,415 hash-only rows and has SHA-256
`b60effb1133826bc608a7590e124fb05359e1f4197edb41be34c9ef471a88258`; it is
mode 0600. The original sidecar SHA-256 is
`2622e9594108cc628916debaf266f2043f75305cb45bca412e19c965b1fe47e2` and is
retained unchanged for audit history.

## Additional R2 lineage sweep — 2026-10-20

A second metadata/content pass located three more potential source copies. All
were streamed and compared against the 369 previously normalized full-pair
unmatched candidate keys, using the same Unicode NFKC, case-folding,
whitespace-collapsing, and ordered user/assistant-turn normalization. No row
text was emitted or retained by this check.

| Object | Size / records | SHA-256 | Match to 369 |
|---|---:|---|---:|
| `r2:whitebat/training/ai-data/raw/counseling_conversations/counseling_conversations.jsonl` | 7,399,534 bytes / 3,508 rows | `4308f9370f56c5f8b2eb420eccd00c0596da549baaf20a0d0fe1b017e098da31` | 0 |
| `r2:whitebat/training/raw/deduped/counseling_conversations.jsonl` | 4,226,986 bytes / 2,025 rows | `43bf2c7b3ea2320ceef88aef1a15a34189d2a719ecb53d53fb66d1e61853c468` | 0 |
| `r2:whitebat/training/raw/hetzner/ai/data/compress/processed/mental_health_clean.jsonl` | 260,254,190 bytes / 64,536 rows | `0b7fee7af26bb7a777636bbc0880b0899fdaacc0be6b59fc144e9e84f3fc7272` | 0 |

The first object is byte-identical to the already audited local saved adapter
output at
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/counseling-conversations-upstream/counseling_conversations.jsonl`;
it adds no independent upstream history and retains the same 1,046 candidate
matches. The second object has no new pair among the 369. The transformed
64,536-row object also has no full-pair match among them. A further copy of
`combined_dataset.json` at
`r2:whitebat/training/raw/hetzner/cot_reasoning/combined_dataset.json` is
4,790,520 bytes and has the same SHA-256 as the already pinned source file
(`e9e1dbb65604b5e41f9a7a6f5c1b5edc57a85de681573be97f14d5730204c7ab`).

These checks leave the normalized coverage at 311 unique, 735 ambiguous, and
369 unmatched (1,046 covered of 1,415). The R2 inventory and metadata search
still yielded no acquisition receipt, immutable source revision, or usable
row locator for the remaining pairs. No candidate rows or clearance/status
fields were altered.
