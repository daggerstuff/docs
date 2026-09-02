# AI Training Pipeline Blueprint — Corrected (Aug 2026)

> **Status legend** — every section is tagged with what actually exists in the
> repo, verified against code on 2026-08-28:
>
> - `SHIPPED` — code exists and matches the description.
> - `PARTIAL` — code exists but incomplete / mock-backed / not wired end-to-end.
> - `PLANNED` — described in a plan but **no code exists yet**.
> - `DOC ONLY` — guidance only; not code.

Audit of the prior revision (`training-pipeline-blueprint-2026-08-10.md`)
produced `docs/TRUTH.md`. This document is the corrected rewrite. It drops the
fabricated claims (Lambda/AWS Activate credits, `zai-org/GLM-4.5` judge, the
`QualityTiers` symbol, "greenfield" assumption) and replaces stale prices/model
lists with current data.

---

## 0. Reality Check: This Is Not Greenfield

**The prior doc's opening assumption was false.** The repo already ships a
mature mental-health training-data pipeline. The training *code* largely exists
as a family of modules in `ai/training/` (69 files). What is missing is not the
data machinery — it is (a) a verified end-to-end training *run*, (b) the
distributed-training layer, and (c) real base-model choice for the actual
product.

---

## 1. Foundational Models (current landscape)

### 1.1 What the repo actually references (`SHIPPED`)

Not a recommendation list — a census of model IDs hardcoded in `ai/training`:

| Model ID | Used by | Role |
|---|---|---|
| `Qwen/Qwen2.5-32B` | `orpo_trainer.py`, `orpo_axolotl.yaml`, `prune_adapter.py` | SFT/ORPO base |
| `Qwen/Qwen2.5-72B-Instruct` | `distill_model.py`, `llm_quality_judge.py` | teacher / primary judge |
| `meta-llama/Llama-3.3-70B-Instruct` | `llm_quality_judge.py`, `dual_judge.py` (`llama3.3:70b`) | secondary judge |
| `LatitudeGames/Wayfarer-2-12B` | `configs/axolotl.yaml` | the **only** config actually wired to a concrete base |
| `@cf/zai-org/glm-5.2` | `nightmare_fuel_generator.py` | adversarial SDG generator |
| `ornith:9b` | `generalized_sdg_pipeline.py` | multi-session SDG generator |
| `mistral-nemo` | `sdg_pipeline.py`, `dedup_normalize.py` default | SDG / tokenizer default |

### 1.2 Field guidance for mental-health fine-tuning (`DOC ONLY`)

Current (2025-2026) peer work in clinical counseling fine-tunes **7-13B
instruct** models, not 32-72B:

- **oMind** (2025): LoRA + DPO on `Llama-3.1-8B`, `Mistral-7B-v3`,
  `Qwen2.5-7B`; oMind-Qwen tops expert-rated empathy and MCQA.
- **counseLLM** (2025): `Llama-3.1-8B-Instruct`, 2-stage SFT(36K)→DPO(2K),
  QLoRA r=64/α=128, H100, ~3h SFT + ~30m DPO.
- **PsyLLM** (2025-2026): diagnostic+therapeutic reasoning, SOTA on
  PSYCHEPASS (2026-04), LLaMA-Factory pipeline.

