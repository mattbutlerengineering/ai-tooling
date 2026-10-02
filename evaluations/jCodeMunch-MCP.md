# Evaluation: jCodeMunch-MCP

**Repo:** [jgravelle/jcodemunch-mcp](https://github.com/jgravelle/jcodemunch-mcp)
**Stars:** 2,700 | **Last updated:** not independently verified (GitHub API unavailable for this repo in this session) | **License:** ⚠️ Dual-use (free for non-commercial use; commercial licenses start at $79 — not OSI-approved OSS)
**Last verified:** 2026-10-02
**Last triaged:** 2026-10-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An MCP server for symbol-level code retrieval via tree-sitter AST parsing across 70+ languages.
Agents search a symbol index (`search_symbols`) and fetch only the exact implementation
(`get_symbol_source`) instead of reading whole files, claiming ~96.5% token savings on typical
edits versus grep-and-read.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This session's GitHub API access is scoped to the
`ai-tooling` repo only, so repo facts came from the public repo page rather than `gh api`.
Source-grounded only: the repo's own README description plus the CATALOG "Overlaps with" cell.
The token-savings figure is the project's own self-reported claim, not independently measured
here. Sufficient to place the lead, not to support any verdict, and none is offered.

## Triage note

Left at `discovery-log`. Cites `headroom` (STACK) in "Overlaps with", which bands this P2, but the
two solve different problems: `headroom` is a generic tool-output/log/file compressor working at
the byte/text level, while jCodeMunch is specifically symbol-level *code* retrieval via AST
parsing — it answers "give me this one function" rather than "shrink this blob of output." That
is a narrower, more specific mechanism, not a redundant implementation of headroom's job, so it
deserves a real hands-on look rather than a mechanical SKIP. Note for any future eval: the license
is a non-OSS dual-use grant (free non-commercial / paid commercial), not a disqualifying copyleft
license — P4 mechanical-skip does not apply (this is an MCP server you run, not a vendored
skill/plugin whose text is copied into the consuming repo) — but it is also not MIT-permissive and
should be weighed accordingly in any eventual verdict.

_Triaged 2026-10-02 by the P2 challenger band (daily discovery pass)._
