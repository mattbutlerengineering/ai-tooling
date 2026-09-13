# Evaluation: ai-data-extractor

**Repo:** [kruzovic7/ai-data-extractor](https://github.com/kruzovic7/ai-data-extractor)
**Stars:** 263 | **Last updated:** 2026-09-11 (pushed) | **License:** MIT
**Last verified:** 2026-09-13
**Last triaged:** 2026-09-13  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Free, open-source extractor that pulls AI coding-assistant chat histories — Claude Code, Cursor, Windsurf, Aider, Cline/Roo Code, and more — out of each tool's own session-log format and into one common export, for analysis or backup.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the
lead and note it isn't redundant with an existing STACK pick; it would not support an
ADOPT, and this eval offers none.

## Triage note

263 stars in two days and a genuinely wider scope than any single-tool export
utility already catalogued (`cli-continues` does any-to-any session *handoff*,
`export-md` is Claude-Code-only markdown export) — neither is a straight incumbent.
No overlap pressure yet (brand new), so it doesn't land in P2. Left at
`discovery-log`; significant enough to deserve a real hands-on eval rather than a
mechanical disposition.

## Verdict

**discovery-log — tentative read** — a cross-tool chat-history extractor worth a
real look once someone needs to actually export/analyze coding-agent session data;
not evaluated hands-on.
