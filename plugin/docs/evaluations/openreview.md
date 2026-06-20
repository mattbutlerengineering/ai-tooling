# Evaluation: OpenReview (Vercel Labs)

**Repo:** [vercel-labs/openreview](https://github.com/vercel-labs/openreview)
**Stars:** 1,438 | **Last updated:** 2026-03-06 (pushed; ⚠️ quiet since) | **License:** ⚠️ none declared | **Releases:** 0
**Dev loop stage:** Review / Ship (automated PR review bot in CI/GitHub)
**Layer:** Infrastructure (self-hosted Next.js app deployed to Vercel; GitHub App)

---

## What it does

OpenReview is an **open-source, self-hosted AI code-review bot** from Vercel Labs. You deploy it to Vercel, connect a GitHub App, and then **mention `@openreview` in any PR comment** to trigger an on-demand review powered by Claude (Sonnet 4.6 via the AI SDK). It is explicitly **beta** — built as an internal Vercel project to dogfood their stack together — with "expect rough edges and breaking changes."

The notable part is *how* it reviews: each run spins up an isolated **Vercel Sandbox**, clones the repo on the PR branch, installs dependencies, and gives a Claude agent **full repo access** — so it can read files, **run linters/formatters/tests**, and explore the codebase, not just diff-read. It then:
- posts **line-level inline comments** with GitHub suggestion blocks for one-click fixes,
- can **directly fix** formatting/lint/simple bugs and **commit + push** to the PR branch,
- uses **reactions** as a control surface (👍/❤️ to approve a suggestion, 👎/😕 to skip),
- runs on **Vercel Workflow** for durable, resumable execution, and
- supports **custom skills** via `.agents/skills/` on top of built-in review skills.

## How we tested it

**Source-grounded inspection — not installed, not deployed.** No Vercel deploy, no GitHub App connected, no PR reviewed. Claims come from the repository (GitHub metadata, README feature list, sequence diagram) — the project's own documentation, not observed review behavior.

```bash
gh api repos/vercel-labs/openreview --jq '{stars,pushed_at,license:.license,releases:0}'
gh api repos/vercel-labs/openreview/readme --jq '.content' | base64 -d   # features, how-it-works, deploy
```

## What worked

- **Sandboxed, tool-running review is the right design.** Cloning the PR branch and letting the agent actually *run* linters/tests/explore — rather than reasoning over a raw diff — produces grounded, executable review and is a clear step up from diff-only bots.
- **Inline suggestions + auto-commit close the loop.** One-click GitHub suggestion blocks and the ability to push trivial fixes (formatting/lint/simple bugs) turn review into remediation, not just commentary.
- **On-demand via mention + reaction controls** is an ergonomic, low-noise interaction model (you ask for review when you want it; you approve/skip with emoji) versus bots that spam every PR.
- **Durable execution + extensible skills.** Vercel Workflow gives resumable runs; `.agents/skills/` means teams can encode their own review standards. Powered by current Claude (Sonnet 4.6).
- **Credible provenance** (Vercel Labs) and a one-click deploy template.

## What didn't work or surprised us

- **⚠️ No license.** No LICENSE file despite "open-source" framing and 1.4K stars — default copyright means no granted right to use/modify/redistribute. For something you're meant to fork and self-host, this is a real blocker; resolve (open an issue) before depending on it.
- **⚠️ Beta + quiet.** Self-described beta with breaking changes, **0 releases**, and last pushed **2026-03-06** (~3 months before evaluation) — momentum is unclear for an "internal project"; treat as experimental.
- **Vercel-platform coupling.** Vercel deploy + Vercel Sandbox + Vercel Workflow + Upstash KV is the happy path; running it elsewhere is non-trivial. It's "self-hosted" but effectively Vercel-hosted.
- **Powerful permissions.** A bot that can commit and push to PR branches and run arbitrary project tooling in a sandbox needs careful GitHub App scoping and branch protections — push access is part of the value and part of the risk.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Running linters/tests and exploring the repo (not just the diff) grounds findings; inline suggestions catch real issues with one-click fixes. |
| Speed | + | On-demand reviews + auto-committed trivial fixes shorten the review→merge loop. |
| Maintainability | neutral | Improves PRs; doesn't change your codebase architecture. |
| Safety | neutral / − | Runs in an isolated Vercel Sandbox (+), but holds GitHub push access and runs project tooling — needs tight App scoping (−). |
| Cost Efficiency | neutral / − | Self-host is free code, but Vercel Sandbox/Workflow/KV + Claude tokens are ongoing platform + model spend. |

## Verdict

**CONDITIONAL** — adopt if you're on Vercel and want a self-hosted, on-demand PR-review bot that actually runs your tooling in a sandbox and can push trivial fixes, with extensible team skills. The sandboxed-execution + inline-suggestion + auto-commit design is strong and the Claude/AI-SDK foundation is current. But two gates are significant: **no declared license** (blocks safe reuse until fixed) and **beta status with no releases and ~3 months of quiet**, plus heavy Vercel-platform coupling. Pilot it; don't make it load-bearing yet. If you want a more turnkey, platform-neutral reviewer, PR-Agent or the Anthropic `code-review` plugin are alternatives.

Compared to neighbors: **PR-Agent** is a mature, platform-agnostic PR bot; **code-review**/**pr-review-toolkit** are Claude Code review plugins for local/agent use; **claude-code-action** wires Claude into GitHub Actions. OpenReview is the **Vercel-native, sandbox-executing, auto-fixing** PR bot — distinctive for running tooling and pushing fixes, distinctive also for its license/maturity gaps.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [openreview](https://github.com/vercel-labs/openreview) | tool | Self-hosted AI PR-review bot (Vercel Labs) — mention @openreview, it reviews in a Vercel Sandbox with full repo access (runs linters/tests), posts inline suggestions, and can auto-commit fixes; powered by Claude (⚠️ beta, no license) | Want on-demand PR review that runs your actual tooling and can push trivial fixes, not just diff-read | PR-Agent, code-review, claude-code-action |
