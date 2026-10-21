# W&B v17 prompt-disjoint evaluation without tool execution — 2026-10-20

This paired diagnostic compared locally mirrored checkpoint v17 (9,000
completed batches) with Qwen/Qwen3.6-35B-A3B on the same 120-case
surface-form-disjoint synthetic suite used for v13/v16. The suite SHA-256 is
`890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`; the
v17 adapter files and train-state were hash-verified before evaluation.

All 240 calls succeeded. Estimated usage was `$0.06658075` under the
configured `$1.50` hard cap; actual billing is unknown. In this run,
`max_tool_rounds=0`, so the evaluator did not execute any tool round. The base
model emitted a model tool-call response in 88/120 cases, while v17 emitted
none. This is a raw tool-call-generation observation only; the tool-status
checks are not comparable to the earlier four-round evaluations. Base passed
8/75 response-content checks and v17 passed 15/75; both passed 45/60
state-value checks, 0/15 memory-value checks, and 15/15 response-omission
checks. The base reached its 512-token output cap in 12 cases; v17 did not.

A comparable four-tool-round v17 evaluation has been launched separately with
the same case suite, matching the v13/v16 settings. Do not use this no-tool
execution run as the v17 tool-status result or for promotion decisions.

Reproduction artifacts (private, mode 0600) are under
`ai/training/output/wandb_live_checkpoint_eval_20261020/v17-prompt-disjoint-heldout120/`.
The config SHA-256 is
`ec7cbac24174b1a28c5eba4fc43469872ab5127887806859b45b7947053911f8`.
