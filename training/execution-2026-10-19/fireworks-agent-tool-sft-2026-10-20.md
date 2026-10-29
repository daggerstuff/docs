# Fireworks agent-tool SFT execution — 2026-10-20

## Current status

The Fireworks Serverless Training API accepted the Muse Glimmer LoRA SFT
session at 10:56 UTC. Run ID is `pixelated-agenttool-20261020-r8-1ep`; session
ID is `ts-29847e445cee48409993881866c9156c`. The local launcher is process
739132. It rendered 960 training rows into 960 supervised examples and 95,185
weighted target tokens. The maximum rendered training sequence was 913 tokens.
Training uses one epoch, batch size 16, learning rate `1e-5`, rank 8, alpha 32,
and the Muse Glimmer renderer with `ALL_ASSISTANT_MESSAGES` so tool-call
messages receive loss. The same release's 120-row validation split is fixed
outside the training rows.

The launcher first compares base and tuned final-answer behavior on validation,
then runs the shared paired mock-tool evaluator against both samplers before
closing the serverless session. It does not promote the checkpoint. Fireworks
documents the tuned sampler as session-scoped; this experiment therefore does
not produce a locally usable adapter or a persistent model.

The base validation completed 120/120 rows with 0/120 exact match and no
unterminated outputs. SFT is underway; the 10:59 UTC log reached step 15/60.
Recent loss moved from 0.6071 at step 1 to 0.2478 at step 15; this is a
training signal, not an evaluation result. The only stderr messages are the
nonfatal Muse Glimmer model-type warning and unavailable prefill-queue
telemetry notice. Follow live output in the private
`ai/training/output/fireworks_agent_tool_20261020/pixelated-agenttool-20261020-r8-1ep/launch.stdout`
and `launch.stderr` files. Sampling costs are billed separately from the
promotional training offer; current billed usage is not exposed by this local
runner.

## Paired tool evaluation and cost boundary

The test suite is the frozen prompt-disjoint synthetic suite with SHA-256
`890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`, 120
development-split cases across eight synthetic scenario families. It is not a
clinical or safety evaluation. The no-provider-call dry run succeeded with both
base and SFT arms, a 2,048-token input cap, at most two tool rounds, and at most
256 sampled tokens. Using published Muse Glimmer sampling rates of $1.96/M
input and $4.88/M output tokens, the conservative maximum is $3.7896192,
below the configured $4 hard cap. The separate built-in base/tuned validation
uses a 512-token output limit; actual inference billing remains to be checked.

The promotional training offer is currently active and lists training as $0
through November 30, 2026. This does not include inference. This is an
experiment-only Fireworks run because the output weights are not being
promoted or exported locally.

## Verification

- Offline launcher syntax check passed.
- Fireworks session-evaluator transport contract tests: 2 passed.
- Paired-evaluation dry run: valid; zero provider calls; all 120 frozen case
  IDs included; estimated maximum $3.7896192 under the $4 cap.
- Provider accepted the actual serverless session and returned the session and
  run IDs recorded above.

The paired evaluation and final validation scores will be appended after the
session completes.

## Paired evaluation follow-up — 2026-10-20 11:27 UTC

The first 120-case paired pass wrote all 240 arm/case records, but the run is
`incomplete`: 182 cases succeeded and 58 were rejected by the configured
context/round limits. The 58 errors were 22 base `ToolContextExceededPreflight`
errors (resource lookup 7, resource compare 15), 21 tuned context-cap errors
(resource lookup 6, appointment explicit consent 15), and 15 tuned
`ToolRoundLimitExceeded` errors (resource compare). Total estimated sampling
cost was $0.71031576 under the $4 hard cap; actual billing is not exposed.

