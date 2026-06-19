# Evaluation: Repomix

**Repo:** [yamadashy/repomix](https://github.com/yamadashy/repomix)
**Stars:** 26,394 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Packs an entire repository (or selected directories/files) into a single XML, Markdown, or plain-text file optimized for LLM consumption. The output includes a file tree, token counts per file, and concatenated file contents with clear boundaries. A `--compress` mode uses Tree-sitter to extract function/class signatures while stripping implementations, reducing tokens ~70%. Also ships as an MCP server (`repomix --mcp`) with 5 tools: `pack_codebase`, `pack_remote_repository`, `attach_packed_output`, `read_repomix_output`, and `grep_repomix_output`.

## How we tested it

Architecture and README review of v26.4K-star repository. Assessed CLI features, MCP server integration, output formats, compression mechanism, and compared with other code understanding tools in the catalog.

```bash
gh api repos/yamadashy/repomix --jq '.description, .stargazers_count, .updated_at'
# README analysis covering: features, MCP server, output formats, compression, security
```

## What worked

- **MCP server mode is the killer feature for Claude Code users**: `repomix --mcp` provides 5 well-designed tools that let the agent pack local or remote repos without manual file preparation — this makes repomix useful even when the agent already has file access
- **Tree-sitter compression** (`--compress`) is genuinely useful for large repos: extracts function signatures and class structures while dropping implementations, ~70% token reduction with semantic preservation
- **Remote packing** (`--remote yamadashy/repomix`) lets agents analyze external repos without cloning — useful for Plan stage when evaluating dependencies or comparing approaches
- **Security scanning** via Secretlint catches secrets before they enter LLM context — unique safety feature not in codegraph or code-context-engine
- **Ecosystem breadth**: CLI, website (repomix.com), Chrome/Firefox extension, VSCode extension, MCP server — every surface is covered
- **Token counting** per file helps agents estimate context usage before committing to a full read

## What didn't work or surprised us

- **Redundant for Claude Code's core use case**: agents can already Read files directly — packing into a single file is solving a problem Claude Code doesn't have. The MCP server partially addresses this by adding grep and remote capabilities, but for local work, direct file access is faster
- **Context explosion risk**: packing a full repo into one file can easily blow the context window. The `--compress` flag mitigates this but adds a Tree-sitter dependency and processing time
- **XML output format** is the default — XML adds significant token overhead vs plain concatenation. Markdown mode is better for LLM consumption but not the default
- **No incremental updates**: every pack is a full re-scan. For large repos being worked on iteratively, this wastes time compared to graph-based tools that maintain an index

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Packing doesn't change code quality; security scanning is a small safety net |
| Speed | + | Remote packing and compression speed up external repo analysis during planning |
| Maintainability | neutral | No direct impact on code structure |
| Safety | + | Secretlint integration prevents accidental secret exposure to LLMs |
| Cost Efficiency | +/- | Compression saves tokens, but full-repo packing without compression wastes them |

## Verdict

**CONDITIONAL**

Use repomix when feeding code to non-agent LLMs (ChatGPT, Claude web, Gemini) that lack file access, when analyzing remote repositories during planning, or when you need the MCP server's `pack_remote_repository` for cross-repo comparison. For day-to-day Claude Code work where the agent has direct file access, codegraph (ADOPT) and context7 (KEEP) provide more targeted context without the context-explosion risk. The MCP server mode makes repomix more relevant to agent workflows than its CLI-only days, but it's still a serialization tool in a world where agents can read files natively.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [repomix](https://github.com/yamadashy/repomix) | tool | Packs entire repo into a single AI-friendly file with Tree-sitter compression and MCP server | Need to feed a full codebase to an LLM that doesn't have file access | codegraph (different approach: serialization vs. graph), code-context-engine |
