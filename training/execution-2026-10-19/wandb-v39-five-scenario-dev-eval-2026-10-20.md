# W&B v39 five-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v39 (20,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite. All 10 calls succeeded. Estimated usage was `$0.0047255`
against a `$0.05376` upper-bound cap; actual billing is unverified.

V39 returned nonempty content in 0/5 cases, made zero local tool rounds, and
passed 2/7 deterministic synthetic checks. The base returned nonempty content
in 3/5 cases, made four local tool rounds, and passed 3/7 checks. The SFT arm
used 41 completion tokens total. This checkpoint is not promotable.

These five cases are diagnostics, not validated measures of clinical quality
or safety. The later 120-case tests found output collapse at v38 and v39, then
recovered response availability at v41 while tool behavior remained broken.
See the [v41 120-case report](wandb-v41-prompt-disjoint-heldout120-eval-2026-10-20.md).

Reproduction:

- Run: `wandb-v4-v39-five-scenario-dev-inference-20261020T061807Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `8aaa819ca80b79da34897b70c251e2cb3c2a77820b713170695ad9a7fda4d13c`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v39`
- Local adapter SHA-256: `8df21efe8eb08e44c411aa94e5179a2e58d2a9f5956360603b5c28b8bc016a50`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v39-five-scenario-dev-autowatch/results/`
