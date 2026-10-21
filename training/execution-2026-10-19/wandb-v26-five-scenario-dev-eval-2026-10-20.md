# W&B v26 five-case paired evaluation — 2026-10-20

Compared W&B adapter v26 (13,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v25. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.00471925` under the `$0.06` hard cap; actual billing is
unverified.

V26 returned nonempty content in 5/5 cases and made no local tool rounds. It
passed 2/7 deterministic checks (state-value and response-omission) and failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. V26's response coverage
matches v21 and v25 on this small suite, but it again made no tool calls and
failed the positive tool check. The result does not support promotion for
agent-tool use and is not clinical quality or safety evidence.

Reproduction:

- Run: `wandb-v4-v26-five-scenario-dev-inference-20261020T041139Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `9acfd0241d4a8e3cb36be4bd7a912d1e6f19df043b61ffca38be67370cf501a5`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v26`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v26-five-scenario-dev-autowatch/results/`
