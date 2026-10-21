# Reddit Mental Health Posts origin binding — 2026-10-19

Status: **partial technical origin evidence; rights, privacy, consent, and provider-transfer clearance remain unresolved.** No candidate, release payload, or provider run was changed. No post text appears in this report.

The checked-in adapter `ai/sourcing/dataset_adapters/reddit_mental_health_posts_adapter.py` (SHA-256 `3e66610594fc48e1137e02f45907a5f584b4c2fdcc1bab4131531060e497016e`) was applied to the five files declared by the adapter in the public Hugging Face dataset `solomonk/reddit_mental_health_posts`, pinned at revision `48c23354c088c4273b260a877dafa424e1c6cc95`. The projection follows the adapter's CSV ordering, body/title selection, subreddit label mapping, whitespace stripping, and normalized-text deduplication. Matching uses the complete ordered non-system role/content sequence and exact SHA-256 comparison. System messages and non-message metadata are excluded, so this is turn-content correspondence rather than complete rendered-record identity.

| v4 source-label rows | Unique upstream projected row | Ambiguous upstream rows | Unmatched |
|---:|---:|---:|---:|
| 30,444 | 10,693 | 0 | 19,751 |

By split, exact matches / unmatched are: train 9,624 / 17,749; validation 532 / 1,049; test 537 / 953. The pinned files contain 151,288 raw rows; adapter deduplication yields 88,223 projected records. Candidate split-group checks found 30,379 content groups, zero groups crossing splits, 10,672 groups with an exact match, and 19,707 groups without one. No matched upstream projected row was assigned to candidate rows in multiple splits. Unmatched rows remain unbound by this comparison.

| File | Bytes | SHA-256 |
|---|---:|---|
| `adhd.csv` | 29,607,487 | `629474a0a50fb08720df9852b68d561a60e012afa05741d7a490f656e516992c` |
| `aspergers.csv` | 17,311,052 | `b60775c2340aeffd5a20a33867e4a32a9a3de127bae7949f3b2c171cc199cdb5` |
| `depression.csv` | 17,176,460 | `5ffda120f9ec2061c2348e03afb07d7704bd326778f795ff39be4e437ca48987` |
| `ocd.csv` | 29,818,604 | `b68da65fd2d82396c4191232b39ae6563d520047681d3a9cb7dd2a3524a22cc1` |
| `ptsd.csv` | 20,085,730 | `43665b27725ee9ea772a81ea2c0ea231c1a95f5fd436671d72458eb7e32115e9` |

The v4 candidate SHA-256 is `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349` (190,244 rows); its internal manifest SHA-256 is `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`. The v4 source-label count is 30,444. Private hash-only row references are in the ignored sidecar `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/reddit-mental-health-posts-v4-upstream-rowrefs.jsonl` (30,444 rows, 13,138,649 bytes, SHA-256 `80ceecbf946d73a0d23c13df7abb534e5e976c64609ff6ca951fe9bd663a397d`, mode `0600` beneath a mode `0700` directory). Its machine-readable aggregate report is stored beside it with mode `0600`.

The HF API returned no license value for the pinned repository. These are Reddit-derived posts; access to the public files and technical matches do not establish Reddit platform-term compliance, author rights, privacy, consent, clinical suitability, or model-training/provider-transfer permission. No clearance is inferred.
