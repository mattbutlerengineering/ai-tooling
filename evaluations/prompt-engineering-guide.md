# Evaluation: Prompt Engineering Guide (dair-ai)

**Repo:** [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
**Stars:** 75,755 | **Last updated:** 2026-03-11 (pushed) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reference (cross-cutting — prompt/context-engineering knowledge base)
**Layer:** Reference (guides, papers, lessons, notebooks)

---

## What it does

The Prompt Engineering Guide is **dair-ai's canonical, long-running reference** for prompt engineering — "guides, papers, lessons, notebooks and resources for prompt engineering, context engineering, RAG, and AI Agents." It's one of the most-starred prompt-engineering resources on GitHub (also published as a website and companion courses), covering techniques (zero/few-shot, CoT, ReAct, self-consistency, etc.), model-specific guidance, RAG, agents, and a curated paper/tool bibliography.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not a hands-on tool.** This is a knowledge base, not software to run. Assessment is based on the repository description, scope, and metadata, plus its well-known status as a reference; no notebooks were executed.

```bash
gh api repos/dair-ai/Prompt-Engineering-Guide --jq '{stars,license:.license.spdx_id,desc:.description}'   # 75.7K, MIT
```

## What worked

- **The default prompt/context-engineering reference.** Comprehensive, technique-by-technique coverage with linked papers — the place to send someone (or an agent) to ground prompting decisions in something other than folklore.
- **Stays current with the field's expansion.** Now explicitly spans context engineering, RAG, and agents, not just single-prompt tricks.
- **MIT, hugely popular, multi-format** (repo + site + notebooks + courses) — credible and broadly used.

## What didn't work or surprised us

- **It's foundations, not Claude-Code-specific.** General LLM prompting knowledge; it won't tell you how to structure CLAUDE.md, skills, or the agentic dev loop — that's what the catalog's Claude-Code-specific references (awesome-claude-code, claude-code-best-practice) cover.
- **Reference, not a workflow tool.** It informs how you write prompts/skills; it doesn't move a quality signal directly.
- **Slower cadence.** Pushed a few months ago — solid foundations, but the bleeding edge moves faster than a curated guide.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Better-grounded prompting/context design improves agent output quality indirectly. |
| Speed | neutral | Knowledge base; no runtime effect. |
| Maintainability | neutral | — |
| Safety | neutral | Covers some prompt-robustness/adversarial topics, but not a security tool. |
| Cost Efficiency | + / neutral | Better prompting (e.g. fewer retries, tighter context) can trim tokens. |

## Verdict

**discovery-log — tentative read (reference)** — the Prompt Engineering Guide is the **canonical foundations reference** for prompt/context engineering, RAG, and agents: MIT, comprehensive, and widely used. Keep it as the go-to grounding for *how to prompt*, distinct from the catalog's Claude-Code-specific guides (which cover skills, CLAUDE.md, and the agentic dev loop). It's background knowledge, not a tool that changes your loop.

Compared to neighbors: **ai-agents-for-beginners** / **genai-agents** teach agent building; **awesome-claude-code** indexes Claude-Code-specific configs. This guide's distinguishing role is **provider-agnostic prompt/context-engineering fundamentals** with a linked paper trail.

## Triage note

Left at `discovery-log`. ★76K, MIT — the canonical prompt- and context-engineering knowledge base,
spanning techniques, papers, notebooks, RAG and agents.

Last pushed 2026-03-11, which is the fact to watch: five months is long for a field this fast, and
the sections most likely to have aged (agents, context engineering) are exactly the ones this
catalog would cite. Still the standard reference; increasingly worth checking a claim's date before
repeating it.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | reference | Canonical prompt/context-engineering knowledge base (★75K, MIT) — techniques, papers, lessons, notebooks spanning prompting, context engineering, RAG, and agents | Want grounded foundations for how to prompt and structure context rather than folklore | ai-agents-for-beginners, genai-agents, awesome-llm-agents |
