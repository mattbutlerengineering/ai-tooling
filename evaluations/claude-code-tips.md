# Evaluation: claude-code-tips

**Repo:** [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips)
**Stars:** 8,852 | **Last updated:** 2026-06-19 | **License:** unlicensed (no SPDX)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** All (cross-cutting reference)
**Layer:** Process

---

## What it does

A curated collection of 43 practical Claude Code tips organized from basics to advanced, written by a power user (YK Dojo / ykdojo). Covers slash commands, voice input, task decomposition, git workflows, context management, verification, TDD, background tasks, containerization, and automation. Ships as a Claude Code plugin (dx plugin) with a custom status line script that displays model, directory, branch, uncommitted files, sync status, and token usage in a configurable color-themed bar.

## How we tested it

**Evidence:** REVIEW

Read the full README (43 tips across ~3,000 lines of content) and assessed each tip against the catalog's existing knowledge base. Checked the repo structure: `.claude-plugin/` with marketplace.json and plugin.json, `scripts/` with the status line bar, `skills/` directory, and `content/` with supplementary articles. Compared against the four other Claude Code reference entries in the catalog (claude-howto, claude-code-best-practice, learn-claude-code, claude-code-system-prompts).

```
gh api repos/ykdojo/claude-code-tips --jq '.description, .stargazers_count, .updated_at'
gh api repos/ykdojo/claude-code-tips/readme --jq '.content' | base64 -d | wc -l
# ~3,000 lines of README content
```

## What worked

- **Practitioner voice**: tips come from genuine usage patterns, not documentation paraphrasing. Tip 5 ("AI context is like milk; it's best served fresh and condensed") encapsulates context management better than most guides
- **Status line script** is the most concrete deliverable — a working bash script with 10 color themes that shows model, tokens, branch, and sync status. Genuinely useful
- **Tip 19 (containers for risky tasks)** and **Tip 14 (git worktrees)** provide actionable setup instructions, not just concepts
- **Tip 31 (audit approved commands)** surfaces a real security concern most users miss — checking what permissions have accumulated
- **dx plugin** ships as an installable Claude Code plugin, making it a living reference rather than a static document
- **Active maintenance**: updated daily, 8.8K stars, community engagement through content articles

## What didn't work or surprised us

- **No SPDX license** — the repo has a LICENSE file but GitHub doesn't recognize it, which may deter enterprise adoption
- **Tips 20, 35, 40, 41 are motivational**, not technical — padding that dilutes the signal ("The best way to get better is by using it", "Keep learning!")
- **No progressive disclosure**: 43 tips in one flat README is overwhelming. No categorization by skill level beyond implicit ordering
- **Overlap with built-in Claude Code knowledge**: tips like "use /clear" and "use Cmd+A" are things Claude Code already tells users. The value is in the non-obvious tips (19, 31, 14, 5)
- **Status line script is macOS-centric** — relies on zsh and macOS-specific paths

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Tips are accurate but don't prevent bugs directly |
| Speed | + | Context management tips (5, 8) and voice input (2) genuinely accelerate workflows |
| Maintainability | neutral | No direct code quality impact |
| Safety | + | Tip 31 (audit permissions) and Tip 19 (containers) improve security posture |
| Cost Efficiency | + | Context management tips (5, 8, 15) reduce token waste |

## Verdict

**SKIP** — superseded by two catalogued guides that dominate it on every axis. "43 tips" at ★9.1K
with no parseable licence (`NOASSERTION`) sits behind `claude-code-best-practice` (★62K, MIT,
comprehensive, pushed today) and `claude-howto` (★39.6K, MIT, visual and example-driven) — both of
which it names in its own "Overlaps with" cell.

The distinctive artifacts it ships beyond the tips are a status-line script and a container setup.
Those are real, and they are also the parts most likely to be stale in a tips repo: harness-specific
scaffolding ages with the harness.

A tips list is the reference genre with the shortest half-life, and this catalog already carries the
two long-form guides that absorb it.

Re-open if the tips repo becomes the fast-moving one — a frequently-updated tips list would beat a
comprehensive guide on recency, which is the one thing it could win on.


_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-tips](https://github.com/ykdojo/claude-code-tips) | reference | 43 tips for getting the most out of Claude Code with status line script and container setup | Need practical tips and tricks for Claude Code power users | claude-code-best-practice, claude-howto |
