# Provider terms and data handling audit

**Reviewed:** 2026-10-18  
**Scope:** Public first-party materials for W&B Inference and Serverless Training, Fireworks inference and training, and Adaption. This
is an operational source review, not a legal opinion or a substitute for the account's accepted contract, order form, DPA, or settings.

## Decision for the current data gate

Public provider statements do not establish that the project may submit the recovered dataset or the 522-row draft. They do not
establish our rights to the source material, clinical-data authorization, or permissions to train and transfer it. Keep
`upload_gate:false` until source rights, privacy review, and the applicable account contract/settings are documented. The
synthetic-only W&B inference probe is distinct from dataset upload or training.

## Findings by provider

### Weights & Biases (W&B)

- **Inference inputs/outputs and improvement use:** W&B AI Terms (last updated 2026-08-04) define submitted Input and returned Output
  as Customer Data between the parties (subject to W&B Background IP) and put responsibility on the customer to obtain rights and
  permissions. The same terms grant W&B rights to use Customer Data to provide/support, develop, and improve W&B Assets, subject to
  customer-configured settings where applicable. The public language therefore does not support assuming a blanket no-improvement-use
  rule; verify the actual setting and account terms. [W&B AI Terms](https://wandb.ai/site/ai-terms/)
- **Third-party transfer:** W&B AI Terms require compliance with third-party AI terms. W&B's MSA says use of Third-Party Platforms is
  governed by the customer's agreement with that provider and may enable data exchange between W&B Assets and those platforms. This is
  directly relevant when W&B Inference routes to a model/provider; identify the selected model's serving provider and terms for the
  actual run. [W&B AI Terms](https://wandb.ai/site/ai-terms/), [W&B MSA](https://site.wandb.ai/terms/)
- **Retention/deletion:** The public W&B DPA says personal data is retained for the agreement term as its listed criterion, with
  deletion/return on request or termination subject to legal retention and isolated backup copies eventually deleted under standard
  deletion policies. This is not a specific inference prompt/output retention schedule. The DPA permits subprocessors and references
  the periodically updated subprocessor list. [W&B DPA](https://wandb.ai/site/dpa/), [W&B
  Subprocessors](https://wandb.ai/site/wb-subprocessors/)
- **Serverless Training:** W&B says its Training service logs metrics and rollout traces to the W&B workspace; pricing documentation
  says trained LoRA checkpoints are stored for evaluation, serving, or continued training, and storage is billed by plan. Training is
  explicitly described as free during public preview on W&B's published Training Pricing page (checked 2026-10-19). The Serverless Training docs also label the feature public preview. Although the docs repository is archived and the training-pricing URL now redirects to CoreWeave Forge, those facts do not erase the published preview statement; the redirect does make the current pricing page difficult to independently reopen. This published offer is distinct from account-level entitlement, which remains unverified for our current runs. The public pages reviewed do not spell out a complete data-retention period,
  model/data rights allocation, or whether training inputs/outputs are used for general model improvement. Apply the account
  agreement/DPA and obtain written product-specific clarification for those points. [W&B Training](https://wandb.ai/site/wb-training/),
  [W&B Training Pricing](https://site.wandb.ai/pricing/training/)

### Fireworks AI

- **Inference inputs/outputs and retention:** Fireworks docs say open-model prompts and generations are not logged or stored by
  default, with content held in volatile memory for the request; metadata such as token counts is logged. For the Responses API,
  `store=True` is the default and stores conversation messages, model responses, and tool calls for 30 days; `store=False` disables
  storage, and a delete endpoint is documented. The Responses API behavior is endpoint-specific; do not generalize it to other
  endpoints. [Zero Data Retention docs](https://docs.fireworks.ai/guides/security_compliance/data_handling)
- **Improvement/training use:** Fireworks' privacy notice states it does not use prompts, training data, or API inputs to train or
  improve its models without explicit opt-in. It also describes zero retention for open models absent opt-in. However, the notice
  explicitly says it is not a contract and directs business customers whose processing is as a service provider to the applicable
  customer's notice. Confirm the binding terms and any enabled opt-ins/settings in our account. [Fireworks Privacy
  Notice](https://fireworks.ai/privacy-policy)
- **Training dataset retention / output rights:** Managed SFT documentation explains dataset upload and job setup, but the public pages
  reviewed do not provide a complete retention/deletion schedule for uploaded training datasets or an explicit allocation of rights in
  resulting trained weights. It documents dataset deletion operations, but an API/CLI delete capability alone is not a deletion
  commitment or proof that derived artifacts/backups are removed. [Managed SFT
  docs](https://docs.fireworks.ai/fine-tuning/fine-tuning-models), [Delete resources
  docs](https://docs.fireworks.ai/tools-sdks/firectl/commands/delete-resources)
- **Training option with customer-controlled storage:** Fireworks documents secure RFT using Bring Your Own Bucket, with
  rollouts/evaluation infrastructure in the customer's environment and optional checkpoint registration to customer storage. This is a
  specific RFT design, not evidence that ordinary managed SFT or Serverless Training has identical data handling. [Secure RFT
  docs](https://docs.fireworks.ai/guides/security_compliance/secure_training/secure_rft)
- **Cross-provider transfer:** Fireworks' public inference statement says its own serving request is processed on its infrastructure
  and is not forwarded to another inference endpoint; that statement concerns routing, not all infrastructure subprocessors, training
  services, or the model's licensing terms. Its privacy notice separately permits service-provider and international processing
  disclosures. [Fireworks Privacy Notice](https://fireworks.ai/privacy-policy), [Fireworks data
  handling](https://docs.fireworks.ai/guides/security_compliance/data_handling)

### Adaption

- **Product behavior verified:** Adaption's official docs describe Adaptive Data as ingesting, transforming, evaluating, exporting
  datasets and AutoScientist as running model training. These pages show that data and derived outputs are processed through its
  service; they are not by themselves contractual privacy or rights commitments. [Adaption docs](https://docs.adaptionlabs.ai/), [API
  getting started](https://docs.adaptionlabs.ai/introduction/getting-started)
- **Legal terms not verifiable from the public page in this review:** Adaption's official FAQ links [Terms of
  service](https://adaptionlabs.ai/terms-of-service) and [Privacy policy](https://adaptionlabs.ai/privacy-policy), but both pages
  returned only a tracking pixel/no substantive legal text to the browser fetch. The available first-party docs did not expose clauses
  establishing customer ownership/license of submitted data and generated dataset/model outputs, retention/deletion periods, general
  training/improvement use, or onward transfers/subprocessors. Mark each as **unverified**, not as permissive or prohibited; obtain
  readable applicable terms/DPA and written answers from Adaption before sending non-synthetic or sensitive data.
- **Output ownership marketing:** Adaption's homepage markets custom model training as “yours to own, serve, and evolve.” This is
  marketing language, not sufficient evidence of the precise rights, license scope, exceptions, or export/retention terms in the
  applicable contract. [Adaption homepage](https://adaptionlabs.ai/)

## Verified public facts versus unresolved account questions

| Question | Public evidence | Still needs account/human confirmation |
|---|---|---|
| May we submit this dataset? | Each service expects customer to have rights/permissions or places responsibility on customer; no public source clears our source dataset. | Source licenses/consents, clinical privacy and purpose authorization, BAA/DPA where required, data minimization, customer account contract. |
| Does the provider use data to improve its models? | W&B AI Terms permit use for W&B Assets subject to settings; Fireworks states no training/improvement absent explicit opt-in; Adaption legal terms could not be verified. | Effective settings, product-specific terms, opt-in state, scope of training vs service improvement, retention of derived signals. |
| Who owns outputs and trained weights? | W&B treats AI Input/Output as Customer Data subject to background IP; Fireworks and Adaption public materials reviewed do not settle exact customer rights for outputs/weights. | Account agreement, model/base-model licenses, rights to adapted data, LoRA/checkpoint export and continued-use terms. |
| How long is data retained? | Fireworks documents inference retention defaults and Responses API 30 days; W&B DPA gives a personal-data criterion and backup caveat; Adaption public legal page unavailable. | Exact training dataset/job/checkpoint/log retention, backup deletion, deletion propagation, retrievability after account/job termination. |
| Is data sent to another provider? | W&B explicitly warns Third-Party Platforms can exchange data; Fireworks says its inference endpoint does not forward inference requests, while disclosing service providers; Adaption's exact subprocessors not verified. | Actual endpoint/model/provider, subprocessors, regions, onward transfers, and any human access/review. |

## Required clearance evidence before any real-data upload or training

1. Archive the accepted order form/contract, current product terms, DPA/BAA if applicable, and relevant settings screenshots or
   provider confirmation for the exact W&B/Fireworks/Adaption account and product.
2. Obtain written answers for training dataset retention/deletion (including backups), checkpoint/model rights and portability, use for
   service/model improvement, and subprocessors/regions.
3. Confirm that every dataset source and derived example is licensed/authorized for the specific processing and downstream
   model-training use, and that privacy review approves the scope.
4. Record the chosen endpoint's model provider and terms. For W&B, do not infer the serving provider from W&B branding alone; identify
   the actual model and any third-party processing terms.
5. Preserve the existing release gate until evidence is attached to the dataset artifact and approved by the responsible reviewer.

## Source notes

Reviewed public first-party pages on 2026-10-18. Search results and rendered policy pages may change; preserve a copy or content hash
of applicable terms at the time of any future submission. Provider documentation is product guidance, while the signed/accepted
contract controls where it conflicts. No provider accounts were accessed and no credentials, provider calls, uploads, or legal
determinations were made for this audit.

## Addendum: plausible 2026-09-17 Vercel AI Gateway / DeepSeek API generation path

**Addendum reviewed:** 2026-10-18. This addresses the two W&B candidate generator runs on 2026-09-17 whose saved config identifies
`backend=vercel` and `model=deepseek/deepseek-v4-flash-0731`. This is the recorded configuration, not a request-level routing receipt.
The W&B metadata reviewed for those runs did not contain a DeepSeek provider receipt or a provider/policy version hash. The assessment
below separates public documents available now from what can actually be proven about the terms accepted on the run date.

### Vercel AI Gateway

- **What the current public AI Product Terms say:** Vercel's [AI Product Terms](https://vercel.com/legal/ai-product-terms) identify AI
  Gateway as a Vercel AI product and define third-party AI providers as Non-Vercel Services. Section 8 says Customer Content sent to or
  received from those services is subject to the applicable third party's terms and privacy notices. The page is marked last updated
  March 17, 2026, effective March 31, 2026. Those dates precede September 17, but the currently published page is not itself an
  archived acceptance receipt for our account.
- **Sensitive data restriction:** Section 3.4 of the current AI Product Terms says, “You must not include any sensitive personal
  information (such as health information...) in your Input.” Because this is a direct restriction in the governing product terms, no
  real clinical or health-related personal data should be sent through AI Gateway under these terms. Whether the historical
  synthetic-generation requests contained any sensitive personal information cannot be established from the saved run metadata alone
  and must be checked against the exact request inputs before concluding whether this clause was implicated.
- **Output rights:** Section 6.2 says that, as between customer and Vercel, customer owns Customer Content and Vercel assigns any
  rights it has in Output. But the same section says output may not be unique, that the assignment does not extend to other users'
  output or third-party rights, and that the customer must assess IP rights and commercial usability. This allocation does not
  establish rights in underlying training/source data or override the provider terms for AI Gateway requests.
- **Retention/use in Gateway:** Current Vercel documentation says the gateway layer does not retain prompts or outputs and deletes user
  data after the request; provider retention is separate. It says ZDR provider routing is opt-in and, when enabled, routes only to
  providers with negotiated ZDR agreements. Vercel's April 6, 2026 announcement describes team-wide ZDR and request-level
  `zeroDataRetention` / `disallowPromptTraining` controls. These are current/product statements, not evidence either control was
  enabled for the historical calls. [Gateway data-routing overview](https://vercel.com/i/secure-ai-gateway), [ZDR controls
  announcement](https://vercel.com/changelog/zero-data-retention-no-prompt-training-on-ai-gateway)
- **Provider selection and onward transfer:** Vercel's provider docs say the Gateway can dynamically choose providers based on
  uptime/latency unless caller settings pin/order/limit them. The 9/17 W&B run metadata records `backend=vercel` and a DeepSeek model
  identifier, but does not prove which underlying provider endpoint, Vercel system credentials vs BYOK, routing policy, or
  request-level privacy controls handled each generation. [Provider
  options](https://vercel.com/docs/ai-gateway/models-and-providers/provider-options)
- **Training/improvement and plan dependency:** Current AI Product Terms say Gateway enterprise customers receive a
  no-training/no-improvement commitment for AI Gateway Customer Content; the general Gateway clause otherwise makes third-party
  provider terms apply. Vercel's current general Terms say Hobby and trial-Pro content may be used for AI model training and shared
  with AI partners, while paid Pro has model training disabled by default with opt-in; the Terms also authorize use of submitted
  content to provide/improve Vercel services. Vercel's March 17 changelog states paid Pro and Enterprise are opted out of AI training
  by default, while Hobby/trial Pro may opt out in settings; its description distinguishes product improvement that does not involve
  model training. The applicable account plan and preferences on September 17 are unknown. [AI Product
  Terms](https://vercel.com/legal/ai-product-terms), [Vercel Terms](https://vercel.com/legal/terms), [March 2026 terms
  update](https://vercel.com/changelog/updates-to-terms-of-service-march-2026)

### DeepSeek Open Platform API

- **Current API terms and output rights:** The official [DeepSeek Open Platform
  Terms](https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html) state release date April 22, 2026 and
  effective date April 29, 2026. Sections 4.1–4.2 make the developer responsible for Inputs and rights/permissions; subject to law and
  the terms, the user retains rights (if any) in Inputs, DeepSeek assigns rights (if any) in Outputs, and the user may use
  Inputs/Outputs for training other models, including distillation. Section 5.1 reserves DeepSeek's own model IP. This is a clearer
  output-use grant than found in the general public Gateway wording, but it does not prove rights in the original source data or a
  particular output's freedom from third-party rights.
- **Sensitive data:** The current DeepSeek Privacy Policy says the Services “are not designed or intended to process sensitive Personal
  Data” and lists health data among examples, and says users should not provide it. The Open Platform Terms also put legal basis/notice
  duties on the developer for downstream personal-data processing. Confirm whether the policy's sensitive-data warning applies to the
  specific API product/account, and do not send clinical personal data pending written confirmation and appropriate contractual
  protections.
- **Training/improvement use:** The linked [DeepSeek Privacy
  Policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html?os=___) (last update February 10, 2026) says Personal
  Data may be used to develop/improve services and train/improve ML models, provides a right to opt out of use of Personal Data for
  model training/technology optimization, and describes use for service safety/security. The policy is phrased around Personal Data and
  consumer services; the Open Platform terms require processing consent/legal basis and point to the policy for personal information.
  Public sources do not establish whether a personal-data training opt-out or any organization-level control was set for the historical
  API calls. Do not extrapolate a consumer setting to an enterprise/API key without evidence.
- **Retention/deletion and location:** The current Privacy Policy gives no fixed universal retention period: it says retention varies
  and gives an account-based example including inputs, and states service data is directly collected, processed, and stored in the
  People's Republic of China. It provides personal-data rights, including deletion/opt-out, subject to law and policy exceptions. It
  does not provide a request-level API prompt deletion SLA in the passages reviewed. Applicability to this exact API traffic should be
  confirmed from the accepted API contract and product notices.
- **Transfers/subprocessors:** The current policy discloses service providers, corporate group processing that includes storage, R&D,
  foundation model training/optimization, and third-party APIs for search where input keywords may be shared. That establishes possible
  processing/transfers in the published policy, not proof those specific routes or search were used in the two calls. The W&B run
  metadata does not establish a direct Vercel-to-DeepSeek API handoff vs another serving arrangement.
- **Exact historical terms status:** The official API docs currently link the Open Platform Terms above. Their displayed effective date
  (2026-04-29) predates the September 17 run date, which is evidence that this published version was intended to apply by then.
  However, absent an archived September 17 snapshot, account acceptance record, or immutable version hash, we cannot prove it was the
  exact text then in force or accepted by the account. The same issue applies to Vercel's presently published terms and privacy/control
  configuration.

### Historical run conclusion and evidence needed

The probable documented model/backend pair is Vercel AI Gateway with a DeepSeek model, but the saved W&B metadata does not prove
request-level provider routing, the Vercel account tier, whether ZDR/no-prompt-training controls were enabled, the credential path
(Gateway credentials or BYOK), or the exact DeepSeek API policy path. Current public docs indicate that the Gateway may route across
providers; its ZDR and no-training controls are configuration-dependent. Vercel's AI Product Terms also restrict submitting sensitive
personal information, including health information. DeepSeek's current API terms assign rights (if any) in outputs to the user, while
the linked privacy policy permits personal-data model improvement subject to an opt-out right and says not to provide sensitive
personal data. There is no historical account evidence for the actual configuration or confirmation that the generation prompts
contained no restricted health information.

To close this historical provenance item, recover an immutable request trace or provider receipt for each run (selected
endpoint/provider, model version, credential mode, routing decision and privacy flags), preserve the Vercel and DeepSeek terms/policy
snapshots accepted on 2026-09-17, and establish the account plan/settings and any opt-out/contract addendum active at that time. Until
then, mark provider-policy provenance **plausible but unverified**; this does not clear the generated artifact's source rights or
clinical/privacy release gates.
