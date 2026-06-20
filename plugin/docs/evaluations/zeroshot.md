# Evaluation: zeroshot

**Repo:** [the-open-engine/zeroshot](https://github.com/the-open-engine/zeroshot)
**Stars:** ~1,520 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Implement (autonomous orchestration)
**Layer:** Tooling

---

## What it does

An open-source AI coding-agent **orchestration CLI** that runs multi-agent workflows to autonomously implement, review, test, and verify code changes. The tagline: point it at an issue, walk away, and return to production-grade code.

Mechanically it runs a **planner**, an **implementer**, and independent **validators** in isolated environments, looping until changes are **verified** or **rejected** with actionable, reproducible failures. It's explicitly built for tasks where correctness matters more than speed — the independent-validator loop is the differentiator from a single agent that might ship subtly wrong code. It's multi-provider (Claude/Codex/Gemini/OpenCode) and supports GitHub, GitLab, Jira, and Azure DevOps as issue backends, so it slots into real ticket workflows.

## How we tested it

Architecture review against the README and the documented loop (planner → implementer → independent validators in isolated environments → verify/reject with reproducible failures). Confirmed the correctness-first framing, the independent-validation design, the multi-provider support, and the multi-platform issue backends. Not run on a live issue, so condition-gated.

```bash
gh api repos/the-open-engine/zeroshot --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/the-open-engine/zeroshot/readme --jq '.content' | base64 -d
```

## What worked

- **Independent validators, correctness-first.** Separating implementation from independent verification (and looping until verified/rejected) directly targets the "agent ships plausible-but-wrong code" failure — a meaningful design choice.
- **Issue→PR, hands-off.** Pointing it at a GitHub/GitLab/Jira/Azure issue and getting verified changes fits real ticket-driven workflows.
- **Provider-agnostic.** Works across Claude/Codex/Gemini/OpenCode, so you're not locked to one model/CLI.

## What didn't work or surprised us

- **Correctness over speed (by design).** The verify/reject loop spends more time and tokens than a single pass — acceptable for the stated use case, but not for quick edits.
- **Autonomy risk.** "Walk away" automation needs guardrails/review on what it merges; verify the isolation and approval model for your repo.
- **Overlaps Archon/flow-next/ruflo.** Several tools orchestrate plan→implement→verify; zeroshot's edge is the independent-validator, reproducible-failure loop with multi-platform issue backends.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Independent validators loop until verified — catches subtle errors |
| Speed | - | Verify/reject iterations trade speed for correctness |
| Maintainability | + | Reproducible failures make rejected runs actionable |
| Safety | + | Isolated environments per run; verification gate before acceptance |
| Cost Efficiency | - | Multi-agent verify loops consume more tokens than a single pass |

## Verdict

**CONDITIONAL**

Adopt for hands-off, correctness-first issue→PR automation where an independent-validation loop (planner/implementer/validators in isolation) matters more than turnaround speed — and you'll review what it merges. Multi-provider and multi-platform-issue support make it practical for ticket-driven teams. Overlaps Archon/flow-next/ruflo; choose zeroshot for the independent-validator, reproducible-failure emphasis.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [zeroshot](https://github.com/the-open-engine/zeroshot) | harness | Autonomous coding-agent orchestration CLI (MIT) — planner → implementer → independent validators in isolated environments, looping until changes verify or reject with reproducible failures; point it at a GitHub/GitLab/Jira/Azure issue; multi-provider | Want hands-off, correctness-first issue→PR automation with independent validation, not a single agent that may ship subtly wrong code | Archon, flow-next, ruflo, claude-octopus |
