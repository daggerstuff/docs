# W&B v32 five-case paired evaluation — 2026-10-20

Compared W&B adapter v32 (16,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v31. The paired evaluator allowed two local
mock-tool rounds. All 10 calls succeeded without inference errors. Estimated
usage was `$0.00482675` under the `$0.06` hard cap; actual billing is unverified.

V32 returned nonempty content in 0/5 cases, made no local tool rounds, and
passed 2/7 deterministic checks (state-value and response-omission). A separate
one-call probe using the same frozen support case confirmed the endpoint returned
`content: null`, a separate reasoning field, and `finish_reason: stop`; the
evaluator correctly measures user-facing content and does not treat the reasoning
field as a final response. It failed
the positive tool-status check. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. Like v31, v32 produced no
nonempty response on this small diagnostic suite and does not support
promotion. This suite does not establish clinical quality or safety.

Reproduction:

- Run: `wandb-v4-v32-five-scenario-dev-inference-20261020T050751Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `21cd9d79f9e889344c99cc9f4acea0e6ea46a5442502e7f56d1a4590fc9eff73`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v32`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v32-five-scenario-dev-autowatch/results/`
