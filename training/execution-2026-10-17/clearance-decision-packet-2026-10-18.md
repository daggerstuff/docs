# Training data clearance decision packet

**Status:** prepared for authorized data, privacy, and training owners; no dataset is cleared by this packet. No message text, prompts,
reviewer rationale, or PHI are included.

## Decision scope

The recovered candidate is **190,139 rows**, SHA-256 `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`. The metadata
audit found **0 rows with exact signed rights plus privacy/consent clearance bound to candidate row references**. The source ledger
joins all rows, but its hashes establish identity, not authorization.

The closest research-only subset is the 522-row synthetic edge branch. Its post-holdout row-reference ledger SHA-256 is
`a5294068c241eb48007c6c33036da0c033a16198094c6e83f307eeaabf443a7a`; the private rendered split contains 410/72/40 rows. It remains
`draft_local_only` with `upload_gate=false`. Its historical generator/model receipt, output-use terms, seed/input privacy and rights,
selected-provider terms, golden-control lineage, and content-bound human decisions remain open.

## Evidence already assembled

- [`source-rights-privacy-audit-2026-10-18.md`](../source-rights-privacy-audit-2026-10-18.md) maps 177,423 candidate rows to 16 source
  IDs. Another 12,716 rows across 459 unmatched labels need curator provenance mapping.
- [`g03-historical-run-provenance-followup.md`](g03-historical-run-provenance-followup.md) narrows the historical generation route to
  two plausible W&B runs, both Vercel / DeepSeek V4 Flash, but neither is tied to the 212-row output hash.
- [`provider-terms-audit-2026-10-18.md`](../provider-terms-audit-2026-10-18.md) identifies the provider's public data-handling terms
  and remaining account contract/settings questions.
- The package has verified payload hashes, group-disjoint splits, private file modes, and assistant-only loss weights. The W&B launcher
  rejects it before upload while the release gate remains closed.

## Priority source decisions

| Source ID | Candidate rows | Evidence issue | Required decision/evidence |
|---|---:|---|---|
| SRC-027 | 70,968 | Reddit posts; current API terms restrict AI training absent rightsholder permission | Identify acquisition path and version; provide written rights-holder permission for research SFT and named vendor transfer, plus privacy/consent authorization |
| SRC-030 | 35,977 | Reddit-derived empathy corpus; exact upstream version/path unresolved | Same Reddit permission and privacy evidence, bound to exact version and row refs |
| SRC-028 | 30,444 | Reddit mental-health posts | Same Reddit permission and privacy evidence, bound to exact version and row refs |
| SRC-031 | 13,890 | Reddit BPD/NLP corpus | Same Reddit permission and privacy evidence, bound to exact version and row refs |
| SRC-039 | 892 | ESConv repository says academic research only and all rights reserved | Written owner permission for this project's purpose, fine-tuning and vendor transfer; verify participant/privacy conditions |
| SRC-046 | 129 | DAIC-WOZ access is restricted under signed application and academic/non-profit limits | Produce signed agreement; verify project eligibility, model training and vendor-transfer permissions, and privacy conditions |
| SRC-047 | 98 | AnnoMI local records conflict; public repo snapshot has no license text | Resolve source-owner decision; supply primary license/permission, consent/privacy evidence and exact row binding |
| Other matched IDs | 25,025 | Per-source records and evidence are itemized in the rights audit | Review each mapped ID/version individually; do not apply one source's decision to another |
| Unmatched labels | 12,716 | 459 labels not mapped to the five proposed manifests | Curator maps each label to immutable source/version and source ID, then source owner and privacy review decide |

The 16 matched source-ID counts sum to 177,423. These counts are inventory joins, not a cleared subset; do not sum source groups as a
release cohort without rechecking the exact row-reference ledger.

## Required decisions

### Source owner / legal reviewer

- Exact source/version and authority for each source ID or mapped unmatched label.
- Permission scope: internal research, research fine-tuning, commercial use if relevant, and transfer to each named provider/product.
- Conditions: attribution, share-alike, non-commercial, purpose limits, redistribution, downstream model restrictions, deletion, or
  expiry.
- Link to primary license, signed permission, or applicable agreement; decision date and reviewer authority.

### Privacy and clinical data owner

- Lawful/authorized purpose and applicable consent or other authorization.
- Sensitive-data and re-identification risk assessment, de-identification checks, and clinical privacy approval for the exact artifact
  hash and scope.
- Whether processing by W&B, Fireworks, or Adaption is permitted, including retention, regions, subprocessors, human access, logs, and
  deletion duties.
- Explicit exclusions and a review date/expiry.

### Training owner

- Exact destination account, product, endpoint and base model.
- Accepted contract/DPA/BAA and effective settings; written answers for dataset and checkpoint retention/deletion, service/model
  improvement use, output and adapter rights, and onward transfers.
- Maximum covered training/inference cost, checkpoint export route, and stop conditions. Confirm that zero-cost promotional training
  does not imply free sampling, inference, storage over quota, or deployment.

### Dataset curator / evaluation owner

- Bind each approval or exclusion to the immutable candidate hash and exact row references; resolve all 459 unmatched labels before
  claiming candidate-wide coverage.
