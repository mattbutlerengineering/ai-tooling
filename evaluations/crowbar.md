# Evaluation: crowbar

**Repo:** [kushvinth/crowbar](https://github.com/kushvinth/crowbar)
**Stars:** 8 | **Last updated:** 2026-10-22 (pushed) | **License:** MIT
**Last verified:** 2026-10-24
**Last triaged:** 2026-10-24  <!-- triaged: bulk -->
**Dev loop stage:** Review (CVE/exploit-intel lookup during security review)
**Layer:** Infrastructure

---

## What it does

Retrieves the CVEs that apply to a given product/version and indexes them locally in
SQLite, so any tool in the repo can query the answer offline — shipped as a CLI, a
20-tool MCP server, and a Claude Code skill.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as P3 backlog (no overlap-pressure citation from another row).
It is closest to `cve-mcp-server` (27 security-intel tools across 21 APIs, already
SKIPped at REVIEW evidence) and `garak`/`OpenOSINT`, but crowbar's offline local-index
design (one SQLite index built from a single product/version query, no per-call API
fan-out) is a different mechanism worth checking on its own rather than folding into
an existing SKIP by name alone. Left at `discovery-log` for a real hands-on eval
rather than a mechanical SKIP.

_Triaged 2026-10-24 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [crowbar](https://github.com/kushvinth/crowbar) | tool | Retrieves CVEs for a product/version and indexes them locally (MIT) — one SQLite index, CLI, and 20-tool MCP server | Querying CVE/exploit data for a dependency means hitting several APIs by hand instead of an indexed local query | cve-mcp-server, garak, OpenOSINT |
