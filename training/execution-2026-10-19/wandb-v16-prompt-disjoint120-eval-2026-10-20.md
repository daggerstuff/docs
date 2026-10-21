# W&B v16 prompt-disjoint paired evaluation — 2026-10-20

Compared checkpoint v16 (8,500 completed batches) with the Qwen/Qwen3.6-35B-A3B
base on the same 120-case paraphrased suite used for v13. The prompts have no
exact overlap with the dedicated tool-SFT training split. All 240 calls
succeeded without inference errors. Estimated usage cost was $0.106166 under
the $1.50 hard cap; actual billing is unknown.

The v16 adapter still issued no tool calls in any case and passed 0/75
tool-status checks. It passed 15/75 response-content checks, compared with
v13's 0/75 on this suite, but remains far below the base's 59/75 content and
73/75 tool-status checks. Both v13 and v16 passed 45/60 state-value checks and
0/15 memory-value checks. Response-omission checks were 15/15 for v16, 15/15
for v13, and 14/15 for the base. This is a limited surface-form-disjoint
synthetic diagnostic, not clinical quality or safety evidence. Do not promote
v16 for agent-tool use.

The base made tool calls in 87/120 cases across 136 rounds; the v16 adapter
made none. The base reached the 512-token output cap in 20 cases; v16 reached
it in none. Median/p95 latency was 4,164/6,766 ms for base and 597/1,120 ms for
v16. Provider-reported token totals were 172,583 and 49,489 respectively.

Reproduction:

- Run: `wandb-v4-v16-prompt-disjoint-heldout120-20261020T0203Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `2fedc123065382982e113216bb0e110edd248d5ff70ae93a0add8d557aedb36d`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v16`
- Local outputs and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v16-prompt-disjoint-heldout120/results/`
