# W&B v13 checkpoint five-case paired evaluation — 2026-10-20

The active W&B full-corpus job's v13 adapter (7,000 completed batches) was
compared with the Qwen3.6-35B-A3B base on the same five synthetic development
cases used for prior checkpoint checks. The versioned adapter was served by
W&B Serverless Inference. Decoding used temperature 0, a 1,024-token output
cap, up to two local mock-tool rounds, and a 2,048-token input preflight cap.
All ten paired inference calls succeeded; no external tools were used.

The base passed 3 of 7 deterministic state checks; v13 passed 2 of 7. The
base used the evaluator's local fixtures on four rounds and v13 made no tool
calls. Two base responses hit the output cap; no v13 response did. This small
diagnostic does not establish a model preference, clinical quality, or safety.
It is consistent with the completed v11 120-case result, where SFT made no
tool calls and scored below the base model. Do not promote this adapter for
agent-tool use.

Estimated inference usage was $0.0047705 combined ($0.00434125 base and
$0.00042925 v13). The hard preflight maximum was $0.05376; actual billed usage
was unavailable. The run manifest records 5,977 provider-reported tokens for
the base and 1,441 for v13. The exact case SHA-256 is
`9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`.

The private configuration, outputs, and manifest are under
`ai/training/output/wandb_live_checkpoint_eval_20261020/v13-five-case/` with
mode 0700 on the directory and 0600 on files. The completed manifest is
`retry-env/results/manifest.json`.
