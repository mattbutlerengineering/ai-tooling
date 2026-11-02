# Evaluation: tucano

**Repo:** [eduwxyz/tucano](https://github.com/eduwxyz/tucano)
**Stars:** 126 | **Last updated:** 2026-11-02 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-02
**Last triaged:** 2026-11-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A team of AI agents that talk to each other in channels, write code, and review each
other's work, running on an existing Claude Code/Codex/OpenCode/Pi install; anything
that touches the real world waits for a human yes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient to
place the lead in a triage band; it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log` — newly catalogued today, no STACK-pick overlap (P3 backlog).
Overlaps `openrig`/`orchestra`/`flopwire` on multi-agent coordination but adds a
peer-review-each-other angle plus an explicit human-approval gate on real-world
actions; worth a first-time look, not examined further in this pass.

_Triaged 2026-11-02 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tucano](https://github.com/eduwxyz/tucano) | tool | Team of AI agents (Apache-2.0) that talk in channels, write code, and review each other on your existing Claude Code/Codex/OpenCode/Pi | Running several coding agents as isolated sessions gives them no shared channel to coordinate or review each other, and nothing that touches the real world waits for a human yes | openrig, orchestra, flopwire |
