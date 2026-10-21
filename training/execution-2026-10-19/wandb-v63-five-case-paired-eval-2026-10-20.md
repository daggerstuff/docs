# W&B v63 five-case paired evaluation — 2026-10-20

Compared the full-corpus v4 adapter v63 (32,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case synthetic development suite.
Both arms used temperature 0, thinking disabled, a 1,024-token response cap,
and up to two tool rounds. The initial paired pass completed all five SFT
cases and four base cases. The base citations case hit the evaluator's
2,048-token cumulative context preflight after two tool rounds; it was retried
base-only at a 4,096-token preflight under a separate $0.012 hard cap. Both
arms therefore have five successful results for the same five cases.

| Measure | Base | v63 SFT |
| --- | ---: | ---: |
| Successful cases | 5/5 (including base-only retry) | 5/5 |
| Non-empty visible responses | 5/5 | 5/5 |
| Evaluator-local tool rounds | 4 | 0 |
| Deterministic synthetic checks | 3/7 | 2/7 |
| Estimated inference cost | $0.001923 | $0.000708 |

Combined estimated usage was **$0.00213775**, within the main pass's `$0.06`
and retry's `$0.012` caps. Actual billing was not returned. Checks are
unvalidated synthetic diagnostics, not measures of clinical quality, safety,
or production readiness. V63 returned visible content with thinking disabled,
but did not learn the benchmark's tool behavior and did not improve the
synthetic check count over base. This is consistent with the v4 training
payload's zero supervised tool-call/result messages; it does not establish
the only cause.

The first pass's evaluator manifest remains `incomplete` because of its
base-only context-preflight error. The successful retry is stored separately
and included above; the original error record is preserved.

Reproduction and integrity:

- Cases: `docs/training/execution-2026-10-17/scenario-dev-v1.jsonl`, SHA-256
  `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`.
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v63`.
- Adapter local backup: `ai/training/output/wandb_local_checkpoints_20261019/v4/v63/`, 117,843,308 bytes; both adapter files matched their mirror manifest.
- Main config SHA-256: `48eed0a4789bf3eb719f3be41d2010df1b6c2899427e5163593975ccd2bd99cb`; evaluator manifest config digest `caa9e05153b5eda9aa3f28b36d3cddd738104cfc61fd25dc0e9b0c67b49539c4`; result JSONL SHA-256 `d593edd2ccbb10cc9183ea8b1efc0f17bc58ea2c294297e086a757ee1a077ffe`.
- Base retry case SHA-256 `c00c3dc10572b54958def9bd40082eebbf4f8bc1070271c3541574b337e367b6`; result JSONL SHA-256 `6e6154a7b82e1d00c088e8f90b95259a719784894f23bc20b1591729db6aba76`.
- Private configs and results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v63-five-case-paired-no-thinking/` (directories mode `0700`, files mode `0600`). No response text is reproduced here.
