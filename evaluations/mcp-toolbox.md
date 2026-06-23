# Evaluation: MCP Toolbox for Databases

**Repo:** [googleapis/mcp-toolbox](https://github.com/googleapis/mcp-toolbox)
**Stars:** 15,661 | **Last updated:** 2026-06-19 (latest release v1.5.0, 2026-06-18) | **License:** Apache-2.0
**Dev loop stage:** Implement (DB-aware coding, schema discovery) — with strong Infrastructure use beyond the dev loop (build production agent tools)
**Layer:** Tooling (prebuilt-tools mode, what the catalog cares about) / Infrastructure (custom-tools framework mode)

---

## What it does

Catalog one-liner: *Google's MCP server for databases — schema inspection, queries, migrations.* That captures one of its two modes. The mechanism is important because **mcp-toolbox is a single Go binary that serves a dual purpose**, and the two modes have very different risk and relevance profiles:

1. **Prebuilt-tools mode (the dev-loop-relevant one).** Run the binary with `--prebuilt=postgres` (or `bigquery`, `mysql`, `spanner`, `mongodb`, etc.) and it exposes a fixed set of generic MCP tools — `list_tables`, `execute_sql`, and similar — over stdio or HTTP. Point Claude Code / Gemini CLI / Codex at it via `mcp.json` and the agent can introspect schemas and run SQL against a live database in plain English. This is the "let the agent talk to my DB during development" use case, directly comparable to the prisma and supabase MCP servers in the catalog.

2. **Custom-tools framework mode (the infrastructure/production one).** You author a `tools.yaml` declaring `sources` (DB connections), `tools` (each a named, parameterized, pre-written SQL statement or semantic-search/NL2SQL operation), `toolsets` (named bundles), and `prompts`. The server then exposes *only those declared tools* to agents. This is the inverse of arbitrary `execute_sql`: the surface is locked to statements the author vetted, with typed parameters. It is meant for building production agents (ADK, LangChain, LlamaIndex, or via the official Python/JS/Go/Java SDKs) where you do **not** want an LLM emitting free-form SQL. It ships connection pooling, IAM/integrated auth, and OpenTelemetry metrics/tracing.

Originally "Gen AI Toolbox for Databases" (`genai-toolbox`), it predates MCP and was renamed to `mcp-toolbox` to align with MCP. It is a Google (`googleapis` org) project. Supported sources span Google Cloud (AlloyDB, BigQuery, Cloud SQL for PG/MySQL/SQL Server, Spanner, Firestore) and a broad non-Google set (PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, MongoDB, Redis, Elasticsearch, CockroachDB, ClickHouse, Couchbase, Neo4j, Snowflake, Trino).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** I verified the repository identity and read the primary artifacts via the GitHub API. I did not stand up the binary, connect a database, or invoke any tool, so no latency, query-result, or success-rate metrics appear below — none are invented.

Repo verification was the first task: the catalog name "mcp-toolbox" is ambiguous (several unrelated `*mcp-toolbox*` repos exist). `gh search repos mcp-toolbox` returned **`googleapis/mcp-toolbox`** (15.7K stars, "MCP Toolbox for Databases is an open source MCP server for databases") as the unambiguous top hit, and the catalog already links to exactly that URL. Google's `genai-toolbox` is the *same project* under its former name (confirmed by the rename banner in the README), so there is no candidate confusion: it is one repo.

```bash
gh search repos mcp-toolbox --limit 15 --json fullName,description,stargazersCount,url
gh api repos/googleapis/mcp-toolbox --jq '{stars:.stargazers_count,license:.license.spdx_id,description,pushed_at,created_at,open_issues:.open_issues_count,homepage,archived,language}'
gh api repos/googleapis/mcp-toolbox/releases --jq '.[] | {tag:.tag_name,published:.published_at}'
gh api repos/googleapis/mcp-toolbox/readme --jq '.content' | base64 -d   # full README
# Catalog cross-check:
grep -inE "mcp-toolbox|genai-toolbox|supabase|prisma" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Identity is unambiguous and the catalog link is already correct.** Despite the generic name, the GitHub search top hit, the star count, and the catalog URL all agree on `googleapis/mcp-toolbox`. The "strong candidate" `genai-toolbox` turned out to be the *prior name of the same repo*, not a competing project — verified by the in-README rename notice.
- **Strong maturity signals.** 15.7K stars, Apache-2.0, written in Go, created mid-2024, past a 1.0 release, on a steady ~2-week release cadence (v1.5.0 shipped 2026-06-18; pushed the same day I evaluated). Google-maintained with official SDKs in four languages (Python/JS/Go/Java), each its own published package. This is not a weekend project.
- **Genuinely broad database coverage** — far wider than prisma (Prisma-ORM-bound) or supabase (Supabase-bound). Postgres, MySQL, MongoDB, BigQuery, Spanner, Snowflake, ClickHouse, Neo4j, and more from one server.
- **The custom-tools framework is a real safety primitive.** Declaring vetted, parameterized statements in `tools.yaml` and exposing only those is meaningfully safer than handing an agent a raw `execute_sql`. For production agents this is the headline feature, and it is the part that differentiates mcp-toolbox from the other DB MCP servers in the catalog.
- **Production-grade operational features built in:** connection pooling, integrated/IAM auth, and OpenTelemetry tracing/metrics out of the box — things the lighter dev-time MCP servers don't offer.

## What didn't work or surprised us

- **Two products in one entry.** The catalog one-liner ("schema inspection, queries, migrations") describes prebuilt mode only and is slightly off — the prebuilt generic tools center on `list_tables`/`execute_sql` (introspection + arbitrary SQL); migrations are not the framing the README leads with. The bigger surprise is that the *primary* documented value is the custom-tools framework (run-time, production), which is **infrastructure for building agents, not a dev-loop tool**. The dev-loop-relevant slice is the smaller, secondary "Quick Start: Prebuilt Tools."
- **Prebuilt `execute_sql` against a live DB is the same blunt-instrument risk as any DB MCP server.** Pointing an agent at it with write credentials means the agent can mutate/drop data. The framework mode exists precisely to avoid this, but the easy on-ramp (`--prebuilt=postgres`) is the unsafe-by-default path; safety is opt-in via `tools.yaml`.
- **Commercial gravity toward Google Cloud.** Coverage is broad and the non-Google databases are real, but the deepest integrations, the managed-server upsell, and the "click-to-install" path (Google Antigravity MCP Store) all orbit Google Cloud. For a non-GCP shop the generic Postgres/MySQL path is fully usable but is clearly the less-promoted lane.
- **Heavier than the alternatives for simple needs.** It is a separate Go binary (or `npx @toolbox-sdk/server`) plus a YAML config for the safe mode. For "let Claude poke at my local Postgres during dev," prisma or supabase (or a thin DBHub-style server) is a lighter lift; mcp-toolbox earns its weight when you need many database types, locked-down tools, or the production SDK path.
- **220 open issues** — expected for a 15K-star, fast-moving Google repo, not a red flag on its own, but worth noting it is actively churning.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Agent reads real schemas and runs real queries instead of guessing table/column shapes; NL2SQL/semantic-search tools ground answers in actual data. |
| Speed | + | Removes the context-switch of hand-writing DB boilerplate or copy-pasting schema into the chat; one server covers many DB types. |
| Maintainability | neutral / + | Custom-tools `tools.yaml` makes the agent's DB surface explicit and version-controlled. But it adds a binary + config to operate; prebuilt mode adds no maintainability benefit. |
| Safety | + / − (mode-dependent) | Framework mode is a genuine safety win (vetted parameterized statements, IAM auth, restricted access). Prebuilt `execute_sql` against a write-credentialed live DB is the standard DB-MCP data-loss risk; safety is opt-in. |
| Cost Efficiency | + | Fewer wasted round-trips guessing schema; connection pooling. Free/open-source binary; running cost is just the DB it fronts. |

## Verdict

**CONDITIONAL**

mcp-toolbox is a mature, Google-maintained, genuinely capable MCP server with the broadest database coverage in this catalog's DB cluster. It is two things at once, and the verdict splits on which you use. **As a dev-loop tool (prebuilt mode), adopt it conditionally when you need agent access to a database type prisma/supabase don't cover, or to several DB types at once** — for a single local Postgres in development, the lighter prisma or supabase servers are a smaller lift. **As production infrastructure (custom-tools framework), it is a strong choice when you are building agents that must hit a database safely**, and there its locked-down, parameterized-tool model is a real differentiator rather than an overlap. Not ADOPT-everywhere because it is heavier than alternatives for simple dev needs, carries a Google-Cloud commercial tilt, and its easy on-ramp (raw `execute_sql`) is unsafe-by-default. Not SKIP because the maturity, breadth, and the framework's safety model are clearly best-in-class. It overlaps with prisma and supabase on the dev-time "agent talks to my DB" job; it is complementary to pg-aiguide, which improves the SQL the agent *writes* (knowledge layer, no DB access) rather than executing it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-toolbox](https://github.com/googleapis/mcp-toolbox) | MCP server | Google's open-source MCP server for 15+ databases — prebuilt tools (`list_tables`, `execute_sql`) for dev-time agent DB access, plus a `tools.yaml` framework for safe, parameterized production agent tools (15.7K stars) | Agents need to inspect schemas and query live databases (many DB types) during dev — and, for production, a way to expose only vetted, parameterized DB operations rather than arbitrary SQL | prisma, supabase (dev-time DB access); complementary to pg-aiguide (knowledge layer — improves SQL the agent writes, no DB access) |
