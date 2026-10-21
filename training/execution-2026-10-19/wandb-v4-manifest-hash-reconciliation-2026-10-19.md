# W&B v4 manifest hash reconciliation — 2026-10-19 20:15 UTC

The apparent v4 metadata hash mismatch is resolved. No staged metadata, frozen dataset, artifact, or job was changed.

The same JSON manifest has two valid SHA-256 values because the fields use different hashing conventions:

| Evidence field | Convention | Verified value |
| --- | --- | --- |
| `metadata.json.release_manifest_sha256` | Canonical JSON: `json.dumps(manifest, sort_keys=True, separators=(",", ":"))`, then SHA-256 | `10d05ac9d820f4f4f9f2a4d8f222ba5c3226e99486a419fd41ed502bee9697e0` |
| Freeze note and launcher state `manifest_sha256` | SHA-256 of the raw manifest file bytes | `a4b0507ff6447644d022e28b1ada91daefa0139f23f8800ae953a0fa9ab5cdb8` |

The metadata generator explicitly sets the first value with `canonical_hash(manifest)` in `ai/training/launch/wandb_sft_g04.py::make_training_artifact`; that helper sorts keys and removes JSON whitespace before hashing. The launcher state records the second with `sha256_file(request.manifest_path)`. Recomputing both forms from the frozen manifest reproduces both values, so this is not a stale-manifest pointer.

Payload identity also agrees end to end. The raw v4 train payload hashes to `60841fbc8d917de4699d1b41eddddf03fade949496db3e561769f94959e37f20`, matching the frozen manifest’s train partition, artifact `metadata.json`, launcher state, and W&B artifact version metadata. The launcher state’s local artifact metadata hash matches the staged `metadata.json`; local artifact total size is 299,152,842 bytes. The saved W&B artifact inventory observed at 2026-10-19 20:12:59 UTC shows version `v0` with the same artifact total size, release ID, payload digest, and 171,261 rows. The state associates that artifact URI with v4 training job `24cc2d06-3ec3-4356-ad3a-179694dd86a7`.

**Impact:** the hash difference does not affect dataset identity, uploaded artifact integrity, or the v4 job’s dataset reference. Do not rewrite `metadata.json` to the raw-byte digest; that would make it disagree with the launcher’s documented canonical-hash convention and alter a local mirror of the already-uploaded artifact. The earlier Adaption follow-up report and handoff were corrected to remove the false mismatch claim.

No upload or training job was launched as part of this audit. Verification used the launcher’s local hash definitions, the frozen manifest and payload, launcher state, and the saved authenticated W&B artifact inventory.
