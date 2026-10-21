# W&B v7 checkpoint five-case paired evaluation — 2026-10-20

The active W&B v4 job's v7 adapter (`arc-sft-baseline-30e158011725-sft-resume:v7`, metadata: 4,000 completed batches) was compared with the Qwen3.6-35B-A3B base on the same five synthetic development cases as v4-v6. The adapter used W&B Serverless Inference with its versioned artifact URI. Decoding used temperature 0, a 1,024 output-token limit, and up to two local mock-tool rounds.

The v7 SFT arm returned nonempty user-facing content in four of five cases, with four distinct nonempty normalized responses; its fifth response was empty. This improves on v6, which returned empty content in all five cases, but v7 still has an empty-answer failure. The base arm had two empty responses and two outputs hit the 1,024 output-token limit. Its research/citations case also exceeded the 1,024 input cap on the first attempt; both arms were rerun for that case at 2,048 under a separate $0.012 maximum-cost cap. Seven deterministic assertions passed 3/7 for base and 2/7 for v7. These assertions are unvalidated for quality or safety; the result does not establish clinical quality or model preference.

Selected paired estimated usage was $0.00435625 for base and $0.000623 for v7, $0.00497925 combined. Including the partial first pass, estimated usage was $0.00686975. W&B did not return actual billed totals. No external tools were invoked; tools were evaluator-local fixtures. No v7 SFT output hit the 1,024 output-token limit; two base outputs did.

The private configs, outputs, and manifests are under `ai/training/output/wandb_live_checkpoint_eval_20261019/` with restrictive permissions. The v7 adapter and matching train-state are also preserved locally under `ai/training/output/wandb_local_checkpoints_20261019/`.
