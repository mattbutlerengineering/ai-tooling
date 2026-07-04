# Evaluation: LangGraph.js

**Repo:** [langchain-ai/langgraphjs](https://github.com/langchain-ai/langgraphjs)
**Stars:** 3,024 | **Last updated:** 2026-06-19 (pushed; created 2024-01-09) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Adjacent to the loop, not inside it. LangGraph.js is a low-level orchestration framework for building *stateful agents and long-running workflows* — i.e. the runtime of an LLM application, not a tool that moves your own plan/implement/verify/review/ship loop. Its only dev-loop bridge is as the engine under a coding agent/harness someone builds.
**Layer:** Tooling (an npm orchestration library you `import` and build on, not a process or infrastructure for the dev loop)

---

## What it does

The catalog one-liner: "TypeScript/JavaScript port of LangGraph — stateful, resilient agent graphs with branching, cycles, and persistence." The README's headline is "**Low-level orchestration framework for building stateful agents**." Where LangChain.js supplies components and integrations, LangGraph.js supplies the *orchestration*: model your agent as a graph of nodes and edges with explicit shared state, then get durable execution, checkpointing, human-in-the-loop interrupts, and short/long-term memory. It is inspired by Pregel and Apache Beam (graph compute) with a NetworkX-flavored public interface, and explicitly can be used without LangChain.

The monorepo is substantial and reveals the real scope. `libs/` ships `langgraph-core` and `langgraph` (the engine), a full family of **checkpointers** (`checkpoint`, `checkpoint-sqlite`, `checkpoint-postgres`, `checkpoint-redis`, `checkpoint-mongodb`, plus `checkpoint-validation`), prebuilt orchestration patterns (`langgraph-supervisor`, `langgraph-swarm`, `langgraph-cua` for computer-use agents), a server/CLI/UI surface (`langgraph-api`, `langgraph-cli`, `langgraph-ui`), framework SDKs (`sdk`, `sdk-react`, `sdk-vue`, `sdk-svelte`, `sdk-angular`), and `create-langgraph` scaffolding. There is a `CLAUDE.md` in the repo root — the maintainers dogfood Claude Code on it.

The value proposition is reliability for *long-running, stateful* agent apps: resume-from-failure, inspect/modify state mid-run, persist memory across sessions. The README routes quick agent-building up to **Deep Agents** and observability/eval to **LangSmith**. Like LangChain.js, this is squarely an **application-building / agent-runtime** framework — the question for this catalog is whether that touches the dev loop, and it largely does not.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Nothing was `npm install`ed, no graph was compiled or executed, no checkpointer or interrupt was exercised. Every claim below comes from the repository (GitHub metadata, README, monorepo file tree, `libs/` package listing, release/contributor/issue counts), not from observed runtime behavior. The "durable / production-ready / trusted by LinkedIn/Uber/Klarna/GitLab" language is the authors' README framing, not anything we measured.

```bash
gh api repos/langchain-ai/langgraphjs --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/langchain-ai/langgraphjs/readme --jq '.content' | base64 -d | head -120
gh api "repos/langchain-ai/langgraphjs/git/trees/HEAD?recursive=0" --jq '.tree[].path'   # note root CLAUDE.md
gh api repos/langchain-ai/langgraphjs/contents/libs --jq '.[].name'   # core, checkpoint{,-sqlite,-postgres,-redis,-mongodb}, supervisor, swarm, cua, api, cli, ui, sdk{,-react,-vue,-svelte,-angular}
gh api repos/langchain-ai/langgraphjs/releases --jq 'length'          # 30 (page-1 cap; frequent changeset releases)
gh api repos/langchain-ai/langgraphjs --jq '{open_issues:.open_issues_count,forks:.forks_count}'  # ~85 open issues, ~508 forks
```

## What worked

- **The orchestration model is genuinely good.** Explicit graph + shared state + durable execution + checkpointing + human-in-the-loop interrupts is a coherent, battle-tested pattern for reliable long-running agents — and it is the one part of the LangChain ecosystem with real conceptual substance beyond integration glue.
- **Serious persistence story.** First-class checkpointers for SQLite/Postgres/Redis/MongoDB plus a `checkpoint-validation` package is more than a toy — this is what "resume from where it left off" actually requires.
- **Standalone-usable.** It explicitly does not require LangChain.js; you can adopt the orchestration engine without buying the whole component stack. That's a cleaner dependency than LangChain.js.
- **Prebuilt patterns + scaffolding.** `langgraph-supervisor`, `langgraph-swarm`, `create-langgraph`, and framework SDKs lower the cost of building multi-agent systems and wiring them into a UI.
- **Maintainer dogfooding.** A root `CLAUDE.md` shows the team builds it with Claude Code — a small but real signal of active, AI-assisted maintenance.

## What didn't work or surprised us

- **It orchestrates *your app's* agents, not *your dev loop*.** This is decisive. LangGraph.js is the runtime engine for an LLM application's agent behavior; it does nothing for how you plan/implement/verify/review/ship your own codebase. That's the same boundary that put Python LangGraph on SKIP.
- **It is the literal JS port of an already-SKIPed entry.** Python LangGraph is in the catalog as **SKIP** with this exact reasoning. Consistency demands the same call here unless the JS version did something dev-loop-specific — it doesn't.
- **Scope creep toward a platform.** `langgraph-api` / `langgraph-cli` / `langgraph-ui` and the LangSmith Deployment funnel push it toward a hosted product. Useful for app teams, irrelevant to the dev loop, and a larger commitment than "a library."
- **Heavier mental model than its problem usually needs.** Graph/state/checkpointer machinery is justified for genuinely long-running stateful agents; for ordinary tool-using assistants it is a lot of ceremony — the same critique leveled at LangChain abstractions generally.
- **Dev-loop relevance is strictly indirect.** The one honest bridge: you could build a coding agent/harness *on* LangGraph.js (sandcastle is the closer in-catalog analog for "orchestrate coding agents in TS"). But then the harness is the dev-loop tool; LangGraph.js is its dependency.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral (out of scope) | Improves reliability of an *agent app you build* (durable execution, resumability); no direct effect on the correctness of your own code or dev loop. |
| Speed | + (for app-building) / neutral (for dev loop) | Prebuilt supervisor/swarm patterns and scaffolding speed building agent systems; no effect on the speed of your normal coding loop. |
| Maintainability | − (as a dependency) | Graph/state/checkpointer machinery plus a sprawling multi-package monorepo adds long-term weight to *your app*; lighter than full LangChain.js but still a large commitment. |
| Safety | neutral | A library you import; risk profile is that of the agent app you build (tool execution, persisted state, provider keys). No host/dev-loop reach by itself. |
| Cost Efficiency | neutral | App-runtime cost depends on the graphs you build; not a dev-loop cost lever. |

## Verdict

**SKIP — for this catalog's purpose, consistent with Python LangGraph. The best orchestration model in the ecosystem, but still an app-runtime framework, not a dev-loop tool.** LangGraph.js is a well-engineered, standalone-usable orchestration framework with a serious persistence/checkpointing story — genuinely the most substantive piece of the LangChain ecosystem. But it builds the *runtime of an LLM application*; it does not improve the loop by which you plan, implement, verify, review, and ship your own software. Since Python LangGraph is already **SKIP** for precisely this reason, the JS port gets the same verdict — the port adds no dev-loop-specific capability that would change the call.

Compared to neighbors: it is the direct sibling of **LangGraph (Python, SKIP)** and the orchestration layer above **LangChain.js (SKIP — components)**; both are app-building tools. **Flowise / dify** are the no-code/visual versions of the same "build an agent app" goal (also SKIP/adjacent). The closest in-catalog tool that *is* dev-loop-relevant is **sandcastle** — "orchestrate sandboxed coding agents in TypeScript" — because it orchestrates *coding* agents specifically; LangGraph.js is the generic engine you'd build something like that *on top of*. Keep the catalog row for ecosystem completeness and cross-linking, but it is not part of the recommended dev-loop stack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [LangGraph.js](https://github.com/langchain-ai/langgraphjs) | framework | TypeScript/JavaScript port of LangGraph — stateful, resilient agent graphs with branching, cycles, and persistence | Need complex stateful agent workflows (branching/cycles/checkpointing) in TS/JS | LangGraph (Python original), LangChain.js, sandcastle |
