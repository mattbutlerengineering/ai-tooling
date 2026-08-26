# Evaluation: halofy

**Repo:** [halofyai/halofy](https://github.com/halofyai/halofy)
**Stars:** 315 | **Last updated:** 2026-08-25 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-08-26
**Last triaged:** 2026-08-26  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

An open access and governance layer for AI agents across an organization —
identity, policy, provenance, audit logging, and signed erasure, exposed with
an MCP-facing surface (pgvector-backed).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata (license) plus the CATALOG "Overlaps with" cell. That is sufficient
for the verdict below, which turns entirely on license, not on the tool's behaviour.

## Verdict

**SKIP** — AGPL-3.0. This is a service you would run as shared organizational
infrastructure (identity/policy/audit for every agent in the org), and AGPL's
network-copyleft clause reaches exactly that deployment shape — running a modified
version as a network service obligates you to offer the source to every user
interacting with it over the network. `agent-governance-toolkit` (MIT) and `decern`
(Apache-2.0) already cover the same governance-layer job under permissive licenses.

_Triaged 2026-08-26 by the daily discovery pass, per the routine's license bar
(copyleft ⇒ SKIP). Not a P4 mechanical-skip band call — halofy is a `tool` you run,
not a vendored skill/plugin copied into a consuming repo — but the routine's own
hard rule is unconditional on copyleft, so it is applied here directly rather than
left for a future triage pass._
