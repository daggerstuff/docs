# Fireworks Muse Glimmer renderer preflight — 2026-10-20

## Decision

The local synthetic agent-tool package fits Muse Glimmer's renderer and the
requested 32,768-token limit. It is ready for a bounded SFT experiment after
the currently running Fireworks training session releases the account's
training slot. This preflight made no provider API call, uploaded no data, and
started no job.

## Dataset integrity

The frozen package is `pixelated-agent-tool-sft-20261019-v1`, generated from
first-party deterministic synthetic data. It has 960 train, 120 validation,
and 120 test rows across eight scenario families. It contains 1,500 assistant
tool-call messages total (1,200 train, 150 validation, 150 test). The manifest
declares zero external content and zero real-person data; no clinical or
production readiness is claimed.

| Split | Rows | Trajectories SHA-256 | Tool-call messages |
| --- | ---: | --- | ---: |
| Train | 960 | `010322208f7938085de42fdd8d2c9e529c94ac1024fd02847c6d31d4edb15d78` | 1,200 |
| Validation | 120 | `3046e03c3281326dae6d9ef28f500e67090ce8b223ecc446a68a516b07dd4b99` | 150 |
| Test | 120 | `b139e49e69c7dda3efdde55b5e3a8dfe7a27665b627cefca4d727ee4e4927d34` | 150 |

Automated structural validation found no duplicate, missing, unmatched, or
duplicate-response call IDs; all calls have exactly one tool response. There
were no non-assistant final messages, malformed/non-object JSON arguments, or
unknown tool names. The 1,200 train groups have zero cross-split collisions.
The release-manifest SHA-256 is
`ad056f472ba03d12199af387fe1167de76ad71495591397c81c625dd4a7dfd82`.

## Model-specific render check

The Fireworks Muse Glimmer starter was adapted in a private temporary copy to
preserve `_muse_glimmer_tools` metadata and structured tool arguments, use
`build_supervised_examples(..., ALL_ASSISTANT_MESSAGES)`, and flatten the
resulting per-assistant-message datums at launch. The exact reviewed diff is
[`fireworks-muse-glimmer-renderer.patch`](fireworks-muse-glimmer-renderer.patch)
(SHA-256 `adb64925c0fbb931ffd6e59c7f23db465c73f711c828005f09d1da152f261dac`).

The offline preflight used the Muse Glimmer tokenizer/renderer, 32,768 maximum
sequence length, learning rate `1e-5`, batch size 16, and LoRA rank 8. Results:

- 960 train rows and 120 holdout rows rendered.
- 960 supervised examples and 95,185 weighted target tokens.
- Maximum rendered training sequence: 913 tokens; maximum evaluation prompt:
  858 tokens.
- Zero oversized sequences, zero oversized evaluation prompts, and zero rows
  without trainable targets.
- A separate decoded loss-mask audit found all 1,200 expected `<atem:invoke>`
  markers inside weighted targets, confirming the tool calls themselves are
  trained rather than only the surrounding text.

The prior starter's `LAST_ASSISTANT_TURN` path omitted the tool definitions
and left earlier assistant tool calls outside the loss. Use the included
patch for the next Muse Glimmer job. The preflight emitted nonfatal
transformers model-type and environment warnings; rendering and mask checks
completed successfully.

The shared synthetic mock-tool evaluator can now use in-session Fireworks
samplers through
[`fireworks_session_eval.py`](../../../ai/training/fireworks_session_eval.py).
It preserves Muse tool metadata and tool-call history, routes base/SFT arms to
separate session samplers, and records local prompt/completion token counts.
Its two offline transport contract tests pass; those tests make no model call.
The bridge must be invoked from the training process that owns the samplers,
after both base and tuned samplers are available.

## Launch gate

The active full-corpus Fireworks job occupies the training slot and does not
publish a tuned checkpoint until completion. Do not upload this candidate or
start the second job until that session ends. Once available, run the bounded
agent-tool SFT, then evaluate it against the same 120-case held-out suite and
base model using the mock-tool loop; the cookbook's built-in final-text check
does not measure tool execution. Keep the test split sealed until that
evaluation. Fireworks results remain experiment-only until the adapter is
exported and verified locally.
