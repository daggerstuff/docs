# Security Policy & Guidelines

> Security and vulnerability disclosure policies for the **Pixelated Empathy** documentation and data engineering platform.

---

## 1. Reporting a Vulnerability

Please report security issues or sensitive findings via email to **security@vectorize.io** with:
- Summary of the vulnerability and potential data impact.
- Step-by-step reproduction instructions, payload examples, or scripts.
- Commit hash or file paths affected.

Do not submit public GitHub issues for security vulnerabilities until coordinated remediation is complete.

---

## 2. Data Engineering & API Security Principles

1. **Authentication Hygiene**:
   - Linear API keys are supplied exclusively via environment variables (`LINEAR_API_KEY`) and are never committed to version control.
   - Linear API keys use raw header format (`Authorization: lin_api_...`), preventing token collision.

2. **Secret Redaction**:
   - Error messages, logs, and tracebacks automatically redact authorization headers, tokens, and private identifiers.

3. **Safe Write-Back (Least Privilege)**:
   - Remediation tools default strictly to dry-run mode (`--dry-run`). The `--apply` flag must be explicitly passed to trigger mutations.

4. **Input Sanitization & Schema Validation**:
   - Ingestion payloads are strictly validated against the v2 flat contract. Corrupted, oversized, or unescaped strings are rejected before writing to persistent storage.

---

## 3. Automated Scanning & SAST

- **Bandit SAST Scans**: Run on all Python files across `linear-audit/` and `tests/`.
- **Ruff Linter & Security Rules**: Enforce zero suppressions, strict formatting, and clean code paths.
- **Dependency Audits**: Automated Dependabot checks keep all runtime and development libraries current.
