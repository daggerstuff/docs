# MentalChat16K origin binding validation — 2026-10-19

The existing exact-turn binding was independently revalidated against the
checked-in adapter and the public `ShenLab/MentalChat16K` snapshot pinned at
`5f60cd380cfc58f0f12d44892bed41ee3670a70a`. The source CSVs matched the
recorded byte counts and SHA-256 hashes. The validator recomputed adapter
projections, compared exact and normalized source-row locators with the private
sidecar, and checked candidate row hashes. It emitted aggregate metadata only.

| Candidate rows | Adapter-usable source rows | Exact sequence matches | Unique source row | Ambiguous source rows | Unmatched |
|---:|---:|---:|---:|---:|---:|
| 11,135 | 16,057 | 1,107 | 1,090 | 17 | 10,028 |

The normalized discovery tier remains 5,472 matches (5,452 unique, 20
ambiguous, 5,663 unmatched) and is not counted as exact. All 1,107 exact
matches have a full non-system turn sequence equal to an adapter-rendered
source row. The 17 ambiguous cases share exact turn sequences across multiple
upstream rows. Candidate system messages do not match the adapter-rendered
system messages, so they cannot distinguish those source rows. No additional
exact bindings were established.

Reproduce the hash-only check from the repository root with:

```sh
python3 scripts/training/validate_mentalchat16k_origin_binding.py
```

It reads the pinned candidate and private source files in memory, uses the
checked-in adapter, and prints JSON containing hashes, locators' aggregate
counts, and statuses. It does not print message content, write source copies,
or change the candidate, frozen payloads, or sidecars. The private source
directory is required at
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/`
with directory mode `0700` and sidecar mode `0600`.

These results establish technical row identity only. They do not establish
licensing, privacy, consent, participant permissions, clinical suitability, or
upstream data-use terms, and they do not authorize provider transfer or
training.
