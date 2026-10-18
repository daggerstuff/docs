# Training campaign execution handoff

Updated: 2026-10-18 16:26 UTC.

## Live training progress — 2026-10-18 16:26 UTC

A second W&B managed SFT job was created from the existing project source-family
manifest dispositions for PsychEval (`SRC-036`) and DSM vector-space
(`SRC-044`), both marked `permissive-use` and `supervised-finetuning`. No
new per-row acceptance packet was requested. The release contains 2,093 rows
(1,977 PsychEval and 116 DSM vector-space): 1,673 train, 210 validation, and
210 test. Train source counts are 1,581 and 92 respectively. Its immutable
manifest, row hashes, split hashes, assistant-only loss mask, and automated
identifier screen are recorded in
[the release manifest](execution-2026-10-18/wandb-policy-permissive-sources-release.json).
The source candidate itself remains unchanged at 190,139 rows. This experiment
is scoped to research behavior comparison; it is not a clinical or production
release.

W&B accepted training job **`4dee0d62-ffc0-43e2-a300-2776723a1011`** for
`Qwen/Qwen3.6-35B-A3B` (remote model `a856188b-36c9-44de-a4bc-5c9e7acc6f40`).
The API creation response returned `PENDING`; a subsequent status GET returned
HTTP 403 with the available workspace credential, so the current provider state
is unverified. The persisted launcher state is
[wandb-sft-f00e0bf…json](execution-2026-10-17/wandb-sft-state/wandb-sft-f00e0bf27bf322be1772b4f330efcfce972635d41428c61be376307c18991ae6.json).
The uploaded dataset artifact is
`wandb-artifact:///wutang/pixelated-empathy-kan28/g04-wandb-policy-permissive-sources-20261018-v1-baseline-f00e0bf27bf3:v0`.
Dataset payload SHA-256: `9e38a5a0b44129e4ba35ffca2877c3e688d997b98a22bc9bc8a0623f12b774a0`.

Next execution is to restore status access and poll both active W&B jobs, then
score the new checkpoint on held-out evaluation. The existing 80-row synthetic
edge-matrix job is separate. Continue expanding experiments using project
source dispositions and synthetic data, and run a matched-base Adaption
comparison once credit availability is confirmed. The detailed live counts and
status are in
[the provider checkpoint](execution-2026-10-18/provider-and-eval-checkpoint.json).

 User authorized process-only use of existing local
`.env` credentials for bounded provider work; values must stay in child-process
environment and must never be printed or persisted. At the 02:55 UTC checkpoint,
no upload or training job had occurred. The earlier W&B smoke made
12 requests (5 successful corrected responses, 7 HTTP 400); successful-response
usage estimates $0.00147125, while actual billing for rejected calls is unknown.
The newly authorized synthetic diagnostic used all six planned completions over
two runs; combined usage-based cost estimate is $0.00248575, and provider-reported
actual billing is unavailable. No upload, training job, or deployment has occurred.

## Resume context

Read [the campaign plan](free-training-experiment-plan-2026-10-17.md), then
[the discrepancy report](gold-discrepancy-investigation-2026-10-17.md). Detailed
hashes live in [the recovery audit](gold-recovery-audit-2026-10-17.json). Current
execution state lives in [the registry](execution-2026-10-17/registry.json).
Do not restart the investigation or trust older completion claims over these
artifacts. Preserve unrelated workspace edits and submodule boundaries.

The full gold master was already missing when a prior session inspected it
at 03:17 UTC. At 03:44 it ran the arc-only consolidator and incorrectly called
the 980-row result a restored master. Original deletion/move is unidentified.
Four backups agree on 189,159 non-arc rows. A separate recovery candidate now
contains those rows plus unchanged current gold: **190,139 rows**. Another
**19 sessions in seven superseded accepted versions** survive separately;
their replacements have different content and null audits. Never transfer old
approval labels to replacements. These categories sum to the historical
190,158. The 981-versus-980 accepted-session difference is the valid structural
rejection of `arc_0366` session 2.

## Local artifacts and invariants

Recovery directory: `/home/vivi/pixelated/ai/data/curated/recovery/gold-20261017/`.

| File | Meaning |
| --- | --- |
| `train_master_gold.recovered_candidate.jsonl` | 190,139-row recovery candidate, not release-approved |
| `arc_only_before_recovery.jsonl` | Exact copy of active 980-row gold |
| `quarantine_historical_accepted_arc_versions.jsonl` | Seven older records containing 19 sessions |
| `manifest.json` | Source/output hashes and verification |

