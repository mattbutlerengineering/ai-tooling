# Evaluation: MinerU

**Repo:** [opendatalab/MinerU](https://github.com/opendatalab/MinerU)
**Stars:** 73,000 | **License:** NOASSERTION (⚠️ unclear/not confirmed permissive, flagged in CATALOG.md)
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling (document conversion)

---

## What it does

Transforms PDFs and Office docs into LLM-ready markdown/JSON — layout parsing, OCR, and structure
extraction for agentic workflows. Picked up from the P3 backlog band of the daily
discovery-and-triage pass.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`markitdown`, `Docling` (ext.), `marker` (ext.)).
`markitdown` is ADOPT and MEASURED in STACK.md, doing the same core job (PDF/Office → LLM-ready
markdown) that MinerU targets. That is sufficient for a SKIP that turns on *redundancy with a
catalogued incumbent*, not on the tool's behaviour.

## Verdict

**SKIP** — redundant with `markitdown` (ADOPT, MEASURED, already in STACK.md), which already
converts PDFs/Office docs to LLM-ready markdown. MinerU adds OCR/layout depth, but its license
resolves as `NOASSERTION` (unclear, flagged in CATALOG.md) — a second, license-uncertain tool for
a job the incumbent already covers well earns nothing.

_Triaged 2026-07-29 by the daily discovery scan's P3-band triage pass._
