# Muse Glimmer experiments — October 13 live recheck

Execution order: adapter/compute access → paired evaluation → one bounded SFT
experiment → task-aligned preference optimization or RL. The user authorized
beginning this sequence on October 13. Preparation below is local; no inference,
training, deployment, upload, or compute start was performed during this recheck.

## 1. Adapter and compute access

Live checks at approximately 11:38–11:41 UTC:

- Fireworks account `linencloset` authenticates through the existing workspace
  API key. The CLI's separate interactive sign-in is absent; REST GETs succeed.
- `wwopccov`: `JOB_STATE_COMPLETED`; model
  `accounts/linencloset/models/arc-pilot-v1-therapist-sft`: `READY`.
- `GET /v1/accounts/linencloset/models/arc-pilot-v1-therapist-sft:getDownloadEndpoint`
  returns HTTP 400, code 9: **“model downloads are temporarily disabled, please
  contact Fireworks AI to get access.”** No weights are available for this eval.
- Account deployment list is empty. No existing hosted endpoint can evaluate
  the tuned model. This check did not provision one.
- Lightning studio `adaption-eval-l4`, ID `01m4np4zwnpxw79gc9v2b5mv1b`, is
  **Stopped**, machine **None**, as confirmed by the Lightning SDK status API.
  A `CLOUD_SPACE_STATE_READY` cloudspace response alone does not mean a GPU is running.
- This host has no NVIDIA device. Starting paid compute before weights are
  available would not unblock the comparison. Current start/billing eligibility
  was not tested by starting a machine.

**Required unblock:** Fireworks must enable model downloads, or the owner must
select a separately costed hosted evaluation route. The support request already
prepared in `fireworks-pilot-log.md` §12.4 can be used; no message was sent.

The actual Glimmer adapter is rank 8 and targets `down_proj`, `gate_proj`,
`k_proj`, `o_proj`, `q_proj`, `up_proj`, and `v_proj`. The prior Qwen adapter's
limited q/v projection coverage is a different experiment and must not determine
the Glimmer recipe. HF metadata reports architecture
`MuseGlimmerForConditionalGeneration`, model type `muse_glimmer`; qualify the
chosen runtime with this architecture before downloading large weights.

## 2. Paired evaluation prepared, inference blocked

New preparation command (from `/home/vivi/hackathon`):

```bash
PYTHONPATH=/home/vivi/pixelated uv run python \
  -m ai.qa.validation.therapy_bench.prepare_glimmer_eval \
  --output /home/vivi/pixelated/ai/training/output/arc_corpus/export/glimmer_eval_20261013
```

That output already exists; use a new output directory for a subsequent snapshot.
The preparer refuses overwrite and hashes all input files before/after reading.
It verifies the frozen pilot's hashes/counts, arc and recorded-group isolation,
and actual generator seed reuse. It keeps references outside the rendered prompt
and pins the provider's training-time date/template.

**Lineage finding:** the v1 manifest's arc-ID fallback for edge cases concealed
seed reuse. `training/arc_plans/seed_map.jsonl`, with `:vN` variation suffixes
normalized, identifies **16 seed groups crossing original split boundaries**.
Eight test arcs (20 session rows) share seeds with train/validation:
`arc_0017`, `arc_0020`, `arc_0191`, `arc_0199`, `arc_0228`, `arc_0230`,
`arc_0006`, `arc_0205`. These are excluded from the new evaluation view.
`pilot_01` has unresolved fallback lineage; it is in the training split, not the
selected test cases. This check establishes recorded seed isolation only, not
absence of semantic overlap or unknown upstream model exposure.

The prepared bundle contains **58 retained final-turn corpus cases + 52 golden
controls = 110 cases**. Cases SHA-256:
`2bd856ac9ba92e169429c51560f283df57a4306f65530274fe22db9ee862fb1f`.
All canonical train/val/test files remain unchanged. The initial unfiltered
preparation was replaced before any inference was run.

After weights and compute are available:

1. Pin runtime, tokenizer/model revision and precision identically across arms.
2. Count prompt tokens and reject context overflow; never silently truncate.
3. Use only each case's `prompt` for inference. Neither `reference` nor
   `expected_behavior` goes into model input.
