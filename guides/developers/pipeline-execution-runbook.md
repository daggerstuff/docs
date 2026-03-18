# Integrated Training Pipeline Execution Runbook

## Quick Start

```bash
# Production run (strict mode enabled by default)
python scripts/run-integrated-training-pipeline.py

# Development run (non-strict mode)
python scripts/run-integrated-training-pipeline.py --non-strict

# Allow missing artifacts only
python scripts/run-integrated-training-pipeline.py --allow-missing-artifacts
```

## Prerequisites

### 1. Environment Setup

```bash
# Ensure Python 3.11+ is available
python --version

# Install dependencies
uv sync

# Activate virtual environment (if using venv)
source .venv/bin/activate
```

### 2. Required Data Assets

The pipeline requires these directories to exist (for strict mode):

**Stage 3 (Edge Stress Test):**
```
ai/pipelines/edge_case/output/edge_cases_training_format.jsonl
ai/pipelines/orchestrator/prompt_corpus/
```

**Stage 4 (Voice Persona):**
```
ai/data/tim_fletcher_voice/
ai/training_data_consolidated/transcripts/
```

**Check availability:**
```bash
ls -la ai/pipelines/edge_case/output/
ls -la ai/pipelines/orchestrator/prompt_corpus/
ls -la ai/data/tim_fletcher_voice/
ls -la ai/training_data_consolidated/transcripts/
```

### 3. Configuration

**Policy manifest** (`ai/data/training_policy_manifest.json`):
- Defines stage distribution targets (40%, 25%, 20%, 15%)
- Defines per-stage quality profiles
- Defines crisis override policies

**Verify manifest:**
```bash
cat ai/data/training_policy_manifest.json | jq '.stages'
```

## Execution Modes

### Production Mode (Strict)

```bash
python scripts/run-integrated-training-pipeline.py
```

**Behavior:**
- ✅ Validates all required Stage 3/4 artifacts exist
- ✅ Validates stage distribution drift < 2%
- ✅ Fails on any quality validation errors
- ✅ Produces run provenance metadata

**Expected output:**
```
✅ STRICT MODE ENABLED (production default)
   - fail_on_stage_drift: True
   - fail_on_missing_stage_artifacts: True
✅ All required stage artifacts present
✅ Stage distribution within tolerance
✅ PIPELINE EXECUTION SUCCESSFUL
```

### Development Mode (Non-Strict)

```bash
python scripts/run-integrated-training-pipeline.py --non-strict
```

**Behavior:**
- ⚠️ Logs warnings instead of failing
- ⚠️ Allows missing Stage 3/4 artifacts
- ⚠️ Allows stage distribution drift
- ⚠️ May produce partial-quality datasets

**Use cases:**
- Testing pipeline logic without all data assets
- Debugging data loading issues
- Smoke testing on limited datasets

### Partial Overrides

```bash
# Allow missing artifacts, but enforce stage drift
python scripts/run-integrated-training-pipeline.py --allow-missing-artifacts

# Allow drift, but enforce artifact presence
python scripts/run-integrated-training-pipeline.py --allow-drift
```

## Execution Steps

### Step 1: Verify Prerequisites

```bash
# Check Python version
python --version  # Should be 3.11+

# Check data assets
python -c "
from pathlib import Path
assets = [
    'ai/pipelines/edge_case/output/edge_cases_training_format.jsonl',
    'ai/pipelines/orchestrator/prompt_corpus',
    'ai/data/tim_fletcher_voice',
    'ai/training_data_consolidated/transcripts',
]
for asset in assets:
    p = Path(asset)
    status = '✅' if p.exists() else '❌'
    print(f'{status} {asset}')
"
```

### Step 2: Run Pipeline

```bash
# Start execution
python scripts/run-integrated-training-pipeline.py

# Monitor output
# - Watch for ✅ checkmarks (success)
# - Watch for ⚠️ warnings (non-strict mode)
# - Watch for ❌ errors (failures)
```

### Step 3: Validate Outputs

```bash
# Check output directory structure
tree ai/training_data_consolidated/final/

# Verify split files exist and are non-empty
wc -l ai/training_data_consolidated/final/splits/*.jsonl

# Verify manifest
cat ai/training_data_consolidated/final/MASTER_STAGE_MANIFEST.json | jq '.'

# Check run provenance
cat ai/training_data_consolidated/final/run_provenance.json | jq '.'

# Check checklist
cat ai/lightning/training_run_checklist.json | jq '.'
```

### Step 4: Review Metrics

```bash
# Extract key metrics
python -c "
import json
from pathlib import Path

# Load provenance
with open('ai/training_data_consolidated/final/run_provenance.json') as f:
    prov = json.load(f)

print('Run Provenance:')
print(f'  Type: {prov[\"run_type\"]}')
print(f'  Timestamp: {prov[\"run_timestamp\"]}')
print(f'  Total samples: {prov[\"dataset_size\"]}')
print(f'  Strict mode: {prov[\"strict_mode_enabled\"]}')

# Load checklist
with open('ai/lightning/training_run_checklist.json') as f:
    checklist = json.load(f)

print(f'\nChecklist:')
print(f'  Total samples: {checklist.get(\"total_samples\", 0)}')
print(f'  Stage distribution: {checklist.get(\"stage_distribution\", {})}')
"
```

## Output Artifacts

### Directory Structure

