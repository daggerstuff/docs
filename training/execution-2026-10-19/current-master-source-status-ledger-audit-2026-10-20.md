# Current v4 source-status ledger audit — 2026-10-20

The current-master source-decision ledger has one row reference for every one
of the 190,244 rows in the frozen v4 candidate. Recomputed raw-row SHA-256 and
exact `source` label both match every reference. All six source fields are
present on every row and uniformly remain unresolved/hold: rights unresolved,
privacy unverified, authority awaiting human sign-off, training held pending
rights/privacy review, family manifest proposed, and generic license not exact
row clearance. These are not permissions or clearances.

The group-level ledger metadata preserves a two-step candidate history: 1,243
source groups covering 190,230 rowrefs retain the predecessor candidate hash
`c5ed52809930b5b602c43a4021afc083eb09e688bf3049c0088f38a8c7bfb606`, and six
source groups covering the 14 added v4 rows carry the current v4 candidate hash
`f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`. The v4 driver documents those 14
rows as the final six ARC additions. Although the group-level digest differs
for the predecessor rows, all 190,230 rowref hashes and labels independently
match their current candidate positions. This preserves the original decision
lineage instead of rewriting the predecessor digest.

Source-specific lane-2 decisions remain unbound for the 1,085 ARC rows, and
source rights, privacy, consent, clinical suitability, and provider-transfer
permission remain unresolved. The audit did not modify candidate data, the
ledger, training payloads, or provider jobs. Reproduce with
`uv run --project ai python scripts/training/audit_current_master_source_status_v4.py`.
Machine-readable counts and hashes are in
`current-master-source-status-ledger-audit-2026-10-20.json`.
