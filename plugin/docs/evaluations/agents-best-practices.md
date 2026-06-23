# Evaluation: agents-best-practices

**Repo:** [DenisSergeevitch/agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices)
**Stars:** 1,976 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Plan / Implement
**Layer:** Tooling

---

## What it does

A provider-neutral agent skill for designing, auditing, and generating MVP blueprints for agentic harnesses. The 209-line SKILL.md orchestrator defines when to activate (any agent architecture conversation), how to classify the design problem (domain, autonomy level, risk, state duration, tool surface, validation), and which of 17 reference files to load on demand. The reference corpus totals 4,518 lines across architecture, agentic loops, tool design, permissions, context/memory/compaction, planning, workflow orchestration, skills/connectors, system prompts, provider API patterns, security, evals, observability, and checklists.

The standout feature is MVP Builder Mode: when a user says "build an agent for X," the skill instructs the agent to produce a concrete domain-specific harness blueprint — not generic advice — covering the core loop, tool registry, permission matrix, context/memory, planning mode, cost strategy, observability, and launch path. A separate `coding-agents.md` reference specializes this for repository-facing coding agents with a "draft + verify + explain, not merge + deploy + own production" boundary.

## How we tested it

**Evidence:** REVIEW

Architecture-review evaluation: read the full SKILL.md, all 17 reference files via GitHub API, and assessed structure, depth, correctness, and progressive disclosure design. Did not install locally (blocked by auto-mode permissions) so no hands-on invocation testing.

```bash
gh api repos/DenisSergeevitch/agents-best-practices/contents/SKILL.md --jq '.content' | base64 -d
gh api repos/DenisSergeevitch/agents-best-practices/contents/references --jq '.[].name'
# Read each reference file via API
```

## What worked

- **Progressive disclosure is well-designed.** The 209-line orchestrator loads only the relevant references for each conversation, not all 4,518 lines. The reference map gives clear activation criteria per file.
- **MVP Builder Mode is actionable.** It produces concrete architecture, not bullet-point advice. The 12-point default answer structure (harness boundary, loop, instructions, tools, context, planning, workflow, skills, safety, observability, rollout, legibility) is a genuine design checklist.
- **Coding-agent specialization is accurate.** The `coding-agents.md` reference correctly scopes an MVP coding agent as "draft + verify + explain" with evidence requirements, task profiles (bug-fix, feature, refactor, migration), and explicit anti-patterns.
- **Checklists are comprehensive.** 6 checklists covering MVP blueprint, design, tools, permissions, context, and security — each with concrete, checkable items (not vague "consider security").
- **Provider-neutral API patterns.** Covers OpenAI, Anthropic, and OpenAI-compatible APIs with implementation differences, making it useful across ecosystems.

## What didn't work or surprised us

- **No hands-on validation.** Could not install due to permissions; evaluation is architecture-review only. The skill's quality depends on whether agents actually follow the multi-reference progressive disclosure pattern correctly.
- **Large context cost when fully loaded.** If all 17 references load simultaneously (unlikely by design, but possible), the ~4,700-line corpus would consume significant context window.
- **No eval harness or metrics.** Unlike guard-skills or Claude-BugHunter, there's no before/after measurement of whether agents produce better harness designs with this skill loaded.
- **Overlap with built-in agent knowledge.** Claude and Codex already know about agent architecture — the skill's value depends on whether it surfaces patterns the model wouldn't otherwise apply.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | MVP Builder Mode produces structured harness designs with explicit boundaries and validation criteria |
| Speed | + | Reference map avoids loading unnecessary context; pre-built checklists save design time |
| Maintainability | + | 12-point design structure and ADR-style decision recording improve long-term harness clarity |
| Safety | + | Permission matrix, risk classification, and draft/commit separation are baked into every blueprint |
| Cost Efficiency | neutral | Progressive disclosure limits context cost, but full reference corpus is large |

## Verdict

**CONDITIONAL**

Use when designing or auditing an agentic harness — especially for non-coding domains (operations, finance, legal, healthcare) where the agent has less built-in architecture knowledge. The MVP Builder Mode and coding-agent specialization are genuinely useful for teams building production harnesses. For simple Claude Code / Codex usage within established patterns, the skill adds context cost without proportional benefit. At 2K stars with active maintenance, it's the most substantive agent architecture reference skill in the catalog.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices) | skill | Provider-neutral agent skill for Codex, Claude Code, and agentic harness design (2K stars) | Agent design best practices are scattered; provides a consolidated reference | claude-code-best-practice, andrej-karpathy-skills |
