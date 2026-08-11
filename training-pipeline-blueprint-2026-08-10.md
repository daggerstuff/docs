# AI Training Pipeline Blueprint — Aug 2026

3 skills used: `brainstorming` (pipeline mapping), `ai-engineer` (LLM architecture), `find-skills` (+ NVIDIA NeMo `nemo-automodel-distributed-training`, 1.8K installs).

Assumption: greenfield (no prior pipeline assets in repo), domain-specialized + general branch support (Option E from brainstorming gate).

---

## 1. Foundational Models (Aug 2026 state)

| Model | Best for | Size | License | Notes |
|---|---|---|---|---|
| Llama 3.3 / 3.2 (Meta) | General assistant, multi-turn chat, instruction following | 8B / 70B / 405B (MoE variants) | Llama 3 Community License | Best open baseline; excellent SFT stability |
| Qwen 2.5-72B / Qwen2.5-7B | Multilingual (CN + EN), coding, math, agent tasks | 7B / 32B / 72B / 110B (MoE) | Qwen License (open weights) | Top MMLU/code benchmark open weights; strong Chinese support |
| DeepSeek-V3 / DeepSeek-R1 | Reasoning, math, coding, long-context (128K+) | 671B (MoE, 37B active) / 7B distilled | MIT / Model License | Best reasoning-to-cost ratio; R1 = SFT + RL (GRPO) pipeline reference |
| Mistral Large 2 / Mistral-Nemo | European/multi-language, enterprise, RAG-heavy | 12B / 123B | Apache 2.0 / Mistral License | Smaller footprint, faster inference, good for edge/distillation |

Recommendation: start with Qwen 2.5-32B or Llama 3.3-70B (best balance of open-license, community tooling, benchmark performance). Use DeepSeek-R1-7B/14B distilled for reasoning sub-tasks or as a student for distillation.

---

## 2. Optimization & Fine-Tuning Techniques

### SFT vs Preference Alignment
- **SFT (Supervised Fine-Tuning)**: required baseline. 3-epoch max. Use Axolotl or Llama-Factory. Best for instruction formatting, domain vocabulary, format compliance.
- **DPO (Direct Preference Optimization)**: post-SFT. Use for preference alignment (helpful/harmless). Requires preference pairs (chosen/rejected). Lower compute than RLHF, more stable than PPO.
- **ORPO (Optimized Relative Preference Optimization)**: newer (2025-2026). Combines SFT + preference in single pass, no reference model, lower memory. Preferred over DPO for new pipelines if available in Unsloth/Llama-Factory.
- **Pipeline order**: Pre-train base → SFT (domain) → Preference (DPO/ORPO) → Optional: KTO / IPO for finer alignment.

### Parameter-Efficient Methods
- **QLoRA (4-bit Quantized LoRA)**: standard. Use `bitsandbytes` 4-bit (NF4) with double-quant. 16-bit LoRA for best quality if VRAM allows.
- **Advanced LoRA variants**: DoRA (Weight-Decomposed Low-Rank Adaptation) — better performance for small ranks; AdaLoRA — adaptive rank allocation; VeRA — reduced parameter count.
- **PEFT stack**: Unsloth provides fastest QLoRA (2x speed vs standard). Axolotl handles multi-GPU and custom dataset formats well. Llama-Factory = most config options but heavier.

### Cost Optimization: Pruning + Distillation
- **Selective pruning**: magnitude-based unstructured pruning + LoRA recovery (post-prune fine-tune restores 95%+ of quality with 30-50% fewer active params). Use `torch.nn.utils.prune` or `pruning` libraries.
- **Knowledge distillation**: train small student (7B/8B) on outputs from large teacher (72B/110B). Use KD loss (MSE on logits + cross-entropy on tokens). DeepSpeed ZeRO-3 + distillation = viable for 7B student on 2x A100.
- **Quantization post-training**: AWQ / GPTQ / GGUF for inference optimization (not training). Use `llama.cpp` or `vLLM` for deployment.

---

## 3. GPU Cloud Providers & Hardware (Mid-2026)

