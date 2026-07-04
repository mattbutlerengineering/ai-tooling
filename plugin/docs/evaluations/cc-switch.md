# Evaluation: cc-switch

**Repo:** [farion1231/cc-switch](https://github.com/farion1231/cc-switch)
**Stars:** 104,624 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (sits beside the inner loop — manages which provider/config the agent runs against, not how it codes)
**Layer:** Infrastructure (config/provider management around the agent CLI)

---

## What it does

Catalog one-liner: "Cross-platform desktop app wrapping Claude Code, Codex, OpenCode, and more in one GUI." CC Switch is a Tauri 2 (Rust + web UI) desktop application that gives you a single visual interface to manage the *configuration* of seven AI coding tools — Claude Code, Claude Desktop, Codex, Gemini CLI, OpenCode, OpenClaw, and Hermes — rather than hand-editing each tool's JSON/TOML/`.env`.

The core mechanism is a **provider/profile switcher**. Each supported CLI reads its model/endpoint/API-key from its own config file (e.g. `~/.claude/settings.json`, Codex's TOML, Gemini's config). CC Switch stores a set of named "providers" (an endpoint + key + model preset) in a local SQLite database and, when you click switch, rewrites the target CLI's config file with atomic writes so the next `claude`/`codex`/`gemini` invocation talks to that provider. It ships 50+ presets (AWS Bedrock, NVIDIA NIM, and a long list of third-party Claude/Codex/Gemini *relay* services — most of which are paid sponsors of the project) plus one-click import, drag-to-sort, and a system-tray quick-switch menu. Beyond switching it has grown adjacent features: a **local proxy** with format conversion / auto-failover / circuit-breaker / health monitoring, a **unified MCP panel** that syncs MCP server definitions across the CLIs, a **Prompts** editor that syncs `CLAUDE.md`/`AGENTS.md`/`GEMINI.md`, a **Skills** installer (GitHub/ZIP, symlink or copy), a usage/cost dashboard, and cloud sync of provider data via Dropbox/OneDrive/iCloud/WebDAV.

Critically, it is a *config manager*, not a GUI client/IDE: you do not chat with the agent inside CC Switch. You use the app to pick which backend a CLI points at, then go run the CLI in your terminal as usual. The "wrapping ... in one GUI" framing in the catalog overstates it — it wraps the *configuration*, not the agent session.

## How we tested it

**Evidence:** REVIEW

Inspected the repository and its English README, pulled maturity metrics via the GitHub API, and read the feature list / "Why CC Switch?" section to determine the mechanism (config-file rewriting vs. a runtime GUI client). **Did not install or run the desktop app.** Doing so requires downloading a native Tauri binary for the host OS, and the app's whole value is in rewriting *real* CLI config files (`~/.claude/settings.json`, Codex/Gemini configs) and pointing them at provider endpoints — exercising that meaningfully would mean wiring up live API keys for third-party relay services in this environment, which is out of scope and against secret-handling rules. The verdict rests on source/README inspection and maturity signals, not a hands-on run.

```bash
gh api repos/farion1231/cc-switch --jq '{stars: .stargazers_count, license: .license.spdx_id, description, created_at, pushed_at, language, open_issues: .open_issues_count}'
# 104,624 stars, MIT, Rust (Tauri 2), created 2025-08-04, pushed 2026-06-19, 1509 open issues
gh api repos/farion1231/cc-switch/readme --jq '.content' | base64 -d   # feature list, mechanism, presets
grep -n -i "cc-switch\|claude-code-router\|claude-code-templates" CATALOG.md   # overlap check
```

## What worked

- **Solves a real, repetitive friction.** If you regularly switch a CLI between providers (official Anthropic vs. a relay, prod vs. a cheaper backend, Bedrock vs. direct), hand-editing JSON/TOML each time is error-prone. A one-click switch with atomic writes to a SQLite-backed store is a clean fix for that specific chore.
- **Genuinely broad coverage.** Seven CLIs, 50+ presets, and a unified MCP/Skills/Prompts panel that syncs across tools is more than any single-CLI config helper. For someone juggling Claude Code + Codex + Gemini, the cross-tool MCP/prompt sync is the most defensible feature.
- **Strong maturity signals.** 104K stars, MIT, native Rust/Tauri app for Windows/macOS/Linux, very active (pushed the day of evaluation), versioned releases (v3.x) with a changelog and release notes. Far past the single-author/days-old risk profile.
- **Non-destructive to the underlying CLIs.** It edits the same config files you would edit by hand; stop using it and your CLIs keep working with whatever config they last had. Low lock-in on the core switch feature.

## What didn't work or surprised us

- **It is a convenience layer, not a dev-loop quality tool.** It changes *which backend* the agent talks to and *how easily you reconfigure it* — it does not touch how the agent plans, implements, verifies, reviews, or ships. The code produced is identical to running the CLI with the same config set by hand.
- **The "GUI wrapping the agents" framing is misleading.** You don't run agent sessions inside CC Switch; it's a config/profile switcher plus a proxy, not a chat client or IDE. The catalog one-liner ("desktop app wrapping Claude Code...in one GUI") oversells it.
- **Heavy commercial/sponsor entanglement.** The README is dominated (~25 entries) by paid third-party "relay" services that resell Claude/Codex/Gemini access at a discount, each with an affiliate link and promo code, and many ship as built-in presets. The app is legitimately MIT and useful, but the preset list is also an affiliate funnel — and routing your keys/traffic through unofficial relays carries account-suspension and trust risk that the convenience can obscure.
- **Feature sprawl raises the surface area.** Beyond switching it now bundles a local proxy with failover/circuit-breaker, cloud sync of provider data (including keys) via Dropbox/OneDrive/iCloud/WebDAV, and a "signature bypass" utility. Each is a new place for an API key to leak or a config to corrupt; 1,509 open issues hints at the maintenance load of that breadth.
- **Overlaps the bare CLI for most users.** A developer who uses one provider on one CLI gets little — they set the config once. The value scales only with how often and across how many tools you switch.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Does not alter agent reasoning, prompts, or verification — same output as running the CLI with that config |
| Speed | + (situational) | One-click/tray provider switching and import beats hand-editing JSON/TOML; only matters if you switch often |
| Maintainability | neutral / + | No effect on your code; cross-tool MCP/prompt sync can reduce config drift across CLIs |
| Safety | - | Steers keys/traffic toward unofficial paid relays (suspension risk), adds cloud sync of provider data and a "signature bypass" utility — new exposure vs. a local-only CLI config |
| Cost Efficiency | + (indirect) | Makes it trivial to point a CLI at a cheaper relay/model, but the saving comes from the chosen backend, not the switcher; partly an affiliate funnel |

## Verdict

**SKIP**

CC Switch is a polished, very popular config/provider switcher, and for a narrow audience — someone constantly juggling multiple coding CLIs and multiple API backends — the one-click switch and cross-tool MCP/prompt sync are a real time-saver. But in this catalog's framework (tools that move quality signals *inside* the dev loop), it has almost no surface area: it doesn't write, review, test, or reason about code; it manages which endpoint the agent dials and how painlessly you reconfigure it. That is account/config administration adjacent to the loop, not part of it.

Two things push it from "borderline CONDITIONAL" to SKIP for the recommended stack. First, the cost-efficiency angle — its most catalog-relevant lever — is owned better by **claude-code-router (CONDITIONAL)**, which does programmatic, category-aware routing (`background`/`think`/`longContext`) that actually optimizes per-request cost while keeping the Claude Code UX; CC Switch only swaps a static config. Second, the README's dominant affiliate-relay funnel plus a "signature bypass" utility and cloud-synced provider data make it a net-negative on Safety, the one signal it clearly moves. Re-evaluate only if you specifically operate across 3+ CLIs daily and need a GUI to keep their configs in sync; otherwise the bare CLI config (set once) or claude-code-router (for cost routing) covers the real need.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cc-switch](https://github.com/farion1231/cc-switch) | tool | Cross-platform desktop app to switch provider/API configs across Claude Code, Codex, Gemini CLI, and more | Need a unified way to manage and switch provider configs across multiple agent CLIs | cherry-studio, superset, claude-squad, claude-code-router |
