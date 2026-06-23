# Evaluation: design-council

**Repo:** [sjsyrek/design-council](https://github.com/sjsyrek/design-council)
**Stars:** 166 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code plugin that convenes 11 role-specialized peer agents (principal-engineer, security-engineer, performance-engineer, product-manager, etc.) as independent Claude contexts to debate a technical decision in real time. The invoking Claude acts as CEO — routing peer DMs, arbitrating deadlocks, and writing a one-page decision log. Each seat is a separate agent with its own context, so disagreement is structural rather than simulated by a single context wearing different hats.

Two modes: **Debate** for single design decisions (verdict tags, cross-talk, arbitration) and **Review** for codebase audits (parallel findings, dedup, tracker filing). Dynamic roster sizing drops irrelevant seats (no UI → drop ui-ux + a11y; internal tooling → 4–6 seats). Decision logs persist at `~/.claude/councils/` outside any repo.

## How we tested it

**Evidence:** REVIEW

Architecture review of the repo structure, SKILL.md, protocol.md (322 lines), 16 role briefs, review-mode variant, implementation-handoff reference, and opening-prompt template. Not hands-on tested due to the multi-agent orchestration requirements (TeamCreate, parallel Agent spawning with team_name).

```
gh api repos/sjsyrek/design-council/git/trees/main?recursive=1 --jq '.tree[].path'
# Read: SKILL.md (120 lines), protocol.md (322 lines), 16 role briefs, review-mode.md, implementation-handoff.md
```

## What worked

- **Structurally independent perspectives.** Each seat is a separate Claude with its own context — no priming bleed. This is fundamentally different from prompting a single agent to "consider security" vs "consider performance" in sequence.
- **Role briefs are practitioner-quality.** The principal-engineer brief has concrete vetoes (premature abstraction, hypothetical future-proofing), a 300-word cap, and requires file:line citations. Not boilerplate.
- **Production-grade protocol.** 6 phases with explicit failure modes: handshake verification catches silent-spawn failures, 3-round cross-talk hard cap prevents runaway debates, Phase 5 silent-promise guard catches deferred items without tracker entries.
- **Implementation handoff is battle-tested.** Documents real gotchas (`team_name` silently overrides `isolation: "worktree"`, worktree cwd leaks into parent Bash) with concrete fixes — evidence of actual production use.
- **Prompt cache optimization.** Shared `brief.md` written once, referenced by all spawn prompts — 7–12K tokens saved per 8-seat council via 5-minute cache hits.
- **Review mode.** Repurposes the debate infrastructure for parallel codebase audits with P0/P1 priority filtering and strict finding format — a different and useful shape.

## What didn't work or surprised us

- **10–20× token cost.** 8+ parallel contexts, each with role brief + brief.md + cross-talk rounds. Explicitly acknowledged in the README, but this makes it impractical for anything less than high-stakes decisions.
- **166 stars.** Low adoption despite high engineering quality — may indicate the orchestration prerequisites (TeamCreate, parallel Agent, SendMessage) are a barrier to entry for most users.
- **Depends on Claude Code features not universally available.** TeamCreate, team_name on Agent, SendMessage between peers — these are advanced harness features. Plugin won't work on all Claude Code configurations.
- **No eval harness or test suite.** No way to verify the protocol works without running a full council session.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Multi-perspective review catches what single-context misses; structural disagreement surfaces blind spots |
| Speed | - | 10–20× token cost and wall-clock latency of slowest seat; overkill for simple decisions |
| Maintainability | + | Decision logs with rationale, file-ownership maps, and execution plans create durable architectural records |
| Safety | + | Security-engineer seat with explicit vetoes for input validation, secrets, path safety; not a single context's afterthought |
| Cost Efficiency | - | Expensive by design; the token cost is the price of genuine parallelism |

## Verdict

**CONDITIONAL**

Use when a decision crosses ≥2 specialist domains and the output must survive handoff (decision log, tracker items, execution plan). The protocol engineering is the most thorough in the catalog — production-grade with battle-tested gotcha documentation. Skip for bug fixes, single-specialist questions, or quick library picks where the 10–20× token cost isn't earned. Requires advanced Claude Code orchestration features (TeamCreate, peer SendMessage) that may not be available in all configurations.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [design-council](https://github.com/sjsyrek/design-council) | plugin | 11 role-specialized peer agents debate technical decisions | Want multiple perspectives (security, perf, UX, etc.) on architecture choices | llm-council (complementary: llm-council = cross-model, design-council = cross-role within Claude) |
