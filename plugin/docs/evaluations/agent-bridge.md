# Evaluation: agent-bridge

**Repo:** [merlinh0/agent-bridge](https://github.com/merlinh0/agent-bridge)
**Stars:** 4 | **Last updated:** 2026-11-14 (pushed) | **License:** MIT
**Last verified:** 2026-11-14
**Last triaged:** 2026-11-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An MCP server that orchestrates parallel AI coding agents (omp, Claude Code, any model) in Tern terminal tabs and git worktrees, reachable from Claude Desktop or Claude Code.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — catalogued today; no hands-on run yet.

## Triage note

Left at `discovery-log`, not SKIPped. Zero overlap pressure (brand new). It shares the parallel-worktree-orchestration space with `stargate`/`diri`/`buildd`, but its specific angle — exposing the orchestration as an MCP server callable from Claude Desktop, tied to Tern terminal tabs — is a distinct enough mechanism to deserve its own read rather than a mechanical redundancy call.

_Triaged 2026-11-14 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-bridge](https://github.com/merlinh0/agent-bridge) | MCP server | Orchestrates parallel coding agents (MIT) in Tern terminal tabs and git worktrees | Running several coding agents in parallel across terminal tabs and worktrees has no MCP-exposed orchestration layer reachable from Claude Desktop or Claude Code | stargate, diri, buildd |
