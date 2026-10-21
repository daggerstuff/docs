# W&B v30 prompt-disjoint paired evaluation — 2026-10-20

Compared adapter v30 (15,500 completed batches) with the Qwen/Qwen3.6-35B-A3B
base on the frozen 120-case prompt-disjoint synthetic suite used for v17 and
v19-v29. The evaluator allowed up to four local mock-tool rounds. All 240
calls succeeded without inference errors. Estimated usage was `$0.1063835`,
below the `$1.50` hard ceiling; actual billing is unverified.

V30 returned nonempty text in 120/120 cases and made no tool rounds. It passed
0/75 tool-status checks, 0/75 response-content checks, 0/15 memory-value
checks, 45/60 state-value checks, and 15/15 response-omission checks. The base
returned nonempty text in 103/120 cases, made 134 local rounds across 86 cases,
and passed 71/75 tool-status, 63/75 response-content, 7/15 memory-value,
45/60 state-value, and 13/15 response-omission checks. The base hit the
output-length finish reason in 19 cases; v30 did not.

Median/p95 latency was 3,017/5,111 ms for base and 388/656 ms for v30.
Provider-reported token totals were 172,228 for base and 49,174 for v30. V30
returned text more consistently and faster, but did not execute tools and
failed every positive tool-content and memory-value check. Do not promote it
for agent-tool use. These synthetic checks do not establish clinical quality
or safety.

Reproduction:

- Run: `wandb-v4-v30-prompt-disjoint-toolrounds4-heldout120-20261020T0455Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `e121206aad56b672d6079bf30144284f8f575b8d03cf06ea1a3bb36697a4caa7`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v30`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v30-prompt-disjoint-toolrounds4-heldout120/results/`
