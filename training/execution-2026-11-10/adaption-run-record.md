# Adaption AutoScientist run record — `93d97ca3`

Status: **training succeeded, adapter downloaded, not evaluated.** The trained
adapter has no serving path we can reach, and it cannot be loaded on this host.
Nothing in this document is a score for the model.

## What ran

| Field | Value |
| --- | --- |
| Experiment | `93d97ca3-5fed-425e-a5c2-3fd2eb7a79eb` |
| Provider | Adaption, `client.autoscientist` (AutoScientist) |
| Dataset | `3dc97e6c-b09a-4bef-b21d-6c694f3130ef` `pixelated-v19-selection-20261110` |
| Dataset rows | 57,573 datums from 7,110 v19 source rows (one datum per assistant turn) |
| Base model | `Qwen/Qwen3.6-35B-A3B` |
| Training method | instruction, LoRA |
| Iterations | 5 of 5 (`max_iterations: 5`) |
| Target win rate | 0.6 |
| Best win rate | **0.3926** — did not reach target |
| Started | 2026-11-10T02:20:42Z |
| Completed | 2026-11-10T09:14:41Z (~6h54m) |

Best hyperparameters AutoScientist settled on:

```json
{
  "lora_r": 8, "lora_alpha": 8, "lora_dropout": 0.15,
  "lora_trainable_modules": "q_proj,v_proj",
  "learning_rate": 1.5e-5, "lr_scheduler_type": "cosine",
  "scheduler_num_cycles": 0.5, "min_lr_ratio": 0.1, "warmup_ratio": 0.05,
  "weight_decay": 0.1, "max_grad_norm": 1, "n_epochs": 1,
  "batch_size": "max", "train_on_inputs": false, "training_type": "lora"
}
```

Observed win rate by iteration (polled from the run; iteration 1 was never
sampled): 2 → 0.2086, 3 → 0.2209, 4 → 0.2270, 5 → 0.3926. The run improved
mostly in the last iteration and still finished 0.21 below target.

## Artifacts

`ai/training/output/adaption/autoscientist-93d97ca3/`:

- `adapter.tar.gz` — 7,693,591 bytes as downloaded (zstd stream, `.tar.gz` name
  is misleading)
- `adapter.tar` — 24,207,360 bytes after `zstd -d`
- extracted: `adapter_config.json`, `adapter_model.safetensors` (4,101,280 B),
  `config.json`, `chat_template.jinja`, `tokenizer.json`, `tokenizer_config.json`,
  `special_tokens_map.json`, `trainer_state.json`, `README.md`

Adapter config: PEFT LORA, `r=8`, `lora_alpha=8`, `target_modules=["q_proj","v_proj"]`,
`lora_dropout=0.15`, `inference_mode=true`, base
`togethercomputer/Qwen3.6-35B-A3B_bnb_4bit_t`.

## Why it was not scored

1. **No hosted inference for the adapter.** Adaption's `responses.create`
   rejects the experiment id (`404 Model not found`), and `models.list(type="hosted")`
   only returns platform base models (gemma-4-31b-it, qwen3.8-27b,
   deepseek-v4-flash, …). There is no deployment step in the SDK — `autoscientist`
   exposes `create/cancel/get/list/download/wait_for_completion` only.
2. **It cannot be loaded here.** This host has no GPU (`nvidia-smi` absent),
   8 CPUs and 28 GB RAM. The adapter targets a 4-bit `bitsandbytes` build of a
   35B MoE base; bnb 4-bit inference is CUDA-only, and an unquantised fallback
   needs roughly 70 GB in bf16.
3. **The harness expects an OpenAI-compatible chat endpoint.** `paired_eval`
   posts to `{base_url}/chat/completions`; Adaption exposes a Responses-style
   API instead, so even a hosted adapter would need a shim.

Scoring it would require either an Adaption deployment API that does not exist
today, or a GPU box with the 4-bit base plus a local chat-completions shim.

## What the result is worth

The win rate is AutoScientist's own preference comparison against its own
candidate pairs, not the 52-case paired harness the other releases use, so
0.3926 is not comparable to v19/v20/v21 scores. Treat this run as an
experiment in provider tooling, not as a model candidate.

Two observations worth keeping:

- AutoScientist chose `r=8` / `alpha=8` / `q_proj,v_proj` / `lr=1.5e-5`. Our
  account-proven W&B recipe is `r=32` / `alpha=32` / `q,k,v,o_proj` / `lr=1e-4`,
  which scored 0.6843 and 0.6414 on the same base in earlier runs. The smaller
  rank is the likely reason this run plateaued.
- The v19 dataset mapping (`prompt_column: original_prompt`,
  `completion_column: original_completion`) persisted from the rejected
  `datasets.adapt` call and was reused here without error, so the column
  mapping path is fine; the account plan ceiling (50,000 rows per launch) was
  never hit because AutoScientist accepted the full 57,573-row dataset.