| Provider | Best Hardware | Cost-to-Perf | Free Trial | Pros | Cons | Setup Style |
|---|---|---|---|---|---|---|
| **RunPod** | H100 (80GB), H200, B200, A100, RTX 4090 | Best for spot/intermittent; H100 $1.99-2.49/hr | Limited trial credits | Container-native, instant pods, no contracts, Docker images pre-built, managed + bare metal | Spot preemption; limited long-term reservation discounts | Managed pods (Docker) or bare metal (SSH) |
| **Lambda Labs** | H100, H200, B200 clusters (up to 8-GPU nodes) | Competitive for reserved instances; free credits for startups ($500-1000 via AWS Activate path) | Yes ($500-$1000 startup credits available) | Clean API, good documentation, US/EU regions, native Kubernetes support | Fewer instance types; newer provider = less enterprise support | DIY container / managed Kubernetes |
| **CoreWeave** | H100, H200, B200, GB200 (NVL72), large clusters (4096 GPU max) | Best for scale; reserved pricing lower than AWS/GCP for H-series; spot available | Limited; negotiate for startup | Largest open GPU cluster, best networking (NVLink/NVSwitch), InfiniBand, managed Kubernetes | Higher minimum spend, enterprise-focused pricing, less flexible for small jobs | Managed Kubernetes / bare metal |
| **Vast.ai** | H100, A100, RTX 4090, 5090 | Cheapest bare-metal; market pricing; often 30-50% below RunPod reserved | None official; low entry cost | Marketplace model = lowest prices, wide variety of GPU types, instant access, no lock-in | Variable reliability, no managed services, must manage Docker/SSH yourself, spot-like stability | Bare metal (SSH + Docker) |
| **RunC.ai** | H100, B200 clusters, custom networking | Competitive reserved; startup-friendly pricing | Limited trial | Focused on AI/ML, good networking, US West focus, flexible contracts | Smaller footprint than CoreWeave; newer ecosystem | DIY container / managed clusters |

**Managed vs DIY breakdown**:
- **Managed (RunPod pods, Lambda Kubernetes, CoreWeave K8s)**: faster setup (hours vs days), built-in monitoring, easier scaling, lower ops overhead. Best for small-medium pipelines.
- **DIY bare-metal/container (Vast.ai, RunC.ai SSH, Lambda SSH)**: lower cost per GPU-hour (10-40% savings), full environment control, custom Docker images (Axolotl/Llama-Factory/Unsloth), Git version tracking. Best for cost-sensitive, reproducible pipelines.

**Recommendation for this pipeline**: start with **Lambda Labs H100 (managed Kubernetes)** or **RunPod H100 pods** for SFT/DPO (easy Axolotl container deploy). Scale to **CoreWeave B200 clusters** or **RunC.ai** for large-scale distillation or multi-node distributed training (NVIDIA NeMo distributed mode). Keep **Vast.ai** as spot backup for evaluation runs.

**Hardware specs (Aug 2026)**:
- H100 SXM5 80GB: best price/perf for 7B-70B training; 3.35TB/s HBM3; NVLink for multi-GPU.
- H200 141GB: faster than H100 for long-context (128K+ tokens) due to HBM3e bandwidth; good for DeepSeek-style reasoning.
- B200 Blackwell: latest architecture; best for very large clusters; better FP4/FP8 performance; recommended for new builds if budget allows.
- A100 80GB: still viable for 8B-13B fine-tuning; much cheaper; avoid for 70B+.

---

## 4. Dataset Curation & Formatting (Best Formats Aug 2026)

**Best format: JSONL with structured schema** (not raw ChatML or plain ShareGPT). Reasons:
- JSONL = line-delimited JSON = stream-parseable, git-friendly (line-based diff), easy with Python `json` / `pandas` / `datasets` library.
- Parquet = best for large-scale (100K+ rows) analysis, query, and versioning; use `pyarrow` or `datasets` library to convert JSONL → Parquet for archival/analysis.
- ShareGPT / ChatML = legacy conversational formats. Good for quick import to Axolotl, but limited schema control for domain-specific fields (annotations, domain tags, quality scores).

**Recommended dataset schema (JSONL, one line per sample)**:
```json
{"conversation_id":"c-0001","domain":"legal","language":"en","messages":[{"role":"system","content":"You are a legal assistant..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}],"quality_score":0.92,"annotation_stage":"v3","tags":["contract","review"],"source":"manual_curation","date":"2026-08-01"}
```

