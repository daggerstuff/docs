## Master Training Gap Closure Plan

### Scope

- Align Stage 1 workflow with the master multi-stage training epic.
- Enforce stage ratio governance in code (not only docs).
- Track unfinished epic items as explicit execution tasks.
- Wire every remaining item into Asana with clear parent-child dependencies,
  artifact links, and completion evidence.

### Completed Today

- Located and reviewed Stage 1 notebook workflow in [ai/lab/Stage1_Training_Notebook.ipynb](ai/lab/Stage1_Training_Notebook.ipynb).
- Compared against
  [ai/training/ready_packages/MASTER_TRAINING_EPIC.md](ai/training/ready_packages/MASTER_TRAINING_EPIC.md)
  and
  [ai/pipelines/orchestrator/MasterTrainingPlan.md](ai/pipelines/orchestrator/MasterTrainingPlan.md).
- Implemented manifest-driven stage distribution loading and final stage drift
  validation in
  [ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py](ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py).
- Implemented manifest-driven stage quality profile enforcement
  (empathy/safety/bias + stage-specific metadata gates) in
  [ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py](ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py).
- Implemented Stage 3/4 required artifact preflight validation in
  [ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py](ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py).
- Implemented aggregate and per-stage train/val/test split artifact export in
  [ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py](ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py).
- Implemented run checklist sync output + optional webhook emission for
  tracker integration (Asana/Jira bridge) in
  [ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py](ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py).

### Source of Truth Links

- Stage implementation context:
  [ai/lab/Stage1_Training_Notebook.ipynb](ai/lab/Stage1_Training_Notebook.ipynb)
- Epic baseline:
  [ai/training/ready_packages/MASTER_TRAINING_EPIC.md](ai/training/ready_packages/MASTER_TRAINING_EPIC.md)
- Orchestrator baseline:
  [ai/pipelines/orchestrator/MasterTrainingPlan.md](ai/pipelines/orchestrator/MasterTrainingPlan.md)
- Pipeline implementation:
  [ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py](ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py)
- Policy manifest:
  [ai/data/training_policy_manifest.json](ai/data/training_policy_manifest.json)
- Checklist output for PM sync:
  [ai/lightning/training_run_checklist.json](ai/lightning/training_run_checklist.json)

### Asana Wiring (End-to-End)

Use one Asana project for this plan and connect every task to both code and docs.

Recommended project name:
`Master Training Gap Closure - 2026-03-17`

Recommended custom fields:

- `Task Key` (text; values like `MTGC-01`)
- `Stage` (enum: `cross-stage`, `stage1`, `stage2`, `stage3`, `stage4`)
- `Track` (enum: `pipeline`, `quality`, `artifacts`, `ops`, `release`)
- `Status` (enum: `todo`, `in_progress`, `blocked`, `ready_for_review`, `done`)
- `Risk` (enum: `low`, `medium`, `high`)
- `Blocking` (multi-select or text)
- `Artifacts` (text link list)
- `Source Plan` (URL to this plan)

Recommended sections:

- `00 Intake`
- `10 Governance and Ratios`
- `20 Stage 3 + Stage 4 Readiness`
- `30 Split and Manifest Integrity`
- `40 Ops and Tracker Sync`
- `90 Verification and Signoff`

Task link template:

- Asana task URL:
  `https://app.asana.com/0/<PROJECT_GID>/<TASK_GID>/f`
- Add these links in every task description:
  - `Plan:` this file
  - `Code:` relevant implementation file(s)
  - `Spec:` master epic and orchestrator plan
  - `Evidence:` CI run, report, or generated artifact

### Asana Task Graph (Expanded and Linked)

<!-- markdownlint-disable MD013 -->

