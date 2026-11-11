# OVHcloud AI Training GPU quota increase request

Draft to send through the OVHcloud support ticket for the project below. Nothing
here has been submitted yet.

## Ticket body

> **Subject:** GPU quota increase for AI Training project `dubstep` (US-EAST-VA)
>
> Hello,
>
> I need GPU quota enabled on an OVHcloud AI Training project that currently has
> zero GPUs. The project is already authenticated and working: CPU jobs run and
> complete normally, and the ObjectStore is reachable, but any GPU job is
> rejected at admission time with HTTP 402.
>
> **Project**
>
> - Project ID: `6d7e4e17cbf14daabf7dee0210ab9cfc` (name: `dubstep`)
> - Region: `US-EAST-VA`
> - AI Training user: `user-7TZn3EbK7FFD`, OAuth token
> - Current quotas: CPU 20, **GPU 0**, storage 9.1 TiB
>
> **What fails**
>
> ```
> ovhai job run --gpu 1 --name v22-gpu-probe --timeout 5m \
>   docker.io/library/alpine:latest -- sh -c 'echo GPU_PROBE_OK'
> ```
>
> ```
> AI Training error: request error: 402: quota exceeded, please contact us
> ```
>
> Debug id `1794364986475`, 2026-11-11T02:42Z. No resource was allocated and
> nothing was billed. The same project runs a CPU job to completion
> (`ovhai job run --cpu 2 ...` → `DONE`, exit 0, job
> `158c2ce9-ea54-4238-80c5-a86a8b1fadb0`), so this is quota, not configuration.
>
> **What I am asking for**
>
> 1. GPU quota of **4 units of `l40s-1-gpu`** (NVIDIA L40s, 13 vCPU / 80 GiB per
>    unit) in `US-EAST-VA`. If `l40s-1-gpu` is unavailable for this account,
>    **4 units of `l4-1-gpu`** (NVIDIA L4, 20 vCPU / 80 GiB per unit) is an
>    acceptable fallback.
> 2. Confirmation of the monthly spend ceiling that applies once the quota is
>    raised, so I can size runs against it.
>
> **What the quota is for**
>
> 4-bit QLoRA supervised fine-tuning of `Qwen/Qwen3.6-35B-A3B` (35B parameters,
> 3B active, MoE) on a clinical conversation corpus:
>
> - Training set: 87,599 rows, 207 MB JSONL, assistant-turn loss masking
> - Sequence length: 4k-8k tokens
> - A single 4-bit quantised replica of the base model is roughly 20-22 GB, so
>   weights plus activations plus the optimiser state do not fit in 24 GB
>   without aggressive sequence truncation. That is why the L40s (48 GB) is
>   preferred and the L4 (24 GB) is a fallback rather than the primary ask.
> - One run is 2-4 GPU-hours; I expect a handful of runs per week while
>   iterating, not a permanently saturated allocation.
>
> **Region note:** the project is pinned to `US-EAST-VA`
> (`https://us-east-va.ai.cloud.ovh.us/v1`). I have no requirement to use
> `US-WEST-OR`; if the GPUs are only available there, I can move the project.
>
> Thank you.

## Facts behind the request (verified 2026-11-11)

| Item | Value | How |
| --- | --- | --- |
| Tenant | `6d7e4e17cbf14daabf7dee0210ab9cfc` ("dubstep") | `ovhai me` |
| User | `user-7TZn3EbK7FFD`, token kind `oauth` | `ovhai me` |
| Quotas | CPU 20 / GPU 0 / storage 9.1 TiB | `ovhai me` |
| Region | `US-EAST-VA` only | `ovhai config ls` |
| GPU flavors offered | `l40s-1-gpu` (L40s, 13 CPU / 80 GiB, max 4), `l4-1-gpu` (L4, 20 CPU / 80 GiB, max 4) | `ovhai flavor list` |
| GPU probe | 402 quota exceeded, debug id `1794364986475` | `ovhai job run --gpu 1` |
| CPU probe | `DONE`, exit 0, `x86_64` | `ovhai job run --cpu 2` |
| Buckets | none yet | `ovhai bucket list US-EAST-VA` |
| Jobs | none | `ovhai job list` |

No A100 or H100 SKU is exposed in this project's catalog, so the request is
scoped to the L40s/L4 pair that is actually orderable.

## Why not just wait for W&B

The W&B training lane already carries the current release and needs no quota.
OVH is the second lane: it is the only place where the base model can be served
next to the adapter for scoring without a serverless round trip, and the only
place where a full-precision attempt is possible at all. Until GPU quota exists,
OVH stays CPU-only and the training work continues on W&B.
