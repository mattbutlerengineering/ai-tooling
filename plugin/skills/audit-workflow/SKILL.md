---
name: audit-workflow
description: Audit your current AI tool setup against the recommended dev loop workflow and identify gaps
---

# Audit Workflow

Check your installed tools against the recommended workflow. Identifies what you have, what you're missing, what's redundant, and which dev loop stages have gaps.

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

Read `${CLAUDE_PLUGIN_ROOT}/docs/WORKFLOW.md`. For each dev loop stage (inner: Plan, Implement, Verify, Review, Ship, Reflect; outer: Discover, Architect, Decompose, Integrate, Retrospect), check which recommended tools are installed and which are missing. Also check cross-cutting sections (Cost Efficiency, Security).

### 3. Check for anti-patterns

Flag these issues:
- **Multiple tools solving the same problem** — e.g., both OMEGA and claude-mem running as memory
- **Tools without supporting infrastructure** — e.g., claude-squad installed but no worktree management
- **Missing feedback loops** — tools installed but the infrastructure they need isn't built (e.g., langfuse installed but no evals configured)
- **Kitchen-sink plugins** — everything-claude-code with 251+ skills when targeted skills would be better

### 4. Check for missing feedback loops (not tools)

These are infrastructure, not installable tools:
- [ ] Coverage gating in CI
- [ ] PR acceptance rate tracking
- [ ] Flaky test detection
- [ ] Error monitoring → auto-issue creation
- [ ] Merge conflict frequency tracking
- [ ] AI code churn rate measurement

### 5. Report

```
## Workflow Audit Report

**Dev loop coverage:** {covered}/{total stages}
**Installed tools:** {count}
**Recommended tools installed:** {count}/{total}
**Redundant tools:** {count}

### Stage-by-Stage Status

#### Inner Loop
| Stage | Tool | Status |
|-------|------|--------|
| Plan | GSD / brainstorming | ✅ / ❌ |
| Implement | superpowers TDD | ✅ / ❌ |
| Verify | stryker-js / agent-browser | ✅ / ❌ |
| Review | code-review / pr-review-toolkit | ✅ / ❌ |
| Ship | commit-commands | ✅ / ❌ |
| Reflect | claude-reflect | ✅ / ❌ |

#### Outer Loop
| Stage | Tool | Status |
|-------|------|--------|
| Discover | GSD new-project / grill-me | ✅ / ❌ |
| Architect | graphify / map-codebase | ✅ / ❌ |
| Decompose | to-issues / to-prd | ✅ / ❌ |
| Integrate | claude-squad / worktrunk | ✅ / ❌ |
| Retrospect | claude-mem timeline | ✅ / ❌ |

#### Cross-Cutting
| Area | Tool | Status |
|------|------|--------|
| Cost Efficiency | caveman / context-mode / headroom | ✅ / ❌ |
| Security | SkillSpector / trailofbits/skills | ✅ / ❌ |
| Observability | langfuse / tokencost / abtop | ✅ / ❌ |

### Redundancies
{tools that overlap — recommend which to keep and which to drop}

### Missing Feedback Loops
{infrastructure gaps that tools can't fill}

### Next Actions
1. {most impactful thing to do next}
2. {second most impactful}
3. {third}
```
