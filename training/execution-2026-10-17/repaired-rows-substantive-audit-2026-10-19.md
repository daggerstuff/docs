# Substantive audit of the 52 repaired candidate rows

**Scope:** local deterministic checks only. Candidate and repair text was inspected in-process; this report contains no row text, row identifiers, names, or PHI. No provider calls were made and no candidate or release payload was changed.

## Structural and binding evidence

- Candidate: 190,139 rows; pinned hash match: `True` (`4f0fd4c5fcfdffeb5434057ff4e122356256f9775540a3b41c1421a75e507663`).
- Repair overlay: 52 rows; pinned hash match: `True` (`17308c80a2eb332774d3549a2ef0260bdfabac6f53044cc0160880e166a7238a`).
- Repair kinds: `{"source_dialogue_recovery_with_generated_continuation": 50, "source_quality_triage_reconstruction": 2}`.
- Exact candidate-row hash bindings: 52/52; v2 internal-release row/hash/kind bindings: 52/52; expected-source-label checks: 52/52.
- Role sequences: `{"system/user/assistant": 50, "user/assistant": 2}`. Generation provenance: `{"explicitly_not_human_reviewed": 50, "wandb-inference:Qwen/Qwen3.6-35B-A3B": 50}`.
- Prompt/context markers: `{"labeled_source_pair_embedded": 50, "original_system_prefix_preserved": 50, "triage_disposition_explicit": 2}`.

These checks confirm that the repair sidecar is the one pinned into the local v2 release and that its messages have the expected structural roles. They do not establish that a generated answer is substantively suitable.

## Deterministic text-quality indicators

- Automated issue-class counts: `{}`. No listed issue class was observed when absent from this object.
- Generated target lengths (characters): `{"max": 440, "median": 188.0, "min": 60, "n": 50}`; Latin-token counts: `{"max": 83, "median": 35.0, "min": 0, "n": 50}`.
- Source-pair match similarity (damaged input pair to pinned source): overall `{"max": 1.0, "median": 1.0, "min": 0.8571, "n": 50}`, counselor `{"max": 1.0, "median": 1.0, "min": 0.7143, "n": 50}`, client `{"max": 1.0, "median": 1.0, "min": 0.8889, "n": 50}`.
- Generated-target character-trigram overlap with embedded client excerpt: `{"max": 0.3659, "median": 0.1151, "min": 0.0, "n": 50}`; with counselor excerpt: `{"max": 0.331, "median": 0.0766, "min": 0.0, "n": 50}`. Below 0.01: client 6, counselor 6.
- Exact duplicate generated targets (excess / pairs): 0 / 0; near-duplicate target pairs at SequenceMatcher ≥0.90: 0.

Source-pair similarity verifies recovery of the damaged input turns from the pinned source. Character-trigram overlap is only a weak continuity indicator: low or high overlap can occur in appropriate or inappropriate answers. These metrics cannot determine whether an answer follows the client’s context, language, safety needs, or therapeutic substance.

## Substantive findings and actionable issue classes

1. **Generated continuation review:** 50 rows contain model-generated continuations from W&B inference (Qwen/Qwen3.6-35B-A3B, temperature 0) and are explicitly marked `not_human_reviewed`. The deterministic check found no empty/placeholder target, generic-advice/refusal phrase, or exact/near duplicate; target length and source-overlap distributions are reported above. These checks do not assess context fit or clinical content. Next, run a batch evaluator against each embedded source excerpt for relevance, unsupported assumptions, diagnosis/medical advice, crisis safety, language consistency, and repetition; bind exceptions privately by row hash. Clinical validation remains separate.
2. **Task-family mismatch:** 2 rows are source-quality triage reconstructions about incomplete/promotional source records, not counseling exchanges. They are structurally valid user/assistant pairs but should be separated into a source-curation task family or excluded from a clinical-response SFT view; mixing them into counseling-response training teaches a different task.
3. **Source continuity:** all 50 source-recovery rows contain the builder’s labeled counselor/client excerpt and continuation instruction; input pair match scores and generated-target overlap are reported above. This establishes that context was supplied to generation, not that the answer responds correctly.
4. **Review status:** this audit finds no evidence of human clinical review, rights clearance, privacy clearance, or consent determination. Do not describe the 52 rows as clinically validated or independently cleared for provider transfer.

## Reproduction

The aggregate report was generated from `ai/data/curated/recovery/gold-20261017/train_master_gold.recovered_candidate.jsonl`, `wandb-full-corpus-repairs-20261018/row_repairs.jsonl`, and `wandb-full-corpus-20261018-v2/manifest_internal.jsonl` by a local Python 3 one-off audit. The candidate and release inputs remain unchanged.

## Limitations

- Text-level checks are deterministic heuristics; lexical overlap does not prove semantic relevance or counseling quality.
- No clinical validation, clinician review, rights clearance, privacy clearance, or consent determination is performed.
- Two source-quality triage examples are not clinical counseling examples and should be handled as a separate task family.
- The 50 generated continuations are model-generated and explicitly marked not human reviewed.
