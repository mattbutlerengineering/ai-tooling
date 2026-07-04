# Evaluation: weave (Ataraxy Labs)

**Repo:** [Ataraxy-Labs/weave](https://github.com/Ataraxy-Labs/weave)
**Stars:** 1,185 | **Last updated:** 2026-06-13 (pushed) | **License:** Apache-2.0 | **Language:** Rust
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Dev Workflow — git merge conflict resolution
**Layer:** Tooling (git merge driver)

---

## What it does

weave is **an entity-level git merge driver** that "resolves merge conflicts that Git can't by understanding code structure via tree-sitter." The problem it targets: Git merges by comparing **lines**, so when two branches both add code to the same file — even to **completely different functions** — Git sees overlapping line ranges and declares a false conflict. weave parses the code structure (tree-sitter) and recognizes that edits to different entities don't actually conflict, resolving the false positives automatically. It's part of the **Ataraxy Labs** stack (siblings: **sem** = semantic version control [already cataloged], **inspect** = semantic code review, **opensessions** = tmux sidebar for coding agents).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No merge driver configured, no conflict resolved.

```bash
gh api repos/Ataraxy-Labs/weave --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 1185, Apache-2.0, pushed 2026-06-13
gh api repos/Ataraxy-Labs/weave/readme --jq '.content' | base64 -d | head -30               # entity-level merge, tree-sitter, false conflicts
```

## What worked

- **Targets a real, common annoyance — agent-relevant.** Parallel agent workflows (multiple worktrees/branches) generate exactly the "two branches touched the same file in different functions" merges that Git falsely flags. Structure-aware resolution removes a class of conflicts that are pure noise.
- **Right mechanism.** tree-sitter entity parsing to decide "different functions → no real conflict" is the correct, deterministic way to resolve these — not an LLM guess.
- **Installs as a git merge driver.** Slots into normal git plumbing (per-file driver), so it works with existing workflows rather than replacing them.
- **Coherent stack.** Pairs naturally with sem (entity diffs) — same entity-level philosophy applied to merge.
- **Rust, Apache-2.0, active.**

## What didn't work or surprised us

- **Scoped to false-positive conflicts.** It resolves conflicts Git *invents* (disjoint entities); genuine same-entity conflicts still need human/agent resolution. It reduces noise, not all conflicts — which is the honest, correct scope.
- **tree-sitter fidelity bounds it.** Resolution quality depends on the grammar correctly delimiting entities; unusual syntax/macros/generated code may degrade. Language coverage isn't verified here.
- **Young, single-vendor stack.** 1.2K stars; value compounds with the broader (early) Ataraxy suite, which is more buy-in.
- **Merge-driver trust.** Auto-resolving merges is high-trust by nature — you want confidence (and tests) that it never silently mis-merges true conflicts.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Removes false conflicts deterministically; must be trusted not to auto-resolve genuine ones (scoped to disjoint entities). |
| Speed | + | Eliminates manual resolution of noise conflicts — especially valuable in parallel-agent/worktree workflows. |
| Maintainability | + | Fewer spurious conflicts means smoother branch integration. |
| Safety | neutral | Auto-merge is high-trust; scoped to non-overlapping entities limits risk, but warrants verification. |
| Cost Efficiency | + (indirect) | Less human/agent time spent on conflicts Git shouldn't have raised. |

## Verdict

**CONDITIONAL** — weave is a focused, Apache-2.0, Rust **entity-level git merge driver** that uses tree-sitter to dissolve the false conflicts Git invents when two branches edit *different functions* in the same file. Adopt it especially in **parallel-agent / multi-worktree workflows**, where these noise conflicts are common, to cut manual resolution — it's deterministic and slots in as a standard git merge driver. It's CONDITIONAL because it's scoped (it removes false positives, not genuine same-entity conflicts), tree-sitter fidelity bounds it per language, and auto-merging is high-trust (verify it never mis-resolves real conflicts). It pairs naturally with its sibling **sem** (entity-level diffs) for an entity-centric git toolkit.

Compared to neighbors: **sem** gives entity-level diff/blame/impact (same stack); the **resolving-merge-conflicts** skill resolves conflicts via an agent reasoning over both sides; **worktrunk** isolates parallel work. weave's distinguishing pitch is **a deterministic, structure-aware git merge driver that auto-resolves false conflicts.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [weave](https://github.com/Ataraxy-Labs/weave) | tool | Entity-level git merge driver (Apache-2.0, Ataraxy Labs) — resolves false conflicts Git invents by understanding code structure via tree-sitter, so two branches editing different functions in the same file no longer collide | Git merges by line ranges and flags conflicts on edits to unrelated functions in one file; want structure-aware automatic resolution | sem, resolving-merge-conflicts (skill), worktrunk |
