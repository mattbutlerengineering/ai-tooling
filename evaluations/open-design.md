# Evaluation: open-design

**Repo:** [nexu-io/open-design](https://github.com/nexu-io/open-design)
**Stars:** 67,833 | **Last updated:** 2026-06-19 (created 2026-04-28; 13 tagged releases) | **License:** Apache-2.0
**Dev loop stage:** None (visual/design artifact authoring, outside the coding dev loop)
**Layer:** Tooling (a standalone native desktop app + daemon that drives coding-agent CLIs as an LLM backend, and exposes its own MCP server)

---

## What it does

Catalog one-liner: *"Local-first design tool with 259+ skills, 142+ design systems, and sandboxed preview."* The accurate expansion: open-design is a **local-first, native desktop design application** — explicitly positioned as a "Claude Design alternative" and "Figma alternative." It turns prompts/notes into **visual design artifacts** — web/desktop/mobile prototypes, slide decks, images, videos, and "HyperFrames" — with sandboxed in-app preview and export to HTML / PDF / PPTX / MP4.

The mechanism (from the repo's monorepo layout — `apps/desktop`, `apps/web`, `apps/daemon`, `apps/landing-page`, `apps/telemetry-worker`): a local **daemon** detects coding-agent CLIs you have already logged in (Claude Code, Codex, Cursor, OpenCode, Qwen, Copilot, Hermes, Kimi, OpenClaw, and 17+ others per the description) and spawns one as a subprocess to do the generation — the same BYOK / "reuse your subscription, zero API key" pattern as its sibling `html-anything`. The 259+ "skills" are `SKILL.md`-convention folders that encode **visual/typographic design systems** (142+ of them), not engineering knowledge; they steer the app's output, not your agent's coding behavior. Output renders into a sandboxed preview and exports to design deliverable formats.

It is the **larger, more product-shaped sibling** of `nexu-io/html-anything` (already cataloged and evaluated SKIP); html-anything's README explicitly borrows credibility signals from this repo, and html-anything's architecture is described as "borrowed directly from" open-design. Where html-anything is a single Next.js app, open-design is a full native-desktop product with a daemon, a web app, telemetry, and a landing page.

One nuance distinguishing it from html-anything: open-design **also ships its own MCP server** (`apps/daemon/src/mcp*.ts`, with live-artifacts server, OAuth, agent-install, and an extensive MCP test suite). That MCP surface exists so the desktop app and external agents can drive *open-design's* artifact engine (create-artifact, get-artifact, get-file, spawn runs) — i.e. it exposes the design app's capabilities as MCP tools. It is a design-artifact MCP, not a software-development MCP (no code, test, review, or infra tools).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** I examined the GitHub API metadata, the recursive file tree, and the existing CATALOG.md entry. I did **not** download/build the desktop app, did not launch the daemon, did not connect the MCP server, did not invoke any agent through it, and did not generate or export any artifact — so no latency, output-quality, MCP-tool, or export-fidelity metrics are claimed below. I cross-read the already-merged calibration evaluations for `impeccable` (CONDITIONAL) and the same-org `html-anything` (SKIP). The "259+ skills / 142+ design systems / 17+ CLIs" figures are the repo's own description copy, confirmed against the tree's `SKILL.md`/`mcp` paths but not individually audited. All findings are read from source and metadata, not benchmarked.

```bash
gh api repos/nexu-io/open-design --jq '{stars:.stargazers_count,license:.license.spdx_id,description,pushed_at,created_at,homepage,topics}'
gh api "repos/nexu-io/open-design/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # → apps/{desktop,web,daemon,...}; apps/daemon/src/mcp*.ts; .claude/skills/od-contribute/SKILL.md
gh api repos/nexu-io/open-design/releases     --jq 'length'   # → 13
gh api repos/nexu-io/open-design/contributors --jq 'length'   # → 30
gh api repos/nexu-io/open-design              --jq '.open_issues_count'  # → 416
grep -in "open-design" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **The "reuse your logged-in CLI session" / BYOK architecture is genuinely clever** (inherited from / shared with html-anything). A local daemon spawns the coding-agent CLI you already authenticated, so for a Claude/Cursor subscriber, generation is effectively free — no API key.
- **It ships a real MCP server with a real test suite.** Unlike html-anything, open-design exposes an MCP interface (live-artifacts, create/get-artifact, spawn, OAuth) backed by ~20 MCP test files. The engineering is more mature and more "integration-shaped" than its sibling.
- **Strong provenance and maturity for the category.** 67.8K stars, Apache-2.0, 30 contributors, 13 tagged releases, same-day commits as this evaluation, a dedicated docs/landing site (open-design.ai), and a native desktop app across web/desktop/mobile surfaces. Not abandonware; clearly the most-invested project in the nexu-io family.
- **The design-system skill templates are high-craft** (142+ design systems following the `SKILL.md` convention with visual-design frontmatter), the same well-built artifact-steering layer the sibling repo uses.

## What didn't work or surprised us

- **It is a standalone design platform, not a coding dev-loop tool.** Its outputs — prototypes, slide decks, images, videos, posters, HyperFrames — are visual deliverables for human viewers, not software. It produces no application code, tests, reviews, PRs, or infrastructure. It is explicitly marketed as a "Figma alternative" / "Claude Design alternative," i.e. a design app, not an agent capability for *your* repo.
- **The "skills" are design templates, not engineering knowledge.** Despite the `SKILL.md` filename convention, the 259+ skills encode typographic/visual design systems and steer the app's artifact output. The only repo skill aimed at a developer's agent (`.claude/skills/od-contribute`) is a contributor-onboarding helper for the project itself, not a dev-loop capability.
- **The Claude Code relationship is inverted — Claude Code gains nothing.** open-design *consumes* Claude Code (and 17+ other CLIs) as an LLM execution backend via its daemon. There is no installable skill, plugin, or hook that adds capability to your coding agent. Its MCP server exposes the *design app's* artifact engine, not software-development tools, so wiring it into your dev-loop agent buys design-artifact generation, not better software.
- **High open-issue count.** 416 open issues against a fast-moving native-app product — expected for a project this size and age, but a maintenance-load signal for anyone considering it as a dependency.
- **Heavy footprint.** A full Electron/native desktop app + daemon + web app + telemetry worker is a large install for what is, in this catalog's terms, an out-of-scope design tool.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Produces visual design artifacts (prototypes/decks/images/video) for human viewers; does not touch application code, tests, or the correctness of a software project. |
| Speed | neutral | May speed up *producing design/marketing artifacts*, but does not affect software development velocity in the dev loop. |
| Maintainability | neutral | Output is exported design deliverables (HTML/PDF/PPTX/MP4); no impact on a codebase's maintainability. |
| Safety | neutral / + | Sandboxed in-app preview + local-first (no upload) is well-handled, but the safety surface is the app's own, not your dev workflow; its MCP server adds an execution surface only if you wire it in. |
| Cost Efficiency | neutral | BYOK / reuse-your-logged-in-CLI is cost-clever, but it optimizes design-artifact generation cost, not coding-agent session cost in the dev loop. |

## Verdict

**SKIP**

open-design is the largest and most mature project in the nexu-io family — a polished, local-first native **design application** ("Figma alternative" / "Claude Design alternative") with a BYOK daemon, an MCP server with a real test suite, 259+ design skills, and 142+ design systems. The engineering is genuinely impressive and a notch more product-complete than its sibling html-anything. But it sits entirely outside the coding dev loop this catalog evaluates: it turns prompts into prototypes, decks, images, and videos for human viewers; it writes no application code, no tests, no reviews; its `SKILL.md` files are design templates rather than engineering skills; and it integrates with Claude Code only by *spawning it as an LLM subprocess* — Claude Code (and your dev-loop agent) gain zero coding capability. Even its MCP server exposes the design app's artifact engine, not software-development tools, so it is not a dev-loop MCP. This is the same call as html-anything (same org, shared architecture) and distinct from the dev-loop frontend-design *skills* it superficially resembles: `impeccable` / `ui-ux-pro-max` are skills that make *your agent* better at building real frontend UI inside a codebase (CONDITIONAL — adopt when the project has a real frontend), whereas open-design is a separate app you produce design artifacts *in*. Strong stars (67.8K) and maturity reinforce that it is real, but provenance is not the basis for the call — it is out of scope by nature. Catalog it as a platform with no dev-loop overlap.

The existing CATALOG.md entry (line 176) is accurate in substance; no change is required as part of this evaluation (per scope, CATALOG.md is not edited here).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [open-design](https://github.com/nexu-io/open-design) | platform | Local-first native desktop design app ("Figma/Claude Design alternative") that drives your logged-in coding-agent CLI to produce prototypes, slides, images, and video across web/desktop/mobile, with 259+ design skills and a design-artifact MCP server | Producing polished visual design deliverables (prototypes, decks, images, video) without a designer — a standalone design platform, not a software dev-loop tool | html-anything (same org, shared BYOK architecture); design-artifact platform — out of scope for the coding dev loop, distinct from dev-loop frontend-design skills impeccable / ui-ux-pro-max |
