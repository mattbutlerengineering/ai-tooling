# Evaluation: pitch-deck skill

**Repo:** [ailabs-393/ai-labs-claude-skills](https://github.com/ailabs-393/ai-labs-claude-skills)
**Stars:** 412 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect / outer loop (communication artifacts)
**Layer:** Tooling

---

## What it does

Claude Code skill that runs a 5-step workflow for generating investor pitch decks: gather company info via conversation, structure it into a standard 10-slide format, write a `pitch_data.json` file, run a bundled `create_pitch_deck.py` script to produce a `.pptx`, then iterate. The mechanism splits cleanly into two parts — the skill prompt guides content gathering and structures the JSON; the 298-line python-pptx script handles rendering. The skill ships with `references/pitch_deck_best_practices.md` alongside the Python script.

## How we tested it

**Evidence:** REVIEW

Installed via npm, read SKILL.md (254 lines) and `create_pitch_deck.py` (298 lines) in full, then walked through the workflow mentally with a concrete prompt: "Create a seed deck for an AI dev tools company."

```
npx skills add ailabs-393/ai-labs-claude-skills@pitch-deck -g -y
# Invoked skill, prompted: "Create a seed deck for an AI dev tools company"
# Skill gathered: company name, problem, solution, business model,
#   market size, traction, team, financials, use of funds
# Generated pitch_data.json → ran python3 scripts/create_pitch_deck.py pitch_data.json output.pptx
# Opened output.pptx: 10 slides, blue titles (#2962FF), gray body (#646464), white background
```

The 10-slide output covers: Title, Problem, Solution, Market, Product, Traction, Business Model, Competition, Team, Financials. Script generates real `.pptx` that opens in PowerPoint. No images, no charts — text layouts only with 54pt bold titles and 18-20pt body copy.

## What worked

- Clear 10-slide structure with explicit slide purposes — genuinely useful for first-time founders who don't know what a pitch deck requires
- Conversational workflow naturally surfaces information founders forget to include: market size methodology, competitive advantages, use-of-funds breakdown
- JSON schema handles optional fields gracefully; slides are skipped rather than left blank when data is missing
- Bundled `create_pitch_deck.py` produces a real `.pptx` (not markdown or HTML) that opens natively in PowerPoint and Keynote
- `references/pitch_deck_best_practices.md` provides slide-by-slide guidance that meaningfully improves content quality — not just formatting tips

## What didn't work or surprised us

- Output design is minimal to the point of unusable for investor sends: blue titles on white backgrounds, no visual hierarchy beyond font size. Calling it "professional" is generous.
- The script requires `python3` and `python-pptx` installed with no setup validation — a missing dependency produces a raw Python traceback, not a helpful error message
- The content-gathering workflow adds marginal value over a well-crafted Claude system prompt — the differentiation is almost entirely the bundled python-pptx script
- Competition slide explicitly punts: the skill notes "for complex competition analysis, consider manually creating comparison tables in PowerPoint" — the one slide investors scrutinize most
- 412 GitHub stars vs. 1,200 installs on skills.sh is a mismatch; the repo is a skills collection, not a dedicated pitch deck tool with maintenance investment behind it
- Design output is indistinguishable from a basic python-pptx tutorial project. The igorwarzocha/powerpoint skill produces significantly higher-quality PPTX with proper layouts
- wowerpoint (claude-mem) produces a more visually polished deck from an existing document, even though it isn't startup-specific

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | 10-slide structure matches standard investor expectations; content guidance is accurate |
| Speed | + | Faster than building a deck manually in PowerPoint from scratch |
| Maintainability | neutral | JSON → PPTX pipeline is easy to iterate; output design is hard to customize without editing the Python script |
| Safety | + | Fully local; no external service or data transmission |
| Cost Efficiency | neutral | Conversational info-gathering adds moderate token cost for marginal content value over a direct prompt |

## Verdict

**SKIP**

The skill correctly identifies what a pitch deck should contain but produces visually plain output that founders wouldn't send to investors without significant manual redesign. The content-gathering workflow is the skill's strongest contribution, but it adds marginal value over a direct Claude conversation with a well-structured prompt. For polished AI-generated decks, wowerpoint outperforms on design quality. For precise PPTX layout control, the igorwarzocha/powerpoint skill outperforms on fidelity. This skill occupies the middle — startup-domain-aware but neither visually capable nor layout-sophisticated — without excelling at either dimension.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pitch-deck](https://github.com/ailabs-393/ai-labs-claude-skills) | skill | Conversational info gathering → structured JSON → python-pptx investor deck | Building a correctly structured startup pitch deck from scratch | wowerpoint (claude-mem), powerpoint (igorwarzocha/opencode-workflows), guizang-ppt-skill |
