# Evaluation: claude-bulkhead

**Repo:** [Myeongseok-Kang/claude-bulkhead](https://github.com/Myeongseok-Kang/claude-bulkhead)
**Stars:** 22 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A set of Claude Code hooks that keep parallel sessions on one machine from
interfering with each other: blocks commands that would kill another session's
processes, take its ports, exhaust shared RAM, or switch branches in a shared git
tree.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`, not SKIPped. `worktrunk` and `dmux` isolate parallel-agent
work via git worktrees; `moire` warns about in-flight logical conflicts between
agents editing related code. None of the three is hook-based machine-level
bulkheading against port collisions, process kills, or RAM exhaustion across
sessions sharing one checkout — a different, complementary layer (worktree
isolation vs. runtime collision prevention). Too new (22 stars, 1 day old) to
judge; left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-14 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-bulkhead](https://github.com/Myeongseok-Kang/claude-bulkhead) | plugin | Claude Code hooks (MIT) stopping parallel sessions on one machine from killing each other's processes, fighting over ports, exhausting shared RAM, or switching a shared branch | Running several Claude Code sessions on one machine lets them silently kill each other's servers, collide on ports, or switch branches under each other | worktrunk, moire, dmux |
