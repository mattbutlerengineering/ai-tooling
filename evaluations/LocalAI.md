# Evaluation: LocalAI

**Repo:** [mudler/LocalAI](https://github.com/mudler/LocalAI)
**Stars:** 48,238 | **Last updated:** 2026-08-05 (pushed) | **License:** MIT
**Dev loop stage:** Implement (local model serving)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An open-source engine for running LLM, vision, voice, image and video models locally on commodity hardware, exposing an OpenAI-compatible API.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Checked against the scope bar this pass applied fourteen times and it lands on
the other side: LocalAI is not a framework for **building** an AI product, it is **infrastructure for
running models** — the layer a coding agent points at.

Its `Overlaps with` cell makes the placement clear: `tabby`, `osaurus`, and Ollama / LM Studio as
external references. `tabby` and `osaurus` were both left at `discovery-log` in the preceding slice on
the same reasoning — self-hosted and local-model serving is a real answer to the privacy, offline and
zero-cost constraints that several catalog rows exist to address (`smallcode` is the agent side of the
same story).

Not disposed, and not promoted either. Whether a local model is *good enough* to run a coding agent
against is precisely the measured question this band may not answer, and the honest state of the row is
that nobody has tried it here.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [LocalAI](https://github.com/mudler/LocalAI) | platform | Self-hosted AI engine (MIT, ★47K) — run LLM, vision, voice, and image models on any hardware, GPU optional, behind a drop-in OpenAI-compatible API | Cloud model APIs carry cost and privacy tradeoffs; LocalAI serves everything locally (model-serving infra; catalogued as the local-inference peer of tabby/osaurus) | tabby, osaurus, Ollama (ext.), LM Studio (ext.) |
