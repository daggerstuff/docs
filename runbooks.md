# Operational Runbooks

Concise procedures for the failure modes this system actually has. Every
workflow referenced here lives in `.github/workflows/`.

## 1. Image publish failed (Build and Publish Images)

**Detection:** `Build and Publish Images` (workflow_run, triggered by CI success
on staging) fails. Production is deployed off AWS: the workflow builds the
app image (`infra/Dockerfile`) and the agent images (`agents/Dockerfile`) and
pushes them to Docker Hub.

What to do:

1. Read the failing step in the run. The most common failure is a Docker Hub
   push rejected — check `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN` are valid.
2. If a build step fails, reproduce locally with the same `docker build`
   command the run prints (same `--build-arg AGENT_DIR` and Dockerfile) before
   pushing a fix.
3. Identify the change: the publish ships the image built from the CI head that
   triggered it. Open the linked CI run to find the commit.
4. Re-run the publish for staging only after the offending commit is fixed or
   reverted. Publishes are dispatchable manually (`workflow_dispatch`) but
   normally follow a green CI run.

Note: the former AWS EKS deployment (and its staged blue/green rollout and
auto-rollback) was removed when production moved off AWS. Serving-origin
rollbacks are handled via the Cloudflare Workers domain (section 4);
image-level rollbacks mean re-publishing the previous tag.

## 2. Monitoring alert fired (Slack)

**Detection:** `Monitoring` (every 6h) routes CRITICAL/HIGH to Slack via
`scripts/ci/health-alerts.mjs`; CRITICAL pages `@here` and fails the run. The
routing table and per-surface ownership live in that script.

1. Open the alert's link to the failed Monitoring run to see which probe failed
   (the step log names the surface and severity).
2. For an app-level failure, check the EKS deployment health (runbook 1, step 3)
   and the Sentry project — error events carry build and release tags from
   `Build & Sentry Release`.
3. For an infrastructure failure (probe could not reach the service at all),
   check the Traefik ingress and NLB hostname:
   `kubectl get svc -n traefik traefik`, and confirm DNS still points at it.
4. Re-run the Monitoring workflow (`workflow_dispatch`) after remediation.

## 3. CI / Quality red on staging

1. Read the failed step first — most Quality failures are **baseline
   regressions** (complexity, duplication, file-size, tech-debt, naming,
   boundaries, version-drift) and the log names the exact offending package or
   file. Growth requires either a fix or a sanctioned re-pin:
   `pnpm lint:<audit> -- --update`.
2. `[ERR_PNPM_OUTDATED_LOCKFILE]` (frozen-lockfile mismatch) means the manifest
   and `pnpm-lock.yaml` diverged — typically a merged dependabot bump without
   its lockfile. Fix: `pnpm install --lockfile-only`, verify with
   `pnpm install --frozen-lockfile --dry-run`, commit the lockfile.
3. Version-drift failures list the new duplicate versions. If the growth is an
   intentional consequence of a merged dependency bump, re-pin the baseline (see
   step 1); otherwise consolidate via pnpm overrides.
4. `Error Insight` posts a digest for red runs; use it for triage, not as a
   substitute for reading the log.

## 4. Serving-origin deploy issue (Cloudflare Workers)

1. Check the `Deploy to Cloudflare Workers` run for the commit — it only
   ships after green CI, and its job log shows the runtime-env sync, the
   `wrangler deploy`, and the workers.dev + production-domain smoke tests.
2. If the deploy is green but the site misbehaves, roll back by reverting the
   offending commit and letting the pipeline redeploy; the Workers zone route
   (wrangler.jsonc `routes`) keeps serving the latest green deploy.
3. To fail back to Vercel wholesale, follow "Failing back to Vercel" in
   `.github/workflows/vercel-policy.md` — the standby stays warm.
4. Sentry releases tag each deploy; use the release view to confirm which
   version is live.

## 5. Nightly accuracy gate is red

**Detection:** `Accuracy gate` (nightly ~03:50) fails. This workflow carries the
bias- and crisis-detection ML accuracy suites — a ~15-minute benchmark
deliberately excluded from the per-push advisory gate (same precedent as the
load/performance excludes), so a red run means an accuracy regression shipped in
the last 24 hours.

