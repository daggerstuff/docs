# Latest W&B checkpoints: 120-case held-out comparison

Observed 2026-10-19T18:23:46.835777Z. Cases hash: `adda06506381f140bf5cdc909c9406574fa55225e4f7cd409801cbc1d7d898d0`.

This is a synthetic deterministic agent/tool diagnostic, not a clinical quality or safety evaluation. Provider manifests expose estimated token cost, not actual billed amount.

| Arm / run | Checkpoint | Status | Successful / failed | Unique outputs | Cases with tool calls | Tool events | Estimated cost |
|---|---:|---|---:|---:|---:|---:|---:|
| base, 2-round run | base | incomplete | 111 / 9 | 82 | 88 | 137 | $0.087427 |
| base, 4-round recovery | base | complete | 9 / 0 | 9 | 9 | 27 | $0.010751 |
| base, combined coverage | base | supplemented | 120 / 0 | 91 | 88 | 146 | $0.098178 |
| v1 | v114 | complete | 120 / 0 | 1 | 0 | 0 | $0.012306 |
| v2 | v112 | complete | 120 / 0 | 1 | 0 | 0 | $0.012306 |
| v1 latest | v115 | complete | 120 / 0 | 1 | 0 | 0 | $0.012306 |
| v2 latest | v113 | complete | 120 / 0 | 1 | 0 | 0 | $0.012306 |

All four adapter runs completed 120 cases each without provider errors. Every run produced the same exact response on every case: one unique output per run, no tool calls, and 60/240 synthetic state checks passed. v1 and v2 matched on all cases; the newer v1 v115 and v2 v113 outputs exactly matched the earlier v114/v112 outputs across all cases. One additional 500-step checkpoint interval changed none of the held-out behavior. Their state checks passed 60/240 each; all tool-status and response-contains checks failed. The state checks are synthetic, unvalidated diagnostics.

At the original two-round cap, the base arm had 111 successful responses and 9 `ToolRoundLimitExceeded` errors, all in `resource_compare`. A separate four-round follow-up evaluated exactly those nine cases; all nine completed after three tool rounds. Combining the original 111 successes with those nine recoveries gives 120 successful base outputs (91 unique responses, 88 cases with tool traces, 146 tool events). Across all 120 cases, base and each adapter had zero exact output matches. The recovery used a different round cap on the nine-case subset, so report it as a supplement rather than a uniform-cap full-suite run.

The adapters were evaluated at v1 v114 (57,500 batches), v2 v112 (56,500), then the newest v1 v115 (58,000) and v2 v113 (57,000). Checkpoints are captured by the local rolling backup workers. Training was still reported `RUNNING` at the last direct job-status read; these results describe the evaluated checkpoint versions only.

The recovery run estimated $0.010751, bringing base usage to $0.098178. Four adapter runs estimated $0.012306 each. All listed evaluation runs total about $0.147402 estimated; actual billing is unknown. Per-metric counts and the original nine capped case IDs are in the paired JSON sidecar; recovery results are in `base-resource-compare-rounds-4-followup-9-20261019T1815Z/`. No raw response text is duplicated in this summary.
