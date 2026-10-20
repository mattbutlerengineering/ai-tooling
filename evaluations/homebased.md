# Evaluation: homebased

**Repo:** [avencera/homebased](https://github.com/avencera/homebased)
**Stars:** 2 | **Last updated:** 2026-10 (recently active; exact push date not independently verifiable this session — see below) | **License:** none specified
**Last verified:** 2026-10-20
**Last triaged:** 2026-10-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Runs long-running tasks (builds, test suites, agent reviews) in the background for
Codex and Claude Code sessions, so the session isn't blocked while they finish, and
reports the result back into the same thread when done.

## How we tested it

**Evidence:** SOURCE-ONLY

**Source-grounded review — not run hands-on.** This session's GitHub access is
scoped to `mattbutlerengineering/ai-tooling` only; arbitrary-repo API lookups and
installs are not available without an explicit `add_repo` grant, which an
unattended discovery pass does not request. This read comes from the repo's public
GitHub page (About text, README, file tree) via a web fetch, not from running the
tool. The repo's visible file tree carries no `LICENSE` file.

## What worked

- N/A — not run.

## What didn't work or surprised us

- N/A — not run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Not exercised. |
| Speed | neutral | Not exercised. |
| Maintainability | neutral | Not exercised. |
| Safety | neutral | Not exercised. |
| Cost Efficiency | neutral | Not exercised. |
| Verifiability | neutral | Not exercised. |

## Triage note

Left at `discovery-log` — a P3 backlog lead (no STACK-pick overlap, no archival/license
disqualifier). It's a small (2-star), genuinely new tool rather than a clear
redundancy call: it targets background execution of long agent tasks specifically for
Codex/Claude Code, which is a narrower, more current-tooling-specific niche than the
general sandboxed-orchestration peers (`sandcastle`, `flow (Aixle)`, `oh-my-agent`) it
cites. No LICENSE file is visible in the repo; note that if it's ever considered
further. Left for a real hands-on eval rather than a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [homebased](https://github.com/avencera/homebased) | tool | Runs long agent tasks (builds, test suites, reviews) in the background for Codex and Claude Code, reporting back to the same thread | Long-running agent tasks block the session until they finish; want to keep working while they complete elsewhere | sandcastle, flow (Aixle), oh-my-agent |
