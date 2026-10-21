# Provider qualification — 2026-10-17 (historical snapshot; current price qualification is in the execution handoff)

Status: partial. Checks used existing authenticated sessions and public
official docs. This worker made no inference, training, upload, deployment, or
resource-creation calls. The evaluation worker's first six synthetic W&B
inference calls returned HTTP 400 because the request included `stop: []`; the
gateway rejects empty stop arrays even though the public schema lists an empty
default. The corrected five-case synthetic smoke omitted `stop` and succeeded
5/5 under the authorized cumulative $0.01 ceiling. Three outputs were
truncated at the 256-token cap. API keys were not printed, written, or included
here; the exposed Together token was not used.

## W&B: training-ready base and bounded inference smoke

Authenticated `GET /v1/preview/base-models` returned 13 training bases,
including `Qwen/Qwen3.6-35B-A3B`. The same exact base is available through the
current W&B Inference catalog and matches Adaption run 2. W&B's read-only
`GET /v1/system-check` returned healthy. The model catalog plus system check
qualifies this base at the account's training API level; a model resource or
job was not created. The destination project
`wutang/pixelated-empathy-kan28` is private (`access=PRIVATE` in an authenticated
read-only project metadata query). Remaining artifact storage was not queried.

The 2026-10-17 snapshot below was too cautious about the published training
terms. Rechecked against W&B's current official pages on 2026-10-20: Serverless
SFT remains in public preview, and W&B states that Serverless SFT/RL training
is free during public preview, with pricing to be announced at general
availability. This establishes the published service status and training
price, but not account-specific eligibility or coverage for inference and
storage. The `/preview/` API path alone is not proof of free pricing. Trained
checkpoints are LoRA artifacts; storage is billed according to the workspace
plan/quota, which remains unknown for this account. W&B says the minimum 5 GB
plan storage is typically enough for about 30 LoRAs, or roughly 170 MB per
adapter if divided evenly; this is an estimate, not an account-specific
ceiling. Check the current project storage and account terms before assuming
there is room for additional checkpoints.

