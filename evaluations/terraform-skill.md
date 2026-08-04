# Evaluation: terraform-skill

**Repo:** [antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill)
**Stars:** 2,238 | **Last updated:** 2026-07-03 (pushed) | **License:** Apache-2.0 (per LICENSE text; GitHub records `NOASSERTION`)
**Dev loop stage:** Implement / Review (infrastructure-as-code)
**Layer:** Tooling (agent skill)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A Terraform and OpenTofu skill for AI coding agents by Anton Babenko (the maintainer of the
`terraform-aws-modules` collection), covering testing, module design, CI/CD, production patterns, and
failure-mode diagnosis, with version-aware guards so guidance matches the Terraform version in use.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the `CATALOG.md` one-liner and "Overlaps with" cell (`azure-skills`, `google/skills`,
`microsoft/skills`). Enough to place and band it; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`. Two things were checked.

**License.** GitHub records `NOASSERTION` — it could not parse the LICENSE file — but the `CATALOG.md`
row already discloses "Apache-2.0 per LICENSE text", meaning someone read the file. This is the
*disclosed* form of the same trap that `academic-research-skills` hides in this slice: there,
`NOASSERTION` concealed a NonCommercial blocker; here it conceals a perfectly permissive grant. Which
is the whole reason `NOASSERTION` never disposes a lead on its own — it carries no information about
the license, only about GitHub's parser.

**Overlap.** Its cell names the three vendor cloud packs, but the relationship is not redundancy: those
are cloud-provider-specific (Azure, GCP, Microsoft SDKs) while Terraform/OpenTofu is the
**vendor-neutral** layer that provisions any of them. An engineer using azure-skills may still want
this; the packs do not substitute for each other. Nothing here is a disposal ground.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [terraform-skill](https://github.com/antonbabenko/terraform-skill) | skill | Terraform & OpenTofu skill by Anton Babenko (Apache-2.0 per LICENSE text, ★2.2K) — testing, modules, CI/CD, and production failure-mode diagnosis with version-aware guards | Agents write plausible-but-wrong IaC; want authoritative Terraform guidance while writing, reviewing, or debugging | azure-skills, google/skills, microsoft/skills |
