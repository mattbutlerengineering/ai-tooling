# Evaluation: compound-engineering

**Repo:** [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
**Stars:** 21,725 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Implement (full-loop: Plan → Implement → Review → Reflect)
**Layer:** Tooling

---

## What it does

A full-loop engineering methodology plugin that structures AI-assisted development around the principle "each unit of work should make subsequent units easier." Ships 38+ user-facing skills and 50+ specialist agents across a defined workflow: `/ce-strategy` → `/ce-ideate` → `/ce-brainstorm` → `/ce-plan` → `/ce-work` → `/ce-code-review` → `/ce-compound`. Each skill produces durable artifacts (requirements docs with stable R/A/F/AE identifiers, plans, learnings) that downstream skills read as context.

The plugin is genuinely cross-editor: it ships plugin manifests for Claude Code, Codex, and Cursor, with a Converter/Writer architecture that translates skills and agents into each target's native format. This is not a Claude Code plugin with aspirational Codex support — there's a tested multi-target install path and real Codex agent registration.

## How we tested it

**Evidence:** REVIEW

Architecture-review-based evaluation. Read the repo README, plugin README, CONCEPTS.md glossary, and deep-dove into two representative skill documentation files (ce-brainstorm and ce-code-review) to assess methodology depth, agent design, and quality of implementation.

```
gh api repos/EveryInc/compound-engineering-plugin --jq '.description, .stargazers_count, .updated_at'
gh api repos/EveryInc/compound-engineering-plugin/contents/docs/skills/ce-brainstorm.md --jq '.content' | base64 -d
gh api repos/EveryInc/compound-engineering-plugin/contents/docs/skills/ce-code-review.md --jq '.content' | base64 -d
gh api repos/EveryInc/compound-engineering-plugin/contents/CONCEPTS.md --jq '.content' | base64 -d
```

## What worked

- **Methodology is real, not marketing.** The "compound" concept is backed by concrete mechanics: `/ce-compound` writes structured learnings, `/ce-compound-refresh` prunes stale ones, and upstream skills like `/ce-brainstorm` and `/ce-plan` read learnings as grounding. The loop genuinely compounds.
- **ce-code-review is exceptionally well-designed.** Diff-aware persona selection (4 always-on + cross-cutting + stack-specific reviewers), confidence-gated findings with P0-P3 severity, autofix classification (`gated_auto` / `manual` / `advisory`), and a dedup pipeline. This is more sophisticated than any single review tool in the catalog.
- **ce-brainstorm is a genuine thinking partner.** One-question-per-turn discipline, named gap lenses for premise pressure-testing, 2-3 concrete approaches with tradeoffs before recommending, synthesis summary gate, and fresh-context claim verification. This addresses a real weakness of raw LLM brainstorming.
- **Cross-editor support is architecturally sound.** The Converter/Writer/Bundle model is a proper abstraction, not a shim. Each target gets native format output (not symlinks to Claude Code files).
- **Self-documenting methodology.** CONCEPTS.md maintains a domain glossary with precise definitions for Plugin, Skill, Agent, Target, Converter, Bundle, etc. The project dogfoods its own methodology extensively (the `docs/brainstorms/` directory shows 30+ real brainstorm artifacts).

## What didn't work or surprised us

- **Heavy adoption commitment.** This is a full methodology, not a single skill. You either adopt the CE workflow or you don't — cherry-picking `/ce-brainstorm` alone loses the compounding effect that is the whole point.
- **Overlaps significantly with superpowers.** Both provide brainstorming, TDD, debugging, code review, and verification workflows. Using both simultaneously would create skill conflicts and confusion about which `/brainstorm` or `/code-review` to invoke.
- **311 skill files in the plugin.** The actual user-facing skill count is 38+, but the repo tree has 311 entries under `skills/` — the rest are presumably reference files and sub-components. This high file count may slow plugin install or clutter skill discovery.
- **Not hands-on tested.** Did not install and run the plugin on a real project to verify the skill quality in practice.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Structured brainstorm → plan → review pipeline catches errors at each gate |
| Speed | + | Compound learnings reduce re-discovery across sessions; structured workflow reduces false starts |
| Maintainability | + | Durable artifacts (requirements docs, plans, learnings) serve as documentation and context for future work |
| Safety | neutral | Security review is one persona in ce-code-review but not a primary focus |
| Cost Efficiency | - | Full multi-agent review pipeline and extensive skill files add token overhead |

## Verdict

**CONDITIONAL**

Use when you want a complete, opinionated AI engineering methodology and are willing to commit to it as your primary workflow. The compounding knowledge mechanism is genuinely novel and the individual skill quality (especially ce-brainstorm and ce-code-review) is among the highest in the catalog. However, it substantially overlaps with superpowers (ADOPT) and requires full adoption to realize the compounding benefit — it's not a tool you add alongside other methodology plugins. Best for teams standardizing on one workflow across Claude Code, Codex, and Cursor.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [compound-engineering](https://github.com/EveryInc/compound-engineering-plugin) | plugin | Full-loop engineering methodology where each unit of work makes the next easier | Traditional dev accumulates debt; need a workflow that compounds knowledge across sessions | superpowers, gstack |
