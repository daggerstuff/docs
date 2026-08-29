# Pixelated Empathy Documentation & Data Engineering Platform

> Central documentation portal, enterprise compliance frameworks, and Linear workspace audit ETL data engineering pipeline for the **Pixelated Empathy** ecosystem.

[![CI](https://img.shields.io/github/actions/workflow/status/daggerstuff/pixelated/ci.yml?style=flat-square&labelColor=0f0f1a)](https://github.com/daggerstuff/pixelated)
[![Python](https://img.shields.io/badge/Python-3.12+-1a1a2e?style=flat-square&labelColor=0f0f1a&logo=python&logoColor=white)](https://python.org)
[![Linear](https://img.shields.io/badge/Linear-MCP%20v2%20Compatible-5e6ad2?style=flat-square&labelColor=0f0f1a)](linear-audit/README.md)
[![License](https://img.shields.io/badge/License-MIT-1a1a2e?style=flat-square&labelColor=0f0f1a)](LICENSE)

---

## 1. 🏗️ Architecture & Data Flow

```mermaid
flowchart TD
    subgraph Sources["Upstream Data Sources"]
        LinearAPI["Linear Workspace GraphQL API
(Projects, Issues, Cycles)"]
        Webhooks["Linear Real-Time Event Webhooks
(Issue Mutations, State Changes)"]
    end

    subgraph Pipeline["Linear Audit ETL & Data Quality Pipeline"]
        Ingest["1. fetch_issues.py
(Bounded Pagination & Ingestion)"]
        Transform["2. MCP v2 Flat Transformation
(Schema Normalization & Contract Gating)"]
        Audit["3. run_audit.py
(Data Quality, Duplicate Detection, Hygiene Checks)"]
        Remediate["4. remediate.py
(Safe Dry-Run & Targeted Mutation Engine)"]
        Dashboard["5. refresh_dashboard.py
(Workstream Aggregation & Metrics Generation)"]
    end

    subgraph Sinks["Downstream Artifacts & Visualizations"]
        IssuesJSON[("issues.json
(Normalized v2 MCP Dataset)")]
        AuditResults[("audit_results.json
(Hygiene & Deduplication Register)")]
        DashboardMD["dashboard.md
(Enterprise Readiness Executive Report)")]
        Mintlify["Mintlify Documentation Portal
(Public & Internal Guides)"]
    end

    LinearAPI --> Ingest
    Webhooks --> Dashboard
    Ingest --> Transform
    Transform --> IssuesJSON
    IssuesJSON --> Audit
    Audit --> AuditResults
    AuditResults --> Remediate
    AuditResults --> Dashboard
    IssuesJSON --> Dashboard
    Dashboard --> DashboardMD
    DashboardMD --> Mintlify
```

---

## 2. 📦 Core Modules & Tooling

| Module | Purpose | Primary Inputs / Outputs |
| :--- | :--- | :--- |
| [`linear-audit/fetch_issues.py`](linear-audit/fetch_issues.py) | Ingests issues from Linear via GraphQL, applies bounded pagination, and flattens into v2 MCP format | Inputs: `LINEAR_API_KEY`, `LINEAR_TEAM_ID`<br/>Output: `issues.json` |
| [`linear-audit/run_audit.py`](linear-audit/run_audit.py) | Analyzes issue dataset for duplicate pairs, unassigned tasks, missing descriptions, and estimate gaps | Input: `issues.json`<br/>Output: `audit_results.json` |
| [`linear-audit/remediate.py`](linear-audit/remediate.py) | Executes safe write-back mutations to resolve duplicates, archive completed items, and set ownership | Input: `audit_results.json`<br/>Flags: `--dry-run` (default), `--apply` |
| [`linear-audit/refresh_dashboard.py`](linear-audit/refresh_dashboard.py) | Calculates workstream progress across enterprise epics and renders dynamic markdown tables | Inputs: Linear API / Live Data<br/>Output: `dashboard.md` |
| [`linear-audit/register_webhook.py`](linear-audit/register_webhook.py) | Manages automated Linear webhook subscriptions for instant dashboard updates on issue updates | Commands: `register`, `list`, `unregister` |

---

## 3. 📋 Data Contracts & Schema Specification

The pipeline standardizes all Linear data into the **v2 Linear MCP Flat Shape**:

```json
{
  "id": "PIX-1873",
  "title": "Implement Redis session caching layer",
  "description": "Configures Redis cluster on port 6379...",
  "priority": { "value": 1, "name": "Urgent" },
  "estimate": { "value": 2, "name": "2" },
  "status": "Done",
  "statusType": "completed",
  "labels": ["backend", "cache"],
  "createdBy": "Chad",
  "createdById": "user-uuid-1",
  "assignee": "Chad",
  "assigneeId": "user-uuid-1",
  "project": "Enterprise Readiness",
  "projectId": "proj-uuid-1",
  "parentId": "PIX-4125",
  "team": "Pixelated",
  "teamId": "team-uuid-1",
  "createdAt": "2026-08-01T12:00:00Z",
  "updatedAt": "2026-08-20T15:30:00Z"
}
```

### Data Quality Rules
- **Non-Empty Identifiers**: Every record must have a valid `PIX-XXX` format key.
- **Normalized Status Types**: `statusType` strictly mapped to Linear state types (`triage`, `backlog`, `unstarted`, `started`, `completed`, `canceled`).
- **Idempotent Ingestion**: Re-running ingestion never duplicates entries or corrupts timestamps.
- **Contract Boundary Validation**: Invalid payloads and missing keys are rejected at ingestion rather than corrupting audit tables.

---

## 4. ⚡ Quickstart & Development

### Setup Environment

```bash
# Clone and enter workspace
cd /home/vivi/pixelated/docs

# Install dependencies using uv
uv pip install -e ".[dev]"
```

### Environment Variables

```bash
# Linear API authentication (Raw API Key contract)
export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxxxxxxxxx"
export LINEAR_TEAM_ID="52861523-9089-49a3-8be5-4032d68cb55a"
export LINEAR_PROJECT_ID="29c133a2-9195-42d3-b53e-31154d47ea7d"
```

### Running the Pipeline

```bash
# 1. Fetch live issues from Linear
python3 linear-audit/fetch_issues.py --limit 50 --max-pages 100

# 2. Run hygiene audit & duplicate detection
python3 linear-audit/run_audit.py

# 3. Dry-run remediation review
python3 linear-audit/remediate.py --dry-run

# 4. Refresh executive readiness dashboard
python3 linear-audit/refresh_dashboard.py
```

### Running Tests & Quality Audits

```bash
# Run unit & data contract test suite
uv run pytest

# Run linting and style validation
uv run ruff check .
uv run ruff format --check .

# Run security SAST audit
uv run bandit -c pyproject.toml -r linear-audit tests
```

---

## 5. 🛡️ Security & Privacy

- **Raw API Key Contract**: Authorization headers use raw API keys (`Authorization: lin_api_...`) avoiding Bearer token collision.
- **Token Redaction**: API keys and tokens are never echoed to logs, exception messages, or stdout.
- **Read-Only Dry Run Default**: `remediate.py` defaults to dry-run mode to prevent accidental workspace mutations.
- See [SECURITY.md](SECURITY.md) and [THREAT_MODEL.md](THREAT_MODEL.md) for full security controls.
