# Evaluation: reporails/cli

**Repo:** [reporails/cli](https://github.com/reporails/cli)
**Stars:** 68 | **Last updated:** 2026-06-27 (pushed) | **License:** NOASSERTION
**Dev loop stage:** Plan (agent-instruction diagnostics)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Diagnostics for AI instruction files across Claude, Codex, Copilot, Cursor and Gemini — tells you
whether your agent instructions are well-formed or conflicting.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata fetched fresh for this pass on
2026-08-04 plus the CATALOG one-liner and "Overlaps with" cell (`agnix`). Enough to place it; not enough
for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. The problem it names is one this repo has first-hand: instruction files grow,
contradict themselves, and nothing tells you. `CLAUDE.md` here is long enough that its own front-door copy
drifted silently twice (#302, #313), and the fix in both cases was to gate the shared facts rather than
trust the prose — which is the same instinct this tool automates.

Not disposed. `agnix` is the only listed neighbour and the overlap cell already marks them complementary:
agnix lints and provides an LSP, this diagnoses whether the instructions are coherent. Different objects.

Two reasons it stays a lead rather than becoming a recommendation. ★68 and pushed 2026-06-27, so there is
little adoption signal either way. And `repo-metadata.json` records **`NOASSERTION`** — per CLAUDE.md that
means GitHub could not parse the LICENSE file, never that a grant is absent, and it never disposes a lead.
It does need a human read before adoption; four rows across this issue now sit in that state
(`NeMo-Guardrails`, `rogue`, `agenta`, and this one), which is enough to be worth a sweep of its own.

The measurable version of its claim is appealing: run it against a set of instruction files with known
planted contradictions and count what it catches.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [reporails/cli](https://github.com/reporails/cli) | tool | AI instructions diagnostics for Claude, Codex, Copilot, Cursor, Gemini agents | Don't know if CLAUDE.md / agent instructions are well-formed or conflicting | agnix (complementary: reporails = diagnostics, agnix = lint + LSP) |
