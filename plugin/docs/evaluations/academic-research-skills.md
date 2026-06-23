# Evaluation: academic-research-skills

**Repo:** [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)
**Stars:** 32,912 | **Last updated:** 2026-06-19 (pushed; created 2026-02-26) | **License:** CC BY-NC 4.0 (NonCommercial)
**Dev loop stage:** Plan (research, outline, literature) → and a Review/Verify analogue for the *writing* loop (peer-review and integrity gates over a manuscript, not over code)
**Layer:** Process / Tooling (a Claude Code plugin: four parent skills, ~30+ agent definitions, modes, hooks; prompt-driven, optional Python guard)

---

## What it does

The catalog one-liner: "Academic research workflow: research, write, review, revise, finalize." It is a Claude Code **plugin** (installable via `/plugin marketplace add Imbad0202/academic-research-skills`) that packages the full scholarly-paper lifecycle as four cooperating Agent Skills — `deep-research`, `academic-paper`, `academic-paper-reviewer`, and an `academic-pipeline` orchestrator — wired together with shared handoff schemas, staged quality gates, and ~30 sub-agent definitions (EIC, domain reviewers, Devil's Advocate, draft writer, literature strategist, formatter, etc.).

The mechanism is an orchestrated multi-agent pipeline run *by the host model* against prompt specs, not a server or SDK. The `academic-pipeline` skill drives a 10-stage flow (research → write → review → revise → finalize) with adaptive checkpoints. Two **integrity gates** (Stage 2.5 and 4.5) run a 7-mode blocking checklist explicitly modeled on the failure modes from "The AI Scientist" (Lu et al., *Nature* 2026) — implementation bugs, hallucinated results, methodology fabrication, citation hallucinations, etc. Citations are verified against the Semantic Scholar API; v3.7.x added "locator" citation anchors and an opt-in claim-audit pass (`ARS_CLAIM_AUDIT=1`) that fetches each cited source and judges whether it actually supports the claim, gate-refusing output through a formatter hard gate. The design is explicitly **human-in-the-loop, not full automation**: the README's framing is "AI is your copilot, not the pilot" — it does the grunt work (reference hunting, citation formatting, consistency checks) and leaves the question, method, and interpretation to the researcher. The core research/write/review skills are prompt-driven and need no Python; a real interpreter is needed only for an optional `PreToolUse` write-scope guard and a few opt-in shell-out features.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** The plugin was not installed via the marketplace command, no pipeline stage was executed, no paper was written or reviewed. Every claim below is from the repository surface (GitHub metadata, README, full file tree, release history, license file), not from observed tool output. The showcase metrics quoted below ("caught 15 fabricated refs," "found 21/68 issues missed by 3 rounds") are the author's self-reported showcase artifacts in `examples/showcase/`, not anything we measured or independently verified.

```bash
gh api repos/Imbad0202/academic-research-skills --jq '{stars,pushed,created,license:.license.spdx_id}'
gh api repos/Imbad0202/academic-research-skills/readme --jq '.content' | base64 -d
gh api "repos/Imbad0202/academic-research-skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/Imbad0202/academic-research-skills/contributors --jq '[.[].login]'   # 11 contributors
gh api repos/Imbad0202/academic-research-skills/releases --jq 'length'            # 30+ (latest v3.13.0)
gh api repos/Imbad0202/academic-research-skills/contents/LICENSE --jq '.content' | base64 -d  # CC BY-NC 4.0
```

## What worked

- **Genuinely high maturity — this is not a toy skill dump.** v3.13.0 with 30+ tagged releases, 11 contributors, a Zenodo DOI and `CITATION.cff`, and a deep CI suite (`pytest`, `eval-harness`, `freshness-check`, `spec-consistency`, `test-count-monotonic`, `harness-retirement-monthly`, `release-cooldown`). The release discipline alone (monotonic test counts, spec-consistency gates) puts it well above the median catalog skill.
- **Integrity gates target the exact failure modes of AI research.** Stage 2.5/4.5 blocking checklists are grounded in published literature (Lu et al. 2026; Zhao et al.'s 111M-reference hallucination audit), and Semantic Scholar verification plus claim-faithfulness auditing directly attack citation hallucination — the single biggest correctness risk in AI-assisted scholarship.
- **Honest, self-aware positioning.** The README explicitly rejects full automation, distinguishes itself from "humanizers" (it does not hide AI use), and labels its own claim-audit gap "L3 — future work" rather than overclaiming. Reproducibility is described as "configuration documentation, not replay guarantee." This restraint is rare and trustworthy.
- **Multi-perspective peer review is structurally sound.** The reviewer skill runs EIC + dynamic reviewers + Devil's Advocate with 0–100 rubrics, concession-threshold protocol, and an opt-in calibration mode that measures its own FNR/FPR against a user-supplied gold set — i.e. it can be told how well its critique actually performs.
- **Cross-tool reach and ecosystem.** Sibling Codex distribution, a companion `experiment-agent` for the run-experiments gap, and a `teaching-skills` companion. Optional cross-model verification (`ARS_CROSS_MODEL`) lets a second model check the first.

## What didn't work or surprised us

- **License is CC BY-NC 4.0 — NonCommercial.** This is the headline caveat. It is *not* an OSI/MIT license; commercial use is restricted. For a company embedding this in a paid workflow or a funded lab with commercial obligations, that is a real adoption blocker that neither of its catalog neighbors (scientific-agent-skills is MIT) imposes.
- **It is a workflow, not enforced code.** As with most Agent Skills, the integrity gates, citation discipline, and review rubrics are *instructions* the host model is asked to follow. The deterministic part is thin (a Python write-scope guard plus a few shell-outs); compilation, reasoning, and the actual gate decisions rest on the driving model. Self-reported showcase numbers cannot substitute for an independent benchmark.
- **Heavy operational surface for what it produces.** Modes, stages, environment flags (`ARS_CLAIM_AUDIT`, `ARS_CROSS_MODEL`), Pandoc/tectonic for DOCX/PDF, Git Bash + real Python on Windows for the guard to work (otherwise the hook logs an error per call). The "30 seconds to install" claim hides a long optional-prerequisite tail.
- **Cost is non-trivial.** The README's own estimate is ~$4–6 for a 15k-word paper, with a 13-agent research team and ~20–30 LLM calls per plotting/lit-review stage. That is fine for a real paper, expensive for casual use.
- **Narrow audience.** This is for people writing actual academic manuscripts — researchers, grad students, labs. For a software team it is mostly irrelevant; it does not touch the code dev loop at all. The 32.9K stars reflect the huge academic-writing audience, not applicability to this catalog's core (code-shipping) use case.
- **Star/fork ratio is unusual** (2,700 forks on 32,912 stars). Plausible for a template-style "fork to use" plugin, but worth noting the stars measure reach, not code longevity.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Semantic Scholar citation verification, claim-faithfulness audit pass, and literature-grounded integrity gates directly attack hallucinated/fabricated references — the dominant correctness risk in AI scholarship. (Effectiveness is self-reported, not independently benchmarked.) |
| Speed | + | Collapses reference hunting, citation formatting, multi-round peer review, and revision into one orchestrated pipeline; for the writing loop this is a large time saving over manual. |
| Maintainability | + / neutral | For *manuscript* maintainability (consistency, traceability matrices, R&R provenance) it is strong; irrelevant to code maintainability. Repo itself is well-maintained (CI, monotonic test counts). |
| Safety | neutral / − | Human-in-the-loop framing and integrity gates are safety-positive for research integrity; offsetting flag is the optional Windows hook degradation logging errors per call, and the NC license is a compliance/safety concern for commercial teams. |
| Cost Efficiency | − | ~$4–6 per 15k-word paper, 13-agent teams, ~20–30 calls per stage. Justified for real papers, costly otherwise. |

## Verdict

**CONDITIONAL** — adopt if you (or your lab) actually write academic papers and can live with the CC BY-NC 4.0 NonCommercial license. It is the most mature, most honestly-positioned tool in this trio: real release discipline, literature-grounded integrity gates, Semantic Scholar verification, and a refreshingly anti-hype "copilot not pilot" stance. Skip it if you write code rather than papers, or if your use is commercial — the NonCommercial license rules out the latter, and that is the gating condition.

Compared to neighbors: **scientific-agent-skills (also CONDITIONAL)** is a *breadth* play — 147 domain skills + 100 databases across all of science, MIT-licensed; ARS is a *depth* play on one workflow (paper writing) with far more rigor per stage and explicit integrity gates, but a restrictive license. **PaperOrchestra (SKIP/CONDITIONAL)** is a single-author implementation of one Google paper's five-agent pipeline — ARS actually *cites and absorbed* PaperOrchestra's techniques (v3.3) and is the more complete, better-maintained superset. **AI-Research-SKILLs** is the generic "turn agents into researchers" library; ARS is the specialized, hardened, paper-specific instance. Among the three evaluated here, ARS is the only one that approaches an ADOPT — held back only by license and audience narrowness.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | skill | Mature Claude Code plugin: research → write → peer-review → revise → finalize, with Semantic Scholar citation verification and literature-grounded integrity gates (CC BY-NC) | Need rigorous, human-in-the-loop AI assistance for writing academic papers without hallucinated citations or fabricated methodology | scientific-agent-skills, PaperOrchestra, AI-Research-SKILLs |