| Task Key | Asana Task Title | Depends On | Blocks | Code / Doc Links | Definition of Done |
| --- | --- | --- | --- | --- | --- |
| MTGC-00 | Create Asana project scaffold and custom fields | - | MTGC-01..13 | This plan | Project exists with sections, custom fields, owner, due dates |
| MTGC-01 | Enforce stage sampling parity and tolerance | MTGC-00 | MTGC-02, MTGC-08 | `integrated_training_pipeline.py`, `training_policy_manifest.json` | Ratio checks hard-fail when drift exceeds threshold without waiver |
| MTGC-02 | Add CI manifest and stage split verification | MTGC-01 | MTGC-11 | `integrated_training_pipeline.py`, CI workflow target | CI asserts stage counts, drift metrics, split completeness |
| MTGC-03 | Implement Stage 3 crisis override quality validator wiring | MTGC-00 | MTGC-06, MTGC-11 | `integrated_training_pipeline.py`, `MasterTrainingPlan.md` | Stage 3 lenient safety mode and override counters exported |
| MTGC-04 | Implement Stage 4 voice signature and persona gates | MTGC-00 | MTGC-06, MTGC-11 | `integrated_training_pipeline.py`, Stage 4 metadata schema refs | Stage 4 rejects records missing required voice/persona metadata |
| MTGC-05 | Ingest edge/safety DPO scenario bank into Stage 3 | MTGC-03 | MTGC-06 | edge corpus + manifest entries | Stage 3 manifest includes DPO scenario bank sources and counts |
| MTGC-06 | Export and validate stage-level train/val/test artifacts | MTGC-02, MTGC-03, MTGC-04, MTGC-05 | MTGC-11 | split artifact outputs + manifest | Per-stage and aggregate splits validated and published |
| MTGC-07 | Add release manifest contract checks for downstream loaders | MTGC-02 | MTGC-11 | release manifest loaders + this plan next-step #1 | Downstream tooling consumes new schema without regressions |
| MTGC-08 | Implement waiver mechanism for justified stage drift | MTGC-01 | MTGC-02 | `integrated_training_pipeline.py` + policy manifest | Drift waiver is explicit, auditable, and time-bound |
| MTGC-09 | Build authenticated Asana status updater from run checklist | MTGC-00 | MTGC-10, MTGC-12 | `training_run_checklist.json`, tracker bridge code path | Checklist keys map to Asana task state transitions |
| MTGC-10 | Map checklist keys to task keys and ownership | MTGC-09 | MTGC-12 | this plan + checklist schema | Mapping table committed and validated with dry-run sync |
| MTGC-11 | Generate integrated stage health report artifact | MTGC-02, MTGC-03, MTGC-04, MTGC-06, MTGC-07 | MTGC-13 | report output from integrated pipeline | Report includes counts, drift, validator pass/fail, blockers |
| MTGC-12 | Wire ops freshness checks (inventory, prompt mirror, voice export) | MTGC-09, MTGC-10 | MTGC-13 | run checklist + ops scripts | Freshness values are emitted and reflected in Asana statuses |
| MTGC-13 | Final signoff and closure pack | MTGC-11, MTGC-12 | - | this plan + final report + Asana board | All success criteria and evidence links are complete |

### Traceability Matrix (Gap Closure)

| Gap / Epic Item | Asana Tasks | Implementation Anchor |
| --- | --- | --- |
| Stage sampling parity and tolerance enforcement | MTGC-01, MTGC-08 | `integrated_training_pipeline.py`, `training_policy_manifest.json` |
| Stage-specific validators + crisis override policy | MTGC-03, MTGC-04 | `integrated_training_pipeline.py`, `MasterTrainingPlan.md` |
| Edge/safety DPO scenario bank in Stage 3 | MTGC-05 | Stage 3 manifest entries and ingestion path |
| Voice signature + persona gate for Stage 4 | MTGC-04 | Stage 4 metadata checks in orchestrator |
| Stage-level and aggregate split verification | MTGC-02, MTGC-06, MTGC-07 | split artifacts + release manifest contract |
| Ops checklist completion tracking | MTGC-09, MTGC-10, MTGC-12 | `training_run_checklist.json` + tracker bridge |

<!-- markdownlint-enable MD013 -->

### Unfinished Epic Items (Execution Queue)

- Asana scaffold task (MTGC-00) and dependency graph materialization remain open.
- Edge/safety DPO scenario bank ingestion into Stage 3 (MTGC-05) remains open.
- Release manifest downstream contract hardening (MTGC-07) remains open.
- Explicit drift waiver authoring workflow finalization (MTGC-08) remains open.

### Execution Progress (Live)

- [x] MTGC-01 Enforce stage sampling parity and tolerance in code.
  - Added stage-specific drift tolerance resolution with manifest-backed waiver support.
  - Drift validation now records tolerance and waiver usage per stage.
- [x] MTGC-03 Wire Stage 3 crisis override policy with measurable output.
  - Stage quality enforcement now counts crisis overrides by stage.
  - Failure reason aggregation added for policy observability.
