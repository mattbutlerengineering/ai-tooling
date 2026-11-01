# Evaluation: helixharness

**Repo:** [didi/helixharness](https://github.com/didi/helixharness)
**Stars:** 228 | **Last updated:** 2026-10-30 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

An enterprise-oriented AI-coding engineering harness (Apache-2.0) that a team extends with its own business knowledge, engineering standards, and R&D process into a persistent, evolving in-house Harness, rather than assembling one from scratch each time.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. It names `superpowers`, `ECC`, and `gstack` as peers in "Overlaps with," none of which are STACK picks (STACK links `obra/superpowers` under the display name `GSD`, but neither that nor `gstack` nor `ECC` is actually installed in STACK today), so there is no mechanical redundancy call available.

## Triage note

No STACK-pick overlap. P3 backlog — left at `discovery-log` with a stamp.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [helixharness](https://github.com/didi/helixharness) | harness | Enterprise AI-coding engineering harness (Apache-2.0) teams extend with their own standards and process into a persistent Harness | Each team re-derives the same coding-agent engineering infrastructure from scratch instead of building on a shared, extensible harness foundation | superpowers, ECC, gstack |
