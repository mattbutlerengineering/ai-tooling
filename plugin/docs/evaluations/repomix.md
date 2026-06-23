# Evaluation: Repomix

**Repo:** [yamadashy/repomix](https://github.com/yamadashy/repomix)
**Stars:** 26,394 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Packs an entire repository (or selected directories/files) into a single XML, Markdown, or plain-text file optimized for LLM consumption. The output includes a file tree, token counts per file, and concatenated file contents with clear boundaries. A `--compress` mode uses Tree-sitter to extract function/class signatures while stripping implementations, reducing tokens ~70%. Also ships as an MCP server (`repomix --mcp`) with 5 tools: `pack_codebase`, `pack_remote_repository`, `attach_packed_output`, `read_repomix_output`, and `grep_repomix_output`.

## How we tested it

**Evidence:** RUN

**Hands-on**, repomix v1.15.0 installed and run against this very repository (the ai-tooling catalog itself — ~1,000 files of mostly Markdown plus a JS presentation dir) on 2026-06-20. Measured full-pack token counts, the `--compress` reduction on both prose and code, the Secretlint security scan, and remote packing.

```bash
npm install repomix@latest            # v1.15.0 (npx cache was corrupt; clean install worked)
# Full pack of this repo (Markdown style):
node node_modules/repomix/bin/repomix.cjs /Users/mbutler/github/ai-tooling --style markdown
#   → Total Files: 1,011 | Total Tokens: 1,819,864 | Security: ✔ No suspicious files
# Compress the whole (prose-heavy) repo:
node .../repomix.cjs <repo> --compress        # 1,819,864 → 1,790,515 tokens  (only −1.6%)
# Compress a CODE directory (presentations/, real JS):
node .../repomix.cjs <repo>/presentations              # 44,325 tokens
node .../repomix.cjs <repo>/presentations --compress   # 17,488 tokens        (−61%)
# Remote pack with no local clone:
node .../repomix.cjs --remote octocat/Hello-World      # 1 file, 365 tokens, ✔ Done
```

**Measured results:** full pack = **1.82M tokens / 1,011 files** (far beyond any context window — context-explosion is real and concrete); Secretlint **ran and passed**; remote packing **worked without cloning**; and crucially, `--compress` cut **~61% on actual code** but **only ~1.6% on prose/Markdown** — the headline "~70%" reduction is a *code* number, not a docs number. Also observed: with no config, repomix packed **both `CATALOG.md` and the synced duplicate `plugin/docs/CATALOG.md`** (41.5K tokens each), so synced/vendored content double-counts unless excluded.

## What worked

- **Remote packing works as advertised** — `--remote octocat/Hello-World` packed an external repo with no manual clone (1 file, 365 tokens, ✔ Done). This is the genuinely useful agent feature: analyze a dependency or compare an approach without cloning.
- **Compression is real *on code*** — verified ~61% reduction on a real JS directory (44.3K → 17.5K tokens), close to the claimed ~70%, while preserving function/class structure.
- **Security scanning runs by default** — Secretlint executed on the full 1,011-file pack and reported "✔ No suspicious files detected"; a real safety net not in codegraph/code-context-engine.
- **Per-file token counts + top-N report** are genuinely useful — the pack summary's "Top 5 Files by Token Count" immediately surfaced that the catalog files dominate, helping budget context.
- **MCP server mode** (`repomix --mcp`, 5 tools incl. `pack_remote_repository`/`grep_repomix_output`) makes it usable from inside Claude Code without manual prep — the most relevant surface for agent workflows.

## What didn't work or surprised us

- **Context explosion is real, not theoretical** — a full pack of this modest repo was **1.82M tokens**, an order of magnitude past any context window. The full pack is unusable as-is; you *must* scope (`--include`) or compress.
- **`--compress` barely helps on prose** — only −1.6% on this Markdown-heavy repo (vs. −61% on code). Tree-sitter extracts code signatures; docs/config/prose get almost nothing. The "~70%" headline is a code-repo number and should not be expected on docs/RAG corpora.
- **Double-counts synced/vendored content by default** — it packed both `CATALOG.md` and the synced `plugin/docs/CATALOG.md` (41.5K tokens each). Without a `.repomixignore`/config you silently pay for duplicates.
- **Redundant for Claude Code's *local* core use case** — agents already Read files directly; serialization mainly earns its keep via the remote/grep MCP tools and for non-agent LLMs.
- **Packaging friction observed** — the `npx repomix` path failed with a corrupt dependency cache (`Cannot find module 'fill-range'`); a clean `npm install` was needed. Minor, environment-specific, but worth knowing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Packing doesn't change code quality; security scanning is a small safety net |
| Speed | + | Remote packing and compression speed up external repo analysis during planning |
| Maintainability | neutral | No direct impact on code structure |
| Safety | + | Secretlint integration prevents accidental secret exposure to LLMs |
| Cost Efficiency | +/- | Compression saves tokens, but full-repo packing without compression wastes them |

## Verdict

**CONDITIONAL** *(verdict confirmed by hands-on testing)*

Use repomix to feed code to **non-agent LLMs** (ChatGPT/Claude web/Gemini) that lack file access, or via its **`--remote` / MCP `pack_remote_repository`** to analyze an external repo without cloning — both verified working here. Two evidence-based cautions: (1) **never pack a full repo blind** — this one hit 1.82M tokens; always `--include` a scope or compress; (2) **`--compress` only pays off on code (~61%), not prose (~1.6%)** — don't expect token savings on docs/RAG corpora, and add a `.repomixignore` so synced/vendored copies aren't double-counted. For day-to-day Claude Code work where the agent reads files natively, codegraph (ADOPT) and context7 (KEEP) give more targeted context without the explosion risk. Net: a solid, well-built serialization tool whose real value for agents is the remote/MCP path, not local full-repo packing.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [repomix](https://github.com/yamadashy/repomix) | tool | Packs entire repo into a single AI-friendly file with Tree-sitter compression and MCP server | Need to feed a full codebase to an LLM that doesn't have file access | codegraph (different approach: serialization vs. graph), code-context-engine |
