# Cloudflare Cutover Runbook

Operational checklist for moving the pixelatedempathy.com origin from Vercel to
Cloudflare Workers. The artifact build is verified (see "State" below); this
document covers credentials, secrets, first deploy, smoke test, and the
reversible DNS flip.

Vercel remains warm standby throughout: nothing here touches Vercel, and the
DNS flip is reversible in ~1 minute.

## 0. State (2026-11-02)

- Build verified green via the canonical path:
  `CI=true DEPLOY_TARGET=cloudflare pnpm build` → `dist/server` (entry2.mjs +
  generated wrangler.json) + `dist/client`.
- Generated worker config: `pixelated-empathy`, `main: entry2.mjs`,
  `kv_namespaces: [SESSION]`, `images: IMAGES`, `assets: ../client`,
  `nodejs_compat`, `no_bundle: true`, `upload_source_maps: true`.
- No deploy has ever happened (`wrangler whoami` = not logged in); live site
  still serves from Vercel (`x-vercel-id` present).
- CI: `.github/workflows/deploy-cloudflare.yml` added — build → artifact →
  `wrangler deploy` → smoke test on the workers.dev URL. Deploy job needs
  `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` GitHub secrets (not yet set).

## 1. Prerequisites (one-time)

1. Create a Cloudflare API token (dash → My Profile → API Tokens):
   - Account: Workers Scripts:Edit
   - Account: Workers KV Storage:Edit (first deploy auto-provisions SESSION KV)
   - Account: Cloudflare Images:Edit (IMAGES binding)
   - Zone: DNS:Edit (only needed later for the cutover step itself)
   - User: User Details:Read (wrangler membership check)
2. Add GitHub secrets: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`.
   (Local `.env` already has `CLOUDFLARE_ACCOUNT_ID`; the token is not stored
   anywhere in the repo.)
3. Verify locally: `pnpm exec wrangler whoami` shows the account.

## 2. First deploy (local or CI)

CI path (preferred once secrets exist): Actions → "Deploy to Cloudflare
Workers" → Run workflow (dispatch always allowed; auto-runs after green CI on
staging).

Local path:

```sh
export CLOUDFLARE_API_TOKEN=...   # not committed; set per-shell only
bash scripts/ci/build-cloudflare.sh
pnpm exec wrangler deploy --config dist/server/wrangler.json
```

First deploy auto-provisions the `SESSION` KV namespace and the `IMAGES`
binding. The workflow's smoke test then hits
`https://pixelated-empathy.<account>.workers.dev/` expecting HTTP 200.

## 3. Secrets on the Worker

`wrangler secret put` reads values from stdin — values are never committed,
echoed, or printed. Set these (names from the current Vercel production env
listing, names only):

Core runtime:

```sh
for KEY in MONGODB_URI MONGODB_DB_NAME DATABASE_URL REDIS_URL \
           UPSTASH_REDIS_REST_URL UPSTASH_REDIS_REST_TOKEN \
           JWT_SECRET JWT_EXPIRES_IN ENCRYPTION_KEY ENCRYPTION_ALGORITHM; do
  echo "Setting $KEY (paste value, Ctrl-D to finish):"
  pnpm exec wrangler secret put "$KEY"
done
```

Auth0 (server side):

```sh
for KEY in AUTH0_DOMAIN AUTH0_AUDIENCE AUTH0_CLIENT_ID AUTH0_CLIENT_SECRET \
           AUTH0_CALLBACK_URL AUTH0_MANAGEMENT_CLIENT_ID \
           AUTH0_MANAGEMENT_CLIENT_SECRET; do
  pnpm exec wrangler secret put "$KEY"
done
```

AI / inference keys actually read by Worker code:

```sh
for KEY in OPENAI_API_KEY OPENAI_BASE_URL ANTHROPIC_API_KEY \
           CLOUDFLARE_ACCOUNT_ID CLOUDFLARE_AI_API_KEY \
           RESEND_API_KEY SLACK_WEBHOOK_URL; do
  pnpm exec wrangler secret put "$KEY"
done
```

Sentry (server):

```sh
for KEY in SENTRY_DSN SENTRY_AUTH_TOKEN SENTRY_ORG SENTRY_PROJECT; do
  pnpm exec wrangler secret put "$KEY"
done
```

Non-secret vars already live in `wrangler.jsonc` `vars`
(`DEPLOY_TARGET`, `NODE_ENV`); do not duplicate them as secrets.

PUBLIC_* / VITE_* values are inlined at build time by Vite — they must be
present in the CI/build environment (they are already on Vercel; add to GitHub
secrets if the build starts failing on missing client vars):
`PUBLIC_AUTH0_CLIENT_ID`, `PUBLIC_AUTH0_DOMAIN`, `PUBLIC_SITE_URL`.

The complete Vercel production env name list is in
`runbooks/cloudflare-env-names.txt` (names only, generated 2026-11-02).
To sync all of them by hand in one sitting:

```sh
npx vercel env pull /tmp/vercel-env.mixed --environment production  # auth'd locally
# then for each name in that file: wrangler secret put "$NAME" < <(grep -E "^NAME=" ...)
# Delete the pulled file immediately afterwards; never commit it.
```

## 4. Smoke test before cutover

```sh
BASE=https://pixelated-empathy.<account>.workers.dev
curl -s -o /dev/null -w '%{http_code}\n' "$BASE/"            # 200
curl -s -o /dev/null -w '%{http_code}\n' "$BASE/api/health"  # 200
curl -sI "$BASE/" | grep -i '^content-type'                   # text/html
```

## 5. DNS cutover (needs explicit human go-ahead)

1. Note current DNS: apex + `www` → Vercel (cname.vercel-dns.com).
2. Point apex/`www` A/AAAA/CNAME records at the Worker (Workers Custom Domain
   in the Cloudflare dashboard binds `pixelatedempathy.com` + `www` to
   `pixelated-empathy`; the zone is already on Cloudflare DNS).
3. Verify: `curl -sI https://pixelatedempathy.com | head` — should show the
   Worker (no `x-vercel-id`).
4. Rollback: delete the custom domain binding + restore the Vercel DNS records
   (~1 minute). Vercel deploy stays intact and warm the whole time.

## 6. Explicitly not moving with this cutover

- Standalone `ws://` TCP socket servers (`BiasWebSocketServer`,
  `TrainingWebSocketServer`, `apps/web/src/server.ts`) — need Durable Objects
  (separate follow-up).
- EKS-only Express `server.prod.ts` and the Python services — separate track,
  unchanged.

## 7. Post-cutover

- Keep Vercel project + `vercel.yml` pipeline as standby for at least a week.
- Watch Workers observability (wrangler tail / dash) for runtime errors during
  the first hours.
