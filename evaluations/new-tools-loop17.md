# Loop 17 — Installed Tools Audit & Optimal Setup Analysis (2026-06-17)

Focus: Shifted from discovery to workflow optimization — auditing installed tools against the recommended stack and identifying the optimal Claude Code configuration.

## Installed vs Recommended Stack

**Coverage: 15 of 27 recommended tools installed (56%)**

### Installed AND Recommended (15 tools)
superpowers, GSD, feature-dev, code-review, pr-review-toolkit, caveman, graphify, agent-browser, shadcn/improve, claude-mem, claude-reflect, context7, playwright, commit-commands, security-guidance, mattpocock skills (grill-me, grill-with-docs, to-issues, to-prd, improve-codebase-architecture, tdd)

### Top 3 Gaps (actionable)

| Gap | Stage | Priority | Why |
|-----|-------|----------|-----|
| SkillSpector | Security | HIGH | 34 skills installed with zero security scanning. Critical supply chain risk. |
| stryker-js | Verify | HIGH | Mutation testing is the Verify stage's key differentiator for JS/TS projects. |
| claude-squad | Integrate | HIGH | Integrate stage has no installed tooling. Essential for parallel agent work. |

### Lower Priority Gaps

| Tool | Stage | Priority | Assessment |
|------|-------|----------|------------|
| worktrunk | Integrate | MEDIUM | Worktree management; useful alongside claude-squad |
| context-mode | Cost Efficiency | MEDIUM | 98% input token reduction; complements caveman's output compression |
| headroom | Cost Efficiency | MEDIUM | 60-95% tool output compression; overlaps context-mode |
| tokencost | Observability | MEDIUM | Session cost tracking |
| reporails/cli | Security | LOW | CLAUDE.md validation |
| abtop | Observability | LOW | Multi-session monitor |
| Infracost | Observability | LOW | Only relevant for IaC projects |
| langfuse | Observability | LOW | Production-grade; only for deployed agents |
| Apache DevLake | Observability | LOW | Team-level DORA metrics |

## Optimal Claude Code Setup (2026 Golden Path)

Based on 17 loops of research, 208 tools cataloged, and web survey of best practices:

### Tier 1 — Install First (every project)
- **superpowers** — structured workflows (TDD, debugging, verification, code review)
- **caveman** — 75% token savings on output
- **context7** — live library documentation
- **claude-reflect** — learn from corrections
- **commit-commands** — git workflow shortcuts

### Tier 2 — Install for Serious Work
- **code-review + pr-review-toolkit** — multi-dimensional review
- **claude-mem** — persistent cross-session memory
- **SkillSpector** — security scanning for installed skills
- **graphify** — codebase visualization

### Tier 3 — Install for Scale
- **claude-squad** — parallel agent sessions
- **stryker-js** — mutation testing (JS/TS)
- **context-mode** — aggressive token compression
- **agent-browser** — visual UI verification

### Key Principle
"A Claude Code setup is a system, not a collection" — quality over quantity. Skills under 2,000 tokens perform best (Anthropic guidance). Install in tiers, not all at once.

## Fresh Discovery (June 2026)
- No repos created in June 2026 with >100 stars found
- Skills.sh worktree/hooks categories are saturated with low-install clones
- Anthropic's `claude-automation-recommender` (4.4K installs) is the top hooks skill — already installed

## Catalog count: 208 (no changes this loop — focus was analysis, not addition)
