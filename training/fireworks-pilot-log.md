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
| Package G spend | cap $635 active; **$0.00 actual** — all three SFT jobs (`jf3tmylp`, `ida9f81a`, `wwopccov`) rated $0.00 (promo verified at completion via `usageCosts:query`, §11.4) |
| Package H experiment | **step 1 (Render Samples) EXECUTED and verified** (§10); **budget gate DISSOLVED** — Glimmer SFT promo (free until 10/31, §10); **step 3 pilot SFT COMPLETED** — job `wwopccov`, 2 epochs, eval loss 0.649→**0.430**, LoRA model `arc-pilot-v1-therapist-sft` READY, $0.00 (§11.4) |

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
| 2026-10-10 | SFT job `wwopccov` (step-3 pilot SFT, 2 epochs, wandb-instrumented, §11.3–11.4) | $0.00 under promo | **$0.00** — verified at completion (`usageCosts:query`: 0 USD, zero rows, attribution COMPLETE) | $0.00 |

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
   post-promo planning). **COMPLETED 2026-10-10: job
   `accounts/linencloset/supervisedFineTuningJobs/wwopccov`** (first attempt
   `ida9f81a` cancelled before any steps ran — §11.1) — 2 epochs (the plan's
   mid-case), `loraRank` 8, `maxContextLength` 32768 explicit, `evalAutoCarveout`
   false, outputModel `accounts/linencloset/models/arc-pilot-v1-therapist-sft`
   (READY), wandb instrumented. Eval loss 0.649→**0.430** (ppl 1.914→**1.537**),
   no overfit at 2 epochs; $0.00 verified (§11.4).
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
steps ran** and replaced by a wandb-instrumented run (`wwopccov`). **Status: `wwopccov`
COMPLETED 20:08:06 UTC** — final telemetry, verification, and $0.00 rated-cost record
in §11.4 below.

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

### 11.4 COMPLETED — `wwopccov` final telemetry (20:08:06 UTC; run time ≈ 85 min)

**Outcome: JOB_STATE_COMPLETED, 2 epochs, $0.00 rated.** The trained LoRA model
`accounts/linencloset/models/arc-pilot-v1-therapist-sft` is **READY** (verified via
GET). The wandb run `wwopccov` (entity `wutang`, project `pixelated-empathy-kan28`)
shows state **finished** with the full step history streamed (created 18:43:28 UTC).

- **Curves (28 optimizer steps — 14/epoch; eval at steps 0/14/28):**
  - train loss 0.7083 → **0.3706** (final train ppl 1.449)
  - eval loss 0.6493 → 0.4617 (end of epoch 1) → **0.4298** (end of epoch 2)
  - eval ppl 1.914 → 1.587 → **1.537**
  - Epoch 2 continued improving (0.4617 → 0.4298): no overfit signal at 2 epochs;
    the curve suggests room for further epochs if a later decision wants them
    (still free under the promo until 10/31).
  - Cross-check: the epoch-1 eval loss (0.4617) matches the cancelled `jf3tmylp`'s
    final eval loss (0.462 at 57% of 1 epoch) — consistent data + config.
- **Metric tokens:** 53,153,680 train metric tokens total ≈ the padded-per-row basis
  (418 rows × 65,536 padded tokens × 2 epochs ≈ 54.8M; §10's 2× `maxContextLength`
  finding). The provider's per-step token counts are consistent across both jobs
  (≈1.9M tokens/step); cross-job pct denominators are not comparable.
- **Render-sample artifact (20 datums across 8 source rows — the same per-user-turn
  unrolling as §10):** renderer `muse_glimmer`, `train_on_what all_assistant_messages`;
  every datum's loss weights sum to exactly **1.0000** (normalized), user/system-side
  chunks masked to 0; max datum 2,065 tokens of the 32,768 limit (no truncation).
  8 distinct source rows rendered as 20 datums (rows 133/206/231/289/310/352/386/415).
- **Cost: $0.00 verified at completion** via `POST /v1/accounts/linencloset/usageCosts:query`
  (`start_time 2026-10-10T00:00:00Z`, `end_time 2026-10-11T00:00:00Z`, `scope ACCOUNT`,
  `group_by ["MODEL"]`): **subtotal 0 USD, zero rows, attribution COMPLETE** —
  covering `jf3tmylp` + `ida9f81a` + `wwopccov`. (API shape pinned: `start_time`,
  `end_time`, `scope` enum, non-empty `group_by` are all required.)
- **Evidence preserved (gitignored export dir, SHA-256):**
  - `sft_job_wwopccov_final.json` — `55d04b4e303c05c4cbf5e2f457d4e0f66824a69afcca068975f05469c86b608c`
  - `metrics_wwopccov.jsonl` — `d59a112d3d6324befd61c27a679e06644004ba03010c192e38c1bd728afb7874`
  - `render_samples_wwopccov.jsonl` — `bc8fb6365c303d0c6b3077bc441ba90e8f408d2b36cebdfa5965b44247c029a0`
- **Step 3 of Package H is complete.** Remaining pilot work: Phase-4 evaluation
  (untuned vs. tuned on held-out `test.jsonl`, §5.4), path decided below (§12).

## 12. Phase-4 evaluation path — owner decision: fully local (2026-10-10, 23:50 UTC)

