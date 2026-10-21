# W&B artifact storage triage — 2026-10-19

## 09:15 UTC next-day reconciliation — 2026-10-20

The user observed checkpoint creation during cleanup and correctly noted that
the visible new items could be different from those being deleted. A fresh
authenticated Artifact API inventory resolves the active stream: v4 adapter
and train-state collections both contain versions through v58 at 29,500
batches (created 09:15:27 and 09:15:30 UTC). Their sizes are 117,843,308 B and
1,060,414,703 B. The v4 training job remains `RUNNING` with no reported error.

The v1 and v2 adapter and train-state resume collections now each return zero
visible versions, whereas the previous inventory showed these streams had
many versions. This strongly indicates that the cleanup removed those older
checkpoint artifacts; the remaining v4 checkpoints were being written in a
different set of collections. Local copies remain: v1 adapters through v144,
v2 adapters through v142, and train-state copies v1 v143 / v2 v142 (the last
recorded mirror heads). The latest v4 artifacts are intact and locally
mirroring through v57 at the time of this check. Do not interpret this as
deletion of the active v4 checkpoint stream. The W&B API has no deletion
history, so it cannot attribute a specific click to a specific version.

The authenticated project GraphQL `storageBytes` meter reads 60,634,387,885 B
at 09:15 UTC, compared with 116,486,273,253 B at 22:09 UTC on Oct 19, a
decrease of 55,851,885,368 B (about 48%). This is consistent with successful
cleanup and substantial reduction in project storage. It is a project meter,
not the account quota, and does not expose physical reclamation timing. No
artifact was modified or deleted by this audit.

## 20:53 UTC live storage meter and refreshed deletion candidates

The owner was right that checkpoints continued to be created during cleanup.
I queried the authenticated W&B project's GraphQL `storageBytes` field directly:
it was 30,167,440,389 B at 15:07 UTC and 101,403,428,801 B at 20:51 UTC, an
increase of about 71.24 GB over 5 hours 44 minutes (about 12.4 GB/hour). This
project metric does not expose the account quota or rolling billable storage,
but it confirms that project storage grew sharply while the owner was making
space.

The Artifact API shows each active job writing a 1,060,414,709-byte train-state
artifact roughly every ten minutes, plus a 117,843,308-byte LoRA. At the latest
snapshot, v1 was at train-state v131 and v2 at v130; v4 remains PENDING. The
two live jobs alone add roughly 12.7 GB/hour of train-state logical artifacts
if that cadence continues. This rate closely matches the project-meter growth
and explains why removing old artifacts can appear ineffective during active
training.

A fresh, read-only dependency check retained the two newest train-state
versions in each active collection and checked every older visible version.
The current candidates are v2 train-state v80–v128 (49 versions) and v1
train-state v82–v129 (48 versions), 97 versions totaling 102,860,226,773 B
(102.86 GB) logical. All 97 are alias-free; each `used_by()` check succeeded
and returned zero dependencies. The newest two per stream (v2 v129/v130; v1
v130/v131) were excluded from deletion candidates to preserve recent recovery
points. The version-by-version evidence is in the private mode-0600
[`live candidate audit`](wandb-live-train-state-delete-candidates-2026-10-19T2051Z.json).

These are the clearest current W&B Artifacts cleanup targets. They are
train-state snapshots rather than model LoRAs; retain the newest two per job
and all LoRA versions for checkpoint comparisons. The logical sizes are not a
promise of physical space reclaimed because W&B does not expose deduplication,
garbage-collection timing, or the account quota in this API. No deletion was
performed by the agent. The user's cleanup may be in progress; a fresh storage
meter read is needed after it settles to verify reclaimed space.

## 20:56 UTC live meter recheck

A second authenticated GraphQL read at 20:56:53 UTC returned 101,403,458,209 B,
only 29,408 B above the 20:51:00 UTC reading. This is effectively flat over
five minutes despite both training jobs remaining active and the checkpoint
watchers running. It does not establish that the user's deletion reclaimed
space because the project meter may update asynchronously, and the Artifact API
snapshot was not refreshed in this read. It does establish that the earlier
12.4 GB/hour growth rate should not be extrapolated across this later interval.
No artifact was deleted or modified by this recheck.

