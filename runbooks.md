# Operational Runbooks

Concise procedures for the failure modes this system actually has. Every
workflow referenced here lives in `.github/workflows/`.

## 1. EKS deployment failed / auto-rollback fired

**Detection:** `Deploy to AWS EKS` (workflow_run, triggered by CI success on
staging) fails. The app deploys in stages (blue/green):

1. The new image is rolled out on the **idle slot** (the deployment the
   service selector is not pointing at) and must pass a pre-live `/health`
   smoke — a failure here has zero user impact.
2. The service selector is flipped to the staged slot, then a second smoke
   runs through the service. On failure the selector flips **back**
   automatically (seconds) and the agent deployments roll back.

What to do after an automatic rollback:

1. Confirm the rollback in the failing run: "Service selector flipped" /
   "Rollback complete." log lines, and that the service selector points at
   the previous slot:
   `kubectl get svc pixelated-empathy -n pixelated-empathy -o jsonpath='{.spec.selector.slot}'`
2. Identify the change: the deploy ships the image digest built from the CI
   head that triggered it. Open the linked CI run to find the commit.
3. If the flip-back itself failed, manually restore the selector to the
   previous slot with `kubectl patch svc pixelated-empathy -n pixelated-empathy
--type merge -p '{"spec":{"selector":{"app":"pixelated-empathy","slot":"<prev>"}}}'`
   and verify with the same jsonpath above, then roll back the agent
   deployments (`kubectl rollout undo deployment/<agent> -n pixelated-empathy`)
   if the run died between their rollout and the app flip.
4. Re-run the deploy for staging only after the offending commit is fixed or
   reverted. Deploys are dispatchable manually (`workflow_dispatch`) but
   normally follow a green CI run.

Note: percentage-based canary (traffic split between slots) is NOT enabled —
Traefik's weighted routing needs the CRD provider, which is not turned on.
Rollout is staged, not fraction-split.

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

## 5. Nightly accuracy gate is red

**Detection:** `Accuracy gate` (nightly ~03:50) fails. This workflow carries
the bias- and crisis-detection ML accuracy suites — a ~15-minute benchmark
deliberately excluded from the per-push advisory gate (same precedent as the
load/performance excludes), so a red run means an accuracy regression shipped
in the last 24 hours.

1. Download the run's `accuracy-test-log` artifact for the failed assertions
   and threshold deltas.
2. Identify the window: the commits merged since the previous green accuracy
   run. Accuracy regressions are usually a dataset/model-threshold change,
   not a code bug — check recent commits touching `tests/bias-detection`,
   `tests/crisis-detection`, and the crisis/bias engines under
   `apps/web/src/lib/ai/`.
3. Fix forward or revert; re-run the workflow (`workflow_dispatch`) to
   confirm green before closing out.

## 6. Suspected flaky test

1. Note the test name and run link. Do not add retries — retries mask
   non-determinism, which the anti-suppression policy bans.
2. Reproduce locally, repeatedly, against the isolated pe test database
   (see CONTRIBUTING.md "pe test database" for the exact invocation).
3. If it reproduces: fix the root cause (usually shared state, time, or
   ordering dependence) before re-running the suite.
4. If it cannot be reproduced locally, re-run the exact workflow with
   `gh run rerun --failed <run-id>` and record the outcome on the linked
   PR or issue.

## 7. ai strict-typing ratchet is red

The quality workflow's "ai submodule strict ratchet" job pins the
strict-mypy debt of the ai submodule's `research/` tree
(`scripts/ci/ai-strict-baseline.json`, enforced by
`scripts/ci/ai-strict-ratchet.mjs`).

1. Read the job log. Two failure classes:
   - `NEW <file> :: <code>` on an **existing** file, or `GREW` on an
     existing key — the debt increased. Fix the new errors (real
     typing repairs, no per-line ignores); never re-pin upward.
   - `New files with strict errors` — a newly added file arrived
     non-strict-clean. Fix it before it can be exempted; the
     exemption never expands to new code.
2. If errors were _removed_, bank the cleanup deliberately:
   `node scripts/ci/ai-strict-ratchet.mjs --update`, review the
   diff (counts must only shrink), and commit the baseline.
3. After deleting legacy files, run `--prune` to drop them from the
   baseline.
4. mypy runs dependency-light (`uv run --no-project --with mypy`,
   `--ignore-missing-imports`), so third-party imports resolve to
   `Any`. Reproduce locally with the exact same script — do not
   compare its numbers against a full-venv mypy run.
