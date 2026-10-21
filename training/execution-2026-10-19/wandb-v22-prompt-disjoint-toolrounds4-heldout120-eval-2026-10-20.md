# W&B v22 prompt-disjoint paired evaluation — 2026-10-20

Compared the W&B adapter checkpoint v22 (11,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the same 120-case prompt-disjoint synthetic suite
used for v17/v19/v20/v21, with up to four local mock-tool rounds. All 240 calls
succeeded without inference errors. Estimated usage was `$0.10732775` under
the `$1.50` hard cap; actual billing is unknown.

V22 made no tool rounds and passed 0/75 tool-status and 0/75 response-content
checks. The base made 130 local tool rounds across 85 cases; its 141 mock-tool
calls all returned `ok`. It passed 71/75 tool-status checks and 52/75
response-content checks. Memory-value checks were 5/15 for base and 0/15 for
v22; both passed 45/60 state-value checks. Response-omission checks were
13/15 for base and 15/15 for v22. The base hit the 512-token output cap in 29
cases; v22 did not. Median/p95 latency was 4,093/6,366 ms for base and
465/1,027 ms for v22. Provider-reported token totals were 170,927 and 49,196
respectively.

This is a limited synthetic diagnostic, not clinical quality or safety
evidence. The v21 content improvement did not persist at v22; v22 again made
no tool rounds. Do not promote it for agent-tool use.

Reproduction:

- Run: `wandb-v4-v22-prompt-disjoint-toolrounds4-heldout120-20261020T0311Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `ebf421190009d54b563e052a90f758cfab1f227004a31aadb6282e86436c5ed0`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v22`
- Local outputs and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v22-prompt-disjoint-toolrounds4-heldout120/results/`
