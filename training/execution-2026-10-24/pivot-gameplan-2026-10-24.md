# Pivot Gameplan — Free-First Experiment Strategy (2026-10-24)

Status: Fireworks export is inconsistent, but its free comparison lane remains
valid. Default rule: stay on no-cost provided lanes. Do not recommend or launch
OVH/paid training unless the owner explicitly asks for a paid phase after free
lanes are exhausted. OVH is optional infrastructure, not the next default.

## 1. What we already own (exportable / portable)

Both W&B v6 selected-model final adapters are already mirrored and validated
locally:

| Model | Local artifact | Weights SHA-256 | Bytes | Rank | Tensors |
|---|---|---|---|---|---|
| Gemma 4 26B A4B | `…/wandb_local_checkpoints_v6_selected_20261021/gemma4/step-00000001-v1` | `c994dea8…31a6ba78` | 61,908,757 | 16 | 540 |
| Nemotron 3.5 Lightning | `…/wandb_local_checkpoints_v6_selected_20261021/nemotron35/step-00000001-v1` | `2bee1ab3…51295b319ce3` | 1,874,997 | 8 | 48 |

These were reproduced through the CPU validator with `--require-trained` and are
the portable comparison baseline for everything below.

## 2. Strategy (free-first order)

| Stage | Lane | Funding | Purpose |
|---|---|---|---|
| 1 | Fireworks (comparison-only) | Free through 11/30 | Fast, no-card SFT comparison; checkpoint-safe runs only; weights remain comparison-only until export works |
| 2 | W&B/CoreWeave Serverless | Training free during public preview; inference/credits tracked | Authorized Gemma/Nemotron comparison/experiment lane; adapters are downloadable and portable |
| 3 | Adaption (primary exportable lane) | Credit-funded; strongest portability | Exportable SFT/DPO through AutoScientist. This lane has already produced a downloadable Qwen adapter and is the cleanest path to a model we control |
| 4 | OVH true fine-tuning | Paid after explicit approval | Optional finishing phase only; do not recommend until free lanes are exhausted or another explicit owner request exists |

## 3. OVH “true fine-tuning” entry requirements

Before spending anything on OVH (paid, approval required):

1. Select the anchor base for which we have an **exact immutable revision, license, tokenizer, chat template, and training-context cap** across catalog (recommended next candidate: `Qwen/Qwen3.6-35B-A3B` where base availability permits, otherwise reuse the Gemma/Nemotron exact revisions).
2. Freeze input data identity:
   - `wandb-full-corpus-current-master-20261021-v6.json`,
   - train payload SHA-256 `1428a1fda03f15cc890e2b4ef44388b7877cf0cdf2b5ddd02149fea3a552f8b4`,
   - 78,681 train / 9,673 validation / 9,310 test, 93,543 holdouts held aside.
3. Prove resume from a checkpoint in one short smoke job (`--num_train_epochs` small, `save_steps` fixed, restore from `output_dir`).
4. Object-storage contract:
   - input bucket read-only,
   - output bucket read-write for checkpoints and final adapter,
   - save `weights (adapter + merged if supported)`, tokenizer/template, config, logs, and evaluation report.
5. Cost/regional quote recorded before any job creation; note documented H100 $3.39/GPU-hour and H200 4-GPU NVLink bundle $27.28/hour in GRA; confirm actual.
6. No download restriction issue (OVH is ours).

## 4. Recommended immediate local steps (no spend)

- [ ] Keep the Fireworks download background poll running; cancel only if it remains restricted.
- [ ] Add an OVH container definition under `scripts/training/` using the repo’s existing PEFT/TRL utilities and `validate_campaign_adapter` as the terminal check.
- [ ] Export adapter + base reference + validation JSON from the W&B lane into a portable bundle (already partially complete under `wandb_local_checkpoints_v6_selected_20261021`).
- [ ] Re-run `audit_v6_evaluation_readiness.py` on the chosen OVH bundle so train/dev/seal overlap remains zero.
- [ ] Record a bounded OVH smoke plan with explicit checkpoint interval and resume test.

## 5. Recommended next *experiment* choices

1. No new Fireworks run beyond the three completed unless downloads unblock.
2. One W&B data/recipe ablation on Gemma (only if a new covered hypothesis and credits exist).
3. One OVH smoke run (small, checkpointed, resumed) to qualify true fine-tuning; this is the highest-leverage paid action because it results in an exportable artifact under our control.
4. Keep Adaption credit quote as a gating artifact before any AutoScientist launch.

## 6. Current artifact anchors

- W&B final Gemma: `step-00000001-v1` (SHA `c994dea8...31a6ba78`, 61,908,757 B)
- W&B final Nemotron: `step-00000001-v1` (SHA `2bee1ab3...51295b319ce3`, 1,874,997 B)
- Frozen Fireworks outputs (comparison-only): 3 READY adapters, checksums recorded in their run reports.
- Evaluation readiness: `v6-evaluation-readiness.json`, fixed 120-case tool + 5-capability + 24-safety development suites.