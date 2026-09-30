# Evaluation: seiso

**Repo:** [scarletkc/seiso](https://github.com/scarletkc/seiso)
**Stars:** 152 | **Last updated:** 2026-09-27 (pushed) | **License:** MIT
**Last verified:** 2026-09-30
**Last triaged:** 2026-09-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Markdown convention and linter, written in Rust, for project docs written by AI and read by
humans and agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. It cites `snifftest` and `code-quality` in "Overlaps with", but neither is
a STACK pick, so this isn't a P2 redundancy call. `snifftest` targets AI-writing *tells* in prose;
`code-quality` gates code diffs; `seiso` is narrower still — a structural convention plus linter for
*docs* specifically. New (four days old, 152 stars) with no adoption signal yet. Significant enough
a gap (nothing in the catalog enforces a markdown convention for AI-authored docs specifically) to
deserve a real look rather than a mechanical dismissal.

_Triaged 2026-09-30 by the P3 backlog band (today's new lead)._
