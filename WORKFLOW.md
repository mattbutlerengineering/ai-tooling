# Recommended AI Workflow

An opinionated, non-overlapping tool stack for AI-assisted development, organized by ACMM level. Each level builds on the previous — don't skip ahead.

## Principles

1. **Fewer tools, more feedback loops.** Five overlapping memory systems don't make you more mature than one memory system with acceptance rate tracking.
2. **Each tool earns its slot.** If two tools solve the same problem, pick one. The overlap markers in [CATALOG.md](CATALOG.md) show where to consolidate.
3. **Match tools to your level.** Installing L5 orchestration tools when you don't have L3 test coverage is the "autonomous action without sufficient guardrails" anti-pattern.

---

## L2 — Instructed: Encode Your Preferences

**Goal:** AI output becomes consistent across sessions and agents. Decisions live in files, not your head.

### Recommended Stack

| Tool | Type | Why |
|------|------|-----|
| CLAUDE.md + rules/ | built-in | Encode conventions, coding style, commit format, security checks |
| [mattpocock/skills](https://github.com/mattpocock/skills) | skill | Battle-tested engineering conventions from a working dev |
| [graphify](https://github.com/safishamsi/graphify) | skill | Gives agents structural awareness of codebase, SQL, docs — not just file contents |
| [context7](https://github.com/upstash/context7) | MCP server | Live documentation lookup so agents use current APIs, not stale training data |
| [reporails/cli](https://github.com/reporails/cli) | tool | Validates that instruction files aren't conflicting or malformed |

### What to skip at this level

- Multiple harnesses (superpowers, gstack, ECC, ruflo) — you don't need methodology enforcement yet, you need instructions
- Memory systems — no point remembering across sessions if each session does the wrong thing consistently
- Agent orchestration — one agent doing the right thing beats five doing the wrong thing

### Transition trigger

You notice the AI is consistent but you can't tell whether it's actually performing well. You want data.

---

## L3 — Measured: Make Feedback Visible

**Goal:** Quantitative signals about AI agent performance. Tests gate quality. Acceptance rates reveal what works.

### Recommended Stack

Everything from L2, plus:

| Tool | Type | Why |
|------|------|-----|
| [superpowers](https://github.com/obra/superpowers) | plugin | TDD workflow, systematic debugging, verification-before-completion — the methodology layer |
| code-review plugin | plugin | Multi-agent code review with confidence-based scoring |
| pr-review-toolkit | plugin | Structured review dimensions: type analysis, silent failures, test coverage |
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | plugin | Captures corrections and preferences, syncs learnings to CLAUDE.md automatically |
| [langfuse](https://github.com/langfuse/langfuse) | platform | Observability: see what agents are doing, track evals, measure performance over time |

### Key feedback loops to build (not tools — infrastructure)

- **Coverage gating in CI** — enforce minimum coverage on every PR
- **PR acceptance rate tracking** — log merged vs. closed PRs by category
- **Flaky test detection** — weekly analysis of non-deterministic test results
- **Error monitoring → issues** — production errors auto-create GitHub issues

### What to skip at this level

- Memory systems — you're still building the measurement infrastructure that makes memory useful
- Multi-agent orchestration — premature without quality gates

### Transition trigger

You see patterns in the data and realize certain responses should be automated. "Why am I manually adjusting weights when the data tells me what to do?"

---

## L4 — Adaptive: Loops Close Themselves

**Goal:** The system acts on its own metrics. Thresholds trigger automated responses. Human oversight shifts from execution to governance.

### Recommended Stack

Everything from L3, plus:

| Tool | Type | Why |
|------|------|-----|
| claude-mem OR OMEGA | plugin / MCP | Persistent cross-session memory — pick ONE. You now have enough measurement to make memory meaningful. |
| [headroom](https://github.com/chopratejas/headroom) | tool | Context compression (60-95% fewer tokens) — longer sessions mean more complex autonomous work |
| [worktrunk](https://github.com/max-sixty/worktrunk) | tool | Git worktree management for parallel agent workflows without branch conflicts |
| GSD | framework | Project orchestration with milestones, phases, verification — structure for larger autonomous tasks |
| feature-dev | plugin | Structured feature development: planning → implementation → verification |

### Memory: pick one

| Option | Strength | Choose if |
|--------|----------|-----------|
| claude-mem | Semantic search, timeline views, knowledge graph | You want structured, queryable memory with temporal awareness |
| OMEGA | Coordination, handoff protocols, knowledge graphs | You want cross-agent coordination and handoff support |

Do not run both. Conflicting memory systems create contradictory context.

### What to skip at this level

- Multiple agent orchestration (claude-squad, gastown) — you're still one human directing agents, just with better automation

### Transition trigger

The system's behavior is now primarily determined by its artifacts — tests, configs, workflows — not by your real-time decisions. You realize the bottleneck is your availability to approve, not the system's ability to propose.

---

## L5 — Semi-Automated: The System Proposes, You Approve

**Goal:** The system detects problems, proposes fixes, and implements them. You review and merge. Issues filed at 2 AM are fixed, tested, and ready for review by 6 AM.

### Recommended Stack

Everything from L4, plus:

| Tool | Type | Why |
|------|------|-----|
| [claude-squad](https://github.com/smtg-ai/claude-squad) | tool | Manage multiple parallel agent sessions — the system now runs enough concurrent work to need this |
| [plannotator](https://github.com/backnotprop/plannotator) | tool | Visual review of agent plans and diffs — you're reviewing proposals, not writing code |
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | tool | Security scanning for any new skills the system proposes to install |

### What to skip at this level

- Full autonomy tools (bernstein audit logs, adaptive workload governance) — you're still approving merges

### Transition trigger

You realize the bottleneck is no longer AI quality — it's your human availability. The system proposes well, but proposals sit unreviewed.

---

## L6 — Fully Autonomous: The System Runs Itself

**Goal:** Agents generate issues, dispatch fixes, merge verified PRs, and roll back failures. You set strategy and policy.

### Recommended Stack

Everything from L5, plus:

| Tool | Type | Why |
|------|------|-----|
| [bernstein](https://github.com/sipyourdrink-ltd/bernstein) | harness | Audit-grade orchestration with tamper-proof logs — compliance for autonomous merges |
| [beads](https://github.com/gastownhall/beads) | tool | Work ledger so agents claim tasks and don't duplicate effort |
| Push notification infrastructure | infra | ntfy, Slack, Discord — humans get notified for strategic decisions only |

### What this level requires beyond tools

- Automated merge queue with verification gates
- Adaptive workload governance (SURGE/BUSY/QUIET/IDLE modes)
- Risk assessment configuration (high-risk paths always require human review)
- Rollback drills and documented procedures
- Strategic dashboard for real-time visibility into agent fleet

---

## Tools deliberately excluded from the workflow

| Tool | Why excluded |
|------|-------------|
| gstack, ECC, ruflo, oh-my-openagent, compound-engineering | Overlap with superpowers. Pick one harness. |
| agentmemory | Overlap with claude-mem/OMEGA. Pick one memory system. |
| everything-claude-code (251+ skills) | Too broad. Use targeted skills (mattpocock, graphify) instead of a kitchen-sink plugin. |
| Flowise, LangGraph | Visual/programmatic agent builders — useful for building AI products, not for your own dev workflow |
| OpenHands | Full platform replacement — you're augmenting Claude Code, not replacing it |
| sandcastle, gastown | Overlap with claude-squad for orchestration |
| Understand-Anything, codegraph | Overlap with graphify. Pick one code understanding tool. |
| repomix | Different approach (serialization vs. graph) — useful for feeding code to non-agent LLMs, not needed when agents have file access |

---

## Current position

**Using:** mattpocock/skills + graphify + ACMM framework

**ACMM level:** L2 (Instructed) — strong instruction files, codebase awareness via graphify, but no measurement infrastructure

**Next step:** Add superpowers + code-review plugin to reach L3. The biggest unlock is testing infrastructure and acceptance rate tracking, not more tools.