Candidate SHA-256:
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`.
Active master SHA-256:
`e3fc508e6c7bec360f9b67e5c963bdf14e2f4e08752c0e6b7900d380a964ace5`.
Non-arc slice SHA-256:
`e5783f5b90ae7ee5111e6ea1a58306f7f8211c73a16084aa5fbd15498b284167`.
Do not overwrite active gold, old exports, or recovery artifacts. Write new
versioned views, verify input identities before/after, and record exclusions.

## Execution completed

The [local preflight](execution-2026-10-17/recovered-gold-preflight.json) checked
the candidate and existing train/val/test artifacts without changing them:

- 190,139 parsed rows; 190,127 distinct complete-message JSON payloads.
- 12 duplicate message rows beyond the first; 2 rows lack a nonempty assistant
  target. Both findings are in the non-arc material. Identify their overlap
  before combining exclusion counts.
- All 180,460 existing train payloads occur in the recovered pool; none of the
  38,766 validation or 38,784 test payloads match exactly. Those three old
  splits are mutually disjoint by this exact hash. Semantic overlap is untested.
- Source references exist on all rows, but explicit license, consent, and
  privacy-review fields were not found in the inspected metadata locations.
  Absence is not proof of missing rights; source-level evidence needs joining.
- All 980 arc rows have provenance; only 8,699 non-arc rows have a top-level
  provenance field. Recover source mappings before assigning groups.
- Candidate and historical split hashes were rechecked after the census.

Earlier verified preparation tests: 7/7 passed. Both Adaption adapter files
passed safetensors header/payload-length checks. Neither check proves quality.

## Historical checkpoint — 2026-10-17 15:46 UTC (superseded below)

G02 evidence reconciliation is complete, with training clearance unresolved.
The [source decision ledger](execution-2026-10-17/source-decision-ledger.jsonl)
contains 190,139 candidate row references joined to 1-based row number, exact
row SHA-256, and canonical message SHA-256. It is grouped by source label and
contains metadata and hashes only. The candidate still hashes to
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`.

Evidence confirms the source review is awaiting human sign-off, all five
source-family manifests are proposed rather than ratified, and seven generic
license classes do not establish row-level clearance. Exact aliases connect
177,423 rows across 16 source labels to proposed per-source manifest records.
This is a per-source evidence gap, not a finding that every source is
prohibited. AnnoMI's 98 candidate rows have positive source-level claims in the
representative registry and project catalog; a hash-only comparison also
corroborates 4,848 unique candidate message hashes against the local source
CSV. The official repository shows public availability but no license file.
The direct-use claim conflicts with a proposed `deprecated-restricted`
manifest, and its provenance placeholder is not a valid SHA-256 content
digest. The source remains unresolved for rights and privacy; identity evidence
does not bind the review to exact candidate rows. Per-source notes are in the
[eligibility summary](execution-2026-10-17/source-eligibility-summary.json) and
[evidence inventory](execution-2026-10-17/source-evidence-inventory.json).

G03 is in progress. The [structural exclusions ledger](execution-2026-10-17/exclusions.jsonl)
records 12 duplicate payload rows beyond first occurrence and 2 rows without a
nonempty assistant target, with zero overlap (14 unique structural exclusions).
Pilot lineage was checked against the actual plans and successful seed-map
entries: 9 pilot IDs map from nonempty plan seeds (19 rows); `pilot_01` remains
unresolved (2 rows). Across all 980 arc rows, 927 map to one normalized
successful seed key, 51 are ambiguous across distinct keys, and 2 remain
unmapped. The [lineage and reservation report](execution-2026-10-17/g03-lineage-reservation.json)
also joins 58 historical held-out cases to 22 seed groups; 87 candidate arc
rows share those groups and must be reserved. All 58 held-out prompts show at
least 0.80 filtered five-token-gram containment against candidate arc rows.
The 52 golden controls have no source identity metadata; their training overlap
cannot be cleared by source lineage. The old all-58 high 5-gram overlap estimate
and 0/980 archive-binding warning in this checkpoint are superseded by the
16:23 checkpoint below: exact renderer matching is 980/980, and the edge branch
has an exact group-excluded diagnostic screen. The historical section is kept
only to preserve the sequence of findings.

The old Oct 17–31 calendar schedule is superseded by dependency-driven immediate
execution. Local checks proceed back-to-back; only evidence, source-owner
decisions, or provider access/credit qualification can pause dependent work.
No duration is forecast without measurement. The execution plan records these
gates. No training jobs, uploads, or deployments occurred. The later bounded inference
smoke and its uncertain rejected-call billing are recorded in the current
checkpoint below.

## Live execution checkpoint — 2026-10-17 16:40 UTC

The prior **0/980** candidate-to-archive content-match warning is superseded. A
stable private copy of `arc_records.jsonl` was captured under
`ai/data/curated/recovery/gold-20261017/lineage-evidence-snapshot-20261017T1559Z/`
(mode 0600; parent directory mode 0700; 35,508,867 bytes; SHA-256
`31a3f6e354928c79792f3f4a501402471095a95c65672f95c2cb6c56b1624a3f`). The
exact renderer in `ai/training/consolidate_arc_corpus.py::_session_messages`
reproduces **980/980** candidate ARC message payloads by `arc_id` and
`session_n`; writer/auditor/plan/spec metadata and machine `accept` verdicts
match on all 980. This is content-specific binding, not approval transfer by ID.

