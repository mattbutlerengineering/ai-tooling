# Evaluation: stop-slop

**Repo:** [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)
**Stars:** 11,386 | **Last updated:** 2026-03-17 | **License:** MIT
**Dev loop stage:** Ship (prose artifacts — docs, PRs, commit messages, release notes); touches Review when the artifact under review is prose
**Layer:** Process

---

## What it does

Removes AI tells from prose — filler words, hedging, corporate speak. The mechanism is a deny-list-driven editing pass packaged as a Claude Code skill: a 2.6 KB `SKILL.md` carrying eight core rules plus a 12-item "Quick Checks" gate and a 5-dimension scoring rubric, backed by three reference files that load on demand (`phrases.md`, `structures.md`, `examples.md`).

When invoked, the agent runs the draft against concrete catalogs of banned patterns and rewrites to eliminate them. The catalogs are specific, not abstract:

- **`phrases.md`** — explicit word/phrase lists: throat-clearing openers ("Here's the thing:", "It turns out"), emphasis crutches ("Let that sink in.", "Make no mistake"), a business-jargon substitution table (navigate → handle, deep dive → analysis), a hard adverb ban ("really", "just", "literally", "genuinely", "fundamentally"), meta-commentary ("In this section, we'll..."), and vague declaratives ("The implications are significant").
- **`structures.md`** — pattern-level clichés expressed as tables: binary contrasts ("Not X, it's Y"), negative listing, dramatic fragmentation ("That's it. That's the tradeoff."), false agency (giving inanimate things human verbs — "the decision emerges"), passive voice, Wh- sentence starters, three-item lists, and a blanket em-dash ban.
- **`examples.md`** — five before/after rewrites demonstrating the transforms (e.g. "Here's the thing: building products is hard. Not because the technology is complex. Because people are complex. Let that sink in." → "Building products is hard. Technology is manageable. People aren't.").

The scoring rubric (Directness, Rhythm, Trust, Authenticity, Density, each 1–10) gives the agent a numeric self-check with a revise-below-35/50 threshold. So it is part deny-list, part rewrite pass, part rubric — not a single dumb find-and-replace.

## How we tested it

Source-grounded review. I did not install the skill or run it on a live draft. I read the complete repository over the GitHub API — every file: `SKILL.md`, all three reference files (`phrases.md`, `structures.md`, `examples.md`), `README.md`, and `CHANGELOG.md` — and reasoned about the method against the catalog framework and the two overlap entries already in `CATALOG.md` (taste-skill, humanizer). The before/after pairs quoted in "What it does" are the author's own examples shipped in `examples.md`, not outputs I generated. I ran no rewrites of my own; any judgement about output quality below is reasoning about the rules, not a measured result.

