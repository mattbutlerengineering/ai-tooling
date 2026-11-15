# Evaluation: solo-to-team-skills

**Repo:** [dabingfy-dot/solo-to-team-skills](https://github.com/dabingfy-dot/solo-to-team-skills)
**Stars:** 900 | **Last updated:** 2026-11-15 (pushed) | **License:** MIT
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Process

---

## What it does

A human-led multi-agent-system toolkit: 16 roles, 6 group templates, and four
platform bundles for coordinating several agent roles on one task, with
evidence-based review and a defined handoff checkpoint between roles.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide
whether this lead is redundant with a catalogued incumbent, not to judge the
tool's actual behavior — this eval offers no ADOPT/KEEP signal.

## Triage note

This lead cites `mattpocock/skills` (a STACK ADOPT pick) in its "Overlaps with"
cell, which bands it P2 challenger. But the overlap is thematic, not a genuine
redundancy: `mattpocock/skills` is a general engineering skill pack, while this
tool is a specific multi-agent-role coordination toolkit (roles, group
templates, platform bundles, evidence-based handoff) — a different, more
specific job. At 900 stars it is a significant, differentiated lead; SKIPping
it as "redundant" would be the mechanical-SKIP-on-weak-overlap mistake the
eliminate-only guardrail warns against. Left at `discovery-log` for a real
hands-on eval.

_Triaged 2026-11-15 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [solo-to-team-skills](https://github.com/dabingfy-dot/solo-to-team-skills) | skill | Human-led multi-agent-system toolkit (MIT) — 16 roles, 6 group templates, four platform bundles, evidence-based review and handoff | Coordinating several agent roles on one task has no shared role vocabulary, group template, or handoff checkpoint | mattpocock/skills, ECC, coleam00/skills |
