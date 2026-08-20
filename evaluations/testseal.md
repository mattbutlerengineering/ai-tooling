# Evaluation: testseal

**Repo:** [satwiksps/testseal](https://github.com/satwiksps/testseal)
**Stars:** 8 | **Last updated:** 2026-08-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-20
**Last triaged:** 2026-08-20  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Deterministic test-suite integrity checks (Apache-2.0) for
AI-assisted Python/pytest pull requests." Mechanical checks that a pytest suite wasn't
weakened or gutted to make an AI-assisted PR pass — catching deleted assertions,
skipped tests, and loosened checks a human reviewer would otherwise have to spot by eye.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata, README, and the CATALOG "Overlaps with" cell.

## Triage note

`triage.py` bands this P2 challenger, citing `stryker-js` as the incumbent via the
CATALOG "Overlaps with" cell — but the two solve different problems: stryker-js
measures whether tests catch injected bugs (mutation testing), while testseal checks
whether the test suite itself was tampered with between commits (integrity, not
quality). Not the same job, so a redundancy SKIP would be a false one. Left at
`discovery-log`; stamped only.

_Triaged 2026-08-20 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [testseal](https://github.com/satwiksps/testseal) | tool | Deterministic test-suite integrity checks (Apache-2.0) for AI-assisted Python/pytest pull requests | Agents can weaken or delete tests to make a PR pass; want mechanical checks that the test suite itself wasn't gutted | stryker-js, tdd-guard, codex-proofloop |
