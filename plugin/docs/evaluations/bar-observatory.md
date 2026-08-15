# Evaluation: bar-observatory

**Repo:** [bar181/bar-observatory](https://github.com/bar181/bar-observatory)
**Stars:** 16 | **Last updated:** 2026-08-14 (pushed) | **License:** MIT
**Last verified:** 2026-08-15
**Last triaged:** 2026-08-15  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Deterministic, local-only audit reports for Claude Code AI agent sessions, built in
Rust with a SQLite store. Makes zero network calls and is exposed to agents as an
MCP server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the
lead and note its differentiation from `ccusage`, not to support an ADOPT, and this
eval offers none.

## Triage note

Bands P2 challenger (overlaps `ccusage`, a STACK pick). Left at `discovery-log`
rather than SKIPped: `ccusage` answers a cost/token-spend question, while
bar-observatory's stated job is a tamper-evident, offline audit trail of session
activity — a compliance/forensics question, not a spend question. Small (16 stars)
and worth a first-time hands-on eval rather than a mechanical "redundant with" call.

_Triaged 2026-08-15 by the P2 challenger band._