The owner chose **off-platform local inference** for Phase 4 ($0; the authorized ≤$480
deployment line stays unused). Scoping found two hard blockers, both recorded here with
their unblock routes.

### 12.1 Blocker A — adapter download is restricted on this account

- `GET /v1/accounts/linencloset/models/arc-pilot-v1-therapist-sft:getDownloadEndpoint`
  → HTTP 400, code 9: **"model downloading is restricted, please contact Fireworks AI
  to get access."** The API path exists (§10's feasibility note was correct) but this
  account lacks the entitlement.
- **Unblock routes (both live):** (1) support request — draft below, ready to paste;
  (2) the owner checks the console UI for a download path when logged in (the API
  gate may not reflect the console).
- Everything else for the local path is staged and ready (§12.3); only the weights
  are gated.

### 12.2 Blocker B — no GPU in reach

- This workstation (`vivi`'s box): 4 CPU cores, 15 GiB RAM, **no GPU** (`nvidia-smi`
  absent), 52 GiB free disk. `headrush` (5.78.155.224, Hetzner; reachable via
  key-auth SSH): identical shape — no GPU, 15 GiB RAM, 4 cores.
- A 30B model is infeasible on both: BF16 needs ~60 GB (no GPU); q4 GGUF ~18 GB
  exceeds RAM and would page-thrash at ~0.1 tok/s (days per eval pass); q2 fits but
  destroys quality so badly the eval would measure the quant, not the fine-tune.
- **Unblock route:** the owner points at a GPU box ("then we run on a GPU you point
  me to"). Requirements to state up front: **≥24 GiB VRAM** for q4/q5 with
  llama.cpp/vLLM (workable), **≥2×48 GiB or 1×80 GiB** for BF16 (faithful); disk
  ~20 GB (q4) to ~60 GB (BF16); the repo, the adapter, and
  `muse_glimmer_template.json` travel by git + download.

### 12.3 Staged and verified now (hardware-independent)

- **Chat template pinned** to `ai/qa/validation/therapy_bench/muse_glimmer_template.json`:
  BOS `<|begin_of_text|>`; turns `<|start|>{role}[ to=user]<|message|>…<|eot|>`;
  the renderer's injected system prompt (knowledge cutoff 2026-01-04, **dynamic
  date stamp** — training saw 2026-10-10; pin the date for eval comparability;
  "Reasoning strength: high"; "# Valid recipients: "self", "user""), generation
  prefix `<|start|>assistant to=user<|message|>`, stop `<|eot|>`. Exactly one distinct
  system prompt and one assistant-header form across all 20 datums.
- **Deterministic-rendering finding:** the `jf3tmylp` and `wwopccov` render-sample
  artifacts are **byte-identical** (same SHA-256 `bc8fb636…c029a0`) — the renderer
  is fully deterministic given (dataset, renderer, template, date stamp). Local
  prompting can therefore reproduce the provider's exact training-time format.
- **Harness ready:** `ai/qa/validation/therapy_bench/therapy_bench.py` — deterministic
  offline heuristic judge (empathy/safety/reflection), `GenerativeModel` protocol
  (`generate(prompt) -> str`); the local server wrapper is a thin client.
- **Base model staged:** HF `meta-models/Muse-Glimmer-30B` public, ungated (13 files).
- **Held-out set local:** `test.jsonl` — 78 rows, 2.6 MiB, multi-turn dialogues
  (row 1: 48 turns, user/assistant alternating, turns up to ~2.1k chars).

### 12.4 Support request — ready to paste (owner sends)

> **To:** Fireworks AI support
> **Subject:** Request model download access — account `linencloset`
>
> We'd like to download a fine-tuned model from our account for local inference and
> artifact portability.
>
> - Account: `accounts/linencloset` (display name "Top Nacho")
> - Model: `accounts/linencloset/models/arc-pilot-v1-therapist-sft` — LoRA (rank 8),
>   base `accounts/fireworks/models/muse-glimmer-30b`, trained via managed SFT job
>   `wwopccov` (completed 2026-10-10, `JOB_STATE_COMPLETED`)
> - Current behavior: `GET /v1/accounts/linencloset/models/arc-pilot-v1-therapist-sft:getDownloadEndpoint`
>   returns HTTP 400 code 9: "model downloading is restricted, please contact
>   Fireworks AI to get access"
> - Request: enable the model-download entitlement for this account so
>   `:getDownloadEndpoint` / `firectl model download` work for our own fine-tunes.
>
> Purpose is evaluation on our own infrastructure; the artifact is our own fine-tune
> of the public Apache-2.0 base `meta-models/Muse-Glimmer-30B`.

### 12.5 Open design questions for the run (when compute lands)

- **Input protocol:** `test.jsonl` rows are full multi-turn dialogues; therapy_bench
  consumes golden questions (`id/category/prompt/expected_behavior`). Adapter needed:
  candidate — `prompt` = dialogue rendered through the last user turn (under a
  context budget), `expected_behavior` = the reference assistant turn, `category`
  mapped from the row's ledger/tier tags where available.
- **Both arms identical:** untuned = base model + the SAME pinned template + same
  generation params as tuned; pinned date stamp in both.
