# Evaluation: Baize

**Repo:** [Xu123-Bob/Baize](https://github.com/Xu123-Bob/Baize)
**Stars:** 69 | **Last updated:** 2026-09-13 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Open-source terminal AI coding agent CLI with multi-backend support (DeepSeek / OpenAI-compatible / local Ollama), tool calling, skill loading, subagent delegation, context compression, and a security sandbox.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — new (created 2026-09-12), catalogued from today's discovery scan.

## Triage note

P3 backlog (no STACK overlap flagged — Agent Harnesses' vendor-agnostic CLI slot is crowded but no single incumbent is in STACK). Baize's local-Ollama backend is a genuine differentiator from most multi-provider CLIs in the catalog, which target hosted APIs. Left at discovery-log.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [Baize](https://github.com/Xu123-Bob/Baize) | harness | Open-source terminal AI coding agent CLI (MIT) with multi-backend support (DeepSeek/OpenAI-compatible/local Ollama), tool calling, skill loading, subagent delegation, context compression, and a security sandbox | Want a vendor-agnostic terminal pair-programming agent that isn't locked to one model provider | command-code, aider, pi |  |
