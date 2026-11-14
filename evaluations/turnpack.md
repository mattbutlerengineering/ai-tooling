# Evaluation: turnpack

**Repo:** [OnlyTerp/turnpack](https://github.com/OnlyTerp/turnpack)
**Stars:** 28 | **Last updated:** 2026-11-13 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-14
**Last triaged:** 2026-11-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local MCP context pack meant to cut AI back-and-forth turns, with a test-gated multi-file ship step and automatic rollback.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — catalogued today; no hands-on run yet.

## Triage note

Left at `discovery-log`, not SKIPped. Zero overlap pressure (brand new). `filesnap`/`mulligan` are git-free checkpoint/rollback CLIs; turnpack bundles rollback with a context pack and a test gate ahead of the ship step, a combination distinct enough to warrant its own read rather than a redundancy call against either incumbent alone.

_Triaged 2026-11-14 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [turnpack](https://github.com/OnlyTerp/turnpack) | tool | Local MCP context pack (Apache-2.0) cutting AI back-and-forth turns, with test-gated multi-file ship and automatic rollback | Multi-file AI changes ship without a test gate or an automatic rollback path when they fail | filesnap, mulligan, moai-adk |
