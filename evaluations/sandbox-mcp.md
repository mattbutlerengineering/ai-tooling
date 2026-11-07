# Evaluation: sandbox-mcp

**Repo:** [shanselman/sandbox-mcp](https://github.com/shanselman/sandbox-mcp)
**Stars:** 160 | **Last updated:** 2026-11-07 (pushed) | **License:** MIT
**Last verified:** 2026-11-07
**Last triaged:** 2026-11-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An MCP server and CLI (MIT) that automates Windows Sandbox, provisioning a fresh,
throwaway Windows machine for testing an app and tearing it down afterward.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the
lead and check it against existing sandbox-infra incumbents, not to support an ADOPT.

## Triage note

Left at discovery-log — brand new (pushed today), zero overlap pressure yet. It
overlaps `devvm`/`vercel-sandbox`/`sandcastle` on the "disposable sandbox" idea but is
differentiated by platform: it is the only one of the three specifically automating
*Windows* Sandbox, which the others don't cover. Not clearly redundant enough for a
mechanical SKIP; left for a real hands-on eval if demand shows up.
