# Evaluation: pydantic-deepagents

**Repo:** [vstorm-co/pydantic-deepagents](https://github.com/vstorm-co/pydantic-deepagents)
**Stars:** ~880 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Python library for building Claude-Code-style "deep agents" on top of Pydantic AI. Its headline mechanic is **self-forking**: "the deep agent that forks itself" — split one task into N parallel branches, run them concurrently, and let an AI judge merge the winner.

Per the README it provides: tool-calling, sandboxed execution, multi-agent teams, skills, checkpoints, and "unlimited context" — usable either as a terminal agent or in one function call. It's 100% type-safe (Pydantic AI foundation), works with any model, and is self-hosted. The forking + judge pattern is the same idea as parallel-attempt/best-of-N harnesses (e.g. claude-octopus), delivered as a typed Python library you embed rather than a standalone app.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented capabilities (forking into N branches + AI-judge merge, tool-calling, sandboxed execution, multi-agent teams, skills, checkpoints, unlimited context; terminal or function-call use). Confirmed the Pydantic AI foundation and the type-safe/any-model/self-hosted properties. Not built a live agent, so condition-gated.

```bash
gh api repos/vstorm-co/pydantic-deepagents --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/vstorm-co/pydantic-deepagents/readme --jq '.content' | base64 -d
```

## What worked

- **Forking + judge as a library primitive.** Splitting a task into parallel branches and merging the best via an AI judge is a strong quality pattern, here as an embeddable, typed Python primitive rather than a separate tool.
- **Built on Pydantic AI, type-safe.** Riding Pydantic AI gives typed tool-calling and structured outputs; "any model, self-hosted" avoids lock-in.
- **Deep-agent kit.** Sandboxed execution, checkpoints, skills, and multi-agent teams cover the patterns deep-agent work needs.

## What didn't work or surprised us

- **Young/small.** ~880 stars; API stability and real-world durability are unproven.
- **Forking is expensive.** N parallel branches + a judge multiplies token cost; use it where the quality gain justifies the spend.
- **Overlaps pydantic-ai/claude-octopus.** It's a deep-agent layer on pydantic-ai with a forking pattern like claude-octopus; pick based on whether you want a typed Python library (this) vs. a standalone multi-model tool.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Fork-N + AI-judge merge raises answer quality vs. single attempt |
| Speed | + | Parallel branches explore concurrently |
| Maintainability | + | Type-safe (Pydantic AI); embeddable as a library |
| Safety | + | Sandboxed execution + checkpoints bound risk |
| Cost Efficiency | - | Forking multiplies token cost (N branches + judge) |

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** A Python library adding deep-agent patterns — self-forking with AI-judge merge, sandboxing, checkpoints, teams — on top of Pydantic AI.

**Its own evaluation says so.** Its recommendation is "adopt if you **build agents in Python** on Pydantic AI", positioning it as "a typed, embeddable library rather than a closed harness".

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

A consistency flag rather than a caveat: its foundation, `pydantic-ai`, is a **P0 measure** lead this band may not touch, and it is an agent-building framework of exactly the class being disposed here. So is `agent-kit`, also P0. The scope bar and the `next-evals.py` scoring function currently disagree about this category, and the scoring function wins by default because P0 is the only band that may reach ADOPT. Raised in the pass write-up; not acted on, because acting on it would mean this lane reaching into P0.

Re-open if it grows a dev-loop bridge of the kind `fast-agent` and `vercel/ai` have — a runnable
coding agent, an installable coding-agent skill, or a documented primitive for building a harness.
Nothing about the project's quality is in dispute; this is a category call.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pydantic-deepagents](https://github.com/vstorm-co/pydantic-deepagents) | framework | Claude Code-style "deep agents" in Python on Pydantic AI (MIT) — "the deep agent that forks itself": split a task into N parallel branches and let an AI judge merge the winner; tool-calling, sandboxed execution, teams, skills, checkpoints, unlimited context; type-safe, any model, self-hosted | Want deep-agent patterns (forking, judging, checkpoints, unlimited context) as a typed Python library, not a closed harness | pydantic-ai, voltagent, agent-kit, claude-octopus |
