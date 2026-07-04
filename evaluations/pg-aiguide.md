# Evaluation: pg-aiguide

**Repo:** [timescale/pg-aiguide](https://github.com/timescale/pg-aiguide)
**Stars:** 1,768 | **Last updated:** 2026-06-10 (latest release v0.5.0, 2026-04-28) | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (writing schema/SQL) — touches Plan when modeling a data model up front
**Layer:** Tooling (knowledge layer, not infrastructure — it does not touch a live DB)

---

## What it does

MCP server + Claude plugin for Postgres — helps AI tools generate correct, idiomatic Postgres. The key thing to understand is the mechanism: **pg-aiguide is a knowledge/guidance layer, not a database-operations layer.** It never connects to your database, runs no migrations, and executes no SQL. It injects two kinds of Postgres expertise into the agent:

1. **Agent Skills** — a bundle of curated, opinionated SKILL.md files (a `postgres` router skill plus 7 specialized references: `design-postgres-tables`, `design-postgis-tables`, `pgvector-semantic-search`, `postgres-hybrid-text-search`, `setup-timescaledb-hypertables`, `find-hypertable-candidates`, `migrate-postgres-tables-to-hypertables`). These are dense, version-aware best-practice docs (e.g. "FK columns are not auto-indexed — add them", "prefer `BIGINT GENERATED ALWAYS AS IDENTITY`", "`UNIQUE ... NULLS NOT DISTINCT` for single-NULL constraints", "`uuidv7()` on PG18+", TOAST storage strategies). They load via progressive disclosure: the router skill triggers on Postgres keywords, then the agent loads only the relevant reference.

2. **A hosted MCP server** (`https://mcp.tigerdata.com/docs`) exposing two tools:
   - `search_docs` — semantic (pgvector), keyword (BM25), or hybrid (RRF-fused, `k=60`) search over the official PostgreSQL manual (scoped by version, `postgres_14`…`postgres_18`), PostGIS docs (`postgis_3.3`…`postgis_3.6`), and TimescaleDB/Tiger docs. Returns ranked doc chunks with distance/score/`rrf_score`.
   - `view_skill` — serves the same skill content over MCP (disabled in the Claude plugin variant, since the plugin ships the skills natively).

Three delivery surfaces from one repo: `npx skills add timescale/pg-aiguide` (works with Claude Code, Cursor, Codex, Gemini CLI, and 40+ agents per agentskills.io); the public hosted MCP server (any MCP client); and `claude plugin marketplace add timescale/pg-aiguide` → `claude plugin install pg@aiguide` (ships skills + wires the MCP server with `view_skill` disabled).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** Examined the GitHub repo metadata, the full README, the recursive file tree, release/tag history, recent commit messages, and read the actual artifacts: the `postgres` router `SKILL.md`, the `design-postgres-tables` reference, `API.md` (the MCP tool contract), and `.claude-plugin/marketplace.json`. The "see the difference" benchmark in the README (4× constraints, 55% more indexes) is **the vendor's own demo video, not reproduced here** — it is cited as a vendor claim, not verified output. No schemas were generated and no `search_docs` queries were run, so no metrics below are invented.

```bash
gh api repos/timescale/pg-aiguide --jq '{stars,license,description,pushed_at,created_at,open_issues}'
gh api repos/timescale/pg-aiguide/readme --jq '.content' | base64 -d
gh api "repos/timescale/pg-aiguide/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api "repos/timescale/pg-aiguide/contents/skills/postgres/SKILL.md" --jq '.content' | base64 -d
gh api "repos/timescale/pg-aiguide/contents/skills/design-postgres-tables/SKILL.md" --jq '.content' | base64 -d
gh api "repos/timescale/pg-aiguide/contents/API.md" --jq '.content' | base64 -d
gh api "repos/timescale/pg-aiguide/contents/.claude-plugin/marketplace.json" --jq '.content' | base64 -d
gh api repos/timescale/pg-aiguide/releases --jq '.[] | {tag:.tag_name,published:.published_at}'
# Catalog differentiation:
grep -inE "supabase|prisma|mcp-toolbox" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **The skills are genuinely high-density, opinionated Postgres expertise — not generic filler.** The `design-postgres-tables` reference packs real gotchas an LLM routinely gets wrong: FK columns aren't auto-indexed, `NULLS NOT DISTINCT` (PG15+), `GENERATED ALWAYS AS IDENTITY` over serials, `uuidv7()` on PG18+, `NUMERIC` for money, `TIMESTAMPTZ` over `TIMESTAMP`, TOAST storage strategies, MVCC dead-tuple awareness. This is exactly the "missing constraints/indexes, unaware of modern PG features" failure mode the catalog names.
- **Version-aware documentation search is a real differentiator.** `search_docs` scopes to a specific PG major (`postgres_17`) or PostGIS minor, so the agent retrieves manual text for the version actually in use rather than whatever the model memorized. Hybrid semantic+keyword with RRF fusion is a sound retrieval design, not a thin vector wrapper.
- **Clean separation of concerns vs. the DB-ops MCP servers.** It is purely a knowledge layer — no DB credentials, no connection string, no write access. That makes it safe to add broadly: there is nothing it can break in a live database.
- **Strong vendor credibility and maintenance.** TimescaleDB/TigerData is a reputable Postgres company; the skills carry the weight of a vendor that ships a Postgres distribution. Active development: regular releases through v0.5.0, hybrid-search and `npx skills` support added in 2026, hosted MCP endpoint maintained by the vendor.
- **Excellent install ergonomics across the ecosystem.** Three install paths and one-click buttons for Cursor, VS Code, Codex, Gemini CLI, Windsurf, Goose, LM Studio — low-friction adoption regardless of agent.

## What didn't work or surprised us

- **The "Postgres" framing partly masks a TimescaleDB on-ramp.** Of 7 specialized skills, 4 are TimescaleDB-specific (hypertables setup, candidate-finding, migration) or extension-specific (PostGIS, pgvector). The general-purpose value (`design-postgres-tables`, hybrid text search) is excellent and vendor-neutral, but the curation has a clear commercial gravity toward TimescaleDB/Tiger Cloud. Opinions like "prefer hypertables for time-series" are sound but vendor-aligned.
- **The hosted MCP server is a third-party network dependency.** `search_docs` calls `mcp.tigerdata.com` — an external service that sees your queries, can have downtime, and could change/deprecate. The skills-only install (`npx skills`) avoids this entirely and gives most of the value offline; the MCP server is the optional "deeper knowledge" upgrade.
- **Vendor benchmark is unverified.** The headline "4× constraints, 55% more indexes" is a single self-run demo in the README. Plausible given the skill density, but not independently reproduced here.
- **Opinionated defaults can over-fire.** Dense best-practice skills risk pushing maximal indexing/constraints onto simple schemas where they add maintenance cost. The skills do hedge ("denormalize only for measured, high-ROI reads"), but an agent applying them literally to a throwaway table may over-engineer.
- **Value is bounded by how much Postgres you write.** This is a Postgres-correctness specialist. For a non-Postgres or Postgres-light project it is dead weight.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (strong) | Targets the exact LLM Postgres failure mode — missing FK indexes, wrong types, no constraints, stale features. Version-scoped manual search grounds SQL in the actual PG version. |
| Speed | + | Skills front-load idiomatic patterns so the agent gets schemas right the first pass instead of iterating; less human round-trip fixing bad DDL. |
| Maintainability | + | Pushes normalization, explicit constraints, sane naming (`snake_case`), and modern identity patterns — schemas age better. Mild risk of over-indexing simple tables. |
| Safety | neutral / + | No DB access at all (no write/exec risk). Slight new exposure: queries to the third-party hosted MCP endpoint; skills-only install removes even that. |
| Cost Efficiency | + | Avoids wasted iteration loops on bad schema/SQL. Skills add some context tokens, but progressive disclosure loads only the relevant reference. Hosted MCP search is vendor-funded. |

## Verdict

**CONDITIONAL**

pg-aiguide is a well-built, vendor-credible knowledge layer that targets a real and specific failure mode (LLMs writing non-idiomatic, under-constrained, version-blind Postgres) and moves Correctness clearly without touching the database. It is categorically different from its catalog "overlaps": **supabase, prisma, and mcp-toolbox are DB-operations MCP servers that act on a live database (migrations, queries, studio); pg-aiguide acts on the agent's knowledge so the SQL it writes is correct in the first place.** They are complementary, not competing — pg-aiguide pairs naturally with prisma/supabase (generate idiomatic schema → then operate on the DB). **Adopt it when a project does meaningful Postgres schema/SQL work** (especially with pgvector, PostGIS, or TimescaleDB), preferring the `npx skills` / plugin skill install for offline correctness and adding the hosted MCP server only when you want version-scoped manual search. Not ADOPT-everywhere because it is Postgres-specific dead weight on non-Postgres projects and carries a (commercially-tilted) TimescaleDB lean plus a third-party network dependency in the MCP path. Not SKIP because the general `design-postgres-tables` and hybrid-search skills are genuinely strong, vendor-neutral correctness wins.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pg-aiguide](https://github.com/timescale/pg-aiguide) | MCP server | Skills + hosted MCP (version-scoped doc search) that teach AI tools to write correct, idiomatic Postgres/PostGIS/TimescaleDB — knowledge layer, no DB access | AI tools generate outdated, under-constrained, version-blind Postgres SQL and schemas | Complementary not competing: supabase / prisma / mcp-toolbox operate on a live DB; pg-aiguide improves the SQL the agent writes before it runs |
