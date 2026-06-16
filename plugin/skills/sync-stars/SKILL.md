---
name: sync-stars
description: Find GitHub starred repos not in CATALOG.md and generate catalog entries for them
---

# Sync Stars

Find starred repos missing from the catalog, classify them, and generate ready-to-paste catalog entries.

## Trigger

`/sync-stars`

## Workflow

### 1. Diff stars against catalog

```bash
# Get all starred repos
gh api user/starred --paginate --jq '.[].full_name' | sort > /tmp/starred.txt

# Extract all GitHub links from catalog
grep -oP 'github\.com/[^)]+' CATALOG.md | sed 's|github.com/||' | sort -u > /tmp/cataloged.txt

# Find gaps
comm -23 /tmp/starred.txt /tmp/cataloged.txt > /tmp/gaps.txt
```

### 2. Classify each gap

For each repo in the gaps list:

```bash
# Fetch description and stars
gh api "repos/OWNER/REPO" --jq '{name: .full_name, stars: .stargazers_count, description: .description}'
```

Classify into one of these buckets:
- **AI tooling** — skills, plugins, harnesses, MCP servers, agents, frameworks, platforms, references
- **Not AI tooling** — general libraries, infrastructure, domain tools unrelated to AI dev workflow

### 3. Generate catalog entries

For each AI-tooling repo, determine:
- **Category** — which CATALOG.md section it belongs in (Code Understanding, Agent Orchestration, Agent Harnesses, Memory & Context, Skills & Plugins, Code Review & Quality, Dev Workflow, MCP Servers, Observability, Research & Discovery, Security & Safety, Reference)
- **Type** — tool / skill / plugin / framework / harness / platform / MCP server / reference
- **One-liner** — from the repo description, trimmed to ~15 words
- **Problem it solves** — one sentence
- **Overlaps with** — check existing catalog entries in the same category

Output a table of entries grouped by category, ready to paste into CATALOG.md.

### 4. Report

Output:
- Count of new AI-tooling repos to add
- Count of non-AI repos (skipped, with names listed)
- The generated catalog entries grouped by section
- Updated entry count for CLAUDE.md

Do NOT modify any files automatically. Present the entries for review.
