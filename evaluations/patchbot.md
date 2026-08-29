# Evaluation: patchbot

**Repo:** [PrismorSec/patchbot](https://github.com/PrismorSec/patchbot)
**Stars:** 19 | **Last updated:** 2026-08-25 (pushed) | **License:** MIT
**Last verified:** 2026-08-29
**Last triaged:** 2026-08-29  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A vulnerability scanner that pairs your own scanners and threat feeds with a coding agent that opens the fix as a PR, rather than stopping at a findings list. Ships as a CLI, a GitHub Action, or a scheduled Managed Agents deployment.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`cdmx-in/security-review`, `ghostsecurity/skills`, `skylos`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. Not SKIPped: `cdmx-in/security-review` chains real scanners and verifies findings against source, and `skylos` does CVE/secret/complexity scanning as a PR gate, but neither claims to open the fix PR automatically the way this does — that's a distinct enough capability (scan → fix, not just scan → report) to warrant a real look rather than a mechanical dismissal.

_Triaged 2026-08-29 by the P3 backlog band ([#565](https://github.com/mattbutlerengineering/ai-tooling/issues/565))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [patchbot](https://github.com/PrismorSec/patchbot) | tool | Vulnerability scanner (MIT) pairing your own scanners/threat feeds with a coding agent that opens the fix PR — CLI, GitHub Action, or scheduled deployment | Vulnerability scanners produce a list of findings; want the fix opened as a PR automatically instead of triaged by hand | cdmx-in/security-review, ghostsecurity/skills, skylos |
