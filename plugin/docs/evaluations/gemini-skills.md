# Evaluation: gemini-skills

**Repo:** [google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills)
**Stars:** 3,671 | **Last updated:** 2026-06-17 (pushed; created 2026-02-06) | **License:** Apache-2.0
**Dev loop stage:** Implement — it is reference context injected at code-gen time so the agent writes correct, current Gemini API/SDK code. Secondarily Plan (model selection). Not a Verify/Review tool.
**Layer:** Process (a small set of `SKILL.md` files installed into the agent's skills directory; no runtime, no code that executes — the optional companion is an MCP docs server, evaluated separately).

---

## What it does

Google's official skill library for building apps against the Gemini API. The premise is the standard skills pitch sharpened to a point: an LLM's weights are frozen at training time, but the Gemini SDKs, model IDs, and best practices move every few weeks, so the model confidently emits **deprecated** code. These skills are the override layer. As inspected, the repo ships **three skills**, each a single `SKILL.md` (one with a `references/migration.md`):

- `gemini-api-dev` — core "build a Gemini app" skill: current model IDs, current SDKs (`google-genai` / `@google/genai` / Go / Java), multimodal, function calling, structured output.
- `gemini-live-api-dev` — real-time bidirectional streaming (WebSocket audio/video/text, VAD, native audio, session management).
- `gemini-interactions-api` — the Interactions API surface (multi-turn chat, streaming, image gen, Deep Research agents, Python + TS).

The mechanism is pure context injection. The `gemini-api-dev` `SKILL.md` opens with `Critical Rules (Always Apply)` that explicitly say "These rules override your training data. Your knowledge is outdated," then lists the current model roster (`gemini-3.5-flash`, `gemini-3.1-pro-preview`, `gemma-4-*`, …) and flags `gemini-2.0-*` / `gemini-1.5-*` and the old `google-generativeai` / `@google/generative-ai` SDKs as deprecated-never-use. There is no orchestration and nothing executes — it is a freshness patch the model reads before writing API code. A companion **Gemini API docs MCP** (`gemini-api-docs-mcp.dev`) is offered for live doc lookup; the README says the skill works with or without it.

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill was installed via `skills.sh`/`ctx7`, no Gemini code was generated, and the docs MCP was not connected. Every claim comes from the repository (GitHub metadata, README, full recursive file tree, the `gemini-api-dev` `SKILL.md` body), not from observed agent behavior. The README's "**87% with Gemini 3 Flash / 96% with Gemini 3.1 Pro**" code-correctness numbers are Google's own published eval (linked to a developers.googleblog.com post), **not** anything we measured or verified.

```bash
gh api repos/google-gemini/gemini-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id}'
gh api repos/google-gemini/gemini-skills/readme --jq '.content' | base64 -d | head -120
gh api "repos/google-gemini/gemini-skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # 3 skills, all SKILL.md
gh api repos/google-gemini/gemini-skills/contents/skills/gemini-api-dev/SKILL.md --jq '.content' | base64 -d | head -40
gh api repos/google-gemini/gemini-skills/releases --jq 'length'   # 0
gh api repos/google/skills --jq '.stargazers_count'               # 13,948 (the larger google/skills monorepo it cross-links)
```

## What worked

- **Solves a real, recurring failure mode.** Agents reliably emit deprecated Gemini model IDs and the old `google-generativeai` SDK from stale training data. A skill that asserts the current roster and explicitly blacklists the legacy ones is exactly the right shape of fix — small, surgical, high-leverage.
- **Authoritative and current.** Maintained by Google's own Gemini team; pushed within the last few days. For a freshness patch, provenance and recency are the whole value, and this has both.
- **Clean, idiomatic skill authoring.** Tight frontmatter `description`, `Critical Rules (Always Apply)` framing, `[!WARNING]`/`[!CAUTION]` callouts for deprecations, progressive disclosure (`references/migration.md` loaded only when needed). A good worked example of the anthropics/skills pattern.
- **Published eval, not just vibes.** Google reports the skill lifts correct-API-code generation to 87% / 96% — rare to see any skill author attach a measured number, even if we didn't reproduce it.
- **Composable with the docs MCP.** The skill carries the durable rules; the optional MCP fills in live API detail. Sensible split that degrades gracefully (skill works alone).

## What didn't work or surprised us

- **Vendor-specific by construction.** This is the opposite of a portable Agent Skill — its entire payload is *Gemini* model IDs, *Gemini* SDKs, *Gemini* APIs. Useful only if you are building on Gemini; zero value for an Anthropic/OpenAI/local-model project. That is correct scoping, but it bounds the audience hard.
- **Inherently perishable.** A skill whose value is "current model IDs" is a maintenance treadmill — `gemini-3.5-flash` becomes legacy on the same schedule that made `gemini-1.5` legacy. It is only as good as its last push, and with **0 tagged releases** you install whatever `main` is, with no pinned, dated snapshot of "the roster as of <date>."
- **Tiny surface.** Three skills. This is a focused freshness patch, not a library — fine for what it is, but don't mistake it for breadth.
- **"Not an officially supported Google product."** The README disclaimer says exactly that and excludes it from Google's OSS vulnerability-reward program — so "official" means "authored by the team," not "supported with an SLA."
- **Overlaps the larger google/skills monorepo.** The README itself notes `vertex-ai-api-dev` has *moved out* to `google/skills` (13.9K stars). Two Google skill homes invites confusion about which is canonical for what.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (Gemini-only) | Directly prevents deprecated-model/SDK code; Google's own eval reports 87–96% correct-API generation with the skill loaded. No effect on non-Gemini work. |
| Speed | + | Skips the round-trips of generating deprecated code, hitting an error, and re-prompting; current SDK shapes are stated up front. |
| Maintainability | + / − | Code you ship is on the current SDK (good); but the skill itself is perishable and unversioned, so it must be re-pulled to stay correct. |
| Safety | neutral | Pure markdown context. No code executes, no host/network reach. (The optional docs MCP is a separate, network-touching component not evaluated here.) |
| Cost Efficiency | + | Loads only when building Gemini apps; fewer wasted retry/correction turns. Small token footprint per skill. |

## Verdict

**CONDITIONAL — adopt if and only if you build on Gemini.** Within its lane this is a near-textbook freshness skill: authoritative, current, well-authored, and backed by a published correctness eval — exactly the override layer that fixes the "model emits deprecated Gemini code" failure. But the lane is narrow (Gemini-only by construction) and the payload is perishable and unversioned, so its value decays without re-pulling. For an Anthropic-centric stack like this catalog's recommended one, it is not a default install; it earns a slot the moment a project targets the Gemini API, and is best paired with the docs MCP.

Compared to neighbors: **google/skills** (13.9K stars) is the broader Google skills monorepo and is where `vertex-ai-api-dev` now lives — gemini-skills is the focused, Gemini-API-only subset. Versus the portable, build-backed **vercel-labs/agent-skills** (real test suites, framework-agnostic React/Next guidance) and the canonical **anthropics/skills** reference, gemini-skills trades portability for vendor depth: it is the right tool only when Gemini is the target, where the others stay useful across stacks.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gemini-skills](https://github.com/google-gemini/gemini-skills) | skill | Google's official 3-skill freshness patch for the Gemini API/SDK — current model IDs, current SDKs, Live + Interactions APIs; overrides stale training data (Google's eval: 87–96% correct API code) | Agents emit deprecated Gemini model IDs and old SDKs from stale training data when building Gemini-powered apps | google/skills (broader Google monorepo); anthropics/skills, vercel-labs/agent-skills (portable, not vendor-locked) |
