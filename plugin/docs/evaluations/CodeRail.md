# Evaluation: CodeRail

**Repo:** [wiva-hq/CodeRail](https://github.com/wiva-hq/CodeRail)
**Stars:** 49 | **Last updated:** 2026-10-31 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-31
**Last triaged:** 2026-10-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A self-hosted remote control (Apache-2.0) for coding-agent chats, approvals, terminals, files, git, and dev-server previews across every computer the operator owns, from the browser or a phone — one Docker container on your own server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (t3code, agentbox, codex-mobile-bridge). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead.

## Triage note

P3 backlog. Left at `discovery-log`; its overlaps (t3code, agentbox, codex-mobile-bridge) are themselves discovery-log leads, not STACK picks, so it doesn't land in P2. The remote-control-across-every-computer-you-own niche is crowded (see also t3code/agentbox/codex-mobile-bridge) but none has graduated to a real eval yet, so a bake-off candidate rather than a bulk disposition.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [CodeRail](https://github.com/wiva-hq/CodeRail) | tool | Self-hosted remote control (Apache-2.0) for coding-agent chats, approvals, terminals, files, git, and dev-server previews across every computer you own | Checking on or steering a coding agent away from your desktop means SSH or nothing; want phone/browser control over every machine you run agents on | t3code, agentbox, codex-mobile-bridge |
