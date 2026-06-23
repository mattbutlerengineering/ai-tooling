# Evaluation: skill-creator

**Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)
**Stars:** 30,648 (monorepo) | **Last updated:** 2026-06-23 (marketplace `pushed_at`) | **License:** Apache-2.0
**Last verified:** 2026-06-22
**Dev loop stage:** Reflect (authoring/improving the tools the loop itself uses)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Create, document, and publish Claude Code skills." It is an official Anthropic plugin distributed inside the `claude-plugins-official` marketplace monorepo. Unlike commit-commands (three thin slash-command markdown files), skill-creator is a substantial skill: one `SKILL.md` (~485 lines) plus a `scripts/` directory of Python tooling, three subagent definitions (`grader`, `comparator`, `analyzer`), reference schemas, and an HTML eval viewer.

Mechanically it is a meta-skill — a skill for authoring skills — that drives a full iterative loop rather than just scaffolding a file:

- **Draft.** Interviews the user for intent (what the skill enables, when it should trigger, output format), then writes `SKILL.md` per Anthropic's own skill-writing guidance: progressive disclosure (metadata → body < 500 lines → bundled resources), imperative voice, "explain the why instead of heavy-handed MUSTs," and deliberately "pushy" descriptions to combat skill under-triggering. There is no `init_skill.py` scaffolder — the directory/SKILL.md is authored by the agent itself from the anatomy template in `SKILL.md`; the runnable deterministic tooling is the *validator* and *packager* described below.
- **Test.** Writes 2-3 realistic test prompts to `evals/evals.json`, then spawns paired subagents per test case in the same turn — one *with* the skill, one *baseline* (no skill for new skills, or a snapshot of the old version for improvements) — capturing `total_tokens`/`duration_ms` timing from each task notification.
- **Grade + benchmark.** A grader subagent scores assertions into `grading.json`; `scripts/aggregate_benchmark.py` rolls those up into `benchmark.json`/`benchmark.md` with pass_rate/time/tokens mean ± stddev and a with-skill-vs-baseline delta; an analyzer pass surfaces non-discriminating assertions and high-variance evals.
- **Review.** `eval-viewer/generate_review.py` (471 lines) launches a local HTML viewer with an Outputs tab (per-test outputs + feedback boxes) and a Benchmark tab; feedback is collected to `feedback.json`. Supports `--static` for headless/Cowork environments.
- **Optimize description.** `scripts/improve_description.py` + `scripts/run_loop.py` run an automated description-tuning loop: split trigger-eval queries train/test, evaluate each query via `scripts/run_eval.py` (which shells out to `claude -p` and detects whether the skill triggered from the stream), propose improved descriptions, and select the best by held-out test score to avoid overfitting.
- **Package.** `scripts/package_skill.py` validates (via `scripts/quick_validate.py`) then zips the folder into a distributable `.skill` file, excluding `__pycache__`, `node_modules`, `*.pyc`, `.DS_Store`, and the root `evals/` dir.

It also carries explicit environment branches for Claude Code, Claude.ai (no subagents), and Cowork (no display), plus a "Principle of Lack of Surprise" safety clause refusing malware/deceptive skills.

## How we tested it

**Evidence:** MEASURED

**Ran the deterministic Python tooling end-to-end** on 2026-06-22 (macOS arm64, Python 3.11.4, pyyaml 6.0.3) against the plugin **as installed on this machine** (`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/`) — the shipped artifact, not a README paraphrase. All work happened in a `mktemp -d` temp dir (`/tmp/skill-creator-eval.XXXXXX`) that was **deleted afterward**; nothing was written into this repo. The scripts use package-relative imports (`from scripts.quick_validate import ...`), so they must be invoked as modules from the skill root — I ran them with `cd <skill-root> && python3 -m scripts.<name> <tmp>/...`.

**1) Scaffold → validate → package (the happy path).** I hand-authored a brand-new throwaway skill `git-tidy/` per the anatomy template in `SKILL.md` (valid frontmatter + `scripts/`, `references/`, `assets/` subdirs), then:

```
git-tidy/SKILL.md
git-tidy/references/notes.md
git-tidy/scripts/list_merged.sh
```

