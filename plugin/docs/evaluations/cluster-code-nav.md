# Evaluation: Code navigation / intelligence cluster — codegraph vs serena

**Cluster:** Code Understanding (structural/semantic code navigation for agents)
**Contenders:** [codegraph](https://github.com/colbymchenry/codegraph) (ADOPT, always-on default) vs [serena](https://github.com/oraios/serena) (ADOPT, conditional)
**Last verified:** 2026-06-22
**Dev loop stage:** Plan + Implement — both feed agents precise structural context; serena also *edits* at the symbol level
**Layer:** Tooling / Infrastructure (both run as MCP servers the client launches)

---

## What it does

Both tools attack the same weakness: without structural awareness, an agent navigates a codebase by grep-and-read — pulling whole files into context and guessing at relationships. Both expose a code-intelligence layer over MCP so the agent can query structure instead. They differ on *what* the layer does:

- **codegraph** — a pre-indexed code knowledge graph that runs as an MCP server and **auto-syncs on file changes**. Agents query function definitions, call graphs, and cross-module dependencies. 100% local, no API keys, no manual rebuild step, and it integrates invisibly (no prompt engineering). It is **read-only** structural navigation.
- **serena** — an IDE-grade semantic toolkit operating at the **symbol** level via language servers (LSP, 40+ languages claimed) or a paid JetBrains backend. Beyond retrieval, it performs atomic cross-file renames, reference lookups, and refactors — it both **reads and edits** at the symbol level. It also ships `execute_shell_command` (arbitrary host code execution) and per-project YAML config.

Choosing within this cluster decides what the STACK installs as its code-navigation default. STACK already splits them: **codegraph as the always-on default** (read-only navigation), **serena as conditional** for heavy refactoring.

## How we tested it

**Source-grounded comparison — not a fresh hands-on A/B.** We did not index the same repo with both tools, did not measure query latency, indexing time, token savings, or refactor correctness, and did not connect either MCP server to a client in this session. Both individual evals are themselves review-based (neither was run hands-on). This entry synthesizes those evals and the catalog verdicts along a shared dimension (read-only navigation vs. symbol-level editing, setup friction, and safety surface), then names the STACK pick per scenario.

**Evidence:** REVIEW

Sources read and cross-referenced:

```
evaluations/codegraph.md   # ADOPT (review-based) — auto-syncing knowledge-graph over MCP, read-only
evaluations/serena.md      # ADOPT (with safety scoping) — LSP symbol-level read + edit
CATALOG.md (Code Understanding rows)  # codegraph, serena overlap markers (graphify, Understand-Anything, etc.)
STACK.md (codegraph default row + serena conditional row)
```

## What worked

- **codegraph's auto-sync is the headline and the reason it's the default.** `codegraph.md`: "the graph is meant to stay current as you edit, with no manual rebuild step, and agents use it automatically over MCP (no prompt engineering)." It is 100% local with no keys, and the author's benchmark reports ~16% cost savings and ~58% fewer tool calls vs. sessions without it (vendor figures, not reproduced). Zero-setup, always-on, invisible.
- **serena operates on the right abstraction — symbols, not text.** `serena.md`: "Operating on symbols and references (via LSP) is categorically better than grep/line-number editing for large codebases: cross-file renames, reference lookups, and moves become single atomic calls instead of multi-step text surgery." It rides mature per-language LSPs (the same machinery IDEs use) rather than a homegrown index, and the eval calls it "the strongest semantic-code MCP in this catalog's Code Understanding cluster."
- **Both are mature and client-agnostic.** codegraph at 51K stars; serena at 25.5K stars, 13 tagged releases, CI, Docker, dogfooded `.serena/memories/`. Both work with Claude Code, Codex, Cursor, Gemini, and other MCP clients.

## What didn't work or surprised us

- **serena carries real setup friction and a security surface that codegraph doesn't.** `serena.md`: "40+ languages" is gated on installing/working language servers, the strongest capabilities are **paywalled** (JetBrains backend), and — critically — "`execute_shell_command` is arbitrary host code execution … the MCP server can execute anything the user can." The eval insists you "scope it per-project, keep `execute_shell_command` disabled where the harness already has shell, and don't aim it at untrusted repositories."
- **codegraph is read-only — it doesn't edit.** `codegraph.md`: "Graph queries return raw structural data — the agent still has to interpret relationships," and there's "no visualization output." It maps structure; it can't perform the atomic cross-file rename that serena can. `serena.md` makes the contrast explicit: "**codegraph** and **Understand-Anything** are read-only structural maps; Serena both reads *and* edits at the symbol level."
- **Both verdicts rest on design + vendor numbers, not independent runs.** codegraph's sub-500ms queries and ~2-min indexing are "the project's, not observed"; serena's "40+ languages / 8-12 steps collapse into one call" figures are README claims, and its headline endorsements are self-graded (agents prompted to rate Serena's own tools).

## Quality signals affected

| Signal | codegraph | serena | Comparison |
|--------|-----------|--------|------------|
| Correctness | + (structural awareness vs. grep-and-guess) | + (symbol/reference-aware atomic edits via LSP) | serena edits correctly across files; codegraph only navigates. |
| Speed | + (author-reported ~58% fewer tool calls) | + (one semantic call replaces multi-step read-edit loops) | Both cut tool calls; serena's win is on refactor-heavy work, codegraph's on everyday navigation. |
| Maintainability | neutral (helps understanding, doesn't change code) | + (refactors preserve references across files) | serena actively keeps the codebase coherent; codegraph is observe-only. |
| Safety | neutral (local-only, no security impact) | − (`execute_shell_command` = arbitrary host execution) | codegraph is the safer always-on default; serena needs per-project scoping. |
| Cost Efficiency | + (author-reported ~16% token savings) | + (symbol retrieval vs. bulk file reads; LSP backend free) | Both cut tokens; serena's JetBrains backend has a license cost the LSP path avoids. |

## Verdict

**Winner (always-on default): codegraph (ADOPT).** It is the STACK's default code-navigation layer because it is zero-setup, auto-syncing, 100% local, and invisible — agents query structure over MCP automatically with no manual rebuild, no API keys, and no security surface. `codegraph.md` rates it **ADOPT (review-based)**: "the always-on, auto-syncing knowledge-graph-over-MCP approach is a sound design for daily development." For everyday "where is this defined / what calls this" navigation, codegraph is the right thing to leave running everywhere.

**When the runner-up wins: serena (ADOPT, conditional) for heavy cross-file refactoring.** The moment the task is symbol-level *editing* — atomic cross-file renames, moves, and reference-preserving refactors — codegraph's read-only graph isn't enough and serena's LSP symbol edits win decisively. `serena.md` is explicit: "For semantic *editing*, adopt Serena; for a zero-setup read-only structural index, the graph tools remain lighter." The trade-off is real and bounded: serena adds LSP setup friction, a paid tier for full coverage, and an arbitrary-shell-execution surface, so adopt it **with safety scoping** — per-project, `execute_shell_command` off where the harness already has shell, and never pointed at untrusted repos. Run codegraph always; pull serena in for refactoring sprints.

## Catalog entry

n/a — this compares existing catalog entries (codegraph, serena) rather than introducing a new row.
