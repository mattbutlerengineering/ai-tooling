# Skills for Generating Presentations

Reference of agent skills that **generate presentation decks/slides** — both
already installed in this environment and notable candidates in the open skills
ecosystem (skills.sh). Scope is *generation*; skills about *delivering* a talk
are listed separately at the bottom.

Searched via `npx skills find {presentation, slides, powerpoint, deck}`.
Install counts from skills.sh (all-time, as of 2026-07-08). Per the find-skills
guidance, **official sources** (`anthropics`, `googleworkspace`, `getsentry`,
`microsoft`, `larksuite`/`open.feishu.cn`, `heygen-com`) are treated as
trustworthy regardless of count; small-install community skills are flagged.

## Already installed

| Skill | Source | What it does | When to reach for it |
|-------|--------|--------------|----------------------|
| `powerpoint` | community (via `~/.agents/skills/`) | High-fidelity `.pptx` via HTML → `html2pptx`; design principles, thumbnail-grid audits | Pixel-precise layout, branded decks, auditing existing decks |
| `powerpoint-ppt` | community (via `~/.agents/skills/`; v1.2, 2026-04-25) | `.pptx` manipulation via an MCP server or local `python-pptx` automation | Creating/formatting slides, placeholders, templates, image insertion |
| `pitch-deck` | `@ai-labs-claude-skills/pitch-deck` (community) | Generates investor/sales/business decks in the standard 10-slide structure | Fundraising, sales, product-launch structured decks |
| `slidev` | community (via `~/.agents/skills/`) | Web decks from Markdown (Vite + Vue); code highlight, Monaco, Mermaid/PlantUML, LaTeX | Technical talks, conference decks, code walkthroughs, export to PDF/PPTX/SPA |

These four auto-trigger on the keywords in their frontmatter (`powerpoint`,
`pitch deck`, `slidev`, "presentation"); no install command needed.

## Ecosystem candidates (skills.sh)

### Official sources — recommended

| Skill | Source | Installs | Install command |
|-------|--------|----------|-----------------|
| `pptx` | `anthropics/skills` | 170.5K | `npx skills add anthropics/skills@pptx -g -y` |
| `gws-slides` | `googleworkspace/cli` | 27.2K | `npx skills add googleworkspace/cli@gws-slides -g -y` |
| `recipe-create-presentation` | `googleworkspace/cli` | 20.4K | `npx skills add googleworkspace/cli@recipe-create-presentation -g -y` |
| `presentation-creator` | `getsentry/skills` | 1.5K | `npx skills add getsentry/skills@presentation-creator -g -y` |
| `slideshow` | `heygen-com/hyperframes` | 73.7K | `npx skills add heygen-com/hyperframes@slideshow -g -y` |
| `lark-slides` | `larksuite/cli` | 278.5K | `npx skills add larksuite/cli@lark-slides -g -y` |
| `lark-slides` | `open.feishu.cn` | 371.3K | `npx skills add open.feishu.cn@lark-slides -g -y` |

Notes:
- **`anthropics/skills@pptx`** (170.5K, #125 on the leaderboard) is the canonical
  official `.pptx` skill — the most defensible pick if you want a maintained,
  battle-tested PowerPoint generator alongside the installed `powerpoint`.
- **`lark-slides`** (Feishu/Lark) and **`gws-slides`** (Google) target specific
  cloud office suites; only relevant if your decks live in Lark or Google Slides.
  Both Feishu entries point at the same Lark skill surface from two publishing
  routes (larksuite CLI vs open.feishu.cn).
- **`slideshow`** is part of HeyGen's `hyperframes` suite (180K+ aggregate
  installs) — motion/animated slides, heavier weight than a static deck.
- **`microsoft/hve-core@powerpoint`** (274 installs) is Microsoft-published but
  near-zero adoption; treat as experimental.

### Community sources — low adoption, verify before adopting

Per find-skills guidance (prefer 1K+ installs, caution under 100), all below
sit at modest counts or come from authors with no established reputation. Listed
for completeness; install and test before relying on any:

| Skill | Source | Installs | Install command |
|-------|--------|----------|-----------------|
| `elite-powerpoint-designer` | `willem4130/claude-code-skills` | 4.2K | `npx skills add willem4130/claude-code-skills@elite-powerpoint-designer -g -y` |
| `powerpoint` | `igorwarzocha/opencode-workflows` | 5K | `npx skills add igorwarzocha/opencode-workflows@powerpoint -g -y` |
| `web-video-presentation` | `conardli/garden-skills` | 2.8K | `npx skills add conardli/garden-skills@web-video-presentation -g -y` |
| `presentation-design` | `jwynia/agent-skills` | 1.8K | `npx skills add jwynia/agent-skills@presentation-design -g -y` |
| `powerpoint-automation` | `aktsmm/agent-skills` | 1.8K | `npx skills add aktsmm/agent-skills@powerpoint-automation -g -y` |
| `pitch-deck` | `ailabs-393/ai-labs-claude-skills` | 1.4K | `npx skills add ailabs-393/ai-labs-claude-skills@pitch-deck -g -y` |
| `presentation-deck` | `owl-listener/designer-skills` | 1.3K | `npx skills add owl-listener/designer-skills@presentation-deck -g -y` |
| `html-slides` | `claude-office-skills/skills` | 9.2K | `npx skills add claude-office-skills/skills@html-slides -g -y` |
| `powerpoint-ppt` | `practicalswan/agent-skills` | 1K | `npx skills add practicalswan/agent-skills@powerpoint-ppt -g -y` |

