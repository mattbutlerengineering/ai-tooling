# Evaluation: gap-trap

**Repo:** [pliablepixels/gap-trap](https://github.com/pliablepixels/gap-trap)
**Stars:** 23 | **Last updated:** 2026-09-14 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Sets up rules and gates in a repo (mutation testing, TDD gates, CI/CD checks) so AI-written code stays correct without a human reviewing every line — a packaged "vibe coding, verified" quality gate rather than a single-purpose linter.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for triage banding, not for an ADOPT/SKIP call on behavior.

## Verdict

**discovery-log — tentative read** — new (created 2026-09-13), catalogued from today's discovery scan.

## Triage note

P2 challenger: cites `stryker-js` (a STACK pick, mutation testing for JS/TS) in Overlaps. gap-trap bundles mutation testing inside a broader rules-and-gates framework (TDD gates, CI/CD checks) rather than being a single-purpose mutation-testing tool, so the overlap is partial, not a clean redundancy — left at discovery-log rather than SKIPped as "redundant with stryker-js". Deserves a real eval to see whether the bundled gates add value beyond stryker-js + tdd-guard already in STACK.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [gap-trap](https://github.com/pliablepixels/gap-trap) | tool | Rules-and-gates framework (MIT) turning vibe-coded output into reviewed-grade code — mutation testing, TDD gates, and CI/CD checks so AI-written code stays correct without reviewing every line | Agent-written code can look right and be wrong; want automated gates catching that instead of manual line-by-line review | agent-delivery-gates, repro-lens, stryker-js, tdd-guard |  |
