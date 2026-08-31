# Tool Comparison

All 808 tools from CATALOG.md with dev loop stage, automation capability, pricing, and evaluation status at a glance.

**Verdict vocabulary** (per [ADR-0005](docs/adr/0005-verdict-vocabulary.md), implemented in #69):

- **ADOPT** / **KEEP** — recommended (KEEP = already installed & validated); run-backed or disclaimered.
- **CONDITIONAL** — a real conditional verdict on a tool we actually exercised (`Evidence` MEASURED/RUN), or one carrying a genuine `adopt-if:` condition.
- **SKIP** / **DEFER** — evaluated and not recommended (now), incl. license-disqualified tools.
- **discovery-log** — a catalogued *lead*, not a verdict: surfaced in triage but never exercised (`Evidence` REVIEW/SOURCE-ONLY). The eval's tentative read is notes, not a recommendation. Excluded from verdict-sync (D) and verdict-evidence (K). Promote to a real verdict by exercising the tool.

## Plan

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| CLI-Anything | tool | | ✓ | SKIP | REVIEW |
| claude-code-templates | tool | | ✓ | SKIP | REVIEW |
| portly | tool | | ✓ | discovery-log | SOURCE-ONLY |
| claude-hud | plugin | ✓ | ✓ | CONDITIONAL | RUN |
| ccstatusline | plugin | ✓ | ✓ | SKIP | REVIEW |
| dsh-TUI | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| codegraph | tool | ✓ | ✓ | ADOPT | MEASURED |
| code-review-graph | tool | | ✓ | discovery-log | REVIEW |
| context7 | MCP server | ✓ | ✓ | KEEP | RUN |
| feature-dev | plugin | | ✓ | KEEP | MEASURED |
| graphify | skill | | ✓ | CONDITIONAL | MEASURED |
| source-reading-methodology | skill | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| gentleman-book-mcp | MCP server | ✓ | ✓ | SKIP | REVIEW |
| git-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| GSD (Get Shit Done) | framework | | ✓ | KEEP | MEASURED |
| Foreman | plugin | | ✓ | discovery-log | SOURCE-ONLY |
| CodeJury | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| know-before-act | skill | | ✓ | SKIP | SOURCE-ONLY |
| requirement-ledger | skill | | ✓ | discovery-log | SOURCE-ONLY |
| vibe-coding-prompt-template | skill | | ✓ | SKIP | SOURCE-ONLY |
| claude-modular | framework | | ✓ | SKIP | REVIEW |
| spec-kit | framework | | ✓ | CONDITIONAL | RUN |
| Finn-loop | skill | | ✓ | discovery-log | SOURCE-ONLY |
| pm-manager | skill | | ✓ | SKIP | SOURCE-ONLY |
| claude-code-spec-workflow | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-my-workflow | tool | | ✓ | SKIP | SOURCE-ONLY |
| design.md | reference | | ✓ | discovery-log | SOURCE-ONLY |
| ccpm | skill | | ✓ | discovery-log | REVIEW |
| featherspec | tool | | ✓ | discovery-log | SOURCE-ONLY |
| OpenSpec | framework | | ✓ | discovery-log | REVIEW |
| BMAD-METHOD | framework | | ✓ | SKIP | REVIEW |
| 8090 Software Factory | platform | ✓ | | DEFER | REVIEW |
| software-factory-plugin | plugin | | ✓ | CONDITIONAL | MEASURED |
| factory (addyosmani) | tool | | ✓ | discovery-log | SOURCE-ONLY |
| spec_driven_develop | skill | | ✓ | discovery-log | REVIEW |
| reversa | framework | ✓ | ✓ | discovery-log | REVIEW |
| flow-next | plugin | ✓ | ✓ | discovery-log | REVIEW |
| mdn/mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| opensrc | tool | | ✓ | discovery-log | REVIEW |
| planning-with-files | skill | | ✓ | SKIP | REVIEW |
| reporails/cli | tool | | $ | discovery-log | SOURCE-ONLY |
| claude-md-doctor | tool | | ✓ | discovery-log | SOURCE-ONLY |
| dont-reinvent | skill | | ✓ | discovery-log | SOURCE-ONLY |
| open-skill-sunset | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| repomix | tool | | ✓ | CONDITIONAL | RUN |
| gitingest | tool | | ✓ | CONDITIONAL | MEASURED |
| repoprompt-ce | tool | | ✓ | discovery-log | SOURCE-ONLY |
| markitdown | tool | | ✓ | ADOPT | MEASURED |
| MinerU | tool | | ✓ | discovery-log | SOURCE-ONLY |
| deepwiki-rs | tool | | ✓ | discovery-log | SOURCE-ONLY |
| serena | MCP server | ✓ | ✓ | ADOPT | MEASURED |
| neuromesh | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| symbolpeek-mcp | MCP server | ✓ | ✓ | SKIP | SOURCE-ONLY |
| ts-morph | tool | | ✓ | CONDITIONAL | RUN |
| repowise | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| PocketFlow-Tutorial-Codebase-Knowledge | tool | ✓ | ✓ | discovery-log | REVIEW |
| project-mentor | skill | | ✓ | discovery-log | SOURCE-ONLY |
| claude-context | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| cocoindex-code | tool | ✓ | ✓ | discovery-log | REVIEW |
| sem | tool | ✓ | ✓ | discovery-log | REVIEW |
| semble | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| Understand-Anything | tool | | ✓ | discovery-log | REVIEW |
| codebase-design | skill | | ✓ | SKIP | REVIEW |
| domain-modeling | skill | | ✓ | SKIP | REVIEW |
| plannotator | tool | | ✓ | discovery-log | REVIEW |
| facet | MCP server | ✓ | ✓ | SKIP | SOURCE-ONLY |
| easel | tool | | ✓ | SKIP | SOURCE-ONLY |
| Remarc | tool | | ✓ | discovery-log | SOURCE-ONLY |
| code-context-engine | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| trace-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| SocratiCode | tool | ✓ | ✓ | discovery-log | REVIEW |
| gortex | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| codebase-to-course | skill | | ✓ | SKIP | REVIEW |
| sourcebot | platform | ✓ | ✓ | discovery-log | REVIEW |

## Implement

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| agency-agents | harness | | ✓ | SKIP | REVIEW |
| sol-skill | skill | ✓ | ✓ | SKIP | SOURCE-ONLY |
| CoordClaw | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| opendot | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| filesnap | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| agent-orchestrator | tool | ✓ | ✓ | discovery-log | REVIEW |
| sigbound | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| agmsg | tool | ✓ | ✓ | discovery-log | REVIEW |
| aidlc-workflows | framework | | ✓ | SKIP | REVIEW |
| arrow-js | framework | | ✓ | SKIP | REVIEW |
| beads | tool | ✓ | ✓ | KEEP | MEASURED |
| succubus | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| fleetpost | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| agent-link | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| aster | harness | | ✓ | SKIP | SOURCE-ONLY |
| caveman | skill | | ✓ | ADOPT | MEASURED |
| cherry-studio | platform | | ✓ | SKIP | REVIEW |
| eigent | platform | ✓ | ✓ | SKIP | REVIEW |
| herdr | tool | | ✓ | discovery-log | REVIEW |
| claurst | harness | | ✓ | SKIP | REVIEW |
| claude-code-harness | harness | | ✓ | SKIP | REVIEW |
| dot-reflex | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-router | tool | | ✓ | discovery-log | REVIEW |
| cursor-bridge | tool | | ✓ | SKIP | SOURCE-ONLY |
| codex-bridge | plugin | | ✓ | discovery-log | SOURCE-ONLY |
| CLIProxyAPI | tool | | ✓ | discovery-log | REVIEW |
| litellm | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| bifrost | tool | ✓ | ✓ | discovery-log | REVIEW |
| claude-code-staff-engineer | harness | | ✓ | SKIP | REVIEW |
| claude-squad | tool | | ✓ | CONDITIONAL | RUN |
| vibe-kanban | tool | | ✓ | discovery-log | SOURCE-ONLY |
| orca | platform | ✓ | ✓ | discovery-log | REVIEW |
| diri | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| hermes-conductor | reference | | ✓ | discovery-log | SOURCE-ONLY |
| task-state-guard | tool | | ✓ | discovery-log | SOURCE-ONLY |
| conflux-agent-workflow-2026 | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| flow (Aixle) | platform | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| multiplayer-ai | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| deadeye-cc | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| HolyClaude | platform | ✓ | ✓ | discovery-log | REVIEW |
| Nimbalyst | platform | | ✓ | SKIP | REVIEW |
| agent-of-empires | tool | | ✓ | SKIP | REVIEW |
| AgentsMesh | platform | ✓ | ✓ | SKIP | REVIEW |
| claude-task-master | tool | | ✓ | SKIP | REVIEW |
| capa | tool | | ✓ | discovery-log | REVIEW |
| ai-rules-sync | tool | | ✓ | discovery-log | SOURCE-ONLY |
| skills-manage | tool | | ✓ | SKIP | REVIEW |
| cc-devenv-doctor | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| skill-view | tool | | ✓ | discovery-log | SOURCE-ONLY |
| align-dev | tool | | ✓ | SKIP | REVIEW |
| cc-switch | tool | | ✓ | SKIP | REVIEW |
| claude-account | tool | | ✓ | discovery-log | SOURCE-ONLY |
| BossConsole | platform | | ✓ | SKIP | SOURCE-ONLY |
| commit-commands | plugin | | ✓ | SKIP | REVIEW |
| compound-engineering | plugin | | ✓ | discovery-log | REVIEW |
| context-mode | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| Continuous-Claude-v3 | harness | ✓ | ✓ | SKIP | REVIEW |
| CowAgent | harness | | ✓ | SKIP | REVIEW |
| deer-flow | harness | | ✓ | SKIP | REVIEW |
| DeepSeek-Reasonix | platform | | ✓ | discovery-log | REVIEW |
| dify | platform | | ✓ | SKIP | REVIEW |
| activepieces | platform | | ✓ | SKIP | SOURCE-ONLY |
| onyx | platform | | ✓ | SKIP | SOURCE-ONLY |
| dmux | tool | | ✓ | SKIP | REVIEW |
| ECC | harness | | ✓ | CONDITIONAL | RUN |
| fast-agent | framework | | ✓ | discovery-log | REVIEW |
| Flowise | platform | | ✓ | SKIP | REVIEW |
| langflow | platform | | ✓ | SKIP | SOURCE-ONLY |
| forkd | tool | | ✓ | discovery-log | REVIEW |
| gastown | tool | | ✓ | discovery-log | REVIEW |
| goose | platform | | ✓ | discovery-log | REVIEW |
| open-interpreter | harness | | ✓ | discovery-log | REVIEW |
| kilocode | platform | | ✓ | discovery-log | REVIEW |
| grok-cli | platform | | ✓ | discovery-log | REVIEW |
| Kaku | tool | | ✓ | SKIP | REVIEW |
| VelaTerm | tool | | ✓ | discovery-log | SOURCE-ONLY |
| jcode | harness | | ✓ | discovery-log | REVIEW |
| gstack | harness | | ✓ | discovery-log | REVIEW |
| gbrain | harness | | ✓ | SKIP | SOURCE-ONLY |
| happy | platform | | $ | discovery-log | REVIEW |
| harness | skill | | ✓ | SKIP | REVIEW |
| headroom | tool | ✓ | ✓ | CONDITIONAL | MEASURED |
| ctxwise | tool | | ✓ | discovery-log | SOURCE-ONLY |
| claude-context-optimizer | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| hive | harness | | ✓ | SKIP | REVIEW |
| humanlayer | harness | | ✓ | SKIP | REVIEW |
| KARIMO | plugin | | ✓ | SKIP | REVIEW |
| LangGraph | framework | | ✓ | SKIP | REVIEW |
| deer-workflow | framework | | ✓ | discovery-log | SOURCE-ONLY |
| langhost | framework | | ✓ | discovery-log | SOURCE-ONLY |
| LangChain.js | framework | | ✓ | SKIP | REVIEW |
| LangGraph.js | framework | | ✓ | SKIP | REVIEW |
| langchain | framework | | ✓ | SKIP | REVIEW |
| autogen | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| MetaGPT | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| llama_index | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| semantic-kernel | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| smolagents | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| dspy | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| crewAI | framework | | ✓ | SKIP | REVIEW |
| praisonai | framework | | ✓ | SKIP | SOURCE-ONLY |
| KADATH | framework | | ✓ | discovery-log | SOURCE-ONLY |
| vercel-ai | framework | | ✓ | discovery-log | REVIEW |
| antigravity-sdk-python | framework | | ✓ | SKIP | REVIEW |
| pydantic-ai | framework | | ✓ | SKIP | REVIEW |
| voltagent | framework | ✓ | ✓/$ | SKIP | REVIEW |
| agent-kit | framework | ✓ | ✓ | SKIP | REVIEW |
| agno | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| conductor | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| cee | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| inngest | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| cloudflare/agents | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| microsoft/agent-framework | framework | | ✓ | SKIP | REVIEW |
| lobehub | platform | | ✓ | SKIP | REVIEW |
| nanoclaw | platform | | ✓ | SKIP | REVIEW |
| nanobot | harness | ✓ | ✓ | SKIP | REVIEW |
| Hermes Agent | harness | ✓ | ✓ | discovery-log | REVIEW |
| flue | framework | | ✓ | discovery-log | SOURCE-ONLY |
| moltworker | tool | | ✓ | discovery-log | SOURCE-ONLY |
| hermes-webui | platform | | ✓ | discovery-log | SOURCE-ONLY |
| agentgpt | platform | | ✓ | SKIP | SOURCE-ONLY |
| khoj | platform | ✓ | ✓ | SKIP | SOURCE-ONLY |
| mindsdb/minds | platform | ✓ | ✓ | SKIP | SOURCE-ONLY |
| oh-my-claudecode | harness | | ✓ | discovery-log | REVIEW |
| oh-my-agent | harness | | ✓ | discovery-log | SOURCE-ONLY |
| oh-my-openagent | harness | | ✓ | SKIP | REVIEW |
| lazycodex | harness | ✓ | ✓ | discovery-log | REVIEW |
| oh-my-pi | platform | | ✓ | SKIP | REVIEW |
| omp-best-of | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| omnigent | framework | | ✓ | discovery-log | REVIEW |
| opencode | platform | | ✓ | CONDITIONAL | RUN |
| deepseek-harness | harness | | ✓ | discovery-log | SOURCE-ONLY |
| dsh-ios | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| plandex | platform | ✓ | ✓ | SKIP | REVIEW |
| forgecode | harness | | ✓ | discovery-log | REVIEW |
| opencode-swarm | plugin | | ✓ | discovery-log | REVIEW |
| OpenHands | platform | | ✓ | discovery-log | REVIEW |
| daytona | platform | ✓ | ✓/$ | SKIP | REVIEW |
| agent-sandbox | tool | ✓ | ✓ | discovery-log | REVIEW |
| axern | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| tabby | platform | ✓ | ✓ | discovery-log | REVIEW |
| Archon | platform | ✓ | ✓ | discovery-log | REVIEW |
| sim | platform | ✓ | ✓/$ | SKIP | REVIEW |
| haystack | framework | ✓ | ✓ | SKIP | REVIEW |
| Portkey-gateway | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| OmniRoute | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| baml | framework | ✓ | ✓ | SKIP | REVIEW |
| moai-adk | plugin | ✓ | ✓ | discovery-log | REVIEW |
| TanStack-cli | tool | ✓ | ✓ | discovery-log | REVIEW |
| mastra | framework | ✓ | ✓ | SKIP | REVIEW |
| pydantic-deepagents | framework | ✓ | ✓ | SKIP | REVIEW |
| pi-subagents | plugin | ✓ | ✓ | discovery-log | REVIEW |
| CopilotKit | framework | ✓ | ✓ | SKIP | REVIEW |
| tambo | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| agent-native | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| assistant-ui | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| hashbrown | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| OpenGenerativeUI | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| json-render | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| mcp-ui | framework | ✓ | ✓ | SKIP | SOURCE-ONLY |
| agentscope | framework | ✓ | ✓ | SKIP | REVIEW |
| open-multi-agent | framework | ✓ | ✓ | SKIP | REVIEW |
| eino | framework | ✓ | ✓ | SKIP | REVIEW |
| vercel/workflow | framework | ✓ | ✓/$ | SKIP | SOURCE-ONLY |
| proof-of-done-loop | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| maintainer-autopilot | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| packrehearsal | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| osaurus | harness | ✓ | ✓ | discovery-log | REVIEW |
| aichat | harness | ✓ | ✓ | discovery-log | REVIEW |
| aider | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| eve | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Trellis | harness | | ✓ | SKIP | SOURCE-ONLY |
| software-factory-harness | harness | | ✓ | SKIP | SOURCE-ONLY |
| command-code | harness | | ✓ | SKIP | SOURCE-ONLY |
| phi | harness | | ✓ | discovery-log | SOURCE-ONLY |
| pi | harness | | ✓ | discovery-log | SOURCE-ONLY |
| FrontierAgent | harness | | ✓ | discovery-log | SOURCE-ONLY |
| Jixu | harness | | ✓ | discovery-log | SOURCE-ONLY |
| acryl | harness | | ✓ | discovery-log | SOURCE-ONLY |
| LocalAI | platform | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| codex | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| gpt-engineer | harness | ✓ | ✓ | SKIP | SOURCE-ONLY |
| SWE-agent | harness | ✓ | ✓ | SKIP | SOURCE-ONLY |
| continue | harness | ✓ | ✓ | SKIP | SOURCE-ONLY |
| cline | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Roo-Code | harness | ✓ | ✓ | SKIP | SOURCE-ONLY |
| void | harness | ✓ | ✓ | SKIP | SOURCE-ONLY |
| GenericAgent | harness | ✓ | ✓ | discovery-log | REVIEW |
| gptme | harness | ✓ | ✓ | discovery-log | REVIEW |
| zeroshot | harness | ✓ | ✓ | discovery-log | REVIEW |
| ccs | tool | ✓ | ✓ | discovery-log | REVIEW |
| mito | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| freestyle | tool | | ✓ | discovery-log | REVIEW |
| beta9 | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| cua | harness | ✓ | ✓/$ | discovery-log | REVIEW |
| txtai | framework | ✓ | ✓ | SKIP | REVIEW |
| UI-TARS-desktop | harness | ✓ | ✓ | discovery-log | REVIEW |
| LongHorizon-Harness | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| opensquilla | tool | | ✓ | SKIP | REVIEW |
| architect-loop | skill |  | ✓ | CONDITIONAL | REVIEW |
| adhd | skill |  | ✓ | CONDITIONAL | REVIEW |
| sandboxd | tool | | ✓ | discovery-log | REVIEW |
| vercel-sandbox | platform | | ✓/$ | discovery-log | REVIEW |
| qwen-code | platform | | ✓ | discovery-log | REVIEW |
| gemini-cli | platform | | ✓ | discovery-log | REVIEW |
| agents-cli | skill | | ✓ | discovery-log | REVIEW |
| ralph-claude-code | harness | ✓ | ✓ | discovery-log | REVIEW |
| ralph | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| rtk | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| ruflo | harness | | ✓ | discovery-log | REVIEW |
| sandcastle | framework | | ✓ | discovery-log | REVIEW |
| superpowers | plugin | | ✓ | ADOPT | SOURCE-ONLY |
| orchestkit | plugin | ✓ | ✓ | SKIP | SOURCE-ONLY |
| eca | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| letta-code | harness | ✓ | ✓ | discovery-log | REVIEW |
| strands-agents (harness-sdk) | framework | ✓ | ✓ | discovery-log | REVIEW |
| Aegis | skill | | ✓ | SKIP | REVIEW |
| superset | tool | | ✓ | SKIP | REVIEW |
| implement | skill | | ✓ | SKIP | REVIEW |
| resolving-merge-conflicts | skill | | ✓ | ADOPT | MEASURED |
| codex-plugin-cc | plugin | | ✓ | discovery-log | REVIEW |
| agy-staff | plugin | | ✓ | discovery-log | SOURCE-ONLY |
| agents-council | plugin | | ✓ | SKIP | SOURCE-ONLY |
| vibecode-pro-max-kit | harness | | ✓ | SKIP | REVIEW |
| re_gent | tool | | ✓ | discovery-log | REVIEW |
| h5i | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| cli-continues | tool | | ✓ | discovery-log | REVIEW |
| export-md | tool | | ✓ | discovery-log | SOURCE-ONLY |
| weave | tool | ✓ | ✓ | discovery-log | REVIEW |
| moire | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| airship | tool | | ✓ | discovery-log | SOURCE-ONLY |
| trace-file-lineage | tool | | ✓ | discovery-log | SOURCE-ONLY |
| phantom | platform | ✓ | ✓ | discovery-log | REVIEW |
| rmux | tool | | ✓ | discovery-log | REVIEW |
| MiMo-Code | platform | | ✓ | discovery-log | REVIEW |
| kimi-code | platform | | ✓ | discovery-log | REVIEW |
| gentle-ai | harness | ✓ | ✓ | discovery-log | REVIEW |
| smallcode | tool | | ✓ | discovery-log | REVIEW |
| clawcodex | harness | | ✓ | discovery-log | REVIEW |
| claudian | plugin | | ✓ | discovery-log | REVIEW |
| jetbrains-cc-gui | plugin | | ✓ | discovery-log | REVIEW |
| babysitter | harness | ✓ | ✓ | SKIP | SOURCE-ONLY |

## Verify

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| agent-browser | tool | | ✓ | CONDITIONAL | RUN |
| moli | tool | | ✓ | discovery-log | SOURCE-ONLY |
| codex-proofloop | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| codex-guard | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| web-quality-skills | skill | | ✓ | ADOPT | MEASURED |
| opencli | tool | | ✓ | discovery-log | SOURCE-ONLY |
| browser-use | framework | | ✓ | discovery-log | REVIEW |
| nanobrowser | tool | | ✓ | SKIP | REVIEW |
| page-agent | tool | ✓ | ✓ | SKIP | REVIEW |
| CloakBrowser | tool | | ✓ | SKIP | REVIEW |
| chrome-devtools-mcp | MCP server | | ✓ | CONDITIONAL | MEASURED |
| scenario | framework | ✓ | ✓ | discovery-log | REVIEW |
| assay | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| aimock | tool | ✓ | ✓ | discovery-log | REVIEW |
| keploy | tool | ✓ | ✓ | discovery-log | REVIEW |
| agentic-playwright | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| midscene | tool | ✓ | ✓ | discovery-log | REVIEW |
| SceneProof | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| evalview | MCP server | ✓ | ✓ | SKIP | REVIEW |
| playwright | MCP server | | ✓ | ADOPT | RUN |
| behalf-chrome-agent | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| playwright-skill | skill | | ✓ | SKIP | REVIEW |
| stryker-js | tool | ✓ | ✓ | CONDITIONAL | RUN |
| testseal | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| frama-c-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| qodo-cover | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| passmark | tool | ✓ | ✓ | SKIP | REVIEW |
| diagnosing-bugs | skill | | ✓ | SKIP | REVIEW |
| mirrord | tool | | ✓/$ | discovery-log | REVIEW |
| browser-act/skills | skill | ✓ | ✓ | SKIP | SOURCE-ONLY |

## Review

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| agentlint | tool | ✓ | ✓ | CONDITIONAL | RUN |
| numbat | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| old-coder | skill | | ✓ | SKIP | SOURCE-ONLY |
| hubo | skill | | ✓ | SKIP | SOURCE-ONLY |
| review-skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| Assumptions | skill | | ✓ | discovery-log | SOURCE-ONLY |
| pr-lens | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| deslop-GPT | skill | | ✓ | discovery-log | SOURCE-ONLY |
| rubber-duck | skill | | ✓ | discovery-log | SOURCE-ONLY |
| forward-implementation-first | skill | | ✓ | discovery-log | SOURCE-ONLY |
| anti-slop | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| anti-slop (oxlint) | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| nopus | tool | | ✓ | discovery-log | SOURCE-ONLY |
| procoder | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| juror | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| oss-pr-reviewer | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| herdr-hunk-diff | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| kodus-ai | platform | ✓ | ✓/$ | SKIP | REVIEW |
| skylos | tool | ✓ | ✓ | CONDITIONAL | RUN |
| simplify-codebase | skill | | ✓ | discovery-log | SOURCE-ONLY |
| gospect-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| code-review | plugin | ✓ | ✓ | KEEP | MEASURED |
| design-council | plugin | | ✓ | discovery-log | REVIEW |
| ghostsecurity/skills | skill | | ✓ | discovery-log | REVIEW |
| vuln-report-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| cdmx-in/security-review | skill | | ✓ | discovery-log | SOURCE-ONLY |
| patchbot | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Quant-Off/skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| PR-Agent | tool | ✓ | ✓ | SKIP | REVIEW |
| open-code-review | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| claude-octopus | plugin | ✓ | ✓/$ | discovery-log | REVIEW |
| crucible | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| tdd-guard | plugin | ✓ | ✓ | CONDITIONAL | RUN |
| ratchet | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| cyclomatic-complexity-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| pristine-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| HERO-Anti-OverDefense | skill | | ✓ | discovery-log | SOURCE-ONLY |
| stop-that-shit | skill | | ✓ | discovery-log | SOURCE-ONLY |
| unlazy | skill | | ✓ | discovery-log | SOURCE-ONLY |
| sloptrim | tool | | ✓ | discovery-log | SOURCE-ONLY |
| shut-up-and-code | skill | | ✓ | discovery-log | SOURCE-ONLY |
| slopware-skills | skill | | ✓ | SKIP | SOURCE-ONLY |
| vet | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| prove-it | skill | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| godkiller-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| AgentSeed | skill | | ✓ | discovery-log | SOURCE-ONLY |
| openrewrite | framework | ✓ | ✓/$ | discovery-log | REVIEW |
| cc-safety-net | tool | ✓ | ✓ | discovery-log | REVIEW |
| secretguard-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| toolpermit | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| pentest-ai-agents | skill | | ✓ | SKIP | REVIEW |
| claude-red | skill | | ✓ | SKIP | SOURCE-ONLY |
| Claude-AD | skill | | ✓ | discovery-log | SOURCE-ONLY |
| pr-review-toolkit | plugin | | ✓ | KEEP | MEASURED |
| security-guidance | plugin | | ✓ | ADOPT | MEASURED |
| shadcn/improve | tool | | ✓ | discovery-log | REVIEW |
| SkillSpector | tool | | ✓ | CONDITIONAL | MEASURED |
| skill-scanner | tool | | ✓ | discovery-log | SOURCE-ONLY |
| skilldoctor | tool | | ✓ | discovery-log | SOURCE-ONLY |
| skill-safety-checker | plugin | | ✓ | SKIP | SOURCE-ONLY |
| trailofbits/skills | skill | | ✓ | SKIP | REVIEW |
| cve-mcp-server | MCP server | ✓ | ✓ | SKIP | REVIEW |
| ida-pro-mcp | MCP server | ✓ | ✓ | SKIP | REVIEW |
| x64dbg-mcp-server | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| ida-headless-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| pentest-ai | MCP server | ✓ | ✓ | SKIP | REVIEW |
| strix | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Claude-BugHunter | skill | | ✓ | SKIP | REVIEW |
| hol-guard | tool | ✓ | ✓ | SKIP | REVIEW |
| OpenOSINT | MCP server | ✓ | ✓ | SKIP | REVIEW |
| agnix | tool | ✓ | ✓ | discovery-log | REVIEW |
| trustmcp | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| agent-vault | tool | | ✓ | discovery-log | REVIEW |
| envlatch | tool | | ✓ | discovery-log | SOURCE-ONLY |
| kru | MCP server | | ✓ | discovery-log | SOURCE-ONLY |
| brooks-lint | skill | | ✓ | CONDITIONAL | MEASURED |
| mkanat/skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| spotpatch | tool | | ✓ | discovery-log | SOURCE-ONLY |
| 1c-quality-gate | plugin | ✓ | ✓ | SKIP | SOURCE-ONLY |
| ship-it | skill | | ✓ | discovery-log | SOURCE-ONLY |
| openreview | tool | ✓ | ✓ | SKIP | REVIEW |
| code-on-incus | tool | ✓ | ✓ | discovery-log | REVIEW |
| ctf-skills | skill | | ✓ | SKIP | SOURCE-ONLY |

## Ship

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| bernstein | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-action | tool | ✓ | ✓ | ADOPT | RUN |
| worktrunk | tool | | $ | discovery-log | REVIEW |

## Reflect

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| claude-reflect | plugin | | ✓ | KEEP | MEASURED |
| awesome-copilot | skill | | ✓ | discovery-log | SOURCE-ONLY |
| documentation-writer | skill | | ✓ | ADOPT | MEASURED |
| documentation-and-adrs | skill | | ✓ | ADOPT | MEASURED |
| iso-24495-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| writing-skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| documentation (anthropics) | skill | | ✓ | discovery-log | REVIEW |
| oo-component-documentation | skill | | ✓ | SKIP | REVIEW |

## Outer Loop

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| ACMM | framework | | ✓ | discovery-log | REVIEW |
| abtop | tool | | ✓ | CONDITIONAL | MEASURED |
| hud-mode | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| rimz | tool | | ✓ | discovery-log | SOURCE-ONLY |
| dev3000 | tool | | ✓ | discovery-log | SOURCE-ONLY |
| debroid | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| roundtable | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| zoetrope | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| agenttrail | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| csift | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Apache DevLake | platform | ✓ | ✓ | DEFER | REVIEW |
| agentacct | tool | | ✓ | discovery-log | SOURCE-ONLY |
| Composio | plugin | | ✓/$ | discovery-log | SOURCE-ONLY |
| Infracost | tool | ✓ | ✓/$ | SKIP | SOURCE-ONLY |
| langfuse | platform | | ✓ | discovery-log | SOURCE-ONLY |
| ccusage | tool | | ✓ | ADOPT | MEASURED |
| token-step-tracker | tool | | ✓ | SKIP | SOURCE-ONLY |
| tokentab | tool | | ✓ | discovery-log | SOURCE-ONLY |
| opencode-cache-stats | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| peek | tool | | ✓ | discovery-log | SOURCE-ONLY |
| bar-observatory | tool | | ✓ | discovery-log | SOURCE-ONLY |
| claude-monitor | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| claude-statusline-burnrate | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| brink | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| vibe-log-cli | tool | | ✓ | SKIP | SOURCE-ONLY |
| agenta | platform | | ✓ | discovery-log | SOURCE-ONLY |
| codeburn | tool | | ✓ | ADOPT | MEASURED |
| trigger.dev | platform | | ✓ | SKIP | REVIEW |
| scorecard | tool | ✓ | ✓ | discovery-log | REVIEW |
| sentrux | tool | ✓ | ✓ | discovery-log | REVIEW |
| claude-fleet | tool | | ✓ | SKIP | REVIEW |
| agentsview | tool | ✓ | ✓ | discovery-log | REVIEW |
| promptfoo | tool | ✓ | ✓ | CONDITIONAL | RUN |
| garak | tool | ✓ | ✓ | discovery-log | REVIEW |
| presidio | tool | ✓ | ✓ | discovery-log | REVIEW |
| NeMo-Guardrails | tool | ✓ | ✓ | discovery-log | REVIEW |
| superagent | tool | ✓ | ✓ | discovery-log | REVIEW |
| deepeval | framework | ✓ | ✓ | discovery-log | REVIEW |
| phoenix | platform | ✓ | ✓/$ | SKIP | REVIEW |
| openinference | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| claude-devtools | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| harbor | framework | ✓ | ✓ | discovery-log | REVIEW |
| claude-code-hooks-multi-agent-observability | tool | ✓ | ✓ | SKIP | REVIEW |
| multi-agent-workflow-lab | tool | | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-agent-monitor | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| rogue | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| giskard-oss | tool | ✓ | ✓ | discovery-log | REVIEW |
| opik | platform | ✓ | ✓ | discovery-log | REVIEW |
| agent-governance-toolkit | framework | ✓ | ✓ | discovery-log | REVIEW |
| decern | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| halofy | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| agent-safe-pipeline | framework | | ✓ | discovery-log | SOURCE-ONLY |
| pezzo | platform | ✓ | ✓ | SKIP | REVIEW |
| ragas | tool | ✓ | ✓ | discovery-log | REVIEW |
| Helicone | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| logfire | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| textgrad | framework | ✓ | ✓ | SKIP | REVIEW |
| ping-island | tool | ✓ | ✓ | SKIP | REVIEW |
| claude-nanny | plugin | ✓ | ✓ | SKIP | SOURCE-ONLY |
| ai-pulse | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| subagent-context | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| tokencost | tool | | ✓ | CONDITIONAL | RUN |

## Skills & Plugins (domain-specific)

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| academic-research-skills | skill | | ✓ | discovery-log | REVIEW |
| ponytail-improved | skill | | ✓ | SKIP | SOURCE-ONLY |
| impeccable-lite | skill | | ✓ | SKIP | SOURCE-ONLY |
| agent-rules-books | skill |  | ✓ | CONDITIONAL | REVIEW |
| doctrine | plugin | | ✓ | discovery-log | SOURCE-ONLY |
| vercel-labs/agent-skills | skill | | ✓ | discovery-log | REVIEW |
| agent-skills | skill | | ✓ | ADOPT | REVIEW |
| coleam00/skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| godmode | skill | | ✓ | discovery-log | SOURCE-ONLY |
| skills-constitution | tool | | ✓ | discovery-log | SOURCE-ONLY |
| autoprompt-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| AI-Research-SKILLs | skill | | ✓ | discovery-log | REVIEW |
| alirezarezvani/claude-skills | plugin | | ✓ | SKIP | REVIEW |
| andrej-karpathy-skills | skill | | ✓ | discovery-log | REVIEW |
| Anthropic-Cybersecurity-Skills | skill | | ✓ | SKIP | REVIEW |
| anthropics/skills | reference | | ✓ | discovery-log | REVIEW |
| antfu/skills | skill | | ✓ | SKIP | REVIEW |
| azure-skills | plugin | | ✓ | discovery-log | REVIEW |
| book-to-skill | skill | | ✓ | discovery-log | REVIEW |
| Claude-Code-Game-Studios | plugin | | ✓ | discovery-log | REVIEW |
| claude-seo | skill | | ✓ | discovery-log | REVIEW |
| excalidraw-diagram-skill | skill | | ✓ | SKIP | REVIEW |
| architecture-drawer | skill | | ✓ | discovery-log | SOURCE-ONLY |
| formkit | framework | | ✓ | SKIP | REVIEW |
| frontend-slides | skill | | ✓ | discovery-log | REVIEW |
| pitch-deck | skill | | ✓ | SKIP | REVIEW |
| powerpoint-ppt | skill | | ✓ | SKIP | REVIEW |
| getsentry/skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| presentation-creator | skill | | ✓ | discovery-log | SOURCE-ONLY |
| lark-slides | skill | | ✓ | discovery-log | SOURCE-ONLY |
| giving-presentations | skill | | ✓ | SKIP | SOURCE-ONLY |
| garden-skills | skill | | ✓ | discovery-log | REVIEW |
| gemini-skills | skill | | ✓ | discovery-log | REVIEW |
| google/skills | skill | | ✓ | discovery-log | REVIEW |
| terraform-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| googleworkspace/cli | tool | | ✓ | SKIP | REVIEW |
| guizang-ppt-skill | skill | | ✓ | SKIP | REVIEW |
| html-anything | tool | | ✓ | SKIP | REVIEW |
| humanizer | skill | | ✓ | discovery-log | REVIEW |
| impeccable | skill | | ✓ | discovery-log | REVIEW |
| frontend-design | plugin | | ✓ | SKIP | SOURCE-ONLY |
| Jeffallan/claude-skills | skill | | ✓ | discovery-log | REVIEW |
| marketingskills | skill | | ✓ | discovery-log | REVIEW |
| mattpocock/skills | skill | | ✓ | ADOPT | MEASURED |
| pm-claude-skills | skill | | ✓ | SKIP | SOURCE-ONLY |
| thinking-claude | framework | | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-infrastructure-showcase | reference | | ✓ | SKIP | SOURCE-ONLY |
| microsoft/skills | skill | | ✓ | discovery-log | REVIEW |
| obsidian-skills | skill | | ✓ | discovery-log | REVIEW |
| open-design | platform | | ✓ | SKIP | REVIEW |
| open-slide | tool | | ✓ | discovery-log | REVIEW |
| slidev | skill | | ✓ | discovery-log | REVIEW |
| powerpoint | skill | | ✓ | SKIP | REVIEW |
| openskills | tool | | ✓ | discovery-log | REVIEW |
| vercel-labs/skills | tool | | ✓ | discovery-log | REVIEW |
| plugin-dev | plugin | | ✓ | SKIP | REVIEW |
| pm-skills | skill | | ✓ | discovery-log | REVIEW |
| ponytail | skill | | ✓ | discovery-log | REVIEW |
| refly | platform | | ✓ | SKIP | REVIEW |
| scientific-agent-skills | skill | | ✓ | discovery-log | REVIEW |
| skill-creator | plugin | | ✓ | ADOPT | MEASURED |
| oil-skill-creator | tool | | ✓ | SKIP | SOURCE-ONLY |
| repo2skill | tool | | ✓ | SKIP | SOURCE-ONLY |
| biks-claude-loader-update | tool | | ✓ | SKIP | SOURCE-ONLY |
| Skill_Seekers | tool | | ✓ | discovery-log | REVIEW |
| skill-recorder | tool | | ✓ | discovery-log | SOURCE-ONLY |
| video-to-skill | tool | | ✓ | SKIP | SOURCE-ONLY |
| SkillOpt | framework | | ✓ | DEFER | REVIEW |
| stop-slop | skill | | ✓ | discovery-log | REVIEW |
| taste-skill | skill | | ✓ | discovery-log | REVIEW |
| agent-vision-toolkit | skill | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| dsh-vision-toolkit | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| dsh-find-plugins | skill | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| xcode-skills | plugin | | ✓ | SKIP | SOURCE-ONLY |
| tech-leads-club/agent-skills | skill | | ✓ | discovery-log | REVIEW |
| softaworks/agent-toolkit | skill | | ✓ | discovery-log | SOURCE-ONLY |
| NVIDIA/skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| loopy | skill | | ✓ | discovery-log | SOURCE-ONLY |
| company-os-starter-kit | plugin | | ✓ | SKIP | SOURCE-ONLY |
| council-of-high-intelligence | tool | | ✓ | discovery-log | SOURCE-ONLY |
| typescript-mcp-server-generator | skill | | ✓ | discovery-log | REVIEW |
| attention-control | skill | | ✓ | discovery-log | SOURCE-ONLY |
| open-steps | skill | | ✓ | discovery-log | SOURCE-ONLY |
| ui-ux-pro-max | skill | | ✓ | discovery-log | REVIEW |
| scroll-craft | skill | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| oa-design | skill | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Waza | skill | | ✓ | SKIP | REVIEW |
| agents (wshobson) | plugin | | ✓ | discovery-log | REVIEW |
| agent-sprite-forge | skill | | ✓ | SKIP | REVIEW |
| SwiftUI-Agent-Skill | skill | | ✓ | discovery-log | REVIEW |
| guard-skills | skill | | ✓ | discovery-log | REVIEW |
| claude-night-market | plugin | | ✓ | discovery-log | REVIEW |
| huashu-design | skill | | ✓ | discovery-log | REVIEW |
| baoyu-design | skill | | ✓ | discovery-log | REVIEW |
| AlphaGBM/skills | skill | | ✓ | SKIP | REVIEW |
| himself65/finance-skills | skill | | ✓ | discovery-log | REVIEW |
| web-access | skill | ✓ | ✓ | discovery-log | REVIEW |
| cc-skills-golang | skill | | ✓ | ADOPT | REVIEW |
| waza (Microsoft) | tool | ✓ | ✓ | discovery-log | REVIEW |
| skills-hub | tool | | ✓ | discovery-log | REVIEW |
| claude-code-plugins-plus-skills | tool | | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-hooks (karanb192) | plugin | | ✓ | discovery-log | SOURCE-ONLY |
| context-engineering-kit | plugin | ✓ | ✓ | SKIP | REVIEW |
| baoyu-skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| Generative-Media-Skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| agent-skill-creator | skill | | ✓ | SKIP | SOURCE-ONLY |
| wondelai/skills | skill | | ✓ | SKIP | SOURCE-ONLY |
| awesome-design-skills | reference | | ✓ | discovery-log | SOURCE-ONLY |

## Memory & Context

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| agentmemory | tool | | ✓ | discovery-log | REVIEW |
| open-index | tool | | ✓ | discovery-log | SOURCE-ONLY |
| kaas | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| PageIndex | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| Acontext | tool | ✓ | ✓ | discovery-log | REVIEW |
| byterover-cli | tool | ✓ | ✓/$ | SKIP | REVIEW |
| LightRAG | tool | ✓ | ✓ | discovery-log | REVIEW |
| memvid | tool | ✓ | ✓ | discovery-log | REVIEW |
| kreuzberg | tool | ✓ | ✓ | discovery-log | REVIEW |
| MineContext | platform | ✓ | ✓ | SKIP | REVIEW |
| obsidian-second-brain | skill | ✓ | ✓ | discovery-log | REVIEW |
| hoist-the-elephant | skill | | ✓ | discovery-log | SOURCE-ONLY |
| claude-mem | plugin | ✓ | ✓ | ADOPT | MEASURED |
| ownmem | tool | | ✓ | discovery-log | SOURCE-ONLY |
| claude-db | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| Perenna | MCP server | | ✓ | SKIP | SOURCE-ONLY |
| memorax-code | plugin | ✓ | ✓ | SKIP | SOURCE-ONLY |
| lean-ctx | tool |  | ✓ | CONDITIONAL | REVIEW |
| heimdall | tool | | ✓ | discovery-log | SOURCE-ONLY |
| letta | platform | | ✓ | DEFER | REVIEW |
| claude-subconscious | plugin | ✓ | ✓ | SKIP | REVIEW |
| cognee | platform | | ✓ | discovery-log | REVIEW |
| MemOS | platform | | ✓ | discovery-log | REVIEW |
| memind | platform | ✓ | ✓ | SKIP | REVIEW |
| ACE (agentic-context-engine) | framework | ✓ | ✓ | discovery-log | REVIEW |
| Recuris | framework | | ✓ | discovery-log | SOURCE-ONLY |
| wikiskill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| claw-compactor | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| evolver | tool | ✓ | ✓ | SKIP | REVIEW |
| memU | platform | ✓ | ✓ | discovery-log | REVIEW |
| memory-os | tool | ✓ | ✓ | SKIP | REVIEW |
| pieces-to-agents | tool | | ✓ | discovery-log | SOURCE-ONLY |
| wife | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Memori | platform | | ✓ | discovery-log | REVIEW |
| OpenViking | platform | | ✓ | SKIP | REVIEW |
| RAGFlow | platform | ✓ | ✓ | SKIP | REVIEW |
| engram | tool | | ✓ | discovery-log | REVIEW |
| ballast | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| mem0 | MCP server | | ✓ | discovery-log | REVIEW |
| memoket-kite | tool | | ✓ | discovery-log | SOURCE-ONLY |
| hypotree | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| OMEGA | MCP server | ✓ | ✓/$ | KEEP | REVIEW |
| staffetta | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| server-memory | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| SimpleMem | tool | | ✓ | discovery-log | REVIEW |
| squish-memory | MCP server | | ✓ | SKIP | REVIEW |
| longhand | MCP server | | ✓ | discovery-log | REVIEW |
| storybloq | plugin | ✓ | ✓ | SKIP | REVIEW |
| handoff-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| portable-handoff | tool | | ✓ | discovery-log | SOURCE-ONLY |
| jiaojie-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-memory-setup | reference | | ✓ | discovery-log | REVIEW |
| claude-obsidian | plugin | ✓ | ✓ | discovery-log | REVIEW |
| ArcRift | tool | | ✓ | discovery-log | REVIEW |
| context-infrastructure | reference | | ✓ | SKIP | REVIEW |
| agentic-stack | tool | | ✓ | discovery-log | REVIEW |
| guild | tool | | ✓ | discovery-log | REVIEW |
| memsearch | tool | ✓ | ✓ | discovery-log | REVIEW |
| supermemory | platform | ✓ | ✓ | discovery-log | REVIEW |
| honcho | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| MemPalace | tool | ✓ | ✓ | discovery-log | REVIEW |
| pro-workflow | plugin | ✓ | ✓ | SKIP | REVIEW |
| hivemind | tool | ✓ | ✓ | SKIP | REVIEW |
| AgentRecall-MCP | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| getspecstory | tool | ✓ | ✓ | SKIP | SOURCE-ONLY |
| mex | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| opencontext | MCP server | | ✓ | SKIP | SOURCE-ONLY |

## MCP Servers (infrastructure)

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| awslabs/mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| nuphus-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| mcp-remote | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| blender-mcp | MCP server | ✓ | ✓ | SKIP | REVIEW |
| unity-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| codebase-memory-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| fastapi_mcp | framework | | ✓ | discovery-log | REVIEW |
| mcp-use | framework | | ✓ | discovery-log | REVIEW |
| cloudflare-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| agent-toolkit-for-aws | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| confluence | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| pi-delegate-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| devfleet | MCP server | ✓ | ✓ | SKIP | REVIEW |
| exa-mcp-server | MCP server | ✓ | ✓/$ | discovery-log | REVIEW |
| mcp-github-trending | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| fal-ai-mcp-server | MCP server | ✓ | ✓/$ | SKIP | REVIEW |
| hyperframes | MCP server | ✓ | ✓ | SKIP | SOURCE-ONLY |
| fastmcp | framework | | ✓ | ADOPT | RUN |
| Figma-Context-MCP | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| firecrawl-mcp | MCP server | ✓ | ✓/$ | discovery-log | REVIEW |
| github-mcp-server | MCP server | ✓ | ✓ | ADOPT | MEASURED |
| mcp-atlassian | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| jira | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| mcp-toolbox | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| prisma | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| llm-safe-sql | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| modelcontextprotocol/servers | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| sequential-thinking | MCP server | ✓ | ✓ | SKIP | REVIEW |
| sentry | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| server-filesystem | MCP server | ✓ | ✓ | SKIP | REVIEW |
| server-github | MCP server | ✓ | ✓ | SKIP | REVIEW |
| supabase | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| token-optimizer-mcp | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| opendocswork-mcp | MCP server | ✓ | ✓ | SKIP | REVIEW |
| plumb-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| figma-mcp-go | MCP server | ✓ | ✓ | SKIP | REVIEW |
| design-extract | MCP server | | ✓ | CONDITIONAL | REVIEW |
| pg-aiguide | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| mcp2cli | tool | ✓ | ✓ | discovery-log | REVIEW |
| mirage | tool | | ✓ | discovery-log | REVIEW |
| Pare | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| warden | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| ref-tools-mcp | MCP server | ✓ | ✓/$ | SKIP | REVIEW |
| Mintlify Index | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| exeora | MCP server | ✓ | ✓ | SKIP | SOURCE-ONLY |
| DesktopCommanderMCP | MCP server | ✓ | ✓ | SKIP | REVIEW |
| mac-developer-bridge | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| DebugMCP | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| google-workspace-mcp | MCP server | ✓ | ✓ | SKIP | REVIEW |
| mcp-context-forge | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| gh-aw-mcpg | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| mcp-migrate | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| mcp-vision-bridge | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |

## Research & Discovery

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| Agent-Reach | tool | | ✓ | SKIP | REVIEW |
| net-deep-research | skill | | ✓ | discovery-log | SOURCE-ONLY |
| poirot | tool | | ✓ | discovery-log | SOURCE-ONLY |
| AutoResearchClaw | harness | ✓ | ✓ | discovery-log | REVIEW |
| aisuite | framework | | ✓ | SKIP | REVIEW |
| webclaw | tool | | ✓ | SKIP | REVIEW |
| firecrawl | tool | | ✓/$ | discovery-log | SOURCE-ONLY |
| oc | tool | | ✓ | discovery-log | SOURCE-ONLY |
| autoresearch | tool | ✓ | ✓ | SKIP | REVIEW |
| ARIS | skill | ✓ | ✓ | discovery-log | REVIEW |
| last30days-skill | skill | | ✓ | ADOPT | MEASURED |
| llm-council | tool | | ✓ | SKIP | REVIEW |
| PaperOrchestra | skill | | ✓ | SKIP | REVIEW |
| storm | tool | ✓ | ✓ | discovery-log | REVIEW |
| AutoSci | harness | ✓ | ✓ | discovery-log | REVIEW |
| notebooklm-py | tool | ✓ | ✓ | discovery-log | REVIEW |
| evo | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| EvoTrace | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| awesome-llm-apps | reference | | ✓ | discovery-log | SOURCE-ONLY |
| Awesome-LLMOps (InftyAI) | reference | | ✓ | SKIP | SOURCE-ONLY |
| Awesome-LLMOps (tensorchord) | reference | | ✓ | discovery-log | SOURCE-ONLY |
| Deep-Research-skills | skill | | ✓ | discovery-log | SOURCE-ONLY |

## Reference

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| antigravity-awesome-skills | reference | | ✓ | discovery-log | REVIEW |
| awesome-agent-skills | reference | | ✓ | discovery-log | REVIEW |
| awesome-agent-skills (libukai) | reference | | ✓ | discovery-log | REVIEW |
| awesome-ai-agents | reference | | ✓ | SKIP | REVIEW |
| awesome-claude-code | reference | | ✓ | CONDITIONAL | RUN |
| awesome-claude-code-subagents | reference | | ✓ | discovery-log | REVIEW |
| ai-agents-for-beginners | reference | | ✓ | discovery-log | REVIEW |
| mcp-for-beginners | reference | | ✓ | ADOPT | REVIEW |
| genai-agents | reference | | ✓ | discovery-log | REVIEW |
| agents-towards-production | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-claude-skills (Composio) | reference | | ✓ | discovery-log | REVIEW |
| awesome-claude-skills (behisecc) | reference | | ✓ | SKIP | SOURCE-ONLY |
| awesome-claude-skills (travisvn) | reference | | ✓ | SKIP | REVIEW |
| claude-cookbooks | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-codex-skills | reference | | ✓ | discovery-log | REVIEW |
| awesome-llm-agents | reference | | ✓ | SKIP | REVIEW |
| awesome-hermes-agent | reference | | ✓ | SKIP | SOURCE-ONLY |
| awesome-ai-tools-for-ui | reference | | ✓ | SKIP | SOURCE-ONLY |
| awesome-openclaw-skills | reference | | ✓ | discovery-log | REVIEW |
| ai-engineering-from-scratch | reference | | ✓ | discovery-log | REVIEW |
| pi-from-scratch | reference | | ✓ | discovery-log | SOURCE-ONLY |
| claude-code | reference | | ✓ | discovery-log | REVIEW |
| claude-code-best-practice | reference | | ✓ | discovery-log | REVIEW |
| claude-code-system-prompts | reference | | ✓ | discovery-log | REVIEW |
| claude-code-tips | reference | | ✓ | SKIP | REVIEW |
| claude-howto | reference | | ✓ | discovery-log | REVIEW |
| Awesome-finance-skills | skill | | ✓ | SKIP | REVIEW |
| claude-plugins-official | reference | | ✓ | KEEP | REVIEW |
| dictionary-of-ai-coding | reference | | ✓ | ADOPT | REVIEW |
| Fabric | framework | | ✓ | SKIP | REVIEW |
| learn-claude-code | reference | | ✓ | discovery-log | REVIEW |
| awesome-harness-engineering | reference | | ✓ | discovery-log | SOURCE-ONLY |
| learn-harness-engineering | reference | | ✓ | discovery-log | SOURCE-ONLY |
| system-prompts-and-models | reference | | ✓ | discovery-log | REVIEW |
| CL4R1T4S | reference | | ✓ | SKIP | SOURCE-ONLY |
| tolaria | tool | | ✓ | SKIP | REVIEW |
| docmd | tool | | ✓ | discovery-log | REVIEW |
| agentskills | reference | | ✓ | ADOPT | REVIEW |
| agents-best-practices | skill | | ✓ | discovery-log | REVIEW |
| buildwithclaude | reference | | ✓ | discovery-log | REVIEW |
| agent-skills-collection | reference | | ✓ | SKIP | SOURCE-ONLY |
| awesome-mcp-servers | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-deepseek-harness | reference | | ✓ | discovery-log | SOURCE-ONLY |
| karpathy-llm-wiki | skill | | ✓ | discovery-log | REVIEW |
| ctx | tool | | ✓ | discovery-log | REVIEW |
| system-prompts-leaks | reference | | ✓ | discovery-log | REVIEW |
| how-claude-code-works | reference | | ✓ | discovery-log | REVIEW |
| claude-code-ultimate-guide | reference | | ✓ | discovery-log | REVIEW |
| Prompt-Engineering-Guide | reference | | ✓ | discovery-log | REVIEW |
| 500-AI-Agents-Projects | reference | | ✓ | discovery-log | REVIEW |
| 12-factor-agents | reference | | ✓ | discovery-log | REVIEW |
| ag-ui | reference | | ✓ | discovery-log | REVIEW |
| openui | reference | | ✓ | discovery-log | SOURCE-ONLY |
| a2ui | reference | | ✓ | CONDITIONAL | REVIEW |
| MCP Apps (ext-apps) | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-generative-ai-guide | reference | | ✓ | discovery-log | SOURCE-ONLY |

---

## Legend

| Column | Values |
|--------|--------|
| **Type** | tool, skill, plugin, framework, harness, platform, MCP server, reference |
| **Auto** | ✓ = runs automatically (hooks, CI, background, MCP on-demand); blank = manual invocation |
| **Free** | ✓ = free/open source; $ = paid/proprietary; ✓/$ = freemium or open core |
| **Evaluated** | ADOPT = use in all projects; KEEP = validated, retaining; CONDITIONAL = use when specific conditions met; SKIP = evaluated and rejected; DEFER = promising but blocked, re-evaluate later; blank = not yet evaluated |

## Summary

| Stage | Tools | Validated | Recommended | Validated % |
|-------|-------|-----------|-------------|-------------|
| Plan | 74 | 35 | 6 | 47% |
| Implement | 242 | 116 | 4 | 48% |
| Verify | 30 | 14 | 2 | 47% |
| Review | 83 | 29 | 3 | 35% |
| Ship | 3 | 1 | 1 | 33% |
| Reflect | 8 | 4 | 3 | 50% |
| Outer Loop | 62 | 19 | 2 | 31% |
| Skills & Plugins | 108 | 38 | 4 | 35% |
| Memory & Context | 67 | 24 | 2 | 36% |
| MCP Servers | 53 | 17 | 2 | 32% |
| Research & Discovery | 22 | 8 | 1 | 36% |
| Reference | 56 | 18 | 4 | 32% |
| **Total** | **808** | **323** | **34** | **40%** |
