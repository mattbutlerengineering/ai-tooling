# Evaluation: marketingskills

**Repo:** [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills)
**Stars:** 34,093 | **Last updated:** 2026-06-17 (pushed; created 2026-01-15) | **License:** MIT
**Dev loop stage:** Outside the software dev loop — it targets a *marketing* workflow (CRO, copy, SEO, ads, lifecycle, GTM), not Plan/Implement/Verify/Review/Ship/Reflect on code. The closest overlap with our loop is "growth engineering" tasks (programmatic SEO pages, schema markup, free-tool builds) where a marketer-developer writes code, but the skills themselves coach *marketing decisions*, not code quality.
**Layer:** Process (a portable collection of `SKILL.md` instruction files installed into any Agent-Skills-compatible tool; no runtime, no executing code)

---

## What it does

The catalog one-liner: "Marketing skills: CRO, copywriting, SEO, analytics, growth engineering." As inspected, it ships **45 `SKILL.md` files** organized (per the README's diagram) into eight families — SEO & Content, CRO, Content & Copy, Paid & Measurement, Growth & Retention, Sales & GTM, and Strategy — all hanging off one foundational `product-marketing` skill that every other skill reads first to load the product's audience and positioning. Each skill is a self-contained markdown prompt: identity ("You are a conversion rate optimization expert"), a check for `.agents/product-marketing.md` context, and a step-by-step analysis framework (e.g. the `cro` skill walks value-prop clarity → friction → social proof in impact order).

The mechanism is install-and-trigger, not orchestration. Skills are installed via `npx skills add coreyhaines31/marketingskills` (or the `.claude-plugin/marketplace.json` for Claude Code/Cursor/Windsurf/Codex), and the agent auto-loads the relevant one when a marketing task is detected by the `description` trigger phrases. Skills *cross-reference* each other (copywriting ↔ cro ↔ ab-testing; seo-audit ↔ schema ↔ ai-seo) but there is no coordinator — it's a dependency map the model follows, not a router. Notably, **43 of 45 skills ship an `evals/evals.json`**, plus `references/` files (templates, platform specs, checklists) — a more disciplined skill-authoring setup than most domain collections in this catalog.

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill was installed via `npx skills`, no marketplace was added, and no marketing task was executed in any tool. Every claim comes from the repository (GitHub metadata, README, full recursive file tree, one sampled `SKILL.md`), not from observed agent behavior. The "proven frameworks / best practices" language is the author's README framing, not anything measured here.

```bash
gh api repos/coreyhaines31/marketingskills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/coreyhaines31/marketingskills/readme --jq '.content' | base64 -d | head -120
gh api "repos/coreyhaines31/marketingskills/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api "...trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|endswith("SKILL.md"))]|length'    # 45 skills
gh api "...trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|endswith("evals.json"))]|length'   # 43 eval files
gh api repos/coreyhaines31/marketingskills/contents/skills/cro/SKILL.md --jq '.content' | base64 -d | head -30
gh api repos/coreyhaines31/marketingskills/contributors --jq '[.[].login]|length'   # 23
```

## What worked

- **Eval-backed skills are a real differentiator.** 43 of 45 skills carry an `evals/evals.json`, which is rare for a domain skill pack — it signals the author tests trigger accuracy and behavior, not just dumps prompts. This is more rigorous authoring than baoyu-design, obsidian-skills, or AlphaGBM/skills offer.
- **Coherent architecture, not a flat dump.** The `product-marketing` foundation + cross-references give the collection a real shared-context design; skills know to read positioning before acting, so output isn't generic.
- **Genuinely well-written domain frameworks.** The sampled `cro` skill is a clean, impact-ordered analysis framework with `references/` templates — useful as a *reference for how to write a good skill*, independent of the marketing content.
- **Broad reach and traction.** 34K stars, ~5.6K forks, 23 contributors, issue/PR templates, and a `sync-skills.yml` CI workflow that keeps the README's skill table in sync. Installs into Claude Code, Codex, Cursor, Windsurf via the universal Agent-Skills spec.

## What didn't work or surprised us

- **It is out of scope for a software-dev catalog.** The job-to-be-done is marketing (write ad copy, audit a landing page, plan a launch), not producing or improving code. Even the "growth engineering" skills (programmatic-seo, schema, free-tools) coach marketing strategy with code as a byproduct — they don't move Correctness/Maintainability of a software project.
- **Heavily commercial framing.** The README is dense with `?ref=marketingskills` affiliate links to the author's agency, course, newsletter, and an autonomous "CMO" product. The skills are MIT and free, but the repo is also a funnel — worth noting for trust calibration.
- **No releases / versioning of the set.** Skills carry an internal `version:` in frontmatter (cro is 2.0.0), but the repo has 0 tagged releases — you install whatever `main` is.
- **"Proven / best practices" is author framing.** The evals test behavior, but the marketing efficacy claims ("better conversions") are not substantiated by anything in the repo; they're domain copy.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | For *software* correctness, no effect — these skills judge marketing copy/pages, not code. (Within marketing, the eval-backed frameworks plausibly sharpen output.) |
| Speed | neutral | Speeds up *marketing* tasks for a marketer-developer; irrelevant to coding throughput. |
| Maintainability | neutral | Pure markdown instructions; no effect on a codebase's maintainability. |
| Safety | + | No code executes — markdown-only, no network/host reach. Lowest-risk install class. The only caveat is the commercial-funnel framing, not a technical risk. |
| Cost Efficiency | neutral | Per-task token cost of loading one focused skill; no structural cost effect on dev work. |

## Verdict

**SKIP for the core software-dev workflow — CONDITIONAL if you do your own marketing.** marketingskills is a well-architected, eval-backed, genuinely useful skill pack — but for *marketing*, not software development. It does not intervene at any dev-loop stage and moves none of our code-quality signals. The right audience is the solo founder / technical marketer who already lives in Claude Code and wants the same agent to also draft a landing page or audit SEO. For that person it's a strong CONDITIONAL adopt (the eval discipline and `product-marketing` foundation make it better than most domain packs). For a software team optimizing the dev loop, SKIP — it's adjacent, not in scope.

Compared to neighbors: it is the **best-authored domain collection in this row** (43 eval files vs. zero for baoyu-design, obsidian-skills, AlphaGBM/skills), but like all of them it's domain-specific and outside core dev. **claude-seo** overlaps directly on the SEO subset and is similarly out-of-scope; **pm-skills** is the closest sibling (a marketplace of business-function skills) and is more dev-relevant only because of its `pm-ai-shipping` plugin. marketingskills has no such bridge into code.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [marketingskills](https://github.com/coreyhaines31/marketingskills) | skill | 45 eval-backed marketing skills (CRO, copy, SEO, ads, lifecycle, GTM) on a shared product-marketing foundation, installable into any Agent-Skills tool | Want an AI agent to do marketing work (audit a page, write copy, plan a launch) with proven frameworks rather than generic text | claude-seo (SEO subset); pm-skills (sibling business-function skill marketplace) — both domain-specific, outside core dev |
