# Tool-argument literal extraction (v13)

Date: 2026-11-05
Suite: `literal_capability_v1` (`ai/qa/validation/therapy_bench/generate_literal_capability_v1.py`)
Arms: `base` = `Qwen/Qwen3.6-35B-A3B`, `sft` = `arc-sft-baseline-ecf35d5e5384:v1` (v13)

Synthetic, non-clinical diagnostics. No quality or safety claim is made from these numbers.

## Why this run exists

The held-out contract suite surfaced a failure that the dev suite cannot see. In
`dev-tool-approval-granted`, v13 called `submit_mock_change` correctly and was denied only because the
argument was `{"change": "workspace announcement to \"Meeting moved\""}` — the user's phrasing, with
the field label welded to the front, instead of the literal value the user quoted.

The dev suite never caught this because `dev-tool-approval` asserts `tool_status=approval_required`
and `state_value changes=[]`. It never inspects the argument. A model can therefore pass the tool
case by calling the right tool with a wrong argument, indefinitely.

This suite asserts the argument itself, across value shapes.

## Method

Six cases, each with a context sentence naming a field and a user message carrying the value:

| case | value shape | required argument |
| --- | --- | --- |
| `literal-quoted` | quoted string | `Meeting moved` |
| `literal-unquoted` | bare clause | `Room booking closed for maintenance` |
| `literal-reference-code` | identifier | `REC-8842` |
| `literal-superstring` | value that contains the field's own word | `Meeting moved to Thursday` |
| `literal-comma` | value with internal punctuation | `Building A, second floor` |
| `memory-cadence` | cadence phrase into a memory key | key `cadence`, value `every second Tuesday` |

Checks are exact: `tool_arguments` requires the argument dict to equal the expected dict, so extra
wrapping fails. Temperature 0, thinking disabled, `max_tokens` 2048, `max_tool_rounds` 4.

## Results

Dev and sealed splits are identical.

| arm | passed | failing cases |
| --- | --- | --- |
| base | 5 / 6 | `literal-unquoted` |
| sft | 2 / 6 | `literal-quoted`, `literal-unquoted`, `literal-superstring`, `literal-comma` |

Base's single miss is a sentence wrapper around the correct value:

```
"Set the fictional release note so it reads Room booking closed for maintenance."
```

Every v13 miss is the same shape: the field label is prepended to the value.

```
"workspace announcement to \"Meeting moved\""
"release note to Room booking closed for maintenance"
"announcement to \"Meeting moved to Thursday\""
"room label to Building A, second floor"
```

v13's two passes are the cases where the user names the value without a labelled object in the
message: the bare identifier (`REC-8842`) and the memory cadence, which goes through `memory_write`
rather than `submit_mock_change`.

## Reading

This is the clearest behavioural difference measured so far, and it runs against the trained arm.
Base extracts the value and sometimes wraps it in prose; v13 reconstructs the sentence and treats the
field label as part of the payload. The trained model has learned the *turn shape* — acknowledge,
call the tool, confirm — more tightly than it learned what belongs in the argument.

The plausible cause is the training distribution. The corpus is therapy dialogue, where the assistant
turn is `ledger JSON \n spoken reply` and nothing in it exercises extracting a literal from a request
into a tool argument. The agent-tool rows that taught tool calling taught the call structure and the
reply shape; the argument-value step had no pressure on it, and the nearest learned pattern (restate
the user's sentence) won.

Two consequences worth stating plainly:

- Any future eval that grades tool calling by tool name or status alone will report v13 as healthy
  while it writes malformed arguments. `tool_arguments` needs to be in the check set wherever an
  argument value is semantically meaningful.
- The defect is a data-coverage gap, not a capacity gap: base solves 5 of 6 with the same
  tokenizer, the same prompt, and no tool training at all.

## Caveats

- Six cases, one sample each, temperature 0. Small enough that a single case is 17 points.
- Only `submit_mock_change` and `memory_write` are exercised; other tools' arguments are untested.
- The expected arguments are single-field dicts. Multi-field arguments, optional fields, and nested
  structures are not covered.
- The suite measures extraction fidelity, not whether the extracted value is the right thing to send.

## Reproduce

```bash
cd /home/vivi/pixelated
ai/.venv/bin/python ai/qa/validation/therapy_bench/generate_literal_capability_v1.py
ai/.venv/bin/python ai/training/run_wandb_paired_eval.py \
  --cases docs/training/execution-2026-10-17/scenario-literal-dev-v1.jsonl \
  --config docs/training/execution-2026-10-17/wandb-literal-v13-heldout.config.json \
  --arm both --results-dir ai/training/output/wandb_live_checkpoint_eval_20261105/literal-dev-v13
```

Results: `ai/training/output/wandb_live_checkpoint_eval_20261105/literal-{dev,sealed}-v13/results.jsonl`.
Per-case pass/fail is in each record's `state_metrics`; the argument actually sent is in `tool_trace`.
