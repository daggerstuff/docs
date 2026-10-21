# W&B v26 prompt-disjoint paired evaluation — 2026-10-20

Compared adapter v26 (13,500 completed batches) with the Qwen/Qwen3.6-35B-A3B
base on the frozen 120-case prompt-disjoint synthetic suite used for v17 and
v19-v25. The evaluator allowed up to four local mock-tool rounds. All 240
calls succeeded without inference errors. Estimated usage was `$0.1089255`,
below the `$1.50` hard ceiling; actual billing is unverified.

V26 returned nonempty text in 120/120 cases and made no tool rounds. It passed
0/75 tool-status checks, 4/75 response-content checks, 0/15 memory-value
checks, 45/60 state-value checks, and 15/15 response-omission checks. The base
returned nonempty text in 97/120 cases, made 128 local rounds across 84 cases,
and passed 71/75 tool-status, 55/75 response-content, 6/15 memory-value,
45/60 state-value, and 14/15 response-omission checks. The base hit the
output-length finish reason in 27 cases; v26 did not.

Median/p95 latency was 3,137/5,583 ms for base and 434/783 ms for v26.
Provider-reported token totals were 170,798 for base and 49,648 for v26. V26
returned text more consistently and faster, but still did not execute tools
and passed only four positive tool-content checks. Do not promote it for
agent-tool use. These synthetic checks do not establish clinical quality or
safety.

Reproduction:

- Run: `wandb-v4-v26-prompt-disjoint-toolrounds4-heldout120-20261020T0422Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `99bb5900d3c06f69a3139d3acc1c724fa883a7c35f5f94bdf4c41b34c517c241`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v26`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v26-prompt-disjoint-toolrounds4-heldout120/results/`
