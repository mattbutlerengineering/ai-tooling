# Evaluation: axuse

**Repo:** [ctoldigital/axuse](https://github.com/ctoldigital/axuse)
**Stars:** 301 | **Last updated:** 2026-10-22 (pushed) | **License:** ⚠️ no license
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

An accessibility-first browser & computer-use MCP server (JavaScript, zero dependencies) for any harness (Codex, Claude Code, OpenCode, Antigravity). Instruments the DOM/accessibility tree via CDP instead of screenshot loops, returning diffed snapshots, stable element refs, trusted input, and typed errors.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-14), pressure 0 — nothing in the catalog cites it yet. Its
"Overlaps with" cell names `browser-use`, `chrome-devtools-mcp`, and `DesktopCommanderMCP`,
none of which is a STACK pick, so this does not band as a P2 challenger. No archived flag
(repo-metadata not yet collected for this new entry), no vendored Type under a
disqualifying license (it's an MCP server, not a skill/plugin), no `Ships inside`
container. The license is unstated (GitHub reports NOASSERTION) — worth flagging for
whoever runs a hands-on eval, since that would need resolving before any ADOPT. Left at
`discovery-log`; its accessibility-tree approach (vs. screenshot loops) is a real
differentiator from the existing browser-automation peers and merits a first-time look.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [axuse](https://github.com/ctoldigital/axuse) | MCP server | Accessibility-first browser & computer-use MCP server (⚠️ no license) — diffed DOM/accessibility-tree snapshots via CDP instead of screenshot loops, one server for every harness | Browser-automation agents burn tokens on screenshot loops with unstable element refs; want diffed accessibility-tree snapshots, stable refs, and typed errors instead | browser-use, chrome-devtools-mcp, DesktopCommanderMCP |