- `python3 -m scripts.quick_validate <tmp>/git-tidy` → `Skill is valid!` (exit 0), 34 ms.
- `python3 -m scripts.package_skill <tmp>/git-tidy <tmp>/dist` → ran validation first (`✅ Skill is valid!`), then produced `git-tidy.skill`, 36 ms. The `.skill` is a deflate zip; `unzip -l` confirmed it contained exactly the 3 source files (501 bytes, build artifacts excluded as designed).

**2) Validator discrimination — good vs. 6 deliberately-broken skills (the A/B oracle).** I created six broken variants and ran the same validator; **all 6 were rejected (exit 1) with a correct, distinct reason**, while the good skill above passed:

| Broken skill | Validator verdict (verbatim) |
|---|---|
| missing `description` | `Missing 'description' in frontmatter` |
| `name: Broken_Name` (not kebab-case) | `Name 'Broken_Name' should be kebab-case (lowercase letters, digits, and hyphens only)` |
| angle brackets in description | `Description cannot contain angle brackets (< or >)` |
| unknown key `author:` | `Unexpected key(s) in SKILL.md frontmatter: author. Allowed properties are: allowed-tools, compatibility, description, license, metadata, name` |
| no frontmatter | `No YAML frontmatter found` |
| no `SKILL.md` | `SKILL.md not found` |

`package_skill` on the missing-`description` skill **refused to zip it** — it printed `❌ Validation failed: Missing 'description' in frontmatter` and exited 1; afterward `<tmp>/dist` contained only the earlier good `git-tidy.skill` and no broken artifact. So the packager genuinely gates on validation, not just decorates it.

**3) Benchmark aggregator — with-skill-vs-baseline rollup.** The grader that produces `grading.json` needs an LLM, but the rollup math in `aggregate_benchmark.py` is pure and headless-drivable. I built the documented benchmark layout (`eval-0/with_skill/run-{1,2}/grading.json`, `eval-0/without_skill/run-{1,2}/grading.json`) with synthetic gradings (with-skill 2/2 pass, baseline 0/2 pass) and ran:

```
python3 -m scripts.aggregate_benchmark <bd> --skill-name git-tidy --skill-path <tmp>/git-tidy -o <bd>/benchmark.json
#   Summary:
#     With Skill: 100.0% pass rate
#     Without Skill: 0.0% pass rate
#     Delta:         +1.00
```

It wrote both `benchmark.json` (with per-run `result`/`expectations` blocks and a `delta`) and a human-readable `benchmark.md`. This confirms the quantitative with-skill-vs-baseline mechanism the catalog values is real, computed, and correct on known inputs.

**4) Static eval viewer (headless).** `generate_review.py` discovers runs by finding directories containing an `outputs/` subdir. With a minimal workspace (`iteration-1/prune-merged/{with_skill,without_skill}/outputs/result.txt` + `transcript.md`) and the `benchmark.json` from step 3:

```
python3 eval-viewer/generate_review.py <tmp>/git-tidy-workspace/iteration-1 \
  --skill-name git-tidy --benchmark <bd>/benchmark.json --static <tmp>/review.html
#   Static viewer written to: <tmp>/review.html
```

It produced a self-contained 47 KB `<title>Eval Review</title>` HTML page carrying both run labels and the Benchmark tab (10 marker hits for `with_skill`/`without_skill`/`prune-merged`/`Benchmark`) — i.e. the `--static`/Cowork path works without a browser or server.

```bash
SC=~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator
TMP=$(mktemp -d)
# ... author <TMP>/git-tidy/ from the SKILL.md anatomy template ...
cd "$SC"
python3 -m scripts.quick_validate "$TMP/git-tidy"                 # Skill is valid! (exit 0)
python3 -m scripts.package_skill  "$TMP/git-tidy" "$TMP/dist"     # -> git-tidy.skill (validated zip)
python3 -m scripts.quick_validate "$TMP/broken-nodesc"           # exit 1 + reason (6 broken variants tested)
python3 -m scripts.aggregate_benchmark "$TMP/.../benchmark" --skill-name git-tidy  # Delta: +1.00
python3 eval-viewer/generate_review.py "$TMP/.../iteration-1" --static "$TMP/review.html"
gh api repos/anthropics/claude-plugins-official -q '{full_name,license:.license.spdx_id,stars:.stargazers_count}'
#   -> anthropics/claude-plugins-official, Apache-2.0, 30648
rm -rf "$TMP"   # temp dir deleted; no files written into this repo
```

