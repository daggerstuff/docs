# TRUTH.md — Errata for `training-pipeline-blueprint-2026-08-10.md`

Audit date: 2026-08-28. Method: assume-lie pass; every claim checked against
repo code, `ai` submodule, DVC config, and the cited skills. Line numbers refer
to the blueprint file.

Severity legend:

- **FALSE** — claim contradicts repo/code or is fabricated.
- **CONTRADICTION** — doc disagrees with itself.
- **MISLEADING** — symbol/path/number stated with false precision or a name that
  does not resolve.
- **UNVERIFIED** — plausible but unsourced; treat as illustrative, not fact.
- **UNIMPLEMENTED** — described as if present, but not in code.

---

## 1. Hard errors

### 1.1 Greenfield assumption is false

> Line 7: "Assumption: greenfield (no prior pipeline assets in repo)"

**CONTRADICTION / FALSE.** The repo ships an extensive existing pipeline —
`curate_pipeline.py`, `dedup_normalize.py`, `provenance.py`, `pii_scrubber.py`,
`dataset_splitter*.py`, SDG modules, `dual_judge.py`, etc. Appendix B of the
same document is built entirely on cross-references to this existing code. The
"greenfield" framing is contradicted by the document itself and by the codebase.

### 1.2 `QualityTiers` symbol does not exist

> Line 856: "Curation + tier balancing | `curate_pipeline.py:QualityTiers` |
> shipped" Also B.4 (line 681), B.7 (line 806).

**FALSE.** No `QualityTiers` symbol exists anywhere in `ai/` (grep: 0 hits).
Tiers are string literals `T1_GOLD` / `T2_SILVER` / `T3_BRONZE` / `T4_SAFETY`
handled by `classify_tier()` in `curate_pipeline.py`. The cross-reference table
column name is invented.

### 1.3 Secondary judge model mis-stated

> Line 375 (Expansion 2B): `zai-org/GLM-4.5` as secondary judge model.

**FALSE + CONTRADICTION.** No judge code references GLM-4.5. The shipped judges
are:

- `dual_judge.py:42` — `llama3.3:70b` (Ollama), primary `qwen2.5:72b`.
- `llm_quality_judge.py:64-65` — `Qwen/Qwen2.5-72B-Instruct` +
  `meta-llama/Llama-3.3-70B-Instruct`.

The doc's own B.3.2 (line 665) correctly says "Secondary: LLaMA 3.3-70B", so the
Expansion-step `zai-org/GLM-4.5` contradicts the same document.

### 1.4 Golden calibration set path + content wrong

> Line 376: `ai/data/golden_judge_calib.jsonl`

**MISLEADING.** The file exists only at
`ai/training/data/golden_judge_calib.jsonl`. `dual_judge.py:50` points to
`.../training/data/golden_judge_calib.jsonl`. The doc's `ai/data/...` path does
not resolve.

