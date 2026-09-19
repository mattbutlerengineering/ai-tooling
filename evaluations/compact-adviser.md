# Evaluation: compact-adviser

**Repo:** [kunchenguid/compact-adviser](https://github.com/kunchenguid/compact-adviser)
**Stars:** 105 | **Last updated:** 2026-09-19 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A plugin that uses TypeSafe.ai's Jev decision model to judge whether "work appears completed or
recorded," advising or auto-triggering `/compact` at the right moment on Pi and Claude Code —
addressing the manual guesswork of when to compact context.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (headroom, token-optimizer-mcp). That is sufficient to place
the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: `headroom` (STACK, Tier 1) compresses tool *output* before it reaches
context; compact-adviser instead judges *when* to run `/compact` on the whole conversation — a
different mechanism and a different point in the loop, so not a redundancy SKIP against the STACK
incumbent. Also requires a proprietary TypeSafe API key, worth noting for anyone evaluating it
hands-on.

_Triaged 2026-09-19 by the daily discovery routine (today's new lead)._