4. Run five identical case IDs across both arms spanning corpus and controls,
   then all 110 if the smoke succeeds. Decoding: temperature 0, max output 1024,
   stop `<|eot|>`. Flag length-limited completions separately.
5. Persist arm/case ID, prompt hash, response, finish reason, token counts,
   runtime identity and latency after each completion. Resume only identical
   configuration and inputs.
6. Review paired responses for ledger structure **and grounding**, continuity,
   response quality, risk handling and unnecessary crisis escalation on ordinary
   controls. Report by suite/seed with ties and invalid outputs explicit.
   Keyword scores or JSON validity do not establish clinical safety.

There is no inference result or model-quality verdict yet. The preparation
command is a dataset/protocol tool, not an inference backend.

## 3. Bounded second experiment staged, launch gated on evaluation

Declarative proposal:
`ai/training/configs/muse_glimmer_followup.json`. This is deliberately marked
`proposal_only_not_submittable`; it is not a provider API request.

The first candidate changes the audited training data while retaining the
baseline's explicit rank 8, two epochs and 32768 context. No sweep, simultaneous
rank/epoch changes, or automatic promotion. Learning rate, alpha, batch size and
other provider defaults are not established by the baseline job's zero-valued
API fields; resolve them before making a reproducibility claim. Recheck current
costs/promo eligibility rather than extrapolating the prior $0 run.

Read-only corpus snapshot: 422 records, **374 ACCEPT / 48 HR**, versus 235 arcs
in the pilot. Corpus SHA-256:
`1add631f161544007c03946daaca10d4673355f545e3f127a5118bd2e4fd9fe4`.
The 139 newly accepted arcs were screened using plan scenario IDs where present,
otherwise the successful seed-map keys normalized across variation passes:

| Classification | Arcs | Sessions |
| --- | ---: | ---: |
| Seed reserved only for prior training | 85 | 215 |
| New identified seed | 2 | 4 |
| Seed seen in validation/test — exclude | 38 | 101 |
| Ambiguous/missing lineage — exclude pending reconciliation | 14 | 41 |

These are candidate inventory counts, not approved/exported training rows.
Some reused arc IDs have multiple successful seed-map entries; last-wins would
hide that uncertainty. Exclude unresolved rows until reconciled. Rebuild the
training view with validation/test seed reservations applied to **original and
expanded rows**, including originally training-assigned rows in cross-split seed
groups. Do not append blindly to v1 or weaken the frozen exporter's assertions.
Use accepted records only and keep source artifacts unchanged.

## 4. RL readiness assessed, no RL launch

There are **1033 internal preference pairs**: 773 attempt, 202 session, 58 case.
All chosen completions contain whole `[C]`/`[T]` writer transcripts; 975 pairs
explicitly mark reconstructed briefs. The other 58 are case-mode pairs, not
evidence of exact therapist-turn contexts. This is writer preference data,
not provider-ready therapist-response DPO data.

For therapist DPO, preserve exact identical conversation prefixes on both arms,
validate the preference at that turn, and retain seed-level split lineage. Do
not convert transcript strings to one assistant message and call it compatible.
GRPO needs a validated task reward; neither clinical keyword scoring nor ledger
syntax alone is an adequate optimization target. Start from the validated SFT
checkpoint and compare against both base and SFT on the reserved cases.

Meta's [fine-tuning guidance](https://dev.meta.ai/docs/muse-glimmer/fine-tuning)
and [RL guidance](https://dev.meta.ai/docs/muse-glimmer/rl) support the SFT-first,
held-out-comparison sequence. The RL page's illustrative snippets point at the
base model even while its text says to start from SFT; explicitly supply the
actual SFT checkpoint when implementing a follow-on.

## Verification

The preparer and its tests pass targeted Ruff checks. Seven offline tests cover
reference exclusion, pinned dates, immutable source hashes, overwrite refusal,
split leakage, hidden seed reuse, ambiguous lineage, invalid prompt termination,
and reproducibility. Production preparation succeeds with the 110-case bundle.
This verifies preparation only. Training and inference remain unexecuted.
