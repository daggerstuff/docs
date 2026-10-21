# W&B v67 prompt-disjoint 120-case evaluation — 2026-10-20

The v67 adapter was evaluated on all 120 cases from the frozen, prompt-disjoint
synthetic agent-tool suite. All 120 requests returned successfully. It made
zero tool calls, passed 0/75 tool-status checks and 0/75 response-content
checks, passed 0/15 memory-value checks and 45/60 state-value checks, and
passed 15/15 response-omission checks. Two of 120 responses reached the
512-token output cap. These deterministic checks are synthetic diagnostics,
not validated clinical-quality or safety measures.

The base reference completed the same 120 cases in the prior v64 paired run
and its 45-case context retry, joined here by case ID and case SHA-256. It made
132 tool rounds across 252 completion calls, passed 71/75 tool-status and
75/75 response-content checks, passed 3/15 memory-value, 45/60 state-value,
and 0/15 response-omission checks. The base results were captured separately
from v67, so their latency is not a same-window comparison. The v64 adapter
also made zero tool calls and had the same deterministic metric counts as v67,
but 77/120 v64 outputs reached the token cap. Thus the later checkpoint is
more concise on this suite, with no measured recovery of agent-tool behavior.

The result agrees with the structural audit of the v4 training payload, which
found no assistant tool-call or tool-result supervision. That is a plausible
explanation for the missing tool behavior, not proof that it is the only cause.
This run does not invalidate the ongoing dialogue SFT job; it establishes that
the job is not sufficient evidence for the intended tool-using agent task.

## Run and artifact accounting

- Run ID: `wandb-v4-v67-prompt-disjoint-toolrounds4-heldout120-sft-nonthinking-20261020T1046Z`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v67`
- Completed training batches: 34,000
- Adapter weights SHA-256: `cf8ff2360d99637cbbd46bfdad8a59ec3d9f2f177abc206a4dace0ac432eee4b`
- Frozen suite SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Canonical config SHA-256: `74ee171c38069351c50780ee150d484a4db7b3c60d977addf214ae1edea2bd1a`
- Config file SHA-256: `82393903c912d825cf1f6e968bdea011d2c01613b0231452106d9d47fba169f4`
- Results SHA-256: `9983b398208f519a30dcf5fd166f2be7cb34d42999b7e4785dc3aed8f95c9329`
- Estimated inference usage: `$0.01400225`; configured hard ceiling: `$0.75`; calculated worst case: `$0.6912`. Actual billed usage was not returned.
- v67 median latency: 322 ms, p95 1,223 ms. v64 median was 5,792 ms; latency differences are observational and may reflect endpoint serving conditions.
- Private config/results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v67-prompt-disjoint-heldout120-sft-only/`, directory mode `0700`, files mode `0600`.

No raw training examples or generated response text are included here. The
base comparison used the complete 120-case join from the previous paired run
and its retry; all case IDs and case hashes matched. See the [v64 paired
report](wandb-v64-prompt-disjoint-heldout120-eval-2026-10-20.md) and the
[v4 training-signal audit](wandb-v4-training-signal-audit-2026-10-20.md).
