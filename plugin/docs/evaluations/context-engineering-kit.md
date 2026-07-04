# Evaluation: context-engineering-kit

**Repo:** [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit)
**Stars:** ~1,150 | **Last updated:** 2026-06-16 | **License:** GPL-3.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan / Implement (context engineering)
**Layer:** Process / Tooling

---

## What it does

A hand-crafted, token-efficient marketplace of context-engineering skills for Claude Code (and OpenCode/Cursor/Antigravity/Gemini CLI). The premise: generic skills bloat the context window and produce inconsistent results; this kit provides curated techniques/patterns focused on improving agent **result quality and predictability** with minimal token footprint.

Per the README, the design principles are: **simple to use** (no dependencies; automatically-used skills plus self-explanatory commands), **token-efficient** (carefully crafted prompts; prefers command-oriented skills backed by **sub-agents** over general information skills, to avoid populating context with unnecessary info), and **quality-focused** (each plugin targets a specific area of agent results). The marketplace is built from prompts the company's developers use daily, supplemented by plugins derived from benchmarked papers and high-quality projects, with a GitHub Action for CI integration.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the design principles (token-efficient, command-oriented sub-agent skills, quality-focused plugins, CI integration). Confirmed the multi-tool compatibility and the deliberate token-minimization approach (sub-agent-backed commands over context-filling info skills). Not installed/run live, so condition-gated.

```bash
gh api repos/NeoLabHQ/context-engineering-kit --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/NeoLabHQ/context-engineering-kit/readme --jq '.content' | base64 -d
```

## What worked

- **Token-efficiency by design.** Preferring command-oriented, sub-agent-backed skills over context-filling info skills directly addresses context bloat — the right instinct for quality+predictability.
- **Curated, not a dump.** Skills come from daily-used company prompts plus benchmarked-paper plugins, rather than an unfiltered awesome-list — higher signal.
- **Multi-tool + CI.** Works across Claude Code/OpenCode/Cursor/Antigravity/Gemini CLI with a GitHub Action, so it fits real pipelines.

## What didn't work or surprised us

- **GPL-3.0.** Strong copyleft may matter depending on how you integrate/distribute it — check obligations.
- **Quality claims need verification.** "Improves agent results" is the right goal but unproven without your own measurement (pair with waza/promptfoo to confirm on your tasks).
- **Overlaps pro-workflow/ACE/superpowers.** Several curated skill systems exist; this one's edge is the explicit token-efficiency + quality focus.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Quality-focused, curated skills aim to improve agent output |
| Speed | + | Sub-agent-backed commands keep the parent context lean |
| Maintainability | + | Curated, CI-integrated skills vs. ad-hoc prompt sprawl |
| Safety | neutral | Skill content; audit individual plugins |
| Cost Efficiency | + | Token-minimizing design reduces context spend |

## Verdict

**CONDITIONAL**

Adopt if you want a curated, token-efficient set of context-engineering skills aimed at agent result quality/predictability across multiple coding agents, and the GPL-3.0 license fits your use. Its sub-agent-backed, context-lean design is a thoughtful answer to skill bloat. Verify the quality gains on your own tasks (waza/promptfoo) rather than trusting the claim. Overlaps pro-workflow/ACE/superpowers — pick by the token-efficiency emphasis.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) | plugin | Token-efficient context-engineering skills marketplace (GPL-3.0) — curated context-engineering techniques (auto-used skills + command-oriented sub-agent skills) focused on improving agent result quality/predictability with minimal token footprint; CI integration; multi-tool | Generic skills bloat context and give inconsistent results; want curated, token-efficient context-engineering skills that measurably improve agent output | pro-workflow, ACE, superpowers (skills), claude-code-best-practice |
