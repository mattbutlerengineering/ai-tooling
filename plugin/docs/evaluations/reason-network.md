# Evaluation: reason-network

**Repo:** [reason-machines/reason-network](https://github.com/reason-machines/reason-network)
**Stars:** 471 | **Last updated:** 2026-10-19 (pushed) | **License:** MIT OR Apache-2.0 (dual, LICENSE-MIT + LICENSE-APACHE)
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A peer-to-peer daemon — one small process per computer, no server — that lets a team's
coding-agent sessions see each other (who, which repo/branch, busy or idle, current activity)
and message the right one directly, straight into the session that's open. Works across Claude
Code, Codex, Cursor, Gemini CLI, Copilot CLI, Grok CLI, opencode, pi, and DeepSeek Harness. Can
run fully local/team-only or sign in to the vendor's cloud for cross-device reach.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the README,
the CATALOG one-liner, and GitHub repo metadata (stars, license, topics). No hands-on run was
performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

New lead, cataloged today. P3 backlog — zero overlap pressure. Closest peers (`agent-link`,
`multiplayer-ai`, `succubus`) are themselves discovery-log leads, not STACK picks, so not a P2
challenger. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [reason-network](https://github.com/reason-machines/reason-network) | tool | Peer-to-peer daemon (MIT/Apache-2.0 dual) so a team's coding-agent sessions see each other and message the right one directly, no server | Coordinating agents across teammates' machines has no shared view of who's working on what, or a direct way to message the right running session | agent-link, multiplayer-ai, succubus |  |
