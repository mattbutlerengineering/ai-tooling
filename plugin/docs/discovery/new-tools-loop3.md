# New Tools Evaluation (Loop 3)

Catalog tools without dedicated evaluations, assessed for WORKFLOW.md inclusion.

## CLI-Anything
**Repo:** [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything)
**Stars:** 43,149 | **Last updated:** 2026-06-14 | **Forks:** 4,043
**What it does:** Auto-generates production-grade, agent-native CLI interfaces for any software via a 7-phase pipeline (analyze, design, implement, test, document, publish). Outputs Click-based Python CLIs with REPL mode, structured `--json` output, and SKILL.md discovery files. Ships 30+ pre-built harnesses covering GIMP, Blender, LibreOffice, FFmpeg, OBS, Draw.io, and more.
**Current workflow alternative:** Nothing in the current workflow covers this. MCP servers expose specific APIs; custom MCP server authoring requires manual integration per tool.
**Key difference:** Targets the long tail of professional desktop and creative software that has no API and no MCP server — GIMP, Blender scripting, LibreOffice, video editors — and auto-generates the entire integration layer including tests and agent-discovery metadata.

**Verdict:** CONDITIONAL at L3
**Justification:** At 43K stars this is a major project solving a real gap. However, most developers (web, backend, API work) won't need to control GIMP or Blender from an agent. The "fewer tools, more feedback loops" principle means this earns a slot only for teams whose workflow involves desktop or creative software that lacks CLI interfaces. When it applies, it's genuinely transformative — but it doesn't create feedback loops, so it shouldn't be in the default L3 stack.

---

## chrome-devtools-mcp
**Repo:** [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)
**Stars:** 43,699 | **Last updated:** 2026-06-14 | **Forks:** 2,813
**What it does:** MCP server that gives agents access to Chrome DevTools Protocol — browser automation (click, type, navigate), network request inspection, console messages with source-mapped stack traces, memory heap snapshots, and performance profiling via Chrome traces and the CrUX API. Connects via Puppeteer to launched or already-running Chrome instances.
**Current workflow alternative:** The `playwright` MCP server covers browser automation and testing. `sentry` MCP covers production error monitoring.
**Key difference:** Oriented toward debugging and profiling a live app under development, not test automation. Exposes Chrome internals — heap snapshots, performance traces, source-mapped stack traces, network inspection — that playwright doesn't surface. The ability to attach to an already-running Chrome instance is uniquely useful for debugging a session the developer is actively using.

**Verdict:** CONDITIONAL at L3 for frontend-heavy work
**Justification:** For backend or CLI projects, playwright covers the browser automation need. For frontend-heavy work, the debugging and profiling capabilities (heap snapshots, performance traces, network inspection with source maps) fill a real gap. At 43K stars and active daily maintenance, this is well-validated. Add it when regularly debugging frontend perf or runtime errors in Chrome.

---

## claude-subconscious
**Repo:** [letta-ai/claude-subconscious](https://github.com/letta-ai/claude-subconscious)
**Stars:** 2,797 | **Last updated:** 2026-05-13 | **Forks:** 205
**What it does:** A background Letta agent that passively observes Claude Code sessions via hooks (Stop, UserPromptSubmit, PreToolUse), processes transcripts asynchronously, and injects structured memory blocks (directives, preferences, project context, pending items) into subsequent sessions — without touching CLAUDE.md. Memory is scoped to a shared agent brain at `~/.letta/claude-subconscious/` plus per-project conversation mappings.
**Current workflow alternative:** claude-mem (L4) provides cross-session persistence via explicit commands. OMEGA memory requires manual `omega_store()` calls.
**Key difference:** Fully passive and automatic — no memory commands ever issued by the developer. It learns from transcripts in the background and injects context silently. The tradeoff is opacity: you don't know what it remembers or why, and it requires a running Letta server.

**Verdict:** CONDITIONAL at L4 as alternative to claude-mem
**Justification:** The passive transcript-learning model solves a real problem: developers forget to run memory commands, so explicit-memory tools degrade in practice. However, requiring a Letta server adds infra overhead, memory is a black box with no easy audit, and it overlaps heavily with claude-mem. Best fit for teams who want zero-friction memory without building the habit of explicit commands.

---

## tokencost
**Repo:** [mr-beaver/tokencost](https://github.com/mr-beaver/tokencost)
**Stars:** 73 | **Last updated:** 2026-06-12 | **Forks:** 3
**What it does:** A local proxy (localhost:8082) that intercepts all LLM API traffic and provides real-time cost tracking, a live dashboard with per-session/model/task breakdowns, a macOS menu bar widget, and automatic optimizations — prompt caching, smart model routing, thinking budget caps, and message deduplication. Covers 218 models across 15+ providers. Integration is a single env var: `ANTHROPIC_BASE_URL=http://localhost:8082`.
**Current workflow alternative:** langfuse (L3) handles general observability — traces, evals, prompt management, performance over time. Nothing in the current stack targets cost-specific visibility or automated spend reduction.
**Key difference:** Cost-first rather than trace-first. Langfuse tells you what your agents are doing and how well; tokencost tells you what they cost and cuts that cost automatically via proxy-side optimizations.

**Verdict:** SKIP (concept is sound but project too small to recommend)
**Justification:** At 73 stars and 3 forks, this project has near-zero community validation. The concept of cost-tracking proxy with automatic optimizations is genuinely useful, but the recommended workflow shouldn't depend on a project this early-stage. If it gains traction (1K+ stars, active community), reconsider for L3 alongside langfuse. The cost visibility gap is real — watch this space.
