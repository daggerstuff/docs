# W&B v38 prompt-disjoint 120-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v38 (19,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen 120-case synthetic prompt-disjoint
tool-use suite. Decoding was temperature 0, max 512 tokens, 2,048-token input
cap, and up to four local mock-tool rounds. All 240 calls succeeded with no
transport errors. Estimated usage was `$0.107427` against a `$1.3824` configured
maximum; actual billing is unknown.

| Aggregate | Base | W&B SFT v38 |
| --- | ---: | ---: |
| Nonempty responses | 102/120 | 1/120 |
| Local mock-tool rounds | 133 | 0 |
| `tool_status` checks passed | 72/75 | 0/75 |
| `response_contains` checks passed | 63/75 | 0/75 |
| `state_value` checks passed | 45/60 | 45/60 |
| `response_omits` checks passed | 12/15 | 15/15 |
| `memory_value` checks passed | 6/15 | 0/15 |
| All deterministic checks passed | 198/240 | 60/240 |
| Completion tokens | 50,390 | 1,622 |
| Latency p50 / p95 | 2,843 / 4,516 ms | 398 / 708 ms |

The v38 adapter produced empty or whitespace-only response fields in 119/120
cases and made no local tool rounds. Its 60/240 checks are the same as v34,
but output availability regressed from v34's 120/120 nonempty responses. The
base retained the expected tool behavior (133 rounds; 72/75 tool-status
checks). This is a strong failure signal for the trained checkpoint on this
suite; it does not support promotion. The cases are synthetic deterministic
diagnostics and are not validated measures of clinical quality or safety.

Response coverage by scenario (15 cases each):

| Scenario | Base nonempty | v38 nonempty |
| --- | ---: | ---: |
| Appointment consent gate | 14/15 | 0/15 |
| Appointment explicit consent | 15/15 | 0/15 |
| Approval gate | 6/15 | 0/15 |
| Memory consent gate | 11/15 | 0/15 |
| Memory opt-in | 13/15 | 0/15 |
| Resource comparison | 14/15 | 1/15 |
| Resource lookup | 15/15 | 0/15 |
| Untrusted note | 14/15 | 0/15 |

Reproduction details:

- Run ID: `wandb-v4-v38-prompt-disjoint-toolrounds4-heldout120-20261020T0613Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Config SHA-256: `9285257e8e5eddea791b09e58fb7b5c294f68a9cdeee1ed7fc140bc7a7041986`
- Checkpoint: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v38`
- Private result rows and full manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v38-prompt-disjoint-toolrounds4-heldout120/results/`.

This inference used W&B Serverless Inference. W&B's published Serverless
Training documentation still labels SFT **public preview**; training's
preview-specific no-charge statement does not apply to inference. The
estimated amount above is not a verified debit.
