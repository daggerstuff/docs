# W&B v55 five-case checkpoint diagnostic — 2026-10-20

Evaluated the SFT-only v55 adapter (28,000 completed batches) on the same
frozen five-case synthetic development suite used for v53 and v54. All five
requests succeeded, but v55 returned no visible response content, made zero
evaluator-local tool rounds, and passed 2/7 unvalidated deterministic checks.
Two completions reached the 1,024-token limit. The v53 sentinel returned
visible content on 3/5 cases with the same tool/check counts; v54 returned
visible content on 0/5. V55 therefore did not recover from the v54 empty-output
regression and is not promotable for agent-tool use.

Do not spend on a 120-case v55 evaluation unless a later checkpoint first
recovers visible responses and improves tool/check behavior on this same
bounded sentinel. The synthetic checks are not validated quality, clinical,
or safety measures.

Estimated inference usage was `$0.00307425`; the configured worst-case
preflight was `$0.02688`. Actual billing is unavailable.

Reproduction and integrity:

- Run ID: `wandb-v4-v55-five-scenario-dev-sft-20261020T0851Z`
- Cases SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `ef9b85f93b45b453b75f8036aa1c453622612cd67ced36c9ca8a64d7e603ac46`
- Result-manifest SHA-256: `567f10efa694e26ec37cff50f1bd3dc172121b94ee12a1050f0f566eca0f356`
- Result rows SHA-256: `2b20484cbe71a33e35fe40541aa0e8d9b3d73f664b2c3f3023d8db6d95ad60c7`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v55`
- Private config/results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v55-five-scenario-dev-sft-only/` (directory mode 0700; files mode 0600).

The v55 adapter and corresponding train-state were mirrored locally at 28,000
batches; all 2 adapter files and 11 train-state files match their manifest
hashes and sizes. The full-corpus training run remains active. See the
[v53](wandb-v53-five-scenario-dev-eval-2026-10-20.md) and
[v54](wandb-v54-five-scenario-dev-eval-2026-10-20.md) sentinel reports.
