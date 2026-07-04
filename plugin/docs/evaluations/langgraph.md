# Evaluation: LangGraph

**Repo:** [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
**Stars:** 35,206 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (library for building AI applications)
**Layer:** Infrastructure

---

## What it does

A low-level orchestration framework for building stateful, multi-actor agents and long-running LLM workflows. You model your agent as a graph: nodes are functions (LLM calls, tools, arbitrary Python/TS) and edges define control flow, including conditional and cyclic edges. State is a typed object threaded through the graph and updated by reducers. The framework is inspired by Pregel and Apache Beam (message-passing over a computational graph), with a public interface drawing from NetworkX.

The core value props are infrastructure for *applications you build*: durable execution (checkpointers in SQLite/Postgres persist state so a run resumes exactly where it failed), human-in-the-loop (interrupt a graph, inspect/modify state, resume), short- and long-term memory, streaming, and a deployment platform (LangSmith Deployment / Studio). The monorepo ships several libraries: `langgraph` (core), `prebuilt` (high-level `create_react_agent`-style helpers), `checkpoint*` (persistence), `cli` (deploy/serve LangGraph apps), and Python/JS SDKs that talk to the LangGraph Server REST API. A higher-level package, Deep Agents, is built on top for plan/subagent/filesystem workflows.

## How we tested it

**Evidence:** REVIEW

Architecture review based on the repo's README, AGENTS.md / CLAUDE.md, monorepo library layout, and the `examples/` directory. Did not hands-on install or run a graph — LangGraph is an application-building framework, not a Claude Code extension, so the relevant question is structural: does it have any surface area in the dev loop, the same lens applied to aisuite.

```bash
gh api repos/langchain-ai/langgraph --jq '{desc,stars,license,lang,homepage}'
gh api repos/langchain-ai/langgraph/contents --jq '.[].name'
gh api repos/langchain-ai/langgraph/contents/examples --jq '.[].name'
gh api repos/langchain-ai/langgraph/contents/examples/code_assistant --jq '.[].name'
gh api repos/langchain-ai/langgraph/contents/CLAUDE.md --jq '.content' | base64 -d   # == AGENTS.md
```

Reviewed: 8 monorepo libraries (core, prebuilt, checkpoint/-postgres/-sqlite, cli, sdk-py, sdk-js); the `examples/` tree (code_assistant, multi_agent, human_in_the_loop, plan-and-execute, lats, rewoo, reflexion, rag, customer-support, web-navigation, usaco); and the AGENTS.md/CLAUDE.md files that prior discovery flagged.

## What worked

- **Durable execution is a genuinely strong primitive** — pluggable checkpointers (SQLite, Postgres) let a stateful run survive a crash and resume from the exact step, which is hard to get right by hand
- **Graph model is expressive** — conditional + cyclic edges cleanly express agent loops, branching, and multi-agent handoffs that are awkward in linear chains
- **First-class human-in-the-loop** — interrupting a graph to inspect/modify state and resume is built in, not bolted on
- **Mature, broadly adopted, well-documented** — 35K stars, MIT, used by Klarna/Replit/Elastic, extensive examples and an academy course; the JS/TS twin (LangGraph.js) gives cross-language parity

## What didn't work or surprised us

- **It is a framework for building agents, not a tool that improves your dev workflow** — the README's own one-liner is "Low-level orchestration framework for building stateful agents." You use LangGraph to build something like a coding agent; you do not run LangGraph to get help coding. Same category as aisuite (SKIP).
- **The AGENTS.md / CLAUDE.md are a red herring** — prior discovery flagged their presence as a possible signal. They are identical files containing only *contributor* instructions for this monorepo (`make format`, `make lint`, `make test`, `TEST=path make test`) plus a library dependency map. They are coding-agent instructions for people *editing LangGraph*, not evidence that LangGraph is a dev-loop tool.
- **The `code_assistant` example is a tutorial, not a tool** — it is two Jupyter notebooks (`langgraph_code_assistant.ipynb`, `_mistral.ipynb`) showing how to *build* a code-generation agent with LangGraph. It is a teaching artifact, not something you install into your workflow.
- **No Claude Code integration whatsoever** — no plugin, skill, MCP server, or hook. It lives entirely outside the inner/outer dev loop, and most of its production value is coupled to the paid LangSmith/LangSmith Deployment ecosystem.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A framework for building apps; doesn't make your own code more correct |
| Speed | neutral | Doesn't affect your development speed within a coding agent |
| Maintainability | neutral | No integration with the dev workflow; adds a dependency only if you build on it |
| Safety | neutral | Human-in-the-loop/durable execution protect apps you build, not your dev sessions |
| Cost Efficiency | neutral | Checkpointing/streaming optimize the apps you ship, not your agent sessions |

## Verdict

**SKIP**

LangGraph is one of the best low-level frameworks for building stateful, durable, multi-actor agent *applications* — the graph model, checkpointers, and human-in-the-loop primitives are well-engineered and widely adopted. But in this catalog's framework (tools that move quality signals in *your* dev loop for AI-assisted coding), it has no surface area: it doesn't write your code, review PRs, manage context, or integrate with any coding agent. The AGENTS.md/CLAUDE.md flagged in discovery are ordinary monorepo contributor instructions, and the `code_assistant` example is a build-it-yourself tutorial — neither makes LangGraph a dev-loop tool. Adopt it when *building* an AI agent product; it does not belong in a development-workflow stack. (Identical reasoning to the aisuite SKIP.)

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [LangGraph](https://github.com/langchain-ai/langgraph) | framework | Low-level orchestration framework for building stateful, durable, multi-actor LLM agents | Building long-running agents with cyclic control flow, persistence, and human-in-the-loop is hard from scratch | aisuite (both are libraries for building AI apps, not dev-loop tools) |
