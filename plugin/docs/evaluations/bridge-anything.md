# Evaluation: bridge-anything

**Repo:** [Artesiana/bridge-anything](https://github.com/Artesiana/bridge-anything)
**Stars:** 56 | **Last updated:** 2026-11-20 (pushed) | **License:** MIT
**Last verified:** 2026-11-25
**Last triaged:** 2026-11-25  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

An agent skill (MIT) that builds a REST, MCP, or CLI integration bridge to
software that has no API of its own, using the author's REA methodology.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on redundancy with a catalogued incumbent, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this
eval offers none.

## Triage note

Newly discovered and catalogued today via the daily discovery pass. No STACK pick
is cited in "Overlaps with" (pressure 0) — it names `fast-anything` (sibling
"-anything" family, different job), `codex-remote-pro` (a specific bridge, not a
generator), and `typescript-mcp-server-generator` (MCP-specific, not REST/CLI too),
none of which is a direct duplicate. Left at `discovery-log` for a real hands-on
eval rather than a first-day guess.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [bridge-anything](https://github.com/Artesiana/bridge-anything) | skill | Agent skill (MIT) that builds a REST, MCP, or CLI bridge to software that has no API | An app needs data from software with no API, and hand-building an integration bridge each time is slow | fast-anything, codex-remote-pro, typescript-mcp-server-generator |
