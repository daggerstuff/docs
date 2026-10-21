# W&B v64 five-case paired evaluation — 2026-10-20

## Result

The v64 adapter still shows no tool-use recovery on this small synthetic
diagnostic. The base model completed all five cases after a separate retry of
the citations case: it made four tool rounds across completed responses and
passed 3 of 7 deterministic synthetic state checks. Its first citations
attempt used two tool rounds before exceeding the 2,048-token context
preflight; the 4,096-token retry completed with two more. The v64 adapter
returned visible responses on all five cases, made zero tool rounds, and
passed 2 of 7 checks. Four of its five completions ended with `length` at the
1,024-token output cap. These synthetic checks are unvalidated diagnostics,
not clinical quality or safety evidence.

The SFT endpoint was slower in this five-case sample: p50 latency was 11.65 s
versus 0.82 s for the base arm. Estimated request usage was $0.006461 for the
paired run and $0.000493 for the base-only retry. The configured worst-case
ceilings were $0.06 and $0.012 respectively. Actual billed amounts were not
available from inference responses.

## Reproducibility

- Run ID: `wandb-v4-v64-five-case-paired-no-thinking-20261020T1019Z`
- Frozen cases: `docs/training/execution-2026-10-17/scenario-dev-v1.jsonl`
- Cases SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Decoding: temperature 0, max output 1,024, `enable_thinking=false`.
- Paired run input cap: 2,048; maximum two tool rounds; five cases; base and
  W&B SFT v64.
- Paired config file SHA-256:
  `656c1cd79d9ff3cd573960dbf62886e425a80c64d2bb93d3c71735ecf405308d`;
  canonical config digest in the evaluator manifest:
  `2fe4fcb0fd993120aa0561d3dfecdec0e25a22cdaf9170cca1f89bfe4d7045e0`.
- Paired results SHA-256:
  `bbc352f6c4f08f195148f504d36c2c189688b7e27e93090d6aa61dbe70e62418`.
- Base citations retry: same frozen case, 4,096 input cap, two tool rounds,
  separate $0.012 ceiling. Retry results SHA-256:
  `c99e931e6278d16026431da8be89f5bf38f534a0ff2354a3c62601209d31a32c`.
- Adapter: W&B artifact
  `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v64`.
  Its local mirrored weights SHA-256 is
  `e6e9b8f54efec232ef3f8f278d01c08100aa62707bd25a991ed05a4981ca35c1`.
- Private config and results directory:
  `ai/training/output/wandb_live_checkpoint_eval_20261020/v64-five-case-paired-no-thinking/`
  (directories mode `0700`, files mode `0600`). No response text is included
  in this report.

An initial attempt with a 4,096-token cap was rejected by local preflight
before provider calls because its calculated worst-case cost ($0.06912)
exceeded the $0.06 ceiling. The completed paired run therefore used 2,048;
the base citations retry used its separate $0.012 ceiling.
