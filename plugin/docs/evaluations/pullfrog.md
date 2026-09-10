# Evaluation: Pullfrog

**Repo:** [pullfrog/pullfrog](https://github.com/pullfrog/pullfrog)
**Stars:** 1.2K | **Last updated:** 2026-09-10 (pushed) | **License:** MIT
**Last verified:** 2026-09-10
**Last triaged:** 2026-09-10  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An open-source, model-agnostic BYOK GitHub bot that runs entirely inside GitHub Actions —
no hosted service. It wraps Claude Code, Codex, or OpenCode (whichever matches your
BYOK/BYO-subscription config) to auto-review every incoming PR (can gate merges via
required status checks), respond to review comments like a human collaborator, and detect
and attempt to fix CI failures on its own PRs (configurable to fix human PRs too).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. Overlaps a cluster of already-catalogued self-hosted
PR-review bots (PR-Agent, open-code-review, juror, openreview) but cites no STACK
incumbent (P3, zero overlap pressure), so there is no named tool to call it redundant with.
Distinct in mechanism from the nearest catalog peer, `openreview` (Vercel Sandbox, Claude-only,
⚠️ dormant since 2026-03): pullfrog is model-agnostic (wraps whichever of Claude
Code/Codex/OpenCode matches your config), runs purely in GitHub Actions rather than a
sandbox service, and is actively developed (commits the day this was triaged). Worth a
real look given the size of this cluster and pullfrog's traction (★1.2K since a May 2026
announcement).

_Triaged 2026-09-10 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pullfrog](https://github.com/pullfrog/pullfrog) | tool | Open-source, model-agnostic BYOK GitHub bot (MIT, ★1.2K) that runs entirely in GitHub Actions — wraps Claude Code/Codex/OpenCode to auto-review every PR (mergeable via status checks), address review comments like a human colleague, and auto-fix its own or human PRs' CI failures | Hosted AI PR-review services charge per-seat and lock you to one model; want a self-hosted, BYOK reviewer that runs in your own GitHub Actions | PR-Agent, juror, open-code-review, openreview |
