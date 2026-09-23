# Evaluation: briefd

**Repo:** [ismailperim/briefd](https://github.com/ismailperim/briefd)
**Stars:** 29 | **Last updated:** 2026-09-23 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

A self-hosted context compiler (Go, Apache-2.0) — serves git-backed team knowledge to coding agents
as token-budgeted bundles over MCP, so agents get briefed without their whole context window flooding
with docs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the git-backed knowledge/token-budgeted bundle model. That is sufficient
to catalog it and place it relative to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog. Overlaps `opencontext`/`mex`/`delx-memory` on "persistent project context over MCP", but
its specific angle — compiling *team* (multi-author, git-backed) knowledge into token-budgeted
bundles, rather than a single agent's session memory — is different enough from any one incumbent to
leave for a hands-on look rather than mechanically SKIP as redundant.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [briefd](https://github.com/ismailperim/briefd) | MCP server | Self-hosted context compiler (Apache-2.0, Go) — serves git-backed team knowledge to coding agents as token-budgeted bundles over MCP | Team knowledge for coding agents is either missing or floods context unbudgeted; want git-backed knowledge served as right-sized bundles | opencontext, mex, delx-memory |  |
