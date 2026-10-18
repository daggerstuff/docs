# Master Plan — RAW UNEDITED LIST

> Generated: 2026-08-01
> Purpose: Complete inventory of every task, plan, roadmap, and work item discovered across the pixelated monorepo and all submodules.
> Method: Exhaustive file search + content scan. No filtering, no dedup, no status assessment.

---

## SOURCE 1: LINEAR PROJECTS & ISSUES

### Enterprise Readiness Program (PIX-4131 EPIC) — ALL DONE
- PIX-4125: Enterprise gap — SOC2/HIPAA — DONE
- PIX-4126: Enterprise gap — DR — DONE
- PIX-4127: Enterprise gap — pen testing — DONE
- PIX-4128: Enterprise gap — chaos eng — DONE
- PIX-4129: Enterprise gap — SLA/SLO — DONE
- PIX-4130: Enterprise gap — vendor risk — DONE
- PIX-4133 (DR-2): Database Backup & Restore Testing — DONE
- PIX-4134 (DR-3): Infrastructure Disaster Recovery Procedure — DONE
- PIX-4146 (SLA-3): Draft Customer SLA Contract Terms — DONE
- PIX-4148 (CE-1): Install Chaos Engineering Tooling — DONE
- PIX-4149 (CE-2): Define Resilience Testing Scenarios — DONE
- PIX-4150 (CE-3): Run Weekly Chaos Experiments — DONE
- PIX-4157 (SOC2-4): Engage External Auditor — DONE

### CI Federation & Release Readiness — ALL DONE/CANCELED
- PIX-3746 (EPIC): CI Federation Execution & Go-Live — DONE
- Promotion gate test workflow — DONE (commit d03f0ac11)
- CI operating model RFC — APPROVED

### ML & Platform Remediation Sprint — ALL DONE (1 CANCELED)
- PIX-4192 (P0): Stage-Aware Deduplication Algorithm — DONE
- PIX-4193 (P0): Stage-Based Dataset Directory Organizer — DONE
- PIX-4194 (P0): Stage 4 Voice Persona Processing Pipeline — DONE
- PIX-4195 (P0): Correct Stage 1 Training Notebook Path — DONE
- PIX-4196 (P1): Stabilize TypeScript Test Baseline (42 Vitest Failures) — DONE
- PIX-4197 (P1): Fix NeMo Data Designer NGC Auth — CANCELED
- PIX-4198 (P1): Field-Level FHE Database Encryption Hooks — DONE
- PIX-4199 (P2): Ingest Stage 5 Safety/DPO Datasets — DONE
- PIX-4200 (P3): Causal DAG Execution Engine & Intervention API — DONE

### Vertical Fidelity Stack Implementation — ALL DONE
- P0-1 Edge-Case Safety Filter Bypass — DONE
- R1 Cryptographic Receipts — DONE
- L4 JIT Trigger Engine — DONE
- INT-1 through INT-5 integration tickets — ALL DONE

### Training Pipeline v2 — Audit Remediation — COMPLETED
- Phase 1-7 all DONE

### AI Research-Clinical Integration — COMPLETED
- PIX-3906 through PIX-3912 — ALL DONE

### Foresight Memory Architecture — COMPLETED
- All issues DONE

### Churnmeon Reliability — COMPLETED

### Remaining Open Linear Issues (not archived, not done)
- PIX-4164: Remove @babel/core override once ecosystem patches — TODO (blocked on external)
- PIX-4165: Remove react-router monitoring workaround — TODO (blocked on external)
- PIX-4166: Remove accepted localstack risk once patched — TODO (blocked on external)
- 26 issues lack project assignment (per linear_audit.md)

---

## SOURCE 2: IMPLEMENTATION_PLAN.md (repo root)

### Vertical Fidelity Stack — Remaining Work (as written in file)
1. Emit Events from Bias Detection — HIGH priority
   - File: src/lib/ai/bias-detection/python-service/bias_detection/services/analysis_orchestrator.py
   - After analyze_session() completes, publish EventBus events
2. Wire Receipt Root Hash to Bias Detection — HIGH priority
   - Same file, accept receipt_root_hash in session_data
3. JIT Scenario Injection into Nightmare Fuel — HIGH priority
   - New file: ai/triggers/jit_scenario_injector.py
4. Per-Clinician Flag Grouping — MEDIUM priority
   - File: foresight/foresight/triggers.py
5. Receipt-Ledger Persistence — MEDIUM priority
   - File: ai/receipts/receipt.py + new ai/receipts/persistence.py
6. FHE Ciphertext Hash Integration — MEDIUM priority
   - NOTE: This was completed (PIX-4190) — file is STALE on this item

**NOTE:** The Linear tickets section at bottom of IMPLEMENTATION_PLAN.md shows ALL items checked [x] including INT-1 through INT-5. The "Remaining Work" section appears to be STALE — not updated after completion.

---

## SOURCE 3: PAL_MEDDIES_IMPLEMENTATION_PLAN.md (ai/)

