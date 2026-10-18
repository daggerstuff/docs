# Dataset break-away and free training experiment plan

Date: 2026-10-17. Status: authorized; local execution started, grounded in a local audit and
public provider documentation. No new upload, training, inference, deployment,
or paid resource was started for this plan. Follow-up read-only checks confirmed
Adaption run 2 succeeded and is downloadable; other account eligibility,
balances, and endpoint access still need live verification.

October 17 follow-up: [the discrepancy investigation](gold-discrepancy-investigation-2026-10-17.md)
found 189,159 non-arc rows recoverable from four agreeing backups and 19 sessions
in superseded accepted arc versions. A separate 190,139-row recovery candidate
was verified; active gold remains unchanged. The user confirmed W&B inference
credits and Adaption credits; Fireworks inference credits are tentative.

Execution authorized October 17. The local preflight is complete; continue through the [execution handoff](TRAINING_EXECUTION_HANDOFF.md) and [task
registry](execution-2026-10-17/registry.json). Scope and credit-use authorization persist; provider eligibility and actual cost coverage still require
qualification. Automatic context compaction occurred; the active model has not been switched. Read §9 for the current provider/portable-finish plan; where it
conflicts with older W&B preview statements in §§3 and 8, §9 is authoritative.

## 1. Recommendation

Freeze an independently validated subset of accepted data, then run controlled
experiments on Fireworks, W&B, and Adaption. Use each provider's qualified
inference service for its trained jobs; Adaption export/runtime qualification
is a separate dependency.
Continue unresolved curation separately. Do not wait for the entire acquisition
and human-review backlog, and do not assume that an audit label makes a row
ready for export.

The first milestone is a reproducible dataset release and a base-versus-SFT
comparison. Subsequent milestones test data composition, training settings,
preference alignment, and agent behavior. These experiments should reduce
uncertainty for our eventual full model stack; they cannot guarantee that a
recipe transfers to a larger model or establishes clinical readiness.

## 2. What the audit established

Counts below are a point-in-time read of local files, not a provider job census.
The workspace contains unrelated edits, including the arc generator; preserve
those edits and pin input hashes before subsequent work.

| Artifact | Current observation | Consequence |
| --- | --- | --- |
| `ai/training/output/arc_corpus/arc_records.jsonl` | 421 distinct arcs; 390 `accept` with 981 sessions, 29 without an audit verdict with 76 sessions, 2 `hr` with 5 sessions | Only accepted, reconciled sessions can enter a candidate release |
| `ai/data/curated/sft_chatml/train_master_gold.jsonl` | 980 rows, all accepted arc sessions, covering 390 arcs | Explain the one-session difference from accepted records before packaging |
| October 14 execution log | Reports 190,158 total gold rows | Current file is materially different; reconcile archive, replacement, and source history before declaring the wider dataset finished |
| `human_review_queue.jsonl` | 87 append-log entries, 56 distinct arcs | Entries are not 87 independent cases; reconcile current decisions with queue history |
| `arc_dpo_pairs.jsonl` | 1,122 pairs: 843 attempt, 202 session, 77 case; 1,045 mark reconstructed briefs | This is writer preference inventory, not validated therapist-turn DPO |
| Frozen Fireworks pilot | 418 train / 80 validation / 78 test rows; files match recorded hashes | Preserve as historical v1; do not silently overwrite |
| Existing evaluation bundle | 110 cases, matching its recorded checksum; 58 corpus + 52 controls | Useful historical starting point, not a full scenario benchmark |
| Evaluation lineage | Seed-map hash changed; fresh audit still finds 16 crossing seed groups, 8 excluded test arcs, unresolved `pilot_01` | Rebuild/version the evaluation view and enforce seed reservations across new data |
| `ai/training/configs/muse_glimmer_followup.json` | Zero bytes | Prior documentation describes a proposal that is not currently usable |
| Fireworks pilot job | Log records `wwopccov` completed, output `accounts/linencloset/models/arc-pilot-v1-therapist-sft` ready | Historical completion only; recheck account state and hosted evaluation access |

