# W&B v27 prompt-disjoint paired evaluation — 2026-10-20

Compared adapter v27 (14,000 completed batches) with the Qwen/Qwen3.6-35B-A3B
base on the frozen 120-case prompt-disjoint synthetic suite used for v17 and
v19-v26. The evaluator allowed up to four local mock-tool rounds. All 240
calls succeeded without inference errors. Estimated usage was `$0.109752`,
below the `$1.50` hard ceiling; actual billing is unverified.

V27 returned nonempty text in 120/120 cases and made no tool rounds. It passed
0/75 tool-status checks, 0/75 response-content checks, 0/15 memory-value
checks, 45/60 state-value checks, and 15/15 response-omission checks. The base
returned nonempty text in 98/120 cases, made 135 local rounds across 87 cases,
and passed 73/75 tool-status, 59/75 response-content, 7/15 memory-value,
45/60 state-value, and 14/15 response-omission checks. The base hit the
output-length finish reason in 25 cases; v27 did not.

Median/p95 latency was 3,245/5,267 ms for base and 437/827 ms for v27.
Provider-reported token totals were 174,820 for base and 49,620 for v27. V27
returned text more consistently and faster, but did not execute tools and
failed all positive tool-content and memory-value checks. Do not promote it for
agent-tool use. These synthetic checks do not establish clinical quality or
safety.

Reproduction:

- Run: `wandb-v4-v27-prompt-disjoint-toolrounds4-heldout120-20261020T0427Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `06b47b49a8a2cdebdc9ba6114062b98a15a3e315c14131215829caa1059707f4`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v27`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v27-prompt-disjoint-toolrounds4-heldout120/results/`
