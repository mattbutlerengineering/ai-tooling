# Evaluation: agentaps

**Repo:** [domenkozar/agentaps](https://github.com/domenkozar/agentaps)
**Stars:** 53 | **Last updated:** 2026-09-29 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-01
**Last triaged:** 2026-10-01  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A desktop workspace app (Rust) for running any Agent Client Protocol (ACP)-compatible coding
harness through one GUI. Manages agent conversations and project sessions locally or over SSH,
with a browser-pairing "Web Connect" feature to continue a session from another device.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. None of its overlaps (`d-code`, `roundtable`, `acryl`) is a STACK pick,
so this is backlog, not a P2 call. New (two days old, 53 stars), but ACP-protocol genericity
(any compatible harness, not just Claude Code) plus cross-device session continuity is a real
differentiator from `d-code` (a Claude-Code-only desktop client) worth a hands-on look later.

_Triaged 2026-10-01 by the P3 backlog band (today's new lead)._
