# W&B v21 prompt-disjoint paired evaluation — 2026-10-20

Compared the W&B adapter checkpoint v21 (11,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the same 120-case prompt-disjoint synthetic suite
used for v17/v19/v20. The suite executed up to four local mock-tool rounds per
case. All 240 calls succeeded without inference errors. Estimated usage was
`$0.1080695` under the `$1.50` hard cap; actual billing is unknown.

The v21 adapter made no tool rounds and passed 0/75 tool-status checks. The
base made 135 local tool rounds across 88 cases; its 146 mock-tool calls all
returned `ok`, and it passed 73/75 tool-status checks. V21 passed 12/75
response-content checks, up from 0/75 for v19 and v20, while the base passed
56/75 in this run. Both arms passed 45/60 state-value checks; memory-value
checks were 0/15 for v21 and 6/15 for base. V21 passed 15/15
response-omission checks; base passed 13/15. The base hit the 512-token output
cap in 22 cases, while v21 did not. Median/p95 latency was 4,048/7,395 ms for
base and 465/1,443 ms for v21. Provider-reported token totals were 173,608 and
49,342 respectively.

This is a limited surface-form-disjoint synthetic diagnostic, not clinical
quality or safety evidence. The 12/75 response-content result is a measurable
improvement over v19/v20, but v21 still emitted no tool rounds and failed all
tool-status and memory-value checks. Do not promote it for agent-tool use.

Reproduction:

- Run: `wandb-v4-v21-prompt-disjoint-toolrounds4-heldout120-20261020T0301Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `b24a9af98bc3495a4d64ebc802268657e5ffedcaa2bb64815137407e9b694626`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v21`
- Local outputs and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v21-prompt-disjoint-toolrounds4-heldout120/results/`
