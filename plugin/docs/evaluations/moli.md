# Evaluation: moli

**Repo:** [lexmount/moli](https://github.com/lexmount/moli)
**Stars:** 119 | **Last updated:** 2026-08-12 (pushed) | **License:** NOASSERTION (⚠️ no LICENSE file)
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A browser built in Rust specifically for AI agents to navigate, automate, and script the web,
rather than automation bolted onto a human-first browser.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: repo metadata plus the CATALOG
"Overlaps with" cell. Enough to place it against nearby browser-automation tools, not enough for
any verdict, and none is offered.

## Triage note

Left at `discovery-log`, not SKIPped, though the license bar (permissive-only) would disqualify it
today: GitHub reports no detected LICENSE file (`NOASSERTION`). Per this catalog's license bar,
copyleft-or-missing means not adoptable — but the repo is 2 days old, and a missing LICENSE file at
this stage is very plausibly an oversight rather than a deliberate all-rights-reserved choice.
Leaving it at `discovery-log` records that it was seen without disposing on a fact that may change
within days; a P4 mechanical-skip is for a *settled* license state (`NONE`/copyleft on a mature
repo), not a brand-new repo's still-forming metadata.

_Triaged 2026-08-12 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [moli](https://github.com/lexmount/moli) | tool | Rust-built browser for AI agents (⚠️ no LICENSE file) — navigate, automate, and script the web natively | Browser automation bolted onto a human-first browser is fragile; want one built agent-first from the ground up | agent-browser, playwright-skill, opencli, browser-act/skills |
