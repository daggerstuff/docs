# V5 full-scale model comparison

## Experimental question

At equal data and SFT settings, which of the two approved base models better
learns the project response behavior on the untouched v5 test split: Gemma 4
26B A4B Instruct or Nemotron 3.5 Lightning?

## Controlled training arms

| Arm | Base model | W&B training job | Task ID | State |
| --- | --- | --- | --- | --- |
| Gemma 4 | `google/gemma-4-26B-A4B-it` | `f41de815-2789-48d8-914d-23c3b9e256b3` | `5c243e8ea48328b9ad2459e94f32072d8d340f0533cbcce1373a9dcdf6e4d333` | Created 2026-10-20; `RUNNING` at 15:08 UTC |
| Nemotron 3.5 | `nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B` | `b46708dd-9726-44f1-a699-62641ecc49e1` | `08ea5de19e5850228494de3382c3d774daa6ec9c8cdebeff93825472321a6af0` | Created 2026-10-20; `RUNNING` at 15:08 UTC |

Both jobs use release `wandb-full-corpus-current-master-20261019-v5`, the
same train SHA-256
`29eea24ce984754eeeb4321ef61301cc7149b92edc430c95591797f4f31cdfbf`, all
77,718 train rows, assistant-only loss on all assistant turns, batch size 16,
and scalar learning rate `1e-5`. The previous v5 launcher supplied an LR list
and an undocumented metric-logging field; both were removed before upload.
Each packaged dataset artifact measured 202,801,904 bytes. Dry-runs passed for
both allowed model IDs before either upload. The 9,310-row test split and
9,673-row validation split remain separate from training.

## Preservation and evaluation

At 15:10 UTC, the provider returned a step-0 checkpoint for Gemma and both
step-0 adapter artifacts were downloaded and SHA-256 verified locally (Gemma:
123,742,920-byte adapter; Nemotron: 1,873,896-byte adapter). These are
initialization checkpoints, not trained results. The adapter mirror now tracks
both artifact collections under the ignored/private directory
`ai/training/output/wandb_v5_local_backups`; a resume-state watcher is active
too. The artifact collections exposed different per-model LoRA defaults:
Gemma rank 1 targeting attention, MLP, and expert modules; Nemotron rank 8
targeting attention projections. W&B's accepted SFT config does not expose a
common rank/target-module override, so this is a comparison of each model's
provider-default adapter recipe under matched data and exposed SFT settings,
not a pure architecture-only comparison. No remote artifacts are deleted.

At 15:19 UTC both jobs remained `RUNNING`. The event API defaults to 20 events
per page; paginating it showed 461 Gemma steps and 465 Nemotron steps (their
start times differ by about 53 seconds). The first observed train losses were
8.01 and 2.31, and the latest were 1.14 and 1.84 respectively; minima so far
were 0.68 and 0.77. These per-batch losses are noisy and not comparable across
architectures. Gemma's gradient norm peaked at 450.80 but later settled;
Nemotron's peak is 1.63. The Gemma spike is being
monitored through the first 500-step checkpoint.
`training_started` reports 4,858 gradient steps, consistent with packing the
77,718 examples at 16 examples per sequence. Wall-clock progress works out to
about 36-37 gradient steps per minute so far, implying roughly 2.2 hours
for the 4,858-step epoch, subject to throughput variation. Step-0 adapters
are safely mirrored; neither run has a trained checkpoint locally yet.
At 15:21 UTC the jobs had passed step 500 (Gemma 535, Nemotron 562), but the
model-checkpoint API and the initially queried base-model collections still
showed only step 0. The jobs continued emitting gradient events without an
error. The actual trained streams were in separate `*-sft-resume` collections,
which the first mirror lookup had missed.

Follow-up found the trained artifacts in separate
`*-sft-resume` collections. Both providers wrote adapters and resume states at
500 completed batches: Gemma adapter 61,907,664 bytes and train-state
565,725,299 bytes; Nemotron adapter 1,873,896 bytes and train-state
14,998,923 bytes. All four artifacts were downloaded locally and SHA-256
verified. The Training API model-checkpoint list still exposes only step 0;
the `sft-resume` collection is the authoritative saved-checkpoint evidence
for these runs, and the local mirror now follows those collections.

Serving is model-specific. The Gemma base ID responds successfully, but both
its initialization artifact and its 500-batch adapter return HTTP 500 with
`backend_status: 500` through the trained-artifact serving route. The saved
Gemma tensors are complete and finite (540 tensors, 30,917,760 parameters;
maximum absolute value 1.49), and its training job remains healthy. Nemotron's
base, step-0 adapter, and 500-batch adapter all respond successfully. This
isolates the current failure to Gemma adapter serving/registration rather than
failed training or missing weights; no provider-side diagnostic beyond the
generic 500 is exposed. The full Gemma held-out inference was stopped after
111/1,000 base responses were preserved because no matching SFT arm could be
served. Its trained job and checkpoint mirroring continue.

