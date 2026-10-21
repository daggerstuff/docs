# W&B v41 prompt-disjoint 120-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v41 (21,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen 120-case synthetic prompt-disjoint
tool-use suite used for v38/v39. Decoding, token caps, and four-round local
mock-tool configuration were unchanged. All 240 calls succeeded with no
transport errors. Estimated usage was `$0.10908275` against a `$1.3824`
configured maximum; actual billing is unknown.

| Aggregate | Base | W&B SFT v41 |
| --- | ---: | ---: |
| Nonempty responses | 101/120 | 117/120 |
| Local mock-tool rounds | 138 | 0 |
| `tool_status` checks passed | 74/75 | 0/75 |
| `response_contains` checks passed | 62/75 | 0/75 |
| `state_value` checks passed | 45/60 | 45/60 |
| `response_omits` checks passed | 13/15 | 15/15 |
| `memory_value` checks passed | 6/15 | 0/15 |
| All deterministic checks passed | 200/240 | 60/240 |
| Completion tokens | 50,829 | 1,951 |
| Latency p50 / p95 | 3,046 / 5,021 ms | 430 / 879 ms |

V41's visible-response rate recovered compared with v38/v39 (117/120 versus
1/120), so their output-collapse behavior did not persist at this checkpoint.
However, v41 made no tool rounds and passed none of the tool-status or
response-content checks. Its 60/240 aggregate checks are identical to v38/v39:
the state-value and response-omission checks pass, while tool execution,
task-specific response content, and memory behavior fail. The checkpoint is
not promotable for the agent-tool objective.

Response coverage by scenario (15 cases each):

| Scenario | Base nonempty | v41 nonempty |
| --- | ---: | ---: |
| Appointment consent gate | 15/15 | 15/15 |
| Appointment explicit consent | 15/15 | 15/15 |
| Approval gate | 5/15 | 14/15 |
| Memory consent gate | 10/15 | 13/15 |
| Memory opt-in | 14/15 | 15/15 |
| Resource comparison | 15/15 | 15/15 |
| Resource lookup | 13/15 | 15/15 |
| Untrusted note | 14/15 | 15/15 |

These are synthetic deterministic diagnostics, not validated measures of
clinical quality or safety.

Reproduction details:

- Run ID: `wandb-v4-v41-prompt-disjoint-toolrounds4-heldout120-20261020T0639Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `2e998341a21e0b2c73227ca71676c371384b654f04065c0b213cfd4fbce4230a`
- Checkpoint: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v41`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v41-prompt-disjoint-toolrounds4-heldout120/results/`

This used W&B Serverless Inference. The usage amount is an estimate, not a
verified debit. The Serverless Training preview's no-charge statement does not
apply to inference.
