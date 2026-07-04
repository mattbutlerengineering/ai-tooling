# Evaluation: OpenCode

**Repo:** [anomalyco/opencode](https://github.com/anomalyco/opencode)
**Stars:** 176,103 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A full open-source AI coding agent — terminal TUI, desktop app, and SDK — that competes directly with Claude Code. Built on TypeScript/Effect with first-party support for 11 providers (Anthropic, OpenAI, Google, Azure, Bedrock, OpenRouter, Mistral, GitLab, GitHub Copilot, and more). Ships two built-in agents: **build** (full-access) and **plan** (read-only exploration), plus a `@general` sub-agent for complex searches. The architecture includes a plugin SDK, skill system, command system, custom tools, MCP server support, workspace adapters, themes, and a desktop app (Electron). At 176K stars it is the most popular open-source coding agent by a wide margin.

## How we tested it

**Evidence:** REVIEW

Architecture review of the source tree, plugin SDK, provider system, config format, and recent commit history. Compared the developer surface (agents, tools, skills, commands, plugins) against Claude Code's equivalent systems.

```bash
gh api repos/anomalyco/opencode --jq '.stargazers_count, .updated_at, .license.spdx_id'
gh api repos/anomalyco/opencode/releases/latest --jq '.tag_name, .published_at'
gh api "repos/anomalyco/opencode/git/trees/dev?recursive=1" --jq '[.tree[].path | select(test("^packages/[^/]+$"))]'
```

v1.17.8 released 2026-06-17. 25 packages in the monorepo. 7,190 open issues, 21,431 forks.

## What worked

- **Multi-provider first-class support**: 11 providers with native integrations, not just OpenAI-compatible shims. Anthropic, Google, Azure, Bedrock, Copilot, OpenRouter, Mistral, GitLab all have dedicated provider configs.
- **Plugin SDK is well-typed**: TypeScript-first plugin system with workspace adapters, tool definitions, TUI extensions, and shell integration — more extensible than Claude Code's plugin/skill/hook model.
- **Plan agent is a genuine differentiator**: read-only mode that denies file edits and asks permission before bash commands. Useful for exploring unfamiliar codebases without risk. Claude Code's Plan tool exists but isn't a separate agent with its own permission model.
- **Desktop app**: cross-platform Electron app for macOS, Windows, and Linux. Claude Code has this too now but OpenCode had it earlier.
- **Extreme development velocity**: 32,837+ PRs, daily releases, massive contributor base.

## What didn't work or surprised us

- **Not a complement to Claude Code**: OpenCode replaces Claude Code entirely rather than enhancing it. You run one or the other, not both. This means adopting OpenCode means leaving the Claude Code ecosystem (plugins, skills, hooks).
- **Effect-heavy codebase**: Built on Effect-TS (functional programming library), which raises the contribution barrier significantly. Understanding the source requires Effect expertise.
- **7,190 open issues**: Volume suggests scaling challenges in community management and bug triage.
- **Sparse built-in skills/agents**: Only 1 skill (Effect) and 2 custom agents (triage, duplicate-pr) ship in the repo — the skill ecosystem depends on the broader SKILL.md ecosystem (same format as Claude Code).
- **No evaluation of actual usage**: This is an architecture review, not a hands-on test. We didn't run OpenCode on a real project due to the replacement nature (switching away from Claude Code for the test would be disruptive).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Same model access as Claude Code; correctness depends on model, not agent shell |
| Speed | + | Multi-provider support lets you choose fastest/cheapest model per task |
| Maintainability | neutral | Plugin/skill format is compatible with Claude Code's; no vendor lock-in |
| Safety | + | Plan agent with read-only mode adds a safety layer for exploration |
| Cost Efficiency | + | Provider flexibility enables cost optimization (Mistral, OpenRouter, local models) |

## Verdict

**CONDITIONAL**

Use when you need multi-provider flexibility (especially non-Anthropic models), want an open-source agent you can fork and modify, or need the plan agent's read-only exploration mode. For teams already invested in the Claude Code ecosystem (plugins, skills, hooks, marketplace), switching carries significant migration cost with no clear quality improvement — the underlying models matter more than the agent shell. The SKILL.md format is shared, so skills are portable between the two.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opencode](https://github.com/anomalyco/opencode) | platform | Open source coding agent with 11 providers, plan mode, plugin SDK (176K stars) | Want an open source alternative to Claude Code with multi-provider support | OpenHands, goose |
