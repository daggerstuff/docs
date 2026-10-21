# Mitch Hamidi BPD NLP v4 prompt and locator split audit — 2026-10-20

This hash-only audit adds prompt and source-locator split checks for the 13,890-row `mitch_hamidi_bpd_nlp` family. It reuses existing pinned source rowrefs and does not reopen or emit source text. The checked-in adapter SHA-256 is `4d5c1e7c9f8ce66d625dc47c2f67013a4081b5a2ad58810710e691bcdd975a16`; the declared repository `mitch-hamidi/may-2024-mental-health-nlp` is pinned at commit `5867af435d9d667ae769058f893e3b35ea9f7496`.

The candidate is 190,244 rows with SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`; the v4 internal manifest is 190,244 rows with SHA-256 `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`. Family status remains 8,000 exact unique, 313 ambiguous, and 5,577 unmatched. The prior binding retains all duplicate source alternatives rather than choosing one.

| Hash key | Distinct hashes | Repeated hashes | Cross-split hashes | Rows touched across splits |
|---|---:|---:|---:|---:|
| Exact ordered non-system input prompt | 2,344 | 964 | 451 | 10,323 |
| NFKC, casefolded, whitespace-collapsed prompt | 2,344 | 964 | 451 | 10,323 |
| Candidate content groups | 13,890 | 0 | 0 | 0 |
| Candidate record hashes | 13,890 | 0 | 0 | 0 |

The 8,803 retained upstream locator references (from rows with source matches, including ambiguity alternatives) resolve to 8,803 distinct file/row/source-hash locators. No locator is reused or crosses candidate splits. This means the observed cross-split prompt overlap does not coincide with cross-split reuse of a bound upstream row locator; the 5,577 unmatched rows remain without source-row evidence. The pinned source-file hashes and origin-matching method are recorded in the existing [origin-binding report](mitch-hamidi-bpd-nlp-v4-origin-binding-2026-10-19.md).

The ignored row-level sidecar is `ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/mitch-hamidi-bpd-nlp-v4-prompt-locator-crosssplit.jsonl` (13,890 rows, 8,741,569 bytes, SHA-256 `3a66fd338f2c03973c2dfafd5d5dc39eab2919c04413ee29a1967c881bc2ab65`, mode `0600` beneath a mode `0700` directory). It contains hashes, splits, statuses, and hashed locators only.

This is technical lineage evidence. The candidate's curation-time source revision remains unverified. The source consists of Reddit-derived content; platform terms, author rights, privacy, consent, clinical suitability, training eligibility, and provider-transfer permission remain unresolved. No rights or privacy clearance is inferred, and no dataset, release, or provider run changed.