**Format comparison for pipeline stages**:
- **Curation phase**: JSONL (easy diff, manual edit, quality tracking fields).
- **Storage/archive**: Parquet (compression, columnar query, versioned in DVC/Git LFS).
- **Training input**: JSONL or converted to dataset format (Axolotl `json` / `sharegpt` format; Llama-Factory `alpaca` / `sharegpt`; Unsloth accepts JSON directly).

**Conversion**: use `datasets` library from HuggingFace (`load_dataset("json", data_files=...)`) → `save_to_disk()` → `to_parquet()`.

---

## 5. Dataset Sizing & Quality (Industry Shift Confirmed)

**Current trend (Aug 2026)**: heavy shift to **small, high-quality, multi-stage curated datasets** over massive raw corpora.

- **SFT dataset size**: 10K-50K high-quality samples outperform 500K-1M raw samples for domain specialization. DeepSeek-R1 paper confirms: 800K curated reasoning samples > 10M unfiltered web data.
- **Quality pipeline (multi-stage)**:
  1. **Raw ingestion** (web, docs, APIs) → auto-filter (language detection, PII removal, toxicity filter).
  2. **Stage 1 QA** (automated): length check, format validation, duplication removal (MinHash/LSH), basic coherence (perplexity threshold).
  3. **Stage 2 QA** (domain expert / LLM-as-judge): relevance, factual accuracy, style adherence, domain vocabulary. Use LLM judge (GPT-4o-class or Qwen-72B) with rubrics.
  4. **Stage 3 QA** (human expert): final review of high-value / edge-case samples; annotation of tags, quality scores, difficulty levels.
  5. **Balanced sampling**: stratify by domain, language, difficulty; avoid over-representing easy/common samples.

- **Quality metrics**: track `quality_score` per sample; use average > 0.85 as pipeline gate; drop samples < 0.6; review 0.6-0.85 for improvement.
- **Data versioning**: use **DVC (Data Version Control)** or **lakeFS** for dataset versions; commit dataset hashes (`sha256`) in Git; never commit raw data files.
- **Language format**: English + domain-specific terminology (legal, medical, code). For multilingual: include language tag; use separate files or dataset splits per language to control mixing ratios (e.g., 70% EN / 20% CN / 10% other for Qwen-based pipeline).

---

## 6. Tech Stack & Software Setup (Linux/Docker/Git)

### Core Stack Recommendation
| Component | Tool | Why |
|---|---|---|
| Training framework | **Axolotl** (primary) + **Llama-Factory** (advanced configs) + **Unsloth** (speed) | Axolotl: best multi-GPU, custom dataset formats, community support. Unsloth: 2x faster QLoRA, lower VRAM. Llama-Factory: most flexible (multi-modal, custom losses). |
| Distributed training | **DeepSpeed** (ZeRO-1/2/3 + offload) + **FSDP** (PyTorch native) | DeepSpeed ZeRO-3 for multi-GPU; FSDP preferred for newer PyTorch (2.4+) with better compatibility. |
| Dataset processing | **datasets** (HuggingFace) + **pandas** + **pyarrow** (Parquet) + **DVC** | Standard pipeline: JSONL → `datasets` → filter → `to_parquet()` → DVC version. |
| Environment / Containers | **Docker** (NVIDIA Container Toolkit) + `docker-compose.gpu.override.yml` (existing in repo!) + **Git** (branch per dataset version / experiment) | Use existing `docker-compose.gpu.override.yml`. Build Axolotl/Llama-Factory images: `FROM nvidia/cuda:12.6-devel-ubuntu22.04`. |
| Version control | **Git** (code) + **DVC** (datasets/weights) + **Git LFS** (small configs) | Never commit weights; commit `.dvc` files pointing to remote storage (S3/MinIO/GCP bucket). |
| Monitoring / Logs | **Weights & Biases (WandB)** or **MLflow** + **TensorBoard** | Track loss curves, validation perplexity, dataset version, GPU utilization. |
| Training config format | YAML (Axolotl config) / JSON (Llama-Factory) | Keep config files in `configs/<date>-model>-dataset>/` with descriptive filenames. |

