# Weekly Operating Review

**Cadence:** Monday 10:00 UTC  
**Duration:** 30 minutes  
**Owner:** Platform Engineering  
**Participants:** Platform on-call, Frontend lead, AI lead, Security lead  
**Source:** `docs/runbooks/ci-escalation.md`,
`docs/runbooks/service-level-objectives.md`

This runbook makes the weekly operational health review repeatable. Each week,
the facilitator copies the template below, fills in the evidence links, and
posts the completed review to the Linear coordination issue.

## Standing KPIs

| KPI                          | Target                       | Evidence source                               |
| ---------------------------- | ---------------------------- | --------------------------------------------- |
| Availability                 | Per SLO table                | Monitoring dashboard / Prometheus             |
| p95 latency                  | Per SLO table                | Monitoring dashboard / Prometheus             |
| Error budget                 | < 10% consumed               | SLO burn-rate query                           |
| Required CI/Quality          | Green on latest `staging`    | `gh-axi run list --branch staging --limit 20` |
| Security alerts              | No open high/critical        | Security scanning dashboard                   |
| Critical bias alerts         | Zero unresolved              | Bias audit dashboard                          |
| Open customer-impacting bugs | < 3                          | Linear bug query                              |
| Backlog health               | No stale high-priority items | Linear backlog query                          |

## Review Template

```md
# Week of YYYY-MM-DD — Operating Review

## Availability

| Service      | Target | Actual | Notes |
| ------------ | ------ | ------ | ----- |
| Therapy Chat | 99.95% |        |       |
| Auth         | 99.99% |        |       |
| REST API     | 99.9%  |        |       |
| AI Inference | 99.5%  |        |       |

## Latency

| Service      | p95 target | p95 actual | Notes |
| ------------ | ---------- | ---------- | ----- |
| Therapy Chat | < 2s       |            |       |
| Auth         | < 500ms    |            |       |
| REST API     | < 500ms    |            |       |
| AI Inference | < 5s       |            |       |

## Alerts and Incidents

- High/critical security alerts: [link]
- Critical bias alerts: [link]
- Incidents opened/closed this week: [link]
- Unresolved patient-impacting issues: [link]

## Pipeline Health

| Workflow          | Last run | Status | Evidence   |
| ----------------- | -------- | ------ | ---------- |
| CI                | [commit] |        | [run link] |
| Quality           | [commit] |        | [run link] |
| Security Scanning | [commit] |        | [run link] |
| Deploy to AWS EKS | [commit] |        | [run link] |
| Vercel            | [commit] |        | [run link] |

## Backlog

- New high-priority issues: [links]
- Stale high-priority issues: [links]
- Reopened issues this week: [links]
- Follow-ups carried over: [links]

## Decisions

1.

## Next Actions

| Action | Owner | Due |
| ------ | ----- | --- |
|        |       |     |
```

## Process Rules

- Fill every KPI cell before the meeting. Empty cells are not acceptable.
- Green checks without links are not evidence.
- Any red required workflow needs an owner, root-cause ticket, and next action
  before the review ends.
- If the error budget is below 10%, the review opens a reliability task and
  freezes non-emergency feature deployments until the next review.
- If any security or clinical-safety alert is open, it is reviewed first.
- The facilitator updates the linked Linear coordination issue immediately after
  the meeting.
