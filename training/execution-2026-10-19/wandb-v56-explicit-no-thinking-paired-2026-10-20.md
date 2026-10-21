# W&B v56 explicit no-thinking paired evaluation — 2026-10-20

## Result

The corrected evaluator completed all 120 prompt-disjoint synthetic cases
through both arms: 240/240 successful requests, no provider/runner errors, and
120 matching case pairs with identical case hashes. This is the valid
no-thinking comparison for full-corpus checkpoint v56 (28,500 training
batches); the earlier v56 report used the provider's default reasoning mode
because the evaluator had omitted `chat_template_kwargs` from HTTP requests.

The corrected request explicitly sent
`chat_template_kwargs: {"enable_thinking": false}`. Base was
`Qwen/Qwen3.6-35B-A3B`; SFT was
`wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v56`.
Both arms used temperature 0, 512 maximum output tokens, a 3,072-token input
cap, and at most three tool rounds. The frozen suite SHA-256 is
`890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`; config
SHA-256 is `6c514d763d20c7c7e3825367ee1042942ef609e134822c0a3cbdf71d02bf7e31`.
The private result JSONL SHA-256 is
`a56526116d7728b602e737e5f083f8f4b94419f452e2a143fa2c79d0916666e9`.

| Measure | Base | SFT v56 |
|---|---:|---:|
| Successful requests | 120/120 | 120/120 |
| Non-empty responses | 120/120 | 120/120 |
| Evaluator-local tool rounds | 131 | 0 |
| Tool-status checks passed | 71/75 | 0/75 |
| Expected-response checks passed | 75/75 | 7/75 |
| Synthetic state-value checks passed | 45/60 | 45/60 |
| Memory-value checks passed | 3/15 | 0/15 |
| Response-omission checks passed | 0/15 | 15/15 |
| Calls / finish-at-token-limit cases | 251 / 0 | 120 / 3 |
| Median / p95 latency | 1.07 / 1.95 s | 1.23 / 3.51 s |
| Prompt + completion tokens | 121,453 + 12,687 | 48,054 + 15,923 |

The aggregate estimated inference use was **$0.07813925**; the preflight
worst-case cap was **$1.35168**. Actual billed use was not returned. Diagnostic
checks are deterministic against synthetic fixtures and marked
`diagnostic_unvalidated`; they do not establish clinical quality, safety, or
production suitability.

## Interpretation

The corrected setting resolves the earlier empty-response anomaly: v56 now
returns non-empty text on all cases. However, it still makes no evaluator-local
tool calls and passes only 7/75 expected-response checks, while the paired base
makes 131 tool rounds and passes 75/75 expected-response checks. This is
strong evidence that v56 is not suitable for the evaluated agent-tool behavior
under this setting. The comparison does not identify the cause (checkpoint,
training payload, chat template, or another serving difference); a corrected
same-config v55 replay is running to distinguish checkpoint behavior from a
shared serving/training issue.

The earlier [initial v56 paired report](wandb-v56-prompt-disjoint-paired-nonthinking-2026-10-20.md)
remains a record of what the default-mode endpoint returned, but its no-thinking
interpretation is superseded by this report. The evaluator request fix and
transmission test are in `ai/qa/validation/therapy_bench/paired_eval.py` and
`ai/qa/validation/tests/test_paired_eval.py`; the focused suite passed 24 tests.

Private request/response details remain in the mode-0700 directory
`ai/training/output/wandb_live_checkpoint_eval_20261020/v56-explicit-no-thinking-paired/`.
