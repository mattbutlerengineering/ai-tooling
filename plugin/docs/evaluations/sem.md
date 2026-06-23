# Evaluation: sem (semantic version control)

**Repo:** [Ataraxy-Labs/sem](https://github.com/Ataraxy-Labs/sem)
**Stars:** 2,948 | **Last updated:** 2026-06-17 (pushed) | **License:** MIT | **Language:** Rust
**Dev loop stage:** Code Understanding — Implement/Review
**Layer:** Tooling (CLI + MCP server for agents)

---

## What it does

sem is **semantic version control built on top of Git**: instead of lines changed, it tells you what *entities* changed — functions, methods, classes. It parses code with **tree-sitter (28+ languages)**, extracts every function/class/method as an entity, and **diffs at the entity level** ("function `blahh` was modified" instead of "lines x–y changed"), plus entity-level **blame** and **impact analysis**. It "works in any Git repo with no setup," ships as a single Rust binary (install script, Homebrew `sem-cli`, or npm wrapper `@ataraxy-labs/sem`), and exposes an **MCP server** so coding agents consume semantic diffs directly. Part of the Ataraxy Labs stack (siblings: `weave` entity-level merge driver, `inspect` semantic code review, `opensessions` tmux sidebar).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No repo diffed, no MCP server connected.

```bash
gh api repos/Ataraxy-Labs/sem --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 2948, MIT (badge), Rust, pushed 2026-06-17
gh api repos/Ataraxy-Labs/sem/readme --jq '.content' | base64 -d | head -75               # entity-level diff/blame/impact, tree-sitter, MCP
```

## What worked

- **Right primitive for agents.** "Code is not text" — diffing by entity (function/class/method) is exactly the structural signal an agent needs to understand a change's *meaning* and blast radius, versus reconstructing it from line hunks.
- **Zero-setup, any repo.** Works on plain Git with no indexing service or config; single Rust binary is fast and easy to adopt.
- **Entity-level blame + impact analysis.** Beyond diffs, "who last changed this function" and "what this change affects" are high-value for review and safe edits.
- **Agent-native via MCP.** Built "for coding agents" with an MCP surface — it slots directly into the loop rather than being a human-only CLI.
- **Broad language coverage.** 28+ languages via tree-sitter; 133 passing tests; trending traction (2.9K stars).

## What didn't work or surprised us

- **Adjacent to, not a replacement for, semantic search.** sem analyzes *changes* (diff/blame/impact); it isn't a whole-codebase retrieval index like serena/claude-context — complementary, not a substitute.
- **Value depends on tree-sitter fidelity.** Entity extraction is only as good as the grammar per language; edge cases (macros, generated code, unusual syntax) may degrade.
- **Young, single-vendor stack.** Part of Ataraxy Labs' broader (early) suite; some value is realized alongside siblings (weave/inspect), which is more buy-in.
- **Impact analysis scope unclear.** "Impact analysis" is powerful but its depth (call-graph vs. file-level) isn't verified here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Entity-level diffs + impact analysis help agents (and reviewers) reason about what actually changed and what it affects. |
| Speed | + | Rust binary, zero-setup; entity diffs are a denser signal than raw line hunks, cutting exploration. |
| Maintainability | + | Entity blame + impact analysis make change archaeology and safe refactoring easier. |
| Safety | + | Knowing a change's blast radius before applying it reduces unintended breakage. |
| Cost Efficiency | + | Compact structural diffs feed agents fewer, higher-signal tokens than full-file/line context. |

## Verdict

**CONDITIONAL** — sem is a sharp, MIT-licensed, zero-setup tool that gives Git an **entity-level semantic layer**: diff, blame, and impact analysis over functions/classes/methods via tree-sitter, delivered as a fast Rust binary with an MCP server built for coding agents. Adopt it to give agents (and reviewers) a structural view of *changes* — what function changed and what it affects — rather than line hunks they must re-interpret. It complements, not replaces, whole-codebase semantic search (serena/claude-context): sem is about understanding diffs, they're about finding code. Pilot it in any Git repo (no setup cost) and weigh deeper buy-in to the Ataraxy stack (weave/inspect) separately.

Compared to neighbors: **serena** does LSP symbol-level find/refactor; **codegraph**/**code-review-graph** build structural/blast-radius graphs; **Understand-Anything** turns code into a knowledge graph. sem's distinguishing pitch is **entity-level git diff/blame/impact (semantic version control) with zero setup and an MCP surface for agents.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sem](https://github.com/Ataraxy-Labs/sem) | tool | Semantic version control on top of Git (MIT, Rust) — parses code with tree-sitter (28+ languages) to diff/blame/impact-analyze at the entity level (functions, classes, methods) instead of lines; works in any repo with no setup, CLI + MCP for agents | Line diffs tell an agent "lines x–y changed," not "function foo was modified"; want structural, entity-level change understanding | serena, codegraph, code-review-graph, Understand-Anything |
