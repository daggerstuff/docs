# W&B v28 five-case paired evaluation — 2026-10-20

Compared W&B adapter v28 (14,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v27. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.0059705` under the `$0.06` hard cap; actual billing is unverified.

V28 returned nonempty content in 5/5 cases, made no local tool rounds, and
passed 2/7 deterministic checks (state-value and response-omission). It failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. V28's nonempty responses
do not resolve its repeated failure to call tools. This small synthetic suite
does not establish quality or safety and does not support promotion for
agent-tool use.

Reproduction:

- Run: `wandb-v4-v28-five-scenario-dev-inference-20261020T043136Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `5ddc5977d16ed03f51ee7591d3678efbe67a99b5c72f681009663febf1621e3d`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v28`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v28-five-scenario-dev-autowatch/results/`
