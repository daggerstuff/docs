# W&B v45 five-case paired diagnostic — 2026-10-20

Compared locally mirrored Serverless Training adapter v45 (23,000 completed
batches) with the Qwen/Qwen3.6-35B-A3B base on the frozen five-case
`synthetic_capability_v1` development suite. All ten requests succeeded. This
is a small synthetic diagnostic, not a validated quality, clinical, or safety
measure.

V45 produced nonempty content on 1/5 cases, made zero tool rounds, and passed
2/7 deterministic synthetic checks. The base produced nonempty content on 3/5,
made four tool rounds, and passed 3/7 checks. V45's one nonempty answer was an
off-task Japanese greeting to the fictional book-swap request. It did not
recover the base model's tool use and is not promoted.

Estimated usage was `$0.00478175` under the configured `$0.06` hard cap; actual
billing is unverified. The synthetic checks are explicitly unvalidated for
quality or safety.

Reproduction details:

- Run ID: `wandb-v4-v45-five-scenario-dev-inference-20261020T0717Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `f5d48cfbace9e4ecfd95ee2996f5a5ce2d3ea7aabb4406298aa5f2865b788ad9`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v45`
- Result manifest SHA-256: `04c2f6e1c13c42f5ae7d6462f7e5acb671b85ce5de1c877c777c6bbe66bb9d19`
- Result rows SHA-256: `fe657da2dbd61dbd3c0e70c659d61c6f35e5add3ef9d0600b4d67c8e9b4bdd7f`
- Private config and results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v45-five-scenario-dev/` (directory mode 0700; files mode 0600).