### PAL Framework Implementation — 5 of 6 phases done
- Phase 1: Persona Data Pipeline — DONE
- Phase 2: Mixed-task SFT — DONE
- Phase 3: DPO Preference Pairs — DONE
- Phase 4: Select-then-Generate Inference — DONE
- Phase 5: Evaluation (C.score) — DONE
- Phase 6: End-to-end smoke — OPEN
  - 6.1: Run SFT + DPO on small subset, confirm checkpoint shape, inference latency, C.score movement

---

## SOURCE 4: PIX-1901 Test Coverage Baseline Plan (docs/plans/)

### Test Coverage Baseline (Plan 02) — Status: "Implementation Ready"
- Phase 1: Infrastructure (Week 1) — PIX-160, PIX-3762
- Phase 2: Critical Path (Weeks 2-3) — 10 P0/P1 modules
- Phase 3: Supporting Modules (Weeks 4-5) — 4 P2 modules
- Phase 4: Scale Modules (Weeks 6-8) — 4 P3 modules
- Phase 5: Baseline Lock (Week 9)

---

## SOURCE 5: Session Progress Metrics Plan (docs/superpowers/specs/)

### PIX-3916: Session Progress Tracking — 4 phases defined
- Phase 1: Database Connection Pool Integration — STATUS UNKNOWN
- Phase 2: Defense Metrics API Endpoint — STATUS UNKNOWN
- Phase 3: React Components for Progress Visualizations — STATUS UNKNOWN
- Phase 4: Enhanced Dashboard & Progress Page Integration — STATUS UNKNOWN

---

## SOURCE 6: Deterministic Batching Design (docs/superpowers/specs/)

### Corpus Fidelity Fixes — 3 implementation steps
1. Create surgical_fix_2025_09.py — STATUS UNKNOWN
2. Update monthly_pipeline.py for Postgres+Redis deterministic batching — STATUS UNKNOWN
3. Modify monthly_llm_prompt templates — STATUS UNKNOWN

---

## SOURCE 7: .omo/plans/unify-pixelated-backend.md

### Unified Backend Docker Compose — ALL 10 TODOS DONE
- Task 1: Consolidate env vars — DONE
- Task 2: Unified docker-compose.backend.yml — DONE
- Task 3: FastAPI Dockerfile — DONE
- Task 4: Node microservice Dockerfiles — DONE
- Task 5: DB migration wiring — DONE
- Task 6: Grafana/Prometheus provisioning — DONE
- Task 7: Integration test — DONE
- Task 8: Makefile + pnpm scripts — DONE
- Task 9: Health-check script — DONE
- Task 10: Final verification — DONE
- Final verification F1-F4 — ALL DONE

---

## SOURCE 8: Business Strategy Documents (business-strategy/)

### Expansion Roadmap (06-expansion-roadmap.md)
- Phase 1: Market Validation (Months 1-12) — US/Canada
- Phase 2: Market Expansion (Months 13-24) — UK/Australia/NZ
- Phase 3: Market Leadership (Months 25-36) — Europe/Asia-Pacific
- Phase 4: Global Leadership (Months 37-48) — Global

### Pilot Program Framework (pilot-program-framework.md)
- 6-month institutional validation program
- Month 1: Foundation & Setup
- Month 2: Core Training Integration
- Month 3: Advanced Scenarios & Edge Cases
- Month 4: Specialization & Customization
- Month 5: Competency Assessment & Certification
- Month 6: Scale Planning & Partnership Development

### Other Business Strategy Docs (no explicit task items, strategic reference)
- 01-executive-summary.md
- 02-market-analysis.md
- 03-sales-tactics.md
- 04-partnership-strategy.md
- 05-marketing-division-structure.md
- 09-expansion-pivot-opportunities.md
- case-study-library.md
- crm-marketing-automation.md
- cultural-adaptation-framework.md
- customer-success-management.md
- demo-strategy.md
- international-market-research.md
- outcome-measurement-system.md
- pilot-program-structure.md
- pitch-deck-outline.md
- pricing-strategy.md
- professional-associations.md
- roi-calculator.md
- sales-team-structure.md
- specialized-training-modules.md
- target-institutions.md
- thought-leadership-strategy.md
- university-research-partnerships.md
- webinar-program.md

---

## SOURCE 9: Enterprise Compliance Documents (docs/enterprise/)

### HIPAA Compliance Gap Assessment
- 17 gaps identified across 4 phases
- Phase 1: Governance & Risk (Weeks 1-4) — 6 P0 items
- Phase 2: Breach & BAA (Weeks 5-8) — 5 items
- Phase 3: Procedures & Training (Weeks 9-12) — 5 items
- Phase 4: Documentation & Audit (Weeks 13-16) — 5 items

### SOC2 Readiness Gap Assessment
- 17 gaps identified across 4 phases
- Phase 1: Foundation (Weeks 1-4) — 6 P0 items
- Phase 2: Data & Privacy (Weeks 5-8) — 5 items
- Phase 3: Vendor & Monitoring (Weeks 9-12) — 5 items
- Phase 4: Audit Preparation (Weeks 13-16) — 4 items