- **Catastrophic-tier caveat stands** (§5.4 / packages §"must say so explicitly"):
  all 10 catastrophic rows are in train — held-out eval cannot measure that tier and
  the report must say so.
- Judge driver: the harness default (`heuristic`, offline, deterministic).

## 13. Adaption Labs credits — option scan and pending owner decisions (2026-10-11)

The owner surfaced **free credits on Adaption** (`docs.adaptionlabs.ai`) and asked how
best to use them. Platform scanned (public docs only; **nothing uploaded, nothing run,
no account access yet** — no `ADAPTION_API_KEY` in this environment). Recorded here so
the analysis survives the session; the Foresight memory carries the same.

- **Products:** (1) **Adaptive Data** — import (jsonl/csv/parquet/HF/Kaggle) → column
  mapping (prompt/completion/context/image/chat) → recipes (dedupe, rephrase, reasoning
  traces) → expand (augment/translate/localize) → brand controls → adapt + evaluate
  (quality signals source-vs-adapted; **free credit estimate before every run**,
  `estimate=True`). (2) **AutoScientist** — automated loop: data optimization →
  training (SFT or SFT→DPO "alignment"; LoRA r 1–64 or full) → eval vs
  `target_win_rate` → hyperparameter revision; best checkpoint is **downloadable**
  (no restriction — unlike our Fireworks entitlement blocker, §12.1).
- **Hard constraints:** Muse-Glimmer-30B is **not** in their model list → any run
  there is a **parallel track, not an A/B** with the Fireworks pilot. Row minimums:
  SFT 1,000 (all models), **10,000 for the 30B-class bases** (Gemma ≥26B, Qwen ≥35B,
  NVIDIA), DPO 12,000; 20K recommended. Our corpus (418 train / 80 val / 78 test =
  576 rows) is below every usable-model floor → **expansion is a prerequisite**.
  No inference-serving product → Phase-4 eval compute is NOT solved by this.
- **Strategy as proposed (pending owner decisions):**
  1. Parallel therapist-model track on AutoScientist — the strategic prize is
     **weights portability** (breaks both Fireworks dependencies at once: the
     download-entitlement blocker and post-10/31 training cost). Candidate bases:
     `Qwen/Qwen3.6-35B-A3B` (MoE, 3B active → local inference feasible even on
     CPU-class hardware — relevant since no GPU is currently in reach, §12.2) or
     `google/gemma-4-31B-it` (closest class match to Glimmer).
  2. Optional cheap Adaptive Data evaluation pass on the arc corpus (independent
     second opinion to our own validators; estimates are free).
  3. DPO/alignment stage later (roadmap stage not yet built; needs ~12K preference
     pairs first).
  4. Expansion path preference: **our own arc pipeline expands (clinical governance,
     ledger discipline), Adaption trains** — their augmentation is fast but
     synthetic-of-synthetic; any augmented rows must clear the clinical review gate.
- **Egress note:** the arc corpus is synthetic/no-PHI, but the packages C–E approval
  covered **Fireworks** — Adaption is a **new third-party processor**; the owner's
  go-ahead on this question is the sign-off.
- **Pending owner actions/decisions:** ~~create an API key~~ **DONE 2026-10-11** (added to
  the root `.env` as `ADAPTION_API_KEY`; value never printed in logs/docs); state the
  credit amount (see below); egress sign-off; base-model pick; expansion path; credit
  budget for the run.

### 13.1 API verification (2026-10-11, read-only probes)

- **SDK works:** `pip install adaption` verified via `uv run --with adaption`
  (ephemeral dependency — the repo lockfile is untouched); client constructs from
  `ADAPTION_API_KEY`. Note: the `.env` is not shell-sourced in agent contexts —
  scripts must read/export the variable explicitly.
- **Runtime model list (authoritative, 19 models — same set as the docs page):**
  both strategy candidates are live — `google/gemma-4-31B-it` (31B, sft/dpo,
  **lora+full**, model context 262,144) and `Qwen/Qwen3.6-35B-A3B` (35B MoE A3B,
  sft/dpo, lora, model context 262,144). Also present: gpt-oss-20b/120b, Llama 3.3
  70B (lora+full), Llama 4 Scout 109B, Nemotron 3 30B-A3B/120B-A12B, Qwen 3.5
  family, Gemma 3 family. Caveat carried over: the docs' per-model **"Context (SFT)"
  column (e.g. 49,152 for Gemma 4 31B) is the training-context cap that actually
  applies to rows** — the runtime `context_length` is the model's serving context.
- **`autoscientist` surface:** `create / get / list / cancel / wait_for_completion /
  download / list_models / recommend_hyperparams` — the latter is worth consulting
  before pinning the run config.
- **Credit balance is NOT API-exposed** (404 on `/credits`, `/v1/credits`, `/user`,
  `/account`; no SDK resource): balance is **app-dashboard-only**. The owner reads
  the amount there; every Adaptive Data run quotes `estimated_credits_consumed`
  for free via `estimate=True` before spending anything.
- **No data has been uploaded and no run has been started** — the egress sign-off
  (§13) gates the first upload. Next concrete step after sign-off: upload the
  corpus (`.jsonl`, `processing_mode="raw"` per the AutoScientist quickstart if
  training-ready, or through Adaptive Data first) and request the free estimate.

### 13.2 Local inventory + upload shape — findings that reshape the model pick (2026-10-11)

