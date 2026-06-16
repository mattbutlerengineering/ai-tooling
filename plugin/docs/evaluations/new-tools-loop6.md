# New Tools Evaluation (Loop 6)

High-star catalog tools and user-requested additions, assessed for WORKFLOW.md inclusion.

## opencode
**Repo:** [anomalyco/opencode](https://github.com/anomalyco/opencode)
**Stars:** 174,943 | **Last updated:** 2026-06-16 | **Forks:** 21,194
**What it does:** Terminal-based open-source AI coding agent with a dual-mode system (Build agent for full file/command access, Plan agent for read-only analysis). Supports multi-platform install and 20+ languages. A `@general` subagent handles complex searches and multi-step tasks.
**Current workflow alternative:** Claude Code is the primary coding agent in this workflow. claude-squad can manage OpenCode alongside Claude Code sessions.
**Key difference:** The dominant open-source competitor to Claude Code — 175K stars. Tiered permission system (read-only Plan mode vs. full Build mode) is a tighter UX affordance than Claude Code's trust-level flags.

**Verdict:** CONDITIONAL — open-source Claude Code alternative
**Justification:** Competes directly with Claude Code, not complementary. Adopting both creates context-switching overhead with no clear gain. Earns conditional mention for teams that need an open-source, self-hostable agent (compliance, cost, or licensing constraints) or for claude-squad parallel sessions across providers. The leading open-source substitute when Claude Code isn't viable.

---

## dify
**Repo:** [langgenius/dify](https://github.com/langgenius/dify)
**Stars:** 145,378 | **Last updated:** 2026-06-16 | **Forks:** 22,865
**What it does:** Visual LLM application platform combining drag-and-drop workflow builder, RAG pipeline, multi-model orchestration, prompt playground, and production observability. Targeted at teams shipping AI-powered applications to end users.
**Current workflow alternative:** Nothing — the workflow is Claude Code-centric and focused on developer tooling, not AI product delivery. Flowise and LangGraph already excluded on the same grounds.
**Key difference:** More complete than Flowise (adds RAG, prompt management, monitoring) and more GUI-driven than LangGraph. But it's a platform for building AI products for others, not a tool that improves how you write software.

**Verdict:** SKIP
**Justification:** Same category as Flowise and LangGraph — product-building platform, not dev-workflow accelerator. With 145K stars it's clearly best-in-class for visual agentic app delivery, but "best-in-class for a different job" is out of scope. If the catalog adds a "Building AI Products" section, dify would be the top entry.

---

## goose
**Repo:** [aaif-goose/goose](https://github.com/aaif-goose/goose)
**Stars:** 49,512 | **Last updated:** 2026-06-16 | **Forks:** 5,233
**What it does:** General-purpose AI agent (desktop app, CLI, embeddable API). Built in Rust, supports 15+ LLM providers and 70+ MCP extensions. Under the Linux Foundation's Agentic AI Foundation governance.
**Current workflow alternative:** Claude Code is the primary agent. Both are agentic CLI/app platforms that run locally, connect to MCP servers, and execute multi-step tasks.
**Key difference:** Model-agnostic and provider-flexible (swap between Claude, GPT-4o, Gemini, local Ollama), ships a native desktop GUI, and is Linux Foundation-governed open source with no vendor lock-in.

**Verdict:** CONDITIONAL — multi-provider alternative to Claude Code
**Justification:** Direct platform-level competitor, not a complement. The case for conditional inclusion is narrow: teams needing multi-provider flexibility (Ollama locally, GPT-4o for cost, air-gapped environments) would find goose a meaningful alternative. Should not be listed alongside Claude Code as additive, but as a swap-in alternative for provider constraints.

---

## agentskills
**Repo:** [agentskills/agentskills](https://github.com/agentskills/agentskills)
**Stars:** 20,565 | **Last updated:** 2026-05-20 | **Forks:** 1,286
**What it does:** The canonical open specification for portable AI agent skills. Defines the SKILL.md file format and three-stage progressive disclosure protocol (Discovery, Activation, Execution). Originally developed by Anthropic, now open-sourced as an ecosystem standard meant to work across all compatible agent clients.
**Current workflow alternative:** This is the underlying specification that agent-skills and mattpocock/skills are both built on. Already implicit in the workflow — every skill in the catalog uses this format.
**Key difference:** This is the spec/format definition, not a skill collection. It is to skills what OpenAPI is to APIs — the schema and contract, not the content.

**Verdict:** ADD to catalog as reference entry (no ACMM level — underpins all levels)
**Justification:** The catalog lists reference entries for skill collections (awesome-claude-code, awesome-claude-skills) but not the canonical spec itself. With 20K+ stars it's the most-referenced item in the skills space. Belongs as a reference entry alongside the skill collections, not as a workflow recommendation at any specific level.
