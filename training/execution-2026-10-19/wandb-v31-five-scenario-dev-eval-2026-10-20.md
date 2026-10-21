# W&B v31 five-case paired evaluation — 2026-10-20

Compared W&B adapter v31 (16,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v30. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.00476925` under the `$0.06` hard cap; actual billing is unverified.

V31 returned nonempty content in 0/5 cases, made no local tool rounds, and
passed 2/7 deterministic checks (state-value and response-omission). It failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. V31 has regressed on this
small diagnostic suite and does not support promotion. This suite does not
establish clinical quality or safety.

Reproduction:

- Run: `wandb-v4-v31-five-scenario-dev-inference-20261020T050220Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `f7454713375458ecd77dd3681a54bb51f9ac59bc81477fadf95d19ade020699b`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v31`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v31-five-scenario-dev-autowatch/results/`
