# Strict Mode Training: Production Safety & Quality Enforcement

## Overview

**Strict Mode** is the default production configuration for the Pixelated Empathy training pipeline. It enforces mandatory quality and completeness checks to prevent partial-quality datasets from entering production.

**Status**: ✅ Enabled by default as of 2026-03-17

## What Strict Mode Enforces

### 1. **Artifact Preflight Validation** (`fail_on_missing_stage_artifacts=True`)

Before any training run, the pipeline validates that all required Stage 3 and Stage 4 assets exist:

**Stage 3 (Edge Stress Test) requires:**
- `ai/pipelines/edge_case/output/edge_cases_training_format.jsonl` — Edge case corpus
- `ai/pipelines/orchestrator/prompt_corpus` — Scenario prompt library

**Stage 4 (Voice Persona) requires:**
- `ai/data/tim_fletcher_voice` — Voice signature data
- `ai/training_data_consolidated/transcripts` — Transcript corpus

**Behavior:**
- ✅ **Strict Mode (default)**: Raises `RuntimeError` if any required artifact is missing
- ⚠️ **Non-strict mode**: Logs warnings and continues (may produce partial-quality datasets)

### 2. **Stage Distribution Drift Validation** (`fail_on_stage_drift=True`)

After training data is balanced, the pipeline validates that the final stage distribution matches policy targets within a 2% tolerance:

**Policy targets** (from `ai/data/training_policy_manifest.json`):
- Stage 1 (Foundation): 40%
- Stage 2 (Therapeutic Expertise): 25%
- Stage 3 (Edge Stress Test): 20%
- Stage 4 (Voice Persona): 15%

**Behavior:**
- ✅ **Strict Mode (default)**: Raises `RuntimeError` if drift exceeds 2%
- ⚠️ **Non-strict mode**: Logs warnings and continues (curriculum balance may be affected)

## Environment Variables

### Production (Default)

```bash
# Strict mode is ON by default
# No environment variables needed
```

### Development/Testing (Override Only)

```bash
# Disable ALL strict checks (logs warnings instead of failing)
export TRAINING_STRICT_MODE=false

# Allow missing Stage 3/4 artifacts (still in strict mode)
export TRAINING_ALLOW_MISSING_ARTIFACTS=true

# Allow stage distribution drift (still in strict mode)
export TRAINING_ALLOW_STAGE_DRIFT=true
```

## Execution Examples

### Production Run (Strict Mode)

```bash
# Strict mode enabled by default
python -m ai.pipelines.orchestrator.orchestration.integrated_training_pipeline

# Expected behavior:
# ✅ STRICT MODE ENABLED (production default)
#    - fail_on_stage_drift: True
#    - fail_on_missing_stage_artifacts: True
# ✅ All required stage artifacts present
# ✅ Stage distribution within tolerance
# ✅ Integration Complete!
```

### Development Run (Non-Strict Mode)

```bash
# Disable strict checks for testing
export TRAINING_STRICT_MODE=false
python -m ai.pipelines.orchestrator.orchestration.integrated_training_pipeline

# Expected behavior:
# ⚠️  STRICT MODE DISABLED via TRAINING_STRICT_MODE=false.
#    This may produce partial-quality datasets. Use only for testing.
# ⚠️  NON-STRICT MODE: Continuing despite missing artifacts.
#    Dataset quality may be reduced.
```

### Partial Override (Allow Missing Artifacts Only)

```bash
# Keep strict mode ON, but allow missing Stage 3/4 artifacts
export TRAINING_ALLOW_MISSING_ARTIFACTS=true
python -m ai.pipelines.orchestrator.orchestration.integrated_training_pipeline

# Expected behavior:
# ✅ STRICT MODE ENABLED (production default)
# ⚠️  TRAINING_ALLOW_MISSING_ARTIFACTS=true.
#    Stage 3/4 artifacts may be missing. Dataset quality may be reduced.
# ✅ Stage distribution within tolerance
```

## CI/CD Integration

### GitHub Actions / GitLab CI

All training pipeline runs in CI **must** use strict mode:

```yaml
# .github/workflows/training-pipeline.yml
jobs:
  training:
    runs-on: ubuntu-latest
    env:
      # Strict mode is default; no override needed
      TRAINING_STRICT_MODE: "true"  # Explicit for clarity
    steps:
      - name: Run integrated training pipeline
        run: |
          python -m ai.pipelines.orchestrator.orchestration.integrated_training_pipeline
```

**CI will fail if:**
- Required Stage 3/4 artifacts are missing
- Stage distribution drifts >2% from policy targets
- Any quality validation fails

## Troubleshooting

### Error: "Required stage artifacts missing"

**Cause**: Strict mode is enabled and required assets don't exist.

**Solutions**:
1. **Recommended**: Create the missing artifacts
   ```bash
   # For Stage 3
   python -m ai.pipelines.edge_case.generator
   python -m ai.pipelines.orchestrator.prompt_corpus_builder
   
   # For Stage 4
   python -m ai.pipelines.voice.tim_fletcher_extractor
   python -m ai.pipelines.transcript_consolidator
   ```

2. **Development only**: Override strict mode
   ```bash
   export TRAINING_ALLOW_MISSING_ARTIFACTS=true
   python -m ai.pipelines.orchestrator.orchestration.integrated_training_pipeline
   ```

### Error: "Stage distribution drift exceeds tolerance"

**Cause**: Final dataset has >2% drift from policy targets.

**Solutions**:
1. **Recommended**: Adjust sampling ratios in `ai/data/training_policy_manifest.json`
2. **Development only**: Override strict mode
   ```bash
   export TRAINING_ALLOW_STAGE_DRIFT=true
   python -m ai.pipelines.orchestrator.orchestration.integrated_training_pipeline
   ```

## Audit Trail

All strict mode decisions are logged:

```
✅ STRICT MODE ENABLED (production default)
   - fail_on_stage_drift: True
   - fail_on_missing_stage_artifacts: True
✅ All required stage artifacts present
✅ Stage distribution within tolerance
```

Non-strict overrides are logged with warnings:

```
⚠️  STRICT MODE DISABLED via TRAINING_STRICT_MODE=false.
    This may produce partial-quality datasets. Use only for testing.
```

## Related Work Items

- [#11](https://gitlab.com/fatdogit/pixelated/-/work_items/11) Document and enforce strict mode as default for production training runs
- [#1](https://gitlab.com/fatdogit/pixelated/-/work_items/1) Execute full integrated training pipeline with real datasets and strict artifact mode

## See Also

- [Training Policy Manifest](../../ai/data/training_policy_manifest.json)
- [Integrated Training Pipeline](../../ai/pipelines/orchestrator/orchestration/integrated_training_pipeline.py)
- [Training Gap-Closure Audit](../audits/2026-03-17-training-gap-closure-execution-audit.md)
