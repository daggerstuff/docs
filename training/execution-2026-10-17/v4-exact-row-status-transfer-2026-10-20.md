# Current v4 exact-row source-status transfer audit — 2026-10-20

Hash-only technical status transfer from the pinned 190,139-row candidate to current v4. It does not clear rights, privacy, clinical suitability, consent, or provider-transfer permission. No candidate, split payload, manifest, source ledger, or provider job was modified.

## Verified inputs and match

- Older candidate: `ai/data/curated/recovery/gold-20261017/train_master_gold.recovered_candidate.jsonl`; 190,139 rows; SHA-256 `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`.
- Older source-decision ledger: `docs/training/execution-2026-10-17/source-decision-ledger.jsonl`; all 190,139 rowrefs validated against old candidate row number, row hash, and source label; ledger SHA-256 `d701de270b9c3a1437f9fc0e71622b11035fc560df2eb604cf8716179f7581b7`.
- Current v4 candidate: `ai/data/curated/sft_chatml/train_master_gold.jsonl`; 190,244 rows; SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`.
- Current v4 split rowrefs: `ai/data/curated/recovery/gold-20261017/wandb-full-corpus-current-master-20261019-v4/rowrefs.jsonl`; all 190,244 row numbers are unique and each row hash matches current v4.

Join key: SHA-256 of each JSONL row after removing only the trailing LF, plus exact equality of candidate `source` and ledger `source_label`. A status was copied only when the row hash occurred once in each candidate and labels matched. No message text was emitted or copied.

## Result

- Exact unique row-and-source matches transferred: **189,141**.
- Excluded due to repeated old row hashes: **18** current row occurrences in 7 duplicate-hash groups.
- Current v4 rows without an exact old-candidate hash match: **1,085**; these are 1,085 ARC rows separately covered by the v4 ARC lineage audit, and no older ledger disposition is assigned here.
- Source-label mismatches: **0**.
- Total current v4 rows not transferred: **1,103**.

All transferred rows carry the same six source-decision fields: `rights_status=unresolved`, `privacy_review_status=unverified`, `authority_status=awaiting_human_sign_off`, `training_eligibility=hold_pending_owner_rights_and_privacy_review`, `family_manifest_status=proposed_not_ratified`, and `generic_license_status=not_exact_row_clearance`. These are unresolved/hold dispositions, not permissions or clearances. The 18 row occurrences represented by duplicate old hashes were withheld because row-level correspondence is ambiguous.

Hash-only row map: `ai/data/curated/recovery/gold-20261017/private-v4-source-status-transfer-20261020.jsonl.gz` (mode 0600), SHA-256 `9544a94646c4d4ed01c77570c46dad4c28b6afec1eadb4247fae66d8dad366d0`, 189,141 rows (8,713,519 compressed bytes). It contains row number/hash, source label, the transferred status fields, and source-decision hash; no messages. Gzip decompression and row count were verified.

## Uniform duplicate-group supplement (2026-10-20)

The remaining 18 book rows were rechecked at `(exact row hash, exact source
label)` group level. Each corresponds to 2 or 4 old candidate rows, and the
source ledger gives every possible match the same six unresolved/hold values.
Those status fields are now recorded for all 18 rows in a separate group-level
sidecar; this does not resolve which historical row or duplicate local source
line produced each current occurrence. The 1,085 ARC rows retain their separate
exact archive lineage evidence, but their lane-2 decisions remain unbound to
candidate content hashes. See the [uniform-group follow-up](../execution-2026-10-19/v4-untransferred-uniform-status-followup-2026-10-20.md).