At 15:29 UTC the jobs were at 897/4,858 (Gemma, latest batch loss 0.988) and
1,000/4,858 (Nemotron, 1.23), both still `RUNNING`. Nemotron base evaluation
had 608/1,000 unique cases and the 500-batch SFT evaluation had progressed
beyond its earlier 174/1,000 snapshot; neither had request errors at that
snapshot. The Gemma base partial had 111 cases and no errors, but is not a
paired result. Recorded token-based estimated usage at 15:27 UTC was $0.3107
for Nemotron base, $0.0474 for its SFT responses, and $0.0617 for Gemma base;
the API exposes no actual-billed amount.

An interim paired analysis of the first 251 matching Nemotron cases at
step 500 showed mean completions of 354 tokens for base and 181 for SFT;
512-token truncation fell from 53.4% to 22.3%. Held-out target unigram F1 rose
from 0.0590 to 0.0764, a +0.0174 paired delta with a bootstrap 95% interval
from +0.0056 to +0.0294. Mean latency decreased from 1.99s to 1.44s. This is
an early lexical and efficiency signal; semantic and clinical scoring plus
the complete 1,000-case paired set remain pending. Snapshot metrics and
file hashes are in the private interim record under the output directory.

After trained checkpoints become available, compare each SFT checkpoint with
its own base model on the same held-out prompts, then compare the two SFT arms.
Report
paired deltas with confidence intervals for reference-grounded content,
clinical quality, safety/resource coverage on crisis cases, response
usefulness, latency, and tokens. Keep synthetic tool-use cases separate: this
release contains no tool-call messages, so those cases do not measure the
training target. Record checkpoint step, inference endpoint, result hashes,
and any incomplete/error counts. Training is research-only; passing this
comparison does not establish clinical or production readiness.

The local held-out set contains 1,000 deterministically sampled cases from all
9,310 test rows, weighted proportionally across single-turn/two-turn/longer
dialogues and short/medium/long contexts (seed `20261020`). Its prompt digest
is `2401df958e2497bdd37de0830a58dfaaaac190b8c2de02cb897ff3149057d2e2`; the
reference sidecar digest is
`f025fbfe3f326fab33fc8505c597f17c3443d9b9831352a9ab14731d17ffc29c`. The
`paired_eval` wrapper now accepts the existing sealed-set opt-in. Base
generation uses the W&B Training API endpoint and 512-token deterministic
decoding. At the 57,344-token preflight limit, the worst-case run cap is $15.10
per model; this is a ceiling, not projected actual usage. A serial run was too
slow for Gemma, so completed rows are preserved and the remainder is split
across two shards per model. Combined per-model worst-case caps stay below
$15.10. At 15:19 UTC there were 19/1,000 Gemma and 113/1,000 Nemotron base
responses, with no request errors; 13 and 59 respectively reached the
512-token output cap. The Gemma base endpoint is much slower in this run, so
latency and output truncation will be first-class outcomes in the comparison.

## Storage and billing caveat

At 15:22 UTC, authenticated W&B GraphQL read project storage at 14,111,450,846
bytes, up from 12,634,241,300 bytes at 15:03. The organization subscription
was enabled with a 200 GB storage entitlement and a 30-day daily-average
storage use of 166,026,268,417 bytes (about 33.97 GB below the entitlement).
That measure is trailing-average entitlement usage, not instantaneous free
space or CoreWeave worker-disk capacity. The v5 checkpoint artifacts are
visible in W&B and mirrored locally, so storage exhaustion did not prevent
these 500-batch checkpoint writes. No artifact cleanup was performed.

The old Qwen job's Training API status still returns HTTP 500 and its
checkpoint endpoint returns 404, so its current state remains unknown.

## Gemma v5 serving recheck

The Gemma v1 resume artifact is present locally and remotely at 1,000
completed batches (adapter SHA-256
`2a4fb6527e01477e740d195ceda6977335574c181e9d7bd2603c8e54ac52d509`). On the
same held-out prompt, base succeeded and the trained v1 artifact returned
HTTP 500 through the Training API route; the provider exposed only
`backend_status: 500` (error-body SHA-256
`9742eb54c11357f3a2a9f5ad0f3835a57c809b18fd9c51fbba153e8a88d26be4`). A
second request to the **same v1 artifact and prompt** through
`api.inference.wandb.ai` succeeded. This isolates the observed failure to the
Training API relay path for v1; the adapter is usable through direct
inference. The paired 1,000-case Gemma base/v1 evaluation is running through
that direct endpoint.

