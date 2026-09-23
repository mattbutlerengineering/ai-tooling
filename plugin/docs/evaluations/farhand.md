# Evaluation: farhand

**Repo:** [CogFlux/farhand](https://github.com/CogFlux/farhand)
**Stars:** 6 | **Last updated:** 2026-09-23 (pushed) | **License:** MIT
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A remote-execution MCP server (Rust, MIT) — runs OpenCode/Claude Code/Codex work on a remote host
over SSH, keeping credentials and the local machine closed off, with an audit trail of what ran.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the SSH-based remote-execution model. That is sufficient to catalog it
and place it relative to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog. Adjacent to `mirrord` (connects a local process to live infra) and `vercel-sandbox`/
`sandboxd` (isolated sandboxes), but farhand's specific shape — driving an agent's *entire* session on
a remote host over SSH rather than sandboxing or infra-connecting locally — isn't a clean match for
any one. Very early (6 stars, created this week); left at `discovery-log` rather than judged on a
thin signal.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [farhand](https://github.com/CogFlux/farhand) | MCP server | Remote-execution MCP server (MIT, Rust) — runs OpenCode/Claude Code/Codex work on a remote host over SSH, keeping credentials and the local machine closed, and audits everything | Running a coding agent against a remote host means exposing local credentials or hand-rolling SSH tooling; want an audited, remote-execution MCP server | mirrord, vercel-sandbox, sandboxd |  |
