# Evaluation: NeMo-Guardrails

**Repo:** [NVIDIA-NeMo/Guardrails](https://github.com/NVIDIA-NeMo/Guardrails)
**Stars:** 6,875 | **Last updated:** 2026-08-05 (pushed) | **License:** Apache-2.0 (per LICENSE text; GitHub's licensee records NOASSERTION)
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Programmable guardrails for LLM apps, by NVIDIA — adds declarative "rails" controlling conversational LLM behavior (topic/jailbreak limits, dialog paths, output format, fact-checking, tool-use constraints), arXiv-backed.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (via `repo-metadata.json`, fetched 2026-08-04) plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — not previously examined; picked up as one of the oldest untriaged leads in the P3 backlog this pass.

## Triage note

P3 backlog (no STACK overlap flagged). A substantial, vendor-backed (NVIDIA), arXiv-documented safety tool with a distinct scope (declarative conversational rails) from the catalog's other guardrail/scanner tools. Left at discovery-log; worth a real eval rather than a mechanical disposition.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [NeMo-Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | tool | Programmable guardrails for LLM apps (Apache-2.0, ★6.5K, by NVIDIA) — add "rails" that control conversational LLM behavior (topic/jailbreak limits, predefined dialog paths, output format, fact-checking, tool-use constraints) via a declarative config layer between user and model; arXiv-backed | "Prompt + model" apps can go off-topic, get jailbroken, or emit unsafe output; want declarative, programmable runtime guardrails | superagent, presidio, garak, strands-agents (harness-sdk) |  |
