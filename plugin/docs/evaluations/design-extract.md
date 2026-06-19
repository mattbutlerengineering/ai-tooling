# Evaluation: design-extract (designlang)

**Repo:** [Manavarya09/design-extract](https://github.com/Manavarya09/design-extract)
**Stars:** 3,294 | **Last updated:** 2026-06-19 (last push; latest tagged release v12.15.0, 2026-05-21) | **License:** MIT
**Dev loop stage:** Implement (design-to-code grounding; also Verify via `grade`/`drift`/`lint`/`visual-diff`)
**Layer:** Tooling (a CLI + an agent-facing MCP/skill/plugin bridge — not hosted infrastructure)

---

## What it does

Catalog one-liner: *"Extract any website's complete design system — DTCG tokens, multi-platform emitters, WCAG remediation (3.3K stars)."*

designlang (npm package `designlang`; repo `design-extract`) points a **headless Playwright/Chromium browser at any live URL** and reads the design system off the rendered DOM and computed styles — not from a Figma file, and not from static CSS parsing. One command (`npx designlang https://stripe.com`) writes 17+ files to `./design-extract-output/`: W3C **DTCG design tokens** in primitive + semantic + composite layers, a drop-in `tailwind.config.js`, a shadcn/ui `globals.css`, **Figma Variables** JSON (light + dark), CSS custom properties, typed React component-anatomy stubs (`.tsx`), motion tokens (durations/easings/springs, plus runtime `getAnimations()` capture with `--motion-runtime`), a brand-voice JSON, page-intent/semantic-region labels, and a paste-ready prompt pack for v0 / Lovable / Cursor / Claude Artifacts. `--platforms web,ios,android,flutter,wordpress,all` additionally emits iOS SwiftUI, Android Compose, Flutter, and a WordPress block theme.

Beyond pure extraction it covers a verification/quality surface: WCAG 2.1 contrast scoring for every fg/bg pair with a **remediation palette** (nearest passing AA/AAA colour), a 7-category A–F design **grade** with a shareable HTML report card + SVG badge, multi-page consistency reconciliation (`site` crawls canonical pages and elects tokens by coverage), and CI-ready `drift` / `lint` / `visual-diff` commands that exit non-zero on failure. It also ships generative extras (`remix`, `theme-swap`, `brand` book, `pair`, `battle`, `clone` → Next.js starter, `studio` live token editor).

For agents specifically, it exposes three on-ramps: (1) a **Claude Code plugin** with eleven slash commands (`/extract`, `/site`, `/grade`, `/battle`, `/remix`, `/pack`, `/theme-swap`, `/brand`, `/pair`, `/studio`, `/verify`) installable via `/plugin marketplace add Manavarya09/design-extract`; (2) an **agent skill** (`npx skills add Manavarya09/design-extract`); and (3) an **MCP server** (`designlang mcp --output-dir ./design-extract-output`) that serves the latest extraction's tokens, regions, components, and contrast pairs to any MCP-aware client (Claude Code / Cursor / Windsurf). The MCP server is notably **disk-backed** — it serves an already-produced extraction rather than crawling on demand.

## How we tested it

**Source-grounded inspection — not installed or run.** I examined the GitHub repo metadata (API), the full README, the release/tag history, recent commit messages, and the existing CATALOG entries for its overlaps. I did **not** install the npm package, the Claude Code plugin, the skill, or the MCP server; I did not run `designlang` against any URL or invoke any MCP tool. Consequently there are no measured extraction latencies, token-fidelity numbers, WCAG-accuracy figures, or output-quality judgments below — only what the repo and its documentation attest. The 17+-file output list, the DTCG/multi-platform/WCAG claims, the three agent on-ramps, the disk-backed MCP design, and the version cadence are taken from the README and confirmed against repo metadata.

```bash
gh api repos/Manavarya09/design-extract
gh api repos/Manavarya09/design-extract/readme --jq '.content' | base64 -d
gh api repos/Manavarya09/design-extract/releases --jq '.[0:6][] | "\(.tag_name) \(.published_at)"'
gh api repos/Manavarya09/design-extract/commits --jq '.[0:6][].commit.message'
# Catalog differentiation:
grep -inE "design-extract|Figma-Context|web-quality-skills|plumb-mcp|figma-mcp-go" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Targets a real, distinct niche from its catalog "overlaps."** Figma-Context-MCP / plumb-mcp / figma-mcp-go all read a *Figma file*. designlang reads a **live, deployed website's rendered DOM** — useful when you have no Figma source (cloning a competitor's look, re-theming around an existing site, auditing your own production styles). The overlap with the Figma tools is the *output* (design tokens for code) more than the *input*.
- **Output breadth is genuinely large and standards-aligned.** W3C DTCG tokens (primitive/semantic/composite), Tailwind v4 config, shadcn theme, Figma Variables, CSS vars, and multi-platform emitters (iOS/Android/Flutter/WordPress) from one crawl. The DTCG alignment matters for downstream tooling interop.
- **Strong agent ergonomics — three first-class on-ramps.** Claude Code plugin (11 slash commands), agent skill (`skills add`), and an MCP server, all from the same CLI. The repo topics (`claude-code-plugin`, `mcp-server`, `agent-skill`, `skills-sh`) show deliberate agent positioning, and the `--emit-agent-rules` flag writes Cursor/CLAUDE.md/agents.md rule files.
- **Covers Verify, not just Implement.** WCAG contrast scoring with a remediation palette, an A–F grade, and CI-ready `drift`/`lint`/`visual-diff` (non-zero exit) make it usable as a design-system regression guard, not only a one-shot extractor — the WCAG-remediation angle overlaps web-quality-skills' accessibility audit.
- **Active and reasonably mature for its age.** Created 2026-04-15, already at v12.x with frequent releases (multiple per week in May 2026), pushed the day of this evaluation, Dependabot-maintained dependencies, a VS Code extension and Chrome extension (MV3, `activeTab` only). 3.3K stars in ~2 months. Deterministic, zero-API-key core (`site` token election is explicitly free/deterministic; AI is optional via `--smart`).

## What didn't work or surprised us

- **The MCP server is disk-backed, not a live crawler.** `designlang mcp` serves the *latest already-produced* extraction's tokens to the client — the actual crawl happens via the CLI/plugin command first. So the "MCP server" framing in the catalog is accurate but narrow: the agent value is mostly in the CLI/plugin/skill; the MCP surface is a read-only payload server over prior output. An agent can't "extract site X" purely through the MCP tools without a CLI run.
- **Extracted ≠ correct design system.** Reading tokens off computed styles captures *what the rendered page does*, which conflates intentional design decisions with one-off page-local values, third-party widget styles, and ad/analytics chrome. The `site` coverage-election mechanism mitigates this, but fidelity (does the emitted token set actually reconstruct the brand?) is unverified here and is the core risk for any DOM-scraping extractor.
- **Very large, fast-moving surface.** Dozens of commands/flags (remix, battle, brand book, pair, studio, theme-swap…) and a v12.x major version reached within ~2 months of creation. Breadth this wide, this fast, on a single-maintainer project means per-command quality almost certainly varies, and rapid major-version churn is an API-stability risk for anything that scripts against it.
- **Sponsor/upsell coupling in the README.** `--smart` classification routes to a sponsor's hosted models (Atlas Cloud), and the README leads with sponsor banners and a "try it on Bloome" CTA. The core is zero-key and the AI path is optional, but the commercial coupling is worth noting for a tool you'd embed in an agent loop.
- **Legal/ToS surface of scraping live sites.** Pointing a headless browser at arbitrary third-party URLs (incl. `--cookie`/`--header` for authenticated pages and `--insecure` for TLS bypass) to lift their design system carries IP/ToS considerations the README does not address. Cloning a competitor's design language is a different risk posture than reading your own Figma file.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (when input is a website, not Figma) | Grounds generated UI code in the *actual rendered* tokens/layout/components of a real site (DTCG, anatomy `.tsx`, regions), so the agent isn't guessing styles; but DOM-scraped tokens can conflate intentional vs incidental styling — fidelity unverified here. |
| Speed | + | One `npx` command emits 17+ ready-to-use files (Tailwind/shadcn/Figma/multi-platform), collapsing a slow manual token-extraction chore; crawl latency unmeasured. |
| Maintainability | + | DTCG-standard tokens + CI-ready `drift`/`lint`/`visual-diff` (non-zero exit) let a team treat the live site as a source of truth and guard against design drift. |
| Safety | - (caution) | Headless scraping of arbitrary third-party URLs (with cookie/header injection and `--insecure` TLS bypass) raises ToS/IP and credential-handling concerns; optional `--smart` ships data to a sponsor's hosted model. |
| Cost Efficiency | + | Core is free, MIT, zero-API-key, deterministic, self-hosted via `npx`; AI classification is opt-in only. |

## Verdict

**CONDITIONAL**

designlang is a capable, actively developed CLI that extracts a full design system from any **live website** and emits standards-aligned DTCG tokens plus Tailwind/shadcn/Figma/multi-platform code, with three legitimate agent on-ramps (Claude Code plugin, skill, MCP server) and a Verify-stage layer (WCAG remediation, grade, drift/lint/visual-diff). **Adopt it when your task is "ground UI work in an existing deployed site's design language" — recreating, re-theming, auditing, or guarding against drift on a real URL — and when you've confirmed the extraction fidelity is good enough for your target on a sample run.** It is the right tool when you have a website but no Figma source.

It is not ADOPT-everywhere: the headline "MCP server" surface is a disk-backed read of prior CLI output (the agent value is really the CLI/plugin/skill, with a one-time crawl needed first); DOM-scraped tokens can conflate intentional design with incidental page styling and fidelity is unverified here; the command/flag surface is very wide and churning fast (v12.x within ~2 months, single maintainer) which is an API-stability risk; and scraping arbitrary third-party sites carries ToS/IP and credential-handling considerations the docs don't address. Not SKIP because it solves a real problem its catalog peers don't — its peers read Figma files, designlang reads live sites — and it's broad, standards-aligned, free, and well-integrated with the agent ecosystem. Among the catalog's design-to-code cluster: choose **Figma-Context-MCP / plumb-mcp / figma-mcp-go** when your source of truth is a **Figma file**, and **design-extract** when your source of truth is a **deployed website**; it also overlaps **web-quality-skills** on the WCAG/accessibility-audit axis.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [design-extract](https://github.com/Manavarya09/design-extract) | MCP server | Extract any website's complete design system — DTCG tokens, multi-platform emitters, WCAG remediation (3.3K stars) | Manual design-token extraction is slow and error-prone, and Figma-based tools can't help when the source of truth is a live deployed site rather than a Figma file | Figma-Context-MCP (design→code, but from Figma not live sites), web-quality-skills (WCAG/a11y audit overlap) |
