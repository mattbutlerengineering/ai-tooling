# Evaluation: bounty-guard

**Repo:** [doomsday-network/bounty-guard](https://github.com/doomsday-network/bounty-guard)
**Stars:** 9 | **Last updated:** 2026-10-24 (pushed) | **License:** MIT
**Last verified:** 2026-10-24
**Last triaged:** 2026-10-24  <!-- triaged: bulk -->
**Dev loop stage:** Review (pre-execution scanning of GitHub-hosted content an agent is about to act on)
**Layer:** Infrastructure

---

## What it does

An MCP security toolkit (zero-dependency Python CLI, GitHub Action, and stdio/remote
MCP server) scanning untrusted GitHub issues and repositories for prompt injection,
CI secret-exfiltration patterns, and cryptographic bounty-escrow scams, backed by a
published, machine-readable honeypot blocklist (33+ confirmed trap repos/owners).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as P3 backlog (no overlap-pressure citation from another row).
It is adjacent to `agent-scan`/`hol-guard` (pre-execution scanning of agent configs
and extensions) and `secretguard-mcp`/`numbat` (secret exfiltration, endpoint
visibility), but its specific focus — GitHub-hosted prompt-injection honeypots and
bounty-escrow fraud aimed at autonomous bounty-hunting agents — is not covered by any
of those. Left at `discovery-log` for a real hands-on eval rather than a mechanical
SKIP.

_Triaged 2026-10-24 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [bounty-guard](https://github.com/doomsday-network/bounty-guard) | tool | MCP security toolkit (MIT) scanning GitHub issues/repos for prompt injection and CI-secret exfiltration, with a published honeypot blocklist | Autonomous coding/bug-bounty agents can walk into GitHub-hosted prompt-injection traps and secret-exfiltration schemes with nothing flagging them first | agent-scan, hol-guard, secretguard-mcp, numbat |
