# Evaluation: claude-task-master (Taskmaster)

**Repo:** [eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master)
**Stars:** 27,612 | **Last updated:** 2026-04-28 (last *code* release `task-master-ai@0.43.1`, 2026-03-31; commits since are URL/branding chores) | **License:** MIT with Commons Clause
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (primary: PRD→tasks breakdown + tracking); spans Implement/Verify via the autopilot TDD loop
**Layer:** Tooling (an installable MCP server + CLI, with a Process workflow layered on top)

---

## What it does

Catalog one-liner: "AI-powered task management for Cursor, Windsurf, Roo, and other editors." Taskmaster is a Node CLI (`task-master-ai` on npm) and a bundled MCP server that turns a Product Requirements Document into a structured, dependency-aware task list and then tracks that list as you implement it. The core loop: write a PRD at `.taskmaster/docs/prd.txt`, run `parse-prd` (an LLM call) to generate `.taskmaster/tasks/tasks.json` — a list of tasks each with `id`, `title`, `description`, `status` (pending/in-progress/blocked/done/deferred/cancelled), `dependencies`, `priority`, `details`, `testStrategy`, and nested `subtasks`, validated with Zod strict schemas for cross-provider structured-output compatibility. From there `next` surfaces the next unblocked task (respecting the dependency graph, not just sequential order), `expand` breaks a task into subtasks, `analyze-complexity` scores each task 1-10 with an AI pass and recommends how many subtasks to split it into, and `set-task-status` moves tasks through states. Tasks are stored as a committed `tasks.json` plus generated per-task `.txt` files, with "tags" acting as parallel workstreams you can move tasks between.

The AI work is provider-agnostic: it needs at least one model key (Anthropic, OpenAI, Gemini, Perplexity, xAI, OpenRouter, Groq, Azure, Ollama, etc.) configured as main / research / fallback roles, with a dedicated **research** role (typically Perplexity) that pulls fresh external information into task context. Beyond planning, the newer **autopilot** subsystem (`apps/cli/src/commands/autopilot/*`: `start`/`next`/`commit`/`complete`/`resume`/`abort`/`finalize`) puts a TDD-and-git loop "on rails": per subtask it creates a tag+task-id branch, generates failing tests (a "Surgical Test Generator" agent), implements to green, commits only on passing tests, never commits to the default branch, persists run state under `.taskmaster/reports/runs/`, and opens a PR — a resumable autonomous executor, not just a planner.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection via the GitHub API — **I did not install the MCP server, run `task-master init`, or execute a parse-PRD/autopilot loop.** Installing would mutate editor MCP config (`claude mcp add`), require provider API keys, and write a `.taskmaster/` tree, so it was out of scope for a read-only eval. Evidence comes from repo metadata, the full README, the Claude Code plugin manifests, the command/agent file manifest, the task-structure docs, the autopilot command tree + design doc, and the commit/release history.

```bash
gh api repos/eyaltoledano/claude-task-master --jq '{stars,license,description,pushed_at,forks,open_issues}'
# 27,612 stars, NOASSERTION (MIT + Commons Clause), 2,595 forks, 196 open issues, created 2025-03-04
gh api repos/eyaltoledano/claude-task-master/readme --jq '.content' | base64 -d
gh api repos/eyaltoledano/claude-task-master/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d
gh api repos/eyaltoledano/claude-task-master/contents/CLAUDE_CODE_PLUGIN.md --jq '.content' | base64 -d
gh api repos/eyaltoledano/claude-task-master/contents/docs/task-structure.md --jq '.content' | base64 -d
gh api "repos/eyaltoledano/claude-task-master/git/trees/main?recursive=1" --jq '.tree[].path'
# packages/claude-code-plugin/{commands/*.md (49), agents/{task-orchestrator,task-executor,task-checker}.md}
# apps/cli/src/commands/autopilot/{start,next,commit,complete,resume,abort,finalize,status}.command.ts
gh api repos/eyaltoledano/claude-task-master/contributors --jq 'length'   # 30
gh api 'repos/eyaltoledano/claude-task-master/commits?per_page=8' --jq '.[] | {date,msg}'
# last code release v0.43.1 (2026-03-31); commits since = URL-redirect / tryhamster.com branding chores
```

## What worked

- **First-class Claude Code integration — three real install surfaces, not just "agent-agnostic."** (1) Native MCP: `claude mcp add taskmaster-ai -- npx -y task-master-ai`. (2) A Claude Code **plugin marketplace** (`.claude-plugin/marketplace.json`): `/plugin marketplace add eyaltoledano/claude-task-master` then `/plugin install taskmaster@taskmaster`, shipping 49 slash commands (`/tm:*`) and 3 agents (`task-orchestrator`, `task-executor`, `task-checker`) from `packages/claude-code-plugin/`. (3) Claude Code as a model **provider** with no API key (`claude-code/sonnet`, `claude-code/opus`) using the local Claude instance. It is one of the most thoroughly Claude-Code-integrated tools in the catalog.
- **The PRD→tasks→dependency-graph→`next` loop is the actual product, and it is well-specified.** Zod-strict `tasks.json` with explicit `dependencies` plus a `next` command that returns the next unblocked task is genuine dependency-aware scheduling, not just a checklist; `validate-dependencies`/`fix-dependencies` catch circular refs. `analyze-complexity` (1-10 scoring → recommended subtask count) avoids over-decomposing simple tasks.
- **Token-budget awareness is unusually mature.** `TASK_MASTER_TOOLS` loads `core` (7 tools, ~5K tokens), `standard` (15, ~10K), or `all` (36, ~21K) — a direct, documented answer to MCP context bloat that most MCP servers ignore.
- **Autopilot adds a real Implement/Verify layer with safety rails.** The design doc enforces "never commit to the default branch," "commit only after green tests," and resumable run state — concrete guardrails, not vibes. This pushes Taskmaster past planning into supervised execution.
- **Strong base maturity signals.** 27.6K stars, 30 contributors, ~1,200 commits, on npm with heavy downloads, CI, changesets-based releases, a backing company (Hamster), and Claude-powered repo automation (issue triage/dedupe/docs-update GitHub Actions).

