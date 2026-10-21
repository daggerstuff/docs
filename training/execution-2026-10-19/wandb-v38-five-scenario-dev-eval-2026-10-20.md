# W&B v38 five-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v38 (19,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite. All 10 calls succeeded. Estimated usage was `$0.0047155`
against a `$0.05376` upper-bound cap; actual billing is unverified.

V38 returned nonempty content in 0/5 cases, made zero local tool rounds, and
passed 2/7 deterministic synthetic checks. The base returned nonempty content
in 3/5 cases, made four local tool rounds, and passed 3/7 checks. The SFT arm
used 33 completion tokens total. This checkpoint is not promotable.

These five cases are diagnostics, not validated measures of clinical quality
or safety. The later 120-case tests found output collapse at v38 and v39, then
recovered response availability at v41 while tool behavior remained broken.
See the [v41 120-case report](wandb-v41-prompt-disjoint-heldout120-eval-2026-10-20.md).

Reproduction:

- Run: `wandb-v4-v38-five-scenario-dev-inference-20261020T060741Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `f387132156e735acac4678ff366d05f70cec731ddb6728d0170d6b84df8ffc0e`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v38`
- Local adapter SHA-256: `ddb5d86499a2be81829865cb8c839a9d2c98899bddf1d2e4433a50d36a2d1f5d`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v38-five-scenario-dev-autowatch/results/`
