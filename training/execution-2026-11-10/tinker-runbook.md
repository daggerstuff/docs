# Running the v19 release on Tinker

Tinker is the third training path after W&B/CoreWeave and Adaption. It runs the
same base model as the release (`Qwen/Qwen3.6-35B-A3B`) with the release's own
LR recipe and is scored by the same `paired_eval` harness, so results are
comparable with the W&B arms.

The datums are only meaningful to the tokenizer that produced them, so the
export pins the release tokenizer and the trainer refuses to run if the export
record names a different base model. Whether Tinker hosts this base is still
unknown: `--check` reports it once the account can reach
`/get_server_capabilities`.

## Status

Blocked on billing. The organization `chad@gemcity.xyz - default org`
(`tml:organization:23000cf6-7982-4de2-b59c-e412b773eed8`) returns HTTP 402 on
every model call:

```
Access is blocked due to billing status. Please add payment at
https://tinker.thinkingmachines.ai/billing/balance
```

Health is fine (`/api/v1/healthz` 200), only `/get_server_capabilities` and the
sampling/training calls are gated. Nothing below can run until payment is added.

## 1. Export

```bash
cd ai
PYTHONPATH=. .venv/bin/python -m training.export_tinker_release
```

Writes `training/output/tinker/tinker-dataset.json`
(schema `tinker-tokenized-datums-v1`). Current export: 7,110 datums from 7,110
source rows, 2,807,808 trained of 4,960,905 total tokens
(sha256 `772195a883f9ccce…`).

The export renders each conversation to text once and masks by character offset.
Prefix re-rendering cannot work: the Qwen3 chat template emits an empty thinking
block for every assistant turn except the last, so already-masked tokens change
under incremental renders. Assistant-first arc sessions have their unprompted
opening turn trimmed, not dropped. The Qwen3.5 template also trims message
content, so the export strips content before locating it in the render.

## 2. Check the blocker before planning a run

```bash
PYTHONPATH=. .venv/bin/python -m training.tinker_sft_release --check
```

Reports `health_status`, `capabilities_status`, and `blocked`. `--dry-run`
validates the export against its record (sha256, datum count, trained tokens) and
prints the full plan without touching the API.

## 3. Train

```bash
PYTHONPATH=. .venv/bin/python -m training.tinker_sft_release --execute
```

Recipe: batch 16, warmup 5% linear 1e-5 to 5e-5, hold to 60%, cosine to 5e-6,
LoRA rank 32 (matches the account-proven Fireworks setting), seed 20261110.
Runs too short for the trapezoid fall back to a flat peak LR and are flagged
`recipe_degenerate`. Writes `training/output/tinker/tinker-run.json`
(schema `tinker-sft-run-v1`) with the sampler weights path.

## 4. Score it

```bash
PYTHONPATH=. .venv/bin/python -m training.tinker_eval_shim \
  --run-record training/output/tinker/tinker-run.json --port 8099
```

Then point a `paired_eval` arm at the shim:

```json
{"id": "tinker-v19", "provider": "tinker", "base_url": "http://127.0.0.1:8099/v1",
 "model": "tinker-sft", "api_key_env": "TINKER_SHIM_TOKEN"}
```

`paired_eval` requires https for remote arms; loopback (`127.0.0.1`, `::1`,
`localhost`) is the only place plain http is accepted. Set `TINKER_SHIM_TOKEN`
and export it under the arm's `api_key_env` name to require a bearer token.

Verified with the real release tokenizer (`Qwen/Qwen3.6-35B-A3B`) and the real
`OpenAIChatCompletions` client: prompt rendering, usage counts, stop strings, and
the completion shape round-trip. Training itself has only been exercised against
a fake client because of the 402.
