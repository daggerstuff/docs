# Training Record Phasing — Authoritative Spec

**Created:** 2026-09-01 (Step 1 of the Clinical Training Dataset & Nightmare Fuel Pipeline, tracker: `.agent/internal/plans/2026-09-01-clinical-nf-pipeline-tracker.md`)
**Purpose:** Single source of truth for the 5-stage training-record phasing model — stage definitions, quotas, classification, dedup policy, manifest layout, and split conventions. Steps 7–9 (generation, consolidation) validate against this doc.

**Authoritative code:**
- Stage model + quotas + splits: `ai/pipelines/orchestration/stage_organizer.py` (PIX-4193)
- Dedup policy: `ai/pipelines/ingestion_deduplication.py` (PIX-4192)
- V7 consolidation path (same policy): `ai/pipelines/data_processing/orchestration/consolidate_v7.py`
- Streaming variants: `s3_stage_organizer.py` (S3 → gdrive via `S3Streamer`), `stage_organizer_streaming.py` (two-pass, memory-bounded)
- Stage 5 ingestion: `ai/pipelines/dpo_ingestion.py` (PIX-4199)

---

## 1. The five stages

| # | Stage ID | Purpose | Target % (code) | Quality profile (empathy / clinical / safety floors) |
|---|----------|---------|-----------------|------------------------------------------------------|
| 1 | `stage1_foundation` | General psych/mental-health foundation | **0.35** | 0.70 / 0.30 / 1.0 |
| 2 | `stage2_therapeutic_expertise` | Modality-grounded clinical work (CBT, DBT, EMDR, …) | 0.25 | 0.75 / 0.50 / 1.0 |
| 3 | `stage3_edge_stress_test` | Edge cases + nightmare fuel (adversarial stress) | 0.20 | 0.60 / 0.40 / 1.0 |
| 4 | `stage4_voice_persona` | Voice/persona tone data (YouTube persona distillation) | 0.15 | 0.80 / 0.35 / 1.0 |
| 5 | `stage5_safety` | Safety/DPO preference data | 0.05 | 0.65 / 0.45 / 1.0 |

⚠️ **Documented-vs-code discrepancy:** the MTGC planning docs and the approved plan say Stage 1 = **40%**, but `DEFAULT_STAGE_CONFIGS` in `stage_organizer.py` sets **0.35**. The code value is what executes. Quotas are soft (see §4), so the effective ratio is emergent either way. Reconciliation decision is deferred to Steps 7–9; this doc records the code value as executable truth.

Historical closure status (PIX-4192/4193/4194/4195/4199, all DONE): Stages 1–4 closed in the MTGC sprint; Stage 5 DPO deferred (partial data only, PAL DPO 148KB). Stage 5 is being revived by the `safety_dpo_pairs_10k` corpus in this pipeline run.

---

## 2. Record schema (ChatML)

Each record is a JSONL line:

```json
{
  "messages": [{"role": "system|user|assistant", "content": "..."}],
  "metadata": {
    "stage": "stage3_edge_stress_test",
    "source": "nightmare_fuel | edge_cases | t1_gold | persona | safety_dpo_pairs_10k | ...",
    "topic_tags": ["edge_case", "crisis"],
    "therapeutic_modality": "",
    "conversation_id": "...",
    "crisis_intensity": "extreme|very_high|high|..."
  }
}
```

Classification inputs: `source` (top-level or metadata), `metadata.topic_tags`, `metadata.therapeutic_modality`. Provenance fields added at consolidation (Step 9): `source`, `family` (10-family taxonomy), `generated_at`.

Edge-case preservation bypass: records tagged `is_training_edge_case: true` pass quality gates that would otherwise filter high-crisis content (MTGC P0-2).

---

## 3. Stage classification (`classify_record`)

Keyword-driven, evaluated in **strict priority order** — first match wins:

