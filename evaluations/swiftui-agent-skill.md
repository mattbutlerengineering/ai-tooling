# Evaluation: SwiftUI-Agent-Skill (SwiftUI Pro)

**Repo:** [twostraws/SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill)
**Stars:** 4,134 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A review-oriented agent skill that checks SwiftUI code against 9 reference documents covering deprecated API, view composition, data flow, navigation, design/HIG compliance, accessibility, performance, Swift concurrency, and code hygiene. When invoked (`/swiftui-pro`), it loads the main SKILL.md which instructs the agent to walk through each reference file in order, reporting genuine issues with file, line, rule, and before/after code fixes. Partial reviews are supported — you can scope to just accessibility or just deprecated API.

The skill uses progressive disclosure well: the root SKILL.md is a compact ~200-line orchestrator that references 9 standalone documents in `references/`. Each reference is a dense, example-heavy checklist targeting specific mistakes LLMs actually make — not general SwiftUI docs. The author (Paul Hudson / @twostraws) is one of the most prolific Swift educators, and the content reflects thousands of hours of real-world SwiftUI experience.

Part of a larger ecosystem: companion skills exist for SwiftData (349 stars), Swift Concurrency (462 stars), and Swift Testing (363 stars), with a meta-repo Swift-Agent-Skills (2,057 stars) that bundles them.

## How we tested it

Read the SKILL.md and all 9 reference files directly from GitHub to assess depth, accuracy, and actionability. Could not install via `npx skills add` due to permission restrictions, so this is an architecture-review evaluation.

```bash
gh api repos/twostraws/SwiftUI-Agent-Skill/contents/swiftui-pro/SKILL.md --jq '.content' | base64 -d
gh api repos/twostraws/SwiftUI-Agent-Skill/contents/swiftui-pro/references/api.md --jq '.content' | base64 -d
gh api repos/twostraws/SwiftUI-Agent-Skill/contents/swiftui-pro/references/accessibility.md --jq '.content' | base64 -d
gh api repos/twostraws/SwiftUI-Agent-Skill/contents/swiftui-pro/references/performance.md --jq '.content' | base64 -d
```

Evaluated against three practical questions:

1. **Does it target real LLM mistakes?** Yes — every rule in `api.md` addresses a specific deprecated-to-modern API swap that LLMs routinely get wrong (`foregroundColor` → `foregroundStyle`, `cornerRadius` → `clipShape(.rect(cornerRadius:))`, `navigationBarLeading` → `topBarLeading`). The accessibility file specifically flags icon-only buttons and `onTapGesture` misuse — both common LLM failure modes.

2. **Is the content current?** Targets iOS 26 and Swift 6.2 — the latest versions as of June 2026. References native `WebView` (iOS 26), `@Entry` macro, `sensoryFeedback()`, and `@ScaledMetric` vs `.font(.body.scaled(by:))` differences by OS version.

3. **Does it follow skill best practices?** Excellent progressive disclosure (main SKILL.md < 200 lines, reference files loaded on demand). Structured output format with file/line/rule/fix. Supports partial review for token efficiency.

## What worked

- **Exceptional depth on LLM-specific mistakes**: not a rehash of Apple docs but a curated list of what AI agents get wrong — deprecated API, invisible VoiceOver buttons, `AnyView` overuse, eager stacks with large data sets
- **Performance section is genuinely useful**: covers `_ConditionalContent` avoidance, `@ViewBuilder` property vs method tradeoffs, `task()` vs `onAppear()` for async work — subtle issues that even experienced developers miss
- **Accessibility coverage is production-grade**: Dynamic Type, VoiceOver, Reduce Motion, `accessibilityDifferentiateWithoutColor`, `accessibilityInputLabels()` for complex buttons
- **Cross-editor compatible**: works with Claude Code, Codex, Gemini, Cursor via standard SKILL.md format
- **Companion ecosystem**: SwiftData, Concurrency, and Testing skills cover the full Apple development stack

## What didn't work or surprised us

- **Not hands-on tested**: could not install due to permissions, so impact on actual generated code quality is inferred not measured
- **iOS 26 targeting may be premature**: if your project supports iOS 17-18, some guidance (native `WebView`, `.font(.body.scaled(by:))`) doesn't apply — no conditional logic for older deployment targets
- **No automated checking**: this is a review skill, not a linter — it relies on the agent to find issues rather than running automated checks
- **Token cost of full review**: loading all 9 reference files for a full review could be expensive; partial reviews help but require the user to know which dimension matters

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Catches deprecated API, broken VoiceOver, invisible buttons, and data flow anti-patterns |
| Speed | + | Structured review process with partial review support reduces review time |
| Maintainability | + | Enforces modern API, proper view decomposition, and code hygiene |
| Safety | neutral | Not security-focused |
| Cost Efficiency | neutral | Full review loads ~9 reference files; partial review mitigates |

## Verdict

**CONDITIONAL**

Use when developing SwiftUI applications targeting iOS 26+. The skill is the highest-quality domain-specific review skill in the catalog — authored by a recognized Swift authority, targeting real LLM failure modes rather than restating documentation, and structured for token-efficient progressive disclosure. The companion skills (SwiftData, Concurrency, Testing) round out a complete Apple development stack. Not relevant for non-Apple projects.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill) | skill | SwiftUI agent skill for Claude Code, Codex, and other AI tools (4.1K stars) | AI agents generate outdated or incorrect SwiftUI code | — (domain-specific: SwiftUI) |
