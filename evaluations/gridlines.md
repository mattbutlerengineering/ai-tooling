# Evaluation: gridlines

**Repo:** [pritamux/gridlines](https://github.com/pritamux/gridlines)
**Stars:** 232 | **Last updated:** 2026-11-22 (pushed) | **License:** MIT
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

An agent skill for alignment passes: it draws guide lines down an interface, finds every item that misses its line, and fixes the padding — a systematic visual-QA pass rather than an eyeballed one.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — a narrow, specific UI-alignment QA pass; no STACK pick does this exact check.

## Triage note

Left at `discovery-log`, stamped. Its Overlaps cell (pixelpact, design-council, dsh-vision-toolkit) names no STACK pick, so there is no redundancy to SKIP against. Differentiated enough (a specific, mechanical alignment check) to be worth a real eval rather than a mechanical disposition.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gridlines](https://github.com/pritamux/gridlines) | skill | Agent skill (MIT) for alignment passes — draws guide lines down an interface, finds every item missing its line, fixes the padding | UI spacing/alignment drift is eyeballed with no systematic pass that finds and fixes every misaligned element | pixelpact, design-council, dsh-vision-toolkit |
