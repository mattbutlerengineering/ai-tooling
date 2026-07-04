# Evaluation: garden-skills

**Repo:** [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills)
**Stars:** 8,369 | **Last updated:** 2026-06-10 (pushed; created 2026-04-21) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Spans outer-loop *output/communication* work, not the core coding loop — Plan/Reflect (diagrams via web-design, knowledge retrieval) and Ship/communicate (presentations, articles, images). These are skills for producing polished deliverables *about* or *alongside* code, plus one retrieval skill that touches context.
**Layer:** Process (a multi-skill collection: each skill is a `SKILL.md` + `references/` + scaffold templates; the repo adds a Claude Code plugin marketplace, a `skills` CLI installer, per-skill release `.zip`s, and CI validation)

---

## What it does

The catalog one-liner — "Web design, knowledge retrieval, and image generation skills" — undersells it. As inspected, garden-skills is a **curated 5-skill collection** by ConardLi, polished and packaged with unusual production discipline. The five skills:

1. **web-video-presentation** — builds record-ready Vite + React + TS presentations that behave like video production surfaces (fixed 1920×1080 stage, `(chapter, step)` cursor, **23 built-in themes**, pluggable TTS with MiniMax + OpenAI providers). Turns scripts/articles into screen-recordable cinematic videos.
2. **web-design-engineer** — a six-step design workflow (requirements → context → design system → v0 → full build → verification) with an anti-cliché blocklist and **25 anchored style recipes** (Linear, Aesop, Bloomberg, Stripe Press, etc.), each with palette/typography/signature-moves.
3. **gpt-image-2** — image generation / prompting.
4. **kb-retriever** — a local knowledge-base retriever doing *progressive* search: navigates hierarchical `data_structure.md` indexes, bounds itself to ≤5 search rounds, handles Markdown/PDF/Excel, answers with sources without flooding context.
5. **beautiful-article** — an editorial harness that turns any source (URL/PDF/DOCX/notes) into a polished, share-ready article through a `source → plan → double-confirm → build → review` loop with hard human checkpoints.

The packaging is the other half of the story: a `.claude-plugin/marketplace.json`, a `skills` npx CLI (`npx skills add ConardLi/garden-skills -s gpt-image-2`), five install methods (CLI, marketplace, pinned `.zip` per skill, manual copy, submodule), 19 per-skill releases, trilingual docs (EN/中文/日本語), and CI (`validate-skills`, `release-skill`). This is a maintained, versioned skill garden, not a markdown dump.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Nothing was installed via the CLI or marketplace, no skill was activated, and no presentation/article/image/diagram was generated. Every claim comes from the repository (GitHub metadata, README, full file tree, per-skill README excerpts), not from observed behavior. Quality language ("beautiful," "production-grade," theme/recipe counts) is the author's README framing and the manifest's stated content, not anything I measured.

```bash
gh api repos/ConardLi/garden-skills --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/ConardLi/garden-skills/readme --jq '.content' | base64 -d
gh api "repos/ConardLi/garden-skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api "repos/ConardLi/garden-skills/git/trees/HEAD?recursive=1" --jq '.tree[]|select(.path|test("^skills/[^/]+$"))|.path'  # 5 skills
gh api repos/ConardLi/garden-skills/commits --jq 'length'    # 30 (page-1 cap)
gh api repos/ConardLi/garden-skills/releases --jq 'length'   # 19
```

## What worked

- **Exceptional packaging and maintenance discipline.** Five install paths, per-skill pinned `.zip` releases (19 of them), a plugin marketplace, a `skills` CLI, trilingual docs, and CI that validates and releases skills. Far above the typical "git clone into .claude/skills" project — you can install *one* skill at a stable version instead of the whole repo.
- **Curated and coherent, not a 200-file dump.** Five focused, individually documented skills, each with its own README, SKILL.md, references, and scaffold templates. Quality-over-quantity — the opposite of bloated mega-collections.
- **Genuinely opinionated craft.** web-design-engineer's anti-cliché blocklist + 25 anchored style recipes, and web-video-presentation's 23 themes, are concrete anti-slop machinery, not vague "make it pretty" prompts. This is the same lineage as the catalog's strong design skills.
- **kb-retriever is the most dev-relevant skill.** Bounded, progressive, source-cited retrieval over a local `knowledge/` directory that avoids context flooding — useful as a context/memory aid in the actual dev loop, distinct from the four output-oriented skills.
- **Strong, recent traction.** 8.4K stars and 1,136 forks in ~7 weeks, actively pushed, MIT-licensed — clean to vendor and adapt.

