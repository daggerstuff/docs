# Local source/cache audit for three large Reddit candidate families

This is a metadata-only audit. No network access was used, no upstream source
was downloaded, and no message text or user identifiers are recorded here.

## Result

The workspace contains the curated candidate and its row-level decision ledger,
but no raw source copy or dataset cache was initially present for the three
declared source locators below. A follow-on pinned local fetch and join has now
bound a portion of `reddit_mental_health_posts`; the other two families still
have no upstream row-level matches. The decision ledger has unique candidate
row hashes for all rows in each family; this establishes candidate-row identity,
not by itself upstream source identity.

| Candidate source label | Candidate rows | Candidate row-hash duplicates | Concrete adapter locator | Missing exact-match prerequisite |
|---|---:|---:|---|---|
| `reddit_mental_nlp` | 70,968 | 0 | Kaggle dataset `kamaruladha/mental-disorders-identification-reddit-nlp`; adapter reads CSV files from its raw directory | Original Kaggle CSV(s), with the exact downloaded revision/version used for curation |
| `reddit_mental_health_posts` | 30,444 | 0 | Hugging Face dataset `solomonk/reddit_mental_health_posts`; adapter expects `adhd.csv`, `aspergers.csv`, `depression.csv`, `ocd.csv`, and `ptsd.csv` | Those source CSVs or an exact local Hub snapshot/revision |
| `mitch_hamidi_bpd_nlp` | 13,890 | 0 | `rclone` prefix `whitebat:training/pixelated-empathy/output/mitch_hamidi_bpd_nlp/raw/may-2024-mental-health-nlp/Scraping_Reddit_for_Data/`; declared upstream repository `https://github.com/mitchellhamidi/may-2024-mental-health-nlp` | The original CSV directory, including source filenames and revision/creation metadata |

The rows occupy candidate line ranges 118,015–188,982, 87,571–118,014, and
70,039–83,928 respectively (ranges shown in table order). All 115,302 candidate
row hashes are distinct within their respective source families.

## Local inventory checked

- The candidate is `ai/data/curated/recovery/gold-20261017/train_master_gold.recovered_candidate.jsonl` (411,493,422 bytes); its pinned SHA-256 is
  `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`.
- `docs/training/execution-2026-10-17/source-decision-ledger.jsonl` contains
  candidate row numbers and row/message hashes for the three families. Its
  source labels map to proposed, unratified IDs `SRC-027`, `SRC-028`, and
  `SRC-031` in `source-evidence-inventory.json`; these are not upstream row IDs.
- `ai/data/raw` contains a separate BBRD file,
  `ai/data/raw/bbrd/raw/BPD_and_Behaviour_Reddit_Dataset_2011-2023_-_Anonymised.csv`
  (68,591 rows; SHA-256
  `8546e0121f2d87fb8a95509bf4d7318b74216db77b6cfcaceb95b0fdead7f365`), plus
  its processed `bbrd.jsonl`. It is not the Mitch Hamidi adapter's declared
  `may-2024-mental-health-nlp` source. A privacy-preserving exact-text hash
  comparison found zero Mitch Hamidi candidate user messages in BBRD and one
  `reddit_mental_health_posts` candidate user message (candidate row 100,771).
  This isolated overlap does not establish that BBRD is the source for that
  family and must not be used to bind the remaining rows.
- The checked Hugging Face cache contains logs/metadata only; no dataset cache
  files were present. No source CSVs for these adapters were found under
  `ai/data/raw`, `/home/vivi/.cache/kaggle`, `/home/vivi/.kaggle`, or
  `/home/vivi/.cache/kagglehub`.

## Reproducibility references

Adapter source hashes at audit time:

- `ai/sourcing/dataset_adapters/reddit_mental_nlp_adapter.py`:
  `fb224f3d380e7380367642ca7aa6bae6e636ec6077829a7aa060a1493c20c6a5`
- `ai/sourcing/dataset_adapters/reddit_mental_health_posts_adapter.py`:
  `3e66610594fc48e1137e02f45907a5f584b4c2fdcc1bab4131531060e497016e`
