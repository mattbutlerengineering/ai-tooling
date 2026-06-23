# Evaluation: moai-adk

**Repo:** [modu-ai/moai-adk](https://github.com/modu-ai/moai-adk)
**Stars:** ~1,100 | **Last updated:** 2026-06-20 | **License:** Apache-2.0
**Dev loop stage:** Plan / Implement
**Layer:** Process / Tooling

---

## What it does

MoAI-ADK ("Agentic Development Kit") is a SPEC-First development kit for Claude Code. It packages an opinionated, spec-driven, test-first workflow as a Go CLI (zero dependencies) plus a bundle of agents and skills.

Per the README it ships **24 AI agents + 52 skills** with **TDD/DDD quality gates**, support for 16-language projects, and 4-language documentation. The thesis is the familiar spec-driven-development one — turn intent into an approved spec, then implement test-first behind quality gates — but delivered as a ready-made kit rather than something you assemble from individual skills. The Go CLI with zero deps means a single-binary install.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented composition (24 agents, 52 skills, TDD/DDD gates, Go CLI, multi-language). Confirmed the SPEC-First + test-first positioning and the packaged-kit delivery model. Did not run the kit on a live project, so condition-gated. (Note: a large bundled agent/skill set is something to audit before adopting wholesale.)

```bash
gh api repos/modu-ai/moai-adk --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/modu-ai/moai-adk/readme --jq '.content' | base64 -d
```

## What worked

- **Opinionated SPEC-First + TDD/DDD in one kit.** Bundling spec gating and test-first gates with the agents/skills that enforce them lowers the assembly cost versus wiring spec-kit + a TDD hook + agents yourself.
- **Zero-dep Go CLI.** Single-binary install is low-friction and portable.
- **Multi-language + multi-locale.** 16-language project support and 4-language docs broaden applicability beyond English/JS-Python shops.

## What didn't work or surprised us

- **Large bundled surface.** 24 agents + 52 skills is a lot to trust at once; audit what's included and whether it fits your conventions before adopting wholesale.
- **Crowded SDD space.** Overlaps spec-kit, OpenSpec, flow-next, Archon, BMAD-METHOD; the differentiator is the all-in-one kit with TDD/DDD gates, not the spec concept itself.
- **Opinion lock-in.** A packaged workflow imposes its structure; teams with an established process may find it prescriptive.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | TDD/DDD gates enforce tests and design discipline per change |
| Speed | + | Ready-made agents/skills avoid assembling a workflow from scratch |
| Maintainability | + | Spec-first artifacts and gates keep changes consistent |
| Safety | neutral | Process kit; audit the bundled agents/skills for safety |
| Cost Efficiency | neutral | Free/OSS; large agent set may add token overhead per task |

## Verdict

**CONDITIONAL**

Adopt if you want a turnkey SPEC-First + TDD/DDD workflow for Claude Code and prefer an opinionated kit over assembling spec-kit + TDD hooks + agents yourself — especially for multi-language teams. Audit the 24-agent/52-skill bundle against your conventions first. Compare with flow-next/Archon (workflow engines) and spec-kit (spec layer) for the spec-driven slot.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [moai-adk](https://github.com/modu-ai/moai-adk) | plugin | SPEC-First Agentic Development Kit for Claude Code (Apache-2.0) — Go CLI (zero deps) shipping 24 agents + 52 skills with TDD/DDD quality gates, 16-language projects, and 4-language docs | Agents skip specs/tests and produce inconsistent quality; want a packaged, opinionated SPEC-first + TDD/DDD workflow with agents and gates built in | spec-kit, OpenSpec, flow-next, Archon, BMAD-METHOD |
