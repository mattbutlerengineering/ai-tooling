# Evaluation: agentbox

**Repo:** [devilcoolyue/agentbox](https://github.com/devilcoolyue/agentbox)
**Stars:** 78 | **Last updated:** 2026-10-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A self-hosted browser workspace (Go, ★78, created 2026-09-28) for Claude Code and
Codex CLI — Docker-backed sessions reachable from a browser, with terminal, file
browser, Git integration, and usage tracking, so a coding-agent session can persist
independently of any one laptop.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Overlaps `orca` (ADOPT-adjacent discovery-log — fleet of parallel agents, desktop +
mobile companion) and `useagent` (SKIP — AGPL-3.0 cloud coworker); neither of orca's own
verdict nor useagent's SKIP is a STACK pick for this specific niche, so this does not
mechanically band as P2. Differentiator from `useagent`: Apache-2.0 rather than
AGPL-3.0, and self-hosted-by-you rather than a vendor's cloud computer. No archived
flag, no disqualifying license, no `Ships inside` container. Left at `discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentbox](https://github.com/devilcoolyue/agentbox) | tool | Self-hosted browser workspace (Apache-2.0) for Claude Code and Codex CLI — Docker sessions, terminal, files, Git, and usage tracking | Running a coding agent persistently needs a standing, browser-accessible workspace, not a terminal tab that dies with your laptop | orca, useagent, Nimbalyst |
