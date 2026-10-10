# Fireworks Export Plan — Arc-Corpus Pilot Payload

**Created:** 2026-10-10 — Phase 2 plan, drafted and executed locally the same day (roadmap row:
pre-plan §2 Phase 2; preparation plan:
[`.junie/plans/fireworks-training-preplan.md`](../../.junie/plans/fireworks-training-preplan.md))
**Status:** EXECUTED LOCALLY 2026-10-10 (§9) under the owner's instruction to begin the four
grant items: the two in-plan dispositions are adopted (§4.1, §5.4) and the local emission is
approved, run, and verified — 576 rows emitted; **nothing left this environment.** Upload,
provisioning, and spend remain separate, un-granted gates (readiness §4), and external transfer
still requires the Phase 1 determinations (readiness items 4–6, 13). This document is the
evidence of record: payload spec (§2), screening (§4), splits (§5), identity (§6), execution
(§9). Signable packages for the remaining human-authority items:
[`fireworks-approval-packages.md`](./fireworks-approval-packages.md).
**Companion:** [`fireworks-readiness.md`](./fireworks-readiness.md) — status register, decision
record D1–D4, provider facts (§2) · [`fireworks-pilot-preplan.md`](./fireworks-pilot-preplan.md) —
conditional roadmap.
**Screening basis:** read-only local passes over the quiescent corpus, 2026-10-10. Every number
below was computed in this environment; nothing left it.

---

## 1. Purpose and scope

Phase 2's exit evidence per the pre-plan is "a reviewable export plan with snapshot identity and
screening results; nothing exported yet." This document freezes, for owner review:

- the **payload specification** (§2) — exactly what would be emitted, and what would never be;
- the **validated inventory and screening results** (§3–§4), including two recorded deviations;
- the **leakage-safe split proposal** (§5) implementing decision D4;
- the **snapshot identity method and values** (§6);
- the **privacy profile** (§7) and the **gated execution checklist** (§8).

Decisions D1 (therapist-response SFT), D2 (inline ledger), D3 (model shortlist, GLM 5.3 Flash
recommended), and D4 (seed-level grouping) are inputs from readiness §2, not re-litigated here.
The corpus itself is not frozen — any future gold change invalidates §6 and requires re-screening
(readiness header; that is what the identity check exists to catch).

## 2. Payload specification

### 2.1 Source and extraction (frozen rule)

- Source of record: `ai/data/curated/sft_chatml/train_master_gold.jsonl`
  (189,735 lines; identity §6).
- The export slice = every row whose `provenance.arc_id` is present: the **576 accepted-arc
  sessions** (all `verdict: accept`, `tier: T1_GOLD`, `family: arc_corpus`). One payload row per
  session. Gold file order is the canonical row order.
- Nothing else contributes. DPO pairs stay out (pre-plan §1: deferred pending their own
  validation).
- The rule depends only on each row's own fields, so it is deterministic and re-runnable; the
  §6 identity check guards against drift between this plan and execution time.

### 2.2 Provider row schema (the only data that would leave this environment)

OpenAI-compatible chat JSONL (readiness §2; provider fine-tuning guide, verified 2026-10-10):

```json
{"messages": [
  {"role": "user",      "content": "<client turn>", "weight": 0},
  {"role": "assistant", "content": "<9-field JSON ledger>\n<spoken reply>", "weight": 1}
]}
```

- Role mapping (D1): client → `user`, therapist → `assistant` — already the gold shape; no
  re-mapping occurs.
