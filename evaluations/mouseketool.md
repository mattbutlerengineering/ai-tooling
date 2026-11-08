# Evaluation: mouseketool

**Repo:** [iDiagoValeta/mouseketool](https://github.com/iDiagoValeta/mouseketool)
**Stars:** 10 | **Last updated:** 2026-11-07 (pushed) | **License:** MIT
**Last verified:** 2026-11-08
**Last triaged:** 2026-11-08  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

An MCP server and agent skill that searches GitHub for projects already covering an idea before
you build it, reads their code, and gives a verdict: reuse, adapt, use as a base, or build.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and its "Overlaps with" cell (`Agent-Reach`, `last30days-skill`, `autoresearch`). That
is sufficient to check for a named STACK redundancy; it is not sufficient to support an ADOPT,
and this eval offers none.

## Verdict

**discovery-log — tentative read** — a small (10-star), brand-new MCP server/skill. None of its
cited peers is a STACK pick. The "check whether this already exists before building it" job it
targets is distinct from the general web/social-research tools it is loosely grouped with here,
and worth a real hands-on eval rather than a mechanical SKIP.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-08 by the daily discovery-and-triage routine._
