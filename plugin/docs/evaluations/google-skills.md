# Evaluation: google/skills

**Repo:** [google/skills](https://github.com/google/skills)
**Stars:** 13,918 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Official Google Agent Skills collection covering Google Cloud products and technologies. 33 skills organized under `skills/cloud/`, spanning databases (AlloyDB, BigQuery, Bigtable, Cloud SQL), compute (Cloud Run, GKE), AI/ML (Gemini API, Agent Platform with 10+ sub-skills), Firebase, and the full 6-pillar Google Cloud Well-Architected Framework (Security, Reliability, Cost, Ops Excellence, Performance, Sustainability). Each skill is a SKILL.md with a `references/` directory containing product-specific deep-dive documents.

The skills act as authoritative grounding documents — they tell the agent the current SDK names, CLI commands, setup sequences, and architectural patterns for each Google Cloud product. The Firebase skill, for example, enforces installing `firebase/agent-skills` as a prerequisite and walks through CLI login and project setup before any implementation.

## How we tested it

**Evidence:** REVIEW

Architecture review of the repository structure and content quality across 4 representative skills (firebase-basics, gemini-api, alloydb-basics, google-cloud-waf-security). Read SKILL.md files and reference directories to assess depth, accuracy, and structural consistency.

```
gh api repos/google/skills --jq '.description, .stargazers_count, .updated_at'
gh api repos/google/skills/contents/skills/cloud --jq '.[].name'
gh api repos/google/skills/contents/skills/cloud/firebase-basics/SKILL.md --jq '.content' | base64 -d
gh api repos/google/skills/contents/skills/cloud/gemini-api/SKILL.md --jq '.content' | base64 -d
```

## What worked

- **Authoritative SDK guidance**: Gemini API skill explicitly forbids deprecated SDKs (`google-cloud-aiplatform`, `google-generativeai`) and mandates the current unified SDK across 5 languages — prevents a common LLM hallucination pattern
- **Well-Architected Framework coverage**: 6 pillars × 200-300 lines each with grounding document URLs pointing to official docs — the most structured cloud architecture skill set in the catalog
- **Progressive disclosure**: Each skill has a lean SKILL.md (100-310 lines) with detailed references loaded on demand (firebase-basics has 7 reference files, gemini-api has 9)
- **Daily commits**: Active development with new skills added weekly (Bigtable on Jun 19, GKE Upgrades on Jun 18)
- **Ecosystem awareness**: Firebase skill chains to `firebase/agent-skills` and Dart/Flutter skills live in separate repos — good separation of concerns

## What didn't work or surprised us

- **Cloud-only scope**: Despite the repo name "google/skills", only `skills/cloud/` exists — no Workspace, Android, Chrome, or web platform skills. Google Workspace has a separate CLI (`googleworkspace/cli` in catalog) but no skills counterpart
- **Agent Platform branding churn**: The Gemini API skill opens with "IMPORTANT: Agent Platform was previously named Vertex AI" — this naming instability means the skill content will need frequent updates as branding settles
- **No install counts visible**: Unlike skills.sh-distributed collections, there's no way to see adoption numbers
- **Prerequisite chains**: Firebase skill requires manual user interaction (browser login, confirmation) which breaks autonomous agent flows

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Prevents deprecated SDK usage and enforces current CLI patterns |
| Speed | + | Pre-built setup sequences eliminate research time for GCP services |
| Maintainability | neutral | Skills are well-structured but cloud products change frequently |
| Safety | + | WAF Security pillar covers IAM, network security, data protection with Google's own framework |
| Cost Efficiency | + | WAF Cost Optimization pillar provides cloud cost reduction patterns |

## Verdict

**discovery-log — tentative read**

Use when building on Google Cloud or Firebase. The 33 skills cover the most common GCP services with authoritative, up-to-date guidance that prevents deprecated SDK usage — a genuine quality signal for Correctness. The 6-pillar Well-Architected Framework is the most structured cloud architecture skill set in the catalog. Skip if you're not using Google Cloud services; the skills have no general-purpose engineering value outside the GCP ecosystem.

## Triage note

Left at `discovery-log`. First-party GCP/Workspace/Firebase pack; in scope under the broad Skills &
Plugins blurb, and its 6-pillar Well-Architected content has no catalogued equivalent to be redundant
with. See the `gemini-skills` note for the one open question that touches this row — whether the
Gemini pack is a subset of this one — which needs a read of both trees rather than a triage guess.

Noted in passing: this eval's embedded `## Catalog entry` row names `microsoft/skills` as the overlap
while `CATALOG.md` says "— (domain-specific)". That mirror drift is not unique to this row and is
filed separately; the authoritative file is `CATALOG.md`.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [google/skills](https://github.com/google/skills) | skill | Agent skills for Google products and technologies | Need AI assistance with Google Cloud, Workspace, Firebase workflows | microsoft/skills |