## 15:32 UTC update

The two full-scale v5 jobs remain `RUNNING` with no reported job error. A
paginated event scan (the first page alone is stale) found Gemma at
966/4,858 gradient steps, latest train loss 1.229, and Nemotron at 1,092/4,858,
latest train loss 1.330. The local artifact mirror now has Nemotron adapter
versions v0 and v1 plus matching resume state; Gemma's v0 adapter and resume
state remain mirrored.

The Nemotron inference comparison now includes the 1,000-batch checkpoint.
At this incomplete snapshot there are 761 successful base, 555 successful
step-500, and 188 successful step-1,000 responses, with no recorded request
errors in any completed shard. Pairing by case ID gives 473 base/step-500
pairs, 106 base/step-1,000 pairs, and 188 step-500/step-1,000 pairs. On the
paired step-500 sample, target unigram F1 improves by 0.0191 over base (paired
bootstrap 95% CI 0.0097 to 0.0289); 512-token truncation drops from 53.3% to
21.8%, mean completion length from 355 to 178 tokens, and mean latency from
2.01s to 1.36s. On the smaller paired step-1,000 sample, F1 improves by 0.0460
over base (95% CI 0.0262 to 0.0686), and by 0.0117 over step 500 (95% CI
0.0014 to 0.0225). The latter's current means are 133 vs 176 completion
tokens, 14.4% vs 22.3% truncation, and 1.04s vs 1.44s latency. These are
interim, case-overlap-dependent lexical and serving-efficiency results, not
clinical-quality scores. The exact result-file hashes and full metric payload
are stored in the private `paired-interim.json`; the reproducible aggregator
is `ai/training/analyze_wandb_v5_paired_eval.py`.

The step-1,000 evaluation uses the same 1,000 held-out cases in two
deterministic shards and is continuing. Complete paired coverage remains the
next result gate; after that, score crisis/safety and usefulness dimensions
separately rather than treating target word overlap as a proxy for quality.

At 15:33 UTC the eval grew to 835 successful base, 677 successful step-500,
and 298 successful step-1,000 responses. Updated paired counts are 595,
216, and 298 respectively. The matched step-500 delta is now +0.0235 unigram
F1 (95% CI +0.0143 to +0.0329); step 1,000 is +0.0282 over base (95% CI
+0.0161 to +0.0415) and +0.0128 over step 500 (95% CI +0.0038 to +0.0224).
Across the paired 500/1,000 samples, the 1,000-step model also remains shorter
(152 vs 180 tokens), is cut off less often (17.4% vs 22.5%), and responds
faster (1.14s vs 1.42s). These partial overlaps will change as shards finish.

The step-500 result was also split by the predeclared scenario buckets. Among
446 matched short-context cases, target F1 was 0.0623 base vs 0.0864 SFT and
512-token truncation 52.9% vs 22.0%. Among 81 medium-context cases, F1 was
0.0543 vs 0.0701 and truncation 61.7% vs 25.9%. The long-context bucket has
only six pairs and is inconclusive. The held-out set is dominated by
single-context short cases and contains no crisis-specific benchmark, so this
run cannot establish crisis-safety or long-context performance. Both training
jobs remain active; the latest paginated event scan was Gemma 1,050/4,858 and
Nemotron 1,201/4,858, with no job errors. Eval samples and metrics remain
private because they contain generated clinical content.

## 15:38 UTC snapshot (superseded by the corrected analysis below)

Nemotron base evaluation has 918/1,000 successes, the step-500 evaluation
1,000/1,000, and step-1,000 evaluation 746/1,000. No failed inference records
are present in the completed shards. On paired cases, step 500 is +0.0173
reference unigram F1 over base (918 pairs; 95% CI +0.0103 to +0.0246), and
step 1,000 is +0.0357 over base (653 pairs; +0.0274 to +0.0442) and +0.0141
over step 500 (735 pairs; +0.0082 to +0.0203). Step 1,000 is also shorter and
faster: 154 vs 174 completion tokens and 1.17s vs 1.32s over their matched
step-500/1,000 cases; 512-token truncation is 18.8% vs 21.4%. These are
paired, partial results; the 82 remaining base and 254 remaining step-1,000
responses are still running. Machine-readable metrics and current file hashes
are in the private `paired-interim.json`.

