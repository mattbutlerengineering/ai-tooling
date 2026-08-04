# Evaluation: handoff-skill

**Repo:** [ToolMonsters/handoff-skill](https://github.com/ToolMonsters/handoff-skill)
**Stars:** 33 | **Last updated:** 2026-07-23 (pushed) | **License:** MIT
**Dev loop stage:** Memory & Context (session handoff)
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Turns the current conversation into a complete handoff document so another agent — or another
session — can resume exactly where it left off.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata fetched fresh for this pass
on 2026-08-04 (the slug had no cached record) plus the CATALOG one-liner and "Overlaps with" cell
(`storybloq`, `byterover-cli`, `getspecstory`, `cli-continues`). Enough to place it; not enough for a
positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. MIT, ★33, pushed 2026-07-23 — small and young, and the star count carries no
signal either way at that size.

The problem it names is real and this session is an instance of it: context runs out, or work moves to a
different agent, and everything decided along the way has to be reconstructed. A structured handoff
document is the obvious fix and one that costs nothing to try, since a skill is text.

Two reasons not to promote it and none to dispose it. The capability overlaps four catalogued neighbours
plus the harness's own compaction, and where a *skill* wins over built-in summarization is precisely the
kind of claim `TEMPLATE.md` requires a triggering test or a with-skill-vs-baseline A/B to support —
detector S tracks exactly this gap. And a vendored `skill` is the Type where licence matters most, since
its text is copied into the consuming repo; MIT is clean here, which is the one thing this pass could
confirm.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [handoff-skill](https://github.com/ToolMonsters/handoff-skill) | skill | Turns the current conversation into a complete handoff document so any LLM can resume exactly where you left off | Switching agents or tools mid-task loses conversation state and decisions made so far | storybloq, byterover-cli, getspecstory, cli-continues (ext.) |
