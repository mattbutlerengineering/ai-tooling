# Evaluation: claude-code-templates

**Repo:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)
**Stars:** 28,175 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan (setup/config) + cross-cutting (Reflect/observability)
**Layer:** Infrastructure

---

## What it does

Catalog one-liner: "CLI tool for configuring and monitoring Claude Code sessions." In practice the project is two things bolted together:

1. **A component installer / marketplace** (the primary product, npm package `claude-code-templates`, also branded "aitmpl.com"). `npx claude-code-templates@latest` opens an interactive picker — or you pass flags to install specific agents, slash commands, MCP server configs, settings, hooks, and skills into your project's `.claude/` directory. The catalog (100+ components) is aggregated from other repos: Anthropic's official skills, wshobson/agents, obra/superpowers, awesome-claude-code, K-Dense scientific skills, etc. So it's a distribution layer over the existing community ecosystem, not original content.

2. **A bundle of operational tools** invoked via flags on the same CLI:
   - `--analytics` — a local web dashboard that monitors live Claude Code sessions (state detection, performance metrics) by reading session transcript files.
   - `--chats` — mobile-optimized viewer for Claude responses in real time, with optional `--tunnel` for remote access via Cloudflare Tunnel.
   - `--health-check` — diagnostics on the local Claude Code install.
   - `--plugins` — dashboard for marketplaces / installed plugins / permissions.

The mechanism for #1 is straightforward file scaffolding: the CLI fetches a component definition and writes the corresponding `.md`/`.json` into `.claude/agents`, `.claude/commands`, etc. The analytics/monitor mechanism is a Node web server that tails the same `~/.claude` session JSONL files that statusline tools (claude-hud, ccstatusline) read, then renders them in a browser instead of the terminal.

## How we tested it

**Evidence:** REVIEW

Method: **Inspected the GitHub repo and README, the npm package metadata, and the project's stated architecture. Did NOT install or run the CLI.** No hands-on metrics were produced; claims below are drawn from documentation plus comparison to already-evaluated peers (claude-hud, abtop).

```
gh api repos/davila7/claude-code-templates --jq '{stars,license,description,pushed_at,forks,open_issues}'
# stars 28175, MIT, "CLI tool for configuring and monitoring Claude Code",
# pushed_at 2026-06-19, forks 2930, open_issues 177

gh api repos/davila7/claude-code-templates/readme --jq '.content' | base64 -d
# full README — installer flags, --analytics / --chats / --health-check / --plugins, attribution list

npm view claude-code-templates version description dist-tags
# 1.29.2  "Component templates and tracking system for Claude Code"
```

## What worked

- **Genuinely huge reach and momentum**: 28K stars, 2.9K forks, pushed same-day, on Trendshift, sponsored (Z.AI, Neon, Vercel OSS, Claude for OSS). This is one of the most-starred Claude Code projects in existence — not abandonware.
- **Low-friction discovery**: `npx ... ` with no install plus a browsable web catalog (aitmpl.com) is a real onramp for someone bootstrapping a `.claude/` config from zero. The flag-driven install (`--agent`, `--command`, `--mcp`, `--hook`, `--setting`) is scriptable and composable.
- **The analytics/chats tools are a legitimate observability angle**: a browser dashboard that reads live session state is a different surface from a terminal statusline, and `--chats --tunnel` (view your agent from your phone) is a feature no peer tool in the catalog offers.
- **Honest attribution**: the README credits every upstream source with its license. It does not pretend to have authored the components it redistributes.
- **MIT licensed**, single npm entry point, active issue tracker.

## What didn't work or surprised us

- **It is mostly a redistribution layer, not original config tooling.** The "templates" are aggregated copies of components that already live in other repos (many already in our catalog: superpowers, wshobson/agents, anthropics/skills). Installing through it means trusting a middleman's copy and update cadence rather than the source.
- **The catalog one-liner is misleading.** "Configuring and monitoring sessions" describes the *secondary* `--analytics`/`--health-check` flags. The headline product is a component marketplace/installer. The framing as a config+monitoring peer to ccstatusline/claude-hud overstates the overlap — those are terminal statuslines; this is a web dashboard plus an installer.
- **Tracking / phone-home concern.** npm describes it as a "tracking system," the README mentions "track installations," and aitmpl.com is a hosted dashboard. The exact telemetry posture wasn't verified hands-on; for a tool that writes into `.claude/` and offers a Cloudflare tunnel, that warrants scrutiny before adoption. (Not confirmed malicious — flagged as unverified.)
- **Supply-chain surface.** A single CLI that installs hooks (arbitrary shell), MCP configs (arbitrary servers), and settings from a third-party-curated catalog is a meaningful trust delegation. Hooks especially run code.
- **Redundant with the catalog's own purpose.** This repo *is* a curated inventory of Claude Code components — which is exactly what ai-tooling's CATALOG.md/STACK.md already provide, but with hands-on evaluation. Routing installs through aitmpl.com bypasses that vetting.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Installs others' components; correctness depends on each component, not this layer |
| Speed | + | Fast zero-to-config bootstrap via `npx` + flags; analytics dashboard surfaces session state without manual commands |
| Maintainability | - | Adds a redistribution middleman between you and component sources; updates lag upstream and pin to aitmpl's copy |
| Safety | - | Installs hooks/MCPs/settings from a curated third party; "tracking system" telemetry and tunnel feature unverified |
| Cost Efficiency | neutral | No direct token impact; analytics may aid awareness but doesn't manage spend like claude-hud's cost line |

## Verdict

**SKIP** (for our stack) — **CONDITIONAL** as a discovery onramp for newcomers.

For this repo's purpose, claude-code-templates is redundant and lower-trust than what we already do: it's a redistribution marketplace for components we prefer to install from source and evaluate ourselves. The unverified "tracking system" framing, the Cloudflare-tunnel remote-access feature, and the supply-chain surface of installing hooks/MCPs through a middleman are enough to keep it out of the recommended stack. We SKIP adopting it as infrastructure.

It earns a CONDITIONAL note for one audience: someone bootstrapping a brand-new `.claude/` directory who wants to browse the community ecosystem in one place — the `npx` onramp and aitmpl.com catalog are genuinely convenient. The `--analytics`/`--chats` dashboard is a real (if separate) observability surface, but it overlaps and is dominated by purpose-built peers: claude-hud (CONDITIONAL, in-terminal HUD) and abtop (ADOPT, cross-session monitor) cover monitoring with tighter scope and clearer trust posture. The catalog one-liner should be corrected from "config + monitoring" to reflect that it is primarily a component installer/marketplace.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-templates](https://github.com/davila7/claude-code-templates) | tool | CLI + web marketplace to install Claude Code agents/commands/MCPs/hooks/skills, plus session analytics dashboard | Bootstrapping a `.claude/` config and discovering community components from one place | ccstatusline, claude-hud, abtop |
