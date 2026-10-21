# Latest full-corpus checkpoint held-out evaluation — 2026-10-19

The same frozen 120-case agent-tool suite (SHA-256 `adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`) was run against the base model and the latest locally preserved W&B checkpoint from each active training job: v1 LoRA v116 / 58,500 batches and v2 LoRA v114 / 57,500 batches. Decoding was deterministic (temperature 0, 512-token output cap); tool-round cap was 2; 2,048-token input cap. Each comparison attempted all 120 cases. The evaluator set its manifest to `incomplete` because it counts any provider/tool-round errors as incomplete, despite recording every case.

| Checkpoint | Arm | Cases | Successful responses | Errors | Unique response bodies | Tool calls | Tool rounds | Tokens used | p50 latency (ms) | Estimated cost |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wandb-full-corpus-latest-v1-v116 | base | 120 | 112 | 8 | 79 | 0 | 137 | 158329 | 4443 | $0.095042 |
| wandb-full-corpus-latest-v1-v116 | sft | 120 | 120 | 0 | 1 | 0 | 0 | 47784 | 431 | $0.012306 |
| wandb-full-corpus-latest-v2-v114 | base | 120 | 112 | 8 | 78 | 0 | 130 | 153675 | 4344 | $0.092888 |
| wandb-full-corpus-latest-v2-v114 | sft | 120 | 120 | 0 | 1 | 0 | 0 | 47784 | 453 | $0.012306 |

## Result

Both SFT endpoints returned exactly one unique 3-character response across all 120 distinct cases. The per-case SFT response hashes were identical across v1 v116 and v2 v114. Neither SFT arm issued a tool call or entered a tool round. Although each returned HTTP-success responses for all cases, this is a degenerate output and fails the intended agent behavior; these checkpoints are not usable for the target task. This is also why HTTP success alone must not be reported as model success.

The two base arms produced 79 and 78 unique response bodies and 0 explicit tool calls. Each had 112 successful completions and 8 `ToolRoundLimitExceeded` errors, all on `resource_compare` cases. A follow-up reran those eight pairs at a four-round cap; all 16 calls succeeded, but neither arm made an explicit tool call. Each SFT checkpoint again returned one identical response body across all eight cases (24 completion tokens per checkpoint), confirming that the collapse is not explained by the two-round cap. The base arm returned eight unique bodies per checkpoint. Retry manifests and per-case records are in [v1](wandb-full-corpus-v1-v116-resource-compare-retry-8-rounds4-20261019T1840Z/manifest.json) and [v2](wandb-full-corpus-v2-v114-resource-compare-retry-8-rounds4-20261019T1840Z/manifest.json). These are diagnostic checks, not validated quality scores.

The evaluator's deterministic synthetic-state checks are unvalidated quality/safety diagnostics. In aggregate, SFT passed 45/60 `state_value` checks and all 15 `response_omits` checks, while failing all `tool_status`, `response_contains`, and `memory_value` checks represented in this suite. These checks are not a clinical assessment.

Estimated inference cost was `$0.10073925` for v1 and `$0.09822975` for v2. Provider-reported actual billing was unavailable (`actual_billed_usd` is null), so these figures are estimates, not confirmed credit consumption. Result manifests: [v1](wandb-full-corpus-latest-v1-v116-agent-tool-heldout-120-20261019T1826Z/manifest.json) and [v2](wandb-full-corpus-latest-v2-v114-agent-tool-heldout-120-20261019T1826Z/manifest.json). Detailed per-case outputs remain in the corresponding JSONL files.

## Newest checkpoint refresh — 2026-10-19 18:51 UTC

After the retry completed, the latest locally mirrored adapters were tested on
the same eight `resource_compare` cases at a four-round cap: v1 v118 (59,500
batches) and v2 v117 (59,000 batches), each paired with the base model. All 16
calls per comparison succeeded. Each SFT arm again returned one identical
response body across its eight cases, used 24 completion tokens, and made no
tool calls. The base arms had eight unique responses and made no explicit
tool calls. Usage-based estimated costs were $0.01018825 for v1 and $0.01030925
for v2; actual billing remains unavailable. This reconfirms that the collapse
persists in later checkpoints. Manifests: [v1 v118](wandb-full-corpus-v1-v118-resource-compare-latest-refresh-20261019T1851Z/manifest.json)
and [v2 v117](wandb-full-corpus-v2-v117-resource-compare-latest-refresh-20261019T1851Z/manifest.json).

The next v1 checkpoint, v119 / 60,000 batches, was also tested on the same
eight cases at a four-round cap. All 16 paired calls succeeded; SFT again
returned one identical body across its eight cases, with 24 completion tokens
and no tool calls. Base returned eight unique bodies and no explicit tool
calls. Estimated usage cost was $0.0098905; actual billing was not exposed.
This newest refresh confirms the degenerate SFT behavior persists as training
continues. See the [v1 v119 manifest](wandb-full-corpus-v1-v119-resource-compare-latest-refresh-20261019T1853Z/manifest.json).
