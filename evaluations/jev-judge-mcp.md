# Evaluation: jev-judge-mcp

**Repo:** [PyModel/jev-judge-mcp](https://github.com/PyModel/jev-judge-mcp)
**Stars:** 28 | **Last updated:** 2026-09-30 (pushed) | **License:** MIT
**Last verified:** 2026-09-30
**Last triaged:** 2026-09-30  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

An MCP server exposing TypeSafe's Jev decision model as eleven typed judgment tools — verify,
screen, classify, rank — for agent policy gating (proceed / review / escalate).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. None of its overlaps (`jev-review`, `compact-adviser`, `jev-use`) are
STACK picks, so this isn't a P2 redundancy call. It's one of a growing cluster of MCP
servers/plugins wrapping TypeSafe's Jev model for a specific coding-agent judgment task; this one's
angle (a general-purpose, multi-tool MCP judge rather than one wired to a single use case) is
distinct enough from its siblings to leave for a real look rather than a mechanical dismissal, but
the cluster itself is worth revisiting together once one member gets a hands-on eval.

_Triaged 2026-09-30 by the P3 backlog band (today's new lead)._
