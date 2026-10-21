# W&B v55 explicit no-thinking paired evaluation — 2026-10-20

## Result

The corrected evaluator completed all 120 prompt-disjoint synthetic cases
through both arms: 240/240 successful requests, zero runner errors, and 120
matching pairs with identical case hashes. V55 is the full-corpus checkpoint
at 28,000 training batches. The request explicitly sent
`chat_template_kwargs: {"enable_thinking": false}`. Base was
`Qwen/Qwen3.6-35B-A3B`; SFT was
`wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v55`.
Settings and suite hash match the corrected v56 comparison: temperature 0,
512 maximum output tokens, 3,072-token input cap, at most three tool rounds,
suite SHA-256 `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`.
Config SHA-256 is `3fb3b2a6031f6f505b2033f0a6b25b3815012d013396c090212375eea0431c99`;
private result JSONL SHA-256 is
`fe3072fdaa69ffbfa215a61a2bd8025a50d2dee243ed716b696f104a2ab320d8`.

| Measure | Base | SFT v55 |
|---|---:|---:|
| Successful requests | 120/120 | 120/120 |
| Non-empty responses | 120/120 | 120/120 |
| Evaluator-local tool rounds | 131 | 0 |
| Tool-status checks passed | 71/75 | 0/75 |
| Expected-response checks passed | 75/75 | 15/75 |
| Synthetic state-value checks passed | 45/60 | 45/60 |
| Memory-value checks passed | 3/15 | 0/15 |
| Response-omission checks passed | 0/15 | 15/15 |
| Calls / finish-at-token-limit cases | 251 / 0 | 120 / 10 |
| Median / p95 latency | 1.09 / 2.14 s | 1.12 / 5.18 s |
| Prompt + completion tokens | 121,453 + 12,691 | 48,054 + 16,628 |

Aggregate estimated inference use was **$0.0790255**, below the preflight
worst-case cap of **$1.35168**. Actual billed use was not returned. The
deterministic checks are unvalidated synthetic diagnostics; they do not
establish clinical quality, safety, or production suitability.

## Interpretation

V55 and v56 show the same core failure under explicit no-thinking: both return
non-empty text on all cases but make zero evaluator-local tool calls. V55
passes 15/75 expected-response checks and v56 passes 7/75; v55 reaches the
512-token cap in 10 cases versus 3 for v56. This reduces the likelihood that
the no-tool behavior is isolated to v56. It points instead to a shared issue
in this checkpoint family, training data/configuration, or serving/template
path. These results do not identify which cause is responsible. The paired
base behaved identically in both runs (131 tool rounds and 75/75 expected
response checks), supporting a checkpoint-path difference rather than an
evaluator or case-suite change.

Results and config are private in
`ai/training/output/wandb_live_checkpoint_eval_20261020/v55-explicit-no-thinking-paired/`.
