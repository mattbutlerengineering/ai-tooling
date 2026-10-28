# Evaluation: diffinery

**Repo:** [codician-team/diffinery](https://github.com/codician-team/diffinery)
**Stars:** 61 | **Last updated:** 2026-10-26 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Ship
**Layer:** Infrastructure

---

## What it does

An open-source, agent-first GitHub and GitHub Actions alternative that runs on your own Cloudflare account — git hosting, pull requests, code review, and drop-in GitHub Actions YAML on Workers, Durable Objects, R2, and Containers.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and the CATALOG one-liner/overlaps. That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. No structural signal disposes it mechanically.

## Triage note

P3 backlog. Left at `discovery-log`; `gitai` (the nearest catalogued neighbor, also server-centric git) solves concurrent-write scaling rather than standing up a full self-hosted GitHub/Actions replacement, so the jobs only partially overlap. Worth a real look given how large a surface (git hosting + CI) it claims to cover; left for a future pass rather than dispositioned on a README skim.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [diffinery](https://github.com/codician-team/diffinery) | tool | Agent-first, self-hosted GitHub/Actions alternative on your own Cloudflare account (Apache-2.0) — git hosting, PRs, code review, Actions-YAML CI | Teams want an agent-first git-hosting/CI alternative to GitHub they control, without standing up their own infra from scratch | gitai, worktrunk, commit-commands |