**Quality issue:** the 200-line file is `neon-consensus-*` generic content
("What is a primary key in SQL?", "How do I bake a cake?", "What is the capital
of France?"). It is not a domain (mental-health) calibration corpus, so it is
not fit as a calibration gate for a clinical Stage-2 judge, despite being
presented as the gate anchor in B.3.4.

### 1.5 Split ratio is self-contradictory

> Lines 299-300 + 348: "80 / 10 / 10"; B.7 line 800:
> "`<80 train; <90 val; else test`"

**CONTRADICTION.** Two shipped splitters disagree, and the doc conflates them:

- `curate_pipeline.py:120`
  `SPLIT_RATIOS = {"train": 0.70, "val": 0.15, "test": 0.15}`; `assign_split()`
  (line 256) uses `<70 train / <85 val / else test`.
- `dataset_splitter.py:63-67` uses `<80 / <90 / else` (80/10/10).

The doc quotes the `dataset_splitter.py` buckets while the primary curation
pipeline actually emits 70/15/15.

### 1.6 DVC remote does not match the doc

> B.6.1 lines 748-755:
> `dvc remote add -d pixelated_s3 s3://pixelated-datasets/dvc`, region
> `us-west-2`.

**FALSE as deployed.** Actual `ai/.dvc/config`:

```ini
[core]
    remote = pixelated_s3
    checksum_jobs = 8
['remote "pixelated_s3"']
    url = s3://whitebat/dvc
    region = nyc1
    endpointurl = https://objectstore.nyc1.civo.com
['remote "pixelated_minio"']
    url = s3://pixelated-datasets/dvc
    endpointurl = http://minio.pixelated.love:9000
```

Backend is Civo object store (`nyc1`, bucket `whitebat/dvc`), not AWS S3
us-west-2. The MinIO alias exists but is not the default remote.

### 1.7 `.gitignore` required by B.6.2 is missing

> B.6.2 line 761: `git add ... ai/data/curated/.gitignore`

**FALSE.** `ai/data/curated/.gitignore` does not exist. Only the three
`*.jsonl.dvc` pointers are present under `ai/data/curated/sft_chatml/`.

### 1.8 "Existing `docker-compose.gpu.override.yml`" is not a training file

> §6 line 286, Action Plan line 351: reuse "existing
> `docker-compose.gpu.override.yml`".

**MISLEADING.** The file exists at `infra/docker-compose.gpu.override.yml`, but
it only attaches an NVIDIA GPU to the **ollama** service (a local-deep-research
compose, see the `curl` URLs in its header). It is not an Axolotl/training
override. The actual training compose is
`infra/docker/docker-compose.axolotl.yml`, which the doc never cites for the SFT
setup step.

---

## 2. UNIMPLEMENTED — written as present tense

### 2.1 FSDP2 / Megatron / torchrun / NCCL launcher

> Action Plan lines 394-401 ("FSDP2 trial on 70B", "Megatron trial TP=4/PP=2",
> "HSDP"), §6 line 259-260, line 143 ("NVIDIA NeMo distributed mode").

**UNIMPLEMENTED.** No `FSDP2`, `Megatron`, `torchrun`, `hybrid_shard`, or
multi-node launcher exists in `ai/training`. Grep for
`fsdp2|FSDP2Config|megatron|torchrun|hybrid_shard|MixedPrecisionPolicy` returns
only:

- `dataloader_callback.py` (`torch.distributed` barrier), and
- DeepSpeed ZeRO-3 passthrough flags (`orpo_trainer.py`, `distill_model.py`,
  `training_optimizer.py`, `train_moe_h100.py`) referencing
  `ai/training/configs/ds_config_zero3.json`.

Appendix A is an accurate transcription of the
`nemo-automodel-distributed-training` skill, but it is forward-looking, not
shipped. The Action Plan's "Week 5 / Month 2 / Month 3" items are plan, not
done.

### 2.2 Multi-node NeMo distributed mode

> Line 143, 357, 400-401.

**UNIMPLEMENTED.** `ai/nemo/` exists but holds service/compose YAML
(`customizer.yaml`, `gpu/Dockerfile`, `services/*.yaml`, `docker-compose.yaml`),
not NeMo AutoModel distributed-training code. No `NeMoAutoModel` /
`nemo_automodel` import anywhere in the repo.

---

## 3. UNVERIFIED / likely fabricated market facts

### 3.1 Lambda Labs "AWS Activate" credits

> Lines 91-92, 405-406: "free credits for startups ($500-1000 via AWS Activate
> path)".

**UNVERIFIED, likely fabricated.** Lambda Labs is not an AWS Activate partner;
the two programs are unrelated. The doc itself flags this with "silent lens
applied" (line 405) but still states it as fact.

### 3.2 GPU pricing precision

> Line 110: "H100
> $1.99-2.49/hr" (RunPod).
> Lines 410-411: "H100 training at $2/hr × 8 GPU =
> $16/hr; 3-day SFT run ≈ $1,100-1,500".

**UNVERIFIED.** On-demand/spot prices move constantly and are not cited to a
date or source. The "$1,100-1,500" range cannot be reconstructed from "$16/hr ×
72h" (= $1,152) plus overhead without source. Treat as order-of-magnitude only.

### 3.3 "RTX 5090" on Vast.ai (line 119)

**MISLEADING.** 5090 exists (Jan 2025), but listing it alongside H100/A100 as a
training GPU in an "Aug 2026 state" without noting driver/CUDA/VRAM caveats is
loose. Minor.

### 3.4 Pruning / distillation recovery numbers

