# Local upstream-source presence audit: Empath and MentalChat16K

> **Correction added 2026-10-19 19:43 UTC:** the original conclusion below
> that no raw upstream copy existed anywhere in the local workspace was too
> broad. Exact Empath and MentalChat16K source files are present in the private
> `private-source-origin-binding-20261019/` directory. A follow-up verified
> that all five files match the pinned public Hugging Face revisions byte for
> byte; see the final update below. The old-cache statement remains accurate.

The initial pass checked the local Hugging Face cache and project search only;
it did not use the network. It missed files already present in the private
origin-binding directory. The follow-up below corrects that search and verifies
the upstream file identities. This remains a source-presence and lineage check,
not a rights, privacy, or quality determination.

## Result

Exact upstream files for both families are present under
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/`.
The pinned public revisions match those files byte for byte, and existing
row-reference sidecars provide exact and ambiguous sequence-level bindings.
The candidate and release were read only; no source or release data was
modified, and no row text was emitted into this report.

The pinned candidate is
`ai/data/curated/recovery/gold-20261017/train_master_gold.recovered_candidate.jsonl`
(190,139 rows; SHA-256
`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`). The
current v4 release manifest is
`docs/training/execution-2026-10-19/wandb-full-corpus-current-master-20261019-v4.json`
(SHA-256
`a4b0507ff6447644d022e28b1ada91daefa0139f23f8800ae953a0fa9ab5cdb8`). Its
row-reference-backed source counts agree with the candidate counts below.

| Candidate family | Candidate rows | Adapter-declared upstream identity | Adapter file SHA-256 | Exact local upstream copy |
|---|---:|---|---|---|
| `empath` | 35,977 | HuggingFace `Adapting/empathetic_dialogues_v2`; original dataset attribution `facebook/empathetic_dialogues` | `0186f04ca326631bf0cdc99f42fa1711eede6a150194666a84ac6aaab7da10dc` | Present in private origin-binding directory; exact public revision file hashes verified |
| `mentalchat16k` | 11,135 | HuggingFace `ShenLab/mentalchat16k`; adapter declares original S3 prefix `whitebat:training/pixelated-empathy/ingestion/hf/mentalchat16k/` | `fc0e06c9d0cb1f4e1e428ec7c2ed2f21cadfe872fe253346e6019324495f7466` | Present in private origin-binding directory; exact public revision file hashes verified |

Candidate row ordinal ranges (zero-based, inclusive) were `11,802–47,778` for
`empath` and `58,896–70,030` for `mentalchat16k`. These are positions in the
pinned candidate only; they are not upstream row numbers or exact bindings.

## Local search evidence

- The initial project search found the adapter declarations, candidate,
  release partitions, manifests, and training artifacts but missed the raw
  exports under the private origin-binding directory.
- `/home/vivi/.cache/huggingface` contains no repository snapshot for either
  `Adapting/empathetic_dialogues_v2` or `ShenLab/mentalchat16k`; its only
  HuggingFace cache entries were a Xet log and cache metadata.
- The adapter-declared source files needed for local matching are:
  - Empath: the exact HuggingFace dataset snapshot/config and all three split
    exports (`train`, `validation`, `test`) corresponding to the candidate's
    source version. The adapter writes these as `train.jsonl`,
    `validation.jsonl`, and `test.jsonl` under its raw-data directory.
  - MentalChat16K: `Interview_Data_6K.csv` and `Synthetic_Data_10K.csv` from the
    adapter's declared S3 prefix, or the exact corresponding files from the
    `ShenLab/mentalchat16k` snapshot, plus the snapshot/revision identity.

## Initial next operation (completed by the 19:43 UTC follow-up)

The follow-up verified the exact pinned file hashes and linked the existing
row-reference sidecars into v4 by complete candidate-row hashes. Counts and
limitations are recorded at the end of this report. No candidate or provider
release needed to change.

## AWS account check for declared `whitebat:` S3 paths

A read-only AWS MCP check in the currently authenticated account returned
account `638175140335` and three buckets: `cf-templates…`,
`pixelated-empathy-terraform-state-638175140335`, and
`sagemaker-us-west-2-638175140335`. None is named `whitebat`. Listing the
`training/pixelated-empathy/output/` prefix in each bucket returned zero
objects. This rules out those declared object paths in the checked account and
prefix; it does not prove that the `whitebat:` alias cannot resolve through a
different account, role, or storage provider. No object data was read or
changed. To make the alias searchable, use the project’s existing rclone or
AWS profile mapping to identify its bucket/account, then list only the exact
source prefixes in that target.

## 2026-10-19 pinned-source and v4 transfer verification

Downloaded the public files from the immutable revisions recorded in the
origin-binding manifest to `/tmp`, then compared their byte counts and SHA-256
values with the manifest. All five files matched. Empath's public `dev.csv`
is the adapter's `validation` split. The local private binding directory also
contains the same source files; the initial presence search missed this
location. No source text was displayed or copied into project documentation.

The existing row-reference sidecars were joined to the current v4 internal
manifest using SHA-256 of the complete original candidate row. All 35,977
Empath and 11,135 MentalChat16K candidate rows from the prior 190,139-row
candidate are byte-identical in the 190,244-row v4 candidate. Their existing
row-level source evidence therefore transfers to v4 without a similarity join
or candidate edits. This is identity transfer, not a new source-row match:
Empath has 12,042 unique exact turn-sequence matches, 15,249 ambiguous matches,
and 8,686 unmatched rows; MentalChat16K has 1,090 unique, 17 ambiguous, and
10,028 unmatched. Full non-system sequences equal the public adapter projection
for 27,287 Empath rows and 1,107 MentalChat16K rows. Four further Empath rows
match only as exact contiguous subsequences. These counts still do not prove
full-record adapter output equality, rights, privacy, or training eligibility.
