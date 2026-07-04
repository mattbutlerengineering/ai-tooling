# Evaluation: baml

**Repo:** [BoundaryML/baml](https://github.com/BoundaryML/baml)
**Stars:** ~8,400 | **Last updated:** 2026-06-20 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
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

**CONDITIONAL**

Adopt when reliable, structured LLM outputs matter and you want prompts as typed, testable functions callable from multiple languages — especially valuable for polyglot teams or apps needing tool-calling on models without native APIs. Accept the new-language/codegen overhead. Compare with pydantic-ai/instructor if you're single-language Python and want a lighter-weight structured-output approach.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [baml](https://github.com/BoundaryML/baml) | framework | Typed prompting language for reliable LLM functions (Apache-2.0, ★8.4K) — write each prompt as a typed function (`f(args) -> Type`) with type-safety, streaming, retries, and reliable tool-calling on any model; generates clients for Python/TS/Ruby/Java/Go/etc. | Free-text prompt strings give unreliable, untyped outputs; want schema-engineered prompts with type-safe parsing and portable codegen | pydantic-ai, instructor (ext.), textgrad, haystack |
