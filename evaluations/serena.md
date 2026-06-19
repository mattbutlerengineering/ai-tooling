# Evaluation: serena

**Repo:** [oraios/serena](https://github.com/oraios/serena)
**Stars:** 25,553 | **Last updated:** 2026-06-19 (pushed; created 2025-03-23) | **License:** MIT
**Dev loop stage:** Implement and Plan — symbol-level semantic retrieval feeds the agent precise context (Plan/understand) and lets it do atomic, IDE-grade edits and refactors (Implement). Also touches Verify via its `execute_shell_command` tool (run builds/tests/linters).
**Layer:** Tooling/Infrastructure — a standalone MCP server (Python, uv-installed) backed by language servers (LSP) or a paid JetBrains plugin; it runs as a process your client launches, not a process step or persona.

---

## What it does

Serena is an MCP toolkit that gives a coding agent **IDE-grade semantic understanding** of a codebase, operating at the *symbol* level rather than on line numbers or raw text. Tagline: "The IDE for Your Coding Agent." Instead of the agent reading whole files and doing fragile text surgery, Serena exposes tools that find symbols, list references, navigate the relational structure, and perform atomic cross-file renames/moves/refactors. It connects to any MCP client (Claude Code, Codex, OpenCode, Gemini-CLI, Cursor, JetBrains, Claude Desktop) via stdio or HTTP.

The semantic power comes from two interchangeable backends: (1) **language servers (LSP)** — the default, free/open-source path, with claimed support for **40+ languages** (Python, TS/JS, Go, Rust, Java, C#, C/C++, Ruby, Swift, Kotlin, Scala, Solidity, and many more); or (2) a **paid JetBrains plugin** that borrows the IDE's analysis (and, exclusively, a breakpoint/REPL debugging tool). The tool surface (in `src/serena/tools/`) splits into `symbol_tools.py` (the semantic core: find/reference/replace symbols), `file_tools.py`, `query_project_tools.py`, `memory_tools.py` (a cross-session memory system), `workflow_tools.py`, `cmd_tools.py` (`execute_shell_command`), `config_tools.py`, and `jetbrains_tools.py`. A layered YAML config system (global / CLI / per-project / context / composable "modes") controls which tools are active.

## How we tested it

**Source-grounded inspection — not installed, not run.** No `uv tool install serena-agent`, no `serena init`, no MCP connection to a client, no symbol query or refactor executed. Every claim is from the repository (GitHub metadata, README, recursive file tree, `src/serena/tools/` listing), not from observed behavior. The "single most impactful addition to my toolkit" quotes are the authors' own evaluation framing (agents prompted to rate Serena), not anything I measured. The "40+ languages / 8-12 steps collapse into one call / faster-more-reliable" figures are README claims, unverified here.

```bash
gh api repos/oraios/serena --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/oraios/serena/readme --jq '.content' | base64 -d           # README
gh api "repos/oraios/serena/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/oraios/serena/releases --jq 'length'   # 13 tagged releases
gh api repos/oraios/serena/commits  --jq 'length'   # 30 (page-1 cap; active)
```

## What worked

- **Symbol-level, not text-level — the right abstraction.** Operating on symbols and references (via LSP) is categorically better than grep/line-number editing for large codebases: cross-file renames, reference lookups, and moves become single atomic calls instead of multi-step text surgery. This is the differentiator over grep-and-read agents.
- **Real semantic backend, not a homegrown parser.** It leans on the language-server protocol — the same machinery IDEs use — so correctness of "find references / rename symbol" rides on mature, per-language LSPs rather than a bespoke index. 40+ languages claimed via that path.
- **Genuinely client-agnostic.** Pure MCP, stdio or HTTP, documented for Claude Code, Codex, JetBrains, Cursor, Gemini-CLI, Claude Desktop and more. Not locked to one harness.
- **Mature, disciplined repo.** 25.5K stars, 1.7K forks, 13 tagged releases (versioned, pinnable), CI (pytest, parallel tests, CodeQL, codespell, Docker images), Dockerfile + compose, devcontainer, dogfooded `.serena/memories/` in-repo. This is a maintained product, not a weekend script.
- **Thoughtful tool gating.** README explicitly says basic file/search/shell tools are *disabled by default* inside agentic harnesses (Claude Code/Codex) to avoid duplicating the host's built-ins — exposing only the semantic tools that add value. Reduces redundant tool-choice surface.

## What didn't work or surprised us

- **`execute_shell_command` is arbitrary host code execution.** Serena ships a tool that runs shell commands on the host (builds/tests/linters). Useful, but it is full host reach — the MCP server can execute anything the user can. It is disabled-by-default inside Claude Code/Codex (the harness supplies shell), but in clients without their own shell it is live. Treat Serena as a trusted, code-and-command-executing process, scope it per-project, and don't point it at untrusted repos.
- **LSP backend = setup friction and per-language dependencies.** "40+ languages" is gated on installing/working language servers; the README warns extra deps may be needed per language. Real-world reliability varies by how mature each LSP is — the breadth number is a ceiling, not a guarantee.
- **The strongest capabilities are paywalled.** Full-language coverage with no LSP fuss, and the breakpoint/REPL debugging tool, require the **paid JetBrains plugin**. The free path is LSP-only and carries the setup burden.
- **Loud "do NOT install via marketplace" warning.** The README insists you must use its Quick Start, not any MCP/plugin marketplace (which carry "outdated/suboptimal" commands). Signals install fragility and that pinning the right version/command matters.
- **Self-graded evaluation.** The headline endorsements are agents prompted to rate Serena's own tools — interesting signal, but it is the vendor's methodology, not independent benchmarking.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Symbol/reference-aware edits via LSP make cross-file renames and refactors atomic and semantically correct, vs. error-prone text surgery — the core value claim. |
| Speed | + | One semantic call replaces multi-step read-and-edit loops; targeted symbol retrieval avoids reading whole files. (Magnitude unverified here.) |
| Maintainability | + | Refactors that preserve references across files keep the codebase coherent; cross-session memory carries project knowledge forward. |
| Safety | − | `execute_shell_command` is arbitrary host code execution; the MCP process has full file + shell reach. Disabled-by-default in some harnesses, but a real attack surface on untrusted code. |
| Cost Efficiency | + | Symbol-level retrieval instead of bulk file reads cuts tokens on large codebases; free LSP backend has no license cost (JetBrains backend does). |

## Verdict

**ADOPT (with safety scoping) — the strongest semantic-code MCP in this catalog's Code Understanding cluster.** Serena does the thing the whole cluster is reaching for, but it does it on the *right* abstraction (LSP symbols/references) and ships as a mature, versioned, client-agnostic product rather than a prototype. For agents working in large codebases — especially refactors, cross-file renames, and reference lookups — it is a clear quality and token win. The one caveat is real: it can execute arbitrary shell commands on the host, so scope it per-project, keep `execute_shell_command` disabled where the harness already has shell, and don't aim it at untrusted repositories.

Compared to neighbors: **code-context-engine**, **gortex**, **codebase-memory-mcp**, and **SocratiCode** mostly build *their own* index/knowledge-graph and sell token-reduction percentages; Serena instead rides real language servers, giving it true rename/reference *editing* (not just retrieval) — a capability those tools don't claim. **codegraph** and **Understand-Anything** are read-only structural maps; Serena both reads *and* edits at the symbol level. The trade-off is Serena's LSP setup friction and shell-execution surface, which the pure-index tools avoid. For semantic *editing*, adopt Serena; for a zero-setup read-only structural index, the graph tools remain lighter.

## Catalog entry

Target category: **Code Understanding**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [serena](https://github.com/oraios/serena) | MCP server | IDE-grade semantic code retrieval and editing over MCP — symbol-level find/reference/rename/refactor via LSP (40+ languages) or a JetBrains backend | Agents do fragile line/text edits and read whole files; need symbol-aware navigation and atomic cross-file refactors | code-context-engine, gortex, codegraph, codebase-memory-mcp, SocratiCode, Understand-Anything |
