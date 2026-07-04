# Evaluation: powerpoint-ppt skill

**Repo:** [practicalswan/agent-skills](https://github.com/practicalswan/agent-skills)
**Stars:** 3 | **Last updated:** 2026-06-15 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect / outer loop (communication artifacts)
**Layer:** Tooling

---

## What it does

Skill for creating and manipulating PowerPoint `.pptx` files via MCP server with a python-pptx fallback. When invoked, it checks whether the host client exposes presentation MCP tools, prefers template-driven deck construction if available, and falls back to a bundled `ppt-automation.py` script. The 106-line SKILL.md covers activation conditions, a 5-check verification protocol, a deck checklist, anti-patterns, and cross-client portability notes for GitHub Copilot, Claude Code, Codex, and Gemini CLI.

## How we tested it

**Evidence:** REVIEW

Installed globally via npx, read SKILL.md in full, and examined the bundled automation script.

```
npx skills add practicalswan/agent-skills@powerpoint-ppt -g -y
# Read ~/.agents/skills/powerpoint-ppt/SKILL.md (106 lines)
# Inspected ppt-automation.py — PresentationBuilder class
```

The critical finding came from `ppt-automation.py`: `PresentationBuilder` defines `add_title_slide()`, `add_content_slide()`, `add_chart_slide()`, and `add_two_column_slide()`, but every method returns a Python dictionary. There are no `python-pptx` imports and no file I/O. The script cannot produce a `.pptx` file. It is a stub.

The MCP premise is undermined by the SKILL.md's own caveat: "Do not assume stable public tool names." The skill never names an actual MCP server to install or configure — it describes a class of tool that might exist in some clients, without specifying which ones reliably have it.

Compared to `igorwarzocha/powerpoint`: that skill ships a working 978-line `html2pptx.js` library plus 5 helper scripts with a complete generation pipeline. This skill ships a non-functional stub and process guidance.

Compared to `wowerpoint` (claude-mem): wowerpoint takes a document, routes it through NotebookLM and AI design, and produces a PDF — zero setup beyond auth. Different output format but a complete, working pipeline.

## What worked

- The 5-check verification protocol is genuinely useful — it prevents "looks okay" sign-offs by requiring pass/fail answers on title slide, layout consistency, font/color match, image resolution, and slideshow-size review
- The anti-patterns section names real failure modes: writing for the author not the reader, skipping concrete examples, letting hyperlinks drift after file moves
- The deck checklist is complete and practical
- Cross-client portability is thoughtfully designed — explicit instructions per AI editor rather than assuming a single environment
- MCP-first, fallback-second is the right architecture for a portable skill

## What didn't work or surprised us

- `ppt-automation.py` is a non-functional stub — every method returns a Python dict, no `python-pptx` import, no file write. The fallback the skill advertises does not work
- The MCP section is circular: "check if your client has presentation MCP tools" with no pointer to an actual MCP server to install
- 3 GitHub stars is the lowest of all candidates in this evaluation batch; the repo shows minimal maintenance investment
- 675 installs on skills.sh despite the broken stub — users likely installed it optimistically and encountered the gap only at fallback time
- The skill is 106 lines of process guidance. `igorwarzocha/powerpoint` delivers working tooling at 10x the LOC. The gap is not style — it's substance
- Does not outperform `wowerpoint`, `pitch-deck`, or `igorwarzocha/powerpoint` on any dimension

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | - | The bundled automation script returns Python dicts, not PPTX files; the advertised fallback does not function |
| Speed | neutral | If MCP tools are already available in the host client, the skill adds no speed; if relying on the stub, it fails silently |
| Maintainability | neutral | The verification protocol and checklist are good practices; the non-functional tooling offsets them |
| Safety | + | Fully local; no external services required |
| Cost Efficiency | neutral | No unique cost efficiency contribution over alternative skills |

## Verdict

**SKIP**

The bundled `ppt-automation.py` is a non-functional stub — `PresentationBuilder` methods return Python dictionaries rather than `.pptx` files, and the module has no `python-pptx` import. The fallback the skill's MCP section depends on does not exist in any working form. The process guidance and verification protocol are well-crafted but are not sufficient to differentiate from a good CLAUDE.md rule set. With 3 GitHub stars and minimal maintenance, the risk of it staying broken is high. `igorwarzocha/powerpoint` covers the same use case with a working 978-line generation library; `wowerpoint` covers AI-generated decks end-to-end.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [powerpoint-ppt](https://github.com/practicalswan/agent-skills) | skill | MCP-first PowerPoint skill with process guidance and verification protocol | Generating and updating `.pptx` decks from AI agents | wowerpoint (claude-mem), powerpoint skill (igorwarzocha/opencode-workflows), pitch-deck-skill (ailabs-393) |
