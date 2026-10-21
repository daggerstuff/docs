# W&B v33 prompt-disjoint 120-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v33 (17,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on 120 frozen synthetic cases, paired by case, with
up to four local mock-tool rounds. All 240 inference calls succeeded with no
errors. Estimated usage was `$0.109211` against a `$1.3824` upper-bound cap;
actual billing is unverified.

| Aggregate | Base | W&B SFT v33 |
| --- | ---: | ---: |
| Nonempty responses | 102/120 | 99/120 |
| Local mock-tool rounds | 137 | 0 |
| `tool_status` checks passed | 73/75 | 0/75 |
| `response_contains` checks passed | 62/75 | 2/75 |
| `state_value` checks passed | 45/60 | 45/60 |
| `response_omits` checks passed | 14/15 | 15/15 |
| `memory_value` checks passed | 6/15 | 0/15 |
| All deterministic checks passed | 200/240 | 62/240 |
| Completion tokens | 51,632 | 1,337 |
| Latency p50 / p95 | 3,148 / 5,075 ms | 399 / 691 ms |

The trained adapter used fewer tokens and returned faster, but its zero tool
rounds and 0/75 tool-status checks show it did not learn the tested tool-use
behavior. Its lower response coverage and weak response-content checks also
mean the apparent latency/token reduction should not be read as a quality
improvement. These deterministic synthetic checks have not been clinically or
externally validated and do not support promotion. This result is consistent
with the frozen v4 payload audit, which found no tool-role messages or
assistant `tool_calls`; it does not prove general model quality or safety.

Reproduction:

- Run: `wandb-v4-v33-prompt-disjoint-toolrounds4-heldout120-20261020T0522Z`
- Test cases: `docs/training/agent-tool-sft-2026-10-19/evaluation/prompt-disjoint-heldout-test-cases.jsonl`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `6ee14f446e8909d6222421cb81c84c5927a69e94f91af35d14f8f3ac7eb4e7ed`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v33`
- Private results and complete manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v33-prompt-disjoint-toolrounds4-heldout120/results/`

The paired test artifact is complete (120/120 pairs; manifest has 240/240
successful calls). W&B Serverless Training/SFT remains documented as public
preview; evaluation used W&B inference for both arms.
