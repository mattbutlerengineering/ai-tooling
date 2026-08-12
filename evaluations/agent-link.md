# Evaluation: agent-link

**Repo:** [Riccardo8888/agent-link](https://github.com/Riccardo8888/agent-link)
**Stars:** 36 | **Last updated:** 2026-08-12 (pushed) | **License:** MIT
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An end-to-end encrypted channel letting coding agents exchange messages across machines, anywhere.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: repo metadata plus the CATALOG
"Overlaps with" cell. Enough to place it against nearby agent-coordination tools, not enough for
any verdict, and none is offered.

## Triage note

Left at `discovery-log`. `succubus` and `fleetpost` solve shared-state coordination (file claims,
task visibility) for agents in one repo or across machines; `agent-link` solves a narrower, distinct
problem — a secure transport between two agents — and doesn't clearly duplicate either. Worth a
real look rather than a mechanical dispose.

_Triaged 2026-08-12 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-link](https://github.com/Riccardo8888/agent-link) | tool | End-to-end encrypted channel (MIT) letting coding agents exchange messages across machines | Coordinating agents across machines/networks means exposing plaintext channels; want an encrypted, direct link | succubus, fleetpost, rmux |
