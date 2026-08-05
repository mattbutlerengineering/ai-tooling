# Evaluation: skill-view

**Repo:** [pc-style/skill-view](https://github.com/pc-style/skill-view)
**Stars:** 62 | **Last updated:** 2026-07-23 (pushed) | **License:** MIT
**Dev loop stage:** Cross-cutting — inspects the skills that every stage runs, without participating in any of them
**Layer:** Tooling (local-only web GUI)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A local web GUI for inspecting agent skills (`SKILL.md`) across all five places they accumulate —
user, project, plugin, cache and marketplace — so you can see what is actually installed, where each
one came from, and whether any conflict.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and its "Overlaps with" cell. Enough to place and to band it; not enough for
any verdict, and none is offered.

## Triage note

Left at `discovery-log`. Its named overlap `skills-manage` is already SKIP, which is the obvious
argument for disposing this one too — and it does not hold. skills-manage *manages* skills;
skill-view is read-only inspection across five distinct sources, and the drift it targets (skills
accumulating in a cache and a marketplace and a plugin dir with no single view) is a real problem
this repo independently confirms: the `--skills` and `--skill-design` detectors exist because
installed-artifact inventory is hard to see. Partial overlap is not redundancy.

What it does not have is evidence. ★62 and never exercised, so promoting it is unjustified and
eliminating it would be a SKIP grounded on a star count. It stays a lead.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skill-view](https://github.com/pc-style/skill-view) | tool | Local-only web GUI for inspecting agent skills (SKILL.md) across user, project, plugin, cache, and marketplace sources | Skills accumulate across many sources with no single place to see what's installed, where it came from, or if it conflicts | skills-manage, capa, openskills |
