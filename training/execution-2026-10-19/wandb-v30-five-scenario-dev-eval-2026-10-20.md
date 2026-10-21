# W&B v30 five-case paired evaluation — 2026-10-20

Compared W&B adapter v30 (15,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v29. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.0047105` under the `$0.06` hard cap; actual billing is unverified.

V30 returned nonempty content in 5/5 cases, made no local tool rounds, and
passed 2/7 deterministic checks (state-value and response-omission). It failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. V30's nonempty responses
do not resolve its repeated failure to call tools. This small synthetic suite
does not establish quality or safety and does not support promotion for
agent-tool use.

Reproduction:

- Run: `wandb-v4-v30-five-scenario-dev-inference-20261020T045150Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `8622043f64d82f2eb9aab4b7688d0bf835463af2c6ed40b36f35b19f17ce96eb`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v30`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v30-five-scenario-dev-autowatch/results/`
