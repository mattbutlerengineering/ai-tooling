# Evaluation: okf-agent-memory

**Repo:** [okf-memory/okf-agent-memory](https://github.com/okf-memory/okf-agent-memory)
**Stars:** 481 | **Last updated:** 2026-09-08 (pushed) | **License:** MIT
**Last verified:** 2026-09-08
**Last triaged:** 2026-09-08  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Git-native persistent memory for AI coding agents, implementing Google's Open Knowledge Format v0.2 — a Go binary with sub-300µs in-memory BM25 search over Markdown+YAML knowledge files, an embedded MCP server, and progressive disclosure so only relevant concepts load into context. No external database or vector-DB API cost.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. None of its overlap citations (mem0, cognee, engram, ownmem) are STACK picks, so this doesn't clear the P2 challenger bar, and it isn't archived, vendored under a disqualifying license, or declared as shipping inside another catalogued container. 481★ in 3 days is a strong signal, worth a real hands-on eval rather than a mechanical disposition — its git-native, zero-dependency, no-vector-DB pitch is differentiated enough from the existing memory-tool field to deserve first-time scrutiny, not a bulk SKIP.

_Triaged 2026-09-08 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [okf-agent-memory](https://github.com/okf-memory/okf-agent-memory) | MCP server | Git-native persistent memory for coding agents (MIT) — sub-300µs in-memory BM25 search, Markdown+YAML knowledge files, zero external DB | Standing up agent memory usually means a vector DB or a paid API; want a local, git-versioned, zero-dependency store | mem0, cognee, engram, ownmem |
