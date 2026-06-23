# Evaluation: byterover-cli

**Repo:** [campfirein/byterover-cli](https://github.com/campfirein/byterover-cli)
**Stars:** ~4,900 | **Last updated:** 2026-06-17 | **License:** source-available (repo SPDX returns NOASSERTION); formerly Cipher
**Dev loop stage:** Reflect (Memory & Context)
**Layer:** Infrastructure

---

## What it does

A portable memory layer for autonomous coding agents — the renamed continuation of Cipher. ByteRover CLI (`brv`) gives AI coding agents persistent, structured memory that developers curate and share across tools and teammates.

Mechanically you run `brv` in any project directory to start an interactive REPL (a React/Ink TUI) powered by your choice of LLM. The agent understands your codebase through an "agentic map," can read/write files and execute code, and stores knowledge for future sessions. The differentiator is the **context tree**: project knowledge is organized into a tree with **git-like version control** — branch, commit, merge, and push/pull — and synced to the cloud so it's shareable across tools and teammates. It supports 20 LLM providers and 24 built-in agent tools (code exec, file ops, knowledge search, memory management), ships a web dashboard (`brv webui`) for curating/querying context, and has a review workflow to approve/reject pending curate operations. It's paper-backed (arXiv).

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented model (context tree + git-like versioning, REPL/TUI, 20 providers, 24 tools, web dashboard, approve/reject review). Confirmed the Cipher lineage and the cloud-sync/sharing story. License resolves to NOASSERTION via the API — it's source-available with a cloud component; pin terms before depending on it commercially. Not run on a live project, so condition-gated.

```bash
gh api repos/campfirein/byterover-cli --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/campfirein/byterover-cli/readme --jq '.content' | base64 -d
```

## What worked

- **Git-like, reviewable memory.** A versioned context tree with branch/commit/merge and an approve/reject review workflow makes memory inspectable and correctable — a strong answer to opaque vector memory.
- **Portable and shareable.** Cloud sync + cross-tool/teammate sharing targets the "memory is trapped in one tool" problem directly.
- **Provider-agnostic, tool-rich.** 20 LLM providers and 24 agent tools (incl. code exec and knowledge search) make it a capable standalone memory REPL, not just a store.

## What didn't work or surprised us

- **Cloud dependency for the headline feature.** Sync/sharing leans on the ByteRover cloud; fully-local use is narrower.
- **License ambiguity.** NOASSERTION + a hosted component means you should confirm terms before commercial reliance.
- **Crowded memory space.** Overlaps ACE, Acontext, claude-mem, memU, supermemory; the edge is the git-like versioned context tree with explicit review.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Reviewed, curated context reduces acting on stale/wrong memory |
| Speed | neutral | Curation/review adds steps; recall speeds future sessions |
| Maintainability | + | Versioned context tree (branch/commit/merge) is auditable |
| Safety | + | Approve/reject review gates what enters shared memory |
| Cost Efficiency | ✓/$ | CLI usable free; cloud sync/sharing is a hosted feature |

## Verdict

**CONDITIONAL**

Adopt when a team wants shared, versioned, reviewable project memory that travels across coding agents and teammates — the git-for-context model is its standout. Confirm the license terms and weigh the cloud dependency for the sharing features. For a solo user already on claude-mem + OMEGA it overlaps existing memory; the draw is the git-like curation and cross-tool sharing.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [byterover-cli](https://github.com/campfirein/byterover-cli) | tool | Portable memory layer for coding agents (formerly Cipher, paper-backed) — `brv` REPL curating project knowledge into a git-like context tree (branch/commit/merge/push/pull), cloud-synced and shareable; 20 LLM providers, 24 tools, web dashboard, approve/reject review | Agent memory is per-tool and opaque; want versioned, reviewable, shareable project context across agents and teammates | ACE, Acontext, claude-mem, memU, supermemory |
