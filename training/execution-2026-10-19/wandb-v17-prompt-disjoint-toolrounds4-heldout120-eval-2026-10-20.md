# W&B v17 prompt-disjoint paired evaluation — 2026-10-20

Compared W&B adapter checkpoint v17 (9,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the same 120-case paraphrased suite used for v13
and v16. The prompts have no exact overlap with the dedicated tool-SFT
training split. Both arms used the evaluator's four-round local mock-tool
execution, matching the v13/v16 setup. All 240 calls succeeded without
inference errors. Estimated usage cost was `$0.1078285` under the `$1.50` hard
cap; actual billing is unknown.

The v17 adapter issued no tool calls in any case and passed 0/75 tool-status
checks; the base passed 74/75. The base used 137 local tool rounds across 87
cases. On response-content checks, v17 passed 14/75 and the base 56/75. The
base passed 6/15 memory-value checks and v17 0/15. Both passed 45/60
state-value checks; v17 passed 15/15 response-omission checks versus 14/15 for
the base. The base reached the 512-token output cap in 23 cases; v17 reached it
in none. Median/p95 latency was 4,089/6,748 ms for base and 592/876 ms for
v17. Provider-reported token totals were 173,847 and 49,795 respectively.

This is a limited surface-form-disjoint synthetic diagnostic, not clinical
quality or safety evidence. The checkpoint is not suitable for the agent-tool
role based on this suite; do not promote it for that role. The lower output
length and latency do not offset the tool-use and content-check deficits.

Reproduction:

- Run: `wandb-v4-v17-prompt-disjoint-toolrounds4-heldout120-20261020T0225Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `35936bcee2a482c479c2f8b5a98b5f77835936a20e1b24a7c82812f6f579c757`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v17`
- Local outputs and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v17-prompt-disjoint-toolrounds4-heldout120/results/`
- A separate earlier run used zero tool rounds and is retained only as a no-tool-execution diagnostic; see `wandb-v17-no-tool-execution-prompt-disjoint120-eval-2026-10-20.md`.
