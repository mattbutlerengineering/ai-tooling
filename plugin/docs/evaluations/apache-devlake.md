# Evaluation: Apache DevLake

**Repo:** [apache/incubator-devlake](https://github.com/apache/incubator-devlake)
**Stars:** 3,039 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Dev loop stage:** Outer loop (Retrospect)
**Layer:** Infrastructure

---

## What it does

Open-source dev data platform that ingests data from DevOps tools (GitHub, Jira, Jenkins, GitLab, etc.) and generates DORA metrics dashboards: lead time for changes, deployment frequency, MTTR, and change failure rate. Built on MySQL with Grafana for visualization.

## How we tested it

Deployed DevLake locally via Docker Compose. Connected to a GitHub repo with 6 months of PR and commit history. Generated DORA dashboards via the built-in Grafana integration.

```
docker compose -f docker-compose.yml up -d
# config-ui at localhost:4000 — added GitHub connection with PAT
# Grafana at localhost:3002 — pre-built DORA dashboard
```

## What worked

- DORA metrics generated automatically once the GitHub connection synced: lead time for changes (PR open to merge), deployment frequency (releases/week), change failure rate (% of deploys causing incidents)
- Pre-built Grafana dashboards are well-designed — trends over time are immediately visible
- Supports 30+ data source plugins (GitHub, GitLab, Jira, Jenkins, BitBucket, PagerDuty)
- Apache governance means long-term maintenance is likely

## What didn't work or surprised us

- Heavy setup: pulls 4 containers (DevLake API, MySQL, Grafana, config-ui). Takes ~10 minutes to get running and ~15 minutes for initial data sync on a modest repo
- Resource cost: ~2GB RAM for the container set. Overkill for a laptop side project
- MTTR metric requires incident tracking integration (PagerDuty, Opsgenie) — not derivable from GitHub alone
- Value for solo dev is limited: DORA metrics are designed for team workflows. A solo dev already knows their lead time is "however long the coding session takes"
- Needs periodic re-sync and schema migrations on version updates

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Observability tool — doesn't affect code quality directly |
| Speed | + | Reveals lead time bottlenecks and deployment frequency trends |
| Maintainability | neutral | No direct effect on code structure |
| Safety | + | Change failure rate tracking surfaces risky deploy patterns |
| Cost Efficiency | - | Infrastructure overhead (4 containers, 2GB RAM) for metrics |

## Verdict

**DEFER**

Promising for teams but premature for solo AI-assisted development. The infrastructure overhead (Docker Compose, 4 containers, 2GB RAM) isn't justified until you have a team generating enough data points for DORA trends to be meaningful. A solo developer gets more value from `git log --shortstat` and session cost tracking. Re-evaluate when working in a team context or when managing multiple repos with CI/CD pipelines.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Apache DevLake](https://github.com/apache/incubator-devlake) | platform | DORA metrics and engineering analytics from DevOps tool data | No visibility into delivery performance trends (lead time, deploy frequency, MTTR) | langfuse (observability), LinearB |
