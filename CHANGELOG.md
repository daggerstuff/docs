# Changelog

All notable changes to the `docs-linear-audit` toolkit are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Split `linear-audit/refresh_dashboard.py` into `dashboard_render.py` (pure
  markdown-rendering helpers) and a thinner `refresh_dashboard.py` (API fetch +
  CLI). Rendering logic is now importable and testable without network access.

## [0.1.0] - 2026-08

### Added

- `fetch_issues.py` — Linear GraphQL ingestion with bounded pagination and v2
  MCP flat-shape transformation.
- `run_audit.py` — workspace hygiene audit (duplicate detection, unassigned
  issues, missing descriptions, estimate coverage, project review, archival).
- `remediate.py` — safe dry-run-by-default write-back mutations.
- `refresh_dashboard.py` — Enterprise Readiness dashboard generator.
- `register_webhook.py` — Linear webhook registration, listing, and removal.
- `models.py` — pydantic v2 data contracts for the v2 Linear MCP flat shape.
- `pipeline.py` — end-to-end ETL orchestrator with data-quality gating.
- Full pytest suite plus ruff, mypy, bandit, and pip-audit CI gates.