# Evaluation: ACE (Agentic Context Engine)

**Repo:** [kayba-ai/agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine)
**Stars:** 2,449 | **Last updated:** 2026-06-13 (pushed) | **License:** Apache-2.0 | **Language:** Python (`ace-framework`; LiteLLM, 100+ providers)
**Dev loop stage:** Memory & Context (in-context learning / self-improvement)
**Layer:** Infrastructure (framework/library; open-source engine behind the hosted Kayba service)

---

## What it does

ACE adds a **persistent learning loop** to agents: "AI agents don't learn from experience — they repeat the same mistakes every session, forget what worked, and ignore what failed." ACE maintains a **Skillbook**, a persistent collection of strategies that evolves with every task, managed by three roles: **Agent** (executes tasks, enhanced with Skillbook strategies), **Reflector** (analyzes execution traces to extract what worked/failed), and **SkillManager** (curates — adds, refines, removes strategies). The key innovation is a **Recursive Reflector** that, instead of summarizing traces in one pass, **writes and runs Python in a sandbox** to programmatically search for patterns, isolate errors, and iterate until it finds actionable insights. No fine-tuning, no training data, no vector DB. Install `uv add ace-framework`; `ace setup` or set a provider key; use `ACELiteLLM(model=...)`, call `agent.ask(...)`, feed corrections via `agent.learn_from_feedback(...)`, inspect with `agent.get_strategies()`. It is the open-source engine behind the managed [Kayba](https://kayba.ai) service. Reported results: **2× consistency** (pass^4 on Tau2 airline, 15 learned strategies, no reward signals), **49% token reduction** on browser automation (10-run learning curve), and a **$1.50** learning run where Claude Code translated 14k lines to TypeScript with zero build errors.

## How we tested it

**Source-grounded inspection — not installed, not run.** No agent trained, no Skillbook built, the benchmark numbers not reproduced.

```bash
gh api repos/kayba-ai/agentic-context-engine --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 2449, Apache-2.0, pushed 2026-06-13
gh api repos/kayba-ai/agentic-context-engine/readme --jq '.content' | base64 -d | sed -n '553,645p'        # Skillbook, three roles, Recursive Reflector
```

## What worked

- **Learning, not just recall.** The Skillbook stores *strategies* distilled from traces, not transcripts — a stronger model than conversation memory, and aligned with the "experience reuse" thesis (cf. memind, MemOS, hivemind).
- **Recursive Reflector is a real idea.** Writing and executing sandboxed Python to mine traces for patterns (rather than one-shot summarizing) is a concrete mechanism for extracting *actionable* insight, and is the genuine differentiator.
- **No fine-tuning / no vector DB.** Purely in-context strategy injection keeps it lightweight and model-agnostic (LiteLLM, 100+ providers), avoiding training pipelines and embedding infra.
- **Falsifiable, specific claims.** Tau2 pass^4, 49% token cut, $1.50/14k-line run are concrete and testable (still vendor-reported).
- **Clean library API + open core.** `learn_from_feedback` / `get_strategies` make the loop legible; Apache-2.0.

## What didn't work or surprised us

- **Vendor-reported metrics.** All headline numbers come from Kayba; "no reward signals, 2× consistency" is impressive but unverified and benchmark-setup-sensitive.
- **Sandboxed code-writing reflector is a power/risk surface.** A component that writes and runs Python to analyze traces is potent but is exactly the kind of capability that needs sandboxing discipline and auditability.
- **Open-core/upsell framing.** ACE is positioned as the engine behind the managed Kayba service (which ships fixes as PRs); the smoothest "whole loop" is the paid product.
- **Crowded self-improving-memory niche.** Overlaps pro-workflow (correction-driven memory), hivemind (traces→skills), MemOS/memind (experience reuse), claude-reflect (corrections→CLAUDE.md). The wedge is the Skillbook + Recursive Reflector, not the category.
- **Curation quality is the whole game.** What the SkillManager promotes/retires determines whether the Skillbook compounds or accumulates noise — not evaluated here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Reflected strategies injected from past traces reduce repeated mistakes; claimed 2× Tau2 consistency. |
| Speed | + / neutral | Learned strategies shortcut re-derivation; the recursive reflection pass itself costs time per learning step. |
| Maintainability | neutral | `get_strategies` makes the Skillbook inspectable; a self-curating strategy store is another component to govern. |
| Safety | neutral / − | Sandboxed code-writing reflector and auto-curated strategies are an auditability surface to govern. |
| Cost Efficiency | + | Claimed 49% token reduction + $1.50 learning runs; no fine-tuning or vector DB to host. |

## Verdict

**CONDITIONAL** — ACE is an Apache-2.0 **in-context learning framework** whose distinctive ideas are the **Skillbook** (persistent, curated strategies distilled from execution traces) and the **Recursive Reflector** (writes and runs sandboxed Python to mine traces for actionable patterns instead of one-pass summarizing) — all without fine-tuning or a vector DB. Adopt it when you want an agent that *measurably improves with use* on repeated task types and you can wire it into your loop via LiteLLM, treating the 2×/49%/$1.50 figures as vendor-reported and piloting on your own data. Govern the code-writing reflector and watch what the SkillManager promotes. For Claude-Code-native correction learning, pro-workflow/claude-reflect are lighter; ACE is the choice when you want a programmatic, provider-agnostic learning engine (and its hosted Kayba upsell ships fixes as PRs).

Compared to neighbors: **pro-workflow** is correction-driven Claude Code memory; **hivemind** turns traces into shared skills; **MemOS**/**memind** crystallize experience into reusable policy; **claude-reflect** syncs corrections to CLAUDE.md. ACE's distinguishing pitch is **a curated Skillbook plus a Recursive Reflector that programmatically mines traces — model-agnostic, no fine-tuning, no vector DB.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ACE (agentic-context-engine)](https://github.com/kayba-ai/agentic-context-engine) | framework | Persistent learning loop (Apache-2.0) — Agent/Reflector/SkillManager roles curate a "Skillbook" of strategies extracted from execution traces (no fine-tuning, no vector DB); claims 2× consistency on Tau2, 49% fewer tokens; LiteLLM/100+ providers | Agents repeat the same mistakes and forget what worked; want experience distilled into reusable in-context strategies | pro-workflow, hivemind, MemOS, memind, claude-reflect |
