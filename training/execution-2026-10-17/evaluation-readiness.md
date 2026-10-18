# E00 evaluation readiness

Reviewed 2026-10-17. Status: **not ready for scored inference**. The audit
identified an uncleared historical evaluation bundle. The synthetic-only W&B
base access probe made 12 bounded requests: seven returned HTTP 400 and five
completed after the request contract was corrected. The sanitized error said
the stop-sequence array cannot be empty; the client now omits `stop` when the
configured list is empty. The successful responses returned usage and finish
metadata. Actual billed cost remains unknown because seven failed requests
returned no usage. No clinical case or source data was sent, and no weights
were downloaded.

## Decision

There is no currently qualified provider-neutral command that runs the same
cleared frozen cases through base and SFT models on Fireworks, W&B, and Adaption
while recording the evidence required by the campaign. A provider-neutral,
offline-tested runner now supports OpenAI-compatible chat endpoints and paired
case orchestration. Adaption has a separate local paired runner for its Qwen
checkpoint. Fireworks has neither local checkpoint access nor an available
hosted evaluation endpoint. W&B has no campaign base/SFT checkpoint pair ready
to evaluate. The historical 110-case Glimmer bundle is
marked `prepared_not_evaluated`; the current G03 audit found held-out overlap
with candidate training rows and unresolved control identities, so it is not
cleared for a new scored comparison.

The existing local preparation suite passes: 7 tests. Those tests establish
that the preparer pins inputs and rejects known leakage conditions. They do
not establish data independence, clinical validity, provider access, or model
quality. The existing TherapyBench heuristic measures empathy cues, safety
keywords, and expected-behavior token overlap. It is useful as a deterministic
smoke signal, but the campaign's prior judge audit found format bias and
disagreement with a blinded judge. It cannot be the promotion gate.

## Frozen bundle and present limitations

The local bundle is
`ai/training/output/arc_corpus/export/glimmer_eval_20261013/`. Its manifest
records 110 cases (58 held-out final turns and 52 controls), case SHA-256
`2bd856ac9ba92e169429c51560f283df57a4306f65530274fe22db9ee862fb1f`,
temperature 0, maximum 1024 output tokens, `<|eot|>` stop, and the requirement
to run identical case IDs in both arms. The Fireworks renderer is pinned in
`ai/qa/validation/therapy_bench/muse_glimmer_template.json`; it injects the
training-time system prompt/date. The manifest keeps `reference` and
`expected_behavior` out of model input.

G03's current report supersedes the bundle's older lineage claim for release
decisions: 87 candidate arc rows share groups with held-out cases, all 58
held-out prompts have high filtered five-token-gram containment against
candidate arc rows, and the 52 controls have no source identity metadata.
This is an exposure warning, not proof that every control is contaminated. Keep
this historical bundle local and diagnostic until lineage, reservations, and
independent control identities are resolved. Do not train on these cases or
call their future score held out.

The bundle is also not directly consumable by `run_adaption_eval.py`: it is
JSONL with rendered prompts and private scoring fields, while that CLI expects
a JSON array of `{id, category, prompt, expected_behavior}` and renders the
prompt through the checkpoint's tokenizer. Converting it would require a
reviewed provider-neutral case contract and cleared evaluation identities.

## Provider and runner support