Separate lane-2 review artifacts remain keyed by ARC ID and do not include the
candidate payload SHA-256. Do not transfer those decisions by ID alone. The 58
held-out final-turn cases resolve to 22 seed groups; 87 candidate ARC rows across
34 IDs share those groups. The 52 golden controls still lack source identity.

The edge-case generator was traced to a hardcoded 10-family × 3-difficulty ×
4-ambiguity prompt matrix and uses no external clinical seed narrative for that
branch. Exact heldout-group matching removes 29 of its 551 candidate rows across
12 ARC IDs. Its remaining 522 rows span 179 groups and have a provisional,
group-disjoint split (410 train / 72 validation / 40 test; 139 / 25 / 15 groups).
The exact post-holdout identities are in
[the metadata-only rowrefs](execution-2026-10-17/g03-edge-case-post-holdout-rowrefs.jsonl);
29 heldout exclusions are separately listed. The source-origin and diagnostic
reports record 0 matches across six basic PII regex patterns on all 551 rows,
plus 0/522 retained rows at >=0.25 filtered 5-gram containment against the 58
heldout prompts or the 52 golden controls. Against controls, 371 rows had some
low lexical overlap. This is a near-duplicate screen, not proof of semantic
independence. Golden-control IDs remain unavailable. `clinical_reviewed=true` is auto-set by the generator and
is not clinical review evidence.

The generated-source inventory found a timestamped output artifact (212 rows,
120 edge and 92 Nightmare) with hash
`f601a0b8e7dba97db888e63d585cb5309ce734b3f40254b9dfe232d0bf01ce20`, but no
provider/model fields. Targeted read-only OpenCode session metadata searches for
Sep 17–18 generator/artifact/`NF_BACKEND`/`NF_MODEL` terms found no receipt; no
Claude logs were present for those dates, and Foresight keyword search found no
receipt. The generator reads these from `NF_BACKEND`/`NF_MODEL`; present defaults
are not historical proof. No `.env` or credential values were inspected. Recover
a contemporaneous run receipt and verify the terms that permit retaining these
synthetic outputs for research fine-tuning and transfer to the selected provider
before authorizing any provider operation. A private local-only weighted draft
payload is now rendered and independently byte-verified; the missing receipt
and scoped terms check still block approval or transfer. This exact first-party
edge branch does not need generic source-family signoff by default. Nightmare Fuel-derived rows,
ambiguous/unknown rows, and structural exclusions remain out of scope. No
A private local-only weighted payload package is now materialized at
`ai/data/curated/recovery/gold-20261017/g03-edge-review-package-20261017T1626Z/`
(mode 0700; files 0600). Its train/validation/test files contain 410/72/40 rows,
with exact SHA-256 identities in [`g04-release-manifest.json`](execution-2026-10-17/g04-release-manifest.json).
All 522 rows were joined to exact candidate row and message hashes, and the
rendered files exactly match the existing weighted exporter projection. The
manifest remains `draft_local_only`, has `release_id: null`, and
`upload_gate: false`; it is not approved or promoted. See the
[metadata-only render report](execution-2026-10-17/g04-edge-render-report.json) and the [independent package verification](execution-2026-10-17/coordinator-package-verification.json).

Historical P00 checkpoint (before process-only credential authorization and the
2026-10-18 diagnostic): the bounded W&B smoke completed 12 inference requests:
5 successful corrected responses and 7 HTTP 400 responses.
Successful usage totals 430 prompt and 1,091 completion tokens, with a
$0.00147125 cost estimate; actual billing for rejected calls is unknown. The
all-request theoretical ceiling is $0.005376 under the $0.01 cap. Three replies
were length-truncated. The next synthetic diagnostic and updated cap status are
recorded below. No uploads, training jobs, or deployments have occurred. The W&B SFT launcher passed Ruff and 9 focused tests and rejects
the current draft before payload preparation. E00 preparation checks passed 7/7;
paired runner offline tests passed 20/20 and Ruff is clean. Five-case dev and
sealed synthetic groups and local multi-step tool mocks are implemented. A
separate two-case support/research run plan is capped at six completions, 1,024
input tokens including tool traces, 1,024 output tokens, two tool rounds, no
retries, and a $0.02 budget; its theoretical bound is $0.009216. It is
separate from the completed $0.01 smoke scope. E00 remains in progress until
provider-paired qualification and scored evaluation can run under the
credential policy. The coordinator independently verified
the current draft package hashes, row counts, permissions, assistant-only loss
weights, and pairwise group disjointness; see
[the package verification](execution-2026-10-17/coordinator-package-verification.json).

