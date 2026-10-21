# Mitch-Hamidi BPD NLP origin binding — 2026-10-19

Status: **partial technical origin evidence; rights, privacy, consent, and provider-transfer clearance remain unresolved.** No candidate, release payload, or provider run was changed. No conversation text is included here.

The checked-in adapter at `ai/sourcing/dataset_adapters/mitch_hamidi_bpd_nlp_adapter.py` (SHA-256 `4d5c1e7c9f8ce66d625dc47c2f67013a4081b5a2ad58810710e691bcdd975a16`) was applied to the 14 CSV files under `Scraping_Reddit_for_Data/` in the adapter-declared public repository `mitch-hamidi/may-2024-mental-health-nlp`, pinned at commit `5867af435d9d667ae769058f893e3b35ea9f7496`. The join compares complete ordered non-system role/content sequences after the adapter's `.strip()` behavior. All matching upstream file/row locators are retained; repeated source rows remain ambiguous. System messages and non-message metadata are excluded, so this establishes turn-content correspondence, not complete rendered-record identity.

| v4 source-label rows | Unique upstream row | Ambiguous upstream rows | Unmatched |
|---:|---:|---:|---:|
| 13,890 | 8,000 | 313 | 5,577 |

By v4 split, exact sequence statuses are: train 7,216 unique / 286 ambiguous / 5,055 unmatched; validation 400 / 14 / 279; test 384 / 13 / 243. The family has 13,890 candidate content groups: 12,557 train, 693 validation, and 640 test. No group crosses splits. 8,313 groups have at least one exact source match; 5,577 groups are unmatched. These are candidate content-group counts; source-row ambiguity remains as shown above.

The pinned source files and SHA-256 values are:

| File | Bytes | SHA-256 |
|---|---:|---|
| `diagnosed_comments.csv` | 1,916,319 | `a1b83312296336b3e91afa88dc4bc41e698bc6328419f878c584ac2e29837e3a` |
| `diagnosed_search.csv` | 246,610 | `4a8b5e922b922e02548be6588c98058b6acc01140bbaa460a460e3e6474ec25c` |
| `drug_comments.csv` | 768,456 | `fd376482abd343e634ce7fc3341226f42ae37ca6d04eaa15219b2f972f9b203e` |
| `drug_search.csv` | 247,790 | `2cbbda0a51bff76bd4dbd2b347a02196910658a192a8fa6848695356c3e08d34` |
| `medicine_comments.csv` | 875,607 | `7841a52860765f0991d3cfd04da948114fe9f370ae3e19e001af1adbf4b8bdab` |
| `medicine_search.csv` | 232,700 | `4d7d3ec73377f1e502f23c01923e9cfd5d5eb2c10f6f453b5b38250e725360a0` |
| `prescribed_comments.csv` | 899,657 | `ed56792b52ed042b183b4c2fe1a8ea03e3aad77bd44359c32dbad832940c5ca9` |
| `prescribed_search.csv` | 190,455 | `6f3aeab138dd551e7d69f296581a3b934bf56acd59610625c1a359b70d6654d7` |
| `recovery_comments.csv` | 467,330 | `b7f758fc60c941711a93aed6f5fdeefc63190a3fa87a74d4f2bb1807d6d9df46` |
| `recovery_search.csv` | 294,454 | `b2244c940212ae3b6653d3e138f3c119bead5e0ab9f296336cda595d29e8e203a` |
| `therapy_comments.csv` | 729,406 | `2c24a652202fc2c5e29dc381ae570e501c16b92adec500077e3f8db1244d0243` |
| `therapy_search.csv` | 228,280 | `93bed7b451fb9c7fb5c22e5c233eee3e81b963ee6f16b44e1443fbc7005c8427` |
| `treatment_comments.csv` | 748,697 | `21a8b53c6f16209e933ad1db563b24b0117cf788f1d55dc83d9984e2bbf6e3cc` |
| `treatment_search.csv` | 307,828 | `593eeb09bf720d622825580a20e3b7116c70364ad7c8aea347cbe632ceabc95a` |

The v4 source candidate is SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349` (190,244 rows); its internal manifest is SHA-256 `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`. The family count matches the manifest's 13,890 rows. Hash-only candidate-to-upstream locators are in the ignored private sidecar `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/mitch-hamidi-bpd-nlp-v4-upstream-rowrefs.jsonl` (13,890 rows, 6,603,508 bytes, SHA-256 `7db68b2d2133dfc6a37154ee9ee4b040f0a5ec3db305d6aae0127d272ef549d8`, file mode `0600` beneath a `0700` directory). The machine-readable aggregate report is beside it, also mode `0600`.

The GitHub API identifies the repository as `mitch-hamidi/may-2024-mental-health-nlp` and reports license `NOASSERTION`; the repository provides Reddit-derived material. This match does not resolve Reddit platform terms, authors' rights, privacy, consent, clinical suitability, or permission for model training/provider transfer. Public access and technical correspondence do not constitute clearance.
