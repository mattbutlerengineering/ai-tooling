# Evaluation: pro-workflow

**Repo:** [rohitg00/pro-workflow](https://github.com/rohitg00/pro-workflow)
**Stars:** 2,322 | **Last updated:** 2026-06-15 | **License:** MIT
**Dev loop stage:** Reflect (primary); spills into Plan, Implement, Review, Ship
**Layer:** Process + Tooling (Claude Code plugin)

---

## What it does

A Claude Code plugin (also cross-agent via SkillKit) marketed as "self-correcting memory that compounds over 50+ sessions." It bundles 34 skills, 8 agents, 22 commands, and 37 hook scripts across 24 events on top of a single local SQLite store (`~/.pro-workflow/data.db`, `better-sqlite3`).

The self-correction mechanism, traced through the actual hook scripts:

1. **Capture.** A `Stop` hook (`learn-capture.js`) scans the assistant's response for `[LEARN] Category: rule / Mistake: / Correction: / Wiki: <slug>` blocks via regex and writes structured rows to SQLite via `store.addLearning(...)`. The `/learn-rule` command is the human-driven path that gets Claude to emit those blocks (propose rule -> you approve -> saved). There is no NLP inference of corrections — capture is literally a regex over an opt-in marker the model must emit.
2. **Recall.** A `SessionStart` hook (`session-start.js`) loads stored learnings (and lists registered wikis) into context; a `UserPromptSubmit` hook (`prompt-submit.js`) auto-injects top-3 wiki hits when a prompt matches the FTS5 index.
3. **Knowledge plane (v3.3).** Persistent on-disk research wikis indexed with SQLite FTS5 (BM25), optional vector embeddings + RRF hybrid retrieval (needs `OPENAI_API_KEY`/`VOYAGE_API_KEY`), a budget-capped auto-research BFS loop (`/wiki research`, kill-switch via `touch ~/.pro-workflow/STOP`), a provider-agnostic multi-LLM "council," and a single-file HTML wiki viewer.
4. **Quality gates.** Deterministic `PreToolUse(Bash)` git guards (commit-validate, blast-radius, pre-push), regex `secret-scan.js` on Edit/Write, plus optional LLM-powered (`type: "prompt"`) gates, cost tracking, MCP-overhead auditing, compaction-aware state preservation.

Note the build-step caveat: the SQLite components require `npm install && npm run build` to produce `dist/db/store.js`; the hook scripts no-op (`getStore()` returns null) if that build is missing, which several marketplaces skip. `/doctor` reports `KB: missing` in that state.

## How we tested it

Architecture review only. **Did not install or run hands-on** — the user already runs claude-mem (ADOPT) + OMEGA as their hook-based memory layer, and installing a third hook-heavy memory plugin into the live setup risks exactly the hook-slot contention this evaluation is meant to assess. Method: inspected the GitHub repo metadata, full README, the recursive file tree, the plugin manifest, `hooks/hooks.json`, and the actual source of the memory-critical hook scripts (`learn-capture.js`, `session-start.js`). Cross-checked the user's live hook configuration in `~/.claude/settings.json` to map real collision risk. Calibrated against the sibling evals `agentmemory.md` (CONDITIONAL — same author, rohitg00) and `memsearch.md` (CONDITIONAL), both judged against claude-mem (ADOPT, the user's choice).

```bash
gh api repos/rohitg00/pro-workflow --jq '{stars,license,description,pushed_at,created_at}'
gh api repos/rohitg00/pro-workflow/readme --jq '.content' | base64 -d
gh api "repos/rohitg00/pro-workflow/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/rohitg00/pro-workflow/tags --jq '.[].name'          # v3.3.0 latest, package.json at 3.4.0
gh api repos/rohitg00/pro-workflow/contributors --jq 'length'    # 4
gh api repos/rohitg00/pro-workflow/contents/hooks/hooks.json --jq '.content' | base64 -d
gh api repos/rohitg00/pro-workflow/contents/scripts/learn-capture.js --jq '.content' | base64 -d
gh api repos/rohitg00/pro-workflow/contents/scripts/session-start.js --jq '.content' | base64 -d
# user's live hooks:
python3 -c "import json; ... json.load(open('~/.claude/settings.json'))['hooks']"
```

Reviewed: 24 hook events / 37 scripts, the regex-based `[LEARN]` capture path, SQLite/FTS5 storage schema, the v3.3 knowledge-plane skills, license (MIT), maturity (4 contributors, 9 tagged releases, no LICENSE detected by `gh` despite MIT badge — `license: null` in the API).

## What worked

- **Markdown/SQLite-on-disk, human-inspectable store.** Learnings and wikis live in `~/.pro-workflow/` with project-scope wikis committable at `<project>/.claude/wikis/`. SQLite is rebuildable and the wiki viewer is a shareable single HTML file. Same sound "your data is yours" philosophy as claude-mem and memsearch.
- **Breadth as a workflow bundle, not just memory.** Beyond memory it ships genuinely useful process pieces: deterministic git/secret quality gates, MCP token-overhead auditing, cost tracking, compaction-aware state, permission-denial analysis, parallel-worktree orchestration. As a *workflow* package it overlaps superpowers/everything-claude-code more than it overlaps a pure memory tool.
- **Budget-capped auto-research with a kill switch.** The `/wiki research` BFS loop is explicitly cost-bounded (`--budget-usd`, `--max-pages`) and has a global `STOP` file — responsible defaults for an autonomous loop.
- **Transparent, debuggable capture.** The `[LEARN]` regex path is simple and auditable — you can see exactly what gets stored and why. No opaque "confidence scoring" black box (a critique that applied to agentmemory).
- **Honest about its own rough edges.** README documents the `npm run build` requirement, the `KB: missing` failure mode, and the `--force` SkillKit security-scanner false positives. That candor is a positive maturity signal.

