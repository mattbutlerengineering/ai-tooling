# Evaluation: humanizer

**Repo:** [blader/humanizer](https://github.com/blader/humanizer)
**Stars:** 25,042 | **Last updated:** 2026-06-07 | **License:** MIT
**Dev loop stage:** Ship (prose artifacts — docs, PRs, commit messages, release notes, blog posts); touches Review when the artifact under review is prose
**Layer:** Process

---

## What it does

Removes signs of AI-generated writing from text. The mechanism is a single large, self-contained Claude Code skill: a 34 KB `SKILL.md` (version 2.8.0) carrying 33 numbered patterns drawn from Wikipedia's "Signs of AI writing" guide (maintained by WikiProject AI Cleanup), plus a voice-calibration mode, a "personality and soul" section, detection guidance, and a draft → audit → final process loop.

When invoked, the agent scans a draft against the 33 patterns and rewrites to eliminate them. Unlike a thin deny-list, each pattern is structured as **Words to watch + Problem statement + Before/After rewrite**, so the model gets both the trigger vocabulary and a worked transform. The patterns are grouped into six families:

- **Content patterns (1–6):** inflated significance/legacy puffery, notability name-dropping, superficial `-ing` analyses, promotional language ("nestled", "vibrant", "stunning"), vague attributions / weasel words, formulaic "Challenges and Future Prospects" sections.
- **Language and grammar (7–13):** the canonical AI-vocabulary list (delve, tapestry, testament, underscore, intricate, vibrant…), copula avoidance, negative parallelisms ("not X, but Y"), rule-of-three overuse, elegant variation (synonym cycling), false ranges, passive voice / subjectless fragments.
- **Style (14–19):** a hard em-dash/en-dash ban, boldface overuse, inline-header vertical lists, title-case headings, emojis, curly quotes.
- **Communication (20–22):** collaborative artifacts, knowledge-cutoff disclaimers, sycophantic tone.
- **Filler and hedging (23–33):** filler phrases, excessive hedging, generic positive conclusions, hyphenated-pair overuse, persuasive-authority tropes, signposting, fragmented headers, diff-anchored writing, manufactured staccato drama, aphorism formulas, conversational rhetorical openers.

Two features distinguish it from the sibling prose skills. First, a **voice-calibration mode**: given a sample of the user's own prior writing, the skill analyzes sentence-length patterns, word-choice level, and punctuation habits, then matches that voice rather than imposing a default. Second, an explicit **`What NOT to flag` (false positives)** section plus a `Signs of human writing (preserve these)` list, and a standing instruction to look for *clusters* of tells rather than punishing isolated ones ("a single em dash means nothing… em dashes plus rule-of-three plus *vibrant tapestry* plus a 'Conclusion' section is a confession"). The "personality and soul" section also warns that sterile, voiceless writing is its own AI tell and is gated to apply only to blog/essay/opinion text, not encyclopedic, technical, legal, or reference prose.

## How we tested it

**Evidence:** REVIEW

Source-grounded review. I did not install the skill or run it on a live draft. I read the repository over the GitHub API: the repo metadata, the full file tree (`AGENTS.md`, `LICENSE`, `README.md`, `SKILL.md`), the complete `SKILL.md` frontmatter and the opening pattern catalog, and the full heading map of all 33 patterns plus the detection-guidance and process sections. I then reasoned about the method against the catalog framework and compared it directly to the existing `stop-slop` evaluation (the prose-quality sibling) and the `taste-skill` catalog entry. The before/after pairs quoted above are the author's own examples shipped in `SKILL.md`, not outputs I generated. I ran no rewrites of my own; any judgement about output quality below is reasoning about the rules, not a measured result.

```bash
gh search repos humanizer skill --json fullName,description,stargazersCount,url   # confirm canonical repo
gh api repos/blader/humanizer --jq '{stars,license,description,pushed_at,created_at}'
gh api "repos/blader/humanizer/git/trees/HEAD?recursive=1" --jq '.tree[] | "\(.type)\t\(.size)\t\(.path)"'
gh api "repos/blader/humanizer/contents/SKILL.md" --jq '.content' | base64 -d   # frontmatter + catalog + heading map
grep -inE "humanizer|taste-skill|stop-slop" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Best-provenanced of the three prose skills.** 25,042 stars (more than double stop-slop's 11.4K), MIT, named author, active to Jun 2026, version 2.8.0, and a documented source of authority (Wikipedia's WikiProject AI Cleanup guide) rather than one author's taste. The catalog entry is already correctly linked to this repo.
- **Pattern format is the right shape for an LLM.** Each of the 33 patterns pairs explicit trigger vocabulary with a Before/After rewrite. That is more applicable than taste-skill's abstract "good taste" framing and richer than a bare phrase list, because the worked transform shows the model what "fixed" looks like.
- **It has the carve-out stop-slop lacks.** The `What NOT to flag` section, the `Signs of human writing` preserve-list, and the cluster-not-isolated rule directly mitigate the main failure mode of this skill class (mechanical over-editing). The "personality and soul" section is explicitly gated off for technical/legal/reference text. This is the single most important differentiator for a code-tooling context, where precise absolutes and passive constructions are often correct.
- **Voice calibration is a genuine feature.** Matching the user's own writing sample, instead of imposing a house style, is a real improvement over a one-size deny-list and reduces the "all humanized text sounds the same" problem.
- **"Rewrite, don't delete; cover everything the original covers" is a sound guardrail** against the common humanizer failure of silently dropping content while stripping AI-isms.

## What didn't work or surprised us

- **The dev-loop surface area is narrow.** Like stop-slop, this is a prose tool in a code-tooling catalog. It moves no code-, test-, or build-correctness signal. Its reach is the prose an engineer's agent emits: PR descriptions, commit bodies, READMEs/docs, release notes, review comments, blog posts. Real value there, but a thin slice of the inner loop.
- **No progressive disclosure — it is one 34 KB file.** Unlike stop-slop's lean `SKILL.md` + on-demand `references/`, humanizer loads its entire 33-pattern catalog whenever the skill fires. The always-loaded footprint is larger, and most of the 33 patterns will be irrelevant to any given short artifact (a commit message will not have a "Challenges and Future Prospects" section).
- **Some absolutes survive despite the carve-out.** The em-dash/en-dash ban is explicitly a "hard constraint, not a preference," and emoji/curly-quote/title-case rules are stylistic dogma that serve blog voice, not engineering clarity. The technical-text gating helps with tone but does not exempt these mechanical style rules.
- **Strong overlap with two existing catalog entries.** taste-skill, stop-slop, and humanizer all target "AI output reads as machine-generated." The catalog does not need three. humanizer is the most comprehensive and best-sourced; stop-slop is the most surgically concrete with progressive disclosure; taste-skill is the weakest (abstract framing).
- **Not verified hands-on.** Verdict rests on reading the rules, not on measured rewrites. The author's before/after pairs are persuasive but self-selected.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Operates on prose, not code; the be-specific / name-the-actor / preserve-all-content rules can make docs clearer, but it moves no code-correctness signal |
| Speed | neutral | A self-running edit pass on text the agent already produces; negligible effect on dev velocity |
| Maintainability | + | Clearer, less-puffed PRs, commits, and docs aid future readers — and the technical-text carve-out keeps it from damaging precise prose, the main risk of this skill class |
| Safety | neutral | Prompt-only skill (Read/Write/Edit/Grep/Glob/AskUserQuestion), no new attack surface; worst case is over-editing, not a security risk |
| Cost Efficiency | - | The 34 KB single-file catalog loads in full on every invocation with no progressive disclosure, a heavier token footprint than the sibling skill for the same job |

## Verdict

**CONDITIONAL**

humanizer is the most comprehensive and best-sourced of the three "de-AI the prose" skills — 33 Wikipedia-grounded patterns, each with worked Before/After rewrites, plus a voice-calibration mode and (crucially) an explicit `What NOT to flag` carve-out and technical-text gating that stop-slop lacks. That carve-out is what makes it safer than its siblings to point at engineering prose. But its surface is narrow for a code-focused catalog (PRs, docs, commits, release notes — not code), it ships as one 34 KB file with no progressive disclosure (heavier per-invocation cost than stop-slop), and a few mechanical style absolutes (hard em-dash ban, emoji/curly-quote rules) still over-edit.

Adopt it **when prose quality is a real deliverable** — public-facing READMEs, release notes, external docs, or blog posts an agent drafts — and lean on its cluster-not-isolated and preserve-human-writing guidance rather than applying every rule mechanically. It does not belong in the default code stack.

**Consolidation recommendation:** of the three overlapping prose skills, keep at most one or two. humanizer wins on **comprehensiveness, provenance (25K stars), and its over-editing carve-out**; stop-slop wins on **conciseness and progressive disclosure (lean footprint)**. taste-skill is the clear drop — its abstract "good taste" framing is the least actionable. If keeping one: humanizer for breadth-plus-safety, stop-slop for a lean footprint. If keeping two: humanizer + stop-slop, and retire taste-skill.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [humanizer](https://github.com/blader/humanizer) | skill | Removes signs of AI-generated writing via 33 Wikipedia-grounded patterns with Before/After rewrites, voice calibration, and a technical-text carve-out | AI output reads as obviously machine-generated | taste-skill, stop-slop |
