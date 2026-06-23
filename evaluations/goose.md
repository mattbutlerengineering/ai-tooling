# Evaluation: goose

**Repo:** [aaif-goose/goose](https://github.com/aaif-goose/goose) (moved from block/goose to Linux Foundation AAIF)
**Stars:** 49,786 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A general-purpose open-source AI agent — desktop app (macOS/Linux/Windows), full CLI, and embeddable REST API — built in Rust for performance and portability. Works with 15+ providers (Anthropic, OpenAI, Google, Ollama, OpenRouter, Azure, Bedrock, and more) via API keys or existing subscriptions through ACP (Agentic Context Protocol). Connects to 70+ extensions via MCP. Designed as a standalone agent runtime, not a Claude Code enhancement — you use goose *instead of* Claude Code, not alongside it.

The architecture is clean: a `goosed` server process exposes a REST API that any frontend (CLI, Electron desktop, custom web/mobile) can consume. Extensions are MCP servers. Providers are pluggable via a trait system. "Recipes" (YAML-based task definitions) enable guided workflows and multi-step automation. Custom distributions ("white labelling") let organizations ship preconfigured goose variants with their own providers, extensions, and branding.

## How we tested it

**Evidence:** REVIEW

Architecture review of the Rust crate structure (458 .rs files across 10 crates), CUSTOM_DISTROS.md, AGENTS.md, provider system, MCP integration, and recipe system. Compared against Claude Code (proprietary, model-locked) and opencode (CONDITIONAL, TypeScript/Effect, 176K stars) on developer surface, extensibility, and ecosystem maturity.

```bash
gh api repos/aaif-goose/goose --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api repos/aaif-goose/goose/releases --jq '.[0:3] | .[] | "\(.tag_name) \(.published_at)"'
gh api "repos/aaif-goose/goose/git/trees/main?recursive=1" --jq '.tree[].path' | grep '^crates/[^/]*$'
```

## What worked

- **Rust foundation is a genuine advantage.** 458 .rs files with clean crate separation (goose core, goose-cli, goose-server, goose-mcp, goose-providers, goose-sdk). Binary distribution means no Node/Python dependency hell — one binary, runs everywhere.
- **Provider abstraction is production-grade.** 15+ providers including ACP (use existing Claude/ChatGPT/Gemini subscriptions without API keys), declarative provider definitions in `crates/goose/src/providers/declarative/`, and a clean Provider trait for custom additions.
- **Custom distro system is unique.** No other coding agent in the catalog explicitly supports white-labelling — preconfigured providers, bundled extensions, custom branding, targeted audiences (devs, legal, designers). This makes goose viable as an enterprise platform, not just a dev tool.
- **Linux Foundation governance.** GOVERNANCE.md, MAINTAINERS.md, SECURITY.md, AAIF foundation membership — institutional backing that de-risks adoption for enterprises. OSSF Scorecard integration shows maturity.
- **Active development.** v1.38.0 (June 17), weekly releases, 5,273 forks, 214 open issues (manageable for a project this size), CI passing.
- **Recipe system for automation.** YAML-based task definitions with sub-recipes and subagents enable guided workflows without code — lower barrier than Claude Code's Workflow tool.

## What didn't work or surprised us

- **Replaces Claude Code entirely.** There's no "use goose alongside Claude Code" story. It's a different runtime with a different CLI, different config format, different extension model. Skills (.goosehints vs SKILL.md) overlap in concept but aren't interoperable without adaptation.
- **Ecosystem is thinner.** 70+ MCP extensions vs Claude Code's 200+ plugins, 50+ skills, and marketplace. The skill/recipe ecosystem is nascent compared to the Claude Code skill explosion (antigravity lists 1,595 SKILL.md files).
- **No built-in TDD enforcement or review workflow.** Claude Code's superpowers/agent-skills provide structured development methodology; goose provides raw agent capability. You'd need to build the methodology yourself via recipes or extensions.
- **Documentation is split.** goose-docs.ai for user docs, CUSTOM_DISTROS.md for white-labelling, AGENTS.md for development, README for overview — no single comprehensive reference.
- **ACP adds provider complexity.** Using existing AI subscriptions via ACP is clever but adds a proxy layer and authentication complexity that API keys don't have.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Same LLM-powered capabilities as Claude Code; no unique correctness advantages |
| Speed | + | Rust binary starts faster; recipe system enables automation without context overhead |
| Maintainability | + | Clean crate architecture; Provider trait makes adding models straightforward |
| Safety | + | Linux Foundation governance, OSSF Scorecard, SECURITY.md with responsible disclosure |
| Cost Efficiency | + | Model-agnostic lets you pick cheaper providers; ACP avoids API key costs for subscription users |

## Verdict

**CONDITIONAL**

Use goose when you need a model-agnostic agent platform (multi-provider support is its primary differentiator), when you're building a custom agent distribution for an organization, or when you want to avoid Claude Code's model lock-in. Choose Claude Code when you want the deepest ecosystem (skills, plugins, marketplace), structured development methodology (superpowers, agent-skills), and Anthropic-optimized performance. The two don't compose — it's a platform choice.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [goose](https://github.com/aaif-goose/goose) | platform | Model-agnostic AI agent with desktop, CLI, API — Rust, 15+ providers, custom distros (49.8K stars) | Want a provider-neutral, extensible agent platform with enterprise governance | OpenHands, opencode, claude-squad |
