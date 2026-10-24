# Evaluation: aletheia

**Repo:** [firatmio/aletheia](https://github.com/firatmio/aletheia)
**Stars:** 8 | **Last updated:** 2026-10-24 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-24
**Last triaged:** 2026-10-24  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

Memory for coding agents (Go binary + MCP server + plugin skill) that carries
evidence from the actual code for every stored fact and re-checks that evidence on
every recall, pointing the agent at the exact lines rather than trusting a stored
summary that may have gone stale.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as a P2 challenger against `claude-mem` (the STACK incumbent,
pressure 0 — the citation is one-directional so far). `claude-mem`'s semantic
search/timeline/knowledge-graph is recall-oriented; `heimdall` and `baron` are the
closer conceptual peers (a verified lookup, and a verdict attached to every answer),
but aletheia's specific mechanism — re-verifying a stored fact against the code on
every recall rather than once at write time — is not what any of the three do. Not
clearly dominated; left at `discovery-log` for a real hands-on eval rather than a
mechanical SKIP.

_Triaged 2026-10-24 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [aletheia](https://github.com/firatmio/aletheia) | tool | Memory for coding agents (Apache-2.0) that re-verifies each stored fact against the code on every recall | Agent memory stores facts that go stale as code changes, with nothing re-checking them before they reach context again | claude-mem, heimdall, baron, OMEGA |
