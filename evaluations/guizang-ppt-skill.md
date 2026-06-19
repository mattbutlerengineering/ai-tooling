# Evaluation: guizang-ppt-skill

**Repo:** [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)
**Stars:** 18,073 | **Last updated:** 2026-06-02 (pushed; created 2026-04-23) | **License:** AGPL-3.0
**Dev loop stage:** Outer-loop *artifact production* — Ship/Communicate, not a code stage. It turns prose/Markdown into a presentation. Tangential to the inner dev loop; it produces a deliverable, not code that ships to users.
**Layer:** Process — a single agent **Skill** (`SKILL.md` + HTML templates, reference docs, themes, a validation script) installed into Claude Code / Codex; no runtime service.

---

## What it does

A web-PPT skill for agent environments (Claude Code, Codex) that generates **single-file HTML horizontal-swipe decks**, slide imagery, and multi-platform cover images. Its differentiator is two opinionated, locked visual systems baked into the templates: **Style A — "electronic magazine × e-ink"** (Noto Serif + Playfair, fluid WebGL backgrounds, warm e-ink palettes; narrative/opinion decks) and **Style B — Swiss International** (grid-dominant, single high-saturation anchor color from IKB / lemon-yellow / lemon-green / safety-orange, hairline rules, extreme type-size contrast; product/data/methodology decks). Style A ships 10 layouts, Style B ships 22 "locked" versions (Cover, Statement, KPI Tower, Loop Diagram, Duo Compare, Image Hero, Closing Manifesto, etc.).

Mechanically it is a skill bundle: `SKILL.md` is the workflow, `assets/template.html` + `assets/template-swiss.html` are the deck shells, `references/` holds themes/layouts/components/checklist docs and a Swiss layout-lock spec, and `scripts/validate-swiss-deck.mjs` programmatically checks Swiss decks for layout, image slots, title alignment, and dangerous SVG. Decks support keyboard/scroll/touch/ESC-index navigation, Lucide icons, and Motion One entrance animation with a low-perf static fallback (press `B`). On Codex it can optionally call GPT-Image / GPT-M to generate documentary photos, infographics, and diagrams sized to template ratios, and reuse the same visual rules for WeChat 21:9, 1:1 share cards, Xiaohongshu 3:4, and Channels covers. The README is explicit about non-fit cases: dense tables, training courseware (not enough density), and multi-author collaborative editing (it is static HTML).

## How we tested it

**Source-grounded inspection — not installed, not run.** No `npx skills add` was executed, no deck was generated, no GPT-Image call made, and `validate-swiss-deck.mjs` was not run. Claims come from the repo (metadata, both READMEs, `SKILL.md`, file tree), not from a rendered deck. The "踩过的每一个坑都写进了 checklist.md" (every pitfall captured) and visual-quality claims are the author's framing plus the visible template/reference structure, not output I evaluated. The repo is primarily Chinese (`README.md` zh, `README.en.md` en).

```bash
gh api repos/op7418/guizang-ppt-skill --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/op7418/guizang-ppt-skill/readme --jq '.content' | base64 -d         # zh README; English at README.en.md
gh api repos/op7418/guizang-ppt-skill/contents/SKILL.md --jq '.content' | base64 -d  # two-style workflow, when-to-use
gh api "repos/op7418/guizang-ppt-skill/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # assets/, references/, scripts/
gh api repos/op7418/guizang-ppt-skill/commits      --jq 'length'   # 24
gh api repos/op7418/guizang-ppt-skill/releases     --jq 'length'   # 1
gh api repos/op7418/guizang-ppt-skill/contributors --jq 'length'   # 2 (effectively single-author)
```

## What worked

- **Opinionated, named design systems beat "make it pretty."** Style A and Style B are concrete aesthetic contracts (specific fonts, anchor colors, layout inventories) with explicit fit/non-fit guidance. This is the most useful thing a slide skill can give an agent — a constraint set, not a blank canvas — and it directly attacks generic AI-slop output.
- **A real validation script.** `scripts/validate-swiss-deck.mjs` programmatically checks layout, image slots, title alignment, and dangerous SVG. Most slide skills hand you a prompt and hope; an automated quality gate on the generated artifact is a genuine differentiator and a maintainability/safety win.
- **HTML-as-text is the right substrate for agents.** Single-file HTML is readable, diffable, and re-editable by the agent (the README argues this explicitly), with no build step or server. Easy to open, present, send, screenshot.
- **Honest scope.** The skill states where it does *not* fit (dense tables, courseware, collaborative editing) — rare candor that prevents misuse.
- **Funded and iterating.** Backed by 360 Security and a ZhenFund Token Grant, with a 22-layout Swiss system added since launch — active development, not a one-shot dump.

