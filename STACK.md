# Recommended Stack

The ~25 tools worth installing on every project, distilled from 497 catalog entries and 469 evaluations. Each tool earned its slot by moving a quality signal in real testing.

## Quick Start — 5 Highest Impact

```bash
# 1. Live docs lookup (never use stale API info again)
claude mcp add --transport sse context7 https://mcp.context7.com/sse

# 2. Output token compression (~60-75% savings)
claude install-skill JuliusBrussee/caveman

# 3. Structured security audit methodology
claude install-skill trailofbits/skills

# 4. Visual verification for UI changes
npx skills add vercel-labs/agent-browser

# 5. CI integration for async review
# Add .github/workflows/claude.yml — see evaluations/claude-code-action.md
```

---

## Plan

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [context7](https://github.com/upstash/context7) | Live documentation lookup — current APIs, not stale training data | `claude mcp add --transport sse context7 https://mcp.context7.com/sse` | Correctness |
| [GSD](https://github.com/obra/superpowers) | Structured project planning with milestone/phase management | `claude install-plugin obra/superpowers` | Correctness, Speed |
| [feature-dev](https://github.com/anthropics/claude-plugins-official) | 7-phase guided feature development for single features | `claude install-plugin anthropics/claude-plugins-official` | Correctness |
| [github-mcp-server](https://github.com/github/github-mcp-server) | GitHub's official MCP server — repos, issues, PRs, actions, search | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` | Speed, Correctness |
| [codegraph](https://github.com/colbymchenry/codegraph) | Always-on code-intelligence graph — agents query structure instead of reading whole files | `npm install -g @colbymchenry/codegraph` (then it auto-wires the MCP server into Claude Code) | Speed, Cost Efficiency |
| [markitdown](https://github.com/microsoft/markitdown) | Converts PDF/Office/images/audio/HTML to clean Markdown so agents can actually read binary docs | `pip install 'markitdown[all]'` | Correctness, Cost Efficiency |
| [serena](https://github.com/oraios/serena) | IDE-grade semantic code retrieval + atomic symbol-level editing over MCP (LSP, 40+ languages) — complements codegraph's read-only graph with safe refactors | `claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server` | Correctness, Speed |

## Implement

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [agent-skills](https://github.com/addyosmani/agent-skills) | Full lifecycle skills: /spec → /plan → /build → /test → /review → /ship, with autonomous mode | `npx skills add addyosmani/agent-skills -g -y` | Correctness, Speed |
| [caveman](https://github.com/JuliusBrussee/caveman) | ~60-75% output token reduction, no accuracy loss | `claude install-skill JuliusBrussee/caveman` | Cost Efficiency, Speed |
| [headroom](https://github.com/chopratejas/headroom) | Compresses tool output before it reaches context window | `pip install "headroom-ai[all]"` (or `npm install headroom-ai`) | Cost Efficiency |
| [claude-squad](https://github.com/smtg-ai/claude-squad) | TUI for managing parallel agent sessions | `go install github.com/smtg-ai/claude-squad@latest` | Speed |
| [beads](https://github.com/gastownhall/beads) | Work coordination ledger — prevents duplicate agent effort | `npm install -g @beads/bd` | Correctness, Speed |
| [fastmcp](https://github.com/PrefectHQ/fastmcp) | Build MCP servers in Python with minimal boilerplate — decorator API, auth, middleware | `pip install fastmcp` | Speed |
| [mattpocock/skills](https://github.com/mattpocock/skills) | Skills for Real Engineers — TDD, debugging, planning skills from a working dev | `npx skills add mattpocock/skills -g -y` | Correctness, Speed |
| [skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) | First-party skill-authoring meta-skill: draft -> eval (with-skill vs baseline) -> benchmark -> optimize triggering -> package | `claude install-plugin anthropics/claude-plugins-official` | Maintainability |

## Verify

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [agent-browser](https://github.com/vercel-labs/agent-browser) | Browser automation for visual verification of UI changes | `npx skills add vercel-labs/agent-browser` | Correctness |
| [stryker-js](https://github.com/stryker-mutator/stryker-js) | Mutation testing — tests the quality of your tests | `npm install -D @stryker-mutator/core` | Correctness |
| [web-quality-skills](https://github.com/addyosmani/web-quality-skills) | Six web quality audit skills: accessibility, SEO, perf, Core Web Vitals, best practices | `npx skills add addyosmani/web-quality-skills -g -y` | Correctness, Maintainability |
| [playwright](https://github.com/microsoft/playwright-mcp) | Browser automation and testing via MCP — lets agents drive real browsers | `claude mcp add playwright -- npx @playwright/mcp@latest` | Correctness |

## Review

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [code-review](https://github.com/anthropics/claude-plugins-official) | 4-agent parallel PR review with confidence scoring | `claude install-plugin anthropics/claude-plugins-official` | Correctness, Safety |
| [pr-review-toolkit](https://github.com/anthropics/claude-plugins-official) | 6 dimension-specific review agents (silent failures, type design, etc.) | Included in claude-plugins-official | Correctness, Safety |
| [trailofbits/skills](https://github.com/trailofbits/skills) | Structured security audit methodology | `claude install-skill trailofbits/skills` | Safety |
| [security-guidance](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance) | First-party in-loop security review (regex + LLM diff review + commit-time cross-file) with self-correction before output | `claude install-plugin anthropics/claude-plugins-official` | Safety |

## Ship

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [claude-code-action](https://github.com/anthropics/claude-code-action) | @claude in GitHub PRs/issues for async review and fixes | Add GitHub Actions workflow YAML | Speed, Correctness |
| [resolving-merge-conflicts](https://github.com/mattpocock/skills) | Intent-preserving merge resolution — trace both sides, resolve, run checks | `npx skills add mattpocock/skills@resolving-merge-conflicts -g -y` | Correctness, Safety |

## Reflect

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | Turns session corrections into persistent CLAUDE.md rules | `claude install-plugin BayramAnnakov/claude-reflect` | Speed, Maintainability |
| [documentation-writer](https://github.com/github/awesome-copilot) | Diátaxis-framework docs: clarify purpose, outline, then generate | `npx skills add github/awesome-copilot@documentation-writer -g -y` | Maintainability |
| [documentation-and-adrs](https://github.com/addyosmani/agent-skills) | ADR templates and agent-context documentation guidelines | `npx skills add addyosmani/agent-skills@documentation-and-adrs -g -y` | Maintainability |

## Memory

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [claude-mem](https://github.com/thedotmack/claude-mem) | Persistent memory with semantic search, timeline, and knowledge-graph recall across sessions | `claude install-plugin thedotmack/claude-mem` | Maintainability, Speed |

## Outer Loop

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [abtop](https://github.com/graykode/abtop) | Live token/cost TUI for comparing agent session efficiency | `cargo install abtop` | Cost Efficiency |
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | Security scanner for AI agent skills — detects prompt injection | `git clone https://github.com/NVIDIA/skillspector` (no PyPI package) | Safety |

---

## Research

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [last30days](https://github.com/mvanhorn/last30days-skill) | Research any topic across Reddit, X, YouTube, HN, Polymarket — engagement-weighted | `npx skills add mvanhorn/last30days-skill -g -y` | Speed, Correctness |

## What's NOT here

- **497 tools** are cataloged in [CATALOG.md](CATALOG.md) — this page is the curated subset
- **CONDITIONAL tools** (context-mode, shadcn/improve, ralph-claude-code, etc.) are documented in [evaluations/](evaluations/) with guidance on when they're worth it
- **Unevaluated tools** are tracked in [COMPARISON.md](COMPARISON.md) with evaluation coverage by stage
