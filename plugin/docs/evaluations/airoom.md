# Evaluation: airoom

**Repo:** [petritavd/airoom](https://github.com/petritavd/airoom)
**Stars:** 37 | **Last updated:** 2026-11-15 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-16
**Last triaged:** 2026-11-16  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A control room for Claude Code agents: every running session on one screen, with
one-click approvals. Ships for macOS and Windows.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a P3
leave-at-discovery-log call, not to judge the tool's actual behavior — it would not
support an ADOPT, and this eval offers none.

## Triage note

Significant-enough standalone tool (multi-session control room with one-click approvals,
cross-platform) to deserve a real hands-on eval rather than a mechanical disposition;
left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [airoom](https://github.com/petritavd/airoom) | tool | Control room (Apache-2.0) putting every Claude Code agent session on one screen with one-click approvals, for macOS and Windows | Running several Claude Code sessions means switching windows to check status or approve each one individually | lot-map, claude-super-sidebar, shoulder |
