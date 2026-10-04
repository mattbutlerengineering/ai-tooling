# Evaluation: squidbrake

**Repo:** [batrapulkit/squidbrake](https://github.com/batrapulkit/squidbrake)
**Stars:** 11 | **Last updated:** 2026-10-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

A governance tool (Python, ★11, created 2026-09-29) that checks every AI-agent tool
call against configured rules, holds risky calls for human approval, and records
everything in a tamper-evident audit trail. Works with Claude Code and any MCP app.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Overlaps `ctrlrun`/`decern` (both discovery-log — execution safety/authorization
layers) and `toolpermit` (discovery-log — local permission firewall); none is a STACK
pick, so this does not band as a P2 challenger despite the dense cluster of similar
governance/approval tools in Security & Safety. No archived flag, no disqualifying
license, no `Ships inside` container. Left at `discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [squidbrake](https://github.com/batrapulkit/squidbrake) | tool | Brakes for AI agents (Apache-2.0) — every tool call is checked against your rules, held for human approval when risky, and recorded in a tamper-evident audit trail | Agents can make risky tool calls with no policy check, no approval step, and no tamper-evident record of what ran | ctrlrun, toolpermit, decern |
