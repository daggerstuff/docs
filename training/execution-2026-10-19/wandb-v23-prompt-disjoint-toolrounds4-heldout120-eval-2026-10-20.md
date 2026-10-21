# W&B v23 prompt-disjoint paired evaluation — 2026-10-20

Compared adapter v23 (12,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen 120-case prompt-disjoint synthetic
suite used for v17/v19-v22. The evaluator allowed up to four local mock-tool
rounds. All 240 calls succeeded without inference errors. Estimated usage was
`$0.10846125`, below the `$1.50` hard ceiling; actual billing is unverified.

V23 returned nonempty text in all 120 cases but made no tool rounds. It passed
0/75 tool-status checks, 0/75 response-content checks, 0/15 memory-value
checks, 45/60 state-value checks, and 15/15 response-omission checks. The base
made 137 local rounds across 87 cases, with 147 mock-tool calls. It passed
73/75 tool-status checks, 60/75 response-content checks, 5/15 memory-value
checks, 45/60 state-value checks, and 14/15 response-omission checks. The base
returned nonempty text in 99/120 cases. It hit the output-length finish reason
in 22 cases; v23 did not.

Median/p95 latency was 2,896/4,580 ms for base and 404/617 ms for v23.
Provider-reported token totals were 174,994 for base and 49,399 for v23.
The model's concise v23 responses and lower latency do not offset its complete
failure on tool-status and response-content checks. Do not promote this
checkpoint for agent-tool use. These synthetic deterministic checks do not
establish clinical quality or safety.

Reproduction:

- Run: `wandb-v4-v23-prompt-disjoint-toolrounds4-heldout120-20261020T0344Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `6f481e67607b0cb6e334799b11915bd5075bb8c2d764694af355b87512eb0779`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v23`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v23-prompt-disjoint-toolrounds4-heldout120/results/`