A blinded pairwise judge pass is now running on 300 sampled base/step-500
pairs, with Gemma 4 base as the judge, candidate order randomized, and a
predeclared 0-4 rubric for relevance, grounding, helpfulness, empathy, and
safety. All 15 available long-context cases are included; the rest are sampled
from short and medium contexts. At 15:38 it had 33/300 successful judgments,
no provider errors, and about $0.027 estimated usage against a $4 hard cap per
150-case shard ($8 combined maximum). This is a blinded model-judge diagnostic,
not independent clinical validation; the rubric, responses, and outputs stay
local/private. Training has advanced to Gemma 1,315/4,858 and Nemotron
1,502/4,858; both remain `RUNNING` without job errors.

## 15:40 UTC correction and next comparisons

The 15:38 Nemotron base denominator omitted the initial 82-case base shard
(`nemotron35-base`); the two later shards covered the other 918 cases. The
aggregator and documented results now include all three base directories.
Corrected totals are 1,000/1,000 base, 1,000/1,000 step 500, and 926/1,000
step 1,000, all completed records successful. Paired deltas are +0.0187 F1
for step 500 over base (1,000 pairs; 95% CI +0.0121 to +0.0255), +0.0355 for
step 1,000 over base (926 pairs; +0.0287 to +0.0427), and +0.0152 for step
1,000 over step 500 (926 pairs; +0.0096 to +0.0210). At 926 matched
step-500/1,000 cases, step 1,000 averages 160 vs 179 completion tokens,
20.2% vs 22.8% output truncation, and 1.19s vs 1.34s latency. The prior
15:38 numbers should be disregarded; the private analysis record has the
corrected result hashes.

The Gemma v1 direct-inference paired run has started over all 1,000 held-out
cases in four 250-case shards. Its first sampled calls show the base and
trained direct endpoints succeeding; the shards remain active. The previous
Gemma relay smoke still fails, so the direct-vs-relay endpoint difference is
now being tested at full scale.

The 300-pair blinded judge pass had 139 successful judgments across short,
medium, and long-context cases, with no provider errors. Estimated usage was
about $0.105 against the $8 combined hard cap. It remains unscored until the
JSON outputs are parsed and checked for schema validity.

## 15:42 UTC full Nemotron result

All three Nemotron inference arms now have 1,000 successful held-out responses:
base, step 500, and step 1,000. There were no recorded inference errors. On
the full paired set, step 500 improves target unigram F1 by +0.0187 over base
(95% bootstrap CI +0.0121 to +0.0255); step 1,000 improves by +0.0345 over
base (+0.0280 to +0.0414) and +0.0159 over step 500 (+0.0105 to +0.0214).
For base versus step 1,000, mean output falls from 356 to 161 tokens,
512-token truncation from 54.4% to 20.1%, and mean latency from 2.05s to
1.18s. For step 500 versus step 1,000, it falls from 180 to 161 tokens,
truncation from 23.0% to 20.1%, and latency from 1.35s to 1.18s.

The 1,000-step F1 delta by context bucket is +0.0381 on 837 short pairs
(95% CI +0.0313 to +0.0452), +0.0145 on 146 medium pairs (−0.0010 to
+0.0325), and +0.0296 on 17 long pairs (−0.0206 to +0.1085). The short-case
gain is clear on this metric; the medium and long estimates remain uncertain.
This reference-overlap signal does not establish semantic or clinical quality.

At this snapshot, the direct Gemma v1 paired run has 19 base/SFT paired cases
completed across four shards, all successful. The blinded judge pass has 178
of 300 judgments complete, all successful, with about $0.137 estimated usage.
The full Nemotron outputs and evaluation prompt/response material remain
private; only aggregate metrics and file hashes are recorded here.

## 15:47 UTC diagnostic update

The complete 300-case Gemma-blinded Nemotron 500-step comparison has 294
schema-valid judgments. Base is preferred in 238, SFT in 20, and 36 are ties.
With ties split evenly, SFT's preference share is 12.9% (paired bootstrap
95% CI 9.7% to 16.3%). Mean SFT-minus-base score deltas are −0.97 relevance,
−1.29 grounding, −1.76 helpfulness, −1.11 empathy, and −0.59 safety on the
0-to-4 judge scale. Candidate order is randomized; base wins 123 times with
it in A and 115 times with it in B, so order does not explain the gap. Two
truncated and four format-invalid outputs are excluded; the parser accepts
fenced JSON and normalizes harmless key/label spacing. This remains one
unvalidated model judge, but the signal is large enough that lexical F1 gains
cannot be treated as a quality win.

