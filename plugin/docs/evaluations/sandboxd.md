# Evaluation: sandboxd

**Repo:** [tastyeffectco/sandboxd](https://github.com/tastyeffectco/sandboxd)
**Stars:** 675 | **Last updated:** 2026-06-16 | **License:** MIT
**Dev loop stage:** Verify / Ship (preview-environment + agent-in-sandbox infrastructure)
**Layer:** Infrastructure

---

## What it does

sandboxd is a self-hosted control plane that gives "every user an isolated cloud dev environment, a built-in coding agent, and a live preview URL — self-hosted, on one machine, in one command." Its own framing is blunter: "The open-source engine for AI app-builder products" — i.e. the open-source backend behind Lovable / Bolt / v0 / Replit-style "describe an app → see it live" services.

The mechanism is deliberately small. One Go binary (the control plane) shells out to the `docker` CLI over a mounted host socket, Traefik v3 handles preview routing/TLS, and SQLite (WAL) is the source of truth with a reconciler that re-converges Docker to the DB on boot. You drive it over HTTP: `POST /sandbox` spins up a hardened `runc` container (cap-drop ALL, no-new-privileges, read-only rootfs) with a bind-mounted persistent workspace; `POST /v1/sandboxes/{id}/tasks` runs a coding agent headlessly inside that sandbox against a prompt and streams progress over SSE; the dev server inside self-registers a route so the app is instantly live at `http://s-<id>-<port>.preview.<domain>`. Cost density is the headline feature: sandboxes stop-on-idle (`docker stop`) to free RAM and wake-on-request transparently, so one box holds many tenants instead of one VM each. Critically, the OpenCode and Claude Code CLIs are pre-installed in every sandbox base image — so the "built-in coding agent" *is* Claude Code (or OpenCode) running inside the container, invoked through the tasks/exec API with an `ANTHROPIC_API_KEY` injected at create time.

## How we tested it

**Evidence:** REVIEW

Inspected the GitHub repo via the API on 2026-06-19: full README, `AGENTS.md` (the self-contained operating runbook), repo tree, release history, and topic tags. Did NOT install or run sandboxd — it requires a **Linux host with Docker Engine + the Compose plugin** and a control plane that mounts the host Docker socket (root-equivalent), none of which is appropriate to stand up on the macOS evaluation machine. This is an architecture/surface-area review for catalog placement, using the same lens applied to forkd (CONDITIONAL) and aisuite (SKIP). No metrics below are measured by us; any figure is the project's own claim.

```bash
gh api repos/tastyeffectco/sandboxd --jq '{stars,license,description,pushed_at,language,topics}'
gh api repos/tastyeffectco/sandboxd/readme --jq '.content' | base64 -d        # full README
gh api repos/tastyeffectco/sandboxd/contents --jq '.[].name'                  # tree
gh api repos/tastyeffectco/sandboxd/releases --jq '.[0:3][]'                  # 0.1.1 (2026-06-07)
gh api repos/tastyeffectco/sandboxd/contents/AGENTS.md --jq '.content' | base64 -d  # agent runbook
gh api "search/code?q=repo:tastyeffectco/sandboxd+mcp"                        # MCP refs: 0
```

Reviewed: the create → build → preview → sleep → wake → persist loop, the full HTTP API table (create/exec/stop/destroy/purge/files/tasks + SSE events), the architecture (Go + docker CLI + Traefik + SQLite, no Kubernetes/queue/DB server), the hardening posture and its explicit "harden before you scale" table, and the agent integration section (Claude Code / OpenCode pre-installed, key injected via `env` at create time).

## What worked

- **Honest, well-scoped positioning.** The README leads with an explicit "✅ Use it if you're running many sandboxes for other people / ❌ Skip it if you just need one or two containers for yourself — a shell script or `docker run` is simpler." A whole "Why not just a shell script?" section argues *against* its own adoption for one-offs. This is unusually candid and makes the trigger condition crisp.
- **Genuinely simple, readable infrastructure.** One Go binary over the `docker` CLI, Traefik for routing, SQLite as source of truth with a boot-time reconciler — no Kubernetes, no message queue, no separate DB. The claim that "you could read the whole thing in an afternoon" is plausible from the architecture, and lowers operator risk versus heavier sandbox platforms.
- **Stop-on-idle + wake-on-request is the real differentiator.** Idle sandboxes `docker stop` to release RAM and wake transparently on the next preview request (warming page, readiness probe, request hold), with workspaces persisted on disk. This density story ("$20 server vs $2,000 cluster") is the part that's well past a shell script.
- **Preview-URL routing with TLS, self-registered.** Each sandbox's dev server self-registers a Traefik route and gets a clean `s-<id>-<port>.preview.<domain>` URL; `*.localhost` resolves to 127.0.0.1 so it works locally with zero DNS/certs, and a wildcard Let's Encrypt DNS-01 cert covers production. This is the Verify/Ship surface — instant shareable previews of agent-generated apps.

## What didn't work or surprised us

- **No Claude Code surface — it *embeds* Claude Code, it doesn't *extend* it.** This is the decisive finding versus forkd. forkd ships a real `forkd-mcp` MCP server with documented `claude mcp add` registration, giving it a tool surface *inside* your dev loop. sandboxd has **zero MCP/plugin/skill/hook** (code search for "mcp" returns 0). Claude Code appears only as a CLI pre-baked into the sandbox base image, invoked headlessly through sandboxd's own HTTP `tasks` API. You don't add sandboxd to Claude Code; you run Claude Code inside sandboxd's containers. Its primary client is *your product backend*, not your editor.
- **It is a product backend, not a dev-loop tool.** The self-description — "the open-source engine for AI app-builder products," "is this a good foundation for a startup? Yes" — places its center of gravity even further toward "build a SaaS" than forkd's "give your agent platform fast sandboxes." For ordinary single-developer Plan/Implement/Verify/Review/Ship coding it does nothing.
- **Linux + Docker-socket-as-root prerequisites.** Requires a Linux host; the control plane mounts the host Docker socket and is "root-equivalent on the host." Cannot run as-is on the macOS evaluation machine, and the security model explicitly treats the host as a trust boundary you must harden.
- **Young, beta, container-only isolation by default.** Latest release 0.1.1 (2026-06-07; repo created 2026-06-03 — about two weeks old at review). README is explicit that several things are "simple on purpose": API auth is OFF by default, preview links are public, network egress is open/unlogged, no disk quotas, and isolation is hardened Docker (not VMs) — fine for your own users, but you must put untrusted strangers' code on gVisor/Kata/Firecracker or VM-per-tenant before scaling. These are stated caveats, not hidden ones, but they mean it is not production-ready out of the box.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't write or check your code; isolation prevents cross-tenant contamination in the product you build, but doesn't move correctness of your own dev work |
| Speed | + | Only if you build a multi-tenant preview product: one-command install + instant self-registered preview URLs collapse months of platform plumbing |
| Maintainability | neutral | An infra dependency (Go control plane + Docker socket + Traefik + SQLite); affects platform ops, not your codebase's maintainability |
| Safety | neutral | Hardened `runc` (cap-drop ALL, no-new-privileges, read-only rootfs) per sandbox, but auth off by default, public previews, container-not-VM isolation, root-equivalent host socket — net neutral for a dev workflow |
| Cost Efficiency | + | Only at fan-out scale: stop-on-idle + wake-on-request packs many tenants on one host (project's "$20 vs $2,000" claim) — but irrelevant to a single dev session |

## Verdict

**CONDITIONAL**

sandboxd is a clean, honest, MIT-licensed control plane for one specific job: standing up a multi-tenant AI app-builder / agent-platform backend with isolated per-user dev environments, headless coding agents, and instant preview URLs — on a single Docker host, in one command. The stop-on-idle/wake-on-request density model and self-registered preview routing are real value that genuinely is "well past a shell script." It lands a hair below forkd on dev-loop relevance: forkd at least ships an MCP server with `claude mcp add` registration, so it has a surface *inside* the dev loop; sandboxd *embeds* Claude Code in its sandboxes and is driven by your product backend over HTTP, so it has no Claude Code surface at all. It also openly markets itself as a startup backend ("the open-source engine for AI app-builder products"), pushing it toward the aisuite "build a product with it" end of the spectrum.

It clears SKIP rather than landing there because it does intervene at a real dev-loop stage — Verify/Ship, via isolated agent-generated previews — and per-branch / per-PR ephemeral preview environments are a legitimate (if narrow) dev-workflow use even outside the SaaS-builder framing.

**Adopt it when** you are building an AI app-builder, an agent/coding-playground product, or per-user / per-branch preview environments and want multi-tenant isolation + preview routing + idle/wake cost control + agent orchestration on one inexpensive Linux box without running Kubernetes. **Skip it for** ordinary single-developer Claude Code coding (especially on macOS), or any workflow that doesn't fan out many sandboxes for other people — the README itself tells you to use a shell script instead. It is the lighter, container-based, product-backend-shaped neighbor of forkd (microVM/KVM, lower-level) and nanoclaw (lighter sandbox orchestration).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sandboxd](https://github.com/tastyeffectco/sandboxd) | tool | Self-hosted dev sandboxes with preview URLs — one command, no Kubernetes | Building a multi-tenant AI app-builder/agent platform requires months of isolation, preview-routing, idle/wake, and agent-orchestration plumbing | forkd, nanoclaw |
