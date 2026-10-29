# W&B Gemma 4 26B LR ablation — 2026-10-25

Two free W&B Serverless SFT runs on the same 418-row arc-pilot-v1 training artifact, varying only learning rate.

## Data artifact
- `wandb-artifact:///wutang/pixelated-empathy-kan28/pixelated-arc-v1-wandb-20261025:v0` (first run)
- `wandb-artifact:///wutang/pixelated-empathy-kan28/pixelated-arc-v1-wandb-20261025b:v0` (second run)
- Source: `ai/training/output/arc_corpus/export/fireworks_pilot_v1/train.jsonl`, 418 rows
- W&B removes dataset artifact memberships after job consumption; each run needs a fresh upload (documented operational finding).

## Runs

| Run | Job ID | LR | Started | Ended | Status | Train loss | Tokens |
|---|---|---:|---|---|---|---:|---:|
| 5e-5 | `c92c7db0-a40a-4f65-9718-c28d6cc52c67` | `5e-5` | 16:43Z | 16:54Z | COMPLETED | 0.6994 | 120,107 |
| 1e-4 | `5f7880bb-90b4-4b46-a5bb-f0ec3657efbb` | `1e-4` | 17:16Z | 17:27Z | COMPLETED | **0.6400** | 120,107 |

Both used:
- base `google/gemma-4-26B-A4B-it`
- `assistant_turns: all`
- `batch_size: 16`
- `metric_logging.enabled: true`
- one provider-side gradient step (SFTTrainingConfig exposes only batch_size, learning_rate, assistant_turns, metric_logging; step count is provider default)

## Adapters

| LR | Local path | SHA-256 | Tensors | Nonzero LoRA-B | B L2 |
|---|---|---|---:|---:|---:|
| `5e-5` | `ai/training/output/wandb_ablation_gemma_26b_20261025/` | `ac0e99fe…4fe176` | 540 | 16,771,840 / 16,771,840 | 50.6685 |
| `1e-4` | `ai/training/output/wandb_ablation_gemma_26b_lr1e4_20261025/` | `8764dccb…4f2558` | 540 | 16,771,840 / 16,771,840 | 50.7433 |

Adapter relative L2 difference: `0.05686`; max absolute tensor difference `0.125`.

## Result

On this single-step, 418-row diagnostic, **LR `1e-4` achieved lower training loss (0.6400) than `5e-5` (0.6994)**. Both produced complete, non-zero LoRA-B updates and are valid exportable W&B artifacts. This is not an evaluation-quality result, not a clinical signal, and not a promotion candidate.

## Reproduction
- Create a fresh W&B dataset artifact from the local JSONL, with `trajectories.jsonl` and `metadata.json` (`total_len` = row count).
- POST `/v1/preview/sft-training-jobs` with `model_id`, `training_data_url`, and the four supported config keys.
- Poll `/v1/preview/training-jobs/{id}`; fetch `/v1/preview/models/{model_id}/checkpoints`; download the `lora` artifact at version `v1`.
- Verify with SHA-256, tensor count, and nonzero LoRA-B count.