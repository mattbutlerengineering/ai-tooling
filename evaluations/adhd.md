# Evaluation: adhd

**Repo:** [UditAkhourii/adhd](https://github.com/UditAkhourii/adhd)
**Stars:** 852 | **Last updated:** 2026-06-04 (pushed; created 2026-05-25) | **License:** MIT
**Dev loop stage:** Inner-loop **Plan / Architect** — a divergent-ideation skill you invoke at a decision point (architecture, API surface, naming, fuzzy-bug hypothesis generation) to widen the option space *before* committing to an approach. Not an implement/verify/ship tool.
**Layer:** Process (a single `SKILL.md` prompt-program that orchestrates parallel `Agent`/`Task` calls), with an optional standalone Node CLI (`adhd-agent` on npm) that reimplements the same loop outside an agent harness.

---

## What it does

Despite the ambiguous name, **adhd is squarely in scope** for a software-dev catalog. It is a brainstorming/ideation skill for coding agents — the README subtitle: "An architectural fix for premature convergence in autoregressive reasoning." The thesis: linear Chain-of-Thought anchors on its first answer, and Tree-of-Thought widens the search but still walks one shared context, so the anchoring persists. ADHD instead spawns **N isolated reasoning branches under deliberately distorted "cognitive frames"** (hardware engineer, regulator/auditor, biology, speedrunner, "10-year-old", "$0 budget", etc., defined in `src/frames.ts`), with **zero shared context during divergence**, then runs a **separate critic pass** to score, cluster, prune "traps," and deepen the survivors.

The mechanism is a strict two-phase loop in `skills/adhd/SKILL.md`: **Phase 1 Diverge** spawns ~5 parallel Agent calls (one per frame), each told "you are a generator, not a critic… the first three obvious answers are banned… push past them into the awkward middle," emitting a JSON array of ideas; **Phase 2 Converge** scores breadth/novelty/traps and deepens the top survivors. A documented **pre-flight gate** is the strongest design choice: the skill is expensive (~10 Agent calls, 30–90s, 5–10× a single answer), so it self-judges open-endedness / stakes / phrasing and **aborts to a direct answer** for closed or canonical questions. The repo also ships a real TypeScript implementation (`src/`: engine, frames, llm, render, cli) and an eval harness (`bench/` + `EVALS.md`).

## How we tested it

**Source-grounded inspection — not installed, not run.** I did not run `npx skills add`, did not invoke `/adhd`, and did not execute the `bench/run-evals.ts` harness. Every claim comes from the repository (GitHub metadata, README, recursive file tree, `skills/adhd/SKILL.md`, `src/frames.ts`, `bench/problems.json`, `EVALS.md`, `.github/workflows/ci.yml`, commit/release counts) — not from observed ideation. **The headline eval numbers below are the author's self-reported, single-run figures, not anything I reproduced.**

```bash
gh api repos/UditAkhourii/adhd --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id}'
gh api repos/UditAkhourii/adhd/readme --jq '.content' | base64 -d           # thesis, adopters, The New Stack feature
gh api "repos/UditAkhourii/adhd/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/UditAkhourii/adhd/contents/skills/adhd/SKILL.md --jq '.content' | base64 -d  # 2-phase loop + pre-flight gate
gh api repos/UditAkhourii/adhd/contents/src/frames.ts --jq '.content' | base64 -d         # cognitive-frame definitions
gh api repos/UditAkhourii/adhd/contents/EVALS.md --jq '.content' | base64 -d              # self-reported 6-problem evals
gh api repos/UditAkhourii/adhd/contents/.github/workflows/ci.yml --jq '.content' | base64 -d  # typecheck/build/CLI-smoke on Node 18/20/22
gh api repos/UditAkhourii/adhd/commits --jq 'length'    # 30 (page-1 cap)
gh api repos/UditAkhourii/adhd/releases --jq 'length'   # 1 tagged release
```

## What worked

- **Names a real failure mode and attacks it architecturally.** Premature convergence / first-answer anchoring is a genuine LLM weakness, and the isolation-during-divergence insight (don't let branches see each other or they re-anchor) is a sharper framing than generic "brainstorm 10 ideas" prompts.
- **The pre-flight gate is the standout.** Most ideation tools fire on everything; ADHD explicitly self-judges and **aborts to a direct answer** for canonical/closed/low-stakes prompts (it even keys off words like "quick", "standard", "textbook"). For a skill that costs 5–10× a normal answer, building in cost-awareness is exactly right and rare.
- **Actually engineered, not just a prompt.** Real TypeScript source (typed `Frame` model, engine/critic/render split), a `bench/` eval harness with an LLM judge, an `EVALS.md` with per-problem verdicts, and CI that typechecks/builds and smoke-tests the CLI across Node 18/20/22. The single-line YAML description is deliberately ≤600 chars to survive Codex truncation — careful cross-harness packaging.
- **Independent traction.** The README lists multiple external projects shipping or porting it (repowire PR #313, mstack, zk-flow-oss, nix-skills) with MIT attribution, plus a critical research review (testdouble/han) tracked openly as issues — signals of real third-party use, not just stars.
- **Trap detection is the genuinely differentiating output.** Across the self-reported evals, the largest, most consistent edge is "trap detection" (naming attractive-but-dead-end ideas with a reason) — arguably more valuable to a builder than the novel ideas themselves.

## What didn't work or surprised us

- **Evals are self-reported, single-run, and self-judged.** `EVALS.md` shows ADHD winning 5/6 with large deltas, but it is one run, scored by an LLM judge the same author configured, on 6 hand-picked problems. The numbers are suggestive, not validated — and on the one problem ADHD lost (`llm-hang-cli`), the judge itself notes ADHD's pick "requires weeks of R&D" while the baseline was immediately shippable, i.e. ideation breadth can actively trade against actionability.
- **Expensive by construction.** ~10 Agent calls and 30–90s per invocation, 5–10× the cost of a direct answer. The pre-flight gate mitigates misuse but the tool is fundamentally a "spend more to think wider" trade — wrong for most day-to-day prompts.
- **Branding/marketing-forward README.** The "ADHD" name is an attention play (the README leans on a New Stack feature, a Tally community signup, an X handle, and a preprint link). The method is sound, but the packaging is louder than a 25-day-old, single-author skill warrants — discount the framing, read the SKILL.md.
- **Cognitive frames are evocative, not validated.** Frames like "10-year-old" or "$0 budget" plausibly shake the model out of ruts, but there's no ablation showing *which* frames move outcomes; frame selection is heuristic ("bias toward engineering tags, always include one wild").
- **Single-author, very young.** 1 release, 30 commits, created 2026-05-25. Real momentum, but unproven over time.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (for decisions) | Widens the option space and flags traps before you commit to a design/API/naming/hypothesis — its self-reported edge is largest on breadth and trap detection. No effect on code correctness directly; it operates before code. |
| Speed | − | Slower at the point of use by design (30–90s, ~10 calls). May save time downstream by avoiding dead-end designs, but the per-invocation cost is real. |
| Maintainability | + / neutral | A better-explored architecture/API decision up front can reduce later rework; no direct effect on an existing codebase. |
| Safety | neutral | Pure ideation; generates text, executes no project code. The optional npm CLI calls an LLM API directly — standard key-handling caveats, nothing host-reaching. |
| Cost Efficiency | − | Explicitly 5–10× a single answer. The pre-flight abort gate is the saving grace, scoping the spend to genuinely open, high-stakes prompts. |

## Verdict

**CONDITIONAL — keep in the catalog; reach for it only at real decision points.** adhd is a legitimate, well-engineered Plan-stage ideation skill, not the ambiguity its name suggests — it belongs in a dev catalog. It names a real failure mode (first-answer anchoring), attacks it with a defensible mechanism (isolated divergence + separate critic), and is unusually disciplined for the genre (pre-flight cost gate, real TS source, CI, an eval harness, third-party adopters). The reasons to gate adoption: the evals are self-reported single-run and self-judged, it costs 5–10× per use, and breadth can trade against shippability (its one eval loss). Use it deliberately for architecture, public API surface, naming, and fuzzy-bug hypothesis generation — and let the pre-flight gate veto it for everything else.

Compared to neighbors: its catalog overlaps (**sequential-thinking**, **planning-with-files**) are *linear/structured* reasoning aids; adhd is their opposite — deliberately *parallel and divergent*, explicitly designed to defeat the single-context anchoring those approaches share. Versus **superpowers:brainstorming** (a conversational intent-exploration skill), adhd is more mechanical and more expensive: it spends real compute to fan out under frames and prune, where brainstorming explores requirements in-dialogue. They compose — brainstorm to frame the problem, ADHD to widen the solution space once the problem is open and the stakes justify the cost.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [adhd](https://github.com/UditAkhourii/adhd) | skill | Parallel divergent ideation: spawns N isolated reasoning branches under distorted cognitive frames, then a critic pass scores, clusters, and prunes traps; with a cost-aware pre-flight gate | Linear/tree reasoning anchors on its first answer; need a wider, trap-aware option space at architecture / API / naming / fuzzy-bug decision points | sequential-thinking, planning-with-files; superpowers:brainstorming (intent vs. solution divergence) |
