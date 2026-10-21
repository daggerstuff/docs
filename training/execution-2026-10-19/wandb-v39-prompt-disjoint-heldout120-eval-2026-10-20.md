# W&B v39 prompt-disjoint 120-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v39 (20,000 completed batches) with the same
Qwen/Qwen3.6-35B-A3B base and frozen 120-case synthetic prompt-disjoint
tool-use suite used for v38. Decoding, token caps, and four-round local
mock-tool configuration were unchanged. All 240 calls succeeded with no
transport errors. Estimated usage was `$0.10802925` against a `$1.3824`
configured maximum; actual billing is unknown.

| Aggregate | Base | W&B SFT v39 |
| --- | ---: | ---: |
| Nonempty responses | 102/120 | 1/120 |
| Local mock-tool rounds | 136 | 0 |
| `tool_status` checks passed | 73/75 | 0/75 |
| `response_contains` checks passed | 64/75 | 0/75 |
| `state_value` checks passed | 45/60 | 45/60 |
| `response_omits` checks passed | 12/15 | 15/15 |
| `memory_value` checks passed | 6/15 | 0/15 |
| All deterministic checks passed | 200/240 | 60/240 |
| Completion tokens | 50,614 | 1,525 |
| Latency p50 / p95 | 3,036 / 4,794 ms | 404 / 635 ms |

The adapter's only nonempty response was in the memory-consent-gate scenario;
the other 119 response fields were empty or whitespace-only, and the adapter
made no tool rounds. This reproduces v38's result (1/120 nonempty, zero tool
rounds, 60/240 checks) at the next 500-batch checkpoint. The base passed
200/240 checks and executed 136 tool rounds. The trained checkpoint remains
unfit for promotion on this diagnostic suite. The cases are synthetic and
their deterministic checks are not validated measures of clinical quality or
safety.

Reproduction details:

- Run ID: `wandb-v4-v39-prompt-disjoint-toolrounds4-heldout120-20261020T0620Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Evaluator config digest: `6347188a67d05ce96192662ce2277202746ceb09b4bfdbaa610573b5b954d8e7`
- Checkpoint: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v39`
- Private result rows and full manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v39-prompt-disjoint-toolrounds4-heldout120/results/`.

This used W&B Serverless Inference; estimates are not verified debits. W&B's
published Serverless Training docs still label SFT **public preview**; the
preview free-training statement does not apply to inference.
