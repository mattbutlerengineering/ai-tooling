# Evaluation: tech-leads-club/agent-skills

**Repo:** [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills)
**Stars:** 4,631 | **Last updated:** 2026-06-19 (pushed; created 2026-01-19) | **License:** NOASSERTION ("Other" — per-skill upstream attribution)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Spans the whole loop by *category*, not by stage — 81 skills across architecture, cloud, creation (ADR/RFC/design-doc), development, design, performance, quality, security, tooling (Nx-heavy), web-automation, and a large GTM/go-to-market band. Engineering-relevant clusters touch Plan (tlc-spec-driven, create-adr/rfc), Implement (nestjs-modular-monolith, react patterns), Verify/Review (security-*, web-quality-audit, perf-*), and Ship (vercel/netlify/cloudflare-deploy).
**Layer:** Tooling + Infrastructure (the skills are Process, but the headline artifact is a published npm CLI `@tech-leads-club/agent-skills` and an MCP server that install/update skills across 19 agents, with a security-scanning CI/CD pipeline behind publishing)

---

## What it does

The catalog one-liner: "Secure, validated skill registry for professional AI coding agents." Unlike a flat skill dump, this is a **registry + distribution platform**: an Nx-managed TypeScript monorepo (100% TS, semantic-release, Nx Cloud) shipping (1) a catalog of **81 skills** under category folders, (2) a published npm CLI (`npx @tech-leads-club/agent-skills`) with an interactive wizard plus full non-interactive subcommands (`install`, `update`, `remove`, `list`, `cache`, `audit`, `credits`), and (3) an MCP server. The CLI installs skills to **19 agents across three tiers** (Claude Code, Cursor, Copilot, Windsurf, Cline; Aider, Antigravity, Gemini CLI, Codex, Roo; Amazon Q, Augment, OpenCode, Cody, Tabnine, etc.), with copy-or-symlink and global-or-local scope.

The pitch is *security and validation*, not breadth. The README leads with "13.4% of marketplace skills contain critical vulnerabilities" (citing a Snyk Agent Scan report) and positions itself as a hardened library: 100% open source / no binaries, static analysis in CI, immutable integrity via lockfiles and content hashing, human-curated prompts, every skill scanned with Snyk Agent Scan before publishing, and a CLI built with defense-in-depth (input sanitization, path isolation, symlink guards, atomic lockfile, audit trail). Notably the catalog is an **aggregator**: skills carry per-source attribution (e.g. `security-best-practices` is authored `github.com/openai/skills`), so this curates and re-publishes upstream skills through a validated pipeline rather than authoring them all in-house.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** The CLI was not invoked, no skill installed, the MCP server not started, and none of the security controls (Snyk scan, lockfile/hash integrity, path/symlink guards, audit log) were exercised or independently verified. Every claim comes from the repository (GitHub metadata, README, recursive file tree, sampled `SKILL.md`). The "13.4% of skills are vulnerable" figure and all "hardened / verified / safe" language are the project's own README claims, not anything I measured; the security posture is described, not validated here.

```bash
gh api repos/tech-leads-club/agent-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'   # license: NOASSERTION
gh api repos/tech-leads-club/agent-skills/readme --jq '.content' | base64 -d
gh api "repos/tech-leads-club/agent-skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api "...trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|test("SKILL.md$"))]|length'   # 81 skills
gh api repos/tech-leads-club/agent-skills/releases --jq 'length'        # 30 (semantic-release)
gh api repos/tech-leads-club/agent-skills/contributors --jq '[.[].login]|length'   # 13
gh api "...contents/packages/skills-catalog/skills/(security)/security-best-practices/SKILL.md" ... | base64 -d  # authored: github.com/openai/skills
```

## What worked

- **The distribution mechanism is the real product, and it's strong.** A published, versioned npm CLI with a clean subcommand surface (install/update/remove/list/cache/**audit**/credits), copy-or-symlink, global-or-local scope, an interactive wizard *and* scriptable flags, targeting 19 agents — this is meaningfully better tooling than the "git clone and copy files" install path of nearly every skill-pack neighbor.
- **Genuine engineering rigor in the repo.** Nx monorepo, 100% TypeScript, semantic-release (30 releases), `libs/core` with hexagonal adapters (filesystem/http/shell/env) each with `__tests__`, a dedicated `.github/actions/security-scan` pipeline, and an `AGENTS.md`/`SECURITY.md`. The CLI is engineered like a product, not a side project.
- **Security framing is a real, differentiated angle.** Whether or not the controls fully hold up, "validated registry with CI scanning, content hashing, lockfiles, and least-privilege install" is exactly the gap most skill marketplaces ignore. The audit log and defense-in-depth CLI design are concrete, not just slogans.
- **Aggregation with attribution is honest curation.** Re-publishing upstream skills (openai/skills, etc.) *through a scanning pipeline* with per-skill author attribution is a legitimate value-add: you get a vetted superset rather than trusting each origin repo individually.
- **Strong process/architecture skills exist.** tlc-spec-driven (4-phase Specify→Design→Tasks→Implement with persistent memory), the DDD/decomposition cluster (tactical-ddd, modular-decomposition, coupling-analysis), and create-adr/rfc/design-doc are squarely the lean process skills this catalog values.