## What didn't work or surprised us

- **Active development has stalled since the commercial pivot.** Last meaningful code release is v0.43.0/0.43.1 (Jan/Mar 2026); every commit since (through the 2026-04-28 `pushed_at`) is a URL-redirect or `tryhamster.com` branding chore (`fix: replace retired task-master.dev URLs`, `chore: update README docs links`). The team appears focused on the commercial Hamster product, with 196 open issues against a near-frozen OSS core. Evaluate v0.43.1 as roughly the final state, not a moving target.
- **Heavy overlap with the user's installed GSD — same job, different mechanism.** GSD already does requirements → roadmap → phases → plan-phase → execute-phase → verify, with dependency-aware planning, parallel executor agents, atomic commits, persistent `.planning/` state, and a TDD/verify loop. Taskmaster's `tasks.json` + `next` + autopilot covers the *same* Plan→Implement→Verify territory. Running both means two competing task/state systems (`.taskmaster/` vs `.planning/`) — redundant, not additive, for this user.
- **External dependency that wants API keys and a model budget.** Every planning action (`parse-prd`, `expand`, `analyze-complexity`, `research`) is an LLM call billed to a provider key, and the recommended research role implies a Perplexity subscription. The `claude-code/sonnet` provider removes the key requirement but not the token spend. GSD runs inside the existing Claude Code session with no separate key.
- **Commons Clause, not plain MIT.** Forbids selling Taskmaster itself or offering it as a hosted service — fine for internal use, but not OSI-open like spec-kit (MIT) or gstack (MIT).
- **Cursor-first design; single-file JSON storage.** README, one-click deeplink, and docs lead with Cursor — Claude Code is excellent but documented as one of several editors. Tasks live in a single `tasks.json` with no DB/indexing/concurrency protection: fine solo, fragile for teams.
- **Not hands-on validated here.** Task-generation quality, `next` scheduling on a real graph, and autopilot's green-rate rest on docs and source, not an observed run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | PRD→tasks with an explicit dependency graph and `next` scheduling forces structured breakdown before coding; autopilot's "commit only on green" enforces test-passing increments |
| Speed | + (large/multi-session) / - (small) | Durable `tasks.json` + `next` makes long, multi-session projects resumable without re-planning; the parse/expand/analyze ceremony is overhead for a bug fix or one-off change |
| Maintainability | neutral/+ | Committed `tasks.json`, per-task files, and tags persist intent/progress in the repo; offset by single-file JSON storage with no indexing or concurrent-access protection |
| Safety | neutral/+ | Autopilot guardrails (no commits to default branch, green-gated commits, resumable state) add real rails; but it's an external MCP server holding multiple provider API keys |
| Cost Efficiency | - | Every plan/expand/analyze/research action is a billed LLM call to a separate provider; `TASK_MASTER_TOOLS` trims context tokens but not the per-action model spend |

## Verdict

**CONDITIONAL** (for the general catalog) — leaning **SKIP for this specific user** due to GSD overlap and the stalled OSS core.

Taskmaster is a genuinely well-built, deeply-integrated tool: the PRD→tasks→dependency-graph→`next` loop is the real product (Zod-typed, dependency-aware, not persona theater), Claude Code is a first-class citizen across MCP, a plugin marketplace, *and* a keyless model provider, and the autopilot TDD-on-rails subsystem extends it credibly into supervised execution. For a team that wants cross-editor, durable, dependency-aware task tracking shared between Cursor/Windsurf/VS Code/Claude Code — especially mixed-IDE teams — it earns **CONDITIONAL: adopt when you need editor-portable structured task management backed by a committed `tasks.json`**, with the caveat that the OSS core looks frozen at v0.43.1 so treat it as a stable-but-static dependency.

For **this user**, who already runs **GSD**, it is largely **redundant**: GSD covers the same Plan→Implement→Verify loop (roadmap/phases/dependency-aware planning/parallel executors/atomic commits/persistent state/TDD verification) natively inside the Claude Code session with no extra API key or model budget. Adopting Taskmaster would mean two competing task/state frameworks; prefer it over GSD only if cross-editor portability or a shared `tasks.json` artifact for non-Claude-Code teammates is a hard requirement. Versus **spec-kit** (also CONDITIONAL): spec-kit produces durable *spec* artifacts (what/why → how → tasks) as a process; Taskmaster produces a durable *task-tracking* artifact with scheduling and an execution engine. They are complementary in principle (spec-kit plans, Taskmaster tracks), but both overlap GSD, so stacking all three on this user's setup is not warranted. Note the **Commons Clause** license caveat versus the plain-MIT alternatives.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-task-master](https://github.com/eyaltoledano/claude-task-master) | tool | AI task-management MCP server + CLI: PRD→dependency-aware tasks.json, `next` scheduling, complexity analysis, and an autopilot TDD loop, across Cursor/Windsurf/VS Code/Claude Code (27.6K stars) | Need structured, durable, dependency-aware task breakdown and progress tracking shared across AI editors | GSD, spec-kit, BMAD-METHOD, OpenSpec |