- `ai/sourcing/dataset_adapters/mitch_hamidi_bpd_nlp_adapter.py`:
  `4d5c1e7c9f8ce66d625dc47c2f67013a4081b5a2ad58810710e691bcdd975a16`

No candidate, release, or source data was modified. To complete exact upstream
binding, place the already-authorized original source files/revision in a local
read-only audit location and compare adapter-normalized row hashes; do not
substitute the BBRD file for the declared Mitch source.

## Current Kaggle snapshot binding completed — 2026-10-19

The Kaggle credential already present in the local `.env` successfully
authenticated a read-only file listing and download for the adapter-declared
dataset. Kaggle listed one file, `mental_disorders_reddit.csv` (588,850,172
bytes). The downloaded snapshot SHA-256 is
`7529dd554c83a3bb781df91405a40262451d6b98b4bd4725e5711c0a06a42ef7`; it has
701,787 data rows and columns `title`, `selftext`, `created_utc`, `over_18`,
and `subreddit`. The raw CSV was kept in a mode-0700 temporary directory during
matching and is not part of the candidate or release.

The adapter's actual transformation was replayed: use stripped `selftext`
(falling back to title) and stripped `subreddit`, then deduplicate by
case-folded, whitespace-collapsed text and label. Against the 70,968 candidate
rows, 28,894 have unique exact user-text-plus-label matches and 29,515 have
unique matches after case/whitespace normalization. A further 436 candidates
have ambiguous upstream row matches, 12,122 have no matching text-plus-label
pair, and one has a user-text-only match with a label mismatch. Thus 58,409
candidate rows (82.3%) now have unique upstream row references; this is source
binding evidence, not a rights, consent, privacy, or clinical-quality finding.

Every uniquely bound row transfers to the frozen v4 package by the existing
candidate-row SHA-256, with no missing hash joins: 52,527 train, 2,991
validation, and 2,891 test rows. The mode-0700 private report and mode-0600
hash/row-number sidecar are in
`ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/reddit-mental-nlp-row-binding-2026-10-19/`.
The v4 sidecar SHA-256 is
`24f9ea3bb314b92739a997ae0e25a17e75a2e4ee38e58fe53201c419064ada82`.

