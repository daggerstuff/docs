# Training Pipeline Blueprint — Audit (2026-08-24)

Audit of `docs/training-pipeline-blueprint-2026-08-10.md` (751 lines). Every claim checked
against repo code, git history, and external sources. Dates ignored — verdict is "as of now".

**Verdict: ~60% describes real code; ~40% is aspirational, stale, or broken.** The curation
half is genuinely built. The training half is scaffolding with broken imports, mock
benchmarks, missing dependencies, and fabricated version pins — plus a model-selection error
that violates a permanent user rule.

---

## 1. Lineage (why it looks old)

The doc is a merge of ~6 separate plans, deleted over the prior year, re-stamped `2026-08-10`:

| Source doc | Created | Folded into |
|---|---|---|
| `docs/ops/training.md` → `docs/guides/training.md` | 2025-10-07 | SFT/DPO/ORPO + LoRA/QLoRA |
| `docs/infrastructure/foundation-model-training-setup.md` | 2025-10-26 | Tech stack, Docker, DeepSpeed, Git/DVC |
| `docs/phase2-model-development-guide.md` | 2026-01-07 | Base models + eval/forgetting (§1, §7) |
| `docs/phase1-data-pipeline-workflow.md` | 2026-01-07 | Dataset curation (§4, §5, App B) |
| `docs/guides/training/PIXEL-MODEL-TRAINING-HUB.md` | 2026-01-09 | Training hub / action plan |
| `docs/plans/2026-01-31-unified-ai-dataset-pipeline.md` | 2026-01-31 | Unified dataset pipeline (App B) |
| `docs/product/training-scenarios.mdx` | 2026-02-23 | Training scenarios |
| `business-strategy/specialized-training-modules.md` | 2026-05-07 | Domain/specialized framing |
| `.ai/internal/plans/2026-05-06-dact-08-freeze-v1-training-slice.md` | 2026-05-06 | v1 freeze language |

Root problem: merge flattened ~9 months of decisions with no per-section dates and no
reconciliation against later user preferences.

---

## 2. Claim-by-claim verdict

### Appendix B — dataset curation (mostly real, some stubs)

| Blueprint claim | Verdict | Evidence |
|---|---|---|
| MinHash/LSH dedup (128 perms/16 bands/8 rows) | ✅ True | `dedup_normalize.py:129-141` exact |
| SHA-256 exact dedup | ✅ True | `_content_hash` uses `sha256` |
| SimHash cross-source dedup | ❌ Missing | no SimHash anywhere; blueprint itself says "add SimHash" |
| Presidio PII (2-layer) | ⚠️ Partial | entities differ: `CRYPTO`/`US_PASSPORT` added; `PERSON`/`LOCATION` removed |
| PII Layer-3 LLM pass | ❌ Missing | `pii_scrubber.py` is an 83-line script, zero LLM |
| `ALLOWED_LICENSES` SPDX set | ✅ True | exact 6 licenses match |
| ClinicalValidityJudge 6-dim rubric | ✅ True | technique/alliance/structure/cultural/ebp/dsm5 exact |
| Judge "generalize to non-clinical" | ❌ Not done | judge still clinical-only |
| QualityTiers T1–T4 | ✅ True | T1_GOLD/T2_SILVER/T3_BRONZE/T4_SAFETY + counts |
| Hash split `% 100` bucket | ✅ True | `dataset_splitter.py:63-64` |
| Stratified split (4-axis) | ⚠️ Half-true | exists but NOT multi-label stratified — hash-bucketing per stratum |
| Split integrity gates ±2pp | ✅ True | implemented |
| IAA Fleiss/Cohen kappa, 0.75/0.85 | ✅ True | `annotation/iaa.py` exact |
| SDG self-instruct (~200 seeds, k=4, N=10000) | ⚠️ Partial | code exists, seed `self_instruct_seed.jsonl` missing |
| SDG back-translation / paraphrase | ✅ True | files exist |
| Golden judge calib (200-sample) | ⚠️ Placeholder | ids `neon-consensus-0000`; warns "synthetic/placeholder" |
| DVC init + S3/MinIO remotes | ✅ True | `ai/.dvc/config` |
| `ingest_router.py` web/DOCX/API | ✅ True | source_type routing + python-docx |

### Tech stack (App C/D) — mixed

| Claim | Verdict |
|---|---|
| `docker-compose.gpu.override.yml` exists | ✅ True (repo root, not `docker/`) |
| Axolotl config exists | ✅ True — but `base_model: LatitudeGames/Wayfarer-2-12B`, not Qwen/Llama |
| Axolotl primary framework | ⚠️ 1 stale yaml; no `qwen32b-sft.yaml` (App C references a nonexistent file) |
| DeepSpeed ZeRO-3 config | ❌ Not implemented — zero `deepspeed` import; JSON in App D not in repo |
| `requirements_training.txt` pins `torch>=2.13`, `transformers>=5.14` | ⚠️ Fabricated — these versions don't exist |
| Python 3.11 + torch 2.4.0 (§6) | ❌ contradicts requirements file |

### Training infra — mostly broken

| Claim | Verdict |
|---|---|
| QLoRA train scripts | ⚠️ Broken — `train_moe_h100.py`/`train_optimized.py` import missing modules → crash |
| DPO trainer | ⚠️ imports `trl`; `trl` not in any requirements file |
| GRPO trainer | ⚠️ imports `trl`, guarded `ImportError`, not in requirements |
| Catastrophic forgetting metric | ⚠️ Mock only — `benchmark_runner.py` docstring: "CPU-mock… deterministic mocks" |
| DeepSeek-R1 "800K curated > 10M unfiltered" | ❌ Misattributed — R1 paper uses 800K samples, no such comparison |
| NeMo/FSDP2 App A | ⚠️ Doc-only, faithful to skill, zero code in repo |

### Models (§1) — the smoking gun

| Claim | Verdict |
|---|---|
| Llama 3.3/3.2 recommended | ❌ Violates permanent rule "NEVER use Llama" (memory `196c0f3b413a34ee`, trait/permanent) |
| Qwen 2.5 recommended | ✅ Allowed ("GLM, Qwen, Mistral") |
| "DeepSeek-R1-7B/14B distilled" | ⚠️ R1 distill line is Qwen/Llama 1.5B–70B; no 7B/14B variant |

---

## 3. Done vs not

**Real, working (verified):** dedup (MinHash/LSH/SHA), provenance+SPDX gate, QualityTiers,
hash split, IAA kappa, dual-judge, stratified splitter + integrity gates, DVC remotes, ingest
router, SDG modules, `docker-compose.gpu.override.yml`.

**Stub/placeholder/broken:** MoE train scripts (missing modules), DPO/GRPO (missing `trl`),
benchmark harness (mock), golden calib set (placeholder), SDG seed file (missing).

**Not built / fiction:** DeepSpeed ZeRO-3, FSDP2/Megatron distributed training, real GPU run,
real catastrophic-forgetting eval, Axolotl Qwen/Llama config.

**Contradicts preferences:** Llama 3.3/3.2 in §1, §5, §6, App C, action plan, dual-judge secondary.

---

## 4. Remaining gaps (not yet fixed)

- `S3DatasetLoader` has only `stream_jsonl`; train scripts reference `load_json`,
  `get_s3_dataset_path`, `load_dataset_from_s3` (never implemented).
- `trl` / `flash_attn` absent from all requirements files.
- `self_instruct_seed.jsonl` missing.
- Golden calib set is placeholder data.
- `benchmark_runner.py` is CPU-mock; no real lm-evaluation-harness wiring.
- Distributed training (App A) has no implementation.