- Loss masking (D1 made concrete): `weight: 0` on every client turn, `weight: 1` on every
  therapist turn — the model trains only on therapist responses, with client turns as context.
  (The provider's own debugging guidance: assistant turns non-zero, system/user masked.)
- Ledger contract (D2): the 9-field ledger stays inline as the leading JSON line of each
  assistant turn — the corpus's native shape, byte-for-byte. No re-rendering. The
  `reasoning_content` variant remains the follow-up A/B, not this payload.
- No `system` messages exist in the slice (verified, §4.5) and none are added.
- Every other gold field is **stripped**: no provenance, no writer/auditor model ids, no
  timestamps, no internal paths, no tags in the provider payload.

### 2.3 Internal manifest (stays in this environment)

Per pre-plan §2, provider payload and private provenance are separated. Emission records one
manifest line per session, kept locally:

```json
{"gold_line_no": 0, "arc_id": "…", "session_n": 1, "split": "train",
 "source_family": "…", "source_id": "…", "line_sha256": "…",
 "difficulty": "…", "domain": "…", "writer_model": "…", "auditor_model": "…",
 "verdict": "accept", "consolidated_at": "…"}
```

The manifest is the audit trail connecting every uploaded row to its accepted-session lineage.

### 2.4 File set and sizes

| Artifact | Contents | Rows | Tokens (chars ÷ 4) |
|---|---|---|---|
| `train.jsonl` | provider rows, split per §5.3 | 418 | 3,106,534 |
| `val.jsonl` | provider rows | 80 | 609,606 |
| `test.jsonl` | provider rows | 78 | 609,215 |
| `manifest_internal.jsonl` | §2.3 records | 576 | — |

- Payload total: 4,325,355 tokens ≈ 17.3 MB of content — far under the provider's <500 MB
  UI-recommended size; `firectl` handles any size.
- Provider dataset limits (verified 2026-10-10): JSONL, minimum 3 / maximum 3M examples per
  dataset — 576 rows is fine.
- Per-example training context: the provider cuts training examples at **32,768 tokens by
  default**; `--max-context-length` raises it (their example: 65,536). The largest row here is
  ≈23.2k tokens by chars/4 (§4.2) — inside the default cutoff, but the plan still requires an
  explicit `--max-context-length` at job creation and a Render Samples truncation check before
  any paid run (Phase 3).

### 2.5 Phase 3 usage notes (recorded here only because they constrain the payload)

- `val.jsonl` is the candidate explicit `evaluation_dataset` (replacing the provider's automatic
  carve-out of training data). `test.jsonl` is **not** uploaded for training; it stays internal
  as the held-out set for Phase 4 evaluation.
- Phase 4 evaluation sends held-out prompts to the deployed endpoint — that traffic also leaves
  this environment and sits under the same privacy-approval boundary as the training upload.
  Flagged for the owner; not decided here.
- ≈91% of message content is assistant-side, so weight masking changes what is learned more than
  how much is processed; Render Samples verifies the masks before any spend.

## 3. Validated inventory (2026-10-10, read-only)

- **576 payload rows = the 576 checkpoint sessions.** The `(arc_id, session_n)` sets in gold's
  arc slice and in `ai/training/output/arc_corpus/sessions_checkpoint.jsonl` are identical.
- **235 distinct arcs**; sessions per arc: 1 arc × 1 session, 127 arcs × 2, 107 arcs × 3.
- All 235 arc records carry `verdict: accept` in `arc_records.jsonl`; the gold arc set equals the
  record set exactly.
- Turn pairs per session: min 8 / median 16 / max 28 → **9,587 assistant turns and 9,587 client
  turns** across the slice.
- Provenance present on every row: `type, arc_id, session_n, plan_path, writer_model,
  auditor_model, verdict, spec_version, domain`. Verdicts: accept ×576. Spec version: 1 ×576.
  Domains: 16 values (largest `nightmare_fuel` ×206).
- Writer models (historical spellings, 7 distinct ids): `deepseek/deepseek-v4.1-flash` ×226,
  `deepseek-v4.1-flash` ×135, `deepseek-ai/DeepSeek-V4.1-Flash` ×111,
  `cf/@cf/deepseek-ai/deepseek-v4-flash-0731` ×43, `cx/gpt-6-astra` ×26,
  `deepseek-ai/deepseek-v4.1-flash` ×25, `Qwen3.8-27B` ×10 — five spellings of one DeepSeek
  family, an artifact of pipeline eras. Cosmetic only: provider rows exclude provenance.
- Auditor models: `moonshotai/kimi-k3` ×507, `cf/@cf/zai-org/glm-5.2` ×69.
- `consolidated_at` range of the slice: 2026-09-26T22:25:59Z → 2026-10-10T04:01:11Z.
- Difficulty spread: severe ×217, moderate ×127, high ×125, adversarial ×97, catastrophic ×10.
- Plan coverage: all 235 arcs have plan files under `ai/training/arc_plans/` (235 `.json` plus a
  non-plan `seed_map.jsonl` index; no orphan plans, no missing arcs).

## 4. Screening results

### 4.1 Ledger validation ([`ARC_CORPUS_SPEC.md`](../../ai/training/ARC_CORPUS_SPEC.md) §4 contract)

- Every assistant turn splits into a leading JSON line + prose; all **9,587** leading JSON lines
  parse and contain **exactly** the nine keys (`dx, def, soma, risk, hx, onset, track, tx, tl`):
  **0 key-set violations**. Value census: **35 turns (0.37%) across 4 sessions carry an empty
  `hx: ""`** — arc_0085 s1 (21), arc_0081 s1 (9), arc_0108 s1 (3), arc_0205 s1 (2). Spec §4
  requires non-empty values, so these are a recorded deviation, not a silent pass. (Correction,
  2026-10-10: the first draft of this section claimed 0 value violations; the emitter's
  independent check during execution found these 35 — the earlier screening had under-counted.)
- Risk-token grammar (spec §4: the value begins with `none` / `passive` / `active`):
  **28 turns flagged (0.29%) across 4 sessions** — `arc_0017` s1 (10), `arc_0109` s1 (1),
  `arc_0160` s2 (2), `arc_0187` s1 (15). All four are DeepSeek-V4.1-Flash-era and audit-accepted
  under spec v1. The values keep the risk read but not token-leading, e.g.
  `third-party child-safety: active — …` (×11), `client risk none stated; partner threat live…`,
  `medical emergency — acute left visual loss…`.
- **Disposition: ship as-is — adopted per the owner's 2026-10-10 instruction to begin the four
  grant items.** The corpus is closed and audit-accepted; rewriting accepted content would break
  the frozen-cursor discipline and the identity scheme. The variances (risk phrasing, empty
  `hx`) are data-realism properties, not safety signals — the risk reads are present and the
  ledgers parse. The alternative (targeted regen) re-opens the closed dataset lane and is out of
  scope for this plan. The empty-`hx` finding surfaced during execution, after the instruction;
  it is flagged in §9 for the owner's review alongside the ratified items.

### 4.2 Token profile (chars ÷ 4; a planning estimate — real tokens get measured via Render Samples)

- Per row: min 1,818 / p50 7,013 / p95 13,448 / max 23,177 tokens.
- Slice total: 4,325,355 tokens. (Readiness §2 records ≈4.36M by chars/4 as the planning
  estimate; the precise content-only recount under this document's method is what is frozen
  here.)

### 4.3 PII / pattern screen

- **0 hits across all 576 rows** for: e-mail addresses, SSN patterns, US phone-number patterns,
  16-digit card-number patterns, URLs, IPv4 literals.
- The corpus is synthetic by construction — plan-driven fictional-client dialogue, no patient
  records. This screen is evidence for the owner's consent/sensitivity determination
  (readiness item 5), not a substitute for it.

### 4.4 Duplicates

- **0 content-hash collisions** across the slice (the splitter's `get_convo_hash`, md5 over all
  message text). Every session is unique.

### 4.5 Structure

- 576/576 rows: strict `user`-first / `assistant`-last alternation, 0 `system` messages,
  0 empty message contents, 0 malformed JSON. The 189,735-line gold file parses loss-free.

## 5. Proposed splits (D4 — seed-level grouping)

### 5.1 Group-key construction (frozen)

Per row, from the arc's plan file (`provenance.plan_path`):

- `source_family` = the plan's `seed.source` (values present: `nightmare_scenarios`,
  `edge_cases`, `probe_arc_v1`);
