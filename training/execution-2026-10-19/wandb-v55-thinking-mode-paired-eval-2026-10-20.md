# W&B v55 response-channel and paired thinking-mode evaluation — 2026-10-20

## Finding

Qwen3.6 defaults to thinking mode. A direct W&B inference probe to v55 in the
default mode returned `content: null` with a separate reasoning field, which
explains the empty visible outputs in the earlier v54/v55 sentinels. Qwen's
official model card documents `chat_template_kwargs: {"enable_thinking":
false}` as the switch for Qwen3.6. A bounded W&B probe confirmed that both the
base and v55 endpoints accept this setting and return nonempty `content`;
reasoning text was not recorded. See the [official Qwen3.6 model card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B).

With thinking disabled identically on both arms, the five-case synthetic
comparison produced visible content on all five base and all five v55 cases
after a separate successful retry for the base research case. The base made
four evaluator-local tool rounds and passed 3/7 unvalidated deterministic
checks. V55 made zero tool rounds, passed 2/7 checks, and reached the
1,024-token limit in two cases. V55 therefore has a response-channel mode that
returns visible text, but this experiment still shows no learned tool-use
behavior and no check improvement over the base. It is not promotable for the
agent-tool task. The synthetic cases are not validated quality, clinical, or
safety measures.

The first paired attempt and a second run before fixing the evaluator's
null-content preflight bug are retained. The final paired run's research case
initially exceeded the 2,048-token local input cap after two tool rounds. A
single base-only retry with a 4,096-token cap completed the same frozen case,
making two tool rounds and passing 0/1 citation checks. The retry is used only
to complete base coverage; its output is retained separately. The evaluator
counter now accounts for the complete serialized message, including null
assistant content and tool-call metadata. A regression test covers that path.

## Usage estimate

The two retained pre-fix/partial attempts and final paired run plus the base
retry estimated `$0.00727875` in total. The separate response-channel probes
estimated about `$0.00033`. Actual billing is unavailable. The final paired
run's `$0.05376` worst-case preflight and the retry's `$0.006912` preflight
were individually within their configured `$0.06` hard cap.

## Reproduction and integrity

Final paired run:

- Run ID: `wandb-v4-v55-five-scenario-dev-paired-nonthinking-v2-20261020T0854Z`
- Full case SHA-256: `9f0734cfde7384faa40e0f45163b12de906c69e6f0b22aa61f82dd5e8c0c10a3`
- Manifest config digest: `c1bab2f6d25c4c17bdb6bd894f5d250a32e8a1d9d91d4f364e7d79c6b3723ec8`
- Manifest file SHA-256: `7a644942650771248850e15a3a35741bf8059b00d82b4bd8cca77474bf1e856a`
- Results file SHA-256: `6176eea3b2ccefd0a015d7e8ae8bd0a6f12111ce1890b79da470034298724766`
- Private results: `ai/training/output/wandb_live_checkpoint_eval_20261020/v55-five-scenario-dev-paired-nonthinking-v2/` (directory mode 0700; files mode 0600).

Base research retry:

- Run ID: `wandb-v4-v55-nonthinking-base-research-retry-20261020T0857Z`
- Single-case SHA-256: `c00c3dc10572b54958def9bd40082eebbf4f8bc1070271c3541574b337e367b6`
- Manifest config digest: `11d2250bbae01ff5d3bcbaa2aee94f5733d92f264cab7ac3e43ff700dd24ee70`
- Manifest file SHA-256: `a976c7803604d4883d70c6886b23364206b86890277756c0132cbe282fb9b40a`
- Results file SHA-256: `e3b3d9da1d97489757a1d48640b545b3e5782487ca5096a99c2c0fa4ac280bd8`
- Private retry output: `ai/training/output/wandb_live_checkpoint_eval_20261020/v55-research-base-context-retry/` (directory and files mode 0700/0600).

## Evaluator changes

The paired evaluator accepts an optional boolean `decoding.chat_template_kwargs.enable_thinking`, and the W&B transport forwards it to the chat-completions API. Defaults are unchanged when the option is omitted. `ConservativeAsciiByteCounter` now measures full serialized messages, so tool-call assistant messages with null content no longer raise `AttributeError` during the next-turn preflight. Verification: `ruff check` passed and `ai/qa/validation/tests/test_paired_eval.py` passed 24 tests.