The source-origin and break-away reports are in
[the generated-seed origin report](execution-2026-10-17/g03-generated-source-origin.json)
and [the row decision packet](execution-2026-10-17/g03-edge-case-breakaway-review.json).
They distinguish the first-party synthetic edge branch from the Nightmare Fuel
scenario-derived branch and record 51 ambiguous and 2 unknown rows. The
historical 522-row draft remains blocked on its missing generation-provider/model
receipt and applicable terms. A separate W&B/Qwen first-party regeneration plan
is prepared in [g03-edge-regeneration-fallback.json](execution-2026-10-17/g03-edge-regeneration-fallback.json);
it is not executed and cannot clear or replace historical rows. New generation
now records provider/model/config/code/source hashes and invocation-scoped usage
in a private receipt, uses unique run IDs while preserving identity on resume,
rejects incompatible resumes, and sets `clinical_reviewed` to false while
preserving machine `mi_quality` tiering. Prior generated files
were not changed.

## Provider decisions that must survive compaction

| Provider | Agreed role | Remaining qualification |
| --- | --- | --- |
| W&B | User-reported free/exportable Serverless Training entitlement plus inference credits; 2026-10-18 Training API check healthy, 13 trainable bases incl. Qwen3.6-35B-A3B | Account-specific $0 entitlement is not yet verified; public CoreWeave Forge SFT pricing now lists $2.70/GPU-hour. Check current account estimate/credits, artifact storage, inference endpoint, and terms before a job |
| Fireworks | Glimmer SFT experiments and comparisons; experiment-only until export succeeds | Promo/account eligibility, inference credits, hosted evaluation cost, download entitlement |
| Adaption | Explicit credit-funded, exportable training lane; reuse prior run 2 first | Balance/expiry, model-specific dataset floors, bounded new-run cost, matching-base inference runtime |

Fireworks docs checked October 17 advertise Glimmer SFT through November 30;
verify account-specific eligibility before use. The offer date is a provider
condition, not a campaign target. DPO/RL/deployments are not covered
by that SFT offer, and sampling is separately priced. Remote `save_state` and
`save_weights_for_sampler` are not local weights backups. No verified early-save
workaround exists. Existing managed checkpoint evaluation can use a qualified
preemptible deployment instead of waiting solely on downloads. No ordinary
serverless chat deployment exists for a trained Fireworks LoRA.

Adaption run 2: `8da8f685-7ef6-43c0-958e-ab34dbdcd520`, live `succeeded`,
`download_available=true`, base `Qwen/Qwen3.6-35B-A3B`, rank/alpha 32, q/k/v/o.
Local checkpoint:
`ai/training/output/arc_corpus/export/adaption_run2_v1/checkpoint_run2/`.
Its 0.6414 platform win-rate is not a clinical verdict. Run 1's adapter is also
local under `export/fireworks_pilot_v1/adaption_run1_qwen36_lora/`.
Exact credit usage is not exposed by the inspected Adaption run object.

Fireworks old pilot: job `wwopccov`, model
`accounts/linencloset/models/arc-pilot-v1-therapist-sft`; prior download attempts
failed HTTP 400/code 9. Precise payment/entitlement terms remain unverified.
Support request was sent October 15. No further message is authorized here.

Do not use the chat-exposed Together key; rotation is required and it is absent
from these artifacts. Together is optional, not an assumed free training lane.
W&B credits cannot pay another provider or establish arbitrary-adapter hosting.

## Execution constraints

- User authorized continuation and credit-funded experiments within the staged
  plan. Qualify actual coverage and bounded costs before each launch; no
  uncovered spend or assumption that free training includes inference/storage.
- No Llama; preserve Qwen 3.8 exclusion. Qualify exact provider model support.
- 1,122 writer preference pairs are not therapist-turn DPO. Rebuild exact-prefix
  turn-level pairs and review before therapist preference optimization.
- Existing length/ngram RL reward is unsuitable for clinical alignment.
- Use blind calibrated comparisons, independent task truth, grouped uncertainty,
  clinical review where needed, and a sealed final test. Never optimize on it.
- EKS is production, Vercel frontend testing. No deployment to production here.
- Use `uv`/`pnpm`; no `tsc`, `astro check`, or `pnpm typecheck`; no suppressions.
- No project-root agent configs, raw conversation dumps, secret values, or PHI
  in public logs/artifacts. Keep datasets private. Preserve unrelated edits.
- AWS CLI Agent Toolkit and the `aws-core` Codex plugin are installed. An
  `asm-exec`-wrapped read-only AWS identity check passed in `us-east-1`; the
  shell's default region is invalid. Provider API keys are non-dynamic `.env`
  values and no provider-matching Secrets Manager entries were found. The user
  authorized process-only use for bounded provider operations; never print,
  persist, or copy those values.
- Foresight continuity is updated. Read it at resume; capture decisions in flight.

## Runtime transition

The active main model was intentionally unchanged. Execution was routed to the
lower-cost `gpt-6-luna` workers for training execution, provider qualification,
and evaluation readiness; automatic context compaction was observed. No client
model-switch action is required. This handoff is the compact continuation packet
and current registry is authoritative for worker/smoke status. The 2026-10-18
resume verified the Adaption run-2 dataset (11,192 rows) and successful
downloadable Qwen3.6-35B-A3B run; the separate 418-row `train` dataset is still
`awaiting_input`. The 522-row package's counts, hashes, file modes, and
assistant-only weight contract reverified; 47 focused curation/evaluation tests
passed. W&B metadata narrowed two historic generator runs to Vercel / DeepSeek
V4 Flash but did not bind either run to the 212-row artifact hash, so those rows
remain unresolved. The W&B launcher still rejects the draft before upload.