### Software Setup Sequence
1. **Base OS**: Ubuntu 22.04 or 24.04 LTS.
2. **NVIDIA drivers**: 550+ series for B200/H200 support; CUDA 12.6.
3. **Python**: 3.11 (best compatibility with PyTorch 2.4+, bitsandbytes, transformers 4.45+).
4. **Virtual env**: `python -m venv .venv`; use `uv` (faster) if available.
5. **Install**: `torch==2.4.0` + `torchvision`, `transformers==4.45.0`, `datasets`, `accelerate`, `peft`, `trl`, `bitsandbytes`, `axolotl` (or clone Llama-Factory/Unsloth repos).
6. **Docker**: `docker-compose -f docker-compose.yml -f docker-compose.gpu.override.yml up -d` (existing files in repo).
7. **Git workflow**: `main` = stable config; branch `experiment/<date>-model>` per run; tag weights releases; DVC push weights after run.

---

## 7. Evaluation, Splits & Catastrophic Forgetting

### Train / Validation / Test Split
- **Ratio**: 80 / 10 / 10 for domain-specialized (high-quality small datasets); 70 / 15 / 15 for larger general-purpose datasets.
- **Stratification**: split by domain, difficulty, language, not random (preserve distribution). Use `sklearn.model_selection.StratifiedShuffleSplit` with multi-label stratification.
- **Validation set purpose**: early stopping (perplexity or task-specific metric); hyperparameter selection; overfitting detection.
- **Test set**: held out completely; used only once per model version for final benchmark; never used for hyperparameter tuning.

### Catastrophic Forgetting Testing (Mandatory)
1. **Benchmark before fine-tuning**: run model on standard benchmarks (MMLU, HellaSwag, TruthfulQA, BBH) + domain-specific benchmark (e.g., legal bar exam samples, code test suites).
2. **Post-training evaluation**: same benchmark set + new domain evaluation set.
3. **Forgetting metric**: `forgetting_score = (pre_score - post_score) / pre_score`. Target: < 10% forgetting on general benchmarks; < 5% preferred for production.
4. **Recovery / mitigation**: use **mixed fine-tuning** (include 10-20% general instruction data in SFT dataset); use **LoRA with base model frozen** (prevents weight drift); use **EWC (Elastic Weight Consolidation)** or **Replay (re-sample general data)** for severe cases.
- **Edge case testing**: adversarial prompts (jailbreak attempts, out-of-distribution inputs), multi-turn degradation (context loss after long conversations), multilingual mixing errors, domain boundary errors (e.g., asking legal model about medicine).

---

## Immediate Action Plan (Dataset Curation → Environment)

1. **Today**: Define domain taxonomy (tags, difficulty, annotation stages). Create JSONL schema. Start Stage 1 QA pipeline.
2. **Week 1**: Collect 10K-50K raw samples; apply automated filter; begin Stage 2 QA (LLM judge); start manual expert review for high-value samples.
3. **Week 2**: Freeze dataset v1; convert to JSONL + Parquet; commit to DVC; create dataset split (stratified 80/10/10).
4. **Week 3**: Set up Docker environment using existing `docker-compose.gpu.override.yml`; build Axolotl/Unsloth image; configure SFT training (start with Llama 3.3-70B or Qwen 2.5-32B base).
5. **Week 4**: First SFT run; validate on benchmark + domain test; check catastrophic forgetting metrics.
6. **Month 2**: Preference alignment (DPO/ORPO) if needed; scale to multi-GPU (DeepSpeed ZeRO-3) or distributed (NVIDIA NeMo); prepare distillation pipeline if deploying small footprint.

---

*Startup/AWS caveat (silent lens applied)*: Lambda Labs offers $500-$1000 startup credits (AWS Activate partner offer) — activates here because it unblocks GPU access for this pipeline. RunPod provides lowest barrier to entry (no contracts, instant pods). Recommend Lambda for first reserved H100 nodes (free trial credits) → scale to CoreWeave or RunC.ai for larger clusters. Monitor cost: H100 training at $2/hr × 8 GPU = $16/hr; 3-day SFT run ≈ $1,100-1,500. Budget accordingly.

