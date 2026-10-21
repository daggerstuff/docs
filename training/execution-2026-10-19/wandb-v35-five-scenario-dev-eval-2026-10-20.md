# W&B v35 five-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v35 (18,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite. All 10 calls succeeded. Estimated usage was `$0.0049705`
against a `$0.05376` upper-bound cap; actual billing is unverified.

V35 returned nonempty content in 1/5 cases, made zero local tool rounds, and
passed 2/7 deterministic synthetic checks. The base returned nonempty content
in 3/5 cases, made four local tool rounds, and passed 3/7 checks. This is
consistent with v33/v34: the adapter still does not use tools. This small
synthetic diagnostic is unvalidated and does not support promotion.

Reproduction:

- Run: `wandb-v4-v35-five-scenario-dev-inference-20261020T053809Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `69fdb897c050ef8a003ddfd0942dcf63a4c0592c42608ed492e0eb9361c6421e`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v35`
- Local adapter SHA-256: `5c348673d104066fa59a7e13b6793eff3e137f890dd0f279bb39667786c48492`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v35-five-scenario-dev-autowatch/results/`

See also the paired [v33 and v34 prompt-disjoint held-out comparisons](wandb-v33-prompt-disjoint-heldout120-eval-2026-10-20.md).
