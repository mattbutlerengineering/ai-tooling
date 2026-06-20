# Evaluation: Mirage

**Repo:** [strukto-ai/mirage](https://github.com/strukto-ai/mirage)
**Stars:** 3,197 | **Last updated:** 2026-06-20 (pushed; created 2026-05-06) | **License:** Apache-2.0 | **Releases:** 2
**Dev loop stage:** Implement / cross-cutting (a tool/data-access layer agents use during execution)
**Layer:** Infrastructure (Python + TypeScript SDKs + CLI/daemon; FUSE-based mounts)

---

## What it does

Mirage is a **unified virtual filesystem for AI agents**: it mounts services and data sources — S3, Google Drive, Slack, Gmail, Redis, Postgres, GitHub, Notion, and more — **side-by-side as one filesystem**. The pitch: any LLM that already knows `bash` can read, `grep`, `cp`, and pipe across every backend with **zero new vocabulary** — "one interface instead of N SDKs and M MCPs."

```ts
const ws = new Workspace({
  '/data': new RAMResource(),
  '/s3': new S3Resource({ bucket: 'logs' }),
  '/slack': new SlackResource({ token: ... }),
})
await ws.execute('grep -r alert /slack/channels/general__C04QX/ | wc -l')
await ws.execute('cp /s3/report.csv /data/local.csv')
```

Key properties:
- **~50 built-in backends** mounted under one root: RAM/Disk/Redis, S3/R2/GCS/Supabase, Gmail/GDrive/GDocs/GSheets, GitHub/Linear/Notion/Trello, Slack/Discord/Telegram, Mongo/Postgres/LanceDB, SSH, etc.
- **Extensible/overridable commands** — register new commands or override one per resource+filetype (e.g. `cat` on S3 Parquet renders rows as JSON; `summarize /data/local.csv`).
- **Portable workspaces** — clone, snapshot, and version a workspace; agent runs move between machines without reconfiguring.
- **Embeddable** Python (`mirage-ai`) and TypeScript SDKs run in-process (FastAPI/Express/browser/edge); no separate process required.
- **Agent integrations** — OpenAI Agents SDK, Vercel AI SDK, LangChain, Pydantic AI, CAMEL, OpenHands via SDKs; Claude Code / Codex via a lightweight CLI + daemon.

Requirements: Python ≥3.11 / Node ≥20, macOS or Linux (FUSE-based mounts).

## How we tested it

**Source-grounded inspection — not installed, not run.** No workspace mounted, no backend connected. Claims come from the repository (GitHub metadata, README examples, backend list, 2 releases) — the project's own documentation, not observed behavior.

```bash
gh api repos/strukto-ai/mirage --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/strukto-ai/mirage/readme --jq '.content' | base64 -d   # VFS model, ~50 backends, command overrides, integrations
gh api repos/strukto-ai/mirage/releases --jq 'length'             # 2
```

## What worked

- **"Filesystem the LLM already understands" is an elegant access paradigm.** Reusing `bash`/`grep`/`cp`/pipes as the universal interface means zero per-tool schema in context and no new vocabulary for the model — a clever answer to the same "N tools bloat the prompt" problem mcp2cli targets, from the data-source angle.
- **Composition across services is the killer feature.** `grep`-ing Slack, `cp`-ing from S3 to local, and piping `find` output across backends "as naturally as a local disk" is genuinely powerful — cross-service pipelines that would otherwise be bespoke glue.
- **Breadth + extensibility.** ~50 backends out of the box, plus per-resource/per-filetype command overrides (Parquet `cat` → JSON), is a lot of leverage; the override model is the right extensibility seam.
- **Portable, snapshot-able workspaces** are a real operational nicety for moving/reproducing agent runs.
- **Broad integration + embeddable, Apache-2.0.** Works with the major agent SDKs and coding agents; runs in-process; permissive license.

## What didn't work or surprised us

- **Very young.** Created May 2026, only **2 releases** at evaluation — the API surface (and the depth/reliability of 50 backends) is unproven; expect churn and uneven backend maturity. "~50 backends" almost certainly means varying completeness per backend.
- **bash-as-interface cuts both ways.** Letting an agent `grep`/`cp`/pipe across S3, Gmail, Postgres, and Slack is powerful *and* a large blast radius — a wrong `rm`/`cp`/overwrite now spans production services. Permissioning/sandboxing per mount is critical and not detailed here.
- **Credential concentration = security surface.** Holding tokens for ~50 services behind one filesystem is a high-value target; this needs careful secret scoping (and pairs naturally with isolation like code-on-incus).
- **Platform-limited.** FUSE mounts → macOS/Linux only; no Windows.
- **Overlaps the MCP ecosystem it positions against.** "Instead of MCPs" is a real philosophical fork; teams invested in MCP servers must weigh adopting a parallel paradigm.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Uniform bash semantics + composable pipelines reduce bespoke glue and per-tool schema errors; backend maturity varies (young). |
| Speed | + | One interface across ~50 services + cross-service pipelines removes a lot of integration code and context overhead. |
| Maintainability | + | "One interface instead of N SDKs and M MCPs" genuinely reduces integration surface to maintain. |
| Safety | − | An agent with bash over S3/Gmail/Postgres/Slack has a large blast radius; ~50 concentrated credentials are a high-value target — needs strict per-mount scoping/sandboxing. |
| Cost Efficiency | + / neutral | No per-tool schemas in context; free/Apache-2.0; spends your own service/LLM costs. |

## Verdict

**CONDITIONAL** — adopt if you want agents to read/compose across many services through a single bash-native filesystem (and like that it sidesteps per-tool MCP/SDK schemas), and you can scope credentials and sandbox the mounts. The unified-VFS paradigm is genuinely elegant, the cross-service `grep`/`cp`/pipe composition is a real capability, and the breadth + Apache-2.0 + agent-SDK integrations are strong. Hold off where maturity matters: it's two releases old with ~50 backends of unverified per-backend depth, FUSE-limits it to macOS/Linux, and — most importantly — bash over 50 live services is a serious blast radius that demands tight permissioning and isolation (pair with something like code-on-incus). Pilot on read-only/non-prod mounts first.

Compared to neighbors: **mcp2cli** turns MCP/OpenAPI/GraphQL endpoints into a CLI (tool-call angle); MCP servers expose one service each as typed tools. Mirage is the **unified-filesystem alternative to MCP** — every service as a mountable path the LLM drives with bash, optimized for *cross-service composition* rather than per-tool calls. The most "treat all your data/services as one disk" option, with a correspondingly large safety surface.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mirage](https://github.com/strukto-ai/mirage) | tool | Unified virtual filesystem for agents — mounts ~50 services (S3, Slack, Gmail, Postgres, GitHub…) as one filesystem so an LLM reads/greps/pipes across all of them via bash; "one interface instead of N SDKs and M MCPs" (Apache-2.0) | Each service needs its own SDK/MCP and bloats agent context; want uniform, composable cross-service access with no new vocabulary | mcp2cli, context-mode |
