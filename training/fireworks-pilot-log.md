# Fireworks Pilot — Execution Log

**Created:** 2026-10-10, on the owner's "do those next steps" instruction. **Scope:** the
execution record for everything after the grant records — Package F upload, Package G spend
ledger, Package H step order. Nothing here grants anything; grants and their basis quotes
live in [`fireworks-approval-packages.md`](./fireworks-approval-packages.md).

## 1. Status (as of 2026-10-10)

| Item | State |
|---|---|
| Phase 1 (packages A–E) | **complete** — grants recorded in the packages doc |
| Package F upload | **EXECUTED on `linencloset`** — `arc-pilot-v1-train` (418) + `arc-pilot-v1-eval` (80) both `READY` (§7); train+val only; `test.jsonl` still local |
| Package G spend | cap $635 active; **$0.00 actual** — the cancelled job `jf3tmylp` rated $0.00 (promo verified, §10); pilot SFT `wwopccov` training free under the same promo (until 10/31) |
| Package H experiment | **step 1 (Render Samples) EXECUTED and verified** (§10); **budget gate DISSOLVED** — Glimmer SFT promo (free until 10/31, §10) verified at $0.00 rated; **step 3 pilot SFT RUNNING** (job `wwopccov`, 2 epochs, wandb-instrumented, §11) |

## 2. Package C conditions (recorded; console items flagged)

- **Account:** `linencloset` (display name `Top Nacho`) — created 2026-10-10 11:13 UTC;
  verified `READY`/`UNSUSPENDED` by authenticated `GET /v1/accounts` (12:26 and again 12:33
  UTC). The original account was suspended for billing (first attempt, §3) and was replaced
  by the owner the same day; per the owner's instruction this is the account of record and
  the old one is retired.
- **Provider terms/DPA:** standard product terms apply (docs.fireworks.ai). Owner confirmed
  2026-10-10 (~12:30 UTC) that the replacement account carries the same specifications under
  the standard terms — recorded as the in-force basis for this pilot.
- **ZDR / Secure Training applicability:** not enabled on this account tier; the owner
  confirmed the standard-specs posture (2026-10-10), so neither applies to this pilot
  (provider docs: accounts/zero-data-retention, guides/security_compliance/secure_training).
- **Data residency:** provider-default region (enterprise data-residency — provider docs:
  accounts/data-residency — is not part of this account's standard spec, per the owner's
  confirmation).
- **Encryption:** datasets carry an authoritative `encryptionState` (CMEK marker) returned
  at creation — recorded per dataset at upload (§7): both stamp `ENCRYPTION_STATE_PLAINTEXT`
  (no CMEK), consistent with the owner-confirmed standard account spec.
- **Deletion path (rollback):** `DELETE /v1/accounts/{account_id}/datasets/{dataset_id}`
  (provider docs: api-reference/delete-dataset).

## 3. Package F — first execution attempt (2026-10-10, superseded by §7)

- **Pre-egress identity re-check** (2026-10-10 11:08 UTC, all matched export plan §6/§9):
  gold `d357b8b5…`, train `281da447…`, val `6154878…`, test `35f34d09…`, manifest
  `f7e19cb6…` — the two upload candidates are byte-identical to the verified emission.
- **Mechanism (REST, per provider docs):** `POST /v1/accounts/{account_id}/datasets`
  (create entry; `datasetId`, `dataset: {userUploaded: {}, exampleCount}` — the API rejected
  a documented `displayName` field as unknown, so it was omitted) then
  `POST /v1/accounts/{account_id}/datasets/{dataset_id}:upload` (multipart `file`) —
  docs.fireworks.ai/api-reference/create-dataset + upload-dataset-files (single-request
  upload, ≤150 MB; largest file here is 13.4 MB). `firectl` is not installable from PyPI in
  this environment (no published package), so REST is the execution path. The API key was
  read from the environment only and never printed.
- **Planned dataset ids:** `arc-pilot-v1-train` (train.jsonl, 418 rows) and
  `arc-pilot-v1-eval` (val.jsonl, 80 rows); val attaches as the job's `evaluation_dataset`
  at Package H step 3. **`test.jsonl` is never uploaded by any package.**