Arc records, gold, queue, and preference files parsed without malformed JSON.
The main gold file SHA-256 at inspection was
`e3fc508e6c7bec360f9b67e5c963bdf14e2f4e08752c0e6b7900d380a964ace5`;
arc records were
`a3f3d181f86af53522749af0c5a9b72246b45fa60b85ac1d5102600a2844e341`.
Recount if these change; neither count is a release commitment.

Prior work remains useful: the October 15 log records a working reference
checkpoint from Adaption run 2, pending HR decisions, and a Fireworks support
request already sent. Its blind 52-question comparison found mixed results;
the platform win rate and a format-biased heuristic are insufficient promotion
evidence. Preserve it as a historical comparator where technically accessible.

## 3. Provider routes and cost boundaries

Public documentation was checked on October 17. Confirm the exact account,
model, method, promo eligibility, and cost immediately before each launch.

| Lane | Training plan | Inference plan | Eligibility boundary |
| --- | --- | --- | --- |
| Fireworks | Muse Glimmer 30B LoRA SFT first | Same-provider in-session sampling for new Serverless Training jobs; hosted evaluation deployment for the existing managed checkpoint | Current offer is SFT-specific; DPO/RL and evaluation costs need separate coverage |
| W&B | Serverless SFT, then bounded RL on independently verifiable tasks | Its automatically hosted checkpoint through W&B inference | Adapter training is free during public preview; inference and artifact storage are charged |
| Adaption | Credit-funded SFT/DPO; retain run 2 as historical reference, then qualify controlled new comparisons | Existing local adapters plus a qualified matching-base runtime; hosted inference availability needs checking | User confirms credits; verify balance, method cost, dataset floor, and export before another run |
| GLM 5.3 / Flash | Catalog and capability qualification, followed by credit-covered experiments if eligible | Same-provider endpoint for each trained checkpoint | Fireworks lists these on its paid Serverless Training rate card; the Glimmer promotion does not establish free GLM training |
| Together | Optional additional lane, subject to the user's provider preference | Together endpoint if a Together job is actually included | The supplied key identifies a separate service; it does not establish free training or credits |

