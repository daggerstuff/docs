# Gold dataset discrepancy investigation

Date: 2026-10-17. Active gold, arc records, audits, and source backups were not
modified. The 980-row file is an incomplete reconstruction of the master corpus.

## Numerical reconciliation

| Component | Rows | Evidence |
| --- | ---: | --- |
| Historical non-arc data absent from active gold | 189,159 | Identical byte slice in four dated gold backups |
| Current accepted, structurally valid arc sessions | 980 | Current gold; unique keys, all under accepted arcs |
| Superseded accepted arc versions | 19 | Seven older accepted versions retained in October 16 backup |
| Previously reported total | 190,158 | 189,159 + 980 + 19 |

The missing content categories survive locally. Recoverability does not mean
every historical row is approved for a new training release.

## What happened

Read-only inspection of the local OpenCode session database and process log
established this sequence:

1. At approximately 03:17:36 UTC on October 17, inspecting the master returned
   `No such file or directory`. The original file was already absent.
2. At 03:44:28 UTC, that earlier session ran
   `training/consolidate_arc_corpus.py` without `--dry-run`, using its default
   gold path. The recreated file's mtime is 03:44:34 UTC.
3. This consolidator reads arc records only. A missing master means an empty
   existing-hash set, and append creates the file. It therefore rebuilt only
   the accepted arc slice, leaving the broader corpus out.
4. The earlier session called the 980-session result a restored master. That
   completion claim was incorrect; it was only an arc reconstruction.

Evidence: session `ses_eb822eb8cffeettHQwVQ6WMotg`, command message
`msg_147f60578001DgPzn0zpEcmniJ`; the missing-file observation is in
`msg_147dd4ddf001HwLMeKuyZwLp4x`. Only relevant command/metadata evidence was
extracted; no full transcript is copied into this report.

The original deletion/move event remains **unidentified**. The rebuild did not
itself delete the non-arc data: the master was missing before it ran. Do not
attribute the disappearance to an agent, `uv`, a watcher, or another process
without evidence. This master JSONL is not Git-tracked; adjacent DVC entries
track train/val/test, not this file.

## Backup and session checks

All four `train_master_gold.jsonl.pre_*` backups parse. Their non-arc slices
each contain 189,159 rows and have SHA-256
`e5783f5b90ae7ee5111e6ea1a58306f7f8211c73a16084aa5fbd15498b284167`.
Recovery used `train_master_gold.jsonl.pre_stale_removal_20261010T040441Z` from
`ai/data/curated/sft_chatml/`. Historical arc rows from that backup were excluded
to avoid restoring stale versions alongside current sessions.

The sole accepted session absent from current gold is `arc_0366`, session 2.
The rejection log records `invalid_session: consecutive therapist turns`.
That explains 981 accepted-record sessions versus 980 gold sessions. There
are no duplicate gold arc/session keys and no keys outside accepted arcs.

The October 16 arc-record backup contains 435 physical rows but 424 distinct
arc IDs. Counting historical acceptance labels without resolving versions
overstates current acceptance. These seven arcs have older accepted content
followed by different content with null audit verdicts:

| Arc | Historical sessions |
| --- | ---: |
| `arc_0231` | 3 |
| `arc_0262` | 3 |
| `arc_0264` | 3 |
| `arc_0302` | 2 |
| `arc_0305` | 2 |
| `arc_0313` | 3 |
| `arc_0358` | 3 |
| Total | 19 |

Each older session-content hash differs from its current version. Acceptance
cannot transfer to the replacements. This explains the numerical remainder;
it does not reconstruct the exact historical master byte stream. All 936
arc/session identities in the Adaption run-2 export are present in current gold;
content equality is a separate check and was not inferred from key coverage.

## Recovery artifacts

Prepared in `ai/data/curated/recovery/gold-20261017/`:

- `arc_only_before_recovery.jsonl`: exact copy of current 980-row gold.
- `train_master_gold.recovered_candidate.jsonl`: 190,139 rows, 411,493,422 bytes;
  recovered non-arc slice followed by unchanged current gold.
- `quarantine_historical_accepted_arc_versions.jsonl`: seven records containing
  the other 19 historical sessions, preserved for separate disposition.
- `manifest.json`: source/output hashes, counts, checks, and open items.

Candidate SHA-256:
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`.
The [audit manifest](gold-recovery-audit-2026-10-17.json) also lives beside this
report. It contains metadata only, not conversation payloads.

Independent readback verified parsing, counts, unique arc/session keys, and
both slice hashes. Source hashes were checked before and after creation.
The historical version source was also checked around extraction. Nothing was
uploaded or promoted. Before training: validate source rights/privacy, content
decisions, duplicates, and splits; disposition the superseded versions without
copying old approval labels to new content.

## Adaption and Fireworks findings

Adaption was included in earlier plans and execution: runs 1 and 2 used
`Qwen/Qwen3.6-35B-A3B`. The October 15 log retained run 2 as a working reference.
Live read-only inspection confirms run
`8da8f685-7ef6-43c0-958e-ab34dbdcd520` succeeded and is downloadable. Its platform
win-rate is 0.6414, not an independent clinical-quality measure.

Both adapters are local: run 1's adapter is 4,101,280 bytes; run 2's is
27,535,856 bytes. The correct run-2 directory is
`ai/training/output/arc_corpus/export/adaption_run2_v1/checkpoint_run2/`.
The October 15 log's shorter `ai/training/adaption_run2_v1/...` path is incorrect.
Configs, tokenizer, template, and trainer state are present; inference still
requires a matching base and qualified runtime.
Safetensors header/payload length checks passed for both adapters (40 tensors
in run 1 and 80 in run 2); this checks file completeness, not model quality.

User-confirmed W&B inference credits and Adaption credits now fund explicit
campaign lanes; Fireworks inference credits remain tentative. Verify balances,
expiry, coverage, and bounds before spend. The inspected Adaption run object
exposes no credit usage. Its current catalog has SFT/DPO options for Gemma,
gpt-oss, Nemotron, and Qwen; per-model dataset floors and costs remain separate.
Existing model exclusions apply. W&B credits cannot pay other providers or
establish hosting support for arbitrary exported adapters.

Fireworks remains experiment-only until an authorized local export succeeds.
Its docs describe adapter downloads, but do not establish whether this account
can obtain access without paying. The recorded download failure establishes a
restriction, not its precise commercial condition.
[Download documentation](https://docs.fireworks.ai/fine-tuning/deploying-loras)

Periodic `save_state` and `save_weights_for_sampler` calls save remote training
state or sampler weights; they do not return a local tensor file. There is no
verified save-earlier route around download entitlement. Preserve local data,
configs, metrics, predictions, comparisons, and supported remote checkpoint
identities; evaluate before session-bound access ends.
[Checkpoint documentation](https://docs.fireworks.ai/fine-tuning/training-api/serverless)
