# OVHcloud AI Training: authenticated state and the GPU blocker

Recorded 2026-11-11. The `ovhai` CLI is authenticated for the first time; this
note captures exactly what the account can and cannot do today, so the next
session does not have to rediscover it.

## Verified state

| Item | Value | How verified |
|---|---|---|
| CLI | `~/.local/bin/ovhai` → `~/bin/ovhai` | symlink present since 2026-10-19 |
| Auth | OAuth, `user-7TZn3EbK7FFD` | `ovhai me` |
| Tenant / project | `6d7e4e17cbf14daabf7dee0210ab9cfc` ("dubstep") | `ovhai me` |
| Region | `US-EAST-VA` (only config) | `ovhai config ls` |
| Endpoint | `https://us-east-va.ai.cloud.ovh.us/v1` | `ovhai config ls` |
| Registry | `registry.us-east-va.ai.cloud.ovh.us/6d7e4e17-cbf1-4daa-bf7d-ee0210ab9cfc` (SHARED) | `ovhai registry list` |
| Datastores | `US-EAST-VA`, `US-WEST-OR` (swift, ovhcloud) | `ovhai datastore list` |
| Object storage | 9.1 TiB quota, zero containers | `ovhai me`, `ovhai bucket list US-EAST-VA` |
| Credentials on disk | OAuth token cached at `~/.config/ovhai/context.json` (mode 600); no `OVH*` keys in `.env` | `ls -la ~/.config/ovhai` |

## The blocker: GPU quota is zero

```
ovhai me
Quotas:
  Resources:
    CPU: 20
    GPU: 0
```

A one-GPU probe is rejected before any resource is allocated:

```
ovhai job run --gpu 1 --name v22-gpu-probe --timeout 5m \
  docker.io/library/alpine:latest -- sh -c 'echo GPU_PROBE_OK'
✘ AI Training error: request error: 402: quota exceeded, please contact us
```

So **no AI Training GPU job can be created** until OVH raises the project's GPU
quota. This is a support action, not a code action: open a quota-increase
request from the OVHcloud control panel (Public Cloud → the `dubstep` project →
Quotas) or a support ticket, stating the flavor (`l40s-1-gpu` or `l4-1-gpu`) and
the count needed.

## What does work today

A CPU job runs end to end: submitted, scheduled, executed, exit 0.

```
ovhai job run --cpu 2 --name v22-cpu-probe --timeout 5m \
  docker.io/library/alpine:latest -- sh -c 'echo CPU_PROBE_OK; uname -m'
→ 158c2ce9-ea54-4238-80c5-a86a8b1fadb0  DONE exit 0
→ logs: CPU_PROBE_OK / x86_64
```

## Available flavors (and why they matter for us)

```
ID          TYPE  DESCRIPTION     CPU/UNIT  MEMORY/UNIT  GPU       DEFAULT  MAX
ai1-1-cpu   cpu   Intel CPU vCores 1        4.0 GiB      ~         true     12
l40s-1-gpu  gpu   NVIDIA L40s     13        80.0 GiB     L40s      false    4
l4-1-gpu    gpu   NVIDIA L4       20        80.0 GiB     L4        true     4
```

Both GPU flavors are 48 GB (L40s) and 24 GB (L4) of VRAM. Our anchor base
`Qwen/Qwen3.6-35B-A3B` needs roughly 70 GB in bf16, or ~20 GB with 4-bit
quantized weights plus activations. That means:

- Full-precision SFT of the 35B anchor: **not possible** on these flavors even
  after a quota grant.
- QLoRA (4-bit) of the 35B anchor: **marginal** on `l40s-1-gpu`, tight on
  `l4-1-gpu`. Feasible only as a slow, checkpointed experiment.
- No A100/H100 flavor is exposed to this project in `US-EAST-VA`.

## Status against the 2026-10-24 OVH entry requirements

From `docs/training/execution-2026-10-24/pivot-gameplan-2026-10-24.md` §3,
OVH "true fine-tuning" was gated on six items. Current position:

1. Anchor base revision frozen: done in the W&B lane (`Qwen/Qwen3.6-35B-A3B`),
   but the flavor list cannot host it — **blocked on hardware, not credentials**.
2. Input data identity frozen: done (v22 manifest).
3. Resume-from-checkpoint smoke job: **not possible** without a GPU.
4. Object-storage contract: containers not created yet; 9.1 TiB is available.
5. Regional cost quote: documented H100 $3.39/GPU-hour and H200 bundle
   $27.28/hour for GRA — neither SKU is in this project's catalog.
6. No download restriction: N/A, OVH is ours.

Net: OVH remains **optional paid infrastructure**, and it is currently
credentials-complete but hardware-blocked. Nothing in the active plan depends on
it; the W&B serverless lane stays primary.
