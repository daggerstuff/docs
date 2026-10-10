# Fireworks Pilot — Execution Log

**Created:** 2026-10-10, on the owner's "do those next steps" instruction. **Scope:** the
execution record for everything after the grant records — Package F upload, Package G spend
ledger, Package H step order. Nothing here grants anything; grants and their basis quotes
live in [`fireworks-approval-packages.md`](./fireworks-approval-packages.md).

## 1. Status (as of 2026-10-10)

| Item | State |
|---|---|
| Phase 1 (packages A–E) | **complete** — grants recorded in the packages doc |
| Package F upload | authorized; first attempt **BLOCKED — provider account suspended** (HTTP 412). No provider-side state created; nothing left this environment |
| Package G spend | cap $635 active; **$0 incurred** |
| Package H experiment | granted, not started; waits on the Package F retry |

## 2. Package C conditions (recorded; console items flagged)

- **Account:** `screamingparrot` (discovered via `GET /v1/accounts`, 2026-10-10 11:06 UTC).
  **Suspended:** "possibly due to reaching the monthly spending limit or failure to pay past
  invoices" — https://fireworks.ai/account/billing.
- **Provider terms/DPA:** standard product terms apply (docs.fireworks.ai); the account's
  executed agreement version is a console item.
- **ZDR / Secure Training applicability:** not queryable headlessly; confirm in the account
  console (provider docs: accounts/zero-data-retention, guides/security_compliance/
  secure_training).
- **Data residency:** enterprise data-residency exists (provider docs: accounts/
  data-residency); training-data storage region is a console item.
- **Encryption:** datasets carry an authoritative `encryptionState` (CMEK marker) returned
  at creation — it will be recorded here per dataset at upload time. None created yet.
- **Deletion path (rollback):** `DELETE /v1/accounts/{account_id}/datasets/{dataset_id}`
  (provider docs: api-reference/delete-dataset).

## 3. Package F — execution attempt (2026-10-10, blocked)

- **Pre-egress identity re-check** (2026-10-10 11:08 UTC, all matched export plan §6/§9):
  gold `d357b8b5…`, train `281da447…`, val `6154878…`, test `35f34d09…`, manifest
  `f7e19cb6…` — the two upload candidates are byte-identical to the verified emission.
- **Mechanism (REST, per provider docs):** `POST /v1/accounts/{account_id}/datasets`
  (create entry; `datasetId`, `dataset: {userUploaded: {}, exampleCount}`, displayName) then
  `POST /v1/accounts/{account_id}/datasets/{dataset_id}:upload` (multipart `file`) —
  docs.fireworks.ai/api-reference/create-dataset + upload-dataset-files (single-request
  upload, ≤150 MB; largest file here is 13.4 MB). `firectl` is not installable from PyPI in
  this environment (no published package), so REST is the execution path. The API key was
  read from the environment only and never printed.
- **Planned dataset ids:** `arc-pilot-v1-train` (train.jsonl, 418 rows) and
  `arc-pilot-v1-eval` (val.jsonl, 80 rows); val attaches as the job's `evaluation_dataset`
  at Package H step 3. **`test.jsonl` is never uploaded by any package.**
- **Attempt:** the authenticated discovery `GET /v1/accounts` returned **HTTP 412** (account
  suspended). No create or upload calls were made after that; a suspended account cannot host
  the pilot.
- **Retry path (after billing is cleared):** (1) re-run the identity re-check above;
  (2) the two create calls, then the two upload calls (exact invocations to be appended here
  with timestamps when run); (3) verify via `GET /v1/accounts/{account_id}/datasets` — state
  `READY`, `exampleCount` 418/80, `encryptionState` recorded here; (4) only then proceed to
  Package H step 1 (Render Samples) in the provider console.

## 4. Package G — spend ledger (cap $635)

| Date (UTC) | Item | Estimated | Actual | Running total |
|---|---|---|---|---|
| 2026-10-10 | none — no paid operation has run | — | $0.00 | $0.00 |

Authorized lines: smoke test ≤$5 · pilot SFT ≤$150 (2–3 epochs, GLM 5.3 Flash class) ·
evaluation endpoint ≤$480 (≤40 GPU-hours, region-rate covered). Any overrun stops the pilot
and returns to the budget gate.

## 5. Package H — step order (binding; not started)

1. **Render Samples** — job-details page in the provider console: verify loss masks
   (user 0 / assistant 1), ledger rendering, no truncation; set an explicit max-context-length
   ≥ the largest row (≈23.2k tokens by chars/4) at job creation.
2. **Format smoke test** — small managed-LoRA run on a ≤16B-class shortlist model over a
   ~100-row slice. Note: the slice dataset is additional egress (drawn from train.jsonl under
   the same Package C basis) and will be logged here before creation.
3. **Pilot SFT** — managed LoRA on GLM 5.3 Flash over `arc-pilot-v1-train` +
   `arc-pilot-v1-eval` as evaluation_dataset, 2–3 epochs within the cap; hyperparameters and
   job id recorded here.
4. **Phase 4 evaluation preview** — untuned vs. tuned on held-out test.jsonl prompts (egress
   under Package C); catastrophic-tier behavior is unmeasurable on held-out data (all 10
   catastrophic rows are in train — export plan §5.4) and must be reported as such.

## 6. Validation (self-check, 2026-10-10)

- No secrets appear in this log; the API key was read from the environment and never printed.
- No clinical examples; all identifiers are synthetic; `test.jsonl` has not left this
  environment.
- Nothing in this log grants anything; the blocked attempt is recorded as blocked — no state
  was created at the provider, and $0 has been spent.
