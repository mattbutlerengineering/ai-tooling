# Evaluation: claude-code-action

**Repo:** [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
**Stars:** 8,046 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Ship (CI/CD integration)
**Layer:** Tooling

---

## What it does

GitHub Actions integration that deploys Claude Code into PR and issue workflows. Responds to `@claude` mentions in PRs/issues, implements fixes, reviews code, and answers architecture questions. Runs on GitHub Actions runners with full repo and GitHub API access. Supports Anthropic API, AWS Bedrock, Google Vertex AI, and Microsoft Foundry as providers.

## How we tested it

Set up claude-code-action in a GitHub Actions workflow on a test repository. Configured the workflow YAML to trigger on `issue_comment` and `pull_request` events with the `@claude` mention pattern. Set `ANTHROPIC_API_KEY` as a repository secret.

```yaml
# .github/workflows/claude.yml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

Triggered by commenting `@claude please review this PR` on an open pull request, and `@claude implement this` on an issue with a feature description.

## What worked

- Setup takes ~10 minutes: add workflow YAML, set API key secret, done
- Responds within 1-2 minutes on most triggers
- Plays well with existing CI — runs in its own job, doesn't interfere with builds or tests
- Async review is the killer use case — push a PR, come back later to Claude's review comments
- Teammates can invoke it without installing anything locally
- Quality for simple fixes and reviews is excellent (comparable to local Claude Code)

## What didn't work or surprised us

- No persistent memory between invocations — each trigger is a fresh session with no context from prior interactions
- Occasionally times out on very large PRs (>2000 lines changed)
- Cost is non-trivial at scale: $0.50–3.00 per invocation depending on task complexity and repo size
- Complex multi-file features are hit-or-miss (same limitation as local Claude Code)
- No way to configure CLAUDE.md per-workflow — it reads the repo's CLAUDE.md but can't be given workflow-specific instructions easily

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Reviews catch real bugs; fixes are accurate for scoped tasks |
| Speed | + | Async operation means no waiting — results ready when you check back |
| Maintainability | neutral | Output follows repo conventions (reads CLAUDE.md) |
| Safety | neutral | Runs in isolated GitHub Actions runner; no local access |
| Cost Efficiency | - | $0.50–3.00 per invocation adds up with frequent triggers |

## Verdict

**ADOPT**

Low setup cost with immediate value for async code review and issue triage. The per-invocation cost ($0.50–3.00) is reasonable for the time saved on review cycles. Best suited for teams where PR review is a bottleneck or for solo developers who want AI review without interrupting flow. The lack of persistent memory between invocations is the main gap — each trigger starts fresh.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-action](https://github.com/anthropics/claude-code-action) | tool | GitHub Actions integration for async Claude Code in PRs and issues | Brings AI review and implementation into the GitHub collaboration layer without local installs | code-review plugin (local vs CI), pr-review-toolkit (local vs async) |
