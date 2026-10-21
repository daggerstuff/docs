# Full-candidate split integrity refresh — 2026-10-20

Read-only recheck of the authorized W&B research release
`wandb-full-corpus-20261018-v2`. No dataset or provider state was changed, and
no row contents were emitted in the report.

| Check | Result |
| --- | ---: |
| Candidate rows | 190,139 |
| Unique rowrefs resolving candidate row numbers | 190,139 |
| Candidate row content hashes matched | 190,139 / 190,139 |
| Row hash mismatches | 0 |
| Repair rows recorded in repair file | 52 |
| Repair-file hash mismatches against release manifest | 0 |
| Train rows | 171,167 |
| Validation rows | 9,666 |
| Test rows | 9,306 |
| Split payload hash and row-count mismatches | 0 |
| Train/validation, train/test, validation/test group intersections | 0 / 0 / 0 |

The candidate hash remains
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`. The
three payload hashes remain the values pinned in
[`wandb-full-corpus-release-v2.json`](wandb-full-corpus-release-v2.json): train
`138045ba6fb263e0d68bb42c3e8d0a7e3bf7314c3fc79397ecfd805a2c980a76`,
validation
`0de3d1e2607f90958db119df89a64f56f1a694b448a56c029fef3412dd15df7b`, and test
`a657d271beee6e05104a69b1a3a57844959b937348666ee34e4d64b691bd588f`.

Reproduction used Python's standard library to parse the release manifest and
rowrefs, hash every candidate JSONL row after removing only its trailing LF,
hash and count each split payload and repair file, and recompute intersections
of `content_group_sha256` by `provisional_split`. The newline-stripped line
hash convention is required: hashing the LF byte would disagree with the
recorded rowref hash despite identical JSON content.

This verifies current technical package integrity. It does not resolve the
source-rights and privacy dispositions recorded per source in the decision
ledger, nor does it claim clinical or production readiness. The user-authorized
research-training scope remains the release manifest's scope.
