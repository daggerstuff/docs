# W&B v29 prompt-disjoint paired evaluation — 2026-10-20

Compared adapter v29 (15,000 completed batches) with the Qwen/Qwen3.6-35B-A3B
base on the frozen 120-case prompt-disjoint synthetic suite used for v17 and
v19-v28. The evaluator allowed up to four local mock-tool rounds. All 240
calls succeeded without inference errors. Estimated usage was `$0.10873925`,
below the `$1.50` hard ceiling; actual billing is unverified.

V29 returned nonempty text in 120/120 cases and made no tool rounds. It passed
0/75 tool-status checks, 0/75 response-content checks, 0/15 memory-value
checks, 45/60 state-value checks, and 15/15 response-omission checks. The base
returned nonempty text in 101/120 cases, made 137 local rounds across 88 cases,
and passed 73/75 tool-status, 60/75 response-content, 5/15 memory-value,
45/60 state-value, and 12/15 response-omission checks. The base hit the
output-length finish reason in 22 cases; v29 did not.

Median/p95 latency was 3,660/5,695 ms for base and 467/841 ms for v29.
Provider-reported token totals were 175,055 for base and 49,530 for v29. V29
returned text more consistently and faster, but did not execute tools and
failed every positive tool-content and memory-value check. Do not promote it
for agent-tool use. These synthetic checks do not establish clinical quality
or safety.

Reproduction:

- Run: `wandb-v4-v29-prompt-disjoint-toolrounds4-heldout120-20261020T0446Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `4673bb0ab1134ce634a020978999007c3030f97e80fee481a31974f464602845`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v29`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v29-prompt-disjoint-toolrounds4-heldout120/results/`