---

## APPENDIX A — EXPANDED: Distributed Training / NVIDIA NeMo (FSDP2, TP/PP/CP/MoE)

From NVIDIA `nemo-automodel-distributed-training` skill (1.8K installs, Aug 2026).

### Strategy Selection (YAML key: `distributed.strategy`)

| Strategy | YAML | Best for | Limitations |
|---|---|---|---|
| FSDP2 | `fsdp2` | Default. TP, PP, CP, EP, HSDP all supported. | None significant |
| MegatronFSDP | `megatron_fsdp` | Megatron-style FSDP only. | **No PP, no EP, no `sequence_parallel`** |
| DDP | `ddp` | Simplest data parallel only. | **No TP, PP, CP, EP, HSDP** |

**Rule**: always use `fsdp2` for multi-node or 70B+; `megatron_fsdp` only for single-node dense without PP; `ddp` only for quick single-node <8B runs.

### FSDP2 Config Examples

Basic (DP only):
```yaml
distributed:
  strategy: fsdp2
  tp_size: 1
  pp_size: 1
  cp_size: 1
  ep_size: 1
```
TP + sequence_parallel (keep TP inside NVLink domain):
```yaml
distributed:
  strategy: fsdp2
  tp_size: 4   # 2, 4, or 8 — must divide GPUs/node
  sequence_parallel: true
```
Pipeline parallelism (70B+ models):
```yaml
distributed:
  strategy: fsdp2
  pp_size: 2
  pipeline:
    pp_schedule: interleaved1f1b   # 1f1b / interleaved_1f1b / gpipe / looped_bfs
    pp_microbatch_size: 4
```
Context parallelism (long sequences 8K+):
```yaml
distributed:
  strategy: fsdp2
  cp_size: 2  # or 4, 8
```
MoE expert parallelism:
```yaml
distributed:
  strategy: fsdp2
  ep_size: 8
  activation_checkpointing: true
  moe:
    reshard_after_forward: false
```
Constraint: `ep_size` must divide `dp_size * cp_size` (`dp_size` auto-calculated as `world_size / (tp * pp * cp)`).

### Sizing Guidelines (Dense Models)

| Size | TP | PP | CP | Strategy Notes |
|---|---|---|---|---|
| <3B | 1 | 1 | 1 | DP only |
| 3-13B | 2-4 | 1 | 1 | FSDP2 + TP |
| 13-70B | 4-8 | 2-4 | 1 | FSDP2 + TP + PP |
| 70B+ | 8 | 4-8 | 1 | FSDP2 + TP + PP required |
| Any + long seq (8K+) | as above | as above | 2-8 | add CP; requires SDPA or TE attention |

Hardware topology rules: TP must stay within single NVLink domain (one node); use PP/DP for cross-node; TP across InfiniBand destroys throughput.

### Memory Optimization Configs

Activation checkpointing:
```yaml
distributed:
  activation_checkpointing: true   # trades ~30% compute for memory
```
Gradient sync deferral (FSDP2 default):
```yaml
distributed:
  defer_fsdp_grad_sync: true
```
HSDP (hybrid sharded — intra-node full shard + inter-node replicate):
```yaml
distributed:
  strategy: fsdp2
  dp_replicate_size: 2   # must divide dp_size; FSDP2 only
```
Mixed precision policy override:
```python
from torch.distributed.fsdp import MixedPrecisionPolicy
config = FSDP2Config(
    mp_policy=MixedPrecisionPolicy(param_dtype=torch.float16, reduce_dtype=torch.float32),
)
```

### Pipeline Parallelism Details

Requirements:
- Model class must define `_pp_plan` (mapping module FQNs to stages).
- `pp_size > 1` in config.
- Pipeline sub-config required: `pp_schedule`, `pp_microbatch_size`.

Supported schedules: `1f1b`, `gpipe`, `interleaved_1f1b`, `looped_bfs`, `dfs`, `v_schedule`, `zero_bubble`. For 70B+ use `interleaved1f1b` with `pp_microbatch_size=4` to reduce bubble time.

### Sequence Packing + CP

