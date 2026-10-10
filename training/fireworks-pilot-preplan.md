# Fireworks Pilot — Conditional Pre-Plan

**Created:** 2026-10-10 (Step 4 of the docs-first Fireworks preparation recorded in
[`.junie/plans/fireworks-training-preplan.md`](../../.junie/plans/fireworks-training-preplan.md))
**Status:** a conditional roadmap only. Phase 1 and the Phase 3 requests were granted 2026-10-10 (packages doc); Phase 2's local emission is executed (export plan §9). The upload (Package F) is **executed** on the replacement account `linencloset` (pilot log §7); spend is capped (Package G, $635, $0 incurred); deployment remains un-approved. This document provisions nothing, uploads nothing, spends nothing, and contains no executable commands.
**Companion:** [`fireworks-readiness.md`](./fireworks-readiness.md) — the status register. The October 10 decisions (D1–D4) settled target role, ledger contract, model shortlist, and the leakage-adapter design; provider facts are verified (readiness §2). The D4 adapter is implemented and the local emission executed and verified (2026-10-10, export plan §9; nothing left this environment). The remaining pending items — licensing, consent, privacy approval, budget, and a named experiment owner — are the entry conditions for Phase 1; signable packages: [`fireworks-approval-packages.md`](./fireworks-approval-packages.md).

---

## 1. Decision record (docs-first choices already made)