**Recommendation** (align with the repo's real code and the field): primary
candidate `Qwen/Qwen2.5-7B-Instruct` or `Qwen/Qwen2.5-32B` (already referenced
by `orpo_trainer.py`). Do **not** recommend GLM-4.5-Air as the judge — no judge
code uses it. For judge models, keep the shipped `Qwen2.5-72B-Instruct` +
`Llama-3.3-70B-Instruct` pair.

---

## 2. Optimization & Fine-Tuning Techniques

### 2.1 SFT vs Preference Alignment (`SHIPPED`)

- **SFT** — `finetune_model.py`, `mental_ift_trainer.py`, `train_llama3_1_qlora_h100.py`.
  Default 3 epochs, LoRA.
- **DPO** — `dpo_trainer.py` (`--base_model_checkpoint`, preference pairs).
- **ORPO** — `orpo_trainer.py` + `configs/orpo_axolotl.yaml` + `ds_config_zero3.json`
  (single-pass, no reference model). **Shipped and tested**
  (`tests/test_orpo_integration.py`, `tests/test_orpo_trainer.py`).
- **GRPO** — `grpo_trainer.py` (pure-Python reward).
- Order: SFT → DPO/ORPO/GRPO. All three preference trainers exist.

### 2.2 Parameter-Efficient Methods (`SHIPPED` / `PARTIAL`)

- **QLoRA** — `bitsandbytes` NF4 + double-quant (`pyproject.toml` ships
  `bitsandbytes>=0.49.2`). LoRA r=64/α=128 in `orpo_axolotl.yaml`.
- **DoRA** — flag exists (`orpo_trainer.py` `--adapter-variant dora`). `PARTIAL`
  (passthrough, not independently verified).
- **AdaLoRA / VeRA** — `DOC ONLY` (mentioned, no code).

### 2.3 Pruning + Distillation (`PARTIAL`)

- **Pruning** — `prune_adapter.py` (L1-unstructured on adapter weights, 0.3
  default, <5% quality-loss gate). `PARTIAL` (mock smoke-testable; no real run).
- **Distillation** — `distill_model.py` (KD, teacher `Qwen2.5-72B-Instruct`,
  DeepSpeed ZeRO-3 passthrough). `PARTIAL`.
- **Quantization** — `quantize_model.py` (AWQ / GPTQ / GGUF q4_k_m). `PARTIAL`
  (harness only; no produced artifacts).
- The "95% quality / 30-50% params" and "7B student on 2×A100" figures are
  heuristics, **not measured** — treat as targets, not results.

---

## 3. GPU Cloud Providers & Hardware (current, sourced Aug 2026)

Prices are on-demand USD/GPU-hr, from Aug-2026 public listings. Ranges, not
commitments; verify before spend.

| Provider | H100 SXM 80GB | H200 141GB | B200 | Notes |
|---|---|---|---|---|
| RunPod | ~$1.99-3.29 | ~$2.69-4.59 | — | per-second billing; community cloud = spot-equivalent |
| GMI Cloud | ~$2.00 | ~$2.60 | — | no min commit, single-GPU ok |
| Lambda Labs | ~$2.86-3.99 | ~$4.49-5.29 | ~$4.99-6.99 | no spot; on-demand fixed |
| CoreWeave | ~$4.25-6.16 | ~$6.31 | ~$6.50-8.60 | 8-GPU min; contract-oriented |
| Nebius | — | ~$5.50 | ~$5.50 | — |
| AWS p5 | ~$6.88 | ~$8.00+ | — | hyperscaler premium |
| Vast.ai | dynamic (below RunPod) | — | — | marketplace, no SLA |

**Reserved** (for sustained training): CoreWeave H100 1yr ~$1.79/GPU-hr;
AWS p5.48xlarge 1yr RI ~$2.40/GPU; Lambda 6mo+ ~$1.69/GPU (est.).

**Hardware guidance** (unchanged physics):

- H100 SXM5 80GB: best $/perf for 7-70B LoRA/QLoRA; ~3.35TB/s HBM3.
- H200 141GB: for long-context (128K+) and 70B+ full-param.
- B200 180GB: only if budget + throughput demand justify ~2× H100 cost.
- A100 80GB: viable 8-13B only.

**Recommendation for this repo**: start **RunPod H100** or **GMI H100** for SFT/
DPO/ORPO (QLoRA 7-32B fits one 80GB card). Move to **Lambda/CoreWeave reserved**
only for sustained 70B+ or distillation. The prior doc's "Lambda AWS Activate
$500-1000 credits" claim is **removed** — Lambda is not an AWS Activate partner.

---

## 4. Dataset Curation & Formatting

### 4.1 Format (`SHIPPED`)

The repo standard is **ChatML JSONL** (one line per sample), produced by
`curate_pipeline.py` into `sft_chatml/`, `sft_alpaca/`, `sft_alpaca_chatml/`,
`safety/`. `format_chatml.py`, `merge_final_dataset.py`, `dedup_normalize.py`
all emit/consume this. Parquet is archival-only (via `datasets` +
`to_parquet()`); no shipped parquet pipeline is wired end-to-end.

### 4.2 Schema (`SHIPPED`)

The real `to_chatml()` output record shape (`curate_pipeline.py`):

```json
{
  "messages": [ { "role": "system", "content": "..." },
                { "role": "user", "content": "..." },
                { "role": "assistant", "content": "..." } ],
  "source": "reddit_mental_nlp",
  "task_type": "therapy_response_generation",
  "tier": "T2_SILVER",
  "diagnostic_tag": null,
  "demographic_tags": [],
  "linguistic_style": null,
  "clinical_reviewed": false,
  "mi_quality": ""
}
```

Note: the prior doc's hypothetical `conversation_id` / `domain` / `language` /
`quality_score` / `annotation_stage` / `tags` / `date` fields are **not** what
the shipped `to_chatml` emits. The shipped fields are above. Provenance fields
are attached separately by `provenance.py:build_provenance` and are **not**
present in the SFT output record.

---

## 5. Dataset Sizing & Quality

### 5.1 Real tier sizes (`SHIPPED`, from `curate_pipeline.py` docstring)

| Tier | Definition | Approx count |
|---|---|---|
| `T1_GOLD` | `clinical_reviewed=True` or `mi_quality=high` | ~133 |
| `T2_SILVER` | multi-turn (5+ msgs), non-adversarial | ~65K |
| `T3_BRONZE` | 3-msg classification, downsampled | ~120K (from ~785K) |
| `T4_SAFETY` | `task_type=adversarial_safety` | ~51K |

- Downsampling: `reddit_mental_nlp` 0.17 (597K→~100K),
  `reddit_mental_health_posts` 0.50 (88K→~44K). Deterministic hash-bucket.
- The shipped split is **70/15/15** (`SPLIT_RATIOS`, `assign_split`), not 80/10/10.

### 5.2 DVC status (`PARTIAL`)

Real, tracked in the `ai` submodule:

- `.dvc` pointers: `ai/data/curated/sft_chatml/{train,val,test}.jsonl.dvc`
  (sizes 166.6MB / 35.3MB / 35.8MB).
- Remote (from `ai/.dvc/config`):

```ini
['remote "pixelated_s3"']
    url = s3://whitebat/dvc
    region = nyc1
    endpointurl = https://objectstore.nyc1.civo.com
```

- **Gaps**: no `ai/data/curated/.gitignore`, no root `dvc.yaml`/`dvc.lock`, and
  the remote is Civo object store, **not** AWS S3 us-west-2. The prior doc's
  `s3://pixelated-datasets/dvc` + `us-west-2` block is wrong.

### 5.3 Quality gates (`SHIPPED`)

- Stage 1 filters: `stage1_filters.py` (language, PII, toxicity, dedup). Real.
- Stage 2 dual-judge: `dual_judge.py` / `llm_quality_judge.py`. Real.
- Stage 3 IAA: `annotation/iaa.py` (Fleiss κ≥0.85 gold / 0.75 min). Real.
- Synthetic QC: `synth_qc_gate.py` (0.80 quality / 0.30 fraction / 0.05 spot).
  Real.
- **Known defect**: `ai/training/data/golden_judge_calib.jsonl` (200 lines) is
  generic `neon-consensus-*` content, **not** mental-health domain. It is not
  fit as the Stage-2 judge calibration gate until replaced with domain samples.

---

## 6. Tech Stack & Software Setup

### 6.1 Python (`SHIPPED`)

`ai/pyproject.toml` pins: `transformers>=5.14.1`, `datasets>=2.19.0`,
`accelerate>=0.33.0`, `peft>=0.11.0`, `trl>=0.11.0`, `bitsandbytes>=0.49.2`,
`fasttext-langdetect>=1.0.2`, `presidio-analyzer/anonymizer>=2.2.0`,
`detoxify>=0.5.2`, `datasketch>=1.6.0`, `torchvision>=0.23.0`,
`requires-python >=3.13`.

Note: **Python 3.13** is the repo minimum — the prior doc's "Python 3.11" is
wrong for this repo.

### 6.2 Docker (`SHIPPED` / `MISLABELED in prior`)

- `infra/docker/docker-compose.axolotl.yml` + `infra/docker/axolotl-train.Dockerfile`
  (base `nvidia/cuda:12.6.3-devel-ubuntu22.04`, Python 3.11, torch, Axolotl).
  This is the **actual training compose**.
- `infra/docker-compose.gpu.override.yml` attaches a GPU to **ollama** only —
  it is **not** a training override. The prior doc wrongly cited it for SFT setup.
- `infra/docker/docker-compose.training.yml`, `docker-compose.nemo-*.yml` also
  exist.

### 6.3 Training frameworks (`SHIPPED`)

- Axolotl (config `configs/axolotl.yaml`, `configs/orpo_axolotl.yaml`).
- HF TRL (`trl>=0.11.0`) via `finetune_model.py` / `dpo_trainer.py` /
  `grpo_trainer.py`.
- Unsloth: **referenced in prose only** — not installed, not imported. `DOC ONLY`.

### 6.4 Monitoring (`PARTIAL`)

`WandB` configs exist (`wandb_project`, `WANDB_*` env in compose), but no
shipped run has been verified. `TensorBoard`/`MLflow`: `DOC ONLY`.

---

## 7. Evaluation, Splits & Catastrophic Forgetting

### 7.1 Splits (`SHIPPED`, with contradiction fixed)

Two splitters exist and **disagree**:

| File | Ratio | Mechanism |
|---|---|---|
| `curate_pipeline.py:assign_split` | **70/15/15** | `<70 train / <85 val / else test` |
| `dataset_splitter.py` | 80/10/10 | `<80 / <90 / else` |
| `dataset_splitter_stratified.py` | 80/10/10 default | 8-axis + source-family grouping |

`curate_pipeline.py` is the production path → **70/15/15 is what ships**.
`dataset_splitter_stratified.py` is the newer, more correct tool (8 axes:
language, tags, difficulty, tier, product_type, policy_mode, diagnosis_topic,
culture_context, safety_severity, conversation_length) with integrity gates
(hash-disjoint, source-family disjoint, eval-in-train, ±2pp ratio, ±2pp domain
balance).

### 7.2 Catastrophic forgetting (`SHIPPED`)

`benchmark_runner.py` computes
`forgetting_score = (pre - post) / pre` with target <10% (preferred <5%), runs
MMLU/HellaSwag/TruthfulQA/BBH + `domain_clinical_empathy`. `PARTIAL`: mock-mode
exists for smoke tests; no real run captured.

---

## 8. Status Matrix — What Is Real

| Capability                                      | Module                                  | Status                       |
|-------------------------------------------------|-----------------------------------------|------------------------------|
| Provenance + SPDX license gate                  | `provenance.py`                         | SHIPPED                      |
| Web/doc/API ingest router                       | `ingest_router.py`                      | SHIPPED                      |
| PDF/EPUB/HTML parsing                           | `book_pdf_converter.py`                 | SHIPPED                      |
| Stage 1 filters (lang/PII/toxicity/dedup)       | `stage1_filters.py`                     |                              |
| Exact+near dedup (MinHash/SimHash)              | `dedup_normalize.py`                    |                              |
| PII scrub (regex+Presidio+LLM)                  | `pii_scrubber.py`                       |                              |
| Curation + tiering                              | `curate_pipeline.py`                    | SHIPPED                      |
| Hash split                                      | `dataset_splitter.py`                   |                              |
| Stratified 8-axis split                         | `dataset_splitter_stratified.py`        |                              |
| Dual LLM judge                                  | `dual_judge.py`, `llm_quality_judge.py` | SHIPPED                      |
| IAA (Fleiss/Cohen)                              | `annotation/iaa.py`                     |                              |
| SDG (self-instruct/BT/paraphrase)               | `sdg_*.py`                              | PARTIAL                      |
| Synthetic QC gate                               | `synth_qc_gate.py`                      |                              |
| DVC versioning                                  | `.dvc` pointers + remote                | PARTIAL (remote/`.gitignore`)|
| SFT                                             | `finetune_model.py` et al               | PARTIAL (no verified)        |
| DPO / ORPO / GRPO                               | `*_trainer.pu`                          | SHIPPED (ORPO tested)        |
| Pruning / distillation / quant                  | `*.py`                                  | PARTIAL                      |
| Forgetting benchmark                            | `benchmark_runner.py`                   | PARTIAL                      |
| **FSDP2 / Megatron / torchrun / NCCL launcher** | —                                       | **NOT IMPLEMENTED**          |
| **NeMo AutoModel distributed**                  | `ai/nemo/` (compose YAML only)          | **NOT IMPLEMENTED**          |

---

## 9. Immediate Action Plan (corrected priority order)

What actually blocks a first real training run, in order:

**Status (2026-08-30):** 1-4 complete; 5-7 deferred pending GPU.

1. **Fix the judge calibration set** — replace `golden_judge_calib.jsonl`
   generic content with 200 mental-health domain samples (or accept the risk).
   ✅ **DONE** — `golden_judge_calib_v2.jsonl` (200 real AnnoMI records) wired
   into `llm_quality_judge.py` + `calibrate_judge.py`; v1 flagged as placeholder.
2. **Pick the real base model** — reconcile `axolotl.yaml` (`Wayfarer-2-12B`)
   vs `orpo_axolotl.yaml` (`Qwen2.5-32B`) vs legacy `Llama-2-7b` default.
   Decide one.
   ✅ **DONE** — standardized on GLM: `zai-org/glm-5.3-flash` for
   weights-loading contexts (axolotl configs, trainers), `@cf/zai-org/glm-5.3-flash`
   as the served judge default; dual-judge primary remains
   `@cf/deepseek-ai/deepseek-v4-pro-0813`. All Qwen3.8/Wayfarer/Qwen2.5
   training references replaced (distillation teacher/student exempt).
3. **Reconcile the splitter** — standardize on
   `dataset_splitter_stratified.py` (8-axis) and retire `dataset_splitter.py`
   hash-split to avoid the 70/15/15 vs 80/10/10 mismatch.
   ✅ **DONE** — `dataset_splitter.py` deleted (zero importers);
   `DEFAULT_RATIO` → `(70, 15, 15)` to match `curate_pipeline`; tests updated (49 pass).
4. **Fix DVC** — add `ai/data/curated/.gitignore`, pin remote to the Civo
   backend actually configured, add `dvc.yaml`/`dvc.lock`.
   ✅ **DONE** — `dvc.yaml` rewritten with ai/-relative paths + per-file outs
   matching committed `.dvc` pointers; fabricated `dvc.lock` (placeholder md5s)
   deleted — regenerate via `dvc repro` after pulling raw input from S3;
   `data/curated/.gitignore` pattern order fixed (`**` before `!*/`/`!*.dvc`).
   Remote already pinned to Civo `pixelated_s3` in `.dvc/config`.
5. **Run one end-to-end SFT** — QLoRA on H100, `orpo_axolotl.yaml`, ~10K-50K
   curated samples, capture real `forgetting_score`.
   ⏸ **DEFERRED** — requires H100 (RunPod ~$1.99-3.29/hr per §3); local box has no GPU.
6. **Then** DPO/ORPO, then pruning/quantization.
   ⏸ **DEFERRED** — gated on task 5.
7. **Distributed training (FSDP2/Megatron) is greenfield** — do not treat it as
   existing; plan it separately after the single-GPU path is proven.
   ⏸ **DEFERRED** — greenfield; plan separately after 5-6.

---

*End of corrected blueprint. Verified against `ai/` submodule code and Aug-2026
GPU pricing on 2026-08-28. Full errata: `docs/TRUTH.md`.*
