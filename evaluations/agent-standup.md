# Evaluation: agent-standup

**Repo:** [Atoll92/agent-standup](https://github.com/Atoll92/agent-standup)
**Stars:** 222 | **Last updated:** not verified (pushed date not fetched this pass) | **License:** MIT
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A live, animated dashboard showing which Claude Code, Codex, and Mistral Vibe sessions are
working, waiting, or need input — shipped as a VS Code extension, a CLI, and a macOS app, and
described by its own README as "your sessions as a live, animated team call."

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the public
GitHub repo page (description, star count, license) plus the CATALOG one-liner and "Overlaps
with" cell. That is sufficient to place the lead; it is not sufficient to support any verdict,
and this eval offers none.

## Triage note

Left at `discovery-log`. No STACK pick is cited in its "Overlaps with" cell (`claude-command-center`,
`agent-of-empires`, `vibe-log-cli` are peers, not incumbents), so this lead carries no structural
redundancy signal — it is ordinary P3 backlog. A multi-session status dashboard is plausibly useful
once several agent sessions run in parallel, but nothing here was exercised to say how well, so it
stays a lead rather than a verdict.

_Triaged 2026-10-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-standup](https://github.com/Atoll92/agent-standup) | tool | Live animated dashboard (MIT) — VS Code extension, CLI, or macOS app — showing which Claude Code, Codex, and Mistral Vibe sessions are working, waiting, or need you | Running several coding-agent sessions gives no at-a-glance view of which one is stalled waiting on input | claude-command-center, agent-of-empires, vibe-log-cli |
