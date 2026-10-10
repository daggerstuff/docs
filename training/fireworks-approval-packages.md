# Fireworks Approval Packages — Signable Determinations and Requests

**Created:** 2026-10-10
**Status:** all eight packages were GRANTED 2026-10-10 by the owner's instructions ("do those
next steps" plus same-day confirmations; a grant record sits under each package heading).
This document authorized nothing by itself — the grants came from the owner. Execution state:
Phase 1 complete (A–E); F **executed** on the replacement account `linencloset` — both
planned datasets `READY` (pilot log §7); G active — **actual spend pending invoice
reconciliation** after the cancelled step-1 job `jf3tmylp` (est. $69–$141 depending on
billing basis, pilot log §10); H **step 1 executed and verified, steps 2–3 blocked at the
budget gate** (the per-epoch cost basis was wrong by ~9× — per-user-turn unrolling, pilot
log §10; re-authorization required). Only `train.jsonl` and `val.jsonl` have left this
environment; `test.jsonl` and all private provenance remain local.
**Companions:** [`fireworks-readiness.md`](./fireworks-readiness.md) — status register (each
package maps to a register item or gate) · [`fireworks-export-plan.md`](./fireworks-export-plan.md)
— payload spec, screening, splits, snapshot identity, execution record (§9) ·
[`fireworks-pilot-preplan.md`](./fireworks-pilot-preplan.md) — conditional roadmap and approval
boundaries.
**Evidence base:** the emitted pilot payload in
`ai/training/output/arc_corpus/export/fireworks_pilot_v1/` (with `identity.json`), re-hashed
against its recorded sha256s immediately before this document was written (2026-10-10): gold
`d357b8b5…`, train `281da447…`, val `6154878…`, test `35f34d09…`, manifest `f7e19cb6…` —
full values in export plan §6/§9.

**Already adopted — no signature needed** (2026-10-10, the owner's instruction to begin the
four grant items; recorded in export plan §9):

1. Split disposition — accept the hash assignment as-is (export plan §5.4, option 1).
2. Content deviation disposition — the 28 risk-grammar turns ship as-is (§4.1).
3. Export approval for the **local** emission (readiness §4 gate 1) — granted and executed;
   nothing left this environment.

The packages below cover what that instruction could not decide on the owner's behalf: the
Phase 1 human-authority determinations (A–E) and the Phase 3 external-gate requests (F–H).

## 1. How to sign

- Each package is independent; sign any subset, in any order. Deny any package by writing
  "DENIED" and a reason under its signature block — a denial is as much a record as an
  approval, and it keeps the corresponding gate closed.
- Edit any package before signing. The signed text (with initialed edits) is the record; a
  package signed "with edits" carries those edits as the approved scope.
- Dependencies (also noted per package): **E** requires A–D; **F** requires A–D and E;
  **G** requires F; **H** requires E, F, and G.
- Signing nothing changes nothing: every gate stays closed and the emitted payload stays
  local, exactly as verified in export plan §9.
- Bookkeeping after signature (§11) is a follow-up documentation pass, not part of signing.

## 2. Package A — Licensing/usage determination for external training

**Maps to:** readiness item 4 · **Requires:** nothing · **Unlocks (with B–E):** Phase 1.

**Grant record (2026-10-10):** GRANTED — owner confirmation "Confirm as written", given the
seed-provenance verification above (seeds self-authored in-repo; no external markers across
all 235 plans) and with the third-party writer/auditor model terms considered and accepted.

**Why this is needed:** per-row provenance is recorded, but no license/usage review for
external provider processing exists on record for the arc-corpus family or the master gold it
lives in (readiness §3).

**Facts of record:**

- The payload content is machine-generated dialogue written by this platform's own pipeline
  (writer models recorded in export plan §3; audited by platform-run auditors — Kimi K3 ×507
  sessions, GLM 5.2 ×69).
