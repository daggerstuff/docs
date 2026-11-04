# EVE_AUTH Credential Rotation Runbook

**Scope:** the HTTP Basic credential shared by the `agents/` fleet (eve
channels and supervisor subagents). This runbook records a confirmed
credential exposure, the code fix that closed the source-side leak, and the
steps to retire the exposed value at every place it still lives.

**Status:** code fix landed. **Rotation not performed.** The exposed value is
still active.

**Related docs:**

- Fleet deploy wiring: `.github/workflows/deploy-aws.yml`
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

## 2. What is fixed

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

| Environment                        | Result                                   |
| ---------------------------------- | ---------------------------------------- |
| neither variable set               | `auth` is `undefined` → remote answers 401 |
| both set                           | `httpBasic` built from the env values    |
| username only                      | `auth` is `undefined`                    |
| `VERCEL=1`                         | `vercelOidc()`                           |

`eve build` succeeds with the new expression, the supervisor suite passes
(8 files, 35 tests), and no source file contains the literal any more.

`EVE_AUTH_*` is documented in `.env.example` under "AGENT FLEET".

## 3. What is still exposed

The code fix does not retire the value. Four copies remain:

| Location                                  | Evidence                                                    |
| ----------------------------------------- | ----------------------------------------------------------- |
| Public git history                        | `92852f528` on `origin/staging`                             |
| Local `.env` line 365                     | verified byte-identical to the exposed literal              |
| GitHub secret `EVE_AUTH_PASSWORD`         | created 2026-08-30T02:28:56Z, never rotated                 |
| EKS secret `eve-auth` in `pixelated-empathy` | last written by deploy run `39525923658` on 2026-10-21    |

The cluster copy is the one that matters: it is what the running fleet
authenticates with.

## 4. How the secret is provisioned

All fleet agents read one secret via `secretKeyRef`:

```yaml
- name: EVE_AUTH_PASSWORD
  valueFrom:
    secretKeyRef:
      name: eve-auth
      key: password
```

`deploy-aws.yml` recreates that secret from GitHub secrets on every deploy:

```bash
kubectl create secret generic eve-auth \
  --from-literal=username="${EVE_AUTH_USERNAME:-}" \
  --from-literal=password="${EVE_AUTH_PASSWORD:-}" \
  --namespace pixelated-empathy \
  --dry-run=client -o yaml | kubectl apply -f -
```

Because there is a single source and a single secret, rotation is atomic from
the fleet's perspective: all pods read the same key, so they cannot end up
disagreeing about the password.

`EVE_AUTH_USERNAME` / `EVE_AUTH_PASSWORD` are also consumed by
`tools/px` (`invoke.ts`, `agents.ts`), so a local `.env` update is required for
operator commands to keep working.

## 5. Rotation procedure

Run in this order. Steps 1-3 are independent of cluster access; step 4 needs a
working deploy.

### Step 1 — generate the replacement

```bash
NEW_PASSWORD="$(openssl rand -base64 24 | tr -d '\n/+=' | cut -c1-32)"
```

Do not reuse the exposed literal and do not derive it from it.

### Step 2 — update the GitHub secret

This is the source of truth for every deploy path that exists.

```bash
printf '%s' "$NEW_PASSWORD" | gh secret set EVE_AUTH_PASSWORD \
  -R daggerstuff/pixelated
```

Confirm it registered without printing the value:

```bash
gh secret list -R daggerstuff/pixelated | grep EVE_AUTH_PASSWORD
```

### Step 3 — update the local `.env`

`.env` is gitignored; keep it in step with the GitHub secret so operator
commands do not 401.

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

### Step 4 — push the new value to the cluster

This requires `deploy-aws.yml` to run successfully. It currently cannot; see
section 6. Once the deploy is repaired, trigger it and confirm the secret was
rewritten:

```bash
gh workflow run deploy-aws.yml -R daggerstuff/pixelated --ref staging
gh run watch -R daggerstuff/pixelated

kubectl get secret eve-auth -n pixelated-empathy \
  -o jsonpath='{.metadata.managedFields[0].time}'
```

The timestamp must be newer than the rotation. Pods pick up the new value on
their next restart; roll them explicitly if the deploy does not:

```bash
kubectl rollout restart deployment -n pixelated-empathy -l app.kubernetes.io/part-of=pixelated-agents
```

### Step 5 — verify the fleet still authenticates

A stale `.env` or a half-rotated secret shows up as 401s, not as a crash, so
verify explicitly:

```bash
# fleet-side: env inside a running pod must match the new value
kubectl exec -n pixelated-empathy deploy/supervisor-agent -- \
  printenv EVE_AUTH_PASSWORD | wc -c

# operator-side: px commands must succeed against the fleet
px agents list
```

### Step 6 — retire the exposed username if it was also the default

`EVE_AUTH_USERNAME` defaulted to `admin`. `admin` is not a secret in the same
sense, but if the fleet is reachable from an untrusted network, rotate it too
and update the same three locations.

## 6. Blocker: the EKS deploy is broken

Step 4 cannot be completed today. `deploy-aws.yml` has failed on every run
since 2026-10-21, always at the credentials step:

```
Configure AWS credentials
Assuming role with OIDC
Retry AssumeRole: attempt 1 of 12 failed:
  Could not assume role with OIDC:
  Not authorized to perform sts:AssumeRoleWithWebIdentity.
```

Last successful run: `39525923658`, 2026-10-21T01:12:11Z — which is also the
last time the `eve-auth` secret was written. The five most recent runs all fail
the same way.

Two separate defects:

1. **The OIDC trust relationship is gone.** The repo's `sts:AssumeRoleWithWebIdentity`
   call is denied, so `AWS_DEPLOY_ROLE_ARN` cannot be assumed. Re-establish the
   GitHub OIDC provider and role trust policy for `daggerstuff/pixelated`.
2. **Three referenced secrets do not exist.** `deploy-aws.yml` reads
   `AWS_REGION`, `EKS_CLUSTER_NAME`, and `REDIS_PASSWORD`, but none are present
   in the repository secret list. Even with the trust policy fixed, the deploy
   will not resolve a target cluster.

Until both are fixed the running fleet keeps the exposed password. That is the
reason rotation is incomplete rather than done.

## 7. Should history be rewritten?

No. The repository is public and the commit has been reachable since
2026-10-12, so the value must be treated as already disclosed. A history rewrite
would require force-pushing a shared branch, break every existing clone and
fork, and would not un-disclose anything. Rotate the value and move on.

If policy requires it anyway, that is a separate, coordinated operation — not
part of this runbook.

## 8. Verification checklist

- [ ] New password generated from a CSPRNG, not derived from the old value
- [ ] `gh secret set EVE_AUTH_PASSWORD` completed and listed
- [ ] `.env` line 365 updated
- [ ] `deploy-aws.yml` OIDC trust repaired
- [ ] `AWS_REGION`, `EKS_CLUSTER_NAME`, `REDIS_PASSWORD` secrets created
- [ ] Deploy run succeeds end to end
- [ ] `eve-auth` secret timestamp is newer than the rotation
- [ ] Pods restarted and carrying the new value
- [ ] `px agents list` authenticates against the fleet
- [ ] No 401s in fleet logs after rollout
