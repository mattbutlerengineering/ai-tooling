# Evaluation: ToolReplay

**Repo:** [Matthew0822/ToolReplay](https://github.com/Matthew0822/ToolReplay)
**Stars:** 170 | **Last updated:** 2026-09-14 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Dependency-free Python CLI that audits AI agent tool-call transcripts: hash-chain sealing (tamper-evidence), deterministic replay, and scope-overreach checks against a declared permission set.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — new (created 2026-09-14), catalogued from today's discovery scan.

## Triage note

P3 backlog (no STACK overlap flagged). Distinct from `numbat` (endpoint activity visibility) and `maddu` (append-only governance log) in being specifically about tamper-evident **replay** of a recorded transcript rather than live monitoring or a governance ledger. Left at discovery-log as a differentiated new entrant worth a real look rather than SKIPped on partial similarity.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [ToolReplay](https://github.com/Matthew0822/ToolReplay) | tool | Dependency-free Python CLI (MIT) auditing AI agent tool-call transcripts — hash-chain sealing, deterministic replay, and scope-overreach checks | Agent tool-call logs can be edited or replayed inconsistently with no tamper-evidence; want a verifiable, replayable audit trail | maddu, numbat, reverify |  |
