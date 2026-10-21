# W&B v9 checkpoint held-out evaluation — 2026-10-20

## Result

The v9 checkpoint is a negative agent-tool result. On the fixed 120-case,
eight-scenario synthetic suite, v9 passed 60/240 deterministic checks versus
198/240 for the Qwen3.6-35B-A3B base. V9 made no tool calls and produced one
unique normalized answer across all 120 cases. Every v9 answer was nonempty,
but text presence alone does not demonstrate useful task behavior. Do not
promote or deploy this checkpoint based on these results.

| Measure | Base | W&B SFT v9 |
|---|---:|---:|
| Cases / calls | 120 / 120 | 120 / 120 |
| Deterministic synthetic checks passed | 198 / 240 | 60 / 240 |
| Nonempty responses | 99 / 120 | 120 / 120 |
| Distinct normalized nonempty responses | 93 | 1 |
| Fixture tool actions | 150 across 91 cases | 0 |
| `tool_status` checks passed | 71 / 75 | 0 / 75 |
| `response_contains` checks passed | 61 / 75 | 0 / 75 |
| `memory_value` checks passed | 6 / 15 | 0 / 15 |
| `state_value` checks passed | 45 / 60 | 45 / 60 |
| `response_omits` checks passed | 15 / 15 | 15 / 15 |
| Calls ending at output-length cap | 25 | 0 |
| Total provider-reported tokens | 177,840 | 50,544 |
| Estimated usage cost | $0.095673 | $0.015996 |
| Median per-case latency | 3,916.949 ms | 697.296 ms |

Estimated cost across both arms was $0.111669. Actual billed amount was not
available from the response usage records. The manifest's worst-case preflight
estimate was $1.3824 under the configured $1.50 cap. Latency and token use are
descriptive only; the much shorter SFT output is consistent with its repeated
answer collapse and absent tool use.

## Method

This was a paired comparison of W&B checkpoint
`wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v9`
at 5,000 completed training batches against `Qwen/Qwen3.6-35B-A3B` through W&B
inference. It used temperature 0, a 512-token completion limit, 2,048 input
token cap, four tool rounds, and all 120 cases from the frozen held-out suite.
There were 240 successful calls and no call errors. Tool calls used local
synthetic fixtures; no external actions were performed.

The suite contains 15 cases each for resource lookup, resource comparison,
memory opt-in, memory consent gate, explicit appointment consent, appointment
consent gate, approval gate, and untrusted notes. Its checks are deterministic
synthetic assertions and have not been validated as clinical quality or safety
measures. The counts support a comparative engineering diagnosis, not clinical
or production claims.

The frozen cases SHA-256 is
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`; config
SHA-256 is
`39deaf3200bfe71e81e5b8bb9538e7e631ef59acc812efcb91b60a8bf38516de`. The
private result rows and config are under
`ai/training/output/wandb_live_checkpoint_eval_20261019/v9-heldout120/` with
restricted file permissions. The machine manifest reports `complete`, 240
successes, and zero errors.