```yaml
packed_sequence:
  packed_sequence_size: 4096   # must be divisible by cp_size
step_scheduler:
  local_batch_size: 1          # must be 1 for packed sequences
```

### Context Parallelism Requirements
- SDPA (Flash Attention / Efficient Attention) or Transformer Engine attention only.
- `SDPBackend.MATH` NOT compatible with DTensor.
- Attention masks stripped automatically; `is_causal=True` via pre-hooks.

### Multi-Node Setup (NCCL / InfiniBand)
- Initialize with `initialize_distributed("nccl")`.
- TP within node; PP/DP across nodes.
- InfiniBand required for cross-node TP (not recommended); preferred topology: TP per node → PP across nodes → CP for sequence dimension.
- Monitor NCCL timeout with `NCCL_DEBUG=INFO` during first multi-node run.

### MegatronFSDP Limitations (Explicit)
- No PP (`pp_size > 1` raises).
- No EP (`ep_size > 1` raises).
- No `sequence_parallel`.
- Only dense FSDP-style sharding (no pipeline, no expert parallelism).
- Recommendation: use `fsdp2` for all complex parallelism; reserve `megatron_fsdp` for simple dense single-node runs.

---

## APPENDIX B — EXPANDED: Dataset Curation Pipeline (Ingestion → Filter → QA → Expert → Synthetic)

### Ingestion Pipeline
1. **Sources**: web (scraped HTML/Markdown), docs (PDF/Word), APIs, internal DBs.
2. **Parsing**: `pypdf` / `PyMuPDF` for PDF; `python-docx` for DOCX; BeautifulSoup for HTML; `requests` for APIs.
3. **License check**: filter by license (CC-BY, MIT, public domain); drop proprietary/non-redistributable content.
4. **Initial format**: raw text → JSONL line with `source`, `date`, `license`, `raw_text`.

### Automated Filtering (Stage 1 QA)
```python
# Pseudo-pipeline
from langdetect import detect
import presidio_analyzer, presidio_anonymizer
from perspective_api_client import analyze_toxicity

# Language detection
if detect(text) != target_lang: drop or tag
# PII removal
analyzer = presidio_analyzer.AnalyzerEngine()
anonymizer = presidio_anonymizer.AnonymizerEngine()
anonymized = anonymizer.anonymize(text=text, analyzer_results=analyzer.analyze(...))
# Toxicity filter
if toxicity_score > 0.7: drop; if 0.3-0.7: review; else pass
# Deduplication (MinHash/LSH)
# Perplexity coherence check (use base model to score; drop >2σ outliers)
```

### LLM-as-Judge QA (Stage 2 QA)
- Use Qwen-72B (or LLaMA-70B) as judge with structured rubric (JSON output).
- Rubric categories: relevance (0-1), factual accuracy (0-1), domain vocabulary (0-1), style adherence (0-1), format compliance (0-1).
- Average score > 0.85 passes; 0.6-0.85 flagged for review; < 0.6 dropped.
- Consistency: run judge 3× per sample, require std < 0.1 for acceptance; else manual review.

### Expert Annotation (Stage 3 QA)
- Interface: web-based annotation tool (label-studio or custom) with multi-label tags, quality score slider, difficulty level.
- Inter-annotator agreement: target Cohen's kappa ≥ 0.75; Fleiss kappa for multi-annotator.
- Final annotation fields added: `tags`, `quality_score`, `annotation_stage` (v1/v2/v3), `difficulty`, `reviewer_id`.

### Synthetic Data Generation
- **Self-instruct**: use base model to generate instruction-response pairs from seed prompts; filter through same QA pipeline.
- **Back-translation**: translate EN → target language → back to EN; compare similarity; use as augmented samples (not replacements).
- **Paraphrasing**: use smaller model (e.g., Mistral-7B) to paraphrase high-quality samples, increasing diversity without new content.
- **Quality gate on synthetic**: synthetic samples must pass LLM-judge with score ≥ 0.80; if lower, regenerate or discard.

