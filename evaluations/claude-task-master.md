# Evaluation: Taskmaster (claude-task-master)

**Repo:** [eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master)
**Stars:** 27,606 | **Last updated:** 2026-06-18 | **License:** MIT + Commons Clause
**Dev loop stage:** Implement / Plan
**Layer:** Tooling

---

## What it does

AI-powered task management system that breaks a PRD into structured tasks with dependencies, priorities, subtasks, and test strategies. Operates as an MCP server (36 tools) or CLI, designed primarily for Cursor but also supports Claude Code, Windsurf, Roo, VS Code, and Q CLI. The core loop: parse a PRD → generate task tree → analyze complexity → expand complex tasks into subtasks → execute with dependency-aware ordering → track status.

Tasks are stored as JSON in `.taskmaster/tasks/tasks.json` with Zod-validated schemas. Each task has id, title, description, status (pending/in-progress/blocked/done/cancelled/deferred), dependencies, priority, details, and testStrategy. The tool uses AI (configurable across 10+ providers) for complexity analysis, task expansion, and research.

The Claude Code integration ships as a marketplace plugin with `/project:tm/` namespaced slash commands covering setup, task generation, status management, analysis, dependencies, tags, and workflows including an `auto-implement` mode.

## How we tested it

Architecture review based on repo source code, schema definitions, command structure, commit history, and release cadence. Did not install and run hands-on.

```bash
gh api repos/eyaltoledano/claude-task-master --jq '.description, .stargazers_count, .updated_at'
gh api repos/eyaltoledano/claude-task-master/readme --jq '.content' | base64 -d
gh api repos/eyaltoledano/claude-task-master/contents/src/schemas/base-schemas.js --jq '.content' | base64 -d
gh api repos/eyaltoledano/claude-task-master/commits?per_page=5 --jq '...'
gh api repos/eyaltoledano/claude-task-master/releases?per_page=5 --jq '...'
```

## What worked

- **Well-designed task schema**: Zod-validated with strict mode for cross-provider compatibility (OpenAI Structured Outputs, Anthropic, Google). Task status enum, dependency arrays, priority levels, and test strategies are all typed.
- **Dependency-aware execution**: `next_task` picks the right task based on dependency resolution, not just sequential ordering. `validate-dependencies` and `fix-dependencies` handle circular refs.
- **Multi-provider flexibility**: 10+ AI providers (Claude, GPT, Gemini, Perplexity for research, xAI, Groq, OpenRouter, Azure, Ollama, Codex CLI) with configurable main/research/fallback models. Can even use Claude Code itself as a provider (no separate API key needed).
- **Complexity analysis**: AI-driven complexity scoring that determines which tasks need subtask expansion — avoids over-decomposing simple tasks.
- **Tool scoping**: `TASK_MASTER_TOOLS` env var lets you expose only core (7), standard (15), or all (36) tools — reduces token overhead for simpler workflows.
- **Claude Code plugin**: Proper marketplace plugin with namespaced commands, not just an MCP server bolted on.

## What didn't work or surprised us

- **Development stalled**: Last meaningful code commit was March 31, 2026 (v0.43.1). Last two commits are just URL redirects to the new `tryhamster.com` brand. The tool appears to be in maintenance mode while the team builds the commercial "Hamster" product.
- **Commons Clause restriction**: Can't host it as a service or build competing products from it — limits adoption in certain enterprise contexts.
- **Cursor-first design**: README, one-click install, and documentation all lead with Cursor. Claude Code is supported but clearly second-class — the plugin was added later and the commands guide is simpler than the Cursor integration.
- **JSON task storage is fragile**: Tasks live in a single `.taskmaster/tasks/tasks.json` file. No database, no indexing, no concurrent access protection. Fine for solo use, risky for teams.
- **Heavyweight for Claude Code users**: GSD (part of superpowers) provides similar milestone/phase/task management with tighter Claude Code integration, no external MCP server, and no separate API key requirements.
- **196 open issues**: High issue count relative to activity suggests the maintainers are focused elsewhere.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Dependency-aware task ordering prevents out-of-order work; complexity analysis avoids premature decomposition |
| Speed | +/neutral | PRD-to-task-tree generation is fast, but MCP server startup and multi-provider config add friction |
| Maintainability | neutral | Structured task files are readable, but single-JSON storage doesn't scale |
| Safety | neutral | No security-specific features |
| Cost Efficiency | - | Requires separate API keys for AI features (unless using Claude Code as provider); adds MCP server overhead |

## Verdict

**CONDITIONAL**

Use Taskmaster when working in Cursor or multi-editor environments where you need structured task management with dependency tracking and AI-driven complexity analysis. For Claude Code-primary workflows, GSD (part of superpowers) offers tighter integration without the MCP server overhead and doesn't require separate API keys. The tool's development has slowed since the commercial pivot to Hamster — evaluate whether v0.43.1 meets your needs before committing, as updates may be infrequent.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-task-master](https://github.com/eyaltoledano/claude-task-master) | tool | AI-powered task management for Cursor, Windsurf, Roo, and other editors | Need structured task breakdown and tracking across AI editors | GSD |
