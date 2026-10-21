# Empath and MentalChat16K source-row binding — 2026-10-19

Status: **technical source-row evidence established for a subset; no rights, privacy, clinical, or provider-transfer clearance.** Candidate and releases were not modified. No source text appears in this report or the private sidecars.

## Method

The pinned candidate (`190,139` rows; SHA-256 `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`) was compared against immutable public Hugging Face revisions. The project adapters' unchanged `convert_to_chatml()` methods were applied locally to the source rows. For matching, system messages were excluded because candidate system prompts differ from the current adapter render. A strict match requires the candidate's complete ordered non-system role/content sequence to occur contiguously and exactly (after adapter `.strip()` behavior) in a single upstream adapter-projected row. Every matching upstream locator is retained, including repeated/ambiguous matches. A separate normalized match tier collapses whitespace and case-folds content; it is a discovery aid and is **not counted as exact**.

| Family | Candidate rows | Adapter-usable source rows | Strict exact turn-sequence matches | Unique upstream row | Ambiguous upstream rows | No strict sequence match | Full non-system sequence equals source row |
|---|---:|---:|---:|---:|---:|---:|---:|
| Empath | 35,977 | 51,234 | 27,291 | 12,042 | 15,249 | 8,686 | 27,287 |
| MentalChat16K | 11,135 | 16,057 | 1,107 | 1,090 | 17 | 10,028 | 1,107 |

Thus strict support exists for 27,291 Empath rows and 1,107 MentalChat16K rows at the turn-content level. In 4 Empath matches, the exact candidate turn sequence is a contiguous sub-sequence rather than the entire source row's turn sequence. **None** of these matches proves that the whole candidate record, including its altered system prompt and non-message metadata, is an exact adapter-rendered record. The unmatched rows have no exact contiguous sequence in the pinned source revisions. They remain unbound by this check; the normalized tier must not be substituted for them.

| Family | Whitespace/case-normalized matches (discovery only) | Normalized unique / ambiguous / unmatched |
|---|---:|---|
| Empath | 32,817 | 15,319 / 17,498 / 3,160 |
| MentalChat16K | 5,472 | 5,452 / 20 / 5,663 |

## Pinned source and local hash evidence

| Family | Public repository revision | File | Bytes | SHA-256 |
|---|---|---|---:|---|
| Empath | [`Adapting/empathetic_dialogues_v2`](https://huggingface.co/datasets/Adapting/empathetic_dialogues_v2/tree/cb66212ad29e9d25cb8a93e2a024926a82e1c8bc) @ `cb66212ad29e9d25cb8a93e2a024926a82e1c8bc` | `train.csv` | 14,716,036 | `a2b72b3296e23413e7733f2a952abeec5c562cd47d853de61a37a6cfe15b34c9` |
| Empath | same | `dev.csv` (adapter split `validation`) | 2,222,715 | `28c63aa95c23389095f460a63e65dc0bade0d3d0bb6a7d0fbda3f84b3de47d06` |
| Empath | same | `test.csv` | 2,204,820 | `29400cb978224a87c39c551c4ad264e0c5e7c8498917ac6148ef36a95cc83a7b` |
| MentalChat16K | [`ShenLab/MentalChat16K`](https://huggingface.co/datasets/ShenLab/MentalChat16K/tree/5f60cd380cfc58f0f12d44892bed41ee3670a70a) @ `5f60cd380cfc58f0f12d44892bed41ee3670a70a` | `Interview_Data_6K.csv` | 13,580,450 | `7a2192299807ab2aa202a51dcc5b8b4cb35d1ee6b6eb38e9573be0aa51dc4992` |
| MentalChat16K | same | `Synthetic_Data_10K.csv` | 32,843,740 | `52273a1d682986013dd6ad077be8a79075bb1877a022cbb33d170527b7fdadea` |

Adapter source hashes: `empath_adapter.py` `0186f04ca326631bf0cdc99f42fa1711eede6a150194666a84ac6aaab7da10dc`; `mentalchat16k_adapter.py` `fc0e06c9d0cb1f4e1e428ec7c2ed2f21cadfe872fe253346e6019324495f7466`.

Private, ignored sidecars bind candidate row number + candidate line/message hashes to every upstream file/split/row reference. Modes are directory `0700`, files `0600`:

- Empath: `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/empath-candidate-upstream-rowrefs.jsonl`, SHA-256 `dbf078d972af54a6a6e8e4bd9d7ba6dde10c68821b569fac4b5da7623e07a5ab`.
- MentalChat16K: `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/mentalchat16k-candidate-upstream-rowrefs.jsonl`, SHA-256 `c156ece7929bd7e854900301b9ca4a070cd46662aef8e47de39fe6ae69ae1dac`.
- Private manifest: same directory, `bindings/manifest.json`, SHA-256 `0f9629364dd75c7e2cd113cc93393a60930d22ff070633a1e8e03d98763cb834`.

Validation parsed every sidecar row, checked candidate-family row totals and hashes, confirmed all files were mode `0600` under mode `0700` directories, and confirmed sidecars contain no message/text fields. Source text remains in the private local cache only.

## 2026-10-19 19:43 UTC v4 identity transfer and public-file verification

The five upstream files at the pinned revisions were downloaded to `/tmp` and
their byte counts and SHA-256 values matched the recorded source manifest
exactly. The original 190,139-row candidate rows were then joined to v4's
190,244-row internal manifest by complete candidate-row SHA-256. All 35,977
Empath and all 11,135 MentalChat16K rows are unchanged and present in v4, so
their existing row-reference evidence transfers without a similarity join.
This does not increase the number of source rows bound: Empath remains 12,042
unique + 15,249 ambiguous + 8,686 unmatched; MentalChat16K remains 1,090 unique
+ 17 ambiguous + 10,028 unmatched. No candidate, provider payload, or training
job was changed. The transfer covers only these unchanged source families and
does not resolve full-record adapter equality, rights, privacy, or eligibility.

## License and access caveats

**Empath:** The HF v2 card declares AFL-3.0 and describes this as a fine-tuned derivative of `facebook/empathetic_dialogues`; the original HF card separately declares CC-BY-NC-4.0. These declarations do not resolve the derivative's permission chain or reconcile the differing terms. Treat rights and provider-training scope as unresolved pending review of the exact pinned versions and original terms. Public access and exact row matches are evidence of technical identity only.

**MentalChat16K:** The pinned HF card declares MIT and its files are publicly accessible. The dataset paper describes a mixture of synthetic examples and anonymized coach/caregiver intervention transcripts. The public card's MIT tag alone does not document participant-level or upstream source permissions for those transcripts. Treat those data-use/privacy terms and provider scope as unresolved; do not interpret this binding as clearance.