**What was NOT exercised (needs a live model / interactive session):** the Draft interview, the paired with-skill/baseline subagent *task runs*, the LLM **grader** that writes the real `grading.json` (I supplied synthetic gradings to drive the rollup), and the description-optimization loop (`run_eval.py`/`improve_description.py`/`run_loop.py`), which shell out to `claude -p` per query across train/test splits and need model credentials and a `.claude/` project root. Those are inherently multi-turn/agentic and not headless-drivable; their behaviour rests on reading the scripts and `SKILL.md`, which are transparent. The deterministic backbone — scaffold layout, validation, packaging, benchmark rollup, and the static viewer — was run end-to-end with captured output and a good-vs-broken A/B.

Repo verification: confirmed via `gh api`. The plugin ships from `anthropics/claude-plugins-official` at `plugins/skill-creator/`, Apache-2.0, 30,648 stars. The catalog one-liner ("Create, document, and publish") is slightly stale relative to the shipped `plugin.json` description, which emphasizes *measuring* skill performance (evals + benchmarks + variance analysis), not just publishing.

## What worked

- **The deterministic tooling runs cleanly and is genuinely useful — measured.** `quick_validate` + `package_skill` execute in ~35 ms on the host Python 3.11 with only `pyyaml`, validate a real scaffolded skill, and produce a correct excluded-artifact `.skill` zip. Not pseudocode — importable, runnable, fast.
- **The validator discriminates — measured A/B.** 6/6 deliberately-broken skills were rejected with correct distinct reasons (missing description, non-kebab name, angle brackets, unknown key, no frontmatter, no SKILL.md) while the good skill passed, and `package_skill` *refused to zip the invalid one*. The packaging gate is real, not cosmetic.
- **The with-skill-vs-baseline benchmark is real and correct — measured.** `aggregate_benchmark.py` rolled synthetic with-skill (2/2) vs baseline (0/2) gradings into a `+1.00` pass-rate delta with mean ± stddev and emitted both `benchmark.json` and `benchmark.md`. This is the Reflect-stage quantitative rigor the catalog is built around, and it computes correctly on known inputs.
- **Headless review path works — measured.** `generate_review.py --static` produced a self-contained 47 KB HTML report (Outputs + Benchmark tabs) with no server/browser, validating the documented Cowork branch.
- **Official, first-party, actively maintained.** Apache-2.0, authored by Anthropic, in the 30k-star official marketplace pushed within a day of this evaluation. The `SKILL.md` doubles as the canonical statement of *how Anthropic itself says skills should be written* (progressive disclosure, the "pushy description" under-triggering fix, "explain the why over caps-lock MUSTs").
- **Built-in safety clause.** "Principle of Lack of Surprise" instructs refusal of malware/exfiltration/deceptive skills — appropriate for a meta-tool that generates executable artifacts.

## What didn't work or surprised us

