# Evaluation: terravision

**Repo:** [patrickchugh/terravision](https://github.com/patrickchugh/terravision)
**Stars:** 1,661 | **Last updated:** 2026-10-19 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Bidirectional cloud-architecture diagramming: draws a diagram from Terraform or a prose
description (AI prompt or JSON), and generates Terraform from a diagram. Ships as a CLI, an
MCP server, and a CI/CD action, using official AWS/Azure/GCP icons.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and GitHub repo metadata (stars, license, activity). No hands-on run was performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

P3 backlog, oldest-untriaged (no prior eval file, never stamped). Not a P2 challenger: its
cited peers (`StructSmith`, `terraform-skill`) are themselves discovery-log leads, not a STACK
pick it's redundant with. Type is `tool` (CLI/MCP server/CI action you run), not a vendored
`skill`/`plugin`, so the AGPL-3.0 license does not trigger P4's vendored-copyleft mechanical
SKIP — copyleft on a CLI you merely invoke imposes nothing. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [terravision](https://github.com/patrickchugh/terravision) | tool | Bidirectional cloud-architecture diagrams (AGPL-3.0) — draws from Terraform/prose or generates Terraform from a diagram; CLI, MCP server, CI action | Cloud architecture diagrams drift from the Terraform that actually defines the infrastructure, with no round-trip between the two | StructSmith, terraform-skill |  |
