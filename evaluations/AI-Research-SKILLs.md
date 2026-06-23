# Evaluation: AI-Research-SKILLs

**Repo:** [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)
**Stars:** 9,862 | **Last updated:** 2026-06-16 (pushed; created 2025-11-03) | **License:** MIT
**Dev loop stage:** Outer loop — Research/Discover, Plan, and a domain-specific Implement/Verify for *ML research engineering* (training, fine-tuning, eval, serving), capped by Reflect (paper writing). Not the general software dev loop.
**Layer:** Process (98 Agent-Skills-spec `SKILL.md` files across 23 categories) + a thin Tooling layer (`@orchestra-research/ai-research-skills` npx installer that symlinks skills into detected agents)

---

## What it does

The catalog one-liner positions it against academic-research-skills. The README's own framing is bolder: **"the most comprehensive open-source skills library enabling AI agents to autonomously conduct AI research — from idea to paper."** As inspected, it ships **98 `SKILL.md` files across 23 numbered categories** — and crucially, most of these are not "research" skills in the literature-and-writing sense; they are **deep, per-framework ML-engineering skills**: `08-distributed-training` (Megatron-core, DeepSpeed, FSDP2, Accelerate, Ray Train), `06-post-training` (TRL, GRPO, OpenRLHF, verl, slime, SimPO), `12-inference-serving` (vLLM, TensorRT-LLM, SGLang, llama.cpp), `10-optimization` (FlashAttention, AWQ, GPTQ, bitsandbytes, GGUF), plus tokenization, RAG, multimodal, mech-interp, MLOps, and observability. The sampled `vllm/SKILL.md` carries `dependencies: [vllm, torch, transformers]` and real PagedAttention/continuous-batching guidance — these are production engineering skills, not prompt personas.

The "research" wrapper sits on top: **`0-autoresearch-skill`** is an orchestration layer that runs a **two-loop architecture** (inner = rapid experiments with a single optimization target; outer = synthesis and direction-setting), maintains `research-state.yaml`/`research-log.md`/`findings.md`, and **routes to the domain skills**. Its frontmatter is explicit that it "runs fully autonomously — do not ask the user for permission," driven via Claude Code `/loop` or an "OpenClaw heartbeat," and produces HTML/PDF presentations and papers. Category 20 adds ML-paper-writing (academic plotting, systems-paper writing, conference talks); 21 adds ideation; 22 adds an "agent-native research artifact" trio (compiler, research-manager, rigor-reviewer).

Distribution is the most polished in this cluster: `npx @orchestra-research/ai-research-skills` (interactive installer, auto-detects Claude Code/OpenCode/Cursor/Gemini CLI/Qoder/etc., symlinks into `~/.orchestra/skills/`), a Claude Code marketplace with **per-category plugin install**, **10 tagged releases (latest v1.7.2)**, a published npm package, a `CITATION.cff`, and ~16 contributors.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No skill was installed, no `npx` installer executed, no autoresearch loop started, and no model was trained, served, or benchmarked. Every claim comes from the repository (GitHub metadata, README, full recursive file tree, sampled `autoresearch` and `vllm` `SKILL.md` frontmatters), not from observed behavior. The "98 skills," "autonomous," "research-grade quality," and "battle-tested" language is the authors' README framing; the only thing I verified is the file count and structure.

```bash
gh api repos/Orchestra-Research/AI-Research-SKILLs --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/Orchestra-Research/AI-Research-SKILLs/readme --jq '.content' | base64 -d
gh api 'repos/Orchestra-Research/AI-Research-SKILLs/git/trees/main?recursive=1' --jq '[.tree[]|select(.path|endswith("SKILL.md"))]|length'  # 98
gh api 'repos/Orchestra-Research/AI-Research-SKILLs/git/trees/main?recursive=1' --jq '.tree[].path'   # 23 numbered category dirs
gh api repos/Orchestra-Research/AI-Research-SKILLs/contents/0-autoresearch-skill/SKILL.md --jq '.content' | base64 -d | head -45
gh api repos/Orchestra-Research/AI-Research-SKILLs/contents/12-inference-serving/vllm/SKILL.md --jq '.content' | base64 -d | head -15
gh api repos/Orchestra-Research/AI-Research-SKILLs/releases --jq 'length'   # 10 (latest v1.7.2)
gh api repos/Orchestra-Research/AI-Research-SKILLs/contributors --jq '[.[].login]'   # ~16
```

## What worked

- **The engineering skills are the real asset — and they are good.** Most of the 98 are deep, framework-specific ML-engineering references (vLLM, Megatron, TRL, FlashAttention) with `dependencies` declared and concrete code/config guidance sourced from official repos. For long-tail training/serving frameworks a frontier model knows only shallowly, this is genuine lift.
- **`autoresearch` is a serious orchestration design, not a persona.** The two-loop architecture (fixed-budget inner experiments + outer synthesis), explicit `research-state.yaml` state, git-tracked progress, and a route-to-domain-skills router is the same disciplined methodology this catalog praised in karpathy/autoresearch — here generalized and made the system's entry point.
- **Best-in-cluster distribution and maintenance.** 10 releases, npm package, an installer that auto-detects multiple agents and symlinks rather than copies, per-category marketplace plugins, MIT license, `CITATION.cff`. This is shipped software, not a README dump.
- **Honest internal sourcing.** Category 22's `rigor-reviewer` and the ml-paper-writing skills show the authors care about research integrity, not just generation volume.
- **MIT, commercially usable** — unlike academic-research-skills (CC BY-NC), there is no license gate.

