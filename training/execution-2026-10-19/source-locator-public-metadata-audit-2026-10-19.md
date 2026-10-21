# Unbound source locator metadata audit — 2026-10-19

Status: **partial; the original audit was metadata-only, and follow-on exact source binding has since been completed for some families. No rights/privacy approvals were created.** This document checks adapter-declared public locators against primary repository/catalog metadata. See the later addenda and the [Reddit binding audit](../execution-2026-10-17/top-reddit-source-local-cache-audit-2026-10-19.md) for follow-on row matching; no clinical text is reproduced here, and no source or candidate rows are changed by this audit.

## Scope and interpretation

The pinned candidate is 190,139 rows (`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`). Its row/message hashes are bound to the local source-decision ledger, but that is not the same as binding rows to upstream source records. The locator sidecar records 9,679 rows with structured local locators and 177,423 with proposed source IDs; it reports 459 source labels without a source-ID mapping and 3,037 rows with neither proposed ID nor structured locator. The 16 proposed IDs are not treated here as exact origin matches.

The audit below covers all 16 proposed-ID families, the two adapter-enriched but unmapped families, and prioritizes remaining labels with at least 1,000 rows. It is **not a per-record upstream join**. Most of the long tail (459 labels without a source-ID mapping) consists of book/title, creator/video, local synthetic, or otherwise non-identifiable labels; absent a unique edition/URL/creator artifact in the local worklist, an online title search cannot establish identity. Those need source locators from existing acquisition/project records, not inferred matches.

## Public source metadata for priority unresolved families