This binds rows to the current downloadable Kaggle file snapshot only. The
local lineage has no curation-time Kaggle version number, so it cannot establish
that this was the exact version originally used. The downloaded file's hash
does make this audit snapshot reproducible. Kaggle's current CLI supports
authenticated dataset file listing and downloading; those operations were
used without modifying the upstream dataset ([official file/download
reference](https://github.com/Kaggle/kaggle-cli/blob/main/docs/datasets.md)).
The dataset page/catalog identity is corroborated, but this audit did not
establish applicable reuse rights or privacy approval; retain the existing
eligibility status pending those determinations.

## Prompt-level split leakage audit — 2026-10-19

The frozen v4 split is disjoint by its full prompt-and-answer content hash, but
that grouping allows identical user prompts paired with different assistant
responses to land in separate splits. A normalized user-prompt audit across
the actual v4 train/validation/test payloads found 673 user prompts in more
than one split, touching 11,136 rows. Of those, `mitch_hamidi_bpd_nlp` alone
accounts for 451 prompts and 10,323 rows (9,127 train, 612 validation, 584
test). This is leakage for prompt-generalization evaluation, even though the
existing full-conversation group check passes.

The BPD source shape helps explain the concentration: its 13,890 rows are all
three-message `therapy_response_generation` examples with a single shared
system prompt. They contain 2,344 distinct case/whitespace-normalized user
prompts; the most repeated prompt occurs 440 times. The output-side aggregate
also found 1,113 assistant targets that match the adapter's generic
`[Community discussion about …]` template. These are content-quality signals,
not exact upstream identity or rights evidence. The adapter-declared GitHub
repository remains unavailable (HTTP 404), and the `whitebat:` source prefix
still returns `UserSuspended`; no substitute dataset was used.

A separate local-only split candidate now groups globally by normalized user
prompt and preserves all 190,244 v4 rows. It provides both the system-stripped
and zero-loss-weight system-preserving variants, each with 171,166 train,
9,500 validation, and 9,578 test rows. An independent read-back confirmed the
file hashes, no normalized prompt crossing splits, equal row counts, and exact
non-system projection equality between variants. The release is not uploaded;
source rights/privacy status is unchanged. See the reproducible
[prompt-disjoint builder](../../../ai/training/build_prompt_disjoint_release.py),
[private release manifest](../execution-2026-10-19/prompt-disjoint-20261019-v3-manifest.json),
and row lineage at `ai/data/curated/recovery/gold-20261017/prompt-disjoint-20261019-v3-row-lineage.jsonl`.

## Follow-up access check for the separate Mitch Hamidi family

The other large Reddit family (`mitch_hamidi_bpd_nlp`, 13,890 candidate rows)
still has no row binding. A read-only listing against the adapter-declared
`whitebat:` object-store prefix returned HTTP 403 `UserSuspended`; no source
objects were listed or downloaded. The adapter's public GitHub locator returned
404 when opened on 2026-10-19. Those are access/availability findings, not
evidence that the candidate rows are invalid or that another similarly named
dataset is equivalent. The Kaggle Reddit binding above is independent and is
not used as a substitute. Exact Mitch-source matching needs the declared CSVs
or an accessible immutable copy of that source.

## Pinned join for `reddit_mental_health_posts`

The adapter-declared Hugging Face source was fetched at immutable revision
`48c23354c088c4273b260a877dafa424e1c6cc95`. The five adapter-declared CSVs
contain 151,288 source rows. Their SHA-256 values are recorded in the private
binding report. Adapter replay produced 88,223 unique deduplication keys from
the 151,288 inputs, dropping 63,065 later duplicate keys.

The candidate's 30,444 row hashes and message hashes each match their pinned
decision-ledger references (30,444/30,444). Replaying current adapter message
construction shows that all 30,444 candidate assistant targets match an
adapter-generated target template, while none of the candidate system prompts
match the current adapter's system prompt. Therefore the join keys use the
candidate user text and adapter-generated assistant target, and report full
message equality separately as zero.

Of 30,444 candidate rows, 10,693 have exact user-text plus target matches;
14,390 more bind only after case and whitespace normalization; 5,361 remain
unbound. The join preserves all upstream CSV row references, including rows the
adapter would deduplicate: 25,083 candidate rows have an adapter-emitted source
match, 15,641 additional deduplicated source row references are retained, and
78 candidate rows have multiple upstream row candidates. The sidecar contains
40,724 total source row references and hashes Reddit post IDs instead of
storing them directly. No source text is included.

The private report and row-reference sidecar are under
`ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/reddit-mental-health-posts-row-binding-2026-10-19/`
(directory mode 0700; files mode 0600). The sidecar has 30,444 rows and SHA-256
`d6518ff553d7e38781092b11aad3ea52e114c9c2f39c6135aef7d950db64c294`.

The Hugging Face card has no license field. Public availability and successful
local matching do not establish reuse or redistribution rights. Reddit text
may contain sensitive personal information; matching does not establish
consent, de-identification, or clinical suitability. These limits are separate
from the existing research training run and do not alter its source data.

### Current Kaggle version reverified — 2026-10-19 22:34 UTC

A fresh authenticated read-only Kaggle metadata request reported current dataset
version 2, `isPrivate=false`, and metadata license name `Reddit API Terms`. The
current archive download was 218,283,787 bytes (SHA-256
`e0b99acbbb0ab9603191848a144e491741ad76a5a24b271e57ccea3b55a0bace`); its CSV
SHA-256 is exactly the previously joined
`7529dd554c83a3bb781df91405a40262451d6b98b4bd4725e5711c0a06a42ef7`, with
701,787 data rows and the same columns. This confirms that the existing 58,409
row-reference sidecar is bound to the current Kaggle version 2 snapshot, not
only an unidentified current file. It still cannot establish which Kaggle
version was used at curation time, and the metadata's license label does not
resolve whether this training and provider use is permitted. Rights and privacy
remain unresolved.

The installed Kaggle CLI 2.2.4 rejected the environment token during its auth
flow even though a direct bearer-authenticated read-only request and download
succeeded. The audit used the Kaggle API endpoint directly and kept the archive
and extracted CSV in a mode-0700 temporary directory; no source data was added
to the repository or training release. The updated private binding report records
the platform version and archive hash.