## 21:03 UTC confirmed checkpoint growth

The 21:03:41 UTC rolling-backup manifest now records v1 train-state v132 at
66,500 completed batches and v2 v131 at 66,000 batches. Each artifact is
1,060,414,709 B, and both source jobs are still `RUNNING`. This is newer than
the 20:51 inventory (v1 v131; v2 v130), so both streams advanced one checkpoint.
The independent GraphQL project meter is 103,288,803,197 B, up
1,885,344,988 B from the 20:56:53 read. That rise is close to the two new
train-state artifacts' 2,120,829,418 logical bytes, with about 235 MB net
difference. It supports the user's observation that newly written checkpoints
can overtake artifact cleanup; it does not identify which objects were removed
or prove physical quota reclamation. Exact backup heads are recorded in the
mode-0600 `ai/training/output/wandb_local_checkpoints_20261019/train-state-manifest.json`.

## 20:12 UTC project-wide deletion reconciliation

I enumerated all 285 artifact collections again through the read-only W&B
Artifact API and compared every `(type, collection, version)` with the complete
19:39 inventory. All 447 versions from 19:39 remain visible; 14 new versions
were added, all in the four active v1/v2 LoRA and train-state streams. No
visible artifact version disappeared from `wutang/pixelated-empathy-kan28`
between those snapshots. The exact mode-0600 inventory is
[`wandb-artifact-inventory-2026-10-19T2012Z.json`](wandb-artifact-inventory-2026-10-19T2012Z.json).

The latest visible heads are v1 LoRA/train-state v127 (64,000 batches,
20:07:36–20:07:40 UTC) and v2 LoRA/train-state v125 (63,000 batches,
20:03:42–20:03:44 UTC). This strengthens the conclusion that the user's
cleanup did not remove versions from this project's visible artifact inventory
after 19:39. It still cannot identify a deletion before that snapshot, another
project/account, a non-artifact storage surface, or physical quota reclamation.
The local rolling mirror has both heads: adapter files and all 11 train-state
files for v1 v127 and v2 v125 passed local size/SHA-256 verification. No
artifacts were deleted by this inventory.

## 20:04 UTC recheck after the user's cleanup observation

The user observed new checkpoints appearing while deleting artifacts, which
may mean the cleanup view showed different items from the four collections
previously inspected. A fresh read-only Artifact API query confirms the live
streams continued advancing through 20:03:44 UTC:

| Stream | Latest version | Created UTC | Bytes |
|---|---:|---|---:|
| v1 LoRA | v126 | 19:58:10 | 117,843,308 |
| v1 train-state | v126 | 19:58:12 | 1,060,414,709 |
| v2 LoRA | v125 | 20:03:42 | 117,843,308 |
| v2 train-state | v125 | 20:03:44 | 1,060,414,709 |

The live checkpoint-writing process explains why storage could keep changing
during cleanup. These four streams do not appear to be the items the user was
deleting: all versions visible in the latest query remain listed, and new
versions were added. This API read cannot identify the UI selection or
deletion, show W&B deletion history, or report reclaimed physical quota. Treat
the older train-state list below as conditional advice only, not as the answer
to which objects were removed. No artifact was deleted by this check.

## 19:52 UTC targeted checkpoint recheck

The owner is right that the checkpoint stream could be mistaken for the items
being deleted. I queried the four live v1/v2 LoRA and train-state collections
directly, rather than inferring from project-wide storage totals. Since the
19:39 snapshot, v1 advanced from v123 to v125 (two checkpoint cycles) and v2
from v122 to v123 (one cycle). Current heads are v1 v125 and v2 v123, created
at 19:48:42–19:48:45 and 19:45:01–19:45:03 UTC respectively. Their train-state
versions are about 1.06 GB apiece; LoRAs are about 118 MB. The collection
versions visible in the 19:39 snapshot remain present in these four streams.

This confirms checkpoint creation while cleanup was happening, and confirms
that the cleanup being observed did not remove versions from these four active
collections. It does not identify what was deleted: I had been using these
checkpoint collections as candidate cleanup targets, but they may not be the
items shown in the user's cleanup view. The API cannot report the UI selection,
deletion history, or current physical quota. So the previous candidate list is
not evidence that those were the right items to delete. Exact current heads are
visible through the W&B API; the earlier complete inventory remains at
[`wandb-artifact-inventory-2026-10-19T1939Z.json`](wandb-artifact-inventory-2026-10-19T1939Z.json).

