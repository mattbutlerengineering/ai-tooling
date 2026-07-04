# Evaluation: LazyCodex

**Repo:** [code-yeongyu/lazycodex](https://github.com/code-yeongyu/lazycodex)
**Stars:** 1,517 | **Last updated:** 2026-06-20 (pushed; created 2026-05-25) | **License:** MIT | **Install:** `npx lazycodex-ai install`
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (agent harness layered onto Codex)
**Layer:** Harness (skill/discipline pack for Codex)

---

## What it does

LazyCodex is **an agent harness for complex codebases that runs inside Codex** — adding **project memory, planning, execution, and verified completion** to OpenAI's Codex. It's explicitly the **Codex-targeted port of the "OmO" quality bar** (Sisyphus Labs' oh-my-* family — `oh-my-openagent` / `oh-my-claudecode`, by the same author code-yeongyu): "If you wanted OmO but did not want the setup ceremony, start here." One-line install: `npx lazycodex-ai install`.

The pitch is bringing a quality-obsessed, structured harness (memory → plan → execute → verify) to Codex, which ships with a leaner default workflow.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No install performed, no Codex session run. Behavior comes from the README and the known OmO lineage, not observed usage. "OmO quality bar" / "token burner" framing is the project's own.

```bash
gh api repos/code-yeongyu/lazycodex --jq '{stars,license:.license.spdx_id,created:.created_at,pushed:.pushed_at}'   # 1.5K, MIT
gh api repos/code-yeongyu/lazycodex/readme --jq '.content' | base64 -d | head -25   # OmO-for-Codex, memory/planning/execution/verified-completion, npx install
```

## What worked

- **Right disciplines, right host.** Project memory + planning + **verified completion** is exactly the structure that curbs agent drift and over-claiming; bringing it to Codex (which is leaner by default) fills a real gap.
- **Credible lineage.** Same author as the cataloged oh-my-openagent and the OmO family — a known, quality-focused harness pedigree rather than a random pack.
- **One-line install** (`npx lazycodex-ai install`) lowers the "OmO setup ceremony" barrier the README calls out.
- **MIT, popular fast** (~1.5K stars in weeks), actively pushed.

## What didn't work or surprised us

- **Codex-specific.** It's built for Codex; Claude Code users are served by the sibling oh-my-claudecode. Useful precisely if Codex is your harness.
- **OmO's "token burner" reputation.** The lineage is openly described as quality-via-heavy-token-use ("terrifying token burner") — expect high token spend in exchange for thoroughness; weigh against cost budgets.
- **Overlaps its own family.** It's the Codex member of the oh-my-* set, so the choice is host-driven (Codex vs. Claude Code), not a new capability.
- **Young; claims unverified.** The "verified completion" quality is the valuable part and isn't validated here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Memory + planning + verified-completion discipline reduces drift and over-claimed "done" inside Codex. |
| Speed | neutral / − | Structure adds steps; OmO lineage trades speed/tokens for thoroughness. |
| Maintainability | + | Project memory and planning give complex-codebase work more continuity and structure. |
| Safety | + / neutral | Verified-completion gating reduces unverified changes shipping. |
| Cost Efficiency | − | OmO-style harnesses are openly token-heavy ("token burner") — quality at a cost. |

## Verdict

**CONDITIONAL** — LazyCodex brings the **OmO quality bar — project memory, planning, execution, and verified completion — to Codex**, MIT-licensed with a one-line install, from the credible oh-my-* author. Adopt it if Codex is your harness and you want structured, drift-resistant workflows on complex codebases without the OmO setup ceremony. The main trade-off is cost: the OmO lineage is openly a "token burner," exchanging spend for thoroughness — fine for high-stakes work, expensive for routine tasks. If you're on Claude Code, use the sibling oh-my-claudecode instead; the choice here is host-driven.

Compared to neighbors: **oh-my-openagent** and **oh-my-claudecode** are the same family for other hosts; **codex-plugin-cc** bridges Codex and Claude Code config. LazyCodex's distinguishing pitch is **OmO-grade memory/planning/verified-completion specifically inside Codex**, one-line installed.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lazycodex](https://github.com/code-yeongyu/lazycodex) | harness | Agent harness for complex codebases inside Codex (MIT) — project memory, planning, execution, and verified completion; brings the OmO (oh-my-*) quality bar to Codex via `npx lazycodex-ai install` | Codex's lean default lacks structured project-memory/planning/verified-completion discipline for complex work | oh-my-openagent, oh-my-claudecode, codex-plugin-cc |