| Lane | Paired base/SFT path found | Current blocker or gap | Next executable command after gates |
|---|---|---|---|
| Adaption | Local `run_adaption_eval` supports `base,adapter`; adapter path can be set to the existing run-2 checkpoint. Both modes use the same JSON golden-question input and Qwen tokenizer path. | Needs roughly 75 GiB base weights/cache and suitable GPU/RAM; this host has no GPU and insufficient free disk. Current runner reads the legacy 52-question golden set, uses the uncalibrated heuristic, and omits per-case latency, token counts, finish/error status, billed usage, and full config/input provenance. It is not the 110-case or three-provider harness. | From repo root, after a cleared suite, hardware and cost gate: `PYTHONPATH=.. uv run python -m ai.qa.validation.therapy_bench.run_adaption_eval --base Qwen/Qwen3.6-35B-A3B --adapter-path ai/training/output/arc_corpus/export/adaption_run2_v1/checkpoint_run2 --questions ai/research/experiments/evals/golden_questions.json --results-dir <new-private-results-dir> --modes base,adapter --load-strategy mm --load-4bit --max-new-tokens 1024 --judge heuristic`. This is an Adaption-only legacy benchmark command; its score is diagnostic, not a clinical verdict. Do not execute before gates. |
| Fireworks | No command found that can serve both the base and existing SFT checkpoint against local cases. | The existing managed Glimmer checkpoint's download endpoint previously returned HTTP 400/code 9 and the account has no evaluation deployment. Fireworks' in-session sampler applies to an active serverless job; it does not accept this promoted managed model ID. Hosted deployment would need separately qualified availability and covered cost. | None currently. Requalify the exact checkpoint's download or hosted evaluation route and cost first; then add a Fireworks adapter to the approved shared case contract. |
| W&B | The new paired runner supports OpenAI-compatible endpoints; P00 qualified `Qwen/Qwen3.6-35B-A3B`, endpoint, project, and pricing. | Seven initial requests returned HTTP 400. A captured diagnostic identified the empty `stop` array as a request rejection; the successful request also added documented project attribution. No SFT artifact exists. Billed cost for the seven failed requests is unknown. | The corrected command is documented below for synthetic-only access checks. No SFT pair is available; scored comparison still needs lineage, rubric, privacy, and SFT gates. |

For Adaption, the CLI fixes greedy decoding and the checkpoint chat template;
`--max-new-tokens 1024` matches the historical bundle's output cap. The
Fireworks template and Qwen tokenizer are different renderers. Cross-provider
comparisons therefore require a provider-neutral canonical conversation plus
documented provider rendering and an explicit tokenizer/template treatment;
they cannot claim identical tokenization. Within each provider, base and SFT
must share the exact renderer, system prompt, decoding, context handling, and
case order.

## Evidence required before a scored run

G03 must clear case lineage, reserve holdouts, and identify independent
controls. P00 must qualify the exact endpoints, model identities, privacy
settings, credit balance/expiry, and covered request/storage/judge costs.
Adaption additionally needs a suitable compute path; Fireworks needs a viable
checkpoint route; W&B needs an available campaign checkpoint pair. The suite
must then be frozen with hashes, a cleared development/test role, blinded and
balanced A/B order, and an anchored rubric calibrated against permitted human
ratings. Risk disagreements require human adjudication.

Each case record should retain arm, case ID, prompt hash, response, completion
status and finish reason, retries/errors, input/output tokens, latency, billed
usage, endpoint/model/checkpoint identity, renderer/tokenizer revision,
decoding/context limits, and run/config/source hashes. Persist each completed
case and reject resume when identities differ. Report endpoint failures and
truncations explicitly. Score safety, task success, format validity, and tool
behavior only where the frozen suite provides independent truth and reviewed
criteria; the current prompt-only 110 cases do not exercise actual tool calls.
Report cost and p50/p95 latency by arm. Use a blinded calibrated judge plus
human review for safety cases, then source-group uncertainty; do not infer
clinical fitness from an automated score.

The shared runner uses a strict canonical messages/tools JSONL contract, two
explicit arms (`base`, `sft`), greedy decoding, per-case hashes/latency/usage/
finish/error/retry fields, append-and-fsync persistence, and identity-checked
resume. Diagnostic plugins cover JSON keys, expected tool calls, and required
terms; each is explicitly labeled unvalidated. It never evaluates clinical
safety or promotion readiness. Synthetic smoke cases exercise formatting,
fictional fact use, tool selection, summary instructions, and short answers.
They contain no source or clinical data.

The runner is `ai/qa/validation/therapy_bench/paired_eval.py`. Its CLI provides
the no-inference dry-run help command:

```bash
uv run --no-project python -m ai.qa.validation.therapy_bench.paired_eval --help
```

The corrected base-only synthetic command used for the access smoke is:

