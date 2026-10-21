# G04 break-away source-provenance reconciliation (2026-10-20)

The frozen 522-row G04 break-away package maps exactly to its pinned 190,139-row recovery candidate and to all 522 G03 post-holdout row references. At each recorded candidate index, both the raw candidate-line hash and canonical messages hash match; candidate indices are unique, and no row is unmatched or mismatched. The G03-to-G04 join also reconciles candidate-row hash, message hash, source-group hash, split, source-class and origin-assessment metadata, and hashed seed-artifact references.

The release has 410 train, 72 development, and 40 test rows across 179 source groups; no source group crosses splits. Message and canonical-row hashes are unique across all 522 rows. The package manifest lists 17 files, and every listed file hash matched on replay. The candidate is 190,139 rows with SHA-256 `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`; the G04 release manifest SHA-256 is `de3820398395629d73bdde0845f5aff7f5c0e7d02e63794fc35accf7fdc1cd9b`, and its lineage SHA-256 is `91ad5047d1dd382025e7fa825f2ffc1c75a2700b78e6ec74375f4dd541b1830b`. The G03 post-holdout row-reference file is SHA-256 `a5294068c241eb48007c6c33036da0c033a16198094c6e83f307eeaabf443a7a`.

The row metadata classify all 522 rows as `edge_cases` with a first-party synthetic edge-generator origin assessment. Two distinct seed-artifact locator hashes account for 522 references: one occurs in 105 train and 16 development rows; the other occurs in 305 train, 56 development, and 40 test rows. Thus both declared seed-artifact identities cross split boundaries, even though source groups and resulting row/message hashes do not. Shared locator identity alone does not establish duplicate content or leakage; it is a traceability signal for follow-up.

The remaining provenance gap is explicit in the frozen package: no artifact-bound historical generation receipt establishes the provider/model or output-use terms. The earlier provenance follow-up identified plausible runs but no run-to-output-hash binding. Next action: recover a contemporaneous receipt that ties the relevant generated artifact hash to its run and effective provider/model, then verify applicable output-use terms. Keep the package local-only until that evidence is resolved. Rights, consent, privacy, de-identification, clinical suitability, and provider-transfer clearance are not inferred here.

An authenticated read-only W&B metadata refresh found five `dataset_generation`
runs named `nf_bulk_*` in the surrounding dates. Three recorded
`featherless` / `ornith-ai/Ornith-1.5-9B` (Sep 13 and 14); two recorded
`vercel` / `deepseek/deepseek-v4-flash-0731` (Sep 17). The Sep 17 runs report
1 and 92 generated records respectively. W&B retained only each run's history
and events artifacts, not the accepted seed JSONL or its SHA-256. A separate
finished run from Sep 13 has no config and no logged artifacts. These records
narrow the plausible generation history but do not bind either accepted seed
file or the 522-row release to any specific run/model; no provider attribution
is upgraded on this evidence. The exact W&B run IDs and counters are preserved
in the private reconciliation report.

Independent hash-only row evidence is stored in the ignored private directory `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/`: rowref sidecar SHA-256 `937243d724bddfd9be0e21e2fa0e11b3517dce9996fa53b63c5178f8658474b1` (522 rows) and machine report SHA-256 `863d83e2e2b33e1f812ba8315a587c82429c6b09b722947b508816265942727f`. Both files are mode 0600 under a mode-0700 directory. The sidecar retains hashes, candidate row indices, and split labels only; it contains no dialogue or raw seed-artifact identifiers. No corpus, release payload, candidate, manifest, or provider job was changed.
