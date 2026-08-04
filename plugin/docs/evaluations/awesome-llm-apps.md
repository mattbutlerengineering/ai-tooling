# Evaluation: awesome-llm-apps

**Repo:** [Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)
**Stars:** 117,152 | **Last updated:** 2026-07-10 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Research & Discovery (reference list)
**Layer:** Reference
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Over a hundred runnable AI agent and RAG applications spanning every major LLM provider, each a
working reference implementation rather than a link.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run any of the examples. Source-grounded only: GitHub metadata (fetched
2026-08-04) plus the CATALOG one-liner and "Overlaps with" cell (`awesome-ai-agents`,
`awesome-llm-agents`, `500-AI-Agents-Projects`). Enough to place it; not enough for a positive
verdict, and none is offered.

## Triage note

Left at `discovery-log`. Apache-2.0, ★117K, pushed 2026-07-10 — one of the most-starred entries in
the entire catalog, and a list this lane has no basis to dispose.

The three rows it overlaps are all curated *link* lists; this one ships **runnable code**, which is
a different artifact with a different failure mode. A link list rots when its targets move; a code
list rots when its dependencies break, and that is at least testable. Calling it redundant with
`awesome-ai-agents` would be the category error the challenger band exists to avoid.

The honest caveat is audience: these are examples of *building* LLM applications, not of using an
agent to write software. That places it in Reference — findable when the question is "what does a
working multi-agent RAG app look like", not part of the dev loop this catalog maps. It is a row to
keep, not a lead to promote.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | reference | 100+ runnable AI agent and RAG app examples across every major LLM provider | Finding concrete, working reference implementations for LLM app patterns (RAG, multi-agent, voice) means searching dozens of repos | awesome-ai-agents, awesome-llm-agents, 500-AI-Agents-Projects |
