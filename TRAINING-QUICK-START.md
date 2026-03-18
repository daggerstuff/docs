# Training Pipeline Quick Start

## 🚀 Run the Pipeline (30 seconds)

```bash
python scripts/run-integrated-training-pipeline.py
```

**That's it!** Strict mode is enabled by default.

## ✅ What You'll Get

```
ai/training_data_consolidated/final/
├── MASTER_STAGE_MANIFEST.json
├── run_provenance.json
└── splits/
    ├── train.jsonl (aggregate)
    ├── val.jsonl (aggregate)
    ├── test.jsonl (aggregate)
    ├── stage1_foundation/
    ├── stage2_therapeutic_expertise/
    ├── stage3_edge_stress_test/
    └── stage4_voice_persona/
```

## 🔍 Verify Outputs

```bash
# Check files exist
ls -la ai/training_data_consolidated/final/splits/

# Count samples
wc -l ai/training_data_consolidated/final/splits/*.jsonl

# View provenance
cat ai/training_data_consolidated/final/run_provenance.json | jq '.'
```

## ⚙️ Development Mode (Non-Strict)

```bash
# Allow missing artifacts
python scripts/run-integrated-training-pipeline.py --allow-missing-artifacts

# Allow stage drift
python scripts/run-integrated-training-pipeline.py --allow-drift

# Disable all strict checks
python scripts/run-integrated-training-pipeline.py --non-strict
```

## 🛑 Troubleshooting

### "Required stage artifacts missing"

**Solution 1: Create the artifacts**
```bash
python -m ai.pipelines.edge_case.generator
python -m ai.pipelines.orchestrator.prompt_corpus_builder
python -m ai.pipelines.voice.tim_fletcher_extractor
python -m ai.pipelines.transcript_consolidator
```

**Solution 2: Override strict mode (dev only)**
```bash
python scripts/run-integrated-training-pipeline.py --allow-missing-artifacts
```

### "Stage distribution drift exceeds tolerance"

**Solution 1: Adjust manifest**
```bash
# Edit ai/data/training_policy_manifest.json
# Adjust target_percentage values
```

**Solution 2: Override strict mode (dev only)**
```bash
python scripts/run-integrated-training-pipeline.py --allow-drift
```

## 📚 Full Documentation

- [Strict Mode Guide](docs/guides/developers/strict-mode-training.md)
- [Execution Runbook](docs/guides/developers/pipeline-execution-runbook.md)
- [Implementation Summary](docs/implementation-summary-2026-03-17.md)

## 🎯 What is Strict Mode?

**Strict Mode (default):**
- ✅ Validates all required Stage 3/4 artifacts exist
- ✅ Validates stage distribution drift < 2%
- ✅ Fails on any quality validation errors
- ✅ Produces run provenance metadata

**Non-Strict Mode (dev only):**
- ⚠️ Logs warnings instead of failing
- ⚠️ Allows missing artifacts
- ⚠️ Allows stage distribution drift
- ⚠️ May produce partial-quality datasets

## 🔗 Related Work Items

- [#1: Execute full integrated training pipeline](https://gitlab.com/fatdogit/pixelated/-/work_items/1)
- [#11: Document and enforce strict mode](https://gitlab.com/fatdogit/pixelated/-/work_items/11)
- [#3: Add CI checks for split artifacts](https://gitlab.com/fatdogit/pixelated/-/work_items/3)
- [#2: Implement Asana/Jira updater](https://gitlab.com/fatdogit/pixelated/-/work_items/2)
