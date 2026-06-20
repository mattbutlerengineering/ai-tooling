# Evaluation: ts-morph

**Repo:** [dsherret/ts-morph](https://github.com/dsherret/ts-morph)
**Stars:** ~6,100 | **Last updated:** 2026-04-12 | **License:** MIT
**Dev loop stage:** Plan / Implement (static analysis + codemods)
**Layer:** Tooling

---

## What it does

A TypeScript Compiler API wrapper that makes it far easier to programmatically navigate and manipulate TypeScript/JavaScript ASTs. Instead of wrestling with the raw `typescript` Compiler API, you get an ergonomic object model for reading, querying, and editing source files.

Mechanically you load a project (or files), then traverse and mutate the AST — find classes/functions/imports, read types, add/remove/rename nodes, and write the changes back as valid code. It ships `@ts-morph/bootstrap` for quickly standing up the Compiler API, and pairs with the [ts-ast-viewer.com](https://ts-ast-viewer.com) playground for exploring AST shapes. In an AI-assisted workflow, ts-morph is the deterministic substrate for codemods and structural refactors: rather than having an LLM string-edit TS and risk syntactic breakage, you (or an agent calling a ts-morph script) make type-aware, structurally-correct transforms.

## How we tested it

Architecture review against the repo (monorepo for `ts-morph` + `@ts-morph/bootstrap`), the README, and the documented purpose (Compiler API wrapper for static analysis and programmatic code changes). Confirmed it's a mature, widely-depended-on library (it underpins many codegen/codemod tools). Note last push ~2026-04 — steady, not high-churn. Not exercised against a live codebase transform here, so condition-gated.

```bash
gh api repos/dsherret/ts-morph --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/dsherret/ts-morph/readme --jq '.content' | base64 -d
```

## What worked

- **Deterministic, type-aware transforms.** AST-level edits are syntactically safe by construction — the right tool when an LLM's regex/string edits to TS would risk corruption.
- **Ergonomic over the raw Compiler API.** Dramatically lower friction than `typescript` directly; `@ts-morph/bootstrap` + ts-ast-viewer shorten the learning curve.
- **Battle-tested foundation.** A long-standing, heavily-used library — a safe base for codegen, codemods, and migrations (conceptually the TS analogue of OpenRewrite's deterministic recipes).

## What didn't work or surprised us

- **It's a library, not an agent tool.** Value in an AI workflow comes from an agent *writing ts-morph scripts*; it isn't a drop-in skill/MCP. The win is giving agents a deterministic transform layer.
- **TS/JS-only.** Scope is the TypeScript ecosystem; for polyglot migrations you'd reach for OpenRewrite or ast-grep.
- **Learning curve remains.** Even wrapped, AST manipulation requires understanding node kinds and the Compiler API model.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | AST/type-aware edits can't produce syntactically invalid TS |
| Speed | + | Scripted bulk refactors beat manual or LLM-by-hand edits |
| Maintainability | + | Repeatable codemods for large structural changes/migrations |
| Safety | + | Deterministic transforms vs. non-deterministic LLM rewrites |
| Cost Efficiency | + | Free, local, no model calls for the transform itself |

## Verdict

**CONDITIONAL**

Adopt as the deterministic transform substrate for TS/JS codemods and refactors — especially to have an agent generate ts-morph scripts instead of string-editing source. For polyglot or recipe-driven migrations, OpenRewrite is the cross-language analogue. Best value when you have repeatable, structural changes across many files rather than one-off edits.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ts-morph](https://github.com/dsherret/ts-morph) | tool | TypeScript Compiler API wrapper (MIT, ★6.1K) — programmatically navigate/manipulate TS/JS ASTs for static analysis and codemods; a typed, structural way for agents/scripts to refactor code instead of regex editing | LLM/regex edits to TS/JS are syntactically fragile; want type-aware, AST-level reads and transforms | openrewrite, sem, serena, ast-grep (ext.) |
