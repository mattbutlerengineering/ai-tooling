# Evaluation: frontend-slides

**Repo:** [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)
**Stars:** 22,282 | **Last commit:** 2026-06-13 | **Created:** 2026-01-28 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect (outer loop)
**Layer:** Tooling

---

## What it does

A coding-agent skill that generates zero-dependency HTML presentations — either from scratch or by converting an existing `.pptx`. Output is single HTML files with inline CSS/JS, a fixed 1920×1080 16:9 stage, and CSS-only animations. The headline pitch is "show, don't tell": instead of asking the user to articulate design preferences, the skill generates several visual style previews and lets the user pick. It is packaged as a Claude Code plugin (`/frontend-slides:frontend-slides`) but the core `SKILL.md` is written to be portable to Codex, Kimi Code, OpenCode, Gemini CLI, and other agents with filesystem/shell access.

The skill leans hard on anti-"AI slop" aesthetics: the `SKILL.md` explicitly warns the agent away from Inter/Roboto/Arial, purple-on-white gradients, and cookie-cutter layouts, and ships a `STYLE_PRESETS.md`, a `bold-template-pack/`, `viewport-base.css`, `html-template.md`, and `animation-patterns.md` loaded via progressive disclosure. Helper scripts cover PPTX extraction (`extract-pptx.py`), PDF export, and deploy.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — we did not install or run the skill. We pulled metadata, README, and the `SKILL.md` header via the GitHub API, and read it against the existing slide-tooling evaluations in this repo (slidev, powerpoint, pitch-deck-skill).

```
gh api repos/zarazhangrui/frontend-slides --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/zarazhangrui/frontend-slides/readme --jq '.content' | base64 -d | head -120
gh api repos/zarazhangrui/frontend-slides/contents/SKILL.md --jq '.content' | base64 -d | head -40
```

This tool is already a catalog entry (skill, line 188). This evaluation upgrades the prior discovery-log row to a full hands-off assessment.

## What worked

- **The "show, don't tell" loop is the right interaction model.** Generating three visual previews and letting the user pick beats asking a non-designer to describe an aesthetic in words. It is a genuinely better UX than the abstract-prompt approach most slide skills use.
- **Zero-dependency single-file HTML output is portable and durable.** No npm, no build step, no framework runtime — the deck is one file you can email, host, or open offline. Lower operational surface than slidev's per-deck pnpm project.
- **The anti-slop design guidance is unusually concrete.** The `SKILL.md` names specific fonts and color cliches to avoid and pushes for distinctive typography/motion — the same editorial stance as guizang-ppt-skill and huashu-design, but baked directly into the prompt.
- **PPTX conversion is a real migration path.** Extracting text, images, and notes from an existing deck and re-rendering it as web slides covers the "I already have a PowerPoint" case that pure from-scratch generators miss.
- **Cross-agent portability is designed in, not accidental.** The README documents how Codex/OpenCode/Gemini agents can consume the same `SKILL.md`, and the plugin layer is additive rather than required.
- **22.3K stars and a June 2026 commit** — actively maintained and broadly adopted, not a weekend project.

## What didn't work or surprised us

- **Heavy crowding in this category.** The catalog already holds slidev, open-slide, powerpoint, guizang-ppt-skill, and huashu-design. frontend-slides overlaps most directly with guizang-ppt-skill (HTML decks with distinctive editorial layouts) — the differentiator is the visual-preview selection loop, not the output format.
- **Output is HTML, not `.pptx`.** Unlike slidev (which exports PPTX) or the powerpoint skill, the primary artifact is a web page. For corporate environments that require an editable `.pptx`, this is the wrong tool — PPTX is an input here, not an output.
- **Fixed 16:9, no reflow — by design, but limiting.** The "non-negotiable" fixed stage means slides do not adapt to phones; they scale as a whole. Fine for presenting, awkward for mobile reading.
- **Quality depends on the agent's frontend taste.** The skill is essentially a high-quality prompt + asset pack; the anti-slop result is only as good as the underlying model's design execution. No deterministic guarantee.
- **Marginal dev-loop relevance.** Like all slide tooling, it lives at the edge of the dev loop (Reflect — communicating results), not in Plan/Implement/Verify/Review/Ship.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Slide tooling — no effect on code correctness |
| Speed | + | Visual-preview selection and single-file output are faster than authoring a deck by hand or in slidev's per-deck project |
| Maintainability | neutral | Single HTML file is portable but not as diff-friendly as slidev's Markdown; no real code-maintenance impact |
| Safety | + | Zero dependencies, runs fully local in a browser, no external service |
| Cost Efficiency | neutral | One generation pass costs tokens; no build infra, but redesign means re-running the agent |

## Verdict

**CONDITIONAL**

Reach for frontend-slides when you want an AI to *generate* a polished, distinctive web deck from a brief — especially for a non-designer who can pick a look but can't specify one — or to convert an existing `.pptx` into web slides. Its visual-preview loop is the strongest reason to pick it over guizang-ppt-skill, its closest neighbor. Skip it when you need an editable `.pptx` (use the powerpoint skill or slidev's PPTX export) or a code-heavy technical talk with magic-move animations and an embedded editor (use slidev). Within the already-crowded HTML-deck cluster it earns its slot on the strength of the selection UX and active maintenance, but it is not a clear winner over guizang-ppt-skill — choose by whether you value the preview loop (frontend-slides) or pre-baked editorial layouts (guizang-ppt-skill).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | skill | Zero-dependency HTML deck generator with a visual style-preview selection loop and PPTX-to-web conversion (22.3K stars) | Non-designers can't articulate an aesthetic, and want AI to build a distinctive deck rather than write code | guizang-ppt-skill, open-slide, slidev, powerpoint |
