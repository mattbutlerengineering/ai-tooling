# Agent Harnesses

Comparative evaluation of agent harness frameworks — tools that structure how a coding agent operates.

## Evaluation Criteria

- **Repo health** — stars, recency, activity, community size
- **Methodology** — what workflow it enforces and how rigidly
- **Scope** — what it covers: TDD, debugging, review, verification, planning, etc.
- **Integration** — Claude Code native? Multi-editor support?
- **Flexibility** — rigid methodology vs. configurable components
- **Maintenance** — actively maintained? Responsive to issues?

---

## Tool Comparisons

### superpowers

**Repo:** [obra/superpowers](https://github.com/obra/superpowers)
**Stars:** 228K | **Forks:** 20K | **Last updated:** 2026-06-16 | **License:** MIT | **Language:** Shell

**What it actually does:** A complete software development methodology delivered as composable skills. Skills auto-trigger based on context — brainstorming fires before creative work, TDD fires before implementation, systematic debugging fires on errors, verification fires before completion claims. The core loop is: brainstorm → spec → plan → subagent-driven development → review → verify. Also includes GSD (Get Shit Done) for project orchestration with milestones, phases, and 12 specialized agents.

**Strengths:**
- Largest community by far (228K stars) — battle-tested across thousands of users
- Skills are composable and auto-triggering — you don't invoke them manually, they activate contextually
- Covers the full development lifecycle: brainstorming, planning, TDD, debugging, code review, verification, git worktrees
- Multi-editor: Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot CLI, OpenCode, Factory Droid
- GSD framework adds structured project management (milestones, phases, verification)
- Plugin marketplace distribution — easy install via `/plugin install superpowers`
- Actively hiring for dedicated maintenance

**Weaknesses:**
- 286 open issues — large issue backlog suggests some bugs go unfixed
- Auto-triggering skills can be overzealous — sometimes fires brainstorming when you just want to make a quick edit
- GSD adds significant complexity (12 agents, 35 commands) — steep learning curve
- Shell-based — harder to extend than TypeScript-based alternatives

---

### gstack

**Repo:** [garrytan/gstack](https://github.com/garrytan/gstack)
**Stars:** 110K | **Forks:** 16K | **Last updated:** 2026-06-14 | **License:** MIT | **Language:** TypeScript

**What it actually does:** A role-based agent configuration where Claude Code acts as a virtual engineering team — CEO (product rethink), eng manager (architecture lock), designer (catch AI slop), reviewer (find production bugs), QA lead (real browser testing), security officer (OWASP + STRIDE audits), release engineer (ships PR). 23 specialists and 8 power tools, all slash commands.

**Strengths:**
- Role-based approach is intuitive — `/review`, `/qa`, `/cso`, `/ship` map to real engineering roles
- Includes real browser-based QA (`/qa` opens a real browser and tests)
- Security auditing built-in (`/cso` runs OWASP + STRIDE)
- Team mode — auto-update for shared repos, teammates get gstack automatically
- TypeScript-based — easier to extend
- Office hours concept (`/office-hours`) — interrogation before building, similar to superpowers brainstorming
- OpenClaw integration for spawning Claude Code sessions

**Weaknesses:**
- 679 open issues — even larger backlog than superpowers
- No TDD enforcement — review and QA happen after code is written, not test-first
- No systematic debugging methodology — `/investigate` exists but is less structured
- Requires Bun runtime — additional dependency
- More opinionated about roles than methodology — tells agents what to be, not how to work
- git clone installation (not plugin marketplace) — more friction

---

### ECC

**Repo:** [affaan-m/ECC](https://github.com/affaan-m/ECC)
**Stars:** 216K | **Forks:** 33K | **Last updated:** 2026-06-15 | **License:** MIT | **Language:** JavaScript

**What it actually does:** Self-described as "the harness-native operator system for agentic work." A comprehensive system covering skills, instincts, memory optimization, continuous learning, security scanning, and research-first development. Works across 7+ editors (Codex, Claude Code, Cursor, OpenCode, Gemini, Zed, GitHub Copilot). v2.0.0 adds the Hermes operator — a cross-harness agent orchestration layer.

**Strengths:**
- Massive community (216K stars, 33K forks, 230+ contributors) — second only to superpowers
- Broadest editor support (7+ harnesses) — if you switch between editors, ECC follows
- Security scanning built-in (AgentShield npm package)
- GitHub App for PR audits — integrates at the repo level, not just locally
- Cross-harness architecture — agents can work across different editors
- Pro tier available ($19/seat/mo) for private repos — indicates commercial viability
- npm distribution (`ecc-universal`) — standard install path

**Weaknesses:**
- Complexity — tries to be everything (operator system, cross-harness, security, memory, learning)
- "Instincts" and "operator" abstractions are novel but add learning curve
- Pro/paid tier for private repos — free tier may have limitations
- 12+ language ecosystem support sounds impressive but spreads attention thin
- README is heavy on marketing badges, light on actual methodology description
- Hermes operator (v2) is new and may not be mature

---

### ruflo

**Repo:** [ruvnet/ruflo](https://github.com/ruvnet/ruflo)
**Stars:** 60K | **Forks:** 7K | **Last updated:** 2026-06-15 | **License:** MIT | **Language:** TypeScript

**What it actually does:** Multi-agent AI harness with a Rust-based engine. Orchestrates 100+ specialized agents across machines with coordinated swarms, self-learning memory, federated communications, and enterprise security. Two install paths: lightweight Claude Code plugin (slash commands only) or full CLI install with MCP server, hooks, daemon, and 98 agents.

**Strengths:**
- Most ambitious scope — federation allows agents across machines to collaborate securely
- Rust-based engine for performance (Cognitum.One)
- Self-learning loop — agents learn from successful patterns automatically
- 33 plugins covering core, memory, knowledge graphs, RAG, trading, and more
- Full CLI install gives you MCP server, hooks, and daemon — deep integration
- Vector database (AgentDB) and knowledge graphs built-in

**Weaknesses:**
- 650 open issues — largest backlog of all tools evaluated
- Scope creep — 98 agents, 60+ commands, 30 skills is overwhelming
- "22.2M+ ecosystem downloads" claim needs scrutiny — badge links to a proof JSON file, not npm stats
- Federation and cross-machine orchestration is enterprise-grade complexity for solo devs
- Two install paths create confusion about what you actually get
- Heavy infrastructure — daemon, MCP server, hooks — for what could be a simpler problem
- More focused on orchestration than development methodology (no TDD, no systematic debugging)

---

### compound-engineering

**Repo:** [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
**Stars:** 21K | **Forks:** 2K | **Last updated:** 2026-06-16 | **License:** MIT | **Language:** TypeScript

**What it actually does:** An engineering methodology built around the idea that each unit of work should make the next unit easier. Core loop: brainstorm requirements → plan implementation → execute with worktrees → review → compound learnings. The "compound" step (`/ce-compound`) explicitly documents what was learned so future agents start with better context. Also includes strategy capture (`/ce-strategy`), product pulse reports, and ideation.

**Strengths:**
- Clearest philosophy — "each unit of work makes the next easier" is a concrete, measurable goal
- Compounding mechanism is unique — `/ce-compound` explicitly captures learnings after each cycle
- Strategy layer (`/ce-strategy`, `/ce-product-pulse`) — ties engineering to product outcomes
- Clean workflow: brainstorm → plan → work → review → compound
- Includes `/ce-debug` for systematic debugging
- Multi-editor: Claude Code, Cursor, Codex
- 37 skills and 51 agents — comprehensive but not overwhelming
- Well-documented philosophy (blog posts explaining the thinking)

**Weaknesses:**
- Smallest community (21K stars) — least battle-tested
- 98 open issues — proportionally high for the star count
- No TDD enforcement — review happens after implementation, not test-first
- No auto-triggering — you manually invoke `/ce-brainstorm`, `/ce-plan`, etc.
- Strategy/product-pulse features assume a product context — less relevant for library or infrastructure work
- From Every (a media company) — engineering focus may drift toward content/product work

---

## Verdict

**Recommended: superpowers**

**Why:** It's the only harness that enforces TDD as a core methodology (test-first, not test-after). The auto-triggering skill system means the methodology is followed without manual discipline — brainstorming fires before you build, verification fires before you claim done, debugging fires before you guess at fixes. The GSD layer adds project orchestration without requiring it. 228K stars and active maintenance (hiring a dedicated community engineer) mean issues get surfaced and fixed. Multi-editor support means it works if you switch tools.

The key differentiator: superpowers changes *how agents think about work*, not just what commands are available. The other tools give you slash commands to invoke; superpowers intercepts the agent's workflow and redirects it through a disciplined methodology automatically.

**Runner-up: compound-engineering**

Pick compound-engineering when:
- You want a lighter-weight methodology without auto-triggering (more control, less magic)
- The "compound learnings" step matters to you — explicitly capturing what was learned after each cycle is unique and aligns with ACMM's continuous improvement philosophy
- You're building a product (not a library) and want strategy/product-pulse features

**When to consider ECC instead:**
- You work across 5+ different editors and need a single harness that follows you everywhere
- You need the GitHub App for automated PR audits on private repos
- Cross-harness agent orchestration (Hermes) is a real requirement

**Skip gstack and ruflo:**
- gstack: strong on roles and QA (real browser testing is excellent), but lacks TDD and systematic debugging. The role-based approach doesn't enforce methodology — it just gives agents personas.
- ruflo: impressive engineering (Rust engine, federation, swarms) but solves orchestration problems most solo devs don't have. 98 agents and 650 open issues suggest scope exceeds capacity.
