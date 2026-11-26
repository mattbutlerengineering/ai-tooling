# Evaluation: autologin-mcp

**Repo:** [olgaysezgin/autologin-mcp](https://github.com/olgaysezgin/autologin-mcp)
**Stars:** 10 | **Last updated:** 2026-11-24 (pushed) | **License:** MIT
**Last verified:** 2026-11-26
**Last triaged:** 2026-11-26  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

An MCP server that logs a coding agent into the app under test, keeping credentials on the
local machine and out of the model's context — for testing flows that require an
authenticated session.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and the "Overlaps with" cell.

## Triage note

Left at `discovery-log`, not SKIPped, despite citing STACK pick `playwright` in its "Overlaps
with" cell. `playwright` drives a browser generically; this tool is narrowly scoped to the
login step and keeping credentials off-model, which `playwright`/`otpkit`/`webapp-testing`
don't specifically solve. Different job, not a redundant competitor — and very low stars (10),
so worth a second look once it has more signal rather than a same-day verdict either way.

_Triaged 2026-11-26 by the daily discovery routine (new lead, same-day triage)._
