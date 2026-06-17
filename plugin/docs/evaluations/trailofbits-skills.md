# Evaluation: trailofbits/skills

**Repo:** [trailofbits/skills](https://github.com/trailofbits/skills)
**Stars:** 5,748 | **Last updated:** 2026-06-17 | **License:** CC-BY-SA-4.0
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Claude Code plugin marketplace from Trail of Bits with 10+ security skills covering smart contract security, C/C++ review, GitHub Actions auditing, differential review, Burp Suite integration, and dimensional analysis for formula bugs. Each skill encodes real audit methodology from one of the most respected security firms in the industry — structured approaches to finding vulnerabilities rather than generic "scan for common issues" prompting.

## How we tested it

Installed the skills via marketplace and ran a security audit on a Node.js Express API project with authentication, database access, and third-party integrations.

```
/plugin marketplace add trailofbits/skills
```

The methodology guided the audit through structured phases:

1. **Threat modeling** — identified attack surface (auth endpoints, file upload, CORS config, session handling)
2. **Category-by-category review** — injection, authentication, cryptography, access control, input validation
3. **Evidence-based findings** — each finding required reproduction steps, not just "this looks risky"

Ran the audit against ~2,000 lines of API code across 12 route files.

## What worked

- Much more structured than prompting "find security issues" — the methodology walks through categories systematically, ensuring nothing is skipped
- Found real, actionable issues: missing rate limiting on auth endpoints, overly broad CORS (`*` in production config), JWT stored in localStorage instead of httpOnly cookies
- Fewer false positives than generic security scans because the methodology requires concrete evidence before flagging an issue
- The differential-review skill is excellent for pre-merge security gates — focuses on what changed, not re-auditing the entire codebase
- Integrates well with the code-review plugin workflow as a security-specific follow-up pass

## What didn't work or surprised us

- The smart contract skills are irrelevant for typical web development — adds weight to the plugin without value unless you're in that domain
- Some skills assume familiarity with Trail of Bits tooling (Slither, Echidna) that most developers won't have installed
- The CC-BY-SA-4.0 license means derivatives must use the same license — not a problem for usage but notable for modification
- No automated severity scoring — findings are structured but prioritization is manual

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't affect correctness of business logic |
| Speed | neutral | Adds review time but prevents rework from security incidents |
| Maintainability | neutral | No impact on code structure |
| Safety | + | Found 3 real vulnerabilities in a single audit pass with evidence |
| Cost Efficiency | + | Structured methodology means fewer wasted passes and less noise than generic prompting |

## Verdict

**ADOPT**

The structured methodology is the differentiator. Generic "find security bugs" prompts produce noise — a wall of maybe-issues with no evidence. Trail of Bits's skills produce actionable findings because the methodology requires evidence before flagging. The firm's reputation backing the audit approach gives confidence that the methodology reflects real-world audit practice. Use as a pre-merge security gate in the Review stage.

**Comparison with ghostsecurity/skills:** Trail of Bits is methodology-focused (how to audit systematically), ghostsecurity is tool-focused (what to scan for in specific frameworks). They're complementary, not redundant — use Trail of Bits for the audit structure and ghostsecurity for framework-specific checklists.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [trailofbits/skills](https://github.com/trailofbits/skills) | plugin | Professional security audit methodology from Trail of Bits | Generic security prompts produce noise; structured methodology produces evidence-based findings | ghostsecurity/skills, SkillSpector |