- `source_id` = `seed.scenario_id` when non-null, else the arc's own `arc_id`;
- group key = `"<source_family>::<source_id>"` — the splitter's own
  [`_source_family_key`](../../ai/training/dataset_splitter_stratified.py) composition.

This is D4 as decided: 147 of 235 plans carry `scenario_id: null` (146 `edge_cases` + 1
`probe_arc_v1`) — those arcs cannot cross-match a seed scenario by construction, so their
sessions group at arc level; the 88 `nightmare_scenarios` plans group at seed level.

### 5.2 Group census

- **224 distinct groups** over 576 rows: 77 seed groups (225 rows) + 147 arc-fallback groups
  (351 rows).
- **11 seed scenarios are shared by more than one arc** — the exact leakage hazard D4 closes.
  Arc-level grouping would have split every pair below across train/val/test:

| Seed scenario | Arcs |
|---|---|
| `nightmare_scenarios::nf_001` | arc_0117, pilot_09 |
| `nightmare_scenarios::nf_002` | arc_0161, pilot_03 |
| `nightmare_scenarios::nf_010` | arc_0174, pilot_05 |
| `nightmare_scenarios::nf_016` | arc_0175, arc_0189 |
| `nightmare_scenarios::nf_018` | arc_0123, arc_0225 |
| `nightmare_scenarios::nf_032` | arc_0116, pilot_02 |
| `nightmare_scenarios::nf_034` | arc_0158, pilot_10 |
| `nightmare_scenarios::nf_048` | arc_0143, arc_0214 |
| `nightmare_scenarios::nf_068` | arc_0148, pilot_06 |
| `nightmare_scenarios::nf_075` | arc_0153, pilot_04 |
| `nightmare_scenarios::nf_087` | arc_0120, arc_0200 |

