# PsychEval v4 prompt split audit and source-availability blocker (2026-10-20)

Audited 1,977 `psycheval` rows by current v4 candidate-record hash transfer: 1,782 train, 103 validation, 92 test. Candidate and internal manifest each have 190,244 rows, with SHA-256 `f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349` and `3e8ca5b68e9dea84f071a5894aa479b7580c3d5089d7bf20227895a922eb89c9`.

All exact and normalized prompt hashes and all manifest content-group hashes are distinct; none repeat or cross splits. Existing source status remains `adapter_locator_only_no_local_raw_source` for all 1,977 rows. No upstream row locators are available, so no source-locator uniqueness or crossing claim is made.

The adapter declares private S3 prefix `whitebat:training/pixelated-empathy/output/psycheval/raw/PsychEval/` and `github.com/PsychEval/PsychEval`. The public GitHub `master` resolved to `834ad53db1b04c14647b2cb1cdb837c16ea267c3`; its 6,060-path tree is an application source tree and contains no adapter-described Chinese counseling JSON dataset or modality-dialogue files. No S3 access or source-data download was attempted. This leaves the exact source files and immutable source revision for the 1,977 candidate rows unavailable.

The next adapter-declared source, `Amod/mental_health_counseling_conversations`, has metadata at revision `d7e86f0813c5690181b41f97403c3674aa55dcef`, but its `combined_dataset.json` is manually gated. The subsequent `saeedzou/DAIC-WOZ` metadata also reports a manual gate (revision `01e0008ab43c540410ce26599e7a0a6c92100cd0`). Neither conversation file was fetched. The private hash-only candidate sidecar has 1,977 records and SHA-256 `1fa7c769588ba669fd290d1bbf3e09f0652bba24159460c3b411325e22044fde`; sidecar/report mode is 0600 in the private provenance directory.

## Public processed-repository candidate check (2026-10-20)

A public Hugging Face repository named `XuShihao6715/counseling-psycheval` was
found during a current availability recheck. Its dataset card describes a
processed PsychEval collection, but its metadata labels the license `other`
and says rights follow the upstream source. At pinned revision
`35ff3f0ee271946d9d8dd63a16fe79a0c760f4f4`, the `all.jsonl` file is 161,805,076
bytes with SHA-256
`8834426746b374d3010b3833630cdbe606b674fac390e67f65860c03d531e626`. Its 2,798
records were compared locally against the exact ordered non-system
user/assistant turns in every v4 `psycheval` candidate row, mapping public
`client`/`counselor` roles to `user`/`assistant` and applying the checked-in
adapter's counselor meta-tag stripping. Exact comparison found 0 matches, 0
ambiguous rows, and all 1,977 candidate rows unmatched. A second complete pass
normalized Unicode with NFKC, case-folded, and collapsed whitespace; it also
found 0 matches and left all 1,977 unmatched. The temporary source download was
deleted after both comparisons. This processed repository is not a usable source-row
binding for the current candidate and does not alter the earlier conclusion
that adapter-declared raw source files/revision remain unavailable.

The public dataset card's own description and license status are recorded at
<https://huggingface.co/datasets/XuShihao6715/counseling-psycheval>; public
availability does not establish rights or authorization to use the data.

This establishes candidate prompt/group split metrics only, not upstream origin. Rights, privacy/consent, clinical review, training eligibility, and provider-transfer permission remain unresolved. No candidate, manifest, release payload, or provider job was changed.

## Superseding source snapshot binding update (2026-10-20)

The prior metadata-only access conclusion is superseded for technical row
matching by the [upstream-origin binding audit](psycheval-v4-upstream-origin-binding-2026-10-20.md).
The configured `r2` object-store remote contains the adapter-declared
`whitebat` bucket path; all 1,977 rows now have unique exact or normalized
matches against its current private snapshot. The immutable upstream source
revision remains unknown, and this does not resolve rights, consent, clinical
suitability, or provider-transfer permission.
