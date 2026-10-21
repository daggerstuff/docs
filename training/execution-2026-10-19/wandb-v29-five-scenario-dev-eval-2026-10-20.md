# W&B v29 five-case paired evaluation — 2026-10-20

Compared W&B adapter v29 (15,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v28. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.004893` under the `$0.06` hard cap; actual billing is unverified.

V29 returned nonempty content in 5/5 cases, made no local tool rounds, and
passed 2/7 deterministic checks (state-value and response-omission). It failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. V29's nonempty responses
do not resolve its repeated failure to call tools. This small synthetic suite
does not establish quality or safety and does not support promotion for
agent-tool use.

Reproduction:

- Run: `wandb-v4-v29-five-scenario-dev-inference-20261020T044218Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `de2a99da7b88a13ffa86acfe0ec7b7a82877ce02e51dbccd3f42767ccfc5b811`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v29`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v29-five-scenario-dev-autowatch/results/`
