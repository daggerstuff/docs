# W&B v41 five-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v41 (21,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite. All 10 calls succeeded. Estimated usage was `$0.00474675`
against a `$0.05376` upper-bound cap; actual billing is unverified.

V41 returned nonempty content in 4/5 cases, made zero local tool rounds, and
passed 2/7 deterministic synthetic checks. The base returned nonempty content
in 3/5 cases, made four local tool rounds, and passed 3/7 checks. The SFT arm
used 71 completion tokens total over five cases. The result does not support
promotion: response presence improved over base, but tool use and the combined
synthetic checks did not.

These five cases are a diagnostic suite, not validated clinical quality or
safety measures. A subsequent 120-case evaluation at v41 showed that response
availability had recovered (117/120 nonempty), while tool behavior remained
broken (zero rounds; 60/240 checks). See the [larger v41 held-out evaluation](wandb-v41-prompt-disjoint-heldout120-eval-2026-10-20.md).

Reproduction:

- Run: `wandb-v4-v41-five-scenario-dev-inference-20261020T063301Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `f48aa31fb3989d977200bcfc213bee3d7010c81fd8d7d1f1d59d13f3d301ecba`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v41`
- Local adapter and train-state backups: `ai/training/output/wandb_local_checkpoints_20261019/v4/v41/` and `ai/training/output/wandb_local_checkpoints_20261019/v4-train-state/v41/`
- Train-state backup: 11 files, 1,060,414,703 bytes; all manifest sizes and SHA-256 hashes verified.
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v41-five-scenario-dev-autowatch/results/`

See the [v38 held-out evaluation](wandb-v38-prompt-disjoint-heldout120-eval-2026-10-20.md),
[v39 held-out evaluation](wandb-v39-prompt-disjoint-heldout120-eval-2026-10-20.md),
and [v19-v37 trend](wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md).
