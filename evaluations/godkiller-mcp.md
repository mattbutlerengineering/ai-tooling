# Evaluation: godkiller-mcp

**Repo:** [taurus42119-stack/godkiller-mcp](https://github.com/taurus42119-stack/godkiller-mcp)
**Stars:** 14 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

Disk-backed verification gate exposed as an MCP server — blocks an agent's `claim_done` until
on-disk evidence actually verifies the work ("disk gates > vibes").

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (vet, tdd-guard, old-coder). That is sufficient to place the
lead and note the overlap is real but not fully dominating, not to support an ADOPT — this eval
offers none.

## Triage note

Left at `discovery-log`: `vet` and `tdd-guard` cover similar ground (independent verification,
red-green-refactor enforcement), but godkiller-mcp's specific mechanism — gating an agent's own
`claim_done` signal behind on-disk evidence, exposed as an MCP server rather than a CLI/skill/CI
step — is different enough integration surface to be worth a first-time look rather than a
mechanical SKIP. Low traction (14 stars) and a name/branding that reads as low-signal noise; watch
for maturity before prioritizing. Left for the P0/eval-runner lane.

_Re-triaged 2026-09-19 by the daily discovery routine (oldest-untriaged sweep) — disposition
re-confirmed unchanged: still no dominating incumbent for its specific MCP-gated `claim_done`
mechanism. Originally triaged 2026-08-03._