- Scenario definitions originate in the platform's own arc plan files
  (`ai/training/arc_plans/`; seed families `nightmare_scenarios`, `edge_cases`,
  `probe_arc_v1`).
- What would leave this environment is dialogue text with role/weight fields only — all
  provenance, model ids, timestamps, internal paths, and tags are stripped (export plan §2.2,
  §7).

**Open question the signer resolves:** whether any upstream seed or scenario material carries
third-party licensing terms that would restrict external training use. If the signer knows of
none, the determination below records that; if any exists, deny or edit this package to name
it.

**Determination for signature:**

> The arc-corpus pilot payload — 576 synthetic therapy-training sessions emitted as
> `fireworks_pilot_v1` (train 418 rows + val 80 rows; export plan §9 identities) — may be
> transmitted to Fireworks AI and processed there for supervised fine-tuning. I confirm that
> no known third-party license or usage restriction applies to this content. Scope is this
> pilot payload only; any larger corpus, regeneration, or new dataset family requires a new
> determination.

```
Decision:  ☐ APPROVED as written   ☐ APPROVED with edits (initialed above)   ☐ DENIED
Signed:   ____________________________   Role: ______________________
Date (UTC): ______________   Notes: ______________________________________________
```

## 3. Package B — Consent & sensitivity determination

**Maps to:** readiness item 5 · **Requires:** nothing.

**Grant record (2026-10-10):** GRANTED — owner instruction "do those next steps" (package
text complete as written; the instruction is recorded in lieu of a signature block).

**Facts of record:**

- Synthetic by construction: plan-driven fictional-client dialogue; no patient records, no
  human subjects (export plan §7).
- PII screen: 0 hits across all 576 rows for e-mail, SSN, US-phone, card-number, URL, and
  IPv4 patterns (export plan §4.3).
- The sensitivity profile is real and deliberate: the corpus dramatizes high-risk clinical
  situations across five difficulty tiers (severe 217 / moderate 127 / high 125 /
  adversarial 97 / catastrophic 10 rows; largest domain `nightmare_fuel`, 206 rows; export
  plan §3). This is what the corpus is for.
- Two documented content deviations ship as-is: 28 risk-grammar turns (4 sessions) and 35
  empty-`hx` turns (4 sessions), counts asserted fail-closed in the emitter (export plan
  §4.1, §9).

**Determination for signature:**

> Synthetic clinical dialogue of this profile is acceptable to process externally at
> Fireworks for the pilot, on the basis of its synthetic provenance and the 0-hit PII screen.
> This determination covers synthetic content only: real patient data, de-identified or not,
> remains prohibited from export under the platform's clinical-privacy doctrine.

```
Decision:  ☐ APPROVED as written   ☐ APPROVED with edits (initialed above)   ☐ DENIED
Signed:   ____________________________   Role: ______________________
Date (UTC): ______________   Notes: ______________________________________________
```

## 4. Package C — Privacy approval for external processing

**Maps to:** readiness item 6 · **Requires:** nothing (logically pairs with A and B).

**Grant record (2026-10-10):** GRANTED — owner instruction "do those next steps". The
conditions are recorded in [`fireworks-pilot-log.md`](./fireworks-pilot-log.md) §2;
account-level items (ZDR applicability, data-residency setting, DPA version) were resolved
2026-10-10: the owner confirmed the replacement account `linencloset` carries the same
standard specifications (no ZDR/CMEK — `encryptionState` PLAINTEXT stamped per dataset),
and the executed upload is recorded in the pilot log §7.

**Egress this approval covers (the only egress requested anywhere in this pilot):**

1. Upload of `train.jsonl` (418 rows) and `val.jsonl` (80 rows, attached as the explicit
   `evaluation_dataset`) — Package F.
2. Phase 4 evaluation traffic: held-out prompts sent to the deployed evaluation endpoint
   (export plan §2.5 — same privacy boundary as the training upload).