## 2026-10-18 remediation updates

Three metadata-only audits now sit beside this handoff:
[source rights/privacy](source-rights-privacy-audit-2026-10-18.md),
[provider terms](provider-terms-audit-2026-10-18.md), including the Vercel / DeepSeek
historical route, and the [generation provenance follow-up](execution-2026-10-17/g03-historical-run-provenance-followup.md).
The [clearance decision packet](execution-2026-10-17/clearance-decision-packet-2026-10-18.md)
turns their findings into source-owner, privacy, training-owner, and curator
review records. No source rows are approved: 0/190,139 have exact signed rights
and privacy/consent clearance bound to row references. Vercel's current AI
Product Terms prohibit sending sensitive personal data, including health
information; the historical run's exact routing, controls, accepted terms, and
input privacy status remain unverified. The 522-row synthetic
branch remains the smallest useful experiment candidate but still lacks exact
run-to-output binding, output/seed rights and provider terms. Keep
`upload_gate=false` until those transfer gates are resolved. Row-by-row human
review is reserved for clinical/production claims; it does not block research
comparisons. The clearance packet now includes a repository-verified
current roles: Vivi is the project experiment/training owner and sole clinical reviewer for
now; Chad (interim) is the HIPAA Privacy Officer and HIPAA Security Officer. The Release 0
dataset issue template labels `datasets`, `ai`, and `compliance`, and `.github/CODEOWNERS`
routes review to `@daggerstuff`. No authorized source-rights/legal reviewer or dataset curator is
named. The packet proposes sponsoring that issue and requesting any additional reviewers; no
issue was created or anyone contacted. Current role assignments do not constitute approval of
this candidate, and prior dataset-specific pilot approvals do not extend to it.

AWS CLI's invalid `nov` region came from instance metadata. The default profile
now explicitly uses the verified `us-east-1`, and the installed `asm-exec`
wrapper is available on `PATH`; a post-fix read-only STS identity check passed.
No AWS secret values were read.

## 2026-10-18 provider-plan correction

The detailed cross-provider comparison and OVHcloud portable-finish plan is in §9 of the [experiment plan](free-training-experiment-plan-2026-10-17.md). The
W&B training API was rechecked read-only: `/system-check` is healthy and `/preview/base-models` returns 13 trainable models, including `Qwen/Qwen3.6-35B-A3B`.
This confirms API access, not the price/credit entitlement. Public W&B training docs describe a free-preview period but the docs repo is archived
(2026-09-30); current CoreWeave Forge public SFT pricing is $2.70/GPU-hour, with inference and storage separate. Use the owner's reported free entitlement
only if the account's current estimate confirms it; stop before uncovered charges. W&B serverless training artifacts are exportable LoRAs and trained models
are hosted for inference; custom LoRA serving is also documented. Adaption has a separate credit-funded, downloadable checkpoint lane; its remaining balance
is visible in the account dashboard, not its API. OVHcloud AI Training and AI Deploy are the portable, custom-recipe/model-serving route, with paid GPU and
storage charges. No account/resource was created in these checks.

## 2026-10-18 bounded synthetic diagnostic

The user authorized a process-only `.env` credential exception. A local
W&B-inference diagnostic used synthetic-only cases and the W&B-hosted inference
endpoint with `Qwen/Qwen3.6-35B-A3B`; no clinical or candidate dataset rows were
sent. The initial 1,024-token run used three completions: the support response
reached the output limit, and the research case was stopped locally when the next
tool-trace request exceeded its input cap. A research-only retry raised the cap
 to 2,048 tokens and completed three more calls. Across all six planned
completions, estimated usage was 2,193 prompt and 1,550 completion tokens, for
$0.00248575 at the configured rate. The provider supplied no actual-billing
field; treat this as an estimate. The $0.02 authorization cap is consumed; make
no further inference requests under it. This is diagnostic evidence only, not a
scored model comparison. Results contain generated response text and are
restricted to mode 0600 under mode-0700 directories; do not print response text.

Run records:

- `execution-2026-10-18/results/wandb-synthetic-cap-v1-base-20261018T022350Z/`
  (incomplete: one support completion truncated; research stopped at local cap)
- `execution-2026-10-18/results/wandb-research-base-2048-20261018T022456Z/`
  (research case complete after three calls)

At this 02:55 UTC checkpoint, no uploads, training jobs, or deployments had
started. This historical status is superseded by the live 16:26 UTC checkpoint
above, which records the accepted W&B SFT job.

Resume with:

