# Evaluation: maddu

**Repo:** [frdyx/maddu](https://github.com/frdyx/maddu)
**Stars:** 5 | **Last updated:** recent (772 commits at inspection; exact push date not captured from the repo page; checked 2026-09-04) | **License:** Apache-2.0
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Local-first governance for AI coding agents: an external, append-only, files-only event log that verifies what agents did, so no agent is the sole witness to its own work. Operates without cloud dependencies; the log is the single source of truth teams can inspect, replay, and challenge instead of trusting an agent's self-reported summary.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Zero overlap pressure (P3 backlog). Sits near `decern`/`agent-governance-toolkit`/`halofy` (governance/audit for agent actions), but its specific angle — a local, files-only, append-only record independent of the agent's own reporting — is differentiated enough from the SMT-verified-authorization (`decern`) and org-wide-identity (`halofy`) approaches to be worth a real look rather than a mechanical SKIP.

_Triaged 2026-09-04 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [maddu](https://github.com/frdyx/maddu) | tool | Local-first governance for AI coding agents (Apache-2.0) — an external, append-only, files-only event log verifying what agents did, so no agent is the sole witness to its own work | Teams must trust an agent's own summary of what it did; want an independent, replayable, challengeable record instead | decern, agent-governance-toolkit, halofy |
