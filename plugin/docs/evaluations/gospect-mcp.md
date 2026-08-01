# Evaluation: gospect-mcp

**Repo:** [backendArchitect/gospect-mcp](https://github.com/backendArchitect/gospect-mcp)
**Stars:** 2 | **Last updated:** 2026-08-01 (pushed) | **License:** MIT
**Last verified:** 2026-08-01
**Last triaged:** 2026-08-01  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Go-only, report-first code scanner exposed as an MCP server — indexes a module
and reports bugs, dead code, stale docs, and outdated APIs, without editing code
until asked.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `skylos` (already a local-first, deterministic static-
analysis CI gate covering dead code, security flaws, and quality regressions across
12 languages, including Go). skylos already covers this job at broader scope; a
single-language, 2-star MCP-only reimplementation earns nothing without a
differentiated angle.

_Triaged 2026-08-01 by the daily discovery routine (today's lead)._