A second blinded judge evaluation is running on the exact same 300 case IDs,
now comparing base with step 1,000 while preserving each pair's A/B placement.
This tests whether more training recovers the helpfulness/grounding loss. In
parallel, the Gemma direct-inference full paired run has 46 complete base/SFT
pairs with no recorded request errors. Nemotron step 1,500 is being evaluated
on the same 1,000 held-out cases; its first 11 SFT responses succeeded. Both
training jobs remain live, and the local mirrors now contain each model's
1,500-batch adapter.

## 15:49 UTC run status

The 300 Gemma-judge calls all returned successfully; estimated usage was
$0.239 total, while actual billing remains unavailable. The scoring parser
accepts the model's fenced JSON and whitespace variants; 294/300 were valid,
with six excluded for truncation or malformed fields. The paired output files
and aggregate record are private under the held-out evaluation directory.

Step-1,000 Nemotron judge comparison has 40/300 successful calls so far. The
Gemma v1 direct-endpoint comparison has 56 matched base/SFT cases, all
successful. Nemotron step-1,500 SFT inference has 197 successful responses
without recorded endpoint errors. Both original 4,858-step training jobs
continue running.

## Response-length diagnostic

On the same 1,000 paired Nemotron cases, the reference target has a median of
8 words (mean 44.8), while base responses have a median of 363 words, step-500
SFT 62.5, and step-1,000 SFT 36. This points to a plausible mechanism for the
metric conflict: SFT moves toward the short reference style and raises
lexical overlap, while the Gemma judge prefers the longer base answers for
helpfulness and grounding. The comparison does not establish that verbosity
is better; it shows that target-word overlap alone misses a substantive
quality tradeoff. The matched blinded judge comparison against step 1,000 is
underway to check whether the same pattern persists with more training.

## 2026-10-21 checkpoint and artifact audit

The two full-corpus SFT jobs finished successfully at 4,858/4,858 gradient
steps: Gemma completed at 2026-10-20 16:54:38 UTC and Nemotron at 16:37:30 UTC.
Paginating all 49 event pages confirms the final step for each; final reported
training losses are 1.589 (Gemma) and 1.572 (Nemotron). The latest locally
mirrored trained adapters are v8 at batch 4,500 for each model; no v9/final
adapter is present in the local mirror.

The remote W&B `sft-resume` artifact collections for both runs still exist but
contain zero versions. W&B Public API lookup returns no `v1` or `v8` membership,
and the previously working Gemma v1 inference URI now returns HTTP 400 because
that artifact version cannot be found. The four Gemma full-eval shards stopped
at 647 complete paired cases; their recorded adapter failures all say the v1
artifact version is missing. The 61.9 MB Gemma v1 adapter is preserved in the
private local mirror, as are later versions. Do not treat Gemma's incomplete
paired run as a model-quality result. Restoring inference requires publishing
the local adapter to W&B again or using a local serving path; re-upload was not
attempted because remote artifact storage is the capacity under investigation.

The complete 1,000-case Nemotron lexical comparison now covers steps 500,
1,000, 1,500, and 2,000. Step 1,000 is the best point among these checkpoints:
step 1,500 is −0.0043 reference unigram F1 versus step 1,000 (95% paired
bootstrap CI −0.0088 to +0.0003), and step 2,000 is −0.0026 (CI −0.0078 to
+0.0028). Steps 1,500 and 2,000 also have more output truncation (26.4% and
28.1% versus 20.1%), longer completions (193 and 198 versus 161 tokens), and
slower responses (1.46s and 1.45s versus 1.18s). Both still beat base on
lexical overlap. The complete metrics and result hashes are in private
`heldout_eval/paired-steps-2000.json`.

The refreshed same-case, same-position blinded Gemma judge evaluation for
step 1,000 has 291 valid judgments out of 300. Base wins 242, SFT wins 7, and
42 tie; SFT preference share with ties split is 9.6% (95% CI 7.0% to 12.4%).
SFT-minus-base score deltas are −1.12 relevance, −1.42 grounding, −1.85
helpfulness, −1.37 empathy, and −0.71 safety on the unvalidated 0-to-4 judge
scale. This is a strong warning signal from one model judge, not clinical
ground truth. Same-case blinded comparisons for steps 1,500 and 2,000 are now
running to test whether the later checkpoints recover any of that quality
signal; their prompts and results remain private.

## 2026-10-21 blinded checkpoint comparison complete

The 1,500- and 2,000-step blinded judge passes completed with no provider
errors. They reused the same 300 cases and preserved the same candidate A/B
positions as the 1,000-step pass. The Gemma judge produced 297 valid judgments
for step 1,500 and 299 for step 2,000. Base won 250, SFT won 10, and 37 tied
at step 1,500; the SFT preference share with ties split is 9.6% (95% CI 7.1%
to 12.3%). At step 2,000, base won 249, SFT won 13, and 37 tied; SFT share is
10.5% (95% CI 7.9% to 13.5%). Step 1,000 was similar: 242 base wins, 7 SFT
wins, and 42 ties among 291 valid judgments, for a 9.6% SFT share (95% CI
7.0% to 12.4%). Step 500 was the least bad SFT checkpoint on this judge, but
still only had a 12.9% share (20 SFT wins, 238 base wins, 36 ties).

