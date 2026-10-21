# W&B v55 prompt-disjoint paired evaluation — 2026-10-20

## Result

The exact 120-case prompt-disjoint suite now has one successful base-model
result and one successful v55 result for every case. Both arms used temperature
0 and a 512-token completion cap. The saved config declared
`enable_thinking=false`, but the evaluator omitted `chat_template_kwargs`
from its HTTP request body. The provider therefore used its default reasoning
mode; this is not a verified no-thinking run. W&B's [chat-completions API
schema](https://docs.wandb.ai/api-reference/chat-completions/create-chat-completion-1)
supports this request field, and the evaluator was fixed on 2026-10-20. The initial paired
run used a 2,048-token input preflight cap and returned all 120 v55 rows plus 75
base rows; the other 45 base rows stopped locally at `ToolContextExceededPreflight`
after tool context grew. Those 45 base cases were rerun alone with a 4,096-token
input cap, preserving the same cases, model, decoding, tools, and four-round
limit. All 45 retries succeeded. Results are joined by case ID and case SHA-256;
the retry has its own run ID, so its pair IDs differ from the original SFT run.

This is a complete diagnostic comparison across the 120 prompts, with an
execution-cap difference on the 45 retried base cases. It does not establish
clinical quality, safety, or promotion readiness. The deterministic synthetic
state checks are diagnostic only.

| Arm | Successful cases | Non-empty visible responses | Tool rounds | Completion calls | `finish_reason=length` |
| --- | ---: | ---: | ---: | ---: | ---: |
| Base Qwen3.6-35B-A3B | 120/120 | 116/120 | 130 | 250 | 5 |
| W&B v55 SFT | 120/120 | 120/120 | 0 | 120 | 7 |

Across applicable synthetic state checks, base passed tool-status checks 68/75,
response-contains checks 69/75, memory-value checks 3/15, state-value checks
45/60, and response-omission checks 0/15. v55 passed tool-status checks 0/75,
response-contains checks 13/75, memory-value checks 0/15, state-value checks
45/60, and response-omission checks 15/15. These sparse deterministic checks
cover fictional state fixtures only. In particular, v55 made no tool calls on
this checkpoint and suite; that is a substantial agent-tool behavior failure
for this diagnostic set, even though every response had visible content.

The 45-row retry manifest is `complete` with estimated usage cost
`$0.04059175`. The original 240-row paired manifest remains `incomplete`
because it faithfully records the 45 baseline preflight failures; it estimates
`$0.06624875` for its successful calls. Combined estimated usage is
`$0.10684050`; provider billing was not returned (`actual_billed_usd` is null),
so this is not a billing statement. The retry JSONL contains 45 initial
credentialless failures followed by 45 successful resumed records; aggregation
uses the latest record per case. No credential or response body was written to
the report.

## Reproduction evidence

- Suite: `docs/training/agent-tool-sft-2026-10-19/evaluation/prompt-disjoint-heldout-test-cases.jsonl`, 120 cases, SHA-256 `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`.
- Main run: `wandb-v4-v55-prompt-disjoint-toolrounds4-heldout120-paired-nonthinking-20261020T0900Z`; original results SHA-256 `90f6eba2e14324eccdcaf3c205fe9ee983e4bf33c2210262868404c4dd44be06`.
- Baseline retry run: `wandb-v4-v55-prompt-disjoint-base-context-retry45-nonthinking-20261020T`; subset SHA-256 `141c49ebc22f5d4a77449993ad2f9c664b650f61d2dba51c338b61959e9c284b`; final results SHA-256 `2de226ceb02eeaab5209db9784a603baa239b7459a825c8048a548ea5b0b5de6`.
- Main and retry outputs are under `ai/training/output/wandb_live_checkpoint_eval_20261020/v55-prompt-disjoint-heldout120-paired-nonthinking/`. The directories are private (mode `0700`) and the output files are mode `0600`.
- Training job `24cc2d06-3ec3-4356-ad3a-179694dd86a7` remains `RUNNING`; the latest event poll at 09:09:50 UTC reported step 29,196/85,631, loss 0.9062, and 995.9 throughput tokens/s. Adapter v56 and its v56 train-state mirror were present locally; all 11 files listed by the train-state manifest passed size and SHA-256 checks.

## Interpretation

The check suite shows that v55 currently does not execute the provided tools
under the provider's default reasoning configuration. Its 120 visible responses do
not offset the zero tool rounds. Continue to treat v55 as an experimental
intermediate checkpoint while the full-corpus W&B training job runs. Re-evaluate
later checkpoints with the same frozen suite and decoding settings, and keep
the base context cap explicit when comparing results.

W&B's current [Training Pricing page](https://site.wandb.ai/pricing/training/)
still labels training as public preview and says training is free during that
period; inference and model storage are separate pricing components. The
preview wording in the handoff is current provider wording, not stale status.
