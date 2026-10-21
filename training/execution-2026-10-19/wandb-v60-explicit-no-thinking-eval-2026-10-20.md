# W&B v60 explicit no-thinking checkpoint evaluation — 2026-10-20

## Result

The SFT-only evaluator completed all 120 prompt-disjoint synthetic cases with
120/120 successful requests and zero runner errors. V60 is the current
full-corpus checkpoint at 30,500 training batches. The request explicitly
sent `chat_template_kwargs: {"enable_thinking": false}`. It used the same
frozen 120-case suite, input/token limits, tool-round cap, and request settings
as the corrected v55/v56 paired comparisons. The case-suite SHA-256 is
`890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`;
config SHA-256 is
`5f7208d40b04a2db2849172ab1e65fff9a5bd006fab43d9fd7a4886b30866d72`;
private result JSONL SHA-256 is
`2129c77203e80c4eb27cebaeae12ebef12c7041c21e1a381cb57cf62345b1d3f`.

| Measure | Base reference | SFT v60 |
|---|---:|---:|
| Successful requests | 120/120 | 120/120 |
| Non-empty responses | 120/120 | 120/120 |
| Evaluator-local tool rounds | 131 | 0 |
| Tool-status checks passed | 71/75 | 0/75 |
| Expected-response checks passed | 75/75 | 12/75 |
| Synthetic state-value checks passed | 45/60 | 45/60 |
| Memory-value checks passed | 3/15 | 0/15 |
| Response-omission checks passed | 0/15 | 15/15 |
| Calls / finish-at-token-limit cases | 251 / 0 | 120 / 1 |
| Median / p95 latency | 1.09 / 2.14 s | 3.03 / 5.31 s |
| Prompt + completion tokens | 121,453 + 12,691 | 48,054 + 25,884 |

The base column is reused from the same-suite corrected v55/v56 paired runs;
its case hashes and explicit decoding settings match. Estimated v60 SFT
inference use was **$0.0443685**, under the **$0.67584** SFT-only preflight
maximum. Actual billing was not returned. Deterministic checks are unvalidated
synthetic diagnostics; they do not establish clinical quality, safety, or
production suitability.

## Interpretation

V60 again returned text on all cases, but made no tool calls and passed only
12/75 expected-response checks. V55 and v56 showed the same zero-tool behavior
under the same request settings. This makes a one-checkpoint anomaly less
likely and indicates a shared issue along the checkpoint/training/serving path.
The evaluation alone cannot isolate the cause. Pause further inference-only
checkpoint sweeps from this run until a controlled training/template change or
independent diagnostic can distinguish those causes. Continue mirroring
checkpoints and monitoring the live training job.

Private results and config are in
`ai/training/output/wandb_live_checkpoint_eval_20261020/v60-explicit-no-thinking-sft-only/`.
