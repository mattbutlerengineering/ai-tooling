---
name: evaluate-tool
description: Evaluate an AI tool, skill, or plugin against the catalog and ACMM framework before adopting it
---

# Evaluate Tool

Evaluate a new AI tool before adding it to your workflow. Prevents tool sprawl by checking for overlap and assessing ACMM-level fit.

## Trigger

`/evaluate-tool <repo-url-or-name>`

## Workflow

### 1. Research the tool

Fetch the repo description and README:

```bash
gh api repos/{owner}/{repo} --jq '.description'
gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d | head -100
```

Determine:
- What it does (one-liner)
- What problem it solves
- What type it is (tool / skill / plugin / framework / harness / MCP server)
- What category it belongs to

### 2. Check for overlap

Read the catalog at `${CLAUDE_PLUGIN_ROOT}/docs/CATALOG.md` and find entries in the same category. For each overlapping tool:
- Is the new tool strictly better, or just different?
- Does it replace something already in the workflow, or add alongside it?
- Would adopting it mean running two tools that solve the same problem?

### 3. Assess ACMM-level fit

Read `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`. Determine which ACMM level this tool belongs to:
- L2 (instructions/preferences)
- L3 (measurement/testing)
- L4 (adaptive/automated)
- L5 (semi-automated)
- L6 (fully autonomous)

Check: is the user at or approaching that level? Adopting L5 tools without L3 infrastructure is the "autonomous action without guardrails" anti-pattern.

### 4. Report

Output a structured evaluation:

```
## Tool Evaluation: {name}

**What it does:** {one-liner}
**Problem it solves:** {pain point}
**Type:** {type}
**Category:** {category}
**ACMM Level:** L{n}

### Overlap Analysis
{list overlapping tools from catalog, with comparison}

### Recommendation
- **ADOPT** — fills a gap in the current workflow
- **REPLACE {x}** — better than current tool for this problem
- **SKIP** — overlaps with {x} which is already in the workflow
- **DEFER** — relevant at L{n}, but you're at L{m}. Revisit when {condition}.

### Catalog Entry (if adopting)
{pre-filled table row for CATALOG.md}
```

### 5. Update catalog

If the recommendation is ADOPT or REPLACE, offer to add the entry to `${CLAUDE_PLUGIN_ROOT}/docs/CATALOG.md` and update `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`.
