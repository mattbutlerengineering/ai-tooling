# Evaluation: myco

**Repo:** [chenhg5/myco](https://github.com/chenhg5/myco)
**Stars:** 74 | **Last updated:** 2026-11-11 (pushed) | **License:** MIT
**Last verified:** 2026-11-11
**Last triaged:** 2026-11-11  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A single Go binary that connects Claude Code, Codex, and any agent CLI across machines, so
agents find each other, delegate tasks, and reply through one hub, per the repo's own
description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-11) plus the CATALOG one-liner and "Overlaps with" cell (`imbo`,
`flopwire`, `reason-network`). That is enough to place it; not enough for a positive verdict,
and none is offered.

## Triage note

Left at `discovery-log` — P3 backlog, zero overlap pressure against any STACK pick. The
cross-machine agent-messaging niche is already well covered (`imbo`, `flopwire`,
`reason-network`, `agent-link`, `succubus`), and a one-liner alone doesn't distinguish this
entrant's "single Go binary, one-line setup" claim enough for a confident SKIP or priority
bump. Stamped and left for a future pass.

_Triaged 2026-11-11 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [myco](https://github.com/chenhg5/myco) | tool | Single Go binary (MIT) connecting Claude Code, Codex, and any agent CLI across machines so agents find each other and delegate tasks through one hub | Coordinating agent CLIs across different machines has no shared hub for agents to find each other and delegate work | imbo, flopwire, reason-network |
