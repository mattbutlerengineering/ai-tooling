# Evaluation: ai-engineering-from-scratch

**Repo:** [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch)
**Stars:** 34,701 | **Last updated:** 2026-06-14 (pushed; created 2026-03-18) | **License:** MIT
**Dev loop stage:** Discover / Plan (outer loop — a learning path that builds background before you touch a real codebase)
**Layer:** Process / Infrastructure (a curriculum-as-process; ships runnable code, prompts, skills, agents, and MCP servers as artifacts)

---

## What it does

The catalog one-liner: "Learn AI engineering: build it, ship it for others." It is a large open-source curriculum — self-described as **503 lessons across 20 phases (~320 hours)** in four languages (Python, TypeScript, Rust, Julia) — that teaches AI/ML engineering from raw math up to multi-agent systems. The arc runs linear algebra and ML fundamentals → deep learning → transformers → "LLMs from scratch" → tools/protocols (MCP), agent engineering, autonomous systems, multi-agent swarms, production infrastructure, alignment, and a capstone.

The pedagogical hook is a six-beat lesson loop: MOTTO → PROBLEM → CONCEPT → **BUILD IT** (raw math, no frameworks) → **USE IT** (the same thing in PyTorch/sklearn) → **SHIP IT**. The "ship it" beat is the distinctive part: every lesson ends with a reusable artifact — a prompt, an Agent Skill (`SKILL.md`), an agent, or an MCP server — collected under each lesson's `outputs/`. The repo ships built-in agent skills (`/find-your-level` placement quiz, `/check-understanding <phase>` per-phase quiz) installable into Claude/Cursor/Codex via `scripts/install_skills.py`, plus a companion site (aiengineeringfromscratch.com).

## How we tested it

**Source-grounded inspection — not installed, not run.** No lesson was completed, no code was executed, no skill was installed, and the placement quiz was not taken. Every claim below is from the repository (GitHub metadata, README, top-level file tree) — including the lesson counts and reader stats, which are the author's self-reported figures, not anything I measured or verified.

```bash
gh api repos/rohitg00/ai-engineering-from-scratch --jq '{desc,stars,pushed,created,license}'
gh api repos/rohitg00/ai-engineering-from-scratch/readme --jq '.content' | base64 -d   # | head -240
gh api repos/rohitg00/ai-engineering-from-scratch/git/trees/HEAD --jq '.tree[].path'
gh api repos/rohitg00/ai-engineering-from-scratch/commits --jq '.[0].commit.committer.date'  # 2026-06-14
```

## What worked

- **Strong editorial structure.** The README is genuinely well-built: a phase dependency graph (mermaid), a fixed per-lesson template, three explicit on-ramps (read / clone-and-run / placement quiz), and a worked agent-loop sample. This is far more curated than a typical "awesome" list.
- **Build-it-then-use-it pedagogy is the right model.** Implementing backprop/tokenizer/attention/agent-loop from raw math before reaching for PyTorch is exactly how you build durable intuition. The ~120-line dependency-free agent loop shown in the README is a good example of the depth.
- **Artifacts make it actionable.** The "every lesson ships a prompt/skill/agent/MCP" framing connects learning to our catalog's own vocabulary, and the artifacts are installable cross-tool (Agent Skills standard).
- **Fresh and high-traction.** Created 2026-03, last pushed 2026-06-14 (active within days of evaluation), 34.7K stars, MIT license, with `CONTRIBUTING.md`, `CHANGELOG.md`, `ROADMAP.md`, and a CI/site build. Real project hygiene.

## What didn't work or surprised us

- **Mostly ML/AI engineering, not AI-assisted software development.** This is the central caveat for *this* catalog. 14+ of the 20 phases (math, ML, deep learning, vision, NLP, speech, RL, transformers, LLMs-from-scratch, multimodal) teach how to build models — not how to use AI tools to ship application code faster. The directly-relevant slice is Phases 13–17 (tools/protocols, agent engineering, autonomous/multi-agent, production). The repo's relevance to our remit is partial.
- **Self-reported scale is unverifiable and likely aspirational.** "503 lessons / 320 hours / 150,639 readers / 241,669 page views" are README figures generated from the author's own `site/stats.json`. The phase graph and ROADMAP suggest many lessons are still being filled in (the README says "open any *completed* lesson"), so 503 is the planned target, not a count of finished, reviewed content. Treat as a roadmap, not a delivered inventory.
- **Single-maintainer, heavy self-promotion.** The README opens by cross-promoting the author's other project (agentmemory) and a paid site, and the four-language promise (Python/TS/Rust/Julia for every lesson) is an enormous surface area for one author to keep correct and current.
- **Breadth over depth risk.** ~320 hours spanning linear algebra to swarms is a survey scope; for a working engineer who wants AI-assisted-dev practice specifically, the signal-to-effort ratio is low compared to a focused Claude Code guide.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Building algorithms from raw math then re-deriving in libraries builds the intuition to spot wrong model/agent behavior — but it teaches model internals, not correctness of AI-assisted *application* code. |
| Speed | neutral | A ~320-hour curriculum is a long-horizon investment; no near-term effect on daily dev velocity. |
| Maintainability | neutral | Pedagogical artifacts (prompts/skills/MCP) are illustrative; not production modules you'd maintain. |
| Safety | + | Dedicated phase on ethics & alignment, plus understanding model internals helps reason about failure modes — modest, indirect. |
| Cost Efficiency | + | Free, open-source, MIT, runs on your own laptop; only cost is time. |

## Verdict

**CONDITIONAL** — adopt as a deep-background learning path for engineers who want to understand how LLMs and agents *actually work* under the hood (Phases 13–17 are the parts most relevant to AI-assisted-dev practitioners), and skip it if you want a fast, focused on-ramp to using AI coding tools day-to-day. Its editorial quality and freshness are high, but the bulk of the curriculum is ML/AI-engineering fundamentals, only partially aligned with this catalog's AI-assisted-software-development remit, and its headline scale (503 lessons) is a self-reported target rather than a verified, completed inventory.

Compared to neighbors: it is a fundamentally different resource from the Claude Code learning entries. **claude-howto** and **claude-code-best-practice** are narrow, practical, copy-paste on-ramps to Claude Code itself — far more directly useful for this catalog's audience and much lower time-cost. **karpathy-llm-wiki / andrej-karpathy-skills** package conceptual knowledge as queryable skills (reference-on-demand), whereas this is a from-scratch *course* you work through linearly. **dictionary-of-ai-coding** is a glossary, not a path. ai-engineering-from-scratch is the most ambitious and best-produced learning resource in the set, but also the broadest and least targeted — recommend it to engineers who specifically want first-principles model/agent understanding, not as the default starting point for getting productive with AI coding tools.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) | reference | Free 20-phase, 503-lesson curriculum building AI/ML and agents from raw math up; each lesson ships a prompt/skill/agent/MCP artifact (34.7K stars) | Want a first-principles learning path for how LLMs and agents actually work, not just how to call APIs | karpathy-llm-wiki, andrej-karpathy-skills (conceptual depth, but reference-skills vs. linear course) |