## What didn't work or surprised us

- **The security pitch is asserted, not provable from here.** The headline "13.4% of skills are vulnerable → we are safe" rests on the project's own claims and a single linked report. I scanned nothing; "every skill scanned with Snyk" and "immutable integrity" are descriptions of a pipeline, not evidence it works. Treat the marketing confidence ("absolute confidence") with the usual skepticism.
- **A large GTM/go-to-market band dilutes the engineering focus.** Roughly 17 of 81 skills are sales/marketing (ai-sdr, ai-cold-outreach, ai-pricing, lead-enrichment, social-selling, partner-affiliate, solo-founder-gtm). For a *coding-agent* skill registry these are off-axis and inflate the count; an engineering team installs none of them.
- **Heavy Nx-tooling bias.** A whole `(tooling)` cluster (nx-workspace, nx-generate, nx-run-tasks, nx-ci-monitor) reflects the maintainers' own stack; valuable if you use Nx, noise if you don't.
- **Aggregation cuts both ways.** Curating upstream skills means quality and freshness depend on sources the team doesn't control, and the `NOASSERTION` top-level license (per-skill attribution instead of one clear license) makes blanket reuse/redistribution terms murkier than a plain-MIT pack.
- **Young and fast-moving.** Created 2026-01-19 (≈5 months old) with 13 contributors; 30 semantic-release versions in that span signal velocity but also churn — the install surface and catalog are still settling.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Strong process/architecture skills (tlc-spec-driven, DDD cluster, create-adr) can improve rigor; correctness of any individual aggregated skill still depends on its upstream author. |
| Speed | + | Best-in-class install/update/remove CLI across 19 agents with scriptable flags removes the manual copy/symlink friction of every other skill pack. |
| Maintainability | + | Nx monorepo, semantic-release (30 versions), tested `libs/core` adapters, lockfiles, and a versioned CLI make installs reproducible and the platform itself well-maintained. |
| Safety | + (claimed) | Differentiated angle: CI security scanning, content hashing, lockfile integrity, path/symlink guards, audit log, least-privilege install — strong *as described*, but unverified here and asserted by the vendor. |
| Cost Efficiency | neutral | Skills use standard `SKILL.md`+`references` progressive disclosure; the GTM/Nx long tail adds catalog noise but no per-use cost if not installed. |

## Verdict

**CONDITIONAL — adopt for the distribution CLI and the security/validation posture; cherry-pick the engineering/process skills and ignore the GTM band.** tech-leads-club/agent-skills is less a skill *collection* than a skill *platform*: the differentiator over every neighbor is the published, well-engineered npm CLI + MCP server that install/update/audit skills across 19 agents through a security-scanning pipeline. That tooling is genuinely the best install experience in this catalog's skill-pack cohort. The caveats are that the security claims are vendor-asserted (unverified here), a big slice of the 81 skills is off-axis go-to-market/Nx content, and the catalog is an aggregator under a murky `NOASSERTION` license. The right use is: install the CLI, pull the architecture/spec/security/quality skills, skip the marketing skills.

Compared to neighbors: where **Jeffallan/claude-skills**, **mattpocock/skills**, **antfu/skills**, and **addyosmani/agent-skills** ship *content* you install by hand or via a single plugin, TLC ships a *registry + multi-agent installer + validation pipeline* — it competes on distribution and trust, not on having the best individual skills (many are aggregated from those very sources). Closest in spirit to a "SkillSpector / validated-marketplace" play than to a one-author skill set. Adopt the platform; don't treat its 81-skill count as 81 things worth installing.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) | skill | Security-validated skill *registry* + npm CLI/MCP server that installs/updates/audits 81 skills (aggregated, Snyk-scanned, content-hashed) across 19 AI agents — distribution and trust, not bespoke content | Want a vetted, reproducible way to install and manage agent skills across many tools rather than trusting and hand-copying unvetted marketplace skills | Jeffallan/claude-skills, mattpocock/skills, antfu/skills, addyosmani/agent-skills, ECC |