| Candidate label (rows) | Adapter declaration vs primary source | Publicly obtainable files without credentials | License/access metadata and consequence |
|---|---|---|---|
| `reddit_mental_nlp` (70,968) | Adapter declares Kaggle `kamaruladha/mental-disorders-identification-reddit-nlp`; the follow-on audit verified current platform version 2 and bound 58,409 candidates uniquely to its CSV snapshot. | **No** credential-free download verified; a token-authenticated Kaggle API request was used. The Kaggle CLI auth flow rejected the environment token, while the direct API request succeeded. | Kaggle metadata names `Reddit API Terms`; whether they permit this model-training/provider use remains unresolved. The original curation-time version is also unknown. See the [versioned source binding record](../execution-2026-10-17/top-reddit-source-local-cache-audit-2026-10-19.md).
| `empath` (35,977) | Adapter declares HF `Adapting/empathetic_dialogues_v2`; this is a real public dataset repository. | **Yes**, the public HF repo exposes CSV data files/splits without a gated-access notice. | HF card marks `afl-3.0`; it also describes the repository as a fine-tuned derivative of `facebook/empathetic_dialogues`, whose separate card marks `cc-by-nc-4.0`. Pinning the exact candidate source revision and resolving the derivative/attribution terms remain necessary. [Adapter-declared HF dataset](https://huggingface.co/datasets/Adapting/empathetic_dialogues_v2), [original HF dataset](https://huggingface.co/datasets/facebook/empathetic_dialogues) |
| `reddit_mental_health_posts` (30,444) | Adapter declares HF `solomonk/reddit_mental_health_posts`; primary page exists and shows a public CSV dataset, one train split (~151k rows). | **Yes**, public HF viewer/repository is accessible without a login gate. | The page exposes Reddit-derived post content and URLs; no license was visible on the inspected card. Public accessibility is not a training license. Candidate version and row matching remain unverified. [HF dataset card/files](https://huggingface.co/datasets/solomonk/reddit_mental_health_posts) |
| `mitch_hamidi_bpd_nlp` (13,890) | Adapter declares `github.com/mitchellhamidi/may-2024-mental-health-nlp`. The canonical repository/file identity could not be confirmed from GitHub primary pages/search in this audit. | **Not verified**; no exact public file identified. | Treat adapter URL as a declaration only, not confirmed identity or access. Obtain the source URL/commit from existing acquisition record or local cache provenance. |
| `mentalchat16k` (11,135) | Adapter declares `ShenLab/mentalchat16k` plus private `whitebat:` cache. Current canonical HF spelling is `ShenLab/MentalChat16K`; repository exists. | **Yes** on HF: `Interview_Data_6K.csv`, `Synthetic_Data_10K.csv`, and `README.md` are listed as public files. The private S3 cache is not publicly accessible. | HF card marks MIT; the dataset paper describes a mixture of synthetic conversations and anonymized behavioral-health coach/caregiver intervention transcripts. Exact version/row binding and any upstream participant/data-use conditions are unresolved; do not infer clearance solely from MIT metadata. [HF repo at pinned revision/file listing](https://huggingface.co/datasets/ShenLab/MentalChat16K/tree/5f60cd380cfc58f0f12d44892bed41ee3670a70a), [dataset paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12520247/) |
| `mental_health_multiagent` (5,606) | Adapter declares `github.com/mental-health-multiagent/mental_health_multiagent`; current primary repo found is `mithatco/mental_health_multiagent`, so the declared owner/URL does not match. Its README identifies an evaluation dataset with chat logs, profiles, and reference documents. | **Yes**, the current `mithatco` public GitHub repository exposes its tracked files without credentials. This does not prove it is the exact source of the local S3-cached files. | README says research/educational use, but no verified license grant for the data was found in this check. Do not treat this project repo as a confirmed origin until its commit/files match the local cache. [Current GitHub repo](https://github.com/mithatco/mental_health_multiagent) |
| `kokorochat` (4,615) | Adapter URL `github.com/kokorochat/kokorochat` does not match the primary project repository found: `UEC-InabaLab/KokoroChat`. | **Yes**, GitHub repo publicly exposes `kokorochat_dialogues`; a linked HF dataset is also referenced from the project page. | Project declares CC BY-NC-ND 4.0. That license has non-commercial/no-derivatives terms; legal review is needed before treating it as usable for fine-tuning or distributing adapted weights. Exact source version and row match are still absent. [Official project repository](https://github.com/UEC-InabaLab/KokoroChat) |
| `clinical_book_DSMV` (3,725) and other `clinical_book_*` labels | No exact title/edition/acquisition locator in the worklist for this label. “DSMV” does not uniquely identify the book/edition or a source file. | **No exact file can be identified from the label alone.** | Do not infer public domain or a license from the abbreviated label. Recover title, edition, ISBN, acquisition source, and licensed file manifest from project records; batch disposition can then be decided without reviewing individual rows. |
| `psycheval` (1,977) | Adapter uses private S3 cache `whitebat:.../psycheval/raw/PsychEval/` and declares `github.com/PsychEval/PsychEval`. The public GitHub identity found is a student mental-health-risk sentiment-analysis project; it does not establish that it is the Chinese counseling-dialogue tree expected by this adapter. | **No exact matching dataset file verified** from the declared GitHub URL. Private S3 source requires project credentials. | The mismatch means the adapter locator is insufficient; trace the S3 object manifest to its upstream repository/revision before asserting public availability or license. [Declared GitHub URL](https://github.com/PsychEval/PsychEval) |
| `crisis_benchmark` (1,522) | Adapter declares HF `arnaiztech/llms-mental-health-crisis-benchmark`. Repository exists, but its card describes an evaluation benchmark and marks CC BY-NC 4.0. | **Yes**, public HF files are listed (Parquet/card) without a gated-access notice. | Current repository viewer reports ~2.25k examples, while candidate family has 1,522 rows; this is not proof of matching rows/version. The CC BY-NC card and evaluation-benchmark purpose do not alone establish suitability for SFT. [HF dataset card/files](https://huggingface.co/datasets/arnaiztech/llms-mental-health-crisis-benchmark) |
| `counseling_conversations` (1,415) | Adapter-declared HF `Amod/mental_health_counseling_conversations` is a real public repository, but currently requires accepting access conditions and sharing contact information. | **No, not anonymously**: HF says sign-in and acceptance are required before accessing contents. | Card declares RAIL-D, non-commercial research use, a donation condition for commercial use, and prohibits altering individual Q&A pairs while allowing filtering/subsetting. This is materially different from anonymous open-file access; verify condition acceptance and source rows before use. [HF card and terms](https://huggingface.co/datasets/Amod/mental_health_counseling_conversations) |
| `esconv` (892) | Adapter declares the official THU-COAI GitHub repository and a direct raw URL for `ESConv.json`. | **Yes**, the adapter-declared raw file is publicly addressable; the repository also lists the data/code. | The official repository is the right identity, but the inspected repo metadata does not itself settle third-party training rights or privacy scope. Exact candidate row/version binding remains missing. [Official repository](https://github.com/thu-coai/Emotional-Support-Conversation), [declared raw file](https://raw.githubusercontent.com/thu-coai/Emotional-Support-Conversation/main/ESConv.json) |
| `psydial` (892) | Adapter declares HF `qiuhuachuan/PsyDial-D101`; HF dataset page exists. | Public HF page is reachable; **file-level anonymous access and license were not verified** in this audit. | Keep unbound pending file/revision and license metadata checks. [HF dataset page](https://huggingface.co/datasets/qiuhuachuan/PsyDial-D101) |
| `psy_insight` (673) | Adapter declares `Psy-Insight/Psy-Insight`; the primary repository discovered is `ckqqqq/Psy-Insight`, a different owner/name. It contains public data files, but repo identity differs from the adapter locator. | **Yes** for the `ckqqqq` repo files; no credentials needed for the public GitHub tree. | Repository exposes a copyright notice/link and no clear dataset license grant was verified. Public file access does not equal authorized training. Resolve canonical owner/revision and terms, then bind rows. [Current repository](https://github.com/ckqqqq/Psy-Insight) |
| `daic_woz` (129) | Adapter declares USC's DAIC-WOZ portal and an HF mirror `saeedzou/DAIC-WOZ`. | **Not established for the authorized source.** The unofficial HF mirror is public-facing, but the USC source is a controlled-access clinical interview corpus; do not use the mirror as permission-free access. | The HF mirror has no license metadata visible in its card. Trace exact participant corpus/version and data-use agreement against USC before any training. [USC DAIC-WOZ portal](https://dcapswoz.ict.usc.edu/), [HF mirror](https://huggingface.co/datasets/saeedzou/DAIC-WOZ) |
| `dsm_vector_space` (116) | Adapter declares `savelee/dsm-in-vector-space`; the repo is a public software/data project and contains DSM-5-TR JSON assets. | **Yes**, its repo tree exposes the declared structured JSON assets without credentials. | Repo declares CC BY 4.0 for its project datasets. However, assets describe DSM-5-TR material; exact cached files and incorporated-text copyright scope still need review. [Repository and license statement](https://github.com/savelee/dsm-in-vector-space) |
| `annomi` (98) | Adapter declares official `uccollab/AnnoMI`; its public README lists `AnnoMI-simple.csv` and `AnnoMI-full.csv`. | **Yes**, both CSVs are publicly listed in GitHub with no credential gate. | Public release is verified, but the inspected README has no explicit license grant. It includes video URLs and expert-annotated counseling transcripts; rights/privacy checks remain. [Official repository](https://github.com/uccollab/AnnoMI) |
| `mitags` (7) | Adapter declares official `Advanced-Reality-Lab/MI-TAGS`. | **Partly**: sample CSVs are public; full data require an access request form. | No license text was found in the repository page. Do not treat sample availability as a grant for full data. [Official repository/access instructions](https://github.com/Advanced-Reality-Lab/MI-TAGS) |
| `hope` (4) | Adapter declares official `LCS2-IIITD/SPARTA_WSDM2022`, which contains `HOPE_data/`. | **No**: the repository instructs users to complete an agreement form and email confirmation to request dataset access. | Exact access requires agreement/authorization; no license grant was found in the repository page. [Official repository and access steps](https://github.com/LCS2-IIITD/SPARTA_WSDM2022) |

## Adapter-declaration-only sidecar and exact binding distinction

The local enrichment audit records 3,037 rowrefs across three adapters: 1,415 `counseling_conversations`, 1,522 `crisis_benchmark`, and 100 `ml_bpd`. These are **adapter declarations**. A separate exact-content join already verifies all 100 `ml_bpd` user-message/severity-label pairs against the public CSV and adapter rule (56 unique source rows; 44 duplicate-text matches with equal severity); system prompts differ, so this is not a complete rendered-record identity join. The two HF families remain source-row-unbound. The enrichment report itself explicitly retains all three in declaration-only status unless upgraded by exact matches.

## Concrete next lineage operation

For sources with public, credential-free files above, record current commit/revision, source-file SHA-256, split/file/row identifiers, then locally run the adapter projection and hash join against candidate rows. Emit only row ordinal, upstream file/revision/row ID, canonical record hash, and duplicate-match count into a private sidecar; keep ties ambiguous. For Kaggle, private-S3-only, book/title, and owner-mismatch families, first use the existing acquisition/cache manifests to identify the actual file and exact upstream revision. Do not replace these with similarly named public repositories. This produces an actionable per-family queue without line-by-line human review.

## Local evidence fingerprints used

| Local report/input | SHA-256 |
|---|---|
| `candidate-lineage-coverage-2026-10-19.json` | `f057adb5580169fa7d1a114c739aba9bbf9cfba13b85b73bd44982ccdf9ff0be` |
| `candidate-source-locator-sidecar-2026-10-19.json` | `faee5f50999fcb886b7ce7e7df41d8497c0a832dc7162b1eacd52593218c2b9a` |
| `190k-source-clearance-worklist.csv` | `9de46eda5830bdcd46aaf4e4a6e4cf2a66b1c470c37cf669c7c8745ba24bc2be` |
| `candidate-adapter-declaration-enrichment-2026-10-19.md` | `77ded212fe2ee8b3eeee8144c46ece37f1218775970b1e922ebad3376b765f25` |
| `local-upstream-source-presence-audit-2026-10-19.md` | `b34b7beff6f2e6540167f67fa0eb0c7ce724ba61a8ef3a576e5d57a2550e683c` |


## Exact-origin join follow-up: AnnoMI

The `annomi` candidate family (98 rows) was projected using the adapter against
the adapter-declared official `AnnoMI-full.csv` and `AnnoMI-simple.csv` files
at upstream commit `42936645ec3857a9c84ab296a36a3c34b779ef49`. The full and
simple source hashes were recorded, and the adapter projection produced 133
records. None of the 98 candidate rows exactly matched the projected ordered
role/content records. All 98 therefore remain upstream-row-unbound; the
candidate's family label alone does not establish origin. No license grant was
found in primary source metadata, and no rights status is inferred. A private
hash-only rowref sidecar and report are under
`ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/`;
see `annomi-official-projection-row-binding-report-2026-10-19.json`.

## Exact-origin joins: Empath and MentalChat16K

The adapter-projected ordered non-system turns were joined to pinned upstream
files. Empath matched 27,291 of 35,977 candidate rows: 12,042 resolve to a
unique upstream row, 15,249 have duplicate-text ambiguity, and 8,686 are
unmatched. MentalChat16K matched 1,107 of 11,135 rows: 1,090 unique, 17
ambiguous, and 10,028 unmatched. Candidate system prompts differ from the
adapter projection, so these are turn-sequence matches rather than exact full
rendered-record identity. Rights, attribution, and any source-specific terms
remain separate from technical lineage. The pinned revisions, file and adapter
hashes, match methods, and private locator sidecars are documented in the
[exact-origin report](empath-mentalchat16k-origin-binding-2026-10-19.md); no
candidate or release files were modified.

## Exact-origin join: Psy-Insight

The current 673-row `psy_insight` family was projected with the checked-in
adapter's role mapping against the original public GitHub files at commit
`0a5bd3f011dd8fdb8d6b7c0081b3510e4a478f5a`. The exact join uses the complete
ordered non-system role/content sequence after the adapter's per-turn
whitespace stripping; it does not use similarity or normalization. The
projection produced 951 source records (520 English, 431 Chinese). It bound
518 candidate rows to a unique source dialogue ID; 155 rows did not exactly
match a full projected dialogue; there were no ambiguous full-sequence matches.
System messages and adapter metadata are excluded from this technical join.

The raw upstream file hashes are `ebbbb482ec19973ab45e76df2192fc8fa84958085534cbd72e30f1af3ce33481`
(English) and `1cc0f35f928e3f8bbfd281264b0c59933a5d449f003ade2bb736e95533429e14`
(Chinese). The row-hash sidecar and report are private mode 0600 under
`ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/psy-insight-exact-binding-20261019/`;
report SHA-256 is `a9b9629cd0db4a09d1bbfbd738fe86e7cb72781d3db515a29d5997c63131d89a`,
and the 673-row sidecar SHA-256 is
`b23454b4da40e0e0d50c2afd27c6658626521bed5e89b0cd6f244c3f5d5d5d3d`.
The next concrete step for the 155 unmatched rows is to compare against the
existing row-keyed repair overlay and the exact source-turn materialization,
then retain only exact contiguous-turn or explicitly generated-continuation
lineage with separate statuses. Do not upgrade these 155 through similarity.
The repository's public availability is not a data license; training,
redistribution, privacy, and weight-distribution rights remain unverified.

### Generated-continuation lineage for the 50 repaired Psy-Insight rows

The 50 Psy-Insight repairs are generated continuations, so their complete
final turn sequences cannot match the upstream source projection. The repair
overlay already records source case IDs from the pinned Hugging Face dataset
`xi1019/counseling-psy-insight` revision
`dd6f2e582377ddb71e976ec8f45ad48b5c5fc57a`. I re-fetched both source JSONL
files and verified their hashes against the repair generator, then checked
each case ID for a unique upstream row and each candidate hash against the v4
internal manifest. All 50 resolve uniquely and transfer to v4 (44 train, 2
validation, 4 test). Of these, 32 also appear in the separate exact public
projection sidecar; 18 were previously among its 155 unmatched final records.

This establishes the source excerpt used to construct the 50 repaired prompts;
it does not turn a generated continuation into an upstream response or imply
clinical review. The mode-0600 rowref sidecar and aggregate report are under
`../../ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/psy-insight-exact-binding-20261019/`.
The final response remains generated, unreviewed, and separate from source
lineage; rights/privacy and clinical-suitability questions remain open.

## Subsequent public row-binding update (2026-10-19)

The earlier table records metadata-only status against the older 190,139-row
snapshot. A later exact-content join against the current 190,244-row gold
candidate and pinned public upstream revisions now binds 1,406
`crisis_benchmark` rows by exact ordered non-system adapter projection (1,370
unique, 36 ambiguous), 22 additional normalized-only rows, and leaves 94
unmatched. For `dsm_vector_space`, all 116 rows match the public repository's
adapter projection, but every row maps to two upstream rows and remains
ambiguous. Neither family has a complete current system+user+assistant adapter
render match. DSM's original cache locator is private S3, so the public
repository match does not prove which private object/revision supplied the
candidate. Full methods, revisions, source-file hashes, and private sidecars are
summarized in the [binding report](public-source-row-binding-summary.md).
These technical joins do not resolve rights, privacy, consent, clinical
suitability, benchmark leakage, or provider-transfer permission.


## Exact-origin joins: ESConv and PsyDial

The current gold candidate's 892 `esconv` and 892 `psydial` rows were joined
against checked-in adapter projections from pinned primary sources. ESConv's
official repository was pinned at `f262d062ad74cb39b17ea476facc81568ddcba24`;
its `ESConv.json` hash matches the locally cached source file. Of 892 candidate
rows, 13 matched one source row exactly, 16 more matched only after
normalization, and 863 did not match. PsyDial's pinned `D101` projection
matched all 892 rows: 891 have a unique source locator and one is ambiguous
between repeated source rows. Although the adapter also declares D4 and D1,
those pinned JSON files project zero records under the adapter's required
`messages` plus `golden` schema; all PsyDial candidate matches resolve to
D101. Exact matching compares ordered user/assistant turns and excludes
system prompts; normalized matches are discovery-only. Full-record identity is
therefore not claimed. See the [private binding report and rowref sidecar](../../ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/esconv-psydial-row-binding-2026-10-19/audit-report.json).
Public source access and HF Apache-2.0 card metadata do not independently
establish all training, incorporated-source, privacy, attribution, or
redistribution rights. Candidate and release files were not changed.

## Private-source cache check (2026-10-19)

The configured `whitebat:` rclone remote is present and resolves to Civo Object
Storage (`objectstore.nyc1.civo.com`, region `nyc1`). Read-only listings of the
declared ingestion prefixes returned HTTP 403 `UserSuspended`. The private
MentalChat16K and PsyEval cache objects therefore could not be read through the
configured account. This is a provider/account state, not evidence that the
objects or their source manifests are absent. Existing public HF files were
used for the exact MentalChat16K join; the private PsyEval origin remains
unresolved. Restore access to the Civo account or use the project-authorized
alternate storage mapping, then list only the exact source prefixes.
