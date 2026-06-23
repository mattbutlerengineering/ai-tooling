# Evaluation: claude-code-action

**Repo:** [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action)
**Stars:** 8,097 | **Last updated:** 2026-06-22 (pushed) | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Ship (CI/CD integration)
**Layer:** Tooling

---

## What it does

GitHub Actions integration that deploys Claude Code into PR and issue workflows. Responds to `@claude` mentions in PRs/issues, implements fixes, reviews code, and answers architecture questions. Runs on GitHub Actions runners with full repo and GitHub API access. Supports Anthropic API, AWS Bedrock, Google Vertex AI, and Microsoft Foundry as providers.

Mechanically (confirmed from the cloned source, not the README): `action.yml` is a **composite** action (`runs.using: "composite"`) — not a Docker or node20 action. Its steps install **Bun 1.3.14** (`oven-sh/setup-bun`), run `bun install --production`, then execute the TypeScript entrypoint `src/entrypoints/run.ts` via `bun --no-env-file run`. Post-steps clean up the SSH signing key, post buffered inline comments, and revoke the GitHub App token. The action auto-detects a **mode** per event (`src/modes/detector.ts` returns `"tag"` for `@claude`-mention/label/assignee triggers, `"agent"` when an explicit `prompt` is supplied), and provider selection is wired by mapping the `use_bedrock`/`use_vertex`/`use_foundry` inputs to the `CLAUDE_CODE_USE_BEDROCK`/`_VERTEX`/`_FOUNDRY` env vars on the run step.

## How we tested it

**Evidence:** RUN

**Cloned the real action and ran its own test suite + typechecker on 2026-06-22** (macOS arm64, Bun 1.3.12, Node v20.19.5). This is a **source-and-build run, not a live CI run**: the end-to-end value — an agent triggered by a real `@claude` PR/issue comment on a GitHub Actions runner, making code changes — requires a hosted runner plus an `ANTHROPIC_API_KEY` (or Bedrock/Vertex/Foundry) repo secret and live webhook events, which **was not exercised here and is not invented below**. What *was* executed: the action's structure was read from the actual `action.yml`/`src` tree, and the project's `bun test` and `tsc --noEmit` were run against the cloned repo with captured pass/fail counts.

```bash
# Clone the real action (shallow) into a temp dir
gh repo clone anthropics/claude-code-action -- --depth 1   # default branch: main

# Inspect the real action definition (composite, Bun-based)
grep -nE '^[a-zA-Z_-]+:' action.yml         # name/description/branding/inputs/outputs/runs
# runs.using == "composite"; entrypoint == bun run src/entrypoints/run.ts
# 39 inputs, 5 outputs (execution_file, branch_name, github_token, structured_output, session_id)

# Build + run the project's own checks
bun install            # 155 packages installed [2.62s]
bun test               # → 753 pass, 0 fail, 1651 expect() calls, 41 files [1.64s]
bun run typecheck      # tsc --noEmit → EXIT 0 (clean)
```

**Action definition (read from the real `action.yml`, not the README).** Top-level keys are `name`, `description`, `branding`, `inputs`, `outputs`, `runs`. `runs.using` is **`composite`** with 11 steps (Install Bun → Install Dependencies → subprocess-isolation deps → Run Claude Code Action → token revoke/cleanup post-steps). There are **39 inputs** — including `trigger_phrase`, `assignee_trigger`, `label_trigger`, `prompt`, `anthropic_api_key`, `claude_code_oauth_token`, `use_bedrock`, `use_vertex`, `use_foundry`, `claude_args`, `use_commit_signing`, `plugins` — and **5 outputs**: `execution_file`, `branch_name`, `github_token`, `structured_output`, `session_id`. The action vendors a nested **`base-action/`** ("Claude Code Base Action") that runs the Claude CLI itself; the top-level action is the GitHub-events/trigger/comment layer on top of it.

**Test suite (measured run).** `bun test` executed **753 tests across 41 files, 0 failures, 1651 assertions, in ~1.6 s**. The 31 top-level `*.test.ts` files cover exactly the security- and correctness-critical paths an unattended CI agent depends on: `trigger-validation.test.ts` (26 cases), `sanitizer.test.ts` (token redaction, invisible-char stripping, HTML-comment stripping — prompt-injection defenses), `permissions.test.ts`/`actor.test.ts`/`actor-filter.test.ts` (who may invoke), `modes/detector.test.ts` (tag-vs-agent mode), `token.test.ts`, and `github-file-ops-path-validation.test.ts` (path traversal). **Typecheck (`tsc --noEmit`) passed clean (exit 0).** That the maintained test suite and types are green on a fresh clone is a real signal the published action builds and its trigger/permission/sanitization logic is exercised — independent of any LLM call.