- **Upload format solved — zero transformation needed:** Adaption's Adaptive Data
  has a native **`chat` column mapping** (`column_mapping={"chat": "messages"}`)
  for OpenAI-style multi-turn rows; prompt/completion are derived by the platform.
  Our `train.jsonl` rows (`{"messages": [ {role, content}, … ]}`) are that exact
  shape. (Verify at upload time how multi-turn rows are split — last-turn vs
  per-turn derivation — the same question the `muse_glimmer` renderer answered
  per-user-turn for Fireworks.)
- **DPO inventory already exists in Adaption's exact schema:** `arc_dpo_pairs.jsonl`
  — **693 pairs** with `prompt`/`chosen`/`rejected` (+ defect-tagged metadata,
  `pair_hash`), generated by the arc pipeline's failed-attempt mode. Adaption's
  DPO floor is 12,000 rows → a ~17× expansion job for the pair generator if/when
  the alignment stage goes to Adaption. Format compatibility: confirmed.
- **Corpus sizes vs Adaption floors (this reshapes the §13 model pick):**
  - Local corpus: 235 arc records (`arc_records.jsonl`, 19.7 MB — long multi-turn
    rows); export = 576 rows (418 train / 80 val / 78 test).
  - SFT floor for **1,000-min models**: we are at 42% of the floor (418/1,000) —
    expansion or augmentation is modest (~580 rows).
  - SFT floor for **10,000-min models** (Gemma 4 31B, Qwen 3.6 35B-A3B, Nemotron,
    Qwen 3.5 122B): 4.2% — a ~24× expansion, real pipeline work.
- **Model-pick tradeoff table (floors vs local-inference profile):**
  | Candidate | Min rows | Local inference profile |
  |---|---|---|
  | `openai/gpt-oss-20b` | 1,000 | MoE ~3.6B active — runs on modest hardware (q4 ≈12 GB); reasoning training supported |
  | `meta-llama/Llama-3.3-70B-Instruct-Reference` | 1,000 | Dense 70B — needs a real GPU (≥48 GB VRAM q4); lora+full |
  | `openai/gpt-oss-120b` | 1,000 | MoE A5B — CPU-viable per OpenAI's targets, larger download; reasoning training |
  | `Qwen/Qwen3.6-35B-A3B` | 10,000 | MoE 3B active — best CPU-class story, but 24× corpus expansion prerequisite |
  | `google/gemma-4-31B-it` | 10,000 | Class-comparable to Glimmer; lora+full; same 24× expansion prerequisite |
- **`recommend_hyperparams` requires an uploaded `dataset_id`** (it sizes against the
  dataset's effective training size and launches nothing) — so the recipe
  recommendation itself is egress-gated; sequence: upload → estimate → recommend →
  decide → run.

### 13.3 Owner decisions + zero-cost execution (2026-10-11)

**Owner decisions (all six):** (1) Fireworks support request **sent**; (2) GPU box —
deferred until the adapter downloads; (3) **egress to Adaption signed off**; (4) model
pick: **`Qwen/Qwen3.6-35B-A3B`**; (5) expansion path: **arc pipeline expands,
Adaption trains** (recommendation followed); (6) credit budget: **estimate first**,
then decide.

**Executed with zero credits spent:**

- **Dataset A** (`adb7d8eb-a3c9-434a-aea0-c4a6a7b8a788`) — `train.jsonl` dialogues,
  418 rows, `awaiting_input`. **Adaptive Data adapt estimate: 5 credits / 16 min**
  (chat mapping `{"chat": "messages"}` validated by the estimate call).
- Raw mode **rejects chat mapping** (requires explicit `prompt` + `completion` or
  `chosen`/`rejected` columns) → performed the **local unroll** locally: per-assistant-turn,
  mirroring the `muse_glimmer` per-datum training semantics (prompt = chat-turn array
  through the preceding user turn; completion = the assistant turn verbatim, structured
  notes intact). **418 dialogues → 6,951 datums** (110 MB) — every assistant turn
  trained exactly once, same as the Fireworks renderer does.
- **Dataset B** (`02e1331f-ff62-4f01-bf03-1df439c62fbd`) — the unrolled set, raw,
  6,951 rows, **`succeeded` — training-ready**, upload + processing free.
- **`recommend_hyperparams` for Qwen3.6-35B-A3B:** at 6,951 rows without augmentation
  → HTTP 400, explicit floor error ("cannot be used… fewer than 10000 effective
  training rows"). Bridged via their augmentation (+3,049 domain, +6,667 general =
  16,667 effective) → **validates**, recommended recipe: LoRA **r 8 / α 8** on
  `q_proj,v_proj`, lr 1e-4 cosine, warmup 0.1, **1 epoch**, batch `max`,
  `train_on_inputs false` — strikingly close to the Fireworks pilot config (loraRank 8,
  lr 1e-4), a useful independent confirmation.
- **Cost-control levers on `autoscientist.create`:** `max_iterations` (hard spend cap
  on the loop), `target_win_rate` (early stop), `voucher`, `idempotency_key`. **No
  pre-run cost quote exists for AutoScientist runs** — only Adaptive Data has the
  estimate endpoint; the run's credit cost is observable at create/first iteration.

**Reshaped expansion math (material):** the unroll changes the floor gap from ~9,582
rows (dialogue basis) to **3,049 datum rows**. Options for the owner:
- (a) **AutoScientist's own augmentation bridges it in-run** (+3,049 domain rows it
  synthesizes — synthetic-of-synthetic; the clinical review gate applies to anything
  its artifact trains on), plus the recommended 40% general-purpose mix (+6,667).
