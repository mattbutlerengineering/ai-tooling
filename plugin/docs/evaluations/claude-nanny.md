# Evaluation: claude-nanny

**Repo:** [app-brew/claude-nanny](https://github.com/app-brew/claude-nanny)
**Stars:** 3 | **Last updated:** 2026-08-06 (pushed) | **License:** MIT
**Last verified:** 2026-08-07
**Last triaged:** 2026-08-07  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling (macOS menu-bar app)

---

## What it does

A menu-bar status HUD for macOS monitoring multiple running Claude Code sessions across
terminals — running / needs-input / done / error at a glance. Installs as a Claude Code
plugin.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (claude-hud, hud-mode, ping-island). That is
sufficient for a redundancy SKIP, which turns on overlap with catalogued incumbents rather
than the tool's behavior.

## Verdict

**SKIP** — redundant with `claude-hud` (and `hud-mode`, `ping-island`). Three catalogued
tools already show live Claude Code session status at a glance — claude-hud (context/tools/
agents/todo progress), hud-mode (compact instrumented HUD), and ping-island (macOS Dynamic
Island command center). claude-nanny (3 stars) is a fourth, narrower entrant in the same
niche (menu-bar-only, macOS-only, status-only) with no disclosed capability the other three
lack; a fourth status-HUD tool earns nothing without differentiation.

_Triaged 2026-08-07 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-nanny](https://github.com/app-brew/claude-nanny) | plugin | Menu-bar status HUD (MIT) for macOS monitoring multiple running Claude Code sessions across terminals — running/needs-input/done/error at a glance | Running several Claude Code sessions across terminals, you can't tell which need input without checking each window | claude-hud, hud-mode, ping-island |