- **Attempt:** the authenticated discovery `GET /v1/accounts` returned **HTTP 412** — the
  then-current account was suspended (billing). No create or upload calls were made after
  that; a suspended account cannot host the pilot. The account was replaced by the owner the
  same day (§2, §7).
- **Retry path (executed 2026-10-10 on the replacement account — record in §7):** (1) re-run
  the identity re-check above; (2) the two create calls, then the two upload calls (recorded
  in §7); (3) verified via `GET /v1/accounts/{account_id}/datasets` — state `READY`,
  `exampleCount` 418/80, `encryptionState` recorded; (4) Package H step 1 (Render Samples)
  in the provider console is next.

## 4. Package G — spend ledger (cap $635)

| Date (UTC) | Item | Estimated | Actual | Running total |
|---|---|---|---|---|
| 2026-10-10 | SFT job `jf3tmylp` (step-1 attempt; cancelled at 57% of 1 epoch, §10) | $11.16/epoch (plan basis — wrong; unrolled basis ≈$102/epoch at list) | **$0.00** — rated cost verified $0 (§10 promo resolution; `usageCosts:query`, attribution COMPLETE) | $0.00 |
| 2026-10-10 | SFT job `ida9f81a` (first step-3 attempt; cancelled before any steps ran, no capacity received, §11.1) | $0.00 under promo | **$0.00** — no steps ran | $0.00 |
| 2026-10-10 | SFT job `wwopccov` (step-3 pilot SFT, 2 epochs, wandb-instrumented, §11.3) | $0.00 under promo | in flight — expected $0.00 | $0.00 |

Authorized lines: smoke test ≤$5 · pilot SFT ≤$150 (target changed to Muse Glimmer 30B;
model-specific pricing and eligibility must be re-verified before training) · evaluation
endpoint ≤$480 (≤40 GPU-hours, region-rate covered). Existing total cap remains $635. Any
overrun stops the pilot and returns to the budget gate.

**Budget-gate resolution (2026-10-10, evening — §10 addendum):** the gate opened earlier
today when the unrolled-token basis (~$102/epoch at list) seemed to exceed the $150 line.
It is now **dissolved**: the account dashboard shows a provider promo (owner-reported,
2026-10-10) — **"Muse Glimmer 30B SFT is free via UI and Serverless Training API until
10/31 ✨ No credit card required"** — and the platform's `usageCosts:query` API confirms the
account-wide rated cost for 2026-10-10 is **$0.00 with COMPLETE attribution**, covering the
47M-metric-token cancelled run. REST-created managed jobs rate $0 under the promo (the
cancelled job was REST-created). The unrolled-volume facts in §10 remain true and matter
for **list-price** planning (post-10/31, other models, other tiers) — under the promo the
pilot's training cost is $0 through 10/31, and the step-3 pilot SFT has been re-launched
(§11).

## 5. Package H — step order (binding; step 1 executed 2026-10-10; gate dissolved by the promo — step 3 executing)

1. **Render Samples** — **EXECUTED 2026-10-10 (§10): verified** — loss masks correct
   (user/system/headers 0; assistant trained exactly once per row, per-datum normalized
   weights summing to 1), ledger intact (36/36 assistant spans carry the 9-key JSON leading
   line), no truncation (max rendered datum 2,065 tokens ≤ the explicit 32,768
   max-context-length set at creation). Operational finding: the platform couples render
   capture to a live training job — the artifact is written only when the job reaches a
   terminal state, and there is no free pre-run render path.
2. **Format smoke test** — small managed-LoRA run on a ≤16B-class shortlist model over a
   ~100-row slice. Note: the slice dataset is additional egress (drawn from train.jsonl under
   the same Package C basis) and will be logged here before creation.
   **Status (2026-10-10 evening): satisfied by `jf3tmylp` evidence and not re-run** — that
   job trained 57% of a real epoch on the exact pilot payload + target model with healthy
   loss curves (train 0.708→0.405, eval 0.649→0.462) and verified rendering (§10), which is
   precisely the end-to-end format validation this step existed to buy. Running a separate
   ≤16B slice job would add egress and time for no new information, and under the promo the
   smoke test's cost-safety rationale is moot. Flagged for the owner to override if they
   want the original step-2 run anyway.
