# Evaluation: aside-codemode

**Repo:** [lidge-jun/aside-codemode](https://github.com/lidge-jun/aside-codemode)
**Stars:** 86 | **Last updated:** 2026-09-15 (pushed) | **License:** MIT
**Last verified:** 2026-09-15
**Last triaged:** 2026-09-15  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Batches an agent's file search/edit and browser-automation tool calls into one sandboxed JavaScript block instead of firing them one round trip at a time — rg-backed search, file tools, and Playwright-driven browser work all inside a single "code mode" call. Its own benchmark claims a 55s multi-call find+grep sequence became ~1s on a real folder.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. It overlaps `agent-browser`, `browser-use`, and `playwright` on driving a browser for an agent, but none is a STACK pick, and its actual job is different — a tool-call batching/efficiency layer (the "code mode" pattern) rather than a browser driver itself, built as a companion to the (uncatalogued) "Aside" agent. Worth a real look at whether the efficiency claim holds up, rather than a mechanical SKIP. 86★ and 2 days old.

_Triaged 2026-09-15 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [aside-codemode](https://github.com/lidge-jun/aside-codemode) | tool | Code-mode batching (MIT) for agent browser/file tool calls — one sandboxed JS call replaces dozens of round trips | Agents burn tool-call round trips (rg/grep/file ops, browser steps) one at a time; batching them into one sandboxed script cut a 55s multi-call sequence to ~1s on a real folder | agent-browser, browser-use, playwright |
