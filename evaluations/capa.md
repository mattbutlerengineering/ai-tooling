# Evaluation: capa

**Repo:** [infragate/capa](https://github.com/infragate/capa)
**Stars:** 284 | **Last updated:** 2026-06-18 (v1.9.15) | **License:** MIT
**Dev loop stage:** Reflect (cross-project capability config; touches Plan when bootstrapping a repo's agent setup)
**Layer:** Infrastructure

---

## What it does

A package manager for AI coding agents. You declare skills, tools, rules, sub-agents, MCP servers, hooks, and plugins once in a `capabilities.yaml` next to your code, run `capa install`, and capa fans the config out into each agent's native format — `.claude/skills/`, `.claude/agents/`, `.claude/rules/`, `CLAUDE.md`, and `.mcp.json` for Claude Code; `.cursor/rules/` for Cursor; `AGENTS.md` for Codex; and so on across 35+ providers.

The mechanism is an ordered install pipeline (TypeScript/Bun). `capa install` parses the capabilities file, resolves provider list (flag → file → DB → auto-detect), clones/caches skill and plugin sources by SHA, then runs ~16 idempotent tasks that write per-provider artifacts: install-skills, install-rules, install-agent-instructions, install-subagents, install-hooks, configure-tools, register-mcp-server. Hand-written content is protected by "capa-managed" marker blocks — capa only touches the regions it tagged, and `prune-orphan-*` tasks remove artifacts that are no longer in the config. Resolved SHAs are pinned in `capabilities.lock` so a fresh clone gets identical bytes, and a local DB tracks managed files so `capa clean` can roll everything back from the DB even after the user edits the yaml.

Two architecturally interesting features beyond config fan-out: (1) capa registers a single `capa` MCP endpoint per agent and proxies the underlying tools, with `toolExposure: on-demand` exposing only `setup_tools`/`call_tool` meta-tools so the full catalog lazy-loads instead of front-loading (the README claims 19–40% cheaper inference across 150 trials on claude-opus-4-8 — vendor-reported, not independently verified). (2) Each sub-agent gets its own filtered `capa-<id>` MCP endpoint so a research sub-agent never holds a git-push tool. Every configured tool is also runnable from the shell via `capa sh <server> <tool>`.

## How we tested it

**Evidence:** REVIEW

Method: inspected the repo, README, maintainer docs (install-pipeline + per-provider matrix), the Claude Code provider doc, and the `capabilities.yaml` schema reference; pulled release/contributor/maintenance signals via the GitHub API. **Did not install or run capa** — this is a repo + schema + architecture review, not hands-on usage. The vendor's cost-savings figure is reported as-is and flagged as unverified. No metrics were invented.

```bash
gh api repos/infragate/capa --jq '{stars,license,description,pushed_at,created_at}'
gh api repos/infragate/capa/readme --jq '.content' | base64 -d
gh api repos/infragate/capa/contents/docs/providers/claude-code.md --jq '.content' | base64 -d
gh api repos/infragate/capa/contents/docs/README.md --jq '.content' | base64 -d   # install pipeline
gh api repos/infragate/capa/contents/skills/capabilities-manager/references/capabilities-schema.md --jq '.content' | base64 -d
gh api repos/infragate/capa/releases --jq '.[] | {tag,date}'   # 46+ releases, weekly cadence
gh api repos/infragate/capa/contributors --jq 'length'         # 4
# Catalog overlap scan:
grep -niE "reporails|openskills|skills-manage|agentic-stack|capa" CATALOG.md
```

## What worked

- **Genuinely deep Claude Code integration, not a lowest-common-denominator export.** The provider doc maps every primitive to its native CC home: skills → `.claude/skills/<id>/`, rules → `.claude/rules/<id>.md` with `appliesTo`→`paths` frontmatter, sub-agents → `.claude/agents/<id>.md`, hooks → `.claude/settings.json` with canonical-event translation (`beforeTool→PreToolUse`, auto `matcher: Bash` for shell hooks), MCP → `.mcp.json`. It even respects the subtlety that an `AGENTS.md` is only written if another active provider needs it. This is the work most "portable config" tools skip.
- **Marker blocks + DB-tracked managed files + lockfile are the right primitives.** Idempotent install, surgical edits to only capa-tagged regions, `prune-orphan-*` cleanup, SHA pinning, and a DB-driven `capa clean` that survives manual yaml edits. This is a real config-management design, not a glorified template renderer.
- **Strong maintenance signals for a small-star project.** 46+ releases, roughly weekly cadence (v1.9.15 shipped the day before this eval), MIT, TypeScript/Bun, dedicated security workflow + SECURITY.md, dependabot, issue/PR templates. Active and disciplined.
- **The MCP-proxy angle is a differentiator vs pure config tools.** One endpoint per agent, per-sub-agent tool filtering, and `on-demand` lazy tool loading address a real context/safety problem that reporails, openskills, and skills-manage do not touch.

## What didn't work or surprised us

- **No license field via the API despite an MIT badge/`LICENSE` file** — minor metadata quirk (the repo does carry MIT), but worth noting.
- **284 stars and 4 contributors.** Real maturity risk for an infrastructure tool you'd standardize a team's whole agent config on. It introduces a yaml format, a local server/DB, and a cache as new dependencies in your repo — meaningful lock-in for an early-stage project.
- **The value proposition is multi-editor.** For a developer working primarily in Claude Code, the core pain capa solves (keeping `.cursor/rules/`, `CLAUDE.md`, and `AGENTS.md` in sync) largely doesn't exist — Claude Code already reads `.claude/` and `CLAUDE.md` natively. You'd be adding a build step and a config indirection layer to manage files the agent already consumes directly.
- **Cost-savings claim is vendor-reported.** "19–40% cheaper, 150 trials on claude-opus-4-8" is plausible given the lazy-load design but is not independently reproduced here; treat as a hypothesis, not a result.
- **Runtime dependency on a local capa server + DB.** `configure-tools` POSTs to a local server and credentials flow through a web UI. That's more moving parts than a file-emitting CLI, and another thing to keep running.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't change code quality; it standardizes which rules/skills the agent loads, which can indirectly help consistency, but it writes no code |
| Speed | neutral/+ | One-command fan-out + lockfile makes onboarding a new clone fast; offset by the added install step and running server for a single-editor user |
| Maintainability | + | Single source of truth, marker-block-safe edits, SHA-pinned lockfile, and DB-driven rollback genuinely reduce config drift — strongest for teams spanning multiple editors |
| Safety | + | Per-sub-agent filtered MCP endpoints and a `security` block (blockedPhrases/allowedCharacters) restrict tool exposure per agent — a real least-privilege lever |
| Cost Efficiency | + (claimed) | `on-demand` tool exposure lazy-loads tools instead of front-loading the catalog; vendor reports 19–40% savings, unverified here |

## Verdict

**CONDITIONAL**

capa is a well-engineered, actively maintained config-as-code package manager for AI agents, with deeper per-editor integration (especially Claude Code) and more thoughtful primitives (marker blocks, lockfile, per-sub-agent MCP filtering, lazy tool loading) than the other multi-editor config tools in the catalog. The decisive question is multi-editor scope: its core pain — keeping `.cursor/rules/`, `CLAUDE.md`, and `AGENTS.md` in sync — barely exists for someone working primarily in Claude Code, where `.claude/` and `CLAUDE.md` are read natively. **Adopt when** you (a) run agents across two or more editors (Cursor + Claude Code + Codex, etc.) or maintain a shared agent config for a team, and (b) are comfortable depending on a 284-star tool's yaml format, local server, and DB. **Skip if** you're a single-editor Claude Code user — it adds an indirection layer over files the agent already consumes directly. Re-evaluate the maturity caveat as the star/contributor base grows.

Versus neighbors: **reporails/cli** is diagnostics (validate existing instructions), capa is generation/management — complementary, as the catalog already notes. **openskills** and **skills-manage** only move *skills* across editors; capa covers the full primitive set (skills + rules + sub-agents + hooks + MCP + plugins) and adds an MCP proxy layer. **agentic-stack** ships a portable `.agent/` folder (brain + memory); capa instead emits each editor's native files from one source — different strategy for the same portability goal.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [capa](https://github.com/infragate/capa) | tool | One capabilities.yaml wires skills, tools, rules, sub-agents, MCP servers, hooks, and plugins into Claude Code, Cursor, Codex, and 35+ AI agents | Configuring agent capabilities is per-tool; need a single version-controlled config format portable across editors | reporails/cli (complementary: capa = config, reporails = diagnostics), openskills, skills-manage, agentic-stack |
