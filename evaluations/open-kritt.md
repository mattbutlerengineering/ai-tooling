# Evaluation: open-kritt

**Repo:** [Kritt-ai/open-kritt](https://github.com/Kritt-ai/open-kritt)
**Stars:** 2,300 | **Last updated:** 2026-09-15 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-10-17
**Last triaged:** 2026-10-17  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

Self-hosted security and vulnerability research platform (docker-compose deployment with
backend, frontend, and database services) that orchestrates AI agents across Claude Code/Codex,
breaking research into small parallel tasks and combining output into de-duplicated, ranked
findings.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the repo's
README and LICENSE file. That is sufficient for the verdict below, because the verdict turns on
license terms for a self-hosted service, not on the tool's finding quality.

## Verdict

**SKIP** — AGPL-3.0. This repo is not a CLI you merely invoke per-call; it's a self-hosted
multi-service platform (engine, backend, frontend, database, deployed via docker-compose) you
run as infrastructure, which is exactly the shape AGPL-3.0's network-use provisions are written
for. That — plus this catalog's bar of permissive, MIT-like OSS — makes it not adoptable as
written, regardless of how capable the vulnerability-research methodology is. `openhack`
(MIT) already covers the same job for a similar class of agent-driven vulnerability research.

## Triage note

New lead, added today, same scan as `openhack`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [open-kritt](https://github.com/Kritt-ai/open-kritt) | tool | Self-hosted platform (⚠️ AGPL-3.0) orchestrating AI agents across Claude Code/Codex to find vulnerabilities — parallel focused tasks, de-duplicated and ranked findings | Pointing a model at a whole repo for vuln-finding produces noisy, unranked results; want focused parallel tasks with validation | openhack, pentest-ai, strix |  |
