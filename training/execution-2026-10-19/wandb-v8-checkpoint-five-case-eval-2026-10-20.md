# W&B v8 checkpoint five-case paired evaluation — 2026-10-20

The active W&B v4 job's v8 adapter (`arc-sft-baseline-30e158011725-sft-resume:v8`, metadata: 4,500 completed batches) was compared with the Qwen3.6-35B-A3B base on the same five synthetic development cases as v4-v7. The adapter used W&B Serverless Inference with its versioned artifact URI. Decoding used temperature 0, a 1,024 output-token limit, and up to two local mock-tool rounds.

The v8 SFT arm returned nonempty user-facing content in all five cases, with five distinct normalized responses. The base arm returned empty content in two cases and reached the 1,024-token output cap in two cases. Its research/citations case exceeded the 1,024 input cap initially; both arms were rerun for that case at 2,048 input tokens under a separate $0.012 maximum-cost cap. Seven deterministic assertions passed 3/7 for base and 2/7 for v8. These assertions are unvalidated for quality or safety; this five-case diagnostic does not establish clinical quality or a model preference.

Selected paired estimated usage was $0.004355 for base and $0.00074675 for v8, $0.00510175 combined. Including the partial first pass, estimated usage was $0.00571725. W&B did not return actual billed totals. No external tools were invoked; tools were evaluator-local fixtures. No v8 SFT output hit the output-token cap.

The private configs, outputs, and manifests are under `ai/training/output/wandb_live_checkpoint_eval_20261019/` with restrictive permissions. The v8 adapter and matching train-state are also preserved locally under `ai/training/output/wandb_local_checkpoints_20261019/`.
