# Tool Comparison

All 590 tools from CATALOG.md with dev loop stage, automation capability, pricing, and evaluation status at a glance.

**Verdict vocabulary** (per [ADR 0001](docs/decisions/0001-verdict-vocabulary.md), implemented in #69):

- **ADOPT** / **KEEP** — recommended (KEEP = already installed & validated); run-backed or disclaimered.
- **CONDITIONAL** — a real conditional verdict on a tool we actually exercised (`Evidence` MEASURED/RUN), or one carrying a genuine `adopt-if:` condition.
- **SKIP** / **DEFER** — evaluated and not recommended (now), incl. license-disqualified tools.
- **discovery-log** — a catalogued *lead*, not a verdict: surfaced in triage but never exercised (`Evidence` REVIEW/SOURCE-ONLY). The eval's tentative read is notes, not a recommendation. Excluded from verdict-sync (D) and verdict-evidence (K). Promote to a real verdict by exercising the tool.

## Plan

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| CLI-Anything | tool | | ✓ | discovery-log | REVIEW |
| claude-code-templates | tool | | ✓ | SKIP | REVIEW |
| claude-hud | plugin | ✓ | ✓ | discovery-log | REVIEW |
| ccstatusline | plugin | ✓ | ✓ | discovery-log | REVIEW |
| codegraph | tool | ✓ | ✓ | ADOPT | MEASURED |
| code-review-graph | tool | | ✓ | discovery-log | REVIEW |
| context7 | MCP server | ✓ | ✓ | KEEP | RUN |
| feature-dev | plugin | | ✓ | KEEP | MEASURED |
| graphify | skill | | ✓ | CONDITIONAL | MEASURED |
| gentleman-book-mcp | MCP server | ✓ | ✓ | SKIP | REVIEW |
| git-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| GSD (Get Shit Done) | framework | | ✓ | KEEP | MEASURED |
| vibe-coding-prompt-template | skill | | ✓ | discovery-log | SOURCE-ONLY |
| claude-modular | framework | | ✓ | SKIP | REVIEW |
| spec-kit | framework | | ✓ | discovery-log | REVIEW |
| claude-code-spec-workflow | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-my-workflow | tool | | ✓ | discovery-log | SOURCE-ONLY |
| design.md | reference | | ✓ | discovery-log | SOURCE-ONLY |
| ccpm | skill | | ✓ | discovery-log | REVIEW |
| OpenSpec | framework | | ✓ | discovery-log | REVIEW |
| BMAD-METHOD | framework | | ✓ | discovery-log | REVIEW |
| 8090 Software Factory | platform | ✓ | | DEFER | REVIEW |
| software-factory-plugin | plugin | | ✓ | CONDITIONAL | MEASURED |
| spec_driven_develop | skill | | ✓ | discovery-log | REVIEW |
| reversa | framework | ✓ | ✓ | discovery-log | REVIEW |
| flow-next | plugin | ✓ | ✓ | discovery-log | REVIEW |
| mdn/mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| opensrc | tool | | ✓ | discovery-log | REVIEW |
| planning-with-files | skill | | ✓ | SKIP | REVIEW |
| reporails/cli | tool | | $ | discovery-log | SOURCE-ONLY |
| repomix | tool | | ✓ | CONDITIONAL | RUN |
| gitingest | tool | | ✓ | CONDITIONAL | MEASURED |
| repoprompt-ce | tool | | ✓ | discovery-log | SOURCE-ONLY |
| markitdown | tool | | ✓ | ADOPT | MEASURED |
| MinerU | tool | | ✓ | discovery-log | SOURCE-ONLY |
| deepwiki-rs | tool | | ✓ | discovery-log | SOURCE-ONLY |
| serena | MCP server | ✓ | ✓ | ADOPT | MEASURED |
| ts-morph | tool | | ✓ | CONDITIONAL | RUN |
| repowise | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| PocketFlow-Tutorial-Codebase-Knowledge | tool | ✓ | ✓ | discovery-log | REVIEW |
| claude-context | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| cocoindex-code | tool | ✓ | ✓ | discovery-log | REVIEW |
| sem | tool | ✓ | ✓ | discovery-log | REVIEW |
| semble | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| Understand-Anything | tool | | ✓ | discovery-log | REVIEW |
| codebase-design | skill | | ✓ | discovery-log | REVIEW |
| domain-modeling | skill | | ✓ | discovery-log | REVIEW |
| plannotator | tool | | ✓ | discovery-log | REVIEW |
| code-context-engine | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| trace-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| SocratiCode | tool | ✓ | ✓ | discovery-log | REVIEW |
| gortex | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| codebase-to-course | skill | | ✓ | SKIP | REVIEW |
| sourcebot | platform | ✓ | ✓ | discovery-log | REVIEW |

## Implement

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| agency-agents | harness | | ✓ | discovery-log | REVIEW |
| agent-orchestrator | tool | ✓ | ✓ | discovery-log | REVIEW |
| agmsg | tool | ✓ | ✓ | discovery-log | REVIEW |
| aidlc-workflows | framework | | ✓ | discovery-log | REVIEW |
| arrow-js | framework | | ✓ | discovery-log | REVIEW |
| beads | tool | ✓ | ✓ | KEEP | MEASURED |
| caveman | skill | | ✓ | ADOPT | MEASURED |
| cherry-studio | platform | | ✓ | SKIP | REVIEW |
| eigent | platform | ✓ | ✓ | discovery-log | REVIEW |
| herdr | tool | | ✓ | discovery-log | REVIEW |
| claurst | harness | | ✓ | SKIP | REVIEW |
| claude-code-harness | harness | | ✓ | discovery-log | REVIEW |
| claude-code-router | tool | | ✓ | discovery-log | REVIEW |
| CLIProxyAPI | tool | | ✓ | discovery-log | REVIEW |
| litellm | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| bifrost | tool | ✓ | ✓ | discovery-log | REVIEW |
| claude-code-staff-engineer | harness | | ✓ | SKIP | REVIEW |
| claude-squad | tool | | ✓ | CONDITIONAL | RUN |
| vibe-kanban | tool | | ✓ | discovery-log | SOURCE-ONLY |
| orca | platform | ✓ | ✓ | discovery-log | REVIEW |
| HolyClaude | platform | ✓ | ✓ | discovery-log | REVIEW |
| Nimbalyst | platform | | ✓ | discovery-log | REVIEW |
| agent-of-empires | tool | | ✓ | discovery-log | REVIEW |
| AgentsMesh | platform | ✓ | ✓ | SKIP | REVIEW |
| claude-task-master | tool | | ✓ | discovery-log | REVIEW |
| capa | tool | | ✓ | discovery-log | REVIEW |
| skills-manage | tool | | ✓ | SKIP | REVIEW |
| align-dev | tool | | ✓ | SKIP | REVIEW |
| cc-switch | tool | | ✓ | SKIP | REVIEW |
| commit-commands | plugin | | ✓ | SKIP | REVIEW |
| compound-engineering | plugin | | ✓ | discovery-log | REVIEW |
| context-mode | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| Continuous-Claude-v3 | harness | ✓ | ✓ | discovery-log | REVIEW |
| CowAgent | harness | | ✓ | SKIP | REVIEW |
| deer-flow | harness | | ✓ | discovery-log | REVIEW |
| DeepSeek-Reasonix | platform | | ✓ | discovery-log | REVIEW |
| dify | platform | | ✓ | SKIP | REVIEW |
| activepieces | platform | | ✓ | discovery-log | SOURCE-ONLY |
| onyx | platform | | ✓ | discovery-log | SOURCE-ONLY |
| dmux | tool | | ✓ | discovery-log | REVIEW |
| ECC | harness | | ✓ | discovery-log | REVIEW |
| fast-agent | framework | | ✓ | discovery-log | REVIEW |
| Flowise | platform | | ✓ | SKIP | REVIEW |
| langflow | platform | | ✓ | discovery-log | SOURCE-ONLY |
| forkd | tool | | ✓ | discovery-log | REVIEW |
| gastown | tool | | ✓ | discovery-log | REVIEW |
| goose | platform | | ✓ | discovery-log | REVIEW |
| open-interpreter | harness | | ✓ | discovery-log | REVIEW |
| kilocode | platform | | ✓ | discovery-log | REVIEW |
| grok-cli | platform | | ✓ | discovery-log | REVIEW |
| Kaku | tool | | ✓ | discovery-log | REVIEW |
| jcode | harness | | ✓ | discovery-log | REVIEW |
| gstack | harness | | ✓ | discovery-log | REVIEW |
| gbrain | harness | | ✓ | discovery-log | SOURCE-ONLY |
| happy | platform | | $ | discovery-log | REVIEW |
| harness | skill | | ✓ | discovery-log | REVIEW |
| headroom | tool | ✓ | ✓ | CONDITIONAL | MEASURED |
| claude-context-optimizer | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| hive | harness | | ✓ | SKIP | REVIEW |
| humanlayer | harness | | ✓ | SKIP | REVIEW |
| KARIMO | plugin | | ✓ | discovery-log | REVIEW |
| LangGraph | framework | | ✓ | SKIP | REVIEW |
| LangChain.js | framework | | ✓ | SKIP | REVIEW |
| LangGraph.js | framework | | ✓ | SKIP | REVIEW |
| langchain | framework | | ✓ | SKIP | REVIEW |
| autogen | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| MetaGPT | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| llama_index | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| semantic-kernel | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| smolagents | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| dspy | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| crewAI | framework | | ✓ | SKIP | REVIEW |
| praisonai | framework | | ✓ | discovery-log | SOURCE-ONLY |
| vercel-ai | framework | | ✓ | discovery-log | REVIEW |
| antigravity-sdk-python | framework | | ✓ | discovery-log | REVIEW |
| pydantic-ai | framework | | ✓ | discovery-log | REVIEW |
| voltagent | framework | ✓ | ✓/$ | discovery-log | REVIEW |
| agent-kit | framework | ✓ | ✓ | discovery-log | REVIEW |
| agno | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| conductor | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| inngest | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| cloudflare/agents | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| microsoft/agent-framework | framework | | ✓ | discovery-log | REVIEW |
| lobehub | platform | | ✓ | SKIP | REVIEW |
| nanoclaw | platform | | ✓ | SKIP | REVIEW |
| nanobot | harness | ✓ | ✓ | discovery-log | REVIEW |
| Hermes Agent | harness | ✓ | ✓ | discovery-log | REVIEW |
| flue | framework | | ✓ | discovery-log | SOURCE-ONLY |
| moltworker | tool | | ✓ | discovery-log | SOURCE-ONLY |
| hermes-webui | platform | | ✓ | discovery-log | SOURCE-ONLY |
| agentgpt | platform | | ✓ | SKIP | SOURCE-ONLY |
| khoj | platform | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| mindsdb/minds | platform | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| oh-my-claudecode | harness | | ✓ | discovery-log | REVIEW |
| oh-my-agent | harness | | ✓ | discovery-log | SOURCE-ONLY |
| oh-my-openagent | harness | | ✓ | SKIP | REVIEW |
| lazycodex | harness | ✓ | ✓ | discovery-log | REVIEW |
| oh-my-pi | platform | | ✓ | SKIP | REVIEW |
| omnigent | framework | | ✓ | discovery-log | REVIEW |
| opencode | platform | | ✓ | discovery-log | REVIEW |
| plandex | platform | ✓ | ✓ | discovery-log | REVIEW |
| forgecode | harness | | ✓ | discovery-log | REVIEW |
| opencode-swarm | plugin | | ✓ | discovery-log | REVIEW |
| OpenHands | platform | | ✓ | discovery-log | REVIEW |
| daytona | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| agent-sandbox | tool | ✓ | ✓ | discovery-log | REVIEW |
| tabby | platform | ✓ | ✓ | discovery-log | REVIEW |
| Archon | platform | ✓ | ✓ | discovery-log | REVIEW |
| sim | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| haystack | framework | ✓ | ✓ | discovery-log | REVIEW |
| Portkey-gateway | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| OmniRoute | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| baml | framework | ✓ | ✓ | discovery-log | REVIEW |
| moai-adk | plugin | ✓ | ✓ | discovery-log | REVIEW |
| TanStack-cli | tool | ✓ | ✓ | discovery-log | REVIEW |
| mastra | framework | ✓ | ✓ | discovery-log | REVIEW |
| pydantic-deepagents | framework | ✓ | ✓ | discovery-log | REVIEW |
| pi-subagents | plugin | ✓ | ✓ | SKIP | REVIEW |
| CopilotKit | framework | ✓ | ✓ | discovery-log | REVIEW |
| tambo | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| agent-native | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| assistant-ui | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| hashbrown | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| OpenGenerativeUI | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| json-render | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| mcp-ui | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| agentscope | framework | ✓ | ✓ | discovery-log | REVIEW |
| open-multi-agent | framework | ✓ | ✓ | discovery-log | REVIEW |
| eino | framework | ✓ | ✓ | discovery-log | REVIEW |
| vercel/workflow | framework | ✓ | ✓/$ | discovery-log | SOURCE-ONLY |
| osaurus | harness | ✓ | ✓ | discovery-log | REVIEW |
| aichat | harness | ✓ | ✓ | discovery-log | REVIEW |
| aider | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| eve | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Trellis | harness | | ✓ | discovery-log | SOURCE-ONLY |
| software-factory-harness | harness | | ✓ | discovery-log | SOURCE-ONLY |
| command-code | harness | | ✓ | discovery-log | SOURCE-ONLY |
| pi | harness | | ✓ | discovery-log | SOURCE-ONLY |
| LocalAI | platform | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| codex | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| gpt-engineer | harness | ✓ | ✓ | SKIP | SOURCE-ONLY |
| SWE-agent | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| continue | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
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
| txtai | framework | ✓ | ✓ | discovery-log | REVIEW |
| UI-TARS-desktop | harness | ✓ | ✓ | discovery-log | REVIEW |
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
| orchestkit | plugin | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| eca | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| letta-code | harness | ✓ | ✓ | discovery-log | REVIEW |
| strands-agents (harness-sdk) | framework | ✓ | ✓ | discovery-log | REVIEW |
| Aegis | skill | | ✓ | discovery-log | REVIEW |
| superset | tool | | ✓ | discovery-log | REVIEW |
| implement | skill | | ✓ | discovery-log | REVIEW |
| resolving-merge-conflicts | skill | | ✓ | ADOPT | MEASURED |
| codex-plugin-cc | plugin | | ✓ | discovery-log | REVIEW |
| vibecode-pro-max-kit | harness | | ✓ | discovery-log | REVIEW |
| re_gent | tool | | ✓ | discovery-log | REVIEW |
| h5i | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| cli-continues | tool | | ✓ | discovery-log | REVIEW |
| weave | tool | ✓ | ✓ | discovery-log | REVIEW |
| phantom | platform | ✓ | ✓ | discovery-log | REVIEW |
| rmux | tool | | ✓ | discovery-log | REVIEW |
| MiMo-Code | platform | | ✓ | discovery-log | REVIEW |
| kimi-code | platform | | ✓ | discovery-log | REVIEW |
| gentle-ai | harness | ✓ | ✓ | discovery-log | REVIEW |
| smallcode | tool | | ✓ | discovery-log | REVIEW |
| clawcodex | harness | | ✓ | discovery-log | REVIEW |
| claudian | plugin | | ✓ | discovery-log | REVIEW |
| jetbrains-cc-gui | plugin | | ✓ | discovery-log | REVIEW |
| babysitter | harness | ✓ | ✓ | discovery-log | SOURCE-ONLY |

## Verify

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| agent-browser | tool | | ✓ | discovery-log | REVIEW |
| web-quality-skills | skill | | ✓ | ADOPT | MEASURED |
| opencli | tool | | ✓ | discovery-log | SOURCE-ONLY |
| browser-use | framework | | ✓ | discovery-log | REVIEW |
| nanobrowser | tool | | ✓ | discovery-log | REVIEW |
| page-agent | tool | ✓ | ✓ | discovery-log | REVIEW |
| CloakBrowser | tool | | ✓ | SKIP | REVIEW |
| chrome-devtools-mcp | MCP server | | ✓ | discovery-log | REVIEW |
| scenario | framework | ✓ | ✓ | discovery-log | REVIEW |
| aimock | tool | ✓ | ✓ | discovery-log | REVIEW |
| keploy | tool | ✓ | ✓ | discovery-log | REVIEW |
| midscene | tool | ✓ | ✓ | discovery-log | REVIEW |
| evalview | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| playwright | MCP server | | ✓ | ADOPT | RUN |
| playwright-skill | skill | | ✓ | SKIP | REVIEW |
| stryker-js | tool | ✓ | ✓ | CONDITIONAL | RUN |
| qodo-cover | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| passmark | tool | ✓ | ✓ | discovery-log | REVIEW |
| diagnosing-bugs | skill | | ✓ | discovery-log | REVIEW |
| mirrord | tool | | ✓/$ | discovery-log | REVIEW |
| browser-act/skills | skill | ✓ | ✓ | discovery-log | SOURCE-ONLY |

## Review

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| agentlint | tool | ✓ | ✓ | CONDITIONAL | RUN |
| kodus-ai | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| skylos | tool | ✓ | ✓ | CONDITIONAL | RUN |
| code-review | plugin | ✓ | ✓ | KEEP | MEASURED |
| design-council | plugin | | ✓ | discovery-log | REVIEW |
| ghostsecurity/skills | skill | | ✓ | discovery-log | REVIEW |
| PR-Agent | tool | ✓ | ✓ | discovery-log | REVIEW |
| open-code-review | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| claude-octopus | plugin | ✓ | ✓/$ | discovery-log | REVIEW |
| tdd-guard | plugin | ✓ | ✓ | discovery-log | REVIEW |
| vet | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| openrewrite | framework | ✓ | ✓/$ | discovery-log | REVIEW |
| cc-safety-net | tool | ✓ | ✓ | discovery-log | REVIEW |
| pentest-ai-agents | skill | | ✓ | discovery-log | REVIEW |
| pr-review-toolkit | plugin | | ✓ | KEEP | MEASURED |
| security-guidance | plugin | | ✓ | ADOPT | MEASURED |
| shadcn/improve | tool | | ✓ | discovery-log | REVIEW |
| SkillSpector | tool | | ✓ | CONDITIONAL | MEASURED |
| skill-scanner | tool | | ✓ | discovery-log | SOURCE-ONLY |
| trailofbits/skills | skill | | ✓ | SKIP | REVIEW |
| cve-mcp-server | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| ida-pro-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| pentest-ai | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| strix | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| Claude-BugHunter | skill | | ✓ | discovery-log | REVIEW |
| hol-guard | tool | ✓ | ✓ | discovery-log | REVIEW |
| OpenOSINT | MCP server | ✓ | ✓ | SKIP | REVIEW |
| agnix | tool | ✓ | ✓ | discovery-log | REVIEW |
| agent-vault | tool | | ✓ | discovery-log | REVIEW |
| brooks-lint | skill | | ✓ | CONDITIONAL | MEASURED |
| openreview | tool | ✓ | ✓ | SKIP | REVIEW |
| code-on-incus | tool | ✓ | ✓ | discovery-log | REVIEW |
| ctf-skills | skill | | ✓ | discovery-log | SOURCE-ONLY |

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
| documentation-writer | skill | | ✓ | ADOPT | MEASURED |
| documentation-and-adrs | skill | | ✓ | ADOPT | MEASURED |
| documentation (anthropics) | skill | | ✓ | discovery-log | REVIEW |
| oo-component-documentation | skill | | ✓ | SKIP | REVIEW |

## Outer Loop

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| ACMM | framework | | ✓ | discovery-log | REVIEW |
| abtop | tool | | ✓ | CONDITIONAL | MEASURED |
| dev3000 | tool | | ✓ | discovery-log | SOURCE-ONLY |
| Apache DevLake | platform | ✓ | ✓ | DEFER | REVIEW |
| Composio | plugin | | ✓/$ | discovery-log | SOURCE-ONLY |
| Infracost | tool | ✓ | ✓/$ | SKIP | SOURCE-ONLY |
| langfuse | platform | | ✓ | discovery-log | SOURCE-ONLY |
| ccusage | tool | | ✓ | ADOPT | MEASURED |
| claude-monitor | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| vibe-log-cli | tool | | ✓ | discovery-log | SOURCE-ONLY |
| agenta | platform | | ✓ | discovery-log | SOURCE-ONLY |
| codeburn | tool | | ✓ | ADOPT | MEASURED |
| trigger.dev | platform | | ✓ | SKIP | REVIEW |
| scorecard | tool | ✓ | ✓ | discovery-log | REVIEW |
| sentrux | tool | ✓ | ✓ | discovery-log | REVIEW |
| claude-fleet | tool | | ✓ | discovery-log | REVIEW |
| agentsview | tool | ✓ | ✓ | discovery-log | REVIEW |
| promptfoo | tool | ✓ | ✓ | discovery-log | REVIEW |
| garak | tool | ✓ | ✓ | discovery-log | REVIEW |
| presidio | tool | ✓ | ✓ | discovery-log | REVIEW |
| NeMo-Guardrails | tool | ✓ | ✓ | discovery-log | REVIEW |
| superagent | tool | ✓ | ✓ | discovery-log | REVIEW |
| deepeval | framework | ✓ | ✓ | discovery-log | REVIEW |
| phoenix | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| openinference | framework | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| claude-devtools | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| harbor | framework | ✓ | ✓ | discovery-log | REVIEW |
| claude-code-hooks-multi-agent-observability | tool | ✓ | ✓ | discovery-log | REVIEW |
| claude-code-agent-monitor | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| rogue | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| giskard-oss | tool | ✓ | ✓ | discovery-log | REVIEW |
| opik | platform | ✓ | ✓ | discovery-log | REVIEW |
| agent-governance-toolkit | framework | ✓ | ✓ | discovery-log | REVIEW |
| pezzo | platform | ✓ | ✓ | discovery-log | REVIEW |
| ragas | tool | ✓ | ✓ | discovery-log | REVIEW |
| Helicone | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| logfire | platform | ✓ | ✓/$ | discovery-log | REVIEW |
| textgrad | framework | ✓ | ✓ | discovery-log | REVIEW |
| ping-island | tool | ✓ | ✓ | discovery-log | REVIEW |
| tokencost | tool | | ✓ | CONDITIONAL | RUN |

## Skills & Plugins (domain-specific)

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| academic-research-skills | skill | | ✓ | discovery-log | REVIEW |
| agent-rules-books | skill |  | ✓ | CONDITIONAL | REVIEW |
| vercel-labs/agent-skills | skill | | ✓ | discovery-log | REVIEW |
| agent-skills | skill | | ✓ | ADOPT | REVIEW |
| AI-Research-SKILLs | skill | | ✓ | discovery-log | REVIEW |
| alirezarezvani/claude-skills | plugin | | ✓ | discovery-log | REVIEW |
| andrej-karpathy-skills | skill | | ✓ | SKIP | REVIEW |
| Anthropic-Cybersecurity-Skills | skill | | ✓ | discovery-log | REVIEW |
| anthropics/skills | reference | | ✓ | discovery-log | REVIEW |
| antfu/skills | skill | | ✓ | discovery-log | REVIEW |
| azure-skills | plugin | | ✓ | discovery-log | REVIEW |
| book-to-skill | skill | | ✓ | discovery-log | REVIEW |
| Claude-Code-Game-Studios | plugin | | ✓ | discovery-log | REVIEW |
| claude-seo | skill | | ✓ | discovery-log | REVIEW |
| excalidraw-diagram-skill | skill | | ✓ | SKIP | REVIEW |
| formkit | framework | | ✓ | SKIP | REVIEW |
| frontend-slides | skill | | ✓ | discovery-log | REVIEW |
| pitch-deck | skill | | ✓ | discovery-log | REVIEW |
| powerpoint-ppt | skill | | ✓ | discovery-log | REVIEW |
| presentation-creator | skill | | ✓ | discovery-log | SOURCE-ONLY |
| lark-slides | skill | | ✓ | discovery-log | SOURCE-ONLY |
| giving-presentations | skill | | ✓ | discovery-log | SOURCE-ONLY |
| garden-skills | skill | | ✓ | discovery-log | REVIEW |
| gemini-skills | skill | | ✓ | discovery-log | REVIEW |
| google/skills | skill | | ✓ | discovery-log | REVIEW |
| terraform-skill | skill | | ✓ | discovery-log | SOURCE-ONLY |
| googleworkspace/cli | tool | | ✓ | SKIP | REVIEW |
| guizang-ppt-skill | skill | | ✓ | SKIP | REVIEW |
| html-anything | tool | | ✓ | SKIP | REVIEW |
| humanizer | skill | | ✓ | discovery-log | REVIEW |
| impeccable | skill | | ✓ | discovery-log | REVIEW |
| Jeffallan/claude-skills | skill | | ✓ | discovery-log | REVIEW |
| marketingskills | skill | | ✓ | discovery-log | REVIEW |
| mattpocock/skills | skill | | ✓ | ADOPT | MEASURED |
| pm-claude-skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| thinking-claude | framework | | ✓ | discovery-log | SOURCE-ONLY |
| claude-code-infrastructure-showcase | reference | | ✓ | discovery-log | SOURCE-ONLY |
| microsoft/skills | skill | | ✓ | discovery-log | REVIEW |
| obsidian-skills | skill | | ✓ | discovery-log | REVIEW |
| open-design | platform | | ✓ | SKIP | REVIEW |
| open-slide | tool | | ✓ | discovery-log | REVIEW |
| slidev | skill | | ✓ | discovery-log | REVIEW |
| powerpoint | skill | | ✓ | SKIP | SOURCE-ONLY |
| openskills | tool | | ✓ | discovery-log | REVIEW |
| vercel-labs/skills | tool | | ✓ | discovery-log | REVIEW |
| plugin-dev | plugin | | ✓ | discovery-log | REVIEW |
| pm-skills | skill | | ✓ | discovery-log | REVIEW |
| ponytail | skill | | ✓ | discovery-log | REVIEW |
| refly | platform | | ✓ | SKIP | REVIEW |
| scientific-agent-skills | skill | | ✓ | discovery-log | REVIEW |
| skill-creator | plugin | | ✓ | ADOPT | MEASURED |
| Skill_Seekers | tool | | ✓ | discovery-log | REVIEW |
| SkillOpt | framework | | ✓ | DEFER | REVIEW |
| stop-slop | skill | | ✓ | discovery-log | REVIEW |
| taste-skill | skill | | ✓ | discovery-log | REVIEW |
| tech-leads-club/agent-skills | skill | | ✓ | discovery-log | REVIEW |
| softaworks/agent-toolkit | skill | | ✓ | discovery-log | SOURCE-ONLY |
| NVIDIA/skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| loopy | skill | | ✓ | discovery-log | SOURCE-ONLY |
| company-os-starter-kit | plugin | | ✓ | discovery-log | SOURCE-ONLY |
| council-of-high-intelligence | tool | | ✓ | discovery-log | SOURCE-ONLY |
| typescript-mcp-server-generator | skill | | ✓ | discovery-log | REVIEW |
| ui-ux-pro-max | skill | | ✓ | discovery-log | REVIEW |
| Waza | skill | | ✓ | discovery-log | REVIEW |
| agents (wshobson) | plugin | | ✓ | discovery-log | REVIEW |
| agent-sprite-forge | skill | | ✓ | SKIP | REVIEW |
| SwiftUI-Agent-Skill | skill | | ✓ | discovery-log | REVIEW |
| guard-skills | skill | | ✓ | discovery-log | REVIEW |
| claude-night-market | plugin | | ✓ | discovery-log | REVIEW |
| huashu-design | skill | | ✓ | discovery-log | REVIEW |
| baoyu-design | skill | | ✓ | discovery-log | REVIEW |
| AlphaGBM/skills | skill | | ✓ | discovery-log | REVIEW |
| himself65/finance-skills | skill | | ✓ | discovery-log | REVIEW |
| web-access | skill | ✓ | ✓ | SKIP | REVIEW |
| cc-skills-golang | skill | | ✓ | ADOPT | REVIEW |
| waza (Microsoft) | tool | ✓ | ✓ | discovery-log | REVIEW |
| skills-hub | tool | | ✓ | discovery-log | REVIEW |
| context-engineering-kit | plugin | ✓ | ✓ | SKIP | REVIEW |
| baoyu-skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| Generative-Media-Skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| agent-skill-creator | skill | | ✓ | discovery-log | SOURCE-ONLY |
| wondelai/skills | skill | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-design-skills | reference | | ✓ | discovery-log | SOURCE-ONLY |

## Memory & Context

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| agentmemory | tool | | ✓ | discovery-log | REVIEW |
| PageIndex | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| Acontext | tool | ✓ | ✓ | discovery-log | REVIEW |
| byterover-cli | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| LightRAG | tool | ✓ | ✓ | discovery-log | REVIEW |
| memvid | tool | ✓ | ✓ | discovery-log | REVIEW |
| kreuzberg | tool | ✓ | ✓ | discovery-log | REVIEW |
| MineContext | platform | ✓ | ✓ | discovery-log | REVIEW |
| obsidian-second-brain | skill | ✓ | ✓ | discovery-log | REVIEW |
| claude-mem | plugin | ✓ | ✓ | ADOPT | MEASURED |
| lean-ctx | tool |  | ✓ | CONDITIONAL | REVIEW |
| letta | platform | | ✓ | DEFER | REVIEW |
| claude-subconscious | plugin | ✓ | ✓ | discovery-log | REVIEW |
| cognee | platform | | ✓ | discovery-log | REVIEW |
| MemOS | platform | | ✓ | discovery-log | REVIEW |
| memind | platform | ✓ | ✓ | discovery-log | REVIEW |
| ACE (agentic-context-engine) | framework | ✓ | ✓ | discovery-log | REVIEW |
| claw-compactor | tool | ✓ | ✓ | CONDITIONAL | REVIEW |
| evolver | tool | ✓ | ✓ | discovery-log | REVIEW |
| memU | platform | ✓ | ✓ | discovery-log | REVIEW |
| memory-os | tool | ✓ | ✓ | discovery-log | REVIEW |
| Memori | platform | | ✓ | discovery-log | REVIEW |
| OpenViking | platform | | ✓ | SKIP | REVIEW |
| RAGFlow | platform | ✓ | ✓ | discovery-log | REVIEW |
| engram | tool | | ✓ | discovery-log | REVIEW |
| mem0 | MCP server | | ✓ | discovery-log | REVIEW |
| OMEGA | MCP server | ✓ | ✓/$ | KEEP | REVIEW |
| server-memory | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| SimpleMem | tool | | ✓ | discovery-log | REVIEW |
| squish-memory | MCP server | | ✓ | SKIP | REVIEW |
| longhand | MCP server | | ✓ | discovery-log | REVIEW |
| storybloq | plugin | ✓ | ✓ | discovery-log | REVIEW |
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
| hivemind | tool | ✓ | ✓ | discovery-log | REVIEW |
| AgentRecall-MCP | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| getspecstory | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| mex | tool | ✓ | ✓ | discovery-log | SOURCE-ONLY |

## MCP Servers (infrastructure)

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| awslabs/mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| blender-mcp | MCP server | ✓ | ✓ | SKIP | REVIEW |
| unity-mcp | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| codebase-memory-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| fastapi_mcp | framework | | ✓ | discovery-log | REVIEW |
| mcp-use | framework | | ✓ | discovery-log | REVIEW |
| cloudflare-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| agent-toolkit-for-aws | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| confluence | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| devfleet | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| exa-mcp-server | MCP server | ✓ | ✓/$ | discovery-log | REVIEW |
| fal-ai-mcp-server | MCP server | ✓ | ✓/$ | discovery-log | REVIEW |
| hyperframes | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| fastmcp | framework | | ✓ | ADOPT | RUN |
| Figma-Context-MCP | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| firecrawl-mcp | MCP server | ✓ | ✓/$ | discovery-log | REVIEW |
| github-mcp-server | MCP server | ✓ | ✓ | ADOPT | MEASURED |
| jira | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| mcp-toolbox | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| prisma | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| sequential-thinking | MCP server | ✓ | ✓ | SKIP | REVIEW |
| sentry | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |
| server-filesystem | MCP server | ✓ | ✓ | SKIP | REVIEW |
| server-github | MCP server | ✓ | ✓ | SKIP | REVIEW |
| supabase | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| token-optimizer-mcp | MCP server | ✓ | ✓ | CONDITIONAL | REVIEW |
| opendocswork-mcp | MCP server | ✓ | ✓ | SKIP | REVIEW |
| plumb-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| figma-mcp-go | MCP server | ✓ | ✓ | SKIP | REVIEW |
| pg-aiguide | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| mcp2cli | tool | ✓ | ✓ | discovery-log | REVIEW |
| mirage | tool | | ✓ | discovery-log | REVIEW |
| Pare | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| ref-tools-mcp | MCP server | ✓ | ✓/$ | discovery-log | REVIEW |
| DesktopCommanderMCP | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| DebugMCP | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| google-workspace-mcp | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| mcp-context-forge | MCP server | ✓ | ✓ | discovery-log | REVIEW |
| gh-aw-mcpg | MCP server | ✓ | ✓ | discovery-log | SOURCE-ONLY |

## Research & Discovery

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| Agent-Reach | tool | | ✓ | discovery-log | REVIEW |
| AutoResearchClaw | harness | ✓ | ✓ | discovery-log | REVIEW |
| aisuite | framework | | ✓ | SKIP | REVIEW |
| webclaw | tool | | ✓ | SKIP | REVIEW |
| firecrawl | tool | | ✓/$ | discovery-log | SOURCE-ONLY |
| autoresearch | tool | ✓ | ✓ | discovery-log | REVIEW |
| ARIS | skill | ✓ | ✓ | discovery-log | REVIEW |
| last30days-skill | skill | | ✓ | ADOPT | MEASURED |
| llm-council | tool | | ✓ | discovery-log | REVIEW |
| PaperOrchestra | skill | | ✓ | discovery-log | REVIEW |
| storm | tool | ✓ | ✓ | discovery-log | REVIEW |
| AutoSci | harness | ✓ | ✓ | discovery-log | REVIEW |
| notebooklm-py | tool | ✓ | ✓ | discovery-log | REVIEW |
| evo | tool | ✓ | ✓/$ | discovery-log | REVIEW |
| awesome-llm-apps | reference | | ✓ | discovery-log | SOURCE-ONLY |
| Awesome-LLMOps (InftyAI) | reference | | ✓ | discovery-log | SOURCE-ONLY |
| Awesome-LLMOps (tensorchord) | reference | | ✓ | discovery-log | SOURCE-ONLY |
| Deep-Research-skills | skill | | ✓ | discovery-log | SOURCE-ONLY |

## Reference

| Tool | Type | Auto | Free | Evaluated | Evidence |
|------|------|------|------|------|------|
| antigravity-awesome-skills | reference | | ✓ | discovery-log | REVIEW |
| awesome-agent-skills | reference | | ✓ | discovery-log | REVIEW |
| awesome-agent-skills (libukai) | reference | | ✓ | discovery-log | REVIEW |
| awesome-ai-agents | reference | | ✓ | SKIP | REVIEW |
| awesome-claude-code | reference | | ✓ | discovery-log | REVIEW |
| awesome-claude-code-subagents | reference | | ✓ | discovery-log | REVIEW |
| ai-agents-for-beginners | reference | | ✓ | discovery-log | REVIEW |
| mcp-for-beginners | reference | | ✓ | ADOPT | REVIEW |
| genai-agents | reference | | ✓ | discovery-log | REVIEW |
| agents-towards-production | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-claude-skills (Composio) | reference | | ✓ | discovery-log | REVIEW |
| awesome-claude-skills (behisecc) | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-claude-skills (travisvn) | reference | | ✓ | SKIP | REVIEW |
| claude-cookbooks | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-codex-skills | reference | | ✓ | discovery-log | REVIEW |
| awesome-llm-agents | reference | | ✓ | discovery-log | REVIEW |
| awesome-hermes-agent | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-ai-tools-for-ui | reference | | ✓ | discovery-log | SOURCE-ONLY |
| awesome-openclaw-skills | reference | | ✓ | discovery-log | REVIEW |
| ai-engineering-from-scratch | reference | | ✓ | discovery-log | REVIEW |
| claude-code | reference | | ✓ | discovery-log | REVIEW |
| claude-code-best-practice | reference | | ✓ | discovery-log | REVIEW |
| claude-code-system-prompts | reference | | ✓ | discovery-log | REVIEW |
| claude-code-tips | reference | | ✓ | discovery-log | REVIEW |
| claude-howto | reference | | ✓ | discovery-log | REVIEW |
| Awesome-finance-skills | skill | | ✓ | SKIP | REVIEW |
| claude-plugins-official | reference | | ✓ | KEEP | REVIEW |
| dictionary-of-ai-coding | reference | | ✓ | ADOPT | REVIEW |
| Fabric | framework | | ✓ | SKIP | REVIEW |
| learn-claude-code | reference | | ✓ | discovery-log | REVIEW |
| awesome-harness-engineering | reference | | ✓ | discovery-log | SOURCE-ONLY |
| learn-harness-engineering | reference | | ✓ | discovery-log | SOURCE-ONLY |
| system-prompts-and-models | reference | | ✓ | discovery-log | REVIEW |
| CL4R1T4S | reference | | ✓ | discovery-log | SOURCE-ONLY |
| tolaria | tool | | ✓ | SKIP | REVIEW |
| docmd | tool | | ✓ | discovery-log | REVIEW |
| agentskills | reference | | ✓ | ADOPT | REVIEW |
| agents-best-practices | skill | | ✓ | discovery-log | REVIEW |
| buildwithclaude | reference | | ✓ | discovery-log | REVIEW |
| awesome-mcp-servers | reference | | ✓ | discovery-log | SOURCE-ONLY |
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
| Plan | 54 | 21 | 6 | 39% |
| Implement | 194 | 40 | 4 | 21% |
| Verify | 21 | 5 | 2 | 24% |
| Review | 33 | 10 | 3 | 30% |
| Ship | 3 | 1 | 1 | 33% |
| Reflect | 5 | 4 | 3 | 80% |
| Outer Loop | 40 | 9 | 2 | 22% |
| Skills & Plugins | 83 | 18 | 4 | 22% |
| Memory & Context | 47 | 9 | 2 | 19% |
| MCP Servers | 39 | 9 | 2 | 23% |
| Research & Discovery | 18 | 3 | 1 | 17% |
| Reference | 53 | 10 | 4 | 19% |
| **Total** | **590** | **139** | **34** | **24%** |
