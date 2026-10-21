# W&B v54 five-case checkpoint diagnostic — 2026-10-20

Evaluated the SFT-only v54 adapter (27,500 completed batches) on the same frozen five-case synthetic development suite used for v53. The W&B base was not queried again; the anchored reference is the base arm from the v51 paired run. All five v54 requests returned successfully and stopped before the 1,024-token cap, but all five had empty user-visible response content. V54 made zero evaluator-local tool rounds and passed 2/7 unvalidated deterministic checks, the same check count as v53. V53 returned visible content on 3/5 cases and also made zero tool rounds. The v51 base reference returned visible content on 3/5 cases, made four local tool rounds, and passed 3/7 checks.

The v54 sentinel shows no improvement over v53 and a substantial regression in visible output on this small suite. Do not spend inference on a 120-case v54 evaluation unless a later checkpoint first recovers visible responses and shows a meaningful tool/check improvement on a fresh bounded sentinel. This is a synthetic diagnostic, not a validated quality, clinical, or safety measure.

Estimated inference usage was `$0.00059425`; the configured worst-case estimate was `$0.02688`. Actual billing is unavailable.

Reproduction and integrity:

- Run ID: `wandb-v4-v54-five-scenario-dev-sft-20261020T0840Z`
- Cases SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `ff044453bc5a84616087c8464cd8d37205b08585166c5edded3e44453fbc61a7`
- Result-manifest SHA-256: `049f0adee09090044cbec79c71440157c557f2314db0e8ffa227d66b570c2df6`
- Result rows SHA-256: `ae04255afafaf57edf8867d04b4f1683d353f4be18fbb6eeec47f5010b9e9305`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v54`
- Private config/results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v54-five-scenario-dev-sft-only/` (directory mode 0700; files mode 0600).

The v54 adapter and matching resumable train-state artifacts were mirrored locally at 27,500 batches. Their 2 adapter files and 11 train-state files match the hashes and sizes in their respective manifests. The full-corpus training job remains active; this evaluation does not interrupt it. See the [v53 five-case report](wandb-v53-five-scenario-dev-eval-2026-10-20.md) and the [v51 paired five-case report](wandb-v51-five-scenario-dev-eval-2026-10-20.md) for anchored comparisons.
