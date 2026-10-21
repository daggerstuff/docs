# W&B v34 five-case paired evaluation — 2026-10-20

Compared the locally backed-up W&B v4 adapter v34 (17,500 completed batches)
with the Qwen/Qwen3.6-35B-A3B base on the frozen five-case
`synthetic_capability_v1` development suite. All 10 calls succeeded. The
estimated usage was `$0.004683`; the manifest's conservative estimate cap was
`$0.05376`. Actual billing is unverified.

V34 returned nonempty content in 5/5 cases, made zero local tool rounds, and
passed 2/7 deterministic synthetic checks. The base returned nonempty content
in 3/5 cases, made four local tool rounds, and passed 3/7 checks. The SFT
responses used 54 completion tokens total across the five cases, versus 2,792
for base; response coverage alone therefore overstates usefulness. This
unvalidated synthetic diagnostic does not establish quality or safety and
does not support promotion. No clinical data was included in this suite.

Reproduction:

- Run: `wandb-v4-v34-five-scenario-dev-inference-20261020T052740Z`
- Case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Config SHA-256: `c94318fd80d09c20b6e9524da624994a164e62ab6245400610cb23f2044bf988`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v34`
- Local adapter SHA-256: `435ecd93cc99ad10123f61930977adbfc4e8ca70d79fa3bf5da39933fa999bd9`
- Private results and manifest: `ai/training/output/wandb_live_checkpoint_eval_20261020/v34-five-scenario-dev-autowatch/results/`

W&B Serverless Training and its SFT API remain documented as public preview;
this evaluation used the W&B inference endpoint for both arms. The training
job remains active. See the [live execution handoff](../TRAINING_EXECUTION_HANDOFF.md).
