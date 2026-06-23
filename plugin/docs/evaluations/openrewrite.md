# Evaluation: OpenRewrite

**Repo:** [openrewrite/rewrite](https://github.com/openrewrite/rewrite)
**Stars:** 3,555 | **Last updated:** 2026-06-19 (pushed) | **License:** Apache-2.0 (framework; some recipes differently licensed) | **Language:** Java (recipes run via Gradle/Maven plugins or Moderne CLI)
**Dev loop stage:** Code Review & Quality / Dev Workflow — deterministic refactoring
**Layer:** Tooling/Infrastructure (auto-refactoring engine + recipe catalog; agent tool calls via Moderne MCP)

---

## What it does

OpenRewrite (by Moderne) is **an open-source automated refactoring ecosystem for source code** — "fast, repeatable refactoring for developers." It's an auto-refactoring engine that runs prepackaged, open-source **recipes** for common framework migrations, security fixes, and stylistic consistency, "reducing your coding effort from hours or days to minutes." It provides parsers and base recipes for **Java, Kotlin, Groovy, JS/TS, Python, and C#**, run via Gradle/Maven plugins (one recipe per repo) or, on the commercial **Moderne** platform, across thousands of repos at once. The key concept is the **Lossless Semantic Tree (LST)** — a type-aware model of source built per run; Moderne serializes LSTs for reuse and exposes them to **coding agents as pre-computed context, type-aware search, and OpenRewrite recipes as deterministic tool calls** (via Prethink, Trigrep, and a local MCP server) — "less token overhead and more accuracy than reading a codebase file by file."

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No recipe executed, no LST built.

```bash
gh api repos/openrewrite/rewrite --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 3555, Apache-2.0, pushed 2026-06-19
gh api repos/openrewrite/rewrite/readme --jq '.content' | base64 -d | sed -n '172,226p'        # recipes, LST, languages, Moderne agent tools/MCP
```

## What worked

- **Deterministic where LLMs are not.** For mechanical, large-scale transformations (framework migrations, security fixes, style), a **type-aware recipe** is correct and repeatable — exactly the work you don't want a stochastic LLM guessing at. It's the deterministic complement to agentic refactoring.
- **The LST is genuinely useful to agents.** A type-aware, lossless model gives agents pre-computed structural context and recipes as **deterministic tool calls** — fewer tokens, fewer hallucinated edits than file-by-file reading. This is the agent-relevant hook.
- **Mature, battle-tested.** Years-old ecosystem, huge recipe catalog, Apache-2.0 core, used widely for enterprise migrations.
- **Multi-language.** Java/Kotlin/Groovy plus JS/TS, Python, C# parsers.

## What didn't work or surprised us

- **JVM-centric, heavyweight.** The engine is Java; deepest support is Java/JVM. Non-JVM languages have parsers, but **running recipes against the additional languages requires a Moderne license** — the open core is real but the breadth pulls toward the commercial platform.
- **The agent value lives mostly in Moderne.** LST serialization, Trigrep/Prethink, and the MCP server are Moderne platform features; the OSS repo alone is the engine + recipes, not the turnkey agent tooling.
- **Recipes, not reasoning.** It executes predefined transformations; novel/bespoke refactors need authoring a recipe (a real skill) — it's not a general "fix my code" agent.
- **Licensing nuance.** Framework Apache-2.0, but recipe and multi-language-execution licensing varies — read the licensing page before assuming "all free."

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Type-aware, deterministic recipes transform code reliably where LLM refactors drift; LST gives agents accurate context. |
| Speed | + | Migrations/fixes drop from hours/days to minutes; serialized LSTs cut agent exploration. |
| Maintainability | + | Repeatable, reviewable recipes eliminate tech debt consistently across a codebase. |
| Safety | + | Deterministic transforms + security-fix recipes avoid the risk of ad-hoc LLM edits. |
| Cost Efficiency | + / neutral | Open core saves token spend (recipes as tool calls vs. LLM reasoning); cross-language/multi-repo runs need a Moderne license. |

## Verdict

**CONDITIONAL** — OpenRewrite is the mature, Apache-2.0 standard for **deterministic, type-aware automated refactoring**, and it's increasingly agent-relevant: its Lossless Semantic Tree gives coding agents pre-computed structural context and exposes recipes as **deterministic tool calls** (via Moderne's MCP), which is more accurate and token-frugal than file-by-file LLM refactoring. Adopt it for **mechanical, large-scale transformations** — framework migrations, security fixes, style — especially in Java/JVM stacks, and pair it with agents so the agent *invokes* recipes rather than hand-rolling stochastic edits. It's CONDITIONAL because it's JVM-centric, the richest agent + multi-language/multi-repo capabilities live in the commercial Moderne platform, and bespoke refactors require authoring recipes.

Compared to neighbors: **code-review** finds issues to fix; **sem** gives entity-level diffs; **serena** does LSP symbol-level edits. OpenRewrite's distinguishing pitch is **deterministic, type-aware, recipe-driven code transformation that agents can call as a tool.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [openrewrite](https://github.com/openrewrite/rewrite) | framework | Deterministic automated refactoring engine (Apache-2.0, by Moderne) — runs/authors type-aware recipes over a Lossless Semantic Tree for framework migrations, security fixes, and style across Java/Kotlin/Groovy/JS-TS/Python/C#; agents call recipes as deterministic tool calls (Moderne MCP) | Large-scale migrations/fixes are slow and error-prone by hand, and LLM refactors are non-deterministic; want repeatable, type-aware code transformation | code-review, sem, serena |
