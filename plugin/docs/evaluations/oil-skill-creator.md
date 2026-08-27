# Evaluation: oil-skill-creator

**Repo:** [oil-oil/oil-skill-creator](https://github.com/oil-oil/oil-skill-creator)
**Stars:** 35 | **Last updated:** 2026-08-23 (pushed) | **License:** MIT
**Last verified:** 2026-08-27
**Last triaged:** 2026-08-27  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (authoring/improving the tools the loop itself uses)
**Layer:** Tooling

---

## What it does

A product-development-style workflow for authoring Agent Skills — create, review,
refine, and publish a SKILL.md through a structured loop rather than one-shot
hand-authoring.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's actual
output quality — a question this eval does not answer.

## Verdict

**SKIP** — redundant with [`skill-creator`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator), the STACK incumbent (ADOPT, MEASURED) for the same job: draft → eval → benchmark → triggering-optimization → package. `oil-skill-creator` covers the same create/review/refine/publish loop with far less evidence (35 stars, no benchmarking or measured-evidence claims) and no differentiating capability over the official, already-adopted tool.

## Triage note

`triage.py` places this in P2 challenger, citing `skill-creator` (a STACK pick) as
the incumbent. The overlap is real and direct — both are meta-tools for authoring
and refining Agent Skills — and `skill-creator` already carries a MEASURED,
ADOPT verdict as the first-party Anthropic tool with eval/benchmark/variance
tooling `oil-skill-creator`'s description does not claim to match. SKIPped per the
P2 disposition rather than left, since a second unvetted tool for a job the
incumbent already does well earns nothing.

_Triaged 2026-08-27 by the daily discovery pass (P2 challenger band)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [oil-skill-creator](https://github.com/oil-oil/oil-skill-creator) | tool | Product-style workflow (MIT) for creating, reviewing, refining, and publishing Agent Skills | Skills get hand-authored ad hoc with no review/refinement loop; want product-development discipline applied to skill authoring | skill-creator, Skill_Seekers, SkillOpt |
