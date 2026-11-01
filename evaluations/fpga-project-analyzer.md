# Evaluation: fpga-project-analyzer

**Repo:** [al-nafisah/fpga-project-analyzer](https://github.com/al-nafisah/fpga-project-analyzer)
**Stars:** 25 | **Last updated:** 2026-11-01 (pushed) | **License:** MIT
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

An MCP server (MIT) that lets AI coding agents see and review a Vivado/Zynq/PYNQ FPGA project — drill-down, Vivado-style diagrams plus clock-domain, constraint, and overlay checks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (floorplan, codegraph, StructSmith). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead.

## Triage note

P2 challenger — cites `codegraph` (ADOPT, MEASURED, in STACK) in "Overlaps with." Left at `discovery-log` rather than SKIPped: codegraph is a general-purpose software code knowledge graph, while this tool is scoped specifically to FPGA/HDL projects (Vivado/Zynq/PYNQ) — clock domains, pin constraints, and block-design overlays that a software-only code graph has no model for. Different domain, not a mechanical redundancy.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [fpga-project-analyzer](https://github.com/al-nafisah/fpga-project-analyzer) | MCP server | Review and diagram tool (MIT) for Vivado/Zynq/PYNQ FPGA projects — drill-down diagrams, clock-domain and constraint checks | AI coding agents have no structural view of an FPGA project's clock domains, constraints, and block design to review against | floorplan, codegraph, StructSmith |
