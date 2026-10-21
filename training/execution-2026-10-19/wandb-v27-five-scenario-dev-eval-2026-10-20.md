# W&B v27 five-case paired evaluation — 2026-10-20

Compared W&B adapter v27 (14,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v26. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.0047455` under the `$0.06` hard cap; actual billing is unverified.

V27 returned nonempty content in 5/5 cases, made no local tool rounds, and
passed 2/7 deterministic checks (state-value and response-omission). It failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and also passed 3/7 checks. V27's improved
nonempty response coverage does not resolve its repeated failure to call tools.
This small synthetic suite does not establish quality or safety and does not
support promotion for agent-tool use.

Reproduction:

- Run: `wandb-v4-v27-five-scenario-dev-inference-20261020T042208Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `f7a7583a4925f7366556579d3afc3cd40782fbcb2a7c802e046b724a9c234df9`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v27`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v27-five-scenario-dev-autowatch/results/`