At 19:58 UTC a follow-up API read showed v2 advanced again to LoRA and
train-state v124, created at 19:54:23–19:54:25 UTC. The local train-state
manifest was last refreshed at 19:53:47 and still showed v2 v123, while the
LoRA mirror had already reached v124. The train-state watcher remains active;
this is mirror lag during a live stream, not evidence of a failed remote save.

At 19:59:25 UTC the active train-state mirror caught up and advanced to v1
v126/v2 v124. All 11 files in each latest state artifact passed local size and
SHA-256 checks against its private manifest. The current adapter manifest is
v1 v125/v2 v124; both adapter files also pass their stored size/hash checks.

## 19:39 UTC fresh check against the user's checkpoint observation

The read-only Artifact API now shows 447 versions, compared with 443 at
19:27. Exactly four versions were added: LoRA and train-state v123 for v1,
and LoRA and train-state v122 for v2. The latest train-state files are each
1,060,414,709 bytes; their adapter files are each 117,843,308 bytes. This is
direct evidence that checkpoint creation continued during cleanup.

The version-by-version comparison found all 443 versions from the 19:27
snapshot still visible. That includes every older active v1/v2 version in the
previous 79-version candidate set. Thus the observed cleanup did not remove
any version from the W&B project's currently visible inventory between these
two snapshots. This does not prove nothing was deleted: deletion could have
been from a different project/account, an unlisted storage surface, or before
the 19:27 snapshot; the API has no deletion history or quota meter. The fresh
private inventory is
[`wandb-artifact-inventory-2026-10-19T1939Z.json`](wandb-artifact-inventory-2026-10-19T1939Z.json)
(mode 0600). Existing older-version candidates remain candidates only; this
check did not perform deletion or verify physical quota recovery.

Observed directly through the authenticated W&B Artifact API at 18:52 UTC and
local mirror manifests at 18:55 UTC in
`wutang/pixelated-empathy-kan28`; job states were fetched separately through
the Training API. No artifact was deleted by this audit.

## 19:27 UTC full-inventory reconciliation

I enumerated every collection and visible version again via the read-only W&B
Artifact API. The exact private snapshot is
[`wandb-artifact-inventory-2026-10-19T1926Z.json`](wandb-artifact-inventory-2026-10-19T1926Z.json)
(mode 0600). It contains 285 collections and 443 visible versions. Compared
with the 15:45 inventory, the project has 2 more collections, 96 more visible
versions, and 55.91 GB more summed logical artifact-version size. By type:

| Type | 15:45 versions | 19:27 versions | Change | 19:27 logical bytes |
|---|---:|---:|---:|---:|
| `lora` | 44 | 92 | +48 | 11,262,534,081 |
| `train-state` | 40 | 87 | +47 | 91,761,390,261 |
| `dataset` | 5 | 6 | +1 | 908,520,985 |
| Other five types | 258 | 258 | 0 | 2,449,640 |

The two added collections are the v4 dataset and base-LoRA collections. The
active v1/v2 checkpoint collections continue to grow and their older visible
versions remain present relative to the 16:26 per-version snapshot. This
supports the user's observation that checkpoint creation continued while they
were deleting items. The aggregate inventory shows net growth in every type
that changed since 15:45, but concurrent checkpoint creation could mask
deletions in the same type. These totals do not prove that no W&B artifacts
were deleted. The API exposes no deletion event history or physical quota
meter. Empty collections are also present, but have zero visible artifact
bytes; they are not storage cleanup targets. Do not claim the user's deleted
items have been identified from this inventory.

### Current low-risk train-state cleanup set

