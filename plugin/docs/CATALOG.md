# AI Tooling Catalog

A flat inventory of every AI tool, skill, agent, framework, harness, workflow, and MCP server in my orbit — starred or installed. Each entry defines what it does, what problem it solves, and what other tools overlap with it.

**Goal:** See everything at a glance, spot redundancy, converge on an ideal AI-assisted dev workflow.

## Field definitions

- **Name** — tool name, linked to repo or source
- **Type** — `tool` / `skill` / `plugin` / `framework` / `harness` / `platform` / `MCP server` / `reference`
- **One-liner** — what it does in plain language
- **Problem it solves** — the specific pain point it addresses
- **Overlaps with** — other entries in this catalog that address a similar problem

---

## Code Understanding

Tools that help you visualize, navigate, and comprehend codebases before or during AI-assisted work.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) | tool | Turns code into interactive knowledge graphs explorable with questions | Hard to grasp unfamiliar codebases; need to ask questions about structure and relationships | codegraph, graphify |
| [codegraph](https://github.com/colbymchenry/codegraph) | tool | Pre-indexed code knowledge graph that auto-syncs on changes | Agents lack structural awareness of the codebase they're working in | Understand-Anything, graphify |
| [graphify](https://github.com/safishamsi/graphify) | skill | Turns code, SQL, docs, images, or videos into queryable knowledge graphs | Need to convert diverse artifacts (not just code) into navigable structure | Understand-Anything, codegraph |
| [repomix](https://github.com/yamadashy/repomix) | tool | Packs entire repo into a single AI-friendly file | Need to feed a full codebase to an LLM that doesn't have file access | — (different approach: serialization vs. graph) |

## Agent Orchestration

Tools for running, managing, and coordinating multiple AI agents working in parallel.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-squad](https://github.com/smtg-ai/claude-squad) | tool | Manages multiple AI terminal agents (Claude Code, Codex, OpenCode, Amp) in parallel | Running one agent at a time is slow; need parallel agent sessions with visibility | gastown, sandcastle, OpenHands |
| [gastown](https://github.com/gastownhall/gastown) | tool | Multi-agent workspace manager | Need to coordinate multiple agents sharing a workspace without conflicts | claude-squad, sandcastle |
| [sandcastle](https://github.com/mattpocock/sandcastle) | framework | Orchestrate sandboxed coding agents in TypeScript | Need programmatic control over agent spawning and isolation | claude-squad, gastown, langgraph |
| [LangGraph](https://github.com/langchain-ai/langgraph) | framework | Build resilient, stateful language model agents with graphs | Need complex agent workflows with branching, cycles, and state management | sandcastle, Flowise |
| [Flowise](https://github.com/FlowiseAI/Flowise) | platform | Build AI agents visually with drag-and-drop | Want to compose agent workflows without writing code | LangGraph |
| [OpenHands](https://github.com/OpenHands/OpenHands) | platform | AI-driven development platform (formerly OpenDevin) | Want a full AI dev environment, not just a CLI agent | claude-squad, gastown |
| [superset](https://github.com/superset-sh/superset) | tool | Code editor for the AI agents era — run an army of Claude Code, Codex, etc. on your machine | Need a unified editor that manages multiple agent instances natively | claude-squad, gastown |
| [goose](https://github.com/aaif-goose/goose) | platform | Extensible AI agent that can install, execute, edit, and test with any LLM | Want a model-agnostic agent platform with plugin extensibility | OpenHands, claude-squad |
| [opencode](https://github.com/anomalyco/opencode) | platform | Open source coding agent | Want an open source alternative to Claude Code | OpenHands, goose |
| [dify](https://github.com/langgenius/dify) | platform | Production-ready agentic workflow platform with visual orchestration | Need visual agent workflow design at production scale | Flowise, LangGraph |
| [codex-plugin-cc](https://github.com/openai/codex-plugin-cc) | plugin | Use OpenAI Codex from Claude Code to review code or delegate tasks | Want to leverage multiple AI providers within a single agent session | — (unique: cross-provider bridge) |
| [opencode-swarm](https://github.com/zaxbysauce/opencode-swarm) | plugin | Architect-centric swarm plugin for OpenCode | Need swarm orchestration with architect agent coordination | claude-squad, gastown |

## Agent Harnesses

Frameworks that structure, enhance, or optimize how a single coding agent operates — its methodology, tooling, and guardrails.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [superpowers](https://github.com/obra/superpowers) | plugin | Agentic skills framework and software development methodology | Raw Claude Code lacks structured workflows for debugging, TDD, code review, and verification | gstack, ECC, ruflo, compound-engineering |
| [gstack](https://github.com/garrytan/gstack) | harness | Garry Tan's Claude Code setup: 23 opinionated agent tools (CEO, Designer, Eng Manager, etc.) | Need a curated, opinionated agent configuration that covers common roles | superpowers, ECC |
| [ECC](https://github.com/affaan-m/ECC) | harness | Agent performance optimization with skills, instincts, memory, and security | Claude Code underperforms without tuned skills, memory integration, and guardrails | superpowers, gstack, ruflo |
| [ruflo](https://github.com/ruvnet/ruflo) | harness | Agent meta-harness with multi-agent swarms, adaptive memory, self-learning | Want an all-in-one framework that combines orchestration, memory, and agent enhancement | superpowers, ECC, harness |
| [harness](https://github.com/revfactory/harness) | skill | Meta-skill that designs domain-specific agent teams and generates specialized skills | Need agents tailored to a specific domain without manually writing each skill | ruflo, superpowers |
| [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | harness | Token-efficient agent harness optimized for complex codebases | Standard agent setup struggles with large repos and wastes context on boilerplate | superpowers, ECC, headroom |
| [bernstein](https://github.com/sipyourdrink-ltd/bernstein) | harness | Audit-grade multi-agent orchestration with HMAC-chained audit log and signed agent cards | Need compliance-ready agent orchestration with tamper-proof logs | superpowers, ruflo |
| [compound-engineering](https://github.com/EveryInc/compound-engineering-plugin) | plugin | Compound engineering plugin for Claude Code, Codex, Cursor, and more | Want a unified engineering methodology that works across multiple AI editors | superpowers, gstack |
| [ralph-claude-code](https://github.com/frankbria/ralph-claude-code) | harness | Autonomous AI development loop with intelligent exit detection | Want Claude Code to run autonomously with self-termination when work is done | superpowers, ruflo |
| [agency-agents](https://github.com/msitarzewski/agency-agents) | harness | Complete AI agency with specialized expert agents (frontend, marketing, QA, etc.) | Want a pre-built team of domain experts rather than configuring individual skills | gstack, harness |
| [Fabric](https://github.com/danielmiessler/Fabric) | framework | Modular AI framework with crowdsourced prompt patterns | Want reusable AI patterns (extract, summarize, analyze) as composable modules | superpowers |
| [claude-code-staff-engineer](https://github.com/FareedKhan-dev/claude-code-staff-engineer) | harness | Staff engineer with sub-agent teams in Claude Code | Want hierarchical agent teams with a lead engineer coordinating specialists | gstack, agency-agents |
| [humanlayer](https://github.com/humanlayer/humanlayer) | harness | AI coding agents for hard problems in complex codebases | Need agents tuned for difficult, multi-file problems in large repos | superpowers, oh-my-openagent |
| [claude-code-harness](https://github.com/Chachamaru127/claude-code-harness) | harness | Autonomous Plan-Work-Review cycle harness for Claude Code (2.7K stars) | Want a structured autonomous dev loop with built-in review gates | superpowers, ralph-claude-code |
| [KARIMO](https://github.com/opensesh/KARIMO) | plugin | Product design-driven agent orchestration with sub-agents and agent teams | Need phased adoption from PRD execution to automated review and CI-friendly agent teams | superpowers, gstack |

## Memory & Context

Tools for persistent memory across sessions, context compression, and learning from past interactions.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| OMEGA | MCP server | Persistent cross-session memory with semantic search, knowledge graphs, and coordination | Agents forget everything between sessions; no continuity | agentmemory, beads, claude-mem |
| [agentmemory](https://github.com/rohitg00/agentmemory) | tool | Persistent memory for AI coding agents based on real-world benchmarks | Need memory that's been validated against actual dev workflows | OMEGA, beads, claude-mem |
| [beads](https://github.com/gastownhall/beads) | tool | Memory upgrade for coding agents | Default agent memory is too shallow or ephemeral | OMEGA, agentmemory, claude-mem |
| claude-mem | plugin | Persistent memory with semantic search, timeline views, and knowledge graph management | Need searchable, structured memory with temporal awareness | OMEGA, agentmemory, beads |
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | plugin | Self-learning system that captures corrections and preferences, syncs to CLAUDE.md | Agent keeps making the same mistakes; doesn't learn from feedback | claude-mem, OMEGA (different focus: learning vs. recall) |
| [headroom](https://github.com/chopratejas/headroom) | tool | Compresses tool outputs, logs, and files before they reach the LLM (60-95% fewer tokens) | Context window fills up too fast with verbose tool output | token-optimizer-mcp |
| [SimpleMem](https://github.com/aiming-lab/SimpleMem) | tool | Efficient lifelong memory for LLM agents (text and multimodal) | Need lightweight memory with multimodal support and academic backing | claude-mem, OMEGA, agentmemory |
| [claude-subconscious](https://github.com/letta-ai/claude-subconscious) | plugin | Give Claude Code a subconscious — persistent state across sessions | Want transparent persistent state without explicit memory commands | claude-mem, OMEGA |
| [mem0](https://github.com/mem0ai/mem0) | MCP server | AI memory layer storing relationships between people, code, and concepts across sessions | Need structured relationship-aware memory, not just key-value persistence | claude-mem, OMEGA, SimpleMem |

## Skills & Plugins

Extensions that add domain-specific capabilities to coding agents.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-skills](https://github.com/addyosmani/agent-skills) | skill | Production-grade engineering skills for AI coding agents | Need battle-tested skills from a senior engineer's perspective | mattpocock/skills, everything-claude-code |
| [mattpocock/skills](https://github.com/mattpocock/skills) | skill | Skills for Real Engineers from experienced dev's .claude directory | Need practical, TypeScript-focused skills from a working dev | agent-skills, everything-claude-code |
| everything-claude-code | plugin | 251+ domain-specific skills covering architecture, testing, 40+ frameworks, and verticals | Want broad skill coverage across many languages and domains | agent-skills, mattpocock/skills |
| [pm-skills](https://github.com/phuryn/pm-skills) | skill | 100+ agentic skills for product management (discovery, strategy, execution, launch) | Need AI assistance with PM work, not just coding | — (domain-specific) |
| [marketingskills](https://github.com/coreyhaines31/marketingskills) | skill | Marketing skills: CRO, copywriting, SEO, analytics, growth engineering | Need AI assistance with marketing tasks | — (domain-specific) |
| [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | skill | Design intelligence for professional UI/UX across platforms | AI generates ugly or generic UIs without design guidance | impeccable, frontend-design plugin |
| [taste-skill](https://github.com/Leonxlnx/taste-skill) | skill | Prevents AI from generating boring, generic output — gives AI good taste | AI output reads as bland, cookie-cutter slop | stop-slop |
| [stop-slop](https://github.com/hardikpandya/stop-slop) | skill | Removes AI tells from prose (filler words, hedging, corporate speak) | AI-written text is obviously AI-written | taste-skill, humanizer |
| [caveman](https://github.com/JuliusBrussee/caveman) | skill | Ultra-compressed communication that cuts 65% of tokens by dropping filler | Context window fills up with verbose agent responses; need token efficiency | headroom, token-optimizer-mcp |
| [humanizer](https://github.com/blader/humanizer) | skill | Removes signs of AI-generated writing from text | AI output reads as obviously machine-generated | taste-skill, stop-slop |
| [book-to-skill](https://github.com/virgiliojr94/book-to-skill) | skill | Turn any technical book PDF into a Claude Code skill for reference while working | Want domain knowledge from a book available as agent context without manual extraction | — (unique: book → skill converter) |
| [impeccable](https://github.com/pbakaus/impeccable) | skill | Design language that makes AI better at visual design | AI struggles with aesthetics and design consistency | ui-ux-pro-max, frontend-design plugin |
| [open-slide](https://github.com/1weiho/open-slide) | tool | Slide framework built for AI agents | Need agents to create presentations, not just code | — |
| [design-council](https://github.com/sjsyrek/design-council) | plugin | 11 role-specialized peer agents debate technical decisions | Want multiple perspectives (security, perf, UX, etc.) on architecture choices | — (unique: adversarial design review) |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | skill | CLAUDE.md based on Karpathy's LLM coding pitfall observations | Want coding guidelines derived from known LLM failure modes | mattpocock/skills, agent-skills |
| [excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | skill | Generates Excalidraw diagrams from Claude Code | Need agents to create visual architecture diagrams, not just code | graphify |
| [google/skills](https://github.com/google/skills) | skill | Agent skills for Google products and technologies | Need AI assistance with Google Cloud, Workspace, Firebase workflows | — (domain-specific) |
| [Composio](https://github.com/ComposioHQ/composio) | plugin | Cross-app workflow integration - connect Claude Code to Linear, Figma, GitHub, Sentry, Slack | Need agents to trigger actions across external tools in one workflow | — (unique: workflow integration layer) |
| skill-creator | plugin | Create, document, and publish Claude Code skills | Need to author custom skills efficiently | plugin-dev plugin |
| plugin-dev | plugin | Plugin development framework with agent, command, and hook support | Need to build Claude Code plugins | skill-creator |

## Code Review & Quality

Tools for automated code review, quality checks, and codebase improvement.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| code-review | plugin | Multi-agent code review with confidence-based scoring | Need automated review that catches real issues, not noise | pr-review-toolkit, shadcn/improve |
| pr-review-toolkit | plugin | PR review utilities: type analysis, silent failure hunting, test coverage, comment analysis | Need structured review dimensions beyond just "looks good" | code-review |
| [shadcn/improve](https://github.com/shadcn/improve) | tool | Use the most capable model to audit codebase, write plans for cheaper models to execute | Want high-quality codebase audits without burning expensive model tokens on execution | code-review |

## Maturity Frameworks

Frameworks for assessing and systematically improving how a codebase leverages AI-assisted development.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ACMM](https://arxiv.org/abs/2604.09388) | framework | 6-level AI Codebase Maturity Model defined by feedback loop topology, not autonomy | Teams plateau at "prompt and review" without a systematic progression path; tools without feedback loops produce chaos | — |

## Dev Workflow

Tools for git management, planning, project orchestration, and development process.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| GSD (Get Shit Done) | framework | Project orchestration: milestones, phases, planning, execution, and verification with 12 specialized agents | Need structured project management around AI-assisted development | superpowers (GSD is part of superpowers), feature-dev |
| [worktrunk](https://github.com/max-sixty/worktrunk) | tool | CLI for git worktree management, designed for parallel AI agent workflows | Need isolated git branches for multiple agents working simultaneously | — |
| [plannotator](https://github.com/backnotprop/plannotator) | tool | Annotate and review coding agent plans and code diffs visually, share with team | Agent plans are hard to review and discuss with teammates | — |
| commit-commands | plugin | Git workflow shortcuts: clean_gone, commit, commit-push-pr | Repetitive git operations slow down agent-assisted workflow | — |
| [reporails/cli](https://github.com/reporails/cli) | tool | AI instructions diagnostics for Claude, Codex, Copilot, Cursor, Gemini agents | Don't know if CLAUDE.md / agent instructions are well-formed or conflicting | — |
| [CLI-Anything](https://github.com/HKUDS/CLI-Anything) | tool | Making all software agent-native via CLI wrappers | Existing tools don't expose interfaces that AI agents can use | — |
| feature-dev | plugin | Feature development workflow with planning, implementation, and verification stages | Need a structured feature development process with AI agents | GSD |
| [claude-code-action](https://github.com/anthropics/claude-code-action) | tool | Run Claude Code as a GitHub Action for CI/CD automation | Want AI agents to respond to issues/PRs automatically in CI pipelines | — (unique: CI integration) |
| [claude-task-master](https://github.com/eyaltoledano/claude-task-master) | tool | AI-powered task management for Cursor, Windsurf, Roo, and other editors | Need structured task breakdown and tracking across AI editors | GSD |
| [gsd-build](https://github.com/gsd-build/get-shit-done) | framework | Standalone GSD: meta-prompting and spec-driven dev for Claude Code | Want GSD methodology without the full superpowers plugin | GSD (superpowers), feature-dev |

## MCP Servers

Model Context Protocol servers that connect AI agents to external services and capabilities.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [context7](https://github.com/upstash/context7) | MCP server | Live documentation lookup with semantic search across library/framework docs | Agent's training data is outdated; needs current API docs | — |
| [playwright](https://github.com/playwright-community/mcp) | MCP server | Browser automation and testing from within agent sessions | Agent can't interact with web UIs or run browser tests | — |
| [cloudflare-mcp](https://github.com/cloudflare/mcp-server-cloudflare) | MCP server | Cloudflare integration: workers, builds, bindings, observability | Need to manage Cloudflare infrastructure from agent sessions | — |
| prisma | MCP server | Database operations via Prisma ORM (migrations, studio, status) | Agent needs to interact with databases during development | — |
| sentry | MCP server | Error tracking and monitoring integration | Agent needs access to production error data for debugging | — |
| [blender-mcp](https://github.com/ahujasid/blender-mcp) | MCP server | Blender 3D modeling integration | Need AI to control 3D modeling workflows | — |
| sequential-thinking | MCP server | Chain-of-thought reasoning enhancement via structured thinking steps | Agent's reasoning is shallow on complex problems | — |
| server-memory | MCP server | Basic persistent key-value memory | Need simple state persistence between agent calls | OMEGA, claude-mem |
| server-github | MCP server | GitHub operations (repos, issues, PRs, actions) | Agent needs to interact with GitHub beyond local git | github plugin |
| server-filesystem | MCP server | Local filesystem access with safety controls | Agent needs structured file operations with guardrails | — |
| exa-mcp-server | MCP server | Web search and research via Exa API | Agent needs to search the web for current information | — |
| firecrawl-mcp | MCP server | Web scraping and crawling | Agent needs to extract content from web pages | exa-mcp-server |
| fal-ai-mcp-server | MCP server | Image, video, and audio generation via fal.ai | Agent needs to generate media assets | — |
| token-optimizer-mcp | MCP server | 95%+ context reduction for tool outputs | Context window fills up too fast | headroom |
| browser-use | MCP server | AI browser agent for autonomous web interaction | Need agents to navigate and interact with web pages autonomously | playwright |
| evalview | MCP server | AI agent regression testing | Can't tell if agent behavior regressed after config changes | langfuse |
| squish-memory | MCP server | Local-first persistent memory runtime | Need memory that runs locally without external dependencies | OMEGA, claude-mem, server-memory |
| longhand | MCP server | Session history indexing for cross-session search | Need to find what happened in past agent sessions | OMEGA, claude-mem |
| devfleet | MCP server | Multi-agent orchestration via MCP | Need to coordinate agents through the MCP protocol rather than CLI | claude-squad, gastown |
| supabase | MCP server | Supabase database and auth operations | Agent needs to interact with Supabase projects during development | prisma |
| jira | MCP server | Jira issue tracking integration | Agent needs to read/update Jira tickets during development | — |
| confluence | MCP server | Confluence wiki integration | Agent needs to read/write team documentation | — |
| [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | MCP server | Chrome DevTools integration for coding agents | Need agents to inspect, debug, and profile web apps in Chrome | playwright |

## Observability

Tools for monitoring, debugging, and understanding AI agent behavior and performance.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [langfuse](https://github.com/langfuse/langfuse) | platform | Open source AI engineering: evals, observability, prompt management, datasets | Can't see what agents are doing, how well they perform, or where they fail | evalview |
| [tokencost](https://github.com/mr-beaver/tokencost) | tool | Track exactly what you spend on Claude CLI with cost optimization insights | Can't see how much agent sessions cost or where tokens are wasted | — (unique: cost tracking) |

## Research & Discovery

Tools for AI-assisted research, information gathering, and multi-model reasoning.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [autoresearch](https://github.com/karpathy/autoresearch) | tool | AI agents running automated research experiments | Research is tedious; want AI to run experiments autonomously | — |
| [llm-council](https://github.com/karpathy/llm-council) | tool | Multiple LLMs work together to answer the hardest questions | Single model has blind spots; committee of models is more reliable | — |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | skill | Research any topic across Reddit, X, YouTube, HN, Polymarket, and the web | Need current sentiment and discussion, not just static docs | Agent-Reach |
| [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | tool | Give AI agents eyes to see the internet — read and search Twitter, Reddit, YouTube, GitHub, zero API fees | Need agents to access social/web content without paid APIs | last30days-skill, exa-mcp-server |
| [aisuite](https://github.com/andrewyng/aisuite) | framework | Simple unified interface to multiple generative AI providers | Switching between AI providers requires different SDKs and APIs | — |

## Security & Safety

Tools for scanning agent-generated code and skills for vulnerabilities.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | tool | Security scanner for AI agent skills — detects vulnerabilities and malicious patterns | Downloaded skills could contain prompt injection or exfiltration | scorecard |
| [scorecard](https://github.com/ossf/scorecard) | tool | OpenSSF security health metrics for open source projects | Can't quickly assess if a dependency or tool is maintained and secure | SkillSpector |
| [ghostsecurity/skills](https://github.com/ghostsecurity/skills) | skill | AppSec skills for AI coding agents — OWASP, threat modeling, secure defaults | Need security-focused skills that catch vulnerabilities during development, not just review | SkillSpector, security-guidance |
| [agentlint](https://github.com/mauhpr/agentlint) | tool | Real-time guardrails for AI agents: 77 rules, 8 packs, inline ignores | Need runtime guardrails that prevent agents from doing dangerous things, not just scan after | SkillSpector |
| [trailofbits/skills](https://github.com/trailofbits/skills) | skill | Trail of Bits security research skills for vulnerability detection and audit workflows | Need professional-grade security analysis from a top security firm's methodology | ghostsecurity/skills, SkillSpector |
| security-guidance | plugin | Security review and vulnerability detection for code | Agent-generated code may introduce security vulnerabilities | ghostsecurity/skills |

## Reference

Curated lists, glossaries, and system prompt collections for learning and discovery.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | reference | Curated skills, hooks, slash-commands, and agent orchestrators for Claude Code | Hard to discover what's available in the Claude Code ecosystem | awesome-claude-skills (travisvn), awesome-claude-skills (Composio) |
| [awesome-claude-skills (travisvn)](https://github.com/travisvn/awesome-claude-skills) | reference | Curated Claude Skills and customization tools | Need a catalog of available skills to evaluate | awesome-claude-code, awesome-claude-skills (Composio) |
| [awesome-claude-skills (Composio)](https://github.com/ComposioHQ/awesome-claude-skills) | reference | Curated list of Claude Skills and customization resources | Need a catalog of available skills to evaluate | awesome-claude-code, awesome-claude-skills (travisvn) |
| [awesome-llm-agents](https://github.com/kaushikb11/awesome-llm-agents) | reference | Curated list of LLM agent frameworks and tools | Need to discover agent frameworks beyond Claude Code ecosystem | awesome-ai-agents |
| [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | reference | List of AI autonomous agents and platforms | Need to discover standalone AI agent projects | awesome-llm-agents |
| [dictionary-of-ai-coding](https://github.com/mattpocock/dictionary-of-ai-coding) | reference | AI coding jargon explained in plain English | Terms like "harness", "skill", "agent" are overloaded and confusing | — |
| [system-prompts-and-models](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | reference | Full system prompts from AI coding tools (Cursor, Devin, Windsurf, Claude Code, etc.) | Want to understand how competing AI tools work under the hood | — |
| [ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) | reference | Learn AI engineering: build it, ship it for others | Need a learning path for AI engineering concepts | — |
| [gentleman-book-mcp](https://github.com/Alan-TheGentleman/gentleman-book-mcp) | MCP server | 18 chapters of software architecture knowledge accessible to AI agents | Agent lacks deep architecture knowledge for design decisions | — |
