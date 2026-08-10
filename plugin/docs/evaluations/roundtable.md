# Evaluation: roundtable

**Repo:** [Kostakurta8/roundtable](https://github.com/Kostakurta8/roundtable)
**Stars:** 14 | **Last updated:** 2026-08-10 (pushed) | **License:** MIT
**Last verified:** 2026-08-10
**Last triaged:** 2026-08-10  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Watches Claude Code agents work as a pixel-art office — replays any second of a
session exactly and shows per-agent cost. Read-only, 100% local, never calls an API.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as a P2 challenger against `abtop` (both are local session
observability tools), but the presentation and interaction model are genuinely
different — an exact, scrubbable visual replay with per-agent cost attribution is
not what `abtop`'s real-time TUI offers, and none of the catalog's other
observability tools (`claude-fleet`, `peek`, `claude-devtools`) provide a replay
view either. Too early (14 stars, 6 days old) to call redundant; left at
discovery-log for a real hands-on eval rather than a mechanical SKIP.

_Triaged 2026-08-10 by the P2 challenger band._
