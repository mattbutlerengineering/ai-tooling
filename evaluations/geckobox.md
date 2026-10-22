# Evaluation: geckobox

**Repo:** [migasrias2/geckobox](https://github.com/migasrias2/geckobox)
**Stars:** 67 | **Last updated:** 2026-10-20 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Runs Claude Code, Codex, or any coding agent across all of your own computers and
dispatches jobs across them (MIT, free, no relay server, no limits).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Bands as a P2 challenger against `claude-squad` (pressure 0), but the two solve different
problems: `claude-squad` manages multiple parallel agent *sessions on one machine*, while
this dispatches jobs *across several of the user's own machines* with no relay server.
Not redundant. No archived flag, no disqualifying license, no `Ships inside` container.
Left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [geckobox](https://github.com/migasrias2/geckobox) | tool | Runs Claude Code, Codex, or any coding agent across all of your own computers and dispatches jobs to them (MIT) | Coordinating a coding agent's jobs across several of your own machines means manual SSH juggling or a relay server | claude-squad, fleetpost, diri |
