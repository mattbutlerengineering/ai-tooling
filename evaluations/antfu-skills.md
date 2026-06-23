# Evaluation: antfu/skills

**Repo:** [antfu/skills](https://github.com/antfu/skills)
**Stars:** 5,339 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A curated collection of 17 agent skills reflecting Anthony Fu's preferences and the Vue/Vite/Nuxt ecosystem. Three tiers of content:

1. **Hand-written** (`antfu`) — 144-line opinionated SKILL.md covering TypeScript conventions, ESLint config, pnpm catalogs, monorepo setup, and library publishing patterns. This is the "personal .claude/rules as a skill" pattern.
2. **Generated from docs** (`vue`, `nuxt`, `vite`, `vitest`, `unocss`, `pinia`, `pnpm`, `vitepress`) — skills auto-generated from official documentation repos via git submodules, then fine-tuned by Anthony. Each has a compact SKILL.md orchestrator (42–84 lines) with progressive-disclosure references (3–23 per skill).
3. **Vendored** (`slidev`, `tsdown`, `turborepo`, `vueuse-functions`, `vue-best-practices`, `vue-router-best-practices`, `vue-testing-best-practices`, `web-design-guidelines`) — synced from external repos that maintain their own skills.

The generation pipeline is documented in AGENTS.md and designed to be forkable — anyone can use it as a template to generate skill collections from their own documentation sources.

## How we tested it

**Evidence:** REVIEW

Read every SKILL.md and sampled reference files across all three tiers. Assessed the generation mechanism (AGENTS.md, meta.ts, git submodules), progressive disclosure architecture, and content quality against the core `antfu` skill and the generated `vue` and `nuxt` skills.

```bash
gh api repos/antfu/skills --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api "repos/antfu/skills/contents/skills/antfu/SKILL.md" --jq '.content' | base64 -d
gh api "repos/antfu/skills/contents/skills/vue/SKILL.md" --jq '.content' | base64 -d
gh api "repos/antfu/skills/contents/skills/nuxt/SKILL.md" --jq '.content' | base64 -d
gh api "repos/antfu/skills/git/trees/main?recursive=1" --jq '.tree[].path'
```

## What worked

- **Progressive disclosure is well-implemented**: compact SKILL.md orchestrators (42–144 lines) with rich reference libraries (up to 23 references for UnoCSS). Low context cost on initial load, deep knowledge available on demand.
- **The `antfu` core skill is high-quality opinionated content**: `@antfu/ni` command table, `fast-npm-meta` for version lookups, pnpm catalog conventions, TypeScript strict config — practical defaults a Vue/Vite developer actually needs.
- **Generation pipeline is the real innovation**: git submodule-based doc syncing with GENERATION.md provenance tracking (source SHA, generation date) means skills can stay current with upstream docs automatically.
- **Vendored skills bring in quality content without duplication**: `web-design-guidelines` (Vercel's), `slidev` (official), `vue-best-practices` (vuejs-ai) — assembled into one install command.
- **613 total files** across 17 skills — substantial depth, not marketing.

## What didn't work or surprised us

- **Exclusively Vue/Vite/Nuxt ecosystem**: no general-purpose engineering skills. If you don't use Vue, only `web-design-guidelines` and the general `antfu` conventions are relevant.
- **README explicitly says "proof-of-concept"**: "I haven't fully tested how well the skills perform in practice" — honest but reduces confidence.
- **Generated skills frozen at January 2026**: GENERATION.md shows `2026-01-28` for most generated skills — nearly 5 months old. Vue 3.5+ APIs may have evolved.
- **No install count data available**: can't assess actual adoption beyond star count.
- **The forkable template is more valuable than the skills themselves**: the pattern of "git submodule → generate → progressive disclosure SKILL.md" is the portable insight.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Vue/Nuxt/Vite skills reference correct APIs for their stated versions with progressive-disclosure depth |
| Speed | + | One `pnpx skills add antfu/skills --skill='*'` installs comprehensive Vue/Vite ecosystem knowledge |
| Maintainability | + | The `antfu` skill's conventions (type separation, pnpm catalogs, ESLint config) enforce clean project structure |
| Safety | neutral | No security-specific content |
| Cost Efficiency | + | Progressive disclosure keeps context costs low (~50–150 lines per skill upfront, references loaded on demand) |

## Verdict

**CONDITIONAL**

Use when working on Vue/Vite/Nuxt projects — it's the most comprehensive one-stop skill collection for that ecosystem, with 17 skills covering framework, tooling, testing, and conventions. The generation pipeline is independently valuable as a template for creating your own doc-sourced skill collections. Not useful outside the Vue ecosystem; general engineering skills are better served by mattpocock/skills (ADOPT) or agent-skills.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [antfu/skills](https://github.com/antfu/skills) | skill | Anthony Fu's curated agent skills collection | Want skills from a well-known open-source developer | mattpocock/skills, agent-skills |
