# Free Training Experiment Gameplan — 2026-10-23

Status: executable. Free-first, checkpoint-safe, $0 out-of-pocket ceiling. Created after verifying that the Fireworks Muse Glimmer 30B SFT promotional window remains open through 11/30 and that the prior account (`linencloset`) still exposes `arc-pilot-v1-train` / `arc-pilot-v1-eval` and the completed model `arc-pilot-v1-therapist-sft`.

## 1. Provider coverage and routes

| Lane | Free / credit terms | Trainable base(s) | Export / serving posture | Notes |
|---|---|---|---|---|
| Fireworks Managed SFT | Muse Glimmer 30B SFT free through 2026-11-30, no card required; REST-rated $0.00 verified (pilot log §§10-11) | `accounts/fireworks/models/muse-glimmer-30b` (only) | Trained models serve on dedicated deployments; local download remains restricted on this account; treat as comparison-only | **Always** enable intermediate sampler checkpoints; prior run was lost at 5,886/10,704 steps with no save |
| W&B / CoreWeave Serverless | SFT/RL free during public preview; inference + artifact storage metered separately; `$250` inference allowance, ~`$162.84` remaining (v6 handoff) | Authorized: Gemma 4 26B A4B, Nemotron 3.5 Lightning 30B A3B. Qwen is outside current model restriction. | Adapters are downloadable and portable to W&B inference / OVH | Only these two bases are allowed; do not restart completed v6 jobs |
| Adaption (credit-funded) | Credit-funded SFT/DPO via AutoScientist | Prior Qwen SFT reference only; run exported and available locally | Best exportable lane; credits required (no card-free free tier) | Qualify credit costs before every operation |
| Together.ai | API key present; no free training confirmed | TBD | TBD | Optional, only after an explicit cost quote |

Second/third lanes exist but Fireworks is the only one explicitly free and no-card right now. Adaption is the lane whose weights can leave the provider; Fireworks and W&B adapters feed export qualification later, not promotion.

## 2. Checkpoint-safety rules (non-negotiable)

1. Every Fireworks managed run sets `sampler_checkpoint_save_interval_steps`. Use 1,000 steps on a ~10,704-step job so at most ~1,000 steps are ever lost.
2. Each run also attempts `wandb_config` integration so loss curves persist off-provider.
3. Do not use `--allow-paid` or any override; the free-first ceiling is $0 out of pocket.
4. Sample sparingly: eval carveout disabled or use the pre-carved `arc-pilot-v1-eval` dataset once; no ad-hoc sampling sweeps.
5. Record job IDs, endpoint names, checkpoint names, and local mirror locations in the pilot log immediately on job creation.
6. If usageCosts shows non-zero rated spend, stop and escalate before any second run.

## 3. Experiment matrix (sequential, not factorial)

Start with at most one Fireworks run per week plus the already-authorized W&B follow-ups. Only add experiments after a completed run report and cost reconciliation.

| ID | Arm | Provider | Base | Treatment | Gate to proceed |
|---|---|---|---|---|---|
| F0 | Baseline re-validation | Fireworks | Muse Glimmer | No new training; rerun 5 paired smoke cases against existing `arc-pilot-v1-therapist-sft` if inference access is granted | Download / serving entitlement verified |
| F1 | Checkpoint-safe SFT v2 | Fireworks | Muse Glimmer | Same `arc-pilot-v1-train`, 2 epochs, save interval 1,000, wandb on | Promo verified $0.00 spend (usageCosts) |
| F2 | Data ablation (nested 50%) | Fireworks | Muse Glimmer | Reuse a 50% train subset derived deterministically from v1 splits | F1 completed with at least one checkpoint |
| F3 | Rank/LR ablation | Fireworks | Muse Glimmer | Rank 8 vs 16 and baseline vs half LR; one factor at a time | F2 completed and F1's report written |
| W1 | Ablation on Gemma | W&B Serverless | Gemma 4 26B | Seed/run replication of v6 baseline on a pre-declared data slice | New hypothesis + covered credits |
| W2 | Ablation on Nemotron | W&B Serverless | Nemotron 3.5 Lightning | Matched W1 configuration | W1 completed and reported |
| A1 | Exportable SFT on anchor base | Adaption | Qwen 3.6 35B (exact revision pinned) | AutoScientist SFT/LoRA; export + local mirror | Credit balance verified and bounded |
| V1 | Evaluation harness check | local | n/a | Freeze `safety-quality-dev-v1` subset and run deterministic tool/state checks | Corpus split unchanged |

## 4. Immediate execution sequence (today)

1. **Read-only qualification** (already authorized): verify Fireworks promo remains $0.00 rated and list jobs/datasets; verify W&B remaining credit estimate; verify Adaption dataset status without creating jobs.
2. **F1 launch**: one bounded Muse Glimmer SFT run on the existing accepted dataset with intermediate sampler saves. This is the single highest-value use of the free window because the previous run produced no checkpoint.
3. **Local mirror + validate**: as soon as F1 reaches a terminal state (or a saved sampler checkpoint is exposed), mirror it, run CPU validation, and record step-level telemetry.
4. **Report**: write `fireworks-muse-glimmer-20261023/run-report.md` covering steps completed, checkpoints saved, cost, and next experiment decision.
5. **Capture memory**: store the run ID, model ID, and outcome in Foresight immediately so it survives session interruption.

### Launch template (F1)

- `base_model`: `accounts/fireworks/models/muse-glimmer-30b`
- `dataset`: `accounts/linencloset/datasets/arc-pilot-v1-train`
- `evaluation_dataset`: `accounts/linencloset/datasets/arc-pilot-v1-eval`
- `epochs`: 2
- `max_context_length`: 32768
- `lora_rank`: 16
- `learning_rate`: 0.0001 (1e-4)
- `sampler_checkpoint_save_interval_steps`: 1000
- `supervised_fine_tuning_job_id`: `pixelated-glimmer-v2-<timestamp>-r1`
- `output_model`: `arc-pilot-v2-therapist-sft-checkpoints`
- `eval_auto_carveout`: false (already have a carved eval set; avoid uncapped eval tokens)
- `wandb_config`: enabled against project `wayfarer-ab-test` if the secret is available at runtime

Do not launch F2 or W1 until F1's report and cost reconciliation are written.

## 5. Reporting and stopping rules

- Report every run with job ID, base/parent checkpoint, recipe, dataset hash, sample/checkpoint names, actual and rated cost, and a one-line "next experiment decision".
- Stop immediately if a provider invoice is non-zero, a credit balance cannot be confirmed before a charge, or a new base/model is not in the approved list.
- Never treat a trained adapter as a promotion; the owner’s blinded assessment remains the promotion gate.
- Keep all clinical or production claims gated on credentialed review and source/privacy clearance.

## 6. Cross-lane dependency on ongoing work

- Continue dataset provenance and `bounded-support-v35` source-context audit in parallel; they do not block F1 because F1 reuses the frozen v1 dataset.
- Continue the unreturned Paige Taylor blinded assessment; do not consume training budget waiting on it.
- Preserve the 93,543 explicit holdouts and source rights/consent dispositions; no experiment clears them.

## 7. First concrete action executed

- `F1` launch captured in the pilot log and Foresight memory.
