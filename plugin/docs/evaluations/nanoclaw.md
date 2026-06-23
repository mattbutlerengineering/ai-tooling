# Evaluation: nanoclaw

**Repo:** [nanocoai/nanoclaw](https://github.com/nanocoai/nanoclaw)
**Stars:** 29,928 | **Last updated:** 2026-06-18 (release v2.1.17, 2026-06-17) | **License:** MIT
**Dev loop stage:** N/A for coding loop — general agent automation runtime (Plan/Implement/Verify/Review/Ship/Reflect are not its target)
**Layer:** Infrastructure

---

## What it does

Catalog one-liner: "Lightweight containerized agent runtime with WhatsApp, Telegram, Slack, Discord, Gmail integrations." nanoclaw is a self-hosted, lightweight alternative to OpenClaw: a single Node host process that orchestrates per-session Claude agents, each running in its own Docker container, triggered by inbound messages from chat apps. It pitches itself against OpenClaw's "~500K LOC, 53 config files, 70+ deps, application-level security" with a small, fully-readable codebase whose security comes from real OS-level container isolation rather than allowlists.

The mechanism: messaging apps → host process (router) → `inbound.db` → container (Bun + Claude Agent SDK) → `outbound.db` → host process (delivery) → messaging apps. When a message arrives, the host resolves it through an entity model (user → messaging group → agent group → session), writes it to that session's `inbound.db` (SQLite, exactly one writer), and wakes the container. An agent-runner inside the container polls `inbound.db`, runs Claude via Anthropic's official Claude Agent SDK, and writes responses to `outbound.db`, which the host polls and delivers back through the channel adapter. A 60s host-sweep handles stale detection, scheduled/recurring tasks, and due-message wake. Each agent group gets its own `CLAUDE.md`, memory, container, and only the mounts you allow. Credentials never enter the container — outbound API calls route through OneCLI's Agent Vault, which injects auth at proxy time with per-agent policies and rate limits.

Its product philosophy is unusual: trunk ships only the registry + infra. Channel adapters (WhatsApp, Telegram, Discord, Slack, Teams, iMessage, Matrix, etc.) and alternative providers (OpenCode, Ollama, Codex) live on separate `channels`/`providers` branches and are copied into *your fork* on demand via `/add-<channel>` skills. Customization is not config — it is telling Claude Code to modify your fork ("change the trigger word to @Bob", `/customize`, `/debug`). The install path (`bash nanoclaw.sh`) is a deterministic scripted bootstrap that hands off to Claude Code when a step needs judgment or fails.

## How we tested it

**Evidence:** REVIEW

Inspected the GitHub repo via the API on 2026-06-19: repo metadata, the full README, the top-level file tree, and the release history. Did NOT install or run nanoclaw. Installing it means a full system service: it installs Node/pnpm/Docker if missing, registers an Anthropic credential with OneCLI, builds an agent container image, and pairs a live messaging channel (Telegram/Discord/WhatsApp bot tokens or a local CLI). That is a standing background daemon plus third-party chat-app credentials — out of scope for a desk-side catalog review, and not meaningfully exercisable without wiring real messaging accounts. This is an architecture/surface-area review for catalog placement, using the same lens as the forkd (CONDITIONAL, agent-runtime infra) and aisuite (SKIP, app-building library) calibration evals. No metrics below are measured by us.

```bash
gh api repos/nanocoai/nanoclaw --jq '{stars,license,description,pushed_at,topics}'
gh api repos/nanocoai/nanoclaw/readme --jq '.content' | base64 -d        # full README
gh api repos/nanocoai/nanoclaw/contents --jq '.[].name'                  # top-level tree
gh api repos/nanocoai/nanoclaw/releases --jq '.[0:3][] | {tag,date}'     # v2.1.17 (2026-06-17)
grep -n -i "nanoclaw" CATALOG.md                                          # existing entry + overlaps
```

Reviewed: the host/container two-DB architecture, the entity/session isolation model, the `/add-<channel>` and `/add-<provider>` skill-installed registry design, the OneCLI Agent Vault credential model, the Claude-Agent-SDK-native runner, the scheduled-task/sweep loop, and the usage examples (sales-pipeline briefings, weekly news digests, recurring jobs).

## What worked

- **It genuinely runs on Claude Code / the Claude Agent SDK, and Claude Code is a first-class operator of its own codebase.** Unlike aisuite (a library you build *against*) or dify (a separate web platform), nanoclaw uses the official Claude Agent SDK for the agent runner, and `/customize`, `/debug`, error-recovery during setup, and every `/add-<channel>` skill are Claude Code surfaces. This is the most "Claude-native" entry in the messaging-agent space.
- **Real OS-level isolation, not permission theater.** Each agent group runs in its own Docker container (with optional Docker Sandboxes micro-VM or macOS-native Apple Container), seeing only explicitly-mounted dirs. Two SQLite files per session with a single writer each removes IPC/stdin-piping contention. Credentials never enter the container (OneCLI Agent Vault injects at the proxy). For a chat-triggered agent with bash access, this is a materially safer design than allowlist-based alternatives.
- **The "small enough to understand, customize = code changes" philosophy is a real differentiator.** Trunk is registry + infra only; channels/providers are skill-copied into your fork so you carry no features you didn't ask for. This is the opposite of the dify/lobehub "monolithic platform" model and aligns with this catalog's preference for many small, comprehensible files.
- **Strong traction and active maintenance.** ~30K stars, MIT, last release v2.1.17 on 2026-06-17 (the day before the review), a v1→v2 migration path, and a tight contribution policy (only security/bug/clear-improvement to trunk; everything else as skills). Not a weekend toy.
- **Multi-provider escape hatch.** `/add-opencode`, `/add-ollama-provider`, `/add-codex`, or `ANTHROPIC_BASE_URL` per agent group — provider is not locked to Anthropic despite the Claude-first default.

## What didn't work or surprised us

- **Its target is a personal/team chat assistant, not the coding dev loop.** Every first-class use case in the README is general life/work automation triggered by a messaging app: "send a sales-pipeline overview every weekday 9am", "compile AI news from HN+TechCrunch and message me a briefing", "review git history Friday and update the README". These are scheduled-assistant jobs, not Plan→Implement→Verify→Review→Ship→Reflect coding stages. Like dify and onyx, its center of gravity is agent automation, not improving how *you* write and ship code.
- **It is a standing infrastructure deployment, not a tool you drop into a repo.** Running it means a persistent host daemon, a built container image, paired chat-app credentials (WhatsApp/Telegram/Discord bots), and a system service (launchd/systemd). Heavy commitment for any single coding project; nothing here speeds up an ordinary Claude Code session in your codebase.
- **The Claude-Code-as-operator hooks are for operating nanoclaw, not your project.** The `/customize`, `/debug`, and `/add-<channel>` skills modify your *nanoclaw fork*. They do not act on your application codebase the way the coding-loop tools in this catalog do. The Claude Code integration is inward-facing.
- **Third-party hard dependency on OneCLI Agent Vault.** The credential-security story (and the "agents never hold raw keys" claim) is delegated to an external project. Solid design, but an additional moving part and trust anchor to stand up.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't write, test, or review your project's code; it runs chat-triggered assistant tasks |
| Speed | neutral | Doesn't speed up the coding dev loop; it automates standing messaging-driven jobs (briefings, digests) |
| Maintainability | neutral | A separate infra deployment; the "small, readable, fork-and-modify" design helps *nanoclaw's* maintainability, not your codebase's |
| Safety | + | Real Docker/micro-VM container isolation per agent group + OneCLI Agent Vault credential injection — but it protects the assistant runtime, not your dev workflow |
| Cost Efficiency | neutral | Self-hosted and provider-flexible (Ollama/OpenCode escape hatch), but no effect on the cost of your own agent coding sessions |

## Verdict

**SKIP** (for this catalog's dev-loop framing; an excellent project in its own domain)

nanoclaw is a well-engineered, genuinely Claude-native self-hosted assistant runtime — its container isolation, single-writer two-DB architecture, skill-installed channel registry, and "small enough to understand, customize by editing your fork" philosophy are all strong, and it earns its ~30K stars. It is more Claude-Code-connected than the other messaging-agent platforms (it runs on the Claude Agent SDK and uses Claude Code as its own operator). But its purpose is a personal/team chat assistant that automates standing jobs (briefings, digests, scheduled tasks) triggered by WhatsApp/Telegram/Discord/etc. — general agent automation, not the coding dev loop. By the same reasoning that sent dify and onyx to SKIP, it does not move the Correctness/Speed/Maintainability signals of *your* code-writing workflow, and its Claude Code hooks operate on the nanoclaw fork rather than your project.

**Adopt it when** you want a self-hosted, OS-isolated, Claude-powered chat assistant reachable from your messaging apps with scheduled tasks and per-agent memory — that is a real and valuable use case, just a different one than this catalog tracks. **Skip it for** the AI-assisted *coding* dev loop: it is standing assistant infrastructure (host daemon, container image, paired chat credentials, system service), not a tool that helps you Plan/Implement/Verify/Review/Ship code in a repo. It sits in the same general-agent-automation neighborhood as dify, onyx, and lobehub; the catalog should keep it listed for completeness but not treat it as a dev-loop tool.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [nanoclaw](https://github.com/nanocoai/nanoclaw) | platform | Lightweight containerized agent runtime with WhatsApp, Telegram, Slack, Discord, Gmail integration | Need a secure container-based assistant runtime triggered by messaging apps, with memory and scheduled jobs | goose, OpenHands; dify, lobehub (general agent automation) |
