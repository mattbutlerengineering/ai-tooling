# Evaluation: html-anything

**Repo:** [nexu-io/html-anything](https://github.com/nexu-io/html-anything)
**Stars:** 7,005 | **Last updated:** 2026-06-16 (created 2026-05-11; no tagged releases) | **License:** Apache-2.0
**Dev loop stage:** None (content/design authoring, outside the coding dev loop)
**Layer:** Tooling (a standalone Next.js app + CLI that drives coding-agent CLIs as an LLM backend)

---

## What it does

Catalog one-liner: *"Agentic HTML editor — AI writes HTML across 9 surfaces."* The accurate expansion: html-anything is a **local-first content/design authoring app** that turns arbitrary input (Markdown / CSV / TSV / Excel / JSON / SQL / raw notes) into a **ship-ready single-file HTML deliverable** — and then one-click exports it to WeChat / X / Zhihu / `.html` / `.png`. The nine "surfaces" are deliverable *formats for human readers*: magazine article, keynote deck, résumé, poster, Xiaohongshu card, tweet card, web prototype, data report, and Hyperframes video frames.

The mechanism: a Next.js app (`next/`, the primary product) plus a thin CLI (`cli/`) scan your `PATH` for any of **8 coding-agent CLIs** you already have logged in (Claude Code, Cursor Agent, Codex, Gemini CLI, Copilot CLI, OpenCode, Qwen Coder, Aider) and spawn one as a subprocess to do the generation. Because it reuses your existing `claude login` / `cursor login` session, there is **zero API key** and marginal cost is whatever your subscription already covers. The user picks one of **75 "skill" templates** (each a folder following the Claude Code `SKILL.md` convention with extended frontmatter: `mode`/`scenario`/`surface`/`design_system`), the app assembles a prompt that injects the template's hard visual constraints (CJK-first font stack, 8px baseline grid, contrast ≥ 4.5, "use real data" rule), invokes the agent over a streaming JSON-line protocol (`claude -p --output-format stream-json`), parses text deltas into Server-Sent Events, and live-updates an `<iframe sandbox>` preview as the HTML "types" in. A notable detail in `next/src/app/api/convert/route.ts`: re-edits send the prior HTML + a diff and instruct the agent to do a **minimal-diff edit** (and explicitly forbid Write/Edit/Bash file tools — the HTML must stream back in the reply body), which both saves tokens and prevents design drift.

Key framing: the coding agent here is an **LLM execution backend for producing design artifacts**, not a participant in software development. The 75 SKILL.md files encode *visual/typographic design systems*, not engineering knowledge. Nothing it produces is application code, tests, reviews, or infrastructure — the artifact is "what your audience sees."

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** I examined repo metadata, the full English README, the recursive file tree, and read the actual source to determine the tool's nature: the CLI entrypoint and help text (`cli/src/index.ts`), the CLI agent-invocation/binary-resolution logic (`cli/src/agents-invoke.ts`), the web app's streaming convert route including the minimal-diff edit prompt (`next/src/app/api/convert/route.ts`), and a representative skill template (`next/src/lib/templates/skills/doc-kami-parchment/SKILL.md`). I did **not** run `pnpm dev`, did not start the app, did not invoke any agent through it, and did not generate or export any HTML — so no latency, output-quality, or export-fidelity metrics are claimed below. All findings are read from source and README, not benchmarked.

```bash
gh api repos/nexu-io/html-anything --jq '{stars,license,description,pushed_at,created_at,open_issues,topics}'
gh api repos/nexu-io/html-anything/readme --jq '.content' | base64 -d
gh api "repos/nexu-io/html-anything/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/nexu-io/html-anything/contents/cli/src/index.ts --jq '.content' | base64 -d
gh api repos/nexu-io/html-anything/contents/cli/src/agents-invoke.ts --jq '.content' | base64 -d
gh api repos/nexu-io/html-anything/contents/next/src/app/api/convert/route.ts --jq '.content' | base64 -d
gh api repos/nexu-io/html-anything/contents/next/src/lib/templates/skills/doc-kami-parchment/SKILL.md --jq '.content' | base64 -d
gh api repos/nexu-io/html-anything/releases   # → empty: no tagged releases
gh api repos/nexu-io/html-anything/contributors --jq 'length'  # → 11
```

## What worked

- **The zero-API-key "reuse your logged-in CLI session" architecture is genuinely clever.** It spawns the coding-agent CLI you already authenticated and pipes JSON-line stdout back as SSE. For someone with a Claude/Cursor subscription, generation is effectively free, and the multi-CLI adapter layer (`cli/src/agents-invoke.ts`, one thin adapter per CLI) is clean and broadly compatible.
- **The minimal-diff edit prompt is a thoughtful token/quality optimization.** On re-edits it sends prior HTML + content diff and forbids the agent from touching design tokens, structure, or fonts — only the changed text nodes — which prevents the creative drift that plagues regenerate-from-scratch workflows.
- **The SKILL.md design-system templates are high-craft.** Each encodes hard visual constraints (exact hex palettes, single-serif rules, baseline grid, contrast floors, anti-AI-slop discipline borrowed from `alchaincyf/huashu-md-html`). As *design* artifacts these are well done.
- **Sandboxed preview is a real safety measure.** User-emitted HTML runs in `<iframe sandbox="allow-scripts allow-same-origin">`, quarantining cookies/localStorage from the host.

## What didn't work or surprised us

- **It is a content/design authoring tool, not a coding dev-loop tool.** The output surfaces — magazine, deck, poster, résumé, Xiaohongshu/tweet card, data report, video frame — are deliverables for human *readers*, not software. It produces no application code, tests, reviews, PRs, or infrastructure. The "coding agent" is just an LLM runtime to render pretty HTML.
- **The "skills" are design templates, not engineering knowledge.** Despite using the Claude Code `SKILL.md` filename convention, the frontmatter axes are `mode`/`scenario`/`surface`/`design_system` and the bodies are typographic/visual rule sets. They do not extend a developer's coding agent in the dev loop; they only steer this app's output.
- **No Claude Code integration in the dev-loop sense.** There is no Claude Code plugin, no installable skill for *your* agent, no MCP server, and no hook. The relationship to Claude Code is inverted: html-anything *consumes* Claude Code as a subprocess; Claude Code gains nothing.
- **Maturity is early and the marketing leans heavily on a sibling project.** Created May 2026, **no tagged releases**, 11 contributors, 45 open issues. Much of the README's credibility signaling (40k★, 200+ contributors, commit-activity badges) points at `nexu-io/open-design`, not this repo — html-anything's own architecture is explicitly "borrowed directly from" open-design.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Produces presentation HTML for human readers; does not touch application code, tests, or correctness of a software project. |
| Speed | neutral | May speed up *producing marketing/doc artifacts*, but does not affect software development velocity in the dev loop. |
| Maintainability | neutral | Output is single-file HTML deliverables; no impact on a codebase's maintainability. |
| Safety | neutral / + | Sandboxed iframe + local-first (no upload) is well-handled, but the safety surface is the app's own, not your dev workflow. |
| Cost Efficiency | neutral | Zero-API-key reuse is cost-clever, but it optimizes content-generation cost, not coding-agent session cost in the dev loop. |

## Verdict

**SKIP**

html-anything is a well-crafted, genuinely clever **content/design authoring app** — the reuse-your-logged-in-CLI architecture, streaming preview, and minimal-diff edit prompt are all thoughtfully built, and the design-system templates are high-craft. But it sits entirely outside the coding dev loop this catalog evaluates. It turns notes/Markdown/CSV into beautiful HTML deliverables (decks, posters, magazines, social cards, résumés) for human readers; it writes no application code, no tests, no reviews, and integrates with Claude Code only by *spawning it as an LLM subprocess* — Claude Code gains zero capability. Its `SKILL.md` files are design templates, not engineering skills, and there is no plugin/MCP/hook that an agent in your dev loop could use. This is the same call as aisuite (a capable tool, but no surface area in the dev-loop quality-signal framework) and distinct from docmd (which at least targets the Ship stage with `llms.txt`). Catalog it as a tool with no dev-loop overlap, not as an agent capability. (Early maturity — no releases, 45 open issues — reinforces the call but is not the basis for it; even at full maturity it would be out of scope.)

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [html-anything](https://github.com/nexu-io/html-anything) | tool | Local-first app that drives your logged-in coding-agent CLI to turn notes/Markdown/CSV into ship-ready HTML deliverables (decks, posters, magazines, social cards) across 9 surfaces | Producing polished, reader-ready HTML/PNG content artifacts without hand-writing CSS — not a software dev-loop tool | — (content/design authoring; out of scope for the coding dev loop — distinct from doc-publishing tools like docmd) |
