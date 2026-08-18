# Security Findings Register

**Parent:** PIX-4126 — Enterprise Gap: Penetration Testing & External Security Assessment
**Sub-issue:** PIX-4143 (S9) — Remediation, Reporting & Retest
**Last updated:** 2026-07-31
**Owner:** Chad
**Status:** Active — pre-populated with S3 automated scan baseline (0 Critical / 0 High)

---

## 1. Purpose

Single lifecycle tracker for every confirmed security finding, from discovery
to closure. Complements the quarterly findings archive
(`docs/runbooks/security-assessments/`) by tracking per-finding remediation
state, SLA deadlines, and verification evidence regardless of which assessment
surfaced the finding.

---

## 2. Finding Lifecycle

```
Discovery → Triage (severity/CVSS) → Linear ticket (SEC-FIND-NNN)
  → Remediation (per SLA) → Retest → Verification → Closure → Archived
```

Closure requires: fix deployed **and** retested by the tester/owner **and**
engineering-lead sign-off for Critical/High (per runbook §7).

---

## 3. Severity & Remediation SLA

| Severity | CVSS | Remediation SLA | Source |
|----------|------|-----------------|--------|
| Critical | 9.0–10.0 | 7 days | `penetration-testing-assessment.md` §7 |
| High | 7.0–8.9 | 30 days | §7 |
| Medium | 4.0–6.9 | 90 days | §7 |
| Low | 0.1–3.9 | 180 days | §7 |
| Info | N/A | Next quarter | §7 |

---

## 4. Findings Tables

> **Baseline (2026-07-30):** S3 automated scans (Trivy, Checkov, pnpm audit,
> pip-audit) — **0 Critical / 0 High**. Reintroduction of any Critical/High
> finding fails CI via the security regression gate (`security-regression-gate.sh`).

### 4.1 Critical

| ID | Title | Asset | CVSS | Found | SLA due | Fix PR | Retest | Closed | Linear |
|----|-------|-------|------|-------|---------|--------|--------|--------|--------|
| _— none —_ | | | | | | | | | |

### 4.2 High

| ID | Title | Asset | CVSS | Found | SLA due | Fix PR | Retest | Closed | Linear |
|----|-------|-------|------|-------|---------|--------|--------|--------|--------|
| _— none —_ | | | | | | | | | |

### 4.3 Medium

| ID | Title | Asset | CVSS | Found | SLA due | Fix PR | Retest | Closed | Linear |
|----|-------|-------|------|-------|---------|--------|--------|--------|--------|
| _— none —_ | | | | | | | | | |

### 4.4 Low

| ID | Title | Asset | CVSS | Found | SLA due | Fix PR | Retest | Closed | Linear |
|----|-------|-------|------|-------|---------|--------|--------|--------|--------|
| _— none —_ | | | | | | | | | |

### 4.5 Info / Recommendations

| ID | Title | Asset | Source | Status |
|----|-------|-------|--------|--------|
| _— none —_ | | | | |

---

## 5. Detailed Finding Entry Template

```markdown
### SEC-FIND-NNN — <Title>

- **Severity / CVSS:** High (7.5)
- **Affected asset:** <service / endpoint>
- **Source:** <assessment ID, e.g. 2026-Q3>
- **Discovered:** YYYY-MM-DD
- **Description:** ...
- **Reproduction steps:**
  1. ...
- **Impact:** ...
- **Remediation:** <PR link>
- **Retest:** <date + result>
- **Verification:** <who signed off>
- **SLA deadline:** YYYY-MM-DD (met? yes/no)
- **Closure date:** YYYY-MM-DD
- **Linear ticket:** SEC-FIND-NNN
```

---

## 6. Regression Gate

The CI security regression gate (`scripts/ci/security-regression-gate.sh`)
fails the pipeline when known-remediated findings are reintroduced (e.g. a
vulnerable dependency reappears in the lockfile). Adding a newly-confirmed
finding's signature to the gate prevents regression while remediation is in
flight.

---

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-07-31 | Chad | Initialized register with S3 baseline (0 Critical / 0 High) |
