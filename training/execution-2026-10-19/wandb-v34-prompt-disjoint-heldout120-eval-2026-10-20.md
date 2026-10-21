# W&B v34 prompt-disjoint 120-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v34 (17,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the same 120 frozen synthetic cases used for v33,
paired by case, with up to four local mock-tool rounds. All 240 inference calls
succeeded with no errors. Estimated usage was `$0.10859525` against a `$1.3824`
upper-bound cap; actual billing is unverified.

| Aggregate | Base | W&B SFT v34 |
| --- | ---: | ---: |
| Nonempty responses | 105/120 | 120/120 |
| Local mock-tool rounds | 138 | 0 |
| `tool_status` checks passed | 74/75 | 0/75 |
| `response_contains` checks passed | 63/75 | 0/75 |
| `state_value` checks passed | 45/60 | 45/60 |
| `response_omits` checks passed | 13/15 | 15/15 |
| `memory_value` checks passed | 6/15 | 0/15 |
| All deterministic checks passed | 201/240 | 60/240 |
| Completion tokens | 50,881 | 1,510 |
| Latency p50 / p95 | 3,012 / 4,809 ms | 392 / 632 ms |

V34 returns some nonempty output for every case, but its outputs are very
short on average (about 13 completion tokens per case) and it made no tool
rounds. It passed 0/75 tool-status checks and 0/75 response-content checks;
the base passed 74/75 and 63/75 respectively. Like v33, the adapter is faster
and uses fewer tokens while failing the tested tool-use behavior. V34's 60/240
total checks are slightly below v33's 62/240. The added response coverage does
not represent better task completion. These deterministic synthetic checks
remain unvalidated and do not support promotion.

Reproduction:

- Run: `wandb-v4-v34-prompt-disjoint-toolrounds4-heldout120-20261020T0532Z`
- Test cases: `docs/training/agent-tool-sft-2026-10-19/evaluation/prompt-disjoint-heldout-test-cases.jsonl`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `51baae35299ef779174dae6d392f961dcb45246d2b5b8cccd25bc6d7ff2b98b8`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v34`
- Local adapter SHA-256: `435ecd93cc99ad10123f61930977adbfc4e8ca70d79fa3bf5da39933fa999bd9`
- Private results and complete manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v34-prompt-disjoint-toolrounds4-heldout120/results/`

Both the v33 and v34 evaluations used W&B inference. W&B Serverless
Training/SFT remains documented as public preview.
