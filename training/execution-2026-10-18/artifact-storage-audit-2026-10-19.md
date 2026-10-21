# W&B artifact storage audit — 2026-10-19

This read-only inventory was broadened beyond the four checkpoint collections
for the active full-corpus jobs. It enumerated 279 collections across 8
artifact types. The summed artifact version sizes were about 79.19 GB, which is
not the same measurement as the W&B project storage gauge or account quota.
The public artifact API did not return quota or artifact deletion history.

Both active jobs continued to create checkpoints while cleanup was underway.
At 17:48 UTC, v1 had adapter and train-state v112 at 56,500 batches; v2 had
both at v110 at 55,500 batches. Each active collection had 31 retained
versions. The exact inventory is in the [current checkpoint snapshot](live-monitor/checkpoint-storage-state-2026-10-19-current.json).

Rechecking in response to the user-visible checkpoint activity at 17:59 UTC
confirmed that both jobs remained `RUNNING` and had advanced: v1 LoRA and
train-state v113 at 57,000 batches; v2 both v111 at 56,000 batches. The four
active collections each listed 32 versions, with retained ranges v82-v113 and
v80-v111. Project `storageBytes` was 65,581,760,073, but the API exposes neither
quota nor deletion history. This is an updated checkpoint snapshot, not an
inventory of which artifacts the user removed. The displayed creation of new
checkpoints is compatible with cleanup occurring in other collections.

The four strongest cleanup candidates are completed run-state artifacts. Their
producer runs are finished, `used_by()` returned no downstream runs, and each
artifact is resume state rather than an inference adapter:

| Collection | Producer run | Artifact size | Finding |
|---|---|---:|---|
| `arc-sft-baseline-f00e0bf27bf3-train-state` | `arc-sft-baseline-f00e0bf27bf3` | 1,060,414,697 bytes | Finished; no downstream use recorded |
| `arc-sft-baseline-7f31c66054dc-train-state` | `arc-sft-baseline-7f31c66054dc` | 1,060,414,691 bytes | Finished; no downstream use recorded |
| `arc-corpus-qwen36-sft-20261011-train-state` | `arc-corpus-qwen36-sft-20261011` | 1,060,414,703 bytes | Finished; no downstream use recorded |
| `pixelated-arc-gemma4-sft-20261011-train-state` | `pixelated-arc-gemma4-sft-20261011` | 565,725,323 bytes | Finished; no downstream use recorded |

Together these list 3,746,969,414 bytes (about 3.49 GiB) of nominal artifact
size. They are the clearest removable set if preserving the ability to resume
those completed training runs is unnecessary. Deleting them would remove their
resume state; it would not delete the separately stored LoRA artifacts. No
deletion was performed.

Keep the active jobs' four `*-sft-resume` / `*-train-state-sft-resume`
collections while those jobs run. Keep their v1/v2 training datasets as well.
Standalone LoRA outputs and historical datasets are also not classified as
safe cleanup by this audit because deletion would remove a trained model or a
reproducible training input. W&B may reclaim less storage than the artifact
size sum indicates; verify the project storage gauge after any cleanup.

## Corrected live-view reconciliation (18:18 UTC)

A fresh direct query of typed W&B `lora` and `train-state` collections confirms
the active checkpoints continued beyond the 17:59 snapshot: v1 is at v115 /
58,000 batches (34 visible versions in each active collection, v82–v115), and
v2 is at v113 / 57,000 batches (34 in each, v80–v113). The Training API
`/models/{model_id}/checkpoints` view had shown only base step-0 entries; it was
the wrong view to use for live SFT checkpoint progress. The rolling Artifact API
collections are the authoritative source here.

Private local backups now retain LoRA and train-state data for both runs. At
18:17:41Z, v1 train-state was locally backed through v115 and its LoRA through
v114; v2's LoRA and train-state were both through v113. The backup workers are
alive and poll on a five-minute interval, so the LoRA/resume mirrors may briefly
lag the newest remote checkpoint by one 500-batch save. The live JSON snapshot
records each mirror version. Project storage quota and deletion history remain
unavailable from the checked APIs, so this still does not identify what the
user deleted or prove physical storage was reclaimed.

## Refresh after user-observed checkpoint creation (18:25 UTC)

The user's report that the UI showed new checkpoints was correct. A fresh typed
artifact backup at 18:24–18:25 found v1 had advanced to v116 / 58,500 batches
and v2 to v114 / 57,500 batches; both jobs remained `RUNNING`. The new LoRA
artifacts and matching `train-state` artifacts were downloaded, file-size and
SHA-256 verified by the backup scripts, and the private rolling mirrors now
match those versions. The earlier model-checkpoints API lookup was the wrong
view for this stream. These saves show cleanup did not stop either active job;
they do not reveal which artifacts were deleted or whether the account quota
was relieved.
