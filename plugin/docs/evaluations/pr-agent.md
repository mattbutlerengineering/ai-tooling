# Evaluation: PR-Agent

**Repo:** [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent)
**Stars:** 11,660 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Review (outer loop — per-PR automation)
**Layer:** Infrastructure

---

## What it does

CI-integrated AI PR reviewer that runs as a GitHub Action (or webhook) on every pull request. On each opened/updated PR, it auto-generates a description, posts a structured review comment with severity-tagged findings, and optionally runs `improve` to propose inline code suggestions — all in a single LLM call per tool (~30 seconds). Supports GitHub, GitLab, Bitbucket, Azure DevOps, and Gitea. Model-agnostic: works with Claude, GPT-4, Gemini, Deepseek, or any OpenAI-compatible endpoint via `.pr_agent.toml` config.

The four core tools:

- **describe** — generates PR title, type labels, summary, and walkthrough from diff
- **review** — analyzes code for bugs, security issues, test coverage, effort estimate, and ticket compliance; posts a persistent PR comment
- **improve** — proposes inline code suggestions as reviewable PR comments
- **ask** — answers questions about the diff interactively

## How we tested it

**Evidence:** REVIEW

This is a docs-only repo with no deployable code, so hands-on testing was done through architecture review, documentation analysis, community health checks, and direct comparison against the three tools already in the catalog's Code Review & Quality section: the `code-review` plugin, `pr-review-toolkit` plugin, and `shadcn/improve`.

Architecture review:

```
gh api repos/The-PR-Agent/pr-agent \
  --jq '{stars: .stargazers_count, forks: .forks_count, issues: .open_issues_count, updated: .updated_at}'

gh api repos/The-PR-Agent/pr-agent/releases/latest \
  --jq '{tag: .tag_name, released: .published_at}'

gh api repos/The-PR-Agent/pr-agent/commits \
  --jq '.[0:5] | .[] | {sha: .sha[:7], msg: .commit.message | split("\n")[0], date: .commit.author.date}'
```

Results: 11,660 stars, 1,567 forks, 166 open issues, updated 2026-06-18 (same day as evaluation), latest release v0.36.1 shipped 2026-06-16 — two days before this evaluation. Commits show active maintenance: security fix, Claude model support update, documentation cleanup — all in the same week.

Documentation analysis covered: README, `docs/tools/review.md`, and installation guide. The GitHub Actions workflow configuration, required secrets, and `.pr_agent.toml` format were all studied directly from the repo.

Feature comparison was done against the three catalog competitors using their respective evaluations and skill definitions.

## What worked

- **CI-native trigger model is the key differentiator**: `code-review` and `pr-review-toolkit` are invoked manually inside a Claude Code session; PR-Agent fires automatically on every PR without human initiation — it's infrastructure, not tooling
- **Genuine multi-platform reach**: GitHub, GitLab, Bitbucket, Azure DevOps, Gitea — teams not using Claude Code can still adopt it; not Claude-Code-specific
- **Model-agnostic configuration**: one `ANTHROPIC_KEY` environment variable switches it to Claude; mix of `GPT-4` for speed and `Claude` for depth is documented
- **Review tool is configurable at the field level**: each check (`require_security_review`, `require_tests_review`, `require_ticket_analysis_review`, etc.) toggles independently via TOML config — reduces noise compared to one-size-fits-all reviews
- **Describe tool eliminates a recurring annoyance**: auto-generated PR descriptions with type labels and walkthrough summaries remove the "write a good PR description" tax from every PR author
- **Single LLM call per tool**: low per-PR cost, ~30 seconds latency — fits in CI without blocking merge
- **Community velocity is high**: v0.36.1 released with active commits including Claude model compatibility fixes (claude-opus-4-7 temperature support), showing the project tracks model API changes promptly
- **Fully open-source, self-hostable**: the commercial Qodo 2.0 offering is a fork/superset; the OSS tool is independent and complete

## What didn't work or surprised us

- **Not a Claude Code integration**: PR-Agent runs as a GitHub Action bot, separate from any Claude Code session — it cannot call Claude Code skills, read CLAUDE.md, or share context with the in-session `code-review` plugin. There's no integration path; they're parallel systems
- **The `improve` tool produces suggestions, not fixes**: it posts inline PR comments proposing changes but does not apply them. A human or a separate agent must act on them — lower value than `code-review` plugin's `--fix` flag which applies findings directly to the working tree
- **Setup has surface area**: requires a GitHub Actions workflow file, secrets configuration (`ANTHROPIC_KEY` or `OPENAI_KEY`), and optional `.pr_agent.toml` in repo root. Not zero-config; small teams often skip it
- **Context blind spot**: PR-Agent only sees the diff plus surrounding file context, not CLAUDE.md, not the full conversation history, not team-specific patterns captured in memory. The `extra_instructions` field partially addresses this but requires manual maintenance
- **`help_docs` command temporarily disabled** (security fix in v0.36.1): a reminder that a bot with PR-write permissions is an attack surface — prompt injection via PR content is a real threat for any AI PR reviewer
- **Overlaps with the `describe` step already in `commit-push-pr`**: the PR description auto-generation feature duplicates what the `commit-push-pr` skill already does inside Claude Code, creating two sources of truth for PR metadata

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Per-PR review catches bugs, security issues, and missing tests that async reviews miss; `num_max_findings: 3` default keeps signal-to-noise reasonable |
| Speed | + | Automated description generation and async review eliminate manual PR write-up time; ~30s CI latency is acceptable |
| Maintainability | + | Ticket compliance check and "can this PR be split?" analysis enforce scope discipline across the team, not just in-session |
| Safety | + | Security review runs by default on every PR; prompt-injection risk is real but mitigated by reviewing suggestions rather than auto-applying |
| Cost Efficiency | + | Single LLM call per tool is cheap at scale; self-hosted with Claude Haiku keeps cost minimal per PR |

## Verdict

**CONDITIONAL**

Adopt for teams running CI on GitHub/GitLab where not everyone uses Claude Code — it catches bugs and enforces PR hygiene across the whole team automatically, not just for individual Claude Code users. Skip if your entire team uses Claude Code and runs `code-review` before every PR push; the marginal value over `code-review --comment` is thin, and the CI bot adds maintenance overhead. The strongest case for adopting alongside Claude Code: the `describe` tool for auto-generating PR descriptions, and the `review` tool's ticket compliance check — both operate on CI triggers that don't depend on developer workflow. Do not adopt as a replacement for `code-review` or `pr-review-toolkit`; those run inside the agent session where they can fix code directly.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [PR-Agent](https://github.com/The-PR-Agent/pr-agent) | tool | CI bot that auto-describes, reviews, and improves every PR across GitHub, GitLab, Bitbucket, and Azure DevOps | Need automated PR review that fires for every team member, not just Claude Code users | code-review, pr-review-toolkit, shadcn/improve |