At 19:29 UTC, I checked every older train-state version in the two active
collections, keeping each collection's newest two versions. All 79 older
versions are unaliased, and the W&B Public API `used_by()` check succeeded and
returned zero dependent runs for every version. They occupy 83,772,762,011
nominal bytes (about 78.04 GiB): v1
`arc-sft-baseline-8ce8354c67ef-train-state-sft-resume` v82–v120 (39 versions),
and v2 `arc-sft-baseline-556695bfd5c4-train-state-sft-resume` v80–v119 (40
versions). The newest two remain remote and have verified local mirrors: v1
v121/v122 and v2 v120/v121. The private per-version dependency audit is
[`active-train-state-cleanup-audit-2026-10-19T1927Z.json`](active-train-state-cleanup-audit-2026-10-19T1927Z.json)
(mode 0600).

If space must be reclaimed through the W&B artifact UI, these are the best
current candidates: select only those exact older **train-state versions**,
not whole collections, LoRAs, datasets, or aliases. This retains two recovery
points per live job and independent local copies. It reduces older rollback
options, and W&B logical size is not guaranteed physical reclamation; both jobs
continue writing roughly 1.06 GB per checkpoint, so cleanup may buy temporary
headroom. No deletion was made by this audit. Four completed-job train-state
artifacts were also checked; they have zero `used_by()` results but retain
`latest` and `step1` aliases, so leave them alone unless those aliases are
separately understood and removed intentionally. Their private audit is
[`completed-train-state-cleanup-audit-2026-10-19T1929Z.json`](completed-train-state-cleanup-audit-2026-10-19T1929Z.json).

## 19:22 UTC retention reconciliation

A direct comparison against the 16:26 UTC artifact-version snapshot now resolves
part of the user's concern. Each active collection has 41 visible versions:
v1 LoRA and train-state v82–v122, and v2 LoRA and train-state v80–v120. All
22 versions previously visible in each collection are still present; each
collection added 19 versions and none of the earlier versions disappeared.
The newest versions are 61,500 batches for v1 and 60,500 for v2. The local
rolling mirrors now contain v1 v122 and v2 v120 for both LoRA and train-state.
See the private [retention reconciliation](active-checkpoint-retention-reconciliation-2026-10-19T1922Z.json).

This is positive evidence that cleanup did not remove versions from these four
active checkpoint collections after 16:26. The user's deleted items therefore
may be elsewhere in the project or predate that snapshot. Neither the API nor
the logged-out Browserbase page identifies deletions in other collections.

## Active checkpoint stream (18:52 snapshot; refreshed above)

| Training job | Artifact collection | Retained versions | Latest | Latest size | Remote aliases | Local verified mirror |
|---|---|---:|---|---:|---|---|
| v1 `2087f223-a48f-45f7-9999-daece5743bba` | `arc-sft-baseline-8ce8354c67ef-sft-resume` (lora) | 38, v82–v119 | v119 / 60,000 batches | 117,843,308 B | `latest`, `sft-resume-2087f223-a48f-45f7-9999-daece5743bba` | v118 and v119, verified by 18:55 |
| v1 | `arc-sft-baseline-8ce8354c67ef-train-state-sft-resume` | 38, v82–v119 | v119 / 60,000 batches | 1,060,414,709 B | `latest`, `sft-resume-2087f223-a48f-45f7-9999-daece5743bba` | v118 and v119, verified by 18:55 |
| v2 `f914f0fb-f892-4e1a-8291-8cea3757274e` | `arc-sft-baseline-556695bfd5c4-sft-resume` (lora) | 38, v80–v117 | v117 / 59,000 batches | 117,843,308 B | `latest`, `sft-resume-f914f0fb-f892-4e1a-8291-8cea3757274e` | v116 and v117 |
| v2 | `arc-sft-baseline-556695bfd5c4-train-state-sft-resume` | 38, v80–v117 | v117 / 59,000 batches | 1,060,414,709 B | `latest`, `sft-resume-f914f0fb-f892-4e1a-8291-8cea3757274e` | v116 and v117 |

The checkpoint records confirm the user's observation: these four collections
continued receiving new versions during cleanup. The adapter files are about
118 MB each; each optimizer/resume-state artifact is about 1.06 GB. On the
observed 500-batch cadence, the two active jobs add about 2.12 GB of nominal
artifact size per checkpoint cycle. This explains why storage can remain tight
while training is succeeding.

## Conditional cleanup candidates; deletion target not identified