Current sources: [W&B Training Pricing](https://wandb.ai/site/pricing/training/)
states that training is free during public preview and storage is billed
monthly; [W&B Serverless Training API reference](https://docs.wandb.ai/api-reference/training-jobs/sft-training-jobs)
still documents the SFT job endpoint under `/v1/preview/`. The preview endpoint
and public-preview label agree, but only the pricing page establishes the
published training-price statement.
W&B's documented read-only `POST /files/query_stats` returns total file bytes
for one project, not remaining account quota. The read-only qualification
checks did not query it. W&B's SFT API requires a model resource created with
`POST /v1/preview/models`, then an SFT job created with
`POST /v1/preview/sft-training-jobs`. The job points to a W&B artifact URI and
expects `trajectories.jsonl` and `metadata.json`. Basic config fields are
`batch_size` (`1..32` or `auto`), `learning_rate`, `assistant_turns` (`all` or
`last`), and optional metric logging. The local launcher
[`wandb_sft_g04.py`](../../../ai/training/launch/wandb_sft_g04.py) is dry-run by default. It
requires the future `g04-release-manifest.json` status
`approved_for_research_training`, source-candidate hash, research-only scope and
limitations, exact train/validation/test hashes and counts, verified seed-group
disjointness evidence, `upload_gate: true`, source-candidate and internal-manifest
file identities, and assistant/user loss weights. Before accepting the release,
it independently hashes/counts those source files, compares the exact row IDs
and seed-group memberships in the rowref and internal manifests, recomputes
group intersections, and checks heldout exclusions. It packages the exact
approved train bytes without re-rendering. Its baseline and single data-ablation
arms use `batch_size=auto`, `learning_rate=0.0001`, and `assistant_turns=all`.
The learning rate is an explicit recipe value mirrored from the existing local
W&B ART SFT launcher, not a claimed service default; `auto` is resolved by the
provider and response/status config is captured for audit. The baseline and
data-ablation configs are otherwise identical; the ablation changes only its
approved dataset payload and requires a separate
`ablations.data_ablation.train` entry.
Every assistant target is included while user tokens are excluded by the
release's `weight=0` mask. The actual API config, release and artifact hashes,
artifact URI, model/job UUIDs, status, and polling state are written locally
with mode 0600. The launcher validates the destination project as PRIVATE and
rechecks the authenticated trainable base catalog before upload.

Dry-run reports the measured input artifact byte count. Training price and
account entitlement are unverified; do not assume the historical public-preview
offer is active. The legacy page claimed at least 5 GB storage,
which W&B says is typically enough for about 30 LoRAs; storage above quota may
be billed monthly. The documented read-only project stats endpoint reports
bytes already used in a single project, not remaining account quota. No exact
account headroom or expected checkpoint size was available, so the launcher
records the limitation without inventing a quota check or treating the average
as a checkpoint bound. No data, model, or job was created. The endpoint contract follows the [W&B SFT create API](https://docs.wandb.ai/api-reference/training-jobs/sft-training-job-create),
[model creation API](https://docs.wandb.ai/api-reference/models/create-model),
and [serverless training usage limits](https://docs.wandb.ai/training/serverless-rl/usage-limits).

### Dataset and sequence-size qualification

I measured the exact current draft train payload locally by streaming JSONL and
recording counts only; no row text was emitted. Its SHA-256 is
`60031b4233196cc66f0467c569486a873caf31eddf383b04c40b9619ec0d5aef`, with
410 examples and 13,248 messages (6,624 user and 6,624 assistant). The longest
example contains 92,707 Unicode characters / 93,061 UTF-8 content bytes across
54 messages; p95 and p99 content sizes are 49,196 and 58,417 bytes. The largest
single message is 5,749 UTF-8 bytes. The exact provider JSONL is 12,445,999
bytes. The canonical G04 release remains diagnostic and upload-gated.

No `transformers`, `tokenizers`, or `tiktoken` package and no cached Qwen
tokenizer were present, so I did not install or download tokenizer weights.
93,061 bytes is a conservative raw-text token upper-bound proxy only under a
byte-fallback tokenizer assumption; it is not a validated Qwen token count and
does not include provider chat-template markers. Qwen's official model config
sets native text `max_position_embeddings` to 262,144, but W&B's public SFT
create schema and serverless-training documentation do not publish a per-example
token/context cap, dataset row/size quota, training-step quota, or whether
overlength rows are rejected, truncated, or otherwise handled. This comparison
does not certify provider acceptance or no-truncation behavior.

The public create request exposes `batch_size` and `learning_rate` in `config`;
the SFT config documentation also describes `assistant_turns=all|last`.
This launcher explicitly sends `batch_size=auto`, `learning_rate=0.0001`, and
`assistant_turns=all`. The API schema does not document an epoch/max-sequence
length setting or a training stop-sequence control; epochs, max steps, and
related scalar values are captured only if the provider returns them in job
metadata. `stop` belongs to inference requests and is omitted when empty. The
launcher copies the hashed provider payload exactly and applies no local
truncation. Before any future create, it will recheck the approved payload hash,
role/weight contract, project privacy, and current model catalog; actual provider
limits and truncation remain unknown because the create endpoint is a
resource-creation call rather than a dry-run validator.

The exact model is present in the current W&B Inference catalog. The synthetic
smoke route is `https://api.inference.wandb.ai/v1/chat/completions` with
`WANDB_API_KEY` and `project="wutang/pixelated-empathy-kan28"` attribution.
Published cost is $0.25/M input and $1.25/M output tokens. The root-authorized
smoke is capped at five synthetic-only calls, <=512 input tokens and <=256
output tokens each, concurrency 1, no retries. This caps the estimate at
$0.00224; enforce a $0.01 ceiling, pretokenize and reject over-limit input, and
stop if usage metadata is absent. The user confirmed substantial W&B inference
credits; the public API did not expose the remaining balance. The corrected
five-case request omitted `stop` and succeeded 5/5; three responses truncated
at 256 tokens. Successful-call usage estimate was $0.00147125; including seven
earlier failed attempts at an upper-bound estimate, cumulative cost remains
under the $0.01 authorized ceiling.

## W&B and Qwen terms review

Public official terms reviewed October 17, 2026 do not establish a request-level
retention period or an exclusive license to W&B inference outputs. W&B's AI
Terms (last updated August 4, 2026) classify prompts and outputs as Customer
Data between W&B and the customer, excluding W&B Background IP, and make the
customer responsible for having rights to submit inputs. The Master Service
Agreement (last updated September 30, 2026) gives W&B rights to process Customer
Data to provide and improve W&B services, develop offerings, and provide or
improve AI features; the free-use terms also allow testing and development use
of free-customer data. The agreement says Customer Data should be exported
before termination and is deleted according to W&B policy after termination;
that is not a per-call retention commitment. W&B's privacy link redirects to
CoreWeave. CoreWeave's policy says it collects inputs and outputs and may use
service content to operate, evaluate, and improve services, but explicitly
excludes customer data processed solely as a processor. It gives no precise
retention term for W&B inference requests.

The reviewed terms do not expressly prohibit customer reuse or third-party
training transfer of outputs, but they also do not grant a distinct blanket
output license or resolve rights in the source prompts. Thus the terms support
using W&B to process a fully authorized synthetic research set, while any
external training transfer still depends on source/rights evidence and the
receiving provider's terms. W&B's MSA defines HIPAA-regulated patient/medical
data and EU special-category data as Sensitive Data and prohibits sending it
without prior written consent; only the approved synthetic, privacy-screened
release is in scope.

For the campaign fallback, a reasonable bounded basis exists for newly
hardcoded first-party synthetic prompts with no external seed text and no
real-person or regulated health data: generate with the identified W&B Qwen
model, preserve its exact generation receipt, and use the output only in W&B's
own research SFT service under the same terms. That route accepts W&B's stated
service, product-improvement, and free-plan testing/development uses. This
does not clear the existing historical rows whose teacher identity/terms are
unknown and does not authorize a transfer to Fireworks or Adaption.

The exact W&B training base, `Qwen/Qwen3.6-35B-A3B`, is marked Apache-2.0 in
the official Qwen repository, whose `LICENSE` is Apache License 2.0. That
license governs use of the model work subject to its conditions; it does not
itself clear training-data provenance or grant a separate license to model
outputs.

The current training catalog also includes `OpenPipe/Qwen3-14B-Instruct` and
`Qwen/Qwen3-30B-A3B-Instruct-2507`, although neither is in this account's
inference catalog. Their account-specific inference routes are not qualified.
For already trained W&B models, use
`wandb-artifact:///<entity>/<project>/<model-name>:<step>` through the W&B
Training API at `https://api.training.wandb.ai/v1`.

## Fireworks

Authenticated metadata confirms `accounts/fireworks/models/muse-glimmer-30b`
is `READY`, supports supervised LoRA and Serverless Training. Fireworks' public
pricing page currently advertises Muse Glimmer 30B SFT free through November
30, 2026, via the UI and Serverless Training API, no credit card required. The
official starter's read-only `plan --surface serverless` was run with the
existing installed Fireworks SDK; it resolved account `linencloset`, reported
the offer active on October 17, and printed `$0 (promotional)` training. No
resource was created. That starter computes activity from a local deadline of
November 1 PDT, rather than querying promotion activation on the account; the
live pricing page remains authoritative for the later published expiry. The
account billing summary showed $0.00 Serverless Training Tokens for the
checked period, but no remaining balance or activation status. Current API
model metadata says `supportsServerless=false` and
`serverlessModes=[]`, and the account inference model list omitted Muse
Glimmer, while the public model page lists serverless inference at $0.35/M
input and $1.50/M output. That mismatch leaves account serving unqualified.
The read-only plan explicitly marks in-session evaluation sampling as a
separate uncovered cost line. The live pricing page lists Muse Glimmer sample
at $4.88/M tokens and prefill at $1.96/M tokens. The SFT offer does not cover
sampling, DPO, RL, deployments, or outside-session inference. For a future
G04-approved Fireworks SFT job, use the cookbook's plan immediately before
launch and omit `--allow-paid`; with a current SFT promotion its launcher
supports a free training path. Keep evaluation separate until its own coverage
is verified.

The existing pilot adapter export remains denied: authenticated
`getDownloadEndpoint` returned HTTP 400 with “model downloads are temporarily
disabled, please contact Fireworks AI to get access.” There are no account
deployments. Fireworks documents active-session sampling for training, but its
pricing table separately meters serverless prefill, sample, and train tokens;
the SFT offer does not qualify those other meters as free. A promoted adapter
requires an on-demand or preemptible deployment. Fireworks inference credits
remain tentative, so this route has no bounded inference plan.

### Pricing scope note — 2026-10-18

The current Fireworks public pricing page separately lists paid token rates for
Serverless Training API (including Muse Glimmer 30B prefill, sample, and train
meters) and Managed Training. This public tariff is not proof that an account's
promotional Managed Training offer is inactive, and the promotion does not make
sampling or inference free. Recheck the account's current offer immediately
before any create call; the earlier read-only cookbook result was promotional
but its local deadline logic was not authoritative. The Muse Glimmer public
model page currently advertises serverless inference at $0.35/M input and
$1.50/M output, while prior account metadata did not show that model in the
inference catalog. Account-level inference remains unqualified. Sources:
[Fireworks pricing](https://fireworks.ai/pricing),
[Muse Glimmer model page](https://fireworks.ai/models/fireworks/muse-glimmer-30b).

## Adaption — live account recheck (2026-10-19 16:12 UTC)

Three authenticated read-only calls were repeated: `list_training_models`,
`list_datasets(limit=50)`, and `list_autoscientist_runs(limit=50)`. They confirm
`Qwen/Qwen3.6-35B-A3B` remains available for SFT/DPO LoRA; historical run 2
(`8da8f685-7ef6-43c0-958e-ab34dbdcd520`) is still succeeded and downloadable,
with platform win rate 0.6414. The 11,192-row training dataset is succeeded;
the separate 418-row dataset remains `awaiting_input`. Both list results have
no evaluation summary. No inference, estimate, dataset write, or training call
was made.

The user-confirmed Adaption credit existence is recorded, but no current
numeric balance, expiry, eligible-use scope, or per-run deduction is exposed by
the available connector. It therefore cannot bound another training run. The
connector also exposes no Adaption-hosted inference endpoint. Run 2 is already
exported locally (path above), but serving it locally has not been qualified on
the available host. The frozen 522-row breakaway dataset is not uploaded or
qualified for Adaption. Continue with the historical adapter only after E00
qualifies an inference route; do not create an Adaption dataset/run until
provenance eligibility and exact credit coverage are evidenced. Detailed
current evidence is recorded in `provider-qualification.json` under
`adaption.live_read_only_recheck_2026_10_19`.

## Adaption

The live catalog includes `Qwen/Qwen3.6-35B-A3B` for SFT/DPO LoRA. Existing
run 2, `8da8f685-7ef6-43c0-958e-ab34dbdcd520`, succeeded, is downloadable, and
is already local at
`ai/training/output/arc_corpus/export/adaption_run2_v1/checkpoint_run2/` (46 MB).
Its 0.6414 platform win rate is not a clinical verdict. The connector exposes
datasets, runs, and model catalogs, but no balance or cost estimate. The
downloaded adapter has no Adaption-hosted inference endpoint; the host has
28 GiB RAM and no NVIDIA utility, so the 35B base was not loaded locally. Reuse
run 2 only after E00 qualifies a matching-base route. Do not start another run
without an exact credit estimate.

The live Adaption model catalog's eligible non-Llama choices are listed in the
JSON evidence file. Llama models remain excluded by user preference; Qwen 3.8
remains excluded. The run-2 Qwen 3.6 model is eligible for LoRA SFT/DPO.

The exact returned IDs, request contracts, cost math, and remaining checks are
in [`provider-qualification.json`](provider-qualification.json).

The W&B launcher and its local tests pass Ruff and the 9-case focused pytest
suite. The canonical G04 draft still fails closed before artifact preparation;
no provider writes were made. The test file is ignored by the `ai` submodule's
existing ignore rules. Run the focused checks with:

```bash
uv run --no-project --with ruff ruff check ai/training/launch/wandb_sft_g04.py ai/training/tests/test_wandb_sft_g04.py
uv run --with pytest --no-project python -m pytest ai/training/tests/test_wandb_sft_g04.py -q
```

## Source links

- [Fireworks Muse Glimmer training cookbook](https://docs.fireworks.ai/fine-tuning/training-api/cookbook/muse-glimmer)
- [Fireworks model training matrix](https://docs.fireworks.ai/fine-tuning/models)
- [Fireworks trained-model evaluation](https://docs.fireworks.ai/fine-tuning/evaluating-fine-tuned-models)
- [Fireworks LoRA deployment and download](https://docs.fireworks.ai/fine-tuning/deploying-loras)
- [Fireworks account cost reporting](https://docs.fireworks.ai/accounts/exporting-usage-and-costs)
- [Fireworks pricing and Muse Glimmer SFT offer](https://fireworks.ai/pricing)
- [Fireworks Muse Glimmer model page](https://fireworks.ai/models/fireworks/muse-glimmer-30b)
- [W&B inference model card](https://wandb.ai/site/inference-model/cw_qwen_qwen3.6-35b-a3b/)
- [W&B inference pricing](https://wandb.ai/site/pricing/inference/)
- [W&B AI Terms](https://wandb.ai/site/ai-terms/)
- [W&B Master Service Agreement](https://wandb.ai/site/terms/)
- [CoreWeave Privacy Policy](https://docs.coreweave.com/policies/terms-of-service/privacy-policy)
- [Qwen3.6-35B-A3B model card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/blob/main/README.md)
- [Qwen3.6-35B-A3B Apache-2.0 license](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/blob/main/LICENSE)
- [W&B Training pricing](https://site.wandb.ai/pricing/training/)
- [W&B Training API overview](https://docs.wandb.ai/api-reference/training-api-overview)
- [W&B SFT job schema](https://docs.wandb.ai/api-reference/training-jobs/sft-training-job-create)
- [W&B Serverless SFT guide](https://docs.wandb.ai/training/serverless-sft)
- [W&B trained model endpoint](https://docs.wandb.ai/training/serverless-rl/use-trained-models)
- [W&B serverless usage and storage](https://docs.wandb.ai/training/serverless-rl/usage-limits)
- [Qwen3.6-35B-A3B model config](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/blob/main/config.json)

## Fireworks live qualification refresh — 2026-10-19

The current Muse Glimmer page advertises free SFT through the UI and Serverless
Training API until **2026-11-30**, with no credit card required. This supersedes
the offer deadline stated in the October 10 notes and the October 19 user
message. The authenticated account model resource reports SFT support, but the
current model page marks ordinary serverless inference unsupported; the
previous authenticated catalog check likewise omitted Muse Glimmer, so the
120-case Fireworks base-inference run did not succeed.

The Serverless Training documentation now describes a viable experiment-only
evaluation path: save sampler checkpoints and sample them while the training
session is active. Training checkpoints contain optimizer state and are
resumable but not promotable; sampler checkpoints are inference weights but
not resumable. After the session, a sampler checkpoint must be promoted and
served through an on-demand deployment; Fireworks states trained LoRAs are not
available for serverless serving. This account's existing model download check
was denied, so this does not establish local weight export. The serverless
training API also lists separate prefill/sample/train token meters; do not
assume the managed SFT promotion covers sampling or post-run deployment. No
Fireworks training job or deployment was created in this refresh.

Sources checked: [Muse Glimmer model page](https://fireworks.ai/models/fireworks/muse-glimmer-30b),
[Fireworks pricing](https://fireworks.ai/pricing), and
[Serverless Training lifecycle, sampling, checkpoints, promotion, and serving](https://docs.fireworks.ai/fine-tuning/training-api/serverless).
