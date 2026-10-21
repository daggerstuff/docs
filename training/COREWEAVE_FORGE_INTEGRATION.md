# CoreWeave Forge Integration & Optimization Architecture

> Comprehensive guide for utilizing CoreWeave Forge across **Pixelated Empathy** (`apps/`, `ai/pkg_mera/`, and `ai/training/`).

---

## 1. Executive Summary: The Unified Forge Ecosystem

CoreWeave Forge unifies high-performance cloud compute with the Weights & Biases machine learning platform. It consolidates model development into an integrated lifecycle:

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                                COREWEAVE FORGE                                    │
│                                                                                   │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌───────────────────┐  │
│  │   Post-Training (SFT)   │  │   Post-Training (RL)    │  │ Model Distill     │  │
│  │  Multi-GPU Auto-Scale   │  │   Multiplexed RL/PPO    │  │ Traffic Synthesis │  │
│  └───────────┬─────────────┘  └───────────┬─────────────┘  └─────────┬─────────┘  │
│              │                            │                          │            │
│              ▼                            ▼                          ▼            │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                   Model & Artifact Registry (Lineage, TTL)                  │  │
│  └──────────────────────────────────────┬──────────────────────────────────────┘  │
│                                         │                                         │
│              ┌──────────────────────────┴──────────────────────────┐              │
│              ▼                                                     ▼              │
│  ┌────────────────────────┐                             ┌──────────────────────┐  │
│  │  Serverless Inference  │                             │   Agent Lens & Weave │  │
│  │ (OpenAI-compatible)    │                             │  (Traces, Evals)     │  │
│  └───────────┬────────────┘                             └──────────┬───────────┘  │
│              │                                                     │              │
│              └──────────────────────────┬──────────────────────────┘              │
│                                         ▼                                         │
│                         ┌───────────────────────────────┐                         │
│                         │ External HiveMind CLI         │                         │
│                         │ (separate; no Forge wiring)   │                         │
│                         └───────────────────────────────┘                         │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. CoreWeave Forge Service Matrix for Pixelated Empathy

| Forge Service | Role in Pixelated Empathy | API Endpoint / Route | Managed Module |
| :--- | :--- | :--- | :--- |
| **Serverless SFT** | Supervised fine-tuning of the selected Gemma 4 and Nemotron 3.5 Lightning foundation models. | `https://api.training.wandb.ai/v1/preview/sft-training-jobs` | `ai/training/scripts/train_sft_serverless.py`, `ai/training/launch/wandb_sft_v6.py` |
| **Serverless RL** | Post-training reinforcement learning targeting multi-turn tool adherence and eliminating fake tool claims. | `https://api.training.wandb.ai/v1/preview/rl-training-jobs` | `ai/training/forge/rl_runner.py`, `ai/training/scripts/train_rl_serverless.py` |
| **Serverless Inference** | OpenAI-compatible serving of base foundation models for synthetic data generation & evaluation. | `https://api.inference.wandb.ai/v1/chat/completions` | `training.forge.client.CoreWeaveForgeClient` |
| **Trained LoRA Serving** | Zero-cold-start inference against trained adapter checkpoints (`wandb-artifact:///...`). | `https://api.training.wandb.ai/v1/chat/completions` | Handled automatically by `ForgeConfig.resolve_inference_endpoint` |
| **HiveMind (separate service)** | Shared developer session tracking, cross-agent search, and token usage reporting. | `https://hivemind.wandb.tools` | Standalone `hivemind` CLI daemon; not wired through `training.forge` |
| **Agent Lens & Weave** | Observability for therapeutic multi-turn simulation agents, prompt quality, and safety gates. | `https://api.wandb.ai` | `ai/pkg_mera/`, `ai/lab/evals` |
| **Registry & Quota Opt**| Versioned checkpoint storage with automated TTL policies against the 200 GB trailing limit. | Forge Artifact Registry | `ai/training/forge/quota_optimizer.py` |

HiveMind is a separate developer-session service, not a Forge API integration.
The local HiveMind CLI daemon handles its authentication and synchronization;
`ForgeConfig.hivemind_endpoint` currently only reads the endpoint setting and
is not consumed by `CoreWeaveForgeClient`, the SFT/RL launchers, or the quota
optimizer. Forge training and inference requests do not create HiveMind traces
or report training spend there.

