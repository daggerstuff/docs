# W&B v42 five-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v42 (21,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite. All 10 calls succeeded. Estimated usage was `$0.0047555`
against a `$0.05376` upper-bound cap; actual billing is unverified.

V42 returned nonempty content in 3/5 cases, made zero local tool rounds, and
passed 2/7 deterministic synthetic checks. The base returned nonempty content
in 3/5 cases, made four local tool rounds, and passed 3/7 checks. The SFT arm
used 93 completion tokens total over five cases. V42 retains the tool-use
failure observed in v41 and does not support promotion.

These five cases are diagnostic only; their checks are not validated measures
of clinical quality or safety. The larger [v41 prompt-disjoint evaluation](wandb-v41-prompt-disjoint-heldout120-eval-2026-10-20.md)
found recovered response availability but continued failure on tool-use and
task-specific response checks.

Reproduction:

- Run: `wandb-v4-v42-five-scenario-dev-inference-20261020T064326Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `7d3733f2e95b6c44dea1ce15ece03ec778c839e5af3ef7b28b432359e8f1e330`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v42`
- Local adapter and train-state backups: `ai/training/output/wandb_local_checkpoints_20261019/v4/v42/` and `ai/training/output/wandb_local_checkpoints_20261019/v4-train-state/v42/`; both passed manifest size and SHA-256 verification.
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v42-five-scenario-dev-autowatch/results/`
