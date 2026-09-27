# Evaluation: quicksilver

**Repo:** [UditAkhourii/quicksilver](https://github.com/UditAkhourii/quicksilver)
**Stars:** 67 | **Last updated:** 2026-09-27 (pushed) | **License:** MIT
**Last verified:** 2026-09-27
**Last triaged:** 2026-09-27  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code skill that hands bulk judgment calls — "which files matter?", "find the
failures", ranking, filtering — to Jev, a separate cheap decision model, instead of
having the main LLM read through the data itself. Aimed at yes/no, categorical, or
ranking judgments across large datasets (log triage, ticket routing, spam filtering,
code-pattern search).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the README's description of the delegation model. That is
sufficient for a discovery-log entry, not for an ADOPT — this eval offers none. The
README's own benchmark figures ("86% fewer Claude tokens on a 12-task benchmark, up
to 20x faster") are the author's self-reported numbers, not independently measured
here, and are deliberately omitted from the catalog one-liner.

## Triage note

Left at `discovery-log`, not SKIPped. It scored no overlap pressure against a STACK
pick, so it landed in P3 rather than P2 — but it is conceptually close to `jev-use`
(also catalogued, also `discovery-log`), which does the same "hand a no-text-output
step to Jev instead of the LLM" trade for individual agent steps rather than bulk
data. Since `jev-use` is itself only a lead and not a STACK incumbent, there is no
"redundant with an installed tool" call to make here — but a future hands-on eval of
either should look at both together rather than in isolation, and should independently
verify the underlying "Jev" decision model's claims (see the note on `jevgrep`'s eval,
added the same day, about the wider wave of Jev-branded repos surfacing in discovery).

_Triaged 2026-09-27 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [quicksilver](https://github.com/UditAkhourii/quicksilver) | skill | Claude Code skill (MIT) that hands bulk judgment calls — which files matter, find the failures, rank, filter — to Jev's cheap decision model instead of the main LLM | Bulk yes/no, categorical, or ranking judgment calls across large datasets burn full LLM calls when a cheap classifier would do | jev-use, deadeye-cc, skillranker |
