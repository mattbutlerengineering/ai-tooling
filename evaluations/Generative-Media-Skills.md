# Evaluation: Generative-Media-Skills

**Repo:** [SamurAIGPT/Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills)
**Stars:** 3,754 | **Last updated:** 2026-06-22 (pushed) | **License:** MIT
**Dev loop stage:** Out of loop (media generation)
**Layer:** Tooling (agent skills)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Skills that give a coding agent image, video and audio generation, implemented as calls to the
muapi.ai hosted generation service.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the `CATALOG.md` one-liner and "Overlaps with" cell (`anthropics/skills`, `vercel-labs/agent-skills`,
`google/skills`). Enough to place and band it; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`. Two disposal grounds were considered and neither holds.

**Scope.** Media generation is about as far from the software dev loop as this section goes. But the
Skills & Plugins blurb is "Extensions that add domain-specific capabilities to coding agents", which
is deliberately broad, and a scope SKIP here would be the same mistake caught and reversed in the
design/presentation slice. Scope SKIPs were available in Security & Safety because *that* blurb is
narrow; they are not available here.

**Redundancy.** Its overlaps cell names three general skill collections (`anthropics/skills`,
`vercel-labs/agent-skills`, `google/skills`), none of which does media generation — the cell records
"other skill collections", not competitors. Nothing in the catalog covers this ground, so there is no
incumbent to be redundant with.

What a future eval must price is the dependency: the skills are a thin layer over **muapi.ai**, a
paid hosted service. That is the same funnel structure that decided `AlphaGBM/skills` in this slice —
but that one had a free, vendor-neutral sibling to be redundant *with*, and this one does not, so the
structure alone is not a disposal.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills) | skill | Multi-modal image/video/audio generation skills for coding agents, powered by muapi.ai | Coding agents lack built-in media generation; packages image/video/audio gen as installable skills | anthropics/skills, vercel-labs/agent-skills, google/skills |
