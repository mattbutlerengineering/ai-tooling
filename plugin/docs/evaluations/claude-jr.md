# Evaluation: claude-jr

**Repo:** [IWhitebird/claude-jr](https://github.com/IWhitebird/claude-jr)
**Stars:** 3 | **Last updated:** 2026-11-18 (pushed) | **License:** MIT
**Last verified:** 2026-11-18
**Last triaged:** 2026-11-18  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Claude Junior: a full coding agent for the terminal in a single ~2 MB Rust binary (0.7 MB idle,
any model), plus half-megabyte MCP "worker" agents the main agent can hand tasks to. The repo
self-reports 88% on SWE-bench Verified.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool and did not attempt to reproduce the SWE-bench Verified
claim. This evaluation is source-grounded only: the CATALOG one-liner and repo metadata. The
88% figure is vendor-reported and unverified here — treat it as a claim to pilot-check, not a
measured result. Not sufficient to support an ADOPT, which this eval does not offer.

## Triage note

Newly discovered and catalogued today (daily discovery pass; 3 stars, brand new). Left at
`discovery-log` rather than SKIPped — a minimal-footprint binary agent with a benchmarked
(if unverified) claim is differentiated enough from the existing `SWE-agent`/`aster`/`eca`
harness cluster to be worth a look once it has more track record, not dismissed as redundant on
day one.
