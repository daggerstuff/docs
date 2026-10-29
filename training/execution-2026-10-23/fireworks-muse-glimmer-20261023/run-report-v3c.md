# Fireworks Muse Glimmer v3c — Rank-8 Ablation (2026-10-24)

- Job ID: `accounts/linencloset/supervisedFineTuningJobs/pixelated-glimmer-v3c-20261024040404-r1`
- State: `JOB_STATE_COMPLETED` (2026-10-24T15:57Z; launch 04:04Z)
- Base model: `accounts/fireworks/models/muse-glimmer-30b`
- Train dataset: `accounts/linencloset/datasets/arc-pilot-v1-train` (418 rows)
- Eval dataset: `accounts/linencloset/datasets/arc-pilot-v1-eval` (80 rows)
- Output model: `accounts/linencloset/models/arc-pilot-v3c-glimmer-rank8` (`READY`)
- Treatment: LoRA rank `8` (vs F1 rank `16`); LR `1e-4` and all other settings identical to F1 (2 epochs, LR warmup 0, max context 32,768, `eval_auto_carveout=false`, checkpoint interval 1000)
- Training telemetry: 28 optimizer steps, eval loss `0.6492 → 0.4295`, ppl `1.914 → 1.536`, step-28 train loss `0.3979`
- Promo/rated cost: `$0.00`, attribution `COMPLETE`, 0 rows (verified post-run)
- Download status: still restricted. `firectl model download` (now signed in as `ccoburn6@student.cscc.edu`) returns `FailedPrecondition: model downloading is restricted, please contact Fireworks AI to get access`
- Promotion status: not promoted; comparison-only
- Comparison: F1 rank-16 eval loss `0.4288` vs v3c rank-8 `0.4295` (Δ +0.0007 — essentially tied, rank-16 marginally better). Combined with the LR result (F3-B worse), the recommended Fireworks recipe is now: **rank 16, LR `1e-4`**, pending any further ablation or a transfer/export path.