# Recommended Stack

The ~20 tools worth installing on every project, distilled from 209 catalog entries and 19 hands-on evaluations. Each tool earned its slot by moving a quality signal in real testing.

## Quick Start — 5 Highest Impact

```bash
# 1. Live docs lookup (never use stale API info again)
claude mcp add --transport sse context7 https://mcp.context7.com/sse

# 2. Output token compression (~60-75% savings)
claude install-skill JuliusBrussee/caveman

# 3. Structured security audit methodology
claude install-skill trailofbits/skills

# 4. Visual verification for UI changes
claude install-skill nichochar/agent-browser

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

## Implement

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [caveman](https://github.com/JuliusBrussee/caveman) | ~60-75% output token reduction, no accuracy loss | `claude install-skill JuliusBrussee/caveman` | Cost Efficiency, Speed |
| [headroom](https://github.com/chopratejas/headroom) | Compresses tool output before it reaches context window | `claude mcp add headroom` | Cost Efficiency |
| [claude-squad](https://github.com/smtg-ai/claude-squad) | TUI for managing parallel agent sessions | `go install github.com/smtg-ai/claude-squad@latest` | Speed |
| [beads](https://github.com/gastownhall/beads) | Work coordination ledger — prevents duplicate agent effort | `npm install -g beads` | Correctness, Speed |

## Verify

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [agent-browser](https://github.com/nichochar/agent-browser) | Browser automation for visual verification of UI changes | `claude install-skill nichochar/agent-browser` | Correctness |
| [stryker-js](https://github.com/stryker-mutator/stryker-js) | Mutation testing — tests the quality of your tests | `npm install -D @stryker-mutator/core` | Correctness |

## Review

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [code-review](https://github.com/anthropics/claude-plugins-official) | 4-agent parallel PR review with confidence scoring | `claude install-plugin anthropics/claude-plugins-official` | Correctness, Safety |
| [pr-review-toolkit](https://github.com/anthropics/claude-plugins-official) | 6 dimension-specific review agents (silent failures, type design, etc.) | Included in claude-plugins-official | Correctness, Safety |
| [trailofbits/skills](https://github.com/trailofbits/skills) | Structured security audit methodology | `claude install-skill trailofbits/skills` | Safety |

## Ship

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [claude-code-action](https://github.com/anthropics/claude-code-action) | @claude in GitHub PRs/issues for async review and fixes | Add GitHub Actions workflow YAML | Speed, Correctness |

## Reflect

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | Turns session corrections into persistent CLAUDE.md rules | `claude install-plugin BayramAnnakov/claude-reflect` | Speed, Maintainability |

## Outer Loop

| Tool | What it does | Install | Signal |
|------|-------------|---------|--------|
| [abtop](https://github.com/abi/abtop) | Live token/cost TUI for comparing agent session efficiency | `pip install abtop` | Cost Efficiency |
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | Security scanner for AI agent skills — detects prompt injection | `pip install skillspector` | Safety |

---

## What's NOT here

- **209 tools** are cataloged in [CATALOG.md](CATALOG.md) — this page is the curated subset
- **CONDITIONAL tools** (context-mode, shadcn/improve, ralph-claude-code, etc.) are documented in [evaluations/](evaluations/) with guidance on when they're worth it
- **Unevaluated tools** are tracked in [COMPARISON.md](COMPARISON.md) with evaluation coverage by stage