- **Documentation before implementation:** two shared documents (readiness register + this roadmap) instead of a CLI skeleton, credentials setup, or new dependencies.
- **Target role — decided October 10 on the owner's delegation (D1):** therapist-response SFT using the accepted-arc export mapping (client→user, therapist→assistant). Ratified at the Phase 1 gate. Patient simulation and supervision remain out of scope pending their own target-specific data.
- **Ledger contract — decided (D2):** the 9-field ledger stays inline in the assistant turn (the corpus's native shape); the `reasoning_content` variant (ledger as a native thinking trace) is the follow-up A/B, not the pilot; serving disposition stays a release-gate item.
- **Base-model shortlist — decided (D3):** no Llama models (standing owner preference). The initial recommendation was GLM 5.3 Flash, with Qwen 3.8 27B as runner-up. Owner instruction on October 10, 2026 superseded that recommendation and selected Muse Glimmer 30B (Fireworks model ID `accounts/fireworks/models/muse-glimmer-30b` — the verified catalog ID; the short `glimmer-30b` slug does not resolve). Access, managed-LoRA eligibility, and pricing are verified 2026-10-10 (pilot log §9); see readiness update 4 and approval-packages §6.
- **Leakage adapter design — decided (D4):** the Phase 2 exporter must emit explicit `source_family`/`source_id` grouped at seed-scenario level (11 seed scenarios are shared across arcs; the current splitter's keys cover no gold rows at all). Implemented and executed locally 2026-10-10 (export plan §5, §9).
- **DPO deferred:** internal preference pairs exist ([`ai/training/build_arc_dpo.py`](../../ai/training/build_arc_dpo.py)) but are not provider-compatible, not validated turn-level, and their prompts are reconstructed. DPO is considered only after preference-context and privacy validation.
- **No deadline planning:** the vendor email's October 31 date is not a planning input.

## 2. Conditional roadmap

Every phase requires the previous phase's exit evidence **and a separate explicit owner approval**. If any readiness item stays pending, the chain stops.

| Phase | Entry condition | Work | Exit evidence | Approval needed |
|-------|-----------------|------|---------------|-----------------|
| 1. Target & vendor decisions | Readiness register: licensing, consent, privacy-approval items resolved; D1–D3 ratified (target role, ledger contract, final model pick) | Confirm the decided target (D1) and output contract (D2); pick the final model from the D3 shortlist; confirm account-level model access and privacy terms | Signed decision record naming target, contract, final model ID, and the privacy determination — packages A–E in [`fireworks-approval-packages.md`](./fireworks-approval-packages.md) — **granted and complete 2026-10-10** (final model GLM 5.3 Flash; account-level quota check pending a live account) | owner — granted |
| 2. Export plan | Phase 1 complete | Read-only inventory; immutable approved snapshot identity; seed-level grouped splits per the D4 adapter (explicit `source_family`/`source_id` metadata); schema/token validation; privacy screening. Provider-only payload separated from private provenance | A reviewable export plan with snapshot identity and screening results; nothing exported yet — **delivered and executed locally 2026-10-10** per the owner's instruction ([`fireworks-export-plan.md`](./fireworks-export-plan.md) §9: 576 rows emitted and verified; nothing left this environment; upload remains gated on Phase 1 + budget) | owner (export) — **granted 2026-10-10 for the local emission; executed** |
| 3. Bounded experiment | Phase 2 approved | Small format smoke test first; then an explicitly budgeted SFT pilot. No production switch, no deployment | Smoke-test result; budgeted pilot run report — packages F–H in [`fireworks-approval-packages.md`](./fireworks-approval-packages.md) | owner (budget + experiment) — packages G–H — **granted 2026-10-10**; upload executed (pilot log §7); step 1 (Render Samples) executed and verified, steps 2–3 **blocked at the budget gate** — cost basis corrected ≈9× upward (unrolling; pilot log §10), re-authorization required |
| 4. Evaluation before expanding | Phase 3 complete | Compare untuned vs. tuned on held-out cases including ordinary non-crisis controls; record safety, factual fidelity, continuity, format validity, latency, cost | Evaluation report; clinician review (release prerequisite, not certifiable by automated checks) | owner (release) |
| 5. Follow-ons, considered separately | Phase 4 review passed | DPO (after preference-context + privacy validation); serving integration (after evidence) | New pre-plans with their own approval boundaries | owner |

## 3. Verification status (research completed 2026-10-10; sources in readiness §2)

- **Provider eligibility — verified:** 44-model training catalog; managed SFT is LoRA for most open models; tunable non-Llama candidates include GLM 5.x, DeepSeek V4, Kimi, Qwen, Mistral, Gemma, MiniMax, Nemotron. Account-level confirmation (quota, tier, model access policy) still happens at Phase 1 sign-off.
- **Promotion — verified:** trained models evaluate first, then serve only on dedicated deployments (`firectl deployment create`); serverless serving is unavailable for tuned models; no serving surcharge over base-model price. Retention/rollback specifics for the tuned artifact are read at Phase 2/3 time from the provider's current docs.
- **Serving economics — verified (list prices):** training ≈$44/epoch for the arc corpus (≈4.36M tokens) in the >300B class; dedicated serving $8–20/GPU-hour (1.5× region-restricted). Training cost is not the budget constraint; dedicated serving is. **No budget exists; budget approval is a separate gate.**
- **Privacy terms — partially verified:** provider mechanisms exist (Zero Data Retention policy, Secure Training surfaces, BYOB, CMEK); their applicability to a chosen surface/tier and the data-processing agreement itself are account-level items for the owner.

## 4. Candidate code (requires later assessment, not approval)

- [`ai/training/consolidate_arc_corpus.py`](../../ai/training/consolidate_arc_corpus.py) — the arc exporter (client→user, therapist→assistant, ledger retained in assistant content). Candidate corpus source; target-role and ledger decisions in Phase 1 determine any needed variant.
- [`ai/training/dataset_splitter_stratified.py`](../../ai/training/dataset_splitter_stratified.py) — grouped, leakage-checked splitting. Its source-family keys must be inspected for coverage of seed cases, arcs, and regenerations before reuse (readiness item 9).
- [`ai/training/build_arc_dpo.py`](../../ai/training/build_arc_dpo.py) — internal preference pairs from revision history. Not a provider payload; Phase 5 candidate only.
- [`ai/training/export_fireworks_payload.py`](../../ai/training/export_fireworks_payload.py) — the Phase 2 emitter, written at execution under the export plan (fail-closed identity/census/deviation assertions, atomic writes, `--dry-run` supported). Executed locally 2026-10-10; output stays local under `ai/training/output/`.

## 5. Deferred contracts (conceptual only; no schema implementation now)

Approved snapshot identity · source lineage records · deterministic grouped splits · provider-only payloads separated from private provenance · experiment/evaluation metadata. Any schema work is Phase 2 output, separately approved.

## 6. Approval boundaries

Four gates, each requiring separate explicit owner approval, none granted by this document: **export** (data leaves this environment), **upload/provisioning** (anything created at the provider), **spend** (any paid job or endpoint), **deployment** (any user-visible behavior change). Documentation imposes no runtime requirements; later tooling must be reproducible, resumable, memory-bounded on large corpora, and must never log sensitive content.

## 7. Non-goals

No CLI skeleton, new dependencies, credential setup, automated evaluation subsystem, corpus freeze, sampling or conversion runs, uploads, paid jobs, or production changes — all remain out of scope until separately approved.

## 8. Self-check (2026-10-10)

- Every phase is conditional; nothing implies training has begun or will begin.
- No executable commands appear; code is referenced by path as candidate material.
- Links resolve; the readiness register is the single source for item statuses; no counts are duplicated here.
- Approval boundaries are explicit; Phase 1 and the Phase 3 requests were granted 2026-10-10 (packages doc). The upload is executed on the replacement account — train+val only left this environment; no spend incurred; deployment remains un-granted.
