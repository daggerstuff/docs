# W&B v13 checkpoint paired held-out evaluation — 2026-10-20

## Outcome

Compared the W&B full-corpus SFT job's v13 adapter (7,000 completed batches)
with its Qwen/Qwen3.6-35B-A3B base on the same 120 held-out synthetic agent
tool cases. The paired run completed all 240 calls successfully with no
inference errors. It stayed under the configured $1.50 hard cost cap; usage-
based cost estimate was $0.1100685, while actual billing remains unavailable.

The adapter is not suitable for the current agent-tool objective. It issued no
tool calls in any of 120 cases. The base issued tool calls in 86 cases, across
136 tool rounds. The base passed 69/75 tool-status checks, while the adapter
passed 0/75; the base passed 56/75 response-content checks, while the adapter
passed 0/75. Both passed all 15 response-omission checks. State-value checks
were 46/60 for base and 45/60 for adapter; memory-value checks were 6/15 and
0/15 respectively. These are deterministic synthetic evaluator checks, not
validated measures of clinical quality, safety, or real-world utility.

The base hit its 512-token completion cap in 33 cases; the adapter hit it in
none. Median/p95 latency was 4,214/7,656 ms for base and 511/862 ms for the
adapter. Provider-reported token totals were 174,948 for base and 48,798 for
adapter. The lower adapter latency and token use do not offset the complete
loss of model-issued tool calls on this task suite.

## Reproduction and limits

- Run: `wandb-v4-checkpoint-7000-vs-base-heldout120-20261020T0140Z`
- Pairing: same 120 cases, deterministic temperature 0, 512-token output cap,
  2,048-token input preflight cap, at most four tool rounds, sealed cases off.
- Case SHA-256: `adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`
- Adapter endpoint: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v13`
- Estimated maximum before launch: $1.3824; actual bill is unknown.
- Full local results and manifest are in
  `ai/training/output/wandb_live_checkpoint_eval_20261020/v13-heldout120/results/`.

Do not promote this checkpoint for agent-tool use. Preserve it as a negative
full-corpus SFT comparison and continue evaluating the dedicated tool-SFT
release against the base. The base is also imperfect: it failed 6 tool-status
checks, hit the output cap 33 times, and did not satisfy all response-content
checks. This report does not claim an overall model winner beyond the measured
synthetic suite.
