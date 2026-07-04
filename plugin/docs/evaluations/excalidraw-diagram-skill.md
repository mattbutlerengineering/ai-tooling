# Evaluation: excalidraw-diagram-skill

**Repo:** [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill)
**Stars:** 3,783 | **Last updated:** 2026-03-01 (pushed; created 2026-03-01) | **License:** none declared
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan / Reflect (outer loop) — it produces architecture and concept diagrams for design docs, READMEs, ADRs, and explanations. Not an inner-loop coding tool; it generates an artifact *about* the system, not the system.
**Layer:** Process (a single-file Claude/OpenCode skill: `SKILL.md` design methodology plus a `references/` bundle with JSON templates, a color palette, and a Python+Playwright render-and-validate pipeline)

---

## What it does

The catalog one-liner: "Generates Excalidraw diagrams from Claude Code." More precisely, it is a coding-agent skill (by coleam00, a well-known AI-dev/Archon author) that turns a natural-language prompt — "show how the AG-UI protocol streams events from an agent to a frontend" — into a hand-drawn-style `.excalidraw` JSON file. The pitch is that the diagrams *argue* rather than *display*: the SKILL.md enforces an "Isomorphism Test" (if you stripped all text, would the shape alone carry the concept?) and an "Education Test" (does it teach concrete formats/event names, not just label boxes?), pushing fan-outs for one-to-many, timelines for sequences, convergence for aggregation — explicitly *not* uniform card grids.

The mechanism is drop-in-and-go: clone into `.claude/skills/`, and the agent reads `SKILL.md` (methodology + depth assessment) plus three references — `element-templates.md` (per-element JSON), `json-schema.md` (Excalidraw format), and `color-palette.md` (the single brand-customization seam). The differentiator is a **closed render-validation loop**: `references/render_excalidraw.py` drives headless Chromium via Playwright to rasterize the generated `.excalidraw` to PNG, so the agent can *see* its own output, catch overlapping text / misaligned arrows / unbalanced spacing, and fix before delivering. That self-correction step is what separates it from "emit JSON and hope."

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Nothing was cloned into `.claude/skills/`, `uv sync` / `playwright install` was not executed, and no diagram was generated or rendered. Every claim comes from the repository (GitHub metadata, README, full file tree, `SKILL.md`), not from observed output. Claims about diagram *quality* ("beautiful," "argue visually") and the render loop's effectiveness are the author's framing and the code's stated intent, not anything I measured.

```bash
gh api repos/coleam00/excalidraw-diagram-skill --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/coleam00/excalidraw-diagram-skill/readme --jq '.content' | base64 -d
gh api "repos/coleam00/excalidraw-diagram-skill/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # 10 paths
gh api repos/coleam00/excalidraw-diagram-skill/contents/SKILL.md --jq '.content' | base64 -d
gh api repos/coleam00/excalidraw-diagram-skill/commits --jq 'length'    # 2
gh api repos/coleam00/excalidraw-diagram-skill/releases --jq 'length'   # 0
```

## What worked

- **A real feedback loop, not blind generation.** The Playwright render-to-PNG step lets the agent inspect and repair its own layout. Among diagram skills this is the standout: most emit a format and stop; this one closes the loop, which is exactly the inner-loop discipline this catalog rewards.
- **Opinionated methodology that fights generic output.** The Isomorphism and Education tests, depth assessment, and "argue not display" framing are concrete rules that steer the model away from undifferentiated box-and-arrow clutter — the diagram equivalent of an anti-slop design skill.
- **Clean single-seam customization.** All brand/color decisions live in `color-palette.md`; everything else is universal methodology. Swap one file and every diagram follows your palette — a tidy, low-coupling design.
- **Editable, version-controllable artifact.** Output is `.excalidraw` JSON (hand-drawn aesthetic), so diagrams are diff-able, re-openable, and tweakable in Excalidraw — unlike an opaque PNG. Good fit for committing architecture diagrams alongside code.
- **Strong author signal and traction.** 3.8K stars and 452 forks within days of a single-day push, from a recognized AI-dev author; the breadth of forks suggests genuine pickup.

## What didn't work or surprised us

- **No license.** "No license declared" means all rights reserved by default — legally you have no granted right to copy, modify, or redistribute it, despite the README saying "clone and drop it in." For a skill you'd vendor into a repo, this is a real adoption blocker until clarified.
- **Two commits, single-day history, zero releases.** Created and last pushed 2026-03-01 with 2 commits and no tags. It is essentially a one-shot drop; there is no maintenance track record and no pinned version to depend on.
- **Heavier dependency than a typical markdown skill.** The validation loop requires `uv`, a Python env, and a Chromium download via Playwright. That is a meaningful install footprint and a sandbox/CI consideration for a "just drop it in" skill.
- **Niche, occasional-use scope.** This is a Plan/docs aid, not something the inner loop touches every task. Value is real but intermittent — architecture diagrams for design docs and READMEs, not day-to-day coding.
- **Quality is unverified here.** "Beautiful and practical" and "diagrams that argue" are the author's claims; we did not generate a diagram, so the actual output quality and how reliably the render-repair loop catches layout defects are untested.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (for docs) | The render-validate loop catches overlapping text / misaligned arrows before delivery; Isomorphism/Education tests push diagrams that accurately mirror structure. Affects doc/diagram correctness, not code correctness. |
| Speed | + | Generates a polished, editable architecture diagram from one prompt — far faster than hand-drawing in Excalidraw, even with the render loop. |
| Maintainability | + | Output is diff-able `.excalidraw` JSON committable beside code; single-file color seam keeps the skill easy to rebrand. |
| Safety | − / neutral | Runs Python + headless Chromium locally via Playwright; more host/dependency surface than a pure-markdown skill. No network reach beyond the Chromium install. |
| Cost Efficiency | neutral / − | The see-and-fix render loop spends extra model turns per diagram; justified for a deliverable artifact but not free. |

## Verdict

**CONDITIONAL — adopt for diagram-heavy Plan/docs work once the license is resolved.** This is the most credible diagram-generation skill in the catalog because it does the one thing the others don't: closes a render-and-repair feedback loop so the agent sees and fixes its own output, backed by a genuinely opinionated "argue, don't display" methodology and a clean single-file brand seam. The blockers are the missing license (all-rights-reserved by default, despite "clone and go" instructions) and a two-commit, zero-release, single-day history with no maintenance signal — plus a heavier `uv`+Playwright+Chromium footprint than a markdown skill. Use it when architecture diagrams in design docs/READMEs/ADRs are a recurring need; skip it for projects that rarely produce diagrams.

Compared to neighbors: its catalog "overlaps with" is **graphify**, but they barely overlap — graphify turns arbitrary input into a *knowledge graph* (clustered communities, HTML/JSON), an analysis artifact, whereas this produces a *designed, hand-drawn architecture diagram* meant to argue a specific concept. Against text-based diagram options (e.g. Mermaid in markdown), Excalidraw output is richer and editable but heavier to produce; the render-validation loop is the deciding advantage. It is orthogonal to the UI/visual-design cluster (impeccable, ui-ux-pro-max, huashu-design) — those polish rendered web UIs; this polishes explanatory diagrams.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | skill | Drop-in skill that generates editable `.excalidraw` architecture/concept diagrams that "argue visually," with a Playwright render-and-repair loop so the agent sees and fixes its own layout (no license declared) | Want polished, version-controllable architecture diagrams from a prompt — not opaque PNGs or generic box-and-arrow clutter | graphify (knowledge-graph artifact, not designed diagrams); Mermaid-style text diagrams (lighter but less rich) |
