# Evaluation: systemprompt-core

**Repo:** [systempromptio/systemprompt-core](https://github.com/systempromptio/systemprompt-core)
**Stars:** 8 | **Last updated:** 2026-10-16 (pushed) | **License:** BSL-1.1 (source-available)
**Last verified:** 2026-10-17
**Last triaged:** 2026-10-17  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

Rust control-plane library for agentic-system governance — identity, MCP/A2A tool execution,
policy, and audit trails.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
(license text and the project's own "source-available" framing). That is sufficient for the
verdict below, because the verdict turns on license terms, not on the tool's behaviour.

## Verdict

**SKIP** — BSL-1.1, not permissive OSS. The repository's own description states production use
requires a commercial license; this catalog adopts only permissively-licensed (MIT-like) tools,
and a source-available license that gates production use behind a paid tier fails that bar
regardless of how capable the governance layer is.

## Triage note

Picked up as one of the oldest untriaged leads (no prior eval file) in the P3 backlog band.
License-disqualified rather than redundant — no STACK pick is cited in Overlaps, so this isn't a
P2 case; it's a plain license bar.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [systemprompt-core](https://github.com/systempromptio/systemprompt-core) | tool | Rust control-plane library (BSL-1.1, source-available) for agentic-system governance — identity, MCP/A2A tool execution, policy, and audit trails | Agentic systems need a self-hosted governance layer (identity, policy, audit) instead of ad-hoc per-tool checks | decern, agent-governance-toolkit, mcp-context-forge |  |
