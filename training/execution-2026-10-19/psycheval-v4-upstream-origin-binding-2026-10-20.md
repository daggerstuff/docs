# PsychEval v4 upstream-origin binding and split audit — 2026-10-20

The previously inaccessible adapter-declared raw source is available in the
configured object-store account under the `whitebat` bucket. I copied the
adapter's `data/` prefix from
`r2:whitebat/training/pixelated-empathy/output/psycheval/raw/PsychEval/data/`
to a local mode-0700 directory. It contains 369 JSON files totaling
314,458,938 bytes. The source has no immutable upstream revision identifier;
the file-level snapshot manifest SHA-256 is
`48a22c255682cc64faccd8aa5f05f0ea1fa61b5da4ce9508143a1a1df154cb9e`.

The checked-in `PsychEvalAdapter` rendered 2,798 records from that snapshot.
Against the frozen v4 candidate (190,244 rows; SHA-256
`f56e10b52ed83645ec3eca1b468724644dcbf6f843da96d7e82b5b4ef47bc349`), all
1,977 `psycheval` rows were matched to one upstream adapter record after
NFKC, case-fold, and whitespace normalization. Exact ordered non-system
turns uniquely matched 1,968 rows; the remaining 9 were normalized-only.
There were no ambiguous matches, and no exact source locator crossed the
train/validation/test split. Family counts are 1,782 train, 103 validation,
and 92 test.

An independent second pass rebuilt the adapter index from all 369 local source
files and rechecked every candidate line hash, split, exact match, and
normalized match against the private hash-only sidecar. It passed with the
same totals. The sidecar is
`ai/data/curated/recovery/gold-20261017/private-source-origin-binding-20261019/bindings/psycheval-v4-upstream-rowrefs.jsonl`,
mode 0600, SHA-256
`219d70ccc7f488dcf548a418f25c48026f607c307ab8892c1fe7449eec0ed052`.
Source JSON remains local under the same mode-0700 private provenance root;
the report contains no dialogue text or raw client identifiers.

This materially improves technical row lineage but does not prove that the
current object-store snapshot is byte-for-byte the version used to create the
candidate. The adapter names a GitHub project whose current public tree does
not contain this counseling corpus, and the object store exposes no immutable
source commit/version. Exact content correspondence also does not establish
rights, consent, clinical suitability, or provider-transfer authorization.
No candidate, split, release payload, or training job was changed.
