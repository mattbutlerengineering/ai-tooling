# Evaluation: skillopt

**Repo:** [microsoft/SkillOpt](https://github.com/microsoft/SkillOpt)
**Stars:** 8,365 | **Last updated:** 2026-06-17 (pushed; created 2026-05-08) | **License:** MIT
**Dev loop stage:** Outer-loop **Reflect** — an offline optimization/training step that takes a seed skill plus a scored task set and iterates it into a better skill document. It is a learning loop *about* a skill, run between dev cycles, not a per-task inner-loop tool.
**Layer:** Tooling (a Python training framework — `pip install skillopt` — with a rollout/reflect/aggregate/select/update/evaluate engine, multi-backend model adapters, six benchmarks, and a Gradio WebUI; produces a `best_skill.md` artifact)

---

## What it does

SkillOpt **treats a skill document as the trainable state of a frozen agent** and optimizes it the way you'd train a network — epochs, (mini-)batch size, a textual "learning-rate" budget, and a validation gate — but in *text space*, touching no model weights. A separate optimizer model turns scored rollouts into bounded **add / delete / replace** edits on a single skill markdown; a candidate edit is accepted only if it *strictly improves a held-out validation score*. A rejected-edit buffer and an epoch-wise slow/meta update keep training stable. The deployed artifact is a compact `best_skill.md` (the README says typically 300–2,000 tokens) that runs against the unchanged target model, adding **zero inference-time model calls** at deployment.

This is a research release from Microsoft (arXiv 2605.23904, project page, demo video) with strong reported numbers: best-or-tied across all 52 evaluated (model, benchmark, harness) cells over six benchmarks, seven target models, and three harnesses (direct chat, Codex CLI, Claude Code CLI); on GPT-5.5 it lifts no-skill accuracy by +23.5 (direct chat), +24.8 (Codex loop), +19.1 (Claude Code), with skills transferring across model scales and to nearby benchmarks. The repo ships the full loop, multi-backend support (OpenAI/Azure/Claude/Qwen/MiniMax + Codex/Claude Code exec backends), six built-in envs (alfworld, docvqa, livemath, officeqa, searchqa, spreadsheetbench) each with a `dataloader.py`/`rollout.py`/`initial.md`, pre-trained `ckpt/*/gpt5.5_skill.md` checkpoints, a WebUI dashboard, templates for adding new backends/benchmarks, and a "SkillOpt-Sleep" preview for nightly offline self-evolution of local coding-agent skills.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Nothing was `pip install`ed; no training run, rollout, or evaluation was executed; no benchmark was reproduced. Every claim about accuracy lifts, token counts, and 52-cell dominance is the authors' README/paper framing, which I did **not** verify — I only confirmed the code, configs, benchmark envs, and example skill checkpoints exist. I did read one shipped artifact (`ckpt/searchqa/gpt5.5_skill.md`) to confirm the output shape: a short markdown file of learned answer-normalization rules, consistent with the "compact skill" claim.

```bash
gh api repos/microsoft/SkillOpt --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,lang:.language,issues:.open_issues_count}'
# {stars:8365, forks:813, pushed:2026-06-17, created:2026-05-08, MIT, Python, issues:17}
gh api repos/microsoft/SkillOpt/readme --jq '.content' | base64 -d | head -130
gh api "repos/microsoft/SkillOpt/git/trees/HEAD?recursive=1" --jq '.tree[].path'
#   skillopt/engine/trainer.py, skillopt/envs/{alfworld,docvqa,searchqa,...}/{rollout,reflect}.py, configs/, ckpt/*/gpt5.5_skill.md, skillopt_webui/, skillopt_sleep/
gh api repos/microsoft/SkillOpt/contents/ckpt/searchqa/gpt5.5_skill.md --jq '.content' | base64 -d | head -15   # short answer-normalization rules
gh api repos/microsoft/SkillOpt/releases --jq 'length'   # 1 release (v0.1.0, 2026-06-02)
```

## What worked

- **The core idea is the most principled thing in this category.** "Optimize skill text against a held-out validation gate, accept an edit only if it strictly improves the score" imports the one discipline that everyone else's skill authoring lacks. Versus hand-crafting (skill-creator) or scrape-and-synthesize (Skill Seekers), this is the only approach that *measures* improvement instead of asserting it.
- **Zero deployment-time overhead.** The trained skill is a static markdown file; all the optimizer cost is paid offline. The deployed agent makes no extra calls — the artifact is just better instructions. That's the right cost model for a Reflect-stage tool.
- **Reproducibility and credibility.** Microsoft authorship, arXiv paper with per-cell tables, six benchmarks with split manifests (train/val/test), shipped checkpoints, WebUI, and `_template/` scaffolding for new backends/benchmarks. The held-out-gate design directly addresses the reproducibility hole in "loosely controlled self-revision."
- **Harness-aware.** Backends for Codex CLI and Claude Code CLI mean skills are trained inside the same agentic loop they'll be deployed in, and the paper reports cross-harness transfer — a meaningful Maintainability signal (a skill survives a harness swap).
- **SkillOpt-Sleep** points at the genuinely interesting use case: nightly consolidation of validated skills from your own past coding sessions behind a held-out gate.

## What didn't work or surprised us

- **It's a research framework, not a drop-in dev tool.** Optimizing a skill requires a *scored task environment*: a dataset with train/val/test splits, a `rollout.py` that runs the agent, and a `reflect.py` that scores it. The six built-ins are academic benchmarks (alfworld, docvqa, searchqa…), not your codebase. Applying it to a real project means authoring a custom env + reward signal — substantial work most teams won't do.
- **Reported gains are on benchmark tasks with clean rewards.** "+23.5 points" is measured where success is objectively scorable. Software-dev skills (architecture taste, review judgment) lack such a reward, so the headline numbers may not transfer to the work this catalog cares about. Unverified by us regardless.
- **Optimizer cost is real and front-loaded.** Training = many rollouts × an optimizer model × epochs. For a one-off skill that's a lot of tokens before you deploy anything; it pays off only for skills used heavily and repeatedly.
- **Very young (created 2026-05-08, one v0.1.0 release).** Promising and active, but early; SkillOpt-Sleep is explicitly a preview.
- **The "train like a neural net" metaphor can mislead** — it sets an expectation of plug-and-play that the env/reward authoring requirement immediately breaks.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | The defining contribution: edits accepted only on strict held-out improvement, so a SkillOpt-trained skill is *measurably* better than its seed on the target task — strongest correctness story in the skill-authoring category. (Reported, not verified here.) |
| Speed | − / neutral | Slow to produce: many offline rollouts/epochs. No inner-loop speedup; the win is artifact quality, not iteration time. |
| Maintainability | + | A skill with a validation harness can be *re-trained* as tasks/models drift, and reported cross-harness/cross-scale transfer means it survives stack changes — turns skills into regression-tested, evolvable assets. |
| Safety | neutral | Pure text optimization; deployed artifact is static markdown, no runtime tool/host reach. Risk limited to a reward signal that optimizes the wrong thing. |
| Cost Efficiency | + / − | Zero deployment-time overhead (static skill) is excellent; offset by heavy offline training cost. Net-positive only for high-reuse skills. |

## Verdict

**DEFER — landmark approach, but it needs a scored task environment most dev teams don't have yet.** SkillOpt is the conceptually strongest entry in skill authoring: it's the only tool that *trains* a skill against a held-out validation gate instead of generating-and-hoping, with credible Microsoft research behind it and a clean zero-overhead deployment artifact. But it is a research framework whose value is gated on you supplying a dataset + rollout + reward for *your* task — trivial for the shipped academic benchmarks, real work for a software project where "correct" isn't auto-scorable. Track it (and especially SkillOpt-Sleep, which targets exactly the coding-agent self-improvement loop) and adopt once a turnkey path from real dev sessions to a reward signal exists; don't expect to point it at your repo today.

Compared to neighbors: **skill-creator** (anthropics) is the practical authoring tool — draft + eval + triggering-optimization, usable now without a labeled dataset; SkillOpt is what skill-creator's "eval" step aspires to but done as gradient-style training. **Skill Seekers** generates skills from docs at volume; SkillOpt is the rigorous opposite — it shrinks and *proves* a skill rather than scraping one. **SkillSpector**/**capa** scan or wire skills and don't touch quality at all. SkillOpt occupies the Reflect/optimization corner none of them reach; the gap to adoption is operational (reward authoring), not conceptual.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SkillOpt](https://github.com/microsoft/SkillOpt) | framework | Trains a skill document like a neural net — epochs, learning-rate budget, held-out validation gate — accepting an edit only if it strictly improves the score; deploys a compact `best_skill.md` with zero inference-time overhead (8.4K stars, Microsoft) | Skills are hand-crafted or one-shot generated and never reliably improve over their starting point; need measured, validated skill optimization | skill-creator (practical authoring + eval, no dataset needed), Skill_Seekers (generates from docs — rigorous opposite), SkillSpector/capa (scan/wire, not quality) |
