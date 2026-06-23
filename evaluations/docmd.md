# Evaluation: docmd

**Repo:** [docmd-io/docmd](https://github.com/docmd-io/docmd)
**Stars:** 2,061 | **Last updated:** 2026-06-19 (latest release 0.8.6, 2026-06-05) | **License:** MIT
**Dev loop stage:** Ship (publishing docs) — touches Reflect (docs an agent can query later)
**Layer:** Tooling (a docs-site generator + an MCP server over your local docs)

---

## What it does

Markdown-to-docs-site generator with an MCP server and `llms.txt` output for AI-native documentation. The core (`@docmd/core`) is a zero-config Node.js static-site generator in the Docusaurus/VitePress/MkDocs lineage: point it at a folder of `.md` files, run `docmd dev`/`docmd build`, and it produces a small (~18kb initial payload) static HTML site with auto-generated navigation, offline search, SEO/sitemap, i18n, versioning, and PWA support. It also ships migration (`docmd migrate` from Docusaurus/VitePress/MkDocs) and deploy-config generation (`docmd deploy` → Docker/nginx/caddy).

The "AI-native" angle has three distinct mechanisms, and they differ a lot in depth:

1. **`llms` plugin (built-in, runs at build time).** A `post-build` hook (`packages/plugins/llms/src/index.ts`) writes two files into the output dir: `llms.txt` (a titled, sorted index of every non-`noindex` page as `- [title](url)` plus descriptions) and `llms-full.txt` (the entire raw markdown of every page concatenated with `---` separators). These are static artifacts an LLM or RAG pipeline can fetch — the same `llms.txt` convention the broader ecosystem has standardized on. This part is solid and genuinely useful.

2. **`docmd mcp` — a native MCP server (`packages/core/src/commands/mcp.ts`).** A hand-rolled stdio JSON-RPC 2.0 server (no `@modelcontextprotocol/sdk` — it parses lines off stdin itself) that exposes four tools and two resources over your *local* docs folder:
   - `search_docs(query)` — **case-insensitive substring line scan** across all `.md` files; returns matching `File / Line N: text`. Not semantic, not indexed, not ranked — `String.includes()` per line.
   - `read_doc(route)` — returns raw markdown of one file.
   - `validate_docs()` — lints local relative markdown links and reports broken paths (a real, useful linter).
   - `get_llms_context()` — returns the generated `llms-full.txt`.
   - Resources: `docmd://context/llms.txt` (the full context) and `docmd://context/skill` (a project `SKILL.md`, with a built-in fallback pointing at the `docmd-skills` repo).

3. **Agent Skills** (separate repo [docmd-io/docmd-skills](https://github.com/docmd-io/docmd-skills), 2 stars) — instruction modules teaching an agent docmd's own config/syntax/plugins so it can *author* docmd projects. This is meta: skills for working on docmd docs, not domain knowledge for your project.

The key clarification for this catalog: **the MCP server lets an agent query *the docs you wrote with docmd*, on your local filesystem.** It is not a context7-style index of third-party library docs, and its "search" is a literal substring grep — far below the semantic/hybrid retrieval the catalog's doc-search entries (context7, code-context-engine) provide.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** Examined repo metadata, the full README, the recursive file tree, release history (0.5.2 → 0.8.6, ~30 releases Mar–Jun 2026), and read the actual source: the entire MCP command (`packages/core/src/commands/mcp.ts` — tool list, `search_docs` handler, resources), the `llms` plugin (`packages/plugins/llms/src/index.ts`), and the `docmd-skills` repo metadata. No site was generated, no `docmd mcp` server was started, and no MCP queries were issued, so no performance/output metrics are claimed below — the search-quality finding is read from the source, not benchmarked.

```bash
gh api repos/docmd-io/docmd --jq '{stars,license,description,pushed_at,created_at,open_issues}'
gh api repos/docmd-io/docmd/readme --jq '.content' | base64 -d
gh api "repos/docmd-io/docmd/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/docmd-io/docmd/contents/packages/core/src/commands/mcp.ts --jq '.content' | base64 -d
gh api repos/docmd-io/docmd/contents/packages/plugins/llms/src/index.ts --jq '.content' | base64 -d
gh api repos/docmd-io/docmd/releases --jq '.[] | {tag:.tag_name, published:.published_at}'
gh api repos/docmd-io/docmd-skills --jq '{stars:.stargazers_count, desc:.description}'
```

## What worked

- **The `llms.txt` / `llms-full.txt` generation is clean and zero-config.** It's a build-time post-hook that respects `noindex` / `llms: false` frontmatter, sorts deterministically, and concatenates raw (not rendered) markdown — exactly what you want to feed a model. Output is a static artifact, so it works with any consumer (RAG, a `WebFetch`, another agent) regardless of MCP support.
- **As a plain docs-site generator it is legitimately strong.** Zero config, tiny payload (~18kb vs ~250kb Docusaurus), native multi-project/versioning/i18n, built-in offline search, OpenAPI rendering, Mermaid, and a `migrate` path off the major competitors. Active maintenance: ~30 tagged releases in four months, MIT, official Docker image.
- **`validate_docs` is a genuinely useful agent tool.** Broken-internal-link detection exposed over MCP means an agent shipping docs can self-check link integrity before publishing — a real Ship-stage quality gate.
- **MCP/skills/llms.txt all built in** where competitors require plugins or a SaaS (per the README's own comparison table) — AI-native is a first-class design goal, not bolted on.

## What didn't work or surprised us

- **`search_docs` is a substring line grep, not search.** It lowercases the query and does `line.toLowerCase().includes(query)` across every markdown file — no tokenization, no ranking, no semantic match, no fuzzy match (note: the *browser* offline search plugin does have fuzzy matching; the *MCP* tool does not). For a small docs set an agent could just as well `Grep`/`Read` the files directly, which Claude Code already does natively. The MCP server's marginal value over built-in filesystem tools is thin.
- **The MCP server is hand-rolled JSON-RPC over stdin, not the official SDK.** It manually parses lines and constructs responses. It works, but it's a bespoke implementation to trust and maintain versus `@modelcontextprotocol/sdk`.
- **The agent value mostly accrues to *consumers* of your published site, not to your dev loop.** The headline win — "agents can query your docs" — primarily benefits *other people's* agents hitting your published `llms.txt`/site. Inside your own repo, your agent already has the source markdown.
- **Two of the three "AI" pillars are weak in isolation.** `docmd-skills` (2 stars) teaches agents to author docmd itself — niche. The MCP `search_docs` is a grep. The one strong, durable pillar is the static `llms.txt` output.
- **`docmd mcp` only adds value once you've already adopted docmd as your docs toolchain.** It is not a standalone agent capability you'd add to an arbitrary project.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral / + | `validate_docs` catches broken internal links before publishing; `llms-full.txt` gives consumers grounded context. Doesn't affect application code correctness. |
| Speed | + | Zero-config generator is fast to stand up; tiny static payload loads fast. Build-time `llms.txt` is automatic. |
| Maintainability | + | One Markdown-in tool with migration off competitors, versioning, and i18n built in; docs stay in-repo as `.md`. |
| Safety | neutral | MCP server reads local `.md` over stdio — no write/exec, no network in the local tools. Hand-rolled JSON-RPC is a minor trust surface. |
| Cost Efficiency | neutral / + | OSS/MIT, self-hosted, no SaaS fees vs Mintlify. MCP `search_docs` could waste tokens vs native Grep, but it's optional. |

## Verdict

**CONDITIONAL**

docmd is a credible, actively maintained, zero-config docs-site generator whose AI story is real but uneven: the `llms.txt`/`llms-full.txt` build-time output is the durable win (a clean, standard artifact agents and RAG pipelines can consume), while the MCP server's `search_docs` is a literal substring grep that adds little over Claude Code's native filesystem tools, and the `docmd-skills` add-on is niche. The "agents can query your docs" angle is mostly a benefit to *downstream consumers of your published site*, not a meaningful inner-loop win for the team writing the docs. **Adopt it when you actually need to publish a documentation site and want first-class `llms.txt`/AI-native output for free** — there it's a strong, lightweight choice versus Docusaurus/Mintlify. It is **not** an agent-capability tool to add to an arbitrary project, and its MCP search should not be mistaken for context7-style semantic doc retrieval. Not ADOPT-everywhere (most projects don't run a docs site, and the agent-query value is thin in-repo); not SKIP (as a docs generator with genuine `llms.txt` support it earns its catalog slot). The existing "unique: AI-native docs site" overlap marker holds — it's a publishing tool, distinct from the doc-*search* MCP servers (context7, mdn/mcp, git-mcp) and doc-*writing* skills already cataloged.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [docmd](https://github.com/docmd-io/docmd) | tool | Zero-config Markdown-to-docs-site generator with built-in `llms.txt`/`llms-full.txt` output and a local-docs MCP server (read/search/validate) | Need to publish a docs site whose content agents and RAG pipelines can also consume programmatically | — (unique: AI-native docs-site *generator*; distinct from doc-search MCP servers like context7/mdn-mcp and doc-writing skills) |
