# W&B v51 prompt-disjoint 120-case paired evaluation — 2026-10-20

Compared W&B Serverless Training adapter v51 (26,000 completed batches) with its Qwen/Qwen3.6-35B-A3B base on the frozen 120-case prompt-disjoint synthetic tool-use suite. Decoding, the 512-token completion cap, 2,048-token input preflight, and four-round evaluator-local mock-tool setup match the v41 evaluation. This is a synthetic deterministic diagnostic, not a validated measure of quality, clinical safety, or suitability.

The initial paired run completed 239/240 successful requests and was marked incomplete because one base call (`tool-eval-memory_opt_in-137`) ended in `ClientPayloadError`. A separate single-case base retry succeeded. The retry replaced only that failed case for the aggregates below; the original incomplete result set and retry are preserved separately. Effective coverage is 120/120 cases for each arm, with one recovered transport error.

| Measure | Base | W&B SFT v51 |
| --- | ---: | ---: |
| Successful visible completions | 102/120 | 29/120 |
| Evaluator-local tool rounds | 137 | 0 |
| `tool_status` checks | 72/75 | 0/75 |
| `response_contains` checks | 64/75 | 0/75 |
| `state_value` checks | 45/60 | 45/60 |
| `response_omits` checks | 12/15 | 15/15 |
| `memory_value` checks | 5/15 | 0/15 |
| All deterministic checks | 198/240 | 60/240 |
| Completion tokens | 49,991 | 54,636 |
| Finish reason `length` | 21 | 102 |

Visible completion counts by scenario (15 cases per scenario):

| Scenario | Base | v51 SFT |
| --- | ---: | ---: |
| Appointment consent gate | 15/15 | 3/15 |
| Appointment explicit consent | 15/15 | 0/15 |
| Approval gate | 6/15 | 1/15 |
| Memory consent gate | 10/15 | 2/15 |
| Memory opt-in | 12/15 | 5/15 |
| Resource comparison | 15/15 | 10/15 |
| Resource lookup | 15/15 | 6/15 |
| Untrusted note | 14/15 | 2/15 |

V51 is not promotable for this agent-tool objective. It made no tool rounds, failed every tool-status and expected-response-content check, and hit the 512-token limit on 102/120 cases. Its 60/240 checks equal v41, but its visible completion count is much worse than v41's 117/120; the base arm remained broadly similar (v41: 101/120 visible, 138 tool rounds, 200/240 checks). The direct v51 PONG probe also found `message.content: null` with only a `reasoning` field. Do not treat reasoning-channel text as final user-visible output. These findings indicate real v51 output/tool-behavior failure at the endpoint; they do not prove checkpoint corruption or establish clinical quality/safety.

Estimated paired-evaluation usage was `$0.1730955`; the separately estimated retry was `$0.00072875`, for `$0.17382425` combined. The original worst-case preflight was `$1.3824` and the retry worst case `$0.00576`, remaining under the configured `$1.50` hard cap. Actual billing is unavailable.

Reproduction and integrity:

- Main run: `wandb-v4-v51-prompt-disjoint-toolrounds4-heldout120-20261020T0815Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Evaluator config digest: `8764d27e2ea12b294276ce475045d1d6aed19a9085b7f5b38261dbcb4b336546`
- Result-manifest SHA-256: `2ae5e456e05f70903849b0ea2cdc1ec2937c18189eb990c31b99e388fa653f0a`
- Result-rows SHA-256: `4e90245a3428513a32957d38b6b1a55495019382d1e3ddbf385f376f8adfc86b`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v51`
- Retry run: `wandb-v4-v51-base-memory-opt-in-137-retry-20261020T0833Z`; one base request succeeded with one evaluator-local tool round.
- Private config, result rows, and retry artifacts are under `ai/training/output/wandb_live_checkpoint_eval_20261020/v51-prompt-disjoint-toolrounds4-heldout120/` (directories mode 0700, files mode 0600).

Compare with the [v41 120-case evaluation](wandb-v41-prompt-disjoint-heldout120-eval-2026-10-20.md), [v51 five-case diagnostic](wandb-v51-five-scenario-dev-eval-2026-10-20.md), and [v51 response-channel checks](wandb-v50-response-channel-diagnostic-2026-10-20.md).
