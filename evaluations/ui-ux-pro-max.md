# Evaluation: ui-ux-pro-max

**Repo:** [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
**Stars:** 93,883 | **Last updated:** 2026-04-03 (pushed) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (build/refine frontend UI) + Review (UI quality/a11y audit)
**Layer:** Process (design knowledge + rules) with a Tooling component (Python search/reasoning engine + validators)

---

## What it does

Catalog one-liner: "Design intelligence for professional UI/UX across platforms." The mechanism is a **searchable design-knowledge database fronted by a reasoning engine**, not just a prompt. The flagship feature (v2) is a "Design System Generator": from a one-line brief ("build a landing page for a beauty spa") it runs ~5 parallel searches over bundled datasets — 161 product types, 67 UI styles, 161 color palettes, 24 landing-page patterns, 57 font pairings — ranks results (the README cites BM25), filters industry-specific anti-patterns, and emits a tailored design system: recommended pattern, style, color tokens, typography pairing with Google Fonts links, key effects, an "AVOID" anti-pattern list, and a pre-delivery checklist.

Structurally it is a **bundle of 7 Claude Code skills** under `.claude/skills/`: `ui-ux-pro-max` (the core design-intelligence skill), plus `brand`, `design`, `design-system`, `ui-styling`, `slides`, and `banner-design`. The core `SKILL.md` carries a priority-ordered rule taxonomy (10 categories, Accessibility/Touch/Performance ranked CRITICAL→LOW) with concrete, checkable rules: contrast ≥4.5:1, touch targets 44×44pt / 48×48dp, CLS <0.1, animation 150–300ms, base 16px / line-height 1.5, SVG-not-emoji icons, `prefers-reduced-motion`, semantic color tokens. The datasets and reasoning live in Python/CJS scripts (`generate-slide.py`, `search-slides.py`, `html-token-validator.py`, token validators, `extract-colors.cjs`), and there is a `uipro-cli` npm package. Installs as a Claude Code marketplace plugin (`.claude-plugin/plugin.json`, v2.5.0) or via the CLI. It explicitly scopes itself OUT of backend/API/DevOps/non-visual work.

## How we tested it

**Evidence:** REVIEW

Source-grounded review over the GitHub API. I did **not** install the skill, run the CLI, invoke the Design System Generator, or generate any UI; I produced no before/after output. I confirmed the canonical repo (disambiguated from ~20 forks/translations/demos via `gh search repos`), pulled repo metadata, walked the full file tree, read the plugin manifest, read the README head (Design System Generator section + pipeline diagram), and read the core `ui-ux-pro-max/SKILL.md` (when-to-apply gates + the full priority rule taxonomy and Quick Reference rules). Counts (67 styles, 161 palettes, 57 pairings, 99 UX rules) are the repo's own claims as stated in `plugin.json`, `skill.json`-adjacent metadata, and `SKILL.md`; I did not independently audit each dataset row or measure ranking quality. Calibrated against `evaluations/impeccable.md` (CONDITIONAL) and `evaluations/taste-skill.md` (CONDITIONAL), the two other frontend-design-cluster evals.

```bash
gh search repos ui-ux-pro-max --json fullName,description,stargazersCount,url   # disambiguate canonical from forks
gh api repos/nextlevelbuilder/ui-ux-pro-max-skill --jq '{description,stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at,created:.created_at,homepage}'
gh api "repos/nextlevelbuilder/ui-ux-pro-max-skill/git/trees/HEAD?recursive=1" --jq '.tree[] | "\(.type)\t\(.size)\t\(.path)"'
gh api "repos/nextlevelbuilder/ui-ux-pro-max-skill/git/trees/HEAD?recursive=1" --jq '.tree[] | select(.path|endswith("SKILL.md")) | .path'   # -> 7 skills
gh api "repos/nextlevelbuilder/ui-ux-pro-max-skill/contents/.claude-plugin/plugin.json" --jq '.content' | base64 -d
gh api "repos/nextlevelbuilder/ui-ux-pro-max-skill/contents/README.md"                       --jq '.content' | base64 -d
gh api "repos/nextlevelbuilder/ui-ux-pro-max-skill/contents/.claude/skills/ui-ux-pro-max/SKILL.md" --jq '.content' | base64 -d
grep -in "ui-ux-pro-max\|nextlevelbuilder" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Concrete, checkable rules ranked by impact.** The 10-category taxonomy is priority-ordered with explicit thresholds (contrast 4.5:1, touch 44×44pt, CLS <0.1, motion 150–300ms, base 16px) and paired anti-patterns. This is the format an LLM can apply deterministically — the same strength impeccable and taste-skill earn — and the a11y/touch coverage is unusually thorough (VoiceOver labels, Dynamic Type, safe-area awareness, drag thresholds).
- **Knowledge breadth and platform reach.** 161 product types and 67 styles across 15 stacks (React, Next.js, Vue, Svelte, Astro, SwiftUI, React Native, Flutter, Jetpack Compose, Tailwind, shadcn/ui) is broader than impeccable or taste-skill, and it explicitly covers **native mobile** (iOS HIG, Material) where the others are web-centric.
- **Retrieval-based recommendation, not just a prompt.** The Design System Generator picks style/palette/typography from a curated database via search+ranking, so output is anchored to vetted combinations rather than free-form model taste. This is a genuinely different mechanism from a pure rules prompt.
- **Clean scoping gates.** SKILL.md spells out Must-Use / Recommended / Skip with a one-line decision criterion ("if it changes how a feature looks, feels, moves, or is interacted with"). Good triggering hygiene that limits firing on backend work.
- **Strong provenance and traction.** 93.9K stars (the most-starred entry in the whole frontend-design cluster), MIT, named maintainer org, dedicated docs site (uupm.cc), `uipro-cli` on npm with download metrics, and a large fork/translation ecosystem. Not abandonware.

## What didn't work or surprised us

- **No deterministic anti-pattern detector + edit hook.** This is the key gap versus impeccable. ui-ux-pro-max ships token validators and an HTML token validator, but the anti-pattern "AVOID" lists are model-applied guidance, not a 44-rule no-LLM detector that re-runs after every UI edit. impeccable closes the inner/outer loop; ui-ux-pro-max mostly informs the first draft.
- **Heavy, multi-skill footprint.** Seven skills plus large Python/CJS scripts and CSV datasets (slide generators, color extractors, token validators) is a meaningfully larger install than a single design prompt, and several bundled skills (slides, banner-design) are off-topic for general frontend work.
- **Counts are self-reported and version-inconsistent.** README/badges and the two manifests disagree (50+ vs 67 styles; "161 reasoning rules" badge vs 99 UX guidelines vs 161 palettes). The numbers are marketing-forward and I did not audit dataset quality or ranking relevance.
- **Subjective, unverifiable quality signal.** As with the whole cluster, "professional design" has no objective check beyond the a11y/contrast/CLS rules; recommendation quality (does BM25 pick the *right* palette?) is unmeasured here.
- **Direct overlap with the cluster.** It targets the same gap as impeccable, taste-skill, frontend-design, garden-skills, open-design, huashu-design, and baoyu-design — "AI generates generic/ugly UI." This is a consolidation question, not an independent adopt.
- **Donation/monetization-forward repo.** Heavy PayPal/cross-promo framing in the README; benign, but a maintenance-incentive signal worth noting.
- **Not verified hands-on.** Verdict rests on reading the skill structure and the maintainer's claims, not measured output.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | For frontend work the contrast/touch/CLS/focus rules and a11y audit catch real defects (sub-4.5:1 text, <44px targets, layout shift); no effect outside the frontend |
| Speed | + | One-pass generation of a tailored design system (style + palette + type + checklist) beats hand-deriving them, for the greenfield-frontend slice; review/audit passes cost time |
| Maintainability | + | Pushes semantic color tokens, a design-system map, and consistency rules toward a documented system rather than one-off styles |
| Safety | neutral | Prompt + local Python/CJS scripts (token/HTML validators, color extraction); no credentials or network calls implied, but a larger local-script execution surface than a prose-only skill |
| Cost Efficiency | - | Seven skills plus datasets and on-invoke reference loads are a large context/footprint; justified only when a polished frontend is the deliverable |

## Verdict

**CONDITIONAL**

ui-ux-pro-max is the most-starred and broadest-knowledge entry in the frontend-design cluster: a curated design-knowledge database (styles, palettes, font pairings, product types) plus a search/reasoning Design System Generator, a concrete impact-ranked rule taxonomy with strong accessibility and **native-mobile** coverage, and clean when-to-use gates. Provenance is excellent (93.9K stars, MIT, docs site, npm CLI, active ecosystem).

Adopt it **when the project has a real frontend** — and especially when you want curated style/palette/typography *recommendations* up front, or you target iOS/Android as well as web (its mobile coverage exceeds impeccable and taste-skill). It is dead weight on backend/CLI/library work, it is a heavier multi-skill install than the alternatives, and it overlaps directly with the rest of the cluster.

**Additive vs redundant (cluster keep decision):** Against **impeccable** (strongest of the cluster — concrete refusable rules + a deterministic 44-rule detector + edit-time hook closing the inner/outer loop), ui-ux-pro-max is **partially additive, not a replacement**. impeccable wins on enforcement/verification (no-LLM detector + hook); ui-ux-pro-max wins on **recommendation breadth and mobile/native reach**. Against **taste-skill** (greenfield/marketing-grade web aesthetics, GSAP-coupled, v2 experimental), ui-ux-pro-max is **largely redundant and broader** — both are model-applied design guidance with no deterministic detector, and ui-ux-pro-max covers more product types, stacks, and platforms while being less opinionated about a specific motion library.

**Recommended keep:** if consolidating to one, keep **impeccable** for the verification loop; keep **ui-ux-pro-max** as the second pick when you need curated design-system recommendations or native-mobile coverage. taste-skill is the most droppable of the three (narrowest scope, experimental default, weakest distinct value once these two are present). Not a universal-default-stack pick — most repos aren't frontend-heavy — but default-grade for frontend-focused work. The existing CATALOG.md entry (line 145) is accurate and needs no change.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | skill | Design intelligence for professional UI/UX across platforms — curated styles/palettes/fonts + reasoning engine, strong a11y and native-mobile coverage | AI generates ugly or generic UIs without design guidance | impeccable, taste-skill, frontend-design plugin |
