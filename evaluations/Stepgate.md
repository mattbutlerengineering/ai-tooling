# Evaluation: Stepgate

**Repo:** [Chaarangan/Stepgate](https://github.com/Chaarangan/Stepgate)
**Stars:** 9 | **Last updated:** 2026-09-30 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-30
**Last triaged:** 2026-09-30  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

An MCP server enforcing ordered, gated procedures by running stepfiles — declarative YAML
workflows where each step must pass validation before the next runs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. Its overlaps (`proof-of-done-loop`, `agentlint`, `sigbound`) are all
`discovery-log` themselves, not STACK picks, so this isn't a P2 redundancy call. Nine stars and
brand new — no adoption signal yet, but a general-purpose gated-procedure MCP server (rather than
a single framework's built-in gate) is a distinct enough shape to warrant a real look before
dismissing it as covered by any one of those.

_Triaged 2026-09-30 by the P3 backlog band (today's new lead)._