**What required live CI + secrets and was NOT exercised:** the actual agentic loop. No GitHub Actions runner was provisioned, no `ANTHROPIC_API_KEY`/Bedrock/Vertex/Foundry secret was supplied, and no real `@claude` mention, PR review, or code-change-and-push was triggered. The documented trigger workflow (verified against the repo's `examples/claude.yml`) is:

```yaml
# .github/workflows/claude.yml  (from examples/claude.yml)
name: Claude Code
on:
  issue_comment: { types: [created] }
  pull_request_review_comment: { types: [created] }
  issues: { types: [opened, assigned] }
  pull_request_review: { types: [submitted] }
jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')   # (+ analogous guards per event)
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write, issues: write, id-token: write, actions: read }
    steps:
      - uses: actions/checkout@v6
        with: { fetch-depth: 1 }
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

The `@claude`-mention response quality, latency, and per-invocation cost figures below are **carried from prior review / vendor docs, not measured in this run** — they are not observed CI behavior and are labeled as such.

## What worked

- **Composite action, not Docker** — `runs.using: composite` means it layers onto an existing job and reuses the runner's checkout/toolchain; confirmed from the real `action.yml`, matching the "runs in its own job, doesn't interfere with builds" claim.
- **Fresh clone builds and tests green** — `bun install` (155 pkgs, 2.6 s) → `bun test` **753 pass / 0 fail** → `tsc --noEmit` exit 0. The published action is in a buildable, type-clean, fully-tested state.
- **Security-critical paths are unit-tested** — dedicated suites for token redaction/sanitization (prompt-injection defense), actor/permission gating, trigger validation (26 cases), and file-path-traversal validation. For an unattended agent with repo write access, these are the right things to test, and they pass.
- **Multi-provider wiring is real** — `use_bedrock`/`use_vertex`/`use_foundry` inputs map to `CLAUDE_CODE_USE_*` env vars in `action.yml`, so the four-provider claim is structurally present, not just marketing.
- **Auto mode detection** — `detectMode()` cleanly separates `@claude`-mention ("tag") from explicit-`prompt` ("agent") flows; this is unit-tested in `modes/detector.test.ts`.

## What didn't work or surprised us

- **The actual agent behavior was not exercised here** — every claim about response quality, the `@claude` round-trip, real code changes, latency, and cost requires a live runner + API secret, which this run did not provision. Those remain review-level claims.
- **No persistent memory between invocations** (carried from prior review/docs) — each trigger is a fresh session; the source confirms per-run token revocation and cleanup post-steps, consistent with a stateless-per-invocation design.
- **Large input surface** — 39 inputs is a lot of configuration to reason about; getting permissions and trigger guards right in the workflow `if:` is on the user (the example workflow enumerates per-event guards manually).
- **Cost is non-trivial at scale** ($0.50–3.00 per invocation, *vendor/prior-review figure, not measured here*) — adds up with frequent triggers; no local way to cap it beyond `claude_args` like `--max-turns`.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Maintained suite of 753 tests passes (0 fail) on a fresh clone; trigger/permission/mode logic is unit-tested. Agent output correctness itself not measured here. |
| Speed | + | Async operation — results ready when you check back. Composite action layers onto existing job. |
| Maintainability | neutral | Output follows repo conventions (reads CLAUDE.md); clean `tsc --noEmit` and tested codebase. |
| Safety | + | Dedicated sanitizer/token-redaction, actor/permission, and path-traversal test suites all pass; runs in isolated GitHub Actions runner. |
| Cost Efficiency | - | $0.50–3.00 per invocation (vendor/prior-review figure, not measured here) adds up with frequent triggers. |

## Verdict

**ADOPT**

A first-party (Anthropic), MIT-licensed composite GitHub Action whose published source — confirmed by clone — builds clean and passes its own **753-test suite and `tsc --noEmit`**, with dedicated, passing coverage of the security-critical paths (token redaction, actor/permission gating, trigger validation, path-traversal) that an unattended CI agent with repo write access depends on. Setup is low-cost (add workflow YAML + an API-key secret) and the four-provider wiring (Anthropic/Bedrock/Vertex/Foundry) is structurally real. The live agentic loop — an `@claude` mention triggering real code changes on a hosted runner — was **not** exercised here (needs a runner + API secret), so response quality, latency, and the $0.50–3.00/invocation cost remain review-level claims; but the build/test/type health and the safety-test coverage are measured and green, which is exactly what justifies adopting an unattended write-capable action.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-action](https://github.com/anthropics/claude-code-action) | tool | GitHub Actions integration for async Claude Code in PRs and issues | Brings AI review and implementation into the GitHub collaboration layer without local installs | code-review plugin (local vs CI), pr-review-toolkit (local vs async) |
