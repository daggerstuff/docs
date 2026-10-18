# Edge-case source provenance decision packet

**Status:** request for one exact historical generation receipt; no release or
provider transfer is approved by this packet.

The recovery candidate is `ai/data/curated/recovery/gold-20261017/train_master_gold.recovered_candidate.jsonl`
(SHA-256 `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`,
190,139 rows). The narrow first-party synthetic edge branch contains 551 exact
candidate rows listed in `g03-edge-case-breakaway-rowrefs.jsonl`
(SHA-256 `b86fdcf371b56ede8a481b71d0f2e6b7be5e55c9ab6031894ddcf197ba92a6a7`).
Exact heldout-group matching excludes 29 rows across 12 ARC IDs. The remaining
522 rows and their exact row/message hashes are listed in
`g03-edge-case-post-holdout-rowrefs.jsonl` (SHA-256
`a5294068c241eb48007c6c33036da0c033a16198094c6e83f307eeaabf443a7a`). They
span 179 source groups, with provisional group-disjoint partitions of 410 train,
72 validation, and 40 test rows.

The generator `ai/training/build_edge_and_nightmare_dataset.py`
(SHA-256 `7a17480eab0bea9245491b3bdf49554678ba0d91ba6d53603da3e0ab093e5d9f`)
constructs this branch from a hardcoded 10-family taxonomy, difficulty,
ambiguity, and variation. It reads no external clinical seed narrative for
these edge cases. Local generated output
`ai/training/output/nightmare_fuel/checkpoints/edge_and_nightmare_generated.jsonl`
(SHA-256 `f601a0b8e7dba97db888e63d585cb5309ce734b3f40254b9dfe232d0bf01ce20`,
212 rows: 120 edge and 92 Nightmare Fuel) and the exact accepted seed corpora
support the first-party synthetic lineage. The candidate ARC text is generated
from those local seed records. This origin evidence is scoped to the edge branch;
it does not decide the Nightmare Fuel-derived rows or any other source class.

The accepted rows, seed map, checkpoint state, and inspected run-log metadata do
not record the generation backend/model. A targeted read-only OpenCode session
search for September 17–18 generator/artifact/`NF_BACKEND`/`NF_MODEL` terms found
no receipt. No corresponding Claude log or Foresight memory was found. A later
read-only W&B metadata query narrowed the likely route to two Vercel / DeepSeek
V4 Flash runs, but neither binds to the 212-row output hash; see the
[provenance follow-up](g03-historical-run-provenance-followup.md) and
[provider terms audit](../provider-terms-audit-2026-10-18.md). Current
configuration and temporal proximity do not establish the historical runtime. The generator
sets `clinical_reviewed=true` itself, so this field is not evidence of actual
clinical review or clinical readiness. Basic email, SSN, phone, card, URL, and
IPv4 pattern screens found no matches; this does not detect every identifier.

**Exact evidence requested:** provide or identify the contemporaneous run
receipt that records the `NF_BACKEND` provider and `NF_MODEL` for the generated
artifact above, without credentials. Confirm the applicable provider terms or
policy permit retaining those synthetic outputs and using them in research
fine-tuning. Separately verify the selected training provider's transfer,
retention, and privacy terms before any upload. This request is limited to the
identified first-party synthetic branch; it does not request generic
source-family signoff. If the receipt cannot be recovered, state the exact
backend/model and evidence basis for that assertion. Until this evidence is
resolved, the weighted JSONL package and `g04-release-manifest.json` remain
`draft_local_only` with `upload_gate: false`.

The local review package is at
`ai/data/curated/recovery/gold-20261017/g03-edge-review-package-20261017T1626Z/`.
It is mode 0700, with payload files mode 0600. The payload rows exactly match
the existing provider exporter projection. No upload, training job, or
promotion occurred. This research-only packet does not authorize clinical or
production use.
