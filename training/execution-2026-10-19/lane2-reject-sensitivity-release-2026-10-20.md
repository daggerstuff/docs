# Lane-2 reject sensitivity dataset — 2026-10-20

Built a separate private, local-only sensitivity variant from the immutable W&B v4 release by removing rows associated with the latest lane-2 `reject` decisions. This directly tests how those ARC-ID joins affect the experiment while preserving the original full-corpus release as the baseline. The review artifacts still do not identify the exact revision reviewers saw, so this is an ablation, not an adjudicated clean corpus.

The variant retains 190,170 of 190,244 rows and excludes 74 rows: {'train': 66, 'validation': 5, 'test': 3}. Its train/validation/test payloads were aligned row-for-row to the source candidate by exact candidate row hashes and canonical message hashes. All split content-group intersections are zero.

The release is mode 0700 with payload/manifests mode 0600. Its manifest sets `upload_gate=false`; no provider upload or job was made. Files are under `ai/data/curated/recovery/gold-20261017/wandb-full-corpus-lane2-reject-sensitivity-20261020-v1/`.
