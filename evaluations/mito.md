# Evaluation: mito

**Repo:** [mito-ds/mito](https://github.com/mito-ds/mito)
**Stars:** ~2,640 | **Last updated:** 2026-06-11 | **License:** open-core (repo SPDX returns NOASSERTION; Mito Pro tier)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A set of Jupyter extensions that help you write Python faster — an AI coding assistant for the notebook/data-science workflow. There are three pieces:

1. **Mito AI** — context-aware AI chat and error debugging *inside* Jupyter, so you don't copy-paste between the notebook and ChatGPT/Claude (a "data copilot").
2. **Mito Spreadsheet** — an interactive spreadsheet UI where you can write formulas (VLOOKUP), apply filters, build pivot tables, and make graphs — and **every edit auto-generates production-ready Python** (pandas).
3. **Mito for Streamlit/Dash** — embed a full-featured spreadsheet into dashboards in two lines.

The core value for the dev loop is the in-notebook AI (chat + error debugging grounded in your notebook context) plus the spreadsheet-to-code generation that turns point-and-click data manipulation into real Python.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the three-component model (Mito AI copilot; spreadsheet→Python codegen; Streamlit/Dash embedding). Confirmed the in-notebook AI-assistant positioning and the auto-codegen mechanic. License resolves to NOASSERTION via the API — it's open-core with a Mito Pro tier; confirm what the OSS install includes. Not run in a live notebook, so condition-gated.

```bash
gh api repos/mito-ds/mito --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/mito-ds/mito/readme --jq '.content' | base64 -d
```

## What worked

- **AI in the notebook, no copy-paste.** Context-aware chat + error debugging grounded in the notebook removes the constant switch to a separate chat LLM — a real workflow win for data-science coding.
- **Spreadsheet-to-Python codegen.** Turning point-and-click data manipulation into production-ready pandas is genuinely useful for analysts who think in spreadsheets but need reproducible code.
- **Fits the data-science dev loop.** Jupyter-native (and Streamlit/Dash embedding) targets a niche the terminal/IDE coding assistants underserve.

## What didn't work or surprised us

- **Niche to notebooks.** Value is specific to Jupyter/data-science work; not relevant to general software dev outside notebooks.
- **Open-core, license unclear.** NOASSERTION via API + a Mito Pro tier — confirm OSS scope and terms before relying on features.
- **Overlaps general coding assistants partially.** tabby/aichat/Copilot also assist coding; mito's edge is the notebook-native AI + spreadsheet-to-code, not general completion.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Spreadsheet edits become reproducible Python; in-context AI debugging |
| Speed | + | In-notebook AI + point-and-click codegen speed data work |
| Maintainability | + | Generated production-ready Python vs. throwaway notebook hacks |
| Safety | neutral | Coding assistant; no direct safety effect |
| Cost Efficiency | ✓/$ | OSS core; Mito Pro tier and LLM usage cost |

## Verdict

**discovery-log — tentative read**

Adopt for Jupyter/data-science work where you want an in-notebook AI copilot (chat + error debugging, no copy-paste) and spreadsheet-to-Python codegen — it underserves a niche that terminal/IDE assistants miss. Confirm the open-core/license boundary. Not relevant to general software development outside notebooks; for that, tabby/aichat or an IDE assistant fit better.

## Triage note

Left at `discovery-log` — **and the eval's open question is now answered.** It asked to "confirm the
open-core/license boundary"; read live on 2026-08-04, `LICENSE` declares everything outside
`mitosheet/**/pro` and `mitosheet/**/enterprise` to be **AGPL-3.0**, with those two directories
proprietary. GitHub reports `NOASSERTION` because of that carve-out preamble, not because terms are
missing — the same parser failure this lane has now seen four times.

**The AGPL does not dispose this lead.** `triage.py`'s P4 copyleft rule is deliberately scoped to
*vendored* Types — `skill`/`plugin`, whose text is copied into your repo — because copyleft on
something you merely *run* imposes nothing. mito is a `tool`: a Jupyter extension you install. The
scoping exists precisely so a naive copyleft sweep can't take out live infrastructure.

Left rather than SKIPped on scope, too: it is a notebook-scoped Implement tool (in-notebook chat,
error debugging, spreadsheet-to-Python codegen) serving a niche terminal and IDE assistants miss.
★2.6K, pushed 2026-07-21.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mito](https://github.com/mito-ds/mito) | tool | AI coding assistant for Jupyter (open-core; SPDX unverified, ★2.6K) — context-aware AI chat + error debugging inside the notebook (no copy-paste to ChatGPT/Claude), plus a spreadsheet UI whose every edit (VLOOKUP/filters/pivots/graphs) auto-generates production-ready Python; also embeds in Streamlit/Dash | Data/notebook work means context-switching to a chat LLM and hand-writing pandas; want in-notebook AI + spreadsheet-to-code without leaving Jupyter | tabby, aichat, gptme |