### 5.3 Assignment and computed proposal

Method: the splitter's own deterministic rule, imported and run (not re-implemented) — each
group is assigned by `int(md5(group_key)[:8], 16) % 100` → <70 train, <85 val, else test; whole
groups move together. **No arc's sessions straddle splits**, and the 11 shared scenarios move as
single units.

| Split | Rows | Share | Tokens (chars ÷ 4) | Groups |
|---|---|---|---|---|
| train | 418 | 72.6% | 3,106,534 | 163 |
| val | 80 | 13.9% | 609,606 | 31 |
| test | 78 | 13.5% | 609,215 | 30 |

| Difficulty | train | val | test |
|---|---|---|---|
| severe | 160 | 25 | 32 |
| moderate | 95 | 16 | 16 |
| high | 88 | 29 | 8 |
| adversarial | 65 | 10 | 22 |
| catastrophic | 10 | 0 | 0 |

### 5.4 Integrity-gate results and recorded deviations

The splitter's `integrity_gates` were run over the proposal:

- **Pass:** hash-disjoint (0 content hashes in >1 split), source-family disjoint (by
  construction — whole groups move), no evaluation-flagged material in train (none exists).
- **Ratio gate (±2pp of 70/15/15):** train fails at 73pp (3pp over target); val 13.9pp and
  test 13.5pp pass.
- **Balance gate:** 5 difficulty strata fall outside ±2pp of the global split ratio —
  severe (val 11.5pp vs 13.9), adversarial (train 67.0pp vs 72.6), moderate (74.8), high (70.4),
  catastrophic (100% train).
- **Why:** those gates were built for the 189k-row master corpus, where one source group is
  ~0.0005% of the data. Here one group averages 2.6 rows (~0.45% of the slice), so pure hash
  assignment cannot land inside ±2pp on every axis at this corpus size.
- **Catastrophic concentration:** all 10 catastrophic rows (the pilot-era arcs
  pilot_03/04/05/09) hash to train (buckets 21–57). All four sit inside shared seed groups, so
  moving them would also move their partner arcs (arc_0117, arc_0153, arc_0161, arc_0174).

