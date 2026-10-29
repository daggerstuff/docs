# Fireworks Muse Glimmer v3b — Half-LR Ablation (2026-10-23)

- Job ID: `accounts/linencloset/supervisedFineTuningJobs/pixelated-glimmer-v3b-20261023171703-r1`
- State: `JOB_STATE_COMPLETED` at 2026-10-24T04:52:01Z (launch 2026-10-23T17:17Z)
- Base model: `accounts/fireworks/models/muse-glimmer-30b`
- Train dataset: `accounts/linencloset/datasets/arc-pilot-v1-train` (418 rows)
- Eval dataset: `accounts/linencloset/datasets/arc-pilot-v1-eval` (80 rows)
- Output model: `accounts/linencloset/models/arc-pilot-v3b-glimmer-lr5e5` (`READY`)
- Treatment: learning rate `5e-5` (half of F1's `1e-4`); every other setting identical to F1 (2 epochs, rank 16, LR warmup 0, max context 32,768, `eval_auto_carveout=false`, checkpoint interval 1000)
- Training telemetry: 28 optimizer steps, eval loss `0.6492 → 0.4485`, ppl `1.914 → 1.566`; step-28 train loss `0.3930`
- Promo/rated cost: `$0.00`, attribution `COMPLETE`, 0 rows (verified post-run)
- Download entitlement: still restricted (same account condition as F1; API keys cannot download)
- Promotion status: not promoted; comparison-only
- Comparison vs F1 (lr `1e-4`): F1 eval loss `0.4288` vs v3b `0.4485` (Δ +0.0196, i.e. half LR worse on this eval slice). On this single ablation, the baseline `1e-4` is the better of the two; recommend retaining `1e-4` for the next data/model experiment rather than halving LR.
- Note: 28-step slice, single seed, and provider-side unrolling mean this is a directional provider-match signal only; the full arc v1 report also contains F1. Treat both as `comparison/diagnostic`, not promotion evidence.