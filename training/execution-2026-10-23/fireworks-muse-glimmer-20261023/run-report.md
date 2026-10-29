# Fireworks Muse Glimmer v2 — Checkpoint-Safe SFT (2026-10-23)

- Job ID: `accounts/linencloset/supervisedFineTuningJobs/pixelated-glimmer-v2-20261023151943-r1`
- State: `JOB_STATE_COMPLETED` (15:19:43Z → 16:16:43Z)
- Base model: `accounts/fireworks/models/muse-glimmer-30b`
- Train dataset: `accounts/linencloset/datasets/arc-pilot-v1-train` (418 rows)
- Eval dataset: `accounts/linencloset/datasets/arc-pilot-v1-eval` (80 rows)
- Output model: `accounts/linencloset/models/arc-pilot-v2-therapist-sft-checkpoints` (`READY`)
- Recipe: 2 epochs, LoRA rank 16, LR `1e-4`, max context 32,768, `eval_auto_carveout=false`
- Checkpoint safety: `sampler_checkpoint_save_interval_steps=1000`
- Training telemetry: 28 optimizer steps, eval loss `0.6492 → 0.4288`, ppl `1.914 → 1.535`; total training token exposure ≈ 58M across the recorded steps
- Promo verification: pre-run and post-run 24h/1d `usageCosts:query` both return subtotal `$0.00`, attribution `COMPLETE`, zero rows
- Download entitlement: still restricted (`403`: "model downloads require signing in with `firectl signin` or the Fireworks console; API keys cannot download models")
- Promotion status: not promoted; treated as Fireworks-only comparison-only adapter
- Next experiment decision: launch F3-B (same dataset, half learning rate `5e-5`, all else identical) as a free one-factor LR ablation. F2 (50% data ablation) is deferred until there is a supported, reproducible dataset-upload path in this account; no manual/undocumented upload was attempted.

## Security and cost boundaries honored

- No `--allow-paid` override or comparable override used.
- No ad-hoc sampling sweeps; only the pre-carved eval dataset was attached.
- No deployment or serving endpoint was provisioned.
- No artifact was downloaded, and weights remain provider-hosted comparison material only.