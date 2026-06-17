# Evaluation: caveman

**Repo:** [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
**Stars:** 74,045 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** All stages (output compression)
**Layer:** Tooling

---

## What it does

Claude Code skill that cuts ~65% of output tokens by instructing the model to drop articles, filler words, and pleasantries while keeping full technical accuracy. Activated via `/caveman` as a mode toggle — not a background process or proxy. The model continues to produce code, commands, and paths at full fidelity; only the surrounding prose is compressed.

## How we tested it

Used caveman mode across multiple sessions in this documentation repo (ai-tooling) and in coding sessions on other projects. Compared output length and quality with and without the mode active on identical tasks.

```
/caveman
# Then performed normal tasks: file edits, git operations, code review
# Observed output in session transcripts
```

Typical session comparison (explanatory responses, not code-only):
- Without caveman: ~400 tokens for a status update + next steps
- With caveman: ~120-150 tokens for the same information
- Code blocks, file paths, and commands: identical in both modes

## What worked

- Immediate activation with zero configuration — just `/caveman` and it's on
- Technical content (code, commands, paths, error messages) completely unaffected
- 60-75% output token reduction on explanatory text, consistent across sessions
- Particularly effective for agent-to-agent communication where readability by humans is not the priority
- No false compression — it doesn't shorten variable names, elide command flags, or truncate paths

## What didn't work or surprised us

- Transcript readability drops for humans reviewing session history — compressed text is harder to skim
- The mode is sticky per-session but doesn't persist across sessions (must re-invoke)
- Occasionally the model "drifts" back to verbose mode on long sessions, requiring a reminder
- Not useful when the user needs polished prose (documentation, PR descriptions, commit messages)

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Technical content (code, commands, paths) unchanged |
| Speed | + | Fewer output tokens = faster response completion |
| Maintainability | neutral | Output content is identical; only prose style differs |
| Safety | neutral | No impact on security-relevant output |
| Cost Efficiency | + | 60-75% output token reduction on non-code responses |

## Verdict

**ADOPT**

Zero-friction mode toggle with real, measurable token savings (60-75% on prose, 0% on code). No accuracy loss on technical content — the compression only removes linguistic filler that adds no information. Ideal for autonomous agent workflows, background tasks, and cost-sensitive sessions. Skip it only when polished human-readable output is the goal (docs, PRs, user-facing copy).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [caveman](https://github.com/JuliusBrussee/caveman) | skill | Cuts ~65% of output tokens by dropping filler while keeping technical accuracy | Verbose agent output wastes tokens and slows responses | context-mode (input side), headroom |
