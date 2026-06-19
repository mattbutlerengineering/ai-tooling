# Evaluation: open-slide

**Repo:** [1weiho/open-slide](https://github.com/1weiho/open-slide)
**Stars:** 5,441 | **Created:** 2026-04-26 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Reflect (outer loop — communicating results)
**Layer:** Tooling

---

## What it does

A slide framework "built for agents." You describe a deck in natural language; your coding agent writes the React. open-slide supplies the runtime — every slide renders into a fixed 1920×1080 canvas as an arbitrary React component (not a constrained DSL), and the framework handles scaling, navigation, hot reload, present mode, and export.

It is distributed as a pnpm + Turbo monorepo with two published packages: `@open-slide/cli` (the `npx @open-slide/cli init` scaffolder) and `@open-slide/core` (the Vite-plugin runtime + dev/build/preview CLI). The scaffolded workspace ships agent skills preconfigured for Claude Code:

- **`/create-slide`** — drafts a deck end-to-end: asks four scoping questions (topic/aesthetic, page count, text density, motion vs. static), picks an id, plans structure, writes pages.
- **`/slide-authoring`** — a technical reference for the canvas, type scale, palette, and layout rules that the agent reads before writing.

Standout features beyond authoring: an in-browser inspector (click an element, attach a `@slide-comment` marker, run `/apply-comments` to have the agent apply edits), an assets manager with svgl logo search, a professional present/presenter mode (speaker notes, next-slide preview, timer), and one-command export to self-contained static HTML or print-ready PDF.

## How we tested it

Source-grounded inspection only — we did not run `npx @open-slide/cli init`. We fetched repo metadata, read the full README, and walked the monorepo tree to confirm the package layout and the agent-skill claims.

```
gh api repos/1weiho/open-slide --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
# => {desc:null, stars:5441, created:2026-04-26, pushed:2026-06-18, license:MIT}
gh api repos/1weiho/open-slide/git/trees/HEAD --jq '.tree[].path'
# => packages/core, packages/cli, apps/demo, biome.json, turbo.json, vitest.config.ts, .claude, CLAUDE.md, AGENTS.md
gh api repos/1weiho/open-slide/readme --jq '.content' | base64 -d
```

We did not generate a deck or measure render fidelity. Claims about inspector, present mode, and export quality are taken from the README, not verified.

## What worked

- **Genuinely agent-native, not a skill bolted on.** Unlike slidev/powerpoint (syntax references the developer drives), open-slide ships a runtime *plus* `/create-slide` and `/apply-comments` skills designed around the present → click-comment → apply loop. The agent owns content; the framework owns the canvas.
- **React components, not a DSL.** Each page is arbitrary React in a fixed 1920×1080 box. Agents are strong at writing React, so this plays to the model's strengths and avoids the expressiveness ceiling of a Markdown DSL.
- **The `@slide-comment` inspector loop is the differentiator.** Visual edits get captured as persisted source markers, then batch-applied — a tight WYSIWYG-to-source feedback loop that none of the neighbors offer.
- **Clean output story.** Plain static build deploys to Vercel/Cloudflare/Netlify; export to self-contained HTML or PDF means no server lock-in. MIT licensed.
- **Real engineering hygiene.** Turbo monorepo, biome, vitest config, AGENTS.md + CLAUDE.md, changesets. This is a maintained project, not a weekend gist.

## What didn't work or surprised us

- **No GitHub description set** (`desc: null`) — minor, but the repo leans entirely on the README cover image for positioning.
- **Heavier than its neighbors.** It is a scaffolded Vite/React workspace you `init` and run with `pnpm dev`, versus dropping a single SKILL.md. For one quick deck that is a lot of moving parts; the value compounds only once you maintain multiple decks (hence the slide manager).
- **Young and fast-moving.** Created April 2026, ~5.4K stars in under two months. Active, but the API surface and skill behavior are still settling — pin versions.
- **Output fidelity unverified.** We did not render a deck, so the "polished, presentable" claim and the design quality of `/create-slide` output are unconfirmed. The fixed-canvas + free-React model can just as easily produce cramped or off-brand slides if the agent's layout judgment is poor.
- **Claude Code-first.** Skills are preconfigured for Claude Code; "works with any agent" is plausible but the out-of-box path assumes Claude Code / AGENTS.md-aware tools.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Presentation tooling — no effect on shipped code correctness |
| Speed | + | One-line prompt to a deck; inspector batch-apply loop is faster than hand-editing React |
| Maintainability | + | Decks are versioned React source + a slide manager; far more maintainable than binary .pptx |
| Safety | neutral | Static output, no server, no network lock-in; MIT |
| Cost Efficiency | + | Static build deploys free; no runtime. Offset by the heavier init/monorepo footprint |

## Verdict

**CONDITIONAL**

Adopt when an agent must *produce* a polished, web-based deck from a prompt — and especially when you will iterate on it visually (the inspector → `/apply-comments` loop is the reason to pick this over the neighbors). Among slide tools in the catalog it occupies a distinct slot: **slidev** and **powerpoint** are syntax/design references the human drives; **frontend-slides** and **guizang-ppt-skill** are HTML-deck generation skills with no runtime or feedback loop. open-slide is the only one that pairs an agent-authoring skill with a present-mode runtime and a visual-comment edit loop. The conditions: you are comfortable running a Vite/React workspace, you want to maintain decks over time (not one-and-done), and you can pin to a young, fast-moving package. If you just need a single `.pptx` for a business audience, reach for `powerpoint`/`wowerpoint` instead; if you want a quick dev talk in Markdown, slidev.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [open-slide](https://github.com/1weiho/open-slide) | tool | Agent-native React slide runtime — prompt to deck, in-browser comment loop, present mode, static/PDF export (5.4K stars) | Need agents to author and visually iterate on presentable decks, not just generate slide markup | slidev, powerpoint, frontend-slides, guizang-ppt-skill |
