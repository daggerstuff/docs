# EVE_AUTH Credential Rotation Runbook

**Scope:** the HTTP Basic credential shared by the `agents/` fleet (eve
channels and supervisor subagents). This runbook records a confirmed
credential exposure, the code fix that closed the source-side leak, and the
rotation that retired the exposed value.

**Status:** code fix landed and **rotation completed 2026-11-04**. The exposed
value is retired everywhere it was under our control; it remains readable in
public git history, which rotation cannot undo.

**Related docs:**

- Fleet auth helper: `agents/lib/channels/eve.ts`
- Secret manifest template: `agents/k8s/namespace-secrets.yaml`
- Systemd install: `agents/deploy/systemd/install.sh`
- Deploy escalation: `docs/runbooks/ci-escalation.md`

## 1. What happened

A default password was hardcoded as an environment-variable fallback in seven
supervisor subagent files:

```
agents/supervisor-agent/agent/subagents/advisor.ts
agents/supervisor-agent/agent/subagents/content.ts
agents/supervisor-agent/agent/subagents/eve_agent.ts
agents/supervisor-agent/agent/subagents/intake.ts
agents/supervisor-agent/agent/subagents/pipeline.ts
agents/supervisor-agent/agent/subagents/qa.ts
agents/supervisor-agent/agent/subagents/session.ts
```

Introduced in `92852f528` (2026-10-12) and pushed to `origin/staging`. The
hosting repository is **public**, so the literal is permanently readable in
that commit regardless of any later fix.

The pattern was `process.env.EVE_AUTH_PASSWORD ?? '<literal>'`, with a matching
`?? 'admin'` default for the username. Any deployment that failed to inject
`EVE_AUTH_*` would silently authenticate with the committed default instead of
failing.

## 2. Source-side fix

Commit `2201ec0a6` (2026-11-04) replaced the fallback with a fail-closed
expression in all seven files:

```ts
auth: process.env.VERCEL
  ? vercelOidc()
  : authUsername && authPassword
    ? httpBasic({ username: authUsername, password: authPassword })
    : undefined
```

Verified behaviour:

| Environment          | Result                                     |
| -------------------- | ------------------------------------------ |
| neither variable set | `auth` is `undefined` → remote answers 401 |
| both set             | `httpBasic` built from the env values      |
| username only        | `auth` is `undefined`                      |
| `VERCEL=1`           | `vercelOidc()`                             |

`eve build` succeeds with the new expression, the supervisor suite passes
(8 files, 35 tests), and no source file contains the literal any more.

`EVE_AUTH_*` is documented in `.env.example` under "AGENT FLEET".

## 3. Rotation record (2026-11-04)

| Location                             | Before                              | After                                |
| ------------------------------------ | ----------------------------------- | ------------------------------------ |
| Local `.env` line 365                | exposed literal                     | new 32-char CSPRNG value             |
| GitHub secret `EVE_AUTH_PASSWORD`    | created 2026-08-30, exposed literal | rewritten 2026-11-04T06:41:58Z       |
| Public git history                   | `92852f528`                         | **unchanged** — cannot be undisclosed |
| EKS secret `eve-auth`                | last written 2026-10-21             | retired with the cluster (see §5)    |

No live deployment consumed the old value at rotation time, so the swap carried
no availability risk.

The replacement was generated with `openssl rand -base64 32` and is not derived
from the old value.

## 4. Where the credential is consumed now

There is no CI or cluster consumer. `deploy-aws.yml` — which previously
recreated the `eve-auth` secret from GitHub secrets on every deploy — was
deleted in `bf6504d5a` (2026-11-04). No workflow references `EVE_AUTH_*`.

Remaining consumers are operator-side:

| Consumer                            | How it reads the value                              |
| ----------------------------------- | --------------------------------------------------- |
| `tools/px` (`invoke.ts`, `agents.ts`) | `process.env.EVE_AUTH_*`, typically from local `.env` |
| `agents/*/agent/channels/eve.ts`    | env, fail-closed when unset                          |
| `agents/deploy/systemd/install.sh`  | templates `/opt/pixelated/agents.env` on install      |

