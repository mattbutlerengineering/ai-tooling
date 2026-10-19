# Evaluation: agentplay

**Repo:** [Entelligence-AI/agentplay](https://github.com/Entelligence-AI/agentplay)
**Stars:** 259 | **Last updated:** 2026-10-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Local session replay for coding agents — `uvx agentplay` builds a map and timeline of which
files, tools, MCP servers, and models a coding-agent session touched, across Claude Code,
Codex, Cursor, and Copilot.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and GitHub repo metadata (stars, license, activity). No hands-on run was performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

P3 backlog, oldest-untriaged (no prior eval file, never stamped). Not a P2 challenger: its
cited peers (`agent-standup`, `muster`, `claude-command-center`) are themselves discovery-log
leads, not a STACK pick it's redundant with. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [agentplay](https://github.com/Entelligence-AI/agentplay) | tool | Local session replay (Apache-2.0, `uvx agentplay`) — a map and timeline of files, tools, MCP servers, and models a coding-agent session touched | Coding-agent sessions leave no replayable record of what was touched and when, across Claude Code, Codex, Cursor, Copilot | agent-standup, muster, claude-command-center |  |
