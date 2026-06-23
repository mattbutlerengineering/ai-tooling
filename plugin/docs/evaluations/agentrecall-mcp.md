# Evaluation: AgentRecall-MCP

**Repo:** [Goldentrii/AgentRecall-MCP](https://github.com/Goldentrii/AgentRecall-MCP)
**Stars:** 303 | **Last updated:** 2026-06-19 | **License:** MIT
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

AgentRecall is an MCP-server (+ SDK + CLI) persistent-memory system for AI coding agents whose distinguishing thesis is **correction-first, compounding memory**: rather than passively capturing everything, its core unit is the `CorrectionRecord` — every time you tell the agent "no, that's wrong" / "ask before assuming", it logs a correction with severity, holder, and evidence, then after N cross-session confirmations auto-promotes it to a cross-project "awareness" insight. It claims a *measurable* learning loop: each correction tracks `retrieved_count`, `heeded_count`, `recurrence_count`, and a `precision = heeded / retrieved` KPI used to archive low-signal memories (`precision < 0.3`) and fast-promote high-signal ones (`precision ≥ 0.8`).

Mechanically, memory is **local markdown only** under `~/.agent-recall/projects/<slug>/`, organized into five layers mapped to the cognitive-psychology taxonomy (episodic `journal/`, semantic `palace/rooms/`, procedural `palace/skills/`, narrative `palace/pipeline/`, correction `corrections/`) plus a cross-project `awareness` layer. Retrieval cites published math: FSRS-lite decay, Modern Hopfield retrieval (Ramsauer 2020), and RRF fusion (Cormack 2009). A deliberate design choice: it ships **only 5 MCP tools by default** (`session_start`, `session_end`, `remember`, `recall`, `check` — a "two-verb inhale/exhale" model), with the full 18-tool surface gated behind `--full`. The author justifies this with an "Automaticity Law" observation that pull-style tools got *zero* organic calls across 44 real projects, so only the push channels (session hooks + correction capture) ship by default. Storage is zero-cloud/zero-key by default; an optional Supabase + pgvector mirror adds semantic embeddings and gracefully degrades to keyword search when unconfigured. Workflow is driven by slash commands: `/arstatus` (cross-project status board), `/arstart` (load context), `/arsave` (consolidate), `/arsaveall`, `/arbootstrap`.

## How we tested it

**Evidence:** REVIEW

Architecture review via the GitHub API — confirmed repo identity, read the main README, `SKILL.md` frontmatter, the recursive file tree, the release list, contributor list, and the shipped benchmark scorecard (`benchmark/replay-results.json`). **Not installed or run hands-on.** Rationale matches the prior memory-category evals (agentmemory, SimpleMem, memsearch): the user already runs claude-mem (ADOPT) + OMEGA, and standing up a competing memory layer with its own session hooks and `~/.agent-recall/` store risks conflicting with the live setup. Calibrated against `evaluations/agentmemory.md` (CONDITIONAL), `evaluations/simplemem.md` (CONDITIONAL), and claude-mem (ADOPT — the user's choice).

```bash
gh search repos AgentRecall --limit 20 --json fullName,description,stargazersCount,url,updatedAt   # disambiguate the name
gh api repos/Goldentrii/AgentRecall-MCP --jq '{description,stars:.stargazers_count,license:.license.spdx_id,pushed_at,created_at,open_issues,forks:.forks_count}'
gh api repos/Goldentrii/AgentRecall-MCP/readme --jq '.content' | base64 -d
gh api "repos/Goldentrii/AgentRecall-MCP/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/Goldentrii/AgentRecall-MCP/releases --jq '.[].tag_name'                 # v3.4.30 latest
gh api repos/Goldentrii/AgentRecall-MCP/contributors --jq '.[].login'                # 2 contributors
gh api repos/Goldentrii/AgentRecall-MCP/contents/SKILL.md --jq '.content' | base64 -d
gh api repos/Goldentrii/AgentRecall-MCP/contents/benchmark/replay-results.json --jq '.content' | base64 -d
```

**Repo identity confirmed.** The catalog name "AgentRecall-MCP" disambiguates against ~6 unrelated "AgentRecall" repos (a .NET skeleton, a TF-IDF CLI, several empty/0-star hackathon repos). The only mature match is `Goldentrii/AgentRecall-MCP` — 303 stars, 52 forks, MIT, npm `agent-recall-mcp`, the description verbatim matching the catalog one-liner ("Persistent, correction-driven memory… npm: agent-recall-mcp").

## What worked

- **Genuinely distinct thesis (correction-first / compounding).** This is *not* another "capture-everything + hybrid-search" recall tool. The first-class unit is the human correction, with a promotion path from per-project `CorrectionRecord` → cross-project `awareness` insight after N confirmations. No other catalog memory entry (claude-mem, agentmemory, SimpleMem, OMEGA, memsearch) makes corrections the primary object. This is the same axis OMEGA touches but framed as a measurable feedback KPI rather than a graph.
- **Token-efficient by design — 5 MCP tools by default.** Directly addresses the biggest knock against agentmemory (53 tools) and the general MCP-tool-bloat problem. The "Automaticity Law" justification (pull tools got zero organic calls across 44 projects) is an honest, data-grounded design decision, and the two-verb inhale/exhale model is the most context-frugal memory surface in the category.
- **Zero-cloud, zero-key, local-markdown-only default.** Everything in `~/.agent-recall/` as plain markdown — greppable, Obsidian-compatible, git-versionable. The SKILL.md frontmatter declares `network: none`, `credentials: none`, `telemetry: none`, `filesystem: read-write ~/.agent-recall/ only`. This is a Safety/Cost win on par with claude-mem and agentmemory, and strictly better than SimpleMem (which mandates a paid LLM key with no local fallback).
- **Measurable precision KPI.** `precision = heeded / retrieved` with archive/promote thresholds is a concrete, falsifiable "is the memory actually working" signal — more operationally honest than competitors' recall-only framing.
- **Real engineering surface.** TypeScript monorepo, 4 published npm packages (core/mcp-server/sdk/cli), CI + release workflows, Dockerfile, a benchmark suite, a security-audit doc, multilingual README, an offline "War Room" dashboard, and frequent releases (v3.4.30, pushed same-day). Broad platform support (Claude Code primary; Cursor/Windsurf/VS Code/Codex via MCP; SDK + CLI).
- **Published-research grounding (cited).** FSRS-lite, Modern Hopfield, RRF — the retrieval/decay mechanisms reference real literature rather than hand-waving.

## What didn't work or surprised us

- **The shipped "benchmark" is a toy.** `benchmark/replay-results.json` (v3.4.30, 2026-06-18) scores on **3 recall items, 6 precision items, 1 staleness item, 2 correction items** — and the headline precision number is **0.33** (2 of 6). This is an internal smoke test, *not* a published, reproducible retrieval benchmark like agentmemory's LongMemEval-S (500 questions) or SimpleMem's arXiv-backed LoCoMo runs. The "measurable learning loop" claim is architecturally credible but **not yet empirically demonstrated at scale**; the precision KPI is the right idea evaluated on near-zero data.
- **Two contributors, single-author design.** `Goldentrii` + one other. Like agentmemory's opaque "iii engine," you're trusting a single-author infrastructure layer — but with far fewer stars (303 vs 23K), no large test-count claim, and 26 open issues. Created 2026-03-24: young, fast-moving (v3.4.x churn), pre-maturity.
- **Hook/store collision risk with the user's live setup.** AgentRecall wants its own `session_start`/`session_end` push channels and its own `~/.agent-recall/` store. The user already runs claude-mem (session hooks + its own store) and OMEGA. Two correction/consolidation-on-session-end systems firing on the same lifecycle is a real conflict surface, with no documented coexistence strategy.
- **Self-referential evidence.** The "Automaticity Law" (zero pull-tool calls across 44 projects) and the precision data come from the author's own live corpus — a reasonable design signal, but self-reported, same caveat applied to agentmemory's and SimpleMem's self-comparisons.
- **Slash-command + manual-discipline workflow.** Compounding depends on the human/agent actually running `/arstatus` … `/arsave` each session (the README stresses "without `/arsave`, nothing compounds"). There are correction hooks, but the headline loop leans on session-bracketing discipline rather than fully transparent auto-capture the way claude-mem's hooks do.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Correction-first capture + cross-project promotion targets the "same bug recurred" failure mode directly; but the recall/precision benchmark is a 3–6-item smoke test, not validated at scale |
| Speed | + | 5 default MCP tools (vs agentmemory's 53) minimizes context/token overhead; local markdown read/write is fast and dependency-free |
| Maintainability | neutral | Clean 4-package TS monorepo with CI, but young (created Mar 2026), 2 contributors, 26 open issues, rapid v3.4.x churn |
| Safety | + | Zero-cloud / zero-key / zero-telemetry default; filesystem scoped to `~/.agent-recall/`; optional Supabase is opt-in and degrades gracefully |
| Cost Efficiency | + | Free local embeddings/keyword search, no API key required, and the deliberately small tool surface reduces per-call context cost |

## Verdict

**CONDITIONAL**

AgentRecall is a credible, MIT-licensed, local-first memory MCP whose real differentiator is **correction-first compounding memory** with a measurable precision KPI and a deliberately minimal 5-tool surface — axes that make it *additive*, not a thin duplicate of the existing memory CONDITIONALs. agentmemory competes on benchmarked hybrid-search recall and 15+ platform breadth; SimpleMem competes on token-efficient compression and multimodality; AgentRecall competes on *learning from human corrections* and tool-surface frugality, which neither of them centers. Use it when the pain you're solving is **"my agent keeps making the same mistake I already corrected"** and you want a zero-cloud, low-tool-count memory you can grep in markdown.

For this user's case — Claude Code, local-first, already on claude-mem (ADOPT) + OMEGA — it does **not** displace claude-mem: it's far younger (303 stars vs claude-mem's mature plugin ecosystem), its "measurable learning loop" is so far validated only on a 3–6-item internal benchmark, and adopting a second session-hook + on-disk store layer risks colliding with the live claude-mem/OMEGA setup. Like agentmemory and SimpleMem (both CONDITIONAL), it wins on a specific axis (correction-first compounding + minimal tool surface) and loses to claude-mem on battle-testing and ecosystem fit. KEEP the catalog entry; CONDITIONAL, not ADOPT, not SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [AgentRecall-MCP](https://github.com/Goldentrii/AgentRecall-MCP) | MCP server | Correction-first, compounding local-markdown memory for AI agents; 5 MCP tools by default, zero-cloud | Agents repeat already-corrected mistakes; need a measurable, low-overhead memory that learns from human corrections across sessions | claude-mem, agentmemory, SimpleMem, OMEGA, memsearch |