**Options (owner's call; option 1 adopted per the 2026-10-10 instruction):**

1. **Accept the hash assignment as-is — adopted 2026-10-10.** Leakage safety is the non-negotiable
   property and holds by construction; val (80 rows / 0.61M tokens) and test (78 rows / 0.61M)
   are well-sized for pilot evaluation; the deviations above are recorded facts, not defects.
2. **Deterministic rebalance after hashing.** Move whole train groups to val/test — ordering
   rule: train groups by row count descending, then group key ascending; move until train ≤ 414
   rows (≤72pp), then top up val to ≥75 rows, preferring moves that also carry catastrophic or
   adversarial rows; every moved group recorded in the manifest. Leakage-safe by construction
   and ratio-clean, but no longer the pure hash — determinism rests on the recorded rule.

## 6. Snapshot identity (frozen method and values)

Three hashes pin the slice. Re-run and compare before any emission; if gold changed, stop,
re-screen, and update this plan first.

1. **Gold source of record** — sha256 of `ai/data/curated/sft_chatml/train_master_gold.jsonl`:
   `d357b8b573740f418c657c5d3e3421542c31d93b36ccc1d65e9a004a5f386bef`
2. **Arc-slice payload identity** — sha256 of the 576 arc lines concatenated byte-for-byte in
   gold file order:
   `0babff8580cf9b2c176187ece019592280e337c03b222f1ab9bca631bf2283a3`
3. **Ordered per-row manifest** — sha256 of the newline-joined per-line sha256 hex digests
   (gold file order):
   `d6c4147d3287f84b7407dc2762aed87c6451af8b2f1ad65a372690c07a3db272`

Reproduction (read-only, local, run from the `ai/` repo root):

```python
import hashlib, json
path = "data/curated/sft_chatml/train_master_gold.jsonl"
gold = hashlib.sha256()
with open(path, "rb") as f:
    for chunk in iter(lambda: f.read(1 << 22), b""):
        gold.update(chunk)
lines = []
with open(path, "rb") as f:
    for raw in f:
        row = json.loads(raw.decode("utf-8"))
        if (row.get("provenance") or {}).get("arc_id"):
            lines.append(raw)
slice_sha = hashlib.sha256(b"".join(lines)).hexdigest()
manifest_sha = hashlib.sha256(
    "\n".join(hashlib.sha256(l).hexdigest() for l in lines).encode()
).hexdigest()
print(gold.hexdigest(), len(lines), slice_sha, manifest_sha)
```

Expected: the three values above and `len(lines) == 576`. At execution, the emitted files'
sha256s and row counts are recorded alongside these before anything is approved for upload.

## 7. Privacy profile

- **Content:** synthetic, plan-driven fictional-client dialogue; no patient records, no real
  persons. PII screen: 0 hits (§4.3).
- **Provider payload contents:** dialogue text with role/weight only — no provenance, model ids,
  timestamps, internal paths, or tags (§2.2).
- **Provider privacy mechanisms exist** (readiness §2): Zero Data Retention policy, Secure
  Training surfaces, BYOB, CMEK. Their account-level applicability is a Phase 1 owner item.
- **The approval boundary is unchanged and total:** the privacy-approval gate (readiness item 6 /
  §4 gate 1) governs everything that leaves this environment — training upload, and later,
  evaluation traffic (§2.5). Nothing in this plan moves data.

## 8. Gated execution checklist (approval granted by the owner's 2026-10-10 instruction; executed same day — §9)

Precondition note: the Phase 1 entry conditions (readiness items 4–6, 13) gate **external**
transfer, and the local emission moves nothing out of this environment, so the owner's
instruction was executed for the local steps only. All steps are local:

1. **Identity re-check** — run §6 against current gold. Mismatch → stop; re-screen and update
   this plan first.
2. **Emit** per §2 (provider files + internal manifest). The emitter was written at execution
   under this spec: `ai/training/export_fireworks_payload.py` (§9).
3. **Validate emission:** per-turn schema (roles, weights, 9-key ledger), token profile re-check,
   group-key and split counts must match §5.3 exactly, PII re-screen, duplicate re-check;
   record emitted-file identities.
4. **Report to owner and stop.** Upload/provisioning is a separate, explicit gate
   (readiness §4); the first provider contact is the Phase 3 format smoke test, itself gated.

## 9. Execution record (2026-10-10)

The owner's 2026-10-10 instruction to begin the four grant items was executed as approval for
the **local emission** (readiness §4 gate 1). Nothing left this environment; every external step
still requires the Phase 1 determinations and the separate upload gate.

- **Identity re-check:** all three §6 hashes matched current gold (`d357b8b5…` /
  `0babff85…` / `d6c4147d…`), 576 arc rows.
- **Emitter:** `ai/training/export_fireworks_payload.py` (sha256
  `49a703d373e09db0ec044a46813d0168a7c35a5d12b1209c6f0f0adc4c5982bd`), ruff-clean, fail-closed on
  identity, census, ledger key-set, PII, duplicates, and content fidelity; `--dry-run` supported;
  re-runnable (atomic writes, idempotent).
- **Artifacts** under `ai/training/output/arc_corpus/export/fireworks_pilot_v1/`:

| File | Rows | sha256 |
|---|---|---|
| `train.jsonl` | 418 | `281da447e675c60f06c56e160bae6fece23db4f2c8d41d4a3ebbbad94a09755b` |
| `val.jsonl` | 80 | `615487846c3fd503c7627b776e17752713924de6d028bf208872dda3194bd609` |
| `test.jsonl` | 78 | `35f34d0986446253ed7f5abb0ab1a5c731522c075b8332164e3831d6ee0de914` |
| `manifest_internal.jsonl` | 576 | `f7e19cb6422b16f77b7cedcf818aaaf7c5a5c37646f58e63ebf765df7e7f2a14` |

- **Validation:** 576/576 rows content-identical to the gold arc slice (independent multiset
  re-derivation); provider rows carry `messages` only, messages carry `role`/`content`/`weight`
  only; weights 0/1 by role; 0 PII hits; 0 duplicates; 0 content hashes, group keys, or arcs
  spanning splits; 9,587 assistant turns; 4,325,355 tokens (chars ÷ 4). Arc-fallback rows by
  split: train 250 / val 55 / test 46 (351 total). Full machine-readable record in the
  directory's `identity.json` (including the emitter's own sha256 and the per-session
  deviation flags).
