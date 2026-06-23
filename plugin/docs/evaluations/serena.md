# Evaluation: serena

**Repo:** [oraios/serena](https://github.com/oraios/serena)
**Stars:** 25,657 | **Last updated:** 2026-06-19 (pushed; created 2025-03-23) | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Implement and Plan — symbol-level semantic retrieval feeds the agent precise context (Plan/understand) and lets it do atomic, IDE-grade edits and refactors (Implement). Also touches Verify via its `execute_shell_command` tool (run builds/tests/linters).
**Layer:** Tooling/Infrastructure — a standalone MCP server (Python, uv-installed) backed by language servers (LSP) or a paid JetBrains plugin; it runs as a process your client launches, not a process step or persona.

---

## What it does

Serena is an MCP toolkit that gives a coding agent **IDE-grade semantic understanding** of a codebase, operating at the *symbol* level rather than on line numbers or raw text. Tagline: "The IDE for Your Coding Agent." Instead of the agent reading whole files and doing fragile text surgery, Serena exposes tools that find symbols, list references, navigate the relational structure, and perform atomic cross-file renames/moves/refactors. It connects to any MCP client (Claude Code, Codex, OpenCode, Gemini-CLI, Cursor, JetBrains, Claude Desktop) via stdio or HTTP.

The semantic power comes from two interchangeable backends: (1) **language servers (LSP)** — the default, free/open-source path, with claimed support for **40+ languages** (Python, TS/JS, Go, Rust, Java, C#, C/C++, Ruby, Swift, Kotlin, Scala, Solidity, and many more); or (2) a **paid JetBrains plugin** that borrows the IDE's analysis (and, exclusively, a breakpoint/REPL debugging tool). The tool surface (in `src/serena/tools/`) splits into `symbol_tools.py` (the semantic core: find/reference/replace symbols), `file_tools.py`, `query_project_tools.py`, `memory_tools.py` (a cross-session memory system), `workflow_tools.py`, `cmd_tools.py` (`execute_shell_command`), `config_tools.py`, and `jetbrains_tools.py`. A layered YAML config system (global / CLI / per-project / context / composable "modes") controls which tools are active.

## How we tested it

**Evidence:** MEASURED

**Ran hands-on** on 2026-06-22 (macOS arm64, macOS 26.3, Python via `uvx`). Installed Serena from source via `uvx --from git+https://github.com/oraios/serena` (**Serena 1.5.4.dev0**, commit `dd7eb6d`), enumerated its live tool surface, **indexed a real third-party Python codebase** ([`psf/requests`](https://github.com/psf/requests), 37 `.py` files), confirmed its **pyright LSP backend** actually starts and negotiates capabilities, then **drove three symbol-level tools end-to-end through Serena's own Python tool API** (`GetSymbolsOverviewTool`, `FindSymbolTool`, `FindReferencingSymbolsTool`) — **verifying every symbol location and reference against `grep` ground truth in the source.** No API key, no network egress for the LSP path; the symbol index is a local pickle cache under `.serena/cache/`.

```bash
# Install + run (uvx builds serena-agent from source)
uvx --from git+https://github.com/oraios/serena serena --version   # → Serena 1.5.4.dev0
uvx --from git+https://github.com/oraios/serena serena tools list   # 28 default-active tools
git clone --depth 1 https://github.com/psf/requests /tmp/serena-target
cd /tmp/serena-target
uvx --from git+https://github.com/oraios/serena serena project index . --language python
uvx --from git+https://github.com/oraios/serena serena project health-check .
```

**Install (measured).** `uvx` resolved and built `serena-agent` from the git HEAD, **installing 77 packages**; first cold run (build + install) was **~6.2 s wall**, subsequent invocations reuse the uv cache. `serena --help` exposes a real CLI: `config`, `context`, `init`, `memories`, `mode`, `project`, `prompts`, `setup`, `start-mcp-server`, `start-project-server`, `tools`.

**Tool surface (measured, live — not README-paraphrased).** `serena tools list` printed **28 default-active tools**, including the semantic core: `find_symbol`, `find_referencing_symbols`, `find_implementations`, `find_declaration`, `get_symbols_overview`, `rename_symbol`, `replace_symbol_body`, `insert_after_symbol`/`insert_before_symbol`, `safe_delete_symbol`, plus `execute_shell_command`, the `*_memory` cross-session tools, and `search_for_pattern`. `rename_symbol`'s description confirms it "Renames a symbol throughout the codebase using language server refactoring capabilities."

**Indexing (measured).** `serena project index` auto-created `.serena/project.yml`, then indexed **37 Python files in ~2.8 s wall** (`Indexed files per language: python=37`), peaking at ~58 files/s. It wrote a **1.8 MB local LSP cache** (`document_symbols.pkl` 1.47 MB + `raw_document_symbols.pkl` 0.45 MB) under `.serena/cache/python/`.

**LSP backend actually starts (measured).** `serena project health-check` spun up the real backend: it launched **pyright-langserver 1.1.403** over stdio, completed `initialize` and printed the negotiated capabilities (`referencesProvider`, `renameProvider` with `prepareProvider`, `documentSymbolProvider`, `callHierarchyProvider`, …), scanned the workspace, and reported **"Language server startup (language=python) completed in 0.300 seconds."** (The health-check itself then reported "No symbols found" — but only because it auto-picked `setup.py` as its first analyzable file, which in modern `requests` is essentially empty; this is a health-check file-selection quirk, not an LSP failure, as the symbol queries below prove.)

**Symbol queries driven end-to-end (verified against grep).** Using the same `agent.get_tool(...).apply(...)` API the health-check uses, I ran three tools against `src/requests/models.py`:

```
get_symbols_overview models.py →
  {"Constant": ["REDIRECT_STATI","DEFAULT_REDIRECT_LIMIT","CONTENT_CHUNK_SIZE","ITER_CHUNK_SIZE"],
   "Class": ["RequestEncodingMixin","RequestHooksMixin","Request","PreparedRequest","Response"]}

find_symbol "Response/json" (include_body) →
  {"name_path":"Response/json","kind":"Method","relative_path":"src/requests/models.py",
   "body_location":{"start_line":1090,"end_line":1123}, "body":"def json(self, **kwargs: Any) -> Any: ..."}
```

Ground truth: `grep -n "def json" src/requests/models.py` → line **1091** (Serena's `body_location` 1090–1123 is the exact symbol body including its leading line — a correct LSP symbol range, not a text grep). The overview's class list (`Request`/`PreparedRequest`/`Response`) matches `grep -n "^class"` exactly.

**Reference-finding (verified, the differentiating capability).** `find_referencing_symbols "PreparedRequest"` returned **cross-file** references with line context — in `src/requests/__init__.py` (the `from .models import PreparedRequest` re-export and `__all__` entry) and `src/requests/_types.py` (the `is_prepared(request: PreparedRequest)` function, the `class _ValidatedRequest(PreparedRequest)` subclass, and the `AuthType` type alias). All match `grep -rn "PreparedRequest"` ground truth across those files. A control query — `find_referencing_symbols "Response/json"` — correctly returned `{}` (the `.json()` method has **no in-project caller**; it's invoked externally), confirming the tool resolves real LSP references rather than naïvely text-matching the name.

## What worked

- **Installs and runs headless on macOS arm64 via uvx** — `uvx --from git+...serena` built and ran in **~6.2 s**, no Homebrew formula or manual LSP install needed; pyright is auto-fetched (`uvx ... pyright==1.1.403 ...`) by Serena itself on first index.
- **Symbol-level, not text-level — and it's real.** Verified `get_symbols_overview`, `find_symbol`, and `find_referencing_symbols` against grep ground truth: symbol ranges, the class/constant inventory, and cross-file references all matched. `find_symbol` returned the exact method body with its on-disk line range; references resolved across files with surrounding context.
- **Real LSP backend, observed.** Indexing started **pyright-langserver 1.1.403** over stdio in **0.300 s** with full capabilities (references, rename-with-prepare, call hierarchy). The 40+-language breadth rides on this LSP machinery — for Python it demonstrably works out of the box.
- **Fast local indexing, small footprint.** 37 files indexed in **~2.8 s** into a **1.8 MB** local pickle cache; no network for the symbol path.
- **28-tool surface confirmed live**, including `rename_symbol`/`replace_symbol_body`/`safe_delete_symbol` (LSP-backed editing, not just retrieval) and the cross-session `*_memory` tools — these were enumerated from the running CLI, not the README.
- **Mature, disciplined repo.** 25.6K stars, MIT, versioned releases, CI (pytest/CodeQL), Docker + devcontainer, dogfooded `.serena/memories/` in-repo.

## What didn't work or surprised us

- **The editing/refactor path (`rename_symbol`, `replace_symbol_body`) was not exercised end-to-end.** I verified the *read* and *reference* tools with real output and the *editing* tools' presence/descriptions, but did not run a live rename-and-check-the-diff. Those mutate source and are intended to be driven by an agent over MCP; the retrieval and reference accuracy that the renames build on are what I measured directly.
- **`project health-check` is misleading on minimal first files.** It auto-selected `setup.py` (near-empty in modern `requests`) and printed "❌ Health check failed: No symbols found" even though the LSP was fully up and every real symbol query against `models.py` succeeded. The check's file-picking heuristic, not the language server, is the weak link — don't read its red ❌ as "Serena is broken."
- **`execute_shell_command` is arbitrary host code execution.** Serena ships a tool that runs shell commands on the host. It is disabled-by-default inside Claude Code/Codex (the harness supplies shell), but in clients without their own shell it is live. Treat Serena as a trusted, code-and-command-executing process, scope it per-project, and don't point it at untrusted repos.
- **LSP backend = per-language dependencies.** Python worked instantly (pyright auto-fetched), but "40+ languages" is gated on each language server installing/working; the breadth number is a ceiling, not a guarantee.
- **The strongest capabilities are paywalled.** Full no-LSP-fuss coverage and the breakpoint/REPL debugging tool require the **paid JetBrains plugin**; the free path is LSP-only.
- **Loud "do NOT install via marketplace" warning** in the README — install fragility; pin the right `uvx --from git+...` command (which is what worked here).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Verified hands-on: `get_symbols_overview`/`find_symbol`/`find_referencing_symbols` against `psf/requests` matched grep ground truth — exact symbol ranges, the full class inventory, and accurate cross-file references (and a correct empty result for an externally-called method). Symbol/reference-aware edits via LSP make cross-file renames atomic, vs. error-prone text surgery. |
| Speed | + | Measured: 37-file Python repo indexed in **~2.8 s**, pyright LSP up in **0.300 s**, one semantic call replaces multi-step read-and-edit loops. (Token/tool-call savings vs a grep agent not A/B'd here.) |
| Maintainability | + | Refactors that preserve references across files keep the codebase coherent; cross-session `*_memory` tools (confirmed present) carry project knowledge forward. |
| Safety | − | `execute_shell_command` is arbitrary host code execution; the MCP process has full file + shell reach. Disabled-by-default in some harnesses, but a real attack surface on untrusted code. |
| Cost Efficiency | + | Symbol-level retrieval (a single `find_symbol` returns the exact body + range) instead of bulk file reads cuts tokens on large codebases; free LSP backend has no license cost (JetBrains backend does). |

## Verdict

**ADOPT (with safety scoping) — the strongest semantic-code MCP in this catalog's Code Understanding cluster.** Confirmed hands-on: Serena installs and runs headless via `uvx`, indexes a real Python repo in seconds, starts a genuine pyright LSP backend, and answers symbol-overview / find-symbol / cross-file-reference queries whose results **matched grep ground truth exactly** — including a correct empty result for an externally-called method, proving real reference resolution rather than text matching. It does the thing the whole cluster reaches for, but on the *right* abstraction (LSP symbols/references) and ships as a mature, versioned, client-agnostic product. For agents working in large codebases — especially refactors, cross-file renames, and reference lookups — it is a clear quality and token win. Two caveats are real: (1) `execute_shell_command` can run arbitrary shell on the host, so scope it per-project, keep it disabled where the harness already has shell, and don't aim it at untrusted repos; (2) the live rename/edit path is agent-driven over MCP and was not exercised end-to-end here — but the retrieval and reference accuracy those edits depend on were directly measured.

Compared to neighbors: **code-context-engine**, **gortex**, **codebase-memory-mcp**, and **SocratiCode** mostly build *their own* index/knowledge-graph and sell token-reduction percentages; Serena instead rides real language servers (verified: pyright 1.1.403), giving it true rename/reference *editing* (not just retrieval) — a capability those tools don't claim. **codegraph** and **Understand-Anything** are read-only structural maps; Serena both reads *and* edits at the symbol level. The trade-off is Serena's per-language LSP dependency and shell-execution surface, which the pure-index tools avoid. For semantic *editing*, adopt Serena; for a zero-setup read-only structural index, the graph tools remain lighter.

## Catalog entry

Target category: **Code Understanding**

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [serena](https://github.com/oraios/serena) | MCP server | IDE-grade semantic code retrieval and editing over MCP — symbol-level find/reference/rename/refactor via LSP (40+ languages) or a JetBrains backend | Agents do fragile line/text edits and read whole files; need symbol-aware navigation and atomic cross-file refactors | code-context-engine, gortex, codegraph, codebase-memory-mcp, SocratiCode, Understand-Anything |
