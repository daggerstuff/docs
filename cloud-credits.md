# Cloud Credits Tracker

Single source of truth for every startup-credit account. Update on every
application, approval, spend alert, and renewal. Research details live in
`.agent/internal/startup-credits/`.

## Accounts

| Provider | Tier applied | Owner email | Billing acct ID | Status | Credit amount | Granted | Expires | Notes |
|----------|--------------|-------------|-----------------|--------|---------------|---------|---------|-------|
| AWS Activate | Founders | info@pixelatedempathy.com | — | not applied | $1k–$5k | — | 1–2y from grant | Needs paid-plan acct; see 01-aws-activate.md |
| Google Cloud | Start | info@pixelatedempathy.com | — | not applied | $2k | — | 1y | Billing acct ID required; see 02 |
| Microsoft | Self-serve | TBD (fresh MS acct) | — | not applied | $200 → $4.8k | — | 90d/180d legs | Legal name must match docs; see 03 |
| OVHcloud | Start | info@pixelatedempathy.com | — | not applied | €10k | — | 12mo | POC/MVP statement; see 06 |
| DigitalOcean | Startups | info@pixelatedempathy.com | — | not applied | up to $100k | — | 12mo | Verify form live first; see 05 |
| NVIDIA Inception | — | info@pixelatedempathy.com | — | not applied | partner-gated | — | varies | Free; unlocks partner status |
| Cloudflare | Bootstrapped | info@pixelatedempathy.com | — | not applied | $10k | — | 1y | Strong fit (Workers prod) |
| Oracle | Growth Engine | TBD post-incorp | — | blocked: incorporation | $5k–$100k | — | 3–12mo | Needs entity + customers |

## Pre-apply checklist (every provider)

- [ ] Domain email owns/administers the billing account
- [ ] pixelatedempathy.com live, product + team pages, no placeholders
- [ ] Crunchbase founding date + stage identical on every form
- [ ] Founder LinkedIn profiles + company page live
- [ ] Incorporation docs ready (where required — currently pending)
- [ ] Billing alerts + spend caps set day one (see below)

## Spend-guard runbook (day one per account)

1. Set $0 / 50% / 80% / 100% budget alerts to info@pixelatedempathy.com.
2. Cap monthly draw where the provider allows fixed caps (DO fixed monthly cap).
3. Note exclusions: AWS excludes Marketplace/Route53 domains/Managed Services;
   GCP excludes 3P Marketplace/Model Garden. Bill those to a separate card.
4. Calendar reminder 30 days before each expiry — credits do not extend.
5. One owner per account; record account + expiry here immediately on grant.

## Blocked until incorporation

Microsoft (legal name/address), Oracle, NVIDIA, Vultr — entity name, state,
EIN, address, bank required.