- [x] MTGC-04 Tighten Stage 4 voice/persona gate reporting.
  - Voice/persona gate failures are now captured in stage-level enforcement summaries.
  - Report output includes stage policy enforcement metrics for release review.
- [x] MTGC-02 CI manifest and split verification wiring.
  - Added artifact verification script for checklist drift checks, stage manifest integrity, and split completeness.
  - Added dedicated CI workflow gate for training artifact verification.
- [x] MTGC-06 Stage-level split validation and publish checks.
  - Updated orchestrator split/manifest writers to emit aggregate and per-stage
    artifacts for all configured stages, including zero-sample stages.
  - Refreshed pipeline outputs and validated with `verify_stage_manifest_and_splits.py --allow-empty`.
- [x] MTGC-09 MTGC-10 MTGC-12 checklist to Asana state integration.
  - Added checklist `ops_freshness` payload with inventory/prompt-mirror/voice-export freshness checks.
  - Added persisted MTGC task-key -> Asana GID mapping artifact and authenticated transition result artifact.
  - Added checklist-signal-to-task-key transition logic with Asana `completed` updates and story audit notes.
- [x] MTGC-11 integrated stage health report artifact.
  - Added `integrated_stage_health_report.json` generation from pipeline report metrics.
  - Added blocker derivation (drift breaches, validator failures, split readiness, and pipeline errors).
  - Added per-stage validator pass/fail summary with failure reason rollups.
- [x] MTGC-13 closure pack artifact generation.
  - Added `mtgc_closure_pack.json` generation with MTGC-13 success-criteria pass/fail status.
  - Added evidence artifact path bundle (checklist, stage health report, manifest, Asana mapping, Asana transitions).
  - Added overall closure `overall_pass` flag to support final signoff automation.
- [x] MTGC-07 release manifest downstream contract checks.
  - Hardened `verify_stage_manifest_and_splits.py` with manifest contract
    validation for `generated_at`, `target`, and `available` fields.
  - Added aggregate and per-stage split line-count parity checks against
    checklist `split_counts` contract.
  - Re-verified with `verify_stage_manifest_and_splits.py --allow-empty`.

### Self-Heal Checkpoints

- Checkpoint A complete:
  - Performed targeted compile validation of orchestrator pipeline after edits.
  - Confirmed no static errors on modified pipeline file.
  - No temporary scripts or one-off files introduced in this batch.
- Checkpoint B complete:
  - Executed new artifact verifier in permissive mode to surface current dataset/report gaps.
  - Confirmed gate behavior correctly flags missing split and stage artifacts.
  - No cleanup debt created; only durable script/workflow assets were added.
- Checkpoint C complete:
  - Re-ran integrated pipeline and regenerated stage/split artifacts after MTGC-06 hardening.
  - Confirmed `verify_stage_manifest_and_splits.py --allow-empty` passes on refreshed artifacts.
  - Confirmed strict execution script still hard-fails on empty aggregate outputs, preserving release safety.

### Next Steps (Asana-First Execution Order)

1. Create Asana scaffold task MTGC-00 and instantiate MTGC-01..13 with dependencies.
2. Link each Asana task to implementation anchors and add `Task Key` in the first line of each description.
3. First implementation batch complete: MTGC-01, MTGC-03, MTGC-04.
4. Execute MTGC-02 and MTGC-06 with CI and artifact verification.
5. [x] Integrate MTGC-09 + MTGC-10 + MTGC-12 so checklist output directly drives tracker states.
6. [x] Complete MTGC-11 report generation and complete MTGC-13 closure pack.
7. [x] Proceed with MTGC-07 downstream manifest contract verification hardening.
8. [ ] Proceed with MTGC-00 Asana scaffold dependency materialization.

### Success Criteria

- Stage share drift for each stage is <= 0.02 unless explicitly waived.
- Manifest and report include final stage counts and drift metrics.
- Stage 3 and Stage 4 required inputs are validated before training launch.
- Run output includes both aggregate and per-stage split artifacts.
- Asana project shows full dependency graph with no orphan tasks.
- Every task has code/doc links and verification evidence before closure.

### Tight Integration Rules (Do Not Skip)

- Every code PR references at least one `MTGC-*` task key.
- Every `MTGC-*` task includes links to:
  - this plan,
  - changed code path,
  - generated evidence artifact.
- No task may move to `done` until linked evidence exists.
- If drift waiver is used, include waiver reason, approver, and expiry in task comments and manifest metadata.
