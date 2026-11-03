# Evaluation: skein

**Repo:** [Balanov/skein](https://github.com/Balanov/skein)
**Stars:** 257 | **Last updated:** 2026-11-03 (pushed) | **License:** MIT
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Fail-closed swarm orchestration runtime: work is dispatched in fenced "epochs," and a
worker that finishes after its epoch has already closed has its result rejected rather
than silently merged into current state. The pitch is that a straggler/late-completion
race in a multi-agent swarm is a correctness bug, not just a performance one, and the
fence is meant to close that race deterministically.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Whether the epoch-fencing mechanism actually
prevents late-completion corruption under real swarm load is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today, no STACK-pick overlap.
Not examined further in this pass.

_Triaged 2026-11-03 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skein](https://github.com/Balanov/skein) | tool | Fail-closed swarm orchestrator (MIT) with epoch-fenced work and late-completion rejection | A straggler worker finishing after its epoch closed can silently apply stale results into current swarm state | task-state-guard, openrig, AgentsMesh |
