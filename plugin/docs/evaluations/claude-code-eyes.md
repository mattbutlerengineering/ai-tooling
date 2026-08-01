# Evaluation: claude-code-eyes

**Repo:** [fcavalcantirj/claude-code-eyes](https://github.com/fcavalcantirj/claude-code-eyes)
**Stars:** 38 | **Last updated:** 2026-07-21 (pushed) | **License:** MIT
**Last verified:** 2026-08-01
**Last triaged:** 2026-08-01  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A camera skill that gives Claude Code eyes on real hardware — verify a rendered
panel, or check wiring before power-on, catching bugs that only exist on the glass
or the board, not in logs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Overlaps `SceneProof`, `midscene`, and `passmark`, but all three verify *rendered
software* (UI/WebGL/browser); claude-code-eyes verifies *physical* hardware via a
real camera, a genuinely different domain the catalog otherwise lacks. Left at
`discovery-log` — niche but differentiated, not a mechanical SKIP.

_Triaged 2026-08-01 by the daily discovery routine (today's lead)._