Fireworks documentation advertises Glimmer SFT through November 30, extending
the email's October 31 date. Verify account-specific eligibility before any
use; this offer expiry is a provider condition, not a campaign delivery target.
The offer does not
cover DPO, RL, full-parameter jobs, deployment, or inference outside the training
run. Its cookbook separately prices in-session evaluation sampling. Use the
read-only starter `plan` step and never enable its `--allow-paid` override in
this free-first campaign. [Fireworks starter documentation](https://docs.fireworks.ai/fine-tuning/training-api/cookbook/muse-glimmer)

For the existing managed checkpoint, a preemptible hosted evaluation deployment
is a documented route that avoids downloading weights. Active serverless jobs
instead use a session sampler; a promoted managed-model ID cannot be passed
to that sampler. Verify availability and price before provisioning; preemptible
does not mean free. Persist results across interruptions and remove temporary
evaluation capacity afterward. This route supersedes waiting solely for weight
downloads. [Fireworks evaluation documentation](https://docs.fireworks.ai/fine-tuning/evaluating-fine-tuned-models)

Fireworks does not support ordinary serverless deployment of trained LoRAs;
its serving guide specifies on-demand deployments. Avoid designing around a
nonexistent adapter chat endpoint. [Fireworks deployment documentation](https://docs.fireworks.ai/fine-tuning/deploying-loras)

W&B automatically hosts trained adapters, but public preview still bills
inference and storage. Confirm current balances, expiry, private artifact
access, and checkpoint identity before a smoke run.
[W&B training documentation](https://raw.githubusercontent.com/wandb/docs/main/serverless-training.mdx)

W&B's ART serverless model list currently names Qwen 3 14B and Qwen 3 30B A3B.
Do not infer support for DeepSeek, GLM, Glimmer, or another model from inference
availability. Respect the existing Qwen 3.8 exclusion and never use Llama models;
qualify the exact proposed W&B model against standing model preferences before
selection. Local ART model support does not establish managed support.
[ART model catalog](https://art.openpipe.ai/resources/models/)

Track training, input/prefill, cached input, output/sampling, judges, storage,
and deployment as separate cost lines. Free training is only one line. Start
with a $0 out-of-pocket ceiling; use verified credits with a bounded token and
storage allowance. Stop before uncovered charges, expired eligibility, or an
unknown-price operation. Historical approvals and estimates are not this
campaign's budget. Fireworks publishes distinct GLM training, prefill, and
sampling rates. [Fireworks pricing](https://fireworks.ai/pricing)

W&B inference credits are user-confirmed and may fund bounded inference,
curation audits, and independent judging. They do not pay another provider's
invoice or establish that W&B can serve an arbitrary Adaption/Fireworks adapter.
Adaption credits make it an explicit third lane, including exportable checkpoint
experiments. Both prior Adaption adapters are local; run 2 is live `succeeded`
with `download_available=true`. Its platform win rate is 0.6414; retain the blind
evaluation protocol rather than treating that number as a clinical verdict.
Check credit coverage and bound each new Adaption run.

Fireworks is experiment-only until local export succeeds under the account's
actual entitlement. Periodic remote checkpoints support resume and evaluation,
but are not local weights backups. No verified save-along-the-way workaround
was found. Preserve results locally and evaluate while access is available;
qualify supported downloads before claiming a checkpoint can leave Fireworks.
The follow-up investigation records the evidence and export limitations.

The key supplied in chat must be rotated; it is not reproduced or used here.
Use the project's approved runtime credential mechanism, and never put values
in plans, datasets, manifests, traces, or commands.

## 4. A — Dataset completion or break-away

Execute local checks back-to-back as soon as their inputs are available. The
previous October 17–31 calendar schedule and one-working-day timebox are
superseded; they do not pace execution or waive release gates. Pause only work
that depends on missing evidence, a source-owner decision, or verified provider
access/credit coverage. Record measured local runtime separately from external
waits; do not estimate duration without evidence. If the full corpus needs
external review, continue assessing independently evidenced sources and prepare
the earliest subset that passes every required gate, while keeping unresolved
sources in a versioned backlog.

1. Inventory all dataset lanes, beyond arcs: source catalog, acquisition,
   normalization, curation, consolidation, expansion waves, preference data,
   calibration sets, and existing exports. Record last successful stage,
   source location, counts, hashes, license/consent, known defects, owner, and
   remaining effort. Check authoritative artifacts rather than old completion
   claims; inspect `ai/training_corpus/`, `ai/core/pipelines/`,
   `ai/pkg_mera/core/pipelines/`, and the training pipeline audit.
2. Validate the prepared recovery candidate against source eligibility and
   release gates. The incomplete arc-only rebuild is established; original
   master disappearance is still unexplained. The 189,159 non-arc rows and
   seven superseded arc versions survive locally. Keep active gold unchanged
   until promotion checks pass; do not append blindly or overwrite history.
3. Join accepted arcs, sessions, audit attempts, queue events, rejection logs,
   and provenance. The 981-to-980 difference is explained by `arc_0366` session
   2's structural rejection. Resolve other missing verdicts and accepted arcs
   still in queue history. Apply decisions to the exact reviewed content hash,
   not a reused arc ID; old approval cannot transfer to regenerated content.
4. Retain the human-review lane: the existing digest groups 4 safety-heavy,
   24 other stance-flagged, and 28 ledger-only arcs. Reconcile dispositions
   before treating these groups as current. Human-review requirements remain
   binding; automated re-audit does not substitute for required human approval.
5. Resolve source and generator seed IDs, including variation suffixes and
   ambiguous reused IDs. Reserve existing evaluation seeds. Keep all turns,
   sessions, revisions, translations, and preference pairs from each source
   group in one split. Check exact and semantic duplicates across splits and
   against calibration/evaluation assets. Quarantine unknown lineage.
6. Validate role order, nonempty replies, tool-call/result pairing, assistant-only
   loss masks, ledger grounding, safety behavior, language/length distributions,
   provider tokenization, license compatibility, and privacy. Redaction and
   mechanical gates need sampled review; synthetic origin alone is insufficient.
7. Freeze a provider-neutral release with disjoint train/development/sealed-test
   views. Produce Fireworks and W&B representations with traceable row maps,
   separate references, and exact tokenizer/renderer versions. Render samples
   and reject context overflow; never silently truncate or drop records.

Release layout, created in a new directory after gates pass:

```text
release-<date>-v<N>/
  manifest.json              # hashes, counts, code revisions, gates, exclusions
  source_licenses.json        # rights, restrictions, consent evidence
  lineage.jsonl              # private source/seed/arc/session/row mapping
  splits.jsonl               # immutable group-to-split assignments
  canonical/{train,dev,test}.jsonl
  providers/{fireworks,wandb}/
  reports/                   # quality, privacy, duplication, coverage, rendering
  backlog.jsonl              # unresolved rows, reasons, owner, next action
  DATA_CARD.md
```

Internal metadata and test answers stay private. Provider uploads contain only
approved training fields. Keep development and test data out of training loss,
rollouts, rewards, writer prompts, and preference synthesis. Calibration assets
remain a separate data role with their own permission and exposure checks.

Exit: every included row has admissible provenance, a passing content decision,
a stable hash and a group-disjoint assignment; every excluded row has a reason.
Only then declare the break-away release ready. Reuse the existing release
manifest machinery where it meets these requirements; keep the frozen v1
exporter's assertions intact and implement a separately versioned successor.

## 5. B/C — Ordered experiments

Use one neutral scenario specification and provider adapters. First establish
each base model's own control; compare each fine-tuned checkpoint with its base
on the same provider before making cross-provider claims. A provider/model
change is a separate treatment, not a replication of a data or recipe change.

| Order / ID | Comparison | Question and controls |
| --- | --- | --- |
| 0 / ACCESS | Model catalog, render check, then 5 paired smoke cases per lane | Can the exact checkpoint train and answer through the intended endpoint, within credit coverage? |
| 1 / BASE | Untuned Glimmer; eligible W&B base; accessible intended production models | Establish quality, cost, latency, tool support, and format baselines |
| 2 / SFT-CORE | Base vs SFT on the frozen accepted subset | Does training improve the target behavior? Pin recipe, prompts, renderer, and decoding |
| 3 / DATA-SIZE | Nested 25%, 50%, 100% training-group subsets | Estimate data value; fix recipe and report actual trained-token exposure |
| 4 / DATA-MIX | General/support/research only vs therapeutic only vs balanced mix | Test specialization and general-capability retention with a fixed training-token budget |
| 5 / HISTORY | Short single-session vs full multi-session context | Test continuity and contradictions; match target cases and training-token exposure |
| 6 / LEDGER | Visible ledger vs private structured state vs response-only | Measure grounding, privacy, verbosity, and downstream utility with format-aware rubrics |
| 7 / RECIPE | Rank 8 vs 16, then baseline LR vs half LR, then 1 vs 2 epochs | One factor at a time; pin target modules and establish provider defaults explicitly |
| 8 / DPO | Best SFT vs SFT+DPO; base remains a reference | Only after exact-prefix therapist preference pairs and covered DPO pricing are established |
| 9 / RL | Best SFT vs bounded RL, with SFT-only continuation control | Begin with objectively verifiable tool/support/research tasks; isolate extra training effects |
| 10 / SYSTEM | Fixed model with memory off/on, retrieval off/on, tool failure/no failure | Identify harness effects separately from model training |
| 11 / ROBUST | Normal vs paraphrased/adversarial/OOD cases; text vs permitted vision | Test robustness, instruction injection, generalization, and modality coverage |
| 12 / CONFIRM | Top two recipes repeated on eligible models, then sealed tests | Test reproducibility and whether the recommendation survives a model change |

This is a sequential campaign, not a full Cartesian sweep. Start with at most
four new SFT jobs: one baseline and one data ablation for each of Fireworks and
W&B, subject to eligibility. Re-evaluate the existing Adaption checkpoint first;
schedule new Adaption training separately when a hypothesis and covered budget
justify it. Reuse trained checkpoints for multiple scenario evaluations. Extend only
after the first paired report, cost reconciliation, and decision to retain or
drop each hypothesis. Replicate finalists with three training seeds if supported
and credit-covered; otherwise disclose provider nondeterminism and unreplicated
training. Repeated inference alone is not a training replication.

Keep internal writer DPO experiments separate if useful for curation. Therapist
DPO must contain the exact same visible conversation prefix for chosen and
rejected responses, a reviewed turn-level preference, and split lineage. Do not
wrap whole writer transcripts as one assistant answer.

The current serverless utility rewards length and n-gram overlap. That is not
an adequate clinical reward. Build bounded rewards from verified tool results,
citation support, state changes, and explicit prohibited effects. Audit valid
alternatives, wrong answers, reward shortcuts, and missing evidence before RL.
Clinical alignment requires independently reviewed judgments, not optimizing
keyword presence or a model judge alone.

## 6. Scenario coverage and evidence

| Suite | Required coverage | Primary evidence |
| --- | --- | --- |
| Therapeutic dialogue | Reflection, MI-style behavior, anti-sycophancy, rupture/repair, actionable support | Blind anchored rubric, human calibration, paired transcripts |
| Risk and boundaries | Explicit/ambiguous risk, ordinary distress, minors, coercion, substance use, delusion/paranoia, medical uncertainty | Appropriate action and missed-risk/over-escalation rates; independent clinical review |
| Longitudinal memory | Fact corrections, contradictions, temporal updates, forgetting, multiple sessions | Hidden state truth and grounded ledger changes |
| Support agents | Retrieval, policy following, tool arguments, retries, escalation, approval boundaries | Tool traces and independent final-state checks |
| Research agents | Source retrieval, citation support, conflicting sources, abstention, long tool chains | Source entailment and task completion |
| Adversarial behavior | Prompt injection in tools/documents, cross-user leakage, false premises, tool outages | No prohibited disclosure/action; trace-level verification |
| Distribution shift | Novel seed families, identity/cultural variation, supported languages, long contexts | Per-stratum quality and calibrated uncertainty |
| Vision, conditional | Synthetic documents/charts and text-image disagreement | Verified extracted fields or answers; require supported training and inference |
| Efficiency and retention | General tasks, structured output, verbosity, repetitions, timeout/rate-limit recovery | Task success, p50/p95 latency, tokens, error rates, actual cost |

Use the historical 110 cases only after lineage revalidation and only for the
arms whose exposure is known. Construct separate development and sealed-test
scenario groups for new optimization. If an old test has influenced selection,
label it development/diagnostic for future runs. Freeze the final evaluation
once; never feed its failures back into training while calling it held out.

Randomize and balance A/B position; hide model/provider identity. Use an
independent second judge and human adjudication for disagreements and safety
cases. Calibrate judges against permitted human-rated examples before trusting
scores. Existing weak judge correlations and the documented format bias rule
out using one heuristic or a single uncalibrated judge as the gate.

Report wins/ties/losses and uncertainty by independent seed group. Bootstrap at
the source/arc cluster level, not individual turns. Separate predeclared primary
comparisons from exploratory sweeps; adjust for multiple comparisons when
making confirmatory claims. Five smoke cases and 110 diagnostic cases do not
establish safety. Size the final test from pilot variance and the minimum
meaningful improvement before opening it; if underpowered, report inconclusive.

Draft selection rule: improve the predeclared primary task metric with a paired
95% confidence interval excluding zero; satisfy preregistered safety and
retention noninferiority margins plus clinical review where applicable. Choose
the margins before scoring. A critical reviewed safety failure blocks promotion
even if the average improves. Invalid access, timeouts, malformed outputs, and
truncation remain visible; report infrastructure availability separately from
model quality and never remove failures to improve a score.

Every run records release/config/prompt hashes, source revision plus relevant
working-tree diff hash, exact model and parent checkpoint, tokenizer/template,
loss masks, actual hyperparameters, seed availability, context/decoding limits,
endpoint identity, retries, finish reasons, token counts, timing, billed usage,
judge/rubric revision, and retained output locations. Results persist after each
case, and resume rejects changed inputs. Use private W&B runs/artifacts and
sanitized Weave traces; avoid publishing the full dataset as old scripts do.

## 7. Dependency-driven execution and completion

The prior October 17–31 schedule is superseded. Move each eligible task forward
immediately when its prerequisites pass; a calendar date is not an execution
gate. The October 31 Fireworks offer date, if still confirmed for the account,
is only an external provider condition and does not override dataset, access, or
cost checks.

| Order | Work | Dependency / external wait |
| --- | --- | --- |
| Now | Finish source-specific lineage, exclusions, held-out reservations, and overlap diagnostics | Local artifacts; continue without waiting on calendar windows |
| Next | Freeze the earliest passing provider-neutral break-away subset and render report | Exact source rights/privacy evidence, content decisions, complete group lineage, disjoint evaluation identities, quality/privacy gates |
| In parallel | Read-only provider/model/export qualification and bounded cost plans | Current account access, credit balance/expiry, terms, and provider responses; no resource creation |
| Then | Revalidate evaluation suite and qualify existing checkpoint inference | Passing data/evaluation dependencies plus provider endpoint and covered inference |
| Then | Run bounded base/SFT comparisons and selected ablations | Frozen eligible release, successful access smoke, verified cost coverage |
| Conditional | DPO/RL, replications, sealed evaluation | Reviewed exact-prefix preferences or validated rewards, covered costs, and frozen test |

The first narrow G04 diagnostic candidate is the 522-row `edge_cases` branch
documented in [`g03-edge-branch-diagnostics.json`](execution-2026-10-17/g03-edge-branch-diagnostics.json).
Its exact local generator uses a hardcoded synthetic scenario matrix and no
external clinical seed narrative. Exact holdout groups remove 29 of 551 rows;
the remaining metadata-only rowrefs have a provisional group-disjoint 410/72/40
split. This evidence supports first-party synthetic origin for this branch and
does not require generic source-family signoff by default. Before creating a
provider payload, recover the contemporaneous generator provider/model receipt
and verify the applicable terms permit retaining the outputs for research
fine-tuning and transferring them to the selected provider. The generator sets
`clinical_reviewed=true` automatically, so that field does not support clinical
quality or production claims. The 52 golden-control source identities remain
unknown; describe the near-duplicate screen as diagnostic only.

Report measured local processing time and identify external approval/provider
waits separately. Do not invent a finish date or treat elapsed calendar time as
work remaining. Keep the registry current with prerequisites, evidence,
completed work, and the next concrete action. If one lane waits on an external
decision, continue independent local checks and qualified lanes.

Maintain an experiment registry with planned/running/completed/invalid/skipped
status, prerequisites, hypothesis, primary metric, result, and next decision.
Do not label blocked or unfunded arms successful. If one provider cannot run,
continue independent local preparation and qualified lanes; retain the missing
comparison explicitly.

For eventual full model choices, carry forward data releases, scenario suites,
provider-neutral harness, and hypotheses. Adapters are architecture-specific.
Re-establish base/SFT controls on each intended model, including the configured
DeepSeek V4 Pro and eligible GLM/Flash or Kimi choices; do not infer their tuning
availability or quality from Glimmer. Measure quality/cost/latency tradeoffs and
recommend by use case, without automatically replacing the production stack.
EKS remains production; these training endpoints are experiment infrastructure.

The next concrete action is validating the recovery candidate's provenance and
release gates, resolving superseded arc versions, and qualifying remaining
provider access and credit coverage. Packaging and new experiments follow
those checks; they have not already run.

## 8. Evidence and verification

Local references:

- [Existing Glimmer protocol](muse-glimmer-experiments.md)
- [Execution history, especially sections 13.16–13.18](fireworks-pilot-log.md)
- [Human-review digest](hr-queue-digest.md)
- [Frozen v1 export contract](fireworks-export-plan.md)
- [Broader pipeline audit](../training-pipeline-audit-2026-08-24.md)

Verified for this plan: JSON parsing and counts of the four arc artifacts and
gold; all frozen pilot file identities; evaluation-case checksum and source
identities; fresh read-only seed-lineage audit. The seven existing preparation
tests pass with isolated pytest:

```bash
uv run --no-project --with pytest python -m pytest \
  ai/qa/validation/tests/test_prepare_glimmer_eval.py -q \
  --confcutdir=ai/qa/validation/tests
```

These checks validate preparation behavior, not inference quality, clinical
fitness, provider account access, or release readiness.

## 9. 2026-10-18 execution addendum — credits, comparisons, portable finish

This addendum supersedes the older W&B “training is free during public preview” assumption in §§3 and 8. The user's account-specific report is that W&B
Serverless Training remains free/exportable and Adaption credits remain available. We will use those entitlements if the live account estimate confirms no
uncovered charge. A read-only W&B check on 2026-10-18 returned a healthy Training API and 13 trainable bases, including `Qwen/Qwen3.6-35B-A3B`; it did not
establish price, remaining credits, or storage headroom. Current public CoreWeave Forge pricing lists Serverless SFT at $2.70/GPU-hour, with inference and
checkpoint storage billed separately. Older W&B docs describe a free public-preview period and are archived in their docs repository as of 2026-09-30. Resolve
this discrepancy from the authenticated account's job estimate/credit view before creating a job. [Current CoreWeave post-training
pricing](https://www.coreweave.com/forge-pricing/post-training) · [W&B Serverless Training docs](https://github.com/wandb/docs/blob/main/serverless-
training.mdx) · [W&B Serverless Inference](https://site.wandb.ai/inference/).

Adaption remains the credit-funded, exportable optimization lane. Its current API supports AutoScientist run creation, downloadable best-model artifacts, and
downloadable/processable datasets. The dashboard, rather than the API, exposes remaining credit balance; estimates are available before credit-consuming
operations. The prior run-2 adapter is downloadable but was trained on the old corpus whose source/privacy clearance is unresolved, so keep it as historical
diagnostic material until its training-data lineage is cleared. Do not adapt, augment, or train on the 190,139-row candidate while its rights/privacy gate is
closed. [Adaption API](https://docs.adaptionlabs.ai/api/) · [Adaption AutoScientist result and export
guidance](https://docs.adaptionlabs.ai/autoscientist/interpreting-results) · [Adaption credit-consuming operations](https://docs.adaptionlabs.ai/tools/mcp/).

### Execution order

1. **Today — verify entitlements and freeze a clean test corpus.** Read-only check the current Adaption credit balance in its dashboard; verify the W&B
   Serverless Training account estimate/credit and artifact quota; verify Fireworks Glimmer promo eligibility and sampling price; check OVHcloud AI Training
   region/GPU availability and account billing. Do not create resources during this check. In parallel, author a new first-party synthetic corpus locally from
   project-owned scenario templates, with no candidate-row text, real patient details, third-party seed text, or model-generated historical outputs. Freeze
   train/dev/sealed-test hashes, split by scenario family, and have Vivi review the scenario coverage. This is a technical research corpus, not a clinically
   validated dataset.

2. **Use one portable anchor model for provider comparisons.** Start with `Qwen/Qwen3.6-35B-A3B`, because the live W&B Training catalog lists it and prior
   Adaption work used the same base. Confirm the exact immutable model revision, license, tokenizer, chat template, and training-context cap across the
   provider catalogs before launch. Add Gemma 4 31B and Nemotron 3 30B A3B only where both the provider and the OVH final path can use the exact same open-
   weight base. Keep Muse Glimmer 30B as a separate Fireworks-only comparison: because it cannot currently be exported from this Fireworks account, its result
   is diagnostic and cannot become the final model. Do not compare one base against another and attribute the difference to the training provider.

3. **Run a controlled provider matrix on the same frozen data.**

   | Arm | Method | Inference/evaluation path | Portable result | |---|---|---|---| | Base control | No tuning | W&B Inference for the chosen base, if its
   account credit covers the run | No adapter | | W&B | Serverless SFT LoRA; one baseline recipe and at most one predeclared data/recipe ablation | W&B
   endpoint for its trained artifact; export adapter and config to our private artifact store | Yes, after local download/hash verification; W&B docs describe
   local/third-party LoRA backup | | Adaption | AutoScientist SFT/LoRA on the same base and same training rows; estimate credits first; disable or separately
   account for optional data augmentation | W&B Serverless LoRA Inference for the exported adapter only after base/adapter compatibility is verified;
   otherwise evaluate in our OVH runtime | Yes, on successful run with `download_available=true`; keep raw export and config | | Fireworks | Muse Glimmer SFT
   using the confirmed free offer; one small, bounded run only | Fireworks-hosted endpoint/sampler with a separately covered inference budget | No, under
   current account download restriction; comparison only |

   W&B documents that its trained LoRAs are stored as artifacts and can be saved locally, and its current inference product accepts custom LoRA weights. That
   makes W&B the common endpoint for the base and W&B-trained LoRAs and a possible endpoint for the Adaption LoRA after compatibility qualification. It does
   not make W&B a cross-provider billing wallet: W&B credits cannot cover Fireworks usage. [W&B Serverless Inference](https://site.wandb.ai/inference/) ·
   [CoreWeave Serverless Inference](https://www.coreweave.com/products/serverless-inference).

4. **Evaluate behavior across scenarios, not just loss.** Use paired, blinded A/B comparisons on a shared scenario suite covering multi-turn tool use, crisis
   escalation/refusal boundaries, empathetic support, research with citations and abstention, adversarial tool/document inputs, cultural and identity
   variation, and long-context/tool-failure recovery. Freeze decoding, system prompt, tools, and scoring rubric. Measure task completion, factual grounding,
   tool-call correctness, safety-policy adherence, response quality, latency, token use, and actual provider cost. Report wins/ties/losses by independent
   scenario group with uncertainty; adjudicate safety disagreements with human review. Keep the sealed set unseen during data and recipe selection. Existing
   corpus-derived and lineage-uncertain evaluation cases remain diagnostic until their own use is cleared.

5. **Select a portable finalist, then finish under our own recipe on OVHcloud.** Take the best exportable base+adapter result—not the Fireworks-only
   result—and reproduce or continue its training in our own versioned Docker/Transformers/PEFT or TRL recipe through OVHcloud AI Training. Pin the base
   revision, tokenizer/template, data hashes, loss mask, rank/alpha, target modules, optimizer, schedule, seeds, and checkpoints. Attach private Object
   Storage read-only for input and read-write for outputs; save resumable checkpoints and the final adapter/merged weights, tokenizer, config, logs, and
   evaluation report to our bucket. OVH AI Training supports custom Docker images, selected CPU/GPU resources, and attached Object Storage output volumes; the
   GPU flavor and region are chosen by us. Its documented current U.S. price list shows H100 at $3.39/GPU-hour and H200 as a four-GPU bundle at $27.28/hour;
   confirm the actual region/account quote and storage charges before starting. H100 capacity is limited to four GPUs per job; H200 is only offered in four-
   GPU NVLink bundles in the documented GRA region. [OVH AI Training job and output volumes](https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-
   learning/ai-training-submit-job) · [OVH GPU pricing](https://www.ovhcloud.com/en/public-cloud/prices/) · [OVH AI Training
   capabilities](https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-training-capabilities).

   Deploy the resulting model with OVH AI Deploy from our custom image and private weights volume, or deploy it on our own EKS stack once the production gate
   is met. AI Deploy can host custom model/application containers and exposes an HTTP endpoint; its app continues running and billing until stopped. Use
   restricted access, verify storage/network and privacy requirements, and stop test deployments after evaluation. [OVH AI Deploy custom
   apps](https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-deploy-apps) · [OVH AI Deploy lifecycle and
   billing](https://docs.ovhcloud.com/en/guides/public-cloud/ai-machine-learning/ai-deploy-billing).

6. **Keep the recovered corpus on a separate clearance track.** Continue source-by-source mapping and review in parallel. A row enters a later training
   release only when exact source/version permissions, privacy/consent decision, row-reference binding, content quality review, and the named provider's terms
   are recorded. Nothing about a synthetic pilot, provider credit, or previous pilot approval clears any of the 190,139 rows.

### Critical path and time boundary

The work that can proceed immediately is account/price verification, clean synthetic authoring, local rendering, evaluation-suite construction, and provider
format dry-runs. Provider jobs can start after the synthetic set passes local and human checks and the account shows covered cost. The Fireworks free window
is time-sensitive (owner-reported through October 31); run only its disposable synthetic diagnostic before that date if eligibility is still active. W&B
public-preview status/pricing and Adaption/OVH credits are account-dependent, so do not infer them from old public terms. OVH training/deployment is paid
compute; request and record a bounded dollar ceiling before resource creation. External reviewer turnaround is a separate wait and does not stop the
independent synthetic/model-comparison lane.

**Promotion gate:** choose the final base and recipe only from models with exact base/revision reproducibility, verified local export, a passing blinded
scenario evaluation, no critical safety failure, and a complete cost/provenance record. Deliver the self-hosted artifact as a versioned package containing
weights (adapter and merged form where supported), base-model/license reference, tokenizer/template, dataset/evaluation hashes, training config, logs, and
deployment image digest. Keep clinical or commercial use claims gated on source/privacy clearance and appropriately credentialed clinical review.
