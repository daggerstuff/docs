# W&B v50 five-case paired diagnostic — 2026-10-20

Compared the locally mirrored Serverless Training adapter v50 (25,500
completed batches) with its Qwen/Qwen3.6-35B-A3B base on the frozen five-case
`synthetic_capability_v1` development suite. All ten requests succeeded. This
is a small synthetic diagnostic, not a validated quality, clinical, or safety
measure.

The base produced nonempty content in 3/5 cases, made four evaluator-local tool
rounds, and passed 3/7 unvalidated deterministic checks. V50 produced no
nonempty extracted content in 5/5 cases, made zero tool rounds, and passed 2/7
checks. Two SFT calls ended at the 1,024-token limit; the other three stopped
after short completions. The base and SFT arm have no evaluator-reported request
errors.

The saved result rows contain empty extracted assistant content for every SFT
case. The runner does not retain the raw provider response object, so these
records cannot distinguish a model returning blank visible content from content
arriving in a response field the runner does not capture. Treat v50 as a failed
behavioral diagnostic and do not promote it; investigate response-channel
handling separately before drawing a checkpoint-integrity conclusion. The
synthetic checks are unvalidated for quality or safety.

Estimated usage was `$0.0073555`, below the configured `$0.06` cap (preflight
worst-case estimate `$0.05376`). Actual billing is not available in the run
response.

Reproduction details:

- Run ID: `wandb-v4-v50-five-scenario-dev-inference-20261020T0724Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config file SHA-256: `d5a915124e4487e55bb2a4f68edccca1a3087e8d8bf7d71017dddc4c9b3cc953`
- Evaluator config digest: `67f4c0e57accff23e823ba4df8f74d2a96dbfa6e39ad7dbb9bad5706b9128aea`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v50`
- Result manifest SHA-256: `e2a8aec305c4b63ae2c062d3e20f269decd24870c6c87de0dd9a4ea005424fae`
- Result rows SHA-256: `911a629944904ffbfe77ee41208a6c49635e4e09b5e019f0996ed93de4f80b4c`
- Private config and results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v50-five-scenario-dev/` (directory mode 0700; files mode 0600).

The earlier v45 diagnostic had one nonempty SFT completion, zero tool rounds,
and 2/7 checks; v50 did not improve on it. See the [v45 paired evaluation](wandb-v45-five-scenario-dev-eval-2026-10-20.md).
