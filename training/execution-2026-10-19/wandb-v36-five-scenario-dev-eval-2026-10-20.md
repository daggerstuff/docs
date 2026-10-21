# W&B v36 five-case paired evaluation — 2026-10-20

Compared W&B v4 adapter v36 (18,500 completed batches) with the
Qwen/Qwen3.6-35B-A3B base on the frozen five-case `synthetic_capability_v1`
development suite. All 10 calls succeeded. Estimated usage was `$0.004733`
against a `$0.05376` upper-bound cap; actual billing is unverified.

V36 returned nonempty content in 2/5 cases (one distinct normalized response),
made zero local tool rounds, and passed 2/7 deterministic synthetic checks.
The base returned nonempty content in 3/5 cases, made four local tool rounds,
and passed 3/7 checks. The result continues the v33-v35 pattern: this adapter
does not show the tested tool-use behavior. This small unvalidated synthetic
diagnostic does not support promotion.

Reproduction:

- Run: `wandb-v4-v36-five-scenario-dev-inference-20261020T054740Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `2974940ffe2ae15d2de31331c418563c1a96c64adcefa84fe22ef6b571292c84`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v36`
- Local adapter SHA-256: `db7cd132ac87c3e0ca2842de1af032c7ee16dedc00b4ae059bedeebfa6f31002`
- Local train-state v36 also backed up; all 11 train-state and 2 adapter files reverified against their manifest hashes.
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v36-five-scenario-dev-autowatch/results/`

See the broader [v19-v37 trend](wandb-v19-v37-five-scenario-dev-evals-2026-10-20.md) and [v33/v34 prompt-disjoint held-out comparisons](wandb-v33-prompt-disjoint-heldout120-eval-2026-10-20.md).
