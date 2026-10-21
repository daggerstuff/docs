# Latest W&B full-corpus checkpoint comparison — 2026-10-19

At 19:32 UTC, the latest locally mirrored active adapters were evaluated
against the same W&B base endpoint on the identical eight-case synthetic
resource-comparison set (case hash
`0d60b1ebe9f40a18504854f27b9e06fcd8cbe90115f84b784ee987911e532ad2`). Both
paired evaluations completed with 16/16 successful calls and zero provider
errors. Estimated inference usage was $0.01145825 for v1 v123 and $0.0108315
for v2 v121, each below the configured $0.10 cap. W&B did not return billed
amounts, so these are usage estimates, not verified credit debits.

The trained arms show the same failure observed at earlier checkpoints. Each
returned the identical three-character response on all eight cases (one unique
normalized response, 24 completion tokens total), made zero tool calls, and
failed all 24 deterministic synthetic state assertions. The raw response is
kept only in the permission-restricted result files and is omitted here. The
base arm returned six distinct responses for v1's eight prompts and eight for
v2's; it also made no tool calls on this particular resource-comparison set.

This confirms a severe response-collapse / tool-use failure in both current
adapters on these eight synthetic cases, after approximately 62,000 and 61,000
training batches. It is not a clinical quality or safety evaluation: the
deterministic assertions are marked unvalidated, and this subset only tests
resource-comparison behavior. The same behavior across both runs suggests the
next diagnostic should inspect the exact training target formatting and
inference response extraction, alongside assistant-target frequency, before
spending more inference credits on a wider repeat.

Run IDs: `wandb-latest-v1-v123-vs-base-8case-20261019T1932Z` and
`wandb-latest-v2-v121-vs-base-8case-20261019T1932Z`. Per-case results, configs,
and manifests are stored beside this report with restrictive local file
permissions; they contain raw model output and must not be published.

## 20:03 UTC latest-checkpoint refresh

The same fixed eight synthetic cases were paired against the newest mirrored
adapters, v1 v125 and v2 v124. Both comparisons completed with 16/16 successful
calls and zero provider errors. Usage-based estimated costs were $0.01086275
for v1 and $0.010802 for v2; actual billed amounts were not returned.

The collapse persists at both newer checkpoints: every SFT case again returned
the same normalized three-character `BPD` response, with zero tool calls and
0/24 passing synthetic state assertions. The base arm returned eight distinct
normalized outputs and passed 22/24 assertions for v1 and 24/24 for v2. This
repeats the earlier failure on the same diagnostic set; it does not measure
clinical quality or establish that system-message removal caused the collapse.
The next decisive controlled run is the already qualified v4 system-preserving
ablation, which retains identical rows/splits and differs only by keeping
system messages at zero loss weight. It remains staged with upload disabled
until W&B storage/job capacity is available.

Per-case raw results and manifests are in private directories
`v1-v125-vs-base/` and `v2-v124-vs-base/` (directory mode 0700). They contain
model outputs and must not be published.

## 20:31 UTC held-out 120-case checkpoint comparison

