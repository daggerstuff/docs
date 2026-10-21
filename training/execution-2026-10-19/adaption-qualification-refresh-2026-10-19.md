# Adaption qualification refresh — 2026-10-19

Initial read-only qualification snapshot. The current outcome is in the dated v4 raw-upload and SFT addendum below, which supersedes this snapshot's no-upload/no-run conclusions.

`Qwen/Qwen3.6-35B-A3B` is currently listed for SFT and DPO with LoRA, and the catalog reports a 262,144-token context. The organization has two visible datasets: `arc-run2-train-v1` (11,192 rows, succeeded) and `train` (418 rows, awaiting input). The 11,192-row dataset has two successful historical instruction/LoRA runs. The newest, `8da8f685-7ef6-43c0-958e-ab34dbdcd520`, completed one iteration, reports platform `best_win_rate=0.6414`, and is downloadable. The older run `cf1ebae0-1197-4362-92a1-3228c38ce96e` is also downloadable and reports 0.4971. These platform scores do not establish task quality or clinical safety.

A live, non-launching hyperparameter recommendation on the succeeded 11,192-row dataset returned one-epoch LoRA SFT settings for Qwen 3.6 (rank/alpha 8; q/v projections; learning rate 0.0001). It returned no price, credit deduction, balance, or expiry. The connector still exposes no Adaption-hosted inference endpoint. Historical run downloads establish export precedent, but do not prove account retention terms or that a future artifact will be portable in the needed runtime.

At this initial snapshot, the frozen v4 corpus had not been uploaded or schema-qualified. The later raw upload below establishes acceptance of the exact local JSONL schema and row count. This provider acceptance does not establish source rights or clinical-data eligibility.

The earlier qualification record states a documented minimum of 1,000 effective SFT rows and 12,000 effective DPO preference pairs. The current 11,192-row dataset is instruction/SFT, not a qualifying DPO preference-pair set. No DPO path is qualified. Adaption credits are user-reported, but the connector does not expose a balance, expiry, use restrictions, or exact cost/coverage for either an SFT or DPO run. At this initial snapshot, no paid job was launched; the later one-iteration experiments follow the user's authorization to use Adaption credits and retain the unknown-cost caveat.

**Initial decision:** Adaption was qualified for Qwen 3.6 LoRA SFT capability and had historical downloadable-run precedent, while v4 upload, cost coverage, and inference evaluation remained unqualified. The current decision and run status are in the later addendum below.

## Follow-up: credit, v4 format, and inference route — 19:19 UTC

