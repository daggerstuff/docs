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
| Package G spend | cap $635 active; **$0 incurred** |
| Package H experiment | granted, not started; next is step 1 (Render Samples, provider console) |

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
- Nothing in this log grants anything; the first attempt is recorded as blocked — no state
  was created at the provider in that attempt — and $0 has been spent. The successful upload
  on the replacement account is recorded in §7.

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
  Current spend ledger remains $0 pending billing reconciliation.
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
