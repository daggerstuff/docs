# Training campaign execution handoff

## Live campaign refresh — 2026-10-20 09:22 UTC

W&B v4 job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` remains `RUNNING` with no
reported error. The latest event poll recorded gradient step 29,844/85,631 at
09:21:57 UTC (loss 0.8423). Local adapter and train-state checkpoint v58,
29,500 batches, are both present and passed size/SHA-256 verification (2 and
11 files respectively). The rolling checkpoint and event-observer processes
remain live.

The initial v56 paired evaluation completed with 240 successful calls, but a
runner bug meant its declared `enable_thinking=false` setting was omitted from
the HTTP request. Its empty SFT responses are real observations under the
provider default, but they are not a verified no-thinking result. The partial
v57 replay was canceled at 63 cases after finding the same mismatch. The
request client is fixed and tested (24 evaluator tests pass); a clean paired
v56 replay with the explicit setting is active under a $1.40 hard cap (preflight
maximum $1.35168). See the
[v56 report](execution-2026-10-19/wandb-v56-prompt-disjoint-paired-nonthinking-2026-10-20.md).
Fireworks' earlier Muse Glimmer session is now recorded as terminally
incomplete at 5,886/10,704 steps, with no trained checkpoint; use the corrected
[Fireworks report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

## Live campaign refresh — 2026-10-20 09:16 UTC

The Fireworks Muse Glimmer 30B experiment is terminally incomplete: its
session expired at 5,886/10,704 steps after a 10-minute period without active
runs. The launcher had disabled promotion and made no intermediate adapter or
optimizer saves; the remaining session checkpoint was only the base sampler.
There is no trained Fireworks model to evaluate. The SDK documents periodic
`save_state` and `save_weights_for_sampler` plus checkpoint promotion, so a
future attempt can preserve intermediate outputs, but it would be a new
experiment. The prior run's training was covered by the promotional offer;
sampling was separately metered. See the [Fireworks report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

The W&B v4 job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` is still
`RUNNING`, with no reported error. W&B has published adapter and resume-state
checkpoint v58 at 29,500 batches (09:15:27–09:15:30 UTC), sized 117,843,308 B
and 1,060,414,703 B. The local rolling mirror was one cycle behind at v57 when
last checked; its watcher remains active. This confirms the new checkpoints
the user saw belong to the current v4 stream.

The authenticated W&B project `storageBytes` meter is 60,634,387,885 B at
09:15 UTC, down 55,851,885,368 B from 116,486,273,253 B at 22:09 UTC on Oct
19. The earlier audit had been tracking v1/v2 as the active streams, but a
fresh inventory now shows both of their LoRA and train-state resume
collections have zero visible versions; v4 is the only one of those three
streams with versions. This strongly indicates the cleanup removed the older
v1/v2 checkpoint artifacts, while v4 continued writing new checkpoints.
Local copies of v1/v2 remain under
`ai/training/output/wandb_local_checkpoints_20261019/` (about 2.7 GB total).
The project meter drop indicates substantially lower project storage, though
W&B does not expose account quota or prove physical reclamation timing. No
remote changes were made during this check.

The v56 120-case paired evaluation is complete: 240/240 calls succeeded with
no runner errors. The base returned visible content in 103/120 cases and made
137 tool rounds; v56 SFT returned empty visible content in all 120 and made
zero tool rounds. This is a severe diagnostic failure, not a clinical-quality
score. Result-level estimated inference usage is $0.121252; actual billing was
not returned. A v57 SFT-only replay on the same 120 cases and exact request
settings is now running, with a $0.75 hard cap and $0.67584 preflight maximum.
See the [v56 evaluation report](execution-2026-10-19/wandb-v56-prompt-disjoint-paired-nonthinking-2026-10-20.md).

Adaption has one reusable exportable control: its completed 11,192-row Qwen
run is locally exported at
`ai/training/output/arc_corpus/export/adaption_run2_v1/checkpoint_run2/`.
The existing paired 52-case diagnostic has base-minus-run2 deltas of +0.0452
empathy, +0.0303 heuristic safety, and +0.0838 reflection on the legacy
heuristic; a separate blinded judge reports overall run2-minus-base -0.0522,
with 22 wins, 5 ties, and 25 losses. These are historical diagnostic scores,
not a fresh campaign evaluation. The environment has CPU-only PyTorch, no base
weights cached, 28 GiB RAM, and no compatible inference server; Adaption has
no hosted inference endpoint exposed. A fresh paired comparison needs a
qualified GPU or a CPU host with roughly 96 GiB RAM and the repo's
Adaption-specific loader. No new Adaption job was launched because the
available connector exposes no training-cost quote or credit balance; its
112-credit estimate is for data processing, not AutoScientist training.

## Live campaign refresh — 2026-10-20 09:10 UTC

The W&B v4 SFT job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` remains
`RUNNING`, at 29,196/85,631 gradient steps in the 09:09:50 UTC event poll,
with no reported job error. Adapter checkpoint v56 (28,500 batches) and its
train-state v56 were mirrored locally. All 11 train-state files listed in the
manifest passed local size and SHA-256 verification. The backup and event
observer processes remain alive.

The 120-case prompt-disjoint no-thinking comparison now has complete effective
coverage: all 120 base cases and all 120 v55 cases succeeded after a 45-case
base-only retry at a 4,096-token context cap. v55 returned visible content in
120/120 cases but made zero tool rounds; the base made 130 tool rounds. The
combined estimated inference usage is $0.10684050; provider billing was not
returned. The original paired manifest remains `incomplete` because it records
45 baseline preflight failures at the initial 2,048-token cap; the retry is
separately recorded and all rows are joined by case ID and case hash. See the
[full evaluation report](execution-2026-10-19/wandb-v55-prompt-disjoint-paired-nonthinking-2026-10-20.md).

The current Adaption dataset remains `awaiting_input` with 522,658 rows and
does not have an active processing or training run. Live estimate-only calls
confirmed the 50,000-row per-launch ceiling and returned 500 credits/635
minutes for 50,000 rows, and 227 credits/294 minutes for 22,658 rows. A
10×50,000 plus 22,658-row processing plan would total an estimated 5,227
credits and 6,644 minutes for Adaptive Data processing only. This is not an
AutoScientist training quote or evidence of available balance; no processing
or training job was launched. See the [Adaption refresh](execution-2026-10-19/adaption-credit-and-dataset-refresh-2026-10-20.md).

W&B's current [Serverless Training documentation](https://docs.coreweave.com/products/post-training/serverless-training)
labels the service public preview and explicitly says adapter training is
free during preview, with inference and artifact storage billed separately.
The current [Forge post-training pricing page](https://wandb.ai/site/pricing/training/)
instead lists SFT/RL at $2.70/GPU-hour; keep this
published-page conflict visible and check the account billing view for the
running job. The docs page itself was last modified October 9, 2026.

## Live campaign refresh — 2026-10-19 23:04 UTC

The Fireworks Muse Glimmer run is still active at step 242/10,704, with no
reported training error. The run remains experiment-only: checkpoint promotion
is disabled, and there is no persistent final adapter until training completes.
See the [live run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

A current Adaption refresh confirms the full-history and three ctx9 attempts
failed before optimizer iteration. The two latest attempts produced the same
empty validation-file error, once with message arrays and once with scalar
text. The successful 11,192-row control also used arrays, so serialization
type alone is not a proven cause. The failure is narrowed to the much larger
522,658-row v4-derived path or provider-side validation preparation; cause is
unresolved. Do not repeat Adaption v4 runs until isolated. The connector
exposes no current balance or v4 training quote. Its prior 112-credit estimate
applies only to the separate 11,192-row dataset. See the [Adaption
qualification record](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md).

The 13,890-row `mitch_hamidi_bpd_nlp` family now has exact non-system
turn-sequence source matches for 8,000 unique upstream rows, 313 ambiguous
duplicate matches, and 5,577 unmatched rows against the adapter-declared
repository pinned to commit `5867af435d9d667ae769058f893e3b35ea9f7496`.
All 14 source CSV hashes and private row-reference validation are recorded in
the [BPD origin-binding report](execution-2026-10-19/mitch-hamidi-bpd-nlp-v4-origin-binding-2026-10-19.md).
Rights, Reddit terms, privacy, consent, and provider-transfer eligibility
remain unresolved; source correspondence is not clearance.

This turn's direct read-only W&B Training API probes returned HTTP 403 for the
OpenAPI and system-check endpoints, so no fresh job status was established.
Treat the last timestamped artifact and job records below as historical until
the authenticated status path is restored. No W&B job or artifact was changed.

Updated: 2026-10-19 23:16 UTC.

## Live recheck — 2026-10-19 23:15 UTC

The authenticated W&B Training API now reports the stripped-system v4 baseline
job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` as `RUNNING`, updated
2026-10-19 22:50:52 UTC; it exposes no step count. The same read returned HTTP
500 for v1 and v2, so their current status is unknown, not terminal. See the
[timestamped status poll](execution-2026-10-19/wandb-job-poll-20261019T2317Z.json).

Fireworks PID 518909 remains active at step 253/10,704 (23:16:17 UTC), with no
reported training error. The last eight measured step intervals range from
55–82 seconds. If that short sample holds, roughly 10,451 steps remain, or
about 6.7–9.9 days before the built-in paired evaluation; this is a rough
cadence projection, not a provider ETA. No tuned checkpoint is saved until
training finishes.

The next-largest publicly sourceable family, `reddit_mental_health_posts`
(30,444 v4 rows), now has 10,693 unique exact adapter-projection matches,
zero ambiguous matches, and 19,751 unmatched rows against a pinned Hugging
Face revision. No source groups or matched rows cross splits. This is
technical origin evidence only: the upstream listing has no license value,
and Reddit rights, privacy, consent, terms, and provider-use status remain
unresolved. See the [origin-binding report](execution-2026-10-19/reddit-mental-health-posts-v4-origin-binding-2026-10-19.md).

## Adaption scalar-text retry — 2026-10-19 23:12 UTC (failed)

The previous chat-format retry failed at 0/1 because the raw `prompt` and
`completion` fields were arrays. Adaption's raw SFT documentation specifies
text columns, and the provider's generated validation JSONL was empty. A new
role-labeled scalar-text ctx9 package preserves all 522,658 assistant targets
and was accepted as ready dataset `c00e322e-3842-4a56-9e6b-b9c81cf8b599`.
Its no-augmentation Qwen3.6-35B-A3B run
`ef278ee7-b04d-4014-9b7a-cb7ee81b66fd` failed at 0/1 with the same empty
validation-file error. The successful 11,192-row control also used arrays, so
scalar versus array fields do not explain the observed difference by
themselves. The 522,658-row path or provider-side validation preparation is
the remaining failure area, not a confirmed root cause. Training and export
did not occur. Balance and cost remain unknown. See the dated Adaption
qualification refresh and the
[local package manifest](../../ai/training/output/adaption_v4_unrolled_ctx9_text_20261019/manifest.json).

## Adaption retry — 2026-10-19 23:07 UTC (failed)

After the prior rate-limit window elapsed, one corrected Adaption run was
created against the ready 522,658-row ctx9 v4-derived dataset. It uses the
structured-message `chat` encoding, no augmentation, Qwen3.6-35B-A3B, and a
one-iteration cap. Adaption returned run
`33bba6d2-d9e5-408c-bd4d-76544d2cde78` as `running` at 0/1, without error or a
checkpoint at creation. This fixes the prior instruction-encoding mismatch;
successful training and export are still unverified. The cap bounds it to one
iteration, but the exact credit balance and this v4 run's credit cost remain
unknown, so no amount of credit coverage is claimed. The request and response
are in the [timestamped Adaption record](execution-2026-10-19/adaption-live-refresh-20261019T2307Z.json). Follow-up polling showed this job failed before iteration because the generated validation JSONL was empty; the submitted raw prompt/completion columns contained arrays although the provider docs specify text columns. The corrected scalar-text attempt is recorded in the qualification refresh below.

## Current execution update — 2026-10-19 20:14 UTC

A project-wide W&B Artifact API comparison now covers 285 collections: all 447
versions visible at 19:39 are still present at 20:12, with 14 new versions in
the active v1/v2 checkpoint streams and zero disappeared versions. Latest
heads are v1 v127 and v2 v125; the exact snapshot is mode 0600. This confirms
the cleanup did not remove any visible artifact versions from this W&B project
after 19:39, but still cannot identify earlier, other-account, or non-artifact
deletions. Current v1/v2 jobs remain RUNNING and v4 remains PENDING; the
Training API still returns no progress or error reason for those jobs. The
[storage reconciliation](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md)
has details.

Fireworks PID 518909 is active at step 67/10,704 (20:13:48 UTC). The current
checkpoint watcher and mirrors are live. See the [Fireworks run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

The 20:10 local W&B mirrors now contain the newest visible adapter and
train-state heads: v1 v127 (64,000 batches) and v2 v125 (63,000 batches). Both
adapter files per job and all 11 train-state files per job passed size/SHA-256
verification. W&B reports v1/v2 RUNNING and v4 PENDING at the 20:14 API poll;
no error or numeric progress fields are exposed. The project-wide inventory
supports that the earlier cleanup did not remove any visible artifact version
after 19:39.

The 50 generated-continuation Psy-Insight repairs now have a separate pinned
source-excerpt binding: every repair case ID uniquely resolves to the
content-hashed Hugging Face revision and candidate row hash, and all 50 map to
v4 (44 train, 2 validation, 4 test). This documents the excerpt used to create
each prompt; the generated assistant target is still not an upstream source
response. Private hash-only evidence and limits are recorded in the [source
metadata audit](execution-2026-10-19/source-locator-public-metadata-audit-2026-10-19.md).

The largest family source binding is now documented with reproducible file
hashes and private row references. For the separate 13,890-row
`mitch_hamidi_bpd_nlp` family, an authenticated read-only listing of its
declared `whitebat:` prefix returned HTTP 403 `UserSuspended`, and the adapter's
GitHub URL returned 404. No matching source files were available through those
locators; this does not invalidate the corpus or identify an equivalent source.
See the [source/cache audit](execution-2026-10-17/top-reddit-source-local-cache-audit-2026-10-19.md).

At 20:12, the newest local mirror snapshot was still 20:09 UTC. The watcher is
on its five-minute cadence; its next inventory will confirm the current local
checkpoint heads.

## Current execution update — 2026-10-19 20:10 UTC

The largest unresolved family, `reddit_mental_nlp` (70,968 rows), now has a
current-snapshot source binding. The adapter-declared Kaggle CSV was downloaded
privately and matched using its actual text/label transformation. 58,409 rows
bind uniquely (28,894 exact and 29,515 case/whitespace-normalized); 436 are
ambiguous, 12,122 unmatched, and one has a label mismatch. All 58,409 unique
row bindings transfer by candidate hash into v4 (52,527 train, 2,991
validation, 2,891 test). The original curation-time Kaggle version remains
unknown, and rights/privacy status remains unresolved. Raw text is not in the
sidecars. Details and private evidence locations are in the [Reddit source
binding update](execution-2026-10-17/top-reddit-source-local-cache-audit-2026-10-19.md).

Fireworks remains active; the worker reported step 64/10,704 at 20:10:29 UTC.
See the private [run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

## Current execution update — 2026-10-19 20:08 UTC

The user's storage cleanup overlapped with active checkpoint writes. A fresh
read-only W&B Artifact API query confirms the four inspected v1/v2 LoRA and
train-state streams continued advancing through 20:03:44 UTC (v1 heads v126;
v2 heads v125). The cleanup did not remove versions from those streams, so the
items the user deleted may be elsewhere in the artifact view. The earlier
train-state cleanup candidates are conditional only and do not identify the
objects seen in the UI. The API exposes neither deletion history nor reclaimed
physical quota. See the [timestamped storage recheck](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).

Fireworks remains active at step 60/10,704 as of 20:06:44 UTC. See the private
[run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md)
for the current observed cadence and limitations.

## Current execution update — 2026-10-19 19:57 UTC

The same-candidate, same-split W&B system-context-preserving v4 package now
passes the G04 release dry-run: 171,261 train rows, a 340,989,438-byte dataset
artifact, and no upload/job created. Split membership is inherited from the
verified v4 rowrefs; all non-system messages match v4, while system messages
are retained with zero loss weight. The staged manifest keeps `upload_gate`
false pending storage and job-capacity qualification. Its machine-readable
record is [here](execution-2026-10-19/wandb-full-corpus-current-master-20261019-v4-preserve-system.json).

Live Adaption checks found a non-launching estimate of 112 credits/150 minutes
for the existing succeeded 11,192-row dataset; the connector still does not
expose the available balance, so no job was started. This is not a v4 estimate.
The 418-row dataset remains `awaiting_input`; its `messages`-as-chat processing
estimate is 5 credits/16 minutes, and Adaption will not recommend training until
it is ready. Details are in the [Adaption
qualification refresh](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md).

The latest W&B Training API poll at 20:01 reports v1/v2 RUNNING and v4
PENDING, with no reported provider errors or numeric progress. `/system-check`
reports the API, database, CPU queue, model-management queue, and GPU queue
healthy; it gives no reason why v4 remains pending. The 19:59:25 local train-state
manifest now shows v1 v126/v2 v124; all 11 files in each latest state
checkpoint passed SHA-256 checks. The 19:56 adapter manifest shows v1 v125/v2
v124, and both adapter files passed their stored size/hash checks. The
Browserbase W&B tab is logged out, so the exact UI items deleted remain
unmatched; the API has no deletion history or physical quota meter. See
[storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).

Fireworks PID 518909 is still live. The last observed training progress was
57/10,704 at 20:05:28 UTC. Recent intervals vary; the current observed sample
supports only a rough multiday estimate, not a reliable completion time.
Paired evaluation has not started. Fireworks stores
no periodic tuned checkpoint in this run, and its final weights remain
temporary until the evaluation lifecycle completes. Current live details are
in its [run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

The latest paired W&B inference checks on v1 v125 and v2 v124 both completed
16/16 calls under the $0.10 per-run hard cap. Each adapter still emitted the
same `BPD` response on all eight synthetic cases, with no tool calls and 0/24
state checks passing; base outputs were varied and passed 22/24 and 24/24
checks. Usage-based estimates were about $0.011 per comparison; W&B did not
return billed totals. This confirms the narrow diagnostic collapse in newer
checkpoints and prioritizes the staged system-context ablation. Full report:
[paired eval results](execution-2026-10-19/latest-checkpoint-evals/report.md).

## Storage/checkpoint correction — 2026-10-19 19:52 UTC

A direct recheck of the four active W&B checkpoint collections confirms new
versions appeared during cleanup: v1 is now at LoRA/train-state v125 and v2 at
v123. The earlier comparison only establishes that these active checkpoint
collections retained their visible versions; it does not establish which
artifacts the owner deleted. Treat prior old-checkpoint deletion candidates as
unmatched to the UI until the actual item names are identified. Current W&B
artifact API exposes no deletion history or physical quota. Details:
[storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).

## Full-corpus execution — 2026-10-18

Responding to the owner's direction, the full 190,139-row recovered candidate is
now the active research-training source. I built a new W&B release containing
**190,087 trainable rows across all 475 source labels**: 171,121 train, 9,664
validation, 9,302 test. The 52 exclusions are structural only: two rows have no
assistant target; 50 have no user prompt before an assistant target. Exact
message groups are kept in one split; 31 groups contain duplicate rows. The
original candidate remains unchanged.

The automated pass redacted 73 emails, 59 phone patterns, 195 IPv4 patterns,
2,854 URLs, and 10 Luhn-valid payment-card patterns. The same-pattern scan
returned zero hits on the rendered release. No NER pass ran, so this is a
research candidate, not a de-identification certification or clinical/production
release. Full source-level counts and hashes are in
[the full-corpus release manifest](execution-2026-10-18/wandb-full-corpus-release.json);
files are under `ai/data/curated/recovery/gold-20261017/wandb-full-corpus-20261018/`.

W&B accepted the full-corpus job **`2087f223-a48f-45f7-9999-daece5743bba`**
and its status is `RUNNING` (last checked 22:44:42 UTC). It uses Qwen 3.6
35B, 171,121 train rows, and the full-corpus artifact
`wandb-artifact:///wutang/pixelated-empathy-kan28/g04-wandb-full-corpus-20261018-v1-baseline-8ce8354c67ef:v0`
(296,246,318 bytes; payload SHA-256
`04217267a3e9e2d4219edc871a4c7b493b3766536a7c736e0e445ccaa1f45cd6`). The
persisted state file is
[wandb-sft-8ce8354c…json](execution-2026-10-18/wandb-full-corpus-state/wandb-sft-8ce8354c67ef10915f78ebd385950aaed8fcac505578645dba907d330befbe91.json).
The 2,093-row and 80-row experiments remain separate comparison arms. Next,
poll the full-corpus job and evaluate its checkpoint against the 9,302 held-out
rows plus the sealed scenario suite.

## Live training progress — 2026-10-18 16:26 UTC

A second W&B managed SFT job was created from the existing project source-family
manifest dispositions for PsychEval (`SRC-036`) and DSM vector-space
(`SRC-044`), both marked `permissive-use` and `supervised-finetuning`. No
new per-row acceptance packet was requested. The release contains 2,093 rows
(1,977 PsychEval and 116 DSM vector-space): 1,673 train, 210 validation, and
210 test. Train source counts are 1,581 and 92 respectively. Its immutable
manifest, row hashes, split hashes, assistant-only loss mask, and automated
identifier screen are recorded in
[the release manifest](execution-2026-10-18/wandb-policy-permissive-sources-release.json).
The source candidate itself remains unchanged at 190,139 rows. This experiment
is scoped to research behavior comparison; it is not a clinical or production
release.

W&B accepted training job **`4dee0d62-ffc0-43e2-a300-2776723a1011`** for
`Qwen/Qwen3.6-35B-A3B` (remote model `a856188b-36c9-44de-a4bc-5c9e7acc6f40`).
The API creation response returned `PENDING`; a subsequent status GET returned
HTTP 403 with the available workspace credential, so the current provider state
is unverified. The persisted launcher state is
[wandb-sft-f00e0bf…json](execution-2026-10-17/wandb-sft-state/wandb-sft-f00e0bf27bf322be1772b4f330efcfce972635d41428c61be376307c18991ae6.json).
The uploaded dataset artifact is
`wandb-artifact:///wutang/pixelated-empathy-kan28/g04-wandb-policy-permissive-sources-20261018-v1-baseline-f00e0bf27bf3:v0`.
Dataset payload SHA-256: `9e38a5a0b44129e4ba35ffca2877c3e688d997b98a22bc9bc8a0623f12b774a0`.

Next execution is to restore status access and poll both active W&B jobs, then
score the new checkpoint on held-out evaluation. The existing 80-row synthetic
edge-matrix job is separate. Continue expanding experiments using project
source dispositions and synthetic data, and run a matched-base Adaption
comparison once credit availability is confirmed. The detailed live counts and
status are in
[the provider checkpoint](execution-2026-10-18/provider-and-eval-checkpoint.json).

 User authorized process-only use of existing local
`.env` credentials for bounded provider work; values must stay in child-process
environment and must never be printed or persisted. At the 02:55 UTC checkpoint,
no upload or training job had occurred. The earlier W&B smoke made
12 requests (5 successful corrected responses, 7 HTTP 400); successful-response
usage estimates $0.00147125, while actual billing for rejected calls is unknown.
The newly authorized synthetic diagnostic used all six planned completions over
two runs; combined usage-based cost estimate is $0.00248575, and provider-reported
actual billing is unavailable. No upload, training job, or deployment has occurred.

## Resume context

Read [the campaign plan](free-training-experiment-plan-2026-10-17.md), then
[the discrepancy report](gold-discrepancy-investigation-2026-10-17.md). Detailed
hashes live in [the recovery audit](gold-recovery-audit-2026-10-17.json). Current
execution state lives in [the registry](execution-2026-10-17/registry.json).
Do not restart the investigation or trust older completion claims over these
artifacts. Preserve unrelated workspace edits and submodule boundaries.

The full gold master was already missing when a prior session inspected it
at 03:17 UTC. At 03:44 it ran the arc-only consolidator and incorrectly called
the 980-row result a restored master. Original deletion/move is unidentified.
Four backups agree on 189,159 non-arc rows. A separate recovery candidate now
contains those rows plus unchanged current gold: **190,139 rows**. Another
**19 sessions in seven superseded accepted versions** survive separately;
their replacements have different content and null audits. Never transfer old
approval labels to replacements. These categories sum to the historical
190,158. The 981-versus-980 accepted-session difference is the valid structural
rejection of `arc_0366` session 2.

## Local artifacts and invariants

Recovery directory: `/home/vivi/pixelated/ai/data/curated/recovery/gold-20261017/`.

| File | Meaning |
| --- | --- |
| `train_master_gold.recovered_candidate.jsonl` | 190,139-row recovery candidate, not release-approved |
| `arc_only_before_recovery.jsonl` | Exact copy of active 980-row gold |
| `quarantine_historical_accepted_arc_versions.jsonl` | Seven older records containing 19 sessions |
| `manifest.json` | Source/output hashes and verification |

Candidate SHA-256:
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`.
Active master SHA-256:
`e3fc508e6c7bec360f9b67e5c963bdf14e2f4e08752c0e6b7900d380a964ace5`.
Non-arc slice SHA-256:
`e5783f5b90ae7ee5111e6ea1a58306f7f8211c73a16084aa5fbd15498b284167`.
Do not overwrite active gold, old exports, or recovery artifacts. Write new
versioned views, verify input identities before/after, and record exclusions.

## Execution completed

The [local preflight](execution-2026-10-17/recovered-gold-preflight.json) checked
the candidate and existing train/val/test artifacts without changing them:

- 190,139 parsed rows; 190,127 distinct complete-message JSON payloads.
- 12 duplicate message rows beyond the first; 2 rows lack a nonempty assistant
  target. Both findings are in the non-arc material. Identify their overlap
  before combining exclusion counts.
- All 180,460 existing train payloads occur in the recovered pool; none of the
  38,766 validation or 38,784 test payloads match exactly. Those three old
  splits are mutually disjoint by this exact hash. Semantic overlap is untested.
- Source references exist on all rows, but explicit license, consent, and
  privacy-review fields were not found in the inspected metadata locations.
  Absence is not proof of missing rights; source-level evidence needs joining.
- All 980 arc rows have provenance; only 8,699 non-arc rows have a top-level
  provenance field. Recover source mappings before assigning groups.
- Candidate and historical split hashes were rechecked after the census.

Earlier verified preparation tests: 7/7 passed. Both Adaption adapter files
passed safetensors header/payload-length checks. Neither check proves quality.

## Historical checkpoint — 2026-10-17 15:46 UTC (superseded below)

G02 evidence reconciliation is complete, with training clearance unresolved.
The [source decision ledger](execution-2026-10-17/source-decision-ledger.jsonl)
contains 190,139 candidate row references joined to 1-based row number, exact
row SHA-256, and canonical message SHA-256. It is grouped by source label and
contains metadata and hashes only. The candidate still hashes to
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`.

Evidence confirms the source review is awaiting human sign-off, all five
source-family manifests are proposed rather than ratified, and seven generic
license classes do not establish row-level clearance. Exact aliases connect
177,423 rows across 16 source labels to proposed per-source manifest records.
This is a per-source evidence gap, not a finding that every source is
prohibited. AnnoMI's 98 candidate rows have positive source-level claims in the
representative registry and project catalog; a hash-only comparison also
corroborates 4,848 unique candidate message hashes against the local source
CSV. The official repository shows public availability but no license file.
The direct-use claim conflicts with a proposed `deprecated-restricted`
manifest, and its provenance placeholder is not a valid SHA-256 content
digest. The source remains unresolved for rights and privacy; identity evidence
does not bind the review to exact candidate rows. Per-source notes are in the
[eligibility summary](execution-2026-10-17/source-eligibility-summary.json) and
[evidence inventory](execution-2026-10-17/source-evidence-inventory.json).

G03 is in progress. The [structural exclusions ledger](execution-2026-10-17/exclusions.jsonl)
records 12 duplicate payload rows beyond first occurrence and 2 rows without a
nonempty assistant target, with zero overlap (14 unique structural exclusions).
Pilot lineage was checked against the actual plans and successful seed-map
entries: 9 pilot IDs map from nonempty plan seeds (19 rows); `pilot_01` remains
unresolved (2 rows). Across all 980 arc rows, 927 map to one normalized
successful seed key, 51 are ambiguous across distinct keys, and 2 remain
unmapped. The [lineage and reservation report](execution-2026-10-17/g03-lineage-reservation.json)
also joins 58 historical held-out cases to 22 seed groups; 87 candidate arc
rows share those groups and must be reserved. All 58 held-out prompts show at
least 0.80 filtered five-token-gram containment against candidate arc rows.
The 52 golden controls have no source identity metadata; their training overlap
cannot be cleared by source lineage. The old all-58 high 5-gram overlap estimate
and 0/980 archive-binding warning in this checkpoint are superseded by the
16:23 checkpoint below: exact renderer matching is 980/980, and the edge branch
has an exact group-excluded diagnostic screen. The historical section is kept
only to preserve the sequence of findings.

The old Oct 17–31 calendar schedule is superseded by dependency-driven immediate
execution. Local checks proceed back-to-back; only evidence, source-owner
decisions, or provider access/credit qualification can pause dependent work.
No duration is forecast without measurement. The execution plan records these
gates. No training jobs, uploads, or deployments occurred. The later bounded inference
smoke and its uncertain rejected-call billing are recorded in the current
checkpoint below.

## Live execution checkpoint — 2026-10-17 16:40 UTC

The prior **0/980** candidate-to-archive content-match warning is superseded. A
stable private copy of `arc_records.jsonl` was captured under
`ai/data/curated/recovery/gold-20261017/lineage-evidence-snapshot-20261017T1559Z/`
(mode 0600; parent directory mode 0700; 35,508,867 bytes; SHA-256
`31a3f6e354928c79792f3f4a501402471095a95c65672f95c2cb6c56b1624a3f`). The
exact renderer in `ai/training/consolidate_arc_corpus.py::_session_messages`
reproduces **980/980** candidate ARC message payloads by `arc_id` and
`session_n`; writer/auditor/plan/spec metadata and machine `accept` verdicts
match on all 980. This is content-specific binding, not approval transfer by ID.

Separate lane-2 review artifacts remain keyed by ARC ID and do not include the
candidate payload SHA-256. Do not transfer those decisions by ID alone. The 58
held-out final-turn cases resolve to 22 seed groups; 87 candidate ARC rows across
34 IDs share those groups. The 52 golden controls still lack source identity.

The edge-case generator was traced to a hardcoded 10-family × 3-difficulty ×
4-ambiguity prompt matrix and uses no external clinical seed narrative for that
branch. Exact heldout-group matching removes 29 of its 551 candidate rows across
12 ARC IDs. Its remaining 522 rows span 179 groups and have a provisional,
group-disjoint split (410 train / 72 validation / 40 test; 139 / 25 / 15 groups).
The exact post-holdout identities are in
[the metadata-only rowrefs](execution-2026-10-17/g03-edge-case-post-holdout-rowrefs.jsonl);
29 heldout exclusions are separately listed. The source-origin and diagnostic
reports record 0 matches across six basic PII regex patterns on all 551 rows,
plus 0/522 retained rows at >=0.25 filtered 5-gram containment against the 58
heldout prompts or the 52 golden controls. Against controls, 371 rows had some
low lexical overlap. This is a near-duplicate screen, not proof of semantic
independence. Golden-control IDs remain unavailable. `clinical_reviewed=true` is auto-set by the generator and
is not clinical review evidence.

The generated-source inventory found a timestamped output artifact (212 rows,
120 edge and 92 Nightmare) with hash
`f601a0b8e7dba97db888e63d585cb5309ce734b3f40254b9dfe232d0bf01ce20`, but no
provider/model fields. Targeted read-only OpenCode session metadata searches for
Sep 17–18 generator/artifact/`NF_BACKEND`/`NF_MODEL` terms found no receipt; no
Claude logs were present for those dates, and Foresight keyword search found no
receipt. The generator reads these from `NF_BACKEND`/`NF_MODEL`; present defaults
are not historical proof. No `.env` or credential values were inspected. Recover
a contemporaneous run receipt and verify the terms that permit retaining these
synthetic outputs for research fine-tuning and transfer to the selected provider
before authorizing any provider operation. A private local-only weighted draft
payload is now rendered and independently byte-verified; the missing receipt
and scoped terms check still block approval or transfer. This exact first-party
edge branch does not need generic source-family signoff by default. Nightmare Fuel-derived rows,
ambiguous/unknown rows, and structural exclusions remain out of scope. No
A private local-only weighted payload package is now materialized at
`ai/data/curated/recovery/gold-20261017/g03-edge-review-package-20261017T1626Z/`
(mode 0700; files 0600). Its train/validation/test files contain 410/72/40 rows,
with exact SHA-256 identities in [`g04-release-manifest.json`](execution-2026-10-17/g04-release-manifest.json).
All 522 rows were joined to exact candidate row and message hashes, and the
rendered files exactly match the existing weighted exporter projection. The
manifest remains `draft_local_only`, has `release_id: null`, and
`upload_gate: false`; it is not approved or promoted. See the
[metadata-only render report](execution-2026-10-17/g04-edge-render-report.json) and the [independent package verification](execution-2026-10-17/coordinator-package-verification.json).

Historical P00 checkpoint (before process-only credential authorization and the
2026-10-18 diagnostic): the bounded W&B smoke completed 12 inference requests:
5 successful corrected responses and 7 HTTP 400 responses.
Successful usage totals 430 prompt and 1,091 completion tokens, with a
$0.00147125 cost estimate; actual billing for rejected calls is unknown. The
all-request theoretical ceiling is $0.005376 under the $0.01 cap. Three replies
were length-truncated. The next synthetic diagnostic and updated cap status are
recorded below. No uploads, training jobs, or deployments have occurred. The W&B SFT launcher passed Ruff and 9 focused tests and rejects
the current draft before payload preparation. E00 preparation checks passed 7/7;
paired runner offline tests passed 20/20 and Ruff is clean. Five-case dev and
sealed synthetic groups and local multi-step tool mocks are implemented. A
separate two-case support/research run plan is capped at six completions, 1,024
input tokens including tool traces, 1,024 output tokens, two tool rounds, no
retries, and a $0.02 budget; its theoretical bound is $0.009216. It is
separate from the completed $0.01 smoke scope. E00 remains in progress until
provider-paired qualification and scored evaluation can run under the
credential policy. The coordinator independently verified
the current draft package hashes, row counts, permissions, assistant-only loss
weights, and pairwise group disjointness; see
[the package verification](execution-2026-10-17/coordinator-package-verification.json).

The source-origin and break-away reports are in
[the generated-seed origin report](execution-2026-10-17/g03-generated-source-origin.json)
and [the row decision packet](execution-2026-10-17/g03-edge-case-breakaway-review.json).
They distinguish the first-party synthetic edge branch from the Nightmare Fuel
scenario-derived branch and record 51 ambiguous and 2 unknown rows. The
historical 522-row draft remains blocked on its missing generation-provider/model
receipt and applicable terms. A separate W&B/Qwen first-party regeneration plan
is prepared in [g03-edge-regeneration-fallback.json](execution-2026-10-17/g03-edge-regeneration-fallback.json);
it is not executed and cannot clear or replace historical rows. New generation
now records provider/model/config/code/source hashes and invocation-scoped usage
in a private receipt, uses unique run IDs while preserving identity on resume,
rejects incompatible resumes, and sets `clinical_reviewed` to false while
preserving machine `mi_quality` tiering. Prior generated files
were not changed.

## Provider decisions that must survive compaction

| Provider | Agreed role | Remaining qualification |
| --- | --- | --- |
| W&B | **Serverless Training, including SFT, is explicitly in public preview.** The Serverless Training documentation says that during preview adapter training is free and only inference usage and artifact storage are charged. The Forge pricing page separately lists SFT/RL at $2.70/GPU-hour, creating a direct published-page conflict. Treat the training docs' free-during-preview statement as the documented preview offer; retain the pricing conflict as a billing risk and check account billing after runs. Inference and storage remain separately chargeable. Adapters are stored as artifacts, can be saved locally/elsewhere, and checkpoints are hosted for Serverless Inference. API access and 13 trainable bases were verified 2026-10-18. | Continue the already-running job and protect its local adapter/train-state backups. Budget inference and artifact storage separately. Capture the account billing view for the run to resolve whether the conflicting rate card applies to this account. |
| Fireworks | Glimmer SFT experiments and comparisons; experiment-only until export succeeds | Promo/account eligibility, inference credits, hosted evaluation cost, download entitlement |
| Adaption | Credit-funded exportable lane; reuse the successful 11,192-row run 2 adapter first. A full 522,658-row dataset is already processed on `5cf8...`, but its two AutoScientist training attempts failed before iteration 1 because the provider produced an empty validation JSONL. | `60ea...` remains `awaiting_input` despite mapped prompt/completion fields; raw-ingest path differs from the successful SDK-shaped raw upload. No balance or AutoScientist training quote is exposed. Diagnose the validation writer and obtain an order-preview quote before another training run. |

Fireworks docs checked October 17 advertise Glimmer SFT through November 30;
verify account-specific eligibility before use. The offer date is a provider
condition, not a campaign target. DPO/RL/deployments are not covered
by that SFT offer, and sampling is separately priced. Remote `save_state` and
`save_weights_for_sampler` are not local weights backups. No verified early-save
workaround exists. Existing managed checkpoint evaluation can use a qualified
preemptible deployment instead of waiting solely on downloads. No ordinary
serverless chat deployment exists for a trained Fireworks LoRA.

Adaption run 2: `8da8f685-7ef6-43c0-958e-ab34dbdcd520`, live `succeeded`,
`download_available=true`, base `Qwen/Qwen3.6-35B-A3B`, rank/alpha 32, q/k/v/o.
Local checkpoint:
`ai/training/output/arc_corpus/export/adaption_run2_v1/checkpoint_run2/`.
Its 0.6414 platform win-rate is not a clinical verdict. Run 1's adapter is also
local under `export/fireworks_pilot_v1/adaption_run1_qwen36_lora/`.
Exact credit usage is not exposed by the inspected Adaption run object.

Fireworks old pilot: job `wwopccov`, model
`accounts/linencloset/models/arc-pilot-v1-therapist-sft`; prior download attempts
failed HTTP 400/code 9. Precise payment/entitlement terms remain unverified.
Support request was sent October 15. No further message is authorized here.

Do not use the chat-exposed Together key; rotation is required and it is absent
from these artifacts. Together is optional, not an assumed free training lane.
W&B credits cannot pay another provider or establish arbitrary-adapter hosting.

## Execution constraints

- User authorized continuation and credit-funded experiments within the staged
  plan. Qualify actual coverage and bounded costs before each launch; no
  uncovered spend or assumption that free training includes inference/storage.
- No Llama; preserve Qwen 3.8 exclusion. Qualify exact provider model support.
- 1,122 writer preference pairs are not therapist-turn DPO. Rebuild exact-prefix
  turn-level pairs and review before therapist preference optimization.
- Existing length/ngram RL reward is unsuitable for clinical alignment.
- Use blind calibrated comparisons, independent task truth, grouped uncertainty,
  clinical review where needed, and a sealed final test. Never optimize on it.
- EKS is production, Vercel frontend testing. No deployment to production here.
- Use `uv`/`pnpm`; no `tsc`, `astro check`, or `pnpm typecheck`; no suppressions.
- No project-root agent configs, raw conversation dumps, secret values, or PHI
  in public logs/artifacts. Keep datasets private. Preserve unrelated edits.
- AWS CLI Agent Toolkit and the `aws-core` Codex plugin are installed. An
  `asm-exec`-wrapped read-only AWS identity check passed in `us-east-1`; the
  shell's default region is invalid. Provider API keys are non-dynamic `.env`
  values and no provider-matching Secrets Manager entries were found. The user
  authorized process-only use for bounded provider operations; never print,
  persist, or copy those values.
- Foresight continuity is updated. Read it at resume; capture decisions in flight.

## Runtime transition

The active main model was intentionally unchanged. Execution was routed to the
lower-cost `gpt-6-luna` workers for training execution, provider qualification,
and evaluation readiness; automatic context compaction was observed. No client
model-switch action is required. This handoff is the compact continuation packet
and current registry is authoritative for worker/smoke status. The 2026-10-18
resume verified the Adaption run-2 dataset (11,192 rows) and successful
downloadable Qwen3.6-35B-A3B run; the separate 418-row `train` dataset is still
`awaiting_input`. The 522-row package's counts, hashes, file modes, and
assistant-only weight contract reverified; 47 focused curation/evaluation tests
passed. W&B metadata narrowed two historic generator runs to Vercel / DeepSeek
V4 Flash but did not bind either run to the 212-row artifact hash, so those rows
remain unresolved. The W&B launcher still rejects the draft before upload.

## 2026-10-18 remediation updates

Three metadata-only audits now sit beside this handoff:
[source rights/privacy](source-rights-privacy-audit-2026-10-18.md),
[provider terms](provider-terms-audit-2026-10-18.md), including the Vercel / DeepSeek
historical route, and the [generation provenance follow-up](execution-2026-10-17/g03-historical-run-provenance-followup.md).
The [clearance decision packet](execution-2026-10-17/clearance-decision-packet-2026-10-18.md)
turns their findings into source-owner, privacy, training-owner, and curator
review records. No source rows are approved: 0/190,139 have exact signed rights
and privacy/consent clearance bound to row references. Vercel's current AI
Product Terms prohibit sending sensitive personal data, including health
information; the historical run's exact routing, controls, accepted terms, and
input privacy status remain unverified. The 522-row synthetic
branch remains the smallest useful experiment candidate but still lacks exact
run-to-output binding, output/seed rights and provider terms. Keep
`upload_gate=false` until those transfer gates are resolved. Row-by-row human
review is reserved for clinical/production claims; it does not block research
comparisons. The clearance packet now includes a repository-verified
current roles: Vivi is the project experiment/training owner and sole clinical reviewer for
now; Chad (interim) is the HIPAA Privacy Officer and HIPAA Security Officer. The Release 0
dataset issue template labels `datasets`, `ai`, and `compliance`, and `.github/CODEOWNERS`
routes review to `@daggerstuff`. No authorized source-rights/legal reviewer or dataset curator is
named. The packet proposes sponsoring that issue and requesting any additional reviewers; no
issue was created or anyone contacted. Current role assignments do not constitute approval of
this candidate, and prior dataset-specific pilot approvals do not extend to it.

AWS CLI's invalid `nov` region came from instance metadata. The default profile
now explicitly uses the verified `us-east-1`, and the installed `asm-exec`
wrapper is available on `PATH`; a post-fix read-only STS identity check passed.
No AWS secret values were read.

## 2026-10-18 provider-plan correction (historical; pricing note superseded)

The detailed cross-provider comparison and OVHcloud portable-finish plan is in §9 of the [experiment plan](free-training-experiment-plan-2026-10-17.md). The
W&B training API was rechecked read-only: `/system-check` is healthy and `/preview/base-models` returns 13 trainable models, including `Qwen/Qwen3.6-35B-A3B`.
This confirms API access. At the time, W&B's training-specific pricing page and Serverless Training docs were read as saying adapter training was free during public preview;
inference and storage remained billable. On 2026-10-20, the current CoreWeave Serverless Training documentation was rechecked and explicitly states that SFT is still in public preview and adapter training is free during preview. The current Forge post-training pricing page lists SFT/RL at $2.70/GPU-hour, so those published pages conflict. Current W&B account billing for this job is not yet verified. W&B serverless training artifacts are exportable LoRAs and trained models
are hosted for inference; custom LoRA serving is also documented. Adaption has a separate credit-funded, downloadable checkpoint lane; its remaining balance
is visible in the account dashboard, not its API. OVHcloud AI Training and AI Deploy are the portable, custom-recipe/model-serving route, with paid GPU and
storage charges. No account/resource was created in these checks.

### W&B preview status recheck — 2026-10-20

The Serverless Training docs explicitly label the product public preview and
say adapter training is free during preview. The pricing page currently
redirects to CoreWeave Forge and lists SFT/RL at $2.70/GPU-hour, plus separate
inference, evaluation, and checkpoint-storage charges; only Model Distillation
is described there as free during private preview. The published pages
conflict. Do not infer the active job's account-specific terms or actual bill
from either page alone. See the 2026-10-20 pricing-conflict entry at the end of
this handoff for the authenticated job-status fields and source links.
The account's live artifact inventory confirms
versions were advancing while the SFT jobs remained `RUNNING`. Rechecked against the
[Serverless Training docs](https://github.com/wandb/docs/blob/main/serverless-training.mdx)
and [W&B Training pricing](https://site.wandb.ai/pricing/training/) on
2026-10-20; search-indexed first-party page text was freshly revalidated after
both canonical URLs redirected when opened directly. The direct
account evidence and timestamped versions are recorded
in [the 21:53 UTC live storage and adapter snapshot](execution-2026-10-19/wandb-live-storage-adapter-refresh-20261019T2153Z.json).

At 21:57 UTC on October 19, a direct query of W&B's `lora` and `train-state`
artifact collections found v1 at v138 / 69,500 batches and v2 at v137 / 69,000
batches. The training job API still returns `RUNNING` for both with null
progress and old `updated_at` values; its separate `/checkpoints` endpoint only
returned step 0 and must not be used as the trained-adapter inventory. v4
remains `PENDING`, with no v4 adapter artifact. The same 21:57 check found the
single exact SFT response hash across all 840 successful outputs from seven
120-case evaluations; the target occurs 12,771 times in each v1/v2 source
payload (about 2.4% of assistant targets). This is a target-attractor
correlation, not causal proof. See the [hash-only target overlap record](execution-2026-10-19/wandb-response-target-attractor-20261019T2158Z.json)
and [latest checkpoint evaluation report](execution-2026-10-19/latest-checkpoint-evals/report.md).
At 22:00 UTC, an additional paired evaluation tested v2 v137 against the W&B
base on the frozen 120-case suite. All 240 calls succeeded; the tuned arm again
had one normalized response, zero tool actions, and 60/240 synthetic assertions
passed. Base had 84 unique normalized responses, 148 simulator tool actions,
and 193/240 assertions passed. Estimated inference usage was $0.111901; actual
billed usage is not exposed. This confirms continued collapse 1,000 batches
after the previous tested v2 checkpoint. v1 v138 is still untested. See the
[paired evaluation report](execution-2026-10-19/latest-checkpoint-evals/report.md).

## 2026-10-18 bounded synthetic diagnostic

The user authorized a process-only `.env` credential exception. A local
W&B-inference diagnostic used synthetic-only cases and the W&B-hosted inference
endpoint with `Qwen/Qwen3.6-35B-A3B`; no clinical or candidate dataset rows were
sent. The initial 1,024-token run used three completions: the support response
reached the output limit, and the research case was stopped locally when the next
tool-trace request exceeded its input cap. A research-only retry raised the cap
 to 2,048 tokens and completed three more calls. Across all six planned
completions, estimated usage was 2,193 prompt and 1,550 completion tokens, for
$0.00248575 at the configured rate. The provider supplied no actual-billing
field; treat this as an estimate. The $0.02 authorization cap is consumed; make
no further inference requests under it. This is diagnostic evidence only, not a
scored model comparison. Results contain generated response text and are
restricted to mode 0600 under mode-0700 directories; do not print response text.

Run records:

- `execution-2026-10-18/results/wandb-synthetic-cap-v1-base-20261018T022350Z/`
  (incomplete: one support completion truncated; research stopped at local cap)
- `execution-2026-10-18/results/wandb-research-base-2048-20261018T022456Z/`
  (research case complete after three calls)

At this 02:55 UTC checkpoint, no uploads, training jobs, or deployments had
started. This historical status is superseded by the live 16:26 UTC checkpoint
above, which records the accepted W&B SFT job.

Resume with:

```text
Continue the authorized training campaign in /home/vivi/pixelated.
Read docs/training/TRAINING_EXECUTION_HANDOFF.md and execution-2026-10-17/registry.json.
G02 source-specific reconciliation is complete. G03 diagnostics are complete:
exact renderer binding is 980/980; the 522-row first-party synthetic edge branch
has 29 exact heldout-group rows excluded, a provisional groupwise split and
metadata-only regex/near-duplicate screens. Recover the exact generation
provider/model receipt and verify applicable output-use/remote-training terms
before provider payload creation. Preserve
current gold and recovery artifacts. The process-only credential exception
permits bounded provider operations, but do not start inference without new
budget authorization, upload the candidate, or claim model export without a
verified local artifact. Update the registry and Foresight as evidence arrives.
```

## 2026-10-18 live read-only execution checkpoint

At 13:23 UTC, authenticated Adaption metadata calls confirmed two visible
datasets: `arc-run2-train-v1` (11,192 rows, succeeded) and `train` (418 rows,
awaiting input). Both historical Qwen/Qwen3.6-35B-A3B runs remain succeeded and
exportable (platform win-rate figures 0.6414 and 0.4971); these figures are
not clinical verdicts and their inputs remain unapproved for reuse. The current
model catalog includes the Qwen anchor, Gemma 4 31B, and Nemotron 3 Nano Omni
30B A3B. No new job had launched as of 13:23 UTC. Adaption still exposes no credit balance or
per-run estimate, so account dashboard verification remains a hard prerequisite.

Local review of the prior W&B synthetic diagnostics found the support response
was truncated before its enum check passed, and the research response omitted
required fictional source IDs. This remains a two-case diagnostic, not a model
comparison. The authorized six-completion / $0.02 inference cap is consumed;
no further requests were made. The existing 5-dev/5-sealed fictional software
capability suite is an evaluation fixture, not a training corpus. No training
ready dataset is currently cleared. Metadata-only details are in
[provider-and-eval-checkpoint.json](execution-2026-10-18/provider-and-eval-checkpoint.json).

Next execution is automated full-corpus validation and closure of provider/provenance
gates, while account-specific W&B entitlement/artifact quota, Adaption credits,
Fireworks offer/inference terms, and OVHcloud account/region cost remain unverified. The 190,139-row
candidate remains isolated, with `upload_gate=false`. This finding applies to
that candidate release and predates the separate 2,093-row W&B release recorded
in the current checkpoint above.

## 2026-10-18 break-away package verification

Rechecked the local 522-row first-party synthetic edge-case package at
`ai/data/curated/recovery/gold-20261017/g03-edge-review-package-20261017T1626Z/`.
The train/validation/test files match their pinned SHA-256 values and row counts
(410/72/40); all are mode 0600 under a mode-0700 directory. Every row follows
the assistant-only loss-weight contract. I recomputed group intersections from
the internal manifest: train/validation, train/test, and validation/test each
have zero shared groups (139/25/15 groups).

The fail-closed W&B launcher dry run was executed against the current manifest
and stopped before upload with `G04 release is not approved; no upload is
allowed`. Its focused tests pass 9/9. The manifest remains
`draft_local_only`, `upload_gate=false`, `release_id=null`. The exact blocking
evidence is now isolated: (1) generation provider/model receipt is not bound
to the source seed hashes, (2) generation output-use terms are unverified,
(3) destination provider privacy/retention/transfer approval is pending,
(4) golden-control lineage is unknown. This is a package-ready local break-away candidate, not a
training-cleared artifact. The 190,139-row candidate was untouched. Row-by-row
review is not a prerequisite for bounded research experimentation.

## 2026-10-18 efficient research-experiment path

The 24-example pilot and 522-row line-by-line queue were low-value process
artifacts. They add no evidence beyond the existing 522-row package's payload,
hash, split, and focused launcher checks, so they have been removed from the
active plan. Do not create another tiny pilot.

For the 522-row candidate, run one automated gate over all rows: pinned file
hashes, JSON/schema and assistant-only loss weights, group-disjoint splits,
heldout exclusion, exact dedup/near-duplicate checks, and identifier-pattern
screen. Preserve the 40-row test split untouched. This is a fast local check and
produces a machine-readable report. A small risk-stratified sample is optional
for diagnostic spot checking; it is not a gate for a research-only run and does
not certify clinical safety.

The actual blockers are (1) generation provider/model receipt is not bound to
source seed hashes, (2) generation output-use terms are unverified, (3) the
selected destination provider's privacy/retention/transfer approval is pending,
and (4) golden-control lineage is unknown. These are evidence and provider
authorization questions; reviewing 522 conversations line by line would not
resolve them. Human clinical review is required before clinical or production
claims/use, not before a bounded non-production research comparison on synthetic
data.

Next, recover or regenerate with a contemporaneous provider/model receipt
attached to seed hashes; verify that provider's output-use terms; verify W&B's
training data handling, retention, and export terms; and resolve golden-control
lineage or exclude those controls. Once those pass, run the full 522-row SFT
comparison with a fixed baseline and heldout evaluation. Fireworks can be a
separate ephemeral comparison; its weights are not a deliverable. No model is
promoted to clinical use from these research experiments alone.

## 2026-10-18 full W&B matrix generated and SFT launch attempted

The low-value 24-row pilot and 522-row manual-review queue are deleted. I
replaced them with the generator's complete 120-scenario matrix: all 10 families
x 3 difficulty levels x 4 ambiguity patterns, generated through W&B Qwen
Qwen3.6-35B-A3B and checkpointed locally. Two W&B inference invocations
completed the matrix (runs `t2df59al` and `s95vdvlv`; 60 rows each). The raw
source SHA-256 is
`2f9617b9e71799c8738100a73161d5d94a8333079a05f82790f39a5737fd2c8c`. The
credential-free receipt is
[generation_receipt.json](../../../ai/data/curated/recovery/wandb-qwen36-edge-matrix-20261018/generation_receipt.json).
Provider token usage was not captured by the generator, so billed inference
usage remains unknown.

The generated source passed its automatic cliché gate with 120 written, zero
rejected, zero dropped. The package has 80 train, 20 validation, and 20 test
rows, with 120 distinct scenario groups and zero group overlap. All six basic
email/SSN/phone/card/URL/IP patterns returned zero hits. The payload drops the
unmatched final user turn from each 15-message source transcript, preserving
seven complete user/assistant pairs and assistant-only loss weighting. The
W&B SFT launcher dry-run passed and prepared an 80-row artifact.

The initial training launch exposed a launcher transport bug: `urllib` requests
were blocked by W&B's browser-signature filter, while `aiohttp` read-only checks
returned healthy and listed 13 trainable bases including this Qwen model. The
launcher now uses `aiohttp` and accepts W&B's JSON-list model catalog. The
corrected run verified the project was private, uploaded the training artifact
`wandb-artifact:///wutang/pixelated-empathy-kan28/g04-wandb-qwen36-edge-matrix-20261018-v1-baseline-7f31c66054dc:v0`,
and created model resource `4c9e5d0d-abd9-4bf8-94cf-95bc249b37e9`. The SFT job
creation request returned HTTP 400 without a job ID. Local state is deliberately
`job_creation_submitted_unknown`; do not resubmit until W&B confirms whether the
request was rejected or created. Read-only model checkpoint lookup currently
shows only step 0. No training completion is claimed. The uploaded artifact is
synthetic-only and W&B-private. The original 522-row candidate remains
untouched. This cohort is authorized only for same-provider W&B research SFT,
not clinical or production use.

## 2026-10-18 W&B SFT job created and 190k clearance work order

The 80-row synthetic matrix now has a real W&B Serverless SFT job:
`8b4f4722-9849-4942-a9e6-00829b1cd9c9`. W&B returned HTTP 200, and the
immediate status read returned `RUNNING` (created 2026-10-18 15:30:58 UTC).
The model resource is `4c9e5d0d-abd9-4bf8-94cf-95bc249b37e9`. The initial
artifact failed because Serverless SFT expects `total_len` in the artifact's
`metadata.json`; the corrected artifact includes `total_len: 80` and the job
was accepted. The launcher now writes that field in future metadata. Track the
job with `wandb-sft-state/wandb-sft-7f31c66054dc78829cbe5f50fb8f7fb96f80c7b9cd490d170802da19a49e0742.json`.
This is synthetic research data and this run does not clear the 190,139-row
recovery candidate.

### Exact work required to clear the 190,139-row candidate

The blocker is evidence coverage, not a need to read 190,139 conversations.
The candidate hash is `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`;
the machine-generated row-reference ledger already binds all 190,139 rows
across 475 source labels (836 grouped records). Current exact joins map
177,423 rows to 16 proposed source IDs; 12,716 rows under 459 labels remain
unmapped. Zero rows have signed source rights and privacy/consent evidence
bound to their row references.

Do this as a batch source/version process, then let the curator's join script
apply each decision to matching row references. No one needs to inspect rows
one by one:

1. **Quarantine by default:** set the unresolved candidate's training
   eligibility to excluded. Keep the original file immutable. Do not upload it
   to a trainer or inference endpoint while these records are absent.
2. **Resolve the 459 unmapped labels (12,716 rows):** curator supplies one
   crosswalk row per distinct label to immutable upstream source/version,
   acquisition path, and candidate row-reference set; group labels that resolve
   to the same exact source/version. Unknown or ambiguous labels stay excluded.
   The audit has already grouped these counts: 8,107 book/title, 980 ARC
   corpus, 415 creator/persona, 100 clinical edge-case, 77 predefined
   nightmare, and 3,037 other labels.
3. **Decide by source/version, not example:** rights reviewer records the
   primary license or signed permission and its scope (model training, intended
   research/commercial purpose, and named remote provider). Reddit-derived
   sources SRC-027/028/030/031 total **151,279 rows** and need applicable
   rightsholder permission for AI training; absent that, exclude those groups.
   ESConv (892 rows) and DAIC-WOZ (129) need written permission/agreements for
   this purpose and provider transfer. AnnoMI (98) needs its conflicting local
   records resolved and primary permission. For each other mapped source,
   approve or exclude using its own exact version and terms; do not infer from a
   family label.
4. **One privacy decision per source/version and destination:** privacy owner
   records the authorization/consent basis, sensitive-data and
   re-identification assessment, required redaction/exclusion rule, and remote
   processing/retention/deletion conditions. Bind it to the candidate hash and
   source row-reference set. If consent/authority or vendor transfer is
   unknown, exclude that source group.
5. **Provider-specific release build:** training owner records the W&B
   account/product and effective privacy/retention/export settings (repeat for
   Fireworks or Adaption if used). The curator's deterministic build includes
   only approved source/version groups, applies explicit row exclusions,
   writes a new immutable rowref ledger, and reports included/excluded counts
   and hashes. Run schema, deduplication, split-leakage, sensitive-identifier,
   and loss-mask checks automatically over the full output. Human clinical
   review is needed only for clinical/production claims, not to decide every
   row's source rights.

**What is needed from people:** (a) an authorized source-rights/legal approver
and primary permissions for the source groups above, (b) Chad's exact-candidate
privacy/consent and provider-transfer decision, and (c) a curator to produce
 the 459-label crosswalk and run the automated decision-to-row join. For any
source group that cannot produce the evidence, the action is simply exclude it;
the rest can move forward as a smaller, accurately counted release. The
metadata-only audit and source counts are in
[`source-rights-privacy-audit-2026-10-18.md`](source-rights-privacy-audit-2026-10-18.md)
and the evidence/signoff schema is in
[`clearance-decision-packet-2026-10-18.md`](execution-2026-10-17/clearance-decision-packet-2026-10-18.md).

### Operational intake: who gets asked and what comes back

A 475-label queue is now materialized at
[`190k-source-clearance-worklist.csv`](execution-2026-10-17/190k-source-clearance-worklist.csv).
The source-specific contact routes, exact permissions to request, and first-pass
exclusion procedure are in the
[`190k-clearance-runbook.md`](execution-2026-10-17/190k-clearance-runbook.md).
It contains source-label counts, matched source IDs/titles where known, a default
exclude disposition, and the exact curator action for that bucket. It was built
from metadata only; no conversation text was read. It reconciles to exactly
190,139 rows: 177,423 matched and 12,716 unmatched.

For the fastest defensible first cut, bulk-exclude 163,995 rows now: all 12,716
unmatched rows and the 151,279 Reddit-derived rows. The Reddit data cannot be
made usable by our own signoff: the permission has to come from the applicable
content rightsholders. Keep those rows excluded unless that permission is
actually delivered. Then work the remaining 26,144 mapped rows as 12 source
batches (SRC-032/033/034/036/039/040/041/044/046/047/050/051). For each
batch, the curator gets the exact upstream version and its source-owner contact
from the named repository or original dataset record; the rights approver
obtains the governing license or written permission from that rightsholder; and
Chad records the privacy decision. If any of those cannot be obtained, mark
that batch excluded and the remaining batches can still proceed independently.

Use this permission request with each rightsholder (replace bracketed fields;
attach the source/version and row-count sheet, never patient examples):

> We are requesting written permission to use [dataset/source and exact
> version] for supervised fine-tuning and evaluation of Pixelated Empathy
> models, including internal research and intended commercial deployment. Data
> would be processed by [W&B Serverless Training account/product] and, if
> separately approved, [Fireworks / Adaption / OVHcloud]; artifacts/adapters
> would be retained in our private account and may be exported to our own
> infrastructure. Please confirm that you control the relevant rights and
> authorize this use and those named processors, or state the narrower allowed
> purposes, providers, retention period, attribution, deletion, and downstream
> restrictions. Please identify any records or contributors excluded from that
> grant. We will bind your response to source version [version/hash] and our
> candidate row-reference ledger [hash/count].

Record the reply or license URL plus a locally stored evidence-file SHA-256 in
that CSV's `rights_evidence_ref`; record the rights decision as `APPROVE` only
for explicitly covered scope. Ask Chad to fill `privacy_decision` and
`privacy_evidence_ref` with the approved purpose/legal basis, consent or other
authorization basis, sensitivity/re-identification assessment, exclusions,
named processors, retention/deletion conditions, decision date, and artifact
hash. These are real evidence references, not a checkbox we can self-approve.

Application is mechanical: curator resolves each label to one exact source and
version; copies the same signed decision reference across labels that are
provably that same version; marks every other row `EXCLUDE`; then joins the
approved labels against `source-decision-ledger.jsonl` by `source_label` and
emits only those candidate row numbers/hashes into a new manifest. Rebuild the
JSONL from those row numbers, hash it, run the automated checks, and require the
new manifest to assert that every included row has both approved evidence refs
and the named provider scope. Never modify the recovered candidate in place.

### Full-corpus W&B experiment (2026-10-18)

The recovered 190,139-row candidate was used for a W&B research experiment; this
is an experiment, not a production or deployment approval gate. The immutable
source candidate was preserved. Automated structural preparation produced
190,087 trainable rows (171,121 train / 9,664 validation / 9,302 test); 52 rows
were omitted only because they lacked an assistant target or a user turn before
the target. The release manifest records all 475 source labels, exact row
references, split membership, and hashes:
[`wandb-full-corpus-release.json`](execution-2026-10-18/wandb-full-corpus-release.json).
The build applied automated identifier-pattern redactions and zero-hit scans;
those scans are not comprehensive de-identification, so treat the resulting job
as a controlled research experiment, not as permission to deploy or redistribute
its outputs.

W&B accepted full-corpus training job
`2087f223-a48f-45f7-9999-daece5743bba` for Qwen/Qwen3.6-35B-A3B. At the latest
poll it remained `RUNNING`, with only step 0 listed. Its status and
model ID are in
[`wandb-sft-8ce8354c67ef10915f78ebd385950aaed8fcac505578645dba907d330befbe91.json`](execution-2026-10-18/wandb-full-corpus-state/wandb-sft-8ce8354c67ef10915f78ebd385950aaed8fcac505578645dba907d330befbe91.json).
Continue polling that job, record checkpoint IDs, and run the same paired cases
against the resulting checkpoint when available.

The W&B inference transport was repaired and a five-case synthetic paired run
against the earlier SFT checkpoint completed: 10/10 endpoint calls succeeded at
an estimated $0.0041 under the $0.05 cap. This is a smoke comparison only, with
unvalidated synthetic diagnostics; the earlier 1,024-token attempt hit the
preflight context ceiling on tool-heavy cases. The completed bounded run uses a
2,048-token context ceiling and 512-token output cap. Results are in
[`wandb-policy-full-2048-512-aiohttp`](execution-2026-10-18/results/wandb-policy-full-2048-512-aiohttp/).
It does not evaluate the newly submitted full-corpus checkpoint. Re-run after
that checkpoint becomes available and broaden scenario coverage before drawing
quality conclusions.

### Corrected full-corpus release and retraining (2026-10-18)

The 52 structural omissions have now been repaired in a versioned overlay; the
recovered candidate itself was not edited. Fifty Psy-Insight counselor/client
excerpts were matched against a pinned processed source mirror and received a
generated next counselor turn. The mirror contains only these two-turn records;
no longer session history was available. The generated turn is new model text,
not recovered source material. The remaining two malformed `Get More.....` book rows were
rewritten as source-quality triage examples that explicitly reject inventing
clinical content. Generated continuations are marked as not human or clinically
reviewed. Repair row numbers, candidate row hashes, source dialogue IDs,
similarity scores, generation parameters, and response usage are recorded in
[`repair_manifest.json`](../../../ai/data/curated/recovery/gold-20261017/wandb-full-corpus-repairs-20261018/repair_manifest.json)
and [`row_repairs.jsonl`](../../../ai/data/curated/recovery/gold-20261017/wandb-full-corpus-repairs-20261018/row_repairs.jsonl).
The upstream dialogues were fetched from the pinned Psy-Insight mirror revision
`dd6f2e582377ddb71e976ec8f45ad48b5c5fc57a`; upstream files and hashes are in
the repair manifest.

Rebuilt release
[`wandb-full-corpus-release-v2.json`](execution-2026-10-18/wandb-full-corpus-release-v2.json)
retains all **190,139 rows**, with **zero structural drops**, 171,167 train,
9,666 validation, and 9,306 test rows. Its payload hash is
`138045ba6fb263e0d68bb42c3e8d0a7e3bf7314c3fc79397ecfd805a2c980a76`.
The first 190,087-row job remains a separate in-flight experiment and cannot be
mutated to include the repairs.

The corrected full-corpus job is
`f914f0fb-f892-4e1a-8291-8cea3757274e`, model ID
`339688ad-b611-439f-afba-a8405efae633`. The dataset-size difference is fully
accounted for: v1 retained 190,087 rows after dropping the 52 structurally
untrainable rows; v2 repairs and retains all 190,139. The source-group split
places those 52 repaired rows as 46 train, 2 validation, and 4 test, explaining
why the training split grew by 46 rows (171,121 to 171,167) rather than 52.
The v2 job state is in
[`wandb-sft-556695bfd5c4dcd55a12d698290840432a5e0c193d5a3180aef274e2ed8e1790.json`](execution-2026-10-18/wandb-full-corpus-v2-state/wandb-sft-556695bfd5c4dcd55a12d698290840432a5e0c193d5a3180aef274e2ed8e1790.json).
Both jobs are still running. Intermediate paired evaluations against the base
model are recorded below; the final-checkpoint evaluation will run when each job
reaches a terminal state. The comparison configs in
[`inference-configs`](execution-2026-10-18/inference-configs/) cap the
preflight worst-case spend below $0.05 per run; results remain synthetic and
diagnostic only.

### 2026-10-19 W&B checkpoint inventory correction

The earlier checkpoint diagnosis was too narrow. The Serverless Training
model-checkpoint endpoint lists only the base `lora` artifact at step 0 and
does not include the jobs' internal resume checkpoints. A read-only inventory
of the project's W&B artifact collections found separate `lora` collections
named `arc-sft-baseline-8ce8354c67ef-sft-resume` and
`arc-sft-baseline-556695bfd5c4-sft-resume`. Their latest retained artifacts at
13:40 UTC were respectively `v86` and `v84`, marked
`sft_internal_checkpoint: true`, with 43,500 and 42,500 completed batches.
Each contains `adapter_config.json` and a 117,842,120-byte
`adapter_model.safetensors`; recent versions were created roughly every ten
minutes. This matches the user's observation that W&B was creating checkpoints
while storage was being cleared. The jobs are saving intermediate resume
artifacts; the earlier step-alias `step500` inference probe and model checkpoint
listing were not valid evidence that checkpoint saving had failed.

The latest paginated event audit at 13:46 UTC found the jobs still advancing:
v1 at gradient step 43,808 of 85,561 and v2 at 42,847 of 85,584. The
checkpoint API alias inventory and internal resume artifact inventory describe
different artifact surfaces. Keep watching the internal `*-sft-resume` artifact
collections for new versions, and use the documented model-checkpoint endpoint
or actual model URI only when selecting an inference-ready checkpoint. Do not
delete current or historical resume artifacts until the desired recovery point
and inference checkpoint are confirmed. See the [checkpoint API](https://docs.wandb.ai/api-reference/models/list-model-checkpoints)
and [Serverless Training overview](https://github.com/wandb/docs/blob/main/serverless-training.mdx).

The versioned resume-artifact URI is accepted directly by W&B's training
inference endpoint. A one-case v2 probe against `...-sft-resume:v84` succeeded
with usage metadata. Five-case paired evaluations then completed against the
base model for v1 `v86` (43,500 batches) and v2 `v84` (42,500 batches), with
10/10 successful calls in each run. The response traces show a severe interim
quality regression: each trained arm returned the same short taxonomy-style
training-corpus completion for all five unrelated scenarios, with no tool
calls. All five cases had at least one failed deterministic outcome check; 2 of
7 secondary checks passed (state unchanged and injection-text omission), which
does not offset the missing task response. The exact v1 completion occurs in
4,378 training rows and the v2 completion in 6,301 rows. This points to a
response-prior/mode-collapse problem on these agent scenarios; it does not by
itself establish the final model result because both checkpoints were taken
mid-training. The base arm produced valid responses for three cases and hit
the 512-token limit on two. Machine-readable counts are in
[`wandb-full-corpus-midrun-assessment.json`](execution-2026-10-18/results/wandb-full-corpus-midrun-assessment.json);
the complete results and manifests are in
[`wandb-full-corpus-v1-step43500-paired`](execution-2026-10-18/results/wandb-full-corpus-v1-step43500-paired/)
and
[`wandb-full-corpus-v2-step42500-paired`](execution-2026-10-18/results/wandb-full-corpus-v2-step42500-paired/).
Estimated inference spend was $0.003493 and $0.00337175 respectively; W&B did
not return actual billed amounts, so credit consumption remains unverified.

At 13:49 UTC the authenticated API still reported both jobs `RUNNING`; the
latest internal artifacts were v1 `v87` at 44,000 completed batches and v2
`v85` at 43,000. The new
[`watch_wandb_full_corpus_final.py`](../../ai/training/watch_wandb_full_corpus_final.py)
monitor polls job and resume-artifact state every five minutes and runs the
same bounded five-case paired evaluation against the last retained artifact
when each job becomes terminal. The monitor is running as local session 79817.
Do not stop either remote job or delete its newest resume
artifact while it is active.

### W&B artifact storage triage

A read-only inventory of 283 visible artifact collections returned about 19.74
GB summed across artifact-version sizes; this is a logical sum, not a confirmed
quota-reclamation estimate because file blobs may be deduplicated. The largest
active collections are each full-corpus job's `train-state-sft-resume`: six
visible versions at 1,060,414,709 bytes apiece (about 6.36 GB logical size per
job). Each current train-state contains a roughly 707 MB optimizer-state file,
the initial 235.6 MB adapter, and the current 117.8 MB adapter. The companion
`lora` resume collection contains the inference adapter separately at 117.8 MB
per version.

The strongest cleanup candidates are the four **completed-run** train-state
artifacts below. Their logged W&B runs are `finished`, `used_by()` reports no
dependent runs, and each final inference LoRA remains in a separate `lora`
collection. Deleting these train-state artifacts would remove optimizer/resume
state for those completed jobs while preserving the separately stored LoRA
artifacts and datasets, provided those jobs do not need to be resumed:

- `arc-sft-baseline-f00e0bf27bf3-train-state:v0` — 1,060,414,697 bytes
- `arc-sft-baseline-7f31c66054dc-train-state:v0` — 1,060,414,691 bytes
- `arc-corpus-qwen36-sft-20261011-train-state:v0` — 1,060,414,703 bytes
- `pixelated-arc-gemma4-sft-20261011-train-state:v0` — 565,725,323 bytes

Together these are about 3.75 GB logical size (about 3.49 GiB); actual freed
quota may be lower if blobs are shared. Preserve both active jobs' latest
train-state artifacts and the `lora` checkpoints used by the mid-run
comparisons. Older unaliased train-state versions from the active jobs are
recovery points, not serving models; consider them only after the newest
checkpoint has been validated and at least one prior recovery point is retained.
No artifacts were deleted during this inventory.

#### 2026-10-19 14:04 UTC live inventory after user storage cleanup

The user reported seeing new checkpoints while deleting artifacts, so I
rechecked the live W&B collections rather than relying on the earlier
inventory. Both jobs are still writing checkpoints: v1 has `lora` and
`train-state` resume versions `v82`–`v88` (41,500–44,500 completed batches),
and v2 has versions `v80`–`v86` (40,500–43,500 batches). The newest versions
were created at 13:59:10 and 13:58:48 UTC respectively. Each collection now
contains seven versions, so older versions are no longer visible in the
collection; version numbering has gaps before the retained range. This is
consistent with older artifacts having been deleted during cleanup, but the
current collection listing cannot establish which specific artifacts were
deleted or attribute individual deletions. The jobs continue successfully and
their newest paired LoRA and train-state versions are present. Keep the newest
pair and at least one previous recovery point for each active job; deleting
older versions while training continues may reduce rollback options and may
not reclaim equivalent physical storage because artifact files can be shared.

The next live poll at 14:09 UTC confirmed checkpointing resumed: v1 published
LoRA and train-state `v89` at 45,000 batches (14:08:46–14:08:48 UTC), and v2
published `v87` at 44,000 batches (14:08:09–14:08:11 UTC). Both jobs remain
`RUNNING`; the job API's `progress` value is null, but run heartbeats and paired
resume artifacts advanced. Based on the last two observed 500-batch intervals
(about 9.5 minutes each), the rough remaining runtime to 85.6K batches is
about 13 hours from 14:09 UTC, around 03:10 UTC on October 20. This extrapolates
recent checkpoint cadence and is not a provider ETA.

The 14:18 UTC follow-up shows continued checkpointing: v1 `v90` at 45,500
batches (created 14:18:22 UTC), v2 `v88` at 44,500 batches (14:17:26 UTC), and
both jobs still `RUNNING`. Their latest run heartbeats were 14:18:28 and
14:17:32 UTC respectively. Each active collection now retains nine versions.

#### 2026-10-19 14:22 UTC artifact storage re-inventory

Enumerating all artifact types and versions in the project returned 283
collections and **26.813 GB summed logical version size**. This is not the
account quota meter or confirmed physical reclamation; deduplicated blobs may
make actual storage usage smaller. The active jobs account for about 21.21 GB
of that logical sum: 18 train-state versions at 1,060,414,709 bytes each
(19.09 GB total) plus 18 LoRA versions at 117,843,308 bytes each (2.12 GB).
The collections were still growing as the jobs ran.

Read-only dependency checks found no W&B run dependencies for 26 unaliased
older active-job versions suitable for cleanup while retaining two latest
recovery points and both already-evaluated midrun LoRAs. The exact candidates
are train-state v1 `v82`–`v88`, train-state v2 `v80`–`v86`, LoRA v1 `v82`–`v85`,
`v87`–`v88`, and LoRA v2 `v80`–`v83`, `v85`–`v86`. Their combined logical size
is 16,259,925,622 bytes (about 15.14 GiB). Preserve v1 train-state `v89`/`v90`
and v2 `v87`/`v88` as two recovery points per job; preserve the already-tested
v1 LoRA `v86` and v2 LoRA `v84` for reproducible midrun comparisons, as well as
the newest LoRA versions and aliases. The active latest LoRAs are v1 `v90` and
v2 `v88`. This is a deletion candidate list only; no artifacts were removed by
this inventory. W&B's logical sizes and zero `used_by()` dependencies do not
guarantee the same amount of quota will be freed or prove there are no provider
internal references, so deletion should be limited to these unaliased historical
versions while the two newest train-state checkpoints and tested LoRAs remain.

#### 2026-10-19 14:28 UTC live checkpoint refresh

The live watcher was confirmed running (PID 433649) and its fresh poll at
14:28:10 UTC reports v1 `RUNNING` at resume LoRA `v91` / 46,000 batches
(artifact created 14:27:54 UTC), and v2 `RUNNING` at `v89` / 45,000 batches
(created 14:26:50 UTC). This confirms new checkpoints continued to appear while
the user was freeing storage. Therefore, the 14:22 cleanup candidate list is a
historical snapshot, not a current deletion instruction; re-enumerate exact
collection/version identities immediately before any cleanup. Do not infer
that a version number shown in an older list is still present or that newly
created versions are safe to delete. No deletion was performed by this refresh.

#### 2026-10-19 source-lineage verification refresh

Recomputed the candidate and ledger binding from the current worktree. The
candidate contains 190,139 rows and its file SHA-256 matches the pinned
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`. All
190,139 row references matched both the exact raw-row SHA-256 and canonical
messages SHA-256; candidate source labels also matched their ledger labels.
The 475 grouped worklist labels reconcile exactly to ledger row-reference
counts and sum to 190,139. There were zero duplicate/missing row references or
hash/label mismatches. This verifies lineage and automated source-group
binding; it does not convert proposed rights/privacy decisions into approvals.

#### 2026-10-19 14:34 UTC fresh W&B artifact inventory

A new read-only project-wide inventory supersedes the 14:22 logical-size
snapshot: 8 artifact types, 283 collections, 315 visible versions, and
29,169,899,136 bytes summed logical version size (about 27.16 GiB). This is
not the account's physical quota meter. Active-job collections now visibly
contain v1 LoRA/train-state versions `v82`–`v91` and v2 versions `v80`–`v89`.
Latest versions are v1 `v91` and v2 `v89`, both aliased `latest`; both jobs
were still RUNNING at 14:33:11 UTC. Each active train-state is 1,060,414,709
bytes and each LoRA is 117,843,308 bytes. The four active collections sum to
23,565,160,340 logical bytes (about 21.95 GiB).

Current visible unaliased cleanup candidates, if the operator chooses to prune
old resume snapshots while keeping two newest recovery points per job and
retaining the tested LoRAs (v1 `v86`, v2 `v84`), are: train-state v1 `v82`–`v89`,
train-state v2 `v80`–`v87`, LoRA v1 `v82`–`v85` and `v87`–`v89`, LoRA v2
`v80`–`v83` and `v85`–`v87`. These 30 versions sum to 18,616,441,656 logical
bytes (about 17.34 GiB). All had no aliases and `used_by()` returned zero in
the inventory. They remain candidates, not a guarantee of physical quota
reclamation or absence of internal provider references. Do not delete latest
aliases, the two recovery points, or tested LoRAs. The inventory cannot recover
the user's deletion history; it only identifies objects visible now.

#### 2026-10-19 14:39 UTC active checkpoint refresh

The four active collections were re-enumerated after another checkpoint
cycle. v1 now has LoRA and train-state `v92` at 46,500 batches; v2 has both at
`v90` at 45,500 batches. The 14:34 cleanup candidate version ranges are
superseded. With the same retention rule (two newest recovery versions per
collection, plus tested LoRAs v1 `v86` and v2 `v84`), the currently visible
candidate set is 34 unaliased versions: train-state v1 `v82`–`v90`, train-state
v2 `v80`–`v88`, LoRA v1 `v82`–`v85` and `v87`–`v90`, LoRA v2 `v80`–`v83` and
`v85`–`v88`. `used_by()` returned zero for these versions. Their summed logical
size is 20,972,957,690 bytes (about 19.53 GiB). See
[`active-checkpoint-inventory-2026-10-19T1439Z.json`](execution-2026-10-18/live-monitor/active-checkpoint-inventory-2026-10-19T1439Z.json).
This is still only a point-in-time deletion candidate list; it does not verify
physical quota release or W&B-internal references, and no deletion was made.

#### 2026-10-19 14:40 UTC W&B project storage metric

An authenticated W&B GraphQL query for `Project.storageBytes` returned
26,396,506,333 bytes (26.397 GB / 24.584 GiB) for the private project at
14:40:56 UTC. The response contains no account-plan limit or rolling-30-day
billable usage. The adjacent `POST /files/query_stats` endpoint is a Weave
file-statistics API and returned only 1,067 bytes; it is not the Model Artifact
storage figure and must not be used for this question. The [W&B pricing page](https://site.wandb.ai/pricing/)
says storage includes artifacts and run data and is calculated over the
preceding 30 days. The GraphQL value is now a direct project-level usage
reading, but it does not establish remaining plan headroom. Machine-readable
response: [`project-storage-usage-2026-10-19T1440Z.json`](execution-2026-10-18/live-monitor/project-storage-usage-2026-10-19T1440Z.json).

### Synthetic agent-tool SFT package, 2026-10-19

Prepared an additional first-party, deterministic synthetic dataset at
`agent-tool-sft-2026-10-19/` for the tool-use gap seen in the full-corpus
midrun evaluations. It has 1,200 examples across eight behavior families,
split by family into 960 train, 120 validation, and 120 test examples, with
1,500 assistant tool-call messages overall. All records and scenarios are
fictional; no clinical or external content is included. Development and sealed
scenario prompt text is checked for exact overlap before release generation.

The W&B payload lines contain only the documented `messages` and `tools`
fields. Separate per-split `rowrefs.jsonl` files bind each payload line's hash
to its deterministic example ID, family, and split index. The release manifest
and all file hashes were independently checked after generation; schema and
row-reference checks passed for all 1,200 rows. Ruff and Python compilation
also pass for `ai/training/build_agent_tool_sft.py`. Its release status remains
`local_synthetic_research_candidate_not_uploaded`: storage and bounded credit
coverage must be rechecked before upload or a new paid inference evaluation.
This is a focused tool-use experiment set, not a replacement for or clearance
of the full clinical-domain candidate. The saved generator is
`ai/training/build_agent_tool_sft.py`.

The 120-row held-out test split is also compiled into
`evaluation/heldout-test-cases.jsonl` (15 cases per family) for the existing
paired evaluator. Its generated fixtures were exercised against the target
tool trajectories: all 120 examples passed their deterministic state checks.
The paired-evaluator input validator accepts all 120 cases, and the focused
offline evaluator suite passes 22/22 tests, including explicit-consent gates
for memory writes and fictional appointment booking. This establishes a
reproducible evaluation path; it is not a model score or a data-upload gate.

The 120-case W&B base-model evaluation is now complete. The initial run used a
two-tool-round cap and completed 110 cases; its 10 resource-comparison cases
that hit the cap were rerun successfully with three rounds. Combined, the two
run manifests cover all 120 cases with no unresolved API errors. The base model
passed all deterministic checks in 77/120 cases and passed 189/240 individual
checks. It passed both no-consent families 15/15, but passed every check in
only 1/15 explicit appointment-consent cases, 6/15 memory-write cases, 6/15
approval-gate cases, and 7/15 resource-lookup cases. It passed 14/15 resource
comparisons and 13/15 untrusted-note cases. This defines baseline behavior for
this synthetic suite only; checks are not clinical-quality or safety
certification. W&B usage-based cost estimate is $0.09516425 against a combined
worst-case cap of $0.4608; actual billing was not returned. Raw traces,
per-run manifests, configuration hashes, and aggregate results are under
`agent-tool-sft-2026-10-19/evaluation/`; see
[`baseline-summary.json`](agent-tool-sft-2026-10-19/evaluation/baseline-summary.json)
and [`experiment-manifest.json`](agent-tool-sft-2026-10-19/evaluation/experiment-manifest.json).
The trained-model arm remains pending until the local package can be uploaded
and a new W&B training job can be justified against current artifact storage.
Readiness review found two concrete launch issues to resolve first: the
existing `wandb_sft_g04.py` path correctly rejects this release because its
manifest is a local synthetic candidate rather than a G04-approved release,
and its hardcoded learning rate (`1e-4`) conflicts with the package metadata
(`1e-5`). Do not relabel the manifest as approved or use that launcher as-is;
prepare a dedicated synthetic-candidate path that validates its hashes/splits
and takes the learning rate from an explicit experiment config. The payload's
tool-call format is supported by the [ART SFT data contract](https://art.openpipe.ai/fundamentals/sft-training),
which W&B links from its Serverless SFT docs: assistant `tool_calls`, `tool`
messages, and a `tools` array are valid. The narrower role check is specific to
the G04 launcher, not a W&B format limitation. Current
verification: `ruff check` passes and the paired-evaluator plus G04-launcher
tests pass 32/32 when invoked from the repository root.

The v2 release manifest was independently rechecked against disk: the recovered
candidate, 52-row repair overlay, train/validation/test partitions, 190,139-row
row-reference ledger, and empty held-out exclusion file all match their recorded
SHA-256 hashes and row counts. This verifies artifact integrity and row-count
lineage; it does not resolve the source-rights gaps recorded in the source audit.

### Adaption run-2 result recheck

The authenticated Adaption inventory confirms run
`8da8f685-7ef6-43c0-958e-ab34dbdcd520` succeeded on Qwen/Qwen3.6-35B-A3B,
reports `download_available: true`, and reached a platform win rate of 0.6414.
Its 11,192 training sequences came from the separate 936-row ARC run-2 snapshot
(679 train, 129 validation, 128 test ARC rows), not from the 190,139-row full
candidate. The exported adapter is already present at
`ai/training/output/arc_corpus/export/adaption_run2_v1/checkpoint_run2/`.

The independent 52-case local evaluation does not support a quality-win claim:
the Kimi K3 judge scored run 2 at 0.704 overall versus 0.7562 for base, a
-0.0522 difference, with 22 wins, 5 ties, and 25 losses. The earlier preflight
comparison also favored base on empathy, safety, and reflection. Treat the
platform win rate as an internal training metric only; do not select this adapter
as the campaign winner without a larger, pre-registered paired evaluation. The
summary and per-case outputs are in
`ai/training/output/arc_corpus/export/adaption_run2_v1/eval_run2/`.

### Fireworks Muse Glimmer offer recheck

The current Fireworks Muse Glimmer model page advertises SFT at no charge via
the UI and Serverless Training API through November 30, with no credit card
required. This supersedes the earlier owner-reported October 31 date. The same
page marks Muse Glimmer serverless inference as unsupported, so this offer does
not provide a verified post-training inference route. Public pricing lists
separate managed-training, serverless-training, and inference charges outside
the offer. Keep Glimmer experiment-only and do not submit a job until the
account's offer is visible and a no-cost or explicitly covered evaluation path
is confirmed. Source: [Fireworks Muse Glimmer model page](https://fireworks.ai/models/fireworks/muse-glimmer-30b)
and [Fireworks pricing](https://fireworks.ai/pricing), checked 2026-10-19.

#### 2026-10-19 14:43 UTC checkpoint creation during cleanup

A fresh authenticated inventory confirms checkpoints continued to be published
while the owner was deleting artifacts. The active runs are writing to these
four collections in `wutang/pixelated-empathy-kan28`:

- v1 LoRA `arc-sft-baseline-8ce8354c67ef-sft-resume` and train state
  `arc-sft-baseline-8ce8354c67ef-train-state-sft-resume`: latest v92,
  46,500 batches, both created 14:37:24-26 UTC.
- v2 LoRA `arc-sft-baseline-556695bfd5c4-sft-resume` and train state
  `arc-sft-baseline-556695bfd5c4-train-state-sft-resume`: latest v90,
  45,500 batches, both created 14:36:21-23 UTC.

The inventory now sees 30 LoRA and 26 train-state artifact versions across the
project, up from 28 and 24 at 14:34. This confirms the earlier cleanup list was
a point-in-time list and must be refreshed immediately before acting; it may
also explain why deleting older items did not stop new checkpoint creation.
The direct `Project.storageBytes` query still returned 26,396,506,333 bytes at
14:43:03 UTC, unchanged from 14:40:56. That field does not establish whether
physical quota was freed or what rolling billable storage reports. No artifacts
were deleted by this check. See the machine-readable
[`14:43 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1443Z.json);
do not treat the 14:39 candidate list as current.

#### 2026-10-19 latest-checkpoint paired evaluation

To check whether the mid-run failure persisted, the newest available adapters
(v1 v92, 46,500 batches; v2 v90, 45,500 batches) were paired against the W&B
base endpoint on the same five synthetic development cases. Both evaluations
completed with zero provider errors. Each adapter made zero tool calls. V1
returned the same short source-style answer on three of five prompts and two
other short variants; v2 returned that same answer on all five. Both adapters
passed only 2 of 7 applicable deterministic scenario checks, versus 3 of 7
for base; each arm had at least one failed check in all five cases. These are
small diagnostic scenarios, not a clinical or deployment evaluation, but they
show the same serious tool-agent capability failure seen at earlier checkpoints.

The repeated answer matches an assistant target that occurs 4,343 times in each
uploaded training split (2.538% of v1's 171,121 training rows and 2.537% of
v2's 171,167). A local scan of the full 190,139-row candidate found 4,774 exact
assistant targets for this response; all were labeled `reddit_mental_health_posts`
and `symptom_classification`. This is strong evidence that the adapters learned
a frequent classification/placeholder response that does not fit these agent
tasks; it does not establish this as the sole cause of failure. Do not promote
either checkpoint. Preserve both active jobs through terminal state as already
requested, then run the final paired evaluations; diagnose the training mix and
assistant-turn weighting before preparing any follow-on training release.

Combined estimated W&B inference usage for these 10 paired cases was
$0.007011; actual billed usage was not returned. Per-case outputs, usage,
latencies, and config hashes are in
[`wandb-full-corpus-latest-checkpoint-summary.json`](execution-2026-10-18/results/wandb-full-corpus-latest-checkpoint-summary.json)
and its `wandb-full-corpus-v1-step-current-paired/` and
`wandb-full-corpus-v2-step-current-paired/` sibling directories. No source
message text is copied into the summary.

#### 2026-10-19 14:50 UTC evaluation trend and current storage

The paired check was repeated on the next checkpoint pair (v1 v93 at 47,000
batches; v2 v91 at 46,000). Results remained poor: both adapters made zero tool
calls and passed 2/7 applicable deterministic checks; v2 returned one identical
answer for all five prompts, and that exact answer appears 4,343 times in its
training split. V1 returned four distinct short answers; one exactly matches
an assistant target appearing 8,047 times in its training split. Across all
six checkpoint evaluations from 42,500 through 47,000 batches, both releases
stay at 2/7 checks and zero tool calls. The
[`checkpoint evaluation trend`](execution-2026-10-18/results/wandb-full-corpus-checkpoint-eval-trend.json)
stores per-run hashes and aggregate response/source-target matches without
including source message text.

The source-bound train split confirms a large task-mix mismatch: 91,186 of
171,121 training rows (53.287%) are `symptom_classification` examples from two
Reddit-labeled source groups. `reddit_mental_nlp` contributes 63,813 rows with
six unique final class labels; `reddit_mental_health_posts` contributes 27,373
rows with five repetitive subreddit/diagnosis templates. The adapters' repeated
outputs match those training targets exactly. This does not prove the source
mix is the sole cause, but it is a specific, measured diagnosis to use for a
controlled follow-on ablation. Keep the full-corpus runs intact and compare
any reweighted or task-focused dataset as a separate, hash-bound variant after
these jobs finish.

At 14:49:51 UTC the project `storageBytes` reading was 28,281,858,307 bytes,
up 1,885,351,974 bytes from 14:43. Each active job added a LoRA checkpoint
(117,843,308 bytes) and train-state checkpoint (1,060,414,709 bytes). This is
net project growth after any concurrent cleanup; the account's quota ceiling
and billable rolling-window usage remain unverified. Current exact versions
and storage reading are in
[`14:49 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1449Z.json).

The 53.287% figure is a row share, not a token-loss share: symptom-classification
assistant targets account for 2,249,532 of 98,689,036 assistant-target
characters (2.28%). The stronger format mismatch is direct: the uploaded
171,121-row split contains 521,053 user messages and 532,557 assistant messages,
with zero `tool` messages and zero structured assistant `tool_calls`. The
887 `long_session_arc` rows also contain no structured tool interactions. Thus
the full-corpus job can test conversational adaptation, but it cannot teach the
requested tool-use behavior from this payload. The existing 1,200-example
first-party synthetic tool-call release is the properly structured next
comparison; its baseline is already complete, and the trained arm remains
pending. Its local candidate has 960 train, 120 validation, and 120 test rows,
with 1,200 structured tool-call messages in training. See
[`release-manifest.json`](agent-tool-sft-2026-10-19/release-manifest.json).

#### 2026-10-19 14:56 UTC training progress and refreshed cleanup candidates

The W&B job endpoint still reports `RUNNING` with a null `progress` field, but
its read-only events endpoint exposes the planned total: 85,561 gradient steps
for v1 and 85,584 for v2. The newest artifacts are v1 v93 at 47,000 steps and
v2 v92 at 46,500 steps. Recent 500-step checkpoint intervals took about 9.5
minutes, implying roughly 12 hours 20 minutes remain if that rate holds and
storage continues to allow saves (projected completion around 03:10-03:20 UTC
on 2026-10-20). This is an estimate from current checkpoint cadence, not a
provider ETA. The final paired-evaluation watcher remains active.

A fresh inventory at 14:55:46 UTC found 42 older artifacts in the four active
collections that can be pruned under a two-newest-checkpoints-per-collection
retention rule: v1 LoRA and train-state v82-v91; v2 LoRA and train-state v80-v90.
All 42 had no aliases and `used_by()` returned zero. Retain v1 v92-v93 and v2
v91-v92 across both artifact types, preserving the two newest recovery points;
these include the last evaluated LoRAs and the latest checkpoints. Candidate
versions total 24,743,418,357 logical bytes (23.04 GiB). This is a concrete
lower-risk cleanup set, not a promise that W&B will reclaim that amount of
physical quota. The direct project storage reading was 28,281,869,701 bytes at
14:56:15 UTC, essentially unchanged from 14:49 despite v2's new checkpoint, so
the storage metric may lag or deduplicate versions. No artifacts were deleted
by this check. Exact current aliases, version metadata, and candidates are in
[`14:55 cleanup inventory`](execution-2026-10-18/live-monitor/checkpoint-cleanup-candidates-2026-10-19T1455Z.json).

#### 2026-10-19 15:00 UTC latest paired evaluation and storage refresh

The newest paired evaluations used v1 v94 (47,500 batches) and v2 v92 (46,500
batches). Both completed all 10 calls without provider errors; each trained arm
returned one identical answer on all five cases, made zero tool calls, and
passed 2/7 applicable deterministic checks. The v1 answer exactly matches a
training target found 8,047 times in its train split; v2's answer matches a
target found 4,343 times. Estimated inference usage was $0.00706475 combined;
actual billing was not returned. The summary now contains eight checkpoint
checks across four paired points, from v1 step 43,500 / v2 step 42,500 through
v1 step 47,500 / v2 step 46,500.

The training events still give totals of 85,561 and 85,584 steps. With the
latest checkpoint cadence, v1 is about 55.5% complete and v2 about 54.3%; the
current estimate remains roughly 12 hours, around 03:15 UTC on October 20 if
saves continue. W&B reports both jobs as `RUNNING`; the final paired-evaluation
watcher is still active.

At 15:00:19 UTC, `Project.storageBytes` returned 30,167,214,689 bytes. This is
up 1,885,344,988 bytes from 14:56:15, following v1's next checkpoint. It had
stayed nearly flat between 14:49 and 14:56 despite a v2 checkpoint, so the
meter may update with delay or deduplication. A fresh version inventory found
44 unaliased, zero-`used_by()` candidates if retaining the newest two artifacts
in each active collection: v1 LoRA and train-state v82-v92, and v2 LoRA and
train-state v80-v90. Keep v1 v93-v94 and v2 v91-v92 for recovery. The candidate
set is 25,921,676,374 logical bytes (24.14 GiB); physical quota reclamation is
not guaranteed. No artifacts were deleted by this check. The 15:00 inventory
supersedes the earlier 14:55 list:
[`15:00 cleanup inventory`](execution-2026-10-18/live-monitor/checkpoint-cleanup-candidates-2026-10-19T1500Z.json).
The corresponding evaluation details are in
[`checkpoint evaluation trend`](execution-2026-10-18/results/wandb-full-corpus-checkpoint-eval-trend.json).

#### 2026-10-19 15:02 UTC synthetic tool-SFT release reproducibility

Rebuilt the existing first-party synthetic tool-use dataset into a temporary
folder and compared it with the frozen release. The generated release manifest,
train/validation/test payload hashes, row-reference hashes, row counts, and
held-out evaluation hash all matched exactly. The training split is 960 rows
with 1,200 structured tool-call messages; the train payload is 1,431,878 bytes
plus 390-byte metadata. The generator's privacy and split checks passed. This
confirms the package is reproducible and small to upload; it does not resolve
W&B checkpoint headroom. The source release remains
`local_synthetic_research_candidate_not_uploaded`; no training job was created
by this verification. See
[`agent-tool-sft-2026-10-19/release-manifest.json`](agent-tool-sft-2026-10-19/release-manifest.json)
and the completed W&B base baseline. The W&B account's available inference
credit balance remains unavailable through the inspected interfaces, so prior
costs are usage estimates rather than reconciled charges.

#### 2026-10-19 W&B inference usage bounds

The 11 completed W&B paired-evaluation runs with local manifests total an
estimated $0.03287050, with $0.323712 in their configured maximum bounds; no
actual billed amount was returned for any of them. Adding the separate 120-case
synthetic tool-use base baseline gives $0.12803475 estimated usage and $0.784512
in combined configured maximums. These bounds cover recorded W&B inference
experiments, not the account's available credit balance. The exact balance and
charge reconciliation remain unavailable, and the ledger excludes the pending
trained-tool-SFT evaluation. See
[`W&B inference usage ledger`](execution-2026-10-18/results/wandb-inference-usage-ledger.json).


#### 2026-10-19 15:05 UTC artifact reconciliation during user cleanup

A fresh read-only W&B API check confirms that checkpoint artifacts were still
being created during the cleanup window: v2 LoRA v93 was created at 15:04:44Z
and its matching train-state v93 at 15:04:46Z. v1 remains at paired v94
(14:56:44Z / 14:56:46Z) in this sample. The earlier 15:00 inventory was a
candidate snapshot, not a deletion log, and was stale for v2 by 15:04. Under
the same newest-two retention rule, v2 candidates would now start at v80-v91;
v1 remains v82-v92. The API still lists these versions, so this read did not
confirm deletion of those candidates and cannot identify other artifacts the
user removed in the UI. Do not interpret a cleanup candidate as a confirmed
removed artifact or assume storage quota was reclaimed. Current snapshot:
[`15:05 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1505Z.json).


#### 2026-10-19 15:07 UTC live checkpoint evaluation and billing qualification

A fresh read-only Training API poll returned both full-corpus jobs as `RUNNING`,
with `progress=null`, stale `updated_at` values, and no error message. Their
training start times remain 2026-10-18 22:44:42Z (v1) and 23:13:12Z (v2). The
artifact API shows paired v1 v94 and v2 v93 checkpoints; the v2 pair landed at
15:04:44Z/15:04:46Z while the owner was clearing space. A matched five-case
base/SFT diagnostic on v2 v93 completed with 10/10 successful calls, no tool
calls from the SFT arm, 2/7 deterministic checks passed for SFT, and all five
SFT responses identical. Base passed 3/7; two base outputs reached the 512-token
cap. Estimated cost was $0.00345425 under the current configured W&B Qwen3.6
35B-A3B token rates; actual billing remains unavailable. The estimated maximum
under that rate and the fixed request cap is $0.03456. This five-case shared
template suite remains diagnostic only. Results are recorded in the
[`v2 v93 paired evaluation`](execution-2026-10-18/results/wandb-full-corpus-v2-step-47000-paired/manifest.json),
[`checkpoint trend`](execution-2026-10-18/results/wandb-full-corpus-checkpoint-eval-trend.json),
and [`latest checkpoint summary`](execution-2026-10-18/results/wandb-full-corpus-latest-checkpoint-summary.json).

The authenticated W&B project `storageBytes` field read 30,167,440,389 B
(28.096 GiB) at 15:07Z, up 225,700 B from the 15:00Z reading. This metric does
not reveal the plan quota, rolling billable storage, or which UI artifacts were
removed; current artifact listings still include the checkpoint versions in
the cleanup-candidate ranges. The older cleanup JSON is a snapshot of possible
retention candidates, not a deletion audit. See the
[`15:07 storage snapshot`](execution-2026-10-18/live-monitor/project-storage-usage-2026-10-19T1507Z.json).

Pricing snapshot (superseded): the then-viewed W&B Training pricing page was
read as saying Serverless SFT/RL was free during public preview and listed
Qwen3.6-35B-A3B inference at $0.25/M input and $1.25/M output. The legacy docs
repository is now archived and the former training-pricing URL redirects to
CoreWeave Forge pricing. W&B training entitlement and charges for existing
jobs remain unverified; do not assume either free preview terms or the Forge
rate applies. Verify current account/provider terms. Inference and storage are
separate meters; actual account balances and charges remain unknown.


The v2 v93 paired diagnostic is included in the refreshed [`W&B inference usage ledger`](execution-2026-10-18/results/wandb-inference-usage-ledger.json). Across its 12 unique completed manifest runs, estimates now total $0.03632475 (configured maxima $0.358272); including the separate 120-case tool-use baseline, campaign estimates are $0.131489 and configured maxima are $0.819072. Actual charges and account credit balance remain unavailable.

#### 2026-10-19 15:19 UTC correction: live checkpoint inventory advanced during cleanup

The owner was right that the previous 15:05 inventory was stale. A new read-only
inventory at 15:19:16Z found v1 LoRA and train-state v96 (created 15:15:58Z and
15:16:00Z), and v2 LoRA and train-state v94 (15:14:13Z and 15:14:15Z). Both
jobs still report `RUNNING`; API progress is null and `updated_at` remains at
job start. The W&B project `storageBytes` metric is now 33,938,141,393 B
(31.605 GiB), up 3,770,701,004 B from 15:07. This is compatible with the
checkpoint writes observed during the user's cleanup, but does not show which
items were deleted or whether physical quota was reclaimed.

If retaining the newest two in each active artifact collection, the older
listed versions are now v1 v82-v94 and v2 v80-v92, for each LoRA and train-state
collection. That represents 30,665,078,442 logical bytes by artifact size, not
a promise of recoverable quota. The API still listed these candidates at this
snapshot. Train-state artifacts are about 1.060 GB each and are needed for
full resume; LoRA artifacts are about 118 MB. Keep the newest two of both types
per run if maintaining resume recovery. This refreshed candidate range is not
a deletion log or a blanket deletion recommendation. See
[`15:19 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1519Z.json).

#### 2026-10-19 15:21 UTC paired diagnostics for active v1/v2 checkpoints

Ran the frozen five-case synthetic dev suite against the matched base and the
newest checkpoints visible at 15:19: v1 LoRA v96 (48,500 batches) and v2 LoRA
v94 (47,500 batches). Both paired runs completed 10/10 calls. Estimated usage
was $0.003528 for v1 and $0.00359175 for v2, each below the $0.03456 request
cap; actual billing was not returned. Both SFT checkpoints produced one
identical response across all five cases, made zero tool calls, and passed 2/7
deterministic checks. Each matched base passed 3/7 checks, made zero tool
calls, and hit the 512-token output cap on two cases. This repeats the existing
collapse/tool-use failure signal at later checkpoints; it does not show
improvement over training. The suite is only a five-case diagnostic and is not
a clinical or deployment evaluation.

Results and per-case hashes are in the
[`v1 v96 paired evaluation`](execution-2026-10-18/results/wandb-full-corpus-v1-step-current-1519-paired/manifest.json)
and
[`v2 v94 paired evaluation`](execution-2026-10-18/results/wandb-full-corpus-v2-step-current-1519-paired/manifest.json).
The refreshed [`checkpoint trend`](execution-2026-10-18/results/wandb-full-corpus-checkpoint-eval-trend.json),
[`latest checkpoint summary`](execution-2026-10-18/results/wandb-full-corpus-latest-checkpoint-summary.json),
and [`inference usage ledger`](execution-2026-10-18/results/wandb-inference-usage-ledger.json)
include both runs. Across 14 completed paired manifest runs, estimated usage
is $0.0434445, with combined configured maxima of $0.427392. Including the
separate 120-case tool-use baseline, the campaign estimates are $0.13860875 and
$0.888192 configured maximum. These are usage estimates, not reconciled bills
or a check of account credits.

#### 2026-10-19 current-master v3 dataset refresh, local staging only

Rebuilt the current 190,230-row master with the established deterministic
projection, pattern redaction, and content-group split. All 190,139 rows in the
pinned v2 candidate were rebound by exact source/message signatures, and all 52
repairs were rebased to current-master row numbers and hashes. The other 91
rows span 35 ARC source labels. The grouped source-decision ledger preserves
all prior dispositions; every one of the 91 added rows remains rights
`unresolved`, privacy `unverified`, training eligibility on hold, authority
awaiting human sign-off, and generic-license clearance not exact-row clearance.
No decision was upgraded. The local v3 manifest has
`status=local_staging_pending_scope_direction` and `upload_gate=false` because
the 2026-10-18 direction and running W&B jobs are pinned to the 190,139-row
candidate hash.

The staged v3 contains all 190,230 rows with no structural drops, 52 repairs,
and exact train/validation/test counts of 171,250 / 9,671 / 9,309. All payload
hashes match the manifest; the three group-split intersections are zero. The
basic post-redaction email/SSN/phone/URL/IP pattern screen has zero hits, after
73 email, 59 phone, 2,854 URL, 195 IPv4, and 10 payment-card redactions.
Clinical NER was not run and this does not certify de-identification or source
rights. No upload or new training job was started. Machine verification is in
[`current-master v3 lineage check`](execution-2026-10-17/current-master-v3-lineage-check-2026-10-19.json),
with the staged
[`v3 manifest`](execution-2026-10-18/wandb-full-corpus-release-v3-staged.json)
and local [payload directory](../../../ai/data/curated/recovery/gold-20261017/wandb-full-corpus-current-master-20261019-v3).

#### 2026-10-19 120-case tool-use comparison for full-corpus checkpoints

Evaluated v1 LoRA v97 and v2 LoRA v95 on the frozen 120-case synthetic
held-out tool-use suite. This is the same case hash as the saved base-model
benchmark; its 110 successful base cases and separate retry of the remaining 10
are combined for comparison. The base result is 189/240 deterministic checks
passed, 77 cases with all checks passing, and 142 tool calls across 85 cases.
Each full-corpus SFT checkpoint completed all 120 cases but passed only 60/240
checks, with only 30 cases passing all checks and zero tool calls. v1 returned
one identical response for all 120 cases; v2 returned only two distinct
responses (110/10 occurrence split). This confirms the repeated-response and
tool-use collapse signal on a substantially broader test set. These are
synthetic capability checks, not clinical safety or quality evidence.

Each SFT run's estimated cost was about $0.0153, below the configured maximum
of $0.41472; actual billing was not returned. The SFT-only comparisons reused
the saved base benchmark, so they did not spend on another base arm. Detailed
per-family results and hashes are in the
[`120-case tool-use comparison`](execution-2026-10-18/results/wandb-full-corpus-tool-heldout-120-comparison.json),
with the individual [v1 v97 run](execution-2026-10-18/results/wandb-full-corpus-v1-tool-heldout-120-v97/manifest.json)
and [v2 v95 run](execution-2026-10-18/results/wandb-full-corpus-v2-tool-heldout-120-v95/manifest.json).
The inference ledger now covers 16 paired/single-arm manifest runs: $0.074044
estimated for those runs, plus the separate base tool-use benchmark, for a
$0.16920825 campaign estimate. Combined configured maxima total $1.717632
including the benchmark retry cap. These remain model-rate usage estimates;
actual billing and available account credits are unknown.

#### 2026-10-19 15:30 UTC full-corpus training heartbeat after cleanup

A fresh authenticated read at 15:30:44Z returned both jobs as `RUNNING` with no
error and null progress. Latest retained artifacts are v1 LoRA/train-state v97
at 49,000 completed batches (15:25:40Z / 15:25:42Z) and v2 v95 at 48,000
batches (15:23:41Z / 15:23:44Z). Each train-state artifact is about 1.06 GB;
each LoRA is about 118 MB. The project `storageBytes` metric is
35,823,507,422 B, up from 34,880,813,887 B at 15:26:44Z. It is not the plan
quota or a deletion audit. Current retention candidates under newest-two
retention are v1 v82-v95 and v2 v80-v93 in each pair of collections; the
artifact inventory still lists them. See
[`15:30 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1530Z.json).

#### Repeated-response diagnosis from the 120-case run

Both checkpoints emit the same exact response hash on the held-out tool suite:
v1 v97 emits it on 120/120 cases and v2 v95 on 110/120. A privacy-safe hash
match against the v2 training payload found that target 8,047 times across
8,016 content groups, all under `reddit_mental_health_posts` /
`symptom_classification`. That is 4.70% of training rows and 1.51% of weighted
assistant-target messages. The remaining 10 v2 responses had no exact training
target match. This is strong evidence for a frequent-completion attractor and
helps explain the collapse, though it does not isolate the sole cause. The
full-corpus runs share the same 190,139-row candidate and the same visible
recipe (`assistant_turns=all`, `batch_size=auto`, `learning_rate=1e-4`), so the
52-row repair difference does not explain the common output. See the
[`collapse diagnosis`](execution-2026-10-18/results/wandb-full-corpus-collapse-diagnosis.json).

Next useful full-scope experiment: preserve every pinned source row, report
results by task family, and alter the training objective/mixture or schedule
so one exact target cannot dominate; evaluate earlier checkpoints with a
larger held-out tool set. Wait for the two active jobs to terminate and verify
artifact headroom before launching another W&B run, since the project storage
metric continues to rise and quota remains unavailable.

#### Adaption route recheck

The live Adaption connector lists Qwen3.6-35B-A3B and a completed existing run
`8da8f685-7ef6-43c0-958e-ab34dbdcd520` on the succeeded 11,192-row dataset
`arc-run2-train-v1`; its internal best win rate is 64.14% and the checkpoint is
downloadable. The dataset's provider quality-evaluation summary is null. This
is a useful historical experiment, but its internal score is not comparable to
the fixed 120-case W&B task suite. The connected Adaption API and its official
API reference expose model download but no inference endpoint; the downloaded
adapter is only 27.5 MB and its pinned base weights are not local. This host
has no NVIDIA GPU, so the comparable next route is a qualified OVHcloud GPU
runtime loading the adapter and base, followed by the same held-out suite.
OVHcloud account access/region/cost remain unqualified. The user confirms
Adaption credits remain, but the live connector exposes no credit balance or
per-run debit. Provider evidence and limits are recorded in
[`provider and evaluation checkpoint`](execution-2026-10-18/provider-and-eval-checkpoint.json).
The official [Adaption API reference](https://docs.adaptionlabs.ai/api/) lists
AutoScientist training and model download routes; the [FAQ](https://docs.adaptionlabs.ai/resources/faq/)
says Adaptive Data estimates can return credits and duration, but those are not
an AutoScientist training quote.

The format audit now identifies a stronger candidate cause: 188,982 of the
190,139 pinned source rows (99.39%) contain a system instruction, including
all symptom-classification, therapy-response, literature, risk, and severity
examples. The v2 release renderer removed system-role messages; the actual v2
payload has zero system messages. The repeated target comes from the
symptom-classification source, so the model was trained on those targets
without most of their task-level instructions. This is consistent with the
observed collapse and should be tested directly. ART's SFT data format accepts
`system` messages and masks instruction/user tokens from the loss, so we have
staged a matched 190,139-row variant that keeps system messages at weight zero
and preserves assistant weight one. It changes only the system-context
projection; model and three training hyperparameters match the active jobs.

The W&B G04 train-row validator previously rejected system roles. It now
accepts `system`, `user`, and `assistant`, while requiring zero weight for
system/user and weight one for assistant. Focused tests pass (2 passed), and
the actual 170,895-row variant train split passes the validator. The variant
payload hashes, 52 repairs, zero post-redaction pattern hits, and zero split
group intersections are verified. It remains local with upload/job gates off
until active runs terminate and storage capacity is verified. See
[`system-preserving package validation`](execution-2026-10-18/results/wandb-preserve-system-package-validation.json),
[`one-factor experiment recipe`](execution-2026-10-18/wandb-preserve-system-experiment-v1.json),
and [ART SFT data format](https://art.openpipe.ai/fundamentals/sft-training/).

#### 2026-10-19 15:39 UTC storage/checkpoint heartbeat

Both training jobs remain `RUNNING` with no API error and null progress. v1 has
LoRA/train-state v98 at 49,500 batches (15:35:13Z/15:35:15Z); v2 has v96 at
48,500 batches (15:33:13Z/15:33:15Z). The project `storageBytes` metric is now
37,708,953,809 B, up 1,855,446,387 B since 15:30. This metric does not return
quota or deletion history. Keep v1 v97-v98 and v2 v95-v96 for resume; older
listed candidates are v1 v82-v96 and v2 v80-v94 for each LoRA/train-state
collection. See
[`15:39 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1539Z.json).

The G04 training payload validator was updated to accept the ART-supported
`system` message role only with zero loss weight; user/context messages stay at
zero and assistant targets stay at one. Focused unit tests verify both
acceptance and rejection of an invalid system loss weight. Validation passed:
`uv run pytest -q tests/unit/ai/training/test_wandb_sft_g04.py` (2 passed),
`uv run ruff check` on the validator/test files, and `uv run ruff format --check`
on those files. The actual preserve-system train split also passes the G04
row validator (170,895 rows). These changes make the ablation package
upload-compatible without weakening assistant-only supervision.

#### 2026-10-19 15:41 UTC checkpoint timing correction

The user noted that new checkpoints appeared while they were deleting artifacts,
so the cleanup-era inventory may not have captured the relevant changes. A new
read-only refresh at 15:40:59Z confirms both jobs still report `RUNNING` and
have no error, while their job `updated_at` values remain at initial creation
and progress remains null. The artifact API lists v1 LoRA and train-state v98
at 49,500 batches (created 15:35:13Z / 15:35:15Z) and v2 v96 at 48,500 batches
(created 15:33:13Z / 15:33:15Z). Thus checkpoint writes are the reliable
progress signal here; the stale job timestamp is not evidence that checkpoints
are missing or the runs have stopped. See
[`15:40 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1540Z.json).

The project storage metric is unchanged from the 15:39 sample at 37,708,953,809
bytes. It provides no quota, deletion history, or reclamation timing, so the
current snapshot cannot identify which user-deleted artifacts were reclaimed
or whether any specific older version is safe to remove. Prior version ranges
were retention candidates based on a newest-two rule, not deletion records.

#### 2026-10-19 15:44 UTC follow-up after user artifact cleanup

A live watcher poll at 15:43:29Z confirms v2 wrote LoRA v97 at 49,000 batches
(created during the run); its train-state v97 is likewise recorded in the
refreshed artifact inventory. v1 remains RUNNING at v98 / 49,500 batches. Both
job API statuses remain RUNNING, while their status-update timestamps are
stale. This confirms the user's observation that checkpoint creation overlapped
artifact deletion; the previous checkpoint inventory was a point-in-time view
and cannot be used to infer that the run had no newer writes during cleanup.
The fresh read-only inventory is
[`15:43 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1543Z.json).
No deletion safety can be concluded without a deletion audit/quota view.

#### 2026-10-19 15:45 UTC project artifact inventory comparison

A fresh read-only inventory compared with 14:34Z shows the same 283 artifact
collections, but 347 visible versions versus 315 (+32). All net growth is in
active training checkpoint types: LoRA +16 versions / 1,885,492,928 logical
bytes and train-state +16 / 16,966,635,344 logical bytes. Dataset and other
artifact-type counts and logical sizes are unchanged. This confirms that the
large visible growth is from ongoing checkpoint writes; new checkpoints may
offset storage freed by cleanup. It does not reveal physical quota use or
provide a deletion audit, so we cannot identify deleted items from this API.
See [`15:44 project artifact inventory`](execution-2026-10-18/live-monitor/artifact-inventory-2026-10-19T1544Z.json).

#### 2026-10-19 15:52 UTC newer-checkpoint 120-case tool-use comparison

The same frozen 120-case synthetic tool-use suite was run against the newer
active checkpoints v1 v99 (50,000 batches) and v2 v97 (49,000 batches), using
the same decoding, token limits, tool-round limit, and $0.45 configured cap per
run. All 120 inference calls succeeded for each arm. Both checkpoints emitted
one identical response per arm across all 120 cases, made zero tool calls, and
passed 60/240 deterministic state checks. v1 is unchanged from v1 v97. v2 has
regressed from two distinct response variants at v95 to one repeated response
at v97, with no tool calls at either checkpoint. That confirms training has
not recovered tool-use behavior by these checkpoints. The test is synthetic
and does not establish clinical quality or safety. Estimated inference cost
was $0.015306 per arm; actual billing remains unavailable. See
[`current 120-case comparison`](execution-2026-10-18/results/wandb-full-corpus-tool-heldout-120-current-comparison.json)
and per-case outputs for [v1 v99](execution-2026-10-18/results/wandb-full-corpus-v1-tool-heldout-120-current-20261019T1548Z/manifest.json)
and [v2 v97](execution-2026-10-18/results/wandb-full-corpus-v2-tool-heldout-120-current-20261019T1548Z/manifest.json).

The usage ledger now contains 18 completed unique manifest runs, $0.104656
estimated inference usage ($0.19982025 including the separate 120-case base
run), and $2.547072 aggregate configured maxima including that baseline.
Actual billed values and remaining W&B credit balance are still not exposed.

#### 2026-10-19 15:54 UTC active checkpoint refresh

The persistent watcher remains live. Its 15:53:32Z poll observed both jobs as
`RUNNING`; v1 was at v99 / 50,000 batches and v2 advanced to v98 / 49,500
batches. A separate artifact refresh at 15:54:23Z found that v1 had advanced
again to v100 / 50,500 batches (both LoRA and train-state), while v2 remained
at v98 / 49,500. The API still supplies null progress and no total-step
estimate. See the [`15:53 watcher poll`](execution-2026-10-18/live-monitor/full-corpus-jobs.jsonl)
and [`15:54 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1553Z.json).
The latest 120-case evaluations at v1 v99 and v2 v97 both showed zero tool
calls and 60/240 synthetic checks passing. The terminal watcher remains set to
evaluate each final checkpoint when its respective job reaches a terminal
state.

The exact response hash at v1 v99 and v2 v97 is the same known training-target
hash previously traced to the high-frequency `reddit_mental_health_posts` /
`symptom_classification` response. It now appears in all 120 cases for both
new checkpoints; v2's 10-case alternate response at v95 disappeared by v97.
This strengthens the completion-attractor diagnosis, while leaving the
system-message-preservation ablation as the next experiment needed to isolate
causality. The raw repeated response is not included in reports. The current
comparison and collapse-diagnosis JSON record only hashes and counts.

#### 2026-10-19 Fireworks serving qualification refresh

The existing `FIREWORKS_API_KEY` authenticated a read-only GET to
`https://api.fireworks.ai/inference/v1/models` (HTTP 200; 22 models). Muse
Glimmer 30B is absent; the catalog includes Muse Spark Open and GLM 5.3 / 5.3
Flash. No inference request or provider spend was made. The current official
[Muse Glimmer model page](https://fireworks.ai/models/fireworks/muse-glimmer-30b)
says fine-tuning is supported, serverless inference is not, and serverless
availability ended starting 2026-09-25; on-demand deployment remains listed.
It currently advertises free SFT through 2026-11-30 (the user-provided notice
said October 31, so the live page is the fresher offer date). Account-specific
promo activation and credit balance remain unavailable. Fireworks remains
qualified for free SFT at the public-offer level, but not for matching hosted
inference or export of the adapter; no paid deployment should be launched
without a bounded cost decision. A current snapshot is recorded in
[`provider qualification`](execution-2026-10-17/provider-qualification.json).

#### 2026-10-19 16:03 UTC local checkpoint preservation

The latest LoRA adapters were downloaded from W&B and verified locally: v1
v100 at 50,500 batches and v2 v99 at 50,000 batches. Each includes
`adapter_config.json` and `adapter_model.safetensors` (117,842,120 bytes); local
SHA-256 digests are recorded in
[`private checkpoint manifest`](../../ai/training/output/wandb_local_checkpoints_20261019/manifest.json).
The private directory is mode 0700 and files are mode 0600. These are adapter
weights only; the base model and optimizer/train-state checkpoints are not
included, so local inference/resume still requires those dependencies. A
read-only backup watcher now snapshots newly published LoRA versions every
five minutes while either training job is active, keeps the two newest
versioned local adapter copies per run, and stops when both jobs are terminal.
It prunes only its own local versioned backup directory and does not delete any
W&B artifacts. Code is in
[`backup_wandb_full_corpus_lora.py`](../../ai/training/backup_wandb_full_corpus_lora.py).

#### 2026-10-19 frozen local breakaway package

The 522-row first-party synthetic edge subset is now frozen locally as
`g03-edge-synthetic-research-522-20261019-v1`. Reverification bound all 522
raw candidate rows and message bodies by SHA-256; the exported projection
preserves those roles and bodies while assigning user weight 0 and assistant
weight 1. The group-disjoint split is 410/72/40; 29 overlapping rows across 12
ARC IDs (11 seed groups) are excluded. Retained splits share no groups with
each other or the held-out exclusions, and the basic email/SSN/phone/card/URL/IP
regex scan found zero matches. The frozen manifest records file hashes and
keeps the package local. The historical generator provider/model receipt is
still missing, so provider transfer remains unqualified; the local freeze does
not assert clinician review, clinical safety, or production readiness. An
independent read-only recheck reconfirmed all 522 candidate row/message hashes,
seed-input artifact bindings, packaged payload hashes and body/role projections,
and split/held-out group disjointness. It found no local artifact that closes
the historical generation-provider/model and output-terms gap. See the
[`independent recheck`](execution-2026-10-17/g03-breakaway-independent-recheck-2026-10-19.md),
[`frozen breakaway manifest`](execution-2026-10-17/g03-edge-case-breakaway-frozen-2026-10-19.json),
and updated [`G03 review`](execution-2026-10-17/g03-edge-case-breakaway-review.json).

#### 2026-10-19 16:09 UTC rolling local checkpoint backup

The live W&B watcher at 16:08:36Z reports both jobs still `RUNNING`; v1 is at
v101 / 51,000 batches and v2 at v99 / 50,000 batches. A separate local backup
watcher has downloaded and hash-verified v1 v101 and v2 v99, with 0600 weights
under the 0700 private directory. The top-level private index was refreshed to
v1 v101 and v2 v99; version-specific manifests preserve each checkpoint's
W&B artifact URI, size, and SHA-256. The backup process remains live and polls
every five minutes. See [`16:08 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1608Z.json)
and the [private local checkpoint index](../../ai/training/output/wandb_local_checkpoints_20261019/manifest.json).

#### 2026-10-19 checkpoint creation during artifact cleanup

The user's observation that W&B showed new checkpoints while older artifacts were
being deleted is consistent with the live artifact timeline. These jobs publish
new versions into the specific `*-sft-resume` LoRA and train-state collections;
they do not stop publishing just because older artifacts are being removed. At
15:54Z, v1 had published v100 / 50,500 batches; by 16:03Z it published v101 /
51,000. v2 published v99 / 50,000 batches at 16:01Z. The 16:08:50Z read still
showed both jobs `RUNNING`, with all four latest LoRA/train-state versions
present. See the [`16:08 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1608Z.json).

This means the earlier concern that no checkpoints were appearing was a
misread of the artifact inventory, not evidence that checkpoint writing had
stopped. The most reliable signal is the newest version and its creation time
in each of the four collections above; the Training API's `progress` and
`updated_at` fields remain stale/null. Each new pair adds about 1.18 GB of LoRA
plus train-state data per run (about 2.36 GB across both runs), so storage can
continue to rise even as older versions are cleaned up. The available reads do
not expose a deletion event log, so they cannot establish which exact artifacts
were deleted or reconcile deletion volume against new writes. The rolling local
backup preserves LoRA weights only; it does not back up the much larger
train-state artifacts.

A fresh read-only backup poll at 16:11:44Z confirms the pattern continued during
this review: both jobs were still `RUNNING`; v1 remained at v101 / 51,000
batches and v2 had advanced to v100 / 50,500. The newly published v2 LoRA
adapter was downloaded and hash-verified locally. The private index now points
to v1 v101 and v2 v100. This live poll directly confirms ongoing checkpoint
creation while artifact cleanup is being discussed; it does not expose a record
of the user's individual deletion actions.

#### 2026-10-19 16:14 UTC checkpoint refresh and W&B price qualification

A fresh read-only poll at 16:13:51Z found both jobs still `RUNNING`: v1
advanced to v102 / 51,500 batches and v2 remained at v100 / 50,500. The local
backup watcher downloaded and verified v1 v102; the private index now tracks v1
v102 and v2 v100. This is further direct evidence that checkpoints continue to
publish while older artifacts are cleaned up.

W&B's published Serverless Training docs explicitly say the product is in
public preview and that W&B charges for inference and artifact storage, but not
adapter training, during preview. The former training-pricing URL now redirects
to CoreWeave Forge pricing, which lists $2.70/GPU-hour for Serverless SFT/RL.
The docs repository is archived, so its explicit preview terms remain the
published documentation but do not by themselves establish whether the terms
or account entitlement changed after the Forge migration. Whether the Forge
rate applies to W&B's existing jobs is also unverified. Do not use that rate
for these jobs without account/provider confirmation. The Training API exposes
no billing fields, and the available workspace credentials do not expose
inference-credit balance or storage headroom. Existing authorized runs remain
under monitoring; no reason to cancel them has been established.
[W&B training pricing](https://site.wandb.ai/pricing/training/)
· [W&B Serverless Training docs](https://github.com/wandb/docs/blob/main/serverless-training.mdx)
· [CoreWeave Forge Post-Training pricing](https://www.coreweave.com/forge-pricing/post-training)

#### 2026-10-19 Adaption account refresh and independent dataset recheck

A 16:12 UTC Adaption refresh used only read-only model, dataset, and run-list
calls. Qwen/Qwen3.6-35B-A3B remains eligible for SFT/DPO LoRA; existing run 2
is succeeded, downloadable, and has a platform win rate of 0.6414. Its 46 MB
adapter export is local, but does not include the base model and no matching
hosted inference route is exposed. The account connector exposes no numeric
credit balance, expiry, or per-run estimate, so it cannot bound another Adaption
run. The 11,192-row dataset is succeeded; the 418-row dataset is awaiting input.
No new run, dataset write, or inference call was made. See the live refresh in
[`provider qualification`](execution-2026-10-17/provider-qualification.md).

An independent read-only audit rechecked the frozen 522-row breakaway package:
all candidate-line and canonical-message hashes, seed input files, nested ARC
and session identifiers, packaged row hashes and exact body/role projection
match. The 410/72/40 split has zero group intersections across partitions and
with the 29 held-out exclusions. This supports its reproducible local research
freeze. The historical provider/model for the generated seeds and associated
output-use terms remain unbound, so the package is still not qualified for
provider transfer. See the [independent recheck](execution-2026-10-17/g03-breakaway-independent-recheck-2026-10-19.md).

#### 2026-10-19 16:17 UTC full-corpus lineage/version boundary

The metadata-only full-corpus audit binds all 190,139 rows in the active
candidate to the pinned source-label decision ledger with zero row-reference
hash or source-label mismatches. It also confirms the exact v2 release split and
payload hashes, with zero cross-split group overlap, and binds all 52 recorded
repairs to exact candidate-row hashes. The active candidate is an exact content
subset of the current 190,230-row master; 91 additional rows span 35 ARC labels
and have existing plan paths, but are absent from the active v2 training
release. This is a version boundary, not a reason to mutate the running jobs.
Preserve the pinned 190,139-row version for their evaluation; assess the 91-row
delta as a separate later release. The technical lineage report does not
resolve source-level rights/privacy questions. See
[`candidate lineage coverage`](execution-2026-10-17/candidate-lineage-coverage-2026-10-19.json)
and [`current-master v3 lineage check`](execution-2026-10-17/current-master-v3-lineage-check-2026-10-19.json).

#### 2026-10-19 16:18 UTC latest-checkpoint 120-case comparison

The same frozen synthetic agent-tool suite (120 cases; SHA-256
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`) was run
against the latest available W&B adapters: v1 v102 and v2 v100. Each completed
120/120 cases with no provider errors, zero tool-call traces, and 60/240
synthetic deterministic checks passed (30 cases passed all checks). The earlier
v1 v99 and v2 v97 runs both emitted one repeated response on every case,
matching the known high-frequency target hash. v2 v100 still emits that same
hash across all 120 cases. v1 v102 now emits a different repeated response
(hash `8c76f24a…`), but still only one response across all cases and still makes
no tool calls. The base benchmark, aggregated from its 110-case run and 10-case
retry, completed 120 cases, passed 189/240 checks, passed every check on 77
cases, and recorded 142 tool-trace events across 85 cases. This synthetic
diagnostic shows the full-corpus runs have not recovered tool use at these
checkpoints; it is not a clinical quality or safety result.

The estimated usage costs were $0.014556 for v1 v102 and $0.015306 for v2
v100. Actual billing remains unavailable. Each arm's configured worst-case cap
was $0.41472, combined $0.82944. The usage ledger now records 20 completed
manifest runs, estimated $0.134518 for those runs, and $0.22968225 including
the separate base benchmark; aggregate configured maxima including that base
benchmark are $3.376512. No actual billed values or remaining account credit
balance were exposed. See the [latest checkpoint comparison](execution-2026-10-18/results/wandb-full-corpus-tool-heldout-120-latest-checkpoint-comparison.json),
per-run [v1 manifest](execution-2026-10-18/results/wandb-full-corpus-v1-tool-heldout-120-v102-20261019T1618Z/manifest.json),
[v2 manifest](execution-2026-10-18/results/wandb-full-corpus-v2-tool-heldout-120-v100-20261019T1618Z/manifest.json),
and [usage ledger](execution-2026-10-18/results/wandb-inference-usage-ledger.json).

A fresh read-only W&B poll at 16:22Z showed both full-corpus jobs still
`RUNNING`; v1 remains v102 / 51,500 batches and v2 has advanced to v101 /
51,000. The new v2 LoRA adapter was downloaded and hash-verified; the private
local index now tracks v1 v102 and v2 v101. No inference rerun was launched at
v2 v101; the just-completed comparison used v2 v100.

#### 2026-10-19 16:26 UTC artifact inventory clarifies cleanup observation

The user was right to question whether the earlier check used the correct
artifacts. A direct inventory of all four active `*-sft-resume` collections
shows continued version creation and retention: v1 LoRA and train-state are at
v103 (52,000 batches), and v2 is at v101 (51,000 batches). Each collection
currently lists 22 versions (v1 LoRA/train-state v82-v103; v2
LoRA/train-state v80-v101). The newest two per run were created about ten
minutes apart. The local backup watcher has copied and hash-verified v1 v103
and v2 v101; its 16:25:44Z private index confirms these exact checkpoints.
See [`16:26 artifact inventory`](execution-2026-10-18/live-monitor/artifact-inventory-2026-10-19T1626Z.json)
and the [private local checkpoint index](../../ai/training/output/wandb_local_checkpoints_20261019/manifest.json).

So the user's deletion may have freed room, but it could not keep storage free
while these jobs continued publishing. The newest artifacts are distinct from
the older versions that may have been removed: each LoRA artifact is ~118 MB,
each train-state artifact ~1.06 GB, and one new pair per run adds ~1.18 GB.
The API inventory still exposes 22 retained versions in each collection; it
does not expose a deletion event log, so it cannot identify which exact items
were deleted or confirm their resulting storage impact. No further cleanup was
performed. The key practical point is that any cleanup during active training
is temporary unless older versions are pruned faster than new checkpoint pairs
are created; local adapter backups are preserved separately, but do not include
train-state files needed for full resume.

#### 2026-10-19 16:28 UTC local resume-state protection

The earlier rolling local backup protected adapter weights but not optimizer
and scheduler state. With about 90 GB free locally, I added
[`backup_wandb_full_corpus_train_state.py`](../../ai/training/backup_wandb_full_corpus_train_state.py)
and ran it against both active jobs. It downloaded and integrity-checked the
latest train-state artifacts: v1 v103 / 52,000 batches and v2 v101 / 51,000
batches, about 1.01 GB each. The private `train-state-manifest.json` records
both artifact URIs, versions, sizes, and local paths under the mode-0700 backup
root; files use mode 0600. A five-minute watcher is now running and retains the
two newest train-state versions per run. Combined with the existing adapter
watcher, future checkpoints should have local adapter and resume-state copies.
The W&B jobs and remote artifacts were not modified. Focused Ruff check passed;
the one-shot backup fetched both current state artifacts successfully.

#### 2026-10-19 16:34 UTC current checkpoints, local resume protection, and rerun

A fresh direct inventory at 16:33:52Z confirms both W&B jobs remain `RUNNING`.
The four relevant collections are the `*-sft-resume` LoRA adapter collections
and their matching `*-train-state-sft-resume` collections. Each currently lists
23 versions: v1 ranges v82-v104, and v2 ranges v80-v102. v1 v104 / 52,500
batches and v2 v102 / 51,500 batches are the current artifacts. Both adapter
backups and both train-state backups have been locally refreshed through those
versions; the private resume-state index records v1 v104 and v2 v102 at about
1.01 GB each. The 92 retained objects across these four collections total
about 54.2 GB (48.8 GB train-state and 5.4 GB adapters), according to W&B's
artifact sizes; this excludes datasets and all other project artifacts. The
train-state watcher remains active on a five-minute poll.
See [`16:33 checkpoint refresh`](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1633Z.json)
and the private [adapter](../../ai/training/output/wandb_local_checkpoints_20261019/manifest.json)
and [resume-state](../../ai/training/output/wandb_local_checkpoints_20261019/train-state-manifest.json)
indexes. The inventory API does not expose a deletion log, so the exact user-
deleted objects and net storage reclaimed cannot be reconstructed here.

Using the same frozen 120-case synthetic held-out suite, v1 v103 and v2 v101
both completed with 120/120 calls and no API errors. Each returned one identical
response for all cases, made zero tool calls, and passed 60/240 deterministic
checks (30/120 cases passed all checks); v2 v101 repeated the known target
response on all 120. v2 then published v102 during the evaluation window; its
same-suite rerun also completed 120/120 and reproduced the same collapsed
behavior (v2 v102 matches the target response hash on all 120). Estimated
inference usage for the three new runs totaled $0.044418; actual billing is
not returned by W&B. The configured cap was $0.41472 per run. The new results
and usage are recorded in the [latest-checkpoint comparison](execution-2026-10-18/results/wandb-full-corpus-tool-heldout-120-latest-checkpoint-comparison.json)
and [inference ledger](execution-2026-10-18/results/wandb-inference-usage-ledger.json).
The later v1 v104 checkpoint appeared at 16:32Z, after the v1 v103 evaluation,
and was then tested on the same suite. v1 v104 also returned one repeated
response for all 120 cases, made zero tool calls, and passed 60/240 checks
(30/120 cases passed all checks). Its output hash differs from the known
repeated target hash, but behavior remains collapsed on this suite. The run's
estimated inference usage was $0.014556; actual billing was unavailable. These
are synthetic diagnostics, not clinical-quality or safety evaluations.

The train-state backup watcher code is
[`backup_wandb_full_corpus_train_state.py`](../../ai/training/backup_wandb_full_corpus_train_state.py).
It keeps two newest local train-state versions per run and does not modify remote
artifacts. Ruff and `git -C docs diff --check` pass. One simultaneous one-shot
backup collided with the already-running watcher while both downloaded v1 v104;
the watcher completed and verified the copy, and the next poll succeeded, so
there is no missing local checkpoint.

#### 2026-10-19 16:44 UTC G04 local break-away release views

The 522-row G03 break-away freeze now has a complete, separate local release
layout at
[`g04-breakaway-release-20261019-v1`](../../../ai/data/curated/recovery/gold-20261017/g04-breakaway-release-20261019-v1/).
The builder is
[`build_g04_breakaway_release_views.py`](../../ai/training/build_g04_breakaway_release_views.py).
It emits provider-neutral canonical train/dev/test files (410/72/40), the exact
W&B weighted-message view, a Fireworks role/content view, row maps, private
lineage and split ledgers, `source_licenses.json`, `DATA_CARD.md`, a rendering
and lineage report, and a row-level backlog. The release manifest hash is
`de3820398395629d73bdde0845f5aff7f5c0e7d02e63794fc35accf7fdc1cd9b`.

An independent readback verified all 522 candidate-to-payload mappings, all 17
listed file hashes, split counts, zero source-group overlap, 29 held-out
exclusions, and private directory/file modes (0700/0600). The backlog records
1,566 open row-gate entries: generation terms, rights/privacy, and content
decision binding for each included row; the 29 held-out rows are separately
marked excluded. This is a technical local freeze and rendering, not a claim
that those 1,566 gates have passed. Upload and training gates remain false.
The Fireworks files use its documented role/content message shape, but do not
carry the canonical loss mask, so assistant-only loss behavior still needs
provider confirmation before any Fireworks job. See the [Fireworks SFT format
reference](https://fireworks.ai/blog/supervised-fine-tuning-tutorial).

The new output directory is private and untracked; no source candidate or
legacy G04 file was changed. Ruff passed for the builder. JSON validation and
`git -C docs diff --check` are the final checks for this update.


#### 2026-10-19 16:46 UTC live checkpoint confirmation and v105/v103 evaluation

A direct read-only W&B poll at 16:46:42Z confirmed both jobs still report `RUNNING` and both artifact streams are advancing. v1 has adapter and train-state v105 at 53,000 batches (created 16:41:32Z and 16:41:37Z); v2 has v103 at 52,000 batches (16:39:28Z and 16:39:31Z). All four collections list 24 current versions. The API does not expose deletion events or quota, so the stable collection count cannot establish what was deleted or how much storage was reclaimed. The new [`checkpoint stream confirmation`](execution-2026-10-18/live-monitor/checkpoint-stream-confirmation-2026-10-19T1646Z.json) records the exact collection names, ranges, sizes, and latest versions. Rolling local adapter and resume-state backups had already copied these versions.

The same 120-case held-out synthetic suite completed against both latest checkpoints: 120/120 responses each, zero API errors, zero tool calls, and 60/240 deterministic state checks passed (30/120 cases passed all checks). Both checkpoints emitted one exact response across all 120 cases, with the same hash (`8c76f24a…`); this differs from the previously observed high-frequency target hash. The model output changed, but remains behaviorally collapsed on this suite. Estimated usage was $0.014556 per run ($0.029112 combined); actual W&B billing was not returned. The ledger now records 26 completed manifest runs, an estimated campaign total of $0.31776825 including the base baseline, and a $5.864832 aggregate configured maximum. See the [latest-checkpoint comparison](execution-2026-10-18/results/wandb-full-corpus-tool-heldout-120-latest-checkpoint-comparison.json) and [inference usage ledger](execution-2026-10-18/results/wandb-inference-usage-ledger.json).


#### 2026-10-19 16:50 UTC v2 system-context inference ablation

To test the inference-time contribution of system instructions without retraining, v2 v103 was evaluated on the same 120 synthetic held-out cases after removing only each case's system message. All calls succeeded. The system-present condition yielded one repeated output on 120/120 cases. Without system messages, output hashes split 105/13/2 across three responses: the dominant response stayed the same, while 15 cases changed. Both conditions made zero tool calls and passed 60/240 deterministic checks (30 cases all checks). Removing system context increased some response variation but did not restore task behavior. This does not identify a training-time cause or substitute for the staged training-time preserve-system ablation. Estimated usage was $0.0128735; actual billing was not returned; configured cap was $0.41472. The case/config/result files are private (0700 directories, 0600 files). See the [system-context ablation summary](execution-2026-10-18/results/system-context-ablation-v2-v103-20261019T1650Z-summary.json).


#### 2026-10-19 16:55 UTC current checkpoint pair and local copies

The next direct W&B poll found v1 v106 and v2 v104, both still `RUNNING`; each of the four adapter/train-state collections had 25 versions (v1 v82-v106, v2 v80-v104). Both versions were evaluated on the same 120 cases. Each returned one exact response across all 120, made zero tool calls, and passed 60/240 deterministic checks (30 cases passed all checks). v1 v106 now emits a very short response (360 completion tokens across all cases); v2 v104 retained its prior repeated response. The result remains collapsed behavior on this suite, not a safety or clinical-quality result. The pair cost estimate was $0.026862, with actual billing unavailable.

The rolling local backup indexes have since caught up through v1 v106 and v2 v104 for both adapter and resume state. All indexed local files exist and match the file sizes in their backup manifests; indexes and local checkpoints remain private. See the [16:55 checkpoint refresh](execution-2026-10-18/live-monitor/checkpoint-refresh-2026-10-19T1655Z.json), [latest checkpoint comparison](execution-2026-10-18/results/wandb-full-corpus-tool-heldout-120-latest-checkpoint-comparison.json), and [inference usage ledger](execution-2026-10-18/results/wandb-inference-usage-ledger.json).


#### 2026-10-19 17:00 UTC full-candidate identity metadata audit

I re-read the exact pinned 190,139-row candidate locally and compared its byte hash with the existing lineage report. All 190,139 rows have a top-level source label and task type (475 distinct source labels), and the current W&B release has exact row-hash/source-label refs for all rows with group-disjoint train/validation/test splits. Only 9,679 rows contain structured provenance objects; 180,460 lack one. The candidate has no source record ID, source URI/URL, or row-level license field. The hash binding proves which recovered row was included; it does not supply the upstream source record or establish rights, privacy, or transfer permission. This is a quantified repair target for lineage enrichment, not a claim that the corpus is disallowed. No source content was changed. See the [metadata audit](execution-2026-10-17/candidate-identity-metadata-audit-2026-10-19.json) and [lineage coverage report](execution-2026-10-17/candidate-lineage-coverage-2026-10-19.json).


#### 2026-10-19 17:00 UTC candidate source-locator sidecar and output-target overlap

The full-corpus lineage gap is now concretely captured in a separate private sidecar. It covers all 190,139 candidate rows, verifies every raw candidate-row hash against the existing 190,139-row source ledger, and leaves the source file unchanged. Of these, 177,423 rows across 16 labels map to proposed but unratified source IDs; 9,679 rows carry structured local locator fields (book title, ARC session/plan, practitioner/channel, or scenario metadata); 12,716 rows across 459 labels remain without a proposed source ID, and 3,037 of those also lack structured locators. The sidecar keeps rights unresolved and privacy unverified, and claims no transfer clearance. It gives concrete row-keyed work products for enriching provenance without changing message text. See the [sidecar manifest](execution-2026-10-17/candidate-source-locator-sidecar-2026-10-19.json), [identity audit](execution-2026-10-17/candidate-identity-metadata-audit-2026-10-19.json), and [full-candidate lineage coverage](execution-2026-10-17/candidate-lineage-coverage-2026-10-19.json).

An aggregate-only exact-hash comparison also shows v1 v106's repeated response is itself present 22,690 times in training (4.26% of 532,603 assistant targets), while v2 v104's response occurs 4,304 times (0.81%) and the earlier repeated target 8,047 times (1.51%). The two minority outputs after removing system prompts had no exact target matches in train, validation, or test. This strengthens a target-attractor correlation but does not prove causation. See the [target-overlap report](execution-2026-10-18/results/wandb-full-corpus-response-target-overlap-20261019T1700Z.json).


#### 2026-10-19 17:05 UTC checkpoint inventory reconciliation

A fresh direct read-only poll of the W&B Training API and the exact `lora` and `train-state` collections confirms that the runs were creating checkpoints during the storage cleanup: v1 is `RUNNING` with v107 at 54,000 batches, and v2 is `RUNNING` with v105 at 53,000 batches. The LoRA and resume-state artifacts are both present at those versions. Current visible version ranges are v1 v82-v107 and v2 v80-v105. I had misread an incomplete/lagging inventory as a possible save failure; the live artifact records contradict that concern. The W&B listing does not expose artifact deletion history, so it cannot identify which items were removed during cleanup. See the [inventory reconciliation](execution-2026-10-18/live-monitor/checkpoint-inventory-reconciliation-2026-10-19T1705Z.json).


#### 2026-10-19 17:10 UTC base-model system-context ablation

The base Qwen endpoint completed all 120 case records after removing system messages. The evaluator recorded 115 successful completions and five `ToolRoundLimitExceeded` behavior failures after the allowed two tool rounds; there were no provider HTTP errors. Those failures remain failures rather than being retried away. On successful rows the base made 145 tool-trace events across 90 cases, with 157/227 observed state checks passing (240 expected); the five failed cases have no state score. The original system-present base outputs are available for all 120 matching case IDs; among the 115 jointly successful cases, outputs changed on 98 and stayed byte-identical on 17. This shows a material inference-time prompt effect on outputs and tool behavior, while the partial state-check coverage limits direct score comparison. It does not explain the trained-model collapse or establish clinical quality. Estimated call usage including failed attempts is $0.10627725; the manifest's success-only estimate is $0.10207775, actual billing is unavailable, and the configured run cap was $0.41472. See the [ablation summary](execution-2026-10-18/results/system-context-ablation-base-20261019T1657Z/no-system/summary.json), [comparison](execution-2026-10-18/results/wandb-full-corpus-tool-heldout-120-latest-checkpoint-comparison.json), and [usage ledger](execution-2026-10-18/results/wandb-inference-usage-ledger.json).


#### 2026-10-19 17:15 UTC paired latest-checkpoint evaluations

The newest locally backed-up adapter versions available at the start of this evaluation—v1 v107 (54,000 batches) and v2 v106 (53,500 batches)—both completed the same 120-case synthetic held-out tool-use suite. Each had 120/120 successful inference calls, returned one identical response hash across all cases (`e4e633d3…`), made zero tool calls, and passed 60/240 deterministic state checks (30/120 cases passed all checks). This is the same short-response hash previously observed at v1 v106; the exact hash appears 22,690 times among 532,603 training assistant targets. Both newest checkpoints changed the exact output on the same 120 case IDs compared with the previously evaluated base model, whose 120-case run is already recorded. Estimated usage was $0.012306 per checkpoint ($0.024612 combined); actual billed amount is unavailable, and each run's configured maximum was $0.41472. More optimization steps have not improved this diagnostic behavior; these are synthetic task-use results, not clinical-quality or safety evidence. See the [comparison](execution-2026-10-18/results/wandb-full-corpus-tool-heldout-120-latest-checkpoint-comparison.json), [target-overlap report](execution-2026-10-18/results/wandb-full-corpus-response-target-overlap-20261019T1700Z.json), and [usage ledger](execution-2026-10-18/results/wandb-inference-usage-ledger.json).

Scenario-level readout for both checkpoints is in their per-run `summary.json` files. The two checkpoints have identical scenario metrics on all eight 15-case groups. They pass all synthetic consent-gate checks in the appointment-consent and memory-consent groups (15/15 each), and 15/30 approval-gate checks and 15/45 untrusted-note checks. They score 0 on all 30 explicit-consent positives, 0/30 memory opt-in checks, 0/45 resource-comparison checks, and 0/30 resource-lookup checks; they invoke no tools. The base model on the same case IDs makes tool calls in all resource groups and passes more positive-task checks. This points to a narrow behavior pattern: the repeated checkpoint response preserves some deny/consent-gate outcomes but does not perform the requested positive tool tasks. It is a synthetic task diagnostic, not a clinical assessment.


#### 2026-10-19 17:23 UTC checkpoint deletion cross-check

The user observed new checkpoints appearing while deleting artifacts to make room. A new direct read-only query verified the exact four job-linked collections, using the W&B `lora` type for adapters and `train-state` type for resume state. Both jobs still report `RUNNING`. v1 currently has LoRA and train-state v109 (55,000 batches); v2 has both at v107 (54,000 batches). Each collection retains 28 versions: v1 v82-v109 and v2 v80-v107. Across these four collections the API reports about 66.6 GB in artifact sizes. The project storage metric last read at 17:19:50Z was 58,040,341,321 bytes; it is a separate metric and is not directly comparable to summed artifact sizes. The account quota and deletion audit remain unavailable through the queried API, so this confirms checkpoint creation but does not identify the items deleted or net space reclaimed. The local train-state mirror is current through v1 v109 and v2 v107; the local LoRA mirror is v1 v108 and v2 v107 as of its last poll, so the v1 adapter mirror may lag one checkpoint until its next five-minute poll. Updated [current checkpoint/storage snapshot](execution-2026-10-18/live-monitor/checkpoint-storage-state-2026-10-19-current.json).

#### 2026-10-19 17:31 UTC corrected live checkpoint inventory

The 17:23 snapshot was stale by the time it was used to discuss the cleanup.
A fresh read-only query of the exact collections linked to both job IDs now
shows v1 LoRA and train-state at v110 / 55,500 batches, and v2 LoRA and
train-state at v108 / 54,500 batches. Both jobs remain `RUNNING`; each of the
four collections lists 29 retained versions. This confirms the user's
observation that checkpoints were appearing during deletion. It does not
identify which artifacts were deleted: the available W&B API still has no
deletion audit or quota field. The local adapter mirror is current at v1 v110
and v2 v108. The train-state watcher had exited; a one-shot verified download
then copied v1 v110 and v2 v108 at 17:34Z, and a fresh five-minute watcher is
now live. Disk had 73 GB free before the 1.01 GB v1 resume-state download. The refreshed
[current inventory](execution-2026-10-18/live-monitor/checkpoint-storage-state-2026-10-19-current.json)
records exact artifact sizes and makes clear they are not a storage-quota
measurement.

#### 2026-10-19 Adaption qualification refresh

A read-only Adaption catalog check confirms `Qwen/Qwen3.6-35B-A3B` remains available for SFT/DPO LoRA; run history still shows two succeeded, downloadable runs. The connector exposes no credit balance/expiry or cost estimate, and no hosted inference endpoint. Current docs specify 1,000 effective SFT rows and 12,000 effective preference pairs for DPO; the recorded 11,192-row run-2 dataset does not meet the DPO floor absent eligible augmentation. Adaption documents AutoScientist model download and processed-dataset export, but the checked public pages do not establish this account's retention terms. No resource or upload was created, and no credit coverage is inferred. See the [machine-readable qualification](execution-2026-10-17/adaption-qualification-refresh.json) and its source links. A new run remains gated on dashboard credits/expiry, a settings-specific cost estimate with no uncovered spend, a matching inference route, and export/retention confirmation.


#### 2026-10-19 local adapter-declaration match for three source labels

Read-only inspection matched the candidate labels `counseling_conversations`
(1,415 rows), `crisis_benchmark` (1,522), and `ml_bpd` (100) to exact local
adapter registrations and emitted `source` fields. For these 3,037 rows, a
private additive sidecar binds candidate row/message hashes and source labels to
the adapter path/hash/key and code-declared upstream URL/repository. All rowrefs
are unique and hash-verified against the current pinned candidate and existing
source-decision ledger. The evidence level is
`adapter_source_declaration_only`; status remains
`upstream_row_locator_unbound`. Adapter declarations do not prove row-level
upstream origin or rights, privacy, clinical, or transfer eligibility. The
sidecar directory/files are mode 0700/0600 and gitignored; no source data or
existing worklist was changed. See the [aggregate report]
(execution-2026-10-17/candidate-adapter-declaration-enrichment-2026-10-19.md)
and private manifest at
`ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/manifest.json`.

#### 2026-10-19 ml_bpd source-row binding and content check

An exact metadata-only join against the public `machine_learning_BPD` CSVs at
commit `41a6535acbd5389766d18882e9b9b20ca89660ea` matched the user-message
content of all 100 candidate `ml_bpd` rows. Fifty-six prompts identify one
upstream record; 44 prompts are duplicated across multiple upstream records,
though every duplicate has the same BDI-derived severity class. All 100
assistant labels match the source adapter's threshold rule. The candidate's
system messages differ from the current adapter system prompt, so none of the
full three-message records are byte-equivalent to current adapter output. The
repository root contains no license file; the source contains sensitive
clinical assessment measures. No rights, privacy, clinical validity, or
provider-transfer conclusion is inferred. A private sidecar binds candidate
hashes to exact upstream file/row candidates; files are mode 0600 in a mode
0700 directory. See the private
[`ml_bpd` report](../../../ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/ml_bpd-upstream-binding-report-2026-10-19.json).

#### 2026-10-19 17:48 UTC corrected checkpoint and full artifact inventory

The user's observation was correct: new checkpoint versions were created while
the artifact cleanup was underway. A direct query at 17:48 UTC found both jobs
still `RUNNING`; v1 LoRA and train-state were v112 / 56,500 batches (created
17:46:38Z and 17:46:40Z), and v2 was v110 / 55,500 batches (17:44:15Z and
17:44:18Z). Each of the four active collections currently lists 31 versions.
At 17:50 UTC, the rolling local adapter and resume-state mirrors had caught up
to v1 v112 and v2 v110. Both backup watchers remain running.

The previous investigation only queried those four job-linked checkpoint
collections. A broader read-only project inventory found 279 artifact
collections across 8 types. It includes 4 completed-run resume-state artifacts
with no downstream `used_by` runs: three about 1.06 GB each and one 566 MB,
approximately 3.49 GiB nominal combined artifact size. Those are the strongest
cleanup candidates if retaining resume ability for those finished runs is not
needed. Their producer runs report `finished`; they are separate from both
active jobs. This is a candidate list, not a deletion: W&B's artifact API does
not expose deletion history or quota, and the displayed artifact sizes do not
guarantee an equal amount of physical storage will be reclaimed. Retain the four
active-job collections and the datasets used by those jobs. The exact named
candidate collections, run IDs, sizes, and retention caveat are recorded in the
[artifact storage audit](execution-2026-10-18/artifact-storage-audit-2026-10-19.md).

#### 2026-10-19 17:59 UTC checkpoint stream recheck

The user noted that the UI showed new checkpoints while cleanup was in
progress, which is consistent with the live artifact stream. A new direct
read-only query at 17:59 UTC found both jobs still `RUNNING`: v1 LoRA and
train-state v113 at 57,000 batches (17:55:53Z / 17:55:55Z), and v2 both at
v111, 56,000 batches (17:53:33Z / 17:53:35Z). Each active collection now lists
32 versions; the retained ranges remain v82-v113 for v1 and v80-v111 for v2.
The project `storageBytes` field read 65,581,760,073 bytes. It is not a quota,
and the API still exposes no deletion audit. This confirms checkpoint creation
but does not identify cleanup targets or prove storage was reclaimed. The
[refreshed snapshot](execution-2026-10-18/live-monitor/checkpoint-storage-state-2026-10-19-current.json)
supersedes the 17:48 figures above.

#### 2026-10-19 repaired-row quality audit and corrected crisis ablation

A local deterministic audit of the 52 repair records verified exact candidate,
repair-overlay, and v2-release row/hash bindings for all 52. It found no empty
or malformed messages, empty targets, placeholder markers, generic advice or
refusal phrase matches, or exact/near duplicate generated targets. All 50
generated continuations include the recovered source pair and continuation
instruction; six have very low character-trigram overlap with each source role.
These are structural and lexical checks, not semantic or clinical validation.
The 50 generated continuations remain unreviewed by a clinician; two source
triage examples are a different task family from counseling responses. The
[aggregate audit](execution-2026-10-17/repaired-rows-substantive-audit-2026-10-19.md)
records results without clinical text.

The first local crisis-benchmark ablation was based on the earlier v1 release
and therefore omitted all 52 repaired rows. The builder now pins the corrected
v2 source release. Its new private package retains 188,617 of 190,139 candidate
rows, excludes exactly the 1,522 placeholder-target crisis rows, and confirms
all 52 repaired row hashes are retained. Split sizes are 169,793 train, 9,587
validation, and 9,237 test; group intersections are zero. The manifest hash is
`688299e71655079b34e0760a6d0887ea70df9587c5ad6e5a49d70dc102d48c03`.
The package remains local-only with `upload_gate=false`; no provider upload or
training job was created. The earlier v1 package is historical and should not
be used as the corrected break-away. The reproducible builder is
[`build_crisis_benchmark_ablation.py`](../../ai/training/build_crisis_benchmark_ablation.py),
and the manifest is private under the `ai/data/curated` recovery tree.

#### 2026-10-19 18:12 UTC latest checkpoint backups and held-out evaluation

The separate W&B model-checkpoints endpoint was the wrong view for following
these jobs; it showed only base entries. The active runs publish to their
rolling LoRA and train-state artifact collections. The rolling monitor observed
v1 v114 at 57,500 batches and v2 v112 at 56,500 batches, and local backups of
both LoRA and train-state versions exist. The local backup workers remain live,
preserve the newest two versions of each artifact family per job, and use about
4.7 GiB of local disk with 66 GiB available. W&B did not expose artifact
Deletion history or quota in the checked APIs. See the local inventory at
`ai/training/output/wandb_local_checkpoints_20261019/` and the prior live
snapshot for the exact timestamped API evidence.

A matched 120-case synthetic held-out agent/tool evaluation completed for v1
v114 and v2 v112, against the W&B base model. Both adapters returned one exact
same response across all 120 cases, made zero tool calls, and passed 60 of 240
synthetic state checks; all tool-status and response-contains checks failed.
The base arm produced 111 successful responses and 9 `ToolRoundLimitExceeded`
failures in `resource_compare`; on its 111 shared successful cases, it made
79 tool traces and had no exact output matches with either adapter. The base
run is marked incomplete because those 9 cases exceeded the configured
2-tool-round cap. Token-based estimated costs were $0.012306 per adapter run
and $0.087427 for the base run; actual billed amounts were not returned. These
synthetic checks do not establish clinical quality or safety. The private
summary and metrics are in
[latest checkpoint comparison](execution-2026-10-18/results/latest-checkpoint-heldout-120-comparison-20261019.md)
and its JSON sidecar.

At the 18:12 UTC Training API check, v1 and v2 still reported `RUNNING` and
v4 job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` still reported `PENDING` with no
error. The v1/v2 event stream and rolling artifact backups remain the progress
signals; the model-checkpoints endpoint is not a reliable run-progress view.

#### 2026-10-19 AWS check for the `whitebat:` source cache

The read-only AWS MCP check in the current account found three buckets and no
bucket named `whitebat`; the declared `training/pixelated-empathy/output/`
prefix was empty in all three. This narrows the source-cache search to a
possible different account, role, or storage provider behind the local rclone
alias. It does not invalidate the candidate or imply that its source rows are
unusable. The exact account and prefix scope are in the
[local source-presence audit](execution-2026-10-19/local-upstream-source-presence-audit-2026-10-19.md).

#### 2026-10-19 18:14 UTC artifact-collection refresh

A direct typed-collection query (W&B Artifact API types `lora` and
`train-state`) at 18:13 UTC found v1 still at v114 / 57,500 batches, with 33
visible versions in each collection; v2 had advanced beyond the earlier 18:09
snapshot to v113 / 57,000 batches, with 34 visible versions in each
collection. The v2 local rolling mirrors were at v112 when checked at 18:14,
so they were one 500-batch checkpoint behind while their 300-second backup
workers continued polling. The current machine-readable snapshot records this
lag explicitly. This is the correct active checkpoint stream; the Training
model-checkpoints API is a separate view that showed only base step-0 entries.
No artifact deletion history or quota is exposed, so this still cannot identify
which UI items were deleted.

At 18:14:45 UTC, the local LoRA mirror had caught up through v1 v114 and v2
v113. The local resume-state mirror was v1 v114 and v2 v112, so only v2's
large train-state artifact lagged by one 500-batch interval at that check. Both
backup processes were alive; the LoRA worker had just refreshed its index. The
checkpoint snapshot has been updated to distinguish adapter and train-state
backup versions rather than reporting a single combined version per job.

The nine two-round base-limit cases were then rerun as a separate follow-up with
a four-round maximum. All nine succeeded after three tool rounds each; estimated
cost was $0.010751. The combined base coverage is now 120/120 successful outputs
(91 unique responses and 88 cases with tool traces), with zero exact output
matches against either adapter across the 120 case IDs. This combines 111
original two-round successes and nine three-round recoveries, so it is not a
single uniform-round-cap run. The machine-readable comparison and the recovery
run directory preserve that distinction.

#### 2026-10-19 18:18 UTC checkpoint mirror refresh

A fresh direct query found both jobs still `RUNNING`. v1 had advanced to LoRA
and train-state v115 / 58,000 batches, with 34 versions per collection. v2
remained at v113 / 57,000 batches, also with 34 per collection. The private
backup indexes at 18:17:41Z had v1 train-state v115, v1 LoRA v114, and both v2
artifact families v113. Thus v1's LoRA mirror lagged by one 500-batch
checkpoint; the other three mirrors were current. The live checkpoint snapshot
records exact creation times, counts, and this per-artifact lag.

The training event setup record reports 85,561 gradient steps for v1 and 85,584
for v2. Using artifact checkpoint deltas over the latest ~28 minutes (v1:
56,500 to 58,000; v2: 55,500 to 57,000), observed rates are about 53–54 steps
per minute. If those rates and reported totals hold, projected remaining time
from 18:18 UTC is roughly 8.5 hours for v1 and 8.8 hours for v2, near 03:00
UTC on 2026-10-20. This is a linear estimate from checkpoint progress, not a
provider ETA; the job status API's progress field is null.

At 18:19:47 UTC, both local backup workers had caught up: v1 LoRA and
train-state v115 / 58,000 batches; v2 LoRA and train-state v113 / 57,000
batches. A fresh SHA-256 and file-size verification passed for every file in
all four latest local artifacts (two adapter files and eleven resume-state
files per run). This is direct evidence that the newest adapters and resumable
optimizer state are being preserved locally while W&B continues creating
checkpoints. The local rolling backup is about 4.7 GiB and the workspace had
66 GiB free at the last disk check.

#### AnnoMI exact-origin follow-up

An exact adapter projection against both official AnnoMI CSV files at commit
`42936645ec3857a9c84ab296a36a3c34b779ef49` produced 133 records but matched
none of the candidate's 98 `annomi` rows by ordered role/content. Those rows
remain unbound; their family label does not establish row origin. The primary
repo did not provide a verified license grant. Hash-only evidence is private
under `ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/`;
the public-metadata audit records this result.

#### Newest-checkpoint behavior recheck (18:22–18:24 UTC)

To check whether the first evaluation was already stale, v1 v115 / 58,000
batches and v2 v113 / 57,000 batches each completed the same 120-case suite.
Both returned the same exact output on every case as each other and as v1 v114
and v2 v112. All four runs therefore emitted one unique response, made no tool
calls, and passed 60/240 unvalidated synthetic state checks per run. An
additional 500 training steps per job produced no change on this held-out suite.
The total estimated token cost for all base and adapter evaluations in this
round is $0.147402; actual billing is not available. The detailed summary is
updated in the [comparison report](execution-2026-10-18/results/latest-checkpoint-heldout-120-comparison-20261019.md).

#### 2026-10-19 18:25 UTC checkpoint view correction

The user's observation of new checkpoints during artifact cleanup was accurate.
The earlier query used the Training model-checkpoints view, which is not the
active SFT artifact stream. A fresh query and immediate local mirror refresh
found v1 at LoRA + train-state v116 / 58,500 batches and v2 at LoRA +
train-state v114 / 57,500 batches; both remain `RUNNING`. All four latest
artifacts were downloaded and file-size/SHA-256 verified. The local rolling
mirrors are caught up, and the five-minute backup workers remain active. The
current snapshot records the confirmed versions. This validates ongoing
checkpoint creation while cleanup was underway; it still does not identify the
specific deleted items or expose the W&B storage quota.

#### 2026-10-19 18:35 UTC artifact-stream recheck during cleanup

The user correctly noted that new checkpoints were appearing while deleting
artifacts. A fresh direct W&B Artifact API query confirms the active streams:
v1 LoRA and train-state are both v117 (59,000 batches, created 18:33:24Z and
18:33:26Z); v2 LoRA and train-state are both v115 (58,000 batches, created
18:30:29Z and 18:30:31Z). Each of the four collections currently lists 36
versions with no gaps in its retained range (v1 v82-v117, v2 v80-v115). The
rolling backup workers remain live; their latest local copies at the 18:33Z
check are v1 v116 LoRA/train-state and v2 v114 LoRA, v115 train-state. The
checkpoint snapshot was refreshed to distinguish the active remote stream from
the slightly lagging local mirror. This confirms checkpoint creation continued
during cleanup, while the API still does not expose which unrelated artifacts
were deleted or the storage quota.

#### Empath and MentalChat16K exact-origin joins

Pinned upstream projections now bind 27,291/35,977 Empath candidate rows and
1,107/11,135 MentalChat16K rows by ordered non-system turn sequence. Empath
breakdown: 12,042 unique, 15,249 duplicate-text ambiguous, 8,686 unmatched.
MentalChat16K: 1,090 unique, 17 ambiguous, 10,028 unmatched. System prompts
differ, so these matches do not establish full rendered-record identity or
rights clearance. Private sidecars, source revisions, and hashes are captured
in the [lineage report](execution-2026-10-19/empath-mentalchat16k-origin-binding-2026-10-19.md).

#### Adaption live read-only refresh (18:27 UTC)

The authenticated live connector still shows two succeeded, downloadable Qwen
3.6 LoRA runs and the `arc-run2-train-v1` dataset at 11,192 rows. A
recommendation call returned one-epoch SFT/LoRA settings but no cost or credit
estimate and created no run. The account's balance and expiry remain hidden, so
this confirms model/data compatibility and export precedent but does not prove
coverage for another job. The qualification JSON records the refreshed account
state.

#### Dataset break-away snapshot pinned (2026-10-19)

The chosen research break-away is the user-directed v4 rebuild from the final
gold candidate: 190,244 total rows and a 171,261 / 9,673 / 9,310 train/validation/test
split. I recomputed the candidate and all three partition hashes and line counts;
all match the manifest. This resolves the earlier 190,139 vs 190,244 difference:
they are distinct candidate snapshots with distinct hashes, and v1/v2 used
older 171,121 / 171,167-row train payloads. v4 job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` is the training job for the newer split
and was still pending at the latest status check. The 52 repairs and remaining
origin-binding caveats are carried forward in the
[break-away freeze note](execution-2026-10-19/dataset-breakaway-freeze-2026-10-19.md).

#### Fireworks training and inference route clarification (2026-10-19)

Current Fireworks documentation advertises Muse Glimmer SFT at no training
charge through 2026-11-30. Its ordinary serverless inference capability is
marked unsupported, and the authenticated model-list check omits Muse Glimmer.
The Serverless Training API does support sampling from saved adapter snapshots
while a training session is active. Those session checkpoints are not local
weight exports; after session end, serving requires promoting a sampler
checkpoint to a model and using an on-demand deployment. The account's prior
model download request was denied. Because Serverless Training lists separate
prefill/sample/train meters, coverage of those charges is not inferred from
the managed SFT offer. Provider qualification is recorded in
[provider qualification](execution-2026-10-17/provider-qualification.md).

#### W&B event-endpoint check (18:32 UTC)

The W&B training system health endpoint reports API, database, CPU queue,
model-management queue, and GPU queue healthy. The job-events endpoint returns
ongoing gradient-step events for v1 and v2; v4 remains `PENDING` and has no
training events at all, with no provider error in its job object. This confirms
v4 has not started yet but does not expose a queue reason. The event and health
snapshot is
[training-job-event-health-2026-10-19T1832Z.json](execution-2026-10-18/live-monitor/training-job-event-health-2026-10-19T1832Z.json).

#### 2026-10-19 Psy-Insight exact-origin binding

The 673-row current `psy_insight` family was joined to the adapter projection
from the original public GitHub repository at commit
`0a5bd3f011dd8fdb8d6b7c0081b3510e4a478f5a`. Exact full ordered non-system
role/content projection bound 518 candidate rows uniquely; 155 remain
unmatched, and no ambiguous exact-sequence matches occurred. The pinned
English/Chinese source JSON hashes, adapter hash, row hashes, and private
mode-0600 rowref sidecar are recorded in the
[Psy-Insight binding report](../../ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/psy-insight-exact-binding-20261019/report.json)
and the [source-locator audit](execution-2026-10-19/source-locator-public-metadata-audit-2026-10-19.md).
Next, reconcile the 155 unmatched candidate rows against the repair overlay
and exact source turns; keep generated continuations separately labeled and
never promote similarity-only matches. This establishes technical lineage
only; source data rights and downstream training/redistribution permission
remain unresolved.

#### 2026-10-19 crisis benchmark and DSM public row bindings

A pinned public-source join against the current 190,244-row gold candidate
matches 1,406/1,522 `crisis_benchmark` rows by exact ordered non-system adapter
projection (1,370 unique, 36 ambiguous), 22 normalized-only, and leaves 94
unmatched. All 116 `dsm_vector_space` rows match the pinned public repository's
adapter projection, but each has two possible upstream rows, so all remain
ambiguous. Neither family has a full current adapter-render match including
system prompt. The crisis source is an evaluation benchmark; DSM's adapter
originally reads a private S3 cache. These findings establish content
correspondence, not licensing, suitability, privacy, or provider-transfer
permission. Private hash-only sidecars preserve all duplicate matches. See the
[public source binding summary](execution-2026-10-19/public-source-row-binding-summary.md)
and [private reports](../../ai/data/curated/recovery/gold-20261017/private-source-public-row-bindings-20261019/).

#### 2026-10-19 private source cache access check

The project has a configured `whitebat:` rclone remote. Its redacted
configuration identifies Civo Object Storage at `objectstore.nyc1.civo.com`
(region `nyc1`). Read-only listing of the declared ingestion prefixes failed
with HTTP 403 `UserSuspended`; the remote exists, but the configured storage
account currently denies access. This leaves private-cache source manifests
unavailable through that account and does not prove the objects are missing.
The exact operation to resume private-source lineage is to restore Civo account
access or use the authorized alternate remote, then list only the recorded
MentalChat16K/PsyEval prefixes. The current AWS account bucket check remains
separate and did not find the `whitebat:` bucket. See the [source-locator
audit](execution-2026-10-19/source-locator-public-metadata-audit-2026-10-19.md).


#### 2026-10-19 ESConv and PsyDial origin binding

Pinned primary-source adapter joins now bind the current candidate's 892 PsyDial rows (891 unique upstream records, one duplicate-text ambiguity) and 13 ESConv rows uniquely; 16 additional ESConv rows match only under normalization and 863 remain unmatched. PsyDial matches resolve to D101; the adapter-declared D4/D1 files do not project records under its current schema. These are transcript-turn lineage checks with system prompts excluded, not whole-record identity or rights clearance. The hash-only row locator sidecar and source/adapter hashes are private at [the audit report](../../ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/esconv-psydial-row-binding-2026-10-19/audit-report.json); source-locator findings are in [the lineage audit](execution-2026-10-19/source-locator-public-metadata-audit-2026-10-19.md). The 863 unmatched ESConv rows are the next concrete lineage target; do not promote normalized matches to exact.

#### 2026-10-19 latest-checkpoint held-out evaluation

Completed attempts against all 120 frozen held-out cases using v1 LoRA v116 and
v2 LoRA v114, each paired with the W&B base model. The eight base-arm errors in
each run were `ToolRoundLimitExceeded` on the same `resource_compare` cases at
the two-round cap; both manifests therefore say `incomplete` although all 120
cases were recorded. Retry jobs now rerun only those eight pairs at a four-round
cap. The decisive finding is the SFT output: each adapter returned the exact
same three-character response on all 120 distinct cases, with zero tool calls;
the per-case response hashes are identical between v1 and v2. These checkpoints
are not usable for the agent-tool task. The deterministic synthetic-state
checks also failed all SFT tool-status, response-content, and memory-value
checks; they are diagnostics, not clinical quality or safety validation.
Estimated inference costs were $0.10073925 for v1 and $0.09822975 for v2;
actual billing/credit consumption is not exposed in result records. See the
[full evaluation report](execution-2026-10-18/results/latest-checkpoint-heldout-120-evaluation-20261019.md)
and private per-case files in its linked result directories.

The four-round diagnostic retries on the same eight cases completed: all 16
calls succeeded, but both SFT checkpoints again emitted one identical response
body across the eight prompts (24 completion tokens per checkpoint); neither
base nor SFT issued explicit tool calls. This confirms the SFT output collapse
is not caused by the two-round cap. See the detailed [120-case report](execution-2026-10-18/results/latest-checkpoint-heldout-120-evaluation-20261019.md)
and linked retry manifests. Do not use v1/v2 as target-task candidates until
the collapsed output and training/inference serialization are diagnosed.

#### 2026-10-19 18:46 UTC checkpoint stream recheck after cleanup

Direct W&B Artifact API reads at 18:46 UTC confirm the user’s observation:
checkpoint uploads continued during artifact cleanup. v1 has LoRA and
train-state v118 at 59,500 batches; v2 has both at v116 / 58,500 batches.
All four artifacts were downloaded and integrity-checked by the rolling local
backup processes; their private latest manifests were refreshed by 18:45 UTC.
The current W&B API reports 37 retained versions in each collection (v1 LoRA
and state v82–v118; v2 LoRA and state v80–v116). This is the active checkpoint
stream, not a list of the other artifacts the user deleted. W&B exposes neither
the deletion audit nor account quota through the queried endpoints, so this
does not identify the deleted objects or prove quota reclamation. Keep these
four active collections; clean up only after matching actual UI items to the
inventory and preserving a verified local copy. The v4 full-corpus job
remains PENDING as of 18:46 UTC, with no error field; its reason has not yet
been established. The two older jobs still report RUNNING, with status
`updated_at` timestamps stale, while their artifact streams demonstrably
advance.

#### 2026-10-19 Adaption catalog and workflow requalification

An authenticated read-only refresh confirms Qwen 3.6 remains available for
SFT/DPO LoRA; the succeeded 11,192-row `arc-run2-train-v1` dataset and two
successful downloadable historical runs remain visible. A fresh, non-launching
SFT recommendation returned one-epoch LoRA settings and no price or credit
estimate. The 418-row `train` dataset remains `awaiting_input`. The v4 corpus
(171,261 train rows) is not uploaded or schema-qualified with Adaption. No
credit balance, expiry, exact job coverage, or hosted inference endpoint is
exposed. Accordingly, Adaption SFT capability and export precedent are
confirmed, but a new v4 run, DPO, cost coverage, and inference evaluation are
not qualified. See the dated
[Adaption qualification refresh](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md)
and its machine-readable [evidence](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.json).

#### 2026-10-19 Adaption credit and v4 route follow-up (19:19 UTC)

The current connector exposes no account balance, billing history, AutoScientist
cost estimate, or inference method. Public Adaption FAQ documentation says
unused credits do not expire and monthly credits accumulate, but the actual
organization balance and a Qwen 3.6 training quote/coverage remain unverified.
The official dataset API supports JSONL file upload in raw mode with `prompt`
and `completion` columns; AutoScientist accepts raw `chat` or `instruction`
format. The frozen v4 payload is `messages`-only JSONL, so convert locally to
prompt-history/completion-target records before upload. Its verified train
partition has 171,261 dialogues and 534,162 assistant targets, exceeding the
documented SFT row floor. No upload was made, so provider-side acceptance is
not verified. No Adaption-hosted inference route appears in the checked tool
inventory or API reference; export and serve through a separately qualified
matching-base runtime. A separate hash audit resolved the apparent v4
metadata inconsistency: `10d05ac9…` is the canonical-JSON hash recorded in
`metadata.json`; `a4b0507f…` is the raw-file hash recorded by the freeze and
launcher state. Both identify the same manifest, and payload hashes agree.
See the [W&B v4 hash reconciliation](execution-2026-10-19/wandb-v4-manifest-hash-reconciliation-2026-10-19.md).
Details and official references are in the dated [Adaption qualification
refresh](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md).

#### 2026-10-19 mental_health_multiagent public repository comparison

Compared all 5,606 current candidate rows labeled `mental_health_multiagent`
with adapter-shaped conversations from 8,012 JSON files in public
`mithatco/mental_health_multiagent` at commit
`3473e6afa3b8da9a2dd8f5c71ea22ea60a0b4099`. Exact ordered non-system
role/content hashes bound 24 rows uniquely; 5,582 were unmatched and none
ambiguous. The adapter's declared GitHub owner/path differs from this public
repository, and its source locator is a private S3 cache that returned
`UserSuspended`. Therefore these 24 correspondences do not establish that the
public files are the candidate's actual source objects. Rights, privacy,
consent, and provider-transfer status remain unresolved. No candidate or
release data changed. Details and the private hash-only rowrefs are in the
[source binding summary](execution-2026-10-19/public-source-row-binding-summary.md)
and [private report](../../ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/mental-health-multiagent-public-repo-row-binding-2026-10-19/binding-report.json).

#### 2026-10-19 KokoroChat official-source comparison

An exact adapter-shaped join against all 6,589 JSON dialogues at the official
`UEC-InabaLab/KokoroChat` commit
`fd1a4a49c30ff32dcbe01d9ab6982293c6b65071` matched 18/4,615 candidate rows
uniquely; 4,597 did not match and none were ambiguous. The adapter's private
S3 cache is inaccessible (`UserSuspended`), so public content matches do not
prove the cached source revision. The project declares CC BY-NC-ND 4.0; no
commercial or derivative-training rights are presumed. Other rights, privacy,
consent, clinical quality, and provider-transfer status remain unresolved.
No candidate/release rows changed. See the [source binding summary]
(execution-2026-10-19/public-source-row-binding-summary.md) and [private
hash-only report](../../ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/kokorochat-official-public-row-binding-2026-10-19/binding-report.json).

#### 2026-10-19 18:52 UTC exact storage candidates and continuing checkpoints

The live W&B collections advanced again during this audit: v1 LoRA and
train-state reached v119 / 60,000 batches at 18:52; v2 remains v117 / 59,000.
The backup caught v2 v117 and v1 v119 by 18:55, with each run's latest two
LoRA and train-state versions hash/size verified locally. The 1.06 GB train-state artifact is about
nine times the 118 MB LoRA artifact, and one new train-state version is written
per 500 batches. The active checkpoint stream therefore explains substantial
storage growth while runs still succeed.

If the cleanup UI showed these exact active `train-state` collections, versions
v1 v82–v117 (36 unaliased internal versions) and v2 v80–v115 (36) are
conditional cleanup candidates while preserving each job's newest two
resume-states. Their nominal size is 76.35 GB total. This audit cannot match
the user's deletions to those candidates: the W&B API does not expose deletion
history, and the user may have been deleting other artifact types or
collections. Physical quota and reclaimed capacity are also unknown. The exact
ranges and rationale are in the [W&B storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).
The Browserbase session reached the project but was logged out, so it did not
show which UI entries were selected for deletion; the user was sent that tab
to sign in if they want an exact UI-to-API match.

At 19:22 UTC, a direct comparison against the 16:26 version snapshot found all
22 previously visible versions still present in each of the four active
checkpoint collections, plus 19 new versions per collection. Current heads are
v1 v122 / 61,500 batches and v2 v120 / 60,500 batches; both LoRA and train-state
mirrors are backed up through those versions. This proves no deletions from the
active streams after 16:26, so the user's cleanup items were elsewhere in the
project or were deleted earlier. The [retention reconciliation](execution-2026-10-19/active-checkpoint-retention-reconciliation-2026-10-19T1922Z.json)
records the exact version join; other collection deletion history remains
unavailable.

The later-checkpoint paired refresh also finished: v1 v118 (59,500 batches)
and v2 v117 (59,000 batches) each returned one identical SFT response across
all eight retried prompts, with zero tool calls and 24 completion tokens; all
16 calls per paired run succeeded. Estimated usage was about $0.01 per run.
The v1 v119 checkpoint at 60,000 batches was also tested: it repeats the same
one-body/24-token SFT result with zero tool calls; all 16 paired calls
succeeded and estimated usage was $0.0098905. Thus the collapse persists in
the newest checkpoint. Detailed manifests are linked in the [evaluation report](execution-2026-10-18/results/latest-checkpoint-heldout-120-evaluation-20261019.md).

At 19:27 UTC I re-enumerated all visible W&B collections and versions after
the user clarified that checkpoint creation was occurring while they deleted
items. The full private inventory contains 285 collections and 443 versions;
compared with 15:45, the visible count grew by 96 and logical artifact-version
size grew by 55.91 GB. `lora` grew from 44 to 92 versions, `train-state` from
40 to 87, and `dataset` from 5 to 6; the other five artifact types were flat.
The two new collections are the v4 dataset and its base-LoRA artifact. These
are net type-level counts; checkpoint growth could mask deletion of other
versions. W&B's current API has no deletion history or physical quota meter, so
the exact UI items remain unidentified. A fresh dependency check found 79
unaliased active-job train-state versions (v1 v82–v120, v2 v80–v119) with zero
`used_by()` run references. They total 83,772,762,011 nominal bytes (about
78.04 GiB). The newest two versions per job remain both remote and locally
mirrored. These are the current specific UI cleanup candidates; delete only
those versions if reclaiming space, and preserve all LoRA artifacts, datasets,
aliases, and the newest two train-state checkpoints per job. Logical size is
not guaranteed physical quota reclamation and the active jobs continue writing
checkpoints. The [private cleanup audit](execution-2026-10-19/active-train-state-cleanup-audit-2026-10-19T1927Z.json)
and [full inventory](execution-2026-10-19/wandb-artifact-inventory-2026-10-19T1926Z.json)
are mode 0600. No deletion was made by this audit.

#### 2026-10-19 latest W&B checkpoint paired evaluation

I ran the same bounded eight-case synthetic resource-comparison set against
the latest mirrored adapters, using the W&B base endpoint for the paired
baseline. v1 v123 and v2 v121 each completed 16/16 endpoint calls with no
provider errors. Estimated usage was $0.01145825 and $0.0108315 respectively,
each under the configured $0.10 cap; actual billed credits were not returned.
Both SFT arms produced one identical three-character response across all eight
cases, 24 completion tokens total, zero tool calls, and failed all 24
deterministic state assertions. This repeats the collapse seen at prior
checkpoints after approximately 62,000/61,000 batches. The base arms produced
six/eight distinct responses and also made no tools on this resource-only
subset. These synthetic checks are not validated clinical-quality or safety
metrics. The finding warrants inspecting target formatting and response
extraction before more broad inference spend. The [private summary](execution-2026-10-19/latest-checkpoint-evals/report.md)
contains the assessment; per-case raw model output remains in mode-0600 files.

#### 2026-10-19 KokoroChat contiguous exact-turn follow-up

Checked every candidate non-system dialogue as an exact contiguous turn
sequence against all 6,589 official public conversations. The 18 exact hits
were the same 18 full-sequence matches already reported; there were no
additional partial-contiguous hits among the remaining 4,597 rows. The private
report and hash-only rowrefs are `contiguous-binding-report.json` and
`candidate-to-upstream-contiguous-rowrefs.jsonl` under
`../../ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/kokorochat-official-public-row-binding-2026-10-19/`.
As above, this public comparison does not identify the inaccessible private
S3 cache revision or settle rights, privacy, or training eligibility.

#### 2026-10-19 Fireworks Muse Glimmer full-corpus Serverless SFT

The Fireworks account's read-only plan at 19:00:43 UTC confirmed the Muse
Glimmer 30B promotional LoRA SFT window active through November 30 Pacific.
A full one-epoch Serverless Training API job is now running against all 171,261
rows in the frozen v4 train partition. Run ID:
`pixelated-v4-fireworks-20261019-r8-full`; Fireworks session
`ts-98142570058847bd9725b827fe101e23`; SDK run
`run-984e7572ea71404eaf8a44231b9f771b`. The job uses rank 8, batch 16, learning
rate `1e-4`, and no dataset upload. The serverless launcher was configured with
`--no-promote`; it creates no persistent model or dedicated deployment, and
its sampler checkpoint/weights will be unavailable after the session closes.

The exact group-disjoint v4 validation partition supplies a deterministic
120-row hash-selected paired evaluation. The Muse renderer produced 32,694
prompt tokens per arm; completions are capped at 512 tokens. The conservative
maximum at Fireworks' current published sampling rates is $0.727815 estimated
for both arms; training is $0 promotional and does not cover sampling. W&B
credits do not transfer to Fireworks. The base arm completed with 32,694 prompt
tokens and 49,674 sampled tokens (about $0.306489 estimated), exact match 0.0,
94 outputs hitting the completion cap, and 85 empty visible-text parses. Treat
exact match as a weak diagnostic for conversational replies. Base predictions
are private and mode 0600; no clinical text is copied into the report.

The first 16 of 10,704 planned optimizer steps were logged (step 1 loss 2.3568;
step 13 loss 0.9627); training remains active. Recent optimizer steps take about
35–58 seconds each, implying roughly 4.3–7.2 days for the remaining 10,688 at
that early flat rate. This is a rough extrapolation, not a service completion
estimate; there are no current training/API errors. The exact row selection, trainer overflow
semantics, preflight, plan, status, and private output paths are in the [Fireworks
run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

#### 2026-10-19 19:28 UTC Fireworks SFT status check

The launcher advanced from step 16 to step 17 (loss 1.0048) by 19:28:22Z,
54 seconds after the prior stdout timestamp. The apparent pause was not a stall;
this matches the observed 35–58 second step cadence. A read-only query to the
Fireworks Training Session checkpoint API returned only the base sampler
checkpoint created at 19:10:40Z. This custom loop writes no periodic optimizer
checkpoints: it creates a tuned sampler snapshot only after all training steps
for evaluation. The serverless session API does not expose optimizer-step
progress, so continue observing the private local launch output. PID 518909
remains active; do not restart it. At the early measured cadence, 10,687
remaining steps extrapolate to about 4.3–7.2 days, not a vendor ETA. The
[private Fireworks report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md)
has the current status and limitations.

At 19:30Z the Fireworks loop reached step 19/10,704 (loss 1.5802) and remains
active. Recent step intervals range about 35–66 seconds, implying a highly
uncertain 4.3–7.9 day linear extrapolation for the remaining 10,685 steps. The
private report reflects this snapshot.

At 19:32Z the loop reached step 22/10,704 (loss 0.998); steps 20–22 arrived
at uneven intervals, about 52–69 seconds. The earliest observed 35–69s interval
range gives a very uncertain 4.3–8.5 day extrapolation for 10,682 remaining
steps. No inference/evaluation has started after training; the fixed paired
suite will run when the launcher reaches its post-training sampler phase.

At 19:38Z the loop reached step 28/10,704 (loss 2.3723); the observed recent
step interval range is now about 35–79s. A linear estimate over that wide range
would put 10,676 remaining steps at roughly 4.3–9.9 days, with substantial
uncertainty from this small sample. The private run report carries the updated
snapshot.

#### 2026-10-19 19:39 UTC W&B storage recheck during cleanup

I compared every visible artifact-version key against the 19:27 inventory.
All 443 previously visible versions remain present; four new versions appeared:
v1 LoRA/state v123 and v2 LoRA/state v122. This confirms the user's observation
that checkpoints were being created while storage cleanup was underway, while
showing no deletion from the visible `wutang/pixelated-empathy-kan28` inventory
between these snapshots. Deletion may have affected another project/surface or
preceded the earlier snapshot; W&B's API exposes no deletion log or current
physical quota meter. No artifact was deleted by this audit. See the updated
[storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md)
and mode-0600 [19:39 inventory](execution-2026-10-19/wandb-artifact-inventory-2026-10-19T1939Z.json).

At 19:40:04Z the Fireworks run reached step 30/10,704 (loss 1.0328); PID
518909 remains active. The six most recent observed intervals were 79, 53, 41,
53, 54, and 59 seconds (mean 56.5s, median 53.5s). At that mean, 10,674
remaining steps imply about 7.0 days; the 41–79 second interval range implies
5.1–9.8 days, with high uncertainty. No new errors appeared; stderr contains
the existing nonfatal model-type and telemetry warnings. The paired evaluation
has not started and runs after training. See the private [run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

#### 2026-10-19 19:43 UTC W&B collapse target audit

The two latest-checkpoint paired evaluations showed the same failure on both
W&B adapters: each produced the exact same three-character response on all
eight cases. An aggregate-only audit of the uploaded v1, v2, and v4 W&B
training payloads found 22,690 exact `BPD` assistant targets in each payload
(4.26% of assistant targets; 13.26% of training rows). Every one maps uniquely
by normalized-message hash to source `reddit_mental_nlp`, task
`symptom_classification`, and diagnostic tag
`borderline_personality_disorder`. Each payload also has 26,389 nonempty
assistant targets of at most three characters (~4.94–4.96%). The v4 rebuild
retained the same target distribution, so this is a concrete candidate cause
for output collapse, though not proof of causation. Because the Fireworks run
also uses v4, it contains these targets too. Preserve the frozen corpus and
test this in a separate controlled ablation: verify provider-ingested target
counts/loss masking, compare task-stratified evaluations, then vary weighting
or mask only the classification assistant targets while retaining the
unaltered full-corpus release. Aggregate-only evidence is in
`execution-2026-10-18/results/wandb-full-corpus-collapse-diagnosis.json` and
the mode-0600 private report under
`../../ai/data/curated/recovery/gold-20261017/private-bpd-target-diagnostic-20261019/aggregate.json`.

#### 2026-10-19 19:43 UTC Empath/MentalChat16K lineage transfer into v4

The five upstream files at the pinned public Hugging Face revisions were
downloaded to `/tmp`; byte counts and SHA-256 values matched the origin-binding
manifest exactly. The prior row-reference sidecars were joined to v4's internal
manifest by full candidate-row SHA-256. All 35,977 Empath rows and all 11,135
MentalChat16K rows from the 190,139-row predecessor remain byte-identical in
the 190,244-row v4 candidate. This transfers the existing source-row evidence
to v4 without approximate matching: Empath has 12,042 unique exact sequence
matches, 15,249 ambiguous, and 8,686 unmatched; MentalChat16K has 1,090 unique,
17 ambiguous, and 10,028 unmatched. The full non-system sequence matches the
pinned adapter projection for 27,287 Empath and 1,107 MentalChat16K rows. This
does not establish full-record adapter equality or resolve rights/privacy.
See the [binding report](execution-2026-10-19/empath-mentalchat16k-origin-binding-2026-10-19.md)
and corrected [local presence audit](execution-2026-10-19/local-upstream-source-presence-audit-2026-10-19.md).

At 19:42:54Z Fireworks reached step 34/10,704 (loss 0.7213), with a 53-second
interval from step 33. The session remains active and no new errors appeared.

At 19:44:32Z Fireworks reached step 35/10,704 (loss 0.7123); this step took
about 98 seconds, showing substantial per-step variation. Across the latest
three individually timed intervals (61, 53, and 98 seconds), the mean projects
about 8.8 days for the remaining 10,669 steps; the observed range projects
6.5–12.1 days. This is a rough linear estimate, not a provider ETA. PID 518909
remains active, and evaluation has not started.

The rolling local W&B mirrors now contain v1 adapter and train-state v124
(62,500 batches) and v2 adapter and train-state v122 (61,500 batches). The
latest train-state copies each pass SHA-256 verification for all 11 files. The
Training API still reports v1/v2 RUNNING and v4 PENDING; it exposes no numeric
progress or error message for those jobs. The 19:39 watcher snapshot records
these states and artifact versions, with the next watcher poll due on its
five-minute cadence.

#### 2026-10-19 20:31 UTC latest W&B checkpoint held-out comparison

Completed paired 120-case comparisons of v1 adapter v127 and v2 adapter v125 against the same W&B base model, using the frozen held-out set SHA `adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`. Each SFT arm completed 120/120 calls, but returned the same three-letter classification label (`BPD`) on all cases, made zero tool calls, and passed only 60/240 deterministic synthetic assertions. This confirms severe response collapse at both tested heads; these assertions are diagnostic only and are not a clinical quality or safety evaluation.

Base completed 111/120 calls for v1 and 112/120 for v2. All 17 failed base calls hit the configured two-round tool limit. Estimated combined usage was $0.19540925, with actual billing not reported. The detailed aggregate report and exact run IDs are in [latest-checkpoint-evals/report.md](execution-2026-10-19/latest-checkpoint-evals/report.md); raw outputs remain private under `ai/training/output/`.

At 20:31 UTC the Fireworks Muse Glimmer run remained active at step 85/10,704; it creates no periodic optimizer checkpoints and its tuned sampler snapshot is only produced after training. The W&B full-corpus v1/v2 training jobs and their local checkpoint mirrors also remain active. No artifact cleanup was performed by these evaluations.

#### 2026-10-19 20:54 UTC storage-growth diagnosis and live deletion candidates

The owner was correct that W&B checkpoints were being created while artifacts
were deleted. A direct authenticated project `storageBytes` query measured
30,167,440,389 B at 15:07 UTC and 101,403,428,801 B at 20:51 UTC, +71.24 GB
in 5h44m (about 12.4 GB/hour). Each active job writes a 1,060,414,709-byte
train-state artifact about every ten minutes, plus a 117,843,308-byte LoRA;
the two train-state streams can add about 12.7 GB/hour. Current heads at 20:53
were v1 v131 and v2 v130. The current GraphQL field does not reveal plan quota,
rolling billable usage, or physical reclamation.

A fresh read-only audit retained the two newest train-state versions for each
active job and checked every older visible version's aliases and dependencies.
The 97 alias-free, zero-dependency candidates are v2 v80–v128 and v1 v82–v129,
102.86 GB logical. Keep v2 v129/v130 and v1 v130/v131 as recent recovery
points; keep all LoRAs for comparisons. Exact per-version checks are in
[`live train-state candidate audit`](execution-2026-10-19/wandb-live-train-state-delete-candidates-2026-10-19T2051Z.json)
and the [triage report](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).
The estimate is logical artifact size and does not guarantee physical space
reclaimed. The agent made no deletion.

The current W&B v4 baseline job (system messages stripped) still reports PENDING with no start
time or provider error; v1/v2 report RUNNING. Fresh latest-head evaluations
were launched on the frozen 120-case first-party synthetic held-out suite for
v1 v131 and v2 v129. They are in progress; results will be added only after
both complete. Fireworks was at step 106/10,704 at 20:53 UTC, roughly one
step/minute in the latest interval.

#### 2026-10-19 20:36 UTC storage and fresh checkpoint comparisons

The latest full W&B project Artifact API inventory found 471 versions across 285 collections: all 461 versions from the 20:12 snapshot remain visible, with 10 new versions limited to the active v1/v2 LoRA and train-state collections. This still does not identify the user's deleted items and supports the possibility that their cleanup view is a separate storage surface. Browserbase session startup returned `Session terminated` again. See [storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md) and its private-permission inventory.

At 20:36 UTC, direct Training API status remained v1/v2 `RUNNING`, v4 `PENDING` without a reason, and the Fireworks run active at step 90/10,704. New four-round paired evaluations are testing v1 v129 and v2 v127 on the frozen held-out 120-case set against the W&B base. Each run's estimated worst-case use is $1.3824, below its configured $1.50 hard cap; actual billed usage is unavailable. Both comparisons were still running at 60/240 and 58/240 arm-calls respectively.

#### 2026-10-19 20:43 UTC newer-head 120-case comparison

The four-round paired comparisons completed for v1 v129 and v2 v127. All 240 calls per comparison succeeded. Base produced 88/83 unique normalized responses and passed 196/240 and 186/240 deterministic synthetic assertions, respectively; both base arms made zero recorded tool calls on this suite. SFT collapse persisted: v1 v129 returned one identical seven-character normalized response across all 120 cases, and v2 v127 returned `BPD` across all 120. Each SFT arm made zero tool calls and passed 60/240 assertions. These metrics are diagnostic and not clinically validated.

Estimated usage was $0.1091435 (v1) and $0.11133425 (v2), $0.22047775 combined; actual billed usage was not reported. The run IDs, configs, and aggregate comparison are recorded in [latest-checkpoint-evals/report.md](execution-2026-10-19/latest-checkpoint-evals/report.md). The four-round limit eliminated all base errors from the previous two-round run.

#### 2026-10-19 20:44 UTC storage size and safe-candidate reconciliation

The 20:35 W&B API snapshot sums to 120.43 GB in logical artifact-version sizes (106.61 GB train-state, 12.91 GB LoRA, 0.91 GB dataset). All 79 old active-job train-state versions previously checked as alias-free and dependency-free are still listed; together they account for 83.77 GB logical. The 19:27 audit retained the two newest state versions per active collection. This is the strongest project-level cleanup candidate set, but logical bytes do not guarantee physical quota reclamation. Exact version identities and caveats are in the [storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md) and its linked audit. No deletion was made by the agent.

The current paired v1 v129/v2 v127 held-out evaluations completed cleanly at 20:43; results are in the latest-checkpoint report. Fireworks continued to step 97/10,704 at 20:44 UTC with no reported training error. W&B mirrored heads were v1 v130 and v2 v129 at the latest 20:41 watcher snapshot.

#### 2026-10-19 20:57 UTC storage meter and newest-checkpoint evaluation progress

A fresh authenticated W&B GraphQL project-storage query at 20:56:53 UTC returned 101,403,458,209 B, only 29,408 B above the 20:51 reading. The earlier 12.4 GB/hour increase therefore did not continue across this five-minute interval. This is compatible with the owner's cleanup, but the project meter may lag and the Artifact API inventory was not refreshed in this check, so reclaimed physical space is not yet proven. No artifacts were modified or deleted by the agent. See the [storage triage report](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).

The newer 120-case paired evaluations remain active and all calls recorded so far succeeded. At 20:56 UTC, v1 checkpoint v131 had 73/120 base and 73/120 SFT calls recorded; the SFT arm had emitted 292 completion tokens total (four per example), no tool calls, and estimated combined spend was $0.0721. v2 checkpoint v129 had 54/120 base and 54/120 SFT calls; its SFT arm had emitted 216 completion tokens (four per example), no tool calls, and estimated combined spend was $0.0546. These partial metrics point to the same collapsed-response failure as earlier checkpoints, but the full paired assertions and totals will be recorded after completion. Fireworks reported step 109/10,704 at 20:56 UTC, still active.

At 20:58 UTC, direct W&B Training API reads still reported v1 and v2 as `RUNNING`, with no progress field, and the v4 baseline job (system messages stripped) `PENDING`, without an error or pending reason. The two newest-head paired evaluations remain active: v1 v131 has 92/120 base and 91/120 SFT calls; v2 v129 has 69/120 on each arm. All recorded calls succeeded. The SFT arms emitted 364 and 276 completion tokens respectively (four per case) and made zero tool calls, reinforcing the response-collapse diagnostic. Fireworks step 111/10,704 was logged at 20:58 UTC with loss 0.9922; the configured gradient clipping applied without error. The active evaluations will be summarized with full assertions and final estimated usage once complete.

#### 2026-10-19 21:03 UTC Adaption v4 experiment launched

The frozen W&B train payload was unrolled for Adaption raw SFT. The structural check found 11,504 of 171,261 dialogues start with an assistant prefix; consistent with the project's existing unroll convention, these turns are retained as context and not treated as targets. The conversion emits 522,658 eligible assistant targets, not 534,162. Its mode-0600 manifest and JSONL are in `ai/training/output/adaption_v4_unrolled_20261019/`; the source payload SHA-256 is unchanged (`60841fbc...e37f20`) and the 2,136,003,932-byte output SHA-256 is `bec73fb3e8ccb54e2c3f404860d7b4264aba7e59f2602473f9046eb720d3cd37`.

Adaption accepted the exact file in raw mode with no augmentation and reported dataset ready: `21f6d03f-5f56-41be-9070-14c8fccbf442` (`pixelated-v4-train-unrolled-20261019`, 522,658 rows; provider-normalized columns `original_prompt` and `original_completion`). The non-launching Qwen3.6 recommendation returned 1-epoch LoRA, rank/alpha 8, q/v projections, LR 0.0003, batch `max`, and `train_on_inputs=false`. A one-iteration instruction AutoScientist run with those settings and no augmentation is now running: `7b859acc-f325-4022-92c7-b1a1ff40c2c3`, `max_iterations=1`. The first status poll showed 0/1 iterations, no error, and no download yet. The first request used pre-normalized column names and was rejected before job creation; the retry used Adaption's actual names. The connector still exposes no balance or training-cost quote, so the single iteration is capped by count but not by a verified credit-dollar amount. See the [Adaption qualification refresh](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md) and its private local manifest.

The fresh v1 v131 and v2 v129 paired evaluations completed with 240/240 successful calls each on the frozen 120-case synthetic held-out suite. Base deterministic state checks passed 197/240 (v1) and 194/240 (v2). Each SFT arm passed 60/240 and returned one identical normalized response across all 120 cases, four completion tokens per example, and zero tool calls. Each base arm also made zero tool calls. Estimated inference usage was $0.109462 and $0.1091605, $0.2186225 combined; actual billed usage was not exposed. The $1.50 configured cap was not approached. This confirms response collapse persists at both newest retained checkpoints. These checks are synthetic diagnostics only. Full results and hashes are in the [latest-checkpoint evaluation report](execution-2026-10-19/latest-checkpoint-evals/report.md); outputs remain access-restricted.

#### 2026-10-19 21:04 UTC W&B checkpoint creation and storage meter

The private rolling-backup manifest at 21:03:41 UTC now identifies v1 train-state v132 (66,500 completed batches) and v2 v131 (66,000 batches), both 1,060,414,709 B; the watcher still sees both jobs `RUNNING`. The 21:03:47 UTC GraphQL project storage meter is 103,288,803,197 B, up 1,885,344,988 B from the 20:56:53 reading. The two new train-state versions total 2,120,829,418 logical bytes. This directly confirms continued checkpoint creation during the cleanup window and is consistent with it overtaking some cleanup, though W&B's meter does not reveal physical reclamation or identify deleted items. See the [storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md); no artifact was modified or deleted by the agent.

#### 2026-10-19 21:37 UTC live W&B adapter inventory and paired evaluations

The user's observation that checkpoints were still being created during
artifact cleanup was correct. A direct read-only W&B collection query at 21:30
found inference adapters v1 v135 (68,000 completed batches) and v2 v134
(67,500). Separate train-state collections had their own publication/version
sequence; at 21:25 the local rolling mirror held v1 train-state v135 and v2
train-state v133. These collections must not be conflated when identifying
inference-ready checkpoints.

Both v1 v135 and v2 v134 completed paired evaluations against the W&B Qwen3.6
base model on the frozen 120-case synthetic suite (hash
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`). All 240
calls per comparison succeeded. The SFT arms each returned one repeated
normalized response across 120 cases, made zero tool calls, and passed 60/240
deterministic state checks. The base arms passed 189/240 and 195/240 checks and
produced 87 and 92 unique normalized responses. Estimated inference usage was
$0.109133 and $0.1088255 ($0.2179585 combined); actual billing was not returned.
Each comparison had a $1.50 cap and a $1.3824 preflight maximum. These synthetic
diagnostics show the same adapter response-collapse failure, not clinical
quality or safety.

A direct artifact refresh at 21:37:30 UTC found that v1 v136 (68,500 batches,
published 21:33:46 UTC) had arrived while the v1 v135 evaluation was running;
v2 v134 remained newest at that refresh. A paired v1 v136 evaluation has now
completed on the same frozen suite with 240/240 successful calls. The SFT arm
again returned one repeated normalized answer, made zero tool calls, and passed
60/240 checks; base passed 197/240 with 87 unique normalized responses and 144
successful simulator tool actions. Estimated usage was $0.109961; actual
billing was unavailable. Run ID:
`wandb-latest-v1-v136-vs-base-heldout120-20261019T2138Z`.

A further direct adapter refresh at 21:44:42 UTC found v1 v137 (69,000 batches,
published 21:43:07 UTC) and v2 v135 (68,000 batches, published 21:38:33 UTC).
Their same-suite paired evaluations completed with 240/240 successful calls
each. Both SFT arms again returned one repeated normalized response, made zero
tool calls, and passed 60/240 checks. Base passed 189/240 (v1) and 190/240
(v2). Estimated usage was $0.1115415 and $0.109696 ($0.2212375 combined);
actual billing was unavailable.

At 21:53:43 UTC, the direct inventory found v1 v138 (69,500 batches,
published 21:52:24 UTC) and v2 v136 (68,500 batches, published 21:47:45 UTC).
These arrived while v1 v137/v2 v135 were running and remain untested. After
multiple adjacent heads repeated the same collapse, further inference work
should shift to training/data diagnostics rather than each new 500-batch
artifact. Exact publication cutoffs are in the [paired evaluation report](execution-2026-10-19/latest-checkpoint-evals/report.md).

Two local launch attempts before the successful runs failed before sending
requests, first due to selecting the adjacent eight-case file and then because
the corrected process lacked `WANDB_API_KEY`; they recorded zero successful
calls and zero usage. The retry sourced the existing local credential
environment and used the frozen 120-case suite.

See the [checkpoint comparison report](execution-2026-10-19/latest-checkpoint-evals/report.md)
for both completed pairs, manifests, and private result paths. No W&B artifacts
were modified or deleted by these reads or evaluations.

The 21:40:49 UTC GraphQL project meter was 110,830,208,881 B, up
4,713,388,202 B from 21:19:01 UTC (about 12.97 decimal GB/hour). It still does
not expose the account quota or physical reclamation. A direct adapter query at
21:37:30 showed v1 v136 and v2 v134 as the newest inference artifacts; the v1
v136 comparison completed with the same response-collapse finding. At 21:25, the private train-state mirror showed
v1 v135 and v2 v133, confirming the distinct artifact streams. The v1/v2 jobs
remain `RUNNING`; the v4 system-preserving job remains `PENDING`. Fireworks
reached step 154/10,704 at 21:40 UTC with no reported error. The exact storage
and adapter snapshot is [here](execution-2026-10-19/wandb-live-storage-adapter-refresh-20261019T2140Z.json);
updated storage interpretation is in the [triage report](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).

At 21:53:43 UTC, project `storageBytes` reached 112,715,553,869 B, another
1,885,344,988 B above the 21:40:49 UTC reading (about 8.77 decimal GB/hour
over that interval). A direct adapter inventory found v1 v138 and v2 v136,
newer than the latest evaluated heads. See the [21:53 snapshot](execution-2026-10-19/wandb-live-storage-adapter-refresh-20261019T2153Z.json).
The meter still does not expose quota or physical reclamation; no remote
artifacts were modified or deleted by these reads.

#### 2026-10-19 21:08 UTC Adaption download-timeout diagnosis and retry

The first Adaption full-history v4 run (`7b859acc-f325-4022-92c7-b1a1ff40c2c3`) failed at 0/1 iterations with a provider timeout after 60 seconds downloading its 2.14 GB S3 train JSONL; no model was made available. To test that transfer bottleneck while preserving all 522,658 eligible assistant targets, a second raw dataset retains only the latest nine prompt messages. This is an explicit context-window ablation: 288,318 targets omit older history, but no target is dropped. Its 791 MB upload processed successfully as dataset `5cf8efd5-3426-4cc4-b3cc-4d40f7912f9d`. The first no-augmentation Qwen3.6 LoRA instruction iteration (`8d00b26c-de36-452a-abc2-5cd36b76036b`) failed at 0/1 because its structured arrays were sent as `instruction` data and the generated validation JSONL was empty. A corrected `chat` format retry was rate-limited before run creation; Adaption returned a 3,040-second cooldown. Do not retry before that window. Per-run credit usage and account balance remain unavailable. The local private manifest and exact hash are in `ai/training/output/adaption_v4_unrolled_ctx9_20261019/`; the qualification refresh records both attempts.

#### 2026-10-19 21:11 UTC W&B preview terms rechecked (corrected below)

This note incorrectly treated the docs archive and pricing-page redirect as
evidence that the published public-preview/free-training statement was no
longer current. The correction below is authoritative: W&B's published page
continues to state those terms. Account-level billing remains a separate check.

#### 2026-10-19 21:14 UTC exact training-payload delta resolved

Compared each frozen train JSONL row by SHA-256 against the Oct. 18 v1/v2
training artifacts, then joined the v4-only rows to the private source manifest
by exact row hash. Both older payloads are strict subsets of the frozen v4
payload: v1 has 171,121 rows and v4 adds 140; v2 has 171,167 rows and v4 adds
94. The 46 rows present in v2 but absent from v1 map uniquely to 44
Psy-Insight rows and two clinical-book reconstruction rows. The 94 rows v4
adds beyond v2 map uniquely to ARC-corpus sources. Duplicate text hashes do
not cross source labels in these added-row groups. No row present in either
older training payload is absent from v4.

This means the running v1/v2 checkpoints and their collapse evaluations are
not checkpoints trained on the exact v4 frozen payload; they are close earlier
releases. The no-system v4 baseline W&B job `24cc2d06-3ec3-4356-ad3a-179694dd86a7`
is the W&B job bound to v4, but remains `PENDING` without provider error or
progress fields. Fireworks is actively training the v4 171,261-row payload
from SHA `60841fbc8d917de4699d1b41eddddf03fade949496db3e561769f94959e37f20`;
its temporary checkpoint/evaluation remains in progress. These results keep
the old W&B comparisons useful as diagnostics, while preventing them from
being reported as v4 training results.

The independent v4 ARC source audit is now closed: 1,085/1,085 ARC rows bind
to unique archive sessions and canonical-rendered messages, with no missing,
ambiguous, or mismatched rows; all source metadata verdicts are `accept`.
Details and the reproducible audit are in the [v4 ARC lineage binding report](execution-2026-10-19/v4-arc-lineage-binding-2026-10-19.md)
and [dataset freeze report](execution-2026-10-19/dataset-breakaway-freeze-2026-10-19.md).

#### 2026-10-19 21:19 UTC training and comparison refresh

The new paired 120-case comparisons completed for older W&B checkpoints v1
v133 and v2 v131. All 240 calls per checkpoint comparison succeeded. Base
passed 196/240 synthetic state checks; both tuned arms passed 60/240, made no
tool calls, and emitted very short low-diversity outputs. Estimated combined
inference usage was $0.21559125; billed usage remains unreported. The
checkpoint-specific report has scenario totals and run IDs. These are the
October 18 subset-trained jobs, not the v4 checkpoint comparison.

W&B's event stream exposes planned totals of 85,561 gradient steps for v1 and
85,584 for v2. Latest private local mirrors at 21:14 had 67,000 and 66,500
completed batches respectively; both jobs still report `RUNNING` with no
error. At the observed rate of about 48.5 steps/minute over the latest 500-step
interval, roughly 6h20m–6h35m remain if throughput holds. This is a measured
extrapolation, not a provider completion estimate. The v4 job remains
`PENDING`, with no start, error, progress, or events. Fireworks is training
the actual v4 payload and logged step 129/10,704 at 21:18 UTC.

W&B project storage measured 106,116,820,679 B at 21:19:01 UTC, up
2,828,017,482 B from the 21:03:47 reading. Active jobs continue adding
checkpoints, and W&B's project meter does not disclose quota or physical
reclamation. No remote artifacts were modified or deleted by these checks.
The private rolling-backup manifest at 21:03:41 UTC now identifies v1 train-state v132 (66,500 completed batches) and v2 v131 (66,000 batches), both 1,060,414,709 B; the watcher still sees both jobs `RUNNING`. The 21:03:47 UTC GraphQL project storage meter is 103,288,803,197 B, up 1,885,344,988 B from the 20:56:53 reading. The two new train-state versions total 2,120,829,418 logical bytes. This directly confirms continued checkpoint creation during the cleanup window and is consistent with it overtaking some cleanup, though W&B's meter does not reveal physical reclamation or identify deleted items. See the [storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md); no artifact was modified or deleted by the agent.

At 22:09 UTC, W&B's project meter reached 116,486,273,253 B, +3,770,719,384 B
over 15m27s (about 14.64 GB/hour). Direct artifact reads found v1 LoRA and
train-state v139 at 70,000 batches and v2 LoRA and train-state v138 at 69,500;
the jobs report `RUNNING`, while v4 remains `PENDING`. The W&B `/checkpoints`
route still returns only step 0, so it is not the trained-artifact inventory.
Local backup processes remain active. SHA-256 and size verification passed for
all files in the newest local v1/v2 LoRA and resume-state backups (v1 v139, v2
v138; 26 files total); the host had 17 GB free. See the [22:09 snapshot](execution-2026-10-19/wandb-live-storage-adapter-refresh-20261019T2208Z.json)
and [storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).
The v1 v139 paired check was launched at 22:10 UTC with the same frozen
120-case suite, 2,048-token input cap, 512-token response cap, and four
tool-round cap. At 22:18 UTC it had completed 102/120 successful calls per arm
with no errors; results are pending. Config and results are under
`execution-2026-10-19/latest-checkpoint-evals/v1-v139-heldout120*`.

At 22:14 UTC, the fresh train-state audit found 114 unaliased artifacts with
successful zero-dependency checks: v1 v82-v138 and v2 v80-v136. They total
120,887,276,826 B logical; the newest two resume versions per run are excluded.
This is an actionable owner-directed cleanup set, but physical reclaimed space
may differ and older rollback points would be lost. Nothing was deleted. The
mode-0600 version-by-version evidence is in the [22:13 candidate audit](execution-2026-10-19/wandb-live-train-state-delete-candidates-2026-10-19T2213Z.json).
W&B's current latest artifacts are v1 v140 / 70,500 batches and v2 v138 /
69,500; local copies of their adapters and resume states passed size and hash
verification. At 22:18, Fireworks was live at step 191 / 10,704 (latest loss
0.9163); a read-only checkpoint listing found only the starter-base checkpoint,
with no tuned checkpoint yet. At 22:18, v1 v139 inference comparison had 102
successful calls per arm, no errors, and remained in progress. Revalidation
recomputed MentalChat16K's exact binding counts (1,090 unique, 17 ambiguous,
10,028 unmatched), rechecked all 35,977 Empath candidate line hashes against
its private sidecar (12,042 unique, 15,249 ambiguous, 8,686 unmatched), and
re-ran the ARC audit (1,085/1,085 exact canonical matches); no candidate or
sidecar was modified. The first ARC recheck with system Python lacked `pydantic`;
the repository's `ai/.venv` rerun passed. The 22:17:45 Fireworks metric and
22:18 checkpoint listing were obtained from the active launcher and documented
read-only checkpoint API, respectively.

At 22:20 UTC, the v1 v139 paired comparison finished: all 240 calls succeeded.
The SFT adapter returned one unique normalized response for all 120 cases,
made zero tool actions, and passed 60/240 deterministic synthetic checks. The
base returned 88 unique responses, made 148 tool actions, and passed 193/240
checks. Estimated inference usage was $0.110632; W&B did not report actual
billed usage. This repeats the severe collapse at v1 v139 (1,000 batches after
the previously evaluated v1 v137), while v1 v141 is now the newest adapter
and is queued for evaluation. A paired v2 v139-versus-base evaluation started at
22:19 UTC; its first check showed 7/120 calls per arm, all successful. Its
preflight maximum is $1.3824. Synthetic checks are unvalidated diagnostics,
not clinical quality or safety measures.

At 22:27 UTC, Fireworks session PID 518909 remained live at step 203 / 10,704
(loss 1.5292 at 22:27:31.502Z) with no new errors. A fresh read-only
checkpoint-list query still returned only the base sampler checkpoint; no
tuned checkpoint is available to export yet. W&B's rolling backup at
22:24:11 recorded v1 v141 / 71,000 and v2 v139 / 70,000; v1 v141's local
adapter files and recorded SHA-256 values are present. The v1 v141 evaluation
had 5 successful calls per arm and zero failures at its first progress check.

The 22:18:53 UTC rolling-backup manifest confirmed local copies of v1 adapter
and train-state v140 / 70,500 batches and v2 v139 / 70,000. The 22:24:11 UTC
refresh advanced v1 to adapter and train-state v141 / 71,000 batches while v2
remained v139 / 70,000; local backups continue to refresh. The v2 v139
evaluation tests the current v2 head, and the prepared next comparison targets
v1 v141.

At 22:24 UTC, a fresh streaming audit recomputed row counts and SHA-256 for the
frozen v4 candidate, internal manifest, and all three split files; all five
matched the release manifest exactly (190,244 candidate/manifest rows;
171,261 train; 9,673 validation; 9,310 test). The technical release remains
`approved_for_research_training` with `upload_gate=true`; this confirms byte
integrity only and does not resolve the listed source rights/privacy/semantic
limits.

At 22:29:31 UTC, a fresh authenticated W&B `Project.storageBytes` query read
120,256,977,933 B, up 2,828,024,834 B from 22:13:53. This is net project
usage, not quota or proof of whether UI deletions reclaimed space. A full
read-only train-state inventory found 117 older versions with no aliases and
successful zero-dependency checks: v1 v82-v139 and v2 v80-v138. They total
124,068,520,953 B logical, which cannot be treated as physical reclaim. Keep
v1 v140/v141 and v2 v139/v140. No W&B artifacts were deleted. Full evidence is
in the private [22:29 inventory](execution-2026-10-19/wandb-live-train-state-delete-candidates-2026-10-19T2229Z.json)
and [storage triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md).

At 22:30 UTC, W&B Training API still reported active v1 and v2 jobs as
`RUNNING`, with null progress and stale prior-day `updated_at`; their versioned
artifacts continue to advance (v1 v141 / 71,000; v2 v140 / 70,500). The
v4 baseline job (system messages stripped) remains `PENDING` with no error or pending reason.
The v1 v141 paired evaluation had 38/120 successful calls per arm and the v2
v140 comparison had 2/120; both had zero failures. Fireworks was live at step
207 / 10,704 (loss 0.6897 at 22:30:02.838Z), with no tuned remote checkpoint
in its latest read-only listing.

The v2 v139 paired evaluation finished at 22:27 UTC with 240/240 successful
calls and no errors. SFT returned one normalized response across the 120 cases,
made zero tool actions, and passed 60/240 synthetic checks; base returned 91
unique responses, made 144 tool actions, and passed 191/240. Estimated usage
was $0.1100935, with actual billed usage unavailable. This reproduces the
collapse at v2's current 70,000-batch head. The v1 v141-versus-base paired
evaluation started at 22:27 UTC with the same frozen suite and a $1.3824
preflight maximum.

#### 2026-10-19 22:34 UTC Kaggle source version confirmed

A fresh authenticated read-only Kaggle metadata lookup confirmed the current
`kamaruladha/mental-disorders-identification-reddit-nlp` snapshot is version 2
and its metadata license name is `Reddit API Terms`. The current archive hash
is `e0b99acbbb0ab9603191848a144e491741ad76a5a24b271e57ccea3b55a0bace`; its
CSV hash exactly matches the previously audited file snapshot, so the 58,409
unique row bindings are reproducible against Kaggle version 2. This still does
not establish the curation-time version or permitted rights/privacy status.
The CLI's auth flow rejected the environment token, but direct bearer API
metadata/download succeeded; source files remained private under `/tmp`.
See the [source/cache audit](execution-2026-10-17/top-reddit-source-local-cache-audit-2026-10-19.md).

#### 2026-10-19 22:35 UTC paired evaluation: W&B v1 v141

The newest v1 checkpoint at evaluation time (v141, 71,000 completed batches)
was compared with base on the fixed held-out 120-case suite. All 240 calls
succeeded. The SFT arm produced one unique normalized response, made zero tool
actions, and passed 60/240 synthetic assertions; base produced 96 unique
responses, made 149 tool actions (143 successful), and passed 201/240. The
estimated usage was $0.11017575; actual billed usage was not available. This
confirms response collapse and tool-use failure at the latest v1 checkpoint;
the synthetic assertions are not validated for quality or safety. The v2 v140
comparison remained active at 80/120 SFT calls and 81/120 base calls, with no
errors. Rolling local backups had advanced to v1 v142 / 71,500 batches and v2
v141 / 71,000 batches, which remain unevaluated. See the private [evaluation
report](execution-2026-10-19/latest-checkpoint-evals/report.md).

#### 2026-10-19 correction: W&B preview pricing

The published [W&B Training Pricing page](https://site.wandb.ai/pricing/training/)
explicitly says Serverless SFT/RL training is free during public preview and
that pricing will be announced at general availability. The [Serverless
Training docs](https://github.com/wandb/docs/blob/main/serverless-training.mdx)
also say the service is in public preview and training is free during that
period; GitHub marks that docs repository archived/read-only as of September
30, 2026. The training-pricing URL currently redirects to CoreWeave Forge, so
the published preview terms are clear but whether W&B has changed this account's
terms is not confirmed by the redirect. Use the published free-preview training
terms for the experiment plan; keep inference usage metered separately and
check artifact storage against the workspace plan/quota. Do not infer that
Forge's post-training rates apply to existing W&B jobs without provider
confirmation. This supersedes the earlier overly cautious wording that treated
the preview offer as historical only.

At 22:44 UTC, the W&B Training API still returned `PENDING` for the no-system
v4 baseline job `24cc2d06-3ec3-4356-ad3a-179694dd86a7`; its event feed was empty
and `/system-check` reported all queues healthy. The service exposes no pending
reason, so storage pressure is a plausible but unproven explanation. The
preserve-system v4 variant remains staged locally and has no W&B job. At the
same time, v1 and v2 stayed `RUNNING`; the rolling local backups were v1 v142
(71,500 batches) and v2 v141 (71,000 batches). Paired comparisons of those
heads against the base are running on the fixed 120-case suite with a $0.50
maximum estimated inference charge per pair. Fireworks remained live at step
222/10,704 as of 22:44 UTC, with no error; it saves no usable tuned checkpoint
until the run completes.

At 22:50 UTC, the two newest-head evaluations finished successfully: both
completed 240/240 calls with no request failures. v1 v142 SFT had one unique
response, zero tool calls, and 60/240 synthetic assertions passed; base had 19
unique responses, tool calls in 84 cases, and 71/240 assertions passed. v2 v141
SFT had the same one-response/zero-tool/60-of-240 result; base had 12 unique
responses, tool calls in 90 cases, and 65/240 assertions passed. Both SFT
heads match the same normalized output hash observed on earlier collapsed
checkpoints. Estimated inference was $0.06809825 and $0.06911325 respectively,
below the $0.2976 preflight ceiling for each run; actual billing is not exposed.
These synthetic checks are not clinical-quality or safety evidence. See the
[evaluation report](execution-2026-10-19/latest-checkpoint-evals/report.md).

A fresh 22:50 UTC Training API check still showed v1 and v2 `RUNNING` with
stale `updated_at` fields, while artifacts continued advancing. The latest
private adapter backup manifest was v1 v144 / 72,500 batches and v2 v142 /
71,500 batches (22:48 UTC); the separate resume-state mirror was v1 v143 /
72,000 and v2 v142 / 71,500 (22:45 UTC). The v4 no-system baseline remained
`PENDING` with no provider error, and the preserve-system variant remains local
only. Fireworks was live at step 228/10,704 at 22:49 UTC without error.

#### 2026-10-19 22:59 UTC prompt-level split audit and breakaway package

An audit across the actual v4 train/validation/test payloads found 673
case/whitespace-normalized user prompts spanning more than one split, affecting
11,136 rows. The current check groups on full conversation content, so two
different assistant answers to the same user prompt can be assigned to
different splits. The largest contribution is `mitch_hamidi_bpd_nlp`: 451
repeated prompts affect 10,323 rows. In that source family, all 13,890 examples
have one shared system prompt; 2,344 unique normalized user prompts; the largest
prompt group has 440 rows; and 1,113 outputs match the adapter's generic
community-discussion label template. The declared source repo is still 404 and
the object-store prefix remains inaccessible, so no exact upstream binding or
rights determination has been added.

Built and independently read back the local-only
`prompt-disjoint-20261019-v3` candidate from the frozen v4 payloads. It retains
all 190,244 rows, groups global prompts by SHA-256 of concatenated user turns
after casefold/whitespace normalization, and yields 171,166 train, 9,500
validation, and 9,578 test rows. Both system-stripped and zero-loss-weight
system-preserving variants are packaged. The output check confirms zero
normalized user prompts cross splits and identical non-system row projections
across the two variants. This diagnoses and fixes prompt-level leakage in a
new offline candidate; it does not alter v4 or the running jobs and is not
uploaded. The manifest keeps `upload_gate=false` pending resolution of the
provider/storage constraints. Reproducible builder tests pass (3/3), Ruff
passes, and the docs diff check passes. See the [split audit and package
details](execution-2026-10-17/top-reddit-source-local-cache-audit-2026-10-19.md)
and [private manifest](execution-2026-10-19/prompt-disjoint-20261019-v3-manifest.json).

#### 2026-10-19 Empath origin and prompt-split recheck

The pinned Empath upstream cache (`Adapting/empathetic_dialogues_v2` at
`cb66212…`) and existing row-binding sidecar were joined against all 35,977
Empath rows in v4. Exact/normalized match counts are unchanged; this identifies
source rows but does not determine rights or privacy clearance. A hash-only
sidecar then exposed prompt leakage within the current v4 split: 33 exact prompt
groups affect 127 rows, and 38 case/whitespace-normalized prompt groups affect
139 rows. Additionally, 1,766 exact and 2,264 normalized source locators are
assigned to multiple splits. Independent replay of the private sidecar verified
all 35,977 unique candidate hashes and reproduced these counts without raw text
fields. No candidate payload was changed. Treat the current Empath split as
non-disjoint for evaluation; the prompt-disjoint v3 package is the corrected
local comparison candidate. See the private [Empath audit](../../ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/empath-v4-row-prompt-split-audit-report.json).

#### 2026-10-19 Reddit mental-health NLP lineage and split audit

The 70,968-row `reddit_mental_nlp` family was rebound using the existing
Kaggle version-2 row-reference evidence (the curation-time snapshot is still
unknown). Hash-only replay confirms 28,894 exact and 29,515 normalized unique
source-row bindings; neither tier repeats a locator across splits. The v4
content-group split is disjoint. Prompt identity has a smaller overlap: 7 exact
prompt hashes across splits affect 14 rows, and 9 normalized prompt hashes
affect 18. I independently replayed the 70,968-row sidecar and reproduced all
counts; it contains no raw text. Reddit terms, rights, privacy, consent, and
provider-use status remain unresolved. See the [audit report](execution-2026-10-19/reddit-mental-nlp-v4-prompt-locator-crosssplit-2026-10-19.md).

#### 2026-10-19 W&B checkpoint backup watcher correction

The v1/v2 job-status endpoint continues to return HTTP 500 while the artifact
versions API currently lists no remote versions. The two local backup scripts
previously stopped at the status error before checking artifacts, and an empty
artifact result would have overwritten their latest local checkpoint indexes.
They now record status as `UNKNOWN`, continue artifact polling, keep status
observations separate, and preserve the last verified local adapter/train-state
index when no remote version is listed. Two workers are running at five-minute
intervals. A one-poll run against the live account reproduced the HTTP 500 and
empty artifact state without overwriting local indexes. Focused regression
tests pass (2/2); Ruff passes. The watchers perform no remote writes and retain
only the newest two local versions per run if newer versions reappear.

#### 2026-10-19 23:22 UTC W&B active artifact visibility recheck

Read-only authenticated W&B SDK checks find all four named v1/v2 LoRA and
train-state collections, but both artifact listing methods return zero
versions. Exact lookups for earlier versions that were previously downloaded
also return “artifact membership not found.” I also listed all 13 LoRA and 8
train-state collections in the project and checked adjacent collections named
with either release hash; those also have zero visible versions. This is strong
evidence that those remote versions are no longer present or visible to this
credential, consistent with deletion. It does not prove the jobs stopped or that newer
checkpoints are no longer being written. The v1 and v2 Training API GETs still
return HTTP 500, so their current states are unknown. The v4 no-system job
still returns `RUNNING` with its last update at 22:50 UTC and no numeric
progress. A 23:27 UTC recheck returned the same three job observations and
zero versions in the four active v1/v2 collections. Local private mirrors
remain intact: v1 LoRA v144 / 72,500 batches and train state v143 / 72,000; v2
LoRA and train state v142 / 71,500. A fresh
local SHA-256/size check passed for all 26 files across those four mirrors.
W&B `/system-check` returned HTTP 200 with API, database, CPU, model-management,
and GPU checks successful, but it exposes no storage quota or usage signal.
That rules out a general API/queue outage, not artifact-specific visibility or
storage exhaustion. No artifacts or jobs were modified. Avoid further artifact
cleanup until a fresh inventory confirms what remains and whether newer
checkpoints are persisting. See the [visibility snapshot](execution-2026-10-19/wandb-active-artifact-visibility-20261019T2322Z.json).
See the [visibility snapshot](execution-2026-10-19/wandb-active-artifact-visibility-20261019T2322Z.json).

#### 2026-10-19 23:35 UTC Reddit mental-health-posts source/prompt replay

I independently replayed the private hash-only sidecar for all 30,444 rows:
candidate hashes are unique; family split sizes reproduce as 27,373 train,
1,581 validation, and 1,490 test; all 10,693 unique upstream row locators occur
once and none cross splits. The report's prompt overlap is limited to one exact
hash (2 rows, train/validation) and two case/whitespace-normalized hashes (4
rows, train/validation). Content groups do not cross splits. The sidecar remains
mode 0600 under a mode 0700 directory. The 19,751 unmatched rows and unresolved
curation-time revision, rights, privacy, consent, and Reddit-term questions
remain open. No corpus payload or provider job changed. See the [audit
report](execution-2026-10-19/reddit-mental-health-posts-v4-prompt-locator-crosssplit-2026-10-19.md).

#### 2026-10-19 23:35 UTC W&B and Fireworks live check

An authenticated direct poll still returns HTTP 500 for the v1 and v2 W&B
training-job endpoints; their state remains unknown. The v4 no-system job
returns `RUNNING`, but its last update is still 22:50:52 UTC and it exposes no
progress. The local checkpoint watchers remain live; their 23:34 observations
still show v1/v2 `UNKNOWN` and no artifact lookup error, while the newest
mirrored heads remain the earlier v1/v2 artifacts recorded above. This is not
evidence of a new checkpoint or of a stopped run. Fireworks is still running at
step 366/10,704 as of 23:33:26 UTC, with no reported error. See the [W&B poll
record](execution-2026-10-19/wandb-job-poll-20261019T2335Z.json) and [Fireworks
run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

#### 2026-10-19 23:37 UTC MentalChat16K split audit

The 11,135-row `mentalchat16k` source family transfers fully into the v4
candidate. Independent replay of the private sidecar found 8 exact and 8
case/whitespace-normalized input groups crossing v4 splits, affecting the same
18 rows (10 train, 4 validation, 4 test). No exact or normalized upstream
locator hash repeats across candidate rows. The family-specific private report
and hash-only sidecar are under the mode-0700 provenance directory; the sidecar
is mode 0600 and contains hashes/split labels only. This is a v4 split defect,
not a reason to discard the source family: the local prompt-disjoint v3 package
was already verified across all candidate rows for zero normalized user-prompt
groups crossing splits. Source rights and privacy are separate unresolved
questions. See the [v3 split manifest](execution-2026-10-19/prompt-disjoint-20261019-v3-manifest.json).

#### 2026-10-19 23:38 UTC break-away package independent verification

I reread both variants of `prompt-disjoint-20261019-v3` from disk and
independently verified every file SHA-256, row count, and normalized user-prompt
hash. Both variants contain all 190,244 rows (171,166 train, 9,500 validation,
9,578 test), have zero empty user prompts, and have zero normalized user-prompt
hash intersections between any pair of splits. Row-by-row non-system message
projections match between the system-stripped and preserve-system versions.
The 190,244-row private lineage file matches its manifest SHA-256 and split
counts; 32 repeated canonical row hashes are all assigned within a single
split. Its 177,004 normalized prompt-group hashes also match the manifest and
none cross destination splits. During this check I found the MentalChat16K audit report had copied the
old 190,233 manifest count; verified the internal manifest has 190,244 rows
and corrected that report field without changing its sidecar. This confirms a
local split-clean research candidate, not source-rights/privacy clearance or
provider upload eligibility.

#### 2026-10-19 23:39 UTC account credit and promotion coverage refresh

No current numeric balance or quota was exposed for Adaption or W&B, and no Fireworks account-specific promo activation was established. The only live Adaption estimate recorded for AutoScientist qualification is absent: its 112-credit / 150-minute estimate applies to an Adaptive Data operation on the separate 11,192-row run-2 dataset, not training or the 522,658-row v4 dataset. The 418-row processing estimate is 5 credits / 16 minutes and is not training coverage. W&B's latest recorded paired 120-case evaluations (22:50Z) estimate $0.06809825 for v1 and $0.06911325 for v2, each under its $0.2976 configured preflight maximum; actual billing and remaining credits were not returned. Earlier aggregate ledger figures are stale relative to later evaluations. Fireworks' official Muse Glimmer page currently advertises free SFT through November 30 with no card required, but the account's prior read-only plan computes eligibility from a local date and the account billing summary does not expose the credit balance. Treat Glimmer SFT coverage as conditional; its separately priced sampling and inference remain uncovered. No next experiment is established as fully credit-covered. See the [timestamped machine-readable account coverage refresh](execution-2026-10-19/provider-account-coverage-refresh-2026-10-19T2339Z.json).

#### 2026-10-19 23:40 UTC W&B storage and checkpoint recheck

The authenticated W&B GraphQL `Project.storageBytes` meter read 9,727,667,199 B
at 23:40:17 UTC, down 106,758,606,054 B (about 91.6%) from the 22:09:10
reading. This confirms a large reduction in project storage usage during the
owner's cleanup; the meter does not expose the quota or prove how much writable
headroom remains. Between the 23:39 and 23:40 readings it also rose by about
943 MB, so usage is still changing. A direct artifact SDK recheck at 23:40
found all four active v1/v2 LoRA and train-state collections but zero visible
versions in each; the 23:39 watcher poll also found none and reported no lookup
error. The v1/v2 job endpoints still return HTTP 500. The v4 no-system job is
`RUNNING` but has no progress and its `updated_at` remains 22:50:52 UTC. Do not
infer that the jobs stopped or that storage is now sufficient. See the
[storage/job snapshot](execution-2026-10-19/wandb-live-storage-and-job-refresh-20261019T2340Z.json).

The 5,606-row `mental_health_multiagent` family audit is independently
reaggregated: 5,064 train, 272 validation, 270 test; 5,601 exact and normalized
prompt-context hashes, with two repeated hashes covering seven rows but none
crossing splits; all 5,606 content groups are distinct; the 24 matched public
source locators are unique and do not cross splits. The remaining 5,582 rows
are unmatched to that pinned public snapshot, and it does not prove the
adapter-declared private S3 origin. Sidecar/report permissions and hashes were
checked. See the [audit report](execution-2026-10-19/mental-health-multiagent-v4-prompt-locator-crosssplit-2026-10-19.md).

The account-coverage refresh found no current numeric Adaption or W&B credit
balance. The public Fireworks Muse Glimmer offer says SFT is free through
November 30, but the available account check does not prove account-specific
activation; sampling/inference charges remain separate. The full Fireworks
run remains live at step 463/10,704 as of 23:44:44 UTC. No new training or
inference job was created. See the [coverage refresh](execution-2026-10-19/provider-account-coverage-refresh-2026-10-19T2339Z.json) and [live run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

#### 2026-10-19 23:43 UTC KokoroChat source/prompt audit replay

The next family, `KokoroChat` (4,615 rows), was independently reaggregated from
its private hash-only sidecar. All rows transfer to v4; exact and normalized
prompt hashes each remain unique across 4,168 train, 226 validation, and 221
test rows. Its 18 matched public-comparator locator hashes are unique and do
not cross splits. The sidecar has 4,615 candidate-row hashes, is mode 0600 under
a mode 0700 directory, and contains no raw text. Only 18 rows bind to the
pinned public comparator; 4,597 are unmatched, and that public repository does
not prove the adapter's different private-S3 cache origin. This audit found no
new split defect. See the private report and sidecar at
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/kokorochat-v4-row-prompt-split-audit-report.json` and
`.../kokorochat-v4-row-prompt-split-audit-sidecar.jsonl`.

#### 2026-10-19 23:43 UTC Adaption empty-validation diagnosis

Read-only API confirms three ctx9 AutoScientist runs failed at 0/1 with the same
empty generated validation JSONL error: array ctx9
`33bba6d2-d9e5-408c-bd4d-76544d2cde78`, scalar-text ctx9
`ef278ee7-b04d-4014-9b7a-cb7ee81b66fd`, and the earlier instruction ctx9
`8d00b26c-de36-452a-abc2-5cd36b76036b`. All used explicit
`original_prompt`/`original_completion` mappings. Their ready dataset metadata
reports 522,658 rows but null `prompt_column`/`completion_column`; the successful
11,192-row control has populated canonical-column metadata. A local integrity
pass found no malformed/blank v4 rows and confirms the successful control's
array-valued prompt/completion shape matches ctx9's array representation; the
scalar-text conversion also failed, so value type alone is not causal. The
full-history run failed earlier during S3 download and does not isolate the
validation writer.

No provider-side split or serialization counters are exposed in available read
APIs. Root cause remains unresolved between large-dataset/split behavior,
corpus-specific validation preparation, and a provider issue. Stop further
Adaption runs/uploads pending support diagnostics for split counts, mapping
resolution, rejected rows, input/output byte counts, temp-file creation, and raw
row/length limits. Local training payloads are private; the previously 0664
control JSONL was tightened to 0600, and all checked hashes match manifests.
See the [qualification diagnosis](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md).

#### 2026-10-19 23:44 UTC checkpoint watcher follow-up

Both backup workers remain alive. Their 23:44:28–29 polls still show v1/v2 job
status `UNKNOWN`, null latest artifact version/batch fields, and no artifact
lookup exception; no new artifact has reappeared in the mirrored collections.
The W&B project storage meter is unchanged at 9,727,667,199 B between 23:40:17
and 23:44:43 UTC. This confirms stable usage across that interval, but still
reveals neither quota nor job health. Fireworks continues without an error at
step 457/10,704 as of 23:44:08 UTC.

#### 2026-10-19 23:44 UTC Adaption failure-path confirmation

Read-only Adaption API polls confirm the three v4-derived ctx9 attempts
(`8d00b26c…`, `33bba6d2…`, and `ef278ee7…`) are terminal failed at 0/1. Both
latest attempts expose the same specific failure: the provider's pre-upload
validation JSONL temp file is empty (0 bytes). Their datasets report succeeded
at 522,658 rows, but dataset metadata returns null canonical prompt/completion
columns even though the run records echo the supplied mapping. Local checks
found no malformed records or empty prompt/completion fields in the control,
array, or scalar-text files; array versus scalar formatting alone is not the
cause. The issue is narrowed to this large dataset's provider-side validation
or column-metadata preparation, with no row-level counter available from the
API. Do not spend another credit-consuming training attempt until Adaption
provides those diagnostics or a locally reproducible split/writer contract.
The current credit balance and debit for the failed jobs remain unknown. See
[Adaption qualification details](adaption-qualification-refresh-2026-10-19.md).

#### 2026-10-19 23:45 UTC Crisis Benchmark audit replay

The 1,522-row `crisis_benchmark` family was reaggregated from its private
hash-only sidecar: 1,374 train, 79 validation, 69 test; all exact and
case/whitespace-normalized user-prompt hashes are unique; all 1,522 content
groups are unique; and no hash crosses splits. The 1,465 bound source locator
and upstream row-hash references are unique with no cross-split reuse. The
remaining 94 unmatched rows and 36 ambiguous source rows retain those statuses.
This source is an evaluation benchmark, so exact source matching does not
resolve benchmark contamination or suitability for SFT; rights, privacy,
consent, and provider-transfer status are also unresolved. See the [audit
report](execution-2026-10-19/crisis-benchmark-v4-prompt-locator-crosssplit-2026-10-19.md).

#### 2026-10-19 23:47 UTC Fireworks live progress

The Fireworks Muse Glimmer SFT process remains alive. The launcher reported
step 480/10,704 at 23:47:16 UTC with loss 1.3471; steps 477–479 completed and
no training/API error was reported. This is still an in-progress experiment,
with no tuned checkpoint or final evaluation yet. The worker's private report
contains the longer loss history and rolling runtime estimates.

#### 2026-10-19 23:48 UTC PsyDial lineage audit replay

An independent hash-only replay validated the 892-row PsyDial sidecar against
the exact v4 candidate and internal manifest hashes. Split counts are 817/39/36;
885 distinct exact and normalized prompt hashes include four repeated groups,
with one prompt group crossing splits across five rows. All 892 content groups
remain split-disjoint. The 893 referenced source locators are unique; 891 rows
are exact-unique bindings and one remains exact-ambiguous. The private sidecar
is mode 0600 and all 892 row hashes, groups, and split labels match the frozen
manifest. This does not resolve rights, privacy, consent, or provider-transfer
status. See the [PsyDial audit](execution-2026-10-19/psydial-v4-prompt-locator-crosssplit-2026-10-19.md).

#### 2026-10-19 23:49 UTC W&B checkpoint watcher poll

Both five-minute local backup workers are still alive. Their 23:49:29 polls
again returned `UNKNOWN` from the job-status API and found no new version in
the watched v1/v2 LoRA or train-state collections; lookups completed without
artifact API errors. Thus, the watcher has not observed a new checkpoint in
those collections since its earlier versions (v1 LoRA v144/train-state v143;
v2 v142). This does not establish job termination or rule out checkpoints in
another collection/path. Preserve the local backups and continue polling; the
W&B status endpoint's repeated `UNKNOWN` remains an unresolved observability
gap.

#### 2026-10-19 23:52 UTC W&B checkpoint collection mismatch found and fixed

The earlier watcher result was incomplete: it monitored only the old v1/v2
collection names. A read-only inventory of all 287 project artifact collections
found the active v4 job's separate collections,
`arc-sft-baseline-30e158011725-sft-resume` and
`arc-sft-baseline-30e158011725-train-state-sft-resume`. Both produced v0–v4;
their v4 artifacts carry alias `sft-resume-24cc2d06-3ec3-4356-ad3a-179694dd86a7`
and were created at 23:48:42/45 UTC. A direct job query returned `RUNNING`.
The v4 metadata reports 2,500 completed batches. This explains why the prior
v1/v2-only poll showed no new checkpoint while the job was saving them.

Downloaded both v4 artifacts to the private local backup root and verified each
file's byte size and SHA-256 against W&B's artifact file records (117,843,308
bytes for the LoRA and 1,060,414,697 bytes for train-state). Both filesets and
manifests are mode 0600 under mode 0700 directories. The two watcher scripts
now include the v4 job and actual collection names; after a clean restart,
23:52:37/41 polls report `RUNNING`, v4 / 2,500 batches, and no lookup errors.
No remote artifact was deleted. A private 0600 project inventory is saved at
`execution-2026-10-19/wandb-project-artifact-collection-inventory-20261019T2349Z.json`.

#### 2026-10-19 23:53 UTC Psy-Insight source audit replay

Independently rechecked the 673-row Psy-Insight sidecar against the 190,244-row
v4 candidate and aligned internal manifest. The family has 588/39/46
train/validation/test rows; exact and normalized prompt hashes are each unique
across all 673; 518 rows bind to unique public source locators and 155 remain
unmatched. All 50 generated-continuation excerpt locators are unique and do not
cross splits. The 673 sidecar row hashes/splits match the frozen manifest and
the sidecar is mode 0600. The public comparison source is not proven to be the
adapter-declared private S3 acquisition; licensing, privacy, consent, clinical
review, and provider-transfer questions remain unresolved. See the
[Psy-Insight audit](execution-2026-10-19/psy-insight-v4-prompt-locator-crosssplit-2026-10-19.md).

#### 2026-10-19 23:49 UTC Fireworks live progress refresh

Fireworks reported step 495/10,704 at 23:49:07.835 UTC, loss 0.7835, with the
process still active and no reported training/API errors. Its current rolling
completion extrapolations are roughly 20.5 hours using the recent faster window
and 91 hours using the longer window; service cadence is variable, so neither
is a provider ETA. The tuned checkpoint and paired evaluation are still pending.

#### 2026-10-19 23:57 UTC W&B v4 checkpoint paired diagnostic

Completed a five-case paired comparison of the active 2,500-batch W&B v4
adapter against its Qwen3.6-35B-A3B base using the frozen synthetic development
set. All five cases now have successful results for both arms; the research
case was rerun as a pair at a 2,048 input-token cap after the base tool trace
exceeded the initial 1,024 cap. Two base outputs hit the 1,024 output cap.
Neither arm used external tools; tools were local mock fixtures, and the small
deterministic assertions are unvalidated for quality/safety. They passed 3/7
for base and 4/7 for SFT, so this is diagnostic evidence only, not a clinical
or model-selection result. Selected paired cost estimates total $0.00497950;
including the failed initial endpoint call and minimal routing probe, estimated
usage across all attempts is $0.006407. Actual billing was not returned. See
the [evaluation report](execution-2026-10-19/wandb-v4-checkpoint-five-case-eval-2026-10-19.md)
and private result directory `ai/training/output/wandb_live_checkpoint_eval_20261019/`.

#### 2026-10-19 23:57 UTC Fireworks live progress refresh

Fireworks reported step 570/10,704 at 23:57:22.764 UTC, loss 0.7748. The
training process remains active with no reported API/training errors; the full
paired evaluation is still deferred until training finishes, and the tuned
checkpoint is not yet available. Current completion extrapolations remain
variable and are maintained in the private [run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

#### 2026-10-20 00:03 UTC W&B v5 checkpoint preserved locally

The corrected local watchers found and downloaded v5 from the active v4 job's
actual artifact collections. At 00:02:43 UTC, the LoRA adapter was recorded at
3,000 completed batches; at 00:03:02 UTC, the 1,060,414,697-byte train-state
artifact was recorded at the same batch count. Both report job `RUNNING` and no
artifact lookup error. Local file sizes and SHA-256 hashes are recorded in
mode-0600 manifests under the mode-0700 backup root
`ai/training/output/wandb_local_checkpoints_20261019/v4/` and
`v4-train-state/`. The current adapter file is 117,842,120 bytes; train-state
includes optimizer state plus step-96 and step-0 adapter snapshots. The
checkpoint metadata says 3,000 completed batches while its optimizer snapshot
is step 96; these are distinct counters and should not be conflated. This
checkpoint is now locally preserved; the watchers remain active for later
versions. No remote artifacts were deleted.

#### 2026-10-20 00:03 UTC ESConv lineage audit completed

The next largest eligible family with pinned row references, ESConv (892
candidate rows), was audited against the frozen v4 candidate and manifest.
Exact and normalized prompt hashes and content groups are all unique, with no
cross-split reuse. Existing source bindings remain 13 exact-unique, 16
normalized-unique, and 863 unmatched; the 29 bound locators are unique and
stay within a single split. This is technical lineage only; rights, privacy,
consent, clinical review, and provider-transfer status remain unresolved. See
the [ESConv audit](execution-2026-10-19/esconv-v4-prompt-locator-crosssplit-2026-10-19.md)
and the [public-source binding summary](execution-2026-10-19/public-source-row-binding-summary.md).

#### 2026-10-20 00:03 UTC Fireworks live progress refresh

The Fireworks Muse Glimmer run reported step 613/10,704 at 00:02:56 UTC, with
loss 1.8785 and no reported training/API error. It remains an experiment-only
run; there is no local tuned checkpoint yet. Rolling completion estimates are
roughly 20 hours from the recent window and 75 hours from the longer window,
with variable service cadence; these are local extrapolations, not a provider
ETA. The [private run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md)
tracks the latest observations.

#### 2026-10-20 00:10 UTC W&B v5 checkpoint paired diagnostic

Ran the same five-case synthetic paired evaluation against W&B checkpoint v5
(3,000 completed batches) and the Qwen3.6 base through W&B Serverless
Inference. Four pairs completed at the existing 1,024-token input cap; the
base research/citations case exceeded it, so both arms were rerun at 2,048
under a separate $0.012 cap. All five selected pairs now have successful
results. Two outputs per arm hit the 1,024 output cap. Seven unvalidated
synthetic state assertions passed 3/7 for base and 2/7 for v5. The base arm
had five evaluator-local mock-tool trace events; no external tools were used.
Selected-pair estimated cost is $0.00727175, and estimated usage including the
partial first pass is $0.00786725; actual billing is unavailable. A separate
preflight rejected an all-five 2,048-token setup at $0.05376 before sending
requests because it exceeded the existing $0.0487 cap. These results are
behavioral diagnostics only, not clinical or model-selection evidence. The
main private run ID contains a stale `v4` label, but its artifact URI and
manifest pin v5. See the [v5 evaluation report](execution-2026-10-19/wandb-v5-checkpoint-five-case-eval-2026-10-20.md).

#### 2026-10-20 00:09 UTC live run monitor refresh

The v4 W&B training job continues to report `RUNNING`. Its latest completed
local checkpoint remains the verified v5 LoRA plus train-state at 3,000
batches (last watcher poll: 00:08:04 UTC); neither watcher reports a lookup
error. Fireworks Muse Glimmer remains active at step 667/10,704 as of 00:09:15
UTC, with no reported training/API error. Its variable rolling completion
estimates are recorded in the private run report and should not be treated as
a provider ETA.

#### 2026-10-20 00:10 UTC ARC corpus lineage audit replay

Independently replayed the 1,085-row ARC corpus hash-only sidecar against its
reported evidence: 981/58/46 train/validation/test rows, all exact and
normalized prompt hashes, content groups, and upstream locator hashes unique,
zero cross-split groups, and all 1,085 rows marked exact canonical message
match. Sidecar SHA-256 matches the public audit report and file mode is 0600.
The ARC archive's machine acceptance is not clinical, rights, privacy/consent,
or transfer clearance. See the [ARC audit](execution-2026-10-19/arc-corpus-v4-prompt-locator-crosssplit-2026-10-20.md).

#### 2026-10-20 00:15 UTC W&B v6 checkpoint preserved and evaluated

The active job's v6 LoRA and train-state checkpoints are both locally backed up:
v6 records 3,500 completed batches and its optimizer-state metadata records
policy step 112. The adapter is 117,843,308 bytes and train-state is
1,060,414,703 bytes; local manifests include file hashes. W&B still reports
`RUNNING`, and both watcher polls found v6 without lookup errors.

A paired five-case diagnostic against base found a functional regression at
this checkpoint: base returned user-facing content for all five cases, while
v6 returned HTTP-successful `stop` responses with empty user-facing content
for all five. A direct minimal endpoint probe confirmed `content` was empty and
response data was in a separate `reasoning` field; the evaluator does not
expose reasoning as an answer. A one-case v5-v6 comparison also returned
nonempty user-facing content for v5 and none for v6. This confirms the finding
is not caused by the evaluator dropping a populated `content` field, but the
cause (training versus serving behavior) is not determined. Treat v6 as
currently unusable for user-facing inference on this diagnostic until the
cause is isolated. The five-case base/v6 assertions passed 3/7 and 2/7
respectively, unvalidated for quality or safety; there were no external tool
calls. Selected paired estimate: $0.00482425; all-pass estimate including the
partial first run: $0.00539350; one-case v5-v6 paired comparison: $0.00039250.
Actual billed totals are unknown. See the [v6 diagnostic report](execution-2026-10-19/wandb-v6-checkpoint-five-case-eval-2026-10-20.md).

#### 2026-10-20 00:16 UTC ML-BPD lineage audit replay

Independently replayed the 100-row ML-BPD hash-only sidecar against its report.
Counts are 86/11/3 train/validation/test; exact and normalized prompts and
content groups are each unique with no split overlaps. The retained origin
statuses are 56 unique and 44 duplicate-content ambiguous, covering 144
unique locator alternatives with no cross-split reuse. Sidecar hash and 0600
mode match the audit. The upstream contains sensitive clinical measures and
has no repository license file; lineage does not clear privacy, consent,
clinical validity, training, or provider transfer. See the [ML-BPD audit](execution-2026-10-19/ml-bpd-v4-prompt-locator-crosssplit-2026-10-20.md).

#### 2026-10-20 00:17 UTC live run progress

The W&B job remains `RUNNING`; v6 is locally preserved at 3,500 completed
batches (last adapter/train-state observation 00:13:23 UTC). Its user-facing
inference result remains the unresolved empty-content regression documented
above. Fireworks Muse Glimmer remains active at step 723/10,704 as of 00:16:17
UTC, with no reported API/training error. Its latest rolling runtime estimates
are in the private run report and remain variable local extrapolations.

#### 2026-10-20 00:26 UTC W&B v7 five-case comparison

The v7 W&B checkpoint (4,000 completed batches) returned nonempty user-facing
content in all five paired synthetic cases, with five distinct normalized SFT
responses. This recovers from v6's empty-content behavior on this small suite.
Seven unvalidated assertions scored 3/7 for base and 2/7 for v7; this remains
diagnostic evidence only. The selected pair estimate was $0.00497925; estimated
usage including the partial initial pass was $0.00686975. Actual billing was
unavailable. No external tools were invoked. See the [v7 evaluation report](execution-2026-10-19/wandb-v7-checkpoint-five-case-eval-2026-10-20.md).

#### 2026-10-20 00:26 UTC local checkpoint retention widened

Updated both private backup watchers from two to 20 retained versions per
job. With about 98 GB available locally and approximately 1.06 GB per train
state, this covers the expected checkpoint cadence for the active run without
pruning earlier local snapshots. Restarted only the two backup watchers; they
now use the updated retention. Restored v4 adapter and train-state from their
versioned W&B artifacts because the former two-version policy had pruned their
local copies. v4-v7 adapter and train-state versions are now present locally;
no remote artifact or training process was changed. The targeted checkpoint
backup tests pass (2 passed).

#### 2026-10-20 00:26 UTC live run progress

W&B remains `RUNNING`, latest mirrored checkpoint v7 at 4,000 batches, with
matching train-state saved. Fireworks Muse Glimmer remains active at step
803/10,704 as of 00:25:46 UTC, no reported training/API errors. Latest rolling
completion estimates remain variable and are recorded in the private run
report, not a provider ETA.

#### 2026-10-20 00:33 UTC correction to v7 five-case summary

A recheck of the selected case-level results corrected the preceding v7 summary:
the SFT arm returned nonempty content in 4/5 cases (four distinct nonempty
responses), with one empty response. Base had two empty responses and two
outputs hit the 1,024-token cap. So v7 improved from v6's 0/5 visible answers,
but still has an empty-answer case; it is not accurate to say all five v7
answers were nonempty. The seven assertions remain 3/7 base and 2/7 v7. The
[v7 evaluation report](execution-2026-10-19/wandb-v7-checkpoint-five-case-eval-2026-10-20.md)
has been corrected.

#### 2026-10-20 00:33 UTC W&B v8 five-case comparison

The v8 checkpoint (4,500 completed batches) returned nonempty user-facing
content in all five SFT cases, with five distinct normalized responses. Base
returned empty content twice and hit the 1,024 output-token cap twice. Seven
unvalidated synthetic assertions scored 3/7 base and 2/7 v8. Selected paired
estimated usage was $0.00510175, or $0.00571725 including the partial initial
pass; actual billing remains unknown. No external tools were invoked. See the
[v8 evaluation report](execution-2026-10-19/wandb-v8-checkpoint-five-case-eval-2026-10-20.md).
The corrected [v7 report](execution-2026-10-19/wandb-v7-checkpoint-five-case-eval-2026-10-20.md)
records one empty SFT response out of five, not zero.

#### 2026-10-20 00:55 UTC W&B v8 120-case held-out comparison

Compared v8 (4,500 completed batches) with the Qwen3.6-35B-A3B base on all
120 cases of the frozen first-party synthetic agent-tool suite, 15 cases in
each of eight scenarios. The initial 2-round pass completed 230/240 calls;
the 10 base resource-comparison calls exceeded the tool-round limit. A paired
3-round retry completed all 20 calls. Selected results therefore cover all
120 cases in both arms. Across 240 checks per arm, base passed 200 and v8 68.
Base returned nonempty content in 103 cases, used 152 local fixture-tool
actions in 92 cases, and hit the 512-token output cap 19 times. V8 returned
nonempty content in all 120 cases with 83 distinct normalized responses, but
made no tool actions and hit the cap five times. These synthetic checks are
unvalidated for clinical quality and safety; they indicate v8 is not ready for
agent-tool use despite varied, nonempty text. Estimated usage summed from all
per-result records, including failed initial calls and retries, is $0.12815375
against configured hard caps totaling $0.95; actual billed usage is unavailable.
The initial runner aggregate omitted estimated use on failed rows, so the
per-result sum is used for attempt accounting. Full details are in the
[v8 held-out report](execution-2026-10-19/wandb-v8-heldout120-eval-2026-10-20.md);
private results/configs remain under restricted permissions.

#### 2026-10-20 00:51 UTC v9 evaluation and cost-accounting fix

The v4 W&B job remains `RUNNING`; adapter and matching train-state v9 (5,000
completed batches) are backed up locally. A paired 120-case evaluation of v9
against base has started with temperature 0, 512 output tokens, up to four
tool rounds, and a $1.50 hard cap. Its local preflight estimated a $1.3824
worst case; at 00:52 UTC, 44/240 calls (22 paired cases) had completed
successfully.

The v8 120-case report exposed an evaluator accounting bug: run summaries
omitted estimated cost and token use from failed records even when those
records contained provider usage. The v8 report therefore uses the sum of all
per-result estimates ($0.12815375 across initial calls and retry attempts),
not the initial run summary's $0.1048125. Fixed the evaluator summary to
include known usage/cost from failed as well as successful calls and added a
regression test. `ai/qa/validation/tests/test_paired_eval.py` passes (22
tests), Ruff passes for both changed Python files, and targeted diff checks
pass. The already-running v9 process imported the earlier code; use its
per-result estimates when reporting total attempted cost.

At 00:49 UTC, the two local checkpoint watchers observed the W&B job as
`RUNNING` at v9/5,000 batches. At 00:52 UTC, the Fireworks launcher was alive
at step 1,017, loss 1.1723; no tuned checkpoint exists yet.

#### 2026-10-20 00:52 UTC Adaption full-corpus next-step qualification

Fresh read-only API checks confirm all four v4-derived AutoScientist runs are
terminal failed, and the historical 11,192-row control remains succeeded. A
non-launching recommendation on the 522,658-row scalar ctx9 dataset still
returns a Qwen3.6-35B-A3B one-epoch LoRA recipe, but no price. Three ctx9
serialization attempts fail with empty validation JSONL; array and scalar
forms were both tried, while the successful 11,192-row control also uses
array-valued prompt/completion messages. This establishes scale/path
correlation (522,658 vs. 11,192 rows), not an exact dataset cap or causal
threshold.

Official Adaption docs publish no AutoScientist raw row/file limit, validation
split option, or per-row limit. The documented Adaptive Data `max_rows` control
is a different workflow; AutoScientist `max_iterations` limits optimization
cycles rather than rows. Splitting into guessed shards would not produce one
full-corpus model without a documented resume-from-adapter feature. No
specific local transformation is justified yet.

The exact next no-cost action is an app order preview on the existing ready
ctx9 dataset: select original prompt/completion, Qwen3.6-35B-A3B, zero
augmentation, and one iteration; capture the separate AutoScientist training
credit quote, total, resolved config, and organization balance, then stop
before Confirm. The app documentation says the final order summary separates
training from optional expansion costs. The API recommendation only returns
hyperparameters, the create endpoint starts a job, and the available connector
has no balance or billing-history method. In parallel, provide Adaption Support
the four run IDs and ask for split sizes, mapping resolution, rejected and
serialized row counters, byte counts, the empty validation-file writer trace,
raw row/file/token limits, and whether sequential shards can resume from a
prior adapter. No message, upload, or job was initiated in this refresh. Full
evidence and exact data contract are in the [Adaption qualification record](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md).

#### 2026-10-20 00:57 UTC checkpoint and evaluation refresh

The owner correctly pointed out that W&B's documentation explicitly describes
Serverless SFT as public preview. W&B's published terms say it charges for
inference and artifact storage during preview, not adapter training. This is
the operative training-price assumption for these experiments; inference usage
and artifact storage remain separate meters, and the project's remaining
storage capacity is still not exposed by the status API.

The active W&B v4 job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` advanced from
v9/5,000 to v10/5,500 batches and remained `RUNNING`. The local LoRA and
train-state watchers both downloaded v10; the train-state is 1,060,414,703
bytes and the adapter is 112.38 MB. The exact latest local observations are
`ai/training/output/wandb_local_checkpoints_20261019/v4-latest.json` and
`v4-train-state-latest.json`.

The v9-versus-base held-out comparison reached 78/120 paired cases (156
successful calls) by 00:56 UTC. No failures were present in the result rows at
that point. It remains in progress under the $1.50 hard cap. The Fireworks
launcher reached step 1,050/10,704 at 00:57 UTC, with no new errors; it does
not publish a usable local checkpoint before training completes.

The authenticated W&B project `storageBytes` meter returned
16,326,404,011 bytes again at 00:56 UTC, unchanged from the 00:55 UTC query.
This is a project-level usage reading, not the account quota or remaining
capacity, so it cannot establish whether deleting artifacts created free
space. The newly observed v10 artifacts confirm that checkpoints continue to
be created while the job runs; retain the local backups and do not infer
checkpoint failure from a stale `/checkpoints` endpoint.

At 00:59 UTC, a direct authenticated Training API check still returned
`RUNNING` for the W&B job, and the Artifact API still listed v10/5,500 as the
latest train-state. The paired evaluation had advanced to 110/120 cases (220
successful calls), with results written through 00:59:14 UTC. Fireworks had
advanced to step 1,071/10,704 with no new errors. These jobs remain active.

#### 2026-10-20 01:00 UTC v9 held-out evaluation complete

The paired comparison completed successfully: all 120 cases (240 calls)
returned without errors. Base passed 198/240 deterministic checks; v9 passed
60/240. V9 produced one unique normalized response across 120 cases, made no
fixture-tool calls, and passed 0/75 tool-status and 0/75 response-content
checks. Base made 150 fixture-tool actions across 91 cases. Estimated usage was
$0.111669 total ($0.095673 base, $0.015996 v9); actual billing is unverified.
Treat v9 as a negative agent-tool result and do not promote it. Full methods
and results are in the [v9 held-out evaluation report](execution-2026-10-19/wandb-v9-heldout120-eval-2026-10-20.md).

At 01:02 UTC, a paired 120-case evaluation of W&B v10/5,500 batches against
the same base model and frozen suite was started under a $1.50 hard cap. The
preflight maximum is $1.3824. Its first three pairs (six calls) completed
successfully. Private config/results are under
`ai/training/output/wandb_live_checkpoint_eval_20261020/`; do not promote v10
until the full comparison and quality review complete.

#### 2026-10-20 01:08 UTC prompt-disjoint next-run package and v10 progress

Built local W&B G04 release
`wandb-full-corpus-prompt-disjoint-20261020-v1` from the already frozen
190,244-row source release. It preserves all candidate row identities and all
rows, changes only split assignment, and places all 177,004 casefolded,
whitespace-normalized user-prompt groups wholly within one partition. The
resulting partitions contain 171,166 train, 9,500 validation, and 9,578 test
rows. The release has `approved_for_research_training` status and an explicit
upload gate under the owner's existing research-training direction; rights,
privacy/consent, and provider-transfer dispositions remain as recorded in its
source release. It is not clinical or production approval. The release
validated through `resolve_train_payload`, including all payload hashes,
candidate rowrefs, partition counts, and prompt-group intersections. The
exact source candidate SHA remains
`f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`.
Package manifest:
[`wandb-full-corpus-prompt-disjoint-20261020-v1.json`](execution-2026-10-19/wandb-full-corpus-prompt-disjoint-20261020-v1.json).

To make the release verifiable, the W&B launcher now accepts verified
`prompt_group_sha256` as a partition key. The release uses its system-stripped
variant; the launcher continues to support zero-weight system context in
preserve-system payloads. Both the focused launcher suite and root-level
contract tests pass (14 tests); Ruff check and format pass. Reproducible
builder: `ai/training/build_g04_prompt_disjoint_release.py`. The package is
ready locally but has not been uploaded or launched while W&B artifact quota
remains unknown and the current job is active.

The v10/5,500-batch comparison against base reached 75/120 paired cases (150
successful calls, zero errors) by 01:08 UTC, under its $1.50 cap.
Fireworks Muse Glimmer advanced to step 1,180/10,704 with no new errors. The
active W&B job remains at the last confirmed checkpoint v10/5,500 until the
next watcher/API observation confirms a newer artifact.

Correction/update: the next watcher observation confirmed v11 at 6,000
batches. Both its 112.38 MB adapter and 1,060,414,703-byte train-state were
downloaded and locally backed up. The v10 held-out comparison has reached
80/120 paired cases (159 successful calls; one paired call still pending),
with no recorded errors and $0.08070075 estimated usage so far. Fireworks was
at step 1,186/10,704 at 01:08 UTC.

Adaption's authenticated API refresh confirmed its 522,658-row scalar-text
dataset is still ready, while all three v4-derived runs remain failed before
training on empty validation JSONL or a train-file timeout. Current
non-launching recommendation is Qwen3.6-35B-A3B, one-epoch LoRA rank/alpha 8,
q/v modules, `train_on_inputs=false`, and learning rate 0.0003; it supplies no
quote. The connected API has no balance/price method, and the attempted
read-only UI check was unavailable because the Browserbase session terminated,
there were no local browser pages, and no Browserbase key is configured.
Adaption credit coverage remains unverified; no order was confirmed and no
retry job was launched. See the [Adaption qualification refresh](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md).

#### 2026-10-20 01:13 UTC v10 result and v11 evaluation

The complete v10 comparison returned 240/240 successful calls. Base passed
191/240 synthetic checks; v10 passed 66/240. V10 produced 73 distinct
normalized answers across 120 cases but made no tool calls; it passed 0/75
tool-status, 6/75 response-content, and 0/15 memory-value checks. Base made
144 fixture-tool actions across 87 cases. Estimated usage was $0.11819675
($0.096937 base and $0.02125975 v10); actual billing was unavailable. V10 is
not suitable for agent-tool use or promotion. See the [v10 evaluation
report](execution-2026-10-19/wandb-v10-heldout120-eval-2026-10-20.md).

A 120-case paired comparison of v11/6,000 batches against the same base and
suite is now running with the same $1.50 cap. At launch, the preflight maximum
is $1.3824. Private configuration and results are under
`ai/training/output/wandb_live_checkpoint_eval_20261020/v11-heldout120/`.
Fireworks continued to advance, reaching step 1,253/10,704 at 01:13 UTC with
no new training errors.

#### 2026-10-20 01:15 UTC checkpoint and evaluation follow-up

The W&B v4 job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` advanced to v12 at
6,500 batches. The local LoRA watcher downloaded v12 (112.38 MB); the train-state
watcher last confirmed v11 at 6,000 batches. Both watcher processes remain
active. This confirms that newly created checkpoints are being observed and
backed up; the previously noted 16.326 GB project storage meter did not expose
remaining quota and should not be used to conclude checkpoint writes had
stopped.

The v11/6,000-batch paired evaluation is still running. It has recorded 18 of
120 cases (36 successful model calls) with no errors so far. Its manifest is
still `running`; do not treat partial metrics as final. Fireworks Muse Glimmer
SFT remains active at the last directly observed 1,266/10,704 steps; model
weights are not exportable until completion under this serverless workflow.

W&B Serverless SFT's documented public-preview/free-training status is
confirmed in the provider-terms section above. Inference is separately metered,
and the account's artifact quota remains unknown. No new training job was
launched while the current W&B job and checkpoint backups are active.

Follow-up at 01:15 UTC: the Fireworks worker observed step 1,283/10,704 with
loss 0.9678 and no new errors. The W&B adapter watcher remains current through
v12/6,500 batches; the train-state watcher is still at v11/6,000 batches. The
v11 paired evaluation has 20/120 cases (40 successful calls) recorded and its
manifest remains `running`.

At 01:16 UTC the train-state watcher also completed the v12 download (1,011.29
MB, 11 files), matching the adapter watcher at v12/6,500 batches. Both latest
checkpoint components are now backed up locally. Fireworks was observed at
step 1,296/10,704 with loss 1.172 and no new errors. The v11 evaluation remains
active with 31 of 120 cases recorded (62 result rows, paired base/SFT); results
are partial pending completion.

At 01:17 UTC, Fireworks remained active at step 1,313/10,704 (loss 1.0419),
with no new errors. The W&B v11 evaluation has advanced to 46/120 paired
cases (92 successful calls) and remains in progress. The v12 adapter and
train-state local backups remain the latest confirmed recovery point.

At 01:18 UTC the Fireworks job advanced to step 1,329/10,704 (loss 0.7527),
with no new errors. The v11 evaluation has completed 60/120 pairs (120/240
calls), all successful; its manifest remains `running` and no final comparison
is recorded yet.

At 01:19 UTC Fireworks reached step 1,346/10,704 (loss 1.0413) without new
errors. The paired v11 evaluation reached 72/120 cases (144 successful calls),
with no failed requests; it remains active.

At 01:20 UTC Fireworks reached step 1,362/10,704 (loss 0.5129), with no new
errors. W&B's paired v11 evaluation is at 89/120 cases (178 successful calls)
and is continuing.

At 01:21 UTC Fireworks advanced to step 1,378/10,704 (loss 1.3129) without
new errors. The v11 comparison has 101/120 paired cases (202 successful calls)
recorded, all successful so far.

#### 2026-10-20 01:24 UTC v11 evaluation complete

The complete v11/6,000-batch comparison returned 240/240 successful calls.
The base passed 183/240 synthetic checks; v11 passed 60/240. V11 produced 54
distinct normalized responses across 120 cases and made no fixture-tool calls.
It passed 0/75 `tool_status`, 0/75 `response_contains`, and 0/15
`memory_value` checks; its `state_value` and `response_omits` counts matched the
base at 45/60 and 15/15. The base made 136 fixture-tool actions across 82
cases. Estimated usage was $0.112309 ($0.098168 base and $0.014141 v11); actual
billing was unavailable. V11 is not suitable for agent-tool use or promotion.
See the [v11 evaluation report](execution-2026-10-19/wandb-v11-heldout120-eval-2026-10-20.md).

This confirms the same core failure seen at v9 and v10: continued SFT has not
recovered the target tool behavior. A v12 full evaluation is unlikely to change
the immediate decision without a training/data intervention, so the next useful
step is to preserve the v12 local adapter and train-state checkpoints, inspect
the exact training target/template against the held-out tool-call format, and
use a small diagnostic only after identifying a concrete correction. Do not
start another full evaluation or training job while the current job is active
and storage headroom is unknown.

#### 2026-10-20 v11 failure diagnosis: training payload lacks tool-call examples

The completed v11 comparison and direct source-payload audit explain the main
measured failure. W&B run state binds this checkpoint line to v4 release
`wandb-full-corpus-current-master-20261019-v4`, whose exact train payload SHA is
`60841fbc8d917de4699d1b41eddddf03fade949496db3e561769f94959e37f20`. A
hash-verified re-read found 171,261 rows / 1,056,820 messages: 534,162
assistant and 522,658 user messages. The serialized message keys are only
`role`, `content`, and `weight`; there are zero `tool` or `function` role
messages and zero assistant-native `tool_calls` or `function_call` fields.
The held-out cases require structured function calls and multi-step execution.
This mismatch plausibly explains why v11 made no tool calls; it does not prove
the trainer cannot learn them from correctly formatted examples. Fireworks uses
the same train JSONL and inherits this limitation.

The next useful comparison is a bounded tool-demonstration SFT experiment on
a train split disjoint from the existing held-out prompts, then evaluate base,
full-dialogue SFT, tool-only SFT, and combined SFT under the same suite. The
current 190k break-away release remains available as the dialogue component;
this diagnosis does not invalidate its provenance or research-training use.
W&B docs continue to describe Serverless Training as public preview and state
that preview charges are for inference and artifact storage, not adapter
training ([official W&B Serverless Training docs](https://github.com/wandb/docs/blob/main/serverless-training.mdx)).

#### 2026-10-20 01:26 UTC storage refresh and next eligible W&B dataset

A fresh authenticated W&B GraphQL read returned project `storageBytes` of
19,154,428,829 B at 01:26 UTC, down 97,331,844,424 B from the 22:09 UTC
snapshot. This is evidence that cleanup reduced the project meter while the
current job continued to emit checkpoints. It is not account quota or
remaining-capacity evidence; no checked API exposes those values. See the
[storage snapshot](execution-2026-10-19/wandb-project-storage-snapshot-20261020T0126Z.json).

The next fit-for-purpose W&B dataset is already built locally as
`pixelated-agent-tool-sft-20261019-v1`: 960 train rows, 120 validation rows,
120 test rows, and 1,500 native structured tool-call messages. An independent
temporary rebuild reproduced the train and held-out hashes. It uses synthetic
fictional tools/resources only, with no real-person or external records. Its
960-row package is only 1.43 MB, but the provider's checkpoint artifacts are
much larger than the dataset. Do not upload or start this job while the account
headroom remains unknown and the current full-corpus run is writing checkpoints.
The readiness refresh is in
[`wandb-agent-tool-sft-readiness-2026-10-20.json`](execution-2026-10-19/wandb-agent-tool-sft-readiness-2026-10-20.json).

W&B's official [Serverless Training documentation](https://github.com/wandb/docs/blob/main/serverless-training.mdx)
labels the service public preview and says training is free during preview;
the [Training Pricing page](https://site.wandb.ai/pricing/training/) says
inference and model storage are charged separately under the account plan.
This resolves the training-price question. It does not establish this account's
remaining storage capacity or inference-credit balance.

Checkpoint watcher detail at 01:26 UTC: train-state v13/7,000 batches has
finished local download and is verified by the watcher. The latest adapter
index still reports v12/6,500 batches as of 01:24:47 UTC; the next adapter poll
has not yet confirmed v13. Both watchers and the Fireworks training process
remain active.

At 01:27 UTC Fireworks reached step 1,452/10,704 (loss 1.2437), with no new
errors beyond previously seen nonfatal warnings.

The OpenPipe ART SFT data-format reference confirms that these fields are the
supported format for tool-call conversations: an optional `tools` array,
`tool_calls` on assistant messages, tool-role replies, and a final assistant
message. The existing synthetic release satisfies that shape. See the
[ART SFT format docs](https://art.openpipe.ai/fundamentals/sft-training/).

#### 2026-10-20 01:33 UTC live run and tool-package validation refresh

The W&B Serverless Training status is still **public preview** in its
documentation. The published preview terms say adapter SFT training is free;
inference and artifact storage are charged separately. This is the documented
pricing basis for the experiment, while the live account's storage headroom and
inference credit balance remain unknown.

The active full-corpus W&B job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` remained
`RUNNING` at 01:31:41 UTC. The train-state watcher confirmed v13 / 7,000 batches
(1,060,414,703 bytes); the adapter watcher independently confirmed v13 / 7,000
batches at 01:29:50 UTC. Both local backup watchers remain active. The
Fireworks Muse Glimmer job remained active at step 1,518 / 10,704 at 01:32:14
UTC, loss 0.742; no new errors were reported.

The local-only W&B tool-SFT launcher's dry run now verifies the release and
staged package hashes, 960 training rows, 1,200 structured training tool
calls, 120 validation rows, and 120 held-out test rows. It did not upload data
or create a job. Its split assignment keeps scenario groups disjoint, but the
same user-prompt templates recur across splits: 60 exact prompt hashes (610
train and 90 validation rows) are shared between train/validation, another 60
(610 train and 90 test rows) between train/test, and 40 (70 rows in each split)
between validation/test. These are repeated prompt templates with distinct
scenario IDs and fixture values, not repeated trajectories. Treat this suite
as familiar-template/held-out-scenario evaluation, not unseen-prompt
generalization. Add a paraphrase-based prompt-disjoint evaluation before
claiming generalization. Keep remote submission pending until storage
headroom is established and the active full-corpus job finishes.

#### 2026-10-20 01:35 UTC W&B v13 paired check

W&B's watcher again confirmed the v4 full-corpus job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` as `RUNNING`, now at adapter v13 /
7,000 batches; the local adapter backup is complete. The Fireworks Muse
Glimmer job was live at step 1,563 / 10,704, with no new errors beyond the
known nonfatal warnings. The authenticated W&B project storage meter was
19,154,428,829 B at 01:33 UTC, unchanged from 01:26 UTC. It still does not
reveal account quota or headroom, so no additional training artifact was
uploaded and no second W&B job was started. A fresh Fireworks worker update at
01:35:40 UTC reported step 1,568 / 10,704, loss 1.0544, with no new errors.

The v13 adapter completed the same five-case paired check against the base:
10/10 calls succeeded, estimated inference usage was $0.0047705 under a
$0.05376 preflight maximum, and actual billing was unavailable. Base passed 3/7
deterministic state checks, while v13 passed 2/7; neither made model-issued
tool calls in this short evaluation. The base used local fixtures on four tool
rounds and two base responses hit the output cap. Do not promote v13 for
agent-tool use. See the [v13 evaluation report](execution-2026-10-19/wandb-v13-five-case-eval-2026-10-20.md)
and its private run manifest at
`ai/training/output/wandb_live_checkpoint_eval_20261020/v13-five-case/retry-env/results/manifest.json`.

#### 2026-10-20 01:44 UTC storage entitlement and active-evaluation refresh

An authenticated GraphQL read now distinguishes the W&B account's storage
allowance from this project's `storageBytes` field. Organization
`wutang-org` has an enabled `ACADEMIC_TRIAL` subscription whose privileges
include `storage_gigs: 200`; W&B's published academic plan describes 200 GB of
cloud storage and calculates storage over a trailing 30-day average. The
organization's `LAST_30_DAYS` storage `dailyAverageUsage` is
164,173,686,280 bytes (about 164.2 decimal GB), roughly 82% of the allowance
and about 35.8 GB below it on the same decimal interpretation. The current
project meter is 20,097,108,669 bytes. This does not support a claim that the
W&B organization is currently out of its published storage allowance, though
the headroom is finite and active checkpoint writes can consume it. It does
not report free space on the CoreWeave worker volume. No artifacts were
deleted. The exact read and caveats are in
[`wandb-storage-entitlement-refresh-20261020T0144Z.json`](execution-2026-10-19/wandb-storage-entitlement-refresh-20261020T0144Z.json).

The v4 full-corpus W&B job remains `RUNNING`; at 01:44:55 UTC its local
verified adapter and train-state mirrors both contained v14 / 7,500 batches.
The fixed v13-checkpoint-versus-base 120-case held-out paired evaluation is
also still running: 150 of 240 arm/case results were written by 01:44:34 UTC.

That paired evaluation completed at 01:48 UTC with 240/240 successful calls.
On the 120 deterministic synthetic cases, the base made tool calls in 86 cases
(136 rounds) and passed 69/75 tool-status checks; the v13 adapter made no tool
calls and passed 0/75. Response-content checks were 56/75 for base and 0/75
for v13; response-omission checks were 15/15 for both. State-value checks were
46/60 and 45/60, and memory-value checks were 6/15 and 0/15, base versus v13.
The usage-based cost estimate was $0.1100685 under the $1.50 hard cap; actual
billing remains unknown. These deterministic checks do not establish clinical
quality or safety. Do not promote v13 for agent-tool use. Full breakdown:
[v13 held-out 120-case report](execution-2026-10-19/wandb-v13-heldout120-eval-2026-10-20.md).

The synthetic agent-tool SFT launcher's local integrity checks passed and its
1.43 MB dataset artifact uploaded as `agent-tool-sft-036a97a69a41:v0`. Model
creation then timed out at 60 seconds, leaving durable state at
`model_creation_submitted_unknown`; there is no model ID or training-job ID.
A later recognized-client catalog request returned 13 base models, but
idempotent model-create calls still timed out. A finished W&B project run
exists with the deterministic model name, but exposes no model UUID. The
documented W&B/Forge dashboard redirects to a login screen in the current
unauthenticated browser session. No training job has been created; recover the
model UUID and submit through W&B owner support or an authenticated UI. The
uploaded dataset is reusable. See the [launch reconciliation report](execution-2026-10-19/wandb-agent-tool-sft-launch-reconciliation-20261020.md).

The old v13 result was then checked on a separate, 120-case surface-form-
disjoint suite generated from the same synthetic fixture/state cases. The
suite has 120 unique paraphrased user prompts and zero exact prompt overlap
with the dedicated tool-SFT training split; preflight validated it with no
provider calls. The paired run completed all 240 calls: base made tool calls
in 85/120 cases and passed 71/75 tool-status checks, while v13 made no tool
calls and passed 0/75. The adapter also passed 0/75 response-content checks;
base passed 60/75. Estimated usage cost was $0.1074965 under the $1.50 cap;
actual billing is unknown. This confirms the negative tool-use result does not
depend on exact prompt reuse, while remaining a synthetic diagnostic rather
than a quality or safety evaluation. See the [prompt-disjoint results](execution-2026-10-19/wandb-v13-prompt-disjoint120-eval-2026-10-20.md)
and reproducible suite builder at `ai/training/build_agent_tool_prompt_disjoint_eval.py`.
The manifest inherited the original run label; the case SHA and result directory
uniquely identify this second run.

The newest locally verified full-corpus checkpoint v16 (8,500 batches) was
then evaluated against the same base on the same prompt-disjoint suite. All
240 calls succeeded. V16 still made zero tool calls and passed 0/75
tool-status checks; it did pass 15/75 response-content checks versus v13's
0/75 on the same cases, while base passed 73/75 tool-status and 59/75
content checks. Both SFT checkpoints passed 45/60 state-value checks and
0/15 memory-value checks. Estimated cost was $0.106166 under the $1.50 hard
cap; actual billing remains unknown. Additional full-corpus SFT through v16
has not restored tool calling, so do not promote it for agent-tool use. See
the [v16 paired report](execution-2026-10-19/wandb-v16-prompt-disjoint120-eval-2026-10-20.md).

#### 2026-10-20 02:03 UTC storage and checkpoint refresh

A fresh authenticated W&B GraphQL read returned project storage of
21,984,664,898 bytes, up 1,887,556,229 bytes from 01:44:34 UTC. The
organization-level trailing 30-day storage average remained
164,173,686,280 bytes against `storage_gigs: 200`; this is close enough to
monitor, but remains below the 200 GB allowance. The project growth is
consistent with active checkpoint writes. It does not indicate the state of
the CoreWeave worker's own disk. The latest local mirrors show v4 at adapter
and train-state v16 / 8,500 batches at 02:00–02:02 UTC; all verified adapter
files are locally preserved. See
[`02:03 storage snapshot`](execution-2026-10-19/wandb-storage-entitlement-refresh-20261020T0203Z.json).

At 02:18 UTC, a further read-only GraphQL refresh measured project storage at
22,927,341,062 bytes, up 942,676,164 bytes from 02:03. Organization
trailing-average usage stayed at 164,173,686,280 bytes against the 200 GB
entitlement. This confirms continued project artifact growth while the account
remains below its measured average-storage allowance; it does not report worker
disk space. No artifacts were deleted. See the private
[`02:18 storage snapshot`](execution-2026-10-19/wandb-storage-entitlement-refresh-20261020T0218Z.json).

#### 2026-10-20 01:37 UTC Adaption access and quote refresh

At 01:37:34 UTC, authenticated read-only Adaption API calls reconfirmed all
three 522,658-row v4-derived datasets are ready and the three ctx9 jobs remain failed
at 0/1 with empty generated validation JSONL. The full-history attempt remains
failed on its 60-second S3 train download; the 11,192-row control remains
succeeded and downloadable after one iteration. Qwen3.6-35B-A3B is still
available for SFT/DPO LoRA. The scalar-text dataset's fresh non-launching
recommendation remains rank/alpha 8, q/v, one epoch, LR 0.0003, batch max,
completion-only loss; it returned no quote or balance.

The current connector exposes no price quote, account balance, or billing
history operation. `recommend_hyperparams` is recipe-only; AutoScientist
`create` launches a credit-spending job and was not called. `datasets.adapt`
can estimate Adaptive Data transformation only, not the training job. Official
docs identify the app's final order-summary page as the training-price preview,
with separate optional expansion lines. Browserbase start returned
`Session terminated`, so that UI quote and current balance were not reachable.
No quote/coverage is claimed, and no upload, job, or message was created/sent.
See the [timestamped API evidence](execution-2026-10-19/adaption-live-refresh-20261020T0137Z.json).

#### 2026-10-20 W&B Serverless Training preview wording rechecked

The published [Serverless Training docs](https://github.com/wandb/docs/blob/main/serverless-training.mdx)
still explicitly state that Serverless Training is in public preview and that
adapter training is not charged during preview, while inference and artifact
storage are charged. The docs repository banner says it was archived on
September 30, 2026. This confirms the documented offer language; the archive
date and Forge pricing redirect leave current account-level applicability and
post-migration billing unverified. This does not change the active job status
or invalidate the already-created training runs.

#### 2026-10-20 v17 prompt-disjoint evaluation

The v17 checkpoint (9,000 batches) completed a 120-case paired run against the
base, with 240/240 successful calls and estimated usage of `$0.06658075`
under the `$1.50` cap; actual billing is unknown. This first run used
`max_tool_rounds=0`: base emitted model tool-call responses in 88/120 cases,
v17 emitted none, but no tool execution occurred and tool-status scores are
not comparable with the prior four-round v13/v16 runs. Base passed 8/75
response-content checks, v17 15/75; both passed 45/60 state checks, 0/15
memory checks, and 15/15 omission checks. A separate four-round evaluation
with matching v13/v16 settings has now started. The no-tool-execution results
are documented in the [v17 diagnostic report](execution-2026-10-19/wandb-v17-no-tool-execution-prompt-disjoint120-eval-2026-10-20.md)
and private outputs at
`ai/training/output/wandb_live_checkpoint_eval_20261020/v17-prompt-disjoint-heldout120/`.

#### 2026-10-20 v17 comparable four-round evaluation completed

The v17 9,000-batch checkpoint's prompt-disjoint 120-case paired evaluation
completed with four local mock-tool rounds enabled, matching v13/v16 settings.
All 240 calls succeeded; estimated inference usage was `$0.1078285` under a
`$1.50` hard cap, with actual billing unavailable. Base passed 74/75
 tool-status checks and invoked 137 local tool rounds across 87 cases; v17
passed 0/75 and made no tool rounds. Base/v17 response-content checks were
56/75 and 14/75; memory-value 6/15 and 0/15; state-value 45/60 for both; and
response-omission 14/15 and 15/15. Do not promote v17 for agent-tool use based
on this diagnostic. Full reproduction details are in the [v17 four-round
evaluation report](execution-2026-10-19/wandb-v17-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

#### 2026-10-20 02:39 UTC live checkpoint and provider refresh

The W&B v4 job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` remains
`RUNNING`. Its two live local backup processes are active; the latest mirrored
adapter and train-state artifacts are both v19 at 10,000 completed batches.
The adapter backup is about 118 MB and train-state backup about 1.06 GB. The
local filesystem holding these backups reports 75 GB available; this is local
disk headroom and does not measure W&B/CoreWeave storage quota. A prompt-
disjoint paired comparison of v19 versus the base has been launched with the
same four-round evaluator, 2,048-token input preflight, and `$1.50` hard cap;
its first 50/240 arm-case records were written with the manifest still
`running` at the observation time. Do not report partial metrics as final.

Fireworks Muse Glimmer remains live in process 518909, observed at 2,462 of
10,704 steps at 02:38:59 UTC, with no new errors beyond known nonfatal
warnings. W&B v17 four-round evaluation is complete and documented above. The
newest Adaption API refresh reconfirmed all three 522,658-row v4-derived datasets as
ready, but their three associated runs failed before training on an empty
generated validation JSONL; the full-history run failed on an S3 download
timeout. Adaption still exposes no account balance or training-price quote.
A structural diagnosis is in progress without launching another credit-spending
run.

#### 2026-10-20 v19 prompt-disjoint four-round evaluation completed

The 10,000-batch W&B v19 checkpoint completed the same 120-case prompt-
disjoint paired evaluation as v13/v16/v17, with four local mock-tool rounds.
All 240 calls succeeded; estimated inference usage was `$0.10833075` under a
`$1.50` hard cap and actual billing remains unavailable. The base passed 73/75
tool-status and 59/75 response-content checks; v19 passed 0/75 on both and
made no tool rounds. Memory-value was 5/15 vs 0/15, state-value 45/60 for both,
and response-omission 11/15 vs 15/15. V19's 0/75 content result is below v17's
14/75 under the same protocol. Do not promote v19 for agent-tool use. Details
and hashes are in the [v19 evaluation report](execution-2026-10-19/wandb-v19-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

#### 2026-10-20 v20 prompt-disjoint four-round evaluation completed

The 10,500-batch W&B v20 checkpoint completed the 120-case prompt-disjoint
paired evaluation with four local mock-tool rounds. All 240 calls succeeded;
estimated inference usage was `$0.1061105` under a `$1.50` hard cap and actual
billing remains unavailable. The base passed 72/75 tool-status and 60/75
response-content checks; v20 passed 0/75 on both and made no tool rounds.
Memory-value was 6/15 vs 0/15, state-value 45/60 for both, and
response-omission 13/15 vs 15/15. V20's 0/75 content score matches v19 and is
below v17's 14/75 under the same protocol. Do not promote v20 for agent-tool
use. See the [v20 evaluation report](execution-2026-10-19/wandb-v20-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

#### 2026-10-20 v21 prompt-disjoint four-round evaluation completed

The 11,000-batch W&B v21 checkpoint completed the same 120-case prompt-
disjoint paired evaluation with four local mock-tool rounds. All 240 calls
succeeded; estimated inference usage was `$0.1080695` under a `$1.50` hard
cap, with actual billing unavailable. The base passed 73/75 tool-status and
56/75 response-content checks; v21 passed 0/75 tool-status and 12/75
response-content checks. Base made 135 local tool rounds across 88 cases; all
146 mock-tool calls returned `ok`. Memory-value was 6/15 for base and 0/15 for
v21; state-value was 45/60 for both; response-omission was 13/15 and 15/15.
V21's content result improves on v19/v20's 0/75, but it still made no tool
rounds and is not suitable for agent-tool use. Details and hashes are in the
[v21 evaluation report](execution-2026-10-19/wandb-v21-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

Across the six comparable prompt-disjoint checkpoints, the adapter made no
tool rounds and passed 0/75 tool-status checks each time. Response-content
checks were 14/75 at v17, 0/75 at v19, 0/75 at v20, 12/75 at v21, and 0/75 at
v22 and v23. The base scored 52-60/75 across these separate inference runs;
its variation cautions against overreading small checkpoint-to-checkpoint
deltas. This diagnostic supports a persistent tool format/capability gap;
v21's partial content recovery did not persist and does not change the
no-promotion decision. See the [v23 four-round evaluation report](execution-2026-10-19/wandb-v23-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

#### 2026-10-20 03:11 UTC live training and checkpoint refresh

The active W&B full-corpus job remains `RUNNING`. Its adapter and train-state
watchers have both downloaded v22 at 11,500 completed batches; the local
train-state copy is about 1.06 GB. These are separate local backups, and no
remote artifacts were deleted. Fireworks Muse Glimmer remains active at step
3,088/10,704 as of 03:24 UTC, with no new errors beyond the known nonfatal
warnings. The v21 and v22 120-case paired evaluations are complete under their
individual `$1.50` estimated-cost ceilings; a further bounded watcher now
checks each of at most 20 new W&B checkpoints against the base on the five-case
synthetic suite, at no more than `$0.06` per comparison. Fireworks' serverless
workflow still has no periodic local tuned-weight export in this run; its
end-of-run result remains an experiment-only checkpoint unless a supported
export route is verified.

At 03:27 UTC a fresh authenticated GET for the W&B job returned `RUNNING`,
with `progress: null`, no `total_steps`, and no completion timestamp. The
service response reports a training start at 2026-10-19 22:50:52 UTC, but its
`updated_at` did not advance with the artifact checkpoints. For progress, use
the authenticated cursor-paginated `/preview/training-jobs/{id}/events` route,
which exposes `gradient_step` and `num_gradient_steps`; the job-status GET
itself still omits usable progress. The documented API overview lists the
events route ([W&B Training API overview](https://docs.wandb.ai/training/api-reference)).
The events establish step progress, but provide no checkpoint-upload progress
or reliable completion-time estimate.

#### 2026-10-20 03:30 UTC checkpoint and training refresh

An authenticated query of both exact v4 W&B collections still returns adapter
v22 and train-state v22 as the newest published versions, each with metadata
`sft_completed_batches=11500`. Their local mirrors agree; no newer version was
available to back up or evaluate as of 03:30 UTC. Both backup processes remain
alive. The W&B training-job endpoint still reports `RUNNING`, but its progress
fields are null and `updated_at` remains 2026-10-19 22:50:52 UTC. This does not
establish whether a newer checkpoint save is in progress; it only confirms no
new artifact has been published yet. Fireworks continued training through
step 3165/10704 by 03:30 UTC, with no new errors beyond previously noted
warnings. The five-case watcher session is still pollable, but its state has
not recorded an evaluation beyond v22; verify it again when a new artifact is
published.

At 03:31 UTC, another authenticated query of all project `lora` and
`train-state` collections found no newer artifact for the active v4 job (or a
recently advancing alternative run). The v4 v22 adapter and train-state were
created at 03:06:31Z and 03:06:33Z, respectively, and both remain at 11,500
batches. The adapter watcher polled again at 03:31:02Z with no lookup error;
the train-state watcher process remains alive. Fireworks reached step
3182/10704 at 03:31:23Z. The live five-case watcher session remains pollable;
its persisted state is unchanged because no v23 has appeared.

At 03:32 UTC the W&B adapter watcher continued polling v4 and still reported
v22 / 11,500 batches with `RUNNING`; the artifact creation timestamps remained
03:06 UTC on the authenticated collection query. Fireworks reached step
3198/10704 at 03:32:31Z, with no new errors reported.

At 03:37 UTC, a complete cursor-paginated W&B events read showed 11,891 of
85,631 gradient steps, with training loss 1.9311. This confirms the training
job had advanced 391 steps past the latest published v22 artifact at 11,500
batches. The job GET still returned `RUNNING`, no error/end time, and a stale
`updated_at`; v23 had not appeared. Repeated event reads found no newer step
for about 1.5 minutes, which is not enough to establish a failure. No exposed
read-only endpoint reports whether an artifact upload is in progress. A new
private progress observer now records event cursors and current step at
`ai/training/output/wandb_local_checkpoints_20261019/v4-training-progress.json`;
its live process is tracked in exec session 82822. Fireworks reached step
3264/10704 at 03:37:09Z.

At 03:39:46Z the event observer received 13 new W&B events and advanced to
gradient step 11,904/85,631, confirming the earlier short no-event window was
not a terminal stall. The latest published adapter remains v22/11,500 at the
03:36 artifact poll. Fireworks reached step 3,296/10,704 at 03:39:24Z.

#### 2026-10-20 v22 prompt-disjoint four-round evaluation completed

The 11,500-batch W&B v22 checkpoint completed the same 120-case prompt-
disjoint paired evaluation with four local mock-tool rounds. All 240 calls
succeeded; estimated usage was `$0.10732775` under the `$1.50` hard cap and
actual billing is unavailable. The base passed 71/75 tool-status and 52/75
response-content checks; v22 passed 0/75 on both and made no tool rounds. The
base made 130 local rounds across 85 cases; all 141 mock-tool calls returned
`ok`. Memory-value was 5/15 for base and 0/15 for v22; state-value was 45/60
for both; response-omission was 13/15 and 15/15. V21's 12/75 response-content
result did not persist in v22. Do not promote v22 for agent-tool use. See the
[v22 evaluation report](execution-2026-10-19/wandb-v22-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

The five-case `synthetic_capability_v1` suite also ran against v19-v23 and the
same base, with two local mock-tool rounds. Across v19-v23 and two v23 repeats,
all 60 calls succeeded at an estimated combined usage of `$0.0281405` (actual
billing unknown). The base returned nonempty content in 3/5 cases and passed
3/7 deterministic checks in each run. SFT nonempty response counts were v19
1/5, v20 0/5, v21 5/5, v22 3/5, and v23 2/5 then 3/5 on repeat. None made
local tool rounds, and each passed 2/7 checks. The response variation and
failed positive tool task do not support promotion. See the [combined
five-case report](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md)
and [v23 repeat report](execution-2026-10-19/wandb-v23-five-scenario-dev-eval-2026-10-20.md).

#### 2026-10-20 03:33 UTC Adaption access recheck

Seven authenticated read-only Adaption connector calls reconfirmed that
Qwen/Qwen3.6-35B-A3B is available for LoRA SFT/DPO and that historical run 2
(`8da8f685-7ef6-43c0-958e-ab34dbdcd520`) succeeded with `download_available`
true. Its 46 MB adapter is already present locally. The latest 522,658-row
import (`60ea43c8-c965-4ab1-968a-b4b82be7703d`) is `awaiting_input`: its
physical `prompt` and `completion` columns are present but canonical column
mappings and processed-row count are null. Three recent runs on registered
522,658-row datasets failed before iteration 0 on an empty validation JSONL;
the full-history attempt separately timed out downloading its S3 train file
after 60 seconds. The connector exposes no balance, expiry, per-run cost,
local-file upload, or checkpoint-byte download operation. No new dataset or
training run was launched. The detailed current evidence and next actionable
fixes are recorded in
[`provider-qualification.json`](execution-2026-10-17/provider-qualification.json).

#### 2026-10-20 03:45 UTC v23 backup and evaluation

W&B published adapter and train-state artifacts v23 at 12,000 completed
batches (created 03:41:40Z and 03:41:42Z). Both were downloaded and verified
locally: the adapter is 117,842,120 bytes and the train-state artifact is
1,060,414,703 bytes. The five-case paired diagnostic ran twice against the
same base; v23 made no mock-tool rounds and passed 2/7 deterministic checks in
both runs, while nonempty response count varied from 2/5 to 3/5. No promotion
is supported; see the v23 reports above.

A larger 120-case prompt-disjoint paired evaluation against v23 and the base
is running with up to four local mock-tool rounds, a 2,048-token input cap,
and a `$1.50` hard ceiling. At the 03:46 UTC check, 56/240 calls had completed
successfully with no errors. Estimated usage so far was `$0.02967575`; the
preflight maximum is `$1.3824`. Partial quality metrics are not reported.
The event observer advanced the W&B job to gradient step 12,209/85,631 at
03:45:49Z; the newest adapter artifact is still v23/12,000 as of 03:46:06Z.
Fireworks reached step 3,373/10,704 at 03:45:21Z, with no new errors reported.

#### 2026-10-20 03:49 UTC live refresh

The v23 prompt-disjoint evaluation remains `running`: 158/240 paired calls
have completed, all successful, with estimated usage `$0.072472` against the
`$1.50` hard cap (the preflight maximum remains `$1.3824`). Do not report
partial quality metrics. The W&B event observer advanced to gradient step
12,369/85,631 at 03:48:51Z, with 54 new events in that poll and no job error.
Both local checkpoint backup processes remain alive; adapter v23 and train
state v23 / 12,000 batches remain the latest published versions as of
03:48:03Z. Fireworks reached step 3,422/10,704 at 03:48:50Z, with no new
errors reported.

#### 2026-10-20 v23 prompt-disjoint four-round evaluation completed

The 12,000-batch v23 checkpoint completed the same prompt-disjoint 120-case
paired evaluation. All 240 calls succeeded at an estimated `$0.10846125` under
the `$1.50` cap; actual billing is unverified. V23 made no local tool rounds
and passed 0/75 tool-status and 0/75 response-content checks, though all 120
outputs were nonempty. The base made 137 rounds across 87 cases and passed
73/75 tool-status and 60/75 response-content checks. Both arms passed 45/60
state-value checks. V23 passed 15/15 omission checks versus 14/15 for base;
its lower latency does not compensate for the missing tool behavior. Do not
promote v23 for agent-tool use. Full metrics and reproduction hashes are in
the [v23 evaluation report](execution-2026-10-19/wandb-v23-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

#### 2026-10-20 03:55 UTC v24 checkpoint and next evaluation

W&B published adapter and train-state v24 at 12,500 completed batches. Both
are now backed up locally and re-hashed against their manifests: the adapter
is 117,843,308 bytes across two files; the train-state is 1,060,414,703 bytes
across 11 files. The initial manual train-state download raced the scheduled
watcher's shared artifact cache, but the watcher completed v24; the local
copies and per-file hashes now verify cleanly. The W&B event observer most
recently reports step 12,680/85,631, status `RUNNING`, no job error (03:54:54Z).
The bounded five-case v24-vs-base diagnostic has started with the same frozen
suite, 2,048-token input cap, two local tool rounds, and `$0.06` hard cap; its
result is pending. The Fireworks Muse Glimmer job reached step 3,504/10,704 at
03:54:38Z, with no new errors beyond prior warnings.

The v24 five-case comparison has completed: all 10 calls succeeded at an
estimated `$0.00477675` under its `$0.06` cap. V24 returned nonempty content
in 4/5 cases, made no local tool rounds, and passed 2/7 checks; the base made
four rounds and passed 3/7. The result does not justify promotion; see the
[v24 five-case report](execution-2026-10-19/wandb-v24-five-scenario-dev-eval-2026-10-20.md)
and [updated v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md).
A matching 120-case prompt-disjoint v24-vs-base evaluation is now running
under the same protocol as v23, with a `$1.50` hard ceiling and `$1.3824`
preflight maximum. At 03:56 UTC, 4/240 calls succeeded without errors and
estimated usage was `$0.00265025`; partial quality metrics are not reported.
The W&B event observer advanced to step 12,733/85,631 at 03:55:54Z, still
`RUNNING` with no job error. Fireworks reached step 3,520/10,704 at
03:55:45Z, with no new errors beyond prior warnings.

An independent current-master reconciliation resolves the earlier dataset
count concern: 190,139 was the Oct. 17 recovery snapshot; the frozen Oct. 19
v4 candidate is 190,244 rows. All 189,159 non-ARC rows match exactly; the ARC
slice grew from 980 to 1,085 rows, with 91 already in the pre-completion v3
master and 14 added by v4 from the six completed arcs. The 171,261 training
rows plus 9,673 validation and 9,310 test rows account for the entire v4
candidate. All 190,244 source row references and group-disjoint split checks
recomputed successfully. See the [reconciliation report](execution-2026-10-19/dataset-size-reconciliation-2026-10-20.md).

At 04:01 UTC, the larger v24 prompt-disjoint run had completed 206/240 calls,
all successfully, at estimated usage `$0.0914` under the `$1.50` cap; partial
quality metrics remain withheld. W&B training had advanced to 13,000/85,631
gradient steps at 04:00:57Z, `RUNNING` with no job error. Fireworks reached
step 3,588/10,704 at 04:00:34Z, with no new errors reported.

#### 2026-10-20 v24 prompt-disjoint four-round evaluation completed

The 12,500-batch v24 checkpoint completed the same 120-case paired evaluation.
All 240 calls succeeded at estimated usage `$0.10812325` under the `$1.50`
cap; actual billing is unverified. V24 made no local tool rounds and passed
0/75 tool-status and 0/75 response-content checks; it returned nonempty text
in only 55/120 cases. Base passed 72/75 tool-status and 61/75
response-content checks and made 136 local rounds across 87 cases. Do not
promote v24 for agent-tool use. Full metrics and hashes are in the [v24
evaluation report](execution-2026-10-19/wandb-v24-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

At 04:02:58Z the W&B event observer advanced the active job to 13,100/85,631
gradient steps, still `RUNNING` with no job error. Adapter v24 and matching
train-state v24 (12,500 batches) are both locally preserved with verified
per-file hashes. Fireworks remained active at step 3,617/10,704 at
04:02:53Z; its tuned sampler checkpoint is still not verified, so that run
remains experiment-only.

#### 2026-10-20 v25 checkpoint, evaluation, and source binding

At 04:03:59Z the W&B event observer advanced the active full-corpus job to
13,155/85,631 gradient steps (`RUNNING`, no job error). The adapter and
matching train-state v25 checkpoint (13,000 batches) were saved locally and
their file hashes verified by the backup watchers. The automatic five-case
paired evaluation completed 10/10 inference calls under its `$0.06` cap
(estimated usage `$0.004738`; actual billing unverified). V25 returned
nonempty content in 5/5 cases, made no local tool rounds, and passed 2/7
deterministic checks; the base made four local rounds and passed 3/7. This
small synthetic suite does not support promotion for agent-tool use or establish
clinical quality/safety. See the [v25 evaluation report](execution-2026-10-19/wandb-v25-five-scenario-dev-eval-2026-10-20.md).

The Reddit Mental NLP source-status audit now binds 58,409 of 70,968 v4 rows
uniquely to the locally available, hash-pinned CSV (28,894 exact and 29,515
normalized-only). Duplicate alternatives, 12,122 unmatched rows, missing
curation-time export/version evidence, and absent stable post IDs remain
explicit; no rights, privacy, clinical-review, or provider-transfer clearance
is inferred. See the [row-level origin audit](execution-2026-10-19/reddit-mental-nlp-v4-complete-origin-status-audit-2026-10-20.md).

A newly found public, processed PsychEval dataset was also checked at immutable
revision `35ff3f0ee271946d9d8dd63a16fe79a0c760f4f4`. Exact and normalized
ordered-turn comparisons found no match to any of the 1,977 v4 PsychEval rows;
the public derivative does not resolve the adapter-declared source lineage.
See the [updated PsychEval availability audit](execution-2026-10-19/psycheval-v4-source-availability-prompt-crosssplit-2026-10-20.md).

The 120-case prompt-disjoint v25 comparison also completed: 240/240 calls
succeeded at estimated usage `$0.11033225` under the `$1.50` cap (actual
billing unverified). V25 made no tool rounds and passed 0/75 positive
tool-status/content checks; the base made 138 rounds across 88 cases and
passed 73/75 tool-status and 61/75 response-content checks. See the [v25
held-out evaluation report](execution-2026-10-19/wandb-v25-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

The Fireworks launcher remains live. A corrected read-only query against the
training-session checkpoint listing (04:17:45Z) found only its promotable base
sampler; there is no tuned sampler yet. The earlier HTTP 404 came from querying
the RLOR checkpoint endpoint with a serverless session ID, so it was not
evidence of a failed run. Fireworks is at step 3,828/10,704 and saves its tuned
sampler only after training completes, with no periodic tuned sampler exports;
until that final artifact is confirmed, this run is experiment-only.

#### 2026-10-20 04:17 UTC W&B v26 and checkpoint-storage clarification

W&B's event observer reports 13,849/85,631 gradient steps at 04:17:05Z,
`RUNNING`, with no job error. This is direct step-event evidence; the job
metadata `updated_at` remains stale at 2026-10-19 22:50:52Z and should not be
used alone as a progress signal. The adapter watcher published v26 at 13,500
batches (04:16:23Z), and the train-state watcher has the matching v26 at 13,500
batches (04:14:14Z). Both are backed up locally. Recomputed SHA-256 and byte
size checks passed for all two adapter files and all eleven train-state files.
Thus checkpoint creation and local preservation are both confirmed through
v26; a storage concern should be assessed against those actual artifacts and
the next watcher polls, not inferred from a stale job metadata timestamp.

The v26 five-case paired evaluation completed 10/10 calls at estimated usage
`$0.00471925` under the `$0.06` cap (actual billing unknown). V26 produced
nonempty text in 5/5 cases but made no local tool rounds, passing 2/7 checks;
the base made four rounds and passed 3/7. The [v26 evaluation](execution-2026-10-19/wandb-v26-five-scenario-dev-eval-2026-10-20.md)
and [updated v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md)
do not support promotion for agent-tool use.


#### 2026-10-20 04:26 UTC W&B v26 held-out evaluation and v27 storage

The 13,500-batch v26 adapter completed the prompt-disjoint 120-case paired
evaluation. All 240 inference calls succeeded at estimated usage `$0.1089255`
under the `$1.50` ceiling; actual billing is unverified. V26 returned nonempty
text in 120/120 cases, made no local tool rounds, and passed 0/75 tool-status,
4/75 response-content, 0/15 memory-value, 45/60 state-value, and 15/15
response-omission checks. Base returned nonempty text in 97/120 cases, made 128
local rounds across 84 cases, and passed 71/75 tool-status, 55/75
response-content, 6/15 memory-value, 45/60 state-value, and 14/15
response-omission checks. V26 is faster and more consistently nonempty, but its
continued failure to execute tools rules it out for agent-tool promotion on
this evidence. See the [v26 120-case report](execution-2026-10-19/wandb-v26-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

The W&B event observer reports 14,330/85,631 gradient steps at 04:26:10Z,
`RUNNING`, with no job error. The adapter watcher has published v27 at 14,000
batches (04:21:28Z); the matching train-state v27 was downloaded at 04:24:35Z.
Both local backups were re-hashed: all two adapter files and all eleven
train-state files match their manifests. This is direct confirmation that
checkpoints continued to be created and preserved while the job advanced;
latest provider artifacts are available locally through v27.


The five-case watcher also evaluated the newly preserved v27 checkpoint: all
10 paired calls succeeded at estimated `$0.0047455` (actual billing
unverified). V27 returned nonempty text in all five cases but made no local
tool rounds and passed 2/7 checks; the base made four rounds and passed 3/7.
The [v27 report](execution-2026-10-19/wandb-v27-five-scenario-dev-eval-2026-10-20.md)
and [updated v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md)
show no tool-use improvement.


The 14,000-batch v27 adapter also completed the 120-case prompt-disjoint
comparison: 240/240 calls succeeded at estimated usage `$0.109752` under the
`$1.50` ceiling (actual billing unverified). V27 returned nonempty text in
120/120 cases but made no tool rounds and passed 0/75 tool-status, 0/75
response-content, and 0/15 memory-value checks. The base made 135 rounds
across 87 cases and passed 73/75 tool-status and 59/75 response-content
checks. The [v27 held-out report](execution-2026-10-19/wandb-v27-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md)
confirms v27 is not suitable for agent-tool promotion.

W&B has since published adapter and train-state v28 at 14,500 batches. The
adapter was observed at 04:31:33Z and train-state downloaded at 04:35:02Z;
local SHA-256/size checks passed for both files in the adapter manifest and all
eleven train-state files. The event observer reports 14,814/85,631 steps at
04:35:14Z, still `RUNNING` without a job error. Fireworks remains active at
step 4,067/10,704 at 04:35:01Z, without new errors.


The five-case watcher has also completed v28: 10/10 calls succeeded at estimated
usage `$0.0059705` (actual billing unverified); v28 returned nonempty text in
5/5 cases but made no local tool rounds and passed only 2/7 checks, while base
passed 3/7 and made four rounds. See the [v28 report](execution-2026-10-19/wandb-v28-five-scenario-dev-eval-2026-10-20.md)
and [updated v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md).


04:36 UTC follow-up: W&B's event endpoint advanced to 14,869/85,631 steps at
04:36:15Z, with status `RUNNING` and no error; adapter backup watcher confirms
v28 remains the latest published version at 14,500 batches. The v28 five-case
comparison completed with no tool calls (10/10 inference calls, estimated
`$0.0059705`). Fireworks reached step 4,078/10,704 at 04:36:11Z, still active
with no new errors.


The 14,500-batch v28 adapter completed the 120-case prompt-disjoint paired
evaluation: 240/240 calls succeeded at estimated usage `$0.10818225` under the
`$1.50` hard ceiling (actual billing unverified). V28 returned nonempty text in
120/120 cases but made no tool rounds and passed 0/75 tool-status, 0/75
response-content, and 0/15 memory-value checks. The base made 133 rounds and
passed 71/75 tool-status and 62/75 response-content checks. The [v28 held-out
report](execution-2026-10-19/wandb-v28-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md)
shows that the same tool-use limitation persists.

W&B published adapter v29 and matching train-state at 15,000 batches; the
adapter watcher observed it at 04:41:37Z and train-state at 04:40:25Z. Local
SHA-256 and byte-size checks passed for both adapter files and all eleven
train-state files. At 04:44:19Z the event stream was at 15,303/85,631 gradient
steps, `RUNNING`, without a job error. Fireworks remained active at step
4,207/10,704 at 04:45:22Z, with no new errors.


The automatic five-case watcher has evaluated v29: all 10 paired calls succeeded
at estimated usage `$0.004893`; v29 returned nonempty text in 5/5 cases but made
no local tool rounds and passed 2/7 checks, while base made four rounds and
passed 3/7. The [v29 report](execution-2026-10-19/wandb-v29-five-scenario-dev-eval-2026-10-20.md)
and [updated v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md)
show no improvement in tool use through 15,000 batches.


The 15,000-batch v29 adapter completed the 120-case prompt-disjoint paired
evaluation: 240/240 calls succeeded at estimated usage `$0.10873925` under the
`$1.50` hard ceiling (actual billing unverified). V29 returned nonempty text in
120/120 cases but made no tool rounds and passed 0/75 tool-status, 0/75
response-content, and 0/15 memory-value checks. The base made 137 rounds across
88 cases and passed 73/75 tool-status and 60/75 response-content checks. See
the [v29 held-out report](execution-2026-10-19/wandb-v29-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).


The five-case watcher has completed v30 at 15,500 batches: 10/10 calls succeeded
at estimated usage `$0.0047105`; v30 made no local tool rounds and passed 2/7
checks, while the base made four rounds and passed 3/7. The [v30 report](execution-2026-10-19/wandb-v30-five-scenario-dev-eval-2026-10-20.md)
and [updated v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md)
show no tool-use improvement through this checkpoint.


The v30 120-case prompt-disjoint comparison is complete: 240/240 calls
succeeded at estimated usage `$0.1063835` under the `$1.50` ceiling (actual
billing unverified). V30 returned nonempty text in 120/120 cases but made no
tool rounds and passed 0/75 tool-status, 0/75 response-content, and 0/15
memory-value checks. Base made 134 rounds across 86 cases and passed 71/75
tool-status and 63/75 response-content checks. See the [v30 held-out report](execution-2026-10-19/wandb-v30-prompt-disjoint-toolrounds4-heldout120-eval-2026-10-20.md).

W&B's 16,000-batch v31 adapter and train-state were downloaded and verified
against their manifests: both adapter files and all eleven train-state files
pass SHA-256 and size checks. Latest event observation is 16,227/85,631 steps
at 05:01:36Z, `RUNNING`, without error. Fireworks is still live at step
4,445/10,704 as of 05:02:27Z, with no new errors.


The v31 five-case watcher completed all 10 calls at estimated usage `$0.00476925`;
the adapter produced no nonempty response, made no tool rounds, and passed
only 2/7 deterministic checks. The [v31 evaluation](execution-2026-10-19/wandb-v31-five-scenario-dev-eval-2026-10-20.md)
and [v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md)
show inconsistent output and no tool-use improvement through 16,000 batches.


05:04 UTC: the W&B observer advanced to 16,390/85,631 steps at 05:04:38Z,
`RUNNING`, no job error. Adapter and train-state backups remain verified
through v31 (16,000 batches). Fireworks reached step 4,473/10,704 at
05:04:27Z, also active without new errors; its correct session checkpoint
listing still has only the base sampler, with the tuned sampler deferred until
training completes.


05:08 UTC follow-up: W&B's event endpoint reports 16,544/85,631 gradient
steps, `RUNNING`, no job error. Adapter v32 (16,500 batches) is locally saved
and its two files match the manifest. At the latest check the separate
train-state watcher still reported v31, so local train-state v32 is pending
verification. Fireworks remains active at 4,523/10,704 steps at 05:07:54Z,
without new errors.


The v32 five-case check is complete: 10/10 calls succeeded at estimated usage
`$0.00482675`, but v32 returned no nonempty response, made no tool rounds, and
passed only 2/7 checks, matching v31's failure on this development diagnostic.
See the [v32 report](execution-2026-10-19/wandb-v32-five-scenario-dev-eval-2026-10-20.md)
and [v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md).


05:09 UTC: the W&B observer advanced to 16,654/85,631 steps at 05:09:40Z,
`RUNNING`, no job error; adapter v32 is the latest locally saved adapter,
while train-state backup is still v31 pending its scheduled poll. The v32
five-case diagnostic completed with no nonempty response or tool calls.
Fireworks remains active at step 4,541/10,704 at 05:09:11Z with no new errors.


05:11 UTC: the matching train-state v32 arrived locally at 16,500 batches.
All two adapter files and all eleven train-state files pass the manifest
byte-size and SHA-256 checks. The W&B event stream is at 16,763/85,631 steps
at 05:11:41Z, `RUNNING`, no error. Fireworks remains active at 4,569/10,704
at 05:11:32Z, with no new error.


A one-call raw-field probe against v32 on the frozen fictional support case
confirmed the empty-response result: W&B returned HTTP 200, `content: null`, a
separate 65-character reasoning field, `finish_reason: stop`, and usage of 55
prompt/18 completion tokens (estimated `$0.00003625` at the configured rates;
actual charge unknown). The evaluator correctly treats this as an empty
user-facing answer; it is not overlooking a final answer in the reasoning
field. No reasoning text was stored in the handoff. The v32 five-case result
therefore reflects model behavior, not a transport error.

05:14 UTC live-state refresh: W&B Serverless Training remains explicitly
documented as **public preview**; the preview label is current status, not
evidence of general availability. The documented free-training statement is
therefore still a preview offer, while this account's present entitlement and
actual billed amount remain unverified. Keep inference and artifact storage as
separate meters. The active W&B job `24cc2d06-3ec3-4356-ad3a-179694dd86a7`
returned `RUNNING`, no error, and 16,874/85,631 gradient steps at 05:13:42Z.
The latest locally verified paired adapter/train-state checkpoint is v32 at
16,500 batches; the v33 artifact has not appeared yet. Both v32 local manifests
remain available, with the adapter and train-state checkpoint hashes matching.
The Fireworks Muse Glimmer serverless SFT remains active at 4,600/10,704 steps
at 05:13:46Z, with no new errors. Its tuned sampler is created only after the
run completes, so there is no periodic tuned-weight checkpoint to save; the
experiment remains evaluation-only because the end-of-run weights cannot be
exported under the current setup.

05:15 UTC Adaption refresh: the latest docs-shaped 522,658-row upload remains
`awaiting_input` with null canonical prompt/completion mappings. A read-only
adaptation estimate with explicit mappings was rejected because one launch is
limited to 50,000 rows; no credits were spent. The connector exposes no quote
or balance, so splitting the corpus into multiple launches would not establish
bounded credit coverage. The older 522,658-row dataset remains processed but
has null canonical mapping fields; previous full-size training attempts failed
before iteration. Do not treat Adaption as qualified for this v4 dataset yet.
See the dated [Adaption refresh](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md).

05:15 UTC live W&B/Fireworks refresh: W&B returned `RUNNING`, no job error, and
16,929/85,631 gradient steps at 05:14:43Z. Its latest locally backed-up adapter
and train state remain v32 at 16,500 batches. Fireworks remains active at
4,616/10,704 steps at 05:14:55Z; the correct session endpoint still lists only
the base sampler, with no tuned sampler yet. No new errors were reported.

05:19 UTC checkpoint/eval update: W&B published adapter and full train-state
v33 at 17,000 batches. Both local backups completed and all 13 files matched
their manifest hashes. Two five-case paired evaluations against base completed 20/20 calls at
combined estimated usage `$0.0097935`: v33 gave nonempty content in 4/5 cases,
made zero local tool rounds, and passed 2/7 unvalidated synthetic checks in
both repeats; base gave nonempty content in 3/5, made four local rounds, and
passed 3/7 in both. This slightly restores answer coverage after v31/v32 but
does not address tool use or justify promotion. See the [v33 evaluation](execution-2026-10-19/wandb-v33-five-scenario-dev-eval-2026-10-20.md)
and updated [checkpoint trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md).
The run remains active with the last event observation at 17,032/85,631 steps
(05:16:44Z); Fireworks remains active at 4,670/10,704 steps (05:18:26Z).

05:20 UTC monitor update: the active W&B job advanced to 17,197/85,631 steps
at 05:19:45Z, still `RUNNING` with no error. Both local backups remain at
v33/17,000 batches; v34 has not published yet. Fireworks advanced to
4,705/10,704 at 05:20:15Z, still active with no new errors; its tuned sampler
is still absent from the session checkpoint listing.

05:21 UTC live poll: direct read-only W&B event query returned 61 new events
since the last recorded cursor, advancing the active job to 17,258/85,631 steps;
job status is still `RUNNING`, with no error. Fireworks remains active at
4,718/10,704 at 05:20:59Z; the session endpoint still has only the base sampler
and no tuned checkpoint. This confirms both services are advancing despite
stale local watcher timestamps; do not infer a stall from those timestamps.

#### Frozen v4 W&B training payload signal audit

An aggregate-only scan of the exact frozen W&B train JSONL found 171,261
message-list rows and 1,056,820 messages (522,658 user, 534,162 assistant),
with zero `tool` role messages and zero assistant `tool_calls`. This explains
why the current dialogue SFT has not learned tool calls: the training payload
contains no tool-use supervision. It is an input/task mismatch signal, not
proof of optimizer failure. Keep this source release unchanged; task-specific
tool trajectories require a separate immutable dataset and matched larger
heldout evaluation. Any new W&B run remains subject to provider entitlement,
storage and spend-cap verification. See the [aggregate-only signal audit](execution-2026-10-19/wandb-v4-training-signal-audit-2026-10-20.md).

#### 2026-10-20 Adaption non-launch estimates and actual readiness

The public API defines `awaiting_input` as an uploaded dataset waiting for an
Adaptive Data run with a column mapping. On the newest scalar `60ea...` upload,
the read-only model-recommendation call returns "Dataset is not ready yet";
the processed scalar-text `c00e...` is recognized and returns Qwen 3.6 LoRA
hyperparameters, but its prior capped run failed before iteration because the
provider generated an empty validation JSONL. Two estimate-only Adaption calls
on `60ea...` returned 500 credits/635 min for 50,000 rows and 227 credits/294
min for 22,658 rows. A hypothetical 10×50,000 plus 22,658 split totals 5,227
Adaptive Data credits and 6,644 estimated minutes; this is not an AutoScientist
training price or verified usable chunking path. No credit was spent. The
account balance remains unreadable through the connector, and the documented
Adaption app requires sign-in, so no balance is inferred. See the [Adaption
qualification addendum](execution-2026-10-19/adaption-qualification-refresh-2026-10-19.md)
and the official [status](https://docs.adaptionlabs.ai/api/resources/datasets/methods/get_status/)
and [estimate](https://docs.adaptionlabs.ai/api/resources/datasets/methods/adapt/) references.

05:31 UTC checkpoint/evaluation refresh: W&B v4 is still `RUNNING`, with the
latest direct event observation at 17,853/85,631 steps (training loss 2.228).
Adapter
v34 and its complete train-state v34 were downloaded locally at 17,500 batches;
the adapter is 117,842,120 bytes with SHA-256
`435ecd93cc99ad10123f61930977adbfc4e8ca70d79fa3bf5da39933fa999bd9`, matching
its manifest. The v34 five-case paired evaluation completed 10/10 calls:
nonempty output 5/5, zero local tool rounds, 2/7 synthetic checks; base had
3/5 nonempty, four local rounds, and 3/7 checks. SFT output used only 54
completion tokens in total versus 2,792 for base, so the apparent coverage
increase is not evidence of better task completion. Estimated evaluation
usage was `$0.004683`; actual billing is unknown. This small unvalidated
synthetic result does not support promotion. See the [v34 evaluation](execution-2026-10-19/wandb-v34-five-scenario-dev-eval-2026-10-20.md).

A prompt-disjoint 120-case v33-vs-base evaluation completed on the frozen
hashed synthetic test file: 240/240 calls succeeded. The base made 137 local
mock-tool rounds and passed 73/75 `tool_status` checks; v33 made zero rounds and
passed 0/75. Base passed 200/240 total deterministic checks, while v33 passed
62/240; those checks are synthetic and unvalidated. Although v33 had shorter
latency and used far fewer completion tokens, it had lower response coverage
and substantially worse task checks, so this is not a quality improvement.
Estimated inference usage was `$0.109211`; actual billing is unknown. See the
[v33 held-out evaluation](execution-2026-10-19/wandb-v33-prompt-disjoint-heldout120-eval-2026-10-20.md).

Fireworks Muse Glimmer remains active at 4,835/10,704 steps (05:32:25 UTC),
with no new errors. Its managed sampler endpoint still has not shown a tuned
checkpoint, so it remains experiment-only pending end-of-run exportability.
W&B's Serverless Training/SFT docs continue to label the service public
preview; the active API path is `/v1/preview/`. See the [official Serverless
Training documentation](https://github.com/wandb/docs/blob/main/serverless-training.mdx).

The v34 120-case prompt-disjoint paired evaluation has completed against the
same base model and frozen test set, using the existing four-round setting and
`$1.50` hard cap. All 240 calls succeeded with no errors; estimated usage was
`$0.10859525`, actual billing unknown. V34 had nonempty responses 120/120 but
zero tool rounds, 0/75 `tool_status` and 0/75 `response_contains` checks, and
60/240 total deterministic checks; base had 105/120 nonempty, 138 rounds,
74/75 tool-status checks and 201/240 total. V34's average was about 13
completion tokens per case. The result reinforces that short, fast answers are
not task success and does not support promotion. See the [v34 held-out report](execution-2026-10-19/wandb-v34-prompt-disjoint-heldout120-eval-2026-10-20.md).

The automatic v35 five-case evaluation also completed at the 18,000-batch
checkpoint. It returned nonempty content in 1/5 cases, zero tool rounds, and
2/7 synthetic checks, versus base at 3/5, four rounds, and 3/7. V35's adapter
was downloaded locally; SHA-256 `5c348673d104066fa59a7e13b6793eff3e137f890dd0f279bb39667786c48492`
matches its manifest. Estimated five-case inference usage was `$0.0049705`,
actual billing unknown. See the [v35 evaluation](execution-2026-10-19/wandb-v35-five-scenario-dev-eval-2026-10-20.md).

05:54 UTC refresh: W&B v4 remains `RUNNING` at 19,010/85,631 gradient steps
(training loss 1.747). Adapter and full train-state v36 at 18,500 batches are
backed up locally; all 13 adapter/train-state files reverified against their
manifest sizes and SHA-256 hashes. The v36 five-case paired inference check
completed 10/10 calls: v36 returned nonempty output in 2/5 cases, made zero
local tool rounds, and passed 2/7 synthetic checks; base was 3/5, four rounds,
and 3/7. Estimated usage was `$0.004733`, actual billing unknown. See the
[v36 evaluation](execution-2026-10-19/wandb-v36-five-scenario-dev-eval-2026-10-20.md)
and [v19-v37 trend](execution-2026-10-19/wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md).

Fireworks Muse Glimmer was last observed active at 5,013/10,704 steps
(05:53:37 UTC), with no new errors. Its managed sampler endpoint still listed
only the base sampler. Neither provider's checkpoint results support model
promotion. W&B's Serverless Training documentation explicitly says “public
preview” and its pricing statement says adapter training is free during
preview, with inference and artifact storage charged separately. Important
qualification: the cited `wandb/docs` repository was archived on 2026-09-30,
so its wording establishes the last published documentation state, not
independently verified live product/contract status. The active API uses
`/v1/preview/`; account-specific entitlement and current billing remain
unverified. Keep these distinctions explicit in provider decisions.

06:00 UTC live refresh: the active W&B v4 job `24cc2d06-3ec3-4356-ad3a-179694dd86a7`
remains `RUNNING`, with no job error. Its event endpoint advanced to
19,327/85,631 gradient steps at 06:00:05Z (training loss 1.4496), despite the
stale job `updated_at` field. Adapter v37 and full train-state v37 are both
present locally at 19,000 completed batches; the adapter has SHA-256
`c70b52c697b48863ff3c67c6e7771a8454a09264bc0cdec9a4fad81b83b8f7ea` and the
five-case v37 paired evaluation finished 10/10 calls. Fireworks Muse Glimmer
was independently observed at 5,076/10,704 steps at 06:00:36Z (loss 0.7971),
still active without new errors; no tuned sampler is available yet. These are
experiment runs only; no checkpoint has met the behavioral evaluation gates.

06:05 UTC refresh: W&B's live event observer advanced job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` to 19,593/85,631 gradient steps at
06:05:08Z, still `RUNNING` without a job error. The train-state watcher has
downloaded v38 at 19,500 batches; the latest adapter backup remains v37 at
19,000 batches, so v38's adapter is not yet confirmed locally. Fireworks was
directly polled at 06:05:18Z: 5,124/10,704 steps, active, no new errors, and
the session API still lists only the base sampler. PsychEval's private-source
binding boundary has also moved: all 1,977 v4 rows now have unique matches to
the current R2 snapshot (1,968 exact and 9 normalized-only), with no split
crossings. Its immutable upstream revision remains unknown. See the [PsychEval
origin-binding audit](execution-2026-10-19/psycheval-v4-upstream-origin-binding-2026-10-20.md).

06:11 UTC refresh: the W&B event observer advanced job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` to 19,925/85,631 gradient steps
(training loss 1.9345), `RUNNING`, without a job error. Adapter checkpoint v38
and its paired train-state v38 (19,500 batches) are now both present locally;
the train-state is 1,060,414,703 bytes. Fireworks Muse Glimmer was observed
active at 5,201/10,704 steps with no new errors. Its current serverless path
still has no exportable end-of-run weights, so it remains experiment-only.

The latest counseling source audit found a private R2 snapshot with partial
pair correspondence, but no unique source row locators: exact matching gives
427 ambiguous and 988 unmatched; normalized matching gives 1,046 ambiguous
and 369 unmatched. Among the 369, 361 have only a prompt match, 7 only a
response match, and 1 neither. Snapshot identity and acquisition-time lineage
remain unknown. The candidate and provider payload are unchanged; this is not
rights or transfer authorization. See the [counseling origin-binding
audit](execution-2026-10-19/counseling-conversations-v4-upstream-origin-binding-2026-10-20.md).

The W&B Serverless Training documentation continues to label SFT as **public
preview** and the free-training statement is conditional on those preview
terms. Because the cited docs repository is archived, this identifies its
last published status; it does not establish current account entitlement or
actual charges. Preserve those as separate, unverified facts.

06:35 UTC checkpoint reconciliation: W&B job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` remains `RUNNING`; the live event stream
reached 21,227/85,631 steps at 06:35:33Z, although the job status endpoint's
`updated_at` remains stale at 2026-10-19 22:50:52Z. The adapter and train-state artifact collections
both contain committed v41 at 21,000 batches (published 06:31:14Z and
06:31:16Z, respectively), with `latest` and job-resume aliases. The adapter
v41 was mirrored locally by 06:32:49Z. The train-state watcher completed the
roughly 1.06 GB v41 mirror at 06:34:56Z. All 11 local files (1,060,414,703
bytes) passed manifest size and SHA-256 checks. The separate model-checkpoints
API still lists only its step-0 entry; that endpoint does not enumerate these
internal resume artifacts. Earlier checks that treated that listing as the
checkpoint inventory were incomplete. Do not delete storage based on that
endpoint; use the artifact collections and local backup manifests as the
authoritative checkpoint inventory. A final poll at 06:35:33Z found no v42;
the latest remote and local versions at that poll were v41. The backup
watchers then downloaded v42 (21,500 batches): adapter pointer updated at
06:42:56Z and train-state pointer at 06:45:16Z. Both v42 local manifests pass
size and SHA-256 verification: two adapter files totaling 117,843,308 bytes,
and 11 train-state files totaling 1,060,414,703 bytes. The job remained
`RUNNING` at 21,699/85,631 steps in the 06:44:30Z event poll.

The paired five-case v41 evaluation completed 10/10 calls. V41 returned
nonempty output in 4/5 cases, made zero tool rounds, and passed 2/7 synthetic
checks; base returned nonempty output in 3/5, made four rounds, and passed
3/7. Estimated inference usage was `$0.00474675`, with actual billing
unverified. A subsequent larger comparison found 117/120 nonempty responses,
zero tool rounds, and 60/240 checks; response availability recovered while
tool use remained broken. Neither evaluation supports promotion. See the
[v41 five-case evaluation](execution-2026-10-19/wandb-v41-five-scenario-dev-eval-2026-10-20.md)
and [120-case report](execution-2026-10-19/wandb-v41-prompt-disjoint-heldout120-eval-2026-10-20.md).

Prompt-disjoint held-out tool-loop evaluations of v38 (19,000 batches) and
v39 (20,000 batches) both reproduced a severe output regression: each returned
nonempty output in only 1/120 cases, made zero local tool rounds, and passed
60/240 deterministic checks, while their paired base arms returned nonempty
output in 102/120 cases and made 133–136 tool rounds. Both evaluations had
240/240 successful inference calls; estimated inference usage was about
`$0.107–$0.108` per paired run, while actual billing was unavailable. Neither
checkpoint is promotable. V41's later 120-case evaluation recovered nonempty
output in 117/120 cases but continued to make no tool rounds and passed only
60/240 checks. See the [v38 evaluation](execution-2026-10-19/wandb-v38-prompt-disjoint-heldout120-eval-2026-10-20.md),
[v39 evaluation](execution-2026-10-19/wandb-v39-prompt-disjoint-heldout120-eval-2026-10-20.md),
and [v41 evaluation](execution-2026-10-19/wandb-v41-prompt-disjoint-heldout120-eval-2026-10-20.md).

V42's automatic five-case paired evaluation completed 10/10 calls: v42
returned nonempty content in 3/5 cases, made zero tool rounds, and passed
2/7 checks; base returned nonempty content in 3/5, made four rounds, and
passed 3/7. Estimated usage was `$0.0047555`, actual billing unverified.
The v42 adapter and train-state were both mirrored locally and verified by
manifest hashes. See the [v42 evaluation](execution-2026-10-19/wandb-v42-five-scenario-dev-eval-2026-10-20.md).

Fireworks Muse Glimmer was still active at 5,638/10,704 steps in the
06:47:01Z direct poll, with only the existing nonfatal warnings. The correct
session-scoped checkpoint endpoint still lists the base sampler only; this
launcher creates its tuned sampler after training completes and does not save
periodic tuned checkpoints. `launch.stdout` is current, while the separate
`metrics.jsonl` lags at step 5,459. See the [Fireworks run report](execution-2026-10-19/fireworks-muse-glimmer-20261019/run-report.md).

## 2026-10-20 06:52 UTC live progress and next Fireworks experiment

The W&B full-corpus job remains `RUNNING` with no error; its event watcher
reached 22,110/85,631 gradient steps at 06:52:34Z (loss 1.8021; throughput
3,427.5 tokens/second). The status endpoint's `updated_at` remains stale, so
the event stream is the progress authority. Existing v42 local adapter and
train-state backups remain the last verified mirrors.

The active Fireworks Muse Glimmer run remains alive at 5,723/10,704 steps in
the current launcher output. It has not produced a tuned checkpoint yet and
continues to occupy the account's training slot; leave it running.

The 960/120/120-row synthetic agent-tool package passed a model-specific
offline Muse Glimmer renderer preflight. All 1,200 training tool-call markers
are in loss-weighted targets; no sequences exceeded 32,768 tokens and no rows
lacked trainable targets. The cookbook adaptation is preserved in
[`fireworks-muse-glimmer-renderer.patch`](agent-tool-sft-2026-10-19/fireworks-muse-glimmer-renderer.patch),
and full counts, split hashes, settings, and the held-out evaluation gate are
in the [preflight report](agent-tool-sft-2026-10-19/fireworks-preflight-2026-10-20.md).
The preflight was offline only: no upload or second Fireworks job was started.
Once the active session completes, run this bounded experiment with the
patched renderer and use the 120-case mock-tool evaluator against both the
trained sampler and base model; the cookbook's text-only evaluation is
insufficient to qualify tool use. The tested in-session bridge is
[`fireworks_session_eval.py`](../../ai/training/fireworks_session_eval.py);
its two offline transport tests pass, and the Fireworks SDK/samplers must be
passed into it by the process that owns the session.

At 06:54 UTC, the W&B event watcher advanced to 22,213/85,631 and a new
adapter checkpoint `v43` (22,000 batches) was mirrored locally and verified
against its two-file manifest. The train-state mirror remains `v42` at 21,500
batches; its watcher is active and will pick up subsequent versions. Fireworks
advanced to 5,745/10,704 steps and its launcher process remains alive.

The current full-candidate release also passed a read-only integrity refresh:
all 190,139 unique rowrefs match candidate-row content hashes, the 52-row
repair file matches its frozen hash, all three split payload hashes and counts
match, and there are no cross-split group collisions. See the
[integrity refresh](execution-2026-10-17/full-candidate-split-integrity-refresh-2026-10-20.md).

06:58 UTC follow-up poll: W&B reached 22,420/85,631 events and remains
`RUNNING` without an error; Fireworks reached 5,809/10,704 and its process is
still live. Both local W&B watchers are alive. The adapter and train-state
v43 mirrors (22,000 batches) both pass manifest verification; all 11 train-state
files totaling 1,060,414,703 bytes match their recorded sizes and SHA-256s.

07:04 UTC refresh: the W&B full-corpus run remains `RUNNING` at 22,670/85,631
gradient steps (latest event 07:03:41Z, loss 1.8368). Both local watchers are
alive. Adapter v44 and train-state v44 at 22,500 batches were downloaded; the
adapter files pass recorded size and SHA-256 checks, and the 11-file train-state
mirror totals 1,060,414,703 bytes. This confirms checkpoint artifacts are being
created during the run; the job status `updated_at` field remains stale, so event
polling and artifact versions are the useful progress signals.

Fireworks Muse Glimmer serverless SFT PID 518909 remains alive at 5,879/10,704
steps in its current launcher output. It still has not produced a tuned
checkpoint; the launcher creates that sampler after training completes.

The offline Fireworks paired-evaluation bridge now constructs the sampler's
actual `tinker.types.SamplingParams` and the contract test uses a real Tinker
`SampledSequence` shape. Targeted validation passed: 2 pytest tests and Ruff.
This fixes SDK compatibility but does not itself provide a caller inside the
active Fireworks training session.

The matching five-case paired evaluation for W&B v44 completed 10/10 calls
against base. V44 returned nonempty content on 3/5 cases, made zero tool rounds,
and passed 2/7 unvalidated synthetic checks; base made four tool rounds and
passed 3/7. Estimated usage was `$0.004753` (actual billing unverified). V44
does not show a tool-use improvement and is not promoted. See the [v44 paired
evaluation](execution-2026-10-19/wandb-v44-five-scenario-dev-eval-2026-10-20.md).

07:06 UTC Fireworks state correction: the local launcher PID is no longer
present. Its `launch.stdout` and `metrics.jsonl` stop at 5,886 and 5,849 of
10,704 steps, respectively; no `summary.json` or tuned-checkpoint evidence
exists. A read-only query to the session-scoped checkpoint endpoint returned
only the original base sampler, created 2026-10-19 19:10:40Z. The query exposes
checkpoints, not a session status, so remote terminal state is unverified. Do
not call this run complete or start a duplicate until the provider session state
can be established; its raw logs remain preserved locally.

07:07 UTC independent SDK audit reconfirmed the same checkpoint result. The
installed Fireworks SDK provides no `get/list/status` method for this serverless
TrainingSession; `TrainerJobManager.get()` applies only to RLOR trainer jobs.
Thus the local process stopping is verified, while the remote session's running,
completed, or failed state remains unknown.

The direct read-only control-plane `GetTrainingSession` query returned session
state `READY`, status `OK/ready`, and an update time equal to session creation.
It also returned `referenceState=BASE`. These fields confirm the session resource
is ready and currently references its base-model route; they do not expose
optimizer progress or terminal state for the local training loop. The checkpoint
endpoint still lists only the base sampler. See the [Fireworks session API reference](https://docs.fireworks.ai/fine-tuning/training-sdk/reference/service-client)
for the separate checkpoint operations.

The current v4 lineage audit now has a hash-only status transfer from the
190,139-row release: 189,141 unique exact row-hash plus exact-source-label
matches inherit the existing unresolved/hold fields. Eighteen duplicate-hash
occurrences were withheld, as were 1,085 nonmatching ARC rows already covered
by separate v4 lineage work. All 190,244 current split rowrefs and all 190,139
source-ledger bindings were validated. No rights, privacy, or training-use
clearance was inferred, and no dataset payload changed. The 8.7 MB compressed
private map is mode 0600. See the [transfer audit](execution-2026-10-17/v4-exact-row-status-transfer-2026-10-20.md).

07:12 UTC W&B refresh: the full-corpus run is `RUNNING` at 23,079/85,631
gradient steps (latest event at 07:11:45Z; no error). The train-state watcher
downloaded v45 at 23,000 batches: all 11 files (1,060,414,703 bytes) pass the
manifest's SHA-256 and size checks. The adapter watcher has not advanced beyond
v44 at 22,500 batches yet; its next poll is pending.

07:14 UTC: W&B reached 23,131/85,631 gradient steps and remains `RUNNING` with
no error. The adapter watcher downloaded v45 at 23,000 batches; its two files
(117,843,308 bytes) also pass the recorded SHA-256 and size checks. Adapter and
train-state v45 are now a verified local pair.

The follow-up exact-source audit found no safe new locator bindings to add.
Among the 1,103 current-v4 positions absent from the status transfer, 1,085
are already covered by exact ARC bindings. The remaining 18 match local book
content but each has multiple upstream source-row candidates (2–6); all remain
marked ambiguous, with alternatives retained in a private hash-only map. The
local book audit has 8,089 exact unique row bindings and these 18 ambiguous
ones. See the private summary
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/v4-untransferred-source-binding-gap-20261020-report.json`.

07:17 UTC W&B v45 paired five-case synthetic diagnostic completed 10/10
requests. V45 produced nonempty content on 1/5 cases, zero tool rounds, and
passed 2/7 unvalidated checks; base produced nonempty content on 3/5, four tool
rounds, and passed 3/7. The SFT arm's sole nonempty response was an off-task
Japanese greeting. Estimated inference usage was `$0.00478175` under the
configured `$0.06` cap; actual billing is unverified. V45 is not promoted. See
the [v45 evaluation](execution-2026-10-19/wandb-v45-five-scenario-dev-eval-2026-10-20.md).
The W&B event observer's latest state at 07:16:47 UTC was `RUNNING`, 23,341 of
85,631 gradient steps, with no reported error; the provider's `updated_at`
remains stale. Adapter and train-state v45 (23,000 batches) remain the latest
verified local checkpoint pair. Continue monitoring; use the next paired
diagnostic at v50 rather than evaluating every intermediate checkpoint.

07:18 UTC Adaption read-only refresh: the uploaded 522,658-row raw dataset now
reports `prompt` and `completion` as mapped columns and an updated timestamp of
07:15:56Z, but its state remains `awaiting_input` with no processed-row count or
progress percentage. Dataset evaluation is empty, and the Qwen3.6-35B-A3B
hyperparameter recommendation still rejects it as not ready. The separate
11,192-row `arc-run2-train-v1` remains processed and ready. No new resources or
training runs were created. The Adaption credit balance/expiry and exact
per-run credit coverage remain unavailable, so no Adaption training job is
launched. See `execution-2026-10-17/adaption-qualification-refresh.json`.

07:22 UTC W&B read-only storage and entitlement refresh: the project reports
50,264,950,081 bytes; the organization reports 166,026,268,417 bytes trailing
30-day average against its 200 GB entitlement (about 33.97 decimal GB average
headroom). This is a billing-average measure, not instantaneous quota or
worker-disk space. The subscription also exposes a 100,000 training-free-limit
field marked unenforced whose interval ended 2026-07-31; that metadata alone
does not prove current billing. Public documentation still labels Serverless
Training public preview and states preview training is free, but confirm
account treatment before relying on it for another job. See the [storage and
entitlement snapshot](execution-2026-10-19/wandb-storage-entitlement-refresh-20261020T0722Z.json).

The synthetic agent-tool SFT release passed its W&B launcher dry-run:
960 training trajectories, 1,200 tool-call messages, 120 validation rows,
120 release-test rows, and a 1.43 MB staged training package. No upload or job
was created. User-prompt text repeats across train/validation/test because
examples vary fixture data under shared scenario templates (60 shared prompt
hashes between train and test); the separately hashed 120-case held-out
evaluation remains the campaign comparison set. The package is local synthetic
research data with no external or clinical records, and remains a candidate for
a separately scheduled W&B run after the active full-corpus job/storage state
is resolved. Current launcher dry-run reports no upload or job creation.

07:22 UTC event poll: the W&B full-corpus job is `RUNNING` at 23,596/85,631
gradient steps (loss 1.8030 on the latest reported step); the event observer and
both local artifact mirrors are alive. The provider's job `updated_at` remains
stale, so progress continues to be read from training events. No second SFT job
was launched while this job is active and storage headroom is limited to the
reported trailing-average measure.

07:23 UTC checkpoint refresh: W&B is `RUNNING` at 23,700/85,631 gradient steps.
Adapter and train-state v46 (23,500 batches) are both mirrored locally and all
13 files (1,178,258,011 bytes) match their manifest sizes and SHA-256 hashes.
The next planned five-case checkpoint comparison remains v50.
A v50 paired-evaluation config is staged privately at
`ai/training/output/wandb_live_checkpoint_eval_20261020/v50-five-scenario-dev/config.json`
with the same five development cases and `$0.06` estimate cap; it is not sent
until the matching v50 adapter and train-state checkpoint are verified.

07:26 UTC book-lineage refinement: rechecking the 18 unresolved exact-content
matches across all 47 local distilled-book files uniquely identifies one local
file for 12 rows (duplicate line numbers remain), while six rows still match
two distinct files. The private file/line sidecar contains no message text and
the v4 payload is unchanged. Local-file matching still does not establish the
book edition, acquisition, rights, or transfer authorization. See the
[follow-up audit](execution-2026-10-19/clinical-book-file-origin-v4-followup-2026-10-20.md).

07:29 UTC status-transfer refinement: the 18 previously withheld clinical-book
rows all match old candidate groups with the same exact content hash and source
label. Revalidation confirms the old candidate and every grouped ledger rowref
match by row number/hash/label; 10 current rows map to two old duplicates and
eight map to four, with exactly one shared six-field unresolved/hold disposition
per group. Those status values are recorded in a supplementary group-level map,
without asserting a unique historical row match or changing the candidate.
The 1,085 ARC rows still have exact archive lineage, but their lane-2 decisions
remain unbound to candidate content hashes. See the [uniform group-status
follow-up](execution-2026-10-19/v4-untransferred-uniform-status-followup-2026-10-20.md).

07:32 UTC complete current-v4 source-status ledger audit: all 190,244 ledger
rowrefs independently match the current candidate at exact row hash and source
label; each has all six generic unresolved/hold fields. The ledger retains the
predecessor v3 candidate digest on 190,230 carried-forward rows, while the 14
added v4 ARC rows reference the current v4 digest. This preserves the decision
history and row-level proof; it does not supply the still-missing source-specific
lane-2 ARC decisions or any rights/privacy/transfer clearance. See the
[full audit](execution-2026-10-19/current-master-source-status-ledger-audit-2026-10-20.md)
and machine-readable [coverage report](execution-2026-10-19/current-master-source-status-ledger-audit-2026-10-20.json).

07:34 UTC direct W&B event refresh: the v4 full-corpus training job remains
`RUNNING` without a reported error at 24,105/85,631 gradient steps (latest loss
0.4578). The remote job `updated_at` remains stale; authenticated training events
are the progress authority. Local artifact watchers are alive, with v46 at
23,500 batches still the latest mirrored adapter/train-state pair; the prepared
v50 eval remains gated on both matching local checkpoint mirrors.

07:35 UTC live refresh: the W&B event observer advanced to 24,263/85,631
steps (latest loss 0.3783), remains `RUNNING`, and reports no job error. Adapter
v47 (24,000 batches; 117,843,308 bytes) and matching train-state v47
(1,060,414,703 bytes) are mirrored locally. I recomputed SHA-256 and size for
all 13 manifest-listed files; all match. The observer is advancing by about
51 steps per minute in the last two polls. v50 has not been published yet, so
the prepared v50 paired evaluation remains pending. Public-preview training
terms are unchanged; this active run's account-specific billing remains
unverified.

07:39 UTC lane-2 hash-attachment follow-up: I compared all four dated lane-2
review artifacts with the current v4 ARC lineage. Their decisions cover 71
unique ARC IDs and attach by ARC ID to 185 candidate rows with exact candidate
row and canonical-message hashes. The review artifacts do not pin the reviewed
content revision, so this is an explicit post-hoc attachment, not proof that
those decisions were made on the current frozen content. It surfaces a concrete
conflict: 27 latest `reject` decisions map to 74 v4 candidate rows whose archive
machine verdict is `accept` (split counts are in the public report). None were
silently removed or treated as cleared, and the live job was left untouched.
The next corpus decision must reconcile the review-time revision against these
row hashes before interpreting these 74 rows as reviewed or rejected current
content. Reproduce with
`scripts/training/audit_lane2_arc_decision_hash_attachment.py`; private hash-only
row map: `ai/data/curated/recovery/gold-20261017/private-lane2-current-content-attachment-20261020/lane2-current-content-attachment.jsonl`
(SHA-256 `e810ee434cc9aad6f3246f8b5a980bb658debfa5064e92dbe3eaceb696ba9086`).
See [the aggregate report](execution-2026-10-19/lane2-current-content-hash-attachment-2026-10-20.md).

07:41 UTC Adaption live refresh: dataset
`60ea43c8-c965-4ab1-968a-b4b82be7703d` remains `awaiting_input` at 522,658
rows with mapped `prompt`/`completion` columns, `processed_rows=null`, and no
progress or document counts. Dataset evaluation returns no status, summary, or
raw results, and the dataset-filtered AutoScientist run list is empty. The
11,192-row `arc-run2-train-v1` reference remains the last known ready dataset.
No run, export, or credit-consuming request was created. Balance/expiry and
bounded credit coverage remain unknown.

07:39 UTC event poll: W&B advanced to 24,470/85,631 steps, remains
`RUNNING`, and reports no training error. Checkpoint watchers are live; the
latest adapter/train-state pair remains the verified v47 pair at 24,000
batches. At the recent ~52 steps/minute, v50 (25,500 batches) is roughly 20
minutes away; this is a short-window estimate, not a provider ETA. The five-case
v50 evaluation still waits for both verified v50 artifacts.

07:42 UTC evaluation watch: a one-shot local watcher is running under tool
session `1639` for the prepared v50 five-case paired comparison. It checks that
both v50 adapter and train-state artifacts belong to the active job and that
every manifest-listed file matches the recorded size and SHA-256 before making
any inference request. It will run the five frozen synthetic development cases
against base and v50 SFT once, under the prepared `$0.06` hard cap, then exit;
its output log and results remain under the private v50 evaluation directory.

07:48 UTC lane-2 snapshot-version detail: of the 71 latest ARC-ID decisions, 27
are rejects. All 25 latest Oct. 5 rejects match the same canonical candidate
session hashes in the nearest preserved Oct. 16 archive snapshot; the other two
latest rejects (Sept. 19) match the nearest preserved Sept. 20 snapshot. This
is evidence that current payloads persisted in those later snapshots, not a
hash captured by the review itself. The public audit now reports both raw
per-review drift and latest-decision snapshot matches.

A separate local sensitivity variant now removes those 74 current-v4 rows
(66 train, 5 validation, 3 test), preserving the full-v4 baseline unchanged.
Its filtered partitions have 171,195/9,668/9,307 rows; all candidate row hashes
and rendered payload content groups were verified, and cross-split group
intersections remain zero. The protected local release is
`ai/data/curated/recovery/gold-20261017/wandb-full-corpus-lane2-reject-sensitivity-20261020-v1/`;
its release manifest sets `upload_gate=false`. No provider upload or second
training job was launched. See the [sensitivity release note](execution-2026-10-19/lane2-reject-sensitivity-release-2026-10-20.md).

07:48 UTC W&B refresh: the active full-corpus job is `RUNNING` at 24,928/85,631
steps, with no reported error. Adapter and train-state v48 (24,500 batches) are
both mirrored locally; the previously prepared v50 paired evaluator remains
waiting for both verified v50 filesets.

07:50 UTC Adaption capability refresh: authenticated model catalog includes
`Qwen/Qwen3.6-35B-A3B`, the same base family as the active W&B run, and Qwen
3.5 4B. On the ready 11,192-row `arc-run2-train-v1` reference dataset, the
read-only recommender returned a one-epoch Qwen3.6-35B-A3B LoRA recipe (rank 8,
alpha 8, q/v projections, learning rate 1e-4). This creates a matched-base
Adaption comparison path once the selected dataset is ready and credit coverage
is bounded. The recommender did not quote credits or start a run. The 522,658-row
raw dataset remains `awaiting_input`.

Provider-cost boundary: Adaption's dataset `/adapt` API supports
`estimate=true` for a no-run dataset-adaptation quote, but the AutoScientist
create endpoint starts a credit-consuming training loop and its public schema
has no estimate-only mode. Hyperparameter recommendation resolves recipe values,
not a credit quote. Dashboard balance, expiry, and per-run coverage remain the
missing evidence before an Adaption training job. See the [dataset adaptation
API](https://docs.adaptionlabs.ai/api/resources/datasets/methods/adapt/) and
[AutoScientist create API](https://docs.adaptionlabs.ai/api/resources/autoscientist/methods/create).

07:51 UTC event poll: the live W&B run advanced to 25,074/85,631 gradient
steps, remains `RUNNING`, and reports no error. The local mirrors are at adapter
and train-state v48 (24,500 batches); the one-shot v50 evaluator watcher is
still live and has made no inference request yet.

07:53 UTC checkpoint refresh: W&B adapter and train-state v49 (25,000 batches)
are now mirrored locally; all 13 manifest-listed files pass recomputed size and
SHA-256 checks (1,178,258,011 total bytes). The authenticated event stream is at
25,179/85,631 steps and remains `RUNNING` without an error. From the recent
24,417-to-25,179 event interval, the observed rate is about 52 steps/minute,
which implies roughly 19.5 hours to the remaining optimizer steps if that pace
holds; pauses and provider-side variation are excluded. v50 remains the next
paired-evaluation checkpoint.

#### 2026-10-20 W&B Serverless Training status recheck

The official W&B Serverless Training documentation still explicitly says the
service is in **public preview**. It names Serverless SFT as a supported method
and says that during preview W&B charges for inference usage and artifact
storage, but not adapter training. The repository hosting this page is marked
archived/read-only (archived September 30, 2026), so this verifies the latest
published documentation available there, not a current account-specific offer
or a post-migration billing guarantee. For planning, keep W&B SFT as a preview
training-cost-free option, budget inference and artifact storage separately,
and verify the workspace's actual billing/entitlement before treating any
future run as covered. The active run's entitlement and charges remain a
separate account-level question.

Source checked 2026-10-20: [W&B Serverless Training documentation](https://github.com/wandb/docs/blob/main/serverless-training.mdx), especially its public-preview and billing statements.

#### 2026-10-20 v50 response-channel root-cause check

A direct W&B inference A/B on the same minimal synthetic prompt (`Reply with
exactly PONG.`) confirms the v50 evaluator result is not caused by dropping a
normal visible answer: the base returned `message.content`, while v50 returned
`message.content: null`, no tool calls, and only a populated `message.reasoning`
field. The adapter's reasoning was unrelated to the PONG instruction and began
with a mental-health questionnaire opening; raw output was not retained. Thus
v50 has a real user-visible response failure on this prompt. This does not
prove checkpoint corruption or determine root cause, but it means v50 must not
be promoted. Keep later checkpoints experimental and gate any use on visible
content and tool-behavior evaluations. Do not expose reasoning as a substitute
for a final response. The two additional synthetic calls used 16 prompt tokens
each and 141/143 completion tokens; estimated cost at the configured rate is
about $0.0004, with actual billing unavailable. See the
[v50 response-channel diagnostic](execution-2026-10-19/wandb-v50-response-channel-diagnostic-2026-10-20.md).

At 2026-10-20 08:08:14 UTC, the live W&B event observer still reports job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` as `RUNNING`, no job error, and 25,949
of 85,631 gradient steps (loss 1.0125 on the latest event). The separate adapter
and train-state watchers are alive and still report v50 / 25,500 batches at
08:08:35Z; the next 500-batch checkpoint has not yet been published. These
observations confirm continued progress, while loss is a volatile per-event
signal and not evidence of behavioral recovery.

#### 2026-10-20 v51 paired evaluation and response-channel follow-up

W&B published resume adapter v51 at 26,000 batches. The bounded five-case
paired evaluation completed successfully (10/10 API requests, zero request
errors) against the base. Base: visible content 3/5, four evaluator-local tool
rounds, 3/7 unvalidated synthetic checks. V51: visible content 2/5, zero tool
rounds, 2/7 checks; four SFT calls stopped and one reached the 1,024-token
limit. This is a small synthetic diagnostic, not a validated quality, clinical,
or safety measure. It improves visible nonempty count over v50's 0/5 but does
not restore task behavior or tool use; do not promote v51.

A further direct synthetic PONG probe to v51 returned HTTP 200 with
`message.content: null`, no tool calls, and only a five-character `reasoning`
field. This confirms that the response-channel issue persists for v51. Raw
reasoning was not retained and must not be substituted for final visible
content. Paired evaluation estimated usage was $0.0070655 (worst-case preflight
$0.05376 under the $0.06 cap); actual billing is unavailable. The additional
probe used 16 prompt and 4 completion tokens, estimated at $0.000009. Full
hashes and reproduction details are in the
[v51 evaluation report](execution-2026-10-19/wandb-v51-five-scenario-dev-eval-2026-10-20.md).

#### 2026-10-20 Adaption full-corpus and credit estimate refresh

Read-only refresh: raw full-corpus dataset has 522,658 rows, prompt/completion
columns, and remains `awaiting_input` with no processing progress or evaluation.
Two derived 522,658-row datasets are marked succeeded but have null prompt and
completion mappings. Three latest full-corpus AutoScientist attempts failed
before any iteration (two empty temporary validation files, one training JSONL
S3 timeout). The earlier 11,192-row Qwen3.6-35B-A3B run remains the only
successful comparable Adaption training run (platform win rate 0.6414).

A non-launch full-corpus processing estimate was rejected because 522,658
exceeds the plan's 50,000-row-per-launch limit. With `max_rows=50000`, estimate
returned 635 minutes and 500 credits; `run_id` was null and `estimate=true`, so
no credits were consumed. This estimates Adaptive Data processing only, not
AutoScientist training. No organization balance endpoint or training estimate
is exposed by the available Adaption tools. Do not launch full-corpus
adaptation or model training based on this quote alone. Resolve the upload
state, select a <=50k subset if using Adaptive Data, and obtain a bounded
AutoScientist cost before another training attempt. See the
[Adaption qualification report](execution-2026-10-19/adaption-credit-and-dataset-refresh-2026-10-20.md).

#### 2026-10-20 Fireworks Muse Glimmer run terminal-state check

The Fireworks Muse Glimmer SFT session is no longer running. The local launcher
PID is absent and its last training output is step 5,886/10,704, with no final
tuned evaluation summary. A direct read-only Fireworks session API check at
08:20 UTC returned HTTP 200 with `DEADLINE_EXCEEDED: training session expired
after 10m without active runs`. The correct session checkpoint API still lists
only the starter base LoRA; no tuned adapter or optimizer-state checkpoint was
saved. Treat this run as incomplete and non-resumable; its loss log is not a
completed experiment result and it produced no deployable/exportable tuned
weights. The run report now records this authoritative status.

#### 2026-10-20 v51 120-case prompt-disjoint paired evaluation

The expanded v51 comparison completed on the same 120-case prompt-disjoint
synthetic tool-use suite used for v41. The first pass succeeded on 239/240
requests; one base call had a transport payload error. A separate one-case
retry succeeded, giving effective 120/120 coverage per arm; both original and
retry outputs are retained.

Base: 102/120 visible responses, 137 evaluator-local tool rounds, 198/240
unvalidated synthetic checks. V51 SFT: 29/120 visible responses, zero tool
rounds, 60/240 checks, and 102/120 completions stopped at the 512-token cap.
V51 failed all tool-status and expected-response-content checks. It is not
promotable for the agent-tool task. Compared with v41 on the identical suite,
v51 had substantially fewer visible responses (29 vs 117), zero tool rounds
like v41, and the same 60/240 check count. The base arm remained similar to its
v41 result. These are synthetic diagnostics only, not clinical-quality or
safety evidence. Direct v51 response inspection also showed `content: null`
with only a reasoning field; reasoning is not a user-visible final response.

Estimated inference was $0.17382425 including the successful retry; actual
billing is unavailable. The original 120-pair preflight worst case ($1.3824)
plus retry worst case ($0.00576) stayed below the $1.50 hard cap. Full
scenario-level counts, metric definitions, hashes, and reproduction details are
in the [v51 120-case report](execution-2026-10-19/wandb-v51-prompt-disjoint-heldout120-eval-2026-10-20.md).

#### 2026-10-20 v53 checkpoint sentinel and 120-case follow-up

V53 (27,000 batches) was checksum-verified locally for both adapter and
train-state artifacts. On the five-case synthetic development sentinel, the
SFT-only v53 run returned visible content on 3/5 cases, zero tool rounds, and
2/7 unvalidated checks; its fixed base reference from the v51 paired run was
3/5 visible, four tool rounds, and 3/7 checks. A direct synthetic PONG probe
to v53 returned non-null visible content. This is a small improvement in
response visibility over v51, not restored agent-tool behavior or a promotion
result. A same-suite SFT-only 120-case prompt-disjoint v53 follow-up is now
running against the v51 verified base results to avoid another paid base pass.

See the [v53 five-case report](execution-2026-10-19/wandb-v53-five-scenario-dev-eval-2026-10-20.md) and the [completed v51 120-case report](execution-2026-10-19/wandb-v51-prompt-disjoint-heldout120-eval-2026-10-20.md).

The v53 SFT-only 120-case prompt-disjoint follow-up completed with 120/120
successful requests. Against the verified v51 base reference on the same case
file (anchored across runs), base had 102/120 visible responses, 137 local tool
rounds, and 198/240 synthetic checks; v53 had 21/120 visible responses, zero
tool rounds, and 62/240 checks. V53 reached the 512-token cap in 14 cases. Its
check count rose by two from v51, but visible output fell from 29 to 21; the
only prominent scenario gain was approval gate (13/15), while most other
scenario outputs remained near zero. Do not promote v53 for agent-tool use.
Inference estimate was $0.02896225 with $0.6912 worst-case preflight under the
$1.50 cap; actual billing is unknown. See the [v53 120-case report](execution-2026-10-19/wandb-v53-prompt-disjoint-heldout120-eval-2026-10-20.md).

#### 2026-10-20 v54 checkpoint and sentinel

The live W&B full-corpus run remains `RUNNING` with no job error. At 08:46 UTC,
the observer recorded step 27,960/85,631 and loss 0.8036 (step loss is noisy;
this single event is not a quality trend). Adapter v54 and its
matching resumable train-state v54 were mirrored locally at 27,500 batches;
all 2 adapter files and 11 train-state files match their published local
manifest sizes and SHA-256 values.

The five-case SFT-only v54 synthetic sentinel completed 5/5 requests, but all
five returned empty visible response content. It made zero local tool rounds
and passed 2/7 unvalidated deterministic checks. By comparison, v53 returned
visible content on 3/5 cases with the same tool-round and check counts; the
anchored v51 base returned visible content on 3/5, made four tool rounds, and
passed 3/7. Do not spend on a 120-case v54 evaluation without a later sentinel
recovering visible responses and showing meaningful tool/check gains. This is
diagnostic only, not quality or safety evidence. Estimated inference usage was
$0.00059425, with $0.02688 worst-case preflight; actual billing is unavailable.
See the [v54 sentinel report](execution-2026-10-19/wandb-v54-five-scenario-dev-eval-2026-10-20.md).

#### 2026-10-20 v55 checkpoint sentinel

Adapter and matching train-state v55 were mirrored at 28,000 batches and
passed manifest hash/size verification (2 adapter files, 11 train-state
files). At 08:51 UTC the live job remained `RUNNING` without error at step
28,224/85,631. The same five-case SFT-only synthetic sentinel completed 5/5
calls, but v55 returned empty visible content on all five, made zero local
tool rounds, passed 2/7 unvalidated checks, and hit the 1,024-token cap in two
cases. V53 returned visible content on 3/5, while v54 and v55 both returned
0/5. Do not spend on a v55 120-case evaluation unless a later bounded
sentinel recovers visible output and improves tool/check behavior. Estimated
inference was $0.00307425; worst-case preflight was $0.02688; actual billing
is unknown. See the [v55 report](execution-2026-10-19/wandb-v55-five-scenario-dev-eval-2026-10-20.md).

#### 2026-10-20 corrected Counseling Conversations source binding

The earlier private-snapshot join counted `combined_dataset.json` and an
equivalent JSONL representation twice, inflating ambiguity. Their 3,512
ordered records are identical. The raw JSON file's Git blob SHA-1 matches the
file at pinned Amod revision `d7e86f0813c5690181b41f97403c3674aa55dcef`, so
the source snapshot is now bound to that exact revision. The corrected
hash-only join maps 151 candidate pairs uniquely on exact turns and 311
uniquely after normalization; 369 remain unmatched (361 prompt-only, 7
response-only, 1 neither). Exact and normalized source locators do not cross
splits. The v2 sidecar preserves source row references without dialogue text.

The R2 bucket is unversioned and has no acquisition receipt. The gated HF data
file could not be downloaded through the current account; no source content
was fetched from HF. This source-binding correction does not change the frozen
candidate, active full-corpus payload, or training job. The 369 unmatched
pairs remain an unresolved source-content/transform issue for later release
decisions. See the [corrected detailed audit](execution-2026-10-19/counseling-conversations-v4-upstream-origin-binding-2026-10-20.md).

#### 2026-10-20 corrected v56 no-thinking paired evaluation

The paired evaluator now transmits `chat_template_kwargs`, including the
explicit `enable_thinking: false` setting; the focused evaluator suite passes
24 tests. The corrected 120-case paired v56 run completed 240/240 requests
with matching case hashes and no runner errors. Both arms returned non-empty
text, but base made 131 evaluator-local tool rounds and passed 75/75 expected
response checks; v56 made zero tool rounds and passed 7/75. The prior v56
report's empty-response observation came from default reasoning mode and is
superseded only for claims about no-thinking behavior. These synthetic checks
remain unvalidated and make no clinical-quality or safety claim. Estimated
inference use was $0.07813925 under a $1.35168 preflight cap; actual billing
was not returned. A corrected paired v55 replay then completed with 240/240
successful requests and identical case hashes. V55 also returned non-empty
text on all cases but made zero tool rounds, compared with the paired base's
131 rounds. V55 passed 15/75 expected-response checks (v56: 7/75), with 10
token-limit finishes (v56: 3/120). The shared zero-tool result across v55 and
v56 points away from a single-checkpoint regression, though it does not
isolate the cause. Estimated inference was $0.0790255 under the same $1.35168
cap; actual billing was not returned. See the [corrected v55 report](execution-2026-10-19/wandb-v55-explicit-no-thinking-paired-2026-10-20.md)
and [corrected v56 report](execution-2026-10-19/wandb-v56-explicit-no-thinking-paired-2026-10-20.md).

At 09:32 UTC the full-corpus v4 W&B job `24cc2d06-3ec3-4356-ad3a-179694dd86a7`
was still `RUNNING`, without a job error, at step 30,382/85,631. Adapter and
train-state checkpoint v59 (30,000 batches) were mirrored locally; both
watchers remain active. W&B Serverless SFT remains explicitly in public
preview; published terms still say adapter training is free during preview,
with inference and artifact storage billed separately. Account-specific
billing and storage coverage must still be verified.

The next checkpoint v60 was mirrored locally at 30,500 batches. Its same-suite
SFT-only explicit no-thinking evaluation completed 120/120 successfully: all
responses were non-empty, but v60 made zero tool rounds and passed 12/75
expected-response checks. This matches the core v55/v56 zero-tool failure.
Estimated inference was $0.0443685 under a $0.67584 cap; actual billing is
unknown. Stop further checkpoint-only inference sweeps from this run until a
training/template-path change or independent probe provides new diagnostic
signal. Continue the live run and local adapter/train-state mirroring. See the
[v60 evaluation report](execution-2026-10-19/wandb-v60-explicit-no-thinking-eval-2026-10-20.md).

At 09:41 UTC the event observer had most recently reported the live v4 job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` `RUNNING`, without error, at step
30,867/85,631. Step loss is noisy and is not a quality measure.

#### 2026-10-20 v4 loss/source-order correlation

A privacy-preserving read of 1,427 training events from steps 30,383–31,809
shows the median loss steady around 0.81–0.90 through step 31,499, then rising
to 1.339 for steps 31,500–31,599 and 2.86–2.98 for steps 31,600–31,799. The
job remained active without a reported error. The ordered v4 payload changes
at train row 63,102 from long-target `mentalchat16k` examples to much shorter
`mitch_hamidi_bpd_nlp` examples; the W&B step count implies almost exactly two
train rows per step. If the trainer preserves input order, this is aligned
with the loss rise near step 31,551. W&B's public docs do not establish its
shuffle behavior, so this is a strong correlation, not confirmed cause or
evidence of corrupted weights. The Mitch source still has unresolved lineage
statuses; the loss pattern does not change them. Keep v4 running and mirrored;
for a follow-up, shuffle the same train rows deterministically with an aligned
hash-only lineage sidecar and compare against the ordered run. Details are in
the [loss/source-order audit](execution-2026-10-19/wandb-v4-loss-source-boundary-audit-2026-10-20.md).

#### 2026-10-20 structural explanation for the tool-use regression

A structural-only audit of the exact v4 train payload found 171,261 rows and
1,056,820 messages, comprising 522,658 user and 534,162 assistant messages.
There are zero assistant tool-call messages and zero tool-result messages in
the entire payload. In contrast, the separate synthetic tool-SFT train split
has 960 rows, 1,200 structured assistant tool calls, and 1,200 matched tool
results. This provides a direct task-alignment explanation for why the plain
conversation SFT checkpoints retain text output but do not call tools on the
agent-tool eval. It does not prove the only cause. The external prompt-disjoint
120-case evaluation has zero exact user-prompt overlap with this tool-SFT
release; its internal val/test splits do share some prompt templates, so use
the external suite for generalization. The package passed its hash and schema
dry-run, but W&B model creation timed out and no training job ID exists. See
the [structural audit](execution-2026-10-19/full-corpus-tool-structure-mismatch-2026-10-20.md).

#### 2026-10-20 deterministic shuffled v4 follow-up prepared locally

Prepared a deterministic row-order shuffle of the exact frozen v4 training
split, retaining all 171,261 rows and aligning each payload row with its
hash-only row-reference and internal-lineage records. Release ID:
`wandb-full-corpus-v4-shuffled-seed-20261020`. Payload SHA-256:
`367df20ef8370b525d4fe9db81d123b62dc0c5b5fc1c82e3ba1d84b2fa9450ac`; rowref
SHA-256: `721d66a4e16e59526b1a5f94d2863107a9e2bc074f189f4f86f4e6cafd09320d`;
internal-sidecar SHA-256:
`12b5823e0c52366c2815b409ea5b0a6deda0e878466cad6749c81a39500c35fe`.
Independent streaming verification confirmed row counts, payload-to-rowref
hashes, sidecar identity and shuffle-position alignment, manifest checksum,
and private file modes. This is prepared locally only; no provider upload or
job was created. Builder: `ai/training/build_wandb_shuffled_full_corpus_variant.py`.
Do not launch until the active v4 run is complete or a separate comparison
slot is deliberately chosen.

At 10:03 UTC the active v4 job was still `RUNNING`, with no reported job
error, at step 32,032/85,631 (loss 2.994). The local train-state mirror had
advanced to v63 at 32,000 batches (~1.06 GB); the adapter mirror was still
v62 at 31,500 batches at its last observation. The state and adapter mirrors
are separate artifacts, so keep watching both rather than treating the v63
state snapshot as proof that a v63 adapter was captured.

#### 2026-10-20 W&B preview wording and pricing conflict

The user correctly pointed out that the current Serverless Training docs
explicitly label the product **public preview** and explicitly say adapter
training is free during preview, with charges for inference and artifact
storage. Keep that documentation statement explicit. Separately, the pricing
page redirects from W&B to CoreWeave Forge and lists Serverless SFT and RL at
$2.70/GPU-hour, with inference, evaluation, and checkpoint storage billed
separately; its free-preview language applies to Model Distillation instead.
Those published pricing statements conflict. The Forge rate does not erase or
change the preview statement in the Serverless Training docs, while the
account-specific billing terms for the existing run remain unverified. The
authenticated job GET returned only `id`, `status`, timestamps,
`error_message`, `model_id`, `progress`, `training_start`, and `training_end`;
it exposes no price or billing fields. At 10:03 UTC it still reported `RUNNING`, updated at
2026-10-19 22:50:52Z, with no error. Until the account's billing view or
written provider terms resolve the discrepancy, classify training cost as
**unknown** and do not launch additional paid work based on an assumed free
preview. Sources checked 2026-10-20: [Serverless Training docs](https://docs.coreweave.com/products/post-training/serverless-training)
and [Post-Training pricing](https://wandb.ai/site/pricing/training/).

#### 2026-10-20 v63 checkpoint and bounded paired diagnostic

The local mirrors caught both adapter and train-state checkpoint v63 at
32,000 batches. The adapter is 117,843,308 bytes and its two files match the
mirror manifest. At 10:05 UTC the active job remained `RUNNING` without an
error at step 32,136/85,631; latest loss was 2.922.

A five-case paired synthetic diagnostic compared v63 with base using the same
frozen cases and explicit `enable_thinking=false`. Both arms returned visible
responses on all five cases after a separate base-only retry of the citations
case at a 4,096-token context cap. Base made four evaluator-local tool rounds
and passed 3/7 unvalidated checks; v63 made zero tool rounds and passed 2/7.
Estimated usage was $0.00213775 under $0.06 and $0.012 caps; actual charges
are unknown. This confirms no tool behavior recovery at v63; the checks remain
synthetic diagnostics. See the [v63 evaluation report](execution-2026-10-19/wandb-v63-five-case-paired-eval-2026-10-20.md).

At 10:08 UTC the event observer advanced to step 32,297/85,631 (loss 4.039);
the event stream continued to advance and the job remained `RUNNING` without
a reported error. The step loss remains elevated and noisy in this segment;
it is not itself a model-quality or corruption test. Both v63 local mirrors
remain present, and their watchers are still alive.

At 10:12 UTC, a fresh authenticated W&B GraphQL read showed the organization
subscription enabled on `ACADEMIC_TRIAL`, with `storage_gigs=200`; its
last-30-day cumulative storage daily average was 166,026,268,417 bytes
(approximately 166.03 decimal GB), leaving about 33.97 decimal GB against that
entitlement measure. The project `storageBytes` was 66,290,448,324 bytes
(66.29 decimal GB). This does not mean 33.97 GB of instantaneous worker-disk
space, and neither field identifies the user's deleted objects. No artifacts
were deleted or modified by the query. Snapshot:
[`wandb-storage-entitlement-refresh-20261020T1012Z.json`](execution-2026-10-19/wandb-storage-entitlement-refresh-20261020T1012Z.json).

At 10:14 UTC the event observer advanced v4 to step 32,605/85,631 (loss
3.1603, throughput about 107 tokens/second), still `RUNNING` with no reported
job error. Both the adapter and train-state watchers independently captured
v64 at 32,500 batches. The adapter mirror is 117,843,308 bytes and its two
files match the local manifest; the train-state mirror is 1,060,414,709 bytes.
This verifies local recovery for the latest checkpoint pair while training
continues. Job `updated_at` remains stale at 2026-10-19 22:50:52Z, so rely on
the advancing event stream and artifacts for progress evidence.

At 10:16 UTC the event observer advanced to step 32,713/85,631 (loss
3.1381); the job still reports `RUNNING` without a surfaced error. Both
checkpoint watchers remain alive; the latest captured adapter and train state
are v64 at 32,500 batches. This poll confirms the event stream is advancing,
while no newer checkpoint has yet appeared.

#### 2026-10-20 v64 paired diagnostic

Compared the v64 adapter with base on the same five synthetic development
cases, with explicit no-thinking decoding and separate bounded retry for the
base citations case. Base completed five visible responses, with four tool
rounds on completed responses and 3/7 unvalidated deterministic checks; v64
completed five visible responses, made zero tool rounds, and passed 2/7. Four
of v64's five outputs reached the 1,024-token cap. Estimated usage was
$0.006461 paired plus $0.000493 for the base retry; actual billing is unknown.
This checkpoint does not recover tool behavior. Full hashes, config, and
latency details: [v64 evaluation report](execution-2026-10-19/wandb-v64-five-case-paired-eval-2026-10-20.md).

At 10:19 UTC, the active W&B v4 event stream reached step 32,873/85,631
(loss 2.7713); job status remained `RUNNING` without a surfaced error. The
latest adapter and train-state mirrors remained v64 at 32,500 batches. Based
on the recent 50–55 steps/minute, the remaining 52,758 steps imply roughly
16–18 hours if throughput stays near that pace; this is a live-rate estimate,
not a provider completion commitment.

Adaption's current AutoScientist schema has no validation split or
disable-validation control, and both supported raw-data formats already fail
on the empty generated validation JSONL. No more training attempts were
launched. A provider diagnostic packet with the dataset and failed-run IDs,
requested internal counters, and safe support channels is documented in the
[Adaption refresh](execution-2026-10-19/adaption-credit-and-dataset-refresh-2026-10-20.md).

The second R2 content sweep checked three additional candidate source copies,
including the 64,536-row transformed counseling payload. All returned 0/369
matches under the same normalized ordered-turn comparison; exact hashes and
row counts are in the [origin-binding report](execution-2026-10-19/counseling-conversations-v4-upstream-origin-binding-2026-10-20.md).

At 10:21 UTC the event observer advanced to step 32,980/85,631 (loss 2.694);
the v4 job remains `RUNNING` without a reported error, and the mirrored
checkpoint pair remains v64 at 32,500 batches.

The 120-case prompt-disjoint paired v64/base comparison and its 45-case
base-only context retry are complete. Across all cases, base made 132 tool
rounds across 252 completion calls and passed 71/75 tool-status and 75/75
response-content checks. V64 made zero tool calls and passed 0/75 tool-status
and 0/75 response-content checks; 77/120 outputs hit the 512-token cap. Both
arms returned a visible response for every case. Estimated combined usage was
$0.12545625 under $1.50 and $0.40 caps; actual billing is unknown. The
first-attempt manifest remains incomplete because it records the 45 base
context-preflight failures; its retry manifest is complete. See the [full v64
120-case report](execution-2026-10-19/wandb-v64-prompt-disjoint-heldout120-eval-2026-10-20.md).

At 10:35 UTC, the active v4 W&B event observer reached step 33,722/85,631
(loss 2.8071), and both adapter and train-state watchers mirrored v66 at
33,500 batches. The job remains `RUNNING` without a surfaced error.

#### 2026-10-20 W&B agent-tool reconciliation retry boundary

The synthetic agent-tool package remains uploaded, but its model-create call
timed out and the durable launcher state remains
`model_creation_submitted_unknown`; there is no model UUID or training job ID.
A read-only `GET /preview/models` probe, with and without project query
parameters, returned HTTP 405, so it does not expose a model inventory. The
official Create Model docs define `return_existing=true` as returning the
existing same-named model, so I repeated the exact named request safely to
recover the UUID; that request also timed out after 60 seconds. `GET
/preview/models` is unsupported (HTTP 405), and the Training API docs list no
model-list route. State still has no model UUID or training-job ID. No SFT-job
request was made. Next resolution needs an authenticated owner UI or
provider-supported lookup; the uploaded artifact can be reused. See the
[launch reconciliation](execution-2026-10-19/wandb-agent-tool-sft-launch-reconciliation-20261020.md).

#### 2026-10-20 10:41 UTC W&B storage and run refresh

An authenticated read-only W&B GraphQL refresh at 10:40:46 UTC found the
organization subscription still enabled on `ACADEMIC_TRIAL` with
`storage_gigs=200`. The organization trailing 30-day cumulative average was
166,026,268,417 bytes (166.03 decimal GB), leaving approximately 33.97 decimal
GB against that entitlement measure. The project `storageBytes` meter had
increased from 66,290,448,324 bytes at 10:12 UTC to 69,118,476,834 bytes
(69.12 GB). The project meter is not the organization quota and does not
identify which objects account for the increase; the trailing average had not
changed in this refresh. Neither reports free CoreWeave worker disk. No
artifacts were deleted or modified. See the [10:40 storage snapshot](execution-2026-10-19/wandb-storage-entitlement-refresh-20261020T1040Z.json).

At 10:41:45 UTC the active W&B v4 event observer advanced job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` to step 34,040/85,631 (loss 3.1290).
It remains `RUNNING` with no reported job error; provider `updated_at` is still
stale, so the event observer is the progress source. Adapter and train-state
backup processes are alive, and both have verified local v66 mirrors at 33,500
batches (117,842,120-byte adapter weights and 1,060,414,709-byte train state).
No v67 checkpoint had appeared by the latest watcher polls at 10:40 UTC. The
event stream advancing past 34,000 while the mirrored checkpoint remains v66
means training is progressing, but the next checkpoint publication is still
pending verification.

At 10:45 UTC both watchers mirrored v67 at 34,000 batches; the adapter is
117,843,308 bytes and the train-state is 1,060,414,709 bytes. The event
observer advanced to step 34,200/85,631 at 10:44:47 UTC, with no reported job
error. A capped inference-credit evaluation of v67 then completed all 120
prompt-disjoint synthetic cases: zero tool rounds, 0/75 tool-status and
response-content checks, 0/15 memory-value checks, 45/60 state-value checks,
and 15/15 response-omission checks. Only 2/120 outputs reached the 512-token
cap, down from 77/120 for v64, but the deterministic behavior scores did not
improve. Estimated inference usage was $0.01400225 under a $0.75 hard cap
(worst-case bound $0.6912); actual billing is unknown. Full run hashes and
paired base comparison are in the [v67 evaluation report](execution-2026-10-19/wandb-v67-prompt-disjoint-heldout120-eval-2026-10-20.md).

The Adaption app's documented final Summary page shows available credits and
the exact Adaptive Data job cost before launch. The AutoScientist app
walkthrough describes reviewing its model/recipe proposal, but does not
document an estimate-only training cost there. The API still has no account
balance or AutoScientist estimate endpoint. A fresh Browserbase session reached
the Adaption login page, with no authenticated browser context available; no
login or job submission occurred. The exact documented UI path and status are
in the [Adaption refresh](execution-2026-10-19/adaption-credit-and-dataset-refresh-2026-10-20.md).

At 10:46:48 UTC the W&B v4 event observer advanced to step 34,309/85,631
(loss 2.5784); job status remains `RUNNING` without a surfaced error. Latest
verified local checkpoint pair remains v67 at 34,000 batches.

#### 2026-10-20 10:58 UTC live training refresh

The official [CoreWeave Serverless Training docs](https://docs.coreweave.com/products/post-training/serverless-training)
explicitly label Serverless SFT as public preview and state that training is
free during the preview; inference and artifact storage are charged. Keep this
as the documented offer. The separate Forge page that lists SFT/RL at
$2.70/GPU-hour is a billing-account reconciliation item, not a reason to
soften or omit the docs' preview statement.

The active W&B v4 run reached step 35,000/85,631 at 10:59:58 UTC (loss
2.3704; reported throughput 80.49 tokens/s). The job is still `RUNNING` with
no surfaced error. Both local checkpoint watchers are alive; latest verified
adapter and train-state are v68 at 34,500 batches (117,842,120-byte adapter
weights and 1,060,414,709-byte train state). The event observer was restarted
and is actively polling again. Its local progress and watcher logs remain
under `ai/training/output/wandb_local_checkpoints_20261019/`.

The Fireworks agent-tool SFT has now started in Serverless Training. The
run ID is `pixelated-agenttool-20261020-r8-1ep`, session
`ts-29847e445cee48409993881866c9156c`. This is the 960-row first-party
synthetic agent-tool train split, with the separate 120-row validation split;
all assistant messages including tool calls are supervised. Settings are one
epoch, batch 16, LR `1e-5`, LoRA rank 8/alpha 32, and 2,048 max sequence
length. No persistent model promotion is requested. The initial base
validation finished 120/120 rows with exact match 0/120 and no unterminated
outputs. SFT has started and reached 15/60 steps by 10:59 UTC; recent per-step
losses are in the private run log. The launcher will run the prompt-disjoint 120-case paired mock-tool
test against base and SFT samplers before closing the session. Its offline
preflight passed with max input 2,048, two tool rounds, 256 output tokens, and
a $3.7896192 worst-case estimate under the $4 cap. The validation output is
limited to 512 tokens. See the [Fireworks execution report](execution-2026-10-19/fireworks-agent-tool-sft-2026-10-20.md).

At 11:25 UTC the W&B event observer reported step 36,381/85,631 (loss
2.0408); status remains `RUNNING`, with no surfaced job error. The adapter
watcher has locally verified v71 at 36,000 batches; train-state watcher remains
active.

The Fireworks built-in base/tuned validation finished 120/120 each: exact
match 0/120 base and 120/120 tuned, with no unterminated outputs. Its first
paired tool pass finished all 240 arm/case records but is marked incomplete:
182 successes and 58 context-cap/tool-round errors. Total estimated sampling
usage was $0.71031576; actual billed amount is unknown. The failure pattern
showed the conservative ASCII-byte context counter was overestimating Muse
Glimmer token usage (the exact renderer counted initial prompts at 447–562
tokens, versus byte-counter values up to 1,224). A corrected exact-token
rerun has started against the retained Fireworks session snapshots, capped at
$2 worst case; the first base case completed within the limit at 512/617/725
tokens across its three turns. It is not yet a final tool-use result. See the
[Fireworks execution report](execution-2026-10-19/fireworks-agent-tool-sft-2026-10-20.md).

#### 2026-10-20 11:33 UTC live run refresh

The official [CoreWeave Serverless Training docs](https://docs.coreweave.com/products/post-training/serverless-training)
still explicitly state that Serverless SFT is in public preview and that
adapter training is free during preview. This remains the documented offer
for the campaign; inference and artifact storage are separately billed. The
Forge rate card's paid SFT listing is a separate published-page conflict to
reconcile against account billing, not a correction to the preview statement.

The W&B full-corpus v4 run remains `RUNNING`, with the event observer at step
36,590/85,631 (loss 2.5611). Both checkpoint watchers remain active and have
verified local v72 adapter and train-state mirrors at 36,500 batches; the
adapter is 117,842,120 bytes and train-state is 1,060,414,709 bytes. This
confirms the run is publishing new checkpoints while training continues.

The corrected Fireworks exact-renderer paired evaluation is still running but
has not advanced beyond its first successful base case. The tuned-checkpoint
sampling request has remained pending for over eight minutes; the process and
HTTPS connections are live, with no returned provider error. Leave this
request in flight and treat the paired comparison as pending, not failed. Its
hard cap remains $2; the first case recorded 512/617/725 prompt tokens and
estimated $0.005254. Output is in the private run directory
`ai/training/output/fireworks_agent_tool_20261020/pixelated-agenttool-20261020-r8-1ep-exact-token-eval/`.

At 11:34 UTC, the W&B event observer advanced to step 36,806/85,631 (loss
2.7823); the job remains `RUNNING` with no surfaced error. The latest verified
local adapter and train-state mirrors are still v72 at 36,500 batches, so the
next periodic mirror is pending. The Fireworks exact-token evaluator remains
alive at 11:03 elapsed with one persisted case; its tuned-checkpoint request
is still pending and has returned no error. A read-only Fireworks checkpoint
list confirms the tuned checkpoint exists, is marked promotable, and matches
the configured canonical API resource name. Keep the sample request in flight;
checkpoint identity does not establish inference readiness.

#### 2026-10-20 11:36 UTC poll

The W&B observer is still receiving training events: step 36,916/85,631 at
11:36:19 UTC (loss 3.2992). The job remains `RUNNING`. The adapter mirror is
still v72 at 36,500 batches (last observed 11:35:45); the train-state watcher
refreshed at 11:36:37 and also remains at v72. Fireworks' exact-token paired
evaluator remains alive at 13:07 elapsed with one persisted case. The active
tuned request has not returned; the SDK's streaming sampler defaults to a
600-second HTTP timeout and retries transient failures. A slow request is not
yet terminal evidence. The read-only checkpoint listing still confirms the
configured tuned checkpoint exists and is promotable.

At 11:37 UTC, the exact-token Fireworks evaluator logged its first tuned
checkpoint sampling failure: `ReadTimeout` after the SDK's 600-second HTTP
request timeout. The SDK classified it as transient and is retrying (attempt
1/7 had failed). The tuned checkpoint still exists and is marked promotable,
so this is evidence of an inference-request timeout, not a missing checkpoint
or training-job failure. The evaluator remains alive; no paired result is
complete yet. W&B's observer reached step 36,970/85,631 at 11:37:19 UTC (loss
3.5737), still `RUNNING`; local checkpoint mirrors remain v72/36,500 batches.

#### Fireworks route-corrected paired run — 2026-10-20 11:38 UTC

The timed-out exact-token attempt was stopped after its flattened checkpoint
name produced an SDK `ReadTimeout` on the first tuned sample. The earlier
successful session evaluator records the tuned snapshot as
`linencloset/<run-id>/starter-tuned-48b75a39`; the sampler SDK expands that
snapshot path under the session checkpoint route. I corrected the direct
sampler route to use that same session snapshot path and preserved the timed
out attempt as `interrupted_route_correction` with its one completed base
record.

The replacement full 120-case exact-token paired run is active at
`ai/training/output/fireworks_agent_tool_20261020/pixelated-agenttool-20261020-r8-1ep-exact-token-eval-route-corrected/`.
Its offline preflight has zero provider calls, exact Muse renderer token counts,
and a $1.8609408 worst-case estimate under the $2 cap. The first five records
are successful (three base, two tuned), confirming that the corrected tuned
route now returns samples. This is an interim execution check; no final paired
scores are available yet.

At 11:40 UTC, the corrected Fireworks paired evaluator remains active and has
persisted nine successful arm/case samples (five base, four tuned), with no
errors. The next sample is the base arm for `tool-eval-resource_lookup-139`;
usage remains below the $2 estimate ceiling. W&B's event observer advanced to
step 37,123/85,631 at 11:40:21 UTC, with the job still `RUNNING`. Its local
adapter and train-state mirrors have not yet advanced from v72/36,500 batches;
the next checkpoint mirror is pending.

The exact-token, route-corrected 2-round run reached 43 persisted records at
11:42 UTC (31 successes; 12 `ToolRoundLimitExceeded` errors, all in the
resource-compare family). This shows that two rounds are insufficient for
those cases on both arms, not that either endpoint failed. I prepared an
exact-token 4-round full-suite dry run: all 120 cases validate with zero
provider calls and a $3.101568 worst-case estimate under a $4 cap. After the
current $2-bounded 2-round run finishes, use the 4-round run to obtain a
complete paired comparison under the evaluator's supported 4-round limit.

At 11:46 UTC, the W&B observer advanced to step 37,451/85,631; adapter and
train-state v73 remain the latest local mirrors at 37,000 batches. The last
12-minute interval advanced 645 steps, about 53 steps/minute. At that recent
rate, the current W&B training job has roughly 15 hours of training left
(48,180 steps); this is a live-run estimate and can move with throughput. It
is not a wait gate for finishing the Fireworks comparison, dataset lineage
work, or other campaign tasks.

The route-corrected Fireworks exact-token run is currently at 59/240 records.
The resource-compare cases are limited by the two-round cap; the case-149 base
and tuned requests have returned/retried transient 503/`SamplingRequestError`
conditions, so keep provider errors separate from the planned round-limit
follow-up. Estimated sampling usage remains below $0.25; the 4-round full-suite
preflight remains $3.101568 under its $4 cap.

At 11:49 UTC, the route-corrected Fireworks run has 62/240 persisted records:
33 successes and 29 errors. Twenty-five errors are the expected two-round cap
in resource-compare cases; four are `SamplingRequestError` records across the
resource-compare and memory-opt-in scenarios, with SDK logs showing repeated
HTTP 503 retry responses. Estimated sampling use is $0.23351072; actual billed
usage is not exposed. Fireworks' official [status page](https://status.fireworks.ai/)
currently reports Serverless fully operational, but its component list does
not name Muse Glimmer or this session checkpoint. Treat that public status as
non-specific and retain the observed per-request 503s as the relevant evidence.

#### 2026-10-20 11:53 UTC storage and live-run reconciliation

A fresh W&B read shows project `storageBytes` at 76,659,882,751 B (76.66 GB)
and the organization subscription at 200 GB with trailing 30-day cumulative
average 166,026,268,417 B (166.03 GB), about 33.97 GB below that measure. The
project meter is up 7,541,405,917 B from 10:40 UTC while active checkpoint
creation continued. These values do not report CoreWeave worker disk or prove
a storage limit has been reached.

The v4 LoRA and train-state collections each have 75 visible versions through
v74 at 37,500 batches. I audited older v4 train-state versions v0-v72: all 73
have no aliases and zero `used_by()` dependencies, totaling 77,410,273,349 B
(77.41 GB) logical. Keep v73/v74; if artifact cleanup is needed, those exact
older train-state versions are the clearest candidates. This reduces old
resume points, and logical bytes do not guarantee physical reclaim. No
artifacts were deleted. The per-version audit is private at
`ai/training/output/wandb_local_checkpoints_20261019/v4-train-state-cleanup-audit-v74.json`;
the [storage snapshot](execution-2026-10-19/wandb-storage-entitlement-refresh-20261020T1153Z.json)
and [artifact triage](execution-2026-10-19/wandb-artifact-storage-triage-2026-10-19.md)
record details.

At 11:53:27 UTC, the W&B observer reached step 37,821/85,631 (job still
`RUNNING`, no surfaced error). Latest local adapter and train-state mirrors
remain v74 at 37,500 batches. The route-corrected Fireworks exact-token run
has 65/240 records; its new requests are encountering repeated HTTP 503s and
being retried by the SDK. Its estimated usage remains $0.233511; this is
inference trouble on the session endpoint, separate from the training run.

#### 2026-10-20 11:55 UTC Fireworks sampler stop and W&B live progress

The route-corrected Fireworks exact-token paired evaluator was stopped locally
at 66/240 arm-case records after repeated HTTP 503 retries made each request
consume roughly 60-100 seconds. Its preserved partial contains 33 successful
rows, 25 `ToolRoundLimitExceeded` rows from the configured two-round cap, and 8
`SamplingRequestError` rows; result digest is recorded in the private manifest
at `ai/training/output/fireworks_agent_tool_20261020/pixelated-agenttool-20261020-r8-1ep-exact-token-eval-route-corrected/results/manifest.json`.
This is not a completed comparison. The $1.8609408 estimate was a worst-case
preflight under the $2 cap; actual billing remains unknown. The next Fireworks
step is to establish a serving-ready endpoint for this checkpoint or conduct
sampling inside an active training session before spending more inference
requests. Do not count HTTP 503s as model-quality failures.

At 11:55:29 UTC, the W&B full-corpus job
`24cc2d06-3ec3-4356-ad3a-179694dd86a7` remained `RUNNING` with no surfaced
error and had advanced to 37,932/85,631 gradient steps (training loss
1.792738; throughput 382.84 tokens/s). Local adapter and train-state mirrors
remain v74 / 37,500 batches; the worker has not yet published the next
checkpoint version. W&B Serverless Training docs still explicitly label SFT
as public preview and state adapter training is free during preview; inference
and artifact storage are separately charged. Account billing is not inferred
from those published terms.

#### 2026-10-20 11:58 UTC checkpoint and serving follow-up

W&B's event observer reports the full-corpus job still `RUNNING`, with no
surfaced error, at 38,088/85,631 steps at 11:58:31 UTC. Local v74 remains the
newest complete adapter; train-state v75 has appeared but adapter v75 has not.
The paired five-case W&B inference comparison of base vs v74 completed 10 rows
(9 successful, 1 base context-preflight failure). The base made four tool
rounds and passed 3/6 scored unvalidated synthetic checks; v74 made zero tool
calls and passed 2/7. Estimated use was $0.001316 total, actual billing
unknown. See [v74 evaluation](execution-2026-10-19/wandb-v74-five-scenario-dev-eval-2026-10-20.md).

A read-only Fireworks session GET returned HTTP 200 with status
`DEADLINE_EXCEEDED` and state `EXPIRED` for the completed Muse Glimmer session.
The Fireworks sampler partial remains incomplete at 66/240 records (33 success,
25 two-round-limit errors, 8 repeated-503 request errors); no promotion or
paid deployment was attempted. The session-scoped path has expired, so that
checkpoint is not currently available for further evaluation under the
experiment-only/no-promotion constraint.

The next fully mirrored W&B checkpoint, v75 at 38,000 batches, was evaluated
against the same five-case suite. It reproduced v74's exact check pass/fail
pattern: SFT made zero tool calls and passed 2/7 checks; base made four rounds
and passed 3/6 scored checks, with one context-cap failure. Estimated usage was
$0.001421. Do not widen v75 to 120 cases without a sentinel improvement. See
[v74/v75 checkpoint comparison](execution-2026-10-19/wandb-v74-five-scenario-dev-eval-2026-10-20.md).