---

## 3. Smart Endpoint Routing Architecture

A common operational failure mode was sending trained adapter checkpoints to the foundation inference route (`api.inference.wandb.ai`), which returned HTTP 500 errors. 

The new unified client implements **Smart Endpoint Routing**:

```python
from training.forge import CoreWeaveForgeClient, ChatCompletionOptions

client = CoreWeaveForgeClient()

# 1. Base Model -> Automatically routes to Serverless Inference (api.inference.wandb.ai)
base_res = client.chat_completion(
    model="nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B",
    messages=[{"role": "user", "content": "Explain cognitive restructuring."}],
)

# 2. Checkpoint Artifact -> Automatically routes to Post-Training completions (api.training.wandb.ai)
adapter_res = client.chat_completion(
    model="wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-8c7be00285f2:v1",
    messages=[{"role": "user", "content": "Patient presents with anxiety."}],
    options=ChatCompletionOptions(temperature=0.3, max_tokens=1024),
)
```

---

## 4. Serverless RL: Resolving Tool-Use Regressions Post-SFT

### Findings from V6 SFT Campaign:
- **Clean Loss Convergence**: Octiles walked from 1.191 down to 1.011 (final-100 mean 1.015, zero spikes > 100).
- **Format Bleed Eliminated**: 0/5 therapy bleed vs 3/5 in v5.
- **Remaining Gap**: Tool-calling regressions on non-clinical queries (e.g., research citations made 0 tool calls and hallucinated citations; memory-write skipped real tool call and returned fake confirmation *"Confirmed: saved"*).

### Forge Serverless RL Solution (`training.forge.rl_runner`):
CoreWeave Serverless RL post-trains the model with custom multi-objective verifier rewards:

1. **Tool-Call Fidelity Reward**:
   - `+1.0` if expected tool is invoked with valid arguments.
   - `-1.0` if tool call is skipped and response fabricates an action confirmation.
   - `-0.5` if tool call is skipped.
2. **Anti-Therapy Bleed Reward**:
   - `+1.0` if factual response contains zero clinical therapeutic framing.
   - `-1.0` if excessive empathy cues appear in factual contexts.
3. **Clinical Safety Disclosure**:
   - `+1.0` if 988 / crisis hotline is triggered appropriately.
   - `-2.0` zero-tolerance penalty if crisis indicators are ignored.

Run dry-run or live submission:
```bash
python3 ai/training/scripts/train_rl_serverless.py \
  --model-id "wandb-artifact:///wutang/pixelated-empathy-kan28/arc-sft-baseline-8c7be00285f2:v1" \
  --dataset-url "wandb-artifact:///wutang/pixelated-empathy-kan28/v6-rl-episodes:v0" \
  --tool-weight 0.40 \
  --bleed-weight 0.20 \
  --safety-weight 0.15 \
  --dry-run
```

---

## 5. Storage Quota Optimization (Managing the 200 GB Ceiling)

Forge organizations are subject to a **200 GB trailing-average storage entitlement**. SFT campaigns generating 100+ intermediate checkpoints can rapidly exhaust this quota.

### Automated Pruning Policy (`training.forge.quota_optimizer`):
- **Milestone Protection**: Keeps `:v0`, every 10th checkpoint step (`:v10`, `:v20`...), and the final 3 checkpoints (`:v_last-2`, `:v_last-1`, `:v_last`).
- **Pruning Candidates**: Flags unneeded intermediate steps for pruning after mirroring to private local disk (`ai/training/output/wandb_local_checkpoints/`).
- **Threshold Alerts**: Triggers warnings whenever storage exceeds 85% of entitlement.

---

## 6. Verification and Testing

All Forge modules are strictly validated under `pytest` with zero suppressions:
```bash
# Run the complete CoreWeave Forge test suite
uv run pytest ai/training/tests/test_coreweave_forge.py

# Verify code style and type safety
uv run ruff check ai/training/forge ai/training/scripts/train_sft_serverless.py ai/training/scripts/train_rl_serverless.py
```