```bash
uv run --env-file .env --no-project python -m ai.qa.validation.therapy_bench.paired_eval \
  --cases docs/training/execution-2026-10-17/diagnostic-smoke-cases.jsonl \
  --config docs/training/execution-2026-10-17/wandb-base-access-smoke.config.json \
  --results-dir docs/training/execution-2026-10-17/results/wandb-base-synthetic-smoke-corrected-20261017 \
  --arm base --max-cases 5 --max-input-tokens 512
```

P00 qualified `Qwen/Qwen3.6-35B-A3B`,
`https://api.inference.wandb.ai/v1/chat/completions`, project
`wutang/pixelated-empathy-kan28`, and current rates of $0.25/M input and
$1.25/M output. The first five requests returned HTTP 400; their response
bodies were not retained. A later one-case request with project attribution
still returned 400 because the runner sent `stop: []`. The error-body digest was
`db718db5d5c398a5cdd5a414a8738cba0e54611f4919949bb83bbb5cb5fc50e5`; a later
one-case response identified `Validation: Stop sequences array cannot be
empty`. Its top-level JSON keys were `code`, `message`, and `type`; the
sanitized message was retained, but that run's extractor did not retain the
top-level code value. [W&B's inference authentication guide](https://docs.wandb.ai/ko/models/support/inference_authentication_401_error)
shows the `OpenAI-Project` header and matching project argument. The
client now includes the qualified `OpenAI-Project` header and omits `stop` only
when its configured list is empty; a nonempty configured stop list is still
sent unchanged. HTTP 4xx responses now stop the run after the first failed
case and persist only bounded sanitized error details.

The corrected five-case run completed. Provider usage was 31/256, 32/256,
294/160, 49/256, and 24/163 prompt/completion tokens; all five finish reasons
were recorded. The estimated usage-based cost for successful responses was
$0.00147125. Three cases ended with `finish_reason=length` at the 256-token
cap. The unvalidated format, fact, and summary checks failed; tool selection
and short-answer checks passed. These are smoke diagnostics only and do not
measure quality or safety. p50 latency was 2.203 seconds and nearest-rank p95
was 3.124 seconds.

The run artifacts are under
`docs/training/execution-2026-10-17/results/`. Across 12 requests, the
configured worst-case estimate was $0.005376, below the $0.01 cap. The five
successful responses have usage-based estimated cost $0.00147125. Actual
provider billing remains unknown for all requests because the seven failed
requests returned no usage and billing for rejected requests was not verified.
No cost-zero claim is made. The probe establishes endpoint access only and
makes no model quality or clinical safety claim.

## Local verification

Commands run:

```bash
uv run --no-project --with pytest python -m pytest \
  ai/qa/validation/tests/test_prepare_glimmer_eval.py -q \
  --confcutdir=ai/qa/validation/tests
```

Results: `test_prepare_glimmer_eval.py` **7 passed** and the new
`test_paired_eval.py` **20 passed** and `test_prepare_glimmer_eval.py` **7
passed** after the multi-turn and split-isolation additions. Ruff passed for
the runner, focused tests, and synthetic fixture generator. The local dry-run
validated the five-case development suite and a bounded two-case support and
research cohort with zero provider calls.
The corrected five-case synthetic W&B base probe completed with five successes,
zero endpoint errors, token usage, finish reasons, and per-case latency.

## Next action

Use the corrected W&B request contract for future synthetic-only access
checks. The smoke is not a paired model-quality result. Scored comparison still
requires G03 lineage clearance, a selected SFT artifact, P00 cost/privacy
gates, and a calibrated human-reviewed rubric. The Adaption command above
remains a separate legacy route and is not cleared for the historical bundle.

## Synthetic capability v1 offline suite

E00 now includes versioned synthetic development and sealed case sets in
`scenario-dev-v1.jsonl` and `scenario-sealed-v1.jsonl`, with hashes and case
and group IDs in `scenario-suite-v1-manifest.json`. The first-party generator
is [generate_synthetic_capability_v1.py](../../../ai/qa/validation/therapy_bench/generate_synthetic_capability_v1.py);
the manifest pins its hash and each JSONL hash. Each split has five cases:
support request structuring, fictional-source research/citations, approval-gated
tool behavior, session-memory writing, and untrusted-document injection. All
state is synthetic and per-case in-memory; mock tools have no external effects.
The case and group IDs are disjoint across the files. Their scenario templates
are shared, so this is split bookkeeping, not evidence of semantic independence
or a statistically powered benchmark. Metric checks are labeled
`diagnostic_unvalidated` or `deterministic_synthetic_state_unvalidated_for_quality_or_safety`.
They do not measure clinical safety or quality.

The paired runner now supports bounded multi-turn calls to local mock tools,
records tool messages/results and partial evidence after failures, aggregates
usage and cost per completion, enforces a tool-round limit, and blocks sealed
cases unless `--allow-sealed` is supplied. It recomputes the input bound before
every completion using the accumulated assistant and tool messages; it stops
before another call if that tool-augmented context exceeds 1024. `--dry-run`
validates case/config hashes, split policy, conservative byte-based input
bounds, and worst-case cost without opening a provider connection or writing a
result directory. A 512 input bound is too small for cases carrying tool
schemas. The preregistered two-case cohort passes conservative preflight at
1024. The offline dry-run command and result were:

```bash
uv run --no-project python -m ai.qa.validation.therapy_bench.paired_eval \
  --cases docs/training/execution-2026-10-17/scenario-dev-v1.jsonl \
  --config docs/training/execution-2026-10-17/wandb-synthetic-capability-v1-budget-0.02.config.json \
  --results-dir /tmp/e00-dry-run-no-write --arm base --max-cases 2 \
  --max-input-tokens 1024 --max-tool-rounds 2 --dry-run
```

It validated the support and research development cases with no provider calls.
At the qualified W&B rates, the separately capped $0.02 cohort allows at most
six completions (two cases, up to two tool rounds) with 1024 input and 1024
output tokens per completion. The worst-case usage estimate is $0.009216; the
remaining cap is budget headroom. This plan is separate from the completed
synthetic access smoke, whose authorized hard cap was $0.01. The combined
planned campaign ceiling for those two scopes is $0.03; this is the sum of
configured scope caps, not a statement of billed amount. The earlier smoke's
actual billing remains unknown for its seven rejected requests. This inference cohort has since run using the user's process-only credential
authorization. Its full six-completion cap is consumed; actual billed cost is
unknown. Do not replay the former command or make further inference requests
under that authorization. A new capped inference scope is required, and any
scored comparison also requires data-release and evaluation gates.

The first run is archived at `results/wandb-synthetic-cap-v1-base-20261018T022350Z/`;
the research-only retry is at `results/wandb-research-base-2048-20261018T022456Z/`.
See the current handoff for the exact completion and usage breakdown.

This command is base-access and tool-contract diagnostic only; it is not a
paired base/SFT result. The earlier 256-token smoke truncated three of five
responses, so this plan uses a 1024 output cap instead of treating the prior
limit as adequate for task utility. It remains a small synthetic diagnostic,
not a calibrated model-selection suite. Sealed cases are not included.

The W&B chat-completions schema documents `reasoning_effort` values `low`,
`medium`, and `high`, plus `include_reasoning` (default true). The schema does
not establish that `include_reasoning=false` suppresses generation or reduces
billed output tokens, so this preregistered plan does not count on that flag.
Qwen documents `enable_thinking=False` through tokenizer chat-template
formatting; its vLLM guide shows
`chat_template_kwargs: {"enable_thinking": false}` for a self-hosted OpenAI-
compatible route. W&B's hosted support for that Qwen-specific template option
is not verified, and the Qwen docs do not establish support on this hosted
model variant. No unverified reasoning parameter is added to this run.
[W&B chat-completion request schema](https://docs.wandb.ai/api-reference/chat-completions/create-chat-completion-1),
[Qwen quickstart](https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html),
and [Qwen vLLM guide](https://qwen.readthedocs.io/en/stable/deployment/vllm.html).

Before model selection, expand unique groups and variants, review rubric
validity and independent task-state evidence, establish case-family separation
beyond distinct IDs, and preserve an untouched sealed set.
