# Evaluation: baoyu-design

**Repo:** [JimLiu/baoyu-design](https://github.com/JimLiu/baoyu-design)
**Stars:** 1,622 | **Last updated:** 2026-06-19 (pushed; created 2026-06-07) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan / Implement on the *design* track — it drives a clarify → context → produce-HTML → preview → verify loop that yields UI mockups, prototypes, decks, and wireframes before (or instead of) production code. Outer-loop-adjacent for pitch/deck artifacts.
**Layer:** Process + Tooling — the design methodology is markdown (`SKILL.md` + `system-prompt.md` + built-in skills), but it ships a real **67-file Node/TypeScript toolchain** (PPTX pipeline, offline Figma `.fig` decoder, design-system compiler/checker) that executes.

---

## What it does

`baoyu-design` repackages **Claude Design** — the engine behind `claude.ai/design` — as a portable Agent Skill you run inside a local file-capable agent (Claude Code, Cursor, Codex, "70+ agents" per the installer). The pitch: get "the vast majority" of the website's design capability without the website, the separate subscription, or the upload step, with every artifact landing in your repo as self-contained HTML under `designs/<project>/`. Authored by Jim Liu ("Baoyu" / @JimLiu); the README leans hard on **Opus 4.8** as the recommended model because the skill is "a long, demanding design brief."

The architecture is a methodology core plus a fan of specialized prompts and scaffolds. `SKILL.md` orchestrates: load `system-prompt.md` (the craft methodology / source of truth), detect the harness and read the matching `references/{claude,cursor,codex}.md` tool map, then pull in only the needed file from **~32 `built-in-skills/`** (hi-fi-design, interactive-prototype, wireframe, make-a-deck, mobile-prototype, animated-video, create/use-design-system, import-from-{figma,github,html}, export-as-{pdf,pptx-editable,pptx-screenshots,video}, send-to-{figma,canva}, handoff-to-claude-code, …). It also ships **starter-components** (iOS/Android/macOS/browser device frames, pan-zoom canvas, deck stage, animation engine, tweaks panel) and an `agents/` directory of executable helpers — a full `gen-pptx` TypeScript project, a `.fig` decoder, and `compile-design-system.mjs` / `check-design-system.mjs` / `build-preview.mjs`. The headline workflow is the localhost-HTML loop: because deliverables are plain HTML on `localhost`, you point at an element in the live preview, say what to change, and the agent edits the source — a visual second-pass loop.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No skill was installed, no `npx` installer was executed, no design was generated, and none of the `agents/` Node/TS code (gen-pptx, figma decode, design-system compiler) was run. Every claim comes from the repository (GitHub metadata, README, full recursive file tree, `SKILL.md` frontmatter + orchestration body, the built-in-skills / starter-components / agents listings), not from observed output. We did **not** verify the README's central claim that it reproduces "the vast majority" of `claude.ai/design`, nor the implied quality of generated artifacts — the side-by-side screenshots are the author's, not ours.

```bash
gh api repos/JimLiu/baoyu-design --jq '{desc,stars:.stargazers_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id}'
gh api repos/JimLiu/baoyu-design/readme --jq '.content' | base64 -d | head -130
gh api "repos/JimLiu/baoyu-design/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/JimLiu/baoyu-design/contents/skills/baoyu-design/SKILL.md --jq '.content' | base64 -d | head -45
gh api "repos/JimLiu/baoyu-design/git/trees/HEAD?recursive=1" --jq '[.tree[].path|select(test("\\.(ts|mjs|js)$"))]|length'   # 67 executable files
gh api repos/JimLiu/baoyu-design/releases --jq 'length'   # 0
```

(On the catalog's "baoyu" question: this is **JimLiu/baoyu-design** — Jim Liu's repo, "Baoyu" his handle. It is *not* the same as a separate "baoyu" skill; treat it as its own entry. It is closely comparable to **huashu-design**, the other HTML-native design skill already in the catalog.)

## What worked

- **Genuinely broad design surface.** ~32 built-in skills span the real design workflow end to end — wireframe → hi-fi → prototype → design system → deck → animated video → export (PDF/PPTX/MP4) → handoff. Few design skills cover this much, and the progressive-disclosure split keeps any one job from loading all of it.
- **Local, owned, versionable output.** Artifacts are self-contained HTML in your repo (`designs/<project>/`), not locked behind `claude.ai/design`. You can diff, fork, and ship them — a real advantage over the hosted product for engineers already in an editor.
- **The point-and-edit localhost loop is the standout idea.** Serving HTML on `localhost` and editing source by annotating the live preview is a tight visual iteration loop that a chat-only or website flow can't easily match — and it cleanly reuses each harness's existing browser/DevTools tooling.
- **Harness-agnostic by design, with real per-tool references.** The craft rules stay tool-independent; only "ask a question / preview / screenshot / verify" are resolved per harness via `references/{claude,cursor,codex}.md`. Clean separation, and Claude Code is first-class.
- **Actual tooling, not just prompts.** Offline `.fig` decode (no Figma account/MCP), an editable-PPTX pipeline, and a design-system compiler+checker move it from "design prompt" to "design tool."

## What didn't work or surprised us

- **It executes a 67-file Node/TS toolchain — the real risk surface.** Unlike a pure-markdown skill, installing this brings shell-invoked `.mjs`/`.ts` agents (gen-pptx with a browser-capture step, the figma decoder, design-system compilers). That is third-party code running on your machine with `npm` deps; it warrants the same supply-chain scrutiny as any dependency, not the "just markdown, safe" assumption skills usually get.
- **Brand-new and unpinned.** Created 2026-06-07 (days old at evaluation), **0 tagged releases** — you install whatever `main` is. Pushes are frequent (active), but there is no stable snapshot and no track record yet.
- **Reproduction claim is unverified and load-bearing.** The whole value proposition is "most of `claude.ai/design`, locally." We did not test it, and "vast majority" is the author's framing — actual parity with the hosted engine is unproven here.
- **Demands the strongest (priciest) model.** The README states it's "a long, demanding design brief … best with Opus 4.8." A large skill payload plus a top-tier model is a real per-run cost, and weaker models degrade the output by the author's own admission.
- **Heavy context footprint.** A `SKILL.md` that orchestrates `system-prompt.md` + 32 built-in skills + per-harness references + scaffolds is a lot of context to manage well; progressive disclosure mitigates but doesn't eliminate this.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (design only) | Drives a structured clarify→context→produce→verify loop with a built-in design-system checker; aims at design-craft quality, not code correctness. Unverified against the hosted engine. |
| Speed | + | One skill covers wireframe→hi-fi→deck→export; the localhost point-and-edit loop shortens visual iteration vs. re-prompting in chat. |
| Maintainability | + / − | HTML artifacts are versionable and owned in-repo (good); the skill itself is brand-new, unversioned (0 releases), and carries a Node/TS toolchain to keep working (ongoing). |
| Safety | − | Ships 67 executable `.ts`/`.mjs` files (gen-pptx, browser capture, figma decode) with npm deps that run locally — a genuine supply-chain surface, unlike pure-markdown design skills. |
| Cost Efficiency | − | Author recommends Opus 4.8 and the payload is large; high per-run token + model cost for top-quality output. |

## Verdict

**CONDITIONAL — strong design capability, but vet the toolchain and pin a commit first.** baoyu-design is one of the most complete HTML-native design skills available: broad workflow coverage, owned/versionable output, a genuinely clever localhost point-and-edit loop, and real tooling (offline Figma decode, editable PPTX, design-system compiler). The reasons to hold short of full ADOPT are concrete: it is days old with zero releases (install a pinned commit, not `main`), its "most of claude.ai/design" claim is unverified, and — unlike the pure-markdown design skills it sits beside — it executes a 67-file Node/TS toolchain that deserves dependency-grade review before you trust it on a real repo. Best paired with Opus 4.8, accepting the cost.

Compared to neighbors: **huashu-design** (19.2K stars) is the closest analog — also HTML-native hi-fi/slides/animation with MP4 export and a design-philosophy framework; it is far more battle-tested by star count, while baoyu-design's differentiators are the explicit `claude.ai/design`-parity goal, the harness-agnostic per-tool references, and the live point-and-edit loop. **impeccable** and **ui-ux-pro-max** are leaner *taste/design-language* skills (pure guidance, no toolchain, lower cost/risk) — pick those if you want aesthetic steering without an executable bench; pick baoyu-design (or huashu-design) when you want the full produce-and-export design pipeline. **open-design** is the heavier platform-scale alternative.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [baoyu-design](https://github.com/JimLiu/baoyu-design) | skill | Run Claude Design locally as a harness-agnostic skill — ~32 built-in design skills (hi-fi, prototype, wireframe, deck, design system, PPTX/MP4 export) producing self-contained HTML, with a localhost point-and-edit loop; ships a 67-file Node/TS toolchain (1.6K stars) | Claude Design lives behind claude.ai/design; want the same design pipeline producing owned, versionable HTML inside a local agent | huashu-design (closest analog, more battle-tested); impeccable, ui-ux-pro-max (leaner, prompt-only); open-design (platform-scale) |
