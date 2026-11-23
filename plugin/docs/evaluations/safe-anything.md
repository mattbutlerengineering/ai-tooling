# Evaluation: safe-anything

**Repo:** [erkamyaman/safe-anything](https://github.com/erkamyaman/safe-anything)
**Stars:** 326 | **Last updated:** 2026-11-23 (pushed) | **License:** MIT
**Last verified:** 2026-11-23
**Last triaged:** 2026-11-23  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An all-Rust vulnerability scanner covering XSS, SQL injection, leaked secrets,
dependency CVEs, and AI agent setups — from the same author as `rust-anything`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`, nothing structural bands it — new lead, first pass.

_Triaged 2026-11-23 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [safe-anything](https://github.com/erkamyaman/safe-anything) | tool | All-Rust vulnerability scanner (MIT) for XSS, SQL injection, leaked secrets, dependency CVEs, and AI agent setups | Codebases and AI agent configs ship with no fast, dependency-light scanner catching common vuln classes and leaked secrets before they land | agentshield, agent-scan, skylos |