The live connector’s entire Adaption tool inventory has no account-balance, billing-history, AutoScientist cost-estimate, model-inference, or chat-completions method. The successful hyperparameter recommendation remains only a recipe response. The official API reference lists the dataset and AutoScientist operations, including artifact download, but no hosted inference operation. Therefore the actual credit balance and training quote remain unavailable through the connected API; the public docs do provide one usable fact about expiry: Adaption’s [FAQ](https://docs.adaptionlabs.ai/resources/faq/) says unused organization credits do not expire and new monthly credits are added to the existing balance. That general statement does not reveal this account’s balance or eligibility/coverage.

Adaption’s documented local-file route accepts JSONL uploads. Its `processing_mode="raw"` requires named `prompt` plus `completion` columns for SFT; the AutoScientist API can train raw datasets with `data_format="chat"` or `"instruction"`. The frozen v4 file itself is JSONL with a single `messages` field. Structural scan of the pinned local W&B train payload verified 171,261 dialogues and 1,056,820 turns; messages are user/assistant, every row ends with assistant, user weights are 0, and assistant weights are 1. However, 11,504 rows start with an assistant prefix before the subsequent user/assistant pairs. These initial assistant messages have no preceding user prompt and are kept as prompt context, not emitted as training targets. The project's existing Adaption unroll convention therefore yields 522,658 eligible assistant targets, rather than 534,162. The payload SHA-256 is `60841fbc8d917de4699d1b41eddddf03fade949496db3e561769f94959e37f20` (299,152,125 bytes).

The W&B v4 manifest digest initially looked inconsistent; a follow-up reconciliation established that it is deliberate and correct. `metadata.json` stores the canonical JSON digest (`10d05ac9…`), while the freeze note and launcher state store the raw manifest file digest (`a4b0507f…`). Both identify the same manifest under their respective hashing conventions. See the [W&B v4 hash reconciliation](wandb-v4-manifest-hash-reconciliation-2026-10-19.md).

**Updated decision:** Adaption accepted the exact full-history v4 raw JSONL conversion, but its one-iteration training run failed before any iteration because the provider timed out after 60 seconds downloading the 2.14 GB S3 training file. A second raw dataset preserving all assistant targets and limiting each prompt to nine messages was accepted. Its initial SFT run failed before training because the structured message arrays were sent with `data_format="instruction"`, leaving the provider validation file empty. A corrected `data_format="chat"` retry was rejected by Adaption's API rate limiter before a run was created (retry-after 3,040 seconds). Adaption exposes no hosted inference in the checked connector or current public API reference; export the adapter and qualify an external matching-base runtime for evaluation. Public docs say credits do not expire, but this account's balance and per-run credit usage remain unavailable through the connector; each one-iteration cap bounds experiment count, not credit cost.

## 2026-10-19 v4 raw upload and one-iteration SFT

The mode-0600 conversion at `ai/training/output/adaption_v4_unrolled_20261019/train_unrolled.jsonl` is 2,136,003,932 bytes with SHA-256 `bec73fb3e8ccb54e2c3f404860d7b4264aba7e59f2602473f9046eb720d3cd37`. Its private manifest records the frozen source payload hash, 171,261 input rows, 11,504 leading-assistant-context rows, and 522,658 emitted targets. The `raw` upload succeeded and became ready without augmentation: dataset `21f6d03f-5f56-41be-9070-14c8fccbf442`, named `pixelated-v4-train-unrolled-20261019`; Adaption normalized the columns as `original_prompt` and `original_completion`.

A non-launching recommendation for Qwen3.6 returned one-epoch LoRA settings (rank/alpha 8, q/v projections, learning rate 0.0003, batch size max, `train_on_inputs=false`). The first instruction AutoScientist run, `7b859acc-f325-4022-92c7-b1a1ff40c2c3`, failed before any iteration: provider error was a 60-second timeout while downloading its S3 train JSONL. It completed 0/1 iterations and produced no checkpoint. The API exposed no credit balance or run-level deduction for the failure.

References: [dataset create/upload API](https://docs.adaptionlabs.ai/api/resources/datasets/methods/create), [run raw data through AutoScientist](https://docs.adaptionlabs.ai/autoscientist/run-on-non-adapted-data/), [AutoScientist run API](https://docs.adaptionlabs.ai/api/resources/autoscientist/methods/create), [AutoScientist app order summary](https://docs.adaptionlabs.ai/tutorials/autoscientist-app-walkthrough/), and [Adaption FAQ](https://docs.adaptionlabs.ai/resources/faq/).

## 19:57 UTC live estimate refresh

The authenticated connector currently lists the succeeded `arc-run2-train-v1`
dataset (11,192 rows) and the `train` dataset (418 rows, still
`awaiting_input`). A non-launching adaptation estimate for the 11,192-row
dataset, mapped from `original_prompt`/`original_completion`, returned **112
estimated credits and 150 minutes**. A separate non-launching recommendation
returned Qwen 3.5 4B LoRA SFT (one epoch, rank 16, learning rate `1e-5`). This
is a distinct recipe from the earlier Qwen 3.6 recommendation, and neither
result confirms the remaining account balance or estimates the frozen v4
corpus. No run or upload was created. The actual balance, expiry/use limits,
exact v4 job quote, export terms, and inference endpoint remain unexposed by
the available connector. The 112-credit estimate is a usable cost bound for
the existing 11,192-row dataset only; it is not authorization to assume 112
credits are available.

The 418-row `train` dataset remains `awaiting_input`. A non-launching estimate
with its existing `messages` column mapped as chat returned 5 credits and 16
minutes, but the hyperparameter recommender rejects it because the dataset is
not ready. No adaptation or training run was started. This gives a bounded
processing estimate, not a viable model-training comparison yet.

## 2026-10-19 context-window ablation SFT

To address the full-history run's S3 download timeout without dropping assistant targets, a second local serialization keeps the same 522,658 targets but limits each prompt to the latest nine messages (current user turn plus up to four preceding exchanges). This omits older history for 288,318 targets and is explicitly a context-window ablation, not an equivalent full-context training input. Its mode-0600 file is `ai/training/output/adaption_v4_unrolled_ctx9_20261019/train_unrolled_ctx9.jsonl`, 790,582,664 bytes, SHA-256 `4f2b4ef53dfc649f5bd6c5e943b4917d2bec9a8ade309a7caf865b2fd975e2a2`; its manifest pins the same frozen source payload hash.

Adaption accepted this second dataset in raw mode without augmentation and marked it ready: dataset `5cf8efd5-3426-4cc4-b3cc-4d40f7912f9d`, `pixelated-v4-train-unrolled-ctx9-20261019`, 522,658 rows. A one-epoch Qwen3.6 LoRA recipe was again recommended. The first one-iteration instruction run with no augmentation (`8d00b26c-de36-452a-abc2-5cd36b76036b`) failed before training: its validation JSONL was empty, and no checkpoint was produced. The subsequent chat-format retry was rate-limited before a run was created. The account balance and cost remain unavailable, so any eventual one-iteration run will have no verified credit-amount bound.

#### 2026-10-19 21:11 UTC retry readiness check

A read-only API refresh confirmed the ctx9 dataset remains `succeeded` with
522,658 rows and columns `uuid`, `original_prompt`, and
`original_completion`. The only run for this dataset is the prior failed
instruction-format attempt (`8d00b26c-de36-452a-abc2-5cd36b76036b`), terminal at
0/1 iterations with no downloadable checkpoint. The corrected chat-format
request had received `retry_after=3040` around 21:08 UTC, so this 21:11 check is
still inside the cooldown. The earliest safe retry is approximately 21:59 UTC;
this is approximate because the exact refusal timestamp was not persisted.

After that time, make exactly one call with dataset
`5cf8efd5-3426-4cc4-b3cc-4d40f7912f9d`, model `Qwen/Qwen3.6-35B-A3B`,
`data_format=chat`, and the established column mapping
`prompt=original_prompt`, `completion=original_completion`. Local structural
inspection confirms both mapped values are arrays of message objects, which is
why chat format is required. Use no augmentation, `max_iterations=1`, and the
previously recommended LoRA settings (rank/alpha 8, q/v projections, learning
rate 0.0003, batch size max, one epoch, `train_on_inputs=false`). Do not retry before the cooldown expires;
if the one allowed retry is rate-limited again, stop and record the new provider
window rather than looping. Credit balance and run cost remain undisclosed.

#### 2026-10-19 23:03 UTC live API refresh

Authenticated, read-only Adaption connector calls rechecked the model catalog,
datasets, AutoScientist runs, the historical run-2 adapter, its dataset
evaluation record, and a non-launching hyperparameter recommendation. The
exact machine-readable response summary is in
[`adaption-live-refresh-20261019T2303Z.json`](adaption-live-refresh-20261019T2303Z.json).

`Qwen/Qwen3.6-35B-A3B` remains available for SFT/DPO LoRA. The ctx9 dataset
remains ready at 522,658 rows. Its sole AutoScientist run is still the failed
instruction-format attempt `8d00b26c-de36-452a-abc2-5cd36b76036b`, terminal at
0/1 iterations with an empty generated validation JSONL and no checkpoint. No
corrected chat-format run exists. The earlier full-history run
`7b859acc-f325-4022-92c7-b1a1ff40c2c3` remains failed at 0/1 after the provider's
60-second S3 train-file download timeout. The cooldown recorded at 21:08 has
elapsed, so the chat-format retry is no longer blocked by that old rate limit;
however, the connector provides neither a current account balance nor an
AutoScientist quote for this 522,658-target job. The previous 112-credit quote
was for the separate 11,192-row dataset and cannot be scaled or represented as
v4 coverage. No retry was launched during this read-only refresh.

The historical run `8da8f685-7ef6-43c0-958e-ab34dbdcd520` remains succeeded,
one iteration, and downloadable with platform `best_win_rate=0.6414`; its
dataset evaluation endpoint currently returns no summary/results. A fresh
non-launching recommendation for that 11,192-row dataset returned Qwen3.6
one-epoch LoRA settings (rank/alpha 8, q/v projections, learning rate
`1e-4`, batch size max, `train_on_inputs=false`). This recommendation is for
that dataset, not a cost quote or a v4-trained model result.

#### 2026-10-19 23:07 UTC corrected ctx9 chat-format retry

After the documented rate-limit window expired, one corrected one-iteration
AutoScientist run was submitted against the already-ready ctx9 dataset. The
request explicitly used `data_format=chat`, mapped the array-valued
`original_prompt` and `original_completion` fields, disabled both augmentation
types, selected Qwen3.6-35B-A3B, and set `max_iterations=1`. Adaption accepted
the request and returned run
`33bba6d2-d9e5-408c-bd4d-76544d2cde78` as `running` at 0/1 iterations, with no
error or checkpoint yet. This establishes job creation and resolved schema
mapping; it does not establish successful training, credit amount, or a
downloadable adapter. The provider connector still does not expose a v4 cost
quote or current balance. The request is pinned in
[`adaption-live-refresh-20261019T2307Z.json`](adaption-live-refresh-20261019T2307Z.json).

#### 2026-10-19 23:12 UTC scalar-text schema correction

The corrected-chat run `33bba6d2-d9e5-408c-bd4d-76544d2cde78` reached terminal
`failed`, 0/1 iterations, with provider error that its generated validation
JSONL was empty (`Pre-upload stat failed ... val file ... is empty (0 bytes)`).
Local structural inspection found the submitted `prompt` and `completion`
columns were JSON arrays, while Adaption's current raw-data documentation
describes these columns as prompt and completion text. This made scalar text a
reasonable schema correction to test, but did not establish the cause of the
empty validation file.

A new ctx9 serialization converts each prompt's chronological turns into
role-labeled plain text and each assistant target into scalar completion text.
It preserves all 522,658 targets, is 675,995,387 bytes, and is mode 0600; the
private manifest is in
`ai/training/output/adaption_v4_unrolled_ctx9_text_20261019/`. Adaption accepted
it as ready dataset `c00e322e-3842-4a56-9e6b-b9c81cf8b599` with all 522,658 rows.
The Qwen3.6 recommender returned a one-epoch LoRA recipe (rank/alpha 8, q/v,
learning rate 0.0003); this is not a cost estimate. A no-augmentation,
one-iteration `chat` run, `ef278ee7-b04d-4014-9b7a-cb7ee81b66fd`, was accepted
at 0/1 with no error at creation. Follow-up polling found it failed at 0/1 with
the same empty generated-validation-JSONL error. The scalar-text form did not
fix the failure. The earlier successful 11,192-row Adaption dataset also used
array-valued prompt/completion messages, so array values alone are not a
proven root cause. Current evidence narrows the problem to the larger
522,658-row v4-derived training path or its provider-side validation
preparation; it does not distinguish those causes. No further Adaption v4
run should be launched until this failure is isolated. The connector still
exposes neither balance nor per-run cost.

Current docs consulted: [raw dataset workflow](https://docs.adaptionlabs.ai/autoscientist/run-on-non-adapted-data/)
and [AutoScientist create API](https://docs.adaptionlabs.ai/api/resources/autoscientist/methods/create).

#### Follow-up diagnosis — 2026-10-19 23:17 UTC

The successful 11,192-row control's dataset API view reports
`prompt_column=original_prompt` and
`completion_column=original_completion`. The full-history, array-ctx9, and
scalar-ctx9 v4-derived datasets report the same three columns
(`uuid`, `original_prompt`, `original_completion`) and processed row counts,
but both canonical column fields are null. All three v4 AutoScientist requests
explicitly supplied those mappings and the API echoed them, so the metadata
difference is a diagnostic lead, not an established cause. A further
one-iteration launch would not be informative without seeing Adaption's
train/validation split and writer counts or understanding why its raw dataset
ingestion did not populate these fields. Requesting such provider-side
diagnostic evidence is the next no-credit step; the available read API has no
per-run preprocessing counters or logs.

#### 2026-10-19 23:43 UTC read-only failure-path comparison

The authenticated API now shows three v4-derived raw SFT runs failed before
iteration 1 with the same empty validation JSONL error: array-valued ctx9
(`33bba6d2-d9e5-408c-bd4d-76544d2cde78`), scalar-text ctx9
(`ef278ee7-b04d-4014-9b7a-cb7ee81b66fd`), and the earlier instruction ctx9
(`8d00b26c-de36-452a-abc2-5cd36b76036b`). Their shared ready dataset schema has
522,658 rows and `prompt_column=null`, `completion_column=null`; each run's API
record echoes the explicit `original_prompt`/`original_completion` mapping. The
full-history dataset also has null canonical columns but failed earlier at the
S3 train-file download stage, so it does not isolate the validation writer.

A local metadata-only integrity pass over the successful 11,192-row control,
array ctx9, and scalar ctx9 files found zero malformed JSONL rows or empty
prompt/completion values. Both control and array ctx9 use one user message in
`prompt`, one assistant message in `completion`, string content, valid weights,
and prompt-ending user / completion assistant roles. Scalar ctx9 has strings
for both fields. All v4 serialization files have mode 0600; the older control
JSONL was mode 0664 and has now been tightened to 0600. Recomputed hashes still
match the stored control and ctx9 manifests. No row content was written to this
report.

This eliminates blank rows, malformed JSON, and the array-versus-scalar
representation as sufficient explanations. It does not distinguish a hidden
large-dataset row/split limit, v4-specific validation split behavior, or a
provider bug. Current raw-data docs say raw mode sends training-ready
prompt/completion rows as-is; the AutoScientist create docs require those fields
and allow explicit mapping, but do not document split construction, maximum raw
row counts, or validation-file writer constraints. A successful 11,192-row
control proves the same array representation can work, but it does not control
for row count or corpus-specific split distribution.

**No-job/no-upload validation plan:** ask Adaption support for the train/validation
split row counts, mapping resolution, rows rejected by validation serialization,
per-file input/output byte counts, and the provider trace around the empty temp
validation file for the three failed ctx9 run IDs; also ask whether raw SFT has a
row-count or per-row-length limit. In the meantime, only use read-only dataset
and run APIs. Do not submit another run or upload until Adaption supplies those
counters or confirms the canonical-column metadata discrepancy and a corrected
provider-side contract. A local subset would only be decisive after provider
confirms that a new upload/iteration is the diagnostic they need.

## 2026-10-20 00:52 UTC no-job qualification and next action

A fresh read-only Adaption API poll at 00:52 UTC confirms no v4-derived run is
active. The three ctx9 jobs remain failed at 0/1: `8d00b26c-de36-452a-abc2-5cd36b76036b`,
`33bba6d2-d9e5-408c-bd4d-76544d2cde78`, and
`ef278ee7-b04d-4014-9b7a-cb7ee81b66fd`. The full-history job
`7b859acc-f325-4022-92c7-b1a1ff40c2c3` remains failed at the earlier S3 download
stage. The successful control `8da8f685-7ef6-43c0-958e-ab34dbdcd520` remains
one-iteration succeeded on the 11,192-row dataset. A current non-launching
`recommend_hyperparams` for dataset `c00e322e-3842-4a56-9e6b-b9c81cf8b599`
and model `Qwen/Qwen3.6-35B-A3B` still returns a one-epoch LoRA recipe (rank/alpha
8, q/v, LR 0.0003, batch `max`, train-on-completions only); it returns no cost
or credit quote. The model catalog still lists Qwen3.6-35B-A3B for SFT LoRA.

The difference that is directly supported is scale: three ctx9 attempts across
two raw datasets with 522,658 rows (array and scalar prompt/completion forms)
fail at validation file preparation; the 11,192-row control succeeds. That is a 46.7× row-count
difference, but it does not establish a maximum. Current official raw-data docs
require a training-ready prompt/completion table and explain raw mode as
passing rows through as-is. AutoScientist documents `data_format` and
`column_mapping`, but publishes no maximum dataset row count, raw-file byte
limit, validation split method, split-size field, or per-row token limit. The
separate Adaptive Data `max_rows` option applies to an adaptation run, not raw
AutoScientist training and would change the data/credit workflow. AutoScientist
`max_iterations` caps optimization cycles, not examples. There is therefore no
documented exact truncation, shard size, or split transformation that both
avoids this failure and trains one model on the complete 522,658 rows. Do not
guesstimate a shard threshold: independent shard jobs would train independent
adapters unless Adaption confirms a supported resume-from-adapter path, and
would not equal one full-corpus run.

**Exact data contract already exercised:** JSONL, one row per assistant target,
raw dataset mapping `prompt -> prompt`, `completion -> completion`; processed
columns are `original_prompt`, `original_completion`. The successful control
and v4 array ctx9 each have `prompt` as a list of `{role, content, weight}`
messages ending in `user` and `completion` as assistant message(s), with string
content and weight 1. The scalar-text ctx9 variant has string prompt/completion.
`data_format="chat"` is documented for raw AutoScientist. Since the exact same
array structure succeeded on the control and scalar conversion did not fix v4,
no local format rewrite is presently justified.

**Next runnable action, without upload or training:**

1. In Adaption's app, select the existing ready scalar-text dataset
   `c00e322e-3842-4a56-9e6b-b9c81cf8b599` (or the ready array ctx9 dataset),
   select the original prompt/completion columns, Qwen3.6-35B-A3B, no domain or
   general augmentation, and the already-returned one-iteration LoRA recipe.
2. Proceed only to the documented final order-summary screen; record the
   separate AutoScientist training credit line, total credits, exact resolved
   config, and the current organization credit balance. Do not click Confirm.
   The app docs say this summary separates training from optional expansion
   costs. The API's `recommend_hyperparams` method is recipe-only and the create API
   starts a run; neither is a training quote. The available connector has no
   balance/billing-history operation.
3. In the same UI, review the raw column mapping and verify the column values
   are populated in the preview. Record whether the full-size raw dataset is
   accepted by the order-preview step and whether it reports a provider limit.
   This may expose a configuration/mapping problem before any charge, but does
   not itself explain the empty validation writer.
4. Capture the three failed run IDs above plus dataset IDs
   `5cf8efd5-3426-4cc4-b3cc-4d40f7912f9d` and
   `c00e322e-3842-4a56-9e6b-b9c81cf8b599` for Adaption Support. Request exact
   train/validation split counts, resolved source columns, rejected-row and
   serialized-row counts, input/output byte counts, temp validation-file
   writer error, and any row/file/token limits. Ask if AutoScientist supports
   resumable sequential shards and the initialization field if a documented
   cap exists. No support message has been sent.

A subsequent run is not yet qualified. First require (a) provider evidence of a
specific supported full-corpus transformation or fix to raw column metadata/
validation preparation, and (b) an exact pre-confirm training quote plus a
visible balance sufficient to cover it. After any later authorized run, verify
the actual credit debit against the pre-run balance and order summary; the
connector currently exposes neither actual debit nor numeric balance.

If provider diagnostics produce a supported fix and the preview quote is
covered, the exact previously exercised one-iteration request shape is:

```python
run = client.autoscientist.create(
    dataset_id="c00e322e-3842-4a56-9e6b-b9c81cf8b599",
    model="Qwen/Qwen3.6-35B-A3B",
    training_method="instruction",
    data_format="chat",
    column_mapping={
        "prompt": "original_prompt",
        "completion": "original_completion",
    },
    hyperparams={
        "training_type": "lora",
        "n_epochs": 1,
        "lora_r": 8,
        "lora_alpha": 8,
        "lora_trainable_modules": "q_proj,v_proj",
        "learning_rate": 0.0003,
        "batch_size": "max",
        "train_on_inputs": False,
    },
    augmentation_domain_rows=0,
    augmentation_general_rows=0,
    max_iterations=1,
)
```

This is documentation only and must not be executed until the support/quote
gates above are met. It specifies a full-dataset run; there is no supported
row-sampling parameter in the documented AutoScientist create schema.

Official references: [raw non-adapted SFT](https://docs.adaptionlabs.ai/autoscientist/run-on-non-adapted-data/),
[AutoScientist create API](https://docs.adaptionlabs.ai/api/resources/autoscientist/methods/create),
[recommend hyperparameters](https://docs.adaptionlabs.ai/api/resources/autoscientist/methods/recommend_hyperparams),
[large dataset processing](https://docs.adaptionlabs.ai/guides/processing-large-datasets),
and [AutoScientist order summary](https://docs.adaptionlabs.ai/tutorials/autoscientist-app-walkthrough/).

## 2026-10-20 live API and UI access refresh

The connected Adaption API was rechecked. Dataset
`c00e322e-3842-4a56-9e6b-b9c81cf8b599` remains `succeeded` with all 522,658
rows processed and columns `uuid`, `original_prompt`, and
`original_completion`; metadata still reports null prompt/completion columns.
All three v4-derived attempts remain failed before training. The newest
scalar-text attempt failed because its downloaded validation JSONL was 0 bytes.
The current non-launching recommendation for this dataset and
Qwen3.6-35B-A3B is one-epoch LoRA, rank/alpha 8, q/v projections, batch size
`max`, `train_on_inputs=false`, cosine schedule, and learning rate 0.0003. It
returns no price or credit balance. Dataset and run IDs, full returned fields,
and failure strings were observed directly from the authenticated API; no
training run was started.

The read-only order-summary and balance check could not be completed through
the UI in this environment: the Browserbase connector returned `Session
terminated`, `browse status` showed no connected browser/pages, and
`BROWSERBASE_API_KEY` is absent from the process environment. The Adaption
connector itself has no balance, billing-history, or AutoScientist price
estimate method. Therefore credit coverage remains unverified, and the prior
support/quote gates remain unchanged. No UI confirmation, upload, or job was
attempted.

## 2026-10-20 01:37 UTC authenticated access and quote-path refresh

Authenticated read-only calls at 01:37:34 UTC reconfirmed the three 522,658-row
v4-derived datasets are `succeeded` and all three ctx9 runs remain failed at 0/1 with
empty generated validation JSONL. The full-history attempt remains failed at
its earlier 60-second S3 train-file download; the 11,192-row control remains
succeeded and downloadable after one iteration. `Qwen/Qwen3.6-35B-A3B` remains
available for SFT/DPO LoRA. A fresh non-launching recommendation on the
scalar-text ctx9 dataset returned LoRA rank/alpha 8, q/v modules, one epoch,
LR 0.0003, batch `max`, and `train_on_inputs=false`. It contained no quote or
balance. Exact records are in
[`adaption-live-refresh-20261020T0137Z.json`](adaption-live-refresh-20261020T0137Z.json).

The exposed Adaption connector has no training-quote, balance, or billing-history
method. Its `recommend_hyperparams` endpoint resolves recipe from effective row
count and optional augmentation but returns hyperparameters only; `create`
starts a credit-spending job, so it is not a safe quote call. The separate
`datasets.adapt(estimate=true)` endpoint quotes Adaptive Data transformation,
not AutoScientist training. Current official docs say the app's final order
summary separates domain expansion, general expansion, and AutoScientist
training costs. A Browserbase session start returned `Session terminated`, so
no app order summary or balance was reachable in this refresh. No quote or
coverage is inferred. No upload, job, or message was created/sent.

## 2026-10-20 Adaption raw-ingest contract diagnosis

Fresh read-only `get_dataset` calls returned all three 522,658-row datasets
(`21f6d03f-5f56-41be-9070-14c8fccbf442`,
`5cf8efd5-3426-4cc4-b3cc-4d40f7912f9d`, and
`c00e322e-3842-4a56-9e6b-b9c81cf8b599`) as `succeeded`, with columns `uuid`,
`original_prompt`, and `original_completion`, but with both `prompt_column`
and `completion_column` null. The three failed ctx9 runs still record the
expected run-level mapping; their current public error says the downloaded
validation file was zero bytes before upload. This establishes that the empty
artifact is provider-side, not malformed local JSONL.

The official [dataset create API](https://docs.adaptionlabs.ai/api/resources/datasets/methods/create)
describes `processing_mode="raw"` and `column_mapping` as top-level request
fields, while the installed generated SDK and its documented `upload_file`
helper place them under `source`. An initial code change sent the fields at the
HTTP-docs top level and passed an offline request-assembly check. To resolve
the mismatch rather than assume either contract, I uploaded the frozen ctx9
file through that changed uploader, using the same full 522,658-target payload
and hash `4f2b4ef53dfc649f5bd6c5e943b4917d2bec9a8ade309a7caf865b2fd975e2a2`.
The provider accepted the 790,582,664-byte upload, but the resulting dataset
`60ea43c8-c965-4ab1-968a-b4b82be7703d` stayed `awaiting_input`, with columns
`prompt`/`completion` and null canonical `prompt_column`/`completion_column`.
Thus the docs-shaped upload does not make the dataset train-ready in the live
service. The polling process was stopped after repeated `awaiting_input`
responses; no training run or credit-spending operation was launched.

I restored the local uploader's original SDK-shaped request, because the
experimental HTTP-docs-shaped path failed the required live readiness check.
The frozen source file and previous Adaption datasets remain unchanged. The
new duplicate provider dataset is retained because the exposed connector has
no delete operation and no verified rollback path. Its private upload receipt
is under `ai/training/output/adaption_v4_ctx9_fixedraw_20261020/evidence/`
(mode 0600 in a mode 0700 directory). This proves a real discrepancy between
the published HTTP contract and the live service/SDK path; it does not explain
the earlier empty validation JSONL, since those failed runs had explicit
run-level mappings. Do not use the new dataset for training while it remains
`awaiting_input`. The unresolved next step is a provider-supported way to
resolve the ingestion-contract mismatch or set the canonical mapping on the
existing dataset, followed by a read-only readiness check before another
training attempt.

## 2026-10-20 05:15 UTC live dataset and row-limit refresh

A current read-only `get_dataset` on the latest docs-shaped upload,
`60ea43c8-c965-4ab1-968a-b4b82be7703d`, still returns `awaiting_input`, 522,658
rows, columns `prompt`/`completion`, null canonical prompt/completion mappings,
and null processed-row count. The prior `c00e322e-3842-4a56-9e6b-b9c81cf8b599`
remains `succeeded` with 522,658 processed rows and columns
`uuid`/`original_prompt`/`original_completion`, but canonical mapping fields
are also null. A non-launching `run_dataset_adaptation(estimate=true)` request
for the latest dataset with explicit `prompt`/`completion` mapping was rejected
before estimation: the requested 522,658 rows exceed the plan's 50,000-row
per-launch limit. No training, transformation, or credit spend occurred. The
connector still exposes no balance or price quote, so a multi-launch split
cannot be cost-bounded from this environment. Do not split and submit the
full source without a usable estimate and provider-supported dataset mapping.

## 2026-10-20 Adaption estimate and account-balance check

The official [dataset-status reference](https://docs.adaptionlabs.ai/api/resources/datasets/methods/get_status/)
defines `awaiting_input` as an uploaded dataset waiting for the user to start
Adaptive Data with a column mapping; it does not become processed by itself.
That matches the latest `60ea...` status. A read-only
`recommend_autoscientist_hyperparameters` call on this dataset returned
"Dataset is not ready yet". The older processed scalar-text `c00e...` dataset
is recognized by the same recommendation endpoint and returns Qwen 3.6 LoRA
settings, but its prior one-iteration training run failed before iteration 0
because the provider-generated validation JSONL was empty. This keeps the
readiness/inference failure distinct from the normal `awaiting_input` meaning.

I requested two non-launching Adaptive Data estimates on `60ea...`, using its
actual scalar `prompt`/`completion` columns and `estimate=true`:

- 50,000 rows: 500 estimated credits and 635 estimated minutes.
- 22,658 rows: 227 estimated credits and 294 estimated minutes.

The API rejects a single 522,658-row launch because the plan limit is 50,000
rows. If the full payload were partitioned into ten 50,000-row batches plus one
22,658-row batch, the quoted Adaptive Data total would be 5,227 credits and
6,644 estimated minutes (about 110.7 hours of provider processing). This is a
calculation from the two returned estimates, not an AutoScientist training
quote, not proof that the service permits arbitrary chunks, and not a balance
or affordability finding. No credit-spending job was created. Current public
docs say estimates do not launch work and actual usage can vary ([estimate and
pricing contract](https://docs.adaptionlabs.ai/api/resources/datasets/methods/adapt/)).

A read-only browser check of the documented app URL
`https://adaptionlabs.ai/app` reached the sign-in page, so the account balance
could not be read. The browser session was closed. The API inventory still has
no balance endpoint. Do not represent the 5,227-credit Adaptive Data estimate
as training cost or as confirmed available credit.

### 2026-10-20 06:54 UTC live Adaption recheck

The current run list has no active jobs. The three ctx9 AutoScientist attempts
remain failed at 0/1; the 11,192-row control remains succeeded and downloadable.
The full-size docs-shaped raw dataset `60ea43c8-c965-4ab1-968a-b4b82be7703d`
still reports `awaiting_input`, 522,658 rows, and canonical `prompt` and
`completion` fields. A fresh no-launch Qwen3.6 hyperparameter recommendation
was rejected with “Dataset is not ready yet.” Per the current raw workflow,
do not call `datasets.adapt` for this passthrough dataset; the live status/API
disagreement remains unresolved. No training or augmentation was started.
