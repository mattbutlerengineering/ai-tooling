# Evaluation: OpenCode

**Repo:** [anomalyco/opencode](https://github.com/anomalyco/opencode)
**Stars:** 200,661 | **Last updated:** 2026-08-23 (last push) | **License:** MIT
**Last verified:** 2026-08-23
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A full open-source AI coding agent — terminal TUI, desktop app, HTTP server and SDK — that
runs the same agent loop Claude Code does against 11 first-party providers (Anthropic,
OpenAI, Google, Azure, Bedrock, OpenRouter, Mistral, GitLab, GitHub Copilot, and more) plus
its own hosted `opencode`/`opencode-go` model gateway. Ships two built-in primary agents —
**build** (full-access) and **plan** (read-only exploration) — plus `explore`/`general`
subagents, and reads project-local **agents**, **skills**, **commands**, **plugins** and
**permission rules** out of the working tree. `opencode serve` exposes that whole surface
over HTTP, which is what makes it scriptable rather than only interactive.

## How we tested it

**Evidence:** RUN

Exercised hands-on against **this repository**, which is the reason opencode is measurable
here at all: `CLAUDE.md`'s ADR-0002 declares opencode a *supported harness alongside Claude
Code* and the tree ships `.opencode/agents/eval-runner.md`, `.opencode/plugins/*.ts` and an
`opencode.json` command/permission map for it. Every claim below is an observed command or
an HTTP response, not a README paraphrase.

**Version under test: opencode 1.17.20**, the build installed at
`/Users/mbutler/.opencode/bin/opencode`. Upstream's latest release is **v1.18.21**
(2026-08-21), so these results are one minor version behind head and are stated as such.

```bash
opencode --version                                    # 1.17.20
opencode agent list                                   # agent discovery
opencode models | head                                # provider/model resolution
opencode run --agent build "Reply with exactly the token OPENCODE_OK and nothing else."
opencode serve --port 4097 --hostname 127.0.0.1 &     # headless HTTP surface
curl -s "http://127.0.0.1:4097/skill?directory=$PWD"  # skill discovery
curl -s "http://127.0.0.1:4097/command?directory=$PWD"
curl -s "http://127.0.0.1:4097/config?directory=$PWD" # loaded plugins
```

**1. A headless run works, and is fast.** `opencode run --agent build` returned the exact
requested token in **7 s** wall-clock on the default free model (`opencode/big-pickle`).
Non-interactive execution is a first-class path, not a TUI afterthought — which is what makes
opencode usable as a *second* harness rather than a replacement for the first.

**2. Agent discovery reaches the repo's symlinked agent.** `opencode agent list` resolves
`eval-runner (subagent)` — the file ADR-0002 keeps canonical at `.opencode/agents/` with
`.claude/agents/eval-runner.md` as a symlink to it. It also lists `build`, `plan`,
`compaction`, `summary`, `title` (primary), `explore`, `general` (subagent), and 11 globally
installed `gsd-*` agents, so discovery spans project-local and globally-installed sources.

**3. Skill discovery is a genuine union of two homes — verified by controlled probe.**
`GET /skill?directory=<repo>` returns all four project skills (`add-catalog-entry`,
`triage-lead`, `find-skills`, `find-catalog-gaps`). That alone does *not* prove
`.agents/skills/` is auto-discovered, because this repo's only `.agents/skills/` entry
(`find-skills`) is symlinked into `.claude/skills/` and opencode reports it at the
`.claude/skills/` path. So the claim was tested directly, in a scratch directory holding one
skill in each home and **no symlink between them**:

```
FOUND: claude-only -> <tmp>/.claude/skills/claude-only/SKILL.md
FOUND: agents-only -> <tmp>/.agents/skills/agents-only/SKILL.md
```

Both came back. `.claude/skills/` and `.agents/skills/` are each auto-discovered on their
own, so ADR-0002's "both harnesses auto-discover" is confirmed rather than assumed.

**4. `CLAUDE.md` really is the rules fallback.** With no `AGENTS.md` in the tree, a
tool-free probe asked the agent for the first `# ` heading of its project instructions and it
answered `` `# AI Tooling` `` — `CLAUDE.md` line 1. ADR-0002's "no `AGENTS.md` content fork"
holds in practice.

**5. Project commands and plugins load.** `GET /command` lists `check`, `fix`, `sync`
(the three declared in `opencode.json`) beside opencode's built-ins and the globally
installed set. `GET /config` reports `plugin:` holding both
`file:///…/.opencode/plugins/commit-gate.ts` and `…/auto-sync.ts`, so the lockstep
invariant's opencode half is loaded, not merely committed.

**Not exercised:** the commit-gate plugin was never *fired* — that needs a real commit
through opencode, a mutation out of scope for an evaluation — and the `skill` permission map's
`"add-catalog-entry": "ask"` gate was not driven to a prompt. Both are noted as unverified
rather than assumed working.

## Test design

- **Task/corpus:** this repository (`mattbutlerengineering/ai-tooling`) as the project under
  test, plus a two-skill scratch directory built specifically to separate the `.claude/skills/`
  and `.agents/skills/` discovery homes.
- **Baseline:** for the discovery claims the baseline is the *assertion in `CLAUDE.md`*, which
  is what the probe was designed to be able to refute; for the run-latency figure there is no
  with/without arm, which is exactly why this is `RUN` and not `MEASURED`.
- **Metric:** binary resolution (does the agent / skill / command / plugin appear) plus one
  wall-clock reading for the headless run.
- **Reproduce:** the command block above; the probe directory is two `SKILL.md` files with
  frontmatter `name`/`description` and no symlink between the two homes.

## What worked

- **Coexists with Claude Code — measured, not assumed.** This repo runs both harnesses off one
  set of source files and both resolve the same agents, skills and instructions. A second
  harness is a real option, not a migration.
- **The headless HTTP surface is the differentiator.** `serve` + `GET /skill|/command|/config`
  turns "is my agent config actually loaded?" into a scriptable question. Nothing in the Claude
  Code surface answers that from outside a session, and it is what let every claim above be
  checked instead of trusted.
- **Discovery is generous about layout.** Two skill homes, project-local and global agents,
  and project commands all resolve without configuration beyond `opencode.json`.
- **Multi-provider is real.** 11 native provider integrations plus a hosted gateway; the
  default free model answered a one-shot correctly in 7 s at no cost.
- **Config is strict and self-documenting.** A built-in `customize-opencode` skill ships in the
  binary and points at the published JSON Schema; opencode refuses to start on invalid config
  rather than silently ignoring a bad field.

## What didn't work or surprised us

- **The previous review's central claim was wrong.** It read *"Not a complement to Claude Code:
  OpenCode replaces Claude Code entirely… You run one or the other, not both"*, and declined to
  run the tool because *"switching away from Claude Code for the test would be disruptive."*
  Both halves are refuted above: the harnesses coexist in this tree, and `opencode run` is
  headless, so testing it never required switching anything. The premise that blocked the
  hands-on run was itself the thing that most needed testing.
- **The local install drifts silently.** 1.17.20 here against v1.18.21 upstream — 1 minor and
  ~1 month behind, with nothing in the repo watching it. Any harness-behaviour claim in
  `CLAUDE.md` is pinned to whatever version last happened to be installed.
- **Skill discovery reports the symlink path, not the target.** `find-skills` comes back as
  `.claude/skills/find-skills/SKILL.md` even though the file lives in `.agents/skills/`. Harmless
  here, but it means a location field cannot be used to prove which home a skill was found in —
  which is precisely why claim 3 needed a controlled probe.
- **Two agent namespaces bleed together.** 11 globally installed `gsd-*` agents show up in this
  project's `agent list` with no scoping marker beyond `(all)`, so a project's agent surface is
  whatever the machine happens to have installed.
- **7K+ open issues and Effect-TS throughout** — the contribution barrier and triage backlog
  noted in the earlier review both still stand; neither was re-measured.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Same models, same SKILL.md format; correctness tracks the model, not the shell |
| Speed | + | 7 s wall-clock for a one-shot headless run; provider choice per task |
| Maintainability | + | One source file per artifact serves both harnesses (agents, skills, hooks-as-plugins) — measured, not designed-for |
| Safety | + | `plan` read-only agent, and a declarative `permission` map (`bash`, `skill`) that is data rather than hook code — though the `ask` gate was not driven to a prompt here |
| Cost Efficiency | + | Free default model answered the smoke test; 11 providers plus a hosted gateway |
| Verifiability | + | `serve` exposes skill/command/config resolution over HTTP, so agent config is checkable from a script instead of by inspection |

## Verdict

**CONDITIONAL** — adopt-if: you want a **second, scriptable harness** beside Claude Code
rather than a replacement for it — specifically, if you need non-Anthropic providers, or you
want agent/skill/command resolution to be checkable from outside a session (`serve` +
`GET /skill|/command|/config`).

Held at CONDITIONAL rather than ADOPT deliberately. What was exercised here is the *harness
plumbing* — discovery, config loading, one headless run — not code produced through it, so
there is no with/without evidence on any quality signal that would justify recommending it as
a primary tool. As a secondary harness the condition is already met in this repo and the setup
cost was zero, which is the honest scope of the recommendation.

This replaces a `discovery-log — tentative read` that had explicitly declined to run the tool.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opencode](https://github.com/anomalyco/opencode) | platform | Open source coding agent, 11 providers, headless `serve` surface (200K stars) | Want an open source second harness whose agent/skill config is checkable from a script | OpenHands, goose |
