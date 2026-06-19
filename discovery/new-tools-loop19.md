# Discovery loop 19 — 2026-06-19

Source: `gh api user/starred` ∩ not-in-CATALOG.md, triaged for AI-assisted-software-development scope. Run after the catalog reached 279/279 (100%) evaluated.

## In-scope candidates → add + evaluate next batch

| Repo | ★ | Type | Proposed category | Note |
|------|----|------|-------------------|------|
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 139.7k | framework | Implement | Python LangChain — the conspicuously-missing counterpart to LangChain.js (just added). App-building framework; likely SKIP/adjacent like LangGraph. |
| [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | 54k | framework | Implement / Agent Orchestration | Role-playing multi-agent orchestration framework; peer of LangGraph/AutoGen. |
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 105k | platform | Implement | Open-source Gemini coding-agent CLI; direct peer of qwen-code, opencode, claude-code. In-scope. |
| [letta-ai/letta](https://github.com/letta-ai/letta) | 23.4k | platform | Memory & Context | Stateful agents with advanced memory (formerly MemGPT); peer of OMEGA/claude-mem/agentmemory. |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | 156k | tool | Code Understanding / Plan | File/Office→Markdown converter — agent doc-ingestion utility; complements repomix/opensrc. |
| [vercel/ai](https://github.com/vercel/ai) | 25k | framework | Implement | Vercel AI SDK for TypeScript; app-building framework, peer of LangChain.js. |
| [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | 8k | MCP server | MCP Servers / Memory | Code-intelligence MCP that indexes a codebase into a persistent knowledge graph; peer of code-context-engine. |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 22.1k | reference | Reference | 100+ specialized Claude Code subagents; peer of awesome-claude-code. |
| [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) | 67.5k | reference | Reference | 12-lesson agent-building course; peer of ai-engineering-from-scratch, claude-howto. |
| [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) | 22.7k | reference | Reference | 50+ GenAI agent technique tutorials; learning reference. |
| [triggerdotdev/trigger.dev](https://github.com/triggerdotdev/trigger.dev) | 15.4k | platform | Ship / Outer Loop | Deploy managed AI agents/workflows; agent-deployment infra. |
| [vercel/sandbox](https://github.com/vercel/sandbox) | 147 | tool | Agent Harnesses | Ephemeral compute primitive to safely run untrusted/agent-generated code; isolation peer of sandboxd/sandcastle. |

## Adjacent / likely SKIP if added (build LLM *apps*, not the dev loop)

reworkd/AgentGPT, infiniflow/ragflow, HKUDS/nanobot, NousResearch/hermes-agent + SamurAIGPT/awesome-hermes-agent (Hermes cluster), activepieces/activepieces, alibaba/page-agent, onyx-dot-app/onyx.

## Out of scope (general dev / creative / non-AI-dev) — not cataloged

three.js, cpython, aseprite, GSAP, ScrollTrigger, Cura, piskel, pixel-art-react, lenis, OpenAPI-Specification, google-maps-scraper, MoneyPrinterTurbo, openmed, FunASR, daily_stock_analysis, kubestellar/*, workos/*, xget, bulletproof-react, Front-End-Checklist, pulumi-fly, and the operator's own repos (mattbutlerengineering/*).

## Reference guides to consider (Reference category, lower priority)

aishwaryanr/awesome-generative-ai-guide, dair-ai/Prompt-Engineering-Guide, ashishpatel26/500-AI-Agents-Projects, NirDiamant/agents-towards-production, enescingoz/awesome-n8n-templates (n8n-specific).
