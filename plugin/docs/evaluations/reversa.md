# Evaluation: Reversa

**Repo:** [sandeco/reversa](https://github.com/sandeco/reversa)
**Stars:** 1,242 | **Last updated:** 2026-05-24 (pushed; created 2026-04-26) | **License:** MIT | **Install:** `npx reversa install`
**Dev loop stage:** Plan / Dev Workflow (spec generation — but *reverse*, from legacy code)
**Layer:** Tooling (multi-agent installer that writes specs into a legacy project)

---

## What it does

Reversa is a **reverse-documentation / specification reverse-engineering framework**: you install it inside a legacy project and it coordinates a team of specialized AI agents to analyze the existing code and **extract executable, traceable specifications** — business rules, flows, module contracts, retroactive architectural decisions — ready for any coding agent to consume. It's backed by an arXiv paper (Macedo & da Costa, May 2026).

The framing is sharp: forward SDD tools (spec-kit, OpenSpec) assume you *write the spec and the agent executes*. Legacy or "pure vibe-coded" systems have **no spec**, so an agent "has no way of knowing what it cannot break." Reversa is the bridge — it produces **operational contracts** (not human-readable docs) that let an agent evolve a legacy system with fidelity to what already exists. `npx reversa install` detects the AI engines present (Claude Code, Codex, Cursor, …) and installs the agent team.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No legacy project processed, no spec generated. Claims (including the "executable/traceable operational contracts") come from the README and the linked paper abstract, not observed output.

```bash
gh api repos/sandeco/reversa --jq '{stars,license:.license.spdx_id,created:.created_at,pushed:.pushed_at}'   # 1.2K, MIT
gh api repos/sandeco/reversa/readme --jq '.content' | base64 -d | head -40   # reverse-spec framing, npx installer, multi-engine
```

## What worked

- **Fills a real gap: the inverse of forward SDD.** spec-kit/OpenSpec/BMAD generate specs forward for new work; Reversa extracts them *backward* from legacy code. That's a genuinely distinct and underserved direction.
- **"Operational contracts, not docs" is the right framing.** Specs an agent can act on (and that bound what it must not break) are more useful for safe legacy evolution than prose documentation.
- **Multi-engine + low-friction.** `npx reversa install` with auto-detection of Claude Code/Codex/Cursor means it drops into existing setups.
- **Paper-backed, MIT, decent traction** (~1.2K stars) — more rigor than a typical prompt pack.

## What didn't work or surprised us

- **Quality of generated specs is the whole ballgame — and unverified.** Reverse-engineering implicit business rules from code is exactly where LLMs hallucinate plausible-but-wrong invariants. The value depends entirely on fidelity, which isn't validated here; a wrong "operational contract" is worse than none.
- **One-shot extraction vs. living spec.** Legacy systems drift; a generated spec is a snapshot. How it's kept in sync after the first pass isn't clear from the README.
- **Newish and single-author.** Promising and paper-backed, but young (created Apr 2026, last push May) and not yet battle-tested at scale.
- **Trust boundary.** It runs a team of agents over your whole legacy codebase to emit contracts you'll then act on — review the output before trusting it as ground truth.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / − | Good specs let agents change legacy code without breaking implicit rules; hallucinated specs actively mislead — verification required. |
| Speed | + | Bootstraps a spec for an undocumented system far faster than manual archaeology. |
| Maintainability | + | Captures trapped knowledge (business rules, contracts) as reusable artifacts. |
| Safety | + / neutral | "What it cannot break" contracts reduce blast radius — *if* accurate. |
| Cost Efficiency | neutral | Multi-agent analysis over a whole codebase has up-front token cost; amortized if the spec is reused. |

## Verdict

**CONDITIONAL** — Reversa targets a real, underserved problem — **extracting executable specifications backward out of legacy / vibe-coded systems** so coding agents can evolve them safely — with a sharp "operational contracts, not docs" framing, MIT license, paper backing, and multi-engine install. Adopt it to bootstrap a spec for an undocumented system, but **treat the generated contracts as a high-value draft to verify, not ground truth**: the failure mode (confidently hallucinated business rules) is the dangerous kind. Pilot on a module you understand to calibrate fidelity before trusting it on the parts "nobody wants to touch."

Compared to neighbors: **spec-kit**, **OpenSpec**, and **BMAD-METHOD** generate specs *forward* for new/continuing work; **Understand-Anything** builds a queryable graph for comprehension. Reversa's distinguishing pitch is **reverse spec-engineering** — turning existing legacy code into agent-ready operational contracts.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [reversa](https://github.com/sandeco/reversa) | framework | Reverse spec-engineering (MIT, paper-backed) — coordinates a team of AI agents over a legacy codebase to extract executable, traceable "operational contracts" (business rules, flows, module contracts) for any coding agent; `npx reversa install`, multi-engine | Legacy / vibe-coded systems have no spec, so agents don't know what they can't break — generate one backward from the code | spec-kit, OpenSpec, Understand-Anything |