A fresh direct artifact API poll at 18:57 UTC returned the same four stream
heads as at 18:52: v1 LoRA and train-state v119 (60,000 batches), and v2 LoRA
and train-state v117 (59,000 batches). The local mirror manifests at 18:55
contain the newest two versions for both runs and both artifact types. This
confirms the observed checkpoint creation and that the streams had not advanced
again by 18:57. It does **not** identify the artifacts the user deleted: the
API does not expose deletion events, and these active checkpoint collections
may not be the storage items that were removed in the UI. Treat the following
list only as conditional candidates if the cleanup view was showing these
specific `train-state` collection versions.

Browserbase reached the CoreWeave Forge W&B project, but that browser session
was logged out and showed the login page. An API token authenticates the
read-only API queries but does not establish the browser session. Therefore,
the exact cleanup-screen items remain unidentified; the user was given the
session link to sign in if they want the UI matched to this inventory.

If the immediate goal is to recover remote artifact storage while retaining
resume capability, the version pattern with the lowest practical risk is to
keep the newest two verified versions in each active collection and target
only older, unaliased train-state versions:

- v1 train-state: v82–v117 (36 versions; 38,174,929,524 nominal bytes).
- v2 train-state: v80–v115 (36 versions; 38,174,929,524 nominal bytes).

Together those ranges are 72 old internal checkpoints / 76,349,859,048 nominal
bytes (about 71.1 GiB). At 18:52, all 72 are unaliased internal checkpoints;
neither range includes the current `latest` alias or immediately previous
checkpoint. v1 and v2's newest two have verified local copies under
`ai/training/output/wandb_local_checkpoints_20261019/`. Keeping the newest two
remote versions preserves a recent recovery pair per job.
Historical internal
train-state versions are resume snapshots, not the trained LoRA outputs; the
separate LoRA collections should be retained for evaluation/model use.

This is a concrete cleanup target, not proof that W&B will reclaim the full
nominal byte total: the Training/Artifact API does not expose physical quota,
deletion audit, or retention semantics. Deleting older checkpoints also gives
the active jobs room to write only temporarily, because each job is still
creating roughly one 1.06 GB state artifact per 500 batches. If W&B applies a
retention rule automatically, or if the job reads historical versions by
numeric version, deletion semantics may differ; verify the exact version
selection in the UI before applying a bulk delete. Do not delete the active
dataset v4 artifact, active `latest` checkpoints, or newest two verified
resume-state versions.

Two additional completed jobs each have one ~1.06 GB state artifact and a
separate final LoRA artifact: `arc-sft-baseline-f00e0bf27bf3-train-state:v0`
(job completed 2026-10-18 16:45 UTC) and
`arc-sft-baseline-7f31c66054dc-train-state:v0` (job completed 2026-10-18
15:36 UTC). These are optional cleanup candidates only if future resume from
those completed jobs is unnecessary; retain their LoRA artifacts if those
models are still needed.

The v4 full-corpus W&B job is still PENDING with no `training_start`, events,
progress, or `error_message`; the `/system-check` reports healthy queues. Its
pending reason is not exposed by the available API. The stale project
`storageBytes` snapshot predates this audit and must not be presented as the
current quota or current physical storage.

## 20:35 UTC refresh after the cleanup-view clarification

A fresh authenticated, read-only inventory of all 285 collections now shows 471
versions, compared with 461 at 20:12 UTC. All 461 earlier version keys remain
visible; the 10 additions are new LoRA and train-state checkpoints in the two
active baseline collections. No visible version disappeared. The exact
mode-0600 snapshot is
[`wandb-artifact-inventory-2026-10-19T2035Z.json`](wandb-artifact-inventory-2026-10-19T2035Z.json).

This supports the user's point that the items being deleted may be on a
separate artifacts/storage view: the W&B project inventory still does not
identify any removed object. The four streams were at v1 v129 and v2 v128 by
20:32 UTC. Direct Training API reads at 20:34 UTC still showed v1/v2
`RUNNING` and the v4 job `PENDING`; the API returned no pending reason or
progress fields. Browserbase session startup again returned `Session
terminated`, so this refresh could not inspect the user's browser view. No
artifact was modified or deleted by these checks.

## Logical size and retained cleanup candidates

