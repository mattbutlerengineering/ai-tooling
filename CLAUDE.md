# AI Tooling

Documentation-only repo. No build, test, or deploy commands.

## Purpose

An operating manual for AI-assisted development that produces high-quality code and keeps improving. Inventory and evaluation of AI tools, skills, agents, frameworks, harnesses, workflows, and MCP servers — organized around the dev loop stages where tools intervene and the quality signals they move.

Evaluates tools against five quality signals: Correctness, Speed, Maintainability, Safety, and Cost Efficiency. The workflow has three layers per stage (process, tooling, infrastructure) connected by feedback arcs that make each cycle better than the last.

## Structure

- `CATALOG.md` — flat inventory of 443 tools, organized by 13 categories with overlap markers
- `WORKFLOW.md` — dev loop stages (inner + outer), tools per stage, quality signals, adoption guide
- `STACK.md` — recommended stack (~20 tools to actually install, with commands)
- `evaluations/` — hands-on tool evaluations following `TEMPLATE.md`
- `discovery/` — bulk discovery logs (`new-tools-loopN.md`) from scanning sessions
- `skills/` — source skills for reference
- `plugin/` — installable Claude Code marketplace package (skills, docs, hooks)
- `README.md` — repo overview with install instructions

## Catalog format

Each entry is a row in a markdown table with these columns:

| Column | Description |
|--------|-------------|
| Name | Tool name, linked to repo |
| Type | tool / skill / plugin / framework / harness / platform / MCP server / reference |
| One-liner | Plain-language description, ~10-15 words |
| Problem it solves | The specific pain point, ~1 sentence |
| Overlaps with | Other catalog entries that address a similar problem (may also name a notable external tool or installed skill as a conceptual peer) |

## Categories

Code Understanding, Agent Orchestration, Agent Harnesses, Memory & Context,
Skills & Plugins, Code Review & Quality, Maturity Frameworks, Dev Workflow,
MCP Servers, Observability, Research & Discovery, Security & Safety, Reference

## Sources

- GitHub stars: `gh api user/starred --paginate --jq '.[].full_name'`
- Locally installed: `~/.claude/plugins/`, `~/.claude/skills/`, MCP servers in settings.json
- Newsletters: TLDR AI, The Rundown AI, The Neuron, AI Leadership Edge, Practical AI, AI Adopters Club
- Registries: skills.sh, npm (claude-code plugins), GitHub trending (AI topic)

## Skills

- `skills/setup-workflow/` — bootstrap the workflow in any repo (use first time on a new project)
- `skills/evaluate-tool/` — evaluate a new tool against catalog, dev loop stage, and quality signals (use when considering a new tool)
- `skills/audit-workflow/` — audit installed tools against recommended stack (use periodically)
- `skills/update-catalog/` — sync catalog with GitHub stars and local installs (use when catalog may be stale)
- `skills/sync-stars/` — find starred repos not in CATALOG.md and generate entries (use after starring new repos)

## Source of truth

- Root files (`CATALOG.md`, `WORKFLOW.md`, `evaluations/`) are authoritative
- `plugin/docs/` is a synced copy — never edit directly
- `plugin/skills/` is authoritative for skills; `skills/` is derived (paths stripped)
- Run `./sync-plugin-docs.sh` after any root doc or plugin skill change

## Agent skills

### Issue tracker

GitHub Issues on `mattbutlerengineering/ai-tooling`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout. See `docs/agents/domain.md`.

## Adding entries

- Fetch repo description: `gh api repos/{owner}/{repo} --jq '.description'`
- Place in the correct category table
- Always fill the "Overlaps with" column — check existing entries in the same category
- If a new category is needed, add a section header with a one-line description

## Evaluations

- **Hands-on evaluations** use `evaluations/TEMPLATE.md` — copy it and fill every section with evidence from actual usage. The "How we tested it" section is mandatory; README-only evaluations are discovery logs, not evaluations.
- **Discovery logs** (`evaluations/new-tools-loopN.md`) are for bulk triage — one-liner verdicts from scanning repos. They feed the catalog but don't constitute a full evaluation.
- Use inner/outer loop vocabulary (Plan, Implement, Verify, Review, Ship, Reflect), not ACMM levels.
