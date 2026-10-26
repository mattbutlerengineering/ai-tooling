# Evaluation: cindy

**Repo:** [makecindy/cindy](https://github.com/makecindy/cindy)
**Stars:** 5,800 | **Last updated:** n/a (not checked via API; this session's GitHub access is repo-scoped) | **License:** Apache-2.0
**Last verified:** 2026-10-26
**Last triaged:** 2026-10-26  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An open-source local AI agent client (pnpm monorepo: Electron desktop app + Expo/React
Native mobile app) that wraps existing coding-agent harnesses — currently Claude Code
and Codex, with a native harness in development — and runs on the user's own machine
against their real files and logged-in apps. Supports a hosted "Cindy" service,
bring-your-own API keys/local models, or a fully local "skip sign-in" mode. Extensible
through memory, skills, automation, MCP integrations, and plugins.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
repo's own README (fetched over the web, since this session's GitHub API access is
scoped to this repository and does not extend to arbitrary repos) plus the CATALOG
"Overlaps with" cell. That is sufficient to place the lead against its closest catalog
peers, not to support any verdict, and none is offered here.

## Triage note

Cites `claude-squad` in its "Overlaps with" cell, which bands this P2 challenger — but
`claude-squad` is a lightweight terminal multiplexer for running several agent sessions
in parallel, while `cindy` is a packaged consumer product: its own desktop/mobile apps,
an optional hosted backend, and a cross-harness abstraction layer, not just a session
manager. That is a meaningfully different scope, the same reasoning that has kept other
packaged agent-client products (e.g. `orca`, `t3code`) at `discovery-log` rather than
SKIPped as redundant with a terminal-only tool. Left at `discovery-log` — a real
hands-on comparison against `orca`/`claude-squad`/`t3code` on actual day-to-day use
would need a first-time eval, not a mechanical SKIP.

_Triaged 2026-10-26 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cindy](https://github.com/makecindy/cindy) | tool | Open-source local AI agent client (Apache-2.0, ★5.8K) wrapping Claude Code/Codex with desktop (Electron) + mobile (Expo) apps, memory/skills/MCP, and a "skip sign-in" local mode | Want a ready-to-use, multi-harness agent client with its own apps, not a bare terminal CLI | orca, t3code, claude-squad |
