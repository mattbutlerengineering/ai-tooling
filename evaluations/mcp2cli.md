# Evaluation: mcp2cli

**Repo:** [knowsuchagency/mcp2cli](https://github.com/knowsuchagency/mcp2cli)
**Stars:** 2,240 | **Last updated:** 2026-06-17 (pushed; created 2026-03-09) | **License:** MIT
**Dev loop stage:** Implement (a tool-access layer that changes how agents reach MCP/HTTP tools; cross-cutting)
**Layer:** Infrastructure (Python CLI, `uvx`/`uv tool install`)

---

## What it does

mcp2cli **turns any MCP server, OpenAPI spec, or GraphQL endpoint into a CLI at runtime, with zero codegen.** Point it at an endpoint and it discovers the available operations and exposes them as subcommands you (or an agent) can call directly:

```bash
mcp2cli --mcp https://mcp.example.com/sse --list
mcp2cli --mcp https://mcp.example.com/sse search --query "test"
mcp2cli --spec https://api.example.com/openapi.json list-pets
mcp2cli --graphql https://api.example.com/graphql users
```

Its headline claim is **token efficiency: "save 96–99% of the tokens wasted on tool schemas every turn."** The insight: when an MCP server is wired directly into an agent, the full JSON schema of *every* tool is injected into the context window on *every* turn. mcp2cli instead lets the agent invoke a CLI (one short command), so tool schemas live behind the CLI rather than in the prompt — the agent discovers/calls tools on demand via `--list` / `--search` instead of carrying all of them.

It ships an installable **skill** (`npx skills add knowsuchagency/mcp2cli`) that teaches Claude Code / Cursor / Codex how to use it — and can even **generate a new skill from an API** (`mcp2cli create a skill for https://api.example.com/openapi.json`). It handles **OAuth** (auth-code+PKCE and client-credentials) across all three modes with token caching/refresh in `~/.cache/mcp2cli/oauth/`, and supports `env:`/`file:` prefixes for secrets so credentials aren't passed as visible CLI args.

## How we tested it

**Source-grounded inspection — not installed, not run.** No CLI invoked, no MCP/OpenAPI endpoint connected. Claims come from the repository (GitHub metadata, README usage examples) — the project's own documentation, not measured token savings.

```bash
gh api repos/knowsuchagency/mcp2cli --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/knowsuchagency/mcp2cli/readme --jq '.content' | base64 -d   # usage, OAuth, skill, token claim
```

## What worked

- **Targets a real, well-known cost.** MCP tool-schema bloat in the context window is a genuine, widely-felt problem (every connected server taxes every turn). Moving schemas behind a CLI the agent calls on demand is a sound, well-motivated pattern — the same "search/index instead of load everything" idea the catalog's code-intelligence tools apply, here applied to *tools*.
- **Three protocols, one interface.** MCP + OpenAPI + GraphQL behind a uniform CLI is broadly useful and means any HTTP API becomes agent-callable without writing an MCP wrapper.
- **Zero codegen, runtime discovery.** Nothing to scaffold or maintain; `--list`/`--search` make it self-describing.
- **Production-grade auth.** Built-in OAuth (both flows) with caching/refresh, plus `env:`/`file:` secret handling, is more than most ad-hoc tool wrappers offer.
- **Ships its own teaching skill** and can generate skills from APIs — lowers the agent-adoption barrier; MIT-licensed, `uvx`-runnable.

## What didn't work or surprised us

- **Token-savings claim is self-reported and workload-dependent.** "96–99%" is a best-case framing (many tools, rarely used); real savings depend on how many servers you'd otherwise connect and how often tools are called. Unverified here.
- **Trades schema tokens for an indirection turn.** The agent must run `--list`/`--search` to discover tools before calling them — for a small number of frequently-used tools, direct MCP wiring may be simpler and not meaningfully more expensive.
- **No releases.** 0 tagged releases despite 2.2K stars and active pushes — versioning/stability signals are thin; pin a commit if you depend on it.
- **Another moving part in the trust path.** It brokers auth tokens and proxies tool calls; a CLI that holds OAuth tokens and hits arbitrary endpoints is a sensitive component to vet.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't change tool behavior; same underlying MCP/API calls. |
| Speed | + / neutral | Less context spent on schemas can mean faster, cheaper turns; offset by an extra discovery step. |
| Maintainability | + | One uniform CLI for MCP/OpenAPI/GraphQL; no generated wrappers to maintain. |
| Safety | neutral / − | Handles OAuth tokens + proxies calls — a credential-bearing component to trust; `env:`/`file:` secret handling mitigates arg leakage. |
| Cost Efficiency | + | Core value prop: cut tool-schema tokens injected every turn (magnitude workload-dependent). |

## Verdict

**CONDITIONAL** — adopt if you wire several MCP servers (or large OpenAPI/GraphQL APIs) into your agents and feel the per-turn tool-schema tax, or if you want any HTTP API callable from an agent without writing an MCP server. The on-demand-discovery pattern is well-reasoned, the multi-protocol + OAuth coverage is strong, and the bundled skill makes agent adoption easy. Hold off if you connect only one or two frequently-used tools (direct MCP wiring is simpler) or need release-tagged stability (none yet). Treat the "96–99%" number as best-case, not a guarantee.

Compared to neighbors: most catalog MCP entries are *servers that expose a capability*; mcp2cli is the inverse — **meta-infrastructure that makes any MCP/API agent-callable from a CLI while keeping schemas out of context**, conceptually adjacent to the token-efficiency tools (opensquilla, headroom, context-mode) but aimed at *tool access* rather than reasoning context.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp2cli](https://github.com/knowsuchagency/mcp2cli) | tool | Turn any MCP server, OpenAPI spec, or GraphQL endpoint into a CLI at runtime (zero codegen) so agents call tools on demand instead of loading every tool schema each turn | Wiring MCP servers into an agent injects all tool schemas into context every turn, wasting tokens | context-mode, headroom, opensrc |