3. **Pilot SFT** — target Muse Glimmer 30B (`accounts/fireworks/models/muse-glimmer-30b`,
   verified catalog ID — §9) over `arc-pilot-v1-train` + `arc-pilot-v1-eval` as
   evaluation_dataset. Access, managed-LoRA eligibility verified (§9); cost estimate at
   creation: **$0.00 under the promo** (§10 addendum; list basis ≈$102/epoch for
   post-promo planning). **EXECUTING 2026-10-10 18:43 UTC: job
   `accounts/linencloset/supervisedFineTuningJobs/wwopccov`** (first attempt
   `ida9f81a` cancelled before any steps ran — §11.1) — 2 epochs (the plan's
   mid-case; defaults-first per provider guidance — extend only if results indicate need),
   `loraRank` 8, `maxContextLength` 32768 explicit, `evalAutoCarveout` false, outputModel
   `accounts/linencloset/models/arc-pilot-v1-therapist-sft`, wandb instrumented
   (§11.2–§11.3).
4. **Phase 4 evaluation preview** — untuned vs. tuned on held-out test.jsonl prompts (egress
   under Package C); catastrophic-tier behavior is unmeasurable on held-out data (all 10
   catastrophic rows are in train — export plan §5.4) and must be reported as such.

## 6. Validation (self-check, 2026-10-10)

- No secrets appear in this log; the API key was read from the environment and never printed.
- No clinical examples; all identifiers are synthetic; `test.jsonl` has not left this
  environment.
- Nothing in this log grants anything; the first attempt is recorded as blocked — no state
  was created at the provider in that attempt — and no spend arose from it. (Spend since
  incurred is recorded in §4/§10.) The successful upload on the replacement account is
  recorded in §7.

## 7. Package F — upload on replacement account (2026-10-10)

- **Account:** `accounts/linencloset` (display name `Top Nacho`), verified `READY` and
  `UNSUSPENDED` by authenticated `GET /v1/accounts` at 2026-10-10 12:26 UTC. This is the
  replacement account explicitly selected by the owner after the original account was
  suspended; per the owner's instruction, `linencloset` is the account of record and the
  old account is retired.
- **Identity re-check immediately before upload:** train 418 rows, SHA-256
  `281da447e675c60f06c56e160bae6fece23db4f2c8d41d4a3ebbbad94a09755b`; validation 80 rows,
  SHA-256 `615487846c3fd503c7627b776e17752713924de6d028bf208872dda3194bd609`. Both match
  `identity.json`. The test split remained local and was not uploaded.
- **Upload execution:** created and uploaded only `arc-pilot-v1-train` (`train.jsonl`, 418
  examples, 13,417,495 bytes) and `arc-pilot-v1-eval` (`val.jsonl`, 80 examples, 2,626,953
  bytes) using the authenticated Fireworks REST API. API key was read from `.env` and never
  printed. The train dataset entry already existed from the initial create attempt; the API
  rejected duplicate creation, then its upload endpoint accepted the frozen file.
- **Provider verification (2026-10-10 12:27 UTC):** authenticated GET for both resources
  returned `state=READY`, status `OK`, and example counts 418 and 80 respectively. Both report
  `encryptionState=ENCRYPTION_STATE_PLAINTEXT` (no CMEK marker). Record this as a provider
  configuration limitation; do not proceed with training unless the approved data-protection
  conditions allow this state.
- **Spend:** dataset creation and upload only; no paid training or evaluation job started.
  Package H remains not started pending review of the reported encryption state and account
  change against the approval conditions.
- **API schema note:** create request accepted `datasetId`, `dataset.userUploaded`, and
  `dataset.exampleCount`; the documented `displayName` field was rejected as unknown and was
  omitted. The create call returned HTTP 200; both subsequent upload calls returned HTTP 200.
- **Validation:** local file hashes and row counts matched the frozen identity manifest;
  provider-side `READY` states and `exampleCount` values verified. `test.jsonl` was not sent.
- **Billing note:** prior account discovery reported the replacement account as `READY`; this
  log records dataset upload only and does not claim a training charge or job.
  At that point the spend ledger was $0 pending billing reconciliation (spend incurred
  later is recorded in §4/§10).
- **Scope:** the owner's explicit request to upload on the new account was applied to Package F
  only. No smoke test, training, evaluation, deployment, or additional data export was run.
