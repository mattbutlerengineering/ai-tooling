# Evaluation: huashu-design

**Repo:** [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)
**Stars:** 19,196 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A 631-line SKILL.md that transforms an AI coding agent into an HTML-native design studio. When invoked, the agent embodies a domain-specific expert (UX designer, animator, slide designer, or prototyper) depending on the task. Outputs include clickable app prototypes with real device bezels, presentation decks, timeline-driven animations exportable to MP4/GIF with BGM and 37 pre-built SFX, design variants with live tweaking, infographics, and 5-dimension design critiques.

The skill's distinctive mechanism is its "Design Direction Advisor" fallback — when user requirements are vague, three parallel logic systems (second-roulette random selection from 40 HTML-native styles, award-winning site migration, best-designer philosophy matching) each produce a real visual direction, not text descriptions. The 40-style library (20 web + 20 PPT) is derived from 100 real-world case studies with per-style "HTML reproducibility scores" (72%–98%) so the agent knows what it can and can't achieve without image generation.

The skill ships with 15 Python/Node scripts for video rendering, PPTX export, PDF generation, TTS narration pipelines, and Playwright verification. 20 reference documents cover animation pitfalls, brand asset protocols, cinematic patterns, audio design rules, and a launch-film director's notes workflow.

## How we tested it

**Evidence:** REVIEW

Architecture review of SKILL.md (631 lines), all 20 reference files, 15 scripts, and 50+ assets. Assessed the design-styles library methodology (100 real-world case studies → 40 categorized styles with reproducibility ratings). Compared the anti-AI-slop system against catalog competitors.

```bash
gh api repos/alchaincyf/huashu-design --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api "repos/alchaincyf/huashu-design/contents/SKILL.md" --jq '.content' | base64 -d
gh api "repos/alchaincyf/huashu-design/contents/references/design-styles.md" --jq '.content' | base64 -d
gh api "repos/alchaincyf/huashu-design/contents/references/critique-guide.md" --jq '.content' | base64 -d
```

Not hands-on tested (no design project available during evaluation), so this is an architecture-and-content review.

## What worked

- **Anti-AI-slop system is the most thorough in the catalog.** A structured table of 7 common AI visual clichés (purple gradients, emoji icons, rounded cards with left-border accent, SVG-drawn faces, GitHub-dark lazy solution) with "why it's slop" reasoning and "when it's actually OK" exceptions. No other design skill explains *why* defaults are bad — they just say "don't use defaults."
- **40-style library with reproducibility ratings** is genuinely novel. Each style has: temperature tag (bold/neutral/quiet), HTML reproducibility score (72%–98%), reference cases, visual DNA spec (exact hex colors, layout patterns, typography), font substitutions (all open-source), and implementation notes. The library is weighted toward bold styles to counteract LLM conservatism — a deliberate and smart design choice.
- **Fact-verification-first principle (核心原则 #0)** addresses a real LLM failure mode: the skill explicitly bans the agent from assuming product existence without WebSearch, citing a real incident where it wasted 2 hours making a "concept" animation for a product that had already launched 4 days earlier. This kind of incident-driven rule is rare and valuable.
- **Junior Designer workflow** (show assumptions first, iterate) is the right interaction model for design — preventing the 100x cost of late-discovered misunderstanding.
- **Real tooling depth:** 15 scripts covering video rendering at 25fps/60fps, PPTX export with editable text boxes, TTS narration pipeline with Doubao integration, SFX mixing, Playwright verification. These aren't stubs.
- **5-dimension critique system** (philosophy alignment, visual hierarchy, craft quality, content fitness, innovation) with 1-10 scoring rubrics provides structured design review that no other skill offers.

## What didn't work or surprised us

- **Primarily Chinese-language** — SKILL.md, all references, and the README are in Chinese. An English README exists but is a translation, not the primary voice. Non-Chinese-speaking users will rely on the agent's translation capability, adding latency and potential meaning loss.
- **Large context footprint** — 631-line SKILL.md plus 20 reference files loaded on demand. The progressive disclosure design (references loaded per task type) mitigates this, but a full animation task could load 3-4 reference files totaling 2,000+ lines.
- **Single release (v2.0)** — all development happened in a 2-month burst (April–June 2026). Long-term maintenance pattern is unclear. 2,375 forks suggest strong community interest but also risk of fragmentation.
- **Watermark insertion by default** on animation exports ("Created by Huashu-Design") is reasonable marketing but may surprise users in professional contexts. The opt-out is documented but requires explicit request.
- **No comparison against Claude Design (Artifacts)** — the README mentions the relationship but the evaluation couldn't assess whether this skill matches, exceeds, or falls short of Claude's native design capabilities in Artifacts.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Fact-verification-first principle prevents building on wrong assumptions; Playwright verify script catches visual regressions |
| Speed | + | 3-30 minute delivery for prototypes, slides, animations; direction advisor eliminates style-decision paralysis |
| Maintainability | + | Brand asset protocol ensures designs are grounded in real brand identity, not generic defaults |
| Safety | neutral | No security implications; watermark removal is opt-out |
| Cost Efficiency | - | Large context footprint (631-line SKILL.md + references) increases token cost per design session |

## Verdict

**CONDITIONAL**

Use when you need HTML-native design output (prototypes, slides, animations, infographics) and want to avoid AI-default aesthetics. The anti-slop system and 40-style library with reproducibility ratings are unmatched in the catalog — no other design skill provides this level of structured visual vocabulary. The Chinese-language primary documentation is the main barrier for non-Chinese teams; the design methodology itself is language-agnostic once loaded. Choose impeccable or frontend-design for simpler "make it look good" use cases; choose huashu-design when you need structured design direction, animation/video export, or 5-dimension critique.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [huashu-design](https://github.com/alchaincyf/huashu-design) | skill | HTML-native design skill — hi-fi prototypes, slides, animations, MP4 export, 20 design philosophies (19.2K stars) | Agents generate generic HTML without design quality; need structured design with evaluation dimensions | impeccable, ui-ux-pro-max, open-design |