1. **Stage 5 (Safety):** source ∈ {safety, crisis_intervention, harm_prevention, suicide_prevention, self_harm, crisis_hotline} or any tag ∈ {safety, crisis, self_harm, suicide, harm_prevention, emergency, crisis_response, mental_health_crisis}
2. **Stage 4 (Voice/Persona):** source ∈ {pixel_voice, voice_persona, dual_persona, persona} or tag ∈ {voice, persona, dual_persona, personality, character, role_play}
3. **Stage 3 (Edge/Stress):** source ∈ {edge_cases, adversarial, stress_test, jailbreak, red_team, safety_test} or tag ∈ {edge_case, adversarial, stress_test, jailbreak, red_team, crisis, boundary_test}
4. **Stage 2 (Therapeutic):** `therapeutic_modality` ∈ {cbt, dbt, psychodynamic, emdr, act, mbct, ipt, sfbt, gottman, somatic, trauma_informed, attachment_based} or tag ∈ {therapy, counseling, psychotherapy, clinical, diagnosis, treatment_plan, intervention, therapeutic_technique, case_study}
5. **Stage 1 (Foundation):** tag ∈ {psychology, mental_health, general, education, self_help, wellness, mindfulness, communication, emotional_intelligence}
6. **Default → Stage 1** for any unclassified conversational content.

⚠️ Tag collision note: `crisis` is a Stage 5 tag **and** a Stage 3 tag. The priority order means a record tagged `crisis` lands in Stage 5, not Stage 3. New pipeline-generated records must be tagged deliberately: crisis-*safety* content (correct crisis handling demonstrations) vs adversarial *stress* content (`edge_case`/`adversarial` tags, no `crisis` tag) unless it is genuinely a safety-behavior exemplar.

---

## 4. Quota enforcement — soft, no silent data loss

`enforce_quotas` treats stage percentages as **soft capacity targets**, not hard caps (P0-4 policy):

- Under-target stages keep **all** their records.
- Over-target overflow is covered by redistributable slack (unused capacity of under-target/missing stages).
- If overflow exceeds slack, records are **retained anyway** with a logged warning — no record is ever silently discarded.
- Stage ratios in the final output are therefore emergent; the ±2% distribution gate (8-Gate validation) is checked, not enforced by truncation.

---

## 5. Dedup policy (PIX-4192)

Implemented in `ai/pipelines/ingestion_deduplication.py` (shared by `consolidate_v7.py`):

**Primary hash (content-based, default):**
`sha256( lowercase( concat( messages[i].role + messages[i].content for all i ) ) )`
- Normalization: role+content pairs concatenated, whole string lowercased, UTF-8. Empty/missing `messages` → sha256 of empty bytes.

**Secondary hash (metadata-based, opt-in `--use-secondary-hash`):**
`sha1( conversation_id + stage + source + crisis_intensity )`
- Catches near-duplicate content re-shipped under different metadata; never the default gate.

**Conflict resolution (stage priority, higher wins):**

| Stage | Priority |
|-------|----------|
| `stage4_voice_persona` | 5 |
| `stage3_edge_stress_test` | 4 |
| `stage2_therapeutic_expertise` | 3 |
| `stage1_foundation` | 2 |
| `supplementary` | 1 |

- Same primary hash seen twice → keep the higher-priority stage's record; count as `stage_conflicts_resolved`.
- Equal priority → first-seen wins; the later record counts as `duplicates_removed`.

⚠️ **Known gap:** `STAGE_PRIORITY` has no `stage5_safety` entry — a Stage 5 record's `get_stage_priority()` returns the default 1 (ties with `supplementary`). Stage 5 records currently lose all collisions. Fix candidate for Step 9's consolidator work (add `stage5_safety: 6`, above voice, since safety exemplars must never be dropped in favor of tone data — or at minimum 5 to break the tie).

---

## 6. Manifest layout

Output root (default): `ai/training_data_consolidated/final/`

```
ai/training_data_consolidated/final/
├── MASTER_STAGE_1.jsonl          # consolidated per-stage records
├── MASTER_STAGE_1_train.jsonl    # 80%
├── MASTER_STAGE_1_val.jsonl      # 10%
├── MASTER_STAGE_1_test.jsonl     # 10%
├── MASTER_STAGE_2.jsonl (+ _train/_val/_test)
├── MASTER_STAGE_3.jsonl (+ _train/_val/_test)
├── MASTER_STAGE_4.jsonl (+ _train/_val/_test)
├── MASTER_STAGE_5.jsonl (+ _train/_val/_test)
└── manifests.json                # index: [{stage, target_percentage, actual_count,
                                  #   quality_profile, split_counts, manifest_file, output_path}]
```

