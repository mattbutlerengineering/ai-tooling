# Evaluation: notebooklm-py

**Repo:** [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py)
**Stars:** ~16,700 | **Last updated:** 2026-06-20 | **License:** MIT
**Dev loop stage:** Reflect (Research & Discovery)
**Layer:** Tooling

---

## What it does

An unofficial Python API and agentic skill for Google NotebookLM, giving full programmatic access to NotebookLM's features — including capabilities the web UI doesn't expose — via Python, a CLI, and AI agents (Claude Code, Codex, OpenClaw).

Mechanically it drives NotebookLM's **undocumented Google APIs**: create/manage notebooks, add sources, query grounded answers, and trigger features that are otherwise click-only in the web app. The agentic-skill packaging means a coding agent can use NotebookLM as a research backend programmatically. The README is explicit and prominent about the risk: it's **not affiliated with Google**, uses **undocumented endpoints that can change without notice**, and is subject to rate limits — "use at your own risk."

## How we tested it

Architecture review against the README and the stated surface (Python API + CLI + agent skill over NotebookLM's internal APIs). Confirmed the programmatic-access value proposition and, importantly, the maintainer's explicit warnings about unofficial/undocumented Google APIs that may break. Not run live (and live use carries the documented breakage/ToS risk), so condition-gated.

```bash
gh api repos/teng-lin/notebooklm-py --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/teng-lin/notebooklm-py/readme --jq '.content' | base64 -d
```

## What worked

- **Programmatic NotebookLM.** Driving NotebookLM (source grounding, notebooks, overviews) from Python/CLI/agents unlocks automation the web UI can't — useful as a grounded research backend.
- **Agent-ready.** Packaged as a skill for Claude Code/Codex/OpenClaw, so agents can use it directly.
- **Candid about risk.** The README leads with the unofficial/undocumented-API caveats rather than hiding them — responsible.

## What didn't work or surprised us

- **Built on undocumented APIs.** Can break without notice and may run against Google's terms; not something to build a critical pipeline on.
- **Rate limits + fragility.** Heavy use gets throttled; reliability is inherently shaky for an unofficial client.
- **Dependency on a closed product.** Value is entirely tied to NotebookLM's continued behavior and Google's tolerance.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | NotebookLM grounding gives cited, source-based answers |
| Speed | + | Automates research tasks otherwise done by hand in the web UI |
| Maintainability | - | Undocumented APIs break without notice — high upkeep risk |
| Safety | - | Unofficial use of Google internals; potential ToS exposure |
| Cost Efficiency | neutral | Free, but rate-limited and breakage-prone |

## Verdict

**CONDITIONAL**

Useful for automating NotebookLM-grounded research from agents/scripts when its grounding is exactly what you want — but treat it as inherently fragile: it rides undocumented Google APIs that can break or run afoul of terms. Fine for exploratory/personal automation; do **not** build a production-critical pipeline on it. For robust research, prefer first-party APIs or tools like storm/deep-research.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | tool | Unofficial Python API + agentic skill for Google NotebookLM (MIT, ★17K) — full programmatic access (incl. features the web UI hides) via Python/CLI/agents; ⚠️ uses undocumented Google APIs that can break without notice | Want to drive NotebookLM (source grounding, notebooks, overviews) from agents/scripts, not just the web UI | deep-research, storm, ref-tools-mcp |