```
ai/training_data_consolidated/final/
├── MASTER_STAGE_MANIFEST.json          # Stage metadata and metrics
├── run_provenance.json                 # Run type, timestamp, dataset size
└── splits/
    ├── train.jsonl                     # Aggregate training split
    ├── val.jsonl                       # Aggregate validation split
    ├── test.jsonl                      # Aggregate test split
    ├── stage1_foundation/
    │   ├── train.jsonl
    │   ├── val.jsonl
    │   └── test.jsonl
    ├── stage2_therapeutic_expertise/
    │   ├── train.jsonl
    │   ├── val.jsonl
    │   └── test.jsonl
    ├── stage3_edge_stress_test/
    │   ├── train.jsonl
    │   ├── val.jsonl
    │   └── test.jsonl
    └── stage4_voice_persona/
        ├── train.jsonl
        ├── val.jsonl
        └── test.jsonl

ai/lightning/
├── training_run_checklist.json         # Operational checklist
└── training_dataset.json               # Full integrated dataset
```

### File Formats

**MASTER_STAGE_MANIFEST.json:**
```json
{
  "stages": {
    "stage1_foundation": {
      "target_share": 0.4,
      "actual_samples": 3200,
      "actual_share": 0.4,
      "quality_profile": {...}
    },
    ...
  },
  "split_stats": {
    "train": {"total": 6400, "by_stage": {...}},
    "val": {"total": 1600, "by_stage": {...}},
    "test": {"total": 1000, "by_stage": {...}}
  }
}
```

**run_provenance.json:**
```json
{
  "run_type": "production",
  "run_timestamp": "2026-03-17T12:00:00+00:00",
  "dataset_size": 8000,
  "stage_distribution": {
    "stage1_foundation": 3200,
    "stage2_therapeutic_expertise": 2000,
    "stage3_edge_stress_test": 1600,
    "stage4_voice_persona": 1200
  },
  "strict_mode_enabled": {
    "fail_on_stage_drift": true,
    "fail_on_missing_stage_artifacts": true
  },
  "warnings": [],
  "errors": []
}
```

## Troubleshooting

### Error: "Required stage artifacts missing"

**Cause**: Strict mode is enabled and required assets don't exist.

**Solution 1: Create missing artifacts**
```bash
# For Stage 3
python -m ai.pipelines.edge_case.generator
python -m ai.pipelines.orchestrator.prompt_corpus_builder

# For Stage 4
python -m ai.pipelines.voice.tim_fletcher_extractor
python -m ai.pipelines.transcript_consolidator
```

**Solution 2: Override strict mode (development only)**
```bash
python scripts/run-integrated-training-pipeline.py --allow-missing-artifacts
```

### Error: "Stage distribution drift exceeds tolerance"

**Cause**: Final dataset has >2% drift from policy targets.

**Solution 1: Adjust sampling ratios**
```bash
# Edit ai/data/training_policy_manifest.json
# Adjust target_percentage values for each stage
```

**Solution 2: Override strict mode (development only)**
```bash
python scripts/run-integrated-training-pipeline.py --allow-drift
```

### Error: "Quality validation failed"

**Cause**: Data samples don't meet quality thresholds.

**Solution:**
```bash
# Check quality profile thresholds
cat ai/data/training_policy_manifest.json | jq '.stages[].quality_profile'

# Review quality validation logs
grep -i "quality\|bias\|safety" logs/training_pipeline.log

# Adjust quality thresholds in manifest if needed
```

### Pipeline runs but produces empty outputs

**Cause**: Data loading failed silently.

**Solution:**
```bash
# Check data source paths
python -c "
from ai.pipelines.orchestrator.orchestration.integrated_training_pipeline import IntegratedPipelineConfig
config = IntegratedPipelineConfig()
for source, cfg in [
    ('edge_cases', config.edge_cases),
    ('pixel_voice', config.pixel_voice),
    ('psychology_knowledge', config.psychology_knowledge),
    ('dual_persona', config.dual_persona),
    ('standard_therapeutic', config.standard_therapeutic),
]:
    print(f'{source}: {cfg.source_path}')
"

# Verify data exists at those paths
ls -la ai/pipelines/edge_case/output/
ls -la ai/pipelines/voice/
# ... etc
```

## Performance Expectations

| Metric | Expected Value |
|--------|-----------------|
| Total samples | 8,000 |
| Execution time | 5-15 minutes |
| Memory usage | <2GB |
| Output size | ~500MB (splits) |

## CI/CD Integration

### GitHub Actions

```yaml
name: Training Pipeline

on: [push, pull_request]

jobs:
  training:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install uv && uv sync
      - run: python scripts/run-integrated-training-pipeline.py
      - uses: actions/upload-artifact@v3
        with:
          name: training-outputs
          path: ai/training_data_consolidated/final/
```

### GitLab CI

```yaml
training_pipeline:
  stage: build
  image: python:3.11
  script:
    - pip install uv && uv sync
    - python scripts/run-integrated-training-pipeline.py
  artifacts:
    paths:
      - ai/training_data_consolidated/final/
    expire_in: 30 days
```

## Related Documentation

- [Strict Mode Training](./strict-mode-training.md)
- [Training Policy Manifest](../../ai/data/training_policy_manifest.json)
- [Training Gap-Closure Audit](../audits/2026-03-17-training-gap-closure-execution-audit.md)
- [Work Item #1: Execute full integrated training pipeline](https://gitlab.com/fatdogit/pixelated/-/work_items/1)
- [Work Item #11: Document and enforce strict mode](https://gitlab.com/fatdogit/pixelated/-/work_items/11)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review pipeline logs: `grep -i error logs/training_pipeline.log`
3. Open an issue with logs and output artifacts attached
