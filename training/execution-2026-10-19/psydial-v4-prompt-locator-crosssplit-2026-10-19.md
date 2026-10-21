# PsyDial prompt and source-locator split audit — 2026-10-19

This hash-only audit reuses the existing pinned PsyDial source rowrefs and independently counts and hashes the current v4 candidate and internal manifest. Both contain 190,244 rows. Candidate SHA-256: `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`. Manifest SHA-256: `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

The `psydial` family has 892 rows: 817 train, 39 validation, and 36 test. Prompt context is the ordered non-system sequence before the final assistant target after per-turn stripping. Normalized context additionally uses NFKC, case-folding, and whitespace collapse.

| Prompt tier | Distinct hashes | Repeated hashes | Rows in repeated hashes | Hashes crossing splits | Rows touched across splits |
|---|---:|---:|---:|---:|---:|
| Exact | 885 | 4 | 11 | 1 | 5 |
| NFKC/case/whitespace normalized | 885 | 4 | 11 | 1 | 5 |

The crossing prompt hash touches two train rows, two validation rows, and one test row. All 892 v4 content groups remain split-disjoint.

The pinned source audit uses `qiuhuachuan/PsyDial-D101` at revision `c4c68ebc81dce63097620f13db365001786843bf` (file SHA-256 `fd238c62de8fcc56502438ded1da4f4bf392a612b20025b2918d51e19e1db5a3`). The adapter also declares D4 at `0ceef5ac19fb8174baa6be31ce1b2637711cb4c2` (file SHA-256 `29bfa723645f3c7213d00e34042c164545b27629487253fa6ebec97c7f3638b9`) and D1 at `0462554c9cdb12739d791566b75dd99ab2bb601f` (file SHA-256 `31918366fbf3ae25e3cd16dcd058004205e872965624943a3bafc3ee55f7b110`); those projections yielded zero usable rows under the adapter schema. The existing rowrefs report 891 exact unique candidate origins, one exact ambiguous candidate row (two source locators), zero normalized-only rows, and zero unmatched rows. Across all 893 referenced source locators, none is reused by multiple candidate rows or crosses splits.

The new private sidecar records candidate hashes, prompts hashes, split labels, binding statuses, and source repo/revision/file/record locators only: `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/psydial-v4-prompt-locator-crosssplit.jsonl` (892 rows, 690,828 bytes, SHA-256 `0c5953540196b222012814a8eceb6a3f0b6530312f71e01455ac1a3457888ba5`, mode `0600` under a mode `0700` directory). The private aggregate report is beside it, also mode `0600`.

HF card metadata reports Apache-2.0, but this technical audit does not settle attribution or incorporated PsyQA source terms, privacy, consent, clinical suitability, or provider-transfer permission. No corpus, release payload, or provider job changed.