## What didn't work or surprised us

- **The "autonomous AI research, idea to paper" headline oversells the skills underneath.** What you actually get is a large, MIT-licensed *ML-engineering* skill library with a research-orchestration shell on top. The autonomy is the `autoresearch` skill's instruction text ("the human is asleep; make progress") — a prompt contract, not a verified capability; nothing in the repo substantiates end-to-end autonomous-paper outcomes.
- **Audience is narrow and specific: ML researchers with GPUs.** These skills assume you train, fine-tune, quantize, and serve neural networks. For application/software engineering — the bulk of this catalog's dev loop — almost none of the 98 apply. It is a vertical research-engineering pack mislabeled (by ambition) as general research.
- **98 skills is a curation/bloat surface.** The per-category marketplace install is the right mitigation — bulk-installing all 98 pollutes the agent's skill namespace and choice space. Quality almost certainly varies file-to-file across 23 categories, which I did not audit individually.
- **"Fully autonomous, don't ask permission" is a real safety posture, not a slogan.** A skill that instructs the agent to run training/serving loops unattended via `/loop`/heartbeat can spend real GPU money and execute long-running jobs without checkpoints with the human. That belongs behind explicit, sandboxed opt-in.
- **Overlaps the standalone karpathy/autoresearch eval** — this repo's `autoresearch` skill is a distinct, generalized re-implementation of that methodology, not the same artifact; the two should not be conflated in the catalog.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (in-domain) | Framework-specific skills (vLLM PagedAttention, Megatron parallelism, TRL/GRPO recipes) encode correct config/usage a model may otherwise get wrong — but only for ML-engineering tasks. |
| Speed | + / − | Pre-documented training/serving recipes save setup and debugging time in-domain; offset by the discovery cost of 98 skills and the autoresearch loop's long unattended runs. |
| Maintainability | neutral | Instruction files; no effect on your codebase. The *repo* is well-maintained (releases, installer, CITATION), but that does not touch your project. |
| Safety | − | `autoresearch`'s "fully autonomous, don't ask permission" loop can launch GPU training/serving jobs unattended; the skills shell out to heavy ML frameworks. Needs sandboxed, budgeted opt-in. |
| Cost Efficiency | − | Autonomous experiment loops on real GPUs are inherently expensive; the value proposition is "spend compute to find results faster," not "spend less." |

## Verdict

**CONDITIONAL — adopt the per-category engineering skills if you do ML research/training; treat `autoresearch`'s autonomy as opt-in and sandboxed.** This is the strongest-distributed and most engineering-substantive member of the research-skills cluster: 98 MIT-licensed, framework-deep skills behind a serious two-loop orchestration layer, with real release discipline. But its "autonomous research, idea to paper" headline overstates what is fundamentally an *ML-engineering* library for GPU-equipped researchers — almost none of it touches the application-software dev loop, and the unattended autonomy posture is a genuine safety/cost concern. Install by category (vLLM, fine-tuning, distributed-training) for the targeted lift; do not bulk-install, and gate the autoresearch loop behind explicit, budgeted, sandboxed runs.

Compared to neighbors: **scientific-agent-skills (CONDITIONAL)** is the broader *science* breadth play (147 skills + 100 databases across bio/chem/med) — AI-Research-SKILLs is the narrower, deeper *ML-engineering* vertical, and the two barely overlap in domain. **academic-research-skills (CONDITIONAL)** is the paper-*writing* depth play with hard citation-integrity gates but a NonCommercial license; AI-Research-SKILLs wins on license (MIT) and on actually *doing* the experiments, but its paper-writing layer (category 20) is thinner on integrity verification. **PaperOrchestra (CONDITIONAL)** is a single benchmarked paper-writing pipeline that this library could route into. Against the standalone **karpathy/autoresearch (CONDITIONAL)** eval, this repo generalizes that two-loop methodology and packages it with a real engineering skill library beneath it — more complete, more maintained, but carrying the same "autonomy overstates verified capability" caveat. Among the cluster it has the best engineering substance and distribution; it is held back by audience narrowness and the unverified autonomy claim.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | skill | 98 MIT-licensed ML-engineering skills (training, fine-tuning, serving, eval, RAG) across 23 categories, behind an `autoresearch` two-loop orchestration layer; per-category install | ML researchers re-debug framework-specific infra (Megatron, vLLM, TRL) instead of testing hypotheses; want agents to run the research engineering autonomously | scientific-agent-skills (science breadth vs. ML-eng depth); academic-research-skills, PaperOrchestra (paper-writing); karpathy/autoresearch (generalizes its two-loop method) |
