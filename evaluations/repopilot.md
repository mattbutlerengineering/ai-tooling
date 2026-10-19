# Evaluation: repopilot

**Repo:** [AZEN-jc/repopilot](https://github.com/AZEN-jc/repopilot)
**Stars:** 4 | **Last updated:** 2026-10-16 (pushed) | **License:** MIT
**Last verified:** 2026-10-17
**Last triaged:** 2026-10-17  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Static-analysis release gate returning a ship-or-block verdict for a public GitHub repo, with
file-and-line evidence and fixes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge the
tool's behaviour hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; picked up as one of the oldest
untriaged leads (no prior eval file) in the P3 backlog band this pass.

## Triage note

No structural signal flags this lead (P3). At ★4 it's early, but the job — an evidenced
ship-or-block verdict on a repo, distinct from `vet`'s and `ship-ready`'s own framings — is
differentiated enough that a mechanical disposition isn't defensible without actually running
it. Left at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [repopilot](https://github.com/AZEN-jc/repopilot) | tool | Static-analysis release gate (MIT) returning a ship-or-block verdict for a public GitHub repo, with file-and-line evidence and fixes | Deciding whether a repo is safe to ship or adopt means auditing it by hand instead of getting an evidenced verdict | vet, ship-ready, skylos |  |