- Bind lane-2 human decisions to exact content digests; never infer those decisions from ARC IDs alone.
- Recover golden-control source identities before claiming source independence or using the 52 controls for sealed evaluation.
- Record privacy-screen limitations and require human clinical quality review before any clinical-quality claim.

## Sign-off record template

Copy one record per source ID / immutable source version and one per destination provider. Do not sign at source-family level unless
the evidence explicitly covers every source and row in that family.

```yaml
record_id: <unique-id>
candidate_sha256: 4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663
rowref_ledger_sha256: <exact-rowref-ledger-sha256>
source_id: <SRC-id-or-newly-mapped-id>
source_name_and_version: <immutable-source-identity>
candidate_row_count: <integer>
decision: defer # approve | approve_with_conditions | reject | defer
allowed_purposes: [] # e.g. internal research, named-provider research SFT
allowed_destinations: [] # provider, product, account, region
primary_rights_evidence: [] # URLs or signed-document IDs and hashes
privacy_consent_evidence: [] # authorization, review record, artifact hash
conditions_and_exclusions: []
retention_deletion_requirements: []
reviewer_role: <source-owner | legal | privacy | clinical-data-owner | training-owner>
reviewer_name: <name>
reviewed_at_utc: <timestamp>
review_expires_at_utc: <timestamp-or-null>
signature_or_approval_reference: <immutable-reference>
```

## Release gate

Keep `upload_gate=false` until the required records exist, the evidence is bound to the exact package and provider, all unresolved rows
are excluded or cleared, and the authorized owners sign. A completed form is evidence to review; it does not automatically change the
manifest. The 522-row package is the smallest current review target, but it still needs its own exact generation, provider-terms,
seed-rights/privacy and content-bound human review evidence.

## Internal ownership and escalation path (repository-only discovery)

The repository identifies current operational and privacy/security role holders, but it does not identify an authorized source-rights/legal approver:

| Decision | Discoverable owner / route | Scope and limitation |
|---|---|---|
| Dataset source inventory | `ai/docs/dataset-source-review.md` is the human sign-off procedure; its sign-off block is blank. `ai/data/source_family_*_manifest.yaml` and `ai/data/source_dossier_manifest.yaml` are explicitly proposals. Git history shows the August 2026 source-family manifest work authored by Steiner (`dagger@pixelated.love`, commit `79952274a`), but authorship is not a current ownership or approval delegation. | Curator maps candidate rows to immutable sources; source owner/rightsholder and the project's authorized rights reviewer decide per source/version. No named rights approver found. Third-party rights can only be evidenced by the applicable rightsholder/license/authorized agreement, not by repository ownership. |
| Privacy / consent | **Chad (interim), current HIPAA Privacy Officer and HIPAA Security Officer** per `docs/enterprise/hipaa-officer-designations.md` (effective 2026-08-01). `.github/PULL_REQUEST_TEMPLATE.md` asks authors to state privacy/clinical impact; `.github/ISSUE_TEMPLATE/release-0-dataset.md` requires privacy, provenance, and human signoff gates. | Current role assignment is distinct from a campaign-specific review. Obtain Chad's privacy/security decision bound to the exact artifact hash; no such decision is recorded yet. |
| Clinical quality / release review | **Vivi (current project experiment owner and sole clinical reviewer for now)**, confirmed by the project owner; recorded in `fireworks-readiness.md` and `fireworks-approval-packages.md`. Additional credentialed reviewers are required before release consideration; automated checks cannot certify safety. | Current role does not itself constitute clinical review or release approval for this candidate. Record Vivi's review against the exact artifact; name additional credentialed reviewers before release consideration. |
| Training execution / stop decisions | **Vivi (current experiment/training owner)**, with execution, budget, reporting, and stop/rollback responsibility. Root `.github/CODEOWNERS` assigns all paths to `@daggerstuff`; no separate training-data owner is listed. | This current role authorizes operational ownership, not source rights, privacy, or clinical clearance. The 2026-10-10 dataset-specific approvals do not cover the 190,139-row recovery candidate, 522-row G03 package, or different provider. |

**Minimum routing to unblock:** the project owner (Vivi, per the existing project record) should open or sponsor a
`datasets` / `ai` / `compliance` decision item using `.github/ISSUE_TEMPLATE/release-0-dataset.md`, then request review from the
`@daggerstuff` CODEOWNER. Name (1) the source-rights reviewer authorized to resolve each source/version, (2) the privacy/compliance
reviewer, (3) the dataset curator who will bind decisions to row-reference hashes, and (4) credentialed clinical reviewer(s) if
clinical-quality or release claims are sought. Attach this packet and the metadata-only audit; keep the upload gate closed until
written decisions and evidence are recorded. This is a proposed internal route only: no issue was created and no one was contacted.

**Current role assignments:** Vivi is the current project experiment/training owner and sole clinical reviewer for now; Chad (interim) is the
current HIPAA Privacy Officer and HIPAA Security Officer. These assignments do not approve this dataset or provider. They do not confer
source-rights authority on Vivi or expand Chad's documented officer remit into a source-license grant. A source-rights/legal approver
remains unassigned in the inspected records.
