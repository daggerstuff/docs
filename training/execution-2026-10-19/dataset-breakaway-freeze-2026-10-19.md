# Dataset break-away freeze — 2026-10-19

## Frozen research-training snapshot

The break-away point is `wandb-full-corpus-current-master-20261019-v4`, pinned
by the release manifest SHA-256
`a4b0507ff6447644d022e28b1ada91daefa0139f23f8800ae953a0fa9ab5cdb8` and
source candidate SHA-256
`f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`.
The manifest is marked `approved_for_research_training` with `upload_gate=true`.
This is a technical release freeze for the user-directed research experiment;
it does not claim clinical or production readiness or settle upstream rights.

The candidate has 190,244 rows. Its exact partitions are 171,261 train,
9,673 validation, and 9,310 test rows. Independent local verification on
2026-10-19 recomputed each file's row count and SHA-256 and matched all four
manifest values. The manifest records pairwise group disjointness and zero
held-out-group intersections.

## Resolving the previously reported count difference

The earlier pinned source-decision audit refers to a distinct 190,139-row
candidate with SHA-256
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`. The v4
manifest records the owner-directed rebuild from the later final 190,244-row
gold candidate. These are different snapshots and hashes, not two counts for
the same file. The earlier v1/v2 training payloads contain 171,121 and 171,167
train rows respectively; v4 contains 171,261. The release manifest and the
source candidate hash are the authority for v4.

The independent hash-level reconciliation now accounts for the exact 105-row
candidate delta and the 18,983 rows assigned to validation/test rather than
training; see the [dataset size reconciliation](dataset-size-reconciliation-2026-10-20.md).

## Repair and provenance limits carried with the freeze

The manifest records 52 repaired rows: two source-quality triage
reconstructions and 50 source-dialogue recoveries with generated
continuations. The generated continuations have not received clinician
semantic review. Exact source-row binding remains incomplete across the
long-tail source families; see the
[source-locator metadata and exact-origin audit](source-locator-public-metadata-audit-2026-10-19.md)
and private per-source sidecars. Those limits are recorded as research-use
qualifications and do not change the user's instruction to train on the full
corpus.

The corresponding W&B job is `24cc2d06-3ec3-4356-ad3a-179694dd86a7`, created
for 171,261 training rows; its latest authenticated status check on 2026-10-19
at 20:01 UTC was still `PENDING` with no provider error, training start, or
numeric progress. The API `/system-check` reports all queues healthy but gives
no pending reason. The two earlier v1/v2 jobs remain separate, older snapshots
and should not be described as training on the v4 candidate.

## Active v1/v2 payload lineage to v4

An exact raw-line SHA-256 multiset comparison of the train payloads verified
that both active-job payloads are strict subsets of the frozen v4 train
payload: v1 has 171,121 rows, v2 has 171,167, and v4 has 171,261. Each
payload's row count and file hash match its release manifest. This proves exact
serialized-row identity for the overlap; it does not make the older runs v4
jobs.

The v2-minus-v1 difference is 46 rows (45 distinct serialized row hashes).
The v2 row references and exact candidate-row hashes identify 44 rows labeled
`psy_insight` and two labeled `clinical_book_Get More.....`. One serialized row hash occurs twice:
the two entries are distinct candidate rows (6,142 and 6,146), each binds to a
unique candidate-row hash, and both have the same source label. No
candidate-row-reference ambiguity remains in those 46 source-label bindings.

The v4-minus-v2 difference is 94 rows, all `long_session_arc` records. Each
has a distinct serialized row hash and uniquely matches its v4 candidate row
reference. The independent canonical ARC source binding for all 1,085 v4 ARC
rows, including these 94, is recorded in
[`v4 ARC lineage binding`](v4-arc-lineage-binding-2026-10-19.md).

Verification used the immutable payload paths in the three manifests and
row-reference order aligned with train payload order. It checked serialized
row-hash multiplicities (so duplicate rows were not silently collapsed),
matched candidate row hashes to the source candidate, and compared the
source-label counts. No training payload or job was changed.
These labels identify candidate provenance categories; this comparison does
not independently bind the rows to upstream source records or establish
rights, privacy, or transfer authorization.

## Provenance reconciliation update (2026-10-20)

The G04 release's 522 lineages now have an independent hash-only reconciliation to the pinned recovery candidate and G03 post-holdout rowrefs by raw candidate-line and message hashes; all rows bind and the 179 source groups stay split-disjoint. The two declared seed-artifact locator hashes are each reused across splits (522 references total), which is a traceability signal but not proof of content leakage. A read-only W&B run-history check found plausible generation runs using Featherless/Ornith-1.5-9B and Vercel/DeepSeek-V4-Flash-0731, but neither accepted seed JSONL nor its hash is linked to any run artifact. Provider attribution and output-use terms therefore remain unverified. Detailed IDs/counters are in the private reconciliation JSON referenced by the [G04 provenance report](g04-breakaway-origin-audit-2026-10-20.md). This audit changes no release or provider state.

A further hash-only replay bound the largest currently audited long-tail family
in the 190,244-row v4 candidate: `reddit_mental_nlp` (70,968 rows) was compared
with its protected local 701,787-row Kaggle CSV. All 59,574 source-row
ordinals/record hashes in the references revalidated against the exact CSV
snapshot; no locator was reused or crossed v4 splits. The row-level status
counts are 28,894 exact unique, 244 exact ambiguous, 29,515 normalized-only
unique, 192 normalized-only ambiguous, one user-only match with a label
mismatch, and 12,122 unmatched. The CSV has no stable Reddit post ID, and its
snapshot does not identify the curation-time export. No candidate or frozen
training payload changed. See the [complete Reddit Mental NLP source audit](reddit-mental-nlp-v4-complete-origin-status-audit-2026-10-20.md)
and [public source-row binding summary](public-source-row-binding-summary.md); private hash-only evidence remains under the local recovery sidecar directory.

The next source-family check added a hash-only prompt and locator split audit for
`mitch_hamidi_bpd_nlp` (13,890 v4 rows). It preserves the prior pinned-origin
statuses (8,000 unique, 313 ambiguous, 5,577 unmatched); 451 exact and normalized
prompt hashes cross splits (10,323 rows touched), while all 13,890 content
groups remain split-contained and all 8,803 bound locator references are unique
and split-stable. Candidate and v4 manifest hashes/counts revalidated. Details
are in the [Mitch Hamidi BPD NLP prompt and locator audit](mitch-hamidi-bpd-nlp-v4-prompt-locator-crosssplit-2026-10-20.md)
and [public source-row binding summary](public-source-row-binding-summary.md);
row-level hashes/locators are private mode 0600. Rights, privacy, consent,
clinical suitability, training eligibility, and provider-transfer decisions
remain unresolved. No candidate, release payload, or provider run changed.

The 13,890-row `mitch_hamidi_bpd_nlp` family also now has a current-v4
hash-only prompt/locator split audit: 8,000 exact source rows bind uniquely,
313 ambiguously, and 5,577 remain unmatched. Its 451 repeated prompt hashes
cross splits (10,323 rows), while candidate record hashes, manifest content
groups, and all 8,803 bound source locators remain split-contained. See the
[Mitch Hamidi audit](mitch-hamidi-bpd-nlp-v4-prompt-locator-crosssplit-2026-10-20.md).
A current-v4 inventory found no other family with both local canonical source
material and an unfinished audit. The largest remaining source-row-unbound
families are PsychEval (1,977; declared S3 unavailable and named public tree
lacks the described data), Counseling Conversations (1,415; manually gated),
and DAIC-WOZ (129; controlled access). No gated/controlled files were fetched.
See the [remaining source-binding boundary report](v4-remaining-source-binding-access-boundary-2026-10-20.md).
These access boundaries do not change the existing full-corpus research-training
instruction or frozen payload.
