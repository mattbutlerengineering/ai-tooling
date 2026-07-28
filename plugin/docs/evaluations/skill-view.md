# Evaluation: skill-view

**Repo:** [pc-style/skill-view](https://github.com/pc-style/skill-view)
**Stars:** 56 | **Last updated:** 2026-07-23 | **License:** MIT
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Plan (skill management)
**Layer:** Tooling

---

## What it does

A local-only web GUI (published to npm as `@pc_style/skillview`) for inspecting `SKILL.md` files across user, project, plugin, cache, and marketplace sources — browse and audit what skills are actually installed and where they came from.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (GitHub API: 56 stars, MIT, pushed 2026-07-23) plus the CATALOG "Overlaps with" cell against skills-hub/skills-manage/capa. Sufficient to catalog and note the gap it fills (read-only inspection vs. those tools' install/sync/config focus), not to judge the UI's usability.

## Triage note

Differentiated from skills-hub (sync/install) and skills-manage (cross-platform management) by being a read-only inspector across every skill source (user/project/plugin/cache/marketplace) rather than an installer — a distinct niche worth a future hands-on eval. Left at discovery-log.
