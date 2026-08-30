# Evaluation: Prisma MCP Server

**Repo:** [prisma/claude-plugin](https://github.com/prisma/claude-plugin) (plugin manifest) / [prisma/prisma](https://github.com/prisma/prisma) (MCP implementation)
**Stars:** 46,347 (main Prisma repo) | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Official Prisma MCP integration distributed as part of the `claude-plugins-official` marketplace. Provides two MCP servers:

1. **Prisma-Local** (stdio, `npx prisma mcp`) — 4 tools for local database development:
   - `migrate-dev` — create and apply migrations with shadow database drift detection
   - `migrate-reset` — drop and recreate database, replay all migrations, run seeds
   - `migrate-status` — compare local migration files vs database `_prisma_migrations` table
   - `Prisma-Studio` — open the visual data browser

2. **Prisma-Remote** (HTTP, `mcp.prisma.io`) — OAuth-authenticated cloud server for Prisma Postgres provisioning, connection string management, and remote database operations.

The local server runs within the Prisma CLI itself (v7.8.0+) — no separate MCP package to install. The agent calls `migrate-dev` with a migration name and project path, and Prisma handles the full 5-step migration cycle (shadow database replay → pending migration detection → new migration generation → application → client generation).

## How we tested it

**Evidence:** REVIEW

Architecture-level evaluation. Loaded all tool schemas via ToolSearch and examined each tool's parameters, descriptions, and behavior contracts. Inspected the plugin manifest at `~/.claude/plugins/cache/claude-plugins-official/prisma/`, which revealed the two-server architecture (Prisma-Local via `npx prisma mcp`, Prisma-Remote via `https://mcp.prisma.io/mcp`). No active Prisma project was available for hands-on migration testing.

```bash
# Plugin config discovered at:
cat ~/.claude/plugins/cache/claude-plugins-official/prisma/815dbc4a045a/.mcp.json
# -> Prisma-Local: { "command": "npx", "args": ["-y", "prisma", "mcp"] }
# -> Prisma-Remote: { "type": "http", "url": "https://mcp.prisma.io/mcp" }

# Tool schemas loaded:
# migrate-dev: requires { name: string, projectCWD: string }
# migrate-reset: requires { projectCWD: string }
# migrate-status: requires { projectCWD: string }
# Prisma-Studio: requires { projectCWD: string }
```

## What worked

- **Zero-install MCP** — the local server ships inside the Prisma CLI (`npx prisma mcp`), no separate package to manage. Any project with Prisma gets MCP for free.
- **Well-scoped tool set** — 4 tools covering the core migration lifecycle. Each tool description includes the exact multi-step process Prisma will execute, so the agent knows what it's invoking.
- **migrate-dev descriptions are excellent** — the 5-step process (shadow database replay, pending detection, new generation, application, client generation) is fully documented in the tool schema itself, giving the agent enough context to decide when to call it.
- **Separation of concerns** — local server for development migrations, remote server for cloud provisioning. The agent can use local tools without any cloud dependency.
- **Destructive operation awareness** — `migrate-reset` description explicitly warns "Only run on development database — never on production!" and suggests confirming with the user.

## What didn't work or surprised us

- **Only 4 tools on the local server** — no `prisma db push`, `prisma db pull`, `prisma generate`, `prisma format`, or `prisma validate`. The agent can't introspect an existing database, push schema changes without migrations, or validate schema files through MCP — it has to fall back to Bash for those operations.
- **No schema reading tool** — the agent can't read or query `schema.prisma` through MCP. It must use the Read tool separately, then call migrate-dev. A `schema-read` or `schema-validate` tool would close this gap.
- **Prisma-Remote requires OAuth** — the cloud server needs interactive browser authentication. In headless/CI contexts, only the local server is available.
- **No query execution** — unlike supabase MCP (which can run arbitrary SQL), Prisma's MCP has no `query` or `execute` tool. The agent can migrate the schema but can't inspect or modify data through MCP (Prisma Studio opens a browser UI, not an MCP data channel).
- **Private plugin repo** — `prisma/claude-plugin` has 0 stars and no public README. Discovery and documentation depend entirely on the marketplace install path.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Shadow database drift detection catches schema divergence before it causes problems |
| Speed | + | Agent can run migrations without switching to terminal; zero-install via existing Prisma CLI |
| Maintainability | neutral | Migrations are the same Prisma migrations you'd create manually |
| Safety | + | Destructive operations (reset) include explicit warnings; shadow database prevents silent drift |
| Cost Efficiency | neutral | 4 tools is minimal context overhead |

## Verdict

**discovery-log — tentative read**

Use when your project uses Prisma ORM. The local MCP server is well-designed for the migration lifecycle it covers — zero-install, drift-aware, with good destructive-operation warnings. However, the tool set is narrow (4 tools vs Supabase's 25+) with no query execution, schema introspection, or `db push` support. The agent still needs Bash for most Prisma operations beyond migrations. Choose Supabase MCP if you're on Supabase; choose Prisma MCP if you're on Prisma — they solve complementary problems (Supabase = full database operations, Prisma = migration lifecycle).

_Headline demoted from `CONDITIONAL` to `discovery-log` (2026-08-07, #433). ADR-0005 grants that word to a tool we exercised (`Evidence` MEASURED/RUN) or one carrying a real `adopt-if:` gate; this is a `REVIEW` read with neither, so the conditional-sounding prose above is a **tentative** read rather than a verdict (detectors T and AB). The row it belongs to reads `discovery-log` and now resolves here — before #433 it resolved to a stub, so the disagreement was invisible to detector D. Nothing about the tool changed; only the claim this file was entitled to make about it._

## Triage note

**From `prisma.md`, merged 2026-08-07 (#433).** A second bulk pass wrote a placeholder for this tool beside this file, believing none existed; its reasoning is preserved here verbatim.

Left at `discovery-log`, with one row-shape observation worth recording.

The CATALOG entry links to `prisma/prisma` — the whole ORM, ★46.9K — while the catalogued artifact is
the **MCP server that ships inside it**. The star count therefore measures the ORM's adoption, not the
MCP server's, and reading it as evidence about this integration would be a mistake. It is a milder
instance of the pattern this triage lane keeps finding (`diagnosing-bugs` and `implement` inside
`mattpocock/skills`; `confluence` and `jira` inside `mcp-atlassian`): a facet of a larger artifact
entered as an independent lead.

That is not a reason to SKIP it. If you already use Prisma, the MCP server comes with the tooling you
have, which makes it the lowest-friction option in the DB cluster — and the `mcp-toolbox` eval says as
much, naming prisma and supabase as the smaller lift for a single local database.

Left because the promotion question ("does agent-driven migration actually help, and how badly can it
go wrong") needs a hands-on run against a real schema, and because whether the row should point at the
ORM or a narrower MCP path is a catalog-shape decision rather than a verdict.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

**Re-triaged 2026-08-30 by the P5 ships-inside band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567)):** no change. `prisma/prisma` (the ★46.9K ORM this row's `Ships inside` cell names) is not itself a candidate catalog row — it's an ORM, not AI-dev tooling — so "settle the container" has no target here; that is the unfixable shape #405/#431 already name for this row. Left at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| prisma | MCP server | Database operations via Prisma ORM (migrations, studio, status) | Agent needs to interact with databases during development | supabase, mcp-toolbox |
