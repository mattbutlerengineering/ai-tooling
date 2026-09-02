# Evaluation: shim-mcp

**Repo:** [justadityaraj/shim-mcp](https://github.com/justadityaraj/shim-mcp)
**Stars:** 48 | **Last updated:** 2026-08-30 (pushed) | **License:** GPL-2.0
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A WordPress MCP server plugin connecting Claude Code, Cursor, or any MCP client to a WordPress site over stdio (via WP-CLI) or HTTP, exposing 58 abilities for managing content and configuration without leaving the agent session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (license, stars, description) from the daily discovery scan. That is sufficient
for the verdict below, because the verdict turns on the repo's declared license, not on
the tool's behavior — a question metadata answers directly. It would not be sufficient to
support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — GPL-2.0. This catalog's license bar admits only permissive, MIT-like OSS; a
copyleft license disqualifies it from adoption regardless of how the tool behaves.

_Triaged 2026-09-02 by the daily discovery-and-triage routine (bulk, eliminate-only). This
is a mechanical license disposition, not a judgment on the tool's quality._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [shim-mcp](https://github.com/justadityaraj/shim-mcp) | MCP server | WordPress MCP server plugin (⚠️ GPL-2.0) — connects Claude Code, Cursor, or any MCP client to WordPress over stdio (WP-CLI) or HTTP, 58 abilities, self-contained, no cloud | Agents can't manage a WordPress site's content/config directly; want a self-hosted MCP bridge instead of hand-rolled REST calls | google-workspace-mcp, opendocswork-mcp |
