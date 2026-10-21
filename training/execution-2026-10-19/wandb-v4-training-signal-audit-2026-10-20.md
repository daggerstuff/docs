# W&B v4 training-signal audit — 2026-10-20

A local aggregate-only scan of the exact frozen W&B training payload
`ai/data/curated/recovery/gold-20261017/wandb-full-corpus-current-master-20261019-v4/train.jsonl`
found 171,261 rows, each containing a `messages` list, and 1,056,820 messages
in total: 522,658 user messages and 534,162 assistant messages. There were no
`tool` role messages, no assistant `tool_calls`, and no row with either form of
tool supervision. No prompt, completion, or clinical text was printed or copied
into this report.

This is directly relevant to the v33 paired result: across two repetitions of
the frozen five-case synthetic capability suite, v33 produced nonempty text in
4/5 cases but made zero evaluator-local tool rounds, while the base made four.
Because the SFT payload contains no tool-use targets, the zero-call result is an
input/task mismatch warning, not evidence that the running optimizer is broken.
The synthetic suite is not clinical-quality or safety evidence. The result does
show that this SFT job alone is not training the requested agent tool behavior.

Do not add synthetic tool traces to, or rewrite, the frozen source release. A
separate task-specific SFT experiment should be prepared as a new immutable
training artifact containing realistic, policy-checked tool-use trajectories
for the intended agent workflows, including tool request, tool result, final
answer, refusal/approval boundaries, and multi-step cases. Compare the unchanged
base, current dialogue SFT, and task-specific SFT on the same larger prompt- and
group-disjoint suite; include failure and abstention checks, not just exact
output strings. Keep that separate experiment gated on confirmed W&B training
entitlement/storage and an explicit spend cap, since current public-preview
documentation does not expose account-specific billing and the live run has not
finished. This is a concrete follow-on experiment design, not a claim that the
current model is tool-qualified.