### Existing Enterprise Docs (reference, not task-bearing)
- hipaa-officer-designations.md
- hipaa-risk-analysis.md
- hipaa-training-program.md
- baa-template.md
- sla-contract-terms.md
- vendor-inventory.md
- vendor-security-reviews.md
- chaos-production-approval-process.md
- policies/access-control-procedure.md
- policies/change-management-policy.md
- policies/deficiency-tracking-procedure.md
- policies/incident-response-plan.md
- policies/information-security-policy.md
- runbooks/backup-restore-testing.md
- runbooks/dr-rto-rpo-targets.md
- runbooks/infra-disaster-recovery.md
- runbooks/resilience-testing.md
- runbooks/sla-breach-response.md
- runbooks/slo-definitions.md

---

## SOURCE 10: Linear Audit Documents (docs/linear-audit/)

### Quarterly Workspace Audit (linear_audit.md) — ALL 7 CRITERIA MET
- 537 issues audited
- 39 remediations applied
- All acceptance criteria met

### Other Audit Docs (reference)
- risk-register.md
- threat-model-scope.md
- pentest-cadence.md
- vendor-register.md
- vendor-risk-assessment-framework.md
- vendor-engagement.md
- vendor-rfp.md
- vendor-sow.md
- api-specification-vendor-share.md
- s3-scan-results.md
- project_descriptions_audit.md

---

## SOURCE 11: Monitoring (monitoring/)

### FIXME.md — ALL ITEMS TRIAGED (PIX-4100)
- 5 items, all RESOLVED or TRIAGED
- 2 items deferred to infrastructure provisioning (not code tasks)

### MONITORING_README.md — Reference doc

### Alert Coverage Audit (alert-coverage-audit.md) — Reference

### Synthetic Monitoring Scope (synthetic-monitoring-scope.md) — Reference

---

## SOURCE 12: Task Sync Gap Matrix (scripts/task_sync/)

### Cross-System Mapping Gaps — 8 fixes identified
1. `review` canonical state missing from STATUS_ALIASES — HIGH
2. No priority sync between providers — HIGH
3. No label sync — MEDIUM
4. No per-project mappings — HIGH
5. 162 unmapped Linear-only issues — MEDIUM
6. No Jira→Linear reverse map — LOW
7. Circular import risk — LOW
8. No automated sync daemon — HIGH

---

## SOURCE 13: Integration Test Plan (src/content-store/docs/testing/)

### Integration Test Plan — 7 next steps listed
1. Implement test framework setup
2. Create initial test scenarios
3. Set up CI/CD integration
4. Create test data management system
5. Implement performance testing infrastructure
6. Set up security testing tools
7. Configure HIPAA compliance validation

---

## SOURCE 14: GitHub Copilot Prompts (.github/prompts/)

### create-implementation-plan.prompt.md — Template/prompt, not a task list
### update-implementation-plan.prompt.md — Template/prompt, not a task list

---

## SOURCE 15: GitHub Plugin Agent Definitions (.github/plugins/)

### Agent planner definitions (not task-bearing, configuration)
- gem-planner.md
- task-planner.md (edge-ai-tasks)
- polyglot-test-planner.md
- task-planner.md (project-planning)
- implementation-plan.md
- plan.md
- planner.md
- terraform-azure-planning.md

---

## SOURCE 16: CI Operating Model RFC (docs/rfc/)

### CI-OPERATING-MODEL.md — APPROVED
- Future Considerations section lists 3 items:
  1. Upgrade ci.yml from SOFT to HARD gates — "Next sprint" — DevOps
  2. Establish weekly CI operations review — "Next sprint" — DevOps/AI Team
  3. Automate readiness aggregator as pre-deploy check — "Q3 2026" — DevOps

---

## SOURCE 17: Miscellaneous Discovered Files

### AI Training Docs (ai/docs/)
- PRD_PIX-499.md — PRD document, may contain implementation steps
- TEST_EXECUTION_REPORT.md — Test report, not a plan
- production_deployment_guide.md — Reference doc
- troubleshooting_guide.md — Reference doc
- user_onboarding_guide.md — Reference doc

### Foresight Deployment (foresight/DEPLOYMENT.md) — Reference doc

### Agent READMEs (agents/)
- supervisor-agent/README.md
- intake-agent/README.md
- pipeline-agent instructions
- advisor-agent instructions
- qa-agent instructions
- session-agent instructions

### Scripts
- scripts/training/KAGGLE_SETUP.md — Setup guide
- scripts/delta-analysis-framework.md — Framework doc

---

## END OF RAW LIST

Total unique task/plan sources discovered: 17 categories
Total individual work items identified: ~200+
Sources with explicit remaining/open work: Sources 2, 3, 4, 5, 6, 8, 9, 12, 13, 16