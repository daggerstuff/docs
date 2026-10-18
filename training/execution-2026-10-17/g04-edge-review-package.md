# G04 edge-branch local review package

Status: `draft_local_only`; upload gate is false. This package contains weighted
provider-format candidate JSONL files under the private recovery directory,
plus a metadata-only row manifest and render report. It is not approved, promoted, or uploaded.

The package contains 522 candidate rows from the first-party synthetic edge
branch after excluding 29 exact heldout-group rows. Its provisional grouped
split is 410 train rows / 72 validation rows / 40 test rows across 139 / 25 / 15
source groups. See `g04-release-manifest.json` for exact file hashes and the
`g03-edge-branch-diagnostics.json` for source, privacy, and overlap evidence.

The exact generation provider/model and applicable output-use/remote-training
terms remain unverified. The accompanying rights/privacy audit found no candidate
rows with exact signed rights plus privacy/consent clearance bound to rowrefs;
the 522-row branch separately needs input-seed review and content-bound human
review. `clinical_reviewed` is auto-set; this package supports
no clinical or production readiness claim. The W&B launcher must reject this
manifest while status is `draft_local_only` or `upload_gate` is false. The existing
exporter projection was verified for all 522 rows. The bounded W&B smoke completed
12 inference requests (5 successful, 7 HTTP 400); actual billable usage for rejected
requests is unknown. A later synthetic-only six-completion W&B diagnostic used a
separate $0.02 cap; its usage estimate was $0.00248575 and actual billing is
unknown. That cap is consumed; no further inference is authorized under it. These
inference requests were not dataset uploads or training jobs.