The installed local `powerpoint-ppt` (v1.2, dated 2026-04-25) is not confirmed
to be `practicalswan/agent-skills@powerpoint-ppt`; do not assume parity.

## Delivering talks (coaching, not deck generation)

Skills that help with *delivery* — narrative, rehearsal, nerves, conference
format — rather than producing slide files. Searched via `npx skills find
{presenting, talk, speaking, public-speaking}`. Install counts from skills.sh
(all-time, as of 2026-07-08). Adoption is modest across the board; weigh
reputation over raw counts here, since delivery skills are a newer category.

| Skill | Source | Installs | What it does | Install command |
|-------|--------|----------|--------------|-----------------|
| `giving-presentations` | `refoundai/lenny-skills` | 2.2K | End-to-end presentation help from 19 product leaders — narrative-first ("bow and arrow" technique), structure for engagement, rehearsal, managing nerves, physical presence. Covers the full arc from "what do I want them to remember" through delivery. Repo has 1.1K GitHub stars; security audits pass. | `npx skills add refoundai/lenny-skills@giving-presentations -g -y` |
| `presenting-conference-talks` | `orchestra-research/ai-research-skills` (originally `zechenzhangagi/ai-research-skills`) | 285 | Conference-talk slides from a compiled research paper — produces Beamer LaTeX PDF + editable PPTX with speaker notes and optional talk script. Academic/research-paper-specific. Repo has 10.5K GitHub stars. | `npx skills add orchestra-research/ai-research-skills@presenting-conference-talks -g -y` |
| `presenting-conference-talks` | `zechenzhangagi/ai-research-skills` | 78 | The original source of the orchestra-research fork above. Prefer the orchestra-research fork (higher install count, same origin, security-audited). | `npx skills add zechenzhangagi/ai-research-skills@presenting-conference-talks -g -y` |
| `speaking` | `steipete/agent-scripts` | 40 | General speaking coaching (low adoption — verify before relying). | `npx skills add steipete/agent-scripts@speaking -g -y` |
| `confident-speaking` | `menkesu/awesome-pm-skills` | 38 | Confidence/coaching for speaking (low adoption — verify before relying). | `npx skills add menkesu/awesome-pm-skills@confident-speaking -g -y` |
| `ielts-speaking-coach` | `jurgendn/agent-skills` | 27 | IELTS speaking exam prep — narrow scope, not general presentation delivery. | `npx skills add jurgendn/agent-skills@ielts-speaking-coach -g -y` |

### Recommendations — delivering

- **General business/product talks:** `refoundai/lenny-skills@giving-presentations`
  (2.2K, 1.1K GitHub stars) is the clear pick — it frames delivery as a
  narrative problem first and is the only one with meaningful adoption. It
  pairs naturally with `pitch-deck` (installed) or `slidev` (installed) for
  the deck itself.
- **Academic / conference talks from a paper:** `presenting-conference-talks`
  (orchestra-research fork, 285 installs, 10.5K-star repo) — note it also
  *generates* Beamer/PPTX, so it straddles the generate/deliver line. Use it
  when the input is a finished research paper, not a business narrative.
- **The other speaking skills** (`speaking`, `confident-speaking`,
  `ielts-speaking-coach`) are sub-100-install and unproven; test before
  adopting, and don't expect maintained quality.

## Adjacent (design coaching, not generation or delivery)

- `nextlevelbuilder/ui-ux-pro-max-skill@ckm:slides` (31.9K) — slide *design
  taste* guidance from a UI/UX skill family. Coaching on visual design, not a
  deck builder or delivery coach. Listed so it isn't mistaken for either.

## Recommendations

- **Static `.pptx`, general purpose:** keep the installed `powerpoint`
  (high-fidelity path) and consider adding `anthropics/skills@pptx` as a
  maintained official reference — overlap is high; pick one and standardize.
- **Investor/sales decks:** the installed `pitch-deck` already covers the
  10-slide structure; the community `ailabs-393/.../pitch-deck` adds nothing
  with higher confidence.
- **Technical/engineering decks:** the installed `slidev` is the right tool;
  no ecosystem candidate beats it for code-heavy decks.
- **Google Slides / Lark** users: add `gws-slides` or `lark-slides`
  respectively — none of the installed skills target those surfaces.
- **Animated/explainer decks:** `heygen-com/hyperframes@slideshow` is the only
  ecosystem entry covering motion, outside the installed set.

To install any candidate: `npx skills add <owner/repo@skill> -g -y`. Verify
with `npx skills check` after.