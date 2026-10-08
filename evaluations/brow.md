# Evaluation: brow

**Repo:** [efim0v/brow](https://github.com/efim0v/brow)
**Stars:** 51 | **Last updated:** 2026-10-06 (pushed) | **License:** GPL-3.0
**Last verified:** 2026-10-08
**Last triaged:** 2026-10-08  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A macOS menu-bar app tracking Claude Code usage and the 5-hour/weekly rate limits
across multiple accounts in the MacBook notch, each signed in via its own browser
profile.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Cites no STACK pick (claude-monitor, brink, hotseat — none in STACK.md), so this
isn't a mechanical redundancy call. GPL-3.0 is a non-issue here regardless: the
catalog Type is `tool` (a standalone menu-bar app you run, not a skill/plugin whose
text is vendored into a consuming repo), so the P4 mechanical-skip license bar
doesn't apply. Left at `discovery-log` — a niche multi-account rate-limit widget,
not differentiated enough to prioritize but not clearly dominated either.

_Triaged 2026-10-08 by the P3 backlog band._