## What didn't work or surprised us

- **Direct hook-slot contention with the user's live OMEGA setup.** The user's `~/.claude/settings.json` already binds OMEGA to `SessionStart`, `PostToolUse(Edit|Write|NotebookEdit|Bash|Read)`, and `Stop` (assistant_capture + session_stop), plus GSD hooks on SessionStart/PostToolUse, plus claude-mem injecting observations on `PreToolUse:Read` (visible in this very session). pro-workflow claims **24 hook events / 37 scripts** and binds the same memory-critical slots: its own `Stop` learn-capture, `SessionStart` learnings load, `UserPromptSubmit` wiki injection, `PreToolUse(Edit/Write)` quality+secret gates, `PreToolUse(Read)` re-read tracking. Two independent capture systems firing on `Stop` and two context injectors on `SessionStart`/`UserPromptSubmit` means duplicated capture, doubled latency, and context-budget competition — not a clean coexistence.
- **"Self-correcting" is opt-in marker capture, not inference.** Capture only fires when the model emits a `[LEARN]` block, which the human prompts via `/learn-rule`. This is closer to a structured `/remember` than to autonomous learning-from-corrections. OMEGA's `assistant_capture` and claude-mem's auto-observation cover the same ground with less ceremony and already run for this user.
- **Memory recall is BM25/FTS5 + optional embeddings — no edge over the incumbents.** claude-mem and agentmemory both deliver hybrid recall from SQLite + *local* embeddings with no API key; pro-workflow's hybrid retrieval requires `OPENAI_API_KEY`/`VOYAGE_API_KEY`. On the core memory axis it does not beat the ADOPTED tool.
- **Maturity is modest for the surface area.** 2.3K stars, 4 contributors, created Feb 2026, still v3.x-but-pre-mature; the API even reports `license: null` despite an MIT badge. 37 hook scripts + a TS build step + a SQLite engine from a 4-person project is a large, young attack/maintenance surface to graft onto a working setup. Compare claude-mem's mature ecosystem and agentmemory's 1,400+ tests.
- **Heavy footprint to get one feature.** The novel piece relative to the incumbents is the *knowledge-plane wikis + auto-research loop*, but adopting it pulls in the entire 34-skill / 8-agent / 24-event bundle, much of which duplicates tools the user already has (orchestrate/agent-teams vs the user's GSD + agent stack; quality gates vs existing hooks).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Self-correction rules + FTS5 recall surface past decisions; but no published benchmark and no edge over claude-mem/agentmemory on recall |
| Speed | - | 37 hook scripts across 24 events add per-event latency; stacked on top of OMEGA's Stop/PostToolUse/SessionStart hooks this compounds |
| Maintainability | - | TS build step (`dist/db/store.js`) is a silent-failure mode; 4 contributors, young project, large surface to maintain alongside two existing memory systems |
| Safety | neutral | Local-first SQLite, deterministic secret/git guards, budget caps + STOP kill-switch are good; but more hooks = more execution surface, and SkillKit needs `--force` past its own scanner |
| Cost Efficiency | neutral | Budget-capped research loop and cost-tracker are pluses; hybrid retrieval needs a paid embedding key; auto-research and LLM gates are net new token spend |

## Verdict

**SKIP** (for this user — KEEP the catalog entry)

pro-workflow is a credible, honestly-documented workflow bundle, and its knowledge-plane wikis + budget-capped auto-research loop are a genuinely novel layer that neither claude-mem nor OMEGA offers. But for **this** user it should not be adopted: its headline "self-correcting memory" is regex-based opt-in `[LEARN]` capture plus BM25 recall, which is strictly covered — with less ceremony and local embeddings — by the user's existing claude-mem (ADOPT) and OMEGA stack. Worse, it directly contends for the same hook slots OMEGA and claude-mem already own (`SessionStart`, `Stop`, `PostToolUse`, `UserPromptSubmit`, `PreToolUse:Read/Write`), so installing it means two capture systems and two context injectors fighting over the same events — duplicated work, added latency, and context-budget competition. The wiki/auto-research feature is the only thing that would justify revisiting, and it doesn't warrant grafting a 37-hook / TS-build / 4-contributor bundle onto a working setup to get it. Same family verdict as the sibling memory tools (agentmemory CONDITIONAL, memsearch CONDITIONAL): a good tool that loses to the incumbents on Claude Code fit — but here the hook-slot conflict pushes it past CONDITIONAL to SKIP for the user's specific configuration. A greenfield user with **no** existing memory layer could reasonably treat it as CONDITIONAL.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pro-workflow](https://github.com/rohitg00/pro-workflow) | plugin | Claude Code learns from your corrections: self-correcting memory that compounds over 50+ sessions (2.3K stars) | Agents repeat the same mistakes; corrections don't persist or compound | claude-mem, OMEGA, agentmemory, memsearch, superpowers, everything-claude-code |