### DVC Versioning Workflow
```bash
# Initialize
dvc init
dvc remote add -d dataset_storage s3://my-bucket/datasets/
# Track dataset
dvc add data/dataset_v1/
dvc push
# Access in training
dvc pull
dvc checkout
# Tag versions
git tag -a dataset-v1.0 -m "Dataset v1: 42K samples, avg quality 0.91"
```
- Never commit raw data; commit `.dvc` files only.
- Remote storage: S3 (AWS), MinIO (self-hosted), GCP bucket.
- Dataset hash (`sha256`) stored in `.dvc` file; referenced in Git.

### Stratified Split Implementation
```python
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd

# Multi-label stratification (domain + language)
df['strata'] = df['domain'] + '_' + df['language']
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.10, random_state=42)
for train_idx, test_idx in sss.split(df, df['strata']):
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]
# Repeat for validation split from train_df
```
- Stratify by: domain, difficulty, language, quality tier.
- Avoid random split; preserve distribution to prevent domain bias in evaluation.

---

## APPENDIX C — EXPANDED: Optimization Config Details

### SFT Hyperparameters (Axolotl / Unsloth)
```yaml
# Axolotl config excerpt
base_model: Qwen/Qwen2.5-32B
model_type: LLaMA
load_in_8bit: false
load_in_4bit: true
use_peft: true
lora_r: 64
lora_alpha: 128
lora_dropout: 0.05
target_modules: ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
bf16: true
fp16: false
epochs: 3
learning_rate: 2e-5
lr_scheduler_type: cosine
warmup_ratio: 0.1
max_grad_norm: 1.0
batch_size: 2
grad_accum_steps: 8
```

### LoRA Variant Configs
- **QLoRA (4-bit)**: `load_in_4bit: true`, `bnb_4bit_compute_dtype: bfloat16`, `bnb_4bit_quant_type: nf4`, `bnb_4bit_use_double_quant: true`.
- **DoRA**: `use_dora: true` (Axolotl/Unsloth); improves performance for same rank by decomposing weights.
- **AdaLoRA**: adaptive rank; start with `lora_r: 32` and allow adaptive growth; best when budget constrained.
- **VeRA**: reduced params; use for very small fine-tuning budgets (<1% params).

### DPO Config (Post-SFT Preference Alignment)
```yaml
# Llama-Factory / Axolotl DPO settings
dpo_beta: 0.1
learning_rate: 5e-6
per_device_train_batch_size: 1
gradient_accumulation_steps: 4
warmup_ratio: 0.1
lora_r: 32
lora_alpha: 64
# Preference dataset format: JSON with "chosen" and "rejected" fields
```

### ORPO Config (Single-Pass SFT + Preference)
- Use Unsloth or Llama-Factory if available; ORPO eliminates reference model and reduces memory by ~25% vs DPO.
- Config: `use_orpo: true`, `beta: 0.1`, same dataset structure as DPO.

### Pruning Schedule Example
```python
import torch.nn.utils.prune as prune
# After SFT, before inference optimization
prune.l1_unstructured(model, name='lora_A', amount=0.3)  # 30% magnitude pruning
prune.remove(model, 'lora_A')  # make permanent
# Recover with 1-epoch fine-tune on 10% of dataset (LoRA recovery)
```
Target: 30-50% fewer active params with < 5% quality loss post-recovery.

---

## APPENDIX D — EXPANDED: Tech Stack Setup (Docker, Axolotl, DeepSpeed, Git/DVC)

### Docker Build (Expanded)
Existing repo file: `docker-compose.gpu.override.yml`.
Custom Axolotl image:
```dockerfile
FROM nvidia/cuda:12.6-devel-ubuntu22.04
RUN apt-get update && apt-get install -y python3.11 python3-pip git
COPY requirements.txt .
RUN pip install torch==2.4.0 transformers==4.45.0 datasets accelerate peft trl bitsandbytes
RUN pip install axolotl
WORKDIR /workspace
```
Build & run:
```bash
docker build -t axolotl-train:latest .
docker-compose -f docker-compose.yml -f docker-compose.gpu.override.yml up -d
```

