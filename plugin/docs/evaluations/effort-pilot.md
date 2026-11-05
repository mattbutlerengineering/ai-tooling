# Evaluation: effort-pilot

**Repo:** [vadympetryshyn/effort-pilot](https://github.com/vadympetryshyn/effort-pilot)
**Stars:** 8 | **Last updated:** 2026-11-05 (pushed) | **License:** MIT
**Last verified:** 2026-11-05
**Last triaged:** 2026-11-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Automatically sets Claude Code's reasoning effort per turn — xhigh for plans, medium
for building, low for questions and trivial turns like git commits — instead of a flat
effort level across every kind of turn.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. The claimed 20-50% token savings and ~1.5x speedup
are self-reported and untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Overlaps `agent-router`
and `claude-code-router` (also pick effort/model per task) and `ccs` (profile
switching), none of which is a STACK pick. Not examined further in this pass.

_Triaged 2026-11-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [effort-pilot](https://github.com/vadympetryshyn/effort-pilot) | tool | Per-turn reasoning-effort automation (MIT) for Claude Code — xhigh for plans, medium for building, low for questions and trivial turns | Every turn burns the same reasoning effort regardless of whether it's a plan, a build step, or a trivial git commit | agent-router, ccs, claude-code-router |
