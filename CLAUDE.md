# AI Tooling

Documentation-only repo. No build, test, or deploy commands.

## Purpose

Inventory and evaluation of AI tools, skills, agents, frameworks, harnesses, workflows, and MCP servers. The goal is to see everything at a glance, spot redundancy across tools that solve the same problem, and converge on an ideal AI-assisted dev workflow.

Uses the ACMM (AI Codebase Maturity Model) as a lens for evaluating which tools matter at each maturity level — the right tool stack depends on what feedback loops exist in a codebase, not on how many tools are installed.

## Structure

- `CATALOG.md` — flat inventory of 149 tools, organized by 13 categories with overlap markers
- `WORKFLOW.md` — recommended tool stack per ACMM level (L2-L6) with daily practice guide
- `evaluations/` — 16 evidence-based evaluation files covering every recommended tool
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
| Overlaps with | Other catalog entries that address a similar problem |

## Categories

Code Understanding, Agent Orchestration, Agent Harnesses, Memory & Context,
Skills & Plugins, Code Review & Quality, Maturity Frameworks, Dev Workflow,
MCP Servers, Observability, Research & Discovery, Security & Safety, Reference

## Sources

- GitHub stars: `gh api user/starred --paginate --jq '.[].full_name'`
- Locally installed: `~/.claude/plugins/`, `~/.claude/skills/`, MCP servers in settings.json

## Skills

- `skills/setup-workflow/` — bootstrap the workflow in any repo
- `skills/evaluate-tool/` — evaluate a new tool against catalog and ACMM fit
- `skills/audit-workflow/` — audit installed tools against recommended stack
- `skills/update-catalog/` — sync catalog with GitHub stars and local installs

## Adding entries

- Fetch repo description: `gh api repos/{owner}/{repo} --jq '.description'`
- Place in the correct category table
- Always fill the "Overlaps with" column — check existing entries in the same category
- If a new category is needed, add a section header with a one-line description
