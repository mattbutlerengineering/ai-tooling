# Evaluation: Pydantic AI

**Repo:** [pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)
**Stars:** 17,861 | **Last updated:** 2026-06-18 (pushed) | **License:** MIT | **Language:** Python (PyPI: `pydantic-ai`)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-05  <!-- triaged: human -->
**Dev loop stage:** Agent Orchestration (agent-building framework) — for building LLM apps, adjacent to the coding dev loop
**Layer:** Infrastructure (framework/library)

---

## What it does

Pydantic AI is **a Python agent framework "to bring that FastAPI feeling to GenAI app and agent development."** From the Pydantic team (whose Pydantic Validation underpins the OpenAI SDK, Google ADK, Anthropic SDK, LangChain, LlamaIndex, CrewAI, Instructor, etc.). Highlights: **model-agnostic** (OpenAI, Anthropic, Gemini, DeepSeek, Grok, Cohere, Mistral, Bedrock, Vertex, Ollama, LiteLLM, Groq, OpenRouter, and many more, plus custom models); **fully type-safe** (moves errors from runtime to write-time, gives IDE/coding agents context); **seamless observability** via Pydantic Logfire / OpenTelemetry (tracing, evals, cost); **powerful evals**; and **extensible composable capabilities** (bundle tools, hooks, instructions, model settings — built-ins for web search, thinking, MCP — plus a Pydantic AI Harness capability library), with agents definable entirely in **YAML/JSON (no code)**.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No agent built, no providers wired.

```bash
gh api repos/pydantic/pydantic-ai --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 17861, MIT, pushed 2026-06-18
gh api repos/pydantic/pydantic-ai/readme --jq '.content' | base64 -d | head -56               # type-safe, model-agnostic, evals, capabilities, YAML agents
```

## What worked

- **Type-safety as a first-class agent concern.** "If it compiles, it works"-style static typing for agents is genuinely differentiating versus the stringly-typed feel of older frameworks, and it helps *coding agents* (and IDEs) reason about the code they write against it.
- **From the validation layer everyone already uses.** Pydantic underpins most of the ecosystem; building the agent framework "at the source" is a strong credibility and integration argument.
- **Observability + evals built in.** Logfire/OTel tracing, eval support, and cost tracking are production concerns most frameworks bolt on later.
- **Composable capabilities + declarative agents.** Bundling tools/hooks/instructions into reusable units, plus YAML/JSON agent specs, is a clean extensibility model.
- **Broadest provider coverage.** Nearly every model/provider, plus custom — avoids lock-in.

## What didn't work or surprised us

- **It builds LLM apps, not coding agents.** Like LangChain/crewAI/vercel-ai in this catalog, it's for *developers building agentic products*, not a drop-in coding harness — relevant as infrastructure, tangential to authoring code with an agent.
- **Logfire gravity.** Observability is tightest with Pydantic's own Logfire (OTel alternatives supported, but the smooth path is theirs).
- **Framework commitment.** A framework you build on; the payoff requires adopting its abstractions (agents, capabilities, deps).
- **Crowded, fast-moving space.** Competes with vercel-ai, LangGraph, crewAI, strands-agents, Microsoft Agent Framework; the wedge is type-safety + Pydantic provenance.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Static typing moves whole error classes to write-time; built-in evals catch behavior regressions. |
| Speed | neutral | Faster to a robust agent than rolling your own; still real app development. |
| Maintainability | + | Type-safe, composable capabilities + declarative specs are more maintainable than ad-hoc chains. |
| Safety | + (indirect) | Validated I/O and OTel observability aid reliability/governance of agentic systems. |
| Cost Efficiency | neutral | MIT/free; Logfire and inference cost money; cost tracking helps optimize. |

## Verdict

**SKIP — a framework for building AI products, which `WORKFLOW.md` excludes by name, and this
eval concedes the mismatch four separate times.**

The codified ground is *"Flowise, LangGraph — Visual/programmatic agent builders — for building AI
products, not for your own dev workflow"* (`WORKFLOW.md`, Tools Deliberately Excluded). The test a
framework must clear to keep a recommendation is a **dev-loop bridge** — something you run on your
own repo, as `fast-agent` has (a runnable MCP-native coding agent) and `vercel/ai` has (an
installable coding-agent skill plus a harness primitive). Pydantic AI ships neither. It is a Python
library you build agent products *on*.

