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
| [code-review-graph](https://github.com/tirth8205/code-review-graph) | tool | Local-first code intelligence graph with blast-radius analysis for reviews | Agents read too many files during review; need to know exactly what a change affects | codegraph, graphify |
| [opensrc](https://github.com/vercel-labs/opensrc) | tool | Fetch npm package source code to give AI coding agents deeper dependency context | Agent can't read inside node_modules to understand dependency internals | context7 (complementary: context7 = docs, opensrc = source) |
| [code-context-engine](https://github.com/elara-labs/code-context-engine) | MCP server | Index codebase, agents search instead of reading files — 94% token savings | AI agents read too many files and waste tokens; indexed search is faster and cheaper | repomix, codegraph, context7 |
| [trace-mcp](https://github.com/nikolai-vysotskyi/trace-mcp) | MCP server | One tool call replaces ~42 minutes of agent exploration via deep trace-based code understanding | Agents waste time exploring codebases file-by-file | codegraph, code-context-engine |
| [SocratiCode](https://github.com/giancarloerra/SocratiCode) | tool | Enterprise-grade codebase intelligence — semantic search, dependency graphs, 61% fewer tokens (3K stars) | Agents waste tokens on large codebases; need indexed code intelligence with impact analysis | codegraph, code-context-engine, trace-mcp |

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
| [opencode-swarm](https://github.com/ZaxbyHub/opencode-swarm) | plugin | Architect-centric swarm plugin for OpenCode | Need swarm orchestration with architect agent coordination | claude-squad, gastown |
| [agent-orchestrator](https://github.com/AgentWrapper/agent-orchestrator) | tool | Plans tasks, spawns parallel coding agents, handles CI fixes and merge conflicts autonomously | Need automated orchestration of multiple agents with conflict resolution | claude-squad, gastown |
| [lobehub](https://github.com/lobehub/lobehub) | platform | Agent operations platform — hire, schedule, and report on 7x24 AI agent teams | Want always-on agent fleet management with scheduling and reporting | claude-squad, OpenHands |
| [cherry-studio](https://github.com/CherryHQ/cherry-studio) | platform | AI productivity studio with smart chat, autonomous agents, and 300+ assistants | Want a unified desktop AI workspace with multi-model support | lobehub, OpenHands |
| [dmux](https://github.com/standardagents/dmux) | tool | Dev agent multiplexer for git worktrees and coding agents | Need lightweight worktree-based agent isolation without full orchestration | worktrunk, claude-squad |
| [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | harness | Teams-first multi-agent orchestration for Claude Code | Need team-oriented multi-agent coordination beyond solo use | claude-squad, agent-orchestrator |
| [CowAgent](https://github.com/zhayujie/CowAgent) | harness | Open-source super AI assistant — plans tasks, runs tools, self-evolves with memory and knowledge | Want a self-evolving agent harness with built-in memory and multi-channel support | superpowers, ralph-claude-code |
| [nanoclaw](https://github.com/nanocoai/nanoclaw) | platform | Lightweight containerized agent runtime with WhatsApp, Telegram, Slack, Discord, Gmail integration | Need a secure container-based agent with messaging app integration | goose, OpenHands |
| [hive](https://github.com/aden-hive/hive) | harness | Multi-agent harness for production AI | Need production-grade multi-agent orchestration | superpowers, agent-orchestrator |
| [happy](https://github.com/slopus/happy) | platform | Mobile and web client for Codex and Claude Code with realtime voice and encryption | Want to use Claude Code from mobile/web with voice support | — (unique: mobile client) |
| [claurst](https://github.com/Kuberwastaken/claurst) | harness | Agentic coding for builders who ship | Need a shipping-focused agent harness with minimal ceremony | superpowers, compound-engineering |
| [cc-switch](https://github.com/farion1231/cc-switch) | tool | Cross-platform desktop app wrapping Claude Code, Codex, OpenCode, and more in one GUI | Need a unified desktop interface to switch between multiple CLI coding agents | cherry-studio, superset, claude-squad |
| [qwen-code](https://github.com/QwenLM/qwen-code) | platform | Alibaba's open-source terminal coding agent powered by Qwen models | Want a Qwen-native coding agent alternative to Claude Code | opencode, goose, OpenHands |
| [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | platform | DeepSeek-native terminal coding agent optimized for prefix-cache stability | Want a long-running coding agent that exploits DeepSeek's prefix caching | opencode, qwen-code, goose |
| [oh-my-pi](https://github.com/can1357/oh-my-pi) | platform | Full coding agent with 32 tools, LSP/DAP integration, hash-anchored edits, 40+ providers | Need a feature-complete open-source coding agent with built-in IDE integration | opencode, goose, OpenHands |
| [omnigent](https://github.com/omnigent-ai/omnigent) | framework | Meta-harness: orchestrate Claude Code, Codex, Cursor, Pi — swap harnesses without rewriting | Need to mix and match different agent harnesses with shared policies and sandboxing | claude-squad, oh-my-claudecode |
| [forkd](https://github.com/deeplethe/forkd) | tool | Fork() for AI agent microVMs — spawn 100 children in ~100ms from a warm parent with KVM isolation | Need fast, isolated agent sandboxes for parallel work without container overhead | nanoclaw, sandcastle |
| [architect-loop](https://github.com/DanMcInerney/architect-loop) | skill | Claude Fable 5 as architect, GPT-5.5 Codex as builder — cross-vendor agent loop | Single-vendor agent loops miss cross-model strengths; separates reasoning from execution | compound-engineering, claude-code-staff-engineer |
| [adhd](https://github.com/UditAkhourii/adhd) | skill | Tree-of-thought with pruning — fans out parallel divergent thoughts under cognitive frames | Linear agent reasoning misses creative and interdisciplinary solutions | sequential-thinking, planning-with-files |
| [opensquilla](https://github.com/opensquilla/opensquilla) | tool | Token-efficient AI agent — same budget, higher intelligence density via optimized context | Need to get more out of each agent session without increasing token spend | headroom, context-mode, caveman |

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
| [deer-flow](https://github.com/bytedance/deer-flow) | harness | ByteDance's long-horizon agent harness for tasks spanning minutes to hours | Need autonomous agent work beyond single-session scope with sandboxes and memory | ralph-claude-code, GSD |
| [agency-agents](https://github.com/msitarzewski/agency-agents) | harness | Complete AI agency with specialized expert agents (frontend, marketing, QA, etc.) | Want a pre-built team of domain experts rather than configuring individual skills | gstack, harness |
| [Fabric](https://github.com/danielmiessler/Fabric) | framework | Modular AI framework with crowdsourced prompt patterns | Want reusable AI patterns (extract, summarize, analyze) as composable modules | superpowers |
| [claude-code-staff-engineer](https://github.com/FareedKhan-dev/claude-code-staff-engineer) | harness | Staff engineer with sub-agent teams in Claude Code | Want hierarchical agent teams with a lead engineer coordinating specialists | gstack, agency-agents |
| [humanlayer](https://github.com/humanlayer/humanlayer) | harness | AI coding agents for hard problems in complex codebases | Need agents tuned for difficult, multi-file problems in large repos | superpowers, oh-my-openagent |
| [claude-code-harness](https://github.com/Chachamaru127/claude-code-harness) | harness | Autonomous Plan-Work-Review cycle harness for Claude Code (2.7K stars) | Want a structured autonomous dev loop with built-in review gates | superpowers, ralph-claude-code |
| [vibecode-pro-max-kit](https://github.com/withkynam/vibecode-pro-max-kit) | harness | Spec-driven coding harness with self-improving context memory and 15-agent autopilot | Agent forgets context and produces spaghetti; need spec-driven memory with automated workflows | superpowers, GSD, ralph-claude-code |
| [KARIMO](https://github.com/opensesh/KARIMO) | plugin | Product design-driven agent orchestration with sub-agents and agent teams | Need phased adoption from PRD execution to automated review and CI-friendly agent teams | superpowers, gstack |

## Memory & Context

Tools for persistent memory across sessions, context compression, and learning from past interactions.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| OMEGA | MCP server | Persistent cross-session memory with semantic search, knowledge graphs, and coordination | Agents forget everything between sessions; no continuity | agentmemory, beads, claude-mem |
| [agentmemory](https://github.com/rohitg00/agentmemory) | tool | Persistent memory for AI coding agents based on real-world benchmarks | Need memory that's been validated against actual dev workflows | OMEGA, beads, claude-mem |
| [beads](https://github.com/gastownhall/beads) | tool | Memory upgrade for coding agents | Default agent memory is too shallow or ephemeral | OMEGA, agentmemory, claude-mem |
| [claude-mem](https://github.com/thedotmack/claude-mem) | plugin | Persistent memory with semantic search, timeline views, and knowledge graph management | Need searchable, structured memory with temporal awareness | OMEGA, agentmemory, beads |
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | plugin | Self-learning system that captures corrections and preferences, syncs to CLAUDE.md | Agent keeps making the same mistakes; doesn't learn from feedback | claude-mem, OMEGA (different focus: learning vs. recall) |
| [headroom](https://github.com/chopratejas/headroom) | tool | Compresses tool outputs, logs, and files before they reach the LLM (60-95% fewer tokens) | Context window fills up too fast with verbose tool output | token-optimizer-mcp |
| [SimpleMem](https://github.com/aiming-lab/SimpleMem) | tool | Efficient lifelong memory for LLM agents (text and multimodal) | Need lightweight memory with multimodal support and academic backing | claude-mem, OMEGA, agentmemory |
| [claude-subconscious](https://github.com/letta-ai/claude-subconscious) | plugin | Give Claude Code a subconscious — persistent state across sessions | Want transparent persistent state without explicit memory commands | claude-mem, OMEGA |
| [mem0](https://github.com/mem0ai/mem0) | MCP server | AI memory layer storing relationships between people, code, and concepts across sessions | Need structured relationship-aware memory, not just key-value persistence | claude-mem, OMEGA, SimpleMem |
| [cognee](https://github.com/topoteretes/cognee) | platform | Open-source AI memory with self-hosted knowledge graph engine for persistent agent memory | Need structured knowledge graph memory that agents can query across sessions | claude-mem, OMEGA, SimpleMem |
| [context-mode](https://github.com/mksglu/context-mode) | skill | Context window optimization — sandboxes tool output for 98% reduction across 15 platforms | Context window fills up with verbose tool output; need aggressive compression | headroom, caveman, token-optimizer-mcp |
| [rtk](https://github.com/rtk-ai/rtk) | tool | CLI proxy that reduces LLM token consumption by 60-90% on common dev commands | Dev commands waste tokens on verbose output agents don't need | headroom, context-mode, caveman |
| [engram](https://github.com/Gentleman-Programming/engram) | tool | Agent-agnostic persistent memory — Go binary with SQLite, FTS5, MCP, CLI, and TUI | Need a single portable binary for memory that works with any AI coding agent | OMEGA, claude-mem, SimpleMem, agentmemory |
| [storybloq](https://github.com/Storybloq/storybloq) | plugin | Cross-session context for Claude Code — CLI + MCP server + /story skill | Claude Code loses context across sessions; tracks tickets, issues, handovers in .story/ | claude-mem, OMEGA, engram |
| [ArcRift](https://github.com/Eshaan-Nair/ArcRift) | tool | Sync browser AI chat context to local IDE agents via SQLite knowledge graph | Context from browser-based AI chats is siloed from IDE agents | claude-mem, OMEGA, storybloq |
| [context-infrastructure](https://github.com/grapeot/context-infrastructure) | tool | Structured context and memory system with personal rules, skills, and scheduled observations | Agent memory is ad-hoc; need a system for rules, observations, and scheduled refresh | OMEGA, claude-mem, engram |
| [AgentRecall-MCP](https://github.com/Goldentrii/AgentRecall-MCP) | MCP server | Correction-driven memory — learns from mistakes, compresses context, consolidates overnight | Memory systems store facts but don't learn from corrections | claude-mem, OMEGA, claude-subconscious |
| [agentic-stack](https://github.com/codejunkie99/agentic-stack) | tool | Portable .agent/ folder (memory + skills + protocols) that plugs into any harness (2.1K stars) | Agent config and memory are locked to one editor; need a portable brain that survives harness changes | engram, OMEGA, capa |

## Skills & Plugins

Extensions that add domain-specific capabilities to coding agents.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-skills](https://github.com/addyosmani/agent-skills) | skill | Production-grade engineering skills for AI coding agents | Need battle-tested skills from a senior engineer's perspective | mattpocock/skills, everything-claude-code |
| [documentation-writer](https://github.com/github/awesome-copilot) | skill | Diátaxis-framework documentation expert: clarify, outline, then generate purpose-specific docs | Agent produces documentation that mixes tutorial steps with reference material, serving no audience well | documentation (anthropics/knowledge-work-plugins), documentation-and-adrs |
| [documentation-and-adrs](https://github.com/addyosmani/agent-skills) | skill | ADR templates, inline comment philosophy, and agent-context documentation guidelines | Code shows what was built but not why; ADRs capture decision rationale for future engineers and agents | documentation-writer, documentation (anthropics/knowledge-work-plugins) |
| [documentation (anthropics)](https://github.com/anthropics/knowledge-work-plugins) | skill | Lightweight documentation skill covering READMEs, API docs, runbooks, and onboarding guides | Agent needs quick, low-ceremony documentation generation without multi-step workflow overhead | documentation-writer, documentation-and-adrs |
| [oo-component-documentation](https://github.com/github/awesome-copilot) | skill | Generate or refresh OO component docs from source code with create/update mode | Documentation drifts from code as classes evolve; no systematic way to keep component docs current | documentation-writer, documentation (anthropics/knowledge-work-plugins) |
| [mattpocock/skills](https://github.com/mattpocock/skills) | skill | Skills for Real Engineers from experienced dev's .claude directory | Need practical, TypeScript-focused skills from a working dev | agent-skills, everything-claude-code |
| [codebase-design](https://github.com/mattpocock/skills) | skill | Deep module design vocabulary — interfaces, seams, adapters, depth/leverage/locality | Agent designs shallow modules; need a shared vocabulary for meaningful abstraction | improve-codebase-architecture |
| [domain-modeling](https://github.com/mattpocock/skills) | skill | Build CONTEXT.md glossaries and ADRs — pin down ubiquitous language as designs evolve | Teams use inconsistent terminology; decisions aren't recorded for future agents | documentation-and-adrs |
| [diagnosing-bugs](https://github.com/mattpocock/skills) | skill | Structured diagnosis loop: build feedback loop first, then bisect/hypothesize/instrument | Jumping straight to "staring at code" wastes hours on hard bugs | systematic-debugging (superpowers) |
| [resolving-merge-conflicts](https://github.com/mattpocock/skills) | skill | Intent-preserving merge conflict resolution — trace both sides, resolve, run checks | Agents blindly pick one side of a conflict without understanding original intent | — |
| [implement](https://github.com/mattpocock/skills) | skill | Thin orchestrator: TDD at seams, typecheck regularly, review when done, commit | Need a repeatable implementation flow that enforces quality gates | tdd, feature-dev |
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
| [open-slide](https://github.com/1weiho/open-slide) | tool | Slide framework built for AI agents | Need agents to create presentations, not just code | slidev, powerpoint |
| [slidev](https://github.com/slidevjs/slidev) | skill | Markdown-to-slides for developers — code highlighting, Vue components, presenter mode | Need developer-focused presentations with live code and technical content | open-slide, powerpoint |
| [powerpoint](https://github.com/igorwarzocha/opencode-workflows) | skill | PowerPoint creation with design principles — layout positioning, template mapping, thumbnail audit | Need .pptx files for business contexts where Markdown slides won't work | open-slide, slidev |
| [design-council](https://github.com/sjsyrek/design-council) | plugin | 11 role-specialized peer agents debate technical decisions | Want multiple perspectives (security, perf, UX, etc.) on architecture choices | — (unique: adversarial design review) |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | skill | CLAUDE.md based on Karpathy's LLM coding pitfall observations | Want coding guidelines derived from known LLM failure modes | mattpocock/skills, agent-skills |
| [excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | skill | Generates Excalidraw diagrams from Claude Code | Need agents to create visual architecture diagrams, not just code | graphify |
| [google/skills](https://github.com/google/skills) | skill | Agent skills for Google products and technologies | Need AI assistance with Google Cloud, Workspace, Firebase workflows | — (domain-specific) |
| [Composio](https://github.com/ComposioHQ/composio) | plugin | Cross-app workflow integration - connect Claude Code to Linear, Figma, GitHub, Sentry, Slack | Need agents to trigger actions across external tools in one workflow | — (unique: workflow integration layer) |
| skill-creator | plugin | Create, document, and publish Claude Code skills | Need to author custom skills efficiently | plugin-dev plugin |
| plugin-dev | plugin | Plugin development framework with agent, command, and hook support | Need to build Claude Code plugins | skill-creator |
| [web-quality-skills](https://github.com/addyosmani/web-quality-skills) | skill | Web quality audit suite: accessibility, SEO, performance, Core Web Vitals, best practices | Agent produces web UIs without checking accessibility, perf, or SEO | claude-seo (SEO overlap), security-best-practices (security headers overlap) |
| [typescript-mcp-server-generator](https://github.com/github/awesome-copilot) | skill | Generate TypeScript MCP servers from API specs or descriptions (10.7K installs) | Building MCP servers requires too much boilerplate; need a generator | fastmcp |
| [anthropics/skills](https://github.com/anthropics/skills) | reference | Official Anthropic skills repository — canonical SKILL.md examples and patterns | Need the authoritative reference for writing agent skills | agentskills |
| [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | reference | Official Anthropic-managed directory of high-quality Claude Code plugins | Need a curated, trusted source for Claude Code plugins | buildwithclaude, awesome-claude-code |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | plugin | 337 skills across engineering, marketing, product, compliance, and 30+ agents | Want broad cross-domain skill coverage for multiple roles | everything-claude-code, mattpocock/skills |
| [antfu/skills](https://github.com/antfu/skills) | skill | Anthony Fu's curated agent skills collection | Want skills from a well-known open-source developer | mattpocock/skills, agent-skills |
| [garden-skills](https://github.com/ConardLi/garden-skills) | skill | Web design, knowledge retrieval, and image generation skills | Need web design and creative skills for AI agents | impeccable, ui-ux-pro-max |
| [microsoft/skills](https://github.com/microsoft/skills) | skill | Skills, MCP servers, and Agents.md for Microsoft SDKs to ground coding agents | Need AI assistance with Microsoft/Azure/dotnet workflows | google/skills |
| [ponytail](https://github.com/DietrichGebert/ponytail) | skill | Makes AI agents think like the laziest senior dev — write minimum code, avoid overengineering | Agent overengineers solutions and writes too much code | andrej-karpathy-skills, caveman |
| [obsidian-skills](https://github.com/kepano/obsidian-skills) | skill | Agent skills for Obsidian — teaches agents to use Obsidian CLI and open formats | Need AI agents to interact with Obsidian knowledge bases | — (domain-specific: Obsidian) |
| [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | skill | Comprehensive AI research and engineering skills library for any AI model | Want to turn coding agents into full-powered AI research agents | autoresearch, last30days-skill |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | skill | Persistent file-based planning that survives context loss, /clear, and crashes | Agent loses track of multi-step plans when context resets | GSD, feature-dev |
| [refly](https://github.com/refly-ai/refly) | platform | Open-source agent skills builder — define skills by vibe workflow, run across editors | Need to build and distribute custom skills without manual SKILL.md authoring | skill-creator, plugin-dev |
| [agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge) | skill | Generate 2D sprite sheets, transparent PNG frames, and animated GIFs from prompts | Need AI agents to create game art assets | — (domain-specific: game dev) |
| [open-design](https://github.com/nexu-io/open-design) | platform | Local-first design tool with 259+ skills, 142+ design systems, and sandboxed preview | Need a full design workflow (web, mobile, slides, video) driven by AI agents | impeccable, ui-ux-pro-max |
| [html-anything](https://github.com/nexu-io/html-anything) | tool | Agentic HTML editor — AI writes HTML across 9 surfaces (magazine, deck, poster, etc.) | Need AI to generate publication-quality HTML for specific formats | open-design |
| [fast-agent](https://github.com/evalstate/fast-agent) | framework | Code, build, and evaluate agents with excellent model and MCP/ACP support | Want a framework for building and evaluating custom agents | — |
| [arrow-js](https://github.com/standardagents/arrow-js) | framework | First UI framework for the agentic era — tiny, performant, with WASM sandboxes | Need a UI framework designed for safe agent-generated code execution | — |
| [claude-seo](https://github.com/AgriciDaniel/claude-seo) | skill | 25 SEO sub-skills + 18 sub-agents covering technical SEO, E-E-A-T, schema, GEO/AEO, and reporting | Need AI-assisted SEO analysis and optimization | — (domain-specific: SEO) |
| [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | plugin | 49 AI agents and 72 workflow skills mimicking a full game dev studio hierarchy | Want a complete AI game development workflow | — (domain-specific: game dev) |
| [gemini-skills](https://github.com/google-gemini/gemini-skills) | skill | Skills for Gemini API, SDK, and model/agent interactions | Need AI assistance with Gemini API workflows | google/skills |
| [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | skill | Academic research workflow: research, write, review, revise, finalize | Need structured academic writing assistance from AI agents | AI-Research-SKILLs |
| [Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills) | skill | 66 specialized skills for full-stack developers | Want a focused full-stack skill set for pair programming | mattpocock/skills, alirezarezvani/claude-skills |
| [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | skill | 754 cybersecurity skills mapped to MITRE ATT&CK, NIST CSF, D3FEND, and ATLAS frameworks | Need comprehensive security skills aligned with industry frameworks | trailofbits/skills, ghostsecurity/skills |
| [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | skill | Generates polished HTML slide decks with editorial magazine and Swiss layouts | Need AI to create presentation slides, not just code | open-slide, frontend-slides |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | skill | Create beautiful slides using a coding agent's frontend skills | Need web-based slide creation from AI agents | guizang-ppt-skill, open-slide |
| [Waza](https://github.com/tw93/Waza) | skill | Engineering habits turned into skills Claude can run | Want everyday engineering practices available as agent skills | mattpocock/skills, agent-skills |
| [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) | skill | Secure, validated skill registry for professional AI coding agents | Need security-validated skills with confidence guarantees | SkillSpector, antigravity-awesome-skills |
| [formkit](https://github.com/formkit/formkit) | framework | The form framework for coding agents | Need agent-optimized form building and validation | — (domain-specific: forms) |
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | tool | Google Workspace CLI for Drive, Gmail, Calendar, Sheets, Docs, Chat, and Admin with AI agent skills | Need agents to interact with Google Workspace services via CLI | google/skills |
| [claude-night-market](https://github.com/athola/claude-night-market) | plugin | 23 plugins: TDD hooks, git/PR workflows, spec-driven dev, multi-LLM delegation (186 skills) | Setting up TDD enforcement, code review, and workflow automation requires many separate tools | superpowers, compound-engineering, commit-commands |
| [SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill) | skill | SwiftUI agent skill for Claude Code, Codex, and other AI tools (4.1K stars) | AI agents generate outdated or incorrect SwiftUI code | — (domain-specific: SwiftUI) |
| [guard-skills](https://github.com/amElnagdy/guard-skills) | skill | Quality gates that catch AI-generated failure modes in code, tests, and docs | AI-generated code has distinct failure patterns not caught by traditional linters | code-review, pr-review-toolkit, trailofbits/skills |
| [huashu-design](https://github.com/alchaincyf/huashu-design) | skill | HTML-native design skill — hi-fi prototypes, slides, animations, MP4 export, 20 design philosophies (19.2K stars) | Agents generate generic HTML without design quality; need structured design with evaluation dimensions | impeccable, ui-ux-pro-max, open-design |
| [baoyu-design](https://github.com/JimLiu/baoyu-design) | skill | Run Claude Design locally as an agent skill — UI mockups, prototypes, decks, wireframes as HTML (1.6K stars) | Claude Design requires claude.ai; need the same design capability in local agent sessions | huashu-design, impeccable, ui-ux-pro-max |
| [AlphaGBM/skills](https://github.com/AlphaGBM/skills) | skill | Real-data options intelligence for AI agents — 29 skills for financial options analysis | AI agents lack domain knowledge for options trading and financial analysis | — (domain-specific: finance/options) |

## Code Review & Quality

Tools for automated code review, quality checks, and codebase improvement.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| code-review | plugin | Multi-agent code review with confidence-based scoring | Need automated review that catches real issues, not noise | pr-review-toolkit, shadcn/improve |
| pr-review-toolkit | plugin | PR review utilities: type analysis, silent failure hunting, test coverage, comment analysis | Need structured review dimensions beyond just "looks good" | code-review |
| [shadcn/improve](https://github.com/shadcn/improve) | tool | Use the most capable model to audit codebase, write plans for cheaper models to execute | Want high-quality codebase audits without burning expensive model tokens on execution | code-review |
| [stryker-js](https://github.com/stryker-mutator/stryker-js) | tool | Mutation testing for JS/TS — tests whether your tests actually catch bugs | Coverage says "tests exist" but not "tests are good"; mutation testing reveals weak test suites | — (unique: test quality verification) |
| [PR-Agent](https://github.com/The-PR-Agent/pr-agent) | tool | Open-source AI PR reviewer with auto-describe, review, improve, and custom prompts | Need automated PR review that adds descriptions, finds bugs, and suggests improvements | code-review, pr-review-toolkit |

## Maturity Frameworks

Frameworks for assessing and systematically improving how a codebase leverages AI-assisted development.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ACMM](https://arxiv.org/abs/2604.09388) | framework | 6-level AI Codebase Maturity Model defined by feedback loop topology, not autonomy | Teams plateau at "prompt and review" without a systematic progression path; tools without feedback loops produce chaos | agents-best-practices (complementary: ACMM = maturity model, ABP = implementation patterns) |

## Dev Workflow

Tools for git management, planning, project orchestration, and development process.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| GSD (Get Shit Done) | framework | Project orchestration: milestones, phases, planning, execution, and verification with 12 specialized agents | Need structured project management around AI-assisted development | superpowers (GSD is part of superpowers), feature-dev |
| [worktrunk](https://github.com/max-sixty/worktrunk) | tool | CLI for git worktree management, designed for parallel AI agent workflows | Need isolated git branches for multiple agents working simultaneously | dmux |
| [plannotator](https://github.com/backnotprop/plannotator) | tool | Annotate and review coding agent plans and code diffs visually, share with team | Agent plans are hard to review and discuss with teammates | planning-with-files (complementary: plannotator = visual review, planning-with-files = persistence) |
| commit-commands | plugin | Git workflow shortcuts: clean_gone, commit, commit-push-pr | Repetitive git operations slow down agent-assisted workflow | claude-code-action (complementary: commit-commands = local, CCA = CI) |
| [reporails/cli](https://github.com/reporails/cli) | tool | AI instructions diagnostics for Claude, Codex, Copilot, Cursor, Gemini agents | Don't know if CLAUDE.md / agent instructions are well-formed or conflicting | agnix (complementary: reporails = diagnostics, agnix = lint + LSP) |
| [CLI-Anything](https://github.com/HKUDS/CLI-Anything) | tool | Making all software agent-native via CLI wrappers | Existing tools don't expose interfaces that AI agents can use | — |
| feature-dev | plugin | Feature development workflow with planning, implementation, and verification stages | Need a structured feature development process with AI agents | GSD |
| [claude-code-router](https://github.com/musistudio/claude-code-router) | tool | Route and customize how you interact with Claude Code while inheriting upstream updates | Want to build coding infrastructure on Claude Code as a foundation layer | claude-code-templates, CLIProxyAPI |
| [aidlc-workflows](https://github.com/awslabs/aidlc-workflows) | framework | AWS adaptive three-phase dev lifecycle rules for AI coding agents across 6 editors | Unstructured AI-assisted development lacks phased gates, risk assessment, and cross-editor consistency | GSD, superpowers |
| [claude-code-action](https://github.com/anthropics/claude-code-action) | tool | Run Claude Code as a GitHub Action for CI/CD automation | Want AI agents to respond to issues/PRs automatically in CI pipelines | — (unique: CI integration) |
| [claude-task-master](https://github.com/eyaltoledano/claude-task-master) | tool | AI-powered task management for Cursor, Windsurf, Roo, and other editors | Need structured task breakdown and tracking across AI editors | GSD |
| [gsd-build](https://github.com/gsd-build/get-shit-done) | framework | Standalone GSD: meta-prompting and spec-driven dev for Claude Code | Want GSD methodology without the full superpowers plugin | GSD (superpowers), feature-dev |
| [docmd](https://github.com/docmd-io/docmd) | tool | Markdown-to-docs-site generator with MCP server and llms.txt for AI-native documentation | Need to publish docs that agents can also query programmatically | — (unique: AI-native docs site) |
| [claude-code-templates](https://github.com/davila7/claude-code-templates) | tool | CLI tool for configuring and monitoring Claude Code sessions | Need structured configuration and monitoring for Claude Code | ccstatusline, claude-hud |
| [capa](https://github.com/infragate/capa) | tool | One capabilities.yaml wires skills, tools, rules, agents, and MCP servers across 30+ AI editors | Configuring agent capabilities is per-tool; need a single config format portable across editors | reporails/cli (complementary: capa = config, reporails = diagnostics) |
| [skills-manage](https://github.com/iamzhihuix/skills-manage) | tool | Desktop app to manage AI coding agent skills across 20+ platforms from one place (2K stars) | Managing skills across Claude Code, Cursor, Codex, Gemini requires per-editor configuration | tolaria, capa |
| [align-dev](https://github.com/razr001/align-dev) | tool | Generate shared coding standards and SKILL.md so agents across teams write consistently | Multiple agents across a team generate inconsistent code; need shared standards generation | reporails/cli (complementary: align-dev = generate, reporails = validate) |
| [claude-hud](https://github.com/jarrodwatts/claude-hud) | plugin | Shows context usage, active tools, running agents, and todo progress in Claude Code | Can't see what's happening inside Claude Code sessions — context, tools, agents | ccstatusline, claude-code-templates |
| [ccstatusline](https://github.com/sirmalloc/ccstatusline) | plugin | Beautiful customizable statusline for Claude Code CLI with powerline and themes | Want a richer status display for Claude Code sessions | claude-hud, claude-code-templates |
| [agent-rules-books](https://github.com/ciembor/agent-rules-books) | skill | 13 classic engineering books distilled into CLAUDE.md rule sets with tiered token budgets | Want canonical software engineering principles (DDD, Clean Architecture, DDIA) as agent rules | mattpocock/skills, andrej-karpathy-skills |
| [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | skill | 140 scientific skills + 100 database connectors for biology, chemistry, medicine, and drug discovery | Need deep domain skills for scientific research and lab workflows | AI-Research-SKILLs, academic-research-skills |
| [openskills](https://github.com/numman-ali/openskills) | tool | Universal skills loader — installs SKILL.md to any agent (Claude Code, Cursor, Codex, Aider) | Skills are editor-specific; need a universal installer that works across all AI editors | refly, skill-creator |
| [agents (wshobson)](https://github.com/wshobson/agents) | plugin | Multi-harness plugin marketplace — 84 plugins, 192 agents, 156 skills across 6 editors | Need a single source of production-ready agents and skills for all AI coding tools | everything-claude-code, alirezarezvani/claude-skills, antigravity-awesome-skills |
| [agent-browser](https://github.com/vercel-labs/agent-browser) | tool | Browser automation CLI for AI agents — navigate, fill forms, screenshot, scrape, test web apps | Agents can't interact with web UIs for testing, verification, or data extraction | playwright, browser-use |
| [azure-skills](https://github.com/microsoft/azure-skills) | plugin | Official Azure agent plugin — skills and MCP configs for Azure scenarios (258K installs) | Need AI assistance with Azure deployment, infrastructure, and cloud workflows | microsoft/skills, google/skills |

## MCP Servers

Model Context Protocol servers that connect AI agents to external services and capabilities.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [context7](https://github.com/upstash/context7) | MCP server | Live documentation lookup with semantic search across library/framework docs | Agent's training data is outdated; needs current API docs | git-mcp (complementary: context7 = library docs, git-mcp = repo source) |
| [playwright](https://github.com/microsoft/playwright-mcp) | MCP server | Browser automation and testing from within agent sessions | Agent can't interact with web UIs or run browser tests | agent-browser, chrome-devtools-mcp, browser-use |
| [cloudflare-mcp](https://github.com/cloudflare/mcp-server-cloudflare) | MCP server | Cloudflare integration: workers, builds, bindings, observability | Need to manage Cloudflare infrastructure from agent sessions | awslabs/mcp (complementary: different cloud provider) |
| prisma | MCP server | Database operations via Prisma ORM (migrations, studio, status) | Agent needs to interact with databases during development | supabase, mcp-toolbox |
| sentry | MCP server | Error tracking and monitoring integration | Agent needs access to production error data for debugging | langfuse (complementary: sentry = errors, langfuse = LLM behavior) |
| [blender-mcp](https://github.com/ahujasid/blender-mcp) | MCP server | Blender 3D modeling integration | Need AI to control 3D modeling workflows | — |
| sequential-thinking | MCP server | Chain-of-thought reasoning enhancement via structured thinking steps | Agent's reasoning is shallow on complex problems | gentleman-book-mcp (complementary: sequential-thinking = reasoning, gentleman-book-mcp = architecture knowledge) |
| server-memory | MCP server | Basic persistent key-value memory | Need simple state persistence between agent calls | OMEGA, claude-mem |
| server-github | MCP server | GitHub operations (repos, issues, PRs, actions) | Agent needs to interact with GitHub beyond local git | github-mcp-server |
| [github-mcp-server](https://github.com/github/github-mcp-server) | MCP server | GitHub's official MCP server — repos, issues, PRs, actions, search, code navigation | Need first-party GitHub integration with full API coverage and official support | server-github |
| server-filesystem | MCP server | Local filesystem access with safety controls | Agent needs structured file operations with guardrails | — |
| exa-mcp-server | MCP server | Web search and research via Exa API | Agent needs to search the web for current information | firecrawl-mcp, Agent-Reach |
| firecrawl-mcp | MCP server | Web scraping and crawling | Agent needs to extract content from web pages | exa-mcp-server |
| fal-ai-mcp-server | MCP server | Image, video, and audio generation via fal.ai | Agent needs to generate media assets | — |
| token-optimizer-mcp | MCP server | 95%+ context reduction for tool outputs | Context window fills up too fast | headroom |
| browser-use | MCP server | AI browser agent for autonomous web interaction | Need agents to navigate and interact with web pages autonomously | playwright |
| evalview | MCP server | AI agent regression testing | Can't tell if agent behavior regressed after config changes | langfuse |
| squish-memory | MCP server | Local-first persistent memory runtime | Need memory that runs locally without external dependencies | OMEGA, claude-mem, server-memory |
| longhand | MCP server | Session history indexing for cross-session search | Need to find what happened in past agent sessions | OMEGA, claude-mem |
| devfleet | MCP server | Multi-agent orchestration via MCP | Need to coordinate agents through the MCP protocol rather than CLI | claude-squad, gastown |
| supabase | MCP server | Supabase database and auth operations | Agent needs to interact with Supabase projects during development | prisma |
| jira | MCP server | Jira issue tracking integration | Agent needs to read/update Jira tickets during development | github-mcp-server (complementary: Jira = issues, GitHub = code) |
| confluence | MCP server | Confluence wiki integration | Agent needs to read/write team documentation | gentleman-book-mcp (complementary: confluence = team wiki, gentleman = architecture book) |
| [chrome-devtools-mcp](https://github.com/benjaminr/chrome-devtools-mcp) | MCP server | Chrome DevTools Protocol integration — network, console, DOM, CSS, performance inspection | Need agents to inspect, debug, and profile web apps in Chrome, not just automate them | playwright (complementary: playwright = automation, chrome-devtools = inspection) |
| [mdn/mcp](https://github.com/mdn/mcp) | MCP server | MDN Web Docs lookup — current browser compatibility data and web platform documentation | Agent's training data has outdated web API info; needs accurate browser support tables | context7 |
| [fastmcp](https://github.com/PrefectHQ/fastmcp) | framework | Fast, Pythonic way to build MCP servers and clients with minimal boilerplate | Building MCP servers requires too much setup; need a framework that makes it easy | — (unique: MCP server builder) |
| [git-mcp](https://github.com/idosal/git-mcp) | MCP server | Remote MCP server for any GitHub project — eliminates code hallucinations | Agents hallucinate APIs and functions; need live repo context as MCP resource | context7 (complementary: context7 = library docs, git-mcp = repo source) |
| [awslabs/mcp](https://github.com/awslabs/mcp) | MCP server | Official AWS MCP servers for S3, Lambda, DynamoDB, CDK, and more | Need agents to interact with AWS services directly during development | cloudflare-mcp |
| [Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) | MCP server | Figma layout information for AI coding agents — bridge designs to code | Need agents to read Figma designs and translate them into code accurately | plumb-mcp, design-extract |
| [mcp-toolbox](https://github.com/googleapis/mcp-toolbox) | MCP server | Google's MCP server for databases — schema inspection, queries, migrations | Need agents to interact with databases via a standardized MCP interface | prisma, supabase |
| [gentleman-book-mcp](https://github.com/Alan-TheGentleman/gentleman-book-mcp) | MCP server | 18 chapters of software architecture knowledge accessible to AI agents | Agent lacks deep architecture knowledge for design decisions | book-to-skill (complementary: gentleman = fixed book, book-to-skill = any book) |
| [opendocswork-mcp](https://github.com/Aimino-Tech/opendocswork-mcp) | MCP server | Rust-native Office document processing — Excel, Word, PowerPoint at sub-millisecond speed | AI agents can't natively read or write Office documents | powerpoint, powerpoint-ppt |
| [plumb-mcp](https://github.com/tathagat22/plumb-mcp) | MCP server | Local Figma MCP server with no REST rate limits and a verification loop | Figma's official MCP has rate limits and metered tool-call quotas | Figma-Context-MCP |

## Observability

Tools for monitoring, debugging, and understanding AI agent behavior and performance.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [langfuse](https://github.com/langfuse/langfuse) | platform | Open source AI engineering: evals, observability, prompt management, datasets | Can't see what agents are doing, how well they perform, or where they fail | evalview |
| [tokencost](https://github.com/mr-beaver/tokencost) | tool | Track exactly what you spend on Claude CLI with cost optimization insights | Can't see how much agent sessions cost or where tokens are wasted | — (unique: cost tracking) |
| [Apache DevLake](https://github.com/apache/devlake) | platform | Open-source dev data platform: DORA metrics, engineering throughput, Grafana dashboards | Can't measure delivery performance (PR rates, lead time, MTTR) without building custom scripts | langfuse (complementary: DevLake = delivery metrics, langfuse = LLM behavior) |
| [Infracost](https://github.com/infracost/infracost) | tool | Cloud cost estimates for Terraform, CloudFormation, and CDK — in terminal, editor, agent, or CI | AI agents generate infrastructure code without knowing what it costs; need cost visibility before deploy | tokencost (complementary: Infracost = infra costs, tokencost = LLM token costs) |
| [abtop](https://github.com/graykode/abtop) | tool | Real-time TUI monitor for AI agent sessions — tokens, context %, rate limits, ports | Can't see what multiple agents are doing across projects without checking each one | tokencost, claude-hud |
| [Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3) | harness | Context management via hooks — ledgers, handoffs, and MCP execution without context pollution | Agents lose state across sessions and pollute context with MCP output | headroom, claude-mem |

## Research & Discovery

Tools for AI-assisted research, information gathering, and multi-model reasoning.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [autoresearch](https://github.com/karpathy/autoresearch) | tool | AI agents running automated research experiments | Research is tedious; want AI to run experiments autonomously | last30days-skill, AI-Research-SKILLs |
| [llm-council](https://github.com/karpathy/llm-council) | tool | Multiple LLMs work together to answer the hardest questions | Single model has blind spots; committee of models is more reliable | design-council (similar multi-perspective approach) |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | skill | Research any topic across Reddit, X, YouTube, HN, Polymarket, and the web | Need current sentiment and discussion, not just static docs | Agent-Reach |
| [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | tool | Give AI agents eyes to see the internet — read and search Twitter, Reddit, YouTube, GitHub, zero API fees | Need agents to access social/web content without paid APIs | last30days-skill, exa-mcp-server |
| [aisuite](https://github.com/andrewyng/aisuite) | framework | Simple unified interface to multiple generative AI providers | Switching between AI providers requires different SDKs and APIs | — |
| [PaperOrchestra](https://github.com/Ar9av/PaperOrchestra) | skill | Automated AI research paper writer with benchmark + autoraters, zero API keys | Writing research papers with AI requires manual orchestration | AI-Research-SKILLs, academic-research-skills |

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
| [cve-mcp-server](https://github.com/mukul975/cve-mcp-server) | MCP server | 27 security intelligence tools across 21 APIs — CVE, EPSS, CISA KEV, MITRE ATT&CK, Shodan | Security research requires querying many APIs manually; unifies vulnerability intelligence | ghostsecurity/skills, Anthropic-Cybersecurity-Skills |
| [pentest-ai](https://github.com/0xSteph/pentest-ai) | MCP server | Offensive-security MCP server with 205 tools, 17 specialist agents, 60 SPA-aware probes | Penetration testing involves many disconnected tools; unifies under MCP for agent-driven testing | ghostsecurity/skills, cve-mcp-server |
| [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | skill | Bug hunting and red-team skill bundle — 71 skills, 15 slash commands, 681 disclosed-report patterns | External security testing lacks structure; provides vulnerability-class-organized hunting patterns | ghostsecurity/skills, Anthropic-Cybersecurity-Skills, pentest-ai |
| [hol-guard](https://github.com/hashgraph-online/hol-guard) | tool | AI antivirus for developer agents — scans plugins, skills, MCP servers before tools run | Downloaded agent extensions could be malicious; need pre-execution scanning | SkillSpector, agentlint |
| [OpenOSINT](https://github.com/OpenOSINT/OpenOSINT) | MCP server | AI-powered OSINT agent with 16 tools for authorized security research | OSINT research requires querying many sources; agent-driven intelligence gathering | cve-mcp-server, pentest-ai |
| [agnix](https://github.com/agent-sh/agnix) | tool | Linter and LSP for AI coding configs — validates CLAUDE.md, AGENTS.md, SKILL.md, hooks, MCP | No validation for AI agent configuration files; errors are silent until runtime | SkillSpector (complementary: agnix validates config, SkillSpector scans for malice) |

## Reference

Curated lists, glossaries, and system prompt collections for learning and discovery.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentskills](https://github.com/agentskills/agentskills) | reference | Canonical open specification for portable AI agent skills (SKILL.md format) | No standard format for writing skills that work across agents and editors | — (unique: the spec itself) |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | reference | Curated skills, hooks, slash-commands, and agent orchestrators for Claude Code | Hard to discover what's available in the Claude Code ecosystem | awesome-claude-skills (travisvn), awesome-claude-skills (Composio) |
| [awesome-claude-skills (travisvn)](https://github.com/travisvn/awesome-claude-skills) | reference | Curated Claude Skills and customization tools | Need a catalog of available skills to evaluate | awesome-claude-code, awesome-claude-skills (Composio) |
| [awesome-claude-skills (Composio)](https://github.com/ComposioHQ/awesome-claude-skills) | reference | Curated list of Claude Skills and customization resources | Need a catalog of available skills to evaluate | awesome-claude-code, awesome-claude-skills (travisvn) |
| [awesome-llm-agents](https://github.com/kaushikb11/awesome-llm-agents) | reference | Curated list of LLM agent frameworks and tools | Need to discover agent frameworks beyond Claude Code ecosystem | awesome-ai-agents |
| [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) | reference | List of AI autonomous agents and platforms | Need to discover standalone AI agent projects | awesome-llm-agents |
| [dictionary-of-ai-coding](https://github.com/mattpocock/dictionary-of-ai-coding) | reference | AI coding jargon explained in plain English | Terms like "harness", "skill", "agent" are overloaded and confusing | — |
| [system-prompts-and-models](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) | reference | Full system prompts from AI coding tools (Cursor, Devin, Windsurf, Claude Code, etc.) | Want to understand how competing AI tools work under the hood | claude-code-system-prompts (subset: Claude Code only) |
| [ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) | reference | Learn AI engineering: build it, ship it for others | Need a learning path for AI engineering concepts | — |
| [awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills) | reference | Curated list of practical Codex skills for automating workflows | Need a catalog of Codex-specific skills to evaluate | awesome-claude-skills, awesome-agent-skills |
| [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | reference | 1000+ agent skills from official dev teams and community, cross-editor compatible | Need a comprehensive skills catalog across all major AI editors | awesome-claude-skills, antigravity-awesome-skills |
| [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) | reference | 5,400+ skills filtered and categorized from the official OpenClaw Skills Registry | Need the broadest possible skills discovery across the ecosystem | awesome-agent-skills, antigravity-awesome-skills |
| [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | reference | 1,500+ installable agentic skills with CLI installer and bundles | Need bulk-installable skill collections with workflow bundles | awesome-agent-skills, awesome-openclaw-skills |
| [tolaria](https://github.com/refactoringhq/tolaria) | tool | Desktop app to manage markdown knowledge bases | Need a visual editor for CLAUDE.md, skills, and documentation files | skills-manage (complementary: tolaria = edit files, skills-manage = manage installations) |
| [claude-howto](https://github.com/luongnv89/claude-howto) | reference | Visual, example-driven guide to Claude Code from basics to advanced agents | Need a structured learning path for Claude Code with copy-paste templates | claude-code-tips, learn-claude-code |
| [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | reference | From vibe coding to agentic engineering — comprehensive best practices guide | Want proven patterns for getting the most out of Claude Code | claude-howto, claude-code-tips |
| [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) | reference | Build a Claude Code-like agent harness from scratch — educational deep dive | Want to understand how agent harnesses work by building one | claude-howto, claude-code-system-prompts |
| [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | reference | All parts of Claude Code's system prompt, 27 tool descriptions, sub-agent prompts | Want to understand Claude Code's internal architecture and prompts | system-prompts-and-models, learn-claude-code |
| [claude-code-tips](https://github.com/ykdojo/claude-code-tips) | reference | 43 tips for getting the most out of Claude Code with status line script and container setup | Need practical tips and tricks for Claude Code power users | claude-code-best-practice, claude-howto |
| [claude-code](https://github.com/anthropics/claude-code) | reference | Official Claude Code repository — source of truth for features, issues, and releases | Want to track Claude Code development, file issues, or understand capabilities | — |
| [awesome-agent-skills (libukai)](https://github.com/libukai/awesome-agent-skills) | reference | Agent Skills ultimate guide with quick start, resources, and curated tools | Need a comprehensive Chinese-language guide to the skills ecosystem | awesome-agent-skills (VoltAgent) |
| [buildwithclaude](https://github.com/davepoon/buildwithclaude) | reference | Hub for finding Claude skills, agents, commands, hooks, plugins, and marketplace collections (3.1K stars) | Discovering Claude Code extensions is fragmented across GitHub, npm, and skills.sh | awesome-claude-code, awesome-claude-skills |
| [agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices) | skill | Provider-neutral agent skill for Codex, Claude Code, and agentic harness design (2K stars) | Agent design best practices are scattered; provides a consolidated reference | claude-code-best-practice, andrej-karpathy-skills |
| [design-extract](https://github.com/Manavarya09/design-extract) | MCP server | Extract any website's complete design system — DTCG tokens, multi-platform emitters, WCAG remediation (3.3K stars) | Manual design-token extraction is slow and error-prone | Figma-Context-MCP, web-quality-skills |
| [karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki) | skill | Agent Skills-compatible LLM wiki — build knowledge bases from raw sources with citations (1.2K stars) | LLM knowledge is scattered; need a structured wiki skill agents can query with citations | andrej-karpathy-skills, gentleman-book-mcp, book-to-skill |
| [ctx](https://github.com/stevesolun/ctx) | tool | Skill, agent, MCP, and harness recommendations via 102K-node LLM-wiki graph (516 stars) | Finding the right skill/agent/MCP for a task requires manual search | awesome-claude-code, awesome-agent-skills, buildwithclaude |