At steps 1,500 and 2,000, every judged score dimension favored base. SFT-minus-
base means on the 0-to-4 rubric were −1.32 relevance, −1.61 grounding, −2.00
helpfulness, −1.60 empathy, and −0.87 safety at step 1,500; and −1.32, −1.61,
−1.97, −1.59, and −0.93 at step 2,000. The judge flagged serious safety
concerns 16 times for step 1,500 SFT versus 2 for base, and 14 versus 1 at
step 2,000. These are model-judge flags, not clinical findings, but they are
consistent with the quality regressions and do not support deploying any of
these SFT checkpoints. Reassess the training target/data and run expert safety
review before another training run.

The two new judge comparisons used an estimated $0.48 in W&B inference under
the configured hard caps; W&B-reported actual billing is unavailable. Private
aggregates, prompt maps, and hashes are stored in the corresponding
`nemotron35-blind-judge-step1500/` and `nemotron35-blind-judge-step2000/`
directories. Their blinded prompts contain generated clinical text and remain
private.

## 2026-10-21 prompt intervention results

To test an inference-time alternative while the trained adapters are missing
from W&B, two Nemotron base prompt policies were compared with the unmodified
base on the same 300 stratified conversations. The first policy enforced a
short, grounded answer and a concrete next step. Gemma's blinded judge preferred
it in 81 cases versus 157 for default, with 55 ties (prompt preference 37.0%,
95% CI 32.3% to 42.0%). Relevance and grounding were unchanged, but helpfulness
fell by 0.22 and empathy by 0.65 on the 0-to-4 rubric; safety rose by 0.27.
The first policy was preferred on only 26% of short-context cases and 47% of
medium-context cases. This is a measured tradeoff, not a good default policy.

The second policy kept the length and grounding constraints but required one
brief, specific empathic reflection before the next step. Across the same 300
cases, 298 judgments were valid: the judge preferred this prompt in 128 cases,
default in 113, and tied 57 times. Prompt preference was 52.5% (95% CI 47.3%
to 57.6%), so overall preference is near even. Its safety score was higher by
0.38 (95% CI 0.29 to 0.48), and serious-safety-concern flags fell from 16 for
default to one for the prompt. Empathy improved by 0.09 (95% CI −0.01 to 0.18)
and helpfulness by 0.10 (−0.03 to 0.24); those intervals do not establish a
clear gain on those dimensions.

The direct same-case comparison between prompt policies is stronger: across
292 judgments valid for both variants, the second prompt gained 16.4 percentage
points in preference (95% paired CI 11.5 to 21.7), with score improvements of
0.72 empathy (0.62 to 0.83), 0.36 helpfulness (0.23 to 0.48), and 0.11 safety
(0.04 to 0.19). This supports keeping the explicit empathic reflection in the
candidate prompt.

The second prompt then ran on the full 1,000-case holdout. All 1,000 default
and 1,000 prompted responses succeeded. Compared with default, reference
unigram F1 rose by 0.0109 (95% paired CI 0.0075 to 0.0144), mean output fell
from 356 to 150 tokens, truncation fell from 54.4% to 0.6%, and mean latency
fell from 2.05s to 0.99s. By context, F1 changed +0.0114 on short cases
(n=837; CI 0.0077 to 0.0149), +0.0047 on medium (n=146; CI −0.0023 to
0.0134), and +0.0443 on long (n=17; CI −0.0067 to 0.1198). The short cohort
has a clear lexical gain; medium and long estimates remain uncertain. Full
paired metrics and hashes are in private `nemotron35-prompt-ab-v2-fullscale/`.

Treat the second prompt as the best current experiment candidate, not as
clinically validated. Its overall blinded preference interval includes 50%,
and the judge is a single unvalidated Gemma model. The prompt inference and
judge calls together were estimated at about $0.52; actual W&B billing is not
available. For SFT evaluation, W&B documents trained model inference through
the Training API using a `wandb-artifact:///...:<step>` URI. The expected
`sft-resume` artifact membership is absent; a separate model-registry
checkpoint path is investigated below.

## 2026-10-21 short-context prompt experiment and data audit