> Line 62: "restores 95%+ of quality with 30-50% fewer active params". Line 65:
> "DeepSpeed ZeRO-3 + distillation = viable for 7B student on 2x A100".

**UNVERIFIED.** No citation; these read as heuristics. The `prune_adapter.py` /
`distill_model.py` modules exist but do not establish these exact figures.

### 3.5 DeepSeek-R1 "800K curated > 10M unfiltered"

> Lines 224-226.

**UNVERIFIED.** The direction (curated > raw) is well-supported, but the exact
"800K vs 10M" attribution to the DeepSeek-R1 paper is loose — R1's reasoning
corpus was on the order of ~600K samples, and the "10M unfiltered web"
comparison is not a headline DeepSeek-R1 result. Treat the numbers as
illustrative.

---

## 4. Minor / quality

### 4.1 `model_type: LLaMA` for Qwen2.5-32B

> Appendix C lines 874-875.

**FALSE as config.** Qwen2.5 is not LLaMA architecture; `model_type: LLaMA`
would not run. The shipped `ai/training/configs/axolotl.yaml` trains
`LatitudeGames/Wayfarer-2-12B` (not Qwen32B) with
`model_type: AutoModelForCausalLM`. Appendix C's excerpt is a non-runnable
mashup.

### 4.2 B.7 says "4 axes", repo ships 8 axes

> B.7 lines 803-806 list `domain / difficulty / language / tier`.

**MISLEADING / STALE.** `dataset_splitter_stratified.py:43-54` ships 8+ axes
(`source_family`, `product_type`, `policy_mode`, `diagnosis_topic`,
`culture_context`, `safety_severity`, `conversation_length`, plus language/tags/
difficulty/tier). The doc describes the older 4-axis design.

### 4.3 Model catalog staleness

> §1 lines 12-25.

**MISLEADING.** Header says "Aug 2026 state" but lists 2024-2025-era models
(Qwen2.5, GLM-4.5, Mistral Large 2, DeepSeek-V3). Not wrong per se, but the
"current state" framing is stale. Note the shipped `axolotl.yaml` uses
`Wayfarer-2-12B`, not any model recommended in §1.

---

## Verified-correct highlights (for confidence calibration)

The following claims are accurate and code-backed — the doc is not uniformly
wrong:

- `provenance.py` `ALLOWED_LICENSES` + `validate_license` (exact match).
- `dedup_normalize.py` MinHash(128/16/8, 0.85) + SimHash-64 Hamming≤3 + SHA-256
  - Jaccard.
- PII 3-layer (regex + Presidio + LLM at confidence<0.8), entity list exact.
- `_NON_ENGLISH_RATIO=0.30`, `fasttext-langdetect` lid.176.bin, `detoxify`
  4-model, toxicity gates 0.30/0.15.
- `NEMO_RETRY_DELAYS=(1,2,4)`, retry statuses {429,500,502,503,504}.
- `ds_config_zero3.json` (matches Appendix D nearly verbatim).
- `dual_judge.py` rubric (5-dim), 0.15 consistency, Pearson r≥0.80, Cohen
  κ≥0.65, k=3 self-consistency variance>0.05.
- `iaa.py` Fleiss κ≥0.85 gold / 0.75 min, Landis-Koch bands, quarantine<0.40,
  retrain 0.40-0.60.
- `synth_qc_gate.py` thresholds 0.80/0.85/0.30/0.60/0.05.
- `data_audit.py:CATEGORY_KEYWORDS`, `multilingual_safety_checker.py`
  (en/es/fr/pt/de).
- All four cited skill directories exist; Appendix A is a faithful skill
  transcription.

---

## Bottom line

The blueprint is a **high-quality architecture scaffold whose dataset/QA/
provenance machinery is real and verifiable**, but it:

1. mislabels 2+ things as "shipped" that don't exist (`QualityTiers`, FSDP2/
   Megatron distributed training);
2. carries a layer of unsourced, partly fabricated market facts (Lambda/AWS
   credits, pricing, `zai-org/GLM-4.5` judge);
3. contradicts itself on split ratio and judge model;
4. has wrong paths/remotes (golden set, DVC backend, `.gitignore`, compose
   file);
5. states "greenfield" while itself cross-referencing existing code.

Fix the hard errors (§1) before treating any of this as authoritative.
