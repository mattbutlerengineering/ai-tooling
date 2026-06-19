# Evaluation: buildwithclaude

**Repo:** [davepoon/buildwithclaude](https://github.com/davepoon/buildwithclaude)
**Stars:** 3,087 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan (discover the right skill/agent/command/plugin before work)
**Layer:** Process

---

## What it does

A discovery hub and Claude Code plugin marketplace for finding skills, agents, commands, hooks, plugins, and marketplace collections to extend Claude Code, Claude Desktop, the Agent SDK, and OpenClaw. It is two things in one repo: (1) a curated in-repo collection installable as a Claude Code marketplace (`/plugin marketplace add davepoon/buildwithclaude`), self-reporting 117 agents, 175 commands, 28 hooks, 26 skills, and 51 bundled plugin packages across categorized directories; and (2) a web platform at buildwithclaude.com that indexes the broader ecosystem — README cites 20k+ community plugins, 4,500+ MCP servers, and 1,100+ plugin marketplaces — with browse/search/filter and one-click copy of install commands.

The mechanism: for the curated half, plugins follow a fixed file format (agent/command/hook markdown with frontmatter) and install via `/plugin install <name>@buildwithclaude` or `cp` from `plugins/*` into `~/.claude/`. For the discovery half, the value is the indexed, searchable web directory that aggregates extensions from across the Claude Code ecosystem so you can locate one without trawling GitHub. It is a directory/marketplace, not a tool that runs in your dev loop.

## How we tested it

Method: inspected the GitHub repo metadata and README only. Did NOT add the marketplace, install any plugin, or visit/exercise the web platform. No hands-on metrics are reported below — all counts are README/repo-sourced and noted as such.

```bash
gh api repos/davepoon/buildwithclaude
gh api repos/davepoon/buildwithclaude/readme --jq '.content' | base64 -d
```

Reviewed: repo description, topics, license, activity dates, and the README (marketplace install flow, curated collection counts, community-discovery counts, plugin format/contribution conventions, web UI feature list).

## What worked

- **Real, low-friction discovery surface**: a searchable web directory plus a native Claude Code marketplace covers both "find an extension" and "install it" in one place — directly the Plan-stage discovery problem this catalog addresses by hand.
- **Native marketplace integration**: works through Claude Code's first-party `/plugin marketplace` mechanism, so the curated half installs without bespoke tooling or scripts.
- **Broad scope**: indexes skills, agents, commands, hooks, plugins, MCP servers, and whole marketplaces — wider extension-type coverage than skills-only or agents-only lists.
- **Maturity signals are strong**: 3,087 stars, 390 forks, MIT license, active daily pushes (last push 2026-06-19), a hosted web platform, and a documented contribution format with `npm test` validation.

## What didn't work or surprised us

- **Not installed or exercised** — all capability and inventory claims (117 agents, 20k+ community plugins, 4,500+ MCP servers, 1,100+ marketplaces) are README-sourced and unverified.
- **Aggregator, not curator, on the discovery half**: the 20k+ community plugins and 4,500+ MCP servers are indexed from the ecosystem, not vetted — it trades curation for coverage, so it surfaces unvetted third-party code (same trade-off noted for ctx).
- **No quality/ranking signal described**: unlike ctx (graph-ranked, task-aware recommendations) or this catalog (per-tool evaluations), buildwithclaude is browse/search/filter — it tells you what exists, not which is good or which fits your task.
- **Overlap with awesome-claude-code is heavy**: both are ecosystem directories of Claude Code extensions; buildwithclaude adds a marketplace install path and a hosted UI, awesome-claude-code is a flat README list.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A directory; correctness depends on the extensions you pick from it, not the hub |
| Speed | + | Searchable UI + native marketplace install beats trawling GitHub for extensions |
| Maintainability | neutral | Helps you find tools; does not touch your codebase |
| Safety | - | Indexes unvetted third-party plugins/MCPs with no quality gate; installing surfaced extensions runs others' code |
| Cost Efficiency | neutral | Discovery aid; no direct token/cost effect |

## Verdict

**CONDITIONAL**

buildwithclaude is a credible, actively-maintained discovery hub and native Claude Code marketplace with broad extension-type coverage and a hosted searchable UI — genuine value for the Plan-stage problem of finding skills/agents/commands/plugins. As a reference directory the right call is to keep it as a discovery resource, not adopt it as an in-loop tool. Use it conditionally — when you need to browse or search the Claude Code extension ecosystem or want one-click marketplace installs — while accepting that the discovery half is an aggregator with no vetting or ranking, so installed extensions are unvetted third-party code. It overlaps with awesome-claude-code (flat list, no marketplace) and ctx (graph-ranked, task-aware recommendations vs. plain browse/search); pick buildwithclaude when you want a searchable UI plus a native install path rather than a curated list or automated recommender.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [buildwithclaude](https://github.com/davepoon/buildwithclaude) | reference | Hub and marketplace to find Claude skills, agents, commands, hooks, plugins, and MCP servers | Hard to discover and install the right Claude Code extension across a sprawling ecosystem | awesome-claude-code, awesome-claude-skills, ctx |
