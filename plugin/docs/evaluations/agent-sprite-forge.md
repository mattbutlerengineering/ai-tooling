# Evaluation: agent-sprite-forge

**Repo:** [0x0funky/agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge)
**Stars:** 2,876 | **Last updated:** 2026-05-05 (pushed; created 2026-04-23) | **License:** MIT
**Dev loop stage:** None of the software dev loop. This is a **game-art asset-generation pipeline**, not a coding tool — it produces sprite sheets, tilemaps, and engine scenes, not application code. The nearest mapping is "Implement" for a game project's *art* pipeline, but it does not touch the Plan/Implement/Verify/Review/Ship loop this catalog is organized around.
**Layer:** Tooling — two Codex skills (`SKILL.md` + Python scripts) that orchestrate built-in image generation plus deterministic local post-processing (numpy/Pillow).

---

## What it does

"Codex skills for game-ready 2D sprites, layered maps, and engine-ready prototypes." Agent Sprite Forge is a **Codex-first** (OpenAI) workflow for generating 2D game art. You ask in natural language; the agent plans an asset pipeline, calls built-in `image_gen` to render raw sheets on a solid-magenta background, then runs local Python processors to chroma-key the background out, extract and align frames, slice prop packs, validate, and export transparent PNG/GIF assets plus Godot/Unity scene wiring.

As inspected, it ships **two skills**: `generate2dsprite` (characters, NPCs, creatures, spells, projectiles, impacts, idle/walk/attack animation sheets, transparent GIF export) and `generate2dmap` (ground bases, dressed references, prop packs, y-sort placement, collision zones, layered previews, Godot TileMap handoff). Each skill is a `SKILL.md` plus an OpenAI agent manifest (`agents/openai.yaml`), reference contracts (e.g. `layered-map-contract.md`, `prompt-rules.md`, `modes.md`), and Python scripts (`generate2dsprite.py`, `extract_prop_pack.py`, `compose_layered_preview.py`). The only runtime dependency is `requirements.txt`: `numpy>=1.26`, `Pillow>=10.0`. The README showcases full playable prototypes (Unity WebGL "Summon Survivors," Godot tower defense, a JS Pokémon-like) assembled from these assets.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No skill was installed into Codex, no `image_gen` call was made, and no sprite/map was generated. There is no sandbox here to run an OpenAI image pipeline, and doing so would incur generation cost. Every claim below comes from the repository (GitHub metadata, README, full recursive file tree, the two `SKILL.md` frontmatters, `requirements.txt`), not from observed output. The showcase prototypes and "engine-ready" framing are the author's README claims, not anything I produced or measured.

```bash
gh api repos/0x0funky/agent-sprite-forge --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,topics:.topics,lang:.language}'
# desc: null | stars 2876 | forks 283 | Python | topics: agent-skills, codex, pixel-art, sprite-generator
gh api repos/0x0funky/agent-sprite-forge/readme --jq '.content' | base64 -d        # English README (also zh-TW/zh-CN/ja/ko)
gh api "repos/0x0funky/agent-sprite-forge/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # 2 skills: generate2dsprite, generate2dmap
gh api repos/0x0funky/agent-sprite-forge/contents/skills/generate2dsprite/SKILL.md --jq '.content' | base64 -d   # asset_type/action/view/sheet params
gh api repos/0x0funky/agent-sprite-forge/commits --jq 'length'    # 28 (page-1 cap)
gh api repos/0x0funky/agent-sprite-forge/releases --jq 'length'   # 0
```

## What worked