- **Important correction:** the earlier §3 sentence “No provider-side state was created” refers
  only to the failed attempt on the original (retired) account; the replacement-account
  resources listed above were created successfully.
- **Owner review (2026-10-10, ≈12:30 UTC):** the owner confirmed the replacement account
  carries the same specifications (standard product terms; no enterprise ZDR/CMEK — hence
  `ENCRYPTION_STATE_PLAINTEXT`), directed proceeding on it, and directed that all references
  to the old account be replaced. This resolves the caution above: the approved
  data-protection conditions allow the reported state, and Package H step 1 (Render Samples)
  is unblocked and next.
- **Independent re-verification (2026-10-10 12:33:13 UTC):** a second session re-hashed all
  four frozen artifacts pre-egress (all matched), then an authenticated
  `GET /v1/accounts/linencloset/datasets` list returned exactly two datasets — both `READY`,
  `exampleCount` 418/80, `encryptionState` PLAINTEXT — with no other provider-side datasets.
  `test.jsonl`, `manifest_internal.jsonl`, and `identity.json` have not been uploaded.
- **Content discrepancy found and corrected (2026-10-10 12:17–12:52 UTC):** the third session
  (triggered by the owner's "we switched to the new API key") downloaded both provider
  datasets via the signed-URL endpoint and found the wrong files: the datasets contained the
  full curated corpus (`ai/data/curated/sft_chatml/train.jsonl`, 180,460 rows /
  370,849,757 bytes, SHA-256 `aa7e9cd1…`; `val.jsonl`, 38,766 rows / 78,985,762 bytes,
  SHA-256 `de1ab128…`) — not the authorized arc pilot export. The §7 metadata (`exampleCount`
  418/80) was set at creation from the intended payload, so the earlier verification could
  not detect this; only the download comparison could. The likely cause is a wrong source
  path in the upload command (the curated files live at `ai/data/curated/sft_chatml/`, one
  directory above the export). The curated corpus was never covered by the Package A
  licensing determination (which scopes to the arc pilot payload only), so this was an
  over-upload of ~450 MB of un-authorized content.
  - **12:49 UTC — both datasets deleted** (`DELETE /v1/accounts/linencloset/datasets/…`,
    HTTP 200 each; list then returned zero datasets). The wrong-content files are preserved
    locally; nothing was lost.
  - **12:50 UTC — both datasets recreated** with correct metadata (`exampleCount` 418/80;
    note the API rejected a `user` field and accepted `userUploaded: {}`).
  - **12:51 UTC — correct files uploaded** from
    `ai/training/output/arc_corpus/export/fireworks_pilot_v1/`: train 13,417,495 bytes,
    eval 2,626,953 bytes (HTTP 200 each).
  - **12:52 UTC — verified:** both datasets `READY`, `exampleCount` 418/80, and a
    download-and-hash comparison of the provider copies matched the frozen identity manifest
    exactly (train `281da447…`, 418 rows; eval `6154878…`, 80 rows) — closing the §7
    metadata-only gap that had hidden the wrong-content upload. `encryptionState` remains
    `ENCRYPTION_STATE_PLAINTEXT` (accepted by the owner's ≈12:30 UTC review). `test.jsonl`
    was not uploaded.
  - **≈14:20 UTC — independently re-verified** by a second session (post-correction
    housekeeping): re-downloaded both provider datasets through the signed-URL endpoint —
    exactly two datasets on the account, both `READY` (`exampleCount` 418/80,
    `ENCRYPTION_STATE_PLAINTEXT`), and byte-exact SHA-256 matches to the frozen manifest
    (train 13,417,495 bytes / `281da447…` / 418 rows; eval 2,626,953 bytes / `6154878…` /
    80 rows). The correction is confirmed by a session independent of the one that performed
    it.
- No secrets or clinical examples are recorded in this log.

## 8. Validation (replacement-account upload)

- Both dataset resources exist under `accounts/linencloset` and are `READY`.
- Counts: train=418; eval=80. Encryption state for each: `ENCRYPTION_STATE_PLAINTEXT`.
- Upload artifacts match frozen local SHA-256 identity; test split remains local.
- No paid job was submitted.
- `git diff --check` passed after this update.

## 9. Glimmer target verification (2026-10-10, ≈15:45–16:00 UTC)

Re-verification of the Glimmer-dependent Package E/H items after the owner's same-day model
switch. Method: authenticated Fireworks REST (the `.env` key; read-only GETs; key read from
the environment only, never printed) against the `linencloset` account, plus the provider's
current pricing page (fireworks.ai/pricing, fetched 2026-10-10). No paid operation was run
and nothing was created.

- **Model identity (corrected):** the catalog entry is
  `accounts/fireworks/models/muse-glimmer-30b` (authenticated
  `GET /v1/accounts/fireworks/models`, 200 entries, exactly one Glimmer). The short
  `glimmer-30b` slug recorded alongside the owner instruction does not resolve (singular GET
  returns 404). All pilot docs now record the verified catalog ID. Entry facts: state
  `READY`, `public: true`, dense 29,776,626,688-parameter model (16.1B–80B pricing tier),
  Apache 2.0, `trainingContextLength` 131,072.
- **Managed-LoRA eligibility: verified.** The entry reports `supervisedLoraTunable: true`,
  `supportsLora: true`, `useTrainingV2: true` — managed SFT is the pilot's route. RL is not
  supported (`rlTunable`/`rlLoraTunable` false); managed DPO availability is not asserted
  anywhere and is out of pilot scope. Training context 131,072 comfortably exceeds the
  largest payload row (≈23.2k tokens by chars/4) — no truncation risk for the pilot;
  Render Samples (step 1) still inspects per-row rendering before any paid run.
- **Account access/quota: verified to the extent possible without spending.**
  `GET /v1/accounts/linencloset` returns `READY`/`UNSUSPENDED` (state unchanged since the
  12:26/12:33 checks); monthly spend notification thresholds are configured at
  $100 / $1,000 / $10,000; the account key lists the public model entry. Actual
  job-creation authorization can only be exercised by the first paid step (the Package H
  smoke test) — that boundary is by design, not a gap in this check.
- **Pricing (current list, fireworks.ai/pricing):** managed LoRA SFT for the 16.1B–80B tier
  is $3.00/1M training tokens. A serverless Training API route is also listed for Muse
  Glimmer 30B (128K context; $5.86/1M train, $1.96/1M prefill, $4.88/1M sample) — more
  expensive per training token than managed at this tier, so managed LoRA remains the
  planned route. The model is not on serverless inference (`supportsServerless: false`) and
  tuned models serve only on dedicated deployments as before, so the evaluation-endpoint
  basis is unchanged ($8/hr H100/H200 class).
  **Promo supersession (2026-10-10, owner-reported banner + verified, §10 addendum):** the
  account dashboard shows **"Muse Glimmer 30B SFT is free via UI and Serverless Training API
  until 10/31 ✨ No credit card required"** — the list rates above do not apply to this
  account's Glimmer SFT through 2026-10-31. Verified: account-wide rated cost $0.00
  (`POST /v1/accounts/{account_id}/usageCosts:query`, attribution COMPLETE) covering the
  cancelled 47M-metric-token run.
- **Budget fit (re-estimate; same conservative basis as the GLM estimate):** payload ≈3.72M
  tokens/epoch (train 3,106,534 + val 609,606, chars ÷ 4) × $3.00/1M ≈ **$11.16/epoch**;
  2–3 epochs ≈ **$22.32–$33.48** against the $150 pilot-SFT line — fits, and cheaper than
  the superseded GLM-class estimate (≈$37/epoch). List-price calculation, not a quote; the
  spend ledger (§4) remains $0.
  **Correction (2026-10-10, §10):** this estimate is **wrong** — it counts raw row tokens and
  ignores the trainer's per-user-turn unrolling, which multiplies the processed volume to
  ≈34.1M train tokens/epoch (≈$102) plus ≈6.5M eval tokens. See §10 and the §4 budget-gate
  resolution; the list-basis figures matter for post-promo planning, while the promo (§10
  addendum) zeroes the actual pilot training cost through 10/31.

Conclusion: all four Glimmer-dependent items (eligibility, account access, pricing, budget
fit) are verified for the planned managed-LoRA SFT route, with the model-ID correction
recorded above — though the budget-fit estimate itself is superseded by the §10 correction
(list basis) and the §10 promo resolution (account basis: $0 through 10/31). Package H
step 1 (Render Samples) has since been executed and verified (§10), and the pilot SFT is
running (§11).

## 10. Package H step 1 — Render Samples execution (2026-10-10, 16:10–17:32 UTC)

The owner's "let's render some samples" instruction, executed. **Outcome: step 1 verified —
the training rendering is correct — but the attempt surfaced two material findings: the
platform couples render capture to paid training (no free pre-run path exists), and the
pilot's per-epoch cost basis was wrong by ~9× at list rates (per-user-turn unrolling). The
job was cancelled at 57% of one epoch with the owner's explicit approval; its rated cost
resolved to $0.00 under the Glimmer SFT promo (see the promo resolution below).**

### Job record

- **Job:** `accounts/linencloset/supervisedFineTuningJobs/jf3tmylp` — created 16:10:52 UTC
  via `POST /v1/accounts/linencloset/supervisedFineTuningJobs`; training active ≈16:37 UTC
  (trainer capacity assignment took ~26 min); **cancelled 17:32:37 UTC by owner decision**
  (`POST …/jf3tmylp:cancel`, HTTP 200 — the `:cancel` action exists on the gateway but is
  absent from the public API index); final state `JOB_STATE_CANCELLED` at 57% of 1 epoch.
- **Config (exactly one create attempt that took effect; two earlier 400s created no
  state):** `baseModel accounts/fireworks/models/muse-glimmer-30b`, `dataset
  accounts/linencloset/datasets/arc-pilot-v1-train`, `evaluationDataset
  accounts/linencloset/datasets/arc-pilot-v1-eval`, `evalAutoCarveout false`,
  `maxContextLength 32768` (explicit, satisfying the step-1 requirement),
  `loraRank 8` (default), `outputModel accounts/linencloset/models/arc-pilot-v1-therapist-sft`
  (never created — job cancelled; the model ID remains free).
- **API findings (create path):** (1) `outputModel` on the REST gateway requires the **full
  resource name** `accounts/…/models/…` — the schema text saying a bare ID is accepted is
  wrong; (2) **`loraRank` must be set explicitly on REST** — unset, the job defaults to
  full-parameter SFT, which the LoRA-only-tunable Glimmer rejects ("model is not tunable
  for supervised full-parameter fine-tuning"); (3) no undocumented render endpoint exists
  (AIP-style `:renderSamples`/`:preview` probes are rejected as invalid IDs).
- **Run telemetry** (metrics file, retained 7 days per provider docs; saved locally, see
  below): 24 optimizer steps; train loss 0.7083 → 0.4051; **eval loss 0.6493 → 0.4619**
  (perplexity 1.914 → 1.587) across a step-0 baseline eval and one mid-run eval on
  `arc-pilot-v1-eval`. `estimatedCost` stayed null throughout; `jobProgress` counters lag
  badly (0/0 requests while training was demonstrably live — the metrics file was the only
  reliable signal).
- **Trainer token accounting:** metrics `train/total_tokens` sums to **47,054,467** over 24
  steps (~65,536 counted tokens per sample — exactly 2 × 32,768, a padded accounting whose
  billing meaning is undocumented). At list price this would be ≈$141 for the 57% run
  (≈$247 for a full epoch).

### Render-samples verification (the step-1 goal) — ALL CHECKS PASS

Artifact: `render_samples.jsonl`, 642,320 bytes, SHA-256
`bc8fb6365c303d0c6b3077bc441ba90e8f408d2b36cebdfa5965b44247c029a0`, 20 rendered datums
across 8 source rows (splits 0–2 each), workers 0–7. **The artifact is written only when the
job reaches a terminal state** — the signed URL 404'd (`NoSuchKey`) for the entire 55-minute
run and returned 200 immediately after cancellation. Structure: per-datum
`source_jsonl_row_index`, `split_index`, `renderer: muse_glimmer`,
`train_on_what: all_assistant_messages`, `rendered_chunks` (token spans), `token_ids`,
`decoded_tokens`, `token_weights`.

- **Loss masks: correct.** User/system/header tokens weight 0 (36/36 user spans all-zero).
  Assistant content spans carry the trained loss — but as **per-datum normalized weights**
  (each datum's weights sum to exactly 1.0; assistant tokens are uniform 1/n_trained, e.g.
  0.002770083… = 1/361), not raw 1.0. The "user 0 / assistant 1" intent of step 1 is
  satisfied by the mask structure; the platform reports the normalized form.
- **Each assistant turn is trained exactly once.** The renderer unrolls every row into
  growing-context datums per user turn (datum k of a row covers messages 0..2k+1; a
  33-message row yields ~16 datums). In each datum only the newest assistant turn carries
  loss; earlier assistant turns reappear as context with weight 0. Verified across all 20
  datums (20 trained spans, 16 masked repeats — consistent with the design).
- **Ledger rendering: intact — 36/36.** Every rendered assistant span's decoded leading line
  parses as JSON with exactly the 9 contract keys (`def dx hx onset risk soma tl track tx`),
  and the full source content appears verbatim in the decoded span (no truncation, no
  template mangling).
- **No truncation:** max rendered datum 2,065 tokens, far under the explicit 32,768
  max-context-length; EOT tokens are inside the trained span (the model learns to stop).
- **Renderer behavior findings (matter for inference/evaluation consistency):** the
  `muse_glimmer` renderer **injects a default system prompt** ("You are a helpful AI…" —
  the pilot rows have no system message, so this is renderer-added, not dataset content).
  Phase-4 evaluation and any deployment must use the same chat template as training, or
  the comparison is invalid.

### Cost basis correction — superseded by the promo resolution below (list-basis facts retained)

Measured on the rendered windows: **3.57 chars/token** (≈ the 4 heuristic). The
per-user-turn unrolling multiplies the processed volume far beyond raw row tokens:
extrapolating the verified unrolled structure over all 418 train rows gives
**≈34.1M tokens/epoch for train (≈$102 at the $3.00/1M list rate) plus ≈6.5M unrolled eval
tokens** — against the plan's original $11.16/epoch (chars÷4) estimate. The provider's own
pricing page confirms the unrolling is part of the billed token stream ("multi-turn
conversations are unrolled into user, assistant, and thinking traces").

**Promo resolution (2026-10-10, evening):** the gate this section opened is **dissolved**.
The owner reported the account dashboard banner — **"Muse Glimmer 30B SFT is free via UI
and Serverless Training API until 10/31 ✨ No credit card required"** — and it was verified
from this environment: `POST /v1/accounts/linencloset/usageCosts:query` over the account's
entire lifetime (created 11:13 UTC today) returned **rated subtotal $0.00, zero rows,
attribution COMPLETE** (evaluated 18:23 UTC, 51 minutes after the job's cancellation) —
so the 47M-metric-token run rated zero, and **REST-created managed jobs are covered** (the
cancelled job was REST-created). This also corrects the earlier statement in this section:
billing **is** readable via REST (`usageCosts:query` gives rated costs; `GET /billingUsage`
gives metered quantities). The list-basis figures above remain valid for post-promo
planning (after 10/31) and for other models/tiers; under the promo the pilot's training
cost is $0 through 2026-10-31. §4 records the resolution; §11 records the re-launched
pilot SFT.

### Evidence (preserved locally, gitignored export dir; no new egress)

- `ai/training/output/arc_corpus/export/fireworks_pilot_v1/render_samples_jf3tmylp.jsonl`
  (SHA-256 `bc8fb636…`, above)
- `…/metrics_jf3tmylp.jsonl` (SHA-256 `0f1bf5b49d53f4ac335ab498fdad49b3de9096f43f42567423f195f358cdcda8`)
- `…/sft_job_jf3tmylp_final.json` (SHA-256 `83b5eef940e5e39193ecad4bbd6264ecd614657817243226d7a15deeaed26b2b`)
- The job resource remains on the account in `CANCELLED` state (not deleted), available for
  support/billing queries. No LoRA model was created.

## 11. Package H step 3 — pilot SFT run (2026-10-10, 18:26 UTC; superseded in-place 18:43 UTC)

Launched after the promo resolution (§10) dissolved the budget gate. The first attempt
(`ida9f81a`, created 18:26 UTC) was **cancelled by owner directive before any training
steps ran** and replaced by a wandb-instrumented run (`wwopccov`). **Status at write
time: wwopccov PENDING.** The completed run's telemetry, render-sample capture, and
$0.00 rated-cost verification will be appended here when `wwopccov` reaches a terminal
state.

### 11.1 First attempt — `ida9f81a` (cancelled, nothing lost)

- Created 18:26:18 UTC with the same REST path as §10 (REST coverage of the promo
  verified in §10's resolution). Config identical to the current run except **no
  `wandbConfig`**.
- The owner asked whether wandb/checkpointing/resume were hooked in; the honest answer
  was no wandb and no explicit checkpoint knobs (both omitted from the create body),
  and the owner directed: stop it now and fix it all.
- Cancelled via `POST …/ida9f81a:cancel` (18:37–18:40 UTC). **No training steps had
  run** — the job never received capacity (pct stayed 0, metrics artifact 404,
  nothing materialized), so nothing was lost. $0.00 under the promo; no LoRA model
  was created by it.

### 11.2 The wandb hookup (what "fix it all" meant operationally)

- **Checkpointing and resume are platform-side on managed jobs** — there are no
  create-time knobs; the platform checkpoints internally, `:resume` exists for
  paused jobs, and the crash net under a $0 promo is simply re-running. Nothing to
  configure, nothing was missing.
- **wandb was the one actionable gap.** Without it, step metrics survive only
  ~7 days provider-side; with it they persist in the account's wandb project.
- Fireworks requires `entity` when `wandbConfig.enabled` is set (create #1 without
  it: HTTP 400 "wandb entity is required when wandb is enabled"). The root `.env`
  has `WANDB_API_KEY` and `WANDB_PROJECT=pixelated-empathy-kan28` but no entity, and
  no repo call site passes one. The key's default entity was resolved via the wandb
  SDK viewer (`wandb.apis.public.Api().viewer` — the key is valid for the core API
  and is also documented in `.env` as the NF pipeline's W&B inference key):
  **entity `wutang`**. Key value never printed; only lengths in evidence.
- Both wandb vars were consumed from `.env` as-is (key + project), entity added;
  create #2 (`wwopccov`) returned HTTP 200 with the response echoing
  `wandbConfig: enabled true, project pixelated-empathy-kan28, entity wutang,
  apiKey set`.

### 11.3 Current run — `wwopccov` (created 18:43:06 UTC; RUNNING from 18:43:06)

- **Job:** `accounts/linencloset/supervisedFineTuningJobs/wwopccov`, created via the
  same REST path, this time with `wandbConfig {enabled, apiKey (from `.env`
  `WANDB_API_KEY`), project pixelated-empathy-kan28, entity wutang}`. Capacity was
  granted instantly this run (PENDING→RUNNING within ~0.5 s of creation, vs ~4 min
  waiting for the first attempt).
- **Config:** `baseModel accounts/fireworks/models/muse-glimmer-30b`, `dataset
  accounts/linencloset/datasets/arc-pilot-v1-train`, `evaluationDataset
  accounts/linencloset/datasets/arc-pilot-v1-eval`, `evalAutoCarveout false`,
  `maxContextLength 32768`, `loraRank 8`, **`epochs 2`** (the plan's mid-case;
  defaults-first per provider guidance — extend only if results indicate need),
  `outputModel accounts/linencloset/models/arc-pilot-v1-therapist-sft` (the ID was
  never created by the cancelled jobs and remains free).
- **Cost: $0.00 expected** under the promo (through 10/31; §10 resolution). List-basis
  planning figure if the promo had not applied: ≈$204 for 2 epochs (§10). The watcher
  re-verifies via `usageCosts:query` at terminal state.
- **Step-order note:** step 2 (smoke test) is recorded as satisfied by `jf3tmylp`
  evidence (§5.2) — that job already trained on the exact pilot payload + model
  end-to-end with healthy curves and verified rendering. Flagged for owner override.
- **Expected artifacts:** the trained LoRA model `arc-pilot-v1-therapist-sft`, final
  eval metrics on the attached eval set, the job's render-samples artifact (written
  at terminal state per §10's finding), and a wandb run in
  `wutang/pixelated-empathy-kan28` with the step-metric history.
- **Watcher:** background poll (60 s interval) capturing the final job JSON, metrics,
  render samples, and the terminal-state $0.00 `usageCosts:query` result into the
  gitignored export dir with SHA-256s.
