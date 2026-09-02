# Evaluation: Only-Skill-You-Need

**Repo:** [Endokelp/Only-Skill-You-Need](https://github.com/Endokelp/Only-Skill-You-Need)
**Stars:** 36 | **Last updated:** 2026-08-27 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

The first Agent Skill a beginner installs — bootstraps Claude Code, Cursor, and other
agents, then routes every task to the current best skill for that job.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata and the CATALOG "Overlaps with" cell.

## Triage note

Bands as a P2 challenger against `skill-creator` (score/overlap computed from the
"Overlaps with" cell), but the jobs are different: `skill-creator` is an *authoring*
meta-skill (draft → eval → benchmark → package), while Only-Skill-You-Need is a *routing*
meta-skill (given hundreds of installed skills, dispatch to the right one for a task) —
closer in spirit to `warden` (routes across MCP servers/skills) or `skills-hub` (browse
and sync skills) than to `skill-creator`. Not clearly redundant with the named incumbent,
so not disposed as SKIP here. Left at `discovery-log` for a real evaluation of whether the
routing actually works across a nontrivial skill library — a low-stars (36★), 6-day-old
repo with no measured triggering accuracy yet.

_Triaged 2026-09-02 by the P2 challenger band (daily discovery-and-triage routine, bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Only-Skill-You-Need](https://github.com/Endokelp/Only-Skill-You-Need) | skill | The first Agent Skill a beginner installs (MIT) — bootstraps Claude Code, Cursor, and other agents, then routes every task to the current best skill for that job | A beginner facing hundreds of skills has no starting point or router to the right one for a given task | skills-hub, skill-creator, warden |