## What didn't work or surprised us

- **AGPL-3.0 is a real adoption hazard.** A copyleft license on a *skill that generates HTML you ship* raises questions most teams will not want to answer. The output is your deck, but the AGPL framing alone will deter corporate adoption — a sharper licensing risk than the permissive MIT/Apache of most neighbors.
- **Effectively single-author (2 contributors), pre-1.0 (1 release).** High star count (18K in ~2 months) reflects design-aesthetic virality and the author's (歸藏 / @op7418) following more than breadth of contribution. Bus-factor is one person.
- **Style-locked is a double edge.** The two systems are excellent *if* they match your need; there is no third register. For corporate/data-dense or branded-template work it actively says "use regular PPT."
- **Output is HTML, not `.pptx`.** Unlike `powerpoint`/`powerpoint-ppt`, you cannot hand the result to someone who needs to edit it in PowerPoint/Keynote. Static HTML only — no collaborative editing, by design.
- **Best imagery path is Codex-bound.** The GPT-Image/GPT-M figure-generation flow is gated to Codex; on Claude Code you get the layouts/themes but not the integrated image pipeline.
- **Chinese-first.** Primary docs and `SKILL.md` description are Chinese; the English README exists but is secondary. Minor, but worth flagging.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Produces presentations, not code; "correctness" maps to layout/visual fidelity, which the Swiss validation script partially enforces. No effect on a codebase. |
| Speed | + | Prose/Markdown to a polished, navigable deck in one pass with locked layouts beats hand-building slides; saves real design time for talk/launch decks. |
| Maintainability | + / neutral | Single-file HTML is agent-editable and diffable; the validation script keeps Swiss decks consistent. AGPL-3.0 is a maintainability/legal liability for shipped artifacts. |
| Safety | neutral / − | Generates static HTML — low runtime risk, and the validator screens dangerous SVG. AGPL-3.0 on shipped output is the real safety concern, not execution. |
| Cost Efficiency | neutral / − | Free skill, but rich WebGL templates + optional GPT-Image generation add token/compute cost per deck vs. a plain Markdown slide tool. |

## Verdict

**CONDITIONAL — adopt for talk/launch/personal-brand decks where its two styles fit and AGPL is acceptable; skip for corporate/.pptx/data-dense work.** guizang-ppt-skill is the most *design-opinionated* slide skill in the catalog: two named, internally-consistent visual systems plus an automated layout validator give an agent a genuine constraint set instead of a blank canvas, which is exactly what raises slide output above generic. The blockers are licensing (AGPL-3.0 on a skill that generates artifacts you ship) and fit — it deliberately excludes dense data, courseware, and collaborative editing, and it emits HTML, not `.pptx`.

Against neighbors: **frontend-slides** (CONDITIONAL) leans on the agent's own frontend skill with less prescriptive structure — more flexible, less designed. **slidev** is the developer/technical-talk standard (Markdown + code highlighting + presenter mode), better for code-walkthroughs, weaker on editorial design. **powerpoint** / **powerpoint-ppt** win when the deliverable must be an editable `.pptx` for business stakeholders — the one place guizang explicitly bows out. **open-slide** is a general agent slide framework without the locked aesthetic. guizang's edge is pure design quality + the Swiss validation gate; its cost is style-lock, AGPL, and HTML-only output. Note: it is already a CATALOG.md entry (line 187) — this evaluation backs and refines that row.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | skill | Generates single-file HTML swipe decks in two locked visual systems (e-magazine + Swiss International), with a layout-validation script and multi-platform covers — design-opinionated, AGPL-3.0 | Need agent-generated presentation slides with real design discipline (not generic slop), for talks/launches — accepting HTML-only output and copyleft | frontend-slides, open-slide, slidev (web/markdown decks); powerpoint, powerpoint-ppt (editable .pptx, where guizang bows out) |
