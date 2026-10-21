# W&B v56 prompt-disjoint paired evaluation — 2026-10-20 (initial request)

**Status correction:** this run used the endpoint's default reasoning mode
because the evaluator omitted `chat_template_kwargs` from its request. Do not
interpret its empty SFT responses as a no-thinking result. The corrected,
explicit no-thinking replay completed separately; see the
[valid paired result](wandb-v56-explicit-no-thinking-paired-2026-10-20.md).

## Result

The run completed all 120 prompt-disjoint cases through both arms: 240/240
calls succeeded with no runner errors. Case IDs and case hashes match across
arms, as do decoding and evaluator-config hashes. The W&B base arm used
`Qwen/Qwen3.6-35B-A3B`; the SFT arm used full-corpus checkpoint v56
(`wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v56`,
28,500 training batches).

Despite technical success, the v56 SFT endpoint returned an empty visible
response for all 120 cases, made no tool calls, and stopped at the turn limit
in 113 cases. Seven responses finished at the token limit. This is a severe
behavioral failure on this synthetic tool-use evaluation. The base returned
non-empty content in 103/120 cases and made 137 tool rounds across 120 cases.
These deterministic checks are diagnostic and unvalidated; they do not
measure clinical quality, safety, or production suitability.

| Measure | Base | SFT v56 |
|---|---:|---:|
| Successful calls | 120/120 | 120/120 |
| Non-empty visible responses | 103/120 | 0/120 |
| Tool rounds | 137 | 0 |
| Completion calls | 257 | 120 |
| Finish reason = length | 19 | 7 |
| Synthetic tool-status checks | 74/75 | 0/75 |
| Synthetic response-contains checks | 60/75 | 0/75 |
| Synthetic memory-value checks | 5/15 | 0/15 |
| Synthetic state-value checks | 45/60 | 45/60 |
| Synthetic response-omits checks | 12/15 | 15/15 |
| Median / p95 latency | 2.90 / 6.56 s | 1.03 / 4.81 s |
| Prompt + completion tokens | 124,019 + 49,642 | 47,814 + 12,993 |
| Estimated inference cost | $0.09305725 | $0.02819475 |

The combined result-level cost estimate is $0.121252. The configured
preflight hard maximum was $1.35168. Actual provider billing was not returned.
Both arms used temperature 0, 512 max output tokens, a 3,072-token input cap,
and at most three tool rounds. Although the config declared thinking disabled,
the evaluator omitted `chat_template_kwargs` from the HTTP payload, so the
provider used its default reasoning mode. This result is not a verified
no-thinking comparison. W&B's [chat-completions schema](https://docs.wandb.ai/api-reference/chat-completions/create-chat-completion-1)
supports the field; the request client now transmits it, with an explicit
no-thinking paired rerun underway. The frozen suite SHA-256
is `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`;
config SHA-256 is
`4a67bf6d0e3389d5eaff63797f7c4e0a7a8d937abc8516d82531fa1c62c8cf77`.
The private result JSONL SHA-256 is
`e448643dfadf294da57a6aead6fb60f25a3da30657b38ba5b9507cb89fcce14e`.

## Interpretation and next experiment

The earlier v55 run returned non-empty content on all 120 cases, whereas v56
returned empty content on every case, both through the provider's default
reasoning mode. Since the earlier request payloads were not saved and v55 used
a four-round cap while v56 used three, do not attribute this result to a
checkpoint regression yet. The partial v57 replay was canceled after 63 cases
when the omitted request field was discovered. The request client now sends
`chat_template_kwargs`; the clean explicit no-thinking paired rerun will
isolate the declared setting.

The output and config are kept in the mode-0700 private directory
`ai/training/output/wandb_live_checkpoint_eval_20261020/v56-prompt-disjoint-heldout120-paired-nonthinking/`.
The result manifest marks the run complete, contains 240 successes and zero
errors, and records actual billed cost as unknown.