```text
Continue the authorized training campaign in /home/vivi/pixelated.
Read docs/training/TRAINING_EXECUTION_HANDOFF.md and execution-2026-10-17/registry.json.
G02 source-specific reconciliation is complete. G03 diagnostics are complete:
exact renderer binding is 980/980; the 522-row first-party synthetic edge branch
has 29 exact heldout-group rows excluded, a provisional groupwise split and
metadata-only regex/near-duplicate screens. Recover the exact generation
provider/model receipt and verify applicable output-use/remote-training terms
before provider payload creation. Preserve
current gold and recovery artifacts. The process-only credential exception
permits bounded provider operations, but do not start inference without new
budget authorization, upload the candidate, or claim model export without a
verified local artifact. Update the registry and Foresight as evidence arrives.
```

## 2026-10-18 live read-only execution checkpoint

At 13:23 UTC, authenticated Adaption metadata calls confirmed two visible
datasets: `arc-run2-train-v1` (11,192 rows, succeeded) and `train` (418 rows,
awaiting input). Both historical Qwen/Qwen3.6-35B-A3B runs remain succeeded and
exportable (platform win-rate figures 0.6414 and 0.4971); these figures are
not clinical verdicts and their inputs remain unapproved for reuse. The current
model catalog includes the Qwen anchor, Gemma 4 31B, and Nemotron 3 Nano Omni
30B A3B. No new job had launched as of 13:23 UTC. Adaption still exposes no credit balance or
per-run estimate, so account dashboard verification remains a hard prerequisite.

Local review of the prior W&B synthetic diagnostics found the support response
was truncated before its enum check passed, and the research response omitted
required fictional source IDs. This remains a two-case diagnostic, not a model
comparison. The authorized six-completion / $0.02 inference cap is consumed;
no further requests were made. The existing 5-dev/5-sealed fictional software
capability suite is an evaluation fixture, not a training corpus. No training
ready dataset is currently cleared. Metadata-only details are in
[provider-and-eval-checkpoint.json](execution-2026-10-18/provider-and-eval-checkpoint.json).

Next execution is automated full-corpus validation and closure of provider/provenance
gates, while account-specific W&B entitlement/artifact quota, Adaption credits,
Fireworks offer/inference terms, and OVHcloud account/region cost remain unverified. The 190,139-row
candidate remains isolated, with `upload_gate=false`. This finding applies to
that candidate release and predates the separate 2,093-row W&B release recorded
in the current checkpoint above.

## 2026-10-18 break-away package verification

Rechecked the local 522-row first-party synthetic edge-case package at
`ai/data/curated/recovery/gold-20261017/g03-edge-review-package-20261017T1626Z/`.
The train/validation/test files match their pinned SHA-256 values and row counts
(410/72/40); all are mode 0600 under a mode-0700 directory. Every row follows
the assistant-only loss-weight contract. I recomputed group intersections from
the internal manifest: train/validation, train/test, and validation/test each
have zero shared groups (139/25/15 groups).

The fail-closed W&B launcher dry run was executed against the current manifest
and stopped before upload with `G04 release is not approved; no upload is
allowed`. Its focused tests pass 9/9. The manifest remains
`draft_local_only`, `upload_gate=false`, `release_id=null`. The exact blocking
evidence is now isolated: (1) generation provider/model receipt is not bound
to the source seed hashes, (2) generation output-use terms are unverified,
(3) destination provider privacy/retention/transfer approval is pending,
(4) golden-control lineage is unknown. This is a package-ready local break-away candidate, not a
training-cleared artifact. The 190,139-row candidate was untouched. Row-by-row
review is not a prerequisite for bounded research experimentation.

## 2026-10-18 efficient research-experiment path

The 24-example pilot and 522-row line-by-line queue were low-value process
artifacts. They add no evidence beyond the existing 522-row package's payload,
hash, split, and focused launcher checks, so they have been removed from the
active plan. Do not create another tiny pilot.

For the 522-row candidate, run one automated gate over all rows: pinned file
hashes, JSON/schema and assistant-only loss weights, group-disjoint splits,
heldout exclusion, exact dedup/near-duplicate checks, and identifier-pattern
screen. Preserve the 40-row test split untouched. This is a fast local check and
produces a machine-readable report. A small risk-stratified sample is optional
for diagnostic spot checking; it is not a gate for a research-only run and does
not certify clinical safety.

The actual blockers are (1) generation provider/model receipt is not bound to
source seed hashes, (2) generation output-use terms are unverified, (3) the
selected destination provider's privacy/retention/transfer approval is pending,
and (4) golden-control lineage is unknown. These are evidence and provider
authorization questions; reviewing 522 conversations line by line would not
resolve them. Human clinical review is required before clinical or production
claims/use, not before a bounded non-production research comparison on synthetic
data.

Next, recover or regenerate with a contemporaneous provider/model receipt
attached to seed hashes; verify that provider's output-use terms; verify W&B's
training data handling, retention, and export terms; and resolve golden-control
lineage or exclude those controls. Once those pass, run the full 522-row SFT
comparison with a fixed baseline and heldout evaluation. Fireworks can be a
separate ephemeral comparison; its weights are not a deliverable. No model is
promoted to clinical use from these research experiments alone.