- **Scripts only run as modules from the skill root.** Package-relative imports (`from scripts.quick_validate import ...`, `from scripts.utils import ...`) mean `python3 scripts/package_skill.py` fails with `ModuleNotFoundError: No module named 'scripts'`; you must `cd` to the skill root and use `python3 -m scripts.package_skill`. The script docstrings still show the old `python utils/package_skill.py ...` invocation, which no longer matches the on-disk layout — a minor doc/path drift worth knowing before you wire these into a script.
- **No `init_skill.py` scaffolder.** The skill is authored by the agent from the `SKILL.md` anatomy template, not stamped out by a CLI. That is fine for an agent-driven workflow but means the "scaffold" step is not itself a runnable script — only validate/package/benchmark are.
- **Heavyweight for the simple case.** For a one-paragraph workflow, the full interview→eval→benchmark→optimize machinery is overkill. The skill allows a lightweight "just vibe with me" path, but the default posture is the heavy loop.
- **The eval/optimize loop has real model cost.** `run_eval.py` spawns `claude -p` per query (default 3 runs/query, 10 parallel workers); `run_loop.py` iterates that over train/test splits. Valuable, but many model invocations — the `SKILL.md` itself warns "this will take some time." Needs `claude` CLI + credentials + a `.claude/` project root, none of which is headless-drivable here.
- **Naming collision in the ecosystem.** One of several skill-authoring tools visible locally (Anthropic `skill-creator`, community `write-a-skill`, superpowers `writing-skills`, and `plugin-dev`'s `skill-development` + `skill-reviewer`). Users must pick deliberately; keyword overlap is high.
- **Catalog one-liner understates it.** "Create, document, and publish" misses the evals/benchmark/triggering-optimization capability that is the actual differentiator.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Measured: validator rejects 6/6 broken skills with correct reasons and packaging refuses to zip an invalid one; benchmark aggregator computes a correct +1.00 with-skill-vs-baseline pass-rate delta — an objective measure that a skill actually improves outputs, not vibes |
| Speed | + | Measured: validate + package run in ~35 ms each and produce a correct `.skill` zip in one guided flow; the full eval loop trades author time for rigor |
| Maintainability | + | Encodes Anthropic's canonical skill structure (progressive disclosure, < 500-line body, references/scripts/assets split) so authored skills stay readable and AI-navigable; validator gates frontmatter hygiene |
| Safety | + | Explicit refusal clause for malicious/deceptive skills; validator + packager gate distribution (measured: invalid skill is not packaged) |
| Cost Efficiency | neutral | Validate/package/benchmark-rollup are free (no LLM, measured); the description-optimization loop spends many `claude -p` invocations (not run here) |

## Verdict

**ADOPT (for anyone authoring or maintaining skills); KEEP for this catalog**

This is the right tool for the job and the job is squarely in scope for this repo, which itself ships five skills and a plugin and is actively writing more. It is first-party, Apache-2.0, and the canonical statement of how Anthropic wants skills written — the `SKILL.md` alone is worth reading as a style guide. Crucially it goes beyond scaffolding into the Reflect-stage rigor the catalog values, and that rigor is now **measured end-to-end**: the validator discriminates good from broken skills (6/6 with correct reasons), packaging gates on it, and `aggregate_benchmark.py` computes a correct quantitative with-skill-vs-baseline delta with the static HTML reviewer rendering headlessly. The deterministic backbone runs cleanly on the host toolchain in tens of milliseconds with only `pyyaml`.

It is ADOPT rather than unconditional only in the sense that the heavy eval/optimize loop is opt-in and model-costed: for a quick one-off skill the full machinery is more than needed, and the description-optimization loop (which needs a live model and was not driven here) has non-trivial `claude -p` cost. Use the lightweight draft path for trivial skills and the full loop when a skill will be invoked repeatedly and triggering accuracy matters.

**Versus alternatives:**
- **plugin-dev** (catalog overlap): complementary, not competing. plugin-dev builds *plugins* (commands, agents, hooks, MCP, plugin.json structure) and includes a `skill-development` skill + `skill-reviewer` agent for the skill *inside* a plugin; skill-creator is the deeper, dedicated skill-authoring loop with evals/benchmarks/packaging. Use plugin-dev for plugin scaffolding, skill-creator when the skill quality itself is the deliverable.
- **openskills**: orthogonal — a cross-editor *installer/loader* for SKILL.md files (Cursor, Codex, Aider), not an authoring tool. skill-creator writes the skill; openskills distributes it across non-Claude agents.
- **skill-reviewer** (plugin-dev agent): a one-shot quality/triggering *reviewer* of an existing skill. skill-creator subsumes this via its description-optimization loop and grader, but skill-reviewer is a lighter touch when you only want a critique, not a full eval harness.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) | plugin | Official Anthropic skill for authoring, eval-benchmarking, triggering-optimizing, and packaging Claude Code skills | Authoring high-quality skills with objective with-skill-vs-baseline measurement, not just scaffolding a SKILL.md | plugin-dev (complementary: plugin-dev = plugin scaffolding, skill-creator = deep skill authoring); openskills (orthogonal: install/distribute); plugin-dev's skill-reviewer (lighter critique) |
