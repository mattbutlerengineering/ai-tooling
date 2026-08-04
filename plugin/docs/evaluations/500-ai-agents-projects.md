# Evaluation: 500-AI-Agents-Projects

**Repo:** [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects)
**Stars:** 32,806 | **Last updated:** 2026-06-06 (pushed) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reference (cross-cutting — agent use-case catalog)
**Layer:** Reference (curated index of projects)

---

## What it does

500-AI-Agents-Projects is a **curated collection of AI agent use cases across industries** — healthcare, finance, education, retail, and more — each illustrating a practical application and linking to **open-source projects** that implement it. It's organized as a browsable index (use case → industry → implementation link), positioned as inspiration + starting points rather than a framework.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not a hands-on tool.** This is a curated list, not software. Assessment is based on the repository description, structure, and metadata; no linked projects were cloned or run.

```bash
gh api repos/ashishpatel26/500-AI-Agents-Projects --jq '{stars,license:.license.spdx_id,desc:.description}'   # 32.8K, MIT
```

## What worked

- **Use-case-first indexing.** Organizing by industry/application (not by framework) is a useful lens when you're scoping "what could an agent do here" and want a concrete open-source starting point.
- **Breadth.** ~500 entries across many sectors is a wide net for inspiration and prior art.
- **MIT, popular, actively maintained** (~33K stars, recent pushes).

## What didn't work or surprised us

- **Curation depth varies.** A 500-item list is inevitably uneven — entries are pointers, not evaluations; quality/maintenance of linked projects isn't vetted here.
- **Overlaps existing agent indexes.** It sits alongside awesome-ai-agents and awesome-llm-agents; differentiation is the industry-use-case framing rather than a tool taxonomy.
- **Inspiration, not implementation guidance.** It shows *what* exists, not *how* to build production agents (that's what tutorial references like genai-agents cover).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Reference index; no runtime effect. |
| Speed | + / neutral | Faster prior-art discovery when scoping an agent use case. |
| Maintainability | neutral | — |
| Safety | neutral | Linked projects are unvetted; evaluate any before adoption. |
| Cost Efficiency | neutral | — |

## Verdict

**discovery-log — tentative read (reference)** — a broad, MIT, industry-organized **catalog of ~500 agent use cases with open-source implementation links**. Useful as a discovery/inspiration index when scoping what an agent could do in a given domain and wanting concrete prior art. It overlaps the catalog's other agent indexes (awesome-ai-agents, awesome-llm-agents); its distinguishing angle is the use-case-by-industry framing. Treat linked projects as leads to evaluate, not vetted recommendations.

Compared to neighbors: **awesome-ai-agents** / **awesome-llm-agents** index agents/tools by type; **genai-agents** teaches building. This list's distinguishing role is **breadth of real-world use cases mapped to implementations**.

## Triage note

Left at `discovery-log`. ★34K, MIT, pushed 2026-06-06 — the broadest use-case index in the catalog,
with each of the ~500 entries linked to an open-source implementation.

That linkage is what distinguishes it from the awesome-lists it sits beside and why it absorbed
`awesome-llm-agents` in this pass: a list of frameworks tells you what exists, a list of use cases
with implementations tells you what has been built. Industry-organized rather than dev-loop
organized, so it is a discovery resource rather than a stack input.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) | reference | Curated index of ~500 AI agent use cases across industries (★33K, MIT), each linked to open-source implementations | Want concrete prior art / inspiration for what agents can do in a given domain, with starting-point repos | awesome-ai-agents, awesome-llm-agents, genai-agents |
