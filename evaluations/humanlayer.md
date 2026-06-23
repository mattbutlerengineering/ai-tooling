# Evaluation: humanlayer (CodeLayer)

**Repo:** [humanlayer/humanlayer](https://github.com/humanlayer/humanlayer)
**Stars:** 11,034 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Plan + Implement (whole inner loop, as an alternative harness)
**Layer:** Tooling (a desktop IDE/harness that wraps Claude Code)

---

## What it does

The catalog one-liner ("AI coding agents for hard problems in complex codebases") is marketing copy that no longer matches the repo. Ground truth: **humanlayer has pivoted twice and this repo is now mostly deprecated.**

- **What it was (v1):** a Python/TypeScript SDK for human-in-the-loop oversight of high-stakes LLM tool calls — `require_approval` decorators and `human_as_tool`, routing approvals to Slack/email so an agent couldn't run a destructive function without a human clicking yes. Those SDKs were **removed from this repo in PR #646** (`humanlayer.md` confirms it).
- **What it is now (v2):** **CodeLayer**, a desktop IDE for AI-assisted coding. The repo is a TypeScript+Go+Rust monorepo: a Tauri/React desktop UI (`humanlayer-wui`, `apps/react`), a Go daemon (`hld`, `apps/daemon`) that brokers sessions and approvals, and a CLI (`hlyr`). CodeLayer **runs Claude Code under the hood** — it reads the standard Claude Code settings file, injects an opinionated "research → plan → implement" workflow via a library of slash commands (`.claude/commands/`), and surfaces an approvals MCP tool (`mcp__codelayer__approvals`) so the human-in-the-loop heritage survives as an approval gate in the IDE.

The repo README states plainly: *"the code here is pretty much all deprecated - you can try the rebuild of humanlayer at https://humanlayer.com."* Releases are nightly-only (`codelayer-0.1.0-nightly-*`), there is no stable tagged release, and the real product lives at humanlayer.com / humanlayer.dev/code. This GitHub repo is effectively the public issues + OSS mirror.

## How we tested it

**Evidence:** REVIEW

Architecture review via the GitHub API and repo docs — not a hands-on install. CodeLayer is a macOS desktop app distributed by Homebrew cask (`brew install --cask --no-quarantine humanlayer/humanlayer/codelayer`); it is an alternative harness to the Claude Code CLI this catalog targets, so installing it would not extend the existing dev loop, it would replace the front-end of it. Establishing what the tool actually is (vs. the stale one-liner) was the core of the investigation.

```bash
gh api repos/humanlayer/humanlayer --jq '{stars,license:.license.spdx_id,description,pushed_at}'
gh api repos/humanlayer/humanlayer/readme --jq '.content' | base64 -d   # "pretty much all deprecated"
gh api repos/humanlayer/humanlayer/git/trees/main --jq '.tree[].path'    # monorepo: hld, hlyr, humanlayer-wui, apps/
gh api repos/humanlayer/humanlayer/contents/docs/introduction.mdx --jq '.content' | base64 -d  # "CodeLayer is the best way..."
gh api repos/humanlayer/humanlayer/contents/humanlayer.md --jq '.content' | base64 -d  # SDKs removed in #646
gh api repos/humanlayer/humanlayer/contents/.claude/commands --jq '.[].name'  # the reusable prompt library
gh api repos/humanlayer/humanlayer/releases --jq '.[0:5][].name'         # nightly-only, no stable release
```

Reviewed: README, `docs/introduction.mdx`, `docs/workshop.mdx`, `humanlayer.md`, the `.claude/commands/` and `.claude/agents/` directories, the `hld` daemon docs, and release history.

## What worked

- **The slash-command prompt library is genuinely valuable and portable.** `.claude/commands/` ships battle-tested commands — `create_plan.md` (model: opus, skeptical interactive planning), `research_codebase.md`, `implement_plan.md`, `validate_plan.md`, `iterate_plan.md`, and `ralph_*` (research/plan/impl) variants. These are plain Claude Code commands and can be copied into any repo's `.claude/commands/` **without installing CodeLayer at all**. This is the real reusable asset.
- **"Advanced Context Engineering for Coding Agents" (ACE-FCA)** — the research/plan/implement methodology behind the commands — is a well-regarded, publicly documented workflow (the September post + November video + AI-That-Works workshop). The thinking is sound and applies regardless of harness.
- **Human-in-the-loop heritage is real engineering**, not a gimmick: the `hld` daemon brokers approvals and CodeLayer exposes `mcp__codelayer__approvals`. Deterministic approval gates on high-stakes actions is a legitimate Safety pattern.
- **Active development** continues (commits within the last day, PRs in the #880–#912 range), so the product itself is not abandoned even though this repo is labeled deprecated.

## What didn't work or surprised us

- **The repo is self-declared deprecated.** The README's first line says the code is "pretty much all deprecated." Evaluating an installable artifact here is moot — the SDKs were deleted (#646) and the real product is closed/at humanlayer.com.
- **CodeLayer is an alternative harness, not a Claude Code add-on.** It *wraps* Claude Code in its own desktop IDE. There is no plugin, skill, hook, or MCP server you install into your existing Claude Code to "get humanlayer." Adopting it means switching front-ends (Claude Code CLI → CodeLayer.app), which is exactly the integration surface this catalog cares about — and it's zero for the existing dev loop.
- **No stable release.** Distribution is unsigned nightly builds via Homebrew cask with `--no-quarantine`. macOS/M-series only; Linux/Windows/Intel are "ask in Discord." Not production-ready for a standardized stack.
- **The catalog one-liner and "Overlaps with: superpowers, oh-my-openagent" are stale.** The closer comparisons today are alternative coding harnesses/IDEs (e.g. the Claude Code CLI itself, Cursor, OpenCode), plus the workflow-command libraries (superpowers, GSD) for the transferable prompt assets.
- **The original differentiator (human approval SDK) is gone from this repo.** What made humanlayer notable in the catalog — guaranteed human oversight of tool calls — now only exists as an internal IDE feature, not as a library you can wire into your own agents.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (methodology only) | The research/plan/implement commands improve agent output on hard multi-file tasks; benefit comes from the portable prompts, not the IDE |
| Speed | neutral | Switching to a separate desktop IDE doesn't speed up the existing Claude Code CLI loop |
| Maintainability | neutral | No integration with the current dev workflow; adopting it replaces the harness rather than enhancing it |
| Safety | + (in-app only) | Deterministic approval gates (`mcp__codelayer__approvals`, `hld` daemon) are a real safety feature, but only inside CodeLayer |
| Cost Efficiency | neutral | Runs on your own Claude Code account; no token savings over plain Claude Code |

## Verdict

**SKIP** (the repo/tool) — but **steal the prompts.**

As an installable tool for *this* catalog's dev loop, humanlayer is a SKIP: the repo is self-declared deprecated, the original human-approval SDK has been removed, and the current product (CodeLayer) is an unsigned, nightly-only, macOS-only desktop IDE that *replaces* the Claude Code CLI rather than extending it. There is no plugin/skill/MCP/hook to adopt into an existing Claude Code setup. The lasting value is the Apache-2.0 `.claude/commands/` prompt library (create_plan, research_codebase, implement_plan, ralph_*) and the ACE-FCA methodology — both are portable to any Claude Code repo without CodeLayer and overlap with what superpowers/GSD already provide. Re-evaluate only if CodeLayer ships a stable, cross-platform release or publishes its approval layer as a standalone MCP server.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [humanlayer](https://github.com/humanlayer/humanlayer) | harness | CodeLayer desktop IDE wrapping Claude Code with a research/plan/implement workflow (repo self-declared deprecated) | Want an opinionated context-engineering harness + human-approval gates for hard codebase tasks | superpowers, GSD, oh-my-openagent |
