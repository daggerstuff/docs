# Gemma 4 serving and evaluation investigation

Date: 2026-10-20

## Findings

- The Gemma SFT training job completed (480/480 steps). Both `step0` and `step1` checkpoint artifacts remained present in W&B and had local backups when checked. The final adapter file is 61,907,664 bytes locally and remotely.
- The prior smoke tests sent the trained checkpoint to `https://api.inference.wandb.ai/v1/chat/completions`, which returned generic HTTP 500. A direct request to the same saved `:step1` checkpoint through `https://api.training.wandb.ai/v1/chat/completions` succeeded. The base model also succeeds through the Training API. W&B's [trained-model inference instructions](https://docs.wandb.ai/training/serverless-rl/use-trained-models) specify the Training API endpoint and `wandb-artifact:///...:<step>` checkpoint form. This confirms the old route was wrong for this trained artifact; it does not indicate missing artifacts or failed training.
- The only two failures in the Gemma base-only 120-case run at a four-round limit were `resource_lookup-137` and `resource_lookup-140`. Both had received four successful tool results but Gemma requested another tool call before producing a final answer. The evaluator now allows up to eight bounded tool rounds. Both cases completed on base and SFT: base used four and five rounds; SFT used four and two rounds.

## Completed validation

The prepared five-case paired smoke completed all 10 base/SFT records through the Training API route. The frozen prompt-disjoint 120-case paired run then completed **240/240 records**, with zero transport or harness errors and no 512-token truncations. It used the same 120-case SHA-256 `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`, an 8,192 input-token cap, and an 8-round limit. Estimated usage was `$0.0211802`; actual billing was not queried.

The paired synthetic diagnostics show little measured change from Gemma SFT: tool-status checks tied 75/75, expected-response checks tied 60/60, omission checks tied 15/15, and memory-value checks tied 14/15 (one SFT-only pass). For state-value checks, 53/60 tied and base alone passed seven. Median latency was 2.43 s for SFT vs 2.19 s for base; token usage was 82,670 vs 85,408. These metrics are unvalidated synthetic diagnostics, not evidence of clinical quality or production readiness; this checkpoint should not be promoted based on this run.

## Fix and evidence

- Raised the evaluator's bounded maximum tool-round limit from four to eight and added a boundary regression test.
- `uv run pytest ai/qa/validation/tests/test_paired_eval.py -q`: 25 passed.
- `uv run ruff check ai/qa/validation/therapy_bench/paired_eval.py ai/qa/validation/tests/test_paired_eval.py`: passed.
- `uv run ruff format --check ai/qa/validation/therapy_bench/paired_eval.py ai/qa/validation/tests/test_paired_eval.py`: passed.
- Full-run config: `ai/training/output/dual_model_sft_20261020/gemma4-paired-training-api-round8-config.json`.
- Full-run manifest/results: `ai/training/output/dual_model_sft_20261020/gemma4-paired-training-api-round8-results/`.
- Two-case regression run: `ai/training/output/dual_model_sft_20261020/gemma4-resource-lookup-round8-results/`.
