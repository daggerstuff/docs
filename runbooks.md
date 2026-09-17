# Operational Runbooks

Concise procedures for the failure modes this system actually has. Every
workflow referenced here lives in `.github/workflows/`.

## 1. EKS deployment failed / auto-rollback fired

**Detection:** `Deploy to AWS EKS` (workflow_run, triggered by CI success on
staging) fails; the "Roll back failed deployment" step reports a failed smoke
test. Rollback to the previous ReplicaSet is **automatic** — the runbook here
covers what happens after.

1. Confirm the rollback completed: the failing workflow run shows
   `Rollback complete.` (or the run failed during rollback — see step 3).
2. Identify the change: the deploy deploys the image digest built from the CI
   head that triggered it. Open the linked CI run to find the commit.
3. If rollback itself failed (a deployment is not healthy after
   `kubectl rollout undo`), manually verify cluster state:
   `kubectl rollout status deployment/<name> -n pixelated-empathy` for each of
   `pixelated-empathy-blue`, `session-agent`, `qa-agent`, `pipeline-agent`,
   then re-run `kubectl rollout undo` for anything still on the bad revision.
4. Re-run the deploy for staging only after the offending commit is fixed or
   reverted. Deploys are dispatchable manually (`workflow_dispatch`) but
   normally follow a green CI run.

## 2. Monitoring alert fired (Slack)

**Detection:** `Monitoring` (every 6h) routes CRITICAL/HIGH to Slack via
`scripts/ci/health-alerts.mjs`; CRITICAL pages `@here` and fails the run.
The routing table and per-surface ownership live in that script.

1. Open the alert's link to the failed Monitoring run to see which probe
   failed (the step log names the surface and severity).
2. For an app-level failure, check the EKS deployment health (runbook 1,
   step 3) and the Sentry project — error events carry build and release tags
   from `Build & Sentry Release`.
3. For an infrastructure failure (probe could not reach the service at all),
   check the Traefik ingress and NLB hostname:
   `kubectl get svc -n traefik traefik`, and confirm DNS still points at it.
4. Re-run the Monitoring workflow (`workflow_dispatch`) after remediation.

## 3. CI / Quality red on staging

1. Read the failed step first — most Quality failures are **baseline
   regressions** (complexity, duplication, file-size, tech-debt, naming,
   boundaries, version-drift) and the log names the exact offending package
   or file. Growth requires either a fix or a sanctioned re-pin:
   `pnpm lint:<audit> -- --update`.
2. `[ERR_PNPM_OUTDATED_LOCKFILE]` (frozen-lockfile mismatch) means the
   manifest and `pnpm-lock.yaml` diverged — typically a merged dependabot
   bump without its lockfile. Fix: `pnpm install --lockfile-only`, verify
   with `pnpm install --frozen-lockfile --dry-run`, commit the lockfile.
3. Version-drift failures list the new duplicate versions. If the growth is
   an intentional consequence of a merged dependency bump, re-pin the
   baseline (see step 1); otherwise consolidate via pnpm overrides.
4. `Error Insight` posts a digest for red runs; use it for triage, not as a
   substitute for reading the log.

## 4. Frontend deploy issue (Vercel)

1. Check the `Vercel (Frontend Test Center)` and `Build & Sentry Release`
   runs for the same commit — the deploy pipeline only ships after green CI,
   gated by the policies in `.github/workflows/vercel-policy.md`.
2. If the build is green but the site misbehaves, roll back in the Vercel
   dashboard to the previous deployment for the affected environment.
3. Sentry releases tag each deploy; use the release view to confirm which
   version is live.

## 5. Suspected flaky test

1. Note the test name and run link. Do not add retries — retries mask
   non-determinism, which the anti-suppression policy bans.
2. Reproduce locally, repeatedly, against the isolated pe test database
   (see CONTRIBUTING.md "pe test database" for the exact invocation).
3. If it reproduces: fix the root cause (usually shared state, time, or
   ordering dependence) before re-running the suite.
4. If it cannot be reproduced locally, re-run the exact workflow with
   `gh run rerun --failed <run-id>` and record the outcome on the linked
   PR or issue.