The latest-checkpoint refresh tested v1 adapter v127 and v2 adapter v125 on
the same frozen 120-case set (SHA-256
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`), paired
against the W&B base endpoint `Qwen/Qwen3.6-35B-A3B`. The SFT and base arms
each received the same cases and shared a two-tool-round cap.

Both SFT arms completed 120/120 calls but each returned the same three-letter
classification label (`BPD`) on all 120 cases, made zero tool calls, and passed
60/240 deterministic synthetic state assertions. These aggregate findings
confirm that the response-collapse behavior persists at both tested heads.
The state assertions are explicitly unvalidated for quality and safety; this
is not a clinical evaluation.

The base arm completed 111/120 cases for v1 and 112/120 for v2. Its 9 and 8
incomplete cases respectively all hit the configured two-round tool limit;
these are evaluation-budget failures, not endpoint errors. On successful
cases, base produced 79 unique normalized responses for v1 and 81 for v2. It
made zero tool calls in successful cases on this suite. Estimated usage cost
was $0.09695275 for the v1 pair and $0.0984565 for the v2 pair ($0.19540925
combined); the provider did not report actual billed amounts.

Run IDs are `wandb-latest-v1-v127-vs-base-heldout120-20261019T2017Z` and
`wandb-latest-v2-v125-vs-base-heldout120-20261019T2030Z`. Full raw outputs are
restricted to mode-0700 directories under
`ai/training/output/wandb_latest_checkpoint_eval_20261019/`; do not publish
them. Manifests identify the exact checkpoint artifact URIs, model, and case
hash.

## 20:43 UTC newer-head paired comparison with four tool rounds

The same 120 held-out cases were run against newer heads v1 v129 and v2 v127,
with the base tool-round ceiling increased to four. All 240 calls succeeded in
each comparison; the previous two-round base failures are resolved. The base
arms produced 88 unique normalized responses and passed 196/240 synthetic
assertions for v1, and 83 unique responses with 186/240 assertions for v2.
The recorded tool-call count was zero for both base arms on this suite.

Response collapse remains at both newer SFT heads. v1 v129 returned one
identical normalized response of seven characters on all 120 cases; v2 v127
returned the same `BPD` classification label on all 120. Each SFT arm made
zero tool calls and passed 60/240 deterministic synthetic assertions. These
assertions are diagnostic and unvalidated for quality or safety.

Estimated usage was $0.1091435 for the v1 pair and $0.11133425 for the v2
pair ($0.22047775 combined). The configured $1.50 per-run hard caps were not
approached; actual billing was not returned. Run IDs:
`wandb-latest-v1-v129-vs-base-heldout120-20261019T2034Z-round4-cap150` and
`wandb-latest-v2-v127-vs-base-heldout120-20261019T2034Z-round4-cap150`.
Raw case results remain private in the corresponding mode-0700 output
directories.

## 21:03 UTC newest retained checkpoint comparison, 120 cases

The same frozen 120-case first-party synthetic held-out suite completed for
W&B checkpoint v1 v131 and v2 v129 against the Qwen3.6 base. Each comparison
recorded 240/240 successful calls with no provider errors. The deterministic
state checks passed 197/240 for v1 base, 194/240 for v2 base, and 60/240 for
each SFT arm. Base output diversity was 94 unique normalized responses for v1
and 88 for v2. Each SFT arm returned one identical normalized response for all
120 cases, with 480 total completion tokens (four per example) and no tool
calls. Base arms also made zero tool calls on this suite. The SFT collapse is
therefore still present at both newest retained checkpoints and is a clear
failure signal for this agent task, not a small quality regression.

Estimated usage was $0.109462 for v1 and $0.1091605 for v2, $0.2186225 combined;
actual billed usage was not reported. Both were configured with a $1.50
per-comparison hard cap, which was not approached. These deterministic state
checks and synthetic cases are not clinically validated and do not establish
safety or clinical quality. Exact run IDs, checkpoint URIs, configs, and case
hashes are in the mode-0600 manifests beside each results file; raw responses
remain in mode-0700 directories.

## 21:18 UTC v1 v133 and v2 v131 refresh

The same 120 synthetic held-out cases (SHA-256
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`) completed
for v1 v133 and v2 v131 against the Qwen3.6 base endpoint. All 240 calls in
each paired comparison succeeded. The base arms passed 196/240 synthetic
state assertions and produced 92 unique normalized responses for v1 and 90 for
v2. The SFT arms each passed 60/240 checks and made zero tool calls. v1 v133
produced four unique normalized short responses (366 completion tokens across
120 cases); v2 v131 returned one normalized response across all cases (480
completion tokens). The short, low-diversity outputs and zero tool calls show
that the agent-task failure persists; this is a synthetic diagnostic, not a
clinical quality or safety assessment.

Estimated inference usage was $0.10801475 for v1 and $0.1075765 for v2,
$0.21559125 combined; actual billed amounts were not returned. Both runs had a
configured $1.50 maximum-cost cap. Run IDs are
`wandb-latest-v1-v133-vs-base-heldout120-20261019T2109Z` and
`wandb-latest-v2-v131-vs-base-heldout120-20261019T2109Z`. Exact configs,
checkpoint URIs, and per-scenario checks are in the corresponding manifests;
raw outputs remain private.

## 21:21–21:37 UTC live-artifact refresh and newest-head comparisons

