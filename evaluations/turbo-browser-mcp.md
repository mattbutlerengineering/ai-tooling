# Evaluation: turbo-browser-mcp

**Repo:** [Tthanh2k6/turbo-browser-mcp](https://github.com/Tthanh2k6/turbo-browser-mcp)
**Stars:** 127 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-17
**Last triaged:** 2026-11-17  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

A Playwright-based MCP server built specifically to cut agent turns and tokens:
one-call form filling, delta (changed-only) snapshots instead of full-page dumps, batched
multi-step actions, and a submit guard enabled by default.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual
behavior — it would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read**

A plausible token-efficiency improvement over the base Playwright MCP server; the actual
delta-snapshot and batched-step savings are unverified claims until someone runs both
side by side.

## Triage note

Banded P2, challenging `playwright` (STACK, RUN) — unsurprising, since this *is* a
Playwright MCP server. But "built on Playwright" is not "redundant with Playwright": the
entire pitch is turn/token efficiency over the base server (one-call form filling, delta
snapshots vs. full-page ones, batched steps, a default submit guard), the same angle
`axuse` takes with accessibility-tree diffing instead of screenshot loops. Whether those
savings are real, and whether they survive contact with a real multi-step browser task, is
exactly what a bulk source-only pass cannot determine. Not SKIPped; left at `discovery-log`
for a real hands-on comparison against `playwright` (and `axuse`) on turns/tokens for an
equivalent task.

_Triaged 2026-11-17 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [turbo-browser-mcp](https://github.com/Tthanh2k6/turbo-browser-mcp) | MCP server | Playwright MCP server (MIT) cutting agent turns and tokens with one-call form filling, delta snapshots, and batched steps | Browser-automation agents burn turns and tokens on one-action-per-call loops and full-page snapshots | playwright, axuse, browser-use |
