# W&B v20 prompt-disjoint paired evaluation — 2026-10-20

Compared W&B adapter checkpoint v20 (10,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the same 120-case paraphrased suite used for
v13/v16/v17/v19. The prompts have no exact overlap with the dedicated tool-SFT
training split. Both arms used four local mock-tool rounds. All 240 calls
succeeded without inference errors. Estimated usage cost was `$0.1061105`
under the `$1.50` hard cap; actual billing is unknown.

The v20 adapter made no tool rounds and passed 0/75 tool-status checks; the
base made 136 local tool rounds across 88 cases and passed 72/75. The base
passed 60/75 response-content checks and v20 passed 0/75. The base passed
6/15 memory-value checks and v20 0/15. Both passed 45/60 state-value checks;
v20 passed 15/15 response-omission checks versus 13/15 for the base. The base
hit the 512-token output cap in 18 cases; v20 did so in none. Median/p95
latency was 4,188/6,702 ms for base and 446/854 ms for v20. Provider-reported
token totals were 173,416 and 48,470 respectively.

This is a limited surface-form-disjoint synthetic diagnostic, not clinical
quality or safety evidence. V20 is not suitable for the agent-tool role on this
suite. It again scored 0/75 on response-content and tool-status checks,
matching v19 and trailing v17's 14/75 content result. Do not promote v20.

Reproduction:

- Run: `wandb-v4-v20-prompt-disjoint-toolrounds4-heldout120-20261020T0247Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `20814cd6ffa612d04e344879cbab071d143a4f204dbb03b8a28aa5faa51e72e8`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v20`
- Local outputs and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v20-prompt-disjoint-toolrounds4-heldout120/results/`
