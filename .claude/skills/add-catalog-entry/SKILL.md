---
name: add-catalog-entry
description: Add a tool to CATALOG.md + COMPARISON.md and propagate all counts, then sync and audit. Use when adding a single catalogued tool by its GitHub slug. Triggers - "add X to the catalog", "catalog this repo", "/add-catalog-entry owner/repo".
disable-model-invocation: true
---

# Add Catalog Entry

Automates the 8-file workflow for adding one tool to the `ai-tooling` catalog. The
error-prone count arithmetic is handled by `reconcile-counts.py`; you supply the
judgement (category, one-liner, overlaps). Detector G then verifies the result.

## Inputs

- **slug** — GitHub `owner/repo` (required)
- **category** — one of the CATALOG section headers (Code Understanding, Agent
  Orchestration, Agent Harnesses, Memory & Context, Skills & Plugins, Code Review &
  Quality, Maturity Frameworks, Dev Workflow, MCP Servers, Observability, Research &
  Discovery, Security & Safety, Reference). Infer it; confirm if ambiguous.

## Steps

1. **Resolve the repo.** `gh api repos/{slug} --jq '{desc:.description, stars:.stargazers_count, license:(.license.spdx_id // "none"), pushed:.pushed_at[0:10]}'`. If it 404s, stop — a broken slug means there is nothing to catalogue.

2. **Dedup.** `grep -inE "\[<name>\]|github\.com/{slug}" CATALOG.md`. If the slug is already an entry, stop. If the *name* appears only inside other rows' prose/overlaps, that is the gap you are filling (this is how aider/cline/codex were found).

3. **Scope check.** Only catalogue dev-loop tooling (produces/reviews/tests/ships code, or agent/MCP infra for that). Skip proprietary-only, model-serving infra, chat UIs, and general business automation — note the skip and why.

4. **Craft the CATALOG row** (match the column format in `CLAUDE.md` > "Catalog format"):
   `| [name](https://github.com/{slug}) | <type> | <one-liner ~12 words> | <problem it solves> | <overlaps> |`
   - **Overlaps**: name 2-4 existing entries in the same category (check them first); mark external/conceptual peers with `(ext.)`.

5. **Insert the CATALOG row** under the chosen `## <category>` section (after a related peer).

6. **Find the COMPARISON stage and insert the body row.** Do NOT guess the stage — locate where a same-category peer already lives:
   `awk '/^## /{s=$0} /^\| <peer> /{print s}' COMPARISON.md`
   Insert `| <name> | <type> | <auto ✓/blank> | <free ✓/blank> | CONDITIONAL |` under that same `## section` (discovery-level adds are CONDITIONAL unless you ran a hands-on eval).

7. **Propagate counts.** `python3 reconcile-counts.py` — rewrites the catalog total in README/CLAUDE/STACK/plugin/CLAUDE and rebuilds COMPARISON's summary + Total from the new body rows. Never hand-edit counts.

8. **Sync the plugin copy.** `./sync-plugin-docs.sh`

9. **Audit.** `python3 audit-evals.py` — detectors A/B/D/G must all say OK (G proves CATALOG == COMPARISON). Also `/bin/bash plugin/hooks/validate-counts.sh` should be silent.

10. **Report** the new total and the one-line entry; commit only if asked (`docs(catalog): add <name> (N->N+1)`).

## Notes

- `reconcile-counts.py --check` reports drift without changing files (useful as a dry run / CI gate alongside detector G).
- For *several* tools at once, repeat steps 4-6 for each, then run 7-9 once.
- This skill changes catalog content (a durable artifact); it is user-invocable only.
