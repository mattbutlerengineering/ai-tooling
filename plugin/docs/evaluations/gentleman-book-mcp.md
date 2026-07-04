# Evaluation: gentleman-book-mcp

**Repo:** [Alan-TheGentleman/gentleman-book-mcp](https://github.com/Alan-TheGentleman/gentleman-book-mcp)
**Stars:** 102 | **Last updated:** 2025-12-29 (created 2025-12-24; no releases/tags) | **License:** MIT (server code) — **but see content licensing below**
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (architecture/design decisions) — touches Implement when applying a pattern
**Layer:** Tooling (knowledge layer — serves book text to the agent; no live system access)

---

## What it does

A Go MCP server that exposes the [Gentleman Programming Book](https://github.com/Alan-TheGentleman/gentleman-programming-book) — 18 chapters of software-architecture and frontend-development content — to MCP clients. The catalog one-liner is "18 chapters of software architecture knowledge accessible to AI agents."

The mechanism: the server does **not** ship the book. It reads the book's MDX source files from a local path (`BOOK_PATH`, default `~/work/gentleman-programming-book/src/data/book`), which you must clone separately. It then parses those MDX files (`internal/book/parser.go`, `models.go`) and surfaces them through three tiers of MCP capabilities:

- **Level 1 tools:** `list_chapters`, `read_chapter` (chapter or section), `search_book` (keyword), `get_book_index`.
- **Level 2 resources + prompts:** `book://index/{es,en}` resources, plus canned prompts `explain_concept`, `compare_patterns`, `summarize_chapter`.
- **Level 3 semantic search:** `semantic_search` (natural-language), `build_semantic_index`, `semantic_status`, backed by embeddings from either OpenAI (`OPENAI_API_KEY`) or local Ollama (`nomic-embed-text` by default). This is the only tier that calls an external/embedding service; Levels 1–2 are pure local file reads.

So it is a retrieval layer over one specific opinionated book, not a general knowledge base. The chapter list mixes architecture (Hexagonal, Clean Architecture, Software Architecture/microservices) with language/framework material (Go, React, Angular, TypeScript, Neovim), soft skills, and an AI-Driven Development chapter.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not built, not run.** No binary was compiled, no `BOOK_PATH` cloned, no MCP query executed, so every claim below is from the repo, not from observed tool output. Examined: GitHub metadata for both the server and the book repos, the full README, the recursive file tree, commit/release/contributor counts, and the licensing of the underlying book repository.

```bash
gh api repos/Alan-TheGentleman/gentleman-book-mcp --jq '{stars,license,description,pushed_at,created_at,language,forks,open_issues}'
gh api repos/Alan-TheGentleman/gentleman-book-mcp/readme --jq '.content' | base64 -d
gh api "repos/Alan-TheGentleman/gentleman-book-mcp/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/Alan-TheGentleman/gentleman-book-mcp/commits --jq 'length'           # 3
gh api repos/Alan-TheGentleman/gentleman-book-mcp/contributors --jq '[.[].login]' # single author
gh api repos/Alan-TheGentleman/gentleman-book-mcp/releases --jq 'length'          # 0
# Underlying content licensing / provenance:
gh api repos/Alan-TheGentleman/gentleman-programming-book --jq '{stars,license,pushed_at}' # license: null
```

## What worked

- **Clear, well-documented three-tier design.** The README is unusually complete for a 3-commit project: explicit tool tables, env-var table, Claude Desktop config, troubleshooting, and an architecture diagram. The progressive structure (keyword tools → resources/prompts → optional semantic search) is a sensible MCP design.
- **Local-first, low-risk surface.** Levels 1–2 are read-only file parsing with no network and no system access — there is nothing it can break. Semantic search can run fully locally via Ollama, so even the embedding tier need not phone home or incur API cost.
- **Bilingual content** (English + Spanish indexes/resources) is a genuine differentiator for Spanish-speaking teams; the author has a large Spanish-language developer audience.
- **First-party authorship.** The MCP server and the book share one author (Gentleman Programming / Alan-TheGentleman), so the content-to-server mapping is authoritative — there is no third party scraping someone else's book.

## What didn't work or surprised us

- **Content licensing is the headline problem.** The server code is MIT, but the *book it serves* ([gentleman-programming-book](https://github.com/Alan-TheGentleman/gentleman-programming-book)) has **no LICENSE file** (GitHub license API returns 404; `license: null`). Under default copyright, "no license" means all rights reserved. Feeding that content into an agent's context for your own development is plausibly fine, but the provenance is informal and there is no explicit grant — a real consideration for any team with IP discipline.
- **Setup friction is high for what it delivers.** You must (1) install Go, (2) clone *this* repo and `go build`, (3) separately clone the *book* repo, (4) point `BOOK_PATH` at it, (5) optionally stand up Ollama or supply an OpenAI key, (6) wire it into the client. That is a lot of moving parts for static prose.
- **Documented for Claude Desktop, not Claude Code.** The README's only client config is `claude_desktop_config.json`. It is a standard stdio MCP server so it should work in Claude Code via `.mcp.json`/`claude mcp add`, but that path is undocumented and unverified.
- **Single-book knowledge has limited marginal value over training data.** Frontier models already know Hexagonal Architecture, Clean Architecture, TDD, React patterns, Big-O, and microservices from far broader, better-edited sources. The book's value-add is its *specific opinions and phrasing* ("according to the book"), which matters only if you specifically want to align an agent to this author's conventions.
- **Very low maturity.** 102 stars, single author, 3 commits, no releases, no tags, no tests visible in the tree, last touched 2025-12-29 (a ~5-day burst). It is a personal companion project, not a maintained tool.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral / slight + | Architecture concepts are mainstream and already in model training data; the book mostly restates them. Net correctness gain over base knowledge is marginal unless you want this author's specific conventions. |
| Speed | neutral / − | Heavy multi-step setup (build server + clone book + optional embeddings) for content the model can already produce; slows initial adoption more than it speeds design work. |
| Maintainability | neutral | Could nudge designs toward documented patterns, but the same patterns are available from broader sources; no clear maintainability lift beyond generic best-practice advice. |
| Safety | neutral, with a licensing caveat | Read-only local file parsing, no system/DB access, local-embedding option avoids data egress. Offsetting concern: the served book content has no license grant (all-rights-reserved by default). |
| Cost Efficiency | neutral | Local/Ollama path is free; OpenAI embeddings add minor cost. Adds context tokens for content the model largely already knows. |

## Verdict

**SKIP** (re-evaluate as CONDITIONAL only for the specific Gentleman-Programming-aligned audience)

gentleman-book-mcp is a tidy, well-documented, low-risk first-party retrieval layer over one author's book — but in this catalog's framework it does not move a quality signal enough to justify its setup cost. The architecture knowledge it serves (Hexagonal/Clean Architecture, TDD, microservices, React/TS patterns) is mainstream material that frontier models already hold from broader, better-curated sources, so the marginal Correctness/Maintainability gain is thin. Against that sits real friction (build the server, separately clone the book, optionally run embeddings) and a genuine provenance flag: the underlying book repo carries **no license**, so there is no explicit grant to redistribute or embed its text.

Compared to its catalog neighbors, the contrast is sharp. **pg-aiguide (CONDITIONAL)** earns its place because it targets a *specific, documented LLM failure mode* (non-idiomatic, version-blind Postgres) with vendor-credible, version-scoped depth — a single-vendor knowledge layer that closes a real gap. **karpathy-llm-wiki** and **book-to-skill** are *general* mechanisms (build a citable wiki / turn any book into a skill) rather than one fixed book, so they scale to whatever knowledge you actually lack. **agent-rules-books** distills 13 canonical engineering books into token-budgeted rule sets — broader coverage, lighter footprint, no separate server. gentleman-book-mcp is the narrowest of the set: one author's book, heavier setup, ambiguous content license. **Adopt only if you specifically want to align an agent to the Gentleman Programming conventions** (e.g. a team that already follows that curriculum, or Spanish-language teams valuing the bilingual content); otherwise prefer the general knowledge-layer tools or rely on the model's base knowledge. Not a full SKIP-and-forget — keep the catalog entry as a marked example of a single-book knowledge MCP — but not part of a recommended stack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gentleman-book-mcp](https://github.com/Alan-TheGentleman/gentleman-book-mcp) | MCP server | Go MCP server serving 18 chapters of the Gentleman Programming Book (architecture/frontend) to agents; local files + optional semantic search | Want an agent aligned to one author's specific architecture/frontend conventions and phrasing | book-to-skill, karpathy-llm-wiki, agent-rules-books (all more general); pg-aiguide (a more focused, higher-value single-domain knowledge layer) |
