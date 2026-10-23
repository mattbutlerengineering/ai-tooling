# Evaluation: TokenForge

**Repo:** [speedydivid/TokenForge](https://github.com/speedydivid/TokenForge)
**Stars:** 30 | **Last updated:** 2026-10-17 (pushed) | **License:** ⚠️ no license
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

A context-window optimizer (JavaScript) spanning 17 agent platforms (Claude Code, Gemini
CLI, VS Code Copilot, OpenCode, Codex CLI, and more) — sandboxes tool output before it
reaches context (self-reported 98% reduction), persists session memory via SQLite+FTS5,
and enforces routing across platforms through MCP + hooks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide the P2
disposition below (which turns on redundancy with a named STACK incumbent, not on the
tool's behavior), not to support any adoption verdict, and none is offered here. The
"98% reduction" figure is self-reported and unverified by us.

## Triage note

Bands as **P2 challenger**: its "Overlaps with" cell names `headroom`, which is a STACK
pick (ADOPT, MEASURED, "Compresses tool outputs, logs, and files before they reach the
LLM, 60-95% fewer tokens, reversibly via local cache"). TokenForge's tool-output
sandboxing covers similar ground to headroom's compression, but it also claims persistent
cross-session memory (SQLite+FTS5) and enforced routing across 17 named platforms —
neither of which headroom's one-liner claims. That is enough differentiation that a
mechanical "redundant with headroom" SKIP would be the evidence-free verdict this lane
exists to avoid; a real hands-on comparison is the only way to tell whether the memory
and routing layers earn their own slot. Left at `discovery-log`, not SKIPped.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [TokenForge](https://github.com/speedydivid/TokenForge) | tool | Context-window optimizer (⚠️ no license; self-reported 98% tool-output reduction) across 17 agent platforms — sandboxes tool output, persists SQLite+FTS5 session memory, enforces MCP+hook routing | Tool output floods context and session memory resets per platform; want sandboxed output and persistent memory enforced centrally across every agent in use | winnow, headroom, opencontext |
