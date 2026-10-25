# Evaluation: ai-memory

**Repo:** [akitaonrails/ai-memory](https://github.com/akitaonrails/ai-memory)
**Stars:** 13,400 | **Last updated:** n/a (not checked via API; this session's GitHub access is repo-scoped) | **License:** MIT
**Last verified:** 2026-10-25
**Last triaged:** 2026-10-25  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A self-contained Rust binary providing long-term memory for AI coding agents. It
captures work through lifecycle hooks and stores it as a git-backed Markdown wiki,
letting different agents (Claude Code, Codex, Cursor, and others) share context and
hand off tasks. Runs with zero LLM calls by default.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the repo's own README (fetched over the web, since this session's GitHub API access
is scoped to this repository and does not extend to arbitrary repos) plus the
CATALOG "Overlaps with" cell. That is sufficient to place the lead against its
closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Cites `claude-mem` (a STACK pick) in its "Overlaps with" cell, which bands this
P2 challenger — but the overlap is not a straight redundancy. `claude-mem` is a
semantic-search + knowledge-graph memory plugin; `ai-memory` is a zero-LLM-call,
git-native Markdown wiki explicitly designed to be shared across agent *vendors*
(Claude Code, Codex, Cursor), not just within Claude Code. That cross-vendor,
zero-cost design is a real differentiator, not a worse version of the same job —
the same reasoning that kept `ownmem` and `byterover-cli` (its closest catalog
peers, both cited in its own "Overlaps with" cell) at `discovery-log` rather than
SKIPped. Left at `discovery-log`; a real head-to-head against `claude-mem` on
recall quality and cross-vendor handoff would need a hands-on eval.

_Triaged 2026-10-25 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ai-memory](https://github.com/akitaonrails/ai-memory) | tool | Git-backed Markdown-wiki long-term memory for AI coding agents (MIT, Rust, ★13.4K) — zero LLM calls by default, lifecycle hooks capture work for Claude Code, Codex, Cursor, and others to share and hand off | Coding agents forget everything between sessions and across vendors; want a zero-cost, git-native memory shared by whichever agent is running | ownmem, byterover-cli, claude-mem |
