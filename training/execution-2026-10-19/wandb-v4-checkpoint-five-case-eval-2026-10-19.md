# W&B v4 checkpoint five-case paired evaluation — 2026-10-19

The v4 W&B checkpoint at artifact version `v4` (2,500 completed batches) was
compared with its `Qwen/Qwen3.6-35B-A3B` base on the five synthetic development
cases in `scenario-dev-v1.jsonl` (SHA-256
`9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`). The
adapter was served through W&B Serverless Inference using the versioned
`wandb-artifact:///` URI. The paired evaluation used temperature 0, a 1,024
output-token cap, and up to two local mock-tool rounds. Four cases ran with a
1,024 input-token cap. The fictional research/citations case needed 2,048 input
tokens because the base arm's tool-augmented context exceeded the narrower
cap; both arms for that case were rerun together at 2,048.

All five cases now have one successful base result and one successful SFT
result. No model arm invoked external tools; any tool calls were confined to
the evaluator's synthetic in-memory fixtures. Two base results ended at the
1,024 output-token cap, so their textual behavior is truncated and should not
be treated as complete. The SFT arm finished all five cases without hitting
that output cap. Both arms still failed to make tool calls on several
tool-oriented cases. Seven deterministic state assertions per arm passed 3/7
for base and 4/7 for SFT; these assertions are explicitly marked
`deterministic_synthetic_state_unvalidated_for_quality_or_safety`. This small
diagnostic does not establish a model preference, clinical quality, or safety.

The selected paired results use estimated token costs of $0.00431375 for base
and $0.00066575 for SFT, $0.00497950 combined. Across the abandoned first
endpoint attempt, the minimal routing probe, and the corrected paired run plus
the wider-context case retry, total estimated usage is $0.006407. These are
usage-based estimates; W&B returned no actual billed amount. The configured
hard caps were $0.05 for the first paired attempt and $0.0487 for the corrected
paired run, with the narrower research-case replay capped at $0.012. Run IDs
are `wandb-v4-checkpoint-2500-vs-base-five-scenario-dev-20261019T2354Z` (the
first, incomplete route attempt),
`wandb-v4-checkpoint-2500-vs-base-five-scenario-dev-inference-20261019T2356Z`
(four paired cases plus the context-limited attempt), and
`wandb-v4-checkpoint-2500-vs-base-research-case-2048-20261019T2357Z` (the
complete fifth pair).

The first SFT request to `api.training.wandb.ai` returned HTTP 403 (`1010`)
without usage metadata. W&B's documented Inference route accepted the same
versioned artifact URI; after that minimal 15-input/7-output-token probe, the
full paired evaluations completed through `api.inference.wandb.ai`. The
research-case replay resolved a harness input-context limit, not a provider
failure.

Private outputs and manifests are kept under
`ai/training/output/wandb_live_checkpoint_eval_20261019/` with restrictive
permissions. The paired config and W&B result manifests pin the exact artifact
URI, case/config hashes, token counts, and cost estimates; raw outputs are not
included in this report.
