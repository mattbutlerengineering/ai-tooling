# Evaluation: claude-agent-flow

**Repo:** [Charlie0113-T/claude-agent-flow](https://github.com/Charlie0113-T/claude-agent-flow)
**Stars:** 5 | **Last updated:** 2026-09-14 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-16
**Last triaged:** 2026-09-16  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A Claude Code mod (`/flow`) that renders a live tree of the session's subagents beside the
transcript.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition
below, not for an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. P3 backlog — nothing structural flags it for a mechanical
disposition; stamping records that it was examined.

_Triaged 2026-09-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-agent-flow](https://github.com/Charlie0113-T/claude-agent-flow) | plugin | Claude Code mod (Apache-2.0) rendering a live tree of the session's subagents beside the transcript (`/flow`) | Subagent delegation is invisible in the scrolling transcript; want to see the live tree of who spawned whom | zoetrope, claude-devtools, roundtable |