Inspection found that this pass used a conservative ASCII-byte token counter
for runtime context rejection. The Muse Glimmer renderer's exact tokenizer
counts the 120 initial test prompts at 447–562 tokens, while the previous byte
counter reported up to 1,224. An exact-token follow-up is therefore running
against the same Fireworks base and tuned session snapshots. It uses an exact
renderer-backed counter, 1,000-token input cap, two tool rounds, 128 output
tokens, and a $2 hard cap (worst-case estimate $1.8609408). The first base
case completed successfully; its three successive prompt counts were 512,
617, and 725 tokens. The full rerun is ongoing at
`ai/training/output/fireworks_agent_tool_20261020/pixelated-agenttool-20261020-r8-1ep-exact-token-eval/`.

The initial fixed-validation result is base 0/120 exact matches versus tuned
120/120, with no unterminated generations. This result and the falling training
loss show the synthetic target is learnable; they do not establish tool-use
quality. The exact-token paired test must finish before interpreting the
tool-use comparison. All metrics remain synthetic, diagnostic, and
unvalidated.

## Exact-renderer rerun refresh — 2026-10-20 11:33 UTC

The corrected paired run remains active at the private output path documented
above. It has persisted only its first base-arm case (512, 617, and 725 prompt
tokens across three turns; estimated $0.005254). The next tuned-checkpoint
request has remained pending for over eight minutes; the process and HTTPS
connections are live and no provider error has returned. The run retains its
$2 hard cap. Treat the comparison as pending and keep the existing request in
flight; do not interpret the delay as a model failure or a completed result.

A read-only Fireworks checkpoint-list refresh at 11:34 UTC confirms the
`tuned` checkpoint still exists, is marked promotable, and its canonical API
resource name matches the endpoint configured for the pending direct-sampler
request. This confirms checkpoint identity, but not that a sample request has
completed or that the inference route is responsive.

### Inference timeout update — 2026-10-20 11:37 UTC

The live exact-token rerun has reached a concrete provider-side failure for
its first tuned-checkpoint sample: Fireworks SDK logged `ReadTimeout` after its
600-second HTTP timeout on attempt 1/7 and is retrying. The checkpoint-list
API confirms the target checkpoint still exists and is marked promotable; the
timeout therefore indicates a stalled/slow inference request, not a missing
checkpoint or failed SFT run. The bounded evaluator remains active with its
$2 cap. No comparison outcome has been produced yet.

### Route correction and successful paired sampling — 2026-10-20 11:38 UTC

The first exact-token attempt used the flattened checkpoint name returned by
the checkpoint-list API directly in the sampler route. It timed out on its
first tuned sample and was stopped after that 600-second SDK timeout. The
previously successful session evaluator had retained the SDK snapshot path
`linencloset/<run-id>/starter-tuned-48b75a39`; Firetitan expands that form under
the session checkpoint route. The corrected runner uses this same snapshot
form, and the first five persisted records now show successful samples from
both base and tuned arms (three base, two tuned). This supports the route
mismatch as the cause of the earlier timeout. The corrected 120-case run is
still active, with exact token counting and a $2 hard cap; final paired metrics
remain pending. The interrupted attempt and its partial result remain
separately preserved under the `...exact-token-eval/` directory.

A 4-round exact-token full-suite dry run is also prepared for the follow-up.
It includes the same 120 frozen cases, makes zero provider calls, and estimates
$3.101568 worst case under a $4 cap. The current 2-round run has persisted 43
records: 31 successes and 12 `ToolRoundLimitExceeded` errors, all in resource
compare cases on both arms. Complete that bounded run, then run the 4-round
suite so the resource-compare family has enough rounds to finish; this design
limit is distinct from endpoint errors.

At 11:49 UTC the corrected exact-token run had 62/240 persisted records: 33
successes and 29 errors. Twenty-five are `ToolRoundLimitExceeded` in the
resource-compare scenario under the configured two-round limit; four are
`SamplingRequestError` records across resource-compare and memory-opt-in, with
SDK output showing repeated HTTP 503 retries. Estimated use is $0.23351072;
actual billing remains unavailable. Fireworks' public status page reports
Serverless fully operational, but does not list Muse Glimmer or this
session-scoped checkpoint, so it does not resolve the observed per-request
503s. The runner remains live and bounded; the separate 4-round preflight is
$3.101568 under its $4 hard cap.
