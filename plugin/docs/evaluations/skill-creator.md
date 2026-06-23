# Evaluation: skill-creator

**Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)
**Stars:** 30,444 (monorepo) | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Reflect (authoring/improving the tools the loop itself uses)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Create, document, and publish Claude Code skills." It is an official Anthropic plugin distributed inside the `claude-plugins-official` marketplace monorepo. Unlike commit-commands (three thin slash-command markdown files), skill-creator is a substantial skill: one `SKILL.md` (~485 lines) plus a `scripts/` directory of Python tooling, three subagent definitions (`grader`, `comparator`, `analyzer`), reference schemas, and an HTML eval viewer.

Mechanically it is a meta-skill — a skill for authoring skills — that drives a full iterative loop rather than just scaffolding a file:

- **Draft.** Interviews the user for intent (what the skill enables, when it should trigger, output format), then writes `SKILL.md` per Anthropic's own skill-writing guidance: progressive disclosure (metadata → body < 500 lines → bundled resources), imperative voice, "explain the why instead of heavy-handed MUSTs," and deliberately "pushy" descriptions to combat skill under-triggering.
- **Test.** Writes 2-3 realistic test prompts to `evals/evals.json`, then spawns paired subagents per test case in the same turn — one *with* the skill, one *baseline* (no skill for new skills, or a snapshot of the old version for improvements) — capturing `total_tokens`/`duration_ms` timing from each task notification.
- **Grade + benchmark.** A grader subagent scores assertions (`scripts/aggregate_benchmark.py` rolls up pass_rate/time/tokens with mean ± stddev and deltas); an analyzer pass surfaces non-discriminating assertions and high-variance evals.
- **Review.** `eval-viewer/generate_review.py` (471 lines) launches a local HTML viewer with an Outputs tab (per-test outputs + feedback boxes) and a Benchmark tab; feedback is collected to `feedback.json`. Supports `--static` for headless/Cowork environments.
- **Optimize description.** `scripts/run_loop.py` runs an automated description-tuning loop: splits trigger-eval queries 60/40 train/test, evaluates each query 3x via `claude -p`, proposes improved descriptions, and selects `best_description` by held-out test score to avoid overfitting.
- **Package.** `scripts/package_skill.py` validates (via `quick_validate.py`) then zips the folder into a distributable `.skill` file.

It also carries explicit environment branches for Claude Code, Claude.ai (no subagents), and Cowork (no display), plus a "Principle of Lack of Surprise" safety clause refusing malware/deceptive skills.

## How we tested it

**Evidence:** REVIEW

Source review of the plugin **as installed on this machine**, plus one real script execution. The plugin is present locally under both `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/` and the cache, so this is the shipped artifact, not a README paraphrase. I read the full `SKILL.md`, `plugin.json`, the agent definitions, and the script docstrings, and confirmed repo identity via `gh api`. I then **actually ran** the bundled validator against a real skill directory to confirm the Python tooling executes (not just that it exists).

I did **not** drive the full draft→test→benchmark→optimize loop end-to-end (that requires an interactive multi-turn session with subagents spawning paired runs and a human reviewing the HTML viewer), so claims about the eval/optimize loop rest on reading the scripts and SKILL.md, which are transparent. The packaging and triggering-optimization scripts were not executed.

```bash
# Repo identity (catalog entry was UNLINKED) and provenance:
gh api repos/anthropics/claude-plugins-official -q '{full_name,license:.license.spdx_id,stars:.stargazers_count}'
#   -> anthropics/claude-plugins-official, Apache-2.0, 30444
find ~/.claude/plugins -ipath '*skill-creator*'   # installed: marketplace checkout + cache

# Read the real artifacts:
.../skill-creator/.claude-plugin/plugin.json
.../skill-creator/skills/skill-creator/SKILL.md
.../skill-creator/skills/skill-creator/{scripts/*.py, agents/*.md, references/schemas.md, eval-viewer/generate_review.py}

# Actually executed the bundled validator against a real skill folder:
python3 -c "from scripts.quick_validate import validate_skill; print(validate_skill('.'))"
#   -> (True, 'Skill is valid!')
python3 --version   # -> Python 3.11.4 (scripts run on the host toolchain)
```

Repo verification: confirmed. The plugin ships from `anthropics/claude-plugins-official` at `plugins/skill-creator/`. The catalog entry one-liner ("Create, document, and publish") is slightly stale relative to the shipped description, which now emphasizes *measuring* skill performance (evals + benchmarks + triggering optimization), not just publishing.

## What worked

