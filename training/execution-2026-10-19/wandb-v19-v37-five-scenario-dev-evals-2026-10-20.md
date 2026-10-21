# W&B v19–v37 five-scenario paired checks — 2026-10-20

Ran each adapter checkpoint against the same Qwen/Qwen3.6-35B-A3B base on the
five-case frozen `synthetic_capability_v1` development suite. Each comparison
enabled two evaluator-local mock-tool rounds, 2,048-token input preflight, and
a `$0.06` hard cap. Twenty-one comparisons (v19-v22, two v23 runs, v24-v32,
two v33 runs, and v34-v37) completed all 210 calls. Estimated five-case
inference usage was `$0.10123675`; actual billing is unknown.

| Checkpoint | Nonempty SFT responses | Distinct nonempty SFT responses | SFT local tool rounds | Estimated paired usage |
| --- | ---: | ---: | ---: | ---: |
| v19 / 10,000 batches | 1/5 | 1 | 0 | `$0.00464175` |
| v20 / 10,500 batches | 0/5 | 0 | 0 | `$0.004713` |
| v21 / 11,000 batches | 5/5 | 4 | 0 | `$0.00467175` |
| v22 / 11,500 batches | 3/5 | 2 | 0 | `$0.00465925` |
| v23 / 12,000 batches, auto watcher | 2/5 | 2 | 0 | `$0.00468175` |
| v23 / 12,000 batches, independent repeat | 3/5 | 3 | 0 | `$0.004773` |
| v24 / 12,500 batches | 4/5 | 3 | 0 | `$0.00477675` |
| v25 / 13,000 batches | 5/5 | 4 | 0 | `$0.004738` |
| v26 / 13,500 batches | 5/5 | 5 | 0 | `$0.00471925` |
| v27 / 14,000 batches | 5/5 | 4 | 0 | `$0.0047455` |
| v28 / 14,500 batches | 5/5 | 4 | 0 | `$0.0059705` |
| v29 / 15,000 batches | 5/5 | 4 | 0 | `$0.004893` |
| v30 / 15,500 batches | 5/5 | 4 | 0 | `$0.0047105` |
| v31 / 16,000 batches | 0/5 | 0 | 0 | `$0.00476925` |
| v32 / 16,500 batches | 0/5 | 0 | 0 | `$0.00482675` |
| v33 / 17,000 batches, two matching repeats | 4/5 | 3 | 0 | `$0.0097935` combined |
| v34 / 17,500 batches | 5/5 | 5 | 0 | `$0.004683` |
| v35 / 18,000 batches | 1/5 | 1 | 0 | `$0.0049705` |
| v36 / 18,500 batches | 2/5 | 1 | 0 | `$0.004733` |
| v37 / 19,000 batches | 5/5 | 5 | 0 | `$0.00476675` |

The base returned nonempty content in three cases and made four local rounds
containing five mock-tool calls in each comparison. It passed 3/7 deterministic
checks; every SFT run passed 2/7. Both arms passed the same state-value and
response-omission checks; the base also passed the one positive tool-status
check. No SFT checkpoint made tool calls on this suite. V23's nonempty response
count changed from 2/5 to 3/5 across the two repeats, while its checks and zero
tool-round result stayed unchanged. V24 returned nonempty content in 4/5
cases but again made no local tool rounds and passed only the two checks also
passed by prior SFT checkpoints. V25-v28 returned nonempty content in 5/5 cases, but made no local tool
rounds and passed only those same two checks. V21's 5/5 response
coverage did not persist in v22-v24; the matching later counts do not establish
a trend. The small suite and inconsistent behavior do not establish quality
or safety. No checkpoint passes the positive tool task; do not promote from
this evidence. V34's 5/5 response coverage came with only 54 completion tokens
total, zero tool rounds, and 2/7 checks; its larger paired test found zero
tool-status passes. V35 returned nonempty content in 1/5 cases, again with no
tool rounds and 2/7 checks. The v34/v35 results do not change the conclusion.

