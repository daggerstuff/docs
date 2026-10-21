# v4 uniform duplicate-group status transfer — 2026-10-20

The original exact-row transfer withheld 18 book rows because their row hashes
occurred multiple times in the older 190,139-row candidate. A read-only join of
the old candidate and grouped source-decision ledger confirms every old rowref
against its row number, raw-row hash, and source label. For all 18 current v4
rows, the exact `(row hash, source label)` group exists in the old candidate:
ten rows have two old matches and eight have four. Every possible old match
within each group has the same six source-decision fields. Therefore those
fields can be transferred at the content+source-label group level without
claiming a unique historical source-row identity.

The transferred values remain unresolved/hold: rights `unresolved`, privacy
`unverified`, authority `awaiting_human_sign_off`, eligibility
`hold_pending_owner_rights_and_privacy_review`, family manifest
`proposed_not_ratified`, and generic license `not_exact_row_clearance`. This
does not clear rights, privacy, consent, clinical suitability, or provider
transfer. The separate exact local-book join narrows 12 rows to one local file
but leaves repeated lines; six still match two local files. No candidate,
source ledger, split payload, or provider job changed.

The private status sidecar is
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/v4-untransferred-uniform-status-transfer-20261020.jsonl`
(18 rows, mode 0600, SHA-256
`d20ece42cce50e9703382995b9e5230757cf548215c14990b03c6383d3d9f472`). It
stores current row hashes, source-label hashes, matching old candidate row
numbers, and the identical status fields; it contains no dialogue text. The
reproducer is `scripts/training/transfer_uniform_duplicate_source_status_v4.py`.