- **Documented deviations carried (content unchanged):** 6 integrity-gate ratio/balance
  deviations (§5.4), 28 risk-grammar turns, 35 empty-`hx` turns (§4.1). The emitter asserts the
  exact counts fail-closed, so any future drift breaks the run instead of shipping silently.
- **Stopped at the upload gate.** Nothing was uploaded, provisioned, or spent. `test.jsonl`
  never leaves this environment regardless of later approvals (Phase 4 held-out set); Phase 3
  evaluation traffic is covered by the same privacy-approval boundary as the upload (§2.5).

## 10. Open items for the owner

- **Resolved 2026-10-10** (owner instruction; recorded in §9): (a) split disposition — accept
  the hash assignment (§5.4 option 1); (b) risk-grammar disposition — ship as-is (§4.1); (c)
  export approval for the **local** emission (readiness §4 gate 1) — granted and executed.
- **Phase 1 determinations — granted 2026-10-10** (owner instruction + same-day confirmations;
  grant records in [`fireworks-approval-packages.md`](./fireworks-approval-packages.md)): items
  4–6 determined/approved, item 13 named (the owner as experiment owner and sole clinical
  reviewer for now), D1–D3 ratified, final model GLM 5.3 Flash. Phase 1 is complete.
- **Later gates — granted 2026-10-10, each recorded separately:** upload/provisioning
  **executed** on the replacement account `linencloset` (Package F — pilot log §7: both
  planned datasets `READY`, 418/80, `encryptionState` PLAINTEXT); budget cap $635 active, $0
  spent (Package G); experiment granted with step-order binding (Package H — next: Render
  Samples). **Release (Phase 4) remains un-granted.**
- For review, not action: the 35 empty-`hx` turns (§4.1) surfaced during execution and ship as
  a documented deviation; the execution record (§9) is the complete evidence.

## 11. Document validation (self-check, 2026-10-10)

- Links resolve to the referenced files; live corpus counts live in the handoff, provider facts
  in readiness §2 (plus the 2026-10-10 fine-tuning-guide facts cited in §2.4), and this
  document's numbers are its own screening subject.
- No secrets, credentials, or clinical examples appear here; the seed/arc identifiers are
  synthetic ids.
- Nothing is uploaded by this document; no provider commands appear. The local emission was
  executed 2026-10-10 under the owner's instruction and is recorded in §9; every external
  step remains un-granted.
- The three recorded deviations (train ratio 73pp; 28 risk-grammar turns; 35 empty-`hx` turns)
  are findings with dispositions — not smoothed over; the correction of the draft's under-count
  is itself recorded (§4.1).
- Screening method note: all checks were defined and run read-only in this environment on
  2026-10-10; the split assignment used the splitter's imported functions, not a re-implementation.
