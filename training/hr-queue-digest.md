# HR queue digest — all 56 arcs, grouped for disposition

Generated 2026-10-15 from `ai/training/output/arc_corpus/human_review_queue.jsonl` (87 rows).
Queue policy: an arc lands here when the auditor's verdict is an outright `fail`, or when
it returns a second consecutive `revise`. Every one of these 56 arrived via the
second-revise rule — **the auditor never issued an outright fail on any arc in the queue.**
Full flag notes (with quoted turns) live in the queue file; each row below carries the
primary issue only. Requeue = the audit notes are already on disk and `generate_arc_corpus`
consumes them, so one more revise round is always available at writer cost only.

**Corpus stakes:** 56 arcs ≈ 136 flagged sessions; the accepted corpus is ~999 gold sessions,
so accepting everything would grow it ~13-15%. That growth is the natural trigger for the
deferred run-3 retrain (pilot log §13.18).

**Cross-cutting finding (worth knowing before per-arc reads):** the dominant safety-flag
signature is *beat-timing drift* — the plan schedules the safety disclosure at turn N, the
client delivers it at turn N−1, and the therapist's required direct assessment at N therefore
misses it. It recurs verbatim across arc_0231/0287/0302/0328/0358/0262/0128 and several
Group B rows. It is a single mechanical failure mode, not 20 independent content problems —
one corrective-note requeue round targeting beat timing is likely to clear much of Groups A
and B at once.

---

## Group A — safety-heavy: 4 arcs (≥3 safety_failure flags)

The therapist's required safety responses failed repeatedly across sessions — in a
therapy-training corpus these are the highest-stakes defects. All four are `nightmare fuel`
severe-family arcs with the same signature: the safety disclosure lands one turn early and the
required direct assessment misses it. Recommend full reads of the flagged turns before any
accept. Suggested disposition: **requeue one focused round** (the shared beat-timing failure is
the kind the corrective notes fix), reject if it recurs.

| Arc | Family | Audit rounds | Sessions | Flags | Primary issue |
|---|---|---|---|---|---|
| arc_0302 | nightmare fuel | 2 | s1+s2 | safety_failure×8, ledger_contradiction×1 | Plan schedules the safety disclosure at session 1 turn 7; it arrives at turn 6. The therapist's assessment at … |
| arc_0358 | nightmare fuel | 2 | s1+s2+s3 | safety_failure×7, fabrication×1 | Plan schedules the passive-SI disclosure at session 1 turn 7 with required direct assessment at that turn; the… |
| arc_0328 | nightmare fuel | 2 | s1+s2+s3 | safety_failure×6 | The plan schedules the safety disclosure at session 1 turn 7 and requires a direct means/plan/intent/timeline … |
| arc_0231 | nightmare fuel | 2 | s1+s2+s3 | safety_failure×5 | The plan schedules the passive-death-wish signal at session 1 turn 9, but the transcript places the client's l… |

## Group B — other stance-flagged: 24 arcs (1-2 stance flags, often mixed with ledger issues)

Single or paired therapist-behavior flags (a missed safety beat, a withheld truth, one
capitulation) alongside otherwise-passing material. The four bonus/retry arcs from §13.17
(arc_0261, arc_0425, arc_0426, arc_0429) land here. Recommended: read the 1-2 flagged turns
per arc, then decide — most will likely resolve to accept-with-caveat or one more revise round.

