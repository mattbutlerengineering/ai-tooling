# Evaluation: 12-Factor Agents

**Repo:** [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents)
**Stars:** 23,418 | **Last updated:** 2025-09-21 (pushed) | **License:** Apache-2.0 (code) / CC-BY-SA-4.0 (content) | **Type:** reference guide
**Dev loop stage:** Reference (agent engineering principles) — informs Plan/architecture
**Layer:** Process/Reference (a written methodology, not a tool)

---

## What it does

12-Factor Agents is **a set of 12 principles for building LLM-powered software "good enough to put in the hands of production customers,"** by Dex (HumanLayer), in the spirit of the [12 Factor App](https://12factor.net/) manifesto. Its thesis: the good agents in production aren't "here's a prompt and a bag of tools, loop until done" — they're **mostly deterministic software with LLM steps inserted at the right points.** The factors: (1) natural language → tool calls, (2) own your prompts, (3) own your context window, (4) tools are just structured outputs, (5) unify execution + business state, (6) launch/pause/resume with simple APIs, (7) contact humans with tool calls, (8) own your control flow, (9) compact errors into the context window, (10) small focused agents, (11) trigger from anywhere / meet users where they are, (12) make your agent a stateless reducer. Backed by conference talks, a visual nav, and per-factor deep-dive docs.

## How we tested it

**Evidence:** REVIEW

**Source-grounded reading — it is a document, not software.** Read the README and factor index; did not build the companion `create-12-factor-agent` scaffold.

```bash
gh api repos/humanlayer/12-factor-agents --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 23418, NOASSERTION (Apache code/CC content), pushed 2025-09-21
gh api repos/humanlayer/12-factor-agents/readme --jq '.content' | base64 -d | head -75               # 12 factors, thesis, visual nav
```

## What worked

- **The single most-cited agent-engineering framework.** 23K stars and ubiquitous reference in the field; "own your context window" / "small focused agents" / "stateless reducer" have become common vocabulary. As a Reference entry it's foundational.
- **Correct, contrarian thesis.** "Good agents are mostly software, with LLM steps sprinkled in" is the antidote to autonomous-loop hype, and it's borne out by what actually ships.
- **Actionable, not abstract.** Each factor is concrete engineering advice (structured outputs, unify state, compact errors, launch/pause/resume) with its own deep-dive — you can apply them directly.
- **Maps onto the catalog's own bias.** It rationalizes why deterministic-orchestration tools (GSD, flow-next, spec-kit) and context-engineering tools beat "prompt-and-pray," giving a principled spine to the whole catalog.
- **Dual-licensed openly.** Apache-2.0 code + CC-BY-SA content invites reuse and contribution.

## What didn't work or surprised us

- **It's principles, not a tool.** No install, nothing to run in your loop; value is in how it shapes design decisions, not in automation.
- **Slightly stale push (2025-09).** The content is durable, but it's not actively churning; some framework references predate the latest models/harnesses.
- **Framework-skeptical by design.** It deliberately avoids endorsing crew/langchain/langgraph — useful honesty, but readers wanting "what library do I use" won't find a recommendation here.
- **Knowing ≠ doing.** Like any manifesto, the factors are easy to nod along to and hard to actually hold the line on under deadline.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (indirect) | "Own your control flow / context / prompts" and "small focused agents" reduce the unreliability that plagues naive agent loops. |
| Speed | neutral | A design reference; no runtime effect — pays off in fewer architectural dead-ends. |
| Maintainability | + (indirect) | Stateless-reducer, unify-state, structured-output principles produce more debuggable, testable agent software. |
| Safety | + (indirect) | Human-contact-via-tool-calls and own-your-control-flow encode HITL and guardrails as first-class. |
| Cost Efficiency | + (indirect) | Context-window ownership and error compaction directly reduce token waste. |

## Verdict

**CONDITIONAL** (reference — read it) — 12-Factor Agents is the **canonical principles document for building production-grade agentic software**, and arguably required reading for anyone designing agent harnesses or LLM features. It earns its catalog place not as a tool but as the methodology that explains *why* the deterministic-orchestration, context-engineering, and human-in-the-loop tools elsewhere in this catalog work. "Adopt" it the way you adopt the 12 Factor App manifesto: internalize the factors, apply the ones that fit, and treat it as a design lens rather than a checklist. Its only real limits are that it's prose (nothing to install) and lightly stale.

Compared to neighbors: **dictionary-of-ai-coding** defines the vocabulary; **agents-best-practices** is a provider-neutral skill of practices; **claude-code-best-practice** is CC-specific. 12-Factor Agents' distinguishing contribution is **a coherent, widely-adopted set of engineering principles for reliable LLM software.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [12-factor-agents](https://github.com/humanlayer/12-factor-agents) | reference | HumanLayer's 12 principles for production-grade LLM software (★23K, Apache-2.0 code / CC-BY-SA content) — own your prompts/context/control-flow, tools as structured outputs, small focused agents, stateless reducer, human-contact via tool calls | "Prompt + tools + loop" agents aren't reliable enough for production; want battle-tested engineering principles for agentic software | dictionary-of-ai-coding, agents-best-practices, claude-code-best-practice |
