# Evaluation: MinerU

**Repo:** [opendatalab/MinerU](https://github.com/opendatalab/MinerU)
**Stars:** 74,101 | **Last updated:** 2026-07-10 (pushed) | **License:** NOASSERTION ⚠️
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Converts PDFs and Office documents into LLM-ready markdown/JSON with layout parsing, OCR, and
structure extraction, aimed at feeding agentic workflows real document content rather than a flat
text dump.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG one-liner and "Overlaps with" cell (`markitdown`, Docling, marker). Enough to
weigh it against the STACK incumbent it names; not enough for any positive verdict, and this eval
offers none.

## Triage note

Left at `discovery-log`, not SKIPped. It does overlap
[`markitdown`](https://github.com/microsoft/markitdown) (STACK, `ADOPT`/`MEASURED`) on the
headline job — documents in, markdown out — but they are not the same class of tool. markitdown
is a fast, broad, dependency-light converter across many formats. MinerU is a heavyweight
ML pipeline for the hard case specifically: layout analysis, OCR, formula and table structure
recovery from PDFs that a plain converter flattens into noise. Where markitdown fails, it fails
on exactly the input MinerU exists for.

At 74K stars this is also squarely the "major tool" the eliminate-only protocol says not to
dismiss as redundant on a source read. **Watch item for whoever evaluates it: the license is not
a standard SPDX identifier** (`NOASSERTION` in `repo-metadata.json`, already flagged with ⚠️ in
its CATALOG row) — that needs reading before adoption, and it is the most likely reason this
lead never graduates.

_Triaged 2026-08-04 by the P2 challenger band ([#265](https://github.com/mattbutlerengineering/ai-tooling/issues/265))._
