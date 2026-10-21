# Long-context therapy recreation — available source data

The original `training/v1/stage1_foundation/curated/` directory (the long_context therapy
SFT source) is not recoverable from any backup. The following therapy/counseling data
IS in r2:pixel-archive and can be used to recreate a long-context therapy set:

- **master_work (cleaned conversation masters)** — 457 files, 6.27 GiB
- **reddit_mental_health_phases (pipeline outputs)** — 16 files, 5.98 GiB
- **Empath (empathetic_dialogues)** — 247 files, 2.63 GiB
- **other mental-health data** — 104 files, 1.86 GiB
- **curated (sft_chatml / sft_alpaca / safety sets)** — 13 files, 1.15 GiB
- **kokorochat** — 2 files, 0.23 GiB
- **long_running_therapy (69.5 MB multi-session)** — 3 files, 0.07 GiB
- **DAIC-WOZ (real therapist-patient sessions)** — 4 files, 0.04 GiB
- **SoulChat2.0** — 1 files, 0.04 GiB
- **Psycheval** — 1 files, 0.02 GiB
- **mental_health_counseling_conversations** — 2 files, 0.00 GiB
- **mitch_hamidi_bpd_nlp** — 2 files, 0.00 GiB
- **VERA-MH** — 8 files, 0.00 GiB
- **LLAMA3_Mental_Counseling_Data** — 1 files, 0.00 GiB

Total therapy-related data files: 861, 18.30 GiB

Largest single sources:
- 1.82 GiB — pixeldata/archive/gdrive/raw/untar/root/pixelated/ai/pipelines/data/processed/phase_4_reddit_mental_health/task_5_27_condition_specific/condition_specific_conversations.jsonl
- 1.18 GiB — pixeldata/archive/gdrive/raw/untar/root/pixelated/ai/pipelines/data/processed/phase_4_reddit_mental_health/task_5_32_control_groups/control_group_conversations.jsonl
- 1.17 GiB — pixeldata/archive/gdrive/raw/untar/root/pixelated/ai/pipelines/data/processed/phase_4_reddit_mental_health/task_5_29_temporal_analysis/temporal_analysis_conversations.jsonl
- 0.89 GiB — pixeldata/archive/gdrive/raw/untar/root/pixelated/ai/pipelines/data/processed/phase_4_reddit_mental_health/task_5_28_specialized_populations/specialized_populations_conversations.jsonl
- 0.88 GiB — pixeldata/archive/gdrive/raw/untar/root/pixelated/ai/pipelines/data/processed/phase_4_reddit_mental_health/task_5_33_tfidf_integration/ml_ready_conversations.jsonl
- 0.54 GiB — whitebat/training/pixelated-empathy/ingestion/master_work/pixelated_v6_SPECIALIZED_RESEARCH_MASTER.jsonl
- 0.54 GiB — whitebat/training/pixelated-empathy/ingestion/master_work/pixelated_v5_RESEARCH_MASTER.jsonl
- 0.52 GiB — whitebat/training/pixelated-empathy/ingestion/master_work/pixelated_v5_REAL_MASTER.jsonl
- 0.45 GiB — whitebat/training/pixelated-empathy/output/psycheval/output/psycheval_ingested.jsonl
- 0.42 GiB — whitebat/training/pixelated-empathy/ingestion/kaggle/synthetic_therapy/train.csv
- 0.35 GiB — whitebat/training/pixelated-empathy/curated/sft_chatml/train.jsonl
- 0.32 GiB — whitebat/training/pixelated-empathy/ingestion/master_work/master_dataset_merged_deslopped.jsonl
- 0.32 GiB — whitebat/training/pixelated-empathy/ingestion/master_work/master_dataset_PERFECT_CLEAN.jsonl
- 0.32 GiB — whitebat/training/pixelated-empathy/ingestion/master_work/master_dataset_100pct_clean.jsonl
- 0.31 GiB — whitebat/training/pixelated-empathy/ingestion/master_work/pixelated_v5_1M_master.jsonl

Notes:
- long_running_therapy.jsonl (69.5 MB, multi-session therapy conversations) is the closest
  match to the original curated set and is already in pixel-archive at
  pixeldata/gdrive/processed/long_running_therapy/ (plus a 370 KB processed variant and a
  1.7 MB judged variant, and a 4.5 MB professional_therapeutic variant).
- The master_work pipeline scripts exist in the ai repo to re-run curation.
- The judged_and_cleaned MASTER_TRAINING_SET (4.96 + 4.87 GiB, salvaged from
  pixeldata-ugly-cleaned) is a quality-filtered master suitable as recreation input.