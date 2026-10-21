# W&B v24 five-case paired evaluation — 2026-10-20

Compared W&B adapter v24 (12,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the same frozen five-case `synthetic_capability_v1`
development suite used for v19-v23. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.00477675` under the `$0.06` hard cap; actual billing is
unverified.

V24 returned nonempty content in 4/5 cases and made no local tool rounds. It
passed 2/7 deterministic checks (state-value and response-omission) and failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. V24's nonempty count
increased from v23's two/three across two repeats, but the five-case variance
and persistent missing tool use do not establish an improvement or support
promotion. The comparison also is not clinical quality or safety evidence.

Reproduction:

- Run: `wandb-v4-v24-five-scenario-dev-inference-20261020T0355Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `8069c5ee267f30114016d7e3fdec180bb64d4710e87714d658f209e13e6e2f6a`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v24`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v24-five-scenario-dev/results/`
