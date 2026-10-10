# Fireworks Training Readiness — Status Register

**Created:** 2026-10-10 (Step 3 of the docs-first Fireworks preparation recorded in
[`.junie/plans/fireworks-training-preplan.md`](../../.junie/plans/fireworks-training-preplan.md))
**Status:** documentation-only. Nothing here provisions, uploads, spends, or trains. **Training has not begun and is not scheduled by this document.**
**Entry gate satisfied:** dataset close-out evidence recorded in
[`ai/training/DATASET_PIPELINE_HANDOFF.md`](../../ai/training/DATASET_PIPELINE_HANDOFF.md) § "Dataset close-out" (October 10, 04:15 UTC). The corpus is not frozen — future arcs or quality work would re-open the dataset items.
**Decisions (October 10, 2026):** the owner delegated the open choices ("you pick the best decision"); §2 records the four decisions made and the verified provider facts. Items requiring human legal/clinical authority (licensing, consent, privacy approval, budget, named experiment owner) remain with the owner.

**Update (later, October 10, 2026):** the owner's instruction to begin the four grant items was executed for the local steps only — the two in-plan dispositions adopted (export plan §4.1, §5.4) and the local emission approved, run, and verified (export plan §9; item 9 below). Nothing left this environment; items 4–6 and 13 and every external gate remain open. Signable decision packages: [`fireworks-approval-packages.md`](./fireworks-approval-packages.md).

**Update 2 (later still, October 10, 2026):** "do those next steps" — the owner granted all eight packages (grant records in the packages doc) and confirmed the licensing determination, the names (experiment owner and sole clinical reviewer: the owner), and the $635 budget cap. Phase 1 is complete: items 4–6 determined, item 13 named, D1–D3 ratified, final model GLM 5.3 Flash. The Package F upload is authorized but its first execution attempt was blocked by the provider: account `screamingparrot` is suspended (HTTP 412, billing). Nothing left this environment; execution state lives in [`fireworks-pilot-log.md`](./fireworks-pilot-log.md).

---

## 1. Purpose

Single place to see what is ready for a possible Fireworks fine-tuning pilot and what still blocks it. Every item carries a status, evidence, date, and owner. Nothing in this register authorizes work; each gate below requires the owner's explicit approval, given separately.

- **verified** — evidence exists and is pointed to; re-check before relying on it.
- **pending** — prerequisite not yet established; no known hard blocker.
- **blocked** — a known, named blocker prevents progress. (No item currently carries this status.)

## 2. Decision record (October 10, 2026 — made on the owner's delegation)

Four decisions were recorded on the owner's delegation. All remain documentation: none provisions, uploads, or spends. D1–D3 are ratified at the Phase 1 gate, not by this file.

**D1 — Target role: therapist-response SFT** (client→user, therapist→assistant). The arc corpus is therapist responses by construction ([`ARC_CORPUS_SPEC.md`](../../ai/training/ARC_CORPUS_SPEC.md) §1: the ledger gives the trained model an explicit state substrate); it is the platform's first training need and the only behavior this corpus can supervise end-to-end. Patient simulation and supervision need their own target-specific data and stay out of scope.

