# W&B v44 five-case paired evaluation — 2026-10-20

Compared locally mirrored W&B adapter v44 (22,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the same frozen five-case
`synthetic_capability_v1` development suite used for v42. All ten requests
succeeded. This is a small diagnostic, not a validated quality, clinical, or
safety measure.

V44 returned nonempty content on 3/5 cases, made zero local tool rounds, and
passed 2/7 deterministic synthetic checks. The base returned nonempty content
on 3/5, made four tool rounds, and passed 3/7 checks. The SFT arm generated 91
completion tokens across five cases. V44 therefore has not recovered the
baseline's tool-use behavior and is not suitable for promotion based on this
evaluation.

Estimated usage was `$0.004753` under the `$0.05376` worst-case cap; actual
billing is unverified. The deterministic checks are explicitly marked
unvalidated for quality or safety.

Reproduction details:

- Run ID: `wandb-v4-v44-five-scenario-dev-inference-20261020T0705Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `4c49475897ae6b618fc679f8f717d8bf1c862596aab7ad1a613cd00856423dc1`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v44`
- Private config, case-level results, and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v44-five-scenario-dev/` (mode 0700 directory, mode 0600 files).
- Result manifest SHA-256: `b48b7d161e554cfef82af84857fe55aed3dd65e29fea734ab0ed1a2d7a386696`
- Result rows SHA-256: `73ec5d94eca42971b56caef4ab71f004c39b929ec980986c79435134d8ada343`