| Arc | Family | Audit rounds | Sessions | Flags | Primary issue |
|---|---|---|---|---|---|
| arc_0287 | coercion or abuse | 3 | s1+s2+s3 | ledger_contradiction×6, safety_failure×2, fabrication×2, tl_drift×1, thread_death×1, comfort_lie×1, false_certainty×1, capitulation×1 | The safety beat is scheduled at session 1 turn 7 but the disclosure actually arrives at turn 6. The therapist'… |
| arc_0429 | delusion or paranoia | 2 | s1+s2+s3 | thread_death×3, truth_withholding×2, capitulation×2, tl_drift×1, false_certainty×1 | The plan requires: 'refuse the verdict plainly; say the transfer is not what this hour is about and will not b… |
| arc_0425 | ambiguous crisis language | 2 | s1+s2+s3 | comfort_lie×2, ledger_contradiction×2, safety_failure×1, truth_withholding×1 | The plan requires direct assessment in Priya's own words: what she means by not coming out, whether she has th… |
| arc_0261 | minor or dependent person | 2 | s1+s2+s3 | safety_failure×1, thread_death×1, truth_withholding×1, capitulation×1, tl_drift×1 | Required: direct assessment in Marisol's own words — how often, how long she's gone, whether her mother has mi… |
| arc_0262 | multi-problem complexity | 2 | s1+s2+s3 | safety_failure×1, fabrication×1, ledger_contradiction×1, false_certainty×1, thread_death×1, tl_drift×1, comfort_lie×1 | The safety beat is scheduled at turn 5 and the client signal arrives at turn 4. T4 asks only about the bottle … |
| arc_0327 | nightmare fuel | 3 | s1+s2+s3 | fabrication×3, ledger_contradiction×2, safety_failure×1, thread_death×1, tl_drift×1, truth_withholding×1, capitulation×1 | Required: direct means/plan/intent assessment in Priya's own words — ask about the car, the curve, whether she… |
| arc_0367 | nightmare fuel | 3 | s1+s2 | ledger_contradiction×5, thread_death×2, fabrication×1, tl_drift×1, truth_withholding×1, capitulation×1, integrity_violation×1 | The therapist grants the true verdict plainly at T 8 — this is correct. (No flag for the grant itself; the gra… |
| arc_0128 | nightmare fuel | 5 | s1+s2+s3 | fabrication×2, safety_failure×1, truth_withholding×1 | The plan schedules the safety beat at session 1 turn 14, but the client delivers the overpass statement at tur… |
| arc_0352 | nightmare fuel | 3 | s1+s2+s3 | ledger_contradiction×2, tl_drift×2, safety_failure×1, capitulation×1, fabrication×1 | The safety assessment covers method/plan and medication access but never directly assesses INTENT — the plan e… |
| arc_0353 | nightmare fuel | 3 | s1+s2 | ledger_contradiction×6, safety_failure×2, fabrication×2 | The plan requires asking specifically about the leftover benzos and whether he has considered taking them all … |
| arc_0396 | ambiguous crisis language | 3 | s1+s2+s3 | ledger_contradiction×2, safety_failure×2, tl_drift×1 | The plan's safety beat is scheduled at session 1 turn 9 with this exact client line, requiring direct assessme… |
| arc_0264 | substance use | 2 | s1+s2+s3 | ledger_contradiction×4, safety_failure×1, tl_drift×1, fabrication×1 | The safety beat is partially performed (quantity/frequency asked, driven-since-Tuesday asked at T8), but the r… |
| arc_0305 | boundary testing | 2 | s1+s2 | fabrication×2, capitulation×1, ledger_contradiction×1, tl_drift×1 | In session 1 the therapist held that he could NOT certify the stress as work-related ('I can't write that your… |
| arc_0312 | therapeutic rupture | 3 | s1+s2+s3 | ledger_contradiction×8, fabrication×3, safety_failure×1, tl_drift×1 | Plan schedules the safety beat at session 1 turn 3 with the client line 'my car won't be around tomorrow' deli… |
| arc_0326 | nightmare fuel | 3 | s1+s2+s3 | ledger_contradiction×3, tl_drift×2, thread_death×2, fabrication×1, safety_failure×1 | The required safety beat calls for direct assessment of intent, plan, AND whether she has thought about not wa… |
| arc_0335 | nightmare fuel | 3 | s1+s2 | ledger_contradiction×3, fabrication×3, tl_drift×1, safety_failure×1 | The plan's ending beat (session 2 turn 16: Marisol commits to bringing her attorney a written list) is never r… |
| arc_0348 | nightmare fuel | 3 | s1+s2 | ledger_contradiction×5, thread_death×1, fabrication×1, safety_failure×1 | The required safety assessment is incomplete: the therapist asks what anger looks like and about hitting/grabb… |
| arc_0357 | nightmare fuel | 3 | s1+s2 | ledger_contradiction×4, fabrication×2, safety_failure×1 | Plan schedules the SI disclosure at session 1 turn 8 with immediate direct means/plan/intent assessment. The d… |
| arc_0361 | nightmare fuel | 3 | s1+s2+s3 | ledger_contradiction×8, fabrication×3, capitulation×1, tl_drift×1 | The plan's ending requires exactly two concrete commitments (garage, one true sentence about the hallway) with… |
| arc_0368 | nightmare fuel | 3 | s1+s2 | thread_death×2, ledger_contradiction×2, safety_failure×1, tl_drift×1 | The plan schedules the direct means/plan/intent assessment at turn 7 in response to this disclosure, but the d… |
| arc_0380 | nightmare fuel | 3 | s1+s2+s3 | ledger_contradiction×6, fabrication×3, tl_drift×1, safety_failure×1 | The safety beat is scheduled at turn 7 and the client's disclosure lands at turn 6; the therapist response at … |
| arc_0387 | coercion or abuse | 3 | s1+s2 | fabrication×5, ledger_contradiction×1, safety_failure×1, tl_drift×1 | The plan requires asking whether Mateo has ever put hands on her or blocked the door as part of the direct ass… |
| arc_0392 | multi-problem complexity | 3 | s1+s2 | fabrication×5, ledger_contradiction×2, false_certainty×1, tl_drift×1 | The demand 'Will I lose the apartment or not? Yes or no' is answered with a flat 'No' — invented certainty abo… |
| arc_0398 | coercion or abuse | 3 | s1+s2 | fabrication×2, thread_death×1, tl_drift×1, ledger_contradiction×1, safety_failure×1 | The safety signal is scheduled at session 1 turn 7 but arrives at turn 5; the required direct assessment (what… |

## Group C — ledger-only: 28 arcs (no stance flags)

The auditor found no therapist-behavior defects; every flag is internal-ledger bookkeeping
(contradictions, fabricated entries, dropped timeline anchors). The ledger is deliberately kept
in gold as training signal, so fabricated ledgers teach fabrication — but the spoken therapy
content itself passed. Options: (a) batch-requeue for one more regeneration round, (b) accept
as-is if spot-checks read minor, (c) reject. Recommend a 3-arc pilot requeue before deciding
the batch.

| Arc | Family | Audit rounds | Sessions | Flags | Primary issue |
|---|---|---|---|---|---|
| arc_0313 | cultural or identity conflict | 2 | s3 | fabrication×33 | Session 3 turn 1 ledger asserts 'fiance named Daniel' and 'mother routes contact through clinic front desk' — … |
| arc_0362 | nightmare fuel | 3 | s1+s2+s3 | ledger_contradiction×9, thread_death×9 | The disclosure_gate beat is scheduled at session 1 turn 9 with the abort line 'it's a process, it's not— anywa… |
| arc_0319 | nightmare fuel | 3 | s1+s2+s3 | tl_drift×13, fabrication×2, ledger_contradiction×1 | Client never mentioned adjuster or insurance calls before this turn; the therapist introduces them as establis… |
| arc_0342 | nightmare fuel | 3 | s1+s2+s3 | fabrication×8, tl_drift×6, ledger_contradiction×1 | The pressure_false_comfort beat is scheduled for session 1 turn 15, but the demand and the refusal occur at tu… |
| arc_0274 | substance use | 3 | s1+s2+s3 | fabrication×6, ledger_contradiction×5 | The kitchen-floor blackout is introduced by the therapist at T12 ('drinking till you're out is how people end … |
| arc_0251 | multi-problem complexity | 3 | s1+s2+s3 | ledger_contradiction×5, fabrication×4, tl_drift×1 | At session 1 turn 13 the client has not yet disclosed any missed bid — he has only said 'the thing at work was… |
| arc_0266 | boundary testing | 3 | s1+s2+s3 | fabrication×4, ledger_contradiction×4, thread_death×1, tl_drift×1 | At session 1 turn 13 the client has disclosed only 'a count that was off' — the dead dog is not revealed until… |
| arc_0238 | medical uncertainty | 3 | s1+s2 | ledger_contradiction×4, fabrication×3, tl_drift×2 | Ledger asserts the envelope is 'in a drawer' at session 1 turn 10, but the client has only said it is 'a thing… |
| arc_0359 | nightmare fuel | 3 | s1+s2+s3 | fabrication×4, ledger_contradiction×3, tl_drift×2 | The therapist states this as fact, but the client never said it in this transcript. The plan's safety beat has… |
| arc_0297 | cultural or identity conflict | 2 | s2+s3 | fabrication×4, tl_drift×3, ledger_contradiction×1 | Ledger invents a '-14m' onset for the relationship. The transcript consistently states the relationship has la… |
| arc_0248 | delusion or paranoia | 3 | s1+s2 | ledger_contradiction×6, thread_death×1 | The client never revised the shift claim — he preemptively scoped the gap to the log ('The log. Not the shifts… |
| arc_0278 | cultural or identity conflict | 3 | s1+s2 | thread_death×5, ledger_contradiction×2 | The revision tag is correctly applied at T 4, but the old anchor 'parents know about Marisol but don't talk ab… |
| arc_0369 | nightmare fuel | 2 | s1+s2+s3 | ledger_contradiction×5, fabrication×1 | Beat performed one turn early relative to the scheduled turn 15; the required handling (refuse false verdict, … |
| arc_0105 | multi-problem complexity | 3 | s1+s2+s3 | ledger_contradiction×4, tl_drift×1 | The arc plan establishes that the session-1 misstatement ('two hours') is to be held until session 2 turn 3, w… |
| arc_0386 | boundary testing | 2 | s3 | fabrication×3, tl_drift×1, ledger_contradiction×1 | Session-3 ledger asserts session-1 facts that never appear in the transcript: no 'last place ran out' line and… |
| arc_0391 | minor or dependent person | 2 | s1+s2 | ledger_contradiction×4, fabrication×1 | Beat performed early and correctly in substance — refusal is plain, the freeze is named, a next step is offere… |
| arc_0426 | boundary testing | 2 | s1+s2+s3 | ledger_contradiction×3, thread_death×1, tl_drift×1 | The ledger tags the client's statement at C17 as a 'revision,' but the arc plan specifies this revision belong… |
| arc_0052 | coercion or abuse | 3 | s1+s2+s3 | ledger_contradiction×3, tl_drift×1 | The arc plan specifies the doorway incident as 'last Thursday' at session 1 turn 7, but the ledger records it … |
| arc_0165 | nightmare fuel | 3 | s1+s2+s3 | tl_drift×2, thread_death×1, ledger_contradiction×1 | The session-1 turn-3 misstatement ('I haven't been within a block of his office') was already contradicted and… |
| arc_0294 | substance use | 2 | s3 | fabrication×4 | The session-3 ledger asserts 'rule: you don't get comfortable, it gets taken' as established history, but this… |
| arc_0338 | nightmare fuel | 3 | s2+s3 | tl_drift×3, fabrication×1 | The ledger carries the session-1 anchor 'last therapist stopped showing up, no termination session (told)' and… |
| arc_0343 | nightmare fuel | 2 | s1+s2 | fabrication×2, tl_drift×1, ledger_contradiction×1 | At turn 12 the missed pickups have not yet been disclosed — Marcus only admits 'I missed a couple pickups' at … |
| arc_0370 | nightmare fuel | 2 | s2+s3 | fabrication×3, tl_drift×1 | Session 2 opening tl silently replaces the session-1 ledger with a different set of anchors: 'Dana schedules c… |
| arc_0394 | substance use | 2 | s1+s3 | ledger_contradiction×3, fabrication×1 | The client never stated she drinks alone after close in session 1. She disclosed a notes-app tally of drinks a… |
| arc_0419 | minor or dependent person | 3 | s1+s3 | fabrication×4 | Client introduces 'the wrist' — no wrist detail (injury, grabbing, bruising) appears anywhere in the prior tra… |
| arc_0265 | therapeutic rupture | 2 | s1+s2 | ledger_contradiction×1, fabrication×1, tl_drift×1 | The plan's misstatement beat specifies the client claims the THERAPIST said 'you're only here to be seen' in s… |
| arc_0373 | nightmare fuel | 2 | s3 | tl_drift×1, fabrication×1, ledger_contradiction×1 | Session 3 opening ledger silently rewrites the timeline ledger: 'moved to nights' was '-8m' in s1/s2, now 'a f… |
| arc_0403 | boundary testing | 2 | s3 | fabrication×1, ledger_contradiction×1 | The therapist speaks the client's line. The client has not said this in session 3 turn 10; the client says it … |
