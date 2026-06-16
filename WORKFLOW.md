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
| [mattpocock/skills](https://github.com/mattpocock/skills) | skill | Battle-tested engineering conventions from a working dev ([eval](evaluations/skills-collections.md)) |
| [codegraph](https://github.com/colbymchenry/codegraph) | MCP server | Always-on code knowledge graph that auto-syncs on changes — 58% fewer tool calls, 16% cheaper ([eval](evaluations/code-understanding.md)) |
| [graphify](https://github.com/safishamsi/graphify) | skill | Deep analysis of code, SQL, docs, images, videos into architecture diagrams — periodic use, not live ([eval](evaluations/code-understanding.md)) |
| [context7](https://github.com/upstash/context7) | MCP server | Live documentation lookup so agents use current APIs, not stale training data ([eval](evaluations/recommended-tools.md#context7)) |
| [reporails/cli](https://github.com/reporails/cli) | tool | Validates that instruction files aren't conflicting or malformed ([eval](evaluations/recommended-tools.md#reporailscli)) |

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
| [superpowers](https://github.com/obra/superpowers) | plugin | TDD workflow, systematic debugging, verification-before-completion — only harness with auto-triggering ([eval](evaluations/agent-harnesses.md)) |
| [agent-skills](https://github.com/addyosmani/agent-skills) | skill | Lifecycle structure (plan → implement → verify) that mattpocock/skills doesn't cover ([eval](evaluations/skills-collections.md)) |
| code-review plugin | plugin | Multi-agent code review with confidence-based scoring ([eval](evaluations/recommended-tools.md#code-review-plugin-anthropic)) |
| pr-review-toolkit | plugin | Structured review dimensions: type analysis, silent failures, test coverage ([eval](evaluations/recommended-tools.md#pr-review-toolkit-anthropic)) |
| [claude-reflect](https://github.com/BayramAnnakov/claude-reflect) | plugin | Captures corrections and preferences, syncs learnings to CLAUDE.md automatically ([eval](evaluations/recommended-tools.md#claude-reflect)) |
| [langfuse](https://github.com/langfuse/langfuse) | platform | Observability: see what agents are doing, track evals, measure performance over time ([eval](evaluations/recommended-tools.md#langfuse)) |

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
| [claude-mem](https://github.com/thedotmack/claude-mem) | plugin | Persistent memory with semantic search, timeline views, observation-based capture — best-validated option ([eval](evaluations/memory-systems.md)) |
| [headroom](https://github.com/chopratejas/headroom) | tool | Context compression (60-95% fewer tokens) — longer sessions mean more complex autonomous work ([eval](evaluations/recommended-tools.md#headroom)) |
| [worktrunk](https://github.com/max-sixty/worktrunk) | tool | Git worktree management for parallel agent workflows without branch conflicts ([eval](evaluations/recommended-tools.md#worktrunk)) |
| GSD | framework | Project orchestration with milestones, phases, verification — structure for larger autonomous tasks ([eval](evaluations/recommended-tools.md#gsd-get-shit-done)) |
| feature-dev | plugin | Structured feature development: planning → implementation → verification ([eval](evaluations/recommended-tools.md#feature-dev-anthropic)) |

### Why claude-mem over alternatives ([full evaluation](evaluations/memory-systems.md))

| Option | Stars | Why not |
|--------|-------|---------|
| claude-mem | 82.5K | **Recommended** — v13, observation-based capture, semantic search, timeline views |
| agentmemory | 23K | Strong alternative if you need cross-agent memory (95.2% recall). Consider if using multiple AI tools. |
| OMEGA | 162 | No benchmarks, much smaller community. Previously listed as equal — it isn't. |

Do not run multiple memory systems. Conflicting context is worse than no memory.

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
| [claude-squad](https://github.com/smtg-ai/claude-squad) | tool | Manage multiple parallel agent sessions — the system now runs enough concurrent work to need this ([eval](evaluations/recommended-tools.md#claude-squad)) |
| [plannotator](https://github.com/backnotprop/plannotator) | tool | Visual review of agent plans and diffs — you're reviewing proposals, not writing code ([eval](evaluations/recommended-tools.md#plannotator)) |
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | tool | Security scanning for any new skills the system proposes to install ([eval](evaluations/recommended-tools.md#skillspector)) |

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
| [bernstein](https://github.com/sipyourdrink-ltd/bernstein) | harness | Audit-grade orchestration with tamper-proof logs — compliance for autonomous merges ([eval](evaluations/recommended-tools.md#bernstein)) |
| [beads](https://github.com/gastownhall/beads) | tool | Work ledger so agents claim tasks and don't duplicate effort ([eval](evaluations/recommended-tools.md#beads)) |
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
| gstack, ECC, ruflo, oh-my-openagent | Overlap with superpowers. Superpowers is the only one with TDD enforcement and auto-triggering ([eval](evaluations/agent-harnesses.md)). |
| compound-engineering | Runner-up harness — lighter weight, good compounding philosophy. Consider if superpowers feels too heavy. |
| agentmemory | Overlap with claude-mem/OMEGA. Pick one memory system. |
| everything-claude-code (251+ skills) | Too broad. Use targeted skills (mattpocock, graphify) instead of a kitchen-sink plugin. |
| Flowise, LangGraph | Visual/programmatic agent builders — useful for building AI products, not for your own dev workflow |
| OpenHands | Full platform replacement — you're augmenting Claude Code, not replacing it |
| sandcastle, gastown | Overlap with claude-squad for orchestration |
| Understand-Anything | Prettier dashboard but no live sync or efficiency benchmarks. codegraph + graphify cover both live and deep analysis ([eval](evaluations/code-understanding.md)). |
| repomix | Different approach (serialization vs. graph) — useful for feeding code to non-agent LLMs, not needed when agents have file access |

---

## Daily Practice

How to actually use these tools together, not just have them installed.

### Starting a session

1. **graphify** scans the codebase on entry — agents start with structural awareness, not blind file reads
2. **CLAUDE.md** loads automatically — conventions, style rules, and project-specific patterns are active from the first prompt
3. **claude-reflect** (L3+) injects learnings from past sessions — mistakes you corrected before won't recur
4. **Memory** (L4+) provides cross-session context — ongoing work, decisions, and handoffs carry forward

### Writing code

1. **State the task clearly** — one feature, one bug, one refactor. Agents perform better with focused scope.
2. **TDD via superpowers** (L3+) — write test first (RED), implement (GREEN), refactor. The skill enforces this sequence.
3. **graphify for orientation** — before touching unfamiliar code, run `/graphify` to see how components connect. Prevents the "fix one thing, break three others" cascade.
4. **context7 for APIs** — when using any library, let context7 pull current docs rather than relying on training data.

### Reviewing code

1. **code-review plugin** (L3+) — run multi-agent review with confidence scoring before committing. Catches real issues, not style nitpicks.
2. **pr-review-toolkit** (L3+) — structured dimensions: type analysis, silent failure hunting, test coverage gaps, comment accuracy.
3. **Review the diff yourself** — tools catch patterns, you catch intent. Both are needed.

### Ending a session

1. **claude-reflect** (L3+) captures what went well and what was corrected — syncs to CLAUDE.md so the next session is better.
2. **Commit with conventional commits** — `feat:`, `fix:`, `refactor:` etc. The commit log is a feedback loop too.

### Weekly maintenance

1. **Run `/audit-workflow`** — check for tool redundancies, missing feedback loops, and ACMM level progress.
2. **Review PR acceptance rates** (L3+) — which categories get merged vs. closed? Data drives the next tuning cycle.
3. **Flaky test analysis** (L3+) — a flaky test in an autonomous workflow randomly blocks good PRs and passes bad ones. Fix or delete.

### Continuous improvement — what actually happens

**Automatic (built into the plugin):**

The ai-tooling plugin runs a SessionStart hook on every session that:
1. Checks if any evaluation file is >30 days old → surfaces a prompt to run `/update-catalog`
2. Checks for new GitHub stars not in the catalog → surfaces a prompt to run `/update-catalog`
3. Stays silent if everything is current

This means stale recommendations and new tools don't go unnoticed — the plugin tells you when the workflow needs attention.

**Manual (you run these):**

| Action | Trigger | What it does |
|--------|---------|-------------|
| `/audit-workflow` | Weekly or after installing new tools | Compares installed tools against recommended stack, flags redundancies and anti-patterns |
| `/update-catalog` | When hook flags stale evals or new stars | Syncs catalog with current GitHub stars and local installs |
| `/evaluate-tool` | Before adopting any new tool | Checks overlap, ACMM fit, and whether it justifies a slot |

**Per-session (via other recommended tools):**

| Mechanism | Tool | What it does |
|-----------|------|-------------|
| Correction capture | claude-reflect (L3) | Captures mistakes and preferences → syncs to CLAUDE.md → fewer repeated errors |
| Code review | code-review + pr-review-toolkit (L3) | Multi-agent review catches issues before commit → quality improves per session |
| TDD enforcement | superpowers (L3) | Forces test-first workflow → coverage stays high without manual discipline |

**Infrastructure you build (not installable tools):**

| Mechanism | Level | What it does |
|-----------|-------|-------------|
| Coverage gating in CI | L3 | Rejects PRs below threshold → coverage never regresses |
| PR acceptance rate tracking | L3 | Logs merged vs. closed by category → reveals what AI does well vs. poorly |
| Flaky test detection | L3 | Weekly analysis → removes non-determinism that corrupts autonomous workflows |
| Self-tuning weights | L4 | Adjusts category priorities based on acceptance rates → less manual config |
| Self-improvement analysis | L5 | System analyzes its own merged PRs → updates its own guidance |

The key insight from ACMM: the intelligence lives in the infrastructure (tests, metrics, feedback loops), not in the AI model. A better model with no tests is worse than a mediocre model with 91% coverage and acceptance rate tracking.

---

## Adopting this workflow in a new repo

Run `/setup-workflow` in any repo to bootstrap:
- Creates a CLAUDE.md with quality-producing rules (coding style, TDD, security, git workflow)
- Checks which global tools are installed
- Identifies gaps for your target ACMM level
- Reports next steps

The global tools (plugins, MCP servers, skills) are installed once in `~/.claude/` and available everywhere. What varies per repo is the CLAUDE.md configuration — that's what `/setup-workflow` generates.

---

## Current position

**Using:** mattpocock/skills + graphify + ACMM framework

**ACMM level:** L2 (Instructed) — strong instruction files, codebase awareness via graphify, but no measurement infrastructure

**Next steps to reach L3:**
1. Add **codegraph** MCP server alongside graphify — live code awareness during sessions ([eval](evaluations/code-understanding.md))
2. Add **superpowers** for TDD and verification methodology ([eval](evaluations/agent-harnesses.md))
3. Add **agent-skills** for lifecycle structure ([eval](evaluations/skills-collections.md))
4. Add **code-review plugin + pr-review-toolkit** for automated review
5. Add **claude-reflect** to capture corrections automatically
6. Build coverage gating and PR acceptance rate tracking in CI

## Evaluations

All recommendations are backed by evidence. See the full evaluations:

**Overlap groups** (compared competitors, picked a winner):
- [Code Understanding](evaluations/code-understanding.md) — graphify + codegraph (complementary), skip Understand-Anything
- [Agent Harnesses](evaluations/agent-harnesses.md) — superpowers (only TDD enforcer), skip gstack/ECC/ruflo
- [Memory Systems](evaluations/memory-systems.md) — claude-mem (best validated), skip OMEGA
- [Skills Collections](evaluations/skills-collections.md) — mattpocock/skills + agent-skills, skip everything-claude-code

**Individual tools** (justified their slot, no direct competitor):
- [Recommended Tools](evaluations/recommended-tools.md) — 15 tools evaluated: 10 KEEP, 5 CONDITIONAL

## Continuous improvement

The plugin includes a SessionStart hook (`plugin/hooks/check-freshness.sh`) that runs on every session:
- Checks if any evaluation file is >30 days old
- Checks for new GitHub stars not in the catalog
- Outputs a prompt to run `/update-catalog` if anything is stale
- Outputs nothing if everything is current (suppressed)
