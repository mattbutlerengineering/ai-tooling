# Evaluation: browser-hands

**Repo:** [214140846/browser-hands](https://github.com/214140846/browser-hands)
**Stars:** 19 | **Last updated:** 2026-11-13 (pushed) | **License:** MIT
**Last verified:** 2026-11-14
**Last triaged:** 2026-11-14  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A Chrome extension plus local MCP server that gives a coding agent hands in your own logged-in browser — parallel sessions, low CPU.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — catalogued today; no hands-on run yet.

## Triage note

Left at `discovery-log`, not SKIPped. It challenges `playwright` (STACK, ADOPT) in "Overlaps with", but `playwright`/`browser-use`/`agent-browser` all automate an isolated, non-logged-in browser instance, while browser-hands' pitch is specifically reusing your own real, already-logged-in browser session — a meaningfully different mechanism (session reuse vs. fresh automation) that the catalog already treats as a legitimate separate axis for sibling tools in this space. Not a clean redundancy call on a README alone.

_Triaged 2026-11-14 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [browser-hands](https://github.com/214140846/browser-hands) | MCP server | Chrome extension + local MCP server (MIT) giving a coding agent hands in your own logged-in browser, parallel and low-CPU | Browser-automation agents can't reuse your real logins or run several sessions in parallel without heavy per-session browser instances | playwright, browser-use, agent-browser |