## What didn't work or surprised us

- **Mostly output/communication, not coding.** Four of five skills (presentations, articles, web-design artifacts, image generation) produce *deliverables about* work — decks, essays, landing pages — rather than improving the code itself. Valuable for devrel/docs/demos, peripheral to writing and shipping software.
- **The catalog one-liner is stale and incomplete.** "Web design, knowledge retrieval, and image generation" omits the two flagship skills (web-video-presentation, beautiful-article) that dominate the README. The entry needs updating to "curated 5-skill collection."
- **Heavy scaffolds and runtime deps.** web-video-presentation and beautiful-article scaffold full Vite + React + TS projects; TTS providers need API keys (MiniMax/OpenAI). These are real projects to run, not lightweight prompt skills — install footprint and cost rise accordingly.
- **Overlap with an already-crowded design cluster.** web-design-engineer competes directly with impeccable, ui-ux-pro-max, taste-skill, huashu-design, and open-design — the catalog's most saturated category. Its differentiator is the style-recipe gallery, but the marginal value over those is unproven.
- **Quality unverified here.** Theme/recipe counts and "production-ready" are README claims; no artifact was generated, so actual output quality and how well the human-checkpoint loops hold up are untested.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (for outputs) | kb-retriever answers with sources and bounds search; beautiful-article/web-design add verification/review steps. Affects deliverable correctness, not code correctness. |
| Speed | + | One-prompt generation of decks, articles, landing pages, and images is far faster than building each by hand; per-skill install avoids pulling the whole repo. |
| Maintainability | + / neutral | Repo itself is well-maintained (releases, CI, CLI); generated React/Vite scaffolds are full projects you then own and maintain. |
| Safety | − / neutral | Scaffolds run Node/Vite build chains; TTS/image skills call external APIs needing keys. More surface and external dependency than markdown-only skills. |
| Cost Efficiency | − / neutral | Multi-step, checkpointed build loops plus paid TTS/image APIs add token and API cost; justified for polished deliverables, not cheap. |

## Verdict

**CONDITIONAL — adopt kb-retriever and (in design-heavy contexts) web-design-engineer; treat the rest as on-demand deliverable tools.** garden-skills is one of the best-*packaged* skill collections in the catalog — curated to five focused skills, per-skill versioned releases, a CLI, a marketplace, CI, and trilingual docs — and the design/video/article skills carry genuine anti-slop craft. But four of five skills produce *outputs about* work (presentations, essays, web artifacts, images) rather than moving code through the loop, and they pull in heavy React/Vite scaffolds and paid TTS/image APIs. The clear dev-loop pick is **kb-retriever** (bounded, source-cited local retrieval). web-design-engineer is worth installing where polished web artifacts matter, but it lands in an already-saturated design cluster.

Compared to neighbors: its catalog "overlaps with" lists **impeccable** and **ui-ux-pro-max**, accurate only for the web-design-engineer slice — and there it also overlaps **taste-skill, huashu-design, baoyu-design, open-design**. As a *collection*, the closer analogue is a curated set like **vercel-labs/agent-skills** (9 focused, test-backed skills) — garden-skills matches the curation and packaging discipline but, unlike Vercel's, is not build/test-validated and skews toward output/communication rather than coding guidance. It is the inverse of bloated menus like agency-agents/antigravity-awesome-skills: small, opinionated, and individually installable.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [garden-skills](https://github.com/ConardLi/garden-skills) | skill | Curated 5-skill collection (web-video-presentation w/ 23 themes, web-design-engineer w/ 25 style recipes, gpt-image-2, kb-retriever, beautiful-article) with per-skill versioned releases, a `skills` CLI, plugin marketplace, and CI | Want a small, well-packaged set of polished output/design/retrieval skills you can install individually at a pinned version, not a bloated mega-collection | impeccable, ui-ux-pro-max, taste-skill, huashu-design (web-design slice); vercel-labs/agent-skills (curated collection); contrast agency-agents (bloated menu) |