1. Download the run's `accuracy-test-log` artifact for the failed assertions and
   threshold deltas.
2. Identify the window: the commits merged since the previous green accuracy
   run. Accuracy regressions are usually a dataset/model-threshold change, not a
   code bug — check recent commits touching `tests/bias-detection`,
   `tests/crisis-detection`, and the crisis/bias engines under
   `apps/web/src/lib/ai/`.
3. Fix forward or revert; re-run the workflow (`workflow_dispatch`) to confirm
   green before closing out.

## 6. Suspected flaky test

1. Note the test name and run link. Do not add retries — retries mask
   non-determinism, which the anti-suppression policy bans.
2. Reproduce locally, repeatedly, against the isolated pe test database (see
   CONTRIBUTING.md "pe test database" for the exact invocation).
3. If it reproduces: fix the root cause (usually shared state, time, or ordering
   dependence) before re-running the suite.
4. If it cannot be reproduced locally, re-run the exact workflow with
   `gh run rerun --failed <run-id>` and record the outcome on the linked PR or
   issue.

## 7. ai strict-typing ratchet is red

The quality workflow's "ai submodule strict ratchet" job pins the strict-mypy
debt of the ai submodule's `research/` tree
(`scripts/ci/ai-strict-baseline.json`, enforced by
`scripts/ci/ai-strict-ratchet.mjs`).

1. Read the job log. Two failure classes:
   - `NEW <file> :: <code>` on an **existing** file, or `GREW` on an existing
     key — the debt increased. Fix the new errors (real typing repairs, no
     per-line ignores); never re-pin upward.
   - `New files with strict errors` — a newly added file arrived
     non-strict-clean. Fix it before it can be exempted; the exemption never
     expands to new code.
2. If errors were _removed_, bank the cleanup deliberately:
   `node scripts/ci/ai-strict-ratchet.mjs --update`, review the diff (counts
   must only shrink), and commit the baseline.
3. After deleting legacy files, run `--prune` to drop them from the baseline.
4. mypy runs dependency-light (`uv run --no-project --with mypy`,
   `--ignore-missing-imports`), so third-party imports resolve to `Any`.
   Reproduce locally with the exact same script — do not compare its numbers
   against a full-venv mypy run.

## 8. Submodule pin not fetchable ("not our ref")

Multiple workflows fail at "Init submodules" with
`pinned commit <sha> is NOT fetchable from github.com/daggerstuff/…`: the parent
gitlink points at a submodule commit that exists locally but was never pushed to
the GitHub mirror (usually a parallel session pushed the submodule to bitbucket
only).

1. Confirm the local submodule has the pinned commit: `git submodule status` and
   `git -C ai rev-parse HEAD` (or `docs`).
2. Fast-forward the mirror branch — never force-push:
   `git -C ai push origin HEAD:staging` (docs uses `master`). This is a mirror
   sync, not a history rewrite.
3. Rerun the failed workflows: `gh run rerun --failed <run-id>`.
4. Root habit to fix: every session that bumps a submodule gitlink must push the
   submodule commit to BOTH remotes before pushing the parent. The CI
   init-submodules.sh check cannot rescue a ref that exists nowhere.

## 9. pnpm-lock.yaml conflicts when merging a PR

**Never resolve lockfile conflict markers by hand.** The lockfile is a pure
function of the merged manifests, so the correct result is whatever pnpm
regenerates — hand-merging produces states CI rejects and eats the most time of
any conflict class.

1. While the merge is conflicted, run one command:

   `make lockfile-resolve`

   (or `scripts/devops/resolve-lockfile-conflict.sh --add`). It seeds the
   lockfile from the incoming side, regenerates it from the merged
   package.json + pnpm-workspace.yaml via `pnpm install --lockfile-only`, and
   stages the result. Then commit the merge as usual.

2. Prevention: merge `staging` into long-lived PR branches early and often —
   most of these conflicts are just two branches churning the same serialized
   dependency graph, and frequent merges keep the churn small.
3. If a lockfile is merely stale (not conflicted), do not hand-edit it either:
   `pnpm install --lockfile-only` re-syncs it.
