# Discovery loop 20 — 2026-06-19

**New vector:** GitHub topic search (`topic:claude-code`, `topic:agent-skills`, `topic:mcp-server`, sorted by stars), NOT the operator's starred set. This matters: the catalog had reached 100% coverage *relative to the user's stars*, but topic search finds in-scope tools beyond them — the ecosystem is larger than one person's stars. Filtered to ≥800★ and cross-referenced against CATALOG.md.

## New in-scope candidates → add + evaluate this batch

| Repo | ★ | Proposed category | Note |
|------|----|-------------------|------|
| [oraios/serena](https://github.com/oraios/serena) | 25.5k | Code Understanding / MCP | Semantic-code MCP toolkit (LSP-backed symbol retrieval + editing); strong peer of code-context-engine, codegraph, gortex, codebase-memory-mcp. |
| [tadata-org/fastapi_mcp](https://github.com/tadata-org/fastapi_mcp) | 11.9k | MCP Servers | Expose FastAPI endpoints as MCP tools with auth; peer of fastmcp (MCP-building). |
| [yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) | 14.2k | Skills & Plugins | Convert doc sites / GitHub repos / PDFs into Claude skills; skill-authoring peer of skill-creator. |
| [microsoft/SkillOpt](https://github.com/microsoft/SkillOpt) | 8.4k | Skills & Plugins | Text-space optimizer that trains reusable NL skills; skill-optimization (Reflect/Maintainability). |
| [mcp-use/mcp-use](https://github.com/mcp-use/mcp-use) | 10.1k | MCP Servers | Fullstack MCP framework for building MCP apps/clients; peer of fastmcp, fast-agent. |
| [microsoft/mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners) | 16.6k | Reference | MCP fundamentals curriculum; peer of ai-agents-for-beginners. |
| [mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) | 9.5k | Security & Safety | AI reverse-engineering MCP bridging IDA Pro to LLMs; niche security/RE peer of cve-mcp-server, pentest-ai. |

## Already cataloged (surfaced by search, confirmed present)

CowAgent, oh-my-claudecode, wshobson/agents, context7, claude-mem, graphify, ruflo, rtk, pm-skills, Agent-Reach, planning-with-files, antigravity-awesome-skills, last30days-skill, claude-howto, taste-skill, ui-ux-pro-max, open-design, nanoclaw, awesome-openclaw-skills, awesome-agent-skills (VoltAgent), trigger.dev, cognee, learn-claude-code, claude-code-best-practice, serena-neighbors, context-mode.

## Out of scope (not cataloged)

n8n, nuclear (music player), FunASR (speech), kubesphere, xiaohongshu-mcp / xiaozhi-esp32 (consumer/IoT), TrendRadar / career-ops / sansan0 (domain apps), NousResearch/hermes-agent (general agent product), sub2api / CLIProxyAPI (LLM relay proxies — borderline; revisit if a model-routing gap appears), OpenMetadata, open-metadata.

## Method note

Topic search is a higher-yield discovery vector than the starred diff once stars are exhausted. Future discovery loops should rotate vectors: starred diff → topic search (claude-code / agent-skills / mcp-server / ai-agents) → npm `claude-code` plugins → newsletter mentions.
