# Evaluation: agents-cli

**Repo:** [google/agents-cli](https://github.com/google/agents-cli)
**Stars:** 3,012 | **Last updated:** 2026-06-15 (pushed; created 2026-04-08) | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Spans the loop *for one narrow domain* — building, evaluating, and deploying agents on Google Cloud: Plan/Implement (scaffold + ADK), Verify (eval generate/grade/analyze/optimize), Ship (deploy, CI/CD, publish to Gemini Enterprise), Reflect (observability via Cloud Trace). It is not a general coding agent.
**Layer:** Tooling + Process — a PyPI CLI (`google-agents-cli`) that does the Google Cloud heavy lifting, plus an installable **Skills pack** that teaches *your* coding assistant how to drive it.

---

## What it does

Despite the bare GitHub description ("turn any coding assistant into an expert"), the README is precise: agents-cli is **Google's official CLI and skills for building agents on the Gemini Enterprise Agent Platform** — i.e. for shipping agents *on Google Cloud using the ADK (Agent Development Kit)*, not for writing general application code. It does not replace Claude Code or gemini-cli; it *augments* them. The pitch is that your existing coding assistant doesn't have to learn every GCP CLI and service — agents-cli supplies the skills and commands so the assistant can scaffold, evaluate, deploy, govern, and optimize enterprise agents for you.

Two install paths: `uvx google-agents-cli setup` installs the CLI plus skills into your coding agents, or `npx skills add google/agents-cli` drops just the skills and lets the assistant handle the rest. It ships a `.claude-plugin/plugin.json` (so it is also a Claude Code plugin) and integrates with Gemini CLI, Claude Code, Codex, and Antigravity. The **seven skills** map to lifecycle stages: `workflow` (lifecycle, code-preservation, model selection), `adk-code` (ADK Python API — agents, tools, orchestration, callbacks, state), `scaffold` (`create`/`enhance`/`upgrade`), `eval` (metrics, datasets, LLM-as-judge, adaptive rubrics), `deploy` (Agent Runtime / Cloud Run / GKE, CI/CD, secrets), `publish` (Gemini Enterprise registration), and `observability` (Cloud Trace, logging). The CLI surface is correspondingly deep: `scaffold`, `run`, `lint`, a full `eval` suite (`generate`/`grade`/`compare`/`analyze`/`optimize`/`dataset synthesize`), `deploy`, `publish gemini-enterprise`, `infra` (single-project, cicd, datastore), and `data-ingestion` for RAG.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `uvx`/`npx` install was performed, no skill was added to any assistant, no GCP project was authenticated, and no agent was scaffolded, evaluated, or deployed. This environment has no Google Cloud credentials, so the eval, deploy, infra, and publish flows are entirely unexercised. Every claim is from GitHub metadata, the README, the file tree, and the docs index — not observed behavior.

```bash
gh api repos/google/agents-cli --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/google/agents-cli/readme --jq '.content' | base64 -d | head -130
gh api "repos/google/agents-cli/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # .claude-plugin/, docs/ (mkdocs), 7-skill matrix in README
gh api repos/google/agents-cli/commits --jq 'length'    # 26 (page-1 cap)
gh api repos/google/agents-cli/releases --jq 'length'   # 8 tagged releases (PyPI google-agents-cli)
gh api repos/google/agents-cli --jq '.forks_count'      # 363 forks, only ~3 listed contributors
```

## What worked

- **First-party Google tooling for a real, painful workflow.** Standing up, evaluating, and deploying an enterprise agent on GCP normally means stitching together ADK, Cloud Run/GKE, Agent Runtime, Cloud Trace, and a pile of `gcloud`. A single official CLI + skill pack that an assistant can drive is a genuine force multiplier for that specific job.
- **The eval suite is the standout.** `eval generate`/`grade`/`compare`/`analyze`/`optimize` plus `dataset synthesize` and LLM-as-judge/adaptive rubrics is a fuller agent-evaluation loop than most catalog entries offer — including failure-mode clustering and prompt auto-tuning from eval data.
- **Cross-assistant by design.** Works with Gemini CLI, Claude Code, Codex, and Antigravity; ships a `.claude-plugin/plugin.json`. The skills-only install path means you can adopt it without committing to its CLI lifecycle.
- **Decent shipping discipline for a new repo.** 8 tagged releases, PyPI distribution (`google-agents-cli`), a versioned mkdocs docs site with hands-on tutorials, issue templates, and CONTRIBUTING — only ~2 months old.

## What didn't work or surprised us

- **Hard Google Cloud lock-in — this is its whole identity.** Every high-value command (`deploy`, `publish gemini-enterprise`, `infra`, `data-ingestion`, observability) assumes GCP + Gemini Enterprise + ADK. Outside that stack, what's left is mostly scaffolding and generic eval. This is GCP-platform tooling, not a portable assistant upgrade.
- **The GitHub one-liner badly undersells/misframes it.** "Turn any coding assistant into an expert" reads like a general coding-skills pack; it is in fact narrow vertical tooling for ADK-on-GCP agent ops. Easy to miscatalog.
- **Bus-factor / freshness caution.** Only ~3 listed contributors and 26 commits on a 2-month-old repo; it tracks a fast-moving Google product (Gemini Enterprise Agent Platform), so skills and commands can drift with the platform.
- **Not evaluable without a GCP account.** The parts that justify adoption (deploy, eval-against-cloud, infra, publish) cannot be assessed without spending on Google Cloud — adoption is a real commitment, not a quick try.
- **Heavy prerequisite chain** (Python 3.11+, uv, Node.js) for what is, for non-GCP users, a thin slice of usable surface.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Eval suite (grade, compare, analyze failure modes, LLM-as-judge, prompt optimize) is built to *measure and improve* agent correctness — strong if you live on GCP/ADK. |
| Speed | + | One CLI + skills replaces hand-stitching ADK + Cloud Run/GKE + Trace; assistant can scaffold-to-deploy without the human learning every service. |
| Maintainability | + / − | Scaffold `upgrade`, CI/CD setup, and structured projects help; offset by tight coupling to a fast-moving Google platform and thin contributor base. |
| Safety | − / neutral | `deploy`/`infra` provision real Google Cloud resources and secrets — production blast radius and cloud spend. The skills/eval/scaffold parts are low-risk. |
| Cost Efficiency | − | Value is gated behind paid GCP usage; `eval optimize` can tune prompts to cut tokens, but the platform itself is the cost. No free/local path for the deploy half. |

## Verdict

**CONDITIONAL — adopt if and only if you build agents on Google Cloud / Gemini Enterprise.** agents-cli is high-quality, official, cross-assistant Google tooling for a genuinely hard vertical: scaffolding, evaluating, deploying, and observing ADK agents on GCP. Its eval suite is a real differentiator and the skills-only install lowers the trial cost. But it is *not* the general "expert coding assistant" upgrade its tagline implies — strip away Google Cloud and little remains. For anyone on the GCP/ADK path it is close to an ADOPT; for everyone else it is out of scope.

Compared to neighbors: it is **not** a peer of gemini-cli / qwen-code / opencode / grok-cli — those are general coding agents; agents-cli is platform-ops tooling that *rides on top of* one of them (it explicitly lists Gemini CLI, Claude Code, Codex, Antigravity as hosts). Its closest catalog kin are vertical skill/plugin packs that teach an assistant a specific domain (e.g. the agency/skills collections) rather than coding-agent CLIs — but unlike pure persona packs, it ships a real CLI doing real Google Cloud work behind the skills. Best filed as a domain-specific Agent Harness skill pack, not an alternative coding CLI.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agents-cli](https://github.com/google/agents-cli) | skill | Google's official CLI + 7-skill pack that teaches any coding assistant to scaffold, evaluate, deploy, and observe ADK agents on Gemini Enterprise / Google Cloud | Building and shipping enterprise agents on GCP without learning every ADK/Cloud Run/GKE/Trace service by hand | gemini-cli (host coding agent it augments, not replaces); agency-agents, harness (skill/persona packs that specialize an assistant) |
