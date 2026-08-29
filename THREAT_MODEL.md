# Threat Model & Security Posture — Linear Audit Data Pipeline

> STRIDE threat analysis, trust boundaries, and data quality controls for the Linear audit ETL system and documentation assets.

---

## 1. System Overview & Boundaries

The Linear audit subsystem acts as an ETL bridge between the upstream Linear GraphQL API and the local/public documentation assets.

```
┌───────────────────────────────────────────────┐
│              Linear GraphQL API               │
│          (Upstream SaaS Data Source)          │
└───────────────────────┬───────────────────────┘
                        │ (HTTPS / Raw API Key Auth)
                        ▼
┌───────────────────────────────────────────────┐
│     Ingestion & Transformation (ETL Layer)    │
│  • fetch_issues.py (Rate-limited, Bounded)    │
│  • Pydantic / Typed Schema Validation         │
└───────────────────────┬───────────────────────┘
                        │ (Local FS Validation)
                        ▼
┌───────────────────────────────────────────────┐
│         Artifacts & Analysis Pipeline         │
│  • issues.json (Flat MCP v2 Dataset)          │
│  • run_audit.py (Hygiene & Duplicate Gating)  │
│  • remediate.py (Safe Write-Back Engine)      │
│  • refresh_dashboard.py (Metrics Rendering)   │
└───────────────────────────────────────────────┘
```

---

## 2. Trust Boundaries

- **TB-1: Linear SaaS to ETL Client** — Network boundary protected by HTTPS and API key authentication.
- **TB-2: ETL Ingestion to On-Disk Artifacts** — File system boundary validating data shape before persistence.
- **TB-3: Remediation Engine to Linear Write API** — Critical boundary requiring explicit opt-in (`--apply`) before triggering mutations.
- **TB-4: Webhook Receiver to Dashboard Refresh** — Boundary verifying webhook payload authenticity and secret validation (`whsec_...`).

---

## 3. STRIDE Threat Analysis & Mitigations

### 1. Spoofing
- **Threat**: Forged or unauthorized API key used to query or manipulate Linear issues.
- **Mitigation**: Environment variable validation, raw key contract enforcement, failure on missing key without silent fallbacks.

### 2. Tampering
- **Threat**: Malformed or malicious JSON injected into `issues.json` to corrupt audit results or trigger code execution.
- **Mitigation**: Strict schema validation (`load_issues` checks shapes, rejects non-list issues, validates issue structure).

### 3. Repudiation
- **Threat**: Remediation updates or archives issues without audit trail.
- **Mitigation**: Dry-run mode by default; every mutation outputs issue identifier, fields altered, and mutation success status to stdout/audit reports.

### 4. Information Disclosure
- **Threat**: API tokens, private customer issue descriptions, or confidential risk items leaked in error logs or dashboards.
- **Mitigation**: Automatic secret redaction in exception handlers; sanitized dashboard output containing only high-level status aggregations.

### 5. Denial of Service
- **Threat**: Unbounded pagination loop exhausts memory or triggers Linear API 429 rate limit lockouts.
- **Mitigation**: Max page guard (`max_pages=100`), configurable page size (`page_size=50`), request delays, and exponential backoff on retries.

### 6. Elevation of Privilege
- **Threat**: Audit tool inadvertently deletes or mutates issues beyond authorized scope.
- **Mitigation**: Scoped GraphQL mutations limited to `issueUpdate` and `issueArchive` on targeted IDs only.

---

## 4. Verification & Continuous Monitoring

1. **Pre-commit & CI SAST**: Bandit security scanning enforced on all scripts.
2. **Data Contract Unit Tests**: Pytest asserting shape compliance on all JSON artifacts.
3. **Redaction Tests**: Automated tests asserting API keys are stripped from error traces.
