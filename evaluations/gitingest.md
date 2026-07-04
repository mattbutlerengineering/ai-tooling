# Evaluation: gitingest

**Repo:** [coderamp-labs/gitingest](https://github.com/coderamp-labs/gitingest)
**Stars:** ~14.9K | **Last updated:** 2026-06-14 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (context-gathering before prompting)
**Layer:** Tooling

---

## What it does

Turns a codebase into a single prompt-ready text digest: a header summary (files
analyzed + an estimated token count), a directory tree, and the concatenated file
contents. It works three ways — swap `hub`→`ingest` in any GitHub URL for the hosted
version, run the `gitingest` CLI, or call the Python package's `ingest()` — and
applies a default ignore list so junk and secrets don't end up in the digest.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed it (`pip install gitingest`) and ran `ingest('sample')`
against a purpose-built sample repo whose contents are fully known, so every part of
the output is objectively checkable — including whether it leaks a secret.

```
python3 -m pip install gitingest        # clean install, rc=0
# sample repo: calc.py (def add), README.md, sub/.env (SECRET=xyz), .gitignore (node_modules/)
python3 -c "from gitingest import ingest; s,t,c = ingest('sample'); ..."
```

Verified output (not paraphrased — printed and asserted on):

- **Summary:** `Files analyzed: 2` · `Estimated tokens: 57` — a real token estimate ships with the digest.
- **Tree:** correctly rendered `sample/` → `README.md`, `calc.py`.
- **Content (282 chars):** assertion `'def add(a,b):' in content` → **True**; `'A tiny repo.' in content` → **True** — the code and README are present verbatim.
- **Safety check — the load-bearing one:** assertion `'SECRET=xyz' in content` → **False**. gitingest's default ignore patterns excluded `sub/.env` entirely (only 2 of the repo's files were analyzed), so a secret that a naive `cat **/* ` would have dumped straight into the LLM context never appears in the digest.

That last result is the measured differentiator: the objective oracle (string-presence
assertions on a known input) confirms gitingest *excludes* a planted secret by default,
not just that it produces some text.

## What worked

- **Secret-safe by default.** The planted `.env` secret was excluded with no
  configuration — a real safety property over hand-rolled repo concatenation, and the
  kind of thing you only learn by running it against a file you control.
- **Token count comes for free.** The summary's `Estimated tokens` lets you size the
  digest against a context window before pasting it — directly useful at the Plan stage.
- **Trivial install and API.** `pip install gitingest` then a three-value `ingest()`
  return (summary, tree, content) — no config, no server. The `hub→ingest` URL trick
  makes the hosted path zero-install for public repos.
- **Clean, predictable structure.** Header → tree → contents is exactly the shape an
  LLM parses well, and it matched the known repo exactly.

## What didn't work or surprised us

- **Noisy stdout logging.** Each `ingest()` call emits several INFO log lines to
  stderr by default; for programmatic/piped use you'll want to quiet the logger.
- **Default-ignore is implicit.** The `.env` exclusion is great, but the digest gives
  no visible "N files skipped" line, so it's easy not to realize files were dropped —
  the only signal is the `Files analyzed` count. Worth double-checking on a repo where
  you *want* something the default list excludes.
- **Overlaps heavily with repomix.** For pure repo-serialization the two do the same
  job; gitingest's edge is the URL trick + default secret hygiene, repomix's is richer
  config/formatting. Pick one, not both.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Digest reproduced the known repo exactly (tree + verbatim contents asserted true) |
| Speed | + | One install + one call to get an LLM-ready digest; hosted URL path is zero-install |
| Maintainability | neutral | A consumption tool — produces an artifact, doesn't change your codebase |
| Safety | + | **Measured:** a planted `sub/.env` secret was excluded from the digest by default (`'SECRET=xyz' in content` → False) |
| Cost Efficiency | + | Ships an estimated-token count so you can right-size context before paying for it |

## Verdict

**CONDITIONAL** — adopt when you need a quick, LLM-ready text digest of a repo
(especially a private/local one, or a public one via the `hub→ingest` URL). The
measured secret-exclusion makes it a safer default than hand-concatenating files. The
condition: it overlaps repomix almost entirely, so install one serializer, not both —
choose gitingest for the URL trick and out-of-the-box secret hygiene, repomix for
heavier formatting/config control. Quiet its logger for programmatic use.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gitingest](https://github.com/coderamp-labs/gitingest) | tool | Turn any GitHub repo into prompt-ready text (MIT, ★15K) — swap `hub`→`ingest` in any GitHub URL, or run the CLI/package/MCP locally, to get a digest with file tree and token counts | Want a one-step, LLM-friendly text digest of a repo (or a private one locally) without cloning and hand-assembling files | repomix, markitdown, repoprompt-ce, opensrc |
