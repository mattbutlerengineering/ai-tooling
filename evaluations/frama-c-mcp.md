# Evaluation: frama-c-mcp

**Repo:** [sysprog21/frama-c-mcp](https://github.com/sysprog21/frama-c-mcp)
**Stars:** 11 | **Last updated:** 2026-08-20 (pushed) | **License:** MIT
**Last verified:** 2026-08-20
**Last triaged:** 2026-08-20  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

Catalog one-liner: "MCP server (MIT) exposing Frama-C's EVA/WP formal-verification
analyzers and sandboxed ACSL iteration to coding agents." An MCP server that wraps
Frama-C's EVA (value analysis) and WP (weakest precondition) analyzers plus sandboxed
ACSL specification iteration, so a coding agent can formally verify C code directly.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata, README, and the CATALOG "Overlaps with" cell.

## Triage note

`triage.py` bands this P2 challenger, citing `stryker-js` as the incumbent via the
CATALOG "Overlaps with" cell — but the two are not actually redundant: stryker-js is
JS/TS mutation testing (do the tests catch injected bugs?), while frama-c-mcp is C
formal verification (does the code satisfy a machine-checked specification?).
Different language, different technique, no substitutability, so a redundancy SKIP
would be a false one. Left at `discovery-log`; stamped only.

_Triaged 2026-08-20 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [frama-c-mcp](https://github.com/sysprog21/frama-c-mcp) | MCP server | MCP server (MIT) exposing Frama-C's EVA/WP formal-verification analyzers and sandboxed ACSL iteration to coding agents | Formally verifying C code (overflow, dead code, spec compliance) needs Frama-C expertise agents don't have; want it wired in as MCP tools | stryker-js, keploy |
