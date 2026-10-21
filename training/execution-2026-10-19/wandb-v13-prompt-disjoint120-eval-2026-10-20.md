# W&B v13 prompt-disjoint paired evaluation — 2026-10-20

This is a second 120-case paired evaluation of the same v13 adapter (7,000
completed batches) and Qwen/Qwen3.6-35B-A3B base. It uses paraphrased user
requests with 120 unique prompt strings and zero exact user-prompt overlap
against the dedicated synthetic tool-SFT training split. The cases preserve
the original synthetic tool fixtures and deterministic state checks; only the
user requests and suite/split metadata changed. This tests surface-form
generalization, not unseen tasks or validated safety.

All 240 inference calls succeeded without errors. The base made tool calls in
85/120 cases (132 rounds) and passed 71/75 tool-status checks. The v13 adapter
made zero tool calls and passed 0/75 tool-status checks. Response-content
checks were 60/75 for base and 0/75 for v13; response-omission checks were
14/15 and 15/15. State-value checks were 45/60 for both arms, and memory-value
checks were 5/15 for base versus 0/15 for v13. Do not promote this adapter for
agent-tool use. The base remains imperfect and these deterministic checks do
not establish clinical quality or safety.

Base hit the 512-token output limit in 21 cases; v13 did so in none. Median/p95
latency was 4,098/6,662 ms for base and 513/789 ms for v13. Provider-reported
total tokens were 171,676 and 49,682 respectively. Estimated usage cost was
$0.1074965 under the $1.50 hard cap; actual billing is unknown.

Reproduction:

- Run: `wandb-v4-checkpoint-7000-vs-base-heldout120-20261020T0140Z`
- The manifest retains the earlier copied run label; use the unique case SHA
  and output directory below to distinguish this run from the original suite.
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `9ae6f4f4ca9a1b534e158e95560d96edfa3f21ca42091fd457f89cf4fbafd4be`
- Local cases: `docs/training/agent-tool-sft-2026-10-19/evaluation/prompt-disjoint-heldout-test-cases.jsonl`
- Local outputs and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/prompt-disjoint-v13-heldout120/results/`
- The preflight dry run validated all cases with zero provider calls and a
  $1.3824 maximum estimate.
