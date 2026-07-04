# Evaluation: TanStack-cli

**Repo:** [TanStack/cli](https://github.com/TanStack/cli)
**Stars:** ~1,300 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (scaffolding + agent integration)
**Layer:** Tooling

---

## What it does

The official TanStack CLI for creating and managing TanStack Start (full-stack SSR) and TanStack Router (type-safe routing) applications. Beyond scaffolding (`npx @tanstack/cli create my-app`), it notably ships an **MCP server and Agent Skills installation** — so AI coding agents get first-class, framework-correct project setup and documentation.

The relevant angle for this catalog is that integration: rather than an agent scaffolding a TanStack app from stale training memory (and getting the routing/SSR wiring subtly wrong), the framework maintainers provide an MCP server and installable skills that give agents accurate, current scaffolding and conventions. It's an example of a framework shipping official agent-facing tooling.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and feature list (TanStack Start/Router scaffolding, `--router-only` SPA mode, MCP server, Agent Skills installation). Confirmed the official-CLI status and the agent-facing MCP + skills integration. Not run live, so condition-gated. Relevance here is the framework-maintained MCP/skills pattern, not general TanStack usage.

```bash
gh api repos/TanStack/cli --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/TanStack/cli/readme --jq '.content' | base64 -d
```

## What worked

- **Framework-maintained agent tooling.** An official MCP server + skills means agents scaffold and configure TanStack apps correctly and currently — directly counters the "LLM builds it from outdated memory" failure mode.
- **Reputable source.** TanStack (TanStack Query/Router/Table) is a widely-trusted ecosystem; official tooling carries weight.
- **Scaffolding + agent path in one CLI.** Both human `create` and agent MCP/skills live in one maintained tool.

## What didn't work or surprised us

- **Framework-specific.** Only relevant if you build with TanStack Start/Router; not a general-purpose tool.
- **Newer CLI.** ~1.3K stars; the MCP/skills surface is recent and evolving.
- **Catalog relevance is the pattern.** It's included as an exemplar of official framework MCP/skills (like pg-aiguide for Postgres), not a universal install.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Agents get framework-correct scaffolding/config, not stale guesses |
| Speed | + | One-command app creation + agent-ready setup |
| Maintainability | + | Conventions come from the maintainers, kept current |
| Safety | neutral | Scaffolding tool; no direct safety effect |
| Cost Efficiency | + | Free/OSS; fewer wasted agent turns fixing wrong scaffolds |

## Verdict

**CONDITIONAL**

Adopt if you build with TanStack Start/Router and want your coding agent to scaffold and configure projects correctly via the official MCP server + skills rather than from memory. Not relevant outside the TanStack ecosystem. It's catalogued as a strong example of the framework-maintained-MCP/skills pattern (cf. pg-aiguide) — worth knowing as that pattern spreads to more frameworks.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [TanStack-cli](https://github.com/TanStack/cli) | tool | Official TanStack CLI (MIT) — scaffolds TanStack Start/Router apps and ships an MCP server + Agent Skills install so agents get framework-correct scaffolding and docs | Agents scaffold framework apps incorrectly from stale memory; want official, framework-maintained MCP + skills for correct setup | pg-aiguide, context7, claude-context, design-extract |
