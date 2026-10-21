# Full-corpus dataset size reconciliation — 2026-10-20

The counts refer to different snapshots and partitions. The older recovered
candidate has 190,139 rows (SHA-256
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`). The
frozen v4 release is built from the later current master with 190,244 rows
(SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`):

| Snapshot | Total | Non-ARC | ARC |
| --- | ---: | ---: | ---: |
| Oct. 17 recovered candidate | 190,139 | 189,159 | 980 |
| Oct. 19 v3 pre-completion master | 190,230 | 189,159 | 1,071 |
| Oct. 19 v4 final master | 190,244 | 189,159 | 1,085 |

This reconciles the 105-row difference: 91 ARC rows were already present in
the v3 current-master snapshot but not in the older recovery candidate, then
v4 added 14 more ARC rows from six completed arcs (`0319`, `0327`, `0342`,
`0380`, `0387`, `0392`). The 189,159 non-ARC rows match exactly as a raw-line
hash multiset between the older candidate and v4. All 980 ARC `(arc_id,
session_n)` keys in the old candidate still occur in v4, and their canonical
message hashes match; v4 has 105 additional ARC keys. The v3 row-reference
hash multiset is a strict subset of v4's, with exactly 14 new row hashes and
no removed rows; all 14 bind to `long_session_arc` rows in the six named arcs.

The count discrepancy between 190,244 total candidate rows and 171,261
training rows is the frozen split, not a missing 18,983 rows: 9,673 are
validation and 9,310 are test, and the three partitions sum to 190,244. The
release row references were independently recomputed against the current
master: all 190,244 one-based positions and candidate row hashes match, and
the `train`/`validation`/`test` content-group intersections are all zero.

This verifies snapshot identity, message-level continuity for the 980 shared
ARC keys, the 14-row v3-to-v4 addition, and the full split arithmetic. It
does not independently clear source rights, privacy, clinical quality, or
provider-transfer terms; those remain separate documented qualifications.

Reproduction inputs: the old recovery candidate and top-level manifest under
`ai/data/curated/recovery/gold-20261017/`; v3/v4 `rowrefs.jsonl` and manifests
under the same recovery directory; and the v4 current master at
`ai/data/curated/sft_chatml/train_master_gold.jsonl`.
