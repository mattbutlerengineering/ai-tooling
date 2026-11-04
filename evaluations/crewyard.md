# Evaluation: crewyard

**Repo:** [orafaelfragoso/crewyard](https://github.com/orafaelfragoso/crewyard)
**Stars:** 2 | **Last updated:** 2026-11-04 (pushed) | **License:** MIT
**Last verified:** 2026-11-04
**Last triaged:** 2026-11-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (multi-agent orchestration)
**Layer:** Infrastructure

---

## What it does

A local-first coordination engine for several independent coding agents working one
repo: task leases so two agents don't claim the same work, isolated worktrees,
versioned context, a review step, and a merge queue that only lets through changes
that are safe to combine. Targets Codex, Claude Code, and OpenCode.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Behavior under real merge conflicts across
several concurrent leases is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Cites no STACK pick in
`Overlaps with` (orca, cross-harness, skein are catalogued leads, not STACK picks). Not
examined further in this pass.

_Triaged 2026-11-04 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [crewyard](https://github.com/orafaelfragoso/crewyard) | tool | Local-first coordination engine (MIT) for independent coding agents — task leases, isolated worktrees, versioned context, reviews, and a safe merge queue | Several coding agents working one repo need task leases and a merge queue, not ad hoc worktrees and manual conflict resolution | orca, cross-harness, skein |