The short-context prompt comparison ran the current policy and a revised
policy on the same 300 shortest held-out user contexts from the v2 extension.
Both Nemotron base runs completed 300/300 with no request errors. The current
policy averaged 90.65 completion tokens, 530 ms latency, and zero truncations;
the revised policy averaged 91.23 tokens, 532 ms, and one truncation. Paired
reference unigram F1 changed by only +0.0002 (95% bootstrap CI −0.0051 to
+0.0057), so lexical overlap is effectively unchanged. The revised policy
removes the forced 2–4 sentence format and makes a next step or question
conditional on usefulness. In 282 valid blinded Gemma 4 judgments, the revised
policy won 146, the current policy won 74, and 62 tied (62.8% preference with
ties split; 95% CI 57.8% to 67.7%). Judge score changes were +0.43 helpfulness
(95% CI +0.30 to +0.55), +0.37 relevance (+0.26 to +0.50), +0.35 grounding
(+0.22 to +0.48), −0.15 empathy (−0.25 to −0.06), and −0.03 safety
(−0.07 to +0.01). The revised prompt is a short-context improvement for
helpfulness/relevance with an empathy tradeoff, according to one unvalidated
judge; treat it as an evaluation candidate, not a universal default. The
private inputs, outputs, and metrics are in
`ai/training/output/wandb_v5_fullscale/heldout_eval/nemotron35-short-prompt-v3/`.

The 190,244-row v5 candidate was not silently reduced to 77,718 examples. Its
manifest records 96,701 retained rows (77,718 train, 9,673 validation, 9,310
test) and 93,543 held-out rows with reason codes. Exclusions are 63,559 exact
duplicate assistant targets above a 50-example cap, 28,380 placeholder
targets, 1,374 prompt echoes, 184 deleted placeholders, and 46 provider API
error targets. The duplicate-target rows are overwhelmingly from
`reddit_mental_nlp` (63,513); those rows have 52 distinct assistant target
strings, a one-word median target length, and 63,522 distinct user prompts.
One one-word target repeats 22,640 times. This is distinct user input with
nearly identical supervision, so dropping excess copies protects SFT from a
single generic response dominating gradients. Placeholder and API-error rows
lack valid assistant targets. These records remain in the original candidate
and are referenced in `heldout.jsonl`; they were not deleted. The manifest
does not justify treating them as usable SFT targets without repair or a
different objective.

Train and held-out source distributions differ: the test split contains 3,514
`reddit_mental_nlp` rows and 1,490 `reddit_mental_health_posts` rows, compared
with 300 and 0 respectively in train. Trajectories also average 5.64 assistant
turns per train row versus 3.03 in test. This matters when interpreting the
held-out score as source generalization rather than a same-distribution
estimate. No held-out rows were moved into training.

The earlier missing-artifact diagnosis was incomplete. Public artifact lookup
still finds no `*-sft-resume:v1` membership, but the W&B Training model API
lists checkpoint versions 0 and 1 for both registered models. The documented
model URI without the `-sft-resume` suffix resolves differently: Nemotron
`arc-sft-baseline-08ea5de19e58:step1` returned HTTP 200, while Gemma
`arc-sft-baseline-5c243e8ea483:step1` still returns backend HTTP 500. On five
neutral prompts, Nemotron `step1` produced distinct outputs and averaged 29
tokens; the base and `step0` each reached the 96-token cap. This confirms a
distinct serving checkpoint exists, but does not establish its quality or
whether it represents the final training step. The paired 700-case check is
running against `step1`. Public W&B artifacts
`arc-sft-baseline-08ea5de19e58:v1` (Nemotron) and
`arc-sft-baseline-5c243e8ea483:v1` (Gemma) were downloadable even though the
separate `*-sft-resume:v1` memberships were absent. Both adapters are now
mirrored locally under
`ai/training/output/wandb_v5_fullscale/model-registry/`, with size and SHA-256
manifests. Their weights differ from every locally mirrored intermediate
checkpoint. W&B metadata does not expose the gradient step for these registry
artifacts. The Nemotron `step1` paired run completed all 700 base/checkpoint
pairs with zero request errors. Under the same v2 response prompt, unigram F1
improved by 0.0108 (paired 95% CI +0.0063 to +0.0155); average completion
length fell from 144 to 90 tokens and latency from 867 to 842 ms. Truncation
increased from 1/700 to 12/700. Usage-based cost was estimated at $0.277;
actual billing was not queried. The blinded Gemma judge comparison completed on 300 sampled cases; 284 judgments
were valid (268 short, 14 medium, 2 long). It strongly preferred base: base won
223, step1 won 26, and 35 tied. Step1 preference share with ties split was
15.3% (paired bootstrap 95% CI 11.8–19.2%). Step1 scored lower on helpfulness
by 1.18 points (95% CI -1.30 to -1.06), empathy by 0.48, grounding by 0.50,
relevance by 0.41, and safety by 0.39 on the judge's rating scale; each interval
excluded zero. One serious safety concern was flagged on step1. There were 5
parse failures and 11 invalid schemas. These are diagnostic judgments from one
unvalidated Gemma judge, not clinical ground truth, but the direction is large
and consistent enough that step1 should not be promoted based on lexical F1
alone. Aggregate metrics, judge output, and private generations are in
`ai/training/output/wandb_v5_fullscale/heldout_eval/nemotron35-step1-recheck-700/`.

