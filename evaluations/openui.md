# Evaluation: openui

**Repo:** [thesysdev/openui](https://github.com/thesysdev/openui)
**Stars:** 7,931 | **Last updated:** 2026-07-10 (pushed) | **License:** MIT
**Dev loop stage:** Reference (generative UI)
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An open standard for generative UI — how an AI system emits structured, renderable interface specs
that any frontend can consume, rather than emitting markup directly.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this — it is a specification. Source-grounded only: GitHub metadata
(fetched 2026-08-04) plus the CATALOG one-liner and "Overlaps with" cell (`ag-ui`, `CopilotKit`).
Enough to place it; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`. MIT, ★7.9K, pushed 2026-07-10 — active, permissive and squarely in a
category this catalog already tracks through the `generative-ui-frameworks` cluster eval.

It is one of three protocol rows in this section addressing adjacent slices of the same problem, and
they are complements rather than duplicates: `ag-ui` standardizes how an agent *streams state* to a
front end, `MCP Apps (ext-apps)` lets an MCP server *ship its own UI* into a host, and openui
standardizes the *spec format* the UI is described in. Disposing any one of them as redundant would
be a category error.

The honest scope caveat is that all three matter when you are building an agent-backed product,
not when you are using an agent to write code. That is why it sits in Reference rather than in a
dev-loop stage — and why it is a row to keep findable rather than a lead to promote.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [openui](https://github.com/thesysdev/openui) | reference | Open standard for generative UI — how AI systems emit structured, renderable interface specs | No standard protocol for AI to produce UI specifications that any frontend can render | ag-ui, CopilotKit |