- **Genuinely well-engineered for its niche.** The `generate2dsprite` SKILL.md is a serious piece of prompt-and-pipeline design: a typed parameter surface (`asset_type`, `action`, `view`, `sheet`, `frames`, `bundle`, `effect_policy`, `anchor`, `margin`), explicit agent rules (don't pack unrelated actions into one atlas, keep wide FX out of body sheets, QC each grid before assembling the engine atlas), and reference contracts. This is not a prompt dump.
- **Hybrid generate-then-deterministic-process design is the right pattern.** Image generation produces raw sheets; local numpy/Pillow scripts handle the parts that must be exact (chroma-key, frame extraction, alignment, transparent export, QA metadata). Pushing determinism to scripts and creativity to the model is exactly how you make AI art reproducible.
- **End-to-end ambition with showcase artifacts.** Playable Unity WebGL and Godot prototypes link out from the README, showing the assets actually wire into engines — not just isolated PNGs.
- **Cheap, transparent dependencies.** Two pure-Python libs (numpy, Pillow). No heavyweight ML stack to install locally; the model work is delegated to Codex's built-in `image_gen`.

## What didn't work or surprised us

- **Out of scope for this catalog.** This is a game *art-asset* generator, not a software development tool. It moves no software dev-loop quality signal — it does not help you write, test, review, or ship application code. Its place in CATALOG.md (already present) is as a domain-specific curiosity alongside Claude-Code-Game-Studios, not as a tool you'd reach for in a normal engineering workflow.
- **Codex-locked.** The skills target OpenAI Codex and its built-in `image_gen` (`agents/openai.yaml`, magenta-chroma raw-sheet convention). Unlike the cross-editor skill packs in this catalog, there is no Claude Code / multi-tool install path; adopting it means adopting Codex's image pipeline.
- **No releases, no eval data.** 0 tagged releases (you install `main`), and no benchmark or eval harness — quality of output is asserted via showcase screenshots, not measured. Sprite quality is inherently subjective and model-dependent.
- **Generation cost is unbounded and unstated.** A full prototype's worth of sheets is many `image_gen` calls; the README sells the breadth (heroes, enemies, bosses, FX, HUD) without flagging the per-asset cost of generating it all.
- **Young and single-author.** Two months old, ~28 commits, one primary author — promising but unproven longevity for a tool you'd build an art pipeline on.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | n/a (out of scope) | "Correctness" here means visual asset quality, not code correctness; the deterministic post-processing scripts make the *processing* step reproducible, but there is no code-quality dimension. |
| Speed | + (for game art only) | Generating a full sprite/map asset set from natural language is far faster than hand-pixeling or sourcing art — but this is art-pipeline speed, not dev-loop speed. |
| Maintainability | n/a | Produces art assets, not source code; no effect on a codebase's maintainability. The skills themselves are cleanly structured. |
| Safety | neutral | Local scripts are pure numpy/Pillow image math; the network/cost surface is Codex's `image_gen`. No host or repo risk beyond writing output files. |
| Cost Efficiency | − | Many image-generation calls per prototype; cost scales with asset volume and is not surfaced in the docs. |

## Verdict

**SKIP (out of scope) — flag as domain-specific game-art tooling, not a dev-loop coding tool.** Agent Sprite Forge is a well-designed, genuinely capable Codex skill pack for generating 2D game art — typed parameters, sensible agent rules, and a smart generate-then-deterministically-process pipeline. But this catalog is an operating manual for AI-assisted *software* development, and sprite/tilemap generation moves none of its quality signals. It earns a catalog row as a domain-specific curiosity (it already has one), but it is not something a backend/web/infra engineer should adopt, and it is not comparable to the language and workflow skill packs the catalog otherwise tracks. If you are specifically building a 2D game *and* already live in Codex, it is worth a look; otherwise skip.

Compared to neighbors: its only true peer is **Claude-Code-Game-Studios** (49 agents / 72 skills mimicking a game-dev studio) — both are game-domain, both out of the core dev loop. Against the *skill-pack* neighbors that actually belong here — **cc-skills-golang**, **SwiftUI-Agent-Skill**, **mattpocock/skills** — it differs in kind: those improve how agents write production application code; agent-sprite-forge produces art assets and is Codex-locked. The catalog's existing "— (domain-specific: game dev)" overlap marker is correct.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-sprite-forge](https://github.com/0x0funky/agent-sprite-forge) | skill | Codex skill pair that generates and post-processes 2D game art — sprite sheets, animated GIFs, layered tilemaps, and Godot/Unity scene handoff (out of dev-loop scope) | Game projects need AI-generated, engine-ready 2D art assets via a generate-then-deterministically-clean pipeline | Claude-Code-Game-Studios (domain-specific: game dev) |