Because the fleet is not currently deployed anywhere, there is no running
process to restart. The value matters again the moment the fleet is
re-provisioned — at which point the systemd or container env file must carry
the current value from `.env`.

## 5. The EKS deployment is retired

Commit `bf6504d5a` removed the AWS EKS path entirely: `deploy-aws.yml`,
`aws-diagnose.yml`, `aws-provision.yml`, `aws-iam-probe.yml`,
`chaos-validation.yml`, `promotion-gate-test.yml`, all eight
`agents/*/k8s/deployment.yaml` manifests, `infra/aws/`, and `infra/k8s/aws/`.

Consequently:

- The `eve-auth` Kubernetes secret no longer exists as a provisioning target.
  Whatever copy lived in the old cluster died with it.
- The earlier failure mode of that pipeline (OIDC `sts:AssumeRoleWithWebIdentity`
  denied, plus missing `AWS_REGION` / `EKS_CLUSTER_NAME` / `REDIS_PASSWORD`
  secrets) is moot — the workflow that needed them is gone.
- `AWS_DEPLOY_ROLE_ARN` remains in the GitHub secret store as an orphan. It can
  be deleted when convenient; nothing reads it.

Production is Vercel for the web surface and Cloudflare Workers as the
migration target. The agent fleet has no production home until one is chosen.

## 6. Re-rotating later

If the fleet is re-provisioned, or if this credential is ever suspected again:

### Step 1 — generate

```bash
NEW_PASSWORD="$(openssl rand -base64 32 | tr -d '\n/+=' | cut -c1-32)"
```

### Step 2 — update the GitHub secret

```bash
printf '%s' "$NEW_PASSWORD" | gh secret set EVE_AUTH_PASSWORD \
  -R daggerstuff/pixelated
```

### Step 3 — update the local `.env`

```bash
python3 - "$NEW_PASSWORD" <<'PY'
import pathlib, sys
new = sys.argv[1]
path = pathlib.Path('.env')
lines = path.read_text().splitlines(keepends=True)
for i, line in enumerate(lines):
    if line.startswith('EVE_AUTH_PASSWORD='):
        lines[i] = f'EVE_AUTH_PASSWORD={new}\n'
        break
else:
    raise SystemExit('EVE_AUTH_PASSWORD not found in .env')
path.write_text(''.join(lines))
PY
```

### Step 4 — update wherever the fleet actually runs

With no cluster, that means the target host's env file:

- systemd: `/opt/pixelated/agents.env`
- containers: `agents/deploy/docker-compose.yaml` reads `.env.agents`

Both must carry the same value as `.env` before the fleet starts, because the
code now fails closed rather than falling back to a default.

### Step 5 — verify

A stale env file shows up as 401s, not as a crash, so check explicitly:

```bash
# operator side
px agents list

# fleet side, on the host
grep -c '^EVE_AUTH_PASSWORD=' /opt/pixelated/agents.env
```

## 7. Should history be rewritten?

No. The repository is public and the commit has been reachable since
2026-10-12, so the value must be treated as already disclosed. A history rewrite
would require force-pushing a shared branch, break every existing clone and
fork, and would not un-disclose anything. The rotation in §3 is the remedy.

If policy requires a rewrite anyway, that is a separate, coordinated operation —
not part of this runbook.

## 8. Verification checklist

- [x] New password generated from a CSPRNG, not derived from the old value
- [x] `gh secret set EVE_AUTH_PASSWORD` completed and listed
- [x] `.env` line 365 updated
- [x] No source file contains the exposed literal
- [x] No CI workflow references `EVE_AUTH_*`
- [x] Confirmed no live deployment was consuming the old value
- [ ] Delete the orphaned `AWS_DEPLOY_ROLE_ARN` secret (optional cleanup)
- [ ] Re-verify once the fleet is re-provisioned
