# Evaluation: codex-mobile-bridge

**Repo:** [try2love/codex-mobile-bridge](https://github.com/try2love/codex-mobile-bridge)
**Stars:** 32 | **Last updated:** 2026-10-04 (pushed) | **License:** MIT
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

A self-hosted bridge (Python, ★32, created 2026-09-29, v1.3.2) that lets you continue
an existing Codex App desktop session from a phone, tablet, or any browser — over
local network, SSH, or an external HTTPS connection — while keeping the original
desktop app's execution context.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Overlaps `agentaps` (discovery-log — universal desktop GUI for ACP-compatible
harnesses) and `orca` (discovery-log — desktop + mobile companion); neither is a STACK
pick, so this does not band as a P2 challenger. Narrower than both: it specifically
continues an existing Codex App session rather than launching/managing a fleet of
agents. No archived flag, no disqualifying license, no `Ships inside` container. Left
at `discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codex-mobile-bridge](https://github.com/try2love/codex-mobile-bridge) | tool | Self-hosted browser bridge (MIT) continuing Codex App sessions from phone, tablet, or any browser — local, SSH, or HTTPS | Codex App sessions are tied to one desktop; want to check on or continue them from another device without a second API meter | agentaps, orca, claude-fleet |
