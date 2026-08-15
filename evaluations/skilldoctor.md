# Evaluation: skilldoctor

**Repo:** [xyiqq/skilldoctor](https://github.com/xyiqq/skilldoctor)
**Stars:** 138 | **Last updated:** 2026-08-15 (pushed) | **License:** MIT
**Last verified:** 2026-08-15
**Last triaged:** 2026-08-15  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A quality gate for Agent Skills — lints SKILL.md files, runs a security audit for
suspicious patterns, and checks cross-harness compatibility (Claude Code, Cursor,
Codex, OpenCode) before a skill is installed or shipped.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the
lead and note its differentiation from `SkillSpector`, not to support an ADOPT, and
this eval offers none.

## Triage note

Bands P2 challenger (overlaps `SkillSpector`, a STACK pick). Left at `discovery-log`
rather than SKIPped: `SkillSpector` is a pure malice/vulnerability scanner, while
skilldoctor's stated scope is broader — lint plus cross-harness compatibility
checking (Claude/Cursor/Codex/OpenCode) in addition to a security pass. That is a
different job worth a first-time hands-on eval rather than a mechanical "redundant
with" call.

_Triaged 2026-08-15 by the P2 challenger band._
