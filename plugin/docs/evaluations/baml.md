# Evaluation: baml

**Repo:** [BoundaryML/baml](https://github.com/BoundaryML/baml)
**Stars:** ~8,400 | **Last updated:** 2026-06-20 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

BAML ("Basically a Made-up Language") is a typed prompting language for building reliable LLM functions, agents, and workflows. Its core idea: turn prompt engineering into **schema engineering** — you define the input/output types and the prompt becomes a typed function.

Mechanically, you write LLM functions in `.baml` files — `function ChatAgent(message: Message[], tone: "happy" | "sad") -> string` — and BAML generates type-safe clients you call from Python, TypeScript, Ruby, Java, C#, Rust, Go, or REST. You only write the prompts in BAML; the rest of your app stays in your language. It comes with full type-safety, streaming, retries, wide model support, and — notably — **reliable tool-calling even on models without native tool-calling APIs** (it handles structured output parsing itself). Tooling includes a VS Code playground, Prompt Fiddle, and example apps.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the function-as-prompt model. Confirmed the typed-function abstraction (`f(args) -> Type`), the multi-language codegen, the type-safe parsing/streaming/retries, and the structured-output approach to tool-calling on any model. Not built a live `.baml` project, so condition-gated.

```bash
gh api repos/BoundaryML/baml --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/BoundaryML/baml/readme --jq '.content' | base64 -d
```

## What worked

- **Schema-engineering over prompt-stringing.** Typing inputs/outputs and parsing structured results yields far more reliable LLM calls than hand-parsing free text — the right abstraction for production prompts.
- **Language-agnostic codegen.** Write prompts once in BAML, call from Python/TS/Ruby/Java/Go/etc. — fits polyglot teams without rewriting prompt logic per language.
- **Tool-calling on any model.** Reliable structured output even without native tool APIs broadens model choice and reduces provider lock-in.

## What didn't work or surprised us

- **A new language to learn.** `.baml` files plus a codegen step add a build dependency and a learning curve versus inline prompt strings.
- **Overlaps pydantic-ai / instructor.** Typed/structured LLM outputs are a crowded idea; BAML's edge is the dedicated language + multi-language codegen + VS Code tooling.
- **Prompts only.** By design you wire BAML functions into your app; it's not a full agent framework, so you still need orchestration around it.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Typed outputs + structured parsing cut malformed-response bugs |
| Speed | + | Streaming/retries built in; faster iteration via playground |
| Maintainability | + | Prompts as typed functions are testable and version-controlled |
| Safety | + | Schema-enforced outputs constrain what the model can return |
| Cost Efficiency | + | Reliable structured output reduces retry/repair token waste |

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** A domain-specific language for writing prompts as typed, testable functions with codegen into multiple host languages.

**Its own evaluation says so.** Its recommendation is "adopt when reliable, structured LLM outputs matter", compared against `pydantic-ai` and `instructor` — the structured-output tooling for AI applications.

The bar is not new and is not this lane's invention. `WORKFLOW.md`'s **Tools Deliberately
Excluded** table states it — "Flowise, LangGraph — visual/programmatic agent builders: for building AI
products, not for your own dev workflow" — and the catalog has already applied it nine times, to
`langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`, `aisuite`, `dify`, `Flowise` and
`RAGFlow`. The `langchain` eval spells out both the test and the exceptions: a framework earns a slot
only if it has a **dev-loop bridge**, as `fast-agent` does by doubling as a runnable MCP-native coding
agent and `vercel/ai` does by shipping a coding-agent skill plus a harness-building primitive.

A SKIP here removes nothing. Per the `Flowise` precedent — "SKIP for this catalog's purpose (keep as
a reference entry)" — the row stays in `CATALOG.md`; what changes is that it stops reading as
something to install into a dev loop.

This was the closest call in the batch, because BAML's differentiator *is* developer experience — a playground, tests, typed functions — which superficially reads like dev-loop tooling. The distinction that decides it: those affordances help you develop **the LLM feature inside your product**, not the loop in which you write code. By that test BAML is `langchain` with better ergonomics, and `langchain` is SKIPped.

Separately, the row is filed under **Dev Workflow** ("git management, planning, project orchestration, and development process"), which fits it no better than Agent Orchestration does. The misfiling is noted, not fixed — re-sectioning a row is a catalog edit, not a triage disposition.

Re-open if it grows a dev-loop bridge of the kind `fast-agent` and `vercel/ai` have — a runnable
coding agent, an installable coding-agent skill, or a documented primitive for building a harness.
Nothing about the project's quality is in dispute; this is a category call.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [baml](https://github.com/BoundaryML/baml) | framework | Typed prompting language for reliable LLM functions (Apache-2.0, ★8.4K) — write each prompt as a typed function (`f(args) -> Type`) with type-safety, streaming, retries, and reliable tool-calling on any model; generates clients for Python/TS/Ruby/Java/Go/etc. | Free-text prompt strings give unreliable, untyped outputs; want schema-engineered prompts with type-safe parsing and portable codegen | pydantic-ai, instructor (ext.), textgrad, haystack |
