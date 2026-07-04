# Evaluation: Giskard (giskard-oss)

**Repo:** [Giskard-AI/giskard-oss](https://github.com/Giskard-AI/giskard-oss)
**Stars:** 5,438 | **Last updated:** 2026-06-19 (pushed) | **License:** Apache-2.0 | **Language:** Python (PyPI: `giskard`)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Observability / Verify — eval, red-teaming, test generation for agents
**Layer:** Tooling (Python library)

---

## What it does

Giskard is **an open-source Python library for testing and evaluating agentic systems** — "evals, red teaming, and test generation for agentic systems," modular, lightweight, dynamic, async-first. The **v3** rewrite is a modular set of focused packages built to wrap anything (an LLM, a black-box agent, a multi-step pipeline): **`giskard-checks`** (beta) — scenario API, built-in checks, LLM-as-judge for multi-turn testing; **`giskard-scan`** (in progress) — agent vulnerability scanner for red teaming, prompt injection, data leakage (successor to v2 Scan); **`giskard-rag`** (planned) — RAG evaluation + synthetic test-set generation (successor to v2 RAGET). `pip install giskard` (Python 3.12+). Optional aggregated telemetry (no prompts/outputs), opt-out documented. v2 remains available but unmaintained.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No scenarios authored, no scan executed.

```bash
gh api repos/Giskard-AI/giskard-oss --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 5438, Apache-2.0, pushed 2026-06-19
gh api repos/Giskard-AI/giskard-oss/readme --jq '.content' | base64 -d | sed -n '115,170p'        # v3 packages, checks/scan/rag, LLM-as-judge
```

## What worked

- **Multi-turn, agent-first testing.** v3 is explicitly built for **dynamic, multi-turn** agent testing — closer to how agents actually behave than single-prompt eval, and a real complement to promptfoo's declarative-config style.
- **Three concerns, one library.** Scenario checks (correctness), a vulnerability scanner (security/red-team), and RAG eval+synthetic data — covering eval, safety, and test generation.
- **Modular, lightweight rewrite.** Dropping heavy deps and splitting into focused packages (each carrying only what it needs) is a sensible architecture and lowers adoption friction.
- **LLM-as-judge built in.** Scenario API + judge make subjective behavior testable.
- **Established vendor, Apache-2.0.** Giskard is a known AI-testing company; open core with a documented telemetry opt-out.

## What didn't work or surprised us

- **v3 is mid-migration.** `giskard-checks` is beta; the **vulnerability scanner and RAG eval still rely on v2** (in-progress/planned in v3). The most-cited features aren't fully on the new architecture yet.
- **Tests your AI product, not your coding agent.** Like promptfoo, the object is the agentic *system you build*; relevant when shipping LLM features, tangential to code authoring.
- **Python 3.12+ only.** A relatively high floor.
- **Overlaps promptfoo head-on.** Both do LLM eval + red-teaming; the wedge is Giskard's multi-turn/agent-scenario focus + synthetic test generation vs. promptfoo's declarative/CI-native breadth and larger ecosystem.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Scenario checks + LLM-as-judge catch agent behavior regressions across multi-turn flows. |
| Speed | neutral | Async-first, lightweight; authoring scenarios + running scans takes effort and inference. |
| Maintainability | + | Versioned scenarios/checks are repeatable regression tests for agent behavior. |
| Safety | + | Vulnerability scanner targets prompt injection and data leakage (red teaming). |
| Cost Efficiency | neutral | Apache-2.0/free; judge + scan inference cost money. |

## Verdict

**CONDITIONAL** — Giskard (v3, `giskard-oss`) is a credible, Apache-2.0 **agent testing + red-teaming library** whose distinctive angle is **dynamic, multi-turn scenario testing** plus a vulnerability scanner and RAG eval/synthetic-data generation. Adopt it when you're shipping agentic/RAG systems and want multi-turn behavioral tests and red-teaming as code — especially as a complement to promptfoo (Giskard for scenario/agent depth, promptfoo for declarative breadth + CI). It's CONDITIONAL because v3 is mid-migration (scan/RAG still on v2), it needs Python 3.12+, and like all eval tools its object is the AI system you build rather than the coding agent. Pilot `giskard-checks` now; watch the v3 scan/RAG ports before relying on them.

Compared to neighbors: **promptfoo** is the declarative, CI-native eval + red-team standard; **langfuse** is tracing-first observability + evals; **evalview** is MCP-based agent regression testing. Giskard's distinguishing pitch is **multi-turn agent scenario testing with LLM-as-judge plus a vulnerability scanner and RAG synthetic-data generation.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [giskard-oss](https://github.com/Giskard-AI/giskard-oss) | tool | Open-source eval, red-teaming, and test generation for agentic systems (Apache-2.0) — v3 rewrite: modular async-first packages for scenario-based checks + LLM-as-judge, an agent vulnerability scanner (prompt injection, data leakage), and RAG evaluation | Need to systematically test multi-turn agents and scan them for vulnerabilities, not just spot-check prompts | promptfoo, langfuse, evalview |
