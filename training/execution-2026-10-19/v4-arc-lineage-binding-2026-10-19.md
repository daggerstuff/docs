# v4 ARC lineage/content binding — 2026-10-19

The v4 release contained 1,085 `arc_corpus` rows whose raw row hashes did not
join to the older 190,139-row source-locator sidecar. I closed that technical
linkage gap using the canonical renderer in
`ai/training/consolidate_arc_corpus.py::_session_messages` and the current ARC
source archive. The frozen candidate, split, training payloads, manifest, and
provider jobs were read only.

The audit recomputed every v4 candidate row hash against its raw line and
matched every ARC row to exactly one archived `(arc_id, session_n)` key. It
then rendered the archived session through the canonical exporter and compared
the complete message arrays in memory. All 1,085 rows matched exactly; there
were no missing or ambiguous keys, source-label mismatches, or content
mismatches. The matching archive audit metadata says `accept` for all 1,085
rows, and every matching record has writer, auditor, and plan metadata. The
rows span 430 ARC IDs: 981 train, 58 validation, and 46 test.

Private, hash-only row references and a protected copy of the exact source
archive are stored under
`ai/data/curated/recovery/gold-20261017/private-v4-arc-lineage-20261019/`.
The directory is mode `0700`; its archive snapshot, row references, and report
are mode `0600`. Snapshot SHA-256 is
`8d5b53b9ea9d2c6e157f072bd3542550d7f0caaa5e4cdfb585d4751746f19936`; the
row-reference sidecar SHA-256 is
`23b6e6eed9f9bb3af22c7ff1605aac1c59414e7ec7b6b77c22ddf5e7cc1a5e12`.
The private report records the input hashes and all aggregate counts. No
message text is emitted in the sidecar or this report.

Reproduce and verify the protected artifacts without overwriting them with:

```bash
PYTHONPATH=ai uv run python ai/training/audit_v4_arc_lineage.py
```

This establishes exact ARC archive-to-candidate content lineage and preserves
the archive state used for the check. The archive's machine `accept` verdict
does not establish clinician review, clinical quality, rights, privacy
clearance, generation-provider identity or terms, or permission to transfer
data. Separate lane-2 human decisions remain unbound to candidate content
hashes and are not transferred by ARC ID.