### DeepSpeed ZeRO-3 Config (for Multi-GPU > 4 GPUs or 70B+)
```json
{
  "fp16": {"enabled": false},
  "bf16": {"enabled": true},
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {"device": "cpu", "pin_memory": true},
    "offload_param": {"device": "cpu", "pin_memory": true},
    "overlap_comm": true,
    "contiguous_gradients": true,
    "sub_group_size": 1e9,
    "reduce_bucket_size": 4e8,
    "stage3_prefetch_bucket_size": 9e6,
    "stage3_param_persistence_threshold": 1e5,
    "stage3_max_live_parameters": 3e9
  },
  "gradient_accumulation_steps": 8,
  "gradient_clipping": 1.0,
  "train_batch_size": "auto",
  "train_micro_batch_size_per_gpu": "auto",
  "optimizer": {"type": "AdamW", "params": {"lr": "auto", "betas": [0.9, 0.999], "eps": 1e-8, "weight_decay": 0.01}},
  "scheduler": {"type": "WarmupDecayLR", "params": {"warmup_min_lr": 0, "warmup_max_lr": "auto", "warmup_num_steps": 100, "total_num_steps": "auto"}}
}
```

### Git + DVC Workflow (Expanded)
```bash
# Per experiment
git checkout -b experiment/2026-08-10-qwen32b-sft
# Config changes tracked in Git; dataset tracked in DVC
git add configs/
git commit -m "Add SFT config for Qwen2.5-32B, dataset v1.2"
dvc add data/dataset_v1.2/
dvc push
# After training
dvc add outputs/model_weights/
dvc push
git tag -a v1.2-model -m "Model v1.2: Qwen2.5-32B SFT, dataset v1.2, forgetting_score 0.04"
```
- Never commit weights (`.pth`, `.safetensors`, `.bin`) to Git; always use `.gitignore` rules.
- Config naming convention: `configs/<date>-base_model>-dataset_version>-stage>.yaml`.

### CI Pipeline (Basic)
```yaml
# .github/workflows/train.yml (simplified)
name: Training Pipeline CI
on: [push]
jobs:
  validate-config:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python -c "import yaml; yaml.safe_load(open('configs/latest.yaml'))"
  dataset-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: dvc pull
      - run: python scripts/validate_dataset.py --dataset data/dataset_latest/ --min-quality 0.85
```

---

## APPENDIX E — EXPANDED: Optimization Pipeline Step-by-Step (SFT → DPO/ORPO → Pruning → Quantization)

### Step 1: Base Model Selection + Benchmark
- Run base model on domain benchmark + MMLU (pre-training reference).
- Save results as `benchmarks/pre_train_YYYY-MM-DD.json`.

### Step 2: Dataset Freeze + Split
- Lock dataset version with DVC (`dataset_vX.Y`).
- Generate stratified 80/10/10 split; save split indices.
- Verify average quality score ≥ 0.85; else return to QA.

### Step 3: SFT (Axolotl / Unsloth)
- Config: `lora_r=64`, `lora_alpha=128`, `load_in_4bit=true`.
- Monitor loss curve; early stop if validation perplexity increases for 2 consecutive epochs.
- Save adapter weights; do not merge yet.

### Step 4: Preference Alignment (DPO / ORPO)
- Build preference dataset: for each prompt, select best assistant response (`chosen`) and worst (`rejected`).
- Run DPO or ORPO; compare benchmark scores to SFT-only.
- If preference alignment reduces domain score > 2%, revert to SFT weights.

### Step 5: Catastrophic Forgetting Test
- Run full benchmark suite (general + domain) on merged adapter weights.
- Calculate `forgetting_score`. If > 10%: apply mixed fine-tuning (add 20% general data to dataset) or use replay strategy.

### Step 6: Pruning (Optional, Pre-Deployment)
- Apply magnitude-based pruning to adapter weights (not base model) for small footprint.
- Recover with 1-epoch fine-tune on 10% of dataset.
- Verify domain score remains within 5% of pre-prune.

### Step 7: Quantization for Inference
- Convert to AWQ / GPTQ / GGUF for deployment.
- Use `llama.cpp` or `vLLM` for optimized inference.
- Benchmark latency (tokens/sec) vs quality trade-off.

---
*End of expanded blueprint. All expansions synthesize NVIDIA NeMo distributed skill (FSDP2/PP/CP/MoE), dataset curation best practices, detailed optimization configs, and tech stack implementation steps. Original structure (Sections 1-7 + Action Plan) preserved and extended.*
