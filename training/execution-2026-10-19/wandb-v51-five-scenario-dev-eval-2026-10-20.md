# W&B v51 five-case paired diagnostic — 2026-10-20

Compared W&B Serverless Training adapter v51 (26,000 completed batches) with its Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1` development suite. All ten paired requests succeeded. This small synthetic diagnostic is not a validated quality, clinical, or safety measure.

The base returned nonempty visible content on 3/5 cases, made four evaluator-local tool rounds, and passed 3/7 unvalidated deterministic checks. V51 returned nonempty visible content on 2/5 cases, made zero tool rounds, and passed 2/7 checks. Four SFT completions ended with `stop`; one ended at the 1,024-token limit. The base and SFT arm had no request errors. V51 therefore shows partial visible-output recovery over v50 (0/5), but no improvement in the check count and no tool use; this is not a promotion result.

A separate direct synthetic PONG probe returned HTTP 200 but `message.content: null`, no tool calls, and a five-character `message.reasoning` field. This confirms the v51 endpoint can still return no user-visible answer, even when the minimal instruction is simple. The probe's raw reasoning was not retained. W&B's `reasoning` field must not be treated as the final assistant response.

Estimated usage for the paired evaluation was `$0.0070655`; the configured worst-case preflight estimate was `$0.05376`, below the `$0.06` cap. Actual billed usage is unavailable. The additional PONG probe used 16 prompt tokens and 4 completion tokens; its estimated cost at the configured rates is `$0.000009`.

Reproduction details:

- Run ID: `wandb-v4-v51-five-scenario-dev-inference-20261020T0810Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `1e7e9559c10a03a0719bdeb28955849b2e0acac25c9c79f6a5a8af83127435aa`
- Manifest SHA-256: `9c6a467c4943b18014ed44ae2bbede5b51e083d4a4f241a2d2e1f4c5158a0e49`
- Results SHA-256: `92ac2a9c979212af6c32ef69f825dd4f7d990a76ed64ee7fa07e152d42ac2080`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v51`
- Private config and results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v51-five-scenario-dev/` (directories mode 0700; files mode 0600).

See the [v50 evaluation](wandb-v50-five-scenario-dev-eval-2026-10-20.md) and [v50 response-channel diagnostic](wandb-v50-response-channel-diagnostic-2026-10-20.md) for the preceding checkpoint and direct response-field comparison. The deterministic scenario checks are unvalidated and must not be represented as quality or safety scores.