A separate Qwen job is still marked `RUNNING`, outside the approved
Gemma/Nemotron experiment set. Its checkpoint watcher is active, and the live
Training API schema exposes no job-cancel route. No unsupported cancellation
request was sent.

## Why the SFT checkpoints regress on response quality

The evidence now points to a target/objective mismatch, not a failed job. Both
runs completed one 4,858-step pass at learning rate `1e-5`; the service has no
quality-based checkpoint selection in this launcher. The released training,
validation, and test payloads contain no system messages (0/77,718 train rows,
0/9,673 validation rows, 0/9,310 test rows), while inference adds a behavioral
system prompt. Training therefore never directly optimized the instruction
used by the evaluator.

The data also shifts substantially across splits. Train assistant targets
have a 30-word median and 181-word mean; test targets have a 9-word median and
81-word mean. Train averages 5.64 assistant turns per row versus 3.03 in test.
The source mix differs too: train has 32,376 `empath`, 11,366
`mitch_hamidi_bpd_nlp`, 10,054 `mentalchat16k`, and 300 `reddit_mental_nlp`
rows; test has 3,514 `reddit_mental_nlp` and 1,490
`reddit_mental_health_posts` rows. This is a useful source-generalization
stress test, but it is a poor proxy for the training distribution and its short
reference answers are not a sound quality target by themselves.

That explains the misleading “improvement”: at step1, lexical F1 rose by
0.0108, but a blinded Gemma judge strongly preferred base and rated step1 lower
on all five dimensions. Earlier sampled Nemotron checkpoints show the same
quality direction. The launch recipe has no measured validation-quality gate,
so finishing more gradient steps was treated as progress even when the desired
behavior was not improving. The judge is also one unvalidated model; it is a
warning signal, not clinical ground truth.

Immediate containment: keep all v5 SFT checkpoints out of use. The v3
short-context prompt won 146 to 74 with 62 ties against the previous wording
on 282 valid Gemma judgments, but empathy fell by 0.15 points. A v4 prompt
preserving v3's flexible format while making the empathic reflection more
explicit was tested against v3 on the same 300 short cases. Of 281 valid
judgments, v4 won 105, v3 won 82, and 94 tied (54.1% preference with ties
split; 95% CI 49.3–58.9%). Empathy improved by 0.32 points (95% CI
+0.22 to +0.41); relevance +0.06 (+0.01 to +0.10), grounding +0.07
(0.00 to +0.15), helpfulness +0.06 (−0.04 to +0.17), and safety −0.03
(−0.07 to +0.01). This suggests a promising way to recover empathy without
losing v3's gains, but the preference interval includes 50%. The direct v4-versus-original comparison completed with 279 valid judgments:
v4 won 165, original won 60, and 54 tied (68.8% preference with ties split;
95% CI 64.2–73.5%). V4 scored +0.51 helpfulness (95% CI +0.38 to +0.63),
+0.38 grounding (+0.27 to +0.50), +0.33 relevance (+0.23 to +0.44), and
+0.18 empathy (+0.08 to +0.28). Safety changed by −0.02 (−0.06 to +0.02),
and neither arm received a serious-safety flag. There were 6 parse failures and
15 schema-invalid judgments. This remains a single unvalidated Gemma judge on
short-context cases, not clinical approval. The measured v4 policy is now the
shared response-generation default in `apps/web/src/lib/ai/services/response-generation.ts`,
with caller-provided instructions preserved after it. This inference-only
correction does not validate or repair the training data.

For the next training attempt, first make train and inference share the same
system instruction, split/weight examples to match the intended deployment
mixture, and hold out a source-balanced quality set scored on helpfulness,
grounding, empathy, and safety. Save and compare intermediate checkpoints on
that gate; stop when the gate regresses. Do not use unigram F1 as the promotion
metric, and do not train DPO from the current single-judge labels. The current
522-row G04 first-party synthetic view is not a shortcut: its manifest remains
provider-transfer blocked and it is not clinically reviewed. A lower learning
rate alone would not fix the missing instruction and target-quality gaps.
