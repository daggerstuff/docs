# Training source rights and privacy audit (metadata only)

**Status:** audit findings only; no data cleared, removed, or approved. **No row contents or PHI were inspected or included.**

## Result

The recovery candidate contains 190,139 row references (SHA-256 `4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`).
The metadata-only evidence inventory found **0 rows with exact signed rights plus privacy/consent clearance bound to the candidate row
references**. It reports source-family manifests as proposed, source-owner sign-off pending, and no campaign-specific signed
privacy/consent/clearance artifact in the paths it scanned. This is an evidence gap, not a determination that every source is
prohibited.

The source-decision ledger covers all 190,139 candidate rows across 475 source labels. Exact normalized alias matching against the five
proposed local source-family manifests maps 177,423 rows to 16 source IDs; 12,716 rows across 459 labels do not match those manifest
aliases. Alias matching is only an inventory join and cannot establish rights. The main matched sources are:

| Source ID | Candidate rows | Local manifest position | Primary-source check / unresolved evidence |
|---|---:|---|---|
| SRC-027 | 70,968 | restricted knowledge extraction; Reddit posts | Reddit's current [Data API Terms](https://redditinc.com/policies/data-api-terms) prohibit using user content to train an ML/AI model absent express permission from the applicable rightsholders. Obtain applicable rights-holder permission and campaign/source-owner review; establish consent/privacy and that acquisition/retention complies with the applicable terms. |
| SRC-030 | 35,977 | restricted knowledge extraction; empathy dialogue corpus | Local manifest traces the data to Reddit. Confirm precise source/version and acquisition path, applicable Reddit terms and rightsholder permissions, plus privacy/consent evidence. |
| SRC-028 | 30,444 | restricted knowledge extraction; Reddit mental-health posts | Same Reddit rights and consent/privacy gap as SRC-027. |
| SRC-031 | 13,890 | restricted knowledge extraction; Reddit BPD NLP | Same Reddit rights and consent/privacy gap as SRC-027. |
| SRC-032 | 11,135 | restricted voice extraction; MentalChat16K | Local manifest gives a paraphrase/restricted-use policy, not campaign-specific permission. Exact upstream dataset membership, license terms, any component-specific restrictions, and privacy/consent remain unverified. |
| SRC-033 | 5,606 | restricted knowledge extraction; generated multi-agent dialogue | Local record labels it GPT-4.1-generated and restricts use. Need generation/provider receipt, applicable output terms, input-source lineage, privacy review and owner decision. |
| SRC-034 | 4,615 | restricted voice extraction; KokoroChat | Local policy is not an exact campaign clearance. Verify model/provider, source lineage, terms, consent/privacy, and exact row binding. |
| SRC-036 | 1,977 | permissive-use claim; synthetic Psycheval | A local label is not primary evidence. Obtain generator/model receipt, output-use terms and seed lineage, then privacy and exact row-binding evidence. |
| SRC-039 | 892 | restricted voice extraction; ESConv | The [official Tsinghua repository](https://github.com/thu-coai/Emotional-Support-Conversation) states that data and code are for academic research use only and all rights reserved. That does not establish permission for this campaign's commercial/non-academic purpose, remote training, or redistribution. Obtain written owner permission and privacy/consent/use-scope evidence. |
| SRC-040 | 892 | restricted voice extraction; PsyDial | Local manifest points to upstream versions with different stated terms. Verify the exact version and governing primary terms, permitted fine-tuning/transfer, privacy/consent and row binding. |
| SRC-041 | 673 | restricted voice extraction; PsyInsight | Verify exact upstream source, license/terms, generated-vs-human lineage, output rights, privacy, and candidate row binding. |
| SRC-046 | 129 | restricted knowledge extraction; DAIC-WOZ | USC ICT's [official DAIC-WOZ page](https://dcapswoz.ict.usc.edu/) says access requires a signed application and, due to consent constraints, distribution is limited to academics and other non-profit researchers. Verify the signed agreement, authorized recipient/use, whether this project qualifies, secondary model-training and vendor-transfer permissions, and participant privacy conditions. |
| SRC-044 | 116 | permissive-use claim; generated DSM vectors | Verify generation receipt, source/version/rights for the DSM material, provider output terms, exact row linkage, and privacy review; the local label alone is insufficient. |
| SRC-047 | 98 | **conflicting local records**: representative registry claims direct-use approval, while source-family manifest marks deprecated/restricted and requires licensing review | The [official AnnoMI repository](https://github.com/uccollab/AnnoMI) makes transcripts available and documents source video URLs, but the repository snapshot has no license text. Public availability is not training permission. Resolve the conflicting local decisions with the source owner and obtain primary license/permission, consent/privacy and exact row binding. |
| SRC-050 | 7 | restricted knowledge extraction; MITAGS | Verify research terms, consent/privacy conditions, permitted model-training and remote transfer, plus exact candidate binding. |
| SRC-051 | 4 | restricted knowledge extraction; HOPE | Verify research terms, consent/privacy conditions, permitted model-training and remote transfer, plus exact candidate binding. |

The 12,716 unmatched rows break down by source-label pattern: 8,107 book/title labels; 980 ARC corpus labels (959 `arc_corpus_arc_*`,
21 pilot labels); 415 creator/persona labels; 100 clinical edge-case labels; 77 `nightmare_fuel_predefined` labels; and 3,037 other
unmatched labels. These figures classify metadata labels only. They do not establish the source identity or rights for any individual
row. Each unmatched label needs source-owner resolution and provenance mapping before a release subset can be assembled.

## Small synthetic branch

The local G03 diagnostics identify a 522-row post-holdout edge-case branch as generated from first-party generator code and accepted
seed artifacts. It remains research-diagnostic-only. The local G04 manifest records generation provider/model and applicable
output-use/remote-training terms as unverified; the clinical-reviewed field is automatically set by code and is not clinician review.
Its basic pattern screen cannot establish absence of PHI. Exact generator receipt, seed/input rights and privacy review, selected
provider transfer/retention terms, golden-control lineage, and human decision content binding remain open. No external transfer or
training is supported by this audit.

## Human decisions and evidence needed

1. The source owner/legal reviewer must resolve source-specific permission and license scope for each source/version, including
   commercial/research fine-tuning and transfer to the named training provider. A generic license manifest or a `permissive-use` field
   does not answer those questions.
2. The privacy/clinical data owner must document lawful/authorized use, participant consent or other applicable authorization,
   de-identification/re-identification risk, sensitive-data status, retention/deletion duties, and whether remote processing is
   permitted. No broad consent evidence was found in the inspected metadata.
3. The data curator must bind each approved decision to exact candidate row references and immutable source/version and artifact
   hashes, resolving all 459 unmatched labels and the SRC-047 conflict. Identity hashes establish row identity only, not permission.
4. The training owner must review the destination provider's current data processing, retention, confidentiality, and training-job
   settings once source clearance is documented.

Until these records exist, no candidate row is identified here as releasable. The audit does not alter the candidate, ledger, source
manifests, or eligibility decisions.

## Evidence basis

- Local metadata: `docs/training/execution-2026-10-17/source-evidence-inventory.json`, `source-eligibility-summary.json`,
  `source-decision-ledger.jsonl`, `g03-generated-source-origin.json`, `g04-release-manifest.json`, and the five source-family manifests
  named in the inventory.
- Public primary sources checked: [Reddit Data API Terms](https://redditinc.com/policies/data-api-terms), [Tsinghua ESConv repository
  README](https://github.com/thu-coai/Emotional-Support-Conversation), [USC ICT DAIC-WOZ access page](https://dcapswoz.ict.usc.edu/),
  and [AnnoMI official repository README](https://github.com/uccollab/AnnoMI).