```bash
gh api repos/hardikpandya/stop-slop --jq '{stars,license,description,pushed,created}'
gh api "repos/hardikpandya/stop-slop/git/trees/HEAD?recursive=1" --jq '.tree[] | "\(.type)\t\(.size)\t\(.path)"'
for f in SKILL.md README.md references/phrases.md references/structures.md references/examples.md CHANGELOG.md; do
  gh api "repos/hardikpandya/stop-slop/contents/$f" --jq '.content' | base64 -d
done
# Catalog overlap scan:
grep -inE "taste-skill|humanizer|stop-slop|AI tells" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **The deny-lists are concrete and actionable, not vibes.** Most "make AI sound human" skills hand the model an abstract goal ("write with taste") and hope. stop-slop ships literal phrase lists and substitution tables, which is the format an LLM can actually apply deterministically. "Kill all adverbs; here are 15 specific offenders" is a checkable instruction; "have good taste" is not.
- **Progressive disclosure is done right.** A lean `SKILL.md` (2.6 KB) holds the rules and the gate; the heavy catalogs live in `references/` and load on demand. This matches Claude Code skill best practices and keeps the always-loaded footprint small — the skill costs almost nothing until it fires.
- **The "false agency" and "passive voice → name the actor" rules are genuinely good editing.** "Complaints don't become fixes — someone fixed it" is a real prose defect that AI drafts exhibit constantly, and the fix (name the human, or use "you") is correct writing advice independent of the AI-tells framing.
- **Built-in scoring rubric closes the loop.** The 5-dimension / 35-of-50 gate gives the agent a self-check before delivering, rather than trusting a single pass. Cheap and sensible.
- **Decent provenance and maintenance.** 11.4K stars, MIT, real named author (Hardik Pandya), a CHANGELOG showing iterative tightening, and a restructure to follow Claude Code skill conventions. Not abandonware.

## What didn't work or surprised us

- **The dev-loop surface area is narrow.** This is a code-tooling catalog, and stop-slop touches prose, not code. It does nothing for correctness of code, tests, or builds. Its reach is limited to the prose an engineer's agent emits: PR descriptions, commit bodies, README/docs, release notes, code-review comments. Real value there, but a thin slice of the inner loop.
- **Several rules are dogmatic absolutes that will over-edit.** "No em dashes at all", "kill ALL adverbs", "no Wh- sentence starters", "two items beat three" — applied mechanically to technical writing these produce damage. A doc that says "the function never returns null" is stating an invariant, not a "lazy extreme"; banning "always/never/every" outright fights precise technical language. The skill has no carve-out for technical prose where absolutes and passive voice ("the request is rejected if...") are correct.
- **Strong overlap with two existing catalog entries.** taste-skill and humanizer both target "AI output reads as machine-generated." stop-slop is the most concrete of the three (explicit lists vs. taste-skill's good-taste framing), so it is the best *implementation* of the idea — but the catalog does not need three skills doing the same job. This is a consolidation question, not three independent adopts.
- **It is a "humanize the prose" tool, which can cut against engineering clarity.** The goal — make text not sound AI-written — is a content-marketing / blogging objective. For internal engineering docs, sounding human is irrelevant; being unambiguous is everything. Some rules (cut hedging, be specific, active voice, name the actor) serve both goals; others (vary rhythm, cut quotables, no em dashes) serve only the blog-voice goal and add nothing to a runbook.
- **Not verified hands-on.** Verdict rests on reading the rules, not on measured rewrites. The author's own before/after pairs are persuasive but self-selected.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Operates on prose, not code; the false-agency / passive-voice / be-specific rules can make docs clearer, but it moves no code-correctness signal |
| Speed | neutral | A self-running edit pass on text the agent already produces; negligible effect on dev velocity either way |
| Maintainability | + | Clearer PRs, commit messages, and docs aid future readers — but only for the prose slice, and only if the dogmatic rules are reined in for technical writing |
| Safety | neutral | Prompt-only skill, no permissions or new attack surface; worst case is over-aggressive edits, not a security risk |
| Cost Efficiency | neutral | Tiny always-loaded footprint via progressive disclosure; reference loads + a rewrite pass add modest tokens when it fires — roughly a wash |

## Verdict

**CONDITIONAL**

stop-slop is the strongest of the three "de-AI the prose" skills in the catalog — its concrete deny-lists and substitution tables are exactly the format an LLM can apply, where taste-skill's abstract framing is not, and its progressive-disclosure structure and scoring rubric are well built. But for a code-focused dev-loop catalog its surface is narrow (it touches PRs, docs, commit messages, and review comments — not code), and several rules are dogmatic absolutes (no em dashes, kill all adverbs, ban "always/never") that will over-edit technical writing where those constructions are correct.

Adopt it **when prose quality is a real deliverable** — public-facing READMEs, release notes, blog posts, external-facing docs an agent drafts — and treat its absolutes as defaults to override, not laws, on technical text. If the catalog consolidates the three overlapping entries (taste-skill, humanizer, stop-slop), stop-slop is the one to keep on implementation quality. It does not earn a place in the default code stack; it earns a place in a writer's toolkit that an engineering agent reaches for at Ship time.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [stop-slop](https://github.com/hardikpandya/stop-slop) | skill | Removes AI tells from prose via concrete deny-lists (filler, jargon, passive voice, em dashes) plus a scoring rubric | AI-written text is obviously AI-written | taste-skill, humanizer |