Two local launch attempts stopped before sending inference requests: the first
pointed at the adjacent eight-case resource subset, and the corrected suite
launch lacked `WANDB_API_KEY` in that process. Both recorded zero successful
calls and zero usage. The corrected runs sourced the existing local credential
environment and used the frozen 120-case test file (SHA-256
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`).

A direct read-only W&B collection refresh showed v1 adapter v134 (67,500
batches) and v2 v133 (67,000 batches) as the newest inference adapters around
21:21 UTC. Both 120-case comparisons completed with 240/240 successful calls.
Base passed 192/240 state checks on both runs and produced 88 unique normalized
responses for v1 and 87 for v2. SFT passed 60/240 checks on both, made zero tool
calls, and returned one repeated normalized response across all 120 cases.
Base traces recorded 139 and 144 successful simulator tool actions,
respectively. Estimated inference usage was $0.111035 (v1 v134) and
$0.11187375 (v2 v133), or $0.22290875 combined. Actual charges were not
returned; the configured maximum remains $1.3824 per comparison, under the
$1.50 cap.

A second direct artifact refresh at 21:30 UTC found newer inference adapters:
v1 v135 (68,000 batches) and v2 v134 (67,500 batches). Both comparisons again
completed with 240/240 successful calls. Base passed 189/240 and 195/240 state
checks, with 87 and 92 unique normalized responses. Both SFT arms again passed
60/240, returned one repeated normalized response across all cases, and made
zero tool calls. Base traces recorded 136 and 139 successful simulator tool
actions. Estimated usage was $0.109133 and $0.1088255 ($0.2179585 combined);
actual billing was unavailable.

While those comparisons ran, v1 v136 was published at 21:33:46 UTC. It is being
evaluated separately against the same frozen suite and base endpoint; its
result will be recorded under its exact artifact version. This confirms the
checkpoint inventory is moving during training. Resumable train-state artifacts
and inference adapter artifacts publish in separate collections, so their
version numbers and publication times must be tracked independently.

Run IDs for the completed pairs are `wandb-latest-v1-v134-vs-base-heldout120-20261019T2123Z`,
`wandb-latest-v2-v133-vs-base-heldout120-20261019T2123Z`,
`wandb-latest-v1-v135-vs-base-heldout120-20261019T2130Z`, and
`wandb-latest-v2-v134-vs-base-heldout120-20261019T2130Z`. Exact manifests,
configs, and restricted case-level outputs sit beside this report. These
deterministic checks are synthetic diagnostics, not clinical-quality or safety
evidence.

At the 21:37:30 UTC artifact refresh, v1 v136 was the newest inference adapter
(68,500 batches; published 21:33:46 UTC), while v2 v134 (67,500 batches)
remained newest. The paired 120-case comparison of v1 v136 completed with
240/240 successful calls. Its SFT arm again returned one repeated normalized
response, made zero tool calls, and passed 60/240 state checks; the base arm
passed 197/240, produced 87 unique normalized responses, and made 144
successful simulator tool actions. Estimated usage was $0.109961, with actual
billing unavailable and the $1.3824 preflight maximum below the $1.50 cap.
Run ID: `wandb-latest-v1-v136-vs-base-heldout120-20261019T2138Z`.

A direct artifact refresh at 21:44:42 UTC found v1 v137 (69,000 batches,
published 21:43:07 UTC) and v2 v135 (68,000 batches, published 21:38:33 UTC).
Both completed paired comparisons on the same frozen suite; aggregate results
appear in the next section. This was one next 500-batch milestone sample after
the response-collapse result repeated on v1 v136. Version and publication
cutoffs are explicit because training continues to publish new adapters while
inference evaluations run.

## 21:45–21:53 UTC next 500-batch milestone

The newest pair at the 21:44:42 UTC artifact cutoff—v1 v137 (69,000 batches)
and v2 v135 (68,000 batches)—completed 240/240 calls per comparison on the
same frozen 120-case suite. The SFT arms again each returned one repeated
normalized response, made zero tool calls, and passed 60/240 state checks.
Base passed 189/240 for v1 and 190/240 for v2, with 80 and 87 unique
normalized responses. Estimated usage was $0.1115415 and $0.109696
($0.2212375 combined); actual billing was unavailable and each $1.3824
preflight maximum remained below the $1.50 cap.

At 21:53:43 UTC, a direct read-only inventory found v1 v138 (69,500 batches,
published 21:52:24 UTC) and v2 v136 (68,500 batches, published 21:47:45 UTC).
These were published while v1 v137/v2 v135 were being evaluated. Since the
same SFT failure has now repeated through several consecutive adapter heads,
the next work shifts to the prepared training/data diagnostics rather than
spending inference credits to test every new 500-batch snapshot. This is an
inventory cutoff, not a claim that these moving artifacts were tested. See the
[21:53 live artifact and storage snapshot](../wandb-live-storage-adapter-refresh-20261019T2153Z.json).

Run IDs: `wandb-latest-v1-v137-vs-base-heldout120-20261019T2145Z` and
`wandb-latest-v2-v135-vs-base-heldout120-20261019T2145Z`. Their manifests and
restricted per-case results are beside the earlier runs. All findings remain
synthetic diagnostics, not clinical-quality or safety evidence.

## 21:57–21:58 UTC live artifact refresh and target overlap

A fresh authenticated query of W&B's actual artifact collections at 21:57 UTC
found v1 adapter/train-state v138 at 69,500 batches (published 21:52:24/26 UTC)
and v2 adapter/train-state v137 at 69,000 batches (published 21:57:00/02 UTC).
The direct Training API still reports the v1/v2 jobs `RUNNING` with null
progress and old status-update timestamps; the v4 job remains `PENDING`. Its
`/checkpoints` API returned only the step-0 model entry, so that endpoint is not
the authoritative trained-adapter inventory. The versioned W&B `lora` and
`train-state` artifact collections are the authoritative sources for those
streams. No artifacts were modified or deleted.

The target-overlap diagnostic was rerun over all seven completed 120-case SFT
results recorded above. All 840 successful SFT outputs have the same exact
SHA-256 (`74fd2e753c4e2cd9afcadf0a6667fc47ef068c8a782d50e2f3c3907fc666d4c8`); that exact target occurs 12,771
times in v1's 532,557 assistant targets (2.3981%) and 12,771 times in v2's
532,603 targets (2.3978%). This is a strong target-attractor correlation, not
causal proof. The result makes target weighting/format and loss configuration
the next diagnosis target, rather than testing every adjacent checkpoint.
By exact-string frequency, this target is third-most-common among assistant
targets; the two most common are 4.26% and 3.30%. These proportions alone do
not explain why the model converged to this target.
Hash-only counts and method are in the [target-overlap record](../wandb-response-target-attractor-20261019T2158Z.json); no raw text is included.

The next milestone check tested v2 v137 against the base on the same fixed 120
cases. All 240 calls succeeded. The SFT arm again produced one normalized
response across all cases, made zero tool calls, and passed 60/240 synthetic
state assertions. The base produced 84 unique normalized responses, made 148
successful simulator tool actions, and passed 193/240 assertions. Estimated
usage was $0.111901 against the $1.3824 preflight maximum; W&B did not report
actual billed usage. This confirms the collapse at a checkpoint 1,000 batches
after the previously tested v2 v135; it still does not establish clinical
quality or safety. Run ID: `wandb-latest-v2-v137-vs-base-heldout120-20261019T2200Z`.
See its [config](v2-v137-heldout120.config.json), [manifest](v2-v137-heldout120-auth/manifest.json),
and restricted case-level results. v1 v138 remains untested.

The current v1 v139 comparison started at 22:10 UTC using the identical case
file and decoding/tool limits. It completed at 22:20 UTC with all 240 calls
successful. The SFT arm produced one unique whitespace/case-normalized response
over 120 cases, made zero tool actions, and passed 60/240 deterministic
synthetic assertions. The base produced 88 unique normalized responses, made
148 tool actions, and passed 193/240 assertions. Estimated usage was $0.110632
total; actual billed usage was not returned. This confirms the same response
collapse and tool-use failure at v1 v139, 1,000 batches after v1 v137. The
assertions remain unvalidated synthetic diagnostics, not clinical quality or
safety measures. Per-case outputs are restricted to the private results
directory.

The same paired comparison against v2 v139 began at 22:19 UTC. Its first
status check had 7/120 successful calls per arm and zero errors. The case set,
decoding, tool limits, and $1.3824 preflight maximum are unchanged.

A fresh artifact inventory at 22:13 UTC found v1 adapter v140 / 70,500 batches
and v2 adapter v138 / 69,500. v1 v140 and v2 v138 are locally mirrored and
SHA-256 verified; they have not been evaluated. The v1 v139 comparison is
therefore a recent-head check, not the newest v1 head.

The rolling backup manifest advanced at 22:18 UTC: v1 adapter/state v140 at
70,500 batches and v2 adapter/state v139 at 70,000 batches, all locally
mirrored with size/hash checks. A later refresh at 22:24 UTC recorded v1
adapter/state v141 at 71,000 batches and v2 v139 at 70,000. The v2 v139
comparison is testing the current v2 head; v1 v141 is queued as the next
comparison after this run.

At 22:27 UTC, v2 v139 completed with 240/240 successful calls. The SFT arm
again produced one unique normalized response, made zero tool actions, and
passed 60/240 synthetic assertions. The base produced 91 unique responses,
made 144 tool actions, and passed 191/240. Estimated usage was $0.1100935;
actual billed usage was unavailable. This is the same collapse at the latest
v2 checkpoint (70,000 batches). The next paired run, v1 v141 against base,
began at 22:27 UTC on the unchanged suite; its configured preflight maximum
is $1.3824.

At 22:30 UTC, the paired v1 v141 run had 38/120 successful calls per arm and
the v2 v140 run had 2/120 per arm; neither had errors. Both use the same
predeclared held-out cases and decoding. v1 v141 and v2 v140 are the newest
locally mirrored checkpoints as of the 22:29 rolling-backup refresh.


### 2026-10-19 22:35 UTC — v1 v141 paired evaluation complete

Run `wandb-latest-v1-v141-vs-base-heldout120-20261019T2224Z` completed with 240/240 successful calls on the fixed 120-case suite. The v1 v141 SFT arm produced one unique normalized response, made zero tool actions, and passed 60/240 deterministic synthetic assertions. The base arm produced 96 unique normalized responses, made 149 tool actions (143 successful), and passed 201/240 assertions. Estimated usage was $0.11017575; actual billed usage is unavailable. This is the same response-collapse/tool-use failure at the latest v1 checkpoint (71,000 batches), so it remains a negative behavioral result, not evidence of quality or safety. Results and case-level outputs remain private in the run directory.

At 22:35 UTC, the paired v2 v140 run had 80/120 completed calls in the SFT arm and 81/120 in base, all successful; it remains active. The rolling backup has advanced to v1 v142 / 71,500 batches and v2 v141 / 71,000 batches; these are not yet evaluated.


### 2026-10-19 22:40 UTC — v2 v140 paired evaluation complete

Run `wandb-latest-v2-v140-vs-base-heldout120-20261019T2229Z` completed with 240/240 successful calls on the fixed suite. The v2 v140 SFT arm produced one unique normalized response, made zero tool actions, and passed 60/240 deterministic synthetic assertions. Base produced 87 unique normalized responses, made 141 tool actions (138 successful), and passed 185/240 assertions. Estimated usage was $0.10955575; actual billed usage is unavailable. The SFT output hash is identical to the one-response output from v1 v141 and matches a frequent 10-character training label; detailed hash-only source attribution is recorded in the [private collapse attribution report](../current-sft-collapse-attribution-2026-10-19.json).

The SFT jobs' v4 baseline data removes system messages. A local same-data/same-split preserve-system variant now passes row-by-row checks on all 171,261/9,673/9,310 train/validation/test examples: all non-system message projections match and every retained system message has zero loss weight. It remains local-only pending storage/job capacity; W&B job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` is bound to the ordinary system-stripped v4 payload, not the preserve-system variant.

### 2026-10-19 22:50 UTC — v1 v142 and v2 v141 paired evaluations

Both newest local W&B adapters were compared with the Qwen3.6 base on the same frozen 120-case suite. Each run completed 240/240 calls with no request failures. v1 v142 returned one unique normalized SFT response, made zero tool calls, and passed 60/240 deterministic synthetic assertions; base returned 19 unique responses, made tool calls in 84 cases, and passed 71/240. v2 v141 also returned one unique normalized SFT response, made zero tool calls, and passed 60/240; base returned 12 unique responses, made tool calls in 90 cases, and passed 65/240. The SFT outputs match the earlier collapsed label response. These synthetic assertions have not been validated for clinical quality or safety. Estimated inference was $0.06809825 for v1 and $0.06911325 for v2, each below its $0.2976 preflight maximum; actual billing remains unavailable. Run IDs are `wandb-latest-v1-v142-vs-base-heldout120-20261019T2245Z` and `wandb-latest-v2-v141-vs-base-heldout120-20261019T2245Z`. Run configs, manifests, and case-level results are in the private `v1-v142-heldout120-auth/` and `v2-v141-heldout120-auth/` directories.