**D2 — Ledger contract: keep the 9-field ledger inline in the assistant turn** (JSON ledger + newline + spoken reply — the corpus's native shape). Rationale: (a) the corpus, the auditor, and the product treat the ledger as first-class (spec §4) — training without it discards the arc track's differentiator; (b) zero re-rendering: gold rows are already valid OpenAI-format chat samples for Fireworks managed SFT; (c) mechanical pilot evaluation: the emitted ledger parses and checks per turn; (d) inline ledgers avoid the billed-token multiplier that `reasoning_content` traces incur under multi-turn unrolling (Fireworks pricing note). The `reasoning_content` variant (ledger as a native thinking trace — supported by managed SFT) is recorded as the follow-up A/B, not the pilot. Whether production serving keeps ledgers in output stays a release-gate decision.

**D3 — Base-model shortlist and recommendation.** The standing owner preference applies: **no Llama models**. Verified tunable (managed LoRA SFT) non-Llama candidates in Fireworks' 44-model catalog (synced 2026-10-08): GLM 5.3 Flash / GLM 5.3 / GLM 5.2 FP8 / GLM 5.1, DeepSeek V4 Flash 0731 / V4.1 Flash / V4-Pro, Kimi K2.5–K3, Qwen (3.8 27B; 3-235B class per pricing tables), Mistral Small 24B, Ministral 3, Gemma 4, MiniMax M3, Nemotron. **Recommendation: GLM 5.3 Flash** — the GLM family already audits part of the corpus (GLM 5.2 ×69 sessions), available on the serverless Training API as a no-provisioning fallback, and in the cheapest-to-serve tier of the GLM family. Runner-up: Qwen 3.8 27B (3–4× cheaper to train and the smallest dedicated serving footprint among candidates). Final pick at Phase 1 sign-off.

**D4 — Leakage adapter design** (implemented and executed locally 2026-10-10; item 9 below; export plan §5, §9). Verified finding: the stratified splitter's grouping key (`metadata.source_family::source_id`) is absent from **every** one of gold's 189,735 rows — all collapse to `unknown::unknown`, so the splitter cannot produce leakage-safe splits for this corpus as-is. Decided design for the Phase 2 exporter: emit explicit `source_family`/`source_id` per row, grouping at **seed-scenario level** (`seed.source` + `seed.scenario_id`, falling back to `arc_id`), because 11 seed scenarios are shared by more than one arc (e.g. `nf_048` → `arc_0143` + `arc_0214`) — arc-level grouping would leak those across splits.

**Verified provider facts** (read-only research, 2026-10-10; sources: `docs.fireworks.ai/fine-tuning/fine-tuning-models`, `docs.fireworks.ai/fine-tuning/models`, `fireworks.ai/pricing`):

- **Format:** managed SFT consumes OpenAI-compatible chat JSONL — the gold `messages` shape, with per-message `weight` loss masking and optional per-assistant-turn `reasoning_content`. A "Render Samples" tool exists to inspect rendered tokens and loss masks before a paid run. Dataset limits: 3 to 3M examples per dataset; per-example training cutoff defaults to 32,768 tokens (`--max-context-length` raises it, e.g. 65,536); a separate `evaluation_dataset` may replace the auto-carved eval split (verified 2026-10-10, `docs.fireworks.ai/fine-tuning/fine-tuning-models`).
- **Eligibility:** managed SFT is LoRA-only for most open models (full-parameter via the dedicated Training API). Trained models serve **only on dedicated deployments** (evaluate first, then `firectl deployment create`); serverless serving is not available for tuned models. "Serve fine-tuned models for the same price as base models."
- **Economics (list prices):** managed LoRA SFT $0.50/1M training tokens (≤16B models) → $3.00 (16.1B–80B) → $6.00 (80B–300B) → **$10.00 (>300B — the class containing GLM 5.3 Flash at 320B)**; tokens ≈ dataset tokens × epochs. Serverless Training API (no provisioning, no idle cost) rates exist for GLM 5.3 Flash ($8.89/1M train, $2.96/1M prefill, $7.41/1M sample) and others. Dedicated serving: $8/hr (H100/H200), $13 (B200), $15 (B300), $20 (GB300) per GPU; region-restricted at 1.5×.
- **Pilot magnitude (arc corpus only, 576 sessions, ≈4.36M tokens by chars/4):** ≈**$44 per epoch** at the >300B class, ≈$13 at the 16–80B class. Training cost is not the budget constraint; **dedicated serving is the cost driver.** These are list-price calculations, not quotes.
- **Privacy mechanisms exist:** Zero Data Retention policy (enterprise), Secure Training surfaces, Bring-Your-Own-Bucket, CMEK. Applicability to a given surface and account tier is an account-level question; the approval to send data externally remains the owner's.

## 3. Readiness register

| # | Prerequisite | Status | Evidence | Date (UTC) | Owner |
|---|--------------|--------|----------|------------|-------|
| 1 | Dataset close-out | verified | Handoff § "Dataset close-out": 235/235 arc records accept (0 HR), 576 checkpoint sessions consolidated, gold and DPO pair files in sync, 0 new rejects; measured on quiescent inputs | 2026-10-10 04:15 | dataset executor |
| 2 | Current verdict evidence | verified | Same section: every accepted record carries `audit.verdict = accept` with flags and auditor model in `ai/training/output/arc_corpus/arc_records.jsonl`; audit trail in `audit_results.jsonl` / `human_review_queue.jsonl` | 2026-10-10 04:15 | dataset executor |
| 3 | Provenance record | verified | Per-row provenance in gold (`source`, `provenance.arc_id/session_n/writer_model/auditor_model/verdict`); rejection log append-only (`consolidation_rejections.jsonl`) | 2026-10-10 04:15 | dataset executor |
| 4 | Licensing for external training | determined (granted 2026-10-10) | Package A grant record ([packages doc](./fireworks-approval-packages.md) §2): no known third-party license/usage restriction — seeds verified self-authored in-repo (no external markers across all 235 plans); third-party writer/auditor model terms considered and accepted by the owner | 2026-10-10 | owner |
| 5 | Consent & sensitivity posture | determined (granted 2026-10-10) | Package B grant record (packages doc §3): synthetic clinical dialogue of this profile is acceptable for external pilot processing; real patient data, de-identified or not, remains prohibited from export | 2026-10-10 | owner |
| 6 | Privacy approval for external processing | approved (granted 2026-10-10) | Package C grant record (packages doc §4); conditions to be recorded in the pilot log before the upload retry; account-level items (ZDR, data residency, DPA version) flagged for console confirmation — no provider-side state exists yet | 2026-10-10 | owner |
| 7 | Target role | verified (ratified 2026-10-10, D1) | Therapist-response SFT, client→user / therapist→assistant — the corpus is therapist responses by construction; ratified per Package E grant record (packages doc §6) | 2026-10-10 | owner |
| 8 | Ledger contract | verified (ratified 2026-10-10, D2) | Keep the 9-field ledger inline in assistant content; `reasoning_content` variant is the follow-up A/B; serving disposition stays a release-gate item; ratified per Package E grant record | 2026-10-10 | owner |
| 9 | Leakage grouping | verified (implemented + executed locally) | D4 adapter implemented in `ai/training/export_fireworks_payload.py` and executed 2026-10-10 under the owner's instruction: 224 groups (77 seed + 147 arc-fallback), splits train 418 / val 80 / test 78, 0 groups or arcs spanning splits; artifacts + `identity.json` in `ai/training/output/arc_corpus/export/fireworks_pilot_v1/`; record in [`fireworks-export-plan.md`](./fireworks-export-plan.md) §5, §9. External transfer still gated (§4) | 2026-10-10 | dataset executor |
| 10 | Provider eligibility | verified (final pick recorded 2026-10-10) | 44-model catalog (synced 2026-10-08); tunable non-Llama candidates: GLM 5.x, DeepSeek V4, Kimi, Qwen, Mistral, Gemma, MiniMax, Nemotron; final pick recorded per Package E: GLM 5.3 Flash (runner-up Qwen 3.8 27B) | 2026-10-10 | owner |
| 11 | Promotion verification | verified | Trained models serve only on dedicated deployments (evaluate → `firectl deployment create`); no serverless serving for tuned models; no serving surcharge over base-model price | 2026-10-10 | owner |
| 12 | Serving economics | verified (list prices) | Training ≈$44/epoch for the arc corpus (GLM 5.3 Flash class); dedicated serving $8–20/GPU-hour, 1.5× region-restricted (§2 facts). **Budget approval still required before any spend.** | 2026-10-10 | owner |
| 13 | Named experiment owner + clinical reviewers | named (2026-10-10) | Package D grant record (packages doc §5): experiment owner = the owner (vivi); sole clinical reviewer = the owner (vivi) for now; additional credentialed reviewers to be named before any release consideration | 2026-10-10 | owner |

Items 1–3, 7–8, 10–12 carry verified evidence; item 9's adapter is implemented and the local emission executed and verified (2026-10-10), with nothing leaving this environment. Items 4–6 and 13 were determined, approved, and named by the owner on 2026-10-10 (grant records in [`fireworks-approval-packages.md`](./fireworks-approval-packages.md)); the authorized upload is blocked only by the suspended provider account ([`fireworks-pilot-log.md`](./fireworks-pilot-log.md)). The pair-file caveats in the handoff (DPO prompts are reconstructed, whole-session preferences not validated turn-level) carry forward unchanged.

## 4. Approval gates (all require the owner, separately and explicitly)

1. **Export approval** — read-only inventory, immutable approved snapshot identity, lineage-aware splitting (per the D4 adapter design), schema/token validation, privacy screening. Nothing leaves this environment before this gate. **Granted 2026-10-10 for the local emission and executed (export plan §9); nothing left this environment. Any upload still requires gate 2.**
2. **Budget approval** — any paid provider operation (upload, training job, serving endpoint) is a new scope with its own budget. No cost may be incurred by documentation. **Granted 2026-10-10: upload authorized (Package F — first attempt blocked by the suspended provider account); spend cap $635 authorized (Package G), $0 incurred.**
3. **Experiment approval** — a bounded, explicitly budgeted SFT pilot after a small format smoke test; no production switch, no deployment to users. **Granted 2026-10-10 (Package H); not started — waits on the Package F retry (pilot log).**
4. **Release approval** — clinician review of tuned behavior before any consideration of serving; automated checks cannot certify safety.

## 5. Pointers (authoritative sources; counts live there, not here)

- Dataset state and close-out: [`ai/training/DATASET_PIPELINE_HANDOFF.md`](../../ai/training/DATASET_PIPELINE_HANDOFF.md) — latest section supersedes earlier snapshots.
- Dataset history and arc-track background: [`DATASET_CREATION_HANDOFF.md`](../../DATASET_CREATION_HANDOFF.md).
- Preparation plan and its boundaries: [`.junie/plans/fireworks-training-preplan.md`](../../.junie/plans/fireworks-training-preplan.md).
- Phase 2 export plan (executed locally 2026-10-10): [`fireworks-export-plan.md`](./fireworks-export-plan.md) — payload spec, screening results, seed-level splits, snapshot identity, execution record §9.
- Owner decision packages (all granted 2026-10-10; grant records in the file): [`fireworks-approval-packages.md`](./fireworks-approval-packages.md) — Phase 1 determinations and Phase 3 requests.
- Pilot execution log: [`fireworks-pilot-log.md`](./fireworks-pilot-log.md) — Package C conditions, the blocked upload attempt, spend ledger, retry path.
- Exporter / preference builder / splitter code: `ai/training/consolidate_arc_corpus.py`, `ai/training/build_arc_dpo.py`, `ai/training/dataset_splitter_stratified.py` (candidates for later assessment, not approval); `ai/training/export_fireworks_payload.py` (the Phase 2 emitter — executed locally 2026-10-10, fail-closed, dry-run supported).
- Provider facts (verified 2026-10-10): `docs.fireworks.ai/fine-tuning/fine-tuning-models`, `docs.fireworks.ai/fine-tuning/models`, `fireworks.ai/pricing`.

## 6. Document validation (self-check, 2026-10-10)

- Links resolve to the referenced files; live counts live in the handoff, provider facts in §2.
- No secrets, credentials, or clinical examples appear in this document.
- No deferred work is presented as approved; no phase implies training has begun (no training job has been created). The four decisions (§2, D1–D4) are recorded on the owner's delegation; D1–D3 were ratified and the final model picked by the owner's 2026-10-10 instruction (D4 is implemented and executed locally, item 9); items 4–6 and 13 were determined, approved, and named by the owner the same day (grant records in the packages doc).
- Dataset items 1–3 state verified evidence with dates; items 7–8 and 10–12 carry sources with their ratification/pick records; item 9 records the implemented adapter and the executed local emission. The authorized upload is blocked only by the suspended provider account (pilot log).
