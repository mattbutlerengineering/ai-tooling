# Evaluation: claude-code-harness

**Repo:** [Chachamaru127/claude-code-harness](https://github.com/Chachamaru127/claude-code-harness)
**Stars:** 2,815 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A structured development harness for Claude Code that enforces a Plan-Work-Review-Release cycle through 5 verb skills (`harness-plan`, `harness-work`, `harness-review`, `harness-release`, `harness-sync`) backed by a Go-native guardrail engine. When you invoke `/harness-plan`, it generates a `spec.md` product contract and `Plans.md` task contract with acceptance criteria, unknowns, and stop conditions. `/harness-work` then executes approved tasks — auto-selecting between solo, parallel (Task tool), and "Breezing" (lead + workers + reviewer) modes based on task count. `/harness-review` runs multi-angle code/plan/scope review as a separate step from implementation. `/harness-release` gates on verified evidence.

The harness intercepts every Write/Edit/Bash call via PreToolUse hooks that route through a compiled Go binary (`bin/harness`), enforcing plan scope and catching drift. It maintains separate `spec.md` (product contract) and `Plans.md` (task ledger) as sources of truth, with precedence rules (`spec.md > sub-spec > Plans.md`). Non-trivial plans automatically trigger multi-perspective validation (Product, Architecture, Security, QA, Skeptic) via subagents or manual single-context pass.

Also supports cross-harness operation: Codex CLI, OpenCode, and Cursor get bounded compatibility via adapter scripts, though only Claude Code is fully supported.

## How we tested it

**Evidence:** REVIEW

Architecture review of the repo structure (1,176+ files), skill content (40 skills across planning, execution, review, session management, and domain-specific workflows), hooks configuration, Go engine source, and documentation. Compared against superpowers (ADOPT) and ralph-claude-code (CONDITIONAL) which occupy the same catalog slot.

```
gh api repos/Chachamaru127/claude-code-harness --jq '.stargazers_count, .updated_at'
# 2815, 2026-06-18T20:52:50Z

# Examined skills: harness-plan, harness-work, harness-review
# Examined hooks.json (63KB of hook configuration)
# Examined Go engine at go/cmd/, go/internal/, go/pkg/
# Checked release cadence: v4.16.0 released today
```

Not hands-on installed — evaluation is architecture-review-based due to the heavy installation footprint (Go binary compilation, hooks rewriting, config files).

## What worked

- **Spec/Plan separation is well-designed.** The `spec.md` (what) vs `Plans.md` (how) split with explicit precedence rules prevents the common failure mode where implementation details leak into requirements. The "Spec delta or Spec skip reason" contract on every plan ensures specs stay current.
- **Auto-mode selection in harness-work is smart.** 1 task = solo, 2-3 = parallel workers, 4+ = Breezing (lead/worker/reviewer). This avoids orchestration overhead on small tasks while scaling up for larger work.
- **Non-trivial planning gate catches scope creep.** Any plan touching multiple files, APIs, data models, or security boundaries automatically triggers multi-perspective validation (5 viewpoints). Lightweight tasks get `not_required_lightweight` and skip the gate.
- **Go-native guardrail engine.** Hooks route through a compiled binary, not shell scripts — faster and more reliable than bash-based hook chains. The engine handles pre-tool validation, relay polling, and state management.
- **Active development with deep documentation.** v4.16.0 released today, 222+ merged PRs, Japanese+English i18n, migration guides, and a cross-harness capability matrix showing honest "not observed" boundaries.
- **The review skill is genuinely independent.** Read-only by default, no auto-commit on approve, explicit "do not push just to review" boundary. This is the right design.

## What didn't work or surprised us

- **Massive installation footprint.** 1,176+ files, 40 skills, Go compilation required, complex hooks.json (63KB). This is a lifestyle choice, not a tool you add to an existing workflow. Compare superpowers which installs via one `claude install-plugin` command.
- **Primary documentation in Japanese.** While English translations exist, the skill files (harness-plan, harness-work, harness-review) have their detailed logic in Japanese. The English descriptions in frontmatter are summaries, not translations of the full skill body. This limits accessibility for English-only teams.
- **Hook interception is aggressive.** Every Write/Edit/Bash/Read call routes through the Go binary — adding latency to every tool invocation. The 10-second timeouts suggest this is a known concern.
- **Not composable.** Like Continuous-Claude-v3, this replaces your workflow rather than enhancing it. You can't cherry-pick the planning skill without the hooks and Go engine. Superpowers' individual skills (TDD, debugging, verification) work independently.
- **Cross-harness support is aspirational.** Codex is "internal-compatible", Cursor is "candidate" — the README is honest about this, but it means the multi-editor promise is largely undelivered.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Spec/Plan contracts prevent scope drift; review is structurally separated from implementation |
| Speed | neutral | Planning overhead saves rework time, but hook latency and Go compilation add friction |
| Maintainability | + | Structured planning with ADR-like spec documents; Plans.md is a persistent task ledger |
| Safety | + | Non-trivial planning gate includes security perspective; hooks enforce plan boundaries |
| Cost Efficiency | - | Heavy context footprint (40 skills, hooks on every tool call, Go binary coordination) |

## Verdict

**CONDITIONAL**

Use when you want a maximally structured development methodology with enforced planning gates and review separation — and you're willing to accept the installation complexity and Japanese-primary documentation. The spec/plan/review separation is genuinely well-designed and the Go-native engine is more robust than bash-based alternatives. However, for most users, superpowers (ADOPT) provides 80% of the discipline with 20% of the complexity: it composes with existing tools, installs in one command, and its individual skills work independently. Choose claude-code-harness over superpowers when you need the non-trivial planning gate (multi-perspective validation), cross-session plan persistence, or the Breezing team execution mode.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-harness](https://github.com/Chachamaru127/claude-code-harness) | harness | Autonomous Plan-Work-Review cycle with Go-native guardrail engine (2.8K stars) | Raw agent work drifts: plans live in chat, tests become optional, review happens too late | superpowers, ralph-claude-code |
