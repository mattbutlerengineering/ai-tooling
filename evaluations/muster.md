# Evaluation: muster

**Repo:** [josefchen/muster](https://github.com/josefchen/muster)
**Stars:** 84 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A free, open-source Mac menu-bar app for Claude Code, Codex, and Cursor: see which
session needs your input and answer it from wherever you are, without switching
apps.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`, not SKIPped, even though the overlap with `claude-nanny`
(same niche: macOS menu-bar HUD for "which session needs you") is close. Two
differences keep this from a confident redundancy call: muster is cross-tool
(Claude Code + Codex + Cursor) where claude-nanny is Claude-Code-only, and muster
claims answer-from-anywhere rather than just at-a-glance status. `agent-standup`
and `ping-island` cover the same general niche with their own differentiators
(cross-tool dashboard; Dynamic Island ambient signal). A real head-to-head against
claude-nanny is the open question; left at `discovery-log` rather than a mechanical
SKIP.

_Triaged 2026-10-14 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [muster](https://github.com/josefchen/muster) | tool | Mac menu-bar app (MIT) flagging which Claude Code, Codex, or Cursor session needs you, answerable from anywhere without switching apps | Running several coding-agent sessions gives no at-a-glance signal of which one is stalled waiting on input | claude-nanny, agent-standup, ping-island |
