# Evaluation: skylos

**Repo:** [duriantaco/skylos](https://github.com/duriantaco/skylos)
**Stars:** ~450 | **Last updated:** 2026-06-20 | **License:** Apache-2.0
**Dev loop stage:** Review (static analysis / PR gate)
**Layer:** Tooling

---

## What it does

A local-first static-analysis CLI and PR gate. One command scans a repo or a changed range across 12 languages (Python, TypeScript, JavaScript, Java, Go, Kotlin, PHP, Rust, Dart, C#, Shell, and deployment config) and reports a broad set of issues without sending code to a service.

Mechanically: `pip install skylos` then `skylos .` (default scan focuses on dead code), `skylos . -a` to add security, secrets, quality, and dependency checks, or `skylos verify . --file src/app.py --range 40:75 --project-context` to gate a specific changed range before an agent hands it to review. `skylos init` creates a project config with thresholds, ignores, template hooks, and a "vibe dictionary." It finds: dead code/unused files; security flaws and dangerous data flows; secrets and dependency CVEs; CI/CD and edge-device deployment misconfigurations; quality regressions (complexity, duplicate branches, deep nesting); **AI-generated code mistakes** (missing guards, fake helpers, invented package APIs, impossible dependency versions); and LLM-app risks (unsafe tool use, missing output validation). Ships a GitHub Action and a VS Code extension.

## How we tested it

**Hands-on**, skylos v4.25.0 `pip install`ed into a clean venv and run against this repo's only real code — the `presentations/` JS (a Web Components deck) — on 2026-06-20. Exercised the default dead-code scan, the `-a` aggregate scan (security/secrets/quality/deps), and the `verify --range` agent-handoff gate.

```bash
python3 -m venv venv && source venv/bin/activate && pip install skylos   # v4.25.0, clean install
skylos <repo>/presentations            # default: 3 "unused functions" @ 100% confidence
skylos <repo>/presentations -a         # graded scorecard across 4 dimensions
skylos verify <repo>/presentations --file development-process/deck-stage.js --range 580:585
#   → {"findings": [], "summary": "No AI-code issues found"}   (clean structured JSON)
```

**Measured results.** The `-a` scan produced a weighted, graded scorecard:

| Dimension | Grade | Finding |
|-----------|-------|---------|
| Security | **F** | **Critical: `new Function()`** (dynamic code execution) + **High: XSS / untrusted input** — both *real* dangerous patterns in the deck JS |
| Quality | D- | 62 complexity/function issues |
| Dead Code | A+ | 3 symbols flagged @ 100% confidence |
| Dependencies | A+ | No issues |

The **security findings were genuinely valuable** — it correctly caught `new Function()` (code-injection risk) and an XSS pattern. But the **dead-code "100% confidence" flags included a false positive**: `DeckStage.observedAttributes` is a Web Components lifecycle getter the browser calls automatically (not dead), and `reset`/`goTo` are public API likely called from HTML — skylos's static analysis doesn't see custom-element callbacks or HTML callers. The `verify` mode returned clean structured JSON, confirming the agent-handoff gate works.

## What worked

- **Security scanning earns its keep (verified).** On real JS it caught a Critical `new Function()` and a High XSS pattern — both genuine risks an LLM might emit and a plain linter often misses. This was the standout validated feature.
- **Clean install + fast, offline.** `pip install skylos` worked first try (v4.25.0) in a venv; the whole multi-dimension `-a` scan ran locally in seconds with no service round-trip or API key.
- **Graded, weighted scorecard is actionable.** Security F / Quality D- / Dead A+ / Deps A+ with severity weighting tells you *where* to look first, not just a flat list.
- **Agent-handoff gate works.** `skylos verify --range` returned clean structured JSON (`{"findings": [], "summary": ...}`) — a clean fit for gating a changed range before (human or AI) review.

## What didn't work or surprised us

- **Dead-code false positives, even at "100% confidence" (observed).** It flagged `observedAttributes` — a Web Components callback the browser invokes automatically — plus two public methods likely called from HTML, all at 100%. Static analysis can't see custom-element lifecycle or non-JS callers, so do **not** auto-delete its dead-code hits; treat "100%" as "100% confident *nothing in the analyzed files* references this," which isn't the same as unused.
- **Deterministic, not semantic.** It catches structural/pattern issues, not logic bugs or intent drift — complements, not replaces, an LLM reviewer (vet, kodus-ai, /code-review).
- **Younger/smaller project.** ~450 stars; broad language coverage means depth-per-language will vary, and (as seen) framework-aware understanding is limited.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | +/- | Catches dangerous data flows pre-merge, but dead-code detection over-reports framework callbacks (observed FP at 100% conf) |
| Speed | + | Local multi-dimension scan ran in seconds; CI action gates PRs |
| Maintainability | + | Flags complexity/duplication regressions (62 quality issues found here) |
| Safety | + | **Verified**: caught Critical `new Function()` + High XSS in real code — all offline |
| Cost Efficiency | + | Free, local, no per-review LLM cost |

## Verdict

**CONDITIONAL** *(verdict confirmed by hands-on testing)*

A fast, free, offline pre-merge gate that earns its place **for the security pass specifically** — verified catching a real Critical `new Function()` and an XSS pattern that a plain linter would miss. Run `skylos . -a` in CI alongside (not instead of) a semantic reviewer (vet / kodus-ai / /code-review) for logic and intent. One hands-on caveat that should shape how you use it: **its dead-code detector over-reports framework callbacks even at "100% confidence"** (it called a Web Components lifecycle getter "unused"), so wire the *security/secrets* dimensions as a blocking gate but keep dead-code as advisory, not auto-delete. Clean `pip install`, runs in seconds locally.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skylos](https://github.com/duriantaco/skylos) | tool | Local-first static-analysis PR gate (Apache-2.0) — one CLI scans 12 languages for dead code, security flaws, secrets, CVEs, quality regressions, and AI-code mistakes plus LLM-app risks; runs locally or as a CI/CD action | Want one offline command to catch dead code, secrets, CVEs, and AI slop before merge without a service | vet, brooks-lint, tdd-guard, semgrep (ext.) |