**The unusual part is that nothing here is a new judgement — the eval already made it.** Four times,
in its own words:

- Header: *"Agent Orchestration (agent-building framework) — for building LLM apps, adjacent to the
  coding dev loop"*
- What didn't work: *"**It builds LLM apps, not coding agents.** Like LangChain/crewAI/vercel-ai in
  this catalog, it's for developers building agentic products, not a drop-in coding harness —
  relevant as infrastructure, tangential to authoring code with an agent."*
- Verdict (previous): *"its object is building LLM-powered applications/agents, not authoring code
  with a coding agent — the same framing as LangChain/crewAI/vercel-ai here"*
- Verdict (previous): *"Adopt it when you're building an agentic product or service in Python …
  it's overkill if you just want a coding harness."*

The three peers it names for that framing — `langchain`, `crewai`, `vercel-ai` — are settled: the
first two are SKIP under this exact rule, and `vercel-ai` is the exception that proves it, kept
because of the bridge Pydantic AI lacks. `agent-kit`, disposed in
[#352](https://github.com/mattbutlerengineering/ai-tooling/issues/352) on identical reasoning, was
one of 22 rows SKIPped by the agent-frameworks pass
([#348](https://github.com/mattbutlerengineering/ai-tooling/issues/348)). Pydantic AI belongs to that
class and was simply out of reach.

None of this is a quality judgement. Pydantic AI is plausibly the strongest general-purpose Python
agent framework going — type-safe, model-agnostic, observable, eval-capable, from the team whose
validation layer the ecosystem already depends on. Build an agentic product in Python and it is an
excellent choice. That is a different question from the one this catalog asks.

The row stays as reference (the `Flowise` precedent), so a reader comparing Python agent frameworks
still finds it with the evaluation intact.

## Triage note

**Disposed from P0 measure — the band it should never have entered
([#353](https://github.com/mattbutlerengineering/ai-tooling/issues/353)).**

`next-evals.py` scores a lead as `2*overlap_pressure + stage_gap_weight + evidence_bonus`. All three
terms measure how much *attention* a lead attracts; none asks whether it is a tool this catalog is
for. Pydantic AI scored 30.9 on **pressure 12** and landed 11th of 25 in the band reserved for leads
that might reach ADOPT — and P0 is the one band an unattended pass may not write to, so the only
lane that could dispose it was the one lane the score had routed it away from.

**Overlap pressure is what put it there, and it is self-reinforcing.** Twelve catalog rows name
Pydantic AI as a peer, and a large share of them are the agent-framework rows SKIPped *alongside* it
in [#348](https://github.com/mattbutlerengineering/ai-tooling/issues/348). The more thoroughly a
class is eliminated, the higher its survivors score. `agent-kit` — same class, same reasoning, same
pass — sat in P3 at pressure 9 and was disposed months earlier simply because it ranked lower.

Detector W (`--scope`, #353) now reports this shape. It flags a lead whose **own eval** concedes the
`WORKFLOW.md` exclusion, gated to the `framework`/`platform` Types the exclusion is about, and it
quotes the conceding phrase rather than deciding scope itself. This eval was its one finding.

Marked as a human pass rather than bulk: the disposition is a scope call on a P0 lead, which
eliminate-only does not delegate — and #353 reserved it explicitly. It costs a catalog row nothing
(the row stays) and frees the slot for a lead that could actually reach ADOPT.

_Triaged 2026-08-05 against `WORKFLOW.md`'s codified exclusion ([#353](https://github.com/mattbutlerengineering/ai-tooling/issues/353))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pydantic-ai](https://github.com/pydantic/pydantic-ai) | framework | GenAI agent framework "the Pydantic way" (MIT) — type-safe, model-agnostic (every major provider), composable capabilities (tools/hooks/MCP/web-search), built-in evals, Logfire/OTel observability, and YAML/JSON agent specs; from the Pydantic team | Building production GenAI apps/agents needs a type-safe, validated, observable framework instead of ad-hoc prompt plumbing | vercel-ai, fast-agent, crewAI, langchain, strands-agents |
