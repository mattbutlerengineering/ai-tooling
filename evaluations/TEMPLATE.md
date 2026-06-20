# Evaluation: {Tool Name}

**Repo:** [{owner}/{repo}](https://github.com/{owner}/{repo})
**Stars:** {count} | **Last updated:** {date} | **License:** {license}
**Dev loop stage:** {Plan | Implement | Verify | Review | Ship | Reflect}
**Layer:** {Process | Tooling | Infrastructure}

---

## What it does

{One-liner from the catalog, then a paragraph explaining the mechanism — what actually happens when you invoke it, not marketing copy.}

## How we tested it

{Describe the actual hands-on usage. What project did you run it on? What commands did you execute? What was the input and what came back? This section must contain evidence of real usage, not README paraphrasing.}

> **Honesty rule (checked by `audit-evals.py`):** if you did NOT actually run the tool, say so plainly — open this section with a disclaimer like "**Source-grounded review — not run hands-on**" and explain why (needs an API key, heavy infra, untrusted install, etc.). Never invent a run, specific metrics, or example outputs; a fabricated run is worse than an honest review. Quote any vendor benchmark as the vendor's, not as measured. Verify every install command resolves (npm/PyPI/crates/GitHub) before publishing — a wrong install command is a dead giveaway the tool was never run.

```
{Paste the actual command(s) you ran — or, for a not-run review, the documented install/usage clearly labeled as such}
```

## What worked

- {Concrete positive finding from hands-on testing}
- {Another}

## What didn't work or surprised us

- {Concrete negative finding or unexpected behavior}
- {Another}

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | {+/-/neutral} | {one sentence} |
| Speed | {+/-/neutral} | {one sentence} |
| Maintainability | {+/-/neutral} | {one sentence} |
| Safety | {+/-/neutral} | {one sentence} |
| Cost Efficiency | {+/-/neutral} | {one sentence} |

## Verdict

**{ADOPT | CONDITIONAL | SKIP | DEFER}**

{2-3 sentences explaining the verdict. ADOPT = use in all projects. CONDITIONAL = use when {specific condition}. SKIP = evaluated and rejected. DEFER = promising but blocked by {reason}, re-evaluate after {trigger}.}

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [{name}]({url}) | {type} | {description} | {problem} | {overlaps} |
