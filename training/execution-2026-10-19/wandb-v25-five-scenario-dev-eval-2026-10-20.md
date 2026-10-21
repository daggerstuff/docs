# W&B v25 five-case paired evaluation — 2026-10-20

Compared W&B adapter v25 (13,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v24. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.004738` under the `$0.06` hard cap; actual billing is unverified.

V25 returned nonempty content in 5/5 cases and made no local tool rounds. It
passed 2/7 deterministic checks (state-value and response-omission) and failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. V25's improved nonempty
count is a small-suite result; persistent missing tool use does not support
promotion for agent-tool use. The comparison is not clinical quality or safety
evidence.

Reproduction:

- Run: `wandb-v4-v25-five-scenario-dev-inference-20261020T040203Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `8d6b693e16035453a066ba87bc040db1b5a693e1a048aa480fbad16c218b531f`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v25`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v25-five-scenario-dev-autowatch/results/`
