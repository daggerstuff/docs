# W&B v37 five-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v37 (19,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite. All 10 calls succeeded. Estimated usage was `$0.00476675`
against a `$0.05376` upper-bound cap; actual billing is unverified.

V37 returned nonempty content in 5/5 cases, made zero local tool rounds, and
passed 2/7 deterministic synthetic checks. The base returned nonempty content
in 3/5 cases, made four local tool rounds, and passed 3/7 checks. The SFT arm
used 73 completion tokens total over five cases. This continues the pattern
seen in v33-v36: response presence varies, but no tested SFT checkpoint uses
tools. The small unvalidated synthetic result does not support promotion.

Reproduction:

- Run: `wandb-v4-v37-five-scenario-dev-inference-20261020T055814Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `b541661e28f36cb177491d2d7a50c6a9c29d983442cc45d42aaf70090da95c4c`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v37`
- Local adapter SHA-256: `c70b52c697b48863ff3c67c6e7771a8454a09264bc0cdec9a4fad81b83b8f7ea`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v37-five-scenario-dev-autowatch/results/`

See the [v19-v37 trend](wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md)
and the larger [v33/v34 paired held-out evaluations](wandb-v33-prompt-disjoint-heldout120-eval-2026-10-20.md).
