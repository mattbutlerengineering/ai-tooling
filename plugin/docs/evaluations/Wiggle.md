# Evaluation: Wiggle

**Repo:** [Razshy/Wiggle](https://github.com/Razshy/Wiggle)
**Stars:** 74 | **Last updated:** 2026-09-08 (pushed) | **License:** mixed — build recipe/docs MIT, bundled skill files proprietary
**Last verified:** 2026-09-08
**Last triaged:** 2026-09-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement (code-execution infrastructure)
**Layer:** Infrastructure

---

## What it does

A reproducible VM sandbox replicating the environment Claude's own code execution runs in — document processing (LibreOffice, pandoc), data science (pandas/numpy/scikit-learn), web automation (Playwright), OCR, media processing (ffmpeg), plus 40 instructional skill files. The repo states any agent that can shell into a container can use the box the same way Claude does.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not mechanically SKIPped. It carries a real license concern — the repo's own README states the 40 bundled skill files and Anthropic binaries carry Anthropic's proprietary license and "does not clearly allow redistribution," which the repo itself frames as "captured research artifacts." That is not a P4 mechanical-skip: Wiggle is Type `tool`, not a vendored `skill`/`plugin` whose text gets copied into a consuming repo, so the license bar that disqualifies vendored artifacts doesn't mechanically apply here (same reasoning `gitwarren-app`'s triage used for its own copyleft flag). The redistribution-rights question is real enough that it deserves a human read rather than a bulk-pass judgement call in either direction — SKIPping on an ambiguous license read is exactly the kind of positive-sounding certainty an unattended pass shouldn't manufacture. The catalog row already discloses the mixed license so a reader isn't misled in the meantime.

_Triaged 2026-09-08 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Wiggle](https://github.com/Razshy/Wiggle) | tool | Reproducible VM sandbox (⚠️ mixed license — build recipe MIT, bundled Anthropic skill files proprietary/no clear redistribution rights) replicating the environment Claude's own code execution runs in | Any agent that can shell into a container wants Claude's own execution environment (doc processing, data science, browser automation, media tooling) without reverse-engineering it | daytona, agent-sandbox, axern |
