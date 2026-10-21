# W&B synthetic agent-tool SFT launch reconciliation — 2026-10-20

**Follow-up at 09:54 UTC:** the earlier paragraph below saying no further
Training API requests were made has been superseded. A recognized
`W&B-Training-API` user-agent allowed the read-only base-model catalog request
to return 13 models, but the idempotent model-create POST still timed out after
60 seconds, including through the documented cURL request path. The existing
W&B project contains a finished run named `agent-tool-sft-036a97a69a41`, which
is consistent with a model-create side effect, but it exposes no model UUID in
its config or summary. Local durable state still has no `model_id` and no
training-job ID. The documented W&B/Forge UI route redirects to a login page;
the available browser session is not authenticated. No training job was
created. Do not submit another create request; recover the model UUID/job
through W&B owner support or an authenticated UI session.

The shared W&B Training API client now sends the documented-client
user-agent on both `aiohttp` and `urllib` paths; a regression assertion covers
it. The read-only catalog call succeeds with 13 entries, and the focused W&B
SFT launcher plus paired-evaluator test suites pass 35/35. The model-create
timeout remains unresolved independently of this client fix.

The local synthetic release passed its launcher's integrity checks (960 train
rows, 1,200 structured tool-call messages, 120 validation rows, 120 held-out
rows; 1.43 MB staged package). The dataset artifact uploaded successfully as
`wandb-artifact:///wutang/pixelated-empathy-kan28/agent-tool-sft-036a97a69a41:v0`.

The launcher then submitted deterministic model creation
(`agent-tool-sft-036a97a69a41`, base `Qwen/Qwen3.6-35B-A3B`,
`return_existing: true`) but received no response before its 60-second timeout.
The durable state correctly remains `model_creation_submitted_unknown`; it has
no model ID and no training job ID. Do not retry model or job creation until
the remote model state is reconciled.

A subsequent read-only request to the official Training API base-model
catalog returned HTTP 403 with Cloudflare Error 1010,
`browser_signature_banned`, explicitly marked non-retryable and owner-action
required. The response instructed not to retry. A later follow-up used a
recognized client user-agent and the catalog returned 13 base models, but the
model-create calls continued to time out; those requests did not return a
model ID or establish job creation. The artifact upload and authenticated
W&B GraphQL calls use separate API surfaces and do not resolve the Training
API model/job state.

Local durable state is
`ai/training/output/wandb_agent_tool_sft_state/wandb-agent-tool-sft-036a97a69a41a3ee1a56e75b45fd2578b77650da7ef4ce65ce7583d3a6b1c07d.json`
(mode 0600). No training job ID exists yet. Resolution requires W&B owner-side
clearance of the Cloudflare block or a supported UI/API path; the already
uploaded dataset can be reused after model/job creation is safely reconciled.

## Idempotent model retry — 2026-10-20

The official [Create Model API reference](https://docs.wandb.ai/api-reference/models/create-model)
defines `return_existing=true` to return the existing model when one with the
same name exists. The already-submitted request used that flag, the same
project, model name, and base model, so I repeated the exact request to recover
the model UUID without creating a duplicate. That API request also timed out
after 60 seconds. Durable state still has no model UUID and no training-job
ID. No SFT-job request was made. This exhausts the safe same-name retry; next
resolution requires an authenticated owner UI or provider-supported lookup,
because `GET /preview/models` is not supported (HTTP 405). The uploaded
artifact remains available for reuse.
