# W&B v4 training-loss and source-order audit — 2026-10-20

## Finding

The v4 W&B run remains active, but its training loss changed sharply at the
same point that the ordered training payload changes source families. The
provider event stream returned 1,427 gradient-step records from steps 30,383
through 31,809. Median loss stayed between 0.81 and 0.90 in 100-step bins
through step 31,499. It then rose to 1.339 in steps 31,500–31,599 (range
0.717–4.332), 2.982 in steps 31,600–31,699 (range 1.514–4.167), and 2.860 in
steps 31,700–31,799 (range 1.567–3.971). The next partial bin had median 3.170
across 10 events. The job remained `RUNNING` with no reported job error.

The exact 171,261-row train payload and its internal row-reference ledger are
written in candidate order by the release builder. The planned total of
85,631 steps is almost exactly two train rows per step. Around train position
63,000, the source ledger is:

| Train-row positions | Source label | Rows |
|---|---|---:|
| 62,901–63,094 | `mentalchat16k` | 194 |
| 63,095–63,101 | `mitags` | 7 |
| 63,102–75,658 | `mitch_hamidi_bpd_nlp` | 12,557 |

If the trainer consumes rows sequentially in batches of two, the transition
falls near step 31,551, inside the exact bin where loss jumps. The observed
steps-to-row ratio and timing make preserved input order a strong explanation;
the provider's public documentation does not say whether its SFT loader shuffles
the artifact, so this remains a correlation rather than confirmed trainer
behavior.

The target-format shift is large: v4 `mentalchat16k` rows (10,054 train rows)
average 2,047 assistant-target characters per example (median 2,148; p95
3,124), while v4 `mitch_hamidi_bpd_nlp` rows (12,557 train rows) average 288
(median 166; p95 969). User-message means are 577 and 83 characters,
respectively. These aggregate statistics contain no dialogue text.

## Interpretation and next step

This evidence does not show corrupted weights or prove a defective source.
It shows an abrupt distribution change aligned with a source boundary, and a
large change in target length/style. The source family still has unresolved
origin statuses (8,000 unique matches, 313 ambiguous, 5,577 unmatched in the
existing audit); the loss alignment does not clear those lineage or use
questions. Keep the authorized v4 run as the ordered-data comparison and
continue checkpoint backups. For a follow-up full-corpus run, preserve the
same rows and split but deterministically shuffle the train order, retain an
aligned hash-only row-reference sidecar, and compare loss curves and the same
heldout suite. Do not call v4 invalid from this loss change alone.

The source-order audit used the exact local train payload at
`ai/data/curated/recovery/gold-20261017/wandb-full-corpus-current-master-20261019-v4/train.jsonl`
and aligned its rows to `manifest_internal.jsonl` without printing message
content. The run is W&B job `24cc2d06-3ec3-4356-ad3a-179694dd86a7`.
