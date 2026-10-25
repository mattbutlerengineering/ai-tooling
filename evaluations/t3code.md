# Evaluation: t3code

**Repo:** [pingdotgg/t3code](https://github.com/pingdotgg/t3code)
**Stars:** 30,000 | **Last updated:** n/a (not checked via API; this session's GitHub access is repo-scoped) | **License:** MIT
**Last verified:** 2026-10-25
**Last triaged:** 2026-10-25  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A mobile + web + desktop (Electron) control surface for driving your own coding-agent
sessions — Claude Code, Codex, Cursor, Grok Build, OpenCode, and Google Antigravity —
remotely, over your existing subscriptions rather than a metered API. The project's own
README describes it as "very very early" with bugs expected and most contributions not
yet accepted.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
repo's own README (fetched over the web, since this session's GitHub API access is
scoped to this repository and does not extend to arbitrary repos) plus the CATALOG
"Overlaps with" cell. That is sufficient to place the lead against its closest catalog
peers, not to support any verdict, and none is offered here.

## Triage note

Cites `claude-squad` (a STACK pick) in its "Overlaps with" cell, which bands this P2
challenger — but `claude-squad` is a local terminal TUI for parallel sessions, while
`t3code` is explicitly a *remote* control surface with native mobile and web apps,
working across six different agent vendors rather than just Claude Code. That is the
same differentiator that kept `orca` (also cited) and `codex-mobile-bridge` at
`discovery-log` rather than SKIPped — remote/mobile access to a fleet of agent CLIs is
a different job from a local TUI, not a worse version of the same one. It is also
explicitly pre-1.0 and "very very early" by its own README, which argues for a real
hands-on look once it stabilizes rather than a mechanical SKIP today. Left at
`discovery-log`.

_Triaged 2026-10-25 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [t3code](https://github.com/pingdotgg/t3code) | platform | Mobile + web + desktop control surface (MIT, ★30K, early/pre-1.0) for driving your own Claude Code, Codex, Cursor, Grok Build, OpenCode, or Antigravity sessions remotely over existing subscriptions | Checking on or steering a running coding-agent session away from your desktop means SSH or nothing; want phone/web/desktop control over agents you already pay for | orca, codex-mobile-bridge, claude-squad |
