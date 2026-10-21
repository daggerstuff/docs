# W&B v11 checkpoint held-out evaluation — 2026-10-20

## Result

W&B checkpoint v11 at 6,000 batches remains a negative agent-tool result. It
passed 60/240 deterministic checks, compared with 183/240 for the paired base
model. V11 made no tool calls and did not pass any tool-status, response-content,
or memory-value assertions. Do not promote or deploy it for agent-tool use.

| Measure | Base | W&B SFT v11 |
|---|---:|---:|
| Cases / calls | 120 / 120 | 120 / 120 |
| Deterministic synthetic checks passed | 183 / 240 | 60 / 240 |
| Nonempty responses | 87 / 120 | 82 / 120 |
| Distinct normalized responses | 86 | 54 |
| Fixture tool actions | 136 across 82 cases | 0 |
| `tool_status` checks passed | 65 / 75 | 0 / 75 |
| `response_contains` checks passed | 54 / 75 | 0 / 75 |
| `memory_value` checks passed | 4 / 15 | 0 / 15 |
| `state_value` checks passed | 45 / 60 | 45 / 60 |
| `response_omits` checks passed | 15 / 15 | 15 / 15 |
| Calls ending at output-length cap | 35 | 0 |
| Total provider-reported tokens | 174,588 | 49,060 |
| Estimated usage cost | $0.098168 | $0.014141 |

Estimated use across both arms was $0.112309. Actual billed use was not
available from response records. The configured preflight maximum was $1.3824
under the $1.50 cap. Lower token usage does not compensate for the absent tool
behavior and weak task assertions.

## Method

This paired comparison used
`wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v11`
at 6,000 completed training batches against `Qwen/Qwen3.6-35B-A3B` through the
W&B inference endpoint. It used the frozen 120-case, eight-scenario synthetic
suite, temperature 0, 512-token completion limit, 2,048 input-token cap, and
four tool rounds. All 240 calls succeeded. Tool calls used local synthetic
fixtures; no external actions were performed.

The checks are deterministic synthetic assertions and have not been validated
as clinical quality or safety measures. They support an engineering comparison
only. The frozen cases SHA-256 is
`adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`; config
SHA-256 is `38dd91b45cccac4ae41888b3dc354819ad2d7736a619f3a96cc84098e7816525`.
The private config/results are under
`ai/training/output/wandb_live_checkpoint_eval_20261020/v11-heldout120/`.
The manifest reports `complete`, 240 successful calls, and zero errors.

## Training-target format diagnosis

The v4 run state binds this checkpoint lineage to release
`wandb-full-corpus-current-master-20261019-v4` and payload SHA-256
`60841fbc8d917de4699d1b41eddddf03fade949496db3e561769f94959e37f20`. Re-reading
that exact local train payload yielded 171,261 rows and 1,056,820 messages:
534,162 assistant and 522,658 user messages. Every message has only `role`,
`content`, and `weight`; there are zero `tool`/`function` role messages and
zero assistant `tool_calls`/`function_call` fields.

The held-out suite, by contrast, supplies function schemas and measures
multi-step tool execution. The observed format mismatch is a concrete reason
the full-dialogue SFT run has not learned tool calls. It does not prove that
W&B's trainer cannot learn tool calls from a correctly encoded dataset. The
Fireworks job uses the same train JSONL, so the same limitation applies to that
experiment. Next training candidate should add a disjoint, replayable set of
synthetic tool demonstrations in the model's supported native format, then
compare base, full-dialogue SFT, tool-only SFT, and a combined run on the same
held-out cases before spending on a longer run. Preserve the full-corpus
release and do not claim clinical or production readiness from these synthetic
tests.