These are synthetic diagnostics only, not clinical quality or safety evidence.
The case-set SHA-256 is
`9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`. Private
configs and results are under
`ai/training/output/wandb_live_checkpoint_eval_20261020/v{19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37}-five-scenario-dev*/` and the v33/v34 prompt-disjoint held-out directories.
The two v23 runs are documented in the [v23 paired-evaluation report](wandb-v23-five-scenario-dev-eval-2026-10-20.md); v24 is documented in the [v24 report](wandb-v24-five-scenario-dev-eval-2026-10-20.md); v25 is documented in the [v25 report](wandb-v25-five-scenario-dev-eval-2026-10-20.md); v26 is documented in the [v26 report](wandb-v26-five-scenario-dev-eval-2026-10-20.md); v27 is documented in the [v27 report](wandb-v27-five-scenario-dev-eval-2026-10-20.md); v28 is documented in the [v28 report](wandb-v28-five-scenario-dev-eval-2026-10-20.md); v29 is documented in the [v29 report](wandb-v29-five-scenario-dev-eval-2026-10-20.md); v30 is documented in the [v30 report](wandb-v30-five-scenario-dev-eval-2026-10-20.md); v31 is documented in the [v31 report](wandb-v31-five-scenario-dev-eval-2026-10-20.md); v32 is documented in the [v32 report](wandb-v32-five-scenario-dev-eval-2026-10-20.md); both v33 runs are documented in the [v33 report](wandb-v33-five-scenario-dev-eval-2026-10-20.md).


## V33 checkpoint update

V33 at 17,000 batches returned nonempty content in 4/5 cases with three
distinct normalized responses, but made zero tool rounds and passed only 2/7
checks. The base again returned content in 3/5 cases, made four local rounds,
and passed 3/7 checks. A second repeat matched the same aggregate. The 17
paired runs now cover 170 calls at an estimated `$0.0820835` total; actual
billing remains unknown. This is a modest text
coverage recovery after v31/v32, with no improvement to tool behavior or
assertion coverage. See the [v33 report](wandb-v33-five-scenario-dev-eval-2026-10-20.md).

## V34–v37 checkpoint update

V34 returned content in 5/5 cases but used just 54 completion tokens total,
made no tool rounds, and passed 2/7 checks. V35 returned content in 1/5,
made no tool rounds, and passed 2/7 checks. Both follow the same low-tool-use
pattern and fail the tested tool-use checks; neither qualifies for promotion.
V34-v37 each had a base arm at 3/5 nonempty, four local rounds,
and 3/7 checks. V36 returned nonempty content in 2/5 cases, and v37 in 5/5,
but v37 used only 73 completion tokens total; both returned no SFT tool rounds
and passed 2/7 checks. Across all 21 five-case comparisons, all 210 calls succeeded;
estimated total inference usage is `$0.10123675`, actual billed amount unknown.
See the [v34 report](wandb-v34-five-scenario-dev-eval-2026-10-20.md) and
[v35 report](wandb-v35-five-scenario-dev-eval-2026-10-20.md) and
[v36 report](wandb-v36-five-scenario-dev-eval-2026-10-20.md) and
[v37 report](wandb-v37-five-scenario-dev-eval-2026-10-20.md). The v33 and v34
120-case held-out reports are [here](wandb-v33-prompt-disjoint-heldout120-eval-2026-10-20.md)
and [here](wandb-v34-prompt-disjoint-heldout120-eval-2026-10-20.md).

## V38–v42 checkpoint update

All five automatic comparisons completed 50/50 calls. The base arm was stable
at 3/5 nonempty responses, four local tool rounds, and 3/7 checks for every
checkpoint. SFT made zero tool rounds and passed 2/7 checks at each version;
nonempty response count varied before recovering at v41:

| Checkpoint | Nonempty SFT responses | SFT tool rounds | SFT checks | Estimated paired usage |
| --- | ---: | ---: | ---: | ---: |
| v38 / 19,500 batches | 0/5 | 0 | 2/7 | `$0.0047155` |
| v39 / 20,000 batches | 0/5 | 0 | 2/7 | `$0.0047255` |
| v40 / 20,500 batches | 2/5 | 0 | 2/7 | `$0.0047305` |
| v41 / 21,000 batches | 4/5 | 0 | 2/7 | `$0.00474675` |
| v42 / 21,500 batches | 3/5 | 0 | 2/7 | `$0.0047555` |

Across v38–v42, estimated inference usage totals `$0.02367375`; actual
billing is unverified. The larger prompt-disjoint v41 evaluation confirms
that response availability recovered (117/120 nonempty), but the adapter made
zero tool rounds and passed only 60/240 checks against the base's 200/240.
This separates the v38/v39 empty-output regression from the continuing agent
tool-use failure. None of these checkpoints qualifies for promotion. See the
[v38](wandb-v38-five-scenario-dev-eval-2026-10-20.md),
[v39](wandb-v39-five-scenario-dev-eval-2026-10-20.md),
[v40](wandb-v40-five-scenario-dev-eval-2026-10-20.md),
[v41](wandb-v41-five-scenario-dev-eval-2026-10-20.md),
[v42](wandb-v42-five-scenario-dev-eval-2026-10-20.md), and
[v41 120-case](wandb-v41-prompt-disjoint-heldout120-eval-2026-10-20.md)
reports. The checks remain synthetic diagnostics, not validated clinical
quality or safety measures.
