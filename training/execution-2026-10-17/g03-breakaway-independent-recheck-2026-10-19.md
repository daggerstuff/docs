# G03 522-row breakaway independent recheck (2026-10-19)

Read-only integrity recheck of `g03-edge-synthetic-research-522-20261019-v1`. No source dataset or package payload was modified.

## Verified

- The active candidate is 190,139 JSONL rows and its current SHA-256 is `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`, matching the freeze manifest.
- The post-holdout row-reference file contains 522 rows and matches SHA-256 `a5294068c241eb48007c6c33036da0c033a16198094c6e83f307eeaabf443a7a`. All 522 one-based row references resolve to the pinned candidate; raw source-line SHA-256 and canonical `messages` SHA-256 both match for every row. The nested provenance `arc_id` and `session_n` also match each reference.
- All 522 references resolve their recorded seed-input artifact paths to current files with matching hashes. Every reference is `edge_cases` with a `written` seed-map status. Current hashes for the two accepted-seed files, seed map, and two generation/consolidation code files match the historical evidence in `g03-generated-source-origin.json` and the breakaway review. The source-class label `edge_cases` is a normalized lineage category; candidate nested provenance uses `clinical_edge_case`.
- The held-out exclusion file has 29 rows and matches its recorded hash. Retained and excluded row numbers do not overlap. The 522 retained rows split into 410/72/40 rows and 139/25/15 groups. Pairwise group intersections between splits are zero, and no retained group occurs in the held-out exclusions.
- All three packaged JSONL files match their recorded byte sizes and SHA-256 digests. Comparing source messages to packaged messages confirms exact body/role projection for all 522 rows; the package assigns weight 0 to user messages and weight 1 to assistant messages for all rows. The internal manifest also matches its recorded byte size and digest.

## What this establishes and what remains open

The frozen package has reproducible technical row lineage from the current candidate through seed references, exact message projection, and group-disjoint splits. It supports keeping the 522-row package as a local research artifact.

It does not establish the historical LLM provider or model used to generate the accepted seed artifacts, the provider's output-use or remote-training terms, or any independent clinical review, comprehensive de-identification, or production/clinical readiness. Existing source-origin records show the edge prompt taxonomy is locally authored, but the subsequent ARC generation backend/model was environment-selected and is not present in accepted-row provenance. The targeted local run-history search is already recorded in `g03-edge-case-source-provenance-decision.md`, `g03-historical-run-provenance-followup.md`, and `g03-generated-source-origin.json`; no current local artifact in this recheck closes that gap. These gaps cannot be repaired by changing lineage metadata. A contemporaneous generation receipt or provider-side job record is needed for provider/model and terms; separate qualified clinical/privacy review would be needed for those claims. Keep the upload gate closed for this package pending that evidence.

## Reproduction

From the repository root:

```sh
sha256sum \
  ai/data/curated/recovery/gold-20261017/train_master_gold.recovered_candidate.jsonl \
  docs/training/execution-2026-10-17/g03-edge-case-post-holdout-rowrefs.jsonl \
  docs/training/execution-2026-10-17/g03-edge-case-heldout-exclusions.jsonl \
  ai/data/curated/recovery/gold-20261017/g03-edge-review-package-20261017T1626Z/train.jsonl \
  ai/data/curated/recovery/gold-20261017/g03-edge-review-package-20261017T1626Z/validation.jsonl \
  ai/data/curated/recovery/gold-20261017/g03-edge-review-package-20261017T1626Z/test.jsonl
wc -l ai/data/curated/recovery/gold-20261017/train_master_gold.recovered_candidate.jsonl \
  docs/training/execution-2026-10-17/g03-edge-case-post-holdout-rowrefs.jsonl \
  docs/training/execution-2026-10-17/g03-edge-case-heldout-exclusions.jsonl
```

The relational checks were independently recomputed with `uv run python` using only the candidate, row-reference/exclusion JSONL, frozen manifest, and packaged JSONL: resolve each `candidate_row_number_1based`, hash the raw candidate line and canonical sorted compact `messages` JSON, compare nested ARC/session identifiers, aggregate `seed_group_sha256` by `provisional_split`, compare retained groups against exclusions, then compare each split's source messages with its package row and validate the role weights. Results: 522/522 for both row hashes and message projections; 522/522 nested ARC/session bindings; 0 row overlap; zero group intersections; all 522 package projections/weight rules pass.
