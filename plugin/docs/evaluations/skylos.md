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

Architecture review against the README, the documented commands/flags, and the issue categories. Confirmed the local-first model, the `-a` aggregate scan, the `verify --range` agent-handoff gate, the `init` config surface, and the AI-code-mistake / LLM-app-risk detectors that distinguish it from generic linters. The published benchmark/real-world-results pages are project-authored — not independently reproduced. Not run on a live repo, so condition-gated.

```bash
gh api repos/duriantaco/skylos --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/duriantaco/skylos/readme --jq '.content' | base64 -d
```

## What worked

- **Single offline command, broad coverage.** Dead code + secrets + CVEs + quality + AI-slop in one `skylos . -a` run, fully local — no service round-trip, good for privacy and for pre-commit/pre-merge speed.
- **Purpose-built for AI-generated code.** Detectors for invented package APIs, fake helpers, missing guards, and impossible versions target exactly the failure modes of LLM output that ordinary linters miss.
- **Agent-handoff gate.** `skylos verify --range ... --project-context` is designed to vet a changed range before it goes to (human or AI) review — a clean fit for an agentic workflow.

## What didn't work or surprised us

- **Deterministic, not semantic.** It's static analysis, so it catches structural/pattern issues, not logic bugs or intent drift — complements, not replaces, an LLM reviewer (vet, kodus-ai, /code-review).
- **Self-reported benchmarks.** Real-world-results and benchmark pages are authored by the project; validate signal/noise on your codebase.
- **Younger/smaller project.** ~450 stars; broad language coverage means depth-per-language will vary.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Catches dead code, dangerous data flows, and AI-code mistakes pre-merge |
| Speed | + | Local single-command scan; CI action gates PRs |
| Maintainability | + | Flags complexity/duplication/dead code regressions |
| Safety | + | Secrets, CVEs, and LLM-app risks (unsafe tool use) detection — all offline |
| Cost Efficiency | + | Free, local, no per-review LLM cost |

## Verdict

**CONDITIONAL**

Adopt as a fast, free, offline pre-merge gate alongside (not instead of) an LLM reviewer — especially valuable for catching AI-generated-code defects and leaked secrets without a service round-trip. Pair `skylos . -a` in CI with a semantic reviewer (vet / kodus-ai / /code-review) for logic and intent. Validate its findings' signal-to-noise on your repo before making it a blocking gate.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skylos](https://github.com/duriantaco/skylos) | tool | Local-first static-analysis PR gate (Apache-2.0) — one CLI scans 12 languages for dead code, security flaws, secrets, CVEs, quality regressions, and AI-code mistakes plus LLM-app risks; runs locally or as a CI/CD action | Want one offline command to catch dead code, secrets, CVEs, and AI slop before merge without a service | vet, brooks-lint, tdd-guard, semgrep (ext.) |
