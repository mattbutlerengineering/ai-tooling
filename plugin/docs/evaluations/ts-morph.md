# Evaluation: ts-morph

**Repo:** [dsherret/ts-morph](https://github.com/dsherret/ts-morph)
**Stars:** ~6,100 | **Last updated:** 2026-04-12 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan / Implement (static analysis + codemods)
**Layer:** Tooling

---

## What it does

A TypeScript Compiler API wrapper that makes it far easier to programmatically navigate and manipulate TypeScript/JavaScript ASTs. Instead of wrestling with the raw `typescript` Compiler API, you get an ergonomic object model for reading, querying, and editing source files.

Mechanically you load a project (or files), then traverse and mutate the AST — find classes/functions/imports, read types, add/remove/rename nodes, and write the changes back as valid code. It ships `@ts-morph/bootstrap` for quickly standing up the Compiler API, and pairs with the [ts-ast-viewer.com](https://ts-ast-viewer.com) playground for exploring AST shapes. In an AI-assisted workflow, ts-morph is the deterministic substrate for codemods and structural refactors: rather than having an LLM string-edit TS and risk syntactic breakage, you (or an agent calling a ts-morph script) make type-aware, structurally-correct transforms.

## How we tested it

**Evidence:** RUN

**Hands-on**, ts-morph v28.0.0 `npm install`ed and driven via a real script against this repo's `presentations/development-process/deck-stage.js` (an IIFE-wrapped Web Components deck, ~1,900 lines) on 2026-06-20.

```js
import { Project, SyntaxKind } from "ts-morph";
const p = new Project({ compilerOptions: { allowJs: true } });
const sf = p.addSourceFileAtPath(".../deck-stage.js");
sf.getClasses().length                                  // → 0  (!)
sf.getDescendantsOfKind(SyntaxKind.ClassDeclaration)    // → 1  (the class is inside an IIFE)
sf.getDescendantsOfKind(SyntaxKind.MethodDeclaration)   // → 48 methods, names+params all readable
method.findReferences()                                 // resolves refs across the AST
```

**Measured results.** It installed clean and parsed real JS via `allowJs`. The instructive surprise: **top-level `getClasses()`/`getFunctions()` returned 0** because the deck wraps everything in an IIFE — the class is nested. Switching to `getDescendantsOfKind(...)` immediately found the class and **all 48 methods** (`connectedCallback`, `attributeChangedCallback`, `_render`, …) with correct names/param counts, and `findReferences()` resolved usages. This also **cross-validated the [skylos](skylos.md) eval**: `reset`/`goTo` showed only **1 AST-visible reference** (their own definition — they're called from HTML, which the TS AST can't see), and `observedAttributes` is a **static getter, not a method** — exactly the framework-callback patterns static tools mishandle.

## What worked

- **Parses real JS accurately (verified).** With `allowJs`, it correctly extracted all 48 methods of an IIFE-wrapped Web Components class with names, params, and resolvable references — clean install (v28), no config beyond `allowJs`.
- **Reference resolution is genuinely useful.** `findReferences()` works at the AST level — and honestly reports what it *can* see (1 ref for HTML-called methods), which is the right semantics for safe refactoring.
- **Deterministic, type-aware transforms.** AST-level edits are syntactically safe by construction — the right tool when an LLM's regex/string edits would risk corruption.
- **Ergonomic over the raw Compiler API.** Far lower friction than `typescript` directly; `@ts-morph/bootstrap` + ts-ast-viewer shorten the learning curve.

## What didn't work or surprised us

- **Top-level getters miss nested code (observed gotcha).** `getClasses()`/`getFunctions()` returned 0 on an IIFE-wrapped file — a real trap. You must reach for `getDescendantsOfKind(...)` for anything not declared at module top level (IIFEs, class expressions, `customElements.define(class …)`). An agent writing ts-morph scripts needs to know this or it'll silently "find nothing."
- **It's a library, not an agent tool.** Value comes from an agent *writing ts-morph scripts*; it isn't a drop-in skill/MCP. The win is giving agents a deterministic transform layer.
- **TS/JS-only.** Scope is the TypeScript ecosystem; for polyglot migrations you'd reach for OpenRewrite or ast-grep.
- **Learning curve remains.** AST manipulation requires understanding node kinds and the Compiler API model (the getClasses-vs-descendants distinction above is a concrete example).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | AST/type-aware edits can't produce syntactically invalid TS |
| Speed | + | Scripted bulk refactors beat manual or LLM-by-hand edits |
| Maintainability | + | Repeatable codemods for large structural changes/migrations |
| Safety | + | Deterministic transforms vs. non-deterministic LLM rewrites |
| Cost Efficiency | + | Free, local, no model calls for the transform itself |

## Verdict

**CONDITIONAL** *(verdict confirmed by hands-on testing)*

A reliable deterministic transform substrate for TS/JS codemods — verified parsing real JS and extracting full class/method/reference structure cleanly. Have an agent generate ts-morph scripts instead of string-editing source, but bake in one tested lesson: **use `getDescendantsOfKind` (not top-level `getClasses`/`getFunctions`)** so IIFE-wrapped and expression code isn't silently missed. For polyglot or recipe-driven migrations, OpenRewrite is the cross-language analogue. Best value for repeatable, structural changes across many files rather than one-off edits.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ts-morph](https://github.com/dsherret/ts-morph) | tool | TypeScript Compiler API wrapper (MIT, ★6.1K) — programmatically navigate/manipulate TS/JS ASTs for static analysis and codemods; a typed, structural way for agents/scripts to refactor code instead of regex editing | LLM/regex edits to TS/JS are syntactically fragile; want type-aware, AST-level reads and transforms | openrewrite, sem, serena, ast-grep (ext.) |
