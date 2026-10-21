# W&B v53 five-case checkpoint diagnostic — 2026-10-20

Compared v53's SFT arm (27,000 completed batches) on the frozen five-case synthetic development suite. This SFT-only run used the same prompts and decoding as the v51 five-case paired run; the base comparison below references that run's base arm, rather than a new base inference pass.

V53 returned visible content in 3/5 cases, made zero evaluator-local tool rounds, and passed 2/7 unvalidated deterministic checks. All five calls succeeded and stopped before the 1,024-token limit. The anchored base arm had visible content in 3/5 cases, four tool rounds, and 3/7 checks. V53 is slightly better than v51's 2/5 visible completions but does not restore any tool behavior or improve the deterministic check count. This is not a promotion result.

A separate direct synthetic PONG request to v53 returned HTTP 200 with non-null visible content (7 characters), a separate 9-character reasoning field, no tool calls, and a clean stop. This shows v53 can emit visible text for this simple prompt; it does not resolve its failure on the agent-tool suite. The raw response text was not retained.

Estimated usage was `$0.000903` for the five-case evaluation and about `$0.000014` for the direct PONG request. Actual billing is unknown. The configured five-case worst-case estimate was `$0.02688`.

Reproduction:

- Run ID: `wandb-v4-v53-five-scenario-dev-sft-20261020T0834Z`
- Cases SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Evaluator config digest: `9900665790be961aea423a011c06942fe97bfe3b21d78799412e146a7bb1f99f`
- Result-manifest SHA-256: `157af0f4f12b6f4e15ae78d8865f6d28566c9b5813dadf270085f8c6749c7212`
- Result rows SHA-256: `08b415f75ff7bcc573e119ca5b340067a3d916d1e31608c77a89f1392e386175`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v53`
- Private config/results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v53-five-scenario-dev-sft-only/` (directory mode 0700; files mode 0600).

The larger [v51 prompt-disjoint 120-case evaluation](wandb-v51-prompt-disjoint-heldout120-eval-2026-10-20.md) found substantial user-visible output and tool-behavior failure. A v53 SFT-only 120-case follow-up is running against the same fixed suite and anchored base results.
