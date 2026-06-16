---
name: audit-workflow
description: Audit your current AI tool setup against the recommended ACMM workflow and identify gaps
---

# Audit Workflow

Check your installed tools against the recommended workflow in WORKFLOW.md. Identifies what you have, what you're missing, what's redundant, and your current ACMM level.

## Trigger

`/audit-workflow`

## Workflow

### 1. Inventory current setup

Scan installed tools:

```bash
# Plugins
ls ~/.claude/plugins/cache/ 2>/dev/null

# Skills
ls ~/.claude/skills/ 2>/dev/null

# MCP servers (from settings)
cat ~/.claude/settings.json | grep -A2 '"mcpServers"' 2>/dev/null

# Project-specific
find . -name "CLAUDE.md" -o -name "AGENTS.md" 2>/dev/null
```

### 2. Map against WORKFLOW.md

Read WORKFLOW.md. For each ACMM level (L2 through L6), check which recommended tools are installed and which are missing.

### 3. Check for anti-patterns

Flag these issues:
- **Multiple tools solving the same problem** — e.g., both OMEGA and claude-mem running as memory
- **Tools above your level** — e.g., claude-squad installed but no test coverage gating
- **Missing feedback loops** — tools installed but the infrastructure they need isn't built (e.g., langfuse installed but no evals configured)
- **Kitchen-sink plugins** — everything-claude-code with 251+ skills when targeted skills would be better

### 4. Check for missing feedback loops (not tools)

These are infrastructure, not installable tools:
- [ ] Coverage gating in CI
- [ ] PR acceptance rate tracking
- [ ] Flaky test detection
- [ ] Error monitoring → auto-issue creation
- [ ] Self-tuning configuration (auto-qa-tuning.json or equivalent)

### 5. Report

```
## Workflow Audit Report

**Current ACMM Level:** L{n}
**Installed tools:** {count}
**Recommended tools installed:** {count}/{total for current level}
**Redundant tools:** {count}

### Level-by-Level Status

#### L2 — Instructed
| Tool | Status |
|------|--------|
| CLAUDE.md | ✅ / ❌ |
| mattpocock/skills | ✅ / ❌ |
| graphify | ✅ / ❌ |
| context7 | ✅ / ❌ |

#### L3 — Measured
...

### Redundancies
{tools that overlap — recommend which to keep and which to drop}

### Missing Feedback Loops
{infrastructure gaps that tools can't fill}

### Next Actions
1. {most impactful thing to do next}
2. {second most impactful}
3. {third}
```
