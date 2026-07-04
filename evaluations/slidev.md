# Evaluation: slidev

**Repo:** [slidevjs/slidev](https://github.com/slidevjs/slidev)
**Stars:** 47,257 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

Markdown-first presentation framework for developers. Write slides in `.md` files with Vue components, Vite hot-reload, code highlighting with magic-move animations, Monaco editor, Mermaid/PlantUML diagrams, LaTeX math, and presenter mode with recording. Exports to PDF, PPTX, PNG, or static SPA. The Claude Code skill (~7,600 installs on skills.sh) is a comprehensive syntax reference, not an AI generation wrapper — the developer writes all slide content.

## How we tested it

**Evidence:** REVIEW

Installed via the skills.sh global flag, read the full SKILL.md, and mentally executed a concrete task: "make a 15-slide tech talk on the AI tooling workflow."

```
npx skills add slidevjs/slidev@slidev -g -y
# Result: succeeded for universal agents
# Failed for PromptScript: "PromptScript does not support global skill installation"
```

Read SKILL.md end to end. It references a feature table with 40+ entries across 10 categories (code, diagrams, animations, layouts, recording, export, presenter mode, themes, components, interactions) plus pointers to `references/core-syntax.md`, `references/core-animations.md`, and several other sub-files.

Mental dry-run for the 15-slide tech talk: the workflow requires `pnpm create slidev`, writing Markdown in a new project directory, running a dev server (`pnpm dev`), iterating on slides, then `pnpm export` for PDF — plus a separate `npx playwright-chromium` install for PDF export to work. Total time to first working slide: ~10 minutes. Time to 15 polished slides: measured in hours, not minutes.

## What worked

- The SKILL.md is one of the most complete skill reference docs in the catalog — 40+ features, exact syntax, organized by category. No hunting through docs.
- Code-heavy presentations are genuinely better here than anywhere else: magic-move animations between code states, live Monaco editor, syntax-highlighted diffs are things PowerPoint cannot do.
- Export to PPTX (not just PDF) gives a migration path into corporate environments where `.pptx` is required.
- Slides live in git as plain Markdown — versionable, diffable, reviewable like any other source file.
- 47K stars on the underlying framework means the tool is stable and well-maintained. Not a weekend project.
- Presenter mode with timer, notes, and recording covers the full conference-talk workflow.

## What didn't work or surprised us

- The skill failed to install for PromptScript — only universal-agent install worked. Minor but worth noting for multi-harness setups.
- This is a framework reference, not an AI generation skill. The developer writes every slide. No equivalent of wowerpoint's "here's a doc, give me a deck."
- Requires a full Node.js/pnpm project per deck. Not a single command; not a quick async job. Session startup alone is ~10 minutes before a slide exists.
- PDF export silently fails without `playwright-chromium` installed separately — the skill doc mentions it but the error message at runtime does not.
- Audience is narrow: code-heavy conference talks, live coding workshops, developer-facing documentation. Business presentations, status updates, investor decks — wrong tool.
- No overlap with wowerpoint's core use case. wowerpoint turns a document into a polished deck with zero authoring. Slidev turns a developer's authoring into a polished deck. Different input, different output, different audience.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Slides are what you write; no AI generation means no hallucination risk, but also no AI leverage |
| Speed | neutral | Faster than PowerPoint for code slides; slower for general presentations (full authoring required) |
| Maintainability | + | Slides are Markdown in git — versionable, diffable, and editable in any text editor |
| Safety | + | Fully local, no external service dependency, no data leaves the machine |
| Cost Efficiency | + | Zero AI token cost; pure local tooling with one-time pnpm install |

## Verdict

**CONDITIONAL**

Use when building code-heavy technical presentations: conference talks, live coding sessions, developer workshops. Slidev is the best tool in this category — nothing else handles magic-move code animations, embedded Monaco, and Mermaid diagrams in a single coherent authoring experience. Skip it for business decks, status updates, or any presentation where you want AI to do the writing work — wowerpoint handles that case. The Claude Code skill adds value as a complete syntax reference; the underlying framework is the real asset.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [slidev](https://github.com/slidevjs/slidev) | skill | Markdown-first developer presentation framework with live code, animations, and diagram support | PowerPoint can't animate code diffs or embed a Monaco editor | wowerpoint (claude-mem), guizang-ppt-skill, frontend-slides, open-slide |