Summing the API-reported size of all 471 versions in the 20:35 inventory gives
120,430,507,205 logical bytes (120.43 GB decimal). `train-state` accounts for
106.61 GB, `lora` for 12.91 GB, and datasets for 0.91 GB. These are sums of
version sizes, not a physical storage meter; backend deduplication or other
storage accounting may differ.

All 79 old active-job train-state versions from the 19:27 dependency/alias
check remain visible in the 20:35 inventory. That audit found zero aliases and
zero dependencies for those candidates, while retaining the two newest train-
state versions in each active collection. Their summed logical size is
83,772,762,011 bytes (83.77 GB decimal). The exact version-by-version audit is
[`active-train-state-cleanup-audit-2026-10-19T1927Z.json`](active-train-state-cleanup-audit-2026-10-19T1927Z.json).
This makes those 79 old versions the clearest W&B project cleanup candidates,
but does not prove that deleting them will reclaim 83.77 GB physically or
identify the objects the user already removed. No deletion was made here.

## 21:40 UTC meter and live-adapter refresh

The authenticated GraphQL `Project.storageBytes` reading was 110,830,208,881 B
at 21:40:49 UTC, up 4,713,388,202 B from 21:19:01 UTC (about 12.97 decimal
GB/hour over that interval). The meter confirms continuing project growth but
still does not reveal whether UI deletions reclaimed physical quota or what the
account limit is. The active v1/v2 jobs remain `RUNNING` with no error or
progress field; the v4 job remains `PENDING` with no start/error/progress. A
direct adapter-collection query at 21:37:30 UTC found v1 inference adapter v136
(68,500 batches, published 21:33:46 UTC) and v2 v134 (67,500 batches,
published 21:29:15 UTC). The separate local train-state mirror at 21:25 held
v1 v135 and v2 v133. This reconciles the checkpoint-creation notice: the
stream was advancing, and the adapter inventory had moved beyond the earlier
snapshot while checks were running. The current v1 v136 evaluation is in
progress; the v1 v135/v2 v134 pair completed and showed the same SFT collapse.
See the mode-0600 [live storage and adapter snapshot](wandb-live-storage-adapter-refresh-20261019T2140Z.json)
and [checkpoint comparison report](latest-checkpoint-evals/report.md). No W&B
artifacts were modified or deleted by this refresh.

## 21:53 UTC after the next adapter milestone

The project `storageBytes` meter reached 112,715,553,869 B at 21:53:43 UTC,
1,885,344,988 B above the 21:40:49 UTC reading (about 8.77 decimal GB/hour
over that interval). A direct adapter query at the same cutoff found v1 v138
(69,500 batches, published 21:52:24 UTC) and v2 v136 (68,500 batches,
published 21:47:45 UTC). The v1 v137/v2 v135 comparisons completed while these
newer versions were appearing; both again showed SFT collapse. The newer v138
and v136 heads are recorded as current but untested. Because consecutive
tested heads show the same severe collapse, the next evaluation budget should
go to the planned training/data diagnostics rather than every adjacent
checkpoint. The [21:53 snapshot](wandb-live-storage-adapter-refresh-20261019T2153Z.json)
records exact versions and meter values. This project meter still does not
identify what was deleted or prove physical quota reclamation; no artifacts
were modified or deleted by the agent.

## 22:09 UTC meter, checkpoint, and local-backup refresh

At 22:09:10 UTC, project `storageBytes` was 116,486,273,253 B, up
3,770,719,384 B since 21:53:43 UTC (15m27s, approximately 14.64 decimal
GB/hour). The fresh `lora` and `train-state` collection queries found v1 v139
at 70,000 batches and v2 v138 at 69,500 batches. Both jobs still report
`RUNNING`; the v4 job remains `PENDING` with no adapter or train-state artifact.
The Training API's `/checkpoints` response still lists only step 0; the two
versioned artifact collections are the source of truth for the trained
checkpoints. The full read-only snapshot is
[`wandb-live-storage-adapter-refresh-20261019T2208Z.json`](wandb-live-storage-adapter-refresh-20261019T2208Z.json).

