---
name: evaluate-tool
description: Evaluate an AI tool, skill, or plugin against the catalog and dev loop quality signals before adopting it
---

# Evaluate Tool

Evaluate a new AI tool before adding it to your workflow. Prevents tool sprawl by checking for overlap and assessing fit against the five quality signals.

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

### 3. Assess dev loop stage and quality signal fit

Read `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`. Determine:
- Which dev loop stage does this tool serve? (Inner: Plan, Implement, Verify, Review, Ship, Reflect; Outer: Discover, Architect, Decompose, Integrate, Retrospect)
- Which quality signals does it improve? (Correctness, Speed, Maintainability, Safety, Cost Efficiency)
- Which layer does it operate at? (Process, Tooling, Infrastructure)

Check: does the user's current setup already have strong coverage for this stage and signal? Adding a third code review tool when Review is already well-covered is lower value than filling a gap in Verify or Integrate.

### 4. Report

Output a structured evaluation:

```
## Tool Evaluation: {name}

**What it does:** {one-liner}
**Problem it solves:** {pain point}
**Type:** {type}
**Category:** {category}
**Dev loop stage:** {stage}
**Quality signals:** {signals}

### Overlap Analysis
{list overlapping tools from catalog, with comparison}

### Recommendation
- **ADOPT** — fills a gap in the current workflow
- **REPLACE {x}** — better than current tool for this problem
- **SKIP** — overlaps with {x} which is already in the workflow
- **DEFER** — relevant but current setup has higher-priority gaps elsewhere

### Catalog Entry (if adopting)
{pre-filled table row for CATALOG.md}
```

### 5. Update catalog

If the recommendation is ADOPT or REPLACE, offer to add the entry to `${CLAUDE_PLUGIN_ROOT}/docs/CATALOG.md` and update `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`.
