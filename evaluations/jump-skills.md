# Evaluation: jump-skills

**Repo:** [fabricioctelles/jump-skills](https://github.com/fabricioctelles/jump-skills)
**Stars:** 28 | **Last updated:** 2026-09-06 (pushed) | **License:** MIT
**Last verified:** 2026-09-08
**Last triaged:** 2026-09-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement (skill discovery/routing)
**Layer:** Tooling

---

## What it does

A meta-skill router ("Ninjas") that reads a task description and loads the single best-matching specialized skill from a curated library of 500+ skills across 10+ cloud platforms and services, instead of the agent — or the developer — searching a large skill catalog by hand.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `skill-creator` despite the overlap citation. `skill-creator` (anthropics/claude-plugins-official) is an *authoring* tool for writing and optimizing SKILL.md files; jump-skills is a *routing* tool that picks which already-installed skill to load for a task. Different job in the skill lifecycle (author vs. dispatch), not the same problem duplicated.

_Triaged 2026-09-08 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jump-skills](https://github.com/fabricioctelles/jump-skills) | skill | Meta-skill router (MIT) that reads a task description and loads the single best-matching specialized skill from a curated library | Hundreds of installed skills means manually searching for the right one per task | Only-Skill-You-Need, skill-creator, skills-hub |
