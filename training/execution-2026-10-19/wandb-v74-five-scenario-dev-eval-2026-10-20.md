# W&B v74 five-case checkpoint evaluation — 2026-10-20

Compared W&B full-corpus adapter v74 (37,500 batches) against the Qwen3.6-35B-A3B base on the frozen five-case synthetic development suite using no-thinking decoding, a 2,048-token input cap, and at most two tool rounds. The run recorded 10 arm/case rows; nine requests succeeded, and the base research case stopped at the configured context preflight after two tool rounds.

| Measure | Base | SFT v74 |
|---|---:|---:|
| Successful requests | 4/5 | 5/5 |
| Evaluator-local tool rounds | 4 | 0 |
| Deterministic synthetic checks passed | 3/6 scored | 2/7 |
| Research case | context-cap failure; unscored | response returned; no tool calls |
| Estimated inference use | $0.0009455 | $0.0003705 |

SFT v74 still did not recover tool use on this suite. These unvalidated synthetic checks are diagnostic only and do not establish clinical quality, safety, or production suitability. The run is marked incomplete because the base research case exceeded the evaluator's configured context preflight; actual provider billing is unknown. The v74 adapter and train-state remain locally mirrored. W&B SFT is documented as public preview, with adapter training free during preview; inference and artifact storage are separate charges.

Reproduction and integrity:

- Run ID: `wandb-v4-v74-five-scenario-dev-paired-no-thinking-20261020T1157Z`
- Cases SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `e199b8fc5cbf0b2ff3e7ab1b3624e30e34d227ca25306f11e309446e687d7ffb`
- Result rows SHA-256: `b2252f3ab66c541242e6a0a31009b986ee6b2171c2af32017d73926c3ca35269`
- Estimated worst-case cap: $0.05376; actual billing unknown.
- Private config/results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v74-five-scenario-dev-paired-no-thinking/` (directory mode 0700; files mode 0600).

## Follow-up: v75 at 38,000 batches

The same paired run was repeated on v75 with the same cases, decoding, input/round limits, and $0.06 hard cap. It completed 9/10 requests; the base again hit the research-case context preflight. Base passed 3/6 scored checks and made four tool rounds. V75 passed the same 2/7 checks as v74 and made zero tool calls. The v74/v75 response text changed on all five cases, but none of the deterministic check outcomes or tool-call behavior changed. This checkpoint-to-checkpoint comparison shows no measured tool-behavior recovery, so do not spend on a 120-case v75 evaluation based on this sentinel alone.

- Run ID: `wandb-v4-v75-five-scenario-dev-paired-no-thinking-20261020T1202Z`
- Adapter and train-state: v75, 38,000 batches, mirrored locally.
- Config SHA-256: `778512698f0713884ad871cf78b709fff3440828d987252316e262467f587a99`
- Result rows SHA-256: `8f878131efb209151c0b75fcfc8e2e1d016f184ec0c046043d0b5a5ace48790e`
- Estimated inference use: `$0.001421`; actual billing unknown; worst-case cap `$0.05376`.
- Private config/results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v75-five-scenario-dev-paired-no-thinking/`.
