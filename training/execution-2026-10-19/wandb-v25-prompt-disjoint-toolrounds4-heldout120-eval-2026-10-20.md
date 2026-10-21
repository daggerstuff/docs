# W&B v25 prompt-disjoint paired evaluation — 2026-10-20

Compared adapter v25 (13,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen 120-case prompt-disjoint synthetic
suite used for v17/v19-v24. The evaluator allowed up to four local mock-tool
rounds. All 240 calls succeeded without inference errors. Estimated usage was
`$0.11033225`, below the `$1.50` hard ceiling; actual billing is unverified.

V25 returned nonempty text in 109/120 cases and made no tool rounds. It passed
0/75 tool-status checks, 0/75 response-content checks, 0/15 memory-value
checks, 45/60 state-value checks, and 15/15 response-omission checks. The base
returned nonempty text in 104/120 cases, made 138 local rounds across 88
cases, and passed 73/75 tool-status, 61/75 response-content, 6/15
memory-value, 45/60 state-value, and 13/15 response-omission checks. The base
hit the output-length finish reason in 20 cases; v25 did not.

Median/p95 latency was 2,836/5,318 ms for base and 493/810 ms for v25.
Provider-reported token totals were 175,880 for base and 50,465 for v25. The
SFT checkpoint is faster and returned text more often in this suite, but it
still produced no tool calls and failed every positive tool-content and
memory-value check. Do not promote v25 for agent-tool use. These synthetic
checks do not establish clinical quality or safety.

Reproduction:

- Run: `wandb-v4-v25-prompt-disjoint-toolrounds4-heldout120-20261020T0409Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `d9de5b377058bc37b857df2b4a5aed5d45b2ea0488f5435bd9a49af3396f451d`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v25`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v25-prompt-disjoint-toolrounds4-heldout120/results/`