The local backup watchers are active. I verified file size and SHA-256 for the
newest local copies of v1 LoRA v139, v2 LoRA v138, v1 train-state v139, and v2
train-state v138; all 26 files matched their manifests. Local filesystem free
space was 17 GB at the check. This provides a verified local copy of current
W&B checkpoints, but no local Fireworks weights are available yet. No remote
artifact was modified or deleted.

## 22:14 UTC refreshed train-state cleanup candidates

A fresh read-only dependency/alias audit at 22:13:53 UTC covered the current
visible train-state collections. It found 114 older versions with no aliases
and successful `used_by()` checks returning zero dependencies, while excluding
the newest two versions per active run. The candidate ranges are v1 v82-v138
(57 versions) and v2 v80-v136 (57 versions), totaling 120,887,276,826 B
(120.89 GB) of logical artifact size. Latest retained recovery points are v1
v139/v140 and v2 v137/v138. The current project meter was 117,428,953,099 B;
logical candidate bytes are not a promise of physical space reclaimed because
W&B does not report quota or garbage-collection effects. If the owner wants to
free space, these unreferenced older train-state versions are the concrete
artifact-level candidates; deleting them would remove older rollback points.
No artifact was deleted. Full version-by-version evidence is in the private
mode-0600 [22:13 candidate audit](wandb-live-train-state-delete-candidates-2026-10-19T2213Z.json).

## 22:29 UTC refreshed storage and cleanup inventory

The authenticated project meter read 120,256,977,933 B at 22:29:31 UTC, up
2,828,024,834 B from 22:13:53 UTC. This is net project usage, not evidence
about the owner's deletion actions or physical quota reclamation; account
quota and garbage-collection status remain unavailable. A full read-only
train-state inventory now finds v1 versions v82-v141 and v2 v80-v140. Keeping
the newest two per job (v1 v140/v141; v2 v139/v140), 117 older versions are
alias-free and every `used_by()` check succeeded with zero dependencies:
v1 v82-v139 (58 versions) and v2 v80-v138 (59 versions). Their logical size
is 124,068,520,953 B. This exceeds the project meter, which itself shows why
logical artifact size cannot be treated as physical reclaim. No artifact was
deleted. The private mode-0600 [22:29 audit](wandb-live-train-state-delete-candidates-2026-10-19T2229Z.json)
contains the version-by-version checks. Local rolling backups now include v1
v141 / 71,000 and v2 v140 / 70,500; both comparison arms are being evaluated.

## 11:53 UTC current v4 artifact and storage audit — 2026-10-20

A fresh W&B GraphQL read returned project `storageBytes` of 76,659,882,751 B
(76.66 decimal GB). The organization subscription remains enabled with a
200-GB storage entitlement; the trailing 30-day cumulative daily average is
166,026,268,417 B (166.03 GB), about 33.97 GB below that measure. The project
meter increased 7,541,405,917 B from 10:40 UTC, while v4 training was actively
publishing checkpoints. This is net growth and cannot isolate concurrent
artifact deletions. These measurements do not report CoreWeave worker disk.
See the [11:53 storage snapshot](wandb-storage-entitlement-refresh-20261020T1153Z.json).

The live v4 `arc-sft-baseline-30e158011725-train-state-sft-resume` collection
has versions v0 through v74; its matching LoRA collection also has 75 visible
versions through v74. The latest checkpoint pair is v74 at 37,500 batches
(1,060,414,709-byte train-state and 117,843,308-byte LoRA). A read-only
dependency audit checked the 73 older **train-state** versions v0-v72: every
one is alias-free and `used_by()` returned zero dependencies. Their combined
logical size is 77,410,273,349 B (77.41 GB). Keep v73 and v74 as the two newest
recovery points. Per-version evidence is in the private, mode-0600 local audit
file at `ai/training/output/wandb_local_checkpoints_20261019/v4-train-state-cleanup-audit-v74.json`.

If cleanup is needed, the exact low-risk candidates are only v0-v72 in that
train-state collection. This discards older resume points; the newest two
remain remote and locally mirrored. Do not delete the v4 LoRA checkpoints or
dataset from this candidate set. The logical 77.41-GB sum is not guaranteed
physical reclaim because W&B does not expose deduplication or garbage
collection. No deletion was made by this audit.