Per-stage `StageManifest` metadata: `stage`, `target_percentage`, `actual_count`, `quality_profile`, `split_counts {train, val, test}`, `manifest_file`, `output_path`. Stages with zero records are skipped (no empty manifests).

**Flat gold:** `ai/data/curated/sft_chatml/train_master_gold.jsonl` (189,122 records / 379 MB at 2026-09-01 baseline) is the *stage-unaware* master. Per Decision 4, consolidation (Step 9) appends gate-passing records to **both** the correct `MASTER_STAGE_N.jsonl` and the flat gold, with hash dedup on each side.

---

## 7. Split conventions

**Stage organizer (this spec's path):** `split_dataset` — 80/10/10 train/val/test, per-stage shuffle with `random.Random(seed=42)`, split AFTER classification and quota enforcement.

**Do not conflate** with the release-manifest splitter: `ai/training/data/dataset_splitter_stratified.py` uses **70/15/15** (8-axis stratified, hash-disjoint + source-family-disjoint integrity gates, ±2pp tolerance) for the DVC-tracked release path (blueprint §7.1). Two different consumers: stage manifests feed staged SFT curriculum; the stratified splitter produces release-grade train/val/test JSONLs with DVC pointers. A record's val/test membership in one path says nothing about the other.

---

## 8. Streaming variants

| Module | Read | Write | Use when |
|--------|------|-------|----------|
| `stage_organizer.py` | local JSONL shards (in-memory) | local FS | small/medium datasets |
| `stage_organizer_streaming.py` | local JSONL (two-pass) | local FS | datasets too large for memory |
| `s3_stage_organizer.py` | S3 via `S3Streamer` (line-by-line, never bulk-download) | gdrive via rclone | remote staged assets (Step 6/9 constraint) |

**Stage 5 path:** `ai/pipelines/dpo_ingestion.py` normalizes HF preference datasets (mlx-community/Human-Like-DPO, flammenai/character-roleplay-DPO, PJMixers/unalignment_toxic-dpo-v0.2 → `{prompt, chosen, rejected}`) and writes `MASTER_STAGE_5.jsonl` directly. The `safety_dpo_pairs_10k` corpus joins this path in Step 8.

---

## 9. Where new pipeline output lands (Steps 7–9 mapping)

| New data | Stage | Route |
|----------|-------|-------|
| Edge cases + nightmare fuel (+50k) | Stage 3 | generate → cliché gate (Step 5) → dedup → `MASTER_STAGE_3.jsonl` + gold append |
| Clinically-backed (+25k): T1_GOLD textbook path | Stage 1–2 | classify via modality/tags → Stage 1 or 2 manifests + gold |
| Clinically-backed (+25k): JMIR / `clinical_redteam` | Stage 3 (adversarial red-team) or Stage 5 (safety exemplars) — per §3 tag rules | same |
| `safety_dpo_pairs_10k` | Stage 5 | `dpo_ingestion.py` path |
| Persona distillation output | Stage 4 | voice pipeline → persona records → `MASTER_STAGE_4.jsonl` + gold |

Every appended record: provenance (`source`, `family`, `generated_at`), primary-hash dedup against existing stage manifest + gold, append+fsync with checkpoint (Step 9).

---

## 10. Open items for Steps 7–9

1. **Stage 1 quota 40% (docs) vs 35% (code)** — pick one before consolidation; if 40% wins, update `DEFAULT_STAGE_CONFIGS`, else amend the MTGC docs' historical note (code is authoritative for execution).
2. **`stage5_safety` missing from `STAGE_PRIORITY`** — add before any Stage 5 consolidation so safety records don't lose collisions.
3. **`crisis` tag double-booking** (Stage 5 vs Stage 3) — define the tagging convention for generated edge/nightmare records in the Step 7 generator config.
4. **8-Gate validation** (coverage, distribution ±2%, hash gate across stages, …) — run at consolidation time, not per-shard.
