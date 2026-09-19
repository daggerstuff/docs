# CI Escalation Runbook

**Scope:** GitHub Actions checks for the Pixelated Empathy monorepo. This runbook
is the operational companion to the branch policy and the SLA breach response
runbook. It answers three questions after a red check: where does the check
live, who owns the failure, and what do I fix first?

**Related docs:**

- Branch and path policy: `.github/branch-pipeline.md`
- Vercel policy: `.github/workflows/vercel-policy.md`
- Shared workflow conventions: `.github/workflows/_shared-conventions.md`
- Incident/SLA escalation: `docs/reference/enterprise/runbooks/sla-breach-response.md`

## Operating Model

- `staging` is the primary integration and preview branch. `main` is production.
- Feature and agent branches do not deploy. Use a PR to `staging` for previews.
- EKS is the production runtime; Vercel is a frontend test center, path-filtered.
- A failing required check blocks merge. Do not rerun a red check without reading
  the failed step.

## Check Matrix

| Check                      | Workflow                                                                          | Primary owner       | First diagnostic step                                                                              |
| -------------------------- | --------------------------------------------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------- |
| Commit CI                  | `ci.yml`                                                                          | Platform            | Inspect the failed `build-test` job; formatting/lint/import errors are fixed at the source.        |
| Code quality               | `quality.yml`                                                                     | Platform            | Identify the ratchet or audit job (boundaries, duplication, complexity, strict types, N+1, tests). |
| Frontend UI tests          | `playwright.yml`, `browser-tests.yml`                                             | Frontend            | Read the failing spec; rerun locally with the same project/spec.                                   |
| Frontend performance       | `lighthouse.yml`, `bundle-size.yml`                                               | Frontend            | Compare budgeted artifact size or Lighthouse category with the pinned baseline.                    |
| Python correctness         | `quality.yml` (mypy/Ruff) + `python-typecheck.sh`                                 | Platform            | Run `uv run ruff check scripts tools` and `bash scripts/ci/python-typecheck.sh`.                   |
| AI submodule strict types  | `quality.yml`                                                                     | AI                  | Run `node scripts/ci/ai-strict-ratchet.mjs`; fix new files or grown error keys in the submodule.   |
| AI/training pipeline       | `training-pipeline.yml`, `ai-validation.yml`                                      | AI                  | Verify dataset gates and fixture paths; do not change gates without an AI owner.                   |
| Security scanning          | `security.yml`, `security-deep.yml`, `security-scanning.yml`                      | Security            | Triage findings by rule/asset; never merge with unexplained high/critical findings.                |
| AWS/EKS deploy             | `deploy-aws.yml`                                                                  | Platform            | Check image build, then rollout/logs; use `aws-diagnose.yml` for deeper diagnostics.               |
| Vercel frontend deploy     | `vercel.yml`                                                                      | Frontend            | Confirm the changed paths are frontend-relevant; check build logs before rerunning.                |
| Release/package generation | `sdk-generation.yml`, `release*.yml`, `sentry-build.yml`                          | Platform            | Verify version/secret inputs; keep release automation changes behind review.                       |
| Scheduled hygiene          | `accuracy-gate.yml`, `flaky-detection.yml`, `stale.yml`, `bias-audit-monthly.yml` | Platform/AI         | Treat repeated scheduled failures as product/platform debt, not flaky CI.                          |
| Monitoring/compliance      | `monitoring.yml`, `baa-compliance-gate.yml`, `consent-expiry-check.yml`           | Platform/Compliance | Check alert destination and health metric before investigating app logs.                           |

## Break/Fix Process

1. **Classify** the failure: build, test, static audit, deploy, or runtime.
2. **Read the exact failed step** before rerunning. A green rerun without a
   identified root cause is not a fix.
3. **Reproduce locally** with the smallest equivalent command:
   - formatting/lint: `pnpm lint`
   - strict AI types: `node scripts/ci/ai-strict-ratchet.mjs`
   - Python strict types: `bash scripts/ci/python-typecheck.sh`
   - tests: `pnpm vitest run -c config/vitest.config.ts`
   - Python tests: `uv run pytest`
4. **Fix the source**, not the gate. No suppression comments or config downgrades.
5. **Verify** the same command locally, then push a focused commit.
6. **Close the Linear/GitHub issue only after** the responsible workflow is green
   on the new `staging` commit, or a named owner has accepted a documented
   follow-up.

## Escalation Path

1. First responder: the owner in the matrix above.
2. Escalate after 30 minutes without a diagnosis, or immediately for:
   - `staging` or `main` is red on a required check,
   - security scanning reports a high/critical finding,
   - EKS/Vercel deploy is down or repeatedly failing,
   - patient-impacting functionality is failing in production.
3. Next escalation: Platform on-call, then the functional lead (AI, Frontend,
   Security, or Docs). Use the SLA breach response runbook for severities and
   timelines.
4. Record the incident in Linear with the failing run URL, commit, failed step,
   root cause, and fix PR. Do not leave an unresolved red run without a linked
   ticket.

## Useful Links

- Run list: `gh-axi run list --branch staging --limit 20`
- Failed log for a run: `gh-axi run view <run-id> --log-failed`
- Rerun failed jobs: `gh-axi run rerun <run-id> --failed`
- Workflow list: `.github/workflows/`