**Never covered by this or any later package:** `test.jsonl` (78 rows — never leaves this
environment; Phase 4 held-out set), `manifest_internal.jsonl`, `identity.json`, the gold
corpus, arc plan files.

**Provider facts (readiness §2):** privacy mechanisms exist — Zero Data Retention policy
(enterprise), Secure Training surfaces, Bring-Your-Own-Bucket, CMEK. **Account-level
applicability is unverified**; confirming it is a condition of this approval, not a
substitute for it.

**Conditions to confirm and record before the upload completes** (Package F's checklist):

- ZDR or Secure-Training applicability to the dataset and fine-tuning job on this account;
- regions that will store and process the data;
- retention terms for datasets, fine-tuned artifacts, and evaluation logs, plus the
  deletion path (rollback);
- the data-processing agreement / privacy terms version in force at upload time.

**Determination for signature:**

> I approve transmitting the pilot payload to Fireworks AI for fine-tuning and for
> evaluation traffic, as scoped above, conditional on the confirmations above being recorded
> in the pilot report before the upload completes.

```
Decision:  ☐ APPROVED as written   ☐ APPROVED with edits (initialed above)   ☐ DENIED
Signed:   ____________________________   Role: ______________________
Date (UTC): ______________   Notes: ______________________________________________
```

## 5. Package D — Named experiment owner + clinical reviewers

**Maps to:** readiness item 13 · **Requires:** nothing · **Fill in and sign.**
Readiness item 13 requires these names before any external data transfer or training.

**Grant record (2026-10-10):** CONFIRMED — owner answer "I am owner and sole reviewer for
now": experiment owner = the owner (vivi); sole clinical reviewer = the owner (vivi) for now.
Additional, credentialed reviewers are to be named before any release consideration
(readiness §4 gate 4); the "for now" scope is recorded, not assumed away.

| Role | Name | Credential / license | Contact |
|---|---|---|---|
| Experiment owner | | | |
| Clinical reviewer 1 | | | |
| Clinical reviewer 2 (optional) | | | |

- The **experiment owner** owns pilot execution, budget adherence (Package G), the run
  report, and stop/rollback decisions.
- The **clinical reviewer(s)** own the Phase 4 clinician review of tuned behavior — the
  release prerequisite (readiness §4 gate 4). Automated checks cannot certify safety.

```
Decision:  ☐ CONFIRMED as filled in   ☐ DENIED
Signed:   ____________________________   Role: ______________________
Date (UTC): ______________   Notes: ______________________________________________
```

## 6. Package E — Phase 1 decision record (ratifications + final model)

**Maps to:** readiness items 7, 8, 10 · **Requires:** A, B, C, D signed.
This is the pre-plan Phase 1 exit evidence: "a signed decision record naming target,
contract, final model ID, and the privacy determination."

**Grant record (2026-10-10):** GRANTED — owner instruction "do those next steps": E1 (D1) and
E2 (D2) ratified; initial final model ID recorded as **GLM 5.3 Flash**. **Superseding owner
instruction (2026-10-10):** pilot target changed to Muse Glimmer 30B, model ID
`accounts/fireworks/models/muse-glimmer-30b` (the verified catalog ID — the short
`glimmer-30b` slug recorded with the original instruction does not resolve; pilot log §9).
This replaces the GLM selection; account access/quota and model eligibility are verified
(2026-10-10, pilot log §9), with job-creation access exercised at the first paid step (the
smoke test). The budget cap is unchanged; the Glimmer re-estimate fits it (§8 row 2).

| Decision | Ratify | Alternative (write in) |
|---|---|---|
| **E1 Target role (D1):** therapist-response SFT — client→`user`, therapist→`assistant` | ☐ | |
| **E2 Ledger contract (D2):** 9-field ledger inline in assistant content; the `reasoning_content` variant is the follow-up A/B, not the pilot | ☐ | |
| **E3 Final model (from the D3 shortlist; no Llama models):** | — | |

**Superseding E3 selection (2026-10-10): Muse Glimmer 30B** — owner-directed replacement
for the original GLM 5.3 Flash recommendation. Fireworks model ID (verified catalog ID):
`accounts/fireworks/models/muse-glimmer-30b`. The earlier shortlist below is historical and
its eligibility/pricing claims do not establish Glimmer's current eligibility or cost.
Verified 2026-10-10 (pilot log §9): managed-LoRA SFT supported at $3.00/1M training tokens
(16.1B–80B tier); re-estimate ≈$11.16/epoch, 2–3 epochs ≈ $22–34 — fits the $150 line.

Historical D3 shortlist (catalog synced 2026-10-08): GLM 5.3 Flash, Qwen 3.8 27B, GLM 5.3 /
5.2 FP8 / 5.1, DeepSeek V4 family, Kimi K2.5–K3, Qwen 3-235B class, Mistral Small 24B,
Ministral 3, Gemma 4, MiniMax M3, Nemotron.

**Confirm at sign-off:** ☐ account-level access/quota for the picked model ID verified ·
☐ privacy terms read per Package C's conditions · ☐ Package D names recorded.

**Final model ID for signature:** ____________________________________

```
Decision:  ☐ APPROVED as written   ☐ APPROVED with edits (initialed above)   ☐ DENIED
Signed:   ____________________________   Role: ______________________
Date (UTC): ______________   Notes: ______________________________________________
```

## 7. Package F — Upload / provisioning approval (first egress)

**Maps to:** readiness §4 gate 2 (provider-side state) · **Requires:** A, B, C, D, E.

**Grant record + execution (2026-10-10):** GRANTED — owner instruction "do those next steps",
with A–E satisfied. **Executed on the replacement account `linencloset`:** the first attempt
had been blocked on the original account (HTTP 412, billing; replaced by the owner the same
day). Both planned datasets were created and uploaded — `arc-pilot-v1-train` (418) and
`arc-pilot-v1-eval` (80, attaches as the job's `evaluation_dataset` at Package H step 3) —
verified `READY` with `encryptionState` PLAINTEXT and independently re-verified 12:33 UTC:
[`fireworks-pilot-log.md`](./fireworks-pilot-log.md) §7. Nothing else was created; no data
beyond train+val left this environment.

**What will be created at the provider — and nothing else:**

- One fine-tuning dataset (proposed name `arc-pilot-v1`) containing:
  - `train.jsonl` — 418 rows, sha256
    `281da447e675c60f06c56e160bae6fece23db4f2c8d41d4a3ebbbad94a09755b`
  - `val.jsonl` — 80 rows, sha256
    `615487846c3fd503c7627b776e17752713924de6d028bf208872dda3194bd609`,
    attached as the explicit `evaluation_dataset` (replaces the provider's automatic eval
    carve-out; export plan §2.5).
- Method: provider console or `firectl`; the exact invocation is recorded in the pilot log at
  execution (no commands are embedded in this document).

**Explicitly never uploaded by any package here:** `test.jsonl` (78 rows, sha256
`35f34d09…`; Phase 4 held-out set), `manifest_internal.jsonl` (576 lines of private
provenance), `identity.json`, the gold corpus, arc plan files.

**Verification before this gate closes:** uploaded row counts match 418 / 80; a sampled hash
check against `identity.json`; the provider-side dataset id recorded in the pilot log;
Package C's conditions recorded.

**Cost note:** dataset upload is not itself a paid job, but it is provider-side state and is
therefore gated. All paid operations sit under Package G.

```
Decision:  ☐ APPROVED as written   ☐ APPROVED with edits (initialed above)   ☐ DENIED
Signed:   ____________________________   Role: ______________________
Date (UTC): ______________   Notes: ______________________________________________
```

## 8. Package G — Budget approval

**Maps to:** readiness §4 gate 2 (spend) · **Requires:** F · **Scope:** paid operations of
this pilot only. One signature covers the sequence below; no spend may occur before this
package is signed.

**Grant record (2026-10-10):** GRANTED — owner confirmation "Confirm $635". Cap active;
spend ledger in the pilot log; **$0 incurred** — no paid operation has run (dataset upload
and storage only; no training or evaluation job exists).

Proposed caps (editable; list-price planning estimates, not quotes — unit prices verified in
readiness §2, 2026-10-10):

| # | Item | Basis (list prices, readiness §2) | Planning estimate | Proposed cap |
|---|---|---|---|---|
| 1 | Format smoke test | tiny managed-LoRA run on a ≤16B-class shortlist model (e.g. Ministral 3; non-Llama), 1 epoch over a ~100-row slice (≈0.7M tokens by chars/4) at $0.50/1M training tokens | ≈ $0.35 | **$5** |
| 2 | Pilot SFT | Muse Glimmer 30B verified (pilot log §9): managed-LoRA SFT supported at $3.00/1M training tokens (16.1B–80B tier, 29.8B params); payload ≈3.72M tokens (chars ÷ 4) | ≈ $11.16/epoch; 2–3 epochs ≈ **$22–34** (vs $150 cap) | **$150** |
| 3 | Evaluation endpoint | tuned models serve only on dedicated deployments; $8/hr (H100/H200 class), $13 (B200), $15 (B300), $20 (GB300); ×1.5 if region-restricted | e.g. 40 GPU-hours ≈ $320 standard / ≈ $480 at 1.5× | **$480** |

- **Total proposed cap: $635.** Spend is tracked against the cap in the pilot report; any
  overrun stops the pilot and returns to this gate.
- Routes for Muse Glimmer 30B verified 2026-10-10 (pilot log §9): managed LoRA SFT supported
  at $3.00/1M (the planned route); a serverless Training API route is listed ($5.86/1M train
  + $1.96/1M prefill + $4.88/1M sample) but is more expensive per training token at this
  tier and remains unauthorized for the pilot. The prior GLM serverless alternative is
  historical.
- The Render Samples inspection before any paid run is free and required (Package H, step 1).
  **Correction (2026-10-10, pilot log §10):** this premise was wrong — the platform couples
  render capture to a live training job and writes the artifact only when the job reaches a
  terminal state; there is no free pre-run render path. The step-1 verification was carried
  out on a paid job, subsequently cancelled at the owner's direction.

```
Decision:  ☐ APPROVED as written   ☐ APPROVED with edits (initialed above)   ☐ DENIED
Signed:   ____________________________   Role: ______________________
Date (UTC): ______________   Notes: ______________________________________________
```

## 9. Package H — Experiment approval (bounded SFT pilot)

**Maps to:** readiness §4 gate 3 · **Requires:** E, F, G. Scope: pre-plan Phase 3, in this
order:

**Grant record (2026-10-10):** GRANTED — owner instruction "do those next steps"; the step
order is binding. Not started: step 1 (Render Samples) operates on a created job in the
provider console, and every step waits on the Package F retry (account suspension, pilot
log).

**Status update (2026-10-10, later — pilot log §10):** step 1 was **executed and verified**
on job `jf3tmylp` (loss masks, ledger, no truncation all pass); two findings supersede the
grant-time premises: (1) render capture is coupled to paid training (no free pre-run
inspection), and (2) the per-epoch token basis in budget row 2 (chars ÷ 4, ≈$11.16/epoch)
ignored the trainer's per-user-turn unrolling — the measured basis is ≈34.1M train
tokens/epoch (≈$102/epoch at list) plus ≈6.5M eval tokens, so 2–3 epochs ≈ $204–$366,
over this package's $150 cap, and the ~100-row smoke slice ≈$24, over the $5 bound.
**Steps 2 and 3 are blocked at this gate pending the owner's re-authorization** with the
corrected numbers (pilot log §4/§10); the cancelled run's spend ($69–$141 depending on
billing basis) awaits invoice reconciliation.

1. **Render Samples (free, required):** verify loss masks (user 0 / assistant 1), ledger
   rendering, and no truncation. Largest row ≈23.2k tokens (chars/4) vs. the 32,768-token
   default training cutoff — set an explicit max-context-length ≥ the largest row at job
   creation (readiness §2; export plan §2.4).
2. **Format smoke test** (Package G #1): confirm the payload format trains end-to-end before
   the full-cost job.
3. **Pilot SFT:** managed LoRA on the Package E model over the uploaded dataset
   (`train.jsonl` + `val.jsonl` as evaluation_dataset), 2–3 epochs (adjustable within the
   Package G cap); hyperparameters and run id recorded in the pilot report.
4. **Phase 4 evaluation preview** (design belongs to Phase 4; release stays separately
   gated): untuned vs. tuned on held-out cases including ordinary non-crisis controls;
   record safety, factual fidelity, continuity, format validity, latency, cost. Held-out
   evaluation traffic is egress covered by Package C.

**Boundaries:** no production switch; no deployment to users; no serving beyond the
evaluation endpoint; no corpus changes; no DPO; the tuned artifact is pilot evidence only.
Clinician review (Package D reviewers) is the release prerequisite.

**Carried caveats the evaluation plan must respect** (export plan §5.4/§9):

- All 10 catastrophic-difficulty rows landed in train under the adopted disposition: **val
  and test contain zero catastrophic rows.** The pilot's held-out sets cannot measure
  catastrophic-tier behavior; Phase 4 must say so explicitly rather than imply coverage.
- Difficulty strata are unbalanced across splits (6 recorded gate deviations; e.g.
  adversarial 65/10/22 across train/val/test, severe under-weighted in val).
- The shipped content deviations (28 risk-grammar, 35 empty-`hx`) are in the training data:
  the tuned model may reproduce risk values that do not lead with the spec's token grammar
  and may emit empty `hx` fields. Phase 4 format-validity checks should expect this legacy
  shape rather than count it as regression; correcting it would be a corpus-lane question,
  not a pilot knob.

```
Decision:  ☐ APPROVED as written   ☐ APPROVED with edits (initialed above)   ☐ DENIED
Signed:   ____________________________   Role: ______________________
Date (UTC): ______________   Notes: ______________________________________________
```

## 10. What no package here requests

Release approval (readiness §4 gate 4 — clinician review, Phase 4) · production serving ·
DPO · any corpus regeneration or edit · provider account or billing changes beyond the items
above · any use of the tuned model outside pilot evaluation.

## 11. Bookkeeping after signature

| Package | Readiness register | Action on signature |
|---|---|---|
| A | item 4 | flip to determined; record date + signer |
| B | item 5 | flip to determined |
| C | item 6 | flip to approved (conditions recorded at upload) |
| D | item 13 | flip to named; names recorded |
| E | items 7, 8, 10 | D1/D2 ratified; final model recorded; Phase 1 marked complete in pre-plan |
| F | §4 gate 2 (upload) | egress executed; provider dataset id + verification recorded |
| G | §4 gate 2 (spend) | budget cap active; spend tracked in pilot report |
| H | §4 gate 3 | Phase 3 begins; smoke-test-first order binding |

A denial of any package keeps the corresponding register item pending and the gate closed.

## 12. Document validation (self-check, 2026-10-10)

- Links resolve; every number traces to the export plan (§2–§9) or readiness §2, re-verified
  2026-10-10; artifact identities re-hashed against the emitted files before writing.
- No secrets, credentials, provider commands, or clinical examples appear; all identifiers
  are synthetic.
- This document granted nothing by itself: the grants recorded under each package heading
  came from the owner's explicit 2026-10-10 instructions, quoted in the grant records; the
  already-adopted items are quoted from export plan §9, not re-granted here. Execution state
  lives in the pilot log.
- Denials are provided for and recorded as first-class outcomes.
