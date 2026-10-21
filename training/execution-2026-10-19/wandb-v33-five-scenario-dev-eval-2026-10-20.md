# W&B v33 five-case paired evaluation — 2026-10-20

Compared W&B adapter v33 (17,000 completed batches) with the
Qwen/Qwen3.6-35B-A3B base twice on the frozen five-case `synthetic_capability_v1`
development suite used for v19-v32. Each paired evaluation allowed two local
mock-tool rounds; all 20 calls succeeded. The two result aggregates matched.
Estimated combined usage was `$0.0097935` under the `$0.06` per-run hard cap;
actual billing is unverified.

V33 returned nonempty user-facing content in 4/5 cases, with three distinct
normalized responses. It made no local tool rounds and passed 2/7 deterministic
checks (state-value and response-omission), matching the prior SFT checkpoint
pattern on tool use and checks. The base returned nonempty content in 3/5
cases, made four local rounds, and passed 3/7 checks. This small synthetic
diagnostic does not establish quality or safety and does not support promotion.

Reproduction:

- Runs: `wandb-v4-v33-five-scenario-dev-inference-20261020T0517Z` and
  `wandb-v4-v33-five-scenario-dev-inference-20261020T0518Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256 values: `60f62e49d12552fefcd6284b8869f97e37d05f6c9a2cb431662fd9fd4fde0168` (05:17Z),
  `857fc7c766d58cae22617c5ea3f618860e6b44476e3960bc57bbf0b3adf91f78` (05:18Z)
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v33`
- Private results/manifests: `ai/training/output/wandb_live_checkpoint_eval_20261020/v33-five-scenario-dev-{autowatch,0518}/results/`

The 05:17Z directory's manifest is complete with 10 successful calls. Its
stderr also contains a later resume attempt rejected because the result
directory identity had changed; that did not alter the complete manifest or
results. The separate 05:18Z run completed cleanly and reproduced the same
aggregates.
