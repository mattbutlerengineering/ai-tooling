---
name: find-catalog-gaps
description: Find tools that probably belong in CATALOG.md but aren't there, via referenced-but-not-catalogued detection + a foundational-tools checklist. Use to audit the catalog for missing heavyweight tools. Triggers - "find catalog gaps", "what's missing from the catalog", "audit catalog completeness".
---

# Find Catalog Gaps

The highest-yield discovery method once star-ranked sweeps saturate: find tools the
catalog already *refers to* but never *entered*. This surfaced codex (92K), cline
(63K), MetaGPT (69K), aider (46K) — all missing despite being the largest tools in
their categories. This skill is **read-only**: it reports candidates; you vet and
add them (with `/add-catalog-entry`).

## Run it

```bash
python3 .claude/skills/find-catalog-gaps/find-gaps.py
```

This combines two signals:

1. **Detector F** (`audit-evals.py --overlaps`) — "Overlaps with" tokens naming a
   tool that has no entry of its own. Multi-reference tokens are the likeliest gaps;
   single-reference ones are usually deliberate external/conceptual peers.
2. **Foundational checklist** — a curated list (in `find-gaps.py`) of heavyweight
   in-scope tools whose peers are catalogued. Anything `MISSING` is a candidate.

## Vet before adding

A candidate is a *lead*, not a decision. Add only dev-loop tooling (produces /
reviews / tests / ships code, or agent/MCP infra for that). Skip — and note why —
proprietary-only tools, model-serving infra (ollama, vllm), chat UIs (open-webui),
and general business automation. Confirm the peer-consistency argument: if a
candidate's peers are catalogued, its absence is a real inconsistency.

## Extend the checklist

`find-gaps.py`'s `CHECKLIST` dict is meant to grow as the ecosystem moves — add new
heavyweight tools under the right group. Keep names matching how they'd appear in a
`[name](` link. A clean run prints "every checklist tool has a catalog entry".

## Related

- `/add-catalog-entry` — add a vetted candidate (handles count propagation + audit).
- Detector F lives in `audit-evals.py`; this skill wraps it with the checklist.
