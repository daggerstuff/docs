# Candidate adapter declaration enrichment (2026-10-19)

A read-only verification matched three previously unmapped source labels in the pinned candidate to exact adapter registrations and emitted `source` values. An additive private sidecar was created for their rowrefs; no candidate, split payload, worklist, or existing rowref ledger was changed. No message text or clinical row content is included.

| Candidate label | Rows | Adapter | Adapter-declared upstream locator | Adapter SHA-256 |
|---|---:|---|---|---|
| `counseling_conversations` | 1,415 | `ai/sourcing/dataset_adapters/counseling_conversations_adapter.py` | `https://huggingface.co/datasets/Amod/mental_health_counseling_conversations` (`Amod/mental_health_counseling_conversations`) | `22caf7afa1f971e055dcc1b4bbdc59a34d17799c697428f2a9f1577e1dc56a7e` |
| `crisis_benchmark` | 1,522 | `ai/sourcing/dataset_adapters/crisis_benchmark_adapter.py` | `https://huggingface.co/datasets/arnaiztech/llms-mental-health-crisis-benchmark` (`arnaiztech/llms-mental-health-crisis-benchmark`) | `7ae485bd5e656cfecbcb005691e393ae87bf0b3d7cba0eab73ae83b96ac932b7` |
| `ml_bpd` | 100 | `ai/sourcing/dataset_adapters/ml_bpd_adapter.py` | `https://github.com/saidejp/machine_learning_BPD` (`https://github.com/saidejp/machine_learning_BPD.git`) | `a65ec3e059e4000a7006f7a4ada73a8120c2d8a76984cbe7df438851df65ff77` |
| **Total** | **3,037** | | | |

For all three, AST inspection confirmed one adapter registration under the candidate label, the adapter's emitted `source` value is that same label, and a source URL constant is declared. The exact current candidate contains the stated row counts. All 3,037 rowrefs bind to unique one-based candidate row numbers and match the existing source-decision-ledger raw-row and canonical-message hashes; each sidecar row also matches its current adapter-file SHA.

The original 3,037-row sidecar is strictly `adapter_source_declaration_only`, with status `upstream_row_locator_unbound`. It shows that local adapter code declares these upstream locations and emits these labels; by itself it does not prove the candidate rows came from those upstream records. A later exact-content check upgrades the `ml_bpd` subset only: all 100 candidate user messages and assistant severity labels match the corresponding public CSV content and the adapter's BDI threshold rule. Fifty-six prompts map to a unique CSV row; 44 have duplicate prompt text across multiple rows, all with the same severity class. The candidate system messages differ from the current adapter, so the complete chat records are not exact source-render matches. See the separate private binding report below. Rights, privacy, clinical, and provider-transfer determinations remain open for all three source families; existing worklist decisions remain unchanged.

The private sidecar is `ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/adapter_rowrefs.jsonl`; its manifest is beside it. The directory is mode 0700 and both files are mode 0600. The directory is gitignored by the `ai` submodule's curated-data ignore rule. Sidecar SHA-256: `3facb706bf88482a4df3b09312ee676c95fd2036df73cc216e9e304e5f898c58`. Private manifest SHA-256: `882e6ea900a5b15c7c84fe9776e1df47b7f38c925b20564fc0bd4861a1790a46`.

## Reproduction checks

From repository root, these commands expose only metadata and hashes:

```sh
sha256sum ai/data/curated/recovery/gold-20261017/train_master_gold.recovered_candidate.jsonl \
  docs/training/execution-2026-10-17/source-decision-ledger.jsonl \
  ai/sourcing/dataset_adapters/counseling_conversations_adapter.py \
  ai/sourcing/dataset_adapters/crisis_benchmark_adapter.py \
  ai/sourcing/dataset_adapters/ml_bpd_adapter.py \
  ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/adapter_rowrefs.jsonl
stat -c '%a %n' ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019 \
  ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/adapter_rowrefs.jsonl \
  ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/manifest.json
```

The metadata-only validator parsed the candidate and ledger, recomputed SHA-256 for each selected raw row and canonical `messages` object, checked label equality and unique row numbers, and rehashed all three adapter files. Result: 3,037/3,037 passed; source row text was not emitted.

The additional `ml_bpd` source-content join is recorded privately at
`ai/data/curated/recovery/gold-20261017/private-source-adapter-enrichment-20261019/ml_bpd-upstream-binding-report-2026-10-19.json`.
It pins repository commit `41a6535acbd5389766d18882e9b9b20ca89660ea`,
all four upstream CSV hashes, candidate/adapter row hashes, and exact-match
counts. No raw clinical content or score values are in the report.
