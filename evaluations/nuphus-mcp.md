# Evaluation: nuphus-mcp

**Repo:** [mrpulor-gh/nuphus-mcp](https://github.com/mrpulor-gh/nuphus-mcp)
**Stars:** 50 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

Desktop automation MCP server — computer use for any AI agent: control screen, windows,
mouse/keyboard, and Chrome over stdio.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (DesktopCommanderMCP, unity-mcp, chrome-devtools-mcp). That
is sufficient to place the lead and note none of its named overlaps is a STACK incumbent, not to
support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: DesktopCommanderMCP covers terminal + filesystem control, not GUI
mouse/screen automation, and unity-mcp / chrome-devtools-mcp are scoped to a specific editor or
browser devtools rather than the whole desktop. nuphus-mcp's OS-level computer-use control is a
real gap none of those close. Left for the P0/eval-runner lane.

_Triaged 2026-08-03 by today's discovery lead._
