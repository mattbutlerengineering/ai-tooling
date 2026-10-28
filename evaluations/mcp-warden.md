# Evaluation: mcp-warden

**Repo:** [ermoluk/mcp-warden](https://github.com/ermoluk/mcp-warden)
**Stars:** 7 | **Last updated:** 2026-10-27 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

A local-first credential broker for MCP (Rust): AI coding agents call APIs, SSH, and databases through scoped presets, while secrets stay in the OS keychain and never enter the agent's context.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and the CATALOG one-liner/overlaps. That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. No structural signal (no STACK-pick overlap, not archived, permissively licensed) disposes it mechanically.

## Triage note

P3 backlog. Left at `discovery-log`; nothing in this catalog does scoped-credential brokering for agent tool calls specifically (the nearest neighbors — geiger, agentshield, agent-scan, numbat — scan/audit agent configs rather than broker live credentials), so it is a differentiated candidate rather than a clear redundancy. A hands-on look is left for a future pass.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-warden](https://github.com/ermoluk/mcp-warden) | tool | Local-first credential broker for MCP (Apache-2.0, Rust) — agents call APIs/SSH/DBs via scoped presets, secrets stay in the OS keychain | Letting a coding agent call APIs, SSH, or databases means handing it raw credentials that then sit in its context | geiger, agentshield, agent-scan, numbat |
