# Evaluation: taste-skill

**Repo:** [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
**Stars:** 47,011 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Implement (frontend UI code generation); touches Plan when used for image-reference boards
**Layer:** Process

---

## What it does

Catalog one-liner: "gives your AI good taste; stops the AI from generating boring, generic slop." The important correction up front: **this is a frontend/UI design-taste skill collection, not a prose-quality skill.** The catalog pairs it with stop-slop and humanizer ("AI-written text reads as AI-written"), but taste-skill's actual target is *AI-built interfaces that look templated* — weak layout, default typography, no motion, generic spacing. Its README subtitle is literally "The Anti-Slop Frontend Framework for AI Agents." The "slop" it fights is visual, not verbal.

The mechanism is a bundle of ~13 portable Agent Skills (SKILL.md files) installable via `npx skills add`, framework-agnostic across Claude Code, Codex, and Cursor. Three buckets:

- **Implementation skills (output code):** `taste-skill` (the v2 default, install name `design-taste-frontend`) is an 87 KB SKILL.md that reads the brief, infers a design language, tunes three 1–10 dials (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY), and emits frontend code with a design-system map, canonical GSAP motion skeletons, a hard em-dash ban, a redesign-audit protocol, and a strict pre-flight check. Style variants ship as separate skills: `soft-skill`, `minimalist-skill` (Notion/Linear), `brutalist-skill` (Swiss type), `gpt-taste` (stricter Codex variant), `redesign-skill` (audit-then-fix existing UI), `stitch-skill` (Google Stitch rules).
- **Image-generation skills (output images only, no code):** `imagegen-frontend-web`, `imagegen-frontend-mobile`, `brandkit` — produce reference comps to feed back into a coding agent.
- **`output-skill`** (install name `full-output-enforcement`) is the outlier and the only prose-adjacent member: it bans truncation/placeholder patterns (`// ...`, `// TODO`, "for brevity", skeleton-instead-of-implementation) and enforces complete output. This is an anti-laziness skill, not a taste skill, and is the only piece relevant to general (non-frontend) agent work.

## How we tested it

Source-grounded review. I did not install the skills or generate any UI with them. Working over the GitHub API I pulled repo metadata, the full file tree, and read the README, `skills/llms.txt` (the maintainer's own one-line summary of every skill), `skills/output-skill/SKILL.md` in full, the plugin manifest, and the CHANGELOG. The two largest SKILL.md files (the 87 KB v2 `taste-skill` and the 40 KB imagegen skills) I characterized from the maintainer's `llms.txt` descriptions and README skill table rather than reading in full, given their size. The Floria example images in the repo are the maintainer's own outputs, not anything I produced. No dials were tuned, no code generated; every judgement below is reasoning about the skill design and surface, not a measured result. Calibrated against the sibling `evaluations/stop-slop.md` (CONDITIONAL).

```bash
gh search repos taste-skill --json fullName,description,stargazersCount,url   # disambiguate the many forks
gh api repos/Leonxlnx/taste-skill --jq '{stars:.stargazers_count,license:.license.spdx_id,description,pushed,created}'
gh api "repos/Leonxlnx/taste-skill/git/trees/HEAD?recursive=1" --jq '.tree[] | "\(.type)\t\(.size)\t\(.path)"'
for f in README.md skills/output-skill/SKILL.md skills/llms.txt .claude-plugin/plugin.json CHANGELOG.md; do
  gh api "repos/Leonxlnx/taste-skill/contents/$f" --jq '.content' | base64 -d
done
grep -inE "taste-skill|humanizer|stop-slop" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **It targets a real and underserved defect: AI frontends look generic.** Default LLM UI output gravitates to centered hero + three cards + system font. A skill that pushes layout variance, intentional typography, and motion attacks a genuine quality gap that no purely-prose skill (stop-slop, humanizer) touches.
- **The dials are a good design.** DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY as 1–10 knobs give the agent a tunable, restatable contract instead of "make it look nice." That is the format an LLM can actually act on, the same strength stop-slop's deny-lists have.
- **Specialization over a monolith.** Shipping `minimalist`, `brutalist`, `soft`, and `redesign` as separate one-job skills (install only what you need) matches Agent Skills best practice and keeps each skill's footprint scoped to the chosen visual direction.
- **`output-skill` is independently useful and the most portable piece.** Its anti-truncation deny-list (`// ...`, "for brevity", skeleton-instead-of-implementation) is a real failure mode for any code-gen agent, frontend or not — the one member of the bundle that earns consideration outside frontend work.
- **Strong provenance.** 47K stars, MIT, named maintainer, Vercel OSS sponsorship, a detailed CHANGELOG documenting the v1→v2 rewrite, framework-agnostic install via the vercel-labs `npx skills add` CLI. Not abandonware; actively iterating toward a v2.0.0 stable.

## What didn't work or surprised us

- **It is miscategorized relative to its catalog siblings.** stop-slop and humanizer fix *prose*; taste-skill fixes *UI*. They share the word "slop" and nothing else. The "Overlaps with" pairing is misleading — the only genuine prose overlap is the small `output-skill` member, and even that is anti-laziness, not de-AI-ing prose.
- **Subjective, hard-to-verify quality signal.** "Good taste" and "premium" are aesthetic claims with no objective check. The skill cannot tell you whether its output is *correct*, only whether it followed style rules. The Floria examples are self-selected showcases.
- **Heavy and opinionated.** The v2 default SKILL.md is 87 KB — a large always-loaded or on-invoke footprint, and it bakes in specific choices (GSAP as the motion library, a hard em-dash ban) that may fight a project's existing stack or design system.
- **The v2 default is self-described as experimental.** README and `llms.txt` both flag `design-taste-frontend` as "v2 (experimental)... actively iterating toward v2.0.0 stable," with v1 preserved as a fallback. Adopting the default means adopting a moving target.
- **Narrow to greenfield/marketing-style frontends.** The aesthetic is Awwwards/landing-page polish (motion, asymmetry, hero sections). For internal tools, dashboards, or back-end-heavy work it adds little, and for a repo with an established design system its opinions are noise.
- **Not verified hands-on.** Verdict rests on reading the skill structure and the maintainer's descriptions, not on generated UI. The two largest SKILL.md files were summarized from `llms.txt`, not read in full.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Operates on visual style, not behavior; `output-skill`'s no-placeholder rule marginally helps code completeness, but the bundle moves no functional-correctness signal |
| Speed | + | Generating a non-generic UI in one pass beats hand-tuning layout/typography/motion after a generic first draft — for the greenfield-frontend slice |
| Maintainability | neutral | Opinionated, GSAP-coupled output can clash with an existing design system; helps only when starting fresh, and the v2-experimental churn cuts the other way |
| Safety | neutral | Prompt-only skills, no permissions or new attack surface; worst case is off-brand or over-animated UI |
| Cost Efficiency | - | The 87 KB v2 SKILL.md is a large context load when invoked; justified only when a polished frontend is the actual deliverable |

## Verdict

**CONDITIONAL**

taste-skill is well-built and addresses a real gap — AI-generated frontends that look templated — which is a *different* gap from its catalog siblings stop-slop and humanizer (those fix prose; this fixes UI). Its dials, one-job specialization, and provenance (47K stars, MIT, Vercel-sponsored, active CHANGELOG) are genuine strengths. But its surface is narrow (greenfield/marketing-grade frontends), its quality signal is subjective and unverifiable, its default v2 skill is large and self-described as experimental, and its opinions (GSAP, em-dash ban) can fight an existing design system.

Adopt it **when the deliverable is a new, polish-grade frontend an agent is building from scratch** — landing pages, portfolios, marketing sites — and pick a single style variant (`minimalist`, `soft`, `brutalist`) rather than the experimental v2 default if predictability matters. Skip it for dashboards, internal tools, back-end work, or any repo with an established design system. The standout member for general code-gen agents is the small `output-skill` (anti-truncation), which is worth lifting independently of the design bundle. It does not belong in the default code stack; it belongs in a frontend-engineer's toolkit reached for at Implement time. Note for catalog hygiene: the "Overlaps with" pairing (stop-slop, humanizer) is weak — this is a UI-taste tool, not a prose tool.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [taste-skill](https://github.com/Leonxlnx/taste-skill) | skill | Anti-slop frontend design skills (layout, typography, motion, spacing) with tunable variance/motion/density dials, plus image-gen and anti-truncation variants | AI-built UIs look generic and templated | humanizer, stop-slop (weak — those target prose; this targets UI) |
