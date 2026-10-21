# W&B v19 prompt-disjoint paired evaluation — 2026-10-20

Compared W&B adapter checkpoint v19 (10,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the same 120-case paraphrased suite used for v13,
v16, and v17. The prompts have no exact overlap with the dedicated tool-SFT
training split. Both arms used four local mock-tool rounds. All 240 calls
succeeded without inference errors. Estimated usage cost was `$0.10833075`
under the `$1.50` hard cap; actual billing is unknown.

The v19 adapter made no tool rounds and passed 0/75 tool-status checks; the
base made 136 local tool rounds across 88 cases and passed 73/75. The base
passed 59/75 response-content checks and v19 passed 0/75. The base passed
5/15 memory-value checks and v19 0/15. Both passed 45/60 state-value checks;
v19 passed 15/15 response-omission checks versus 11/15 for the base. The base
hit the 512-token output cap in 19 cases; v19 did so once. Median/p95 latency
was 4,044/6,905 ms for base and 540/1,535 ms for v19. Provider-reported token
totals were 173,354 and 50,285 respectively.

This is a limited surface-form-disjoint synthetic diagnostic, not clinical
quality or safety evidence. V19 is not suitable for the agent-tool role on this
suite. Its response-content result (0/75) is below v17's 14/75 under the same
protocol; increasing this adapter from 9,000 to 10,000 completed batches did
not improve the measured tool-SFT behavior. Do not promote this checkpoint.

Reproduction:

- Run: `wandb-v4-v19-prompt-disjoint-toolrounds4-heldout120-20261020T0237Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `65630e5d728183835b8fb43bcf10dd4e190c8cbe62a84a7be3fd4e56373cc41c`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v19`
- Local outputs and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v19-prompt-disjoint-toolrounds4-heldout120/results/`