- (b) **Arc pipeline expansion is now a ~7× smaller job** than scoped pre-unroll:
  ~3,049 datum-equivalents ≈ ~185 more dialogues at the observed 16.6 datums/dialogue.
  The owner's standing decision (arc pipeline expands) now costs a fraction of the
  original estimate — or can be revisited given (a) exists.
- val/test splits and `arc_dpo_pairs.jsonl` were **not** uploaded (held-out discipline;
  test stays strictly local for Phase-4).

**Next owner inputs:** ~~augmentation vs arc-expand; run caps; balance~~ — **delegated
to the agent 2026-10-11 ("you decide the best options here")**; decided and executed
(§13.4).

### 13.4 Run-1 decisions + launch (2026-10-11, 10:52 UTC; agent-decided per owner delegation)

**The decisions, with reasons:**

1. **Gap bridge: AutoScientist's in-run domain augmentation (+3,049 rows), minimum
   effective size, NO general mix** — validated for free via `recommend_hyperparams`
   (exactly 10,000 effective passes the floor check). Reasons: (a) the arc-pipeline
   expansion, while clinically governed, is a multi-session generation job on the NF
   inference budget — it would delay the parallel track's whole point (a portable
   artifact) by days; (b) in-run augmentation is synthesized FROM our uploaded corpus,
   so it inherits the real dialogues' style and format; (c) run 1 is a probe, not a
   production candidate — minimum size = minimum compute = minimum credit exposure
   under an unknown balance. The general-purpose mix (~6,667 rows, "strongly
   recommended" for diversity) is deferred to a quality run if run 1 justifies one.
   **Caveat stands:** the +3,049 synthetic rows mean this artifact is NOT
   clinically-governed training data — the parallel-track checkpoint must clear the
   clinical review gate before any clinical promotion, same as any augmented corpus.
2. **`max_iterations=1`, `target_win_rate=0.6`** — a hard cap of one
   optimize→train→evaluate cycle: bounded credit burn, still yields a downloadable
   checkpoint (best-of-1), their win-rate evaluation, and the per-iteration cost
   signal that decides whether a longer run is worth it. The 0.6 target is moot at
   1 iteration but recorded for continuity into any follow-up run.
3. **Credit balance (unknown, dashboard-only):** mitigated by the 1-iteration cap —
   worst case is one iteration's cost; `client.autoscientist.cancel` exists as the
   kill switch mid-run.

**Launch record:**

- `training_method="instruction"` (SFT — the DPO/alignment stage comes later; 693
  local pairs exist but the DPO floor is 12,000), model `Qwen/Qwen3.6-35B-A3B`,
  dataset B (`02e1331f`, 6,951 rows, succeeded), augmentation +3,049 domain / 0
  general, `max_iterations=1`, `target_win_rate=0.6`, idempotency key
  `adaption-qwen36-35b-a3b-run1-20261011` (double-create protection on retries).
- **Run `cf1ebae0-1197-4362-92a1-3228c38ce96e` — status `running`** at 10:52 UTC.
  Run object exposes no credit fields at create time (cost observable as the run
  progresses / at terminal state).
- **Watcher:** background poll (60 s, 6 h cap) saving the final run JSON to the
  gitignored export dir at terminal state (run id, best_win_rate, download flag,
  any credit fields). Checkpoint download happens after the watcher reports.
- Baseline recipe (platform-recommended, unchanged — the loop's job to own):
  LoRA r8/α8 q,v-proj, lr 1e-4 cosine, 1 epoch, batch max, train_on_inputs false.

### 13.5 Post-run readiness — verified while run 1 is in flight (2026-10-11)

- **Base model is locally obtainable:** `Qwen/Qwen3.6-35B-A3B` is public and ungated
  on HF (26 safetensors shards, ≈35B params; 3.5M downloads). MoE A3B (3B active)
  keeps inference CPU-viable on a 32 GB-class machine without a GPU.
- **The checkpoint will be a LoRA adapter, not merged weights** (docs: archive =
  `adapter_config.json` + `adapter_model.safetensors` + tokenizer + trainer_state):
  the local stack is HF base + peft (all present in this repo's venv: torch 2.14
  CPU, transformers 5.18, peft 0.21.1), or a merge for GGUF quantization.
- **Template note for this track:** unlike muse_glimmer (§12.3), the Qwen artifact
  uses Qwen's own HF chat template — the §12.3 pin is Fireworks-pilot-specific and
  does not apply to the Adaption artifact.
- **Eval adapter design settles (§12.5's open question):** `manifest_internal.jsonl`
  carries per-row provenance — `arc_id`, `session_n`, `split`, `source_family`
  (e.g. `nightmare_scenarios`), `difficulty` (e.g. `severe`), `domain` (e.g.
  `boundary_testing`), `verdict`, `line_sha256`. therapy_bench's golden-question
  `category` maps cleanly onto `domain`/`source_family`, `expected_behavior` onto
  the reference assistant turn, prompt onto the rendered dialogue prefix — with
  ledger-grade provenance per row via `line_sha256`.
- Ready state: on run-1 success the remaining work is download → inspect archive →
  wire therapy_bench (GenerativeModel wrapper over base+adapter) → run the 78-row
  held-out eval locally — no Fireworks dependency on this track's eval.

### 13.6 Run-1 results + checkpoint secured (2026-10-11, 12:06 UTC)

**Status: `succeeded` — 74 minutes end-to-end** (created 10:52:16, completed 12:06:21).

- **`best_win_rate` 0.4971 vs target 0.6** — a coin-flip on their generic judge, below
  target, with `max_iterations=1` capping any recipe adjustment. Honest read: this
  number says little about therapy quality (their judge is domain-generic); it says
  the probe's mechanics work. The real quality test is the local therapy_bench eval.
- **Training was healthy:** `trainer_state.json` shows train loss **0.827 → 0.444**
  over 58 steps / 1 epoch — a clean descent curve, comparable in magnitude to the
  Fireworks pilot (0.708 → 0.371 over 2 epochs; eval loss 0.430). The 58 steps over
  ~10,000 rows imply sequence packing (~170 rows/step at batch max) on their side.
- **Recipe actually used** (matches the recommendation): LoRA r8/α8, dropout 0,
  `q_proj,v_proj`, CAUSAL_LM.
- **Checkpoint downloaded and verified** (no restriction, no ceremony):
  `adaption_run1_qwen36_lora.tgz` — plain tar (not gzip, despite the name), 7.7 MB,
  sha `2ff7a31f75c8be38cb135cd5944b52175736824e7df226502067ad70f4dd2ee1`;
  contents: `adapter_config.json`, `adapter_model.safetensors` (**4.1 MB** — r8 on
  q,v is tiny), `chat_template.jinja`, `config.json`, tokenizer trio,
  `trainer_state.json`, `README.md`. Extracted to
  `export/fireworks_pilot_v1/adaption_run1_qwen36_lora/`.
- **Reproduction nuance:** `adapter_config.base_model_name_or_path` =
  `togethercomputer/Qwen3.6-35B-A3B_bnb_4bit_t` — the LoRA was trained against a
  **bitsandbytes 4-bit quantized base**. Applying the adapter to the full-precision
  HF base works (standard practice) with some drift; faithful reproduction wants the
  same 4-bit base (bnb requires CUDA — GPU). Included `chat_template.jinja` is the
  authoritative template for this artifact.
- **Credit cost: not API-exposed even at terminal state** (no credit fields on the
  run object). Balance and burn are dashboard-only — the owner's read of the
  dashboard is the only way to know what run 1 consumed.
- **Next decision (owner):** (a) read the dashboard (credit burn + remaining
  balance); (b) local therapy_bench eval of THIS checkpoint first (free, no
  Adaption spend, tells us whether a run-2 is worth anything) — my recommendation;
  (c) run 2 with the general mix and more iterations, if the balance justifies it.
  Eval compute note: this artifact's eval needs a modest GPU (≥24 GB with the 4-bit
  base, or 40 GB+ for FP16) or a 32 GB-RAM machine with a GGUF quant — a lower bar
  than the Fireworks artifact (dense 30B), but still not runnable on this
  workstation or `headrush`.

### 13.7 Reading the results properly — the augmented dataset, pulled apart (2026-10-11, 12:45 UTC)

The owner pushed back on "dashboard-only" ("read the results yourself, use the API
properly") — correct: `datasets.list()` surfaced a **third dataset we never created
directly**, and reading it changed the picture of run 1.

- **Discovered: `a7079227-…` — "train_unrolled_adaption (augmented)", kind
  `augmented`, `source_dataset_id` = our unrolled upload, run id
  `augmented-a7079227-…`, created 11:16:40 UTC (run 1's augmentation phase), 9,994
  rows, `succeeded`.** This is the materialized training set of run 1 — and it is
  downloadable and fully inspectable. Downloaded (225.6 MB jsonl, plain, not
  tarred).
- **Composition, quantified:**
  - **6,951 rows = our corpus, verbatim passthrough.** `enhanced_completion` is the
    literal string `"N/A"` on exactly these rows (count matches our upload to the
    row); `original_prompt`/`original_completion` carry our turns with content
    intact (character-level verification done — earlier mismatch fears were an
    artifact of comparing decoded text against escaped-JSON bytes).
  - **3,043 rows = platform-synthesized — and NOT derived from our corpus.** Their
    sources are generic health-advice Q&A (HealthCareMagic-style: "Hi Tabitha!
    Welcome to HCm…", HIV-risk reassurance, abdominal-pain advice), rewritten into
    elaborate single-turn compassionate-clinician prompt/completion pairs
    (`original_prompt` None on 2,416 of them). **Zero** of them carry our structured
    note format; zero share content with our corpus. So "domain augmentation" here
    means *topic-adjacent generic content*, not corpus-derived synthesis — materially
    different from what "domain-targeted" suggested, and directly relevant to run-2
    design and the clinical-review scope.
- **The "N/A" question, honestly:** if run 1 trained `"N/A"` as a literal target on
  69% of rows, the artifact would be poisoned; if "N/A" is an export marker meaning
  "no enhancement applied" (training on the original), the corpus is a sane mix.
  The loss curve (0.827→0.444, ordinary LM descent — a constant-target corpus would
  collapse far faster) points to the benign reading, but it cannot settle it from
  outside. **The therapy_bench eval settles it empirically.**
- **Export quirk:** the dataset download stringifies turn-arrays with a malformed
  repr (`'role': user` — missing quotes), so the export is not programmatically
  round-trippable without repair. Raw material is preserved; the encoding is sloppy.
- **Augmentation count:** 3,043 rows generated, not the requested 3,049 (9,994 vs
  10,000 — six short; presumably dedupe).
- **Credits, exhaustively re-verified negative:** no credits endpoint (17
  undocumented paths swept: 404s), no credit fields on run/dataset/model objects,
  SDK exposes exactly three resources (`autoscientist`, `datasets`,
  `training_models`). Balance/burn are dashboard-only — that specific claim stands,
  but the results themselves were absolutely readable, and the initial
  "get_status-only" reading was too shallow.
- **Implication for run 2:** the augmentation knob pulls generic health content,
  not corpus-derived therapy material — a general-mix run 2 would add more of the
  same. By contrast, the arc-pipeline expansion (~185 real dialogues ≈ 3,049 datums)
  now looks strictly better for domain quality; the platform's augmentation's main
  remaining value is regularization/diversity, which the general mix provides anyway.

### 13.8 Eval harness built, CPU-smoke-verified (2026-10-11, 14:40 UTC)

**The therapy_bench A/B of the run-1 checkpoint is now one command on a GPU box**
(bare base vs base+LoRA). It answers the §13.6 open question — whether `"N/A"`
was trained as a literal target (a poisoned adapter should score at-or-below the
bare base) or skipped as an export marker (at-or-above) — and measures the
adapter's actual therapy delta.

- **New harness** (`ai/qa/validation/therapy_bench/`):
  - `adaption_lora_model.py` — the bench's `GenerativeModel` over the checkpoint
    stack: tokenizer + chat template from the checkpoint dir; thinking markers
    derived programmatically at runtime (template bytes never hardcoded —
    display/transcription mangles tag-like strings); no-thinking prefill by
    default, greedy, 512 new tokens; two load strategies (below). Heavy imports
    are lazy so the module imports (and unit tests run) without torch.
  - `run_adaption_eval.py` — CLI A/B runner: `--modes base,adapter` (or `stub`),
    `--limit N` smoke, per-mode `results.json` + a `comparison.json` with deltas
    vs base.
  - 13 new tests (pure helpers, lazy-import guard, stub end-to-end); 32 pass
    total with the existing suite; ruff clean (three pre-existing
    `therapy_bench.py` debts fixed at root: an unused noqa, two magic numbers).
- **Verified offline, zero spend** (meta-instantiation + local files; nothing
  downloaded but configs/index):
  - The public base `Qwen/Qwen3.6-35B-A3B` is **multimodal**
    (`Qwen3_5MoeForConditionalGeneration`); its text weights live under
    `model.language_model.*` plus top-level `lm_head.weight` and cover the
    checkpoint's text-only CausalLM **exactly** (692 + 1 = 693 keys, zero
    missing/extra). No official text-only or BNB-4bit sibling exists (Instruct
    404s; togethercomputer's bnb variant is private; unsloth/nvidia FP8/GGUF/
    NVFP4 variants are different stacks).
  - Adapter census: **20 modules** — q_proj (out 8192) and v_proj (out 512) of
    the **ten full-attention layers only**; the hybrid model's linear-attention
    layers use a different module family (`linear_attn`) and were never matched.
    40 tensors, three shape groups (A [8, 2048] ×20; B [8192, 8] ×10; B [512,
    8] ×10).
  - **`remap` strategy** (default): text-only CausalLM instantiated from the
    checkpoint's own config, public shards streamed in under the prefix remap,
    adapter attached with native PEFT (keys align exactly). BF16 → ~70 GiB: an
    80 GiB GPU or a ~96 GiB-RAM CPU box.
  - **`mm` strategy**: full multimodal `from_pretrained` — required for bnb NF4
    (the faithful training-time quantization; fits a **~24 GiB GPU**) — then LoRA
    injected into the language-model subtree with a name-restricted regex and
    the adapter tensors copied in under a key rewrite. Meta-verified: exactly 20
    modules injected, **zero vision-tower escapes**; strict load-time accounting
    asserts all 40 tensors land.
  - Training rows carry **no system turn** → eval messages are user-only,
    matching training conditions exactly.
  - Live CPU smoke all green: tokenizer + template auto-load from the checkpoint
    dir; 52-question stub run through the full pipeline (heuristic judge +
    comparison); CLI form verified
    (`PYTHONPATH=.. uv run python -m ai.qa.validation.therapy_bench.run_adaption_eval`).
- **Invocation on the GPU box** (from the ai repo root):
  - ~24 GiB GPU: `PYTHONPATH=.. uv run python -m ai.qa.validation.therapy_bench.run_adaption_eval --modes base,adapter --load-strategy mm --load-4bit`
  - ~80 GiB GPU or ~96 GiB-RAM CPU box: `PYTHONPATH=.. uv run python -m ai.qa.validation.therapy_bench.run_adaption_eval` (remap default)
  - Pre-flight first: `--modes adapter --limit 5`. Disk: ~75 GiB for the 26-shard
    base download either way.
- **Still blocked on hardware** (unchanged): this workstation (4-core/15 GiB, no
  GPU, 5.5 GiB free, swap full) and `headrush` cannot run it. The deferred owner
  decision is now due: which GPU box ("cross that bridge when we download
  adapter" — the adapter is downloaded and fully wired). Also noted: an Adaption
  MCP server is connected to this session but needs owner authentication via
  `/mcp` before its tools become usable.

### 13.9 Run-1 A/B verdict: adapter at parity — "N/A" benign, delta nil (2026-10-11, 19:30 UTC)

**The A/B ran to completion on Lightning GPU compute and settles the §13.6
question: the augmented dataset's `"N/A"` pass-through rows did not poison the
run-1 checkpoint — and the checkpoint adds no measurable therapy delta over the
bare base.** 52 golden questions, both arms through the checkpoint's own chat
template (greedy, 512 new tokens, no-thinking prefill), deterministic heuristic
judge, `mm` strategy + bnb NF4 (faithful to the training-time quantization; the
adapter's own `adapter_config.json` records its training base as the
togethercomputer bnb-4bit variant, confirming the quantization match):

| arm                              | empath  | safety  | reflection |
| -------------------------------- | ------- | ------- | ---------- |
| base (`Qwen/Qwen3.6-35B-A3B`)    | 0.8000  | 0.8596  | 0.5186     |
| base + run-1 LoRA                | 0.7962  | 0.8851  | 0.5019     |
| **Δ adapter−base**              | −0.0038 | +0.0255 | −0.0168    |

- **Verdict 1 — no poisoning.** A poisoned adapter (literal `"N/A"` trained as a
  target) would land at-or-below base across the board; instead empath and
  reflection are flat within judge noise and safety is slightly up. The §13.7
  augmented dataset (6,951 verbatim + 3,043 generic-health synth rows) produced a
  functioning adapter, not a degenerate one.
- **Verdict 2 — no transfer.** Train loss fell 0.827→0.444 and the training win
  rate was 0.4971, but none of that fit surfaces as golden-question gains. The
  r8 q/v-proj LoRA over the ten full-attention layers is a wash on TherapyBench;
  the +0.026 safety edge is the only positive signal. For run 2 this reframes
  the question: the dataset forensics are settled benign, so effort belongs in
  arc-pipeline expansion / a stronger recipe (rank, target modules, or
  full-attention coverage), not in re-litigating the corpus.
- **Artifacts**: `ai/research/experiments/evals/evaluation_results_adaption_run1_{base,adapter,comparison,preflight_adapter}.json`
  (ai `d7094746`); the multi-mode GPU fix landed as ai `8613ee7e`.

**How the run went (ops record):**

- **L4 attempt (~$0.79/hr, GCP)**: payment-method gate cleared by owner
  mid-session; start succeeded. `uv` defaulted to CPython 3.15 (no torch
  2.13.0 wheels) — pinned `-p 3.14`. The 4-bit preflight load then failed:
  forced `device_map={"": 0}` placed 20.65 GiB before a ~1 GiB quantization
  workspace hit CUDA OOM against 22.03 GiB usable — the mm+NF4 load
  (vision tower included) is genuinely ~1 GiB too big for a 22 GiB card
  without the vision-offload patch.
- **A100-80 in-place switch (~$5.68/hr, owner-approved)**: filesystem, venv,
  and the 67 GB HF cache survived `switch_machine()`. Cold load 19:18 for
  1026 tensors; preflight (5 adapter questions) passed at empath 0.86 / safety
  0.92 / reflection 0.51.
- **Base arm completed** (52 questions, ~53 min of generation), **then the
  adapter arm died loading**: the multi-mode loop builds each arm's model in
  the same process, and the CUDA caching allocator kept the first load's
  ~65 GiB staging reserve; the second `from_pretrained` sized its
  `device_map=auto` plan against the held memory, offloaded linears to
  CPU/disk, and bnb refused to quantize them. Fixed at the harness root
  (ai `8613ee7e`: drop mode references, `gc.collect()`,
  `torch.cuda.empty_cache()` between modes; lazy torch import keeps stub
  mode torch-less; PLC0415 per-file-ignore matches `adaption_lora_model.py`).
  The adapter arm then ran clean in a fresh process.
- **Studio plumbing lessons**: `upload_file`/`download_folder` paths are
  unreliable around machine switches — writing/reading via base64 through the
  `run()` command channel is deterministic; driver chains need an ERR trap
  (the first chain failed silently at the `&&`); the studio shell presets
  `HF_HOME` to `.cache/huggingface` (driver must export its own); and
  `.lightningignore` does not cover `hfhome`/`evalvenv`, so both (~90 GB) were
  deleted before `stop()` to avoid a slow sync. Studio `adaption-eval-l4`
  stopped 19:22 UTC.
- **Spend**: ~55 min L4 (~$0.73) + ~2.9 h A100-80 (~$16.5) ≈ **$17.2** total
  for the complete A/B, against the 5-credit free balance noted in §13.8's
  hardware decision.
