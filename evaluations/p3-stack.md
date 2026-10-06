# Evaluation: p3-stack

**Repo:** [uzairansaruzi/p3-stack](https://github.com/uzairansaruzi/p3-stack)
**Stars:** 115 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-06
**Last triaged:** 2026-10-06  <!-- triaged: bulk -->
**Dev loop stage:** Implement / Agent Orchestration
**Layer:** Tooling

---

## What it does

A subagent/worktree/PR stack reworked for T3 Code — delegated subagents, isolated worktree
threads, PR watching, and scheduled runs, per the repo description and topics.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the GitHub
repository description, topics, and metadata (stars, license, push date). That is sufficient to
place the lead in the catalog, not to judge its behavior hands-on.

## Triage note

Left at `discovery-log`. No `Overlaps with` cell names a STACK pick, so this is plain P3 backlog —
nothing structural to dispose on. A real eval would need to check whether the four claimed
capabilities (subagent delegation, worktree isolation, PR watching, scheduling) work together or
are four thin wrappers, and how it differs from `orca`/`stargate`/`buildd`.

_Triaged 2026-10-06 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [p3-stack](https://github.com/uzairansaruzi/p3-stack) | tool | Subagent/worktree/PR stack (MIT) reworked for T3 Code — delegated subagents, isolated worktree threads, PR watching, scheduled runs | Delegating subagents, isolating worktree threads, watching PRs, and scheduling runs for one coding harness are four separate scripts with nothing tying them together | orca, stargate, buildd |
