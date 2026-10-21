# W&B v10 checkpoint held-out evaluation — 2026-10-20

## Result

V10 remains a negative agent-tool result. It generated more varied text than
v9, but made no tool calls and passed only 66/240 synthetic checks, compared
with 191/240 for the base model. Do not promote or deploy it for agent-tool
use.

| Measure | Base | W&B SFT v10 |
|---|---:|---:|
| Cases / calls | 120 / 120 | 120 / 120 |
| Deterministic synthetic checks passed | 191 / 240 | 66 / 240 |
| Nonempty responses | 94 / 120 | 120 / 120 |
| Distinct normalized nonempty responses | 88 | 73 |
| Fixture tool actions | 144 across 87 cases | 0 |
| `tool_status` checks passed | 69 / 75 | 0 / 75 |
| `response_contains` checks passed | 56 / 75 | 6 / 75 |
| `memory_value` checks passed | 6 / 15 | 0 / 15 |
| `state_value` checks passed | 45 / 60 | 45 / 60 |
| `response_omits` checks passed | 15 / 15 | 15 / 15 |
| Calls ending at output-length cap | 30 | 9 |
| Total provider-reported tokens | 175,424 | 54,755 |
| Estimated usage cost | $0.096937 | $0.02125975 |
| Median per-case latency | 4,467.362 ms | 576.854 ms |

Estimated usage summed to $0.11819675; actual billed amount was not available.
The preflight estimate was $1.3824 under a configured $1.50 hard cap. Token and
latency differences are descriptive and do not compensate for absent tool use
and weak task assertions.

## Method

This was a paired comparison of W&B checkpoint
`wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v10`
at 5,500 completed training batches against `Qwen/Qwen3.6-35B-A3B` through W&B
inference. It used temperature 0, a 512-token completion limit, 2,048 input
token cap, four tool rounds, and all 120 cases from the frozen held-out suite.
There were 240 successful calls and no call errors. Tool calls used local
synthetic fixtures; no external actions were performed.

The suite contains 15 cases each for resource lookup, resource comparison,
memory opt-in, memory consent gate, explicit appointment consent, appointment
consent gate, approval gate, and untrusted notes. Its checks are deterministic
synthetic assertions and have not been validated as clinical quality or safety
measures. They support an engineering comparison only.

The frozen cases SHA-256 is
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`; config
SHA-256 is
`93ebe31fed58076777aa8bd511b42cb9c1dda6fad540ded1f1431e40a0a8e919`. The
private config/results are under
`ai/training/output/wandb_live_checkpoint_eval_20261020/v10-heldout120/`. Its
manifest reports `complete`, 240 successes, and zero errors.
