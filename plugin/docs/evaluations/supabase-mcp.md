# Evaluation: Supabase MCP

**Repo:** [supabase/mcp](https://github.com/supabase/mcp)
**Stars:** 2,742 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

MCP server that connects Claude (and other AI assistants) directly to Supabase projects for database management, edge functions, storage, branching, and debugging. Uses HTTP transport with OAuth 2.1 authentication — no API keys to manage. Claude can list tables, run SQL, apply migrations, deploy edge functions, search Supabase docs, generate TypeScript types, and manage branches.

## How we tested it

**Evidence:** REVIEW

README-based evaluation. The server is HTTP-hosted by Supabase (`https://mcp.supabase.com/mcp`) and requires an active Supabase project with OAuth login. No local Supabase project was available to configure and invoke tools hands-on. Evaluation is based on the comprehensive tool surface documented in the README, architecture decisions (HTTP+OAuth vs stdio+token), security model, and comparison with the Prisma MCP server.

```
# Configuration (not tested — no active Supabase project)
{
  "mcpServers": {
    "supabase": {
      "type": "http",
      "url": "https://mcp.supabase.com/mcp?project_ref=<ref>&read_only=true"
    }
  }
}
```

## What worked

- **Granular security model**: Read-only mode, project scoping, and feature groups let you tightly control what the LLM can touch — far beyond what most MCP servers offer
- **Zero-config auth**: OAuth 2.1 flow means no API keys to manage or leak; the MCP client handles login automatically
- **Full platform coverage**: 25+ tools across database, edge functions, storage, branching, debugging, and docs — covers the entire Supabase surface, not just SQL
- **Migration tracking**: `apply_migration` separates DDL from queries, so schema changes are tracked and replayable — Claude generates proper migrations, not ad-hoc ALTER statements
- **Built-in docs search**: `search_docs` tool lets the LLM self-serve Supabase documentation, reducing hallucinated API calls
- **TypeScript type generation**: `generate_typescript_types` from live schema eliminates manual type sync
- **Prompt injection mitigations**: SQL results are wrapped with instructions to discourage LLMs from following injected commands in data — not foolproof but shows security awareness

## What didn't work or surprised us

- **Cloud-hosted only for full features**: Local CLI and self-hosted modes offer a "limited subset of tools" with no OAuth — the full experience requires a Supabase cloud project
- **No RLS policy management**: Despite Supabase's RLS-first security model, there are no dedicated tools for creating, listing, or testing Row Level Security policies — you'd need to use raw `execute_sql`
- **Storage disabled by default**: Storage tools require explicit opt-in via `features=storage`, which means users might not discover them
- **Pre-1.0 disclaimer**: Breaking changes expected between versions, though the README notes LLMs adapt automatically to available tools
- **No offline/local-first workflow**: Unlike Prisma MCP which works with any local database, this server requires network access to Supabase infrastructure

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Migration tracking separates DDL from queries; TypeScript type generation from live schema eliminates type drift |
| Speed | + | Full Supabase management from the editor — no dashboard context-switching for schema design, function deployment, or log inspection |
| Maintainability | + | Migrations are tracked and replayable; generated types stay in sync with schema |
| Safety | + | Read-only mode, project scoping, feature groups, and prompt injection mitigations — strongest security model of any MCP server in the catalog |
| Cost Efficiency | neutral | Free and open source; requires an existing Supabase project (free tier available) |

## Verdict

**CONDITIONAL**

Use when building on Supabase. The server's security model (read-only mode, project scoping, feature groups) is the most thoughtful of any MCP server in the catalog and sets a good standard. The 25+ tools cover the full Supabase platform surface. However, it's strictly Supabase-specific — if you're using raw Postgres or another provider, the Prisma MCP server is the better fit. The cloud-hosted requirement for full features and the lack of dedicated RLS tooling are minor gaps that don't block adoption for Supabase projects.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [supabase](https://github.com/supabase/mcp) | MCP server | Connects Claude to Supabase for database, functions, storage, and branch management | Eliminates dashboard context-switching for schema design, migrations, edge functions, and debugging | prisma |