- **Official, first-party, actively maintained.** Apache-2.0, authored by Anthropic, in the 30k-star official marketplace pushed the same day as this evaluation. It is the canonical source for *how Anthropic itself says skills should be written* — the SKILL.md doubles as authoritative guidance (progressive disclosure, the "pushy description" under-triggering fix, "explain the why over caps-lock MUSTs").
- **Genuinely additive, not just scaffolding.** The eval/benchmark/description-optimization loop is the real value. Most skill-authoring tools stop at "write a SKILL.md"; this one closes the loop with paired with-skill/baseline runs, quantitative pass-rate/token/time deltas, and a held-out-test-selected description optimizer — exactly the Reflect-stage rigor this catalog is built around.
- **The bundled scripts actually run.** `quick_validate.validate_skill('.')` returned `(True, 'Skill is valid!')` on the host Python 3.11 with no extra setup beyond `pyyaml`. The tooling is real and importable, not pseudocode.
- **Strong environment awareness.** Explicit, correct branches for Claude Code (subagents), Claude.ai (no subagents → serial self-run, skip benchmarking), and Cowork (no display → `--static` HTML). Few community skills handle these splits.
- **Built-in safety clause.** "Principle of Lack of Surprise" instructs refusal of malware/exfiltration/deceptive skills — appropriate for a meta-tool that generates executable artifacts.

## What didn't work or surprised us

- **Heavyweight for the simple case.** If a user just wants to capture a one-paragraph workflow as a SKILL.md, the full interview→eval→benchmark→optimize machinery is overkill. The skill does say "if the user is like 'just vibe with me,' you can do that," but the default posture is the heavy loop.
- **Description-optimization loop has real cost.** `run_loop.py` runs each trigger-eval query 3x across up to 5 iterations on train+test splits via `claude -p` subprocess calls — that is many model invocations. Valuable, but not free; the SKILL.md itself warns "this will take some time."
- **External-toolchain dependencies for the advanced path.** The full loop needs Python, `pyyaml`, subagents, a browser/display (or `--static`), and the `claude` CLI for description optimization. On a constrained host the value degrades to "a very good skill-writing guide + a validator + a packager."
- **Naming collision in the ecosystem.** This is one of *three* skill-authoring tools visible in the local install (Anthropic `skill-creator`, plus community `write-a-skill` and superpowers `writing-skills`), and the `plugin-dev` plugin separately ships `skill-development` + a `skill-reviewer` agent. Users must pick deliberately; keyword overlap is high.
- **Catalog one-liner understates it.** "Create, document, and publish" misses the evals/benchmark/triggering-optimization capability that is the actual differentiator.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Paired with-skill/baseline runs + grader assertions + benchmark deltas give an objective measure that a skill actually improves outputs, not just vibes |
| Speed | + | Scaffolds SKILL.md + bundled-script structure and packages a `.skill` in one guided flow; but the full eval loop trades author time for rigor |
| Maintainability | + | Encodes Anthropic's canonical skill structure (progressive disclosure, < 500-line body, references/scripts/assets split) so authored skills stay readable and AI-navigable |
| Safety | + | Explicit refusal clause for malicious/deceptive skills; validator gates packaging |
| Cost Efficiency | neutral | Authored skills can bundle scripts to avoid re-deriving work (saves future tokens), but the description-optimization loop itself spends many `claude -p` invocations |

## Verdict

**ADOPT (for anyone authoring or maintaining skills); KEEP for this catalog**

This is the right tool for the job and the job is squarely in scope for this repo, which itself ships five skills and a plugin and is actively writing more. It is first-party, Apache-2.0, and the canonical statement of how Anthropic wants skills written — the SKILL.md alone is worth reading as a style guide. Crucially it goes beyond scaffolding into the Reflect-stage rigor the catalog values: quantitative with-skill-vs-baseline benchmarks and a held-out-test description optimizer that directly attacks the most common skill failure mode (under-triggering). The bundled validator runs cleanly on the host toolchain, confirming the tooling is real.

It is ADOPT rather than unconditional only in the sense that the heavy eval/optimize loop is opt-in: for a quick one-off skill the full machinery is more than needed, and the description-optimization loop has non-trivial model cost. Use the lightweight draft path for trivial skills and the full loop when a skill will be invoked repeatedly and triggering accuracy matters.

**Versus alternatives:**
- **plugin-dev** (catalog overlap): complementary, not competing. plugin-dev builds *plugins* (commands, agents, hooks, MCP, plugin.json structure) and includes a `skill-development` skill + `skill-reviewer` agent for the skill *inside* a plugin; skill-creator is the deeper, dedicated skill-authoring loop with evals/benchmarks/packaging. Use plugin-dev for plugin scaffolding, skill-creator when the skill quality itself is the deliverable.
- **openskills**: orthogonal — a cross-editor *installer/loader* for SKILL.md files (Cursor, Codex, Aider), not an authoring tool. skill-creator writes the skill; openskills distributes it across non-Claude agents.
- **skill-reviewer** (plugin-dev agent): a one-shot quality/triggering *reviewer* of an existing skill. skill-creator subsumes this via its description-optimization loop and grader, but skill-reviewer is a lighter touch when you only want a critique, not a full eval harness.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) | plugin | Official Anthropic skill for authoring, eval-benchmarking, triggering-optimizing, and packaging Claude Code skills | Authoring high-quality skills with objective with-skill-vs-baseline measurement, not just scaffolding a SKILL.md | plugin-dev (complementary: plugin-dev = plugin scaffolding, skill-creator = deep skill authoring); openskills (orthogonal: install/distribute); plugin-dev's skill-reviewer (lighter critique) |
