# Evaluation: devfleet (Claude DevFleet)

**Repo:** [LEC-AI/claude-devfleet](https://github.com/LEC-AI/claude-devfleet)
**Stars:** 16 | **Last updated:** 2026-05-28 | **License:** Apache-2.0
**Dev loop stage:** Implement (also Plan — AI project planner; Ship — auto-merge of worktree branches)
**Layer:** Infrastructure (a coordination service, not a single tool)

---

## Repo identification

The catalog entry "devfleet — Multi-agent orchestration via MCP" was **unlinked**. `gh search repos devfleet` returns ~18 repos sharing the name; most are unrelated (a transport-fleet API, a Node.js project launcher, a PR-review bot, a distributed job runner). The entry's one-liner — "Multi-agent orchestration via MCP" — maps cleanly to **`LEC-AI/claude-devfleet`** ("Claude DevFleet"), and to nothing else in the result set:

- Its own description: "Multi-agent coding platform that dispatches Claude CLI agents... MCP-powered tools... coordinate autonomously."
- It is the only candidate that frames itself as multi-agent **orchestration** AND is built on MCP, AND has any traction (16 stars, 6 forks, Apache-2.0, ~24 pages of commit history).
- The one near-rival, `42433422/devfleet` ("multi-device controller with Trae, Codex CLI and MCP"), is 4 days old, 0 stars, no license, and is a device-fan-out controller, not an orchestration platform.

Confidence is **high but not certain** — the catalog string is generic and no provenance link existed to confirm against. I am proceeding on `LEC-AI/claude-devfleet` as the best-supported match and flag that the catalog row should be linked to it (or the entry retired if a different source was intended).

## What it does

Catalog one-liner: "Multi-agent orchestration via MCP." Claude DevFleet is a self-hosted platform (FastAPI + SQLite backend, React 19 + Vite UI, Docker or local venv) that dispatches Claude Code agents to work on "missions" (coding tasks) and coordinates them autonomously. MCP is the connective tissue at two layers, which is what distinguishes it from the worktree-cockpit tools in this cluster.

The mechanism: you create a project (pointed at a git repo) and missions. Dispatching a mission spawns a Claude Code agent (via the `claude-code-sdk` Python API by default, or the `claude` CLI subprocess as a fallback engine) in an **isolated git worktree/branch**, auto-merged on success — the same isolation primitive as dmux/gastown. Every dispatched agent is automatically given **two built-in stdio MCP servers**: a *context* server (`get_mission_context`, `get_project_context`, `get_session_history`, `get_team_context`, `read_past_reports`) so an agent can see requirements, prior reports, and what its peers are doing; and a *tools* server (`submit_report`, `create_sub_mission`, `request_review`, `get_sub_mission_status`, `list_project_missions`) so an agent can decompose its own work into sub-missions and file structured reports. A background **mission watcher** polls for missions whose `depends_on` dependencies are satisfied and auto-dispatches them to free agent slots (default `DEVFLEET_MAX_AGENTS=3`); a **scheduler** clones template missions on cron; an **auto-loop** turns a goal into parallel tasks. The whole platform is *also itself* an MCP server (Streamable HTTP at `/mcp`, legacy SSE at `/mcp/sse`), so any MCP client — Claude Code, Cursor, Windsurf, Cline — can call `plan_project`, `dispatch_mission`, `wait_for_mission`, `get_report`, etc. to drive a fleet from the outside. So MCP is used both *inward* (each agent's self-service/context API) and *outward* (the orchestrator's control API). It adds Claude-Code-native ergonomics on top: per-mission model selection (Opus/Sonnet/Haiku), tool-access presets (full/implement/review/test/explore/fix), max-turn and budget caps, cost/token tracking, session resume/fork, live SSE output, phone "remote control" via `claude remote-control`, a Python plugin system (hooks + tools auto-exposed as MCP tools), and optional `context-mode` integration for context compaction.

## How we tested it

Inspected the repo metadata, full README, recursive file tree, contributor count, commit-page count, and last-commit date via the GitHub API; cross-checked the `devfleet` candidates from `gh search repos devfleet` to identify the right repo; and grepped CATALOG.md for the overlap entries. **Did not install or run it.** Running it meaningfully requires Python 3.11+, Node 18+, the Claude CLI with a configured Anthropic API key, and at least one target git repo, then standing up a long-running FastAPI service plus background watcher/scheduler — a stateful, multi-process deployment rather than a scriptable one-shot command, and it would consume live Anthropic API tokens. This is a repo/README/structure review and a repo-identification exercise, not hands-on usage. No timing, throughput, cost, or "98% context savings" numbers are claimed here; the context-savings figure is `context-mode`'s claim, surfaced in the README.

```bash
gh search repos devfleet --limit 20 --json fullName,description,stargazersCount,url,updatedAt,language
gh api repos/LEC-AI/claude-devfleet --jq '{stars,license:.license.spdx_id,desc:.description,pushed:.pushed_at,created:.created_at,forks,lang:.language}'
gh api repos/LEC-AI/claude-devfleet/readme --jq '.content' | base64 -d
gh api "repos/LEC-AI/claude-devfleet/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/LEC-AI/claude-devfleet/contributors --jq 'length'        # 1
gh api "repos/LEC-AI/claude-devfleet/commits?per_page=1" -i | grep -i 'rel="last"'  # ~24 pages
gh api "repos/LEC-AI/claude-devfleet/commits?per_page=1" --jq '.[0].commit.author.date'  # 2026-05-28
gh api repos/LEC-AI/claude-devfleet/tags --jq '.[].name'             # (none)
grep -inE "claude-squad|gastown|devfleet" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **The MCP-as-orchestration-bus design is the real differentiator.** Unlike dmux (tmux TUI) and gastown (bespoke `gt` CLI + Dolt ledger), DevFleet uses MCP both *inward* — each agent gets context + self-service MCP servers so it can read peer state and spawn sub-missions — and *outward* — the platform is itself an MCP server, so Claude Code/Cursor/Cline can orchestrate a fleet without leaving their own session. That is precisely what the catalog one-liner promises and is genuinely different from the worktree-cockpit peers.
- **Substantial, coherent codebase for its star count.** ~24 pages of commit history, ~30 backend modules with clear separation (`sdk_engine`, `mission_watcher`, `scheduler`, `autoloop`, three MCP servers, `worktree`, `planner`, `remote_control`), a documented SQLite schema, a full React UI, Docker compose, and per-client integration docs. This is not a thin README-only repo — it is an implemented platform.
- **Worktree isolation + dependency DAG + auto-dispatch.** Each agent runs in its own branch (auto-merged on success), and the watcher dispatches missions only when `depends_on` is satisfied — a credible autonomous pipeline, closer to gastown's ambition than dmux's manual cockpit.
- **Strong Claude Code fit.** SDK-first (with CLI fallback), per-mission model selection, tool-access presets that mirror the dev-loop stages (implement/review/test/explore/fix), budget/turn caps, cost tracking, session resume/fork, and phone remote-control via `claude remote-control`. It is built around Claude Code's feature set rather than treating it as one backend among many.
- **Apache-2.0 and extensible.** Permissive license; a Python plugin system where dropped-in hooks/tools auto-surface as MCP tools is a clean extension story.

## What didn't work or surprised us

- **Not validated hands-on here.** Everything above is from the README, file tree, and metadata. Claims about autonomous coordination, auto-merge reliability, and sub-mission dispatch are the project's, not observed in this environment.
- **Single-maintainer, very early traction.** 1 contributor, 16 stars, 6 forks, **no tagged releases**, last commit 2026-05-28 (~3 weeks before this eval). This is one person's actively-built platform, not a community-hardened system. Bus-factor and longevity risk are real.
- **Heavy, stateful deployment for a coordination layer.** A long-running FastAPI service + background watcher + scheduler + React UI + (optionally) Docker is a lot of standing infrastructure compared to dmux (a TUI you launch in a repo) — and it self-hosts on plaintext local ports (`18801`/`3100`) with no auth story described in the README. Exposing the `/mcp` control endpoint beyond localhost would need its own hardening.
- **Repo-name ambiguity.** The catalog said "devfleet"; the actual repo is `LEC-AI/claude-devfleet`. The Docker quick-start even `cd devfleet`s after cloning `claude-devfleet` (a copy-paste bug), and ~17 other "devfleet" repos exist — a discoverability and identity hazard worth recording in the catalog link.
- **Default cap of 3 concurrent agents.** `DEVFLEET_MAX_AGENTS=3` — this is a "coordinate a handful of agents intelligently via MCP" tool, not a 20–30-agent fleet substrate like gastown. Useful framing, not a flaw, but it bounds the use case.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Structured reports, request_review sub-missions, and dependency-gated dispatch add coordination structure; but no merge-queue/verification gate like gastown — correctness still rests on the agents and your acceptance criteria. |
| Speed | + | Up to 3 agents run in parallel in isolated worktrees with auto-dispatch on dependency satisfaction, vs. one-at-a-time; auto-loop fans a goal into parallel tasks. |
| Maintainability | + | Worktree-per-mission keeps branches isolated and auto-merged; persisted missions/sessions/reports in SQLite survive restarts and preserve session history. |
| Safety | neutral | Tool-access presets and per-mission budget/turn caps constrain agents, and worktree isolation contains file changes; offset by a self-hosted service on plaintext local ports with no described auth and auto-merge on success. |
| Cost Efficiency | neutral | Free/Apache-2.0 with budget caps and cost tracking per dispatch, and optional context-mode for context savings; but running multiple Claude agents multiplies underlying token spend — a throughput play, not a savings play. |

## Verdict

**CONDITIONAL**

Consider Claude DevFleet when you specifically want **MCP to be the orchestration bus** — i.e., you want to drive a small fleet of Claude Code agents *from inside* another MCP client (Claude Code, Cursor, Cline) via `plan_project`/`dispatch_mission`/`wait_for_mission`, and you want the agents themselves to coordinate over MCP (context server + sub-mission/report tools) rather than over a bespoke CLI. That MCP-native design is the genuine reason this entry earns a slot distinct from the worktree-cockpit cluster. It is **not** a default adoption: it is a single-maintainer, 16-star, no-tagged-release platform that requires standing up a stateful self-hosted service, caps at 3 agents by default, and has no described auth on its control endpoint. Adopt only if the MCP-orchestration angle is the point and you accept early-stage, single-author risk; otherwise prefer the more mature peers below. Re-evaluate after it gains tagged releases, additional contributors, and an auth story for the `/mcp` endpoint.

**vs. claude-squad / dmux / gastown (the parallel-agent cluster).** All four isolate agents (worktrees or terminal sessions), but they differ on the *coordination substrate*:
- **claude-squad** — a TUI that runs multiple Claude/Codex/Amp terminal sessions in parallel for visibility. Lightweight, agent-agnostic, no programmatic control plane.
- **dmux** — a tmux + Ink/React cockpit to launch/watch/browse/one-step-merge a handful of agents in git worktrees. Interactive, no autonomous dispatch, no MCP.
- **gastown** — the heavyweight autonomous substrate (16K stars, 30 contributors): git-backed Beads ledger, Bors-style bisecting merge queue, three-tier watchdog, escalation, 20–30-agent scale. Coordinates over its own `gt` CLI + Dolt, not MCP.
- **devfleet (claude-devfleet)** — the **MCP-native** member: orchestrates over MCP both inward (agent context + sub-mission tools) and outward (the platform is itself an MCP server callable from any MCP client). Smaller scope than gastown (default 3 agents, no merge queue), more autonomous than dmux/claude-squad (dependency-DAG auto-dispatch), and uniquely controllable from inside another agent's session. Its distinct niche is the protocol, not the topology.

This is **additive, not a duplicate**: it occupies the "coordinate agents *through MCP* / control a fleet from inside another MCP client" point that none of claude-squad, dmux, or gastown fills. The existing "overlaps with claude-squad, gastown" is accurate, but the real differentiator to record is *MCP as the orchestration interface*.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [devfleet](https://github.com/LEC-AI/claude-devfleet) | MCP server | Multi-agent orchestration via MCP — dispatch and coordinate Claude Code agents through the MCP protocol | Need to coordinate a fleet of agents over MCP (and drive them from inside another MCP client) rather than a bespoke CLI/TUI | claude-squad, gastown, dmux |
