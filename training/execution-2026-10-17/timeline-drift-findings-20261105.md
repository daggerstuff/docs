# Timeline anchor drift on long prefixes (v13)

Date: 2026-11-05
Probe: `ai/training/probe_timeline_drift.py`
Arms: `base` = `Qwen/Qwen3.6-35B-A3B`, `sft` = `arc-sft-baseline-ecf35d5e5384:v1` (v13)

Synthetic, non-clinical diagnostics. No quality or safety claim is made from these numbers.

## Why this run exists

The arc-corpus writer gate recorded `tl_drift` as its second most common rejection (200 of 1,195
failed attempts). `tl_drift` means an accepted ledger dropped a time anchor that an earlier ledger
had already established — the append-only invariant on the `tl` field of the nine-field ledger. If
that failure mode survived into the trained adapter, it would be a long-context coherence defect:
the therapist quietly rewrites when things happened as the conversation grows.

The probe measures exactly that, in isolation from the writer's other obligations.

## Method

- Corpus: `ai/training/output/arc_corpus/arc_records.jsonl` (1,085 accepted sessions, 430 arcs).
- Prefixes: the deepest prefix in each context band per session, ledgers serialised exactly as
  training serialises them (`<ledger JSON>\n<spoken reply>`), so the model sees its training
  distribution.
- Exclusion: the 94 arcs present in the v13 validation, test, or heldout splits, so every prefix is
  on an arc the adapter never trained on.
- Selection: up to 12 prefixes per bucket, preferring distinct arcs. 48 prefixes across 48 distinct
  arcs; `short` 8 messages, `medium` 14–18, `long` 20–30, `very_long` 32–42.
- Sampling: 2 samples per prefix, temperature 0.7, thinking disabled, `max_tokens` 1400.
- Scoring: parse the leading ledger object from the reply, extract `tl` anchors, compare with the
  anchors inherited from the prefix ledgers. A dropped inherited anchor is drift; an emitted anchor
  that no earlier ledger had is counted separately as invented.

Reference check: the accepted next turn in the corpus drifts on 0 of the 48 selected prefixes, so
the invariant does hold in the data being used.

## Results

| arm | bucket | samples | parsed | drifted | rate | collapsed | recall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| base | short | 24 | 24 | 0 | 0.0% | 0 | 1.000 |
| base | medium | 24 | 24 | 0 | 0.0% | 0 | 1.000 |
| base | long | 24 | 24 | 1 | 4.2% | 1 | 0.958 |
| base | very_long | 24 | 24 | 0 | 0.0% | 0 | 1.000 |
| sft | short | 24 | 24 | 0 | 0.0% | 0 | 1.000 |
| sft | medium | 24 | 24 | 0 | 0.0% | 0 | 1.000 |
| sft | long | 24 | 24 | 0 | 0.0% | 0 | 1.000 |
| sft | very_long | 24 | 24 | 0 | 0.0% | 0 | 1.000 |

Overall: base 1 of 96 samples drifted (1.0%, 3 anchors lost), sft 0 of 96 (0.0%).

The single miss is not incremental drift. It is a total collapse: `arc_0217` session 1, `long`
bucket, inherited `-3w`, `-4y`, `now`, emitted an empty `tl`. One sample out of two at that prefix;
the other sample preserved the anchors.

Invented anchors: 0 in both arms, across all 192 samples. Neither arm ever adds a `tl` anchor that
the prefix did not already establish.

## Reading

Timeline-anchor preservation is not a v13 defect. Both arms keep the append-only invariant, and the
rate does not grow with prefix length — the deepest band (32–42 messages) is as clean as the
shallowest (8 messages). Ledger emission itself is intact: 192 of 192 replies contained a parseable
leading ledger object.

That does not contradict the writer gate's `tl_drift` count, because the two tasks differ. The
writer generated whole sessions from a plan: it had to invent the timeline forward across 8–40
turns, and its failures were anchor sets that shrank as it went. The probe hands the model a
timeline that already exists and asks for the next turn, which is the easier problem — and both
models solve it.

The interesting residual is the opposite of drift: neither arm advances the timeline. Both copy the
inherited anchor set verbatim, which is consistent with the corpus (0 drift across 17,853 accepted
therapist turns) but also means a `tl` field is being treated as a value to echo rather than a
structure to extend. Whether the model can introduce a *new* anchor when a session legitimately
moves forward in time is untested here, because the probe only scores preservation.

## Caveats

- Single run, 2 samples per prefix at temperature 0.7, 48 prefixes. A 0.0% rate is an upper bound
  of roughly one drift per 96 samples, not proof of perfection.
- Held-out arcs only, so the numbers describe generalisation, not the arcs in training.
- Only the `tl` field is scored. The other eight ledger fields are parsed but not checked.
- The prefix is truncated at a client turn, so the probe never asks the model to close a session.

## Reproduce

```bash
cd /home/vivi/pixelated
PYTHONPATH=/home/vivi/pixelated ai/.venv/bin/python ai/training/probe_timeline_drift.py --dry-run
PYTHONPATH=/home/vivi/pixelated ai/.venv/bin/python ai/training/probe_timeline_drift.py \
  --arm both --per-bucket 12 --out-dir ai/training/output/timeline_drift_probe
```

Output: `ai/training/output/timeline_drift_probe/20261105T090941Z/` (`probe.json`, `samples.jsonl`).

Note: run with `PYTHONPATH=/home/vivi/pixelated` (repo root). With `PYTHONPATH` pointing at `ai/`,
the first `ai.training.*` import caches a foreign `ai` package and the fallback path cannot recover.
