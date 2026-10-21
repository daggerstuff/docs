# W&B v53 prompt-disjoint 120-case evaluation — 2026-10-20

Evaluated only the v53 SFT arm (27,000 completed batches) on the frozen 120-case prompt-disjoint synthetic tool-use suite. Decoding, case file, 512-token completion cap, 2,048-token input preflight, and four-round evaluator-local mock-tool setup match v51/v41. To avoid another base inference pass, the base reference below is the completed v51 paired run's base arm on the identical suite; that arm has 120/120 effective successes after its recorded single-case retry. This is an anchored comparison across runs, not a same-session pair. The test suite and deterministic checks are synthetic and unvalidated for quality or clinical safety.

All 120 v53 SFT requests succeeded. The v51 base reference returned visible content on 102/120 cases, made 137 local tool rounds, and passed 198/240 checks. V53 returned visible content on 21/120, made zero tool rounds, and passed 62/240 checks. Fourteen v53 completions reached the 512-token limit. V53 gained two checks over v51's 60/240 but lost eight visible completions (21 vs 29), and still failed every tool-status check. It is not promotable for the agent-tool task.

Visible completion counts by scenario (15 cases each):

| Scenario | Base reference | v53 SFT |
| --- | ---: | ---: |
| Appointment consent gate | 15/15 | 0/15 |
| Appointment explicit consent | 15/15 | 1/15 |
| Approval gate | 6/15 | 13/15 |
| Memory consent gate | 10/15 | 0/15 |
| Memory opt-in | 12/15 | 3/15 |
| Resource comparison | 15/15 | 3/15 |
| Resource lookup | 15/15 | 0/15 |
| Untrusted note | 14/15 | 1/15 |

V53's largest visible-output gain is isolated to approval-gate prompts; most other scenarios remain near zero. The earlier five-case sentinel showed 3/5 visible answers, zero tool rounds, and 2/7 checks. A separate direct PONG probe did return non-null visible content, so response-channel behavior is prompt-dependent. Do not equate visible text with task correctness, and do not promote v53.

Estimated SFT-only inference usage was `$0.02896225`; worst-case preflight was `$0.6912` under the `$1.50` hard cap. Actual billing is unavailable.

Reproduction and integrity:

- Run ID: `wandb-v4-v53-prompt-disjoint-toolrounds4-heldout120-sft-only-20261020T0835Z`
- Case SHA-256: `890718d9da3e697ee20c7683f13303e07c85985d07b35d45417ad853f0722773`
- Evaluator config digest: `bfc1b287f932d45e8dca230ddda12396559a081d28590bc4809404ea6765502d`
- Manifest SHA-256: `56f39e8ce1d88723b63c1afb39ffd083f2d2f7c96b566ac7afebd458514cbd53`
- Results SHA-256: `42b8dd28c3e113837be3af0ec2a6832276ac694ef20f5edbea9406f2b8ae69d9`
- Adapter: `wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-30e158011725-sft-resume:v53`
- Private config/results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v53-prompt-disjoint-toolrounds4-heldout120-sft-only/` (directory mode 0700; files mode 0600).

See the [v51 120-case evaluation](wandb-v51-prompt-disjoint-heldout120-eval-2026-10-20.md) and [v53 five-case sentinel](wandb-v53-five-scenario-dev-eval-2026-10-20.md).
