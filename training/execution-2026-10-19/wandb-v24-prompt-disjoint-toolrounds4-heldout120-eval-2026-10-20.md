# W&B v24 prompt-disjoint paired evaluation — 2026-10-20

Compared adapter v24 (12,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen 120-case prompt-disjoint synthetic
suite used for v17/v19-v23. The evaluator allowed up to four local mock-tool
rounds. All 240 calls succeeded without inference errors. Estimated usage was
`$0.10812325`, below the `$1.50` hard ceiling; actual billing is unverified.

V24 returned nonempty text in 55/120 cases and made no tool rounds. It passed
0/75 tool-status checks, 0/75 response-content checks, 0/15 memory-value
checks, 45/60 state-value checks, and 15/15 response-omission checks. The base
returned nonempty text in 101/120 cases, made 136 local rounds across 87
cases, and passed 72/75 tool-status, 61/75 response-content, 5/15
memory-value, 45/60 state-value, and 12/15 response-omission checks. The base
hit the output-length finish reason in 22 cases; v24 did not.

Median/p95 latency was 2,821/5,784 ms for base and 379/667 ms for v24.
Provider-reported token totals were 174,568 for base and 49,181 for v24. The
SFT checkpoint's faster, shorter responses do not compensate for its lack of
tool behavior or useful content in this suite. Do not promote v24 for
agent-tool use. The checks are synthetic diagnostics, not clinical quality or
safety evidence.

Reproduction:

- Run: `wandb-v4-v24-prompt-disjoint-toolrounds4-heldout120-20261020T0356Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `3b56db8ad3d30e0141aae4494ad522419d745bcf85a62ae93bd4fed0392ed63e`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v24`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v24-prompt-disjoint-toolrounds4-heldout120/results/`
