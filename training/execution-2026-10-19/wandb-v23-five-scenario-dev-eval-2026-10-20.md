# W&B v23 five-scenario paired diagnostics — 2026-10-20

Ran the five-case frozen `synthetic_capability_v1` development suite twice
against adapter v23 / 12,000 batches and the same Qwen/Qwen3.6-35B-A3B base.
Both comparisons allowed up to two evaluator-local mock-tool rounds, used a
2,048-token input preflight, and stayed under the `$0.06` hard cap. All 20 arm
calls succeeded. Estimated usage was `$0.00468175` and `$0.004773`; actual
billing remains unknown.

| Paired run | Base nonempty | Base tool rounds/calls | Base checks | v23 nonempty | v23 distinct nonempty | v23 tool rounds | v23 checks |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Auto watcher | 3/5 | 4/5 | 3/7 | 2/5 | 2 | 0 | 2/7 |
| Independent repeat | 3/5 | 4/5 | 3/7 | 3/5 | 3 | 0 | 2/7 |

The v23 completion rate changed between repeats, but it still made no tool
rounds and passed only the same two deterministic state checks (state-value
and response-omission); it failed the positive tool-status check. The base
made four local rounds with five mock calls, and its checks were unchanged.
This variation shows the small suite is not a reliable quality estimate. It
does not support promotion or safety claims.

Both runs used case-set SHA-256
`9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`.
The auto-watcher run ID is
`wandb-v4-v23-five-scenario-dev-inference-20261020T034305Z` (config SHA-256
`78d56b8666bb1f09b4747135d1cbef839ab8ec0040e933c3db66bc4530af0722`). The
independent repeat ID is
`wandb-v4-v23-five-scenario-dev-inference-20261020T0342Z` (config SHA-256
`ee7fb87591c439889ae7de4c6b95504e63ab21ac3199bdc32665e3e6155cc018`).
Private configs and results are under
`ai/training/output/wandb_live_checkpoint_eval_20261020/v23-five-scenario-dev*/`.