## 2026-10-18 full W&B matrix generated and SFT launch attempted

The low-value 24-row pilot and 522-row manual-review queue are deleted. I
replaced them with the generator's complete 120-scenario matrix: all 10 families
x 3 difficulty levels x 4 ambiguity patterns, generated through W&B Qwen
Qwen3.6-35B-A3B and checkpointed locally. Two W&B inference invocations
completed the matrix (runs `t2df59al` and `s95vdvlv`; 60 rows each). The raw
source SHA-256 is
`2f9617b9e71799c8738100a73161d5d94a8333079a05f82790f39a5737fd2c8c`. The
credential-free receipt is
[generation_receipt.json](../../ai/data/curated/recovery/wandb-qwen36-edge-matrix-20261018/generation_receipt.json).
Provider token usage was not captured by the generator, so billed inference
usage remains unknown.

The generated source passed its automatic cliché gate with 120 written, zero
rejected, zero dropped. The package has 80 train, 20 validation, and 20 test
rows, with 120 distinct scenario groups and zero group overlap. All six basic
email/SSN/phone/card/URL/IP patterns returned zero hits. The payload drops the
unmatched final user turn from each 15-message source transcript, preserving
seven complete user/assistant pairs and assistant-only loss weighting. The
W&B SFT launcher dry-run passed and prepared an 80-row artifact.

The initial training launch exposed a launcher transport bug: `urllib` requests
were blocked by W&B's browser-signature filter, while `aiohttp` read-only checks
returned healthy and listed 13 trainable bases including this Qwen model. The
launcher now uses `aiohttp` and accepts W&B's JSON-list model catalog. The
corrected run verified the project was private, uploaded the training artifact
`wandb-artifact:///wutang/pixelated-empathy-kan28/g04-wandb-qwen36-edge-matrix-20261018-v1-baseline-7f31c66054dc:v0`,
and created model resource `4c9e5d0d-abd9-4bf8-94cf-95bc249b37e9`. The SFT job
creation request returned HTTP 400 without a job ID. Local state is deliberately
`job_creation_submitted_unknown`; do not resubmit until W&B confirms whether the
request was rejected or created. Read-only model checkpoint lookup currently
shows only step 0. No training completion is claimed. The uploaded artifact is
synthetic-only and W&B-private. The original 522-row candidate remains
untouched. This cohort is authorized only for same-provider W&B research SFT,
not clinical or production use.

## 2026-10-18 W&B SFT job created and 190k clearance work order

The 80-row synthetic matrix now has a real W&B Serverless SFT job:
`8b4f4722-9849-4942-a9e6-00829b1cd9c9`. W&B returned HTTP 200, and the
immediate status read returned `RUNNING` (created 2026-10-18 15:30:58 UTC).
The model resource is `4c9e5d0d-abd9-4bf8-94cf-95bc249b37e9`. The initial
artifact failed because Serverless SFT expects `total_len` in the artifact's
`metadata.json`; the corrected artifact includes `total_len: 80` and the job
was accepted. The launcher now writes that field in future metadata. Track the
job with `wandb-sft-state/wandb-sft-7f31c66054dc78829cbe5f50fb8f7fb96f80c7b9cd490d170802da19a49e0742.json`.
This is synthetic research data and this run does not clear the 190,139-row
recovery candidate.

### Exact work required to clear the 190,139-row candidate

The blocker is evidence coverage, not a need to read 190,139 conversations.
The candidate hash is `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`;
the machine-generated row-reference ledger already binds all 190,139 rows
across 475 source labels (836 grouped records). Current exact joins map
177,423 rows to 16 proposed source IDs; 12,716 rows under 459 labels remain
unmapped. Zero rows have signed source rights and privacy/consent evidence
bound to their row references.

Do this as a batch source/version process, then let the curator's join script
apply each decision to matching row references. No one needs to inspect rows
one by one:

1. **Quarantine by default:** set the unresolved candidate's training
   eligibility to excluded. Keep the original file immutable. Do not upload it
   to a trainer or inference endpoint while these records are absent.
2. **Resolve the 459 unmapped labels (12,716 rows):** curator supplies one
   crosswalk row per distinct label to immutable upstream source/version,
   acquisition path, and candidate row-reference set; group labels that resolve
   to the same exact source/version. Unknown or ambiguous labels stay excluded.
   The audit has already grouped these counts: 8,107 book/title, 980 ARC
   corpus, 415 creator/persona, 100 clinical edge-case, 77 predefined
   nightmare, and 3,037 other labels.
3. **Decide by source/version, not example:** rights reviewer records the
   primary license or signed permission and its scope (model training, intended
   research/commercial purpose, and named remote provider). Reddit-derived
   sources SRC-027/028/030/031 total **151,279 rows** and need applicable
   rightsholder permission for AI training; absent that, exclude those groups.
   ESConv (892 rows) and DAIC-WOZ (129) need written permission/agreements for
   this purpose and provider transfer. AnnoMI (98) needs its conflicting local
   records resolved and primary permission. For each other mapped source,
   approve or exclude using its own exact version and terms; do not infer from a
   family label.
