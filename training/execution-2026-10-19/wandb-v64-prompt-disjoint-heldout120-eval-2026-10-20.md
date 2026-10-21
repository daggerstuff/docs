# W&B v64 prompt-disjoint 120-case paired evaluation — 2026-10-20

## Result

After combining the paired run with its separate base-only context retry, both
arms have one successful visible response for each of the same 120
prompt-disjoint synthetic cases. Base completed 132 tool rounds across 252
completion calls, with 71/75 tool-status checks and 75/75 response-content
checks passed. W&B SFT v64 made no tool calls across 120 completion calls and
passed 0/75 tool-status checks and 0/75 response-content checks. Both arms
passed 45/60 state-value checks; base passed 3/15 memory-value checks while
v64 passed 0/15; v64 passed 15/15 response-omission checks while base passed
0/15. These are deterministic synthetic checks and are not validated clinical
quality or safety measures.

Seventy-seven of 120 v64 outputs ended at the 512-token cap. Its median
latency was 5.75 s, versus 1.15 s for the base arm in the paired run (the
separate 45-case retry had 1.90 s median latency). The result is a clear
agent-tool task mismatch for this full-corpus SFT checkpoint. It is consistent
with the structural audit showing no tool calls or tool results in the v4
training payload; that alignment is a plausible explanation, not proof of a
single cause.

## Run and cost accounting

- Frozen suite: `docs/training/agent-tool-sft-2026-10-19/evaluation/prompt-disjoint-heldout-test-cases.jsonl`
- Cases SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Main run ID: `wandb-v4-v64-prompt-disjoint-toolrounds4-heldout120-paired-nonthinking-20261020T1022Z`
- Main run: 2,048-token input preflight; 512-token completion cap; up to four
  tool rounds; explicit `enable_thinking=false`; base plus v64.
- Main results: 120/120 SFT successes; 75/120 base successes; the other 45
  base cases stopped locally at `ToolContextExceededPreflight`. Main manifest
  remains `incomplete` to preserve those first-attempt errors.
- Main results SHA-256:
  `bd592ac442f020750178b6024208b7505f007b31e4496ced02268628247a18eb`;
  config file SHA-256:
  `6b3dc0071168b3475c8c5068975d0235bdecece05f50ea1242d370216729a72b`;
  canonical config digest in the evaluator manifest:
  `89f66bb6df0b79dec841860109848e6fb9fc13c09eff40e9a71ebb0592198dc5`.
- Base retry ID: `wandb-v4-v64-prompt-disjoint-toolrounds4-heldout120-paired-nonthinking-20261020T1022Z-base-context-retry45`.
  It reran the 45 exact failed base cases with a 4,096-token input cap and a
  separate $0.40 hard ceiling; all 45 succeeded. Its calculated worst-case
  cap is $0.3744.
- Retry results SHA-256:
  `0042c5c72fc97b1b63a59d724112aae47521acf7a73132afcaebc64794b4a66d`;
  retry subset SHA-256:
  `7594598b2b72562bb69afe1fc03d87dc02277b990dd2472b14d64db955bdca45`.
- Estimated usage across main and retry was $0.12545625; actual billed cost
  was not returned. Main and retry worst-case estimates were $1.3824 and
  $0.3744 under their $1.50 and $0.40 configured ceilings.
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v64`.
- Private configs/results:
  `ai/training/output/wandb_live_checkpoint_eval_20261020/v64-prompt-disjoint-heldout120-paired-no-thinking/`
  (directories mode `0700`, files mode `0600`). The report excludes response
  text.

Base and v64 main-run results are joined with the retry by case ID and case
SHA-256. The first-attempt manifest is retained as incomplete; the retry has
its own complete manifest. No raw clinical dataset rows were used in this
evaluation.
