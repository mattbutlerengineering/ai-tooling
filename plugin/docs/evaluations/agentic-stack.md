# Evaluation: agentic-stack

**Repo:** [codejunkie99/agentic-stack](https://github.com/codejunkie99/agentic-stack)
**Stars:** 2,117 | **Last updated:** 2026-05-25 | **License:** Apache-2.0
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A portable `.agent/` folder — memory + skills + protocols — that installs into 12 coding-agent harnesses (Claude Code, Cursor, Windsurf, OpenCode, OpenClaw, GitHub Copilot CLI, Gemini CLI, Hermes, Pi, Codex, Antigravity, or a DIY Python loop) via one Homebrew-distributed CLI, and keeps the same brain when you switch tools. Its tagline is "one brain, many harnesses."

The mechanism: `agentic-stack <harness>` (or `./install.sh <harness>`) drops a `.agent/` skeleton into a project plus a thin per-harness adapter shim (the Claude Code adapter writes `CLAUDE.md` + `.claude/settings.json` hooks). Memory is four explicit layers — `working/`, `episodic/`, `semantic/`, `personal/` — each with its own retention policy. The loop is a *staging-then-review* design rather than auto-graduation: skills log every action to episodic memory; a nightly `auto_dream.py` cycle mechanically clusters recurring patterns into **candidate** lessons (no LLM call, no network, no git — "cluster, stage, prefilter, decay" only); the **host agent** then reviews candidates in-session via CLI tools (`list_candidates.py`, `graduate.py --rationale`, `reject.py --reason`, `reopen.py`, `retract_lesson.py`) where accept/reject requires a written rationale and is logged append-only. Graduated lessons land in `semantic/lessons.jsonl` (source of truth) rendered to `LESSONS.md`, and future sessions load query-relevant accepted lessons automatically (salience × relevance retrieval). It ships nine seed skills (skillforge, memory-manager, git-proxy, debug-investigator, deploy-checklist, design-md, data-layer, data-flywheel, tldraw, plus a v0.18 `brain` bridge skill), a permissions hook that enforces `protocols/permissions.md`, an opt-in FTS5 memory search (`[BETA]`, falls back to ripgrep then grep), a local-only cross-harness monitoring "data layer" (dashboard.html / daily-report.md / token-cost estimates), and a local "data flywheel" exporter that turns approved redacted runs into trace records / eval cases / training-ready JSONL without training a model or sending telemetry. As of v0.18.0 it can optionally bridge to the author's separate [`codejunkie99/brain`](https://github.com/codejunkie99/brain) git-backed long-term memory binary for cross-project recall.

## How we tested it

Architecture review via the GitHub API — read the full README, the v0.1→v0.18 release/changelog history, the documented `.agent/` repo layout, the supported-harness + hook-support matrix, the seed-skill list, and the actual Claude Code adapter `settings.json` to verify how hooks are wired. **Did not install or run hands-on.** Rationale matches every prior memory-category eval (claude-mem ADOPT, memsearch / agentmemory / SimpleMem all CONDITIONAL): the user already runs claude-mem + OMEGA as the live memory stack, and agentic-stack installs its own `.claude/settings.json` PostToolUse + Stop hooks and a `CLAUDE.md` — dropping that into the working setup risks hook/instruction collisions with the existing claude-mem, superpowers, claude-reflect, and OMEGA wiring. The repo was also UNLINKED in the catalog; the first step was to verify identity.

```bash
gh search repos agentic-stack --limit 20 --json fullName,description,stargazersCount,url   # disambiguate the name
gh api repos/codejunkie99/agentic-stack --jq '{stars:.stargazers_count,license:.license.spdx_id,description,pushed_at,created_at,open_issues,forks:.forks_count}'
gh api repos/codejunkie99/agentic-stack/readme --jq '.content' | base64 -d
gh api repos/codejunkie99/agentic-stack/releases --jq '.[].tag_name'            # v0.18.0 latest, ~24 releases
gh api repos/codejunkie99/agentic-stack/contributors --jq 'length'             # 14 contributors
gh api repos/codejunkie99/agentic-stack/contents/adapters/claude-code/settings.json --jq '.content' | base64 -d
```

**Repo identity confirmed.** `gh search repos agentic-stack` returns many unrelated "agentic stack" projects (Llama Stack apps, UI-TARS, CopilotKit, Mastra, ClickHouse's data stack, an `i-am-bee` "Agent Stack" template). The only one matching the catalog's Memory & Context framing — a portable agent memory/skills layer — is `codejunkie99/agentic-stack` (2.1K stars, Apache-2.0, 257 forks, 14 contributors, Homebrew-distributed). This is the correct repo; the catalog entry should be linked to it.

## What worked

- **Cross-harness portability is the genuine, distinctive value — and the widest in the category.** 12 harnesses from one `.agent/` brain (vs memsearch's 4). A `transfer` wizard exports preferences + accepted lessons + skills + working/episodic memory as a SHA-256-verified curl bundle to re-import into a different harness. For someone who actually switches between Claude Code, Cursor, Codex, etc., this is real, unique utility.
- **Staging-then-human-review is a deliberate, safety-forward memory design.** `auto_dream.py` only *stages* candidates — it performs "no git commits, no network, no reasoning," explicitly safe to cron unattended. Nothing enters semantic memory without a host-agent `graduate.py --rationale`. This separates mechanical clustering from judgment and keeps an append-only audit trail (rejected candidates retain decision history; lessons can be `retract`ed with rationale). It is a more conservative, auditable model than the auto-summarize-everything peers.
- **Markdown/JSONL as source of truth, fully git-versionable.** `lessons.jsonl` is the source; `LESSONS.md` is rendered; `git log .agent/memory/` is "the agent's autobiography." Same human-readable, no-DB-lock-in philosophy that earned claude-mem/memsearch/agentmemory praise — and here with *no vector DB at all* by default (FTS5/ripgrep keyword search is the only index, and it's opt-in beta).
- **Zero external DB and zero API key on the default path.** No vector database, no embedding model, no LLM key required to run the core loop — clustering is mechanical, search is FTS5/ripgrep. This is even lighter than memsearch (Milvus Lite + ONNX) and a hard contrast with SimpleMem (mandatory OpenAI-compatible key). Strong local-first / cost story.
- **Lean, well-scoped Claude Code hook surface.** Verified in the adapter: only **2 hooks** — PostToolUse (logging, scoped to Bash/Edit/Write/Task/TodoWrite) and Stop (auto_dream staging) — both `$CLAUDE_PROJECT_DIR`-anchored, plus a `permissions.deny` block (`git push --force`, `rm -rf /`). Fewer hook slots than agentmemory's 12; lower collision risk.
- **Unusually mature engineering for a 2-month-old solo-origin project.** ~24 releases (v0.1→v0.18), Homebrew formula, Windows PowerShell installer with concurrent-write locking (fcntl/msvcrt), manifest-driven adapter system, safe `upgrade --dry-run` / `sync-manifest` that won't clobber user memory, a `doctor` audit, hook-validation test suites (`test_claude_code_hook.py` 54 checks, `verify_codex_fixes.py` 33 checks), and progressive-disclosure skills (lightweight manifest always loads, full SKILL.md only on trigger match).
- **Genuinely additive features beyond memory** — a local-only cross-harness monitoring data layer (dashboards, token/cost estimates, cron timelines) and a local data-flywheel exporter (traces/evals/training-JSONL, no telemetry). Neither claude-mem nor the other CONDITIONALs offer fleet-level monitoring across harnesses.

## What didn't work or surprised us

- **It overlaps claude-mem on the core job (auto-capture → reflect → recall) without beating it for a Claude Code-only user.** For someone who lives in one harness, the portability that justifies agentic-stack is unused, and claude-mem is more battle-tested in the Claude Code ecosystem with a richer MCP/search surface. The unique axis (12-harness portability) only pays off if you actually switch harnesses — same shape as the memsearch verdict.
- **Capture is less automatic than the auto-summarizing peers.** Lessons require an explicit host-agent review step (`graduate.py --rationale`) — by design, but it means the brain doesn't compound passively; you must do the in-session review or candidates just accumulate. claude-mem/memsearch summarize-and-store with no manual graduation gate. This is a maintainability/effort tradeoff, not a defect.
- **Pre-1.0 and young.** Created Apr 2026, latest v0.18.0, still v0.x — fast-moving (the changelog shows frequent format/path changes, a Python 3.9 crash fix, timezone-drift sweeps) and not yet API-stable. claude-mem is far more proven.
- **Single-author origin with a self-promotion thread.** Built by one developer (@AV1DLIVE), "coded using Minimax-M2.7," based on the author's own X article. 14 contributors and 257 forks show real traction, but the bus factor and the v0.18 pivot to bridging the author's *separate* `brain` product are worth noting (the Brain bridge is optional, not lock-in).
- **Breadth risks dilution.** Memory + skills + protocols + 12 adapters + data layer + data flywheel + tldraw canvas + Mission Control web dashboard + Brain bridge is a lot of surface for a 2-month-old project; some pieces (tldraw, FTS search, Mission Control) are explicitly beta/opt-in. The core memory loop is the solid part; the periphery is less proven.
- **No published retrieval benchmarks.** Unlike agentmemory (LongMemEval-S R@5) or SimpleMem (LoCoMo F1), agentic-stack ships no quantified recall numbers — recall quality can't be verified from sources, only the design.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Query-relevant accepted lessons (salience × relevance) surface past decisions into future sessions; but recall is keyword/FTS-based with no published benchmark, and capture depends on manual graduation |
| Speed | neutral | Mechanical nightly clustering and FTS/ripgrep search are fast and add no per-turn LLM cost; but the human review step is manual effort, not throughput |
| Maintainability | + | Markdown/JSONL source of truth, git-versionable, no DB lock-in, safe `upgrade --dry-run` that preserves user memory; offset by pre-1.0 churn and a large feature surface |
| Safety | + | Staging-only unattended cycle (no network/reasoning/commits), permissions-enforcement hook with deny rules, secret-blocking transfer wizard, append-only audited accept/reject/retract, fully local-first |
| Cost Efficiency | + | Zero vector DB, zero embedding model, zero LLM key on the default path; mechanical clustering means no per-turn token cost — the lightest-cost memory tool evaluated so far |

## Verdict

**CONDITIONAL**

agentic-stack is a credible, well-engineered, local-first portable memory-and-skills layer whose real, unique value is the **widest cross-harness portability in the category** (12 harnesses, one git-versionable `.agent/` brain, a SHA-256-verified transfer wizard) combined with a deliberately **safety-forward staging-then-human-review** memory model and a genuinely additive **local cross-harness monitoring + data-flywheel** layer that no other catalog memory entry offers. It is **not** a thin duplicate of memsearch/agentmemory/SimpleMem — it attacks portability + auditable human-in-the-loop curation + fleet monitoring rather than competing on hybrid-search recall, and it does so with *no DB and no API key* on the default path, the lightest footprint of any memory tool evaluated. Use it when you actually work across multiple coding-agent harnesses and want one portable, auditable brain plus local fleet monitoring — that is its real differentiator. For this user's case (Claude Code-only, already on claude-mem ADOPT + OMEGA), it does **not** displace claude-mem: the portability is unused in a single-harness setup, claude-mem is more battle-tested with a richer Claude Code recall surface, and agentic-stack's manual-graduation capture is more effort than claude-mem's passive auto-capture. Like memsearch, agentmemory, and SimpleMem (all CONDITIONAL), it wins on a specific axis (cross-harness portability + auditable curation + monitoring) but loses to claude-mem on single-harness ecosystem fit and zero-effort capture. KEEP the catalog entry (now linked to the verified repo); do not adopt over claude-mem.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentic-stack](https://github.com/codejunkie99/agentic-stack) | tool | Portable `.agent/` brain (4-layer memory + skills + protocols) that installs into 12 coding-agent harnesses and survives tool switches | Switching coding agents resets your memory/skills; need one portable, auditable, local-first brain across harnesses | claude-mem, memsearch, agentmemory, SimpleMem, OMEGA, mem0 |