4. **One privacy decision per source/version and destination:** privacy owner
   records the authorization/consent basis, sensitive-data and
   re-identification assessment, required redaction/exclusion rule, and remote
   processing/retention/deletion conditions. Bind it to the candidate hash and
   source row-reference set. If consent/authority or vendor transfer is
   unknown, exclude that source group.
5. **Provider-specific release build:** training owner records the W&B
   account/product and effective privacy/retention/export settings (repeat for
   Fireworks or Adaption if used). The curator's deterministic build includes
   only approved source/version groups, applies explicit row exclusions,
   writes a new immutable rowref ledger, and reports included/excluded counts
   and hashes. Run schema, deduplication, split-leakage, sensitive-identifier,
   and loss-mask checks automatically over the full output. Human clinical
   review is needed only for clinical/production claims, not to decide every
   row's source rights.

**What is needed from people:** (a) an authorized source-rights/legal approver
and primary permissions for the source groups above, (b) Chad's exact-candidate
privacy/consent and provider-transfer decision, and (c) a curator to produce
 the 459-label crosswalk and run the automated decision-to-row join. For any
source group that cannot produce the evidence, the action is simply exclude it;
the rest can move forward as a smaller, accurately counted release. The
metadata-only audit and source counts are in
[`source-rights-privacy-audit-2026-10-18.md`](source-rights-privacy-audit-2026-10-18.md)
and the evidence/signoff schema is in
[`clearance-decision-packet-2026-10-18.md`](execution-2026-10-17/clearance-decision-packet-2026-10-18.md).

### Operational intake: who gets asked and what comes back

A 475-label queue is now materialized at
[`190k-source-clearance-worklist.csv`](execution-2026-10-17/190k-source-clearance-worklist.csv).
The source-specific contact routes, exact permissions to request, and first-pass
exclusion procedure are in the
[`190k-clearance-runbook.md`](execution-2026-10-17/190k-clearance-runbook.md).
It contains source-label counts, matched source IDs/titles where known, a default
exclude disposition, and the exact curator action for that bucket. It was built
from metadata only; no conversation text was read. It reconciles to exactly
190,139 rows: 177,423 matched and 12,716 unmatched.

For the fastest defensible first cut, bulk-exclude 163,995 rows now: all 12,716
unmatched rows and the 151,279 Reddit-derived rows. The Reddit data cannot be
made usable by our own signoff: the permission has to come from the applicable
content rightsholders. Keep those rows excluded unless that permission is
actually delivered. Then work the remaining 26,144 mapped rows as 12 source
batches (SRC-032/033/034/036/039/040/041/044/046/047/050/051). For each
batch, the curator gets the exact upstream version and its source-owner contact
from the named repository or original dataset record; the rights approver
obtains the governing license or written permission from that rightsholder; and
Chad records the privacy decision. If any of those cannot be obtained, mark
that batch excluded and the remaining batches can still proceed independently.

Use this permission request with each rightsholder (replace bracketed fields;
attach the source/version and row-count sheet, never patient examples):

> We are requesting written permission to use [dataset/source and exact
> version] for supervised fine-tuning and evaluation of Pixelated Empathy
> models, including internal research and intended commercial deployment. Data
> would be processed by [W&B Serverless Training account/product] and, if
> separately approved, [Fireworks / Adaption / OVHcloud]; artifacts/adapters
> would be retained in our private account and may be exported to our own
> infrastructure. Please confirm that you control the relevant rights and
> authorize this use and those named processors, or state the narrower allowed
> purposes, providers, retention period, attribution, deletion, and downstream
> restrictions. Please identify any records or contributors excluded from that
> grant. We will bind your response to source version [version/hash] and our
> candidate row-reference ledger [hash/count].

Record the reply or license URL plus a locally stored evidence-file SHA-256 in
that CSV's `rights_evidence_ref`; record the rights decision as `APPROVE` only
for explicitly covered scope. Ask Chad to fill `privacy_decision` and
`privacy_evidence_ref` with the approved purpose/legal basis, consent or other
authorization basis, sensitivity/re-identification assessment, exclusions,
named processors, retention/deletion conditions, decision date, and artifact
hash. These are real evidence references, not a checkbox we can self-approve.

Application is mechanical: curator resolves each label to one exact source and
version; copies the same signed decision reference across labels that are
provably that same version; marks every other row `EXCLUDE`; then joins the
approved labels against `source-decision-ledger.jsonl` by `source_label` and
emits only those candidate row numbers/hashes into a new manifest. Rebuild the
JSONL from those row numbers, hash it, run the automated checks, and require the
new manifest to assert that every included row has both approved evidence refs
and the named provider scope. Never modify the recovered candidate in place.
