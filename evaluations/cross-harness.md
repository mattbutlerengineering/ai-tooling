# Evaluation: cross-harness

**Repo:** [AI-BizOS/cross-harness](https://github.com/AI-BizOS/cross-harness)
**Stars:** 48 | **Last updated:** 2026-10-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-15
**Last triaged:** 2026-10-15  <!-- triaged: bulk -->
**Dev loop stage:** Implement (multi-agent orchestration)
**Layer:** Infrastructure (orchestrator process; one worktree per agent)

---

## What it does

An orchestrator that runs several coding agents (Claude Code, Codex) on one project
via each vendor's own protocol, with one shared approval queue and one worktree per
agent — avoiding separate terminals, duplicate permission prompts, and conflicting
edits when running multiple agents in parallel.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
repo's description, topics, and the CATALOG.md one-liner/overlaps cell. That is
sufficient to place the lead at `discovery-log`; it would not support an ADOPT, and
this eval offers none.

## Triage note

Left at `discovery-log`. A newly catalogued lead (created 2026-10-10) with no
archival or license signal that would license a mechanical SKIP. It does cite
catalog overlaps (orca, diri, agent-of-empires) but none is a STACK pick, so P2
"redundant with `<incumbent>`" does not apply. A real verdict needs running several
agents through it concurrently, outside eliminate-only authority. Left for a future
hands-on eval or the P0/`eval-runner` lane.

_Triaged 2026-10-15 by the P3 backlog band._
