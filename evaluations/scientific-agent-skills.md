# Evaluation: scientific-agent-skills

**Repo:** [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
**Stars:** 28,756 | **Last updated:** 2026-06-15 (pushed; created 2025-10-19) | **License:** MIT
**Dev loop stage:** Plan (domain research, data access, literature) → Implement (writing analysis code against scientific libraries/databases); a research-domain analogue, not the code dev loop
**Layer:** Tooling (147 Agent Skills — curated `SKILL.md` + references + a few deterministic Python scripts per skill; cross-tool via the open Agent Skills standard)

---

## What it does

The catalog one-liner: "140 scientific skills + 100 database connectors for biology, chemistry, medicine, and drug discovery." It is the largest science-focused **Agent Skills library** in the catalog — 147 skills (the badge says 147; the file tree confirms 147 `SKILL.md` files) spanning bioinformatics, cheminformatics, proteomics, clinical research, medical imaging, materials science, physics/astronomy, geospatial, lab automation, and research methodology. It installs cross-tool via `npx skills add K-Dense-AI/scientific-agent-skills` or `gh skill install ...` (with version pinning to a tag or SHA).

The mechanism is **curated capability documentation, not new code**. As the README states plainly, "the agent can use any Python package or API on its own" — each skill simply ships a dense `SKILL.md` plus `references/` (and occasionally a deterministic `scripts/` helper, e.g. `arboreto/scripts/basic_grn_inference.py`) that give the host model curated docs, working examples, and best practices for a specific library (RDKit, Scanpy, BioPython, OpenMM, Qiskit, scVelo, TimesFM…) or data source. The headline "100+ databases" is mostly a single `database-lookup` skill providing deterministic, provenance-rich access to 78 public databases (PubChem, ChEMBL, UniProt, COSMIC, ClinicalTrials.gov, FRED, USPTO…), plus dedicated skills and multi-database packages (BioServices, gget). It is the open-source skill layer beneath K-Dense's "BYOK" desktop co-scientist product.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No skill was installed via `npx skills add` or `gh skill install`, no scientific workflow was executed, no database queried. Every claim is from the repository surface (metadata, README, file tree, release history, license), not observed output. The "160,000+ scientists worldwide" and "#1 Agent Skills library for science" claims in the description are the vendor's marketing, not anything we verified; treat as self-reported.

```bash
gh api repos/K-Dense-AI/scientific-agent-skills --jq '{stars,pushed,created,license:.license.spdx_id}'
gh api repos/K-Dense-AI/scientific-agent-skills/readme --jq '.content' | base64 -d
gh api "repos/K-Dense-AI/scientific-agent-skills/git/trees/HEAD?recursive=1" --jq '[.tree[].path | select(endswith("SKILL.md"))] | length'  # 147
gh api repos/K-Dense-AI/scientific-agent-skills/contributors --jq '[.[].login]'   # ~30 contributors
gh api repos/K-Dense-AI/scientific-agent-skills/releases --jq '.[0].tag_name'     # v2.52.0
```

## What worked

- **Breadth is the product, and it is real.** 147 skills across ~18 scientific domains with a confirmed 147 `SKILL.md` count. For a lab whose agent keeps re-deriving how to call Scanpy, RDKit, or the COSMIC API, a pre-documented, example-bearing skill genuinely raises reliability over cold-start tool use.
- **Healthy maturity for a skill library.** MIT-licensed, v2.52.0, ~30 contributors (including bot-assisted releases), and a security-conscious CI suite: `security-scan.yml`, `pr-skill-scan.yml`, plus `scan_skills.py` / `scan_pr_skills.py` that vet incoming skills. For a library that ships content executed by an agent, scanning PRs for malicious skill content is the right instinct.
- **Honest about what a skill is.** The README repeatedly notes the agent can use any package; the skills are "the optimized, pre-documented paths," not a moat. The `database-lookup` skill emphasizes deterministic, provenance-rich access — provenance matters in science.
- **Excellent distribution.** Standards-based install (`npx skills add`, `gh skill install` with `--pin` for reproducible installs and `--agent` targeting), works across Cursor / Claude Code / Codex / Gemini CLI / Antigravity and more. Version pinning to a SHA is a supply-chain plus.
- **MIT license** — no commercial restriction, unlike the academic-research-skills neighbor.

## What didn't work or surprised us

- **It is fundamentally a curated documentation pack, not capability.** Value is real but bounded: it makes the model *more reliable* at things it can already attempt. For frontier models that already know RDKit/Scanpy well, the marginal lift on any single skill is modest — the value is the long tail of obscure libraries and the database catalog, not the famous ones.
- **Per-skill depth is uneven by construction.** 147 skills maintained by ~30 contributors means quality varies skill-to-skill; some have rich `references/` trees (aeon has 11 reference files), others are thin. There is no per-skill freshness/eval guarantee comparable to academic-research-skills' spec-consistency CI.
- **Security surface is inherent.** Skills instruct an agent to run scientific code against external databases and platforms (Benchling, DNAnexus, LatchBio, Opentrons lab hardware). The repo's own `SECURITY.md` / security disclaimer exists for a reason — agent-driven lab automation and clinical-data skills carry real-world risk that prompt docs do not contain.
- **Marketing-heavy README.** Star-history chart, "#1," "160,000+ scientists," repeated star-this-repo appeals, social badges. None of the headline adoption numbers are independently verifiable; discount accordingly.
- **Wrong audience for this catalog's core.** Like its neighbors, this serves working scientists, not software teams shipping product code. It does not touch Verify/Review/Ship of the code dev loop. Its catalog place is as a *domain research enabler*, not a general dev tool.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Curated docs + working examples + provenance-rich `database-lookup` reduce wrong API usage and unsourced data access vs. cold-start tool use; deterministic helper scripts (schema/validation) where present add rigor. |
| Speed | + | "Save days of work" by skipping API-doc research and integration setup; one prompt can drive a multi-step pipeline against pre-documented libraries. |
| Maintainability | neutral | A skill library doesn't make *your* code more maintainable; per-skill quality varies and there is no per-skill eval guarantee. Repo itself is reasonably maintained. |
| Safety | − | Skills drive agents to run code against external databases, cloud bio-platforms, and physical lab hardware (Opentrons); real-world action risk. Mitigated by PR security scanning, not eliminated. |
| Cost Efficiency | neutral | The skills add no infra/API cost themselves (no embedded LLM calls); cost is the host model's tokens for whatever workflow they enable. |

## Verdict

**CONDITIONAL** — adopt if you do scientific/research computing (bio, chem, med, materials, geospatial, physics) and want your agent to reliably reach a large, pre-documented library and database surface. It is mature, MIT-licensed, well-distributed, and security-scans its own contributions. Skip it for general software work: it is a domain-research enabler that does not touch the code dev loop, and for libraries a frontier model already knows well the marginal lift is small — the real value is the long-tail libraries and the 78-database catalog.

Compared to neighbors: this is the **breadth** complement to **academic-research-skills (CONDITIONAL)**, which is a *depth* play on the single paper-writing workflow with hard integrity gates and citation verification — but a NonCommercial license. scientific-agent-skills wins on license (MIT), distribution, and domain coverage; ARS wins on rigor-per-workflow. They are genuinely complementary: use scientific-agent-skills to *do* the science (data access, analysis libraries) and ARS to *write it up*. Against **AI-Research-SKILLs** (the generic "turn agents into researchers" library), this is the science-specialized, far larger, better-maintained instance. Among the three evaluated here it ties academic-research-skills as the strongest, separated mainly by which problem you have.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | skill | 147 MIT-licensed Agent Skills + a 78-database lookup layer across bio, chem, med, materials, physics, geospatial — cross-tool via the Agent Skills standard | Agent keeps re-deriving how to call scientific libraries/APIs; want curated, provenance-rich, pre-documented paths for reliable research workflows | academic-research-skills, AI-Research-SKILLs, PaperOrchestra |
