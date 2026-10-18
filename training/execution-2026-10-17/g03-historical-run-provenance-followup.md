# G03 historical generator-run provenance follow-up

**Status:** unresolved; metadata narrows the likely run but does not bind it to the artifact.  
**Scope:** metadata only. No source rows, prompts, dialogue, credentials, inference, uploads, or source-data edits.

## Verified evidence

- The local generated checkpoint is recorded as `ai/training/output/nightmare_fuel/checkpoints/edge_and_nightmare_generated.jsonl`,
  SHA-256 `f601a0b8e7dba97db888e63d585cb5309ce734b3f40254b9dfe232d0bf01ce20`, 1,113,006 bytes, 212 rows (120 edge-case and 92 Nightmare
  Fuel), modified 2026-09-17T14:24:26.825969Z. See [`g03-edge-branch-diagnostics.json`](g03-edge-branch-diagnostics.json) and
  [`g03-generated-source-origin.json`](g03-generated-source-origin.json).
- The existing read-only W&B metadata review identified two plausible runs in the same time window: `9fpcyelc` at 2026-09-17T14:02:00Z
  and `r2fkgmd9` at 2026-09-17T14:04:50Z. Both finished and record `backend=vercel`, `model=deepseek/deepseek-v4-flash-0731`, code path
  `ai/training/build_edge_and_nightmare_dataset.py`, and git commit `20f3a3f31b034c4aa9a961ab80b39d1b0137d3eb`.
- The inspected run file manifests contain configuration, metadata, code snapshot, and system history/events artifacts; neither exposes
  the generated JSONL or its SHA-256. Neither run config has `NF_BACKEND`/`NF_MODEL` or an output receipt/hash tying it to the 212-row
  checkpoint. The history parquet is telemetry, not the output dataset.
- The checked local receipt searches are documented in the two reports above: targeted OpenCode SQLite search for Sep 17–18 yielded no
  relevant receipt; there were no Claude logs for Sep 17–19; Foresight keyword search found no historical receipt.

## Assessment by confidence

- **Verified:** two W&B runs used Vercel with DeepSeek V4 Flash and the relevant generator code path/commit; the checkpoint exists with
  the hash, row counts, and timestamp above.
- **Inferred, not established:** those runs are plausible generators for the checkpoint because the code path, commit, and times align.
  There are two candidate runs and no recorded run-to-output relationship, so neither can be selected as the artifact's source.
- **Unknown:** which run (if either) produced the checkpoint; whether both contributed; the exact per-run settings/receipt; and whether
  contemporaneous Vercel/DeepSeek terms permitted retaining the output and transferring it for research fine-tuning.

## Smallest evidence that would close the gap

Recover one authoritative contemporaneous receipt (W&B run config/history or an associated generation-job log) that explicitly binds
the exact checkpoint SHA-256—or a deterministic output manifest containing it—to a run ID and records the effective backend/model. If
no artifact hash was recorded, a receipt that binds the run to the exact output path plus a contemporaneous SHA-256 manifest for that
path is the minimum substitute. Then retain the applicable Vercel and DeepSeek terms/policy snapshot or dated account confirmation
showing output retention and research fine-tuning/transfer rights for that run. A run timestamp or matching code commit alone is
insufficient.

Until that evidence is found and the terms are checked, keep all 212 rows out of any external training or upload package. The 120
first-party synthetic edge rows may still be evaluated under their separate lineage and privacy gates; this report does not change
their release status. The 92 Nightmare Fuel rows remain separately restricted as already documented.
