# Evaluation: hud-mode

**Repo:** [adrida/hud-mode](https://github.com/adrida/hud-mode)
**Stars:** 21 | **Last updated:** 2026-08-05 (pushed) | **License:** MIT
**Last verified:** 2026-08-06
**Last triaged:** 2026-08-06  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Compact heads-up display for a coding agent — instruments while it works, shows the answer when it stops. Works with Claude Code, Codex, and OpenCode.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: the agent-HUD niche is crowded (claude-hud, ccstatusline,
abtop) but none is a settled ADOPT/KEEP STACK incumbent for this job — ccstatusline
was itself SKIPped, and claude-hud/abtop remain discovery-log/CONDITIONAL. No clean
"redundant with `<incumbent>`" SKIP is defensible; leave for a real eval to sort out
which HUD (if any) is worth adopting.

_Triaged 2026-08-06 by the daily discovery routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hud-mode](https://github.com/adrida/hud-mode) | tool | Compact heads-up display for your coding agent (MIT) — instruments while it works, shows the answer when it stops; Claude Code, Codex, OpenCode | Agent progress is a wall of scrolling text; want a compact live status view instead of reading the whole transcript | claude-hud, ccstatusline, abtop |
