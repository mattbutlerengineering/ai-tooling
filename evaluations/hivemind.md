# Evaluation: hivemind

**Repo:** [activeloopai/hivemind](https://github.com/activeloopai/hivemind)
**Stars:** 1,313 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Reflect (capture/codify) + Plan/Implement (recall at inference time)
**Layer:** Infrastructure

---

## What it does

Turns agent execution traces into reusable skills shared across agents. Hivemind is a cloud-backed "shared brain" from Activeloop (the Deeplake team, YC-backed). It installs as hooks/plugins into multiple coding agents (Claude Code, OpenClaw, Codex, Cursor, Hermes, pi) and does four things on a loop: **Capture → Codify → Propagate → Compound.**

The mechanism: every agent interaction (prompt, tool call, response) is captured as a structured trace and stored in Deeplake (Activeloop's tensor database). A background "skillify" worker fires on Stop (every `HIVEMIND_SKILLIFY_EVERY_N_TURNS`, default 20) and SessionEnd. It pulls the last 10 in-scope sessions newer than a per-project watermark, strips them to prompt + assistant text, and runs `claude -p haiku --permission-mode bypassPermissions` with a gate prompt. The model returns `KEEP <name> <body>`, `MERGE <existing> <body>`, or `SKIP <reason>`. On KEEP/MERGE it writes a real `SKILL.md` to `<project>/.claude/skills/<name>/` (or `~/.claude/skills/` globally) with provenance frontmatter, and appends a row to a Deeplake `skills` table for org-wide sharing. Teammates install each other's mined skills with `hivemind skillify pull`. Beyond skills, it also generates AI wiki summaries per session, builds a codebase graph from traversed files, injects shared team "rules" at SessionStart, and offers VFS-backed goals/KPIs.

## How we tested it

**Evidence:** REVIEW

Architecture review — inspected the GitHub repo, full README, `docs/SKILLIFY.md`, repo tree, and topics via the `gh` API. Did NOT install or run the tool (it requires a Deeplake account, browser sign-in, and stores all session data in Activeloop's cloud by default — outside the bounds of a doc-review evaluation). Compared the mechanism against catalog peers it overlaps with (openskills, claude-mem) and against calibration evals agentmemory (CONDITIONAL) and aisuite (SKIP).

```bash
gh api repos/activeloopai/hivemind --jq '{stars,license,description,pushed_at,topics}'
gh api repos/activeloopai/hivemind/readme --jq '.content' | base64 -d
gh api repos/activeloopai/hivemind/git/trees/main --jq '.tree[].path'
gh api repos/activeloopai/hivemind/contents/docs/SKILLIFY.md --jq '.content' | base64 -d
```

Verified: real `claude-code-plugin` + `claude-skills` topics; marketplace install path (`/plugin marketplace add activeloopai/hivemind`); SKILL.md output format with provenance frontmatter; six-platform support; LoCoMo benchmark table; Deeplake/Activeloop vendor backing; npm package `@deeplake/hivemind`.

## What worked

- **Genuine Claude Code integration, not just infra.** Ships as a first-class marketplace plugin (`/plugin install hivemind`), wires SessionStart/Stop/SessionEnd hooks, exposes slash commands (`/hivemind:login`, `/skillify`), and auto-updates each session. This is a dev-loop tool, unlike aisuite (SKIP). It sits in the Reflect stage and feeds Plan/Implement.
- **Outputs standard `SKILL.md` files.** Codified patterns are written to `.claude/skills/<name>/SKILL.md` with provenance frontmatter — portable, inspectable, and compatible with the native Claude Code skill loader. Not a proprietary format locked in the cloud.
- **A real differentiator from both overlap peers.** openskills *distributes* skills authors already wrote (a loader); claude-mem *stores and recalls* memory. Hivemind *generates new skills* by mining traces with an LLM gate, then shares them team-wide. The "mine successful runs → codify → propagate" loop is its own niche — the catalog's stated problem ("successful runs aren't captured as skills") is exactly what it targets.
- **Published benchmark with a stated method.** LoCoMo (100 QA pairs, Claude Haiku via `claude -p`, hybrid retrieval): 25% cheaper, 1.7x fewer tokens, 31% fewer turns vs. no-memory baseline. Self-run (Activeloop's own eval), but methodology is disclosed.
- **Team-scale design is the real value prop.** Cross-agent rules, team scoping for skill mining (`scope me|team`), pull/unpull across teammates, BYOC (GCS/Azure/S3/on-prem). This is the only catalog memory/skill tool built primarily for a *team* substrate, not a solo dev.
- **Honest, prominent data-collection notice** and per-session opt-out (`HIVEMIND_CAPTURE=false`), plus documented code-level controls (SQL escaping, 0600 creds, allowlisted VFS builtins).

## What didn't work or surprised us

- **Cloud-by-default with a vendor tie-in.** The whole pipeline backs onto Deeplake/Activeloop. Default storage is "Hivemind Cloud"; an account and (for shared memory) sign-in are required. BYOC exists but you still depend on Activeloop's orchestration. This is a hosted SaaS with an OSS client, not a self-contained local tool like engram or claude-mem.
- **"All users in your workspace can read this data. That's the design."** Every prompt, full tool input, and full tool output is captured and shared workspace-wide. For a solo dev or a privacy-sensitive shop this is a hard blocker; for a team it's the intended trade-off. Either way it is a significant safety/privacy posture to accept.
- **Skill mining runs `claude -p haiku --permission-mode bypassPermissions`.** A background worker spawning the agent with permissions bypassed is a reasonable engineering choice for unattended generation, but it is a surface worth knowing about.
- **Mined-skill quality is unproven here.** Auto-generated SKILL.md files from a Haiku gate could be noisy or generic; human review before org-wide propagation is only on the roadmap ("Skill versioning and review"), not shipped. No independent evidence of skill quality.
- **Young project, fast-moving.** Created April 2026, ~1.3K stars, very active (pushed today). Promising but not yet battle-tested at the level of claude-mem.
- **Value collapses for a single solo user.** The compounding "junior's agent is sharper because of the senior's" story requires a team. A lone developer gets only the much narrower self-mining + memory slice, which overlaps heavily with claude-mem/OMEGA (which the user already runs).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Recurring solved patterns are codified and re-injected, so agents re-derive less and reuse proven approaches |
| Speed | + | LoCoMo: 31% fewer turns; prior work is in scope at recall time, not re-derived |
| Maintainability | neutral | Outputs standard SKILL.md (good), but auto-mined skills lack a review gate and the store is cloud-hosted |
| Safety | - | Captures full prompts/tool I/O and shares workspace-wide by design; cloud-default; worker bypasses permissions |
| Cost Efficiency | + | LoCoMo: 25% cheaper, 1.7x fewer tokens per question vs. no-memory baseline (self-reported) |

## Verdict

**CONDITIONAL**

Use Hivemind if you run coding agents across a **team** and want successful runs automatically codified into shared SKILL.md files that propagate to every teammate's agent — that "mine traces → codify → propagate" loop is a genuine niche no other catalog entry fills, and it is a real Claude Code plugin, not building-block infra (so it is not a SKIP like aisuite). The conditions: (1) you are comfortable with full session data (prompts, tool inputs, tool outputs) captured to Activeloop's cloud and readable workspace-wide, or you set up BYOC; (2) you are a team, since the compounding value barely exists for a solo dev; (3) you accept auto-mined skill quality without a shipped human-review gate. For a solo Claude Code user already running claude-mem + OMEGA (this user's setup), the memory slice is redundant and the team-skill slice has no audience — for that profile it leans SKIP. CONDITIONAL on "you are a team that accepts cloud trace capture."

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hivemind](https://github.com/activeloopai/hivemind) | tool | Turns agent execution traces into reusable skills shared across agents (1.3K stars) | Agents re-derive the same solutions; successful runs are not captured as skills | claude-mem, openskills |
