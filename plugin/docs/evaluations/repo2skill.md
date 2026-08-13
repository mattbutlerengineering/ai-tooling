# Evaluation: repo2skill

**Repo:** [Hhhkarimi/repo2skill](https://github.com/Hhhkarimi/repo2skill)
**Stars:** 3 | **Last updated:** 2026-08-12 (pushed) | **License:** MIT
**Last verified:** 2026-08-13
**Last triaged:** 2026-08-13  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (authoring skills — the tools the loop itself uses)
**Layer:** Tooling

---

## What it does

A browser-first web app that turns any public GitHub repository into repository-native Agent
Skills for ChatGPT and Claude — no AI API key required. Point it at a repo and it generates a
`SKILL.md` (and supporting files) capturing that codebase's own conventions, rather than a
generic skill written by hand.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy
with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers
directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `skill-creator` (already ADOPT, MEASURED). `skill-creator` is the
first-party, evaluated tool for this exact job — authoring a `SKILL.md` — with a
draft→eval→benchmark→triggering-optimization→package methodology this brand-new, 3-star tool
does not yet demonstrate. repo2skill's differentiator (auto-generate from an existing repo,
no AI API) is real but narrow; `skill-creator` already covers the job in STACK, and a second
tool for it earns nothing without evidence it does the job better.

_Triaged 2026-08-13 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [repo2skill](https://github.com/Hhhkarimi/repo2skill) | tool | Browser-first generator (MIT) turning any public GitHub repo into repository-native Agent Skills, no AI API required | Hand-writing a SKILL.md for a codebase's own conventions is manual; want one generated straight from the repo | skill-creator, Skill_Seekers, SkillOpt |
