#!/usr/bin/env python3
"""
audit-evals.py — integrity checks for the ai-tooling catalog.

Fifteen detectors (A-O), each proven to catch real problems (see git history,
2026-06-20), plus a --selftest that unit-tests the evidence classifier:

  A. INSTALL RESOLVER — every install command in STACK.md / CATALOG.md / evaluations/
     should point at an artifact that actually exists (npm / PyPI / crates.io / GitHub).
     A broken install command is strong evidence the tool was never run. The one
     GATING detector that touches the network, so it reports n/total CHECKED and
     three outcomes, not two (#447): only a 404 is BROKEN and fails the build, while
     a 429 / 5xx / timeout / missing binary is UNCHECKED — printed, counted, and never
     a build failure, because nothing a commit did caused it. Detector C's rule (#319),
     which this detector broke in both directions at once.

  B. FABRICATION CLASSIFIER — an eval's "How we tested it" section should either
     disclose it was NOT run (honest review) or describe a real hands-on run.
     A section that asserts a specific run (past-tense verbs, invented metrics) with
     NO honesty disclaimer is a fabrication candidate to review.

  C. LINK ROT (opt-in, --links) — every github.com/owner/repo link in CATALOG.md
     should resolve to its canonical current name. Flags 404s (dead) and silent
     renames (moved). ~450 network requests, so it is off by default. Reports
     n/total CHECKED and says INCONCLUSIVE rather than OK when any link could not
     be verified: only a 404 means "gone", and every other failure (429 rate limit,
     5xx, timeout) is "could not check". Folding those into "ok" once made the
     sweep print a clean bill of health for 612 links while GitHub 429'd all of
     them (#319).

  D. VERDICT SYNC — each eval's "## Verdict" should agree with its COMPARISON.md
     row. Tolerates dual verdicts ("ADOPT for X — CONDITIONAL otherwise") and the
     KEEP (installed/validated) status standing in for ADOPT. Offline.

  E. SKILL EVIDENCE (opt-in, --skills, REPORT-ONLY) — a skill's value is a
     behaviour change, so an ADOPT verdict on a *skill* should rest on a measured
     eval (triggering / with-skill-vs-baseline), not a README review. Lists which
     ADOPT skills are measured vs the review-based backlog. Does NOT affect the
     exit code — it's a tracked metric, not a gate (the backlog is pre-existing).

  F. DANGLING OVERLAPS (opt-in, --overlaps, REPORT-ONLY) — an "Overlaps with"
     token naming a tool that isn't itself catalogued is either a deliberate
     external peer (allowed) or a real gap (a notable tool we forgot). The more
     rows cite the same uncatalogued token, the likelier it's a gap — this is how
     aider/continue/agenta were found. Report-only; surfaces candidates.

  G. COMPARISON CONSISTENCY — COMPARISON.md's per-stage summary must sum to its
     own body rows, and its Total must equal the CATALOG.md entry count. Catches
     manual count drift between the two authoritative files (a tool addition edits
     both). Offline, gating, on by default.

  H. ARCHIVED REPOS (opt-in, --archived, REPORT-ONLY) — a catalogued repo GitHub has
     flagged `archived` is unmaintained; the entry should carry a ⚠️ archived note or
     repoint to a successor. Link rot (C) misses this (the link still resolves).
     Found 4 (incl. gpt-engineer ★55K). Uses authenticated `gh api`; report-only.

  J. STACK-DERIVATION DRIFT — STACK.md must be derivable from the verdict data
     (COMPARISON.md) plus the exclusion ledger (STACK-LEDGER.md, #64): every ADOPT/
     KEEP tool is either in STACK or has a logged exclusion reason, ledger verdicts
     match COMPARISON, and nothing marked in-STACK is missing from STACK.md. Kills the
     hand-maintained drift prior audits kept finding. Offline, gating, on by default.

  K. VERDICT EVIDENCE GATE — a strong verdict can't rest on a README skim. An ADOPT/
     KEEP eval must be run-backed (Evidence MEASURED or RUN) or carry an explicit honesty
     disclaimer (the documented escape hatch); a REVIEW/SOURCE-ONLY ADOPT/KEEP with no
     disclaimer fails. Generalizes the skills-only report-only detector E into a catalog-
     wide gate (#71). Offline, gating, on by default.

  L. STALENESS SWEEP (opt-in, --staleness, REPORT-ONLY) — a point-in-time eval rots:
     a fast-moving harness can be wrong months after it was written. Flags evals whose
     **Last verified:** date is older than its category threshold (STALENESS_DAYS, keyed
     by Type — harnesses/MCP servers age faster than references). Report-only (#65).

  I. EVIDENCE-STRENGTH FIELD (opt-in, --evidence, REPORT-ONLY) — tallies each eval's
     declared **Evidence:** field (MEASURED / RUN / REVIEW / SOURCE-ONLY): how hard we
     looked, recorded as data and separate from the verdict (what we concluded). The
     tracer-bullet slice (issue #62) only parses and reports; backfill + a COMPARISON
     column (#67) and gating on weak backing (#71) build on it. Offline.

  M. CLUSTERS WITHOUT A PICK (opt-in, --clusters, REPORT-ONLY) — ADR 0001 / #69: a
     catalog should name ONE best-in-class ADOPT pick per overlap cluster, not hedge
     CONDITIONAL on all of them. Flags overlap clusters (connected via "Overlaps with")
     where no member is ADOPT/KEEP yet at least one is CONDITIONAL — the clusters still
     awaiting a pick. Makes the #69 migration findable; migrates nothing.

  N. TOKEN-SAVINGS CLAIMS (opt-in, --savings-claims, REPORT-ONLY) — a CATALOG row
     whose one-liner makes a numeric token-savings headline (a % or N× next to token
     vocabulary) should be run-backed (Evidence MEASURED/RUN) or carry an in-row
     self-reported/unverified disclaimer. Turns the Optimize cluster's unverified
     savings claims into a number to shrink (evaluations/token-savings-protocol.md).

  O. ROW SHAPE — a malformed table row in CATALOG.md / COMPARISON.md used to be
     silently skipped by the parse sites, quietly corrupting the counts G gates on.
     validate_catalog_rows / validate_comparison_rows (catalog_lib) report any
     unrecognized, wrong-width, indented, or nameless entry row, and any per-stage
     COMPARISON row whose Evaluated cell isn't a verdict token, with file and line
     number (#198). Offline, gating, on by default.

  P. WORKFLOW-STACK DRIFT (opt-in, --workflow-drift, REPORT-ONLY) — WORKFLOW.md and
     STACK.md must not give a newcomer two different answers to "what do I use for X".
     Every STACK pick (matched by owner/repo slug, not display name) must appear
     somewhere in WORKFLOW.md; the reverse is not required, since WORKFLOW legitimately
     lists non-STACK CONDITIONAL options. Offline.

  Q. ELIMINATE-ONLY BULK TRIAGE — an eval marked "triaged: bulk" may only read SKIP or
     stay at discovery-log; it may never carry ADOPT/KEEP/CONDITIONAL. A false SKIP is
     cheap and reversible, a false ADOPT poisons STACK, and K's honesty-disclaimer
     escape hatch would otherwise let a README skim carry an ADOPT. Also fails an
     UNATTRIBUTED stamp: a `**Last triaged:**` with neither the bulk marker nor
     `<!-- triaged: human -->` is unpoliceable, not innocent — Q can only constrain a
     lane it can identify, so a bare date looks exactly like a lane that behaved (#327).
     The human marker exempts the verdict ceiling, since reaching a real verdict is what
     a human pass is for. This is what makes eliminate-only mechanical rather than a
     promise. Offline, gating, on by default.

  S. SKILL TEST-DESIGN (opt-in, --skill-design, REPORT-ONLY) — every skill/plugin-Type
     eval should record at least one skill dimension (a Triggering test or a
     with-skill-vs-baseline A/B) per TEMPLATE.md (#38). Conservative by design: an eval
     counts as compliant on any triggering/A-B vocabulary, so an honest measured eval is
     never false-flagged. A tracked metric, not a gate. Offline.
     (Was a second "Q" until #317 — Q belongs to eliminate-only, which is referenced by
     letter in CLAUDE.md, triage.py, TEMPLATE.md, routines.md and the triage-lead skill.)

  T. LEAD HEADLINE OVERREACH (opt-in, --lead-headlines, REPORT-ONLY) — a COMPARISON row
     reading `discovery-log` says the tool was never exercised, so its eval is notes,
     not a recommendation. 324 of them nonetheless opened `## Verdict` with **CONDITIONAL**,
     a word ADR-0005 grants only to a tool we ran or one carrying a real adopt-if gate.
     #324 relabelled them to `discovery-log — tentative read`; this keeps them relabelled.
     Scoped to REVIEW/SOURCE-ONLY: a run-backed CONDITIONAL has earned the word, and
     there the row is the stale half — a human's verdict call, not a headline defect.
     Report-only; the survivors are escalations awaiting a human (#259). Offline.

  R. METADATA STALENESS (opt-in, --metadata-staleness, REPORT-ONLY) — repo-metadata.json
     is a committed snapshot the triage bands rest on, and it rots in one direction:
     a repo archived after our last refresh keeps `archived: false`, so it never
     reaches the P1 successor-check band and nobody is told. Ages the cache from the
     per-record `fetched_at` stamp refresh-metadata.py writes (`pushed_at` is the
     REPO's push date, not ours). Unstamped records report undated, never backfilled.
     Offline (#260). Cannot become a gate: it would fail for a reason no code change
     caused, and its only fix needs the network CI must not depend on.

  U. CATALOG-ENTRY MIRROR DRIFT (opt-in, --catalog-mirror, REPORT-ONLY) — TEMPLATE.md
     has every eval close with a `## Catalog entry` copy of its CATALOG.md row: a fact
     restated in ~520 places with no generator and no test, so it drifted (#345). Four
     kinds, reported apart because they are not equally dangerous. LINK — the eval and
     the catalog name different repos, so a rename leaves the eval asserting a dead
     slug and the stars/license it was written against (#336; `herdr` was SKIP-eligible
     on exactly this). ORPHAN — an embedded row naming no catalogued tool. TEXT — the
     one-liner/problem/overlaps cells disagree; not cosmetic, since triage.py bands
     leads from the overlaps cell. AMBIG — two catalog rows collapse to one name_key
     ('agent-skills' vs 'agentskills'), so the mirror cannot be identified; resolution
     is exact-name-first for this reason, and an ambiguous fallback resolves to nothing
     rather than to a coin flip. CASE — the URLs differ only in capitalization, which
     GitHub redirects; kept out of LINK so that bucket stays actionable, but printed,
     not filtered. Offline: a string comparison between two files already in the tree,
     unlike C's ~450 requests. Report-only and deliberately NOT a bulk fixer — #345's
     sequencing note is that a wholesale rewrite in either direction destroys real work
     in the other, because the eval side is sometimes the better text (`azure-skills`).

  V. MAINTENANCE SIGNAL (opt-in, --maintenance, REPORT-ONLY) — triage.py's P1
     successor-check band is `archived == true`, which only catches maintainers who
     flipped GitHub's flag. daytonaio/daytona (★72K, the catalog's canonical sandbox
     answer) announced discontinuation in its README in June 2026, moved development to
     a private codebase, kept `archived: false`, and sat in P3 backlog as ordinary
     un-examined work for two months (#351). Reports the two per-record signals
     `refresh-metadata.py --maintenance` writes: `discontinued` (the README banner
     phrase, quoted so a human judges the phrase rather than trusting the regex) and
     `license_lost` (a real license that became NONE/404 since the last snapshot).
     A match is a CANDIDATE, not a disposition: the phrase's subject may be a component
     or a version rather than the repo (giskard-oss's "no longer actively maintained"
     is about Giskard **v2** while the repo ships v3), which no regex resolves. That is
     why the phrase is quoted in the output and why this detector never bands anything.
     Deliberately NOT a pushed_at threshold — dormancy is not discontinuation, and
     `plandex` vs `ralph` is why. Sorted strongest-verdict-first: a dead tool we still
     recommend outranks a dead lead nobody was going to reach. An uncollected signal
     reports 0 RECORDS, never 0 findings — absence of the field means "not collected".
     Offline (reads the committed cache).

  W. P0 SCOPE MISMATCH (opt-in, --scope, REPORT-ONLY) — next-evals.py scores a lead as
     2*overlap_pressure + stage_gap_weight + evidence_bonus. All three terms measure how
     much ATTENTION a lead attracts; none asks whether it is a tool this catalog is FOR.
     So a row can be both clearly out of scope and highly ranked — and ranking high puts
     it in P0 measure, the one band an unattended pass may not write to (#353). Overlap
     pressure is the trap: a framework accumulates pressure from the very rows SKIPped
     alongside it, so the more thoroughly a class is eliminated, the higher its survivors
     score. `pydantic-ai` sits in P0 at pressure 12 while `agent-kit`, same class, was
     disposed in P3.
     Reports leads whose OWN EVAL concedes the WORKFLOW.md exclusion — "visual/programmatic
     agent builders — for building AI products, not for your own dev workflow" — gated to
     the framework/platform Types that exclusion is about. The detector does not decide
     scope; it finds evals that already said it, which is why the conceding phrase is
     QUOTED (V's rule) and why it bands nothing.
     Two bucketing rules keep it precise. An eval that argues it CLEARS the bar is bucketed
     apart, not counted — `fast-agent` and `sandcastle` quote the exclusion in order to
     distinguish themselves from it, and `opik`/`helicone` concede tangency while asserting
     "catalog-relevant as the obs layer". That is detector B's HONEST-vocabulary shape:
     widen the clearance vocab if it false-flags, do not tighten the concession vocab.
     The Type gate drops `mirrord` (a k8s tool whose eval says "not a coding agent" about
     itself) and `12-factor-agents` (a reference). Both survived the phrase match alone.
     Report-only: the immediate item is a HUMAN read of a P0 lead, and moving that
     authority is exactly what #353 declined to do. Offline.

  X. COLLAPSED CATALOG IDENTITY (opt-in, --identity, REPORT-ONLY) — a row that names a
     COMPONENT of an artifact catalogued as a WHOLE is not an independent lead. The P3
     lane hit this five times from both directions before it was filed (#343): three
     separate leads for skills that all ship in `mattpocock/skills` (a STACK pick), and
     `jira`+`confluence`, which are one repo. Three observed effects — the queue is
     overstated (installing the pack settles all three at once), a redundancy verdict
     between the two is meaningless (that is the same thing, not a competitor), and the
     eliminate-only band cannot act, so every pass spends a note re-explaining why.
     Groups catalog rows by resolved `owner/repo` and splits them by whether the CATALOG
     links already distinguish the rows:
       SETTLED   — a discovery-log lead sharing a slug with an ADOPT/KEEP row. Strongest:
                   the decision is made; the lead is a facet of an adopted artifact.
       COLLAPSED — a lead sharing a slug with other rows, none of them settled.
       FACETED   — every row in the group links its own subpath, so the catalog already
                   distinguishes them. Printed, never counted: `claude-plugins-official`
                   (8 rows, 8 subpaths) and `modelcontextprotocol/servers` (3 and 3) are
                   monorepos of independently-installable artifacts, which is a different
                   thing from one artifact counted N times.
       DECLARED  — every member row names its container in CATALOG.md's `Ships inside`
                   column, or IS the container the others name (#343's resolution). Also
                   printed, never counted, and checked FIRST: FACETED *infers* from
                   distinct subpaths that the catalog distinguishes the rows, while this
                   means the catalog says so outright, in the column triage.py's P5 band
                   reads to keep them out of the queue.
     That link-shape split is the whole precision story — the four collapsed groups all
     have EVERY row pointing at one identical URL, so nothing in the catalog distinguishes
     them, while the faceted ones point at distinct paths.
     The two cases a slug compare structurally cannot see are exactly the two the column
     now carries by hand: a row whose pack is not itself catalogued (`presentation-creator`
     inside `getsentry/skills`) and a row whose link is the WHOLE product while the
     artifact is a component inside it (`prisma`, where the ★46.9K measures the ORM, not
     the MCP server). Neither is a finding here and neither ever will be — the column is
     where a human records what the compare cannot reach.
     Report-only, and still not a fixer. #343 asked for a decision between merging rows,
     a "ships inside" column, and excluding facets from the queue; the column was chosen,
     and it delivers the third as a consequence (triage.py's P5 band). Offline.

  Y. INSTALL-RECORD MISMATCH (opt-in, --installed, REPORT-ONLY, LOCAL-ONLY) — KEEP is
     DEFINED as the validated-INSTALLED status, STACK.md is the install list, and detector
     J gates STACK derivation against the verdict data. Every one of those rests on an
     install fact, and until now nothing looked at one (#366). It cannot be a gate: install
     status is a property of one laptop, which is exactly why it drifts unobserved.
     Reads the records a machine actually keeps — `~/.agents/.skill-lock.json` (the
     `npx skills` v3 lockfile: a `source` slug, path and hash per skill),
     `~/.claude/plugins/installed_plugins.json`, and the `~/.claude/skills/` directory —
     and joins them to ADOPT/KEEP rows of `skill`/`plugin` Type, the only Types these
     records cover.
     Joined on SLUG, never on name, because name-matching IS the bug. #332's "already
     installed/active" was a marketplace CACHE directory read as an install; three STACK
     members turned out to be name COLLISIONS, a same-named artifact from a different
     source (`code-review` is ADOPT-as-anthropics/claude-plugins-official while what is
     symlinked in is `mattpocock/skills`'s `skills/engineering/code-review`, a different
     tool with a different design). That is #343's root — identity by name rather than by
     slug — one layer out, on a filesystem where 72 skills from 16 sources are flattened
     into one directory.
       COLLISION    — the name resolves, to something from another repo. Strongest.
       NO-RECORD    — no record and no directory answers to the row at all.
       UNCATALOGUED — an installed source with no catalog row (found from the install
                      side; a scan only ever looks at what exists, never at what runs here).
     NO-RECORD is deliberately NOT called "not installed": `claude install-skill` and npm
     globals leave no entry in either record, so absence is absence OF A RECORD. The
     directory fallback is what makes it worth printing anyway. Missing record files report
     0 RECORDS, never 0 findings — V's rule, same reason. Never in `make check`: CI has no
     lockfile, and a build that fails for a reason no code change caused is worse than
     unobserved drift.

  Z. UNREAD LICENSE DECLARATION (opt-in, --license-declared, REPORT-ONLY) — GitHub's
     licensee detector reads a root LICENSE file and nothing else, so `license_spdx:
     NONE` means "no LICENSE file", not "no license". triage.py's P4 mechanical-skip
     band disposes vendored leads on that value, and 8 of 28 NONE records turned out to
     declare a license anyway — in a README `## License` section, in package.json, or in
     both (#372). Reads the `license_declared` field refresh-metadata.py writes and
     reports it against the disposition each row already carries.
       GROUNDED — the row is SKIP and its `## Verdict` rests on the license. The
                  disposition is false: `andrej-karpathy-skills` and `web-access` were
                  both SKIPped "text carrying no license grant cannot be copied in"
                  against a README reading `## License` / `MIT`. Strongest.
       CONFLICT — the README and the manifest name different licenses. The standing
                  "the LICENSE file governs" tiebreak (#26) has nothing to govern with
                  when there is no LICENSE file, so a human picks.
       RECORDED — declared elsewhere, but no verdict rests on it. The record is still
                  wrong and the next bulk pass reads it.
     The declaration is QUOTED, per V's rule: a README line naming MIT without the
     license text or a copyright holder is a thinner record than a LICENSE file, and
     whether that clears the bar is a human's call. This detector never says a tool is
     adoptable — only that the ground under a mechanical SKIP is not an absence.
     A verdict that has ALREADY withdrawn its license ground is bucketed apart and not
     counted, because an honest retraction quotes the claim it retracts and would
     otherwise flag forever — W's "argues it clears the bar" shape. Widen
     LICENSE_WITHDRAWN if it misses an honest retraction; never narrow LICENSE_GROUND
     to compensate, which would hide live findings to clear stale ones.
     Report-only: the remedy is a re-read of a human's verdict, not a build failure.
     Offline — it compares two files already in the tree.

  AB. UNENTITLED CONDITIONAL (opt-in, --conditional-gate, REPORT-ONLY) — ADR-0005
     collapsed the CONDITIONAL bucket because at 83% of rows the verdict carried no
     discriminating signal, and its rule is a DISJUNCTION: a real verdict requires
     EITHER the tool exercised OR a genuine `adopt-if:` condition ("no genuine
     condition => it is not a CONDITIONAL"). #69 demoted the 404 rows satisfying
     neither and parked point 1 — condition strings on the survivors — as an optional
     follow-up. It was never done, nothing ever asked the verdict data, and the bucket
     regrew from 12 to 33 (#407).
       UNENTITLED   — neither exercised nor gated. Counted. Two remedies, both named on
                      the line because the detector cannot pick between them: declare
                      the gate (usually a one-line edit by whoever wrote the verdict),
                      or demote to `discovery-log` — #69's operation, and the
                      eliminate-only-safe direction, since it removes a verdict rather
                      than asserting one.
       no-condition — exercised but carrying no condition string. Entitled under the
                      second clause, so NOT a finding; printed because point 1 still
                      wants a condition and that number should be visible rather than
                      implied (V's `acked`, W's `cleared`, X's `FACETED`).
     Detector T guards ONE direction of this rule — an eval headlining CONDITIONAL over
     a `discovery-log` row — and exits early on any other row verdict, so a row reading
     CONDITIONAL in COMPARISON.md itself was never examined. D, which checks that eval
     and row AGREE, passes happily when both name a verdict neither is entitled to.
     Report-only and deliberately not a bulk demotion: blanket-demoting would destroy
     the real judgment in rows whose gate was merely never written in the parseable
     form — #345's reason for refusing to bulk-fix mirror drift in either direction.
     Offline — it reads files already in the tree.

  AE. WORKFLOW RECOMMENDS A SKIP (opt-in, --workflow-skips, REPORT-ONLY) — detector P
     guards ONE direction of "the manual and the install list must not give a newcomer
     two different answers", and grants the reverse an explicit exemption: "WORKFLOW
     legitimately lists non-STACK CONDITIONAL options." Right for CONDITIONAL and
     `discovery-log`; not right for SKIP, which is the catalog concluding DON'T USE
     THIS. Five of the manual's 62 catalogued links carry one and none discloses it —
     including `trailofbits/skills`, listed twice as a Review-stage option and SKIPped
     because vendoring it attaches CC-BY-SA ShareAlike to the consuming repo (#414).
       RECOMMENDED — the link's row reads SKIP and the line does not say so. Counted.
       disclosed   — the line says SKIP/excluded/superseded, or sits in the manual's own
                     `## Tools Deliberately Excluded` section. Printed, never counted.
     Matched by slug, never display name (P's rule — "GSD" links to obra/superpowers).
     The disclosure vocabulary is deliberately GENEROUS: flagging a line that already
     discloses pressures a human to re-add a note that is there, inverting detector V's
     rule that flagging a healthy row costs more than missing a sick one. Report-only
     like P — the remedy is a human choosing to drop the line or disclose on it.
     Offline.

  AF. UNFALSIFIED CONTAINMENT (opt-in, --containment-evidence, REPORT-ONLY) — `Ships
     inside` is DEFINED by "empty means independently installable" (#343), so a filled
     cell asserts an artifact is NOT — and nothing could contradict one. Detector AA
     checks the other rules (findable container, no self-link); this checks the one the
     column is defined by. It matters because triage.py reads the cell FIRST and bands
     the row P5, whose disposition is "never an independent lead": a wrong cell does not
     misrank a lead, it removes it from the queue. Three were wrong — each
     `modelcontextprotocol/servers` subpath ships its own package.json while the
     container's manifest is `"private": true`, so "settle the container" named an
     operation that cannot be performed (#431).
       REFUTED   — the declared subpath publishes its own package. Counted.
       confirmed — checked, publishes nothing. NOT proof of containment (a pack may
                   publish without per-member manifests), so the test only ever REFUTES.
                   Printed, never counted.
       unchecked — no record, or the row links a repo root so there is no component to
                   ask about (already AA's SELF-LINKED). Printed, never counted.
     Collected by `refresh-metadata.py --containment` and read here offline — detector
     V's shape, and for V's reason: the finding comes from upstream's package layout, so
     gating it would fail a build for something no commit caused. 0 records is not 0
     findings. Offline.

  AG. STAGE DRIFT (opt-in, --stage-drift, REPORT-ONLY) — a tool's dev loop stage is
     written twice: every eval declares `**Dev loop stage:**`, and every COMPARISON.md
     row sits under a stage section. Nothing compared them and 16 rows sit under a stage
     their own eval never names (#453). The cost is not the ranking (no lead changes
     band) but the per-stage Summary, and through it `stage_gap_weight` — the one term
     whose job is to say which stage is starving. Ship holds THREE rows, one of them
     `worktrunk`, whose eval says Implement; that bucket produces the largest inner-loop
     gap weight there is, 6.67, and the headers taken at face value drop it to 5.00 —
     hungriest by a distance to fourth.
       DRIFT       — the section is none of the stages the eval's header names. Counted.
       STACK-DRIFT — STACK.md's stage tables are a third copy of the fact and name a
                     different stage. Counted.
     Only the six inner-loop sections are compared (the rest are categories, not
     stages); a header naming no stage is an honest non-answer; ANY named stage matching
     the section is agreement, so a multi-stage tool filed under one of its stages is
     healthy. Never says which side is wrong — the header is quoted and a human reads
     it. Offline.

  AH. UNREAD REPO INSTALL RECORD (opt-in, --repo-installs, REPORT-ONLY) — `skills-lock.json`
     is the one install record that lives INSIDE the tree, and nothing read it (#473).
     Detectors F and Y both want an install fact and both read `~/.agents/.skill-lock.json`
     — a fact about one laptop, which is exactly why Y is local-only and never runs in CI.
     That reasoning is right about the HOME lockfile and does not transfer: this one is
     committed, so it is as readable in CI as CATALOG.md. The cost is that "we already run
     this" reaches no derived surface. `vercel-labs/skills` — vendored here, its symlink and
     lockfile added in one commit — sits at `discovery-log` in P3 backlog (score 12.56),
     while `openskills`, which does the same job and which nobody here has run, sits in P2
     challenger at 18.56: six points and one band apart, in the wrong order. next-evals.py
     scores `2*overlap_pressure + stage_gap_weight + evidence_bonus`, and none of the three
     terms can see use — detector W's observation in a second dimension.
       UNEVALUATED-INCUMBENT — the repo runs it and its row is a `discovery-log` lead.
                               Counted. The queue holds a lead for a tool already in use.
       UNCATALOGUED          — the vendored source has no catalog row at all. Counted.
       evaluated             — the row carries a real verdict. This is the outcome the
                               detector exists to produce, so it is printed and never
                               counted (V's `acked`, W's `cleared`, X's `FACETED`) — the
                               headline could not reach zero otherwise.
     Resolved by SLUG, never by the lockfile KEY: `find-skills` is a skill name four packs
     use, `vercel-labs/skills` is the identity (#343/#366/#374). A missing or empty lockfile
     reports 0 records, never 0 findings — vendoring nothing is a different statement from a
     clean sweep. Report-only and staying that way: the remedy is a human running an eval,
     which is work rather than bookkeeping. Offline.

  AI. LAYER DRIFT (opt-in, --layer-drift, REPORT-ONLY) — `**Layer:**` was the one eval
     header field NOTHING read (#475). Every other one has a consumer: `**Stars:**`
     (check-stars.py), `**Last verified:**` (backfill-lastverified.py + the staleness
     sweep), `**Evidence:**` (backfill-evidence.py, tier-stack.py), `**Last triaged:**`
     (detector Q), `**Dev loop stage:**` (detector AG). Layer had a comment and three test
     fixtures. It is not decorative — CLAUDE.md's opening states the three-layer model and
     TEMPLATE.md declares a CLOSED set — and the fact is written in three places, all
     drifted.
       DRIFT      — a WORKFLOW.md `| Layer |` row whose eval header names a different
                    layer. 18 of 34 comparable rows, 53%, against AG's 5% for the STAGE
                    axis of the very same tables. Counted.
       SELF-DRIFT — a tool the `## Adopting This Workflow` ladder and a stage table file
                    differently: 12 of the 15 named twice. Internal to one file, so it
                    cannot be a resolution artifact, and it is the copy a newcomer acts
                    on — the ladder's Process heading reads "NO INFRASTRUCTURE NEEDED"
                    over four tools the tables file under Tooling. Counted.
       UNDECLARED — an eval whose `**Layer:**` names none of the three: 30, in five
                    invented vocabularies (Harness x12, Reference x9, Platform, Skill
                    pack, N/A). Counted.
       no-layer   — no `**Layer:**` line at all. Printed, never counted.
     AG's rules carry over verbatim: ANY named layer matching is agreement (`Process /
     Tooling` filed under either is healthy), the header is QUOTED because the detector
     cannot say which side is stale, and it bands nothing. The ladder's FOURTH layer name
     (`Orchestration`, in no template, no eval header and no stage table) is reported
     verbatim rather than normalised — the name is the finding. Report-only: every remedy
     is a human choosing between two judgements. Offline.

  AJ. LINK IDENTITY (opt-in, --link-identity, REPORT-ONLY) — every identity fix this repo
     has landed asked the same question in ONE direction: given a slug, which catalog row
     is it about (#343/#366/#374/#413/#457/#463/#465). Nothing asked the other one — given
     the NAME a link puts in front of a reader, does the URL under it point at that tool.
     It does not, 8 times, and 4 are in `STACK.md`, the page whose whole purpose is to be
     executed (#416): `| [GSD](github.com/obra/superpowers) | ... |
     claude install-plugin obra/superpowers |`, so a reader who wants GSD installs
     `superpowers` — a different catalogued tool, different owner, different verdict, and
     it ships none of GSD's skills. GSD's own MEASURED eval calls that framing "mistaken".
       MISNAMED — the link's text resolves to catalogued row A; its URL's slug resolves to
                  a set of rows not containing A. Counted.
     Every other detector passes, and all for one reason: they resolve by SLUG, and
     `obra/superpowers` is a good ADOPT row. J derives STACK from the ledger and finds it
     ADOPT. P demands every STACK pick appear in WORKFLOW.md and finds `superpowers` on
     line 77 — note what that agreement is worth, since the manual never names GSD at all,
     so the two pages agree about a tool the install list is not recommending. AE asks
     whether a WORKFLOW link carries a SKIP. U never reads STACK. The one fact none of
     them holds is the link's own TEXT.
     Both sides must resolve or the link is not walked (907 do), which is what keeps it
     conservative. The precision rule is that the healthy set is EVERY row behind the slug
     (`rows_for_slug`), never the one a single-answer resolver picks: STACK and the evals
     link a pack member at the pack ROOT, #465's documented healthy shape, and 85 walked
     links sit behind a shared slug — a first-row resolver flags 49 of them, all healthy.
     Report-only and not a fixer: the repair reaches STACK, the ledger, CATALOG prose and
     8 SKIP verdicts, which is a per-item human read (#345). Offline.

  AC. LICENSE HEADER vs RECORD (opt-in, --license-header, REPORT-ONLY) — every eval
     header restates an upstream fact by hand (`**License:** none specified`) next to
     `repo-metadata.json`, which holds the same fact for the same repo. Nothing
     compared them, and 7 of 646 comparable evals disagree — including a SKIP whose
     whole stated ground is "no declared license" against a record reading MIT (#411).
       UNGROUNDED — the header asserts an ABSENCE and the record names a license. The
                    load-bearing kind: an absence is the one ground a mechanical SKIP
                    may rest on (#372), so contradicting it can invalidate a
                    disposition, not merely a fact.
       CONFLICT   — both name a real license and no family is shared. Milder, still
                    wrong. Families, not strings, and a SET of them: a header reading
                    `Apache-2.0 (docs CC-BY-4.0)` agrees with a record naming either.
       redirected — `resolved_name` differs in its OWNER, so the record arrived through
                    a redirect and describes the DESTINATION. Printed, never counted:
                    assuming the record wins would pressure a human to copy a
                    known-false fact into a header (V's rule inverted).
     This is #372's shape in the file #372 did not look at: detector Z reports when the
     RECORD understates the license (`NONE` = no LICENSE *file*), and fires only on
     `NONE` — so it can never see an understatement on the EVAL's side. For the same
     reason a record reading NONE/NOASSERTION/404 is skipped here rather than
     re-reported: two detectors scoring one row is how a count stops meaning anything.
     A vague header (`n/a`, `unknown`) is an honest non-answer and never a conflict —
     check-stars.py's rule, which refuses to grade a legitimately-`n/a` field.
     Stars and `Last updated` are deliberately OUT of scope: they are point-in-time
     facts that SHOULD move as the repo does, and reporting them would be --staleness
     a second time. A license is a ground, and changes rarely.
     Report-only: the remedy is a human re-reading a LICENSE file, and the record can
     be the wrong side. Offline — two files already in the tree.

  AD. DUPLICATE EVALS (opt-in, --duplicate-evals, REPORT-ONLY) — `prisma-mcp.md` carries
     a written CONDITIONAL while its row reads `discovery-log` / `SOURCE-ONLY` — the
     value backfill-evidence assigns to "a name with no eval" — so NEXT-EVALS.md queues
     an evaluation that already exists, and detector D, whose job IS that an eval agrees
     with its row, cannot see the disagreement because it cannot find the eval (#412).
       SHADOWED  — the row resolves to the weaker of two claimants (a real verdict where
                   the resolved one has none, or higher Evidence), so the row reports
                   less than the tree holds. A wrong record, not merely a redundant one.
       DUPLICATE — the row already resolves to the stronger file; the second is a
                   redundant eval of one tool.
     An eval CLAIMS the row its `## Catalog entry` mirror names, LINK OR NO LINK — #401's
     ruling that an unlinked entry is still a catalogued tool. The same filter still sits
     in `name_aliases`, which is why the stubs were written: TEMPLATE.md mirrors carry a
     bare name, so the clause discards exactly the cell that says which row an eval
     claims, and three of these stubs were created in ONE triage pass (#339) beside evals
     that already existed. Two precision rules read off the corpus: an eval embedding
     more than one mirror row is a COMPARISON document whose rows are references, not
     claims (`cost-observability` embeds tokencost/Infracost/abtop); and resolution is
     EXACT catalog name first, since `agent-skills` and `agentskills` collapse to one
     name_key (U's AMBIG example) but are two rows with two evals.
     Report-only: merging two evals is a human's call every time — sometimes the stub's
     triage note is the newer thinking and belongs in the older file. Offline.

  AA. UNACTIONABLE CONTAINMENT (opt-in, --containment, REPORT-ONLY) — `Ships inside`
     (#343) makes containment machine-readable, and triage.py reads it FIRST to band a
     row P5, whose disposition is "settle the container ... never an independent lead".
     Nobody checked that the container is findable: the cell is free text, and its two
     documented rules (a slug, never a display name; empty means independently
     installable) are enforced by nothing (#405).
       UNROWED     — the declared container has no catalog row, so P5's disposition
                     names something not in the inventory. This is the case CLAUDE.md
                     records as invisible to X and needing a human — true before the
                     column existed, a slug compare after it.
       SELF-LINKED — the row's own link IS the container's repo root, so it asserts
                     "I am a component of X" while pointing at X. Every fact hanging
                     off that link then describes the container: prisma's ★46.9K
                     measures the ORM, not the MCP server.
     A row can carry either independently, so they are reported apart — UNROWED wants a
     catalog row, SELF-LINKED wants a narrower link (or no declaration). Resolution keys
     on the URL SLUG, never the display name: the column stores
     `anthropics/claude-plugins-official` while the row is named
     `claude-plugins-official`, and that gap is why this went unlooked-at.
     Report-only, because each finding's remedy is a human deciding WHICH fact is wrong.
     Offline — it reads one file already in the tree.

Usage:
  python3 audit-evals.py              # A + B + D + G + J + K + O + Q (all offline but A)
  python3 audit-evals.py --offline    # B + D + G + J + K + O + Q only (no network)
  python3 audit-evals.py --installs   # install resolver only
  python3 audit-evals.py --fabrication # fabrication classifier only
  python3 audit-evals.py --verdicts   # verdict-sync only (offline)
  python3 audit-evals.py --comparison # COMPARISON.md vs CATALOG.md consistency (offline)
  python3 audit-evals.py --drift      # STACK.md vs verdicts + exclusion ledger (offline)
  python3 audit-evals.py --verdict-evidence  # ADOPT/KEEP must be run-backed or disclaimered (offline)
  python3 audit-evals.py --rows       # malformed CATALOG/COMPARISON table rows (offline)
  python3 audit-evals.py --bulk-triage  # bulk-marked evals may only SKIP (offline)
  python3 audit-evals.py --scope      # P0 leads whose eval concedes it is out of scope (offline)
  python3 audit-evals.py --identity   # catalog rows that are facets of one artifact (offline)
  python3 audit-evals.py --installed  # ADOPT/KEEP rows vs this machine's install records (local)
  python3 audit-evals.py --license-declared  # 'NONE' licenses declared outside a LICENSE file (offline)
  python3 audit-evals.py --containment  # `Ships inside` declarations P5 cannot act on (offline)
  python3 audit-evals.py --conditional-gate  # CONDITIONAL rows entitled to neither ADR-0005 clause (offline)
  python3 audit-evals.py --license-header  # eval `**License:**` headers vs repo-metadata.json (offline)
  python3 audit-evals.py --duplicate-evals  # COMPARISON rows with more than one eval file (offline)
  python3 audit-evals.py --workflow-skips  # WORKFLOW.md links whose catalog row reads SKIP (offline)
  python3 audit-evals.py --containment-evidence  # `Ships inside` cells npm refutes (offline)
  python3 audit-evals.py --stage-drift   # rows filed under a stage their eval disowns (offline)
  python3 audit-evals.py --repo-installs  # sources this repo vendors but never judged (offline)
  python3 audit-evals.py --layer-drift   # Process/Tooling/Infrastructure disagreements (offline)
  python3 audit-evals.py --link-identity  # links naming one tool and pointing at another (offline)
  python3 audit-evals.py --links      # link-rot sweep only (slow, ~450 requests)
  python3 audit-evals.py --archived   # archived-repo report (slow, ~450 gh-api calls)
  python3 audit-evals.py --skills     # skill-evidence backlog report (offline)
  python3 audit-evals.py --overlaps   # dangling overlap-reference report (offline)
  python3 audit-evals.py --clusters   # overlap clusters still awaiting a pick (offline)
  python3 audit-evals.py --savings-claims  # unverified token-savings headlines (offline)
  python3 audit-evals.py --evidence   # declared Evidence-field distribution (offline)
  python3 audit-evals.py --staleness  # flag evals past their last-verified threshold (offline)
  python3 audit-evals.py --metadata-staleness  # age the repo-metadata.json cache (offline)
  python3 audit-evals.py --lead-headlines  # discovery-log leads claiming a verdict (offline)
  python3 audit-evals.py --selftest   # unit-test the evidence classifier (offline)

Exit code is non-zero if any gating detector finds a problem — a BROKEN install
(A), a FABRICATION candidate (B), a VERDICT mismatch (D), COMPARISON drift (G),
STACK-derivation drift (J), a WEAK-backed ADOPT/KEEP verdict (K), a MALFORMED
table row (O), or link rot (C, when --links is run) — so it can gate CI or a
pre-commit hook. E (skill evidence), F (dangling overlaps), and I (evidence field)
are report-only and never affect the exit code; --selftest exits non-zero on a
failing assertion, so it can gate alone.
"""
import collections
import contextlib
import datetime
import functools
import glob
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_sibling(name, filename):
    """Load a hyphenated sibling script as a module, ON DEMAND.

    triage.py loads THIS module at its own import time, so anything here that needs
    triage.py must import it lazily or the two recurse. Called from a detector rather
    than at module scope, the nested copy never re-enters the detector, so it
    terminates at depth 2."""
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
TIMEOUT = 15

# Staleness thresholds in days, by eval Type (#65). Fast-moving categories rot sooner
# than stable references — configured in ONE place. Tune here, not per detector call.
STALENESS_DAYS = {
    "harness": 120, "MCP server": 120, "framework": 120, "platform": 120,  # fast-moving
    "tool": 180, "skill": 180, "plugin": 180,                              # moderate
    "reference": 365,                                                       # stable
}
DEFAULT_STALENESS_DAYS = 180

# How old a repo-metadata.json record may get before detector R reports it (#260).
# The cache answers "is this repo archived / what license" for the triage bands, and
# a repo archived tomorrow keeps its stale record until someone refreshes. Archival
# and relicensing move on a scale of months, so this sits with the fast-moving eval
# categories rather than below them. A starting heuristic — tune here.
METADATA_STALE_DAYS = 120

# ---------------------------------------------------------------- helpers
# Detector A's three outcomes. `ok` and `dead` are verdicts about the artifact;
# `unknown:<reason>` is a fact about the request, and the two must never collapse
# (#447). Only a 404 means gone — detector C's rule (#319), which lived forty lines
# from here and which A never learned, in either direction: the HTTP checkers folded
# every 429/5xx/timeout into BROKEN and failed the build for a reason no commit caused,
# while the subprocess checkers folded a missing binary into RESOLVED and printed a
# clean bill of health over targets they never reached.
OK, DEAD = "ok", "dead"

# How many distinct unreachable targets to name before summarising the rest.
UNCHECKED_SHOWN = 10

def _unknown(reason): return f"unknown:{reason}"

def http_status(url):
    """`ok` / `dead` / `unknown:<reason>` for a registry metadata URL.

    A 404 is the only status that means the package is gone. A 429 (PyPI and crates.io
    both rate-limit a 24-way burst), a 5xx, a timeout, a DNS failure and a TLS error all
    mean this run could not answer — and a gate that treats them as `dead` is
    non-deterministic: run 31207021528 failed `make check` on `BROKEN [crates] abtop`
    while crates.io was answering 200, and re-running the identical tree passed."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ai-tooling-audit"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return OK if r.status == 200 else _unknown(f"HTTP {r.status}")
    except urllib.error.HTTPError as e:
        # An HTTPError IS the response object, so the error path has a socket to close
        # exactly as the `with` above does. Only this branch leaked, which is why it went
        # unseen: on a healthy network almost every reply is a 200 (#455).
        with contextlib.closing(e):
            return DEAD if e.code == 404 else _unknown(f"HTTP {e.code}")
    except Exception as e:  # noqa: BLE001 — every non-404 outcome is inconclusive by design
        return _unknown(type(e).__name__)

# `npm view` and `gh api` exit non-zero for a missing package AND for a registry 5xx,
# a rate limit or an auth wall, so the exit code alone cannot classify. Both name the
# 404 explicitly when that is what happened (`npm error code E404` / `404 Not Found`;
# `gh: Not Found (HTTP 404)`), so the marker is what distinguishes gone from unreachable.
_NOT_FOUND = re.compile(r"\bE404\b|404 Not Found|HTTP 404|\bNot Found\b", re.IGNORECASE)

def _run_status(cmd):
    """`ok` / `dead` / `unknown:<reason>` for a CLI existence probe.

    A missing binary and a hung process are `unknown`, not `ok`: returning True there
    counted 57 of 85 targets as resolved without reaching any of them, which is #319's
    "silence is not success" inside the detector that gates. Without the timeout a
    single wedged `npm view` blocks the whole gate; without the FileNotFoundError catch,
    a machine with no `npm` takes the run down with a traceback."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT, check=False)
    except subprocess.TimeoutExpired:
        return _unknown("timeout")
    except FileNotFoundError:
        return _unknown(f"no {cmd[0]}")
    if r.returncode == 0:
        return OK
    return DEAD if _NOT_FOUND.search(r.stderr + r.stdout) else _unknown("exit "
                                                                       f"{r.returncode}")

def npm_exists(pkg):
    return _run_status(["npm", "view", pkg, "version"])

def gh_repo_exists(slug):
    return _run_status(["gh", "api", f"repos/{slug}", "--jq", ".full_name"])

def pypi_exists(pkg):   return http_status(f"https://pypi.org/pypi/{pkg}/json")
def crates_exists(pkg): return http_status(f"https://crates.io/api/v1/crates/{pkg}")

# ---------------------------------------------------------------- A. installs
PKG_CLEAN = lambda s: re.sub(r"[<>=].*|\[.*?\]|['\"]|@latest$", "", s).strip()

# A package token that is really a placeholder / prose fragment, not installable.
PLACEHOLDER = re.compile(r"^\.+$|\.\.\.|[<>{}|&]|^-|,$|"
                         r"^(install|installer|command|version|CLI|skills|name|pkg|package|foo|bar)$", re.IGNORECASE)
# If a backtick command is discussed as the WRONG/non-existent option ("not `npx x`",
# "listed as `npx x` (doesn't exist)", "earlier draft showed `x`, which does not exist"),
# it's a correction note, not an install to resolve. Markers can sit on either side.
NEGATION = re.compile(r"\b(not|non-?existent|does ?n.?t exist|do(es)? not exist|no such|wrong|"
                      r"instead of|isn.?t|rather than|earlier draft|was wrong|404|nonexistent)\b", re.IGNORECASE)

# A package name, after PKG_CLEAN has taken quotes, PEP 508 extras and a version pin off.
# Anything else on an install line ends the package list — see `_install_packages`.
_PKG_TOKEN = re.compile(r"^@?[A-Za-z0-9._][A-Za-z0-9._/-]*$")

# `npm install`, and the two aliases npm documents for it. Requiring the literal word left
# 10 real install commands invisible to a GATE whose headline read "86/86 checked" (#485).
_NPM_INSTALL = re.compile(r"^npm +(?:install|i|add) +(.*)$")
_PIP_INSTALL = re.compile(r"^pip(?:x| install| ) *install +(.*)$")


def _install_packages(rest):
    """Every package on the tail of an install command, in order.

    `npm install a b c` installs three packages and the extractor used to check `a`, so
    `strands-agents-tools` had never been verified at all. Two rules keep this safe inside
    a detector that GATES, where a false BROKEN fails the build for a healthy eval:

      * a `-flag` is skipped, never treated as a package;
      * the FIRST token that is not package-shaped ENDS the list, rather than being
        skipped over. Four lines in the corpus continue past the packages with a shell
        operator (`npm install -g flowise && npx flowise start`), and a naive split would
        mint targets named `&&`, `npx` and `start`. Stopping leaves all four behaving
        exactly as they did.

    Cleaning is `PKG_CLEAN`/`PLACEHOLDER`, the same pair the single-package patterns use
    rather than a second copy — quotes, PEP 508 extras and version pins all come off there,
    which is what keeps `pip install 'markitdown[all]'` resolving as `markitdown`.
    """
    out = []
    for tok in rest.split():
        if tok.startswith("-"):
            continue
        pkg = PKG_CLEAN(tok)
        if not pkg or PLACEHOLDER.search(pkg) or not _PKG_TOKEN.match(pkg):
            break
        out.append(pkg)
    return out


def extract_installs(text):
    """Yield (kind, package) from install-like commands in markdown."""
    for m in re.finditer(r"`([^`]*)`", text):
        cmd = m.group(1).strip()
        # skip commands framed as the WRONG/non-existent option (correction notes), either side
        window = text[max(0, m.start() - 70):m.end() + 60]
        if NEGATION.search(window):
            continue
        # Multi-package forms first: these consume the whole tail of the command.
        multi = ((_PIP_INSTALL, "pypi"), (_NPM_INSTALL, "npm"))
        matched = False
        for pat, kind in multi:
            mm = pat.match(cmd)
            if mm:
                matched = True
                for pkg in _install_packages(mm.group(1)):
                    yield kind, pkg
                break
        if matched:
            continue
        for pat, kind in [
            (r"^cargo install +([A-Za-z0-9._-]+)", "crates"),
            (r"^npx +(?:-y +)?(@?[A-Za-z0-9._/-]+)", "npm"),
            # `claude plugin marketplace add <owner/repo>` is the real form. `claude
            # install-plugin` / `install-skill` — what STACK.md told a reader to run for
            # ten months — are not subcommands at all, and this pattern resolved their
            # ARGUMENT (the repo exists) while never asking whether the VERB does (#487).
            (r"claude plugins? marketplace add +([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)", "gh"),
        ]:
            mm = re.match(pat, cmd)
            if mm:
                pkg = PKG_CLEAN(mm.group(1))
                if pkg and not PLACEHOLDER.search(pkg):
                    yield kind, pkg

def audit_installs(ctx):
    """Detector A: every install command must point at a real artifact.

    Returns (broken, unknown, targets) — the same (rel, kind, pkg) shape for the first
    two, with a reason appended to each unknown, plus the unique-target count so the
    caller can report n/total the way detector C does. The split is the whole point
    (#447): `broken` is a verdict about the artifact and gates, `unknown` is a fact
    about the request and must not, or the gate becomes non-deterministic — but it is
    printed and counted, because "could not check" and "checked and fine" being the same
    value is the defect #319 fixed one detector over.

    Resolution runs concurrently (85 unique targets, ~22s serial) — no two lookups
    depend on each other, so this mirrors audit_links' ThreadPoolExecutor. Mentions are
    collected first and filtered afterwards, which keeps the reported order and the
    per-occurrence shape exactly as they were: lookups DEDUPE, findings do NOT, so a
    broken package cited in three evals is still three findings."""
    import concurrent.futures
    files = ["STACK.md", "CATALOG.md", *sorted(glob.glob("evaluations/*.md", root_dir=ctx.root))]
    checkers = {"pypi": pypi_exists, "crates": crates_exists, "npm": npm_exists, "gh": gh_repo_exists}
    mentions = []  # (rel, kind, pkg) in file order — this IS the reported order
    for rel in files:
        if not os.path.exists(ctx.path(rel)): continue
        for kind, pkg in extract_installs(ctx.read(rel)):
            mentions.append((rel, kind, pkg))
    targets = sorted({(kind, pkg) for _rel, kind, pkg in mentions})
    # max_workers matches audit_links. Do NOT raise it: PyPI and the npm registry
    # rate-limit, and a 429 would surface as a false BROKEN.
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
        seen = dict(zip(targets, ex.map(lambda t: checkers[t[0]](t[1]), targets), strict=True))
    broken = [(rel, kind, pkg) for rel, kind, pkg in mentions if seen[(kind, pkg)] == DEAD]
    unknown = [(rel, kind, pkg, seen[(kind, pkg)][len("unknown:"):])
               for rel, kind, pkg in mentions if seen[(kind, pkg)].startswith("unknown:")]
    return broken, unknown, len(targets)

# ---------------------------------------------------------------- B. fabrication
# Disclaimers / review verbs that mark an eval as an HONEST not-run review.
HONEST = re.compile(r"not installed|not run|did not|do not|source-grounded|architecture review|"
                    r"readme review|readme[- ]based|repo[/ ].*review|review[ -]based|inspection — not|"
                    r"not exercised|not hands-on|review only|mechanism review|scope review|review — not|"
                    r"not connected|not deployed|not reproduced|not a hands-on|source review|"
                    r"source-and-docs|architecture[- ]level|surface[- ]area review|"
                    r"\bread (the|every|all|\d|through|\d+)|\bfetched\b|\binspected\b|\bexamined\b|"
                    r"\benumerated\b|\bcounted\b|\bdiffed\b|queried the (github|rest) api|github[- ]api|"
                    r"as (installed|checked out) on this machine|mentally|applied (to|against)|"
                    r"could not install|attempted to apply", re.IGNORECASE)
# Specific run claims a fabricator invents (used only when no honest/verified marker is present).
RUN_CLAIM = re.compile(r"\b(ran it|we ran|i ran|ran the|ran against|added the .* server|"
                       r"used it (on|to|across)|deployed |generated |executed |"
                       r"launched |wrapped the|let it index|pointed it|fed it)\b", re.IGNORECASE)
# Markers of a genuine, trustable hands-on run.
VERIFIED = re.compile(r"\*\*hands-on\*\*|verified hands-on|verified (live|:)|re-verified|re-ran|"
                      r"ran it \*\*live\*\*|ran it (live|for real)|ran the .*\blive\b|live from inside|"
                      r"installed (it|the real|via|globally|as a skill|as a claude)|"
                      r"installed \(|pip[- ]?install.*\bran\b|exercised the|one real script execution|"
                      r"ran `|loaded all tool schemas", re.IGNORECASE)

def how_section(text):
    m = re.search(r"#+\s*How we tested.*?(?=\n#+\s|\Z)", text, re.DOTALL | re.IGNORECASE)
    return m.group(0) if m else ""

# --- gate coverage (#481) --------------------------------------------------------
# #467's rule — a check reports the population it walked, because `0 findings` and
# `0 examined` print identically — reached all thirteen report-only detectors and NONE
# of the seven gates, where a bare `OK` is the strongest claim in the file and the line
# CI goes green on. Each population below lives in ONE function read by both the gate
# and its headline: two extractors for one fact is #443, and a headline recomputing a
# detector's own filter would drift from it on the first edit.
#
# A gate that runs SEVERAL checks reports SEVERAL numbers. Forcing one `walked/total`
# onto J's three checks or O's two files would reintroduce the exact defect #479 just
# removed from detector U — one number standing for two populations.
#
# The invariant, pinned in both directions: coverage never reaches `rc`. A gate's exit
# code is a function of its findings alone, so adding a population here is observably
# free of behaviour change. That is the whole difference between this and a new gate.


def fabrication_population(ctx):
    """The evals B can examine. One with no `## How we tested` section asserts nothing
    about a run, so there is nothing to classify — an abstention, not a silent pass."""
    return [ev for ev in ctx.evals if ev.how]


def audit_fabrication(ctx):
    return [ev.name for ev in fabrication_population(ctx)
            if ev.evidence.is_fabrication_candidate]

# ---------------------------------------------------------------- C. link rot
def check_repo(slug):
    """Return 'ok', 'dead', 'moved:<new>', or 'unknown:<reason>' for a github
    owner/repo slug.

    'unknown' exists because this used to fold every non-404 into 'ok' (#319).
    GitHub answers this detector's ~600-request unauthenticated burst with HTTP
    429, so EVERY link — including live ones like torvalds/linux — came back
    'ok' and the sweep printed a clean bill of health having verified nothing.
    "Could not check" and "checked and fine" must not be the same value: silence
    is not success."""
    url = f"https://github.com/{slug}"
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "ai-tooling-audit"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            final = r.geturl().replace("https://github.com/", "").rstrip("/")
            if final.lower() != slug.lower():
                return f"moved:{final}"   # C's alone — detector A has no analogue
            return OK
    except urllib.error.HTTPError as e:
        # Closed for the same reason as http_status, and this is the checker it matters
        # for: this docstring's own ~600-request burst comes back 429, so the documented
        # normal case leaked one response per link (#455).
        with contextlib.closing(e):
            # DEAD is the one status that genuinely means "gone"; a 429 rate limit, a
            # 5xx or an auth wall is not a verdict. Same constants detector A uses —
            # one vocabulary, not two copies of it forty lines apart.
            return DEAD if e.code == 404 else _unknown(f"HTTP {e.code}")
    except Exception as e:  # noqa: BLE001 — every non-404 outcome is inconclusive by design
        return _unknown(type(e).__name__)   # timeout / DNS / TLS — also not a verdict

def audit_links(ctx):
    """(problems, unknowns, total) — problems are dead/moved links, unknowns are
    links this run could not verify. Callers MUST NOT report success while
    unknowns is non-empty; an inconclusive sweep is not a passing one."""
    import concurrent.futures
    slugs = catalog_lib.github_repos(ctx.catalog)
    problems, unknowns = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
        for slug, res in zip(slugs, ex.map(check_repo, slugs), strict=True):
            if res.startswith("unknown:"):
                unknowns.append((slug, res[len("unknown:"):]))
            elif res != "ok":
                problems.append((slug, res))
    return problems, unknowns, len(slugs)

# ---------------------------------------------------------------- L. staleness sweep
def audit_staleness(ctx, today=None):
    """Detector L (#65, REPORT-ONLY): flag evals whose **Last verified:** date is older
    than its category threshold (STALENESS_DAYS, keyed by Type) — fast-moving harnesses/
    MCP servers rot sooner than stable references. `today` is injectable for tests.
    Returns (stale, undated) where stale is a list of (name, type, date, age_days,
    threshold) and undated is the count of evals carrying no last-verified date."""
    today = today or datetime.date.today()
    stale, undated = [], 0
    for ev in ctx.evals:
        d = ev.last_verified
        if d is None:
            undated += 1
            continue
        threshold = STALENESS_DAYS.get(ev.type, DEFAULT_STALENESS_DAYS)
        age = (today - d).days
        if age > threshold:
            stale.append((ev.name, ev.type, d.isoformat(), age, threshold))
    return stale, undated

# ---------------------------------------------------------------- R. metadata staleness
# repo-metadata.json is a COMMITTED SNAPSHOT of GitHub facts (license, archived, stars)
# that the triage bands rest on. It rots in silence and in one direction: a repo archived
# tomorrow keeps its `archived: false` record, so it never reaches the P1 successor-check
# band and nobody is told. Detector L covers evals rotting; nothing covered the cache.
#
# REPORT-ONLY on purpose, and this one cannot become a gate the way F/N might. Gating it
# would fail `make check` for a reason no code change caused — the cache ages on the
# calendar — and the only fix is `refresh-metadata.py`, which needs the network that the
# offline-gate invariant forbids CI from depending on.
#
# Age comes from a per-record `fetched_at` stamp that refresh-metadata.py writes. Records
# predating that stamp report as UNDATED rather than being backfilled: a floor date would
# assert a fetch that never happened, the same reason `**Last triaged:**` is never
# backfilled while `**Last verified:**` (which has an honest git-derived floor) is.
def audit_metadata_staleness(ctx, today=None):
    """Detector R (#260, REPORT-ONLY): age the repo-metadata.json cache. Returns
    (total, undated, stale, oldest) — total records; count with no `fetched_at`;
    a list of (slug, date, age) past METADATA_STALE_DAYS, oldest first; and the
    oldest (slug, date, age) overall, or None when nothing carries a stamp.
    A missing or unreadable cache is (0, 0, [], None), never an exception: a fresh
    clone has no cache and `make check` must still run (same tolerance triage.py's
    load_metadata() has)."""
    today = today or datetime.date.today()
    try:
        records = json.loads(ctx.read("repo-metadata.json"))
    except (OSError, ValueError):
        return 0, 0, [], None
    if not isinstance(records, dict):
        return 0, 0, [], None
    dated, undated = [], 0
    for slug, meta in records.items():
        stamp = meta.get("fetched_at") if isinstance(meta, dict) else None
        try:
            d = datetime.date.fromisoformat(stamp)
        except (TypeError, ValueError):
            undated += 1  # never stamped, or unparseable — both mean "age unknown"
            continue
        dated.append((slug, d, (today - d).days))
    dated.sort(key=lambda r: -r[2])
    stale = [(s, d.isoformat(), age) for s, d, age in dated if age > METADATA_STALE_DAYS]
    oldest = (dated[0][0], dated[0][1].isoformat(), dated[0][2]) if dated else None
    return len(records), undated, stale, oldest

# ---------------------------------------------------------------- H. archived repos
# A catalogued repo that GitHub has flagged `archived` is no longer maintained — the
# entry shouldn't read as a live recommendation without saying so. Link rot (C) can't
# catch this: an archived repo's link still resolves. This is how 4 archived entries
# (incl. gpt-engineer ★55K and a same-named superseded chrome-devtools fork's cousin)
# were found. Opt-in (uses authenticated `gh api`, so not rate-limited), report-only:
# keep notable/historical tools but expect the entry to carry a ⚠️ archived note.
def check_archived(slug):
    r = subprocess.run(["gh", "api", f"repos/{slug}", "--jq", "[.archived, .pushed_at[0:7]]"],
                       capture_output=True, text=True, check=False)
    if r.returncode != 0:
        return None
    try:
        arch, pushed = json.loads(r.stdout)
        return (bool(arch), pushed)
    except Exception:  # noqa: BLE001 — a malformed `gh` payload means 'unknown', not a crash
        return None

def audit_archived(ctx):
    import concurrent.futures
    text = ctx.catalog
    slugs = catalog_lib.github_repos(text)
    archived = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        for slug, res in zip(slugs, ex.map(check_archived, slugs), strict=True):
            if res and res[0]:
                # already disclosed in the entry? (a ⚠️ near the link)
                flagged = bool(re.search(re.escape(slug) + r".{0,400}?(?:archived|⚠️)", text, re.DOTALL | re.IGNORECASE))
                archived.append((slug, res[1], flagged))
    return archived, len(slugs)

# ---------------------------------------------------------------- D. verdict sync
# discovery-log (ADR 0001 / #69): a COMPARISON status for catalogued tools that were
# never exercised (Evidence REVIEW/SOURCE-ONLY) — leads, not verdicts. They are
# excluded from verdict-sync (D) and verdict-evidence (K): an eval's tentative
# CONDITIONAL read is the lead's notes, not a promoted verdict to enforce.
VERDICTS = catalog_lib.VERDICTS  # vocabulary defined once, in catalog_lib (#193)

VerdictCoverage = collections.namedtuple(
    "VerdictCoverage", "compared declared leads unmapped")


def verdict_pairs(ctx):
    """(eval, its COMPARISON.md verdict or None) for every eval carrying a `## Verdict`.
    One classification, read by both the gate and its headline (#443)."""
    comp = ctx.comparison_verdict_map
    return [(ev, next((comp[c] for c in ev.name_aliases if c in comp), None))
            for ev in ctx.evals if ev.verdict]


def verdict_coverage(ctx):
    """What D compared and what it declined to (#481). Two abstentions, and only one of
    them was ever stated: `leads` is the documented skip (a `discovery-log` row is a
    lead, not a verdict), while `unmapped` sat behind `# name didn't map — not a
    verdict-sync problem`, an UNCHECKED ASSERTION and the one thing a verdict-sync gate
    cannot check about itself. `design-extract` is the precedent — a tool carrying a
    written CONDITIONAL with no CATALOG.md row and no COMPARISON.md row, so D had
    nothing to sync against and passed, silently, until a report-only detector noticed
    it as a formatting disagreement. Both buckets are PRINTED and never counted: all six
    live ones are protocol, recipe and comparison documents that correctly have no row,
    and turning them into findings would flag healthy files (detector V's rule)."""
    pairs = verdict_pairs(ctx)
    leads = [ev.name for ev, cv in pairs if cv == "discovery-log"]
    unmapped = [ev.name for ev, cv in pairs if cv is None]
    return VerdictCoverage(len(pairs) - len(leads) - len(unmapped),
                           len(pairs), leads, unmapped)


def audit_verdicts(ctx):
    """Flag evals whose ## Verdict disagrees with their COMPARISON.md row.
    Tolerates: KEEP (installed/validated status) vs ADOPT, and dual verdicts
    ("ADOPT for X — CONDITIONAL otherwise") where COMPARISON matches either."""
    compatible = {frozenset(("KEEP", "ADOPT"))}  # installed-tool status ~ adopt
    flagged = []
    for ev, cv in verdict_pairs(ctx):
        ev_set = ev.verdict_set  # every verdict word — handles dual verdicts
        if cv is None:
            continue  # name didn't map — reported as coverage, never as a pass (#481)
        if cv == "discovery-log":
            continue  # lead, not a verdict — the eval's tentative read isn't synced
        if cv in ev_set:
            continue  # matches (incl. dual verdict)
        if any(frozenset((cv, x)) in compatible for x in ev_set):
            continue  # KEEP vs ADOPT etc.
        flagged.append((ev.name, ev.verdict, cv))
    return flagged

# ---------------------------------------------------------------- J. stack-derivation drift
# STACK.md must be *derivable* from the verdict data (COMPARISON.md) plus the
# exclusion ledger (STACK-LEDGER.md, #64): every ADOPT/KEEP tool is either in STACK
# or has a logged exclusion reason, and nothing in STACK contradicts its verdict.
# This kills the hand-maintained drift prior audits kept finding (abtop/codeburn,
# serena, documentation-writer). Gating, on by default. Consumes the #64 ledger.
# The trailing `(?:[^|]*\|)?` is the Install evidence column (ADR-0006 / #382), optional so
# this keeps matching a ledger written before it existed. Without it the regex — anchored to
# end-of-line — matched ZERO rows the moment a sixth column landed; the failure was loud
# rather than silent (the COMPARISON cross-check below then flags every ADOPT/KEEP tool as
# missing from the ledger), but it is a trap worth naming for the next column.
_LEDGER_ROW = re.compile(
    r"^\|\s*([^|]+?)\s*\|\s*(ADOPT|KEEP)\s*\|[^|]*\|\s*(yes|conditional|no)\s*\|\s*([^|]*?)\s*\|"
    r"(?:[^|]*\|)?\s*$", re.MULTILINE)

def _stack_member_key_map(stack_text):
    """alias key -> sorted STACK display names, for tools recommended in STACK.md.

    Keyed by BOTH link text and repo basename — so an entry installed under another
    name (GSD ← obra/superpowers) still matches. One key can name SEVERAL picks:
    `claudepluginsofficial` reaches code-review, feature-dev and pr-review-toolkit,
    which is why the value is a list and never a winner (#457)."""
    m = {}
    for pick in catalog_lib.stack_picks(stack_text):
        for k in catalog_lib.alias_keys(pick.text, pick.url):
            m.setdefault(k, set()).add(pick.text)
    return {k: sorted(v) for k, v in m.items()}

def _stack_member_keys(stack_text):
    """Tools recommended in STACK.md, keyed by BOTH link text and repo basename —
    so an entry installed under another name (GSD ← obra/superpowers) still matches."""
    return set(_stack_member_key_map(stack_text))

def _stack_picks_by_slug(stack_text):
    """(display text, link, owner/repo) for every STACK.md row that links a github repo.

    Resolution downstream keys on the SLUG, never the display text — detector P's rule,
    since names vary ("GSD" links to obra/superpowers) and a basename is not a synonym
    between two rows (#374). The LINK comes along because a slug is not always an
    identity: see `catalog_lib.resolve_link`.

    A thin alias for `catalog_lib.stack_picks` — the ONE definition of a pick, which this
    and `_stack_member_key_map` used to spell out as byte-identical regexes one file
    apart, with a third copy in tier-stack.py and two more rules elsewhere (#469)."""
    return catalog_lib.stack_picks(stack_text)


# Resolving a link to a catalog row lives in catalog_lib, next to identity_keys and
# alias_keys — the other two answers to "which row is this?" (#463, generalized in #465).
# It used to be a private `by_slug.setdefault(...)` here and in three more detectors, so
# whichever row CATALOG.md listed first answered for every row behind a shared slug.


def audit_stack_drift(ctx):
    """Detector J: cross-check STACK.md against COMPARISON.md verdicts + the ledger.
    Flags: an ADOPT/KEEP tool absent from both STACK and the ledger; a ledger row whose
    verdict disagrees with COMPARISON; an excluded row with no reason; a ledger row
    marked in-STACK that isn't actually in STACK.md; and a STACK member the catalog
    SKIPped.

    That last check is the reverse direction, added in #416. Every other check runs
    ledger -> STACK or verdict -> STACK, so a member of the INSTALL LIST whose verdict is
    SKIP passed silently: `trailofbits/skills` sat in the table and in the copy-paste
    install block for ten months after a bulk license triage SKIPped it because
    `claude install-skill` is precisely the operation that vendors the text and attaches
    its CC-BY-SA ShareAlike to the consuming repo. Gating, like the rest of J — a SKIP is
    a conclusion already reached, so agreeing with it is bookkeeping, not judgement."""
    problems = []
    comp = ctx.comparison_verdict_map
    stack = _stack_member_keys(ctx.stack)
    index = catalog_lib.link_index(ctx.catalog)
    for text, url, slug in _stack_picks_by_slug(ctx.stack):
        row, candidates = catalog_lib.resolve_link(index, text, url, slug)
        if candidates:
            problems.append(
                f"STACK pick '{text}' links {slug}, which {len(candidates)} catalog rows "
                f"claim ({', '.join(c.name for c in candidates)}) — narrow the link to the "
                "row's own subpath, or the SKIP check cannot say which one it checked (#463)")
            continue
        if not row:
            continue
        if next((comp[k] for k in catalog_lib.identity_keys(row.name) if k in comp), None) == "SKIP":
            problems.append(
                f"STACK pick '{text}' resolves to catalog row '{row.name}' ({slug}), which "
                "is SKIPped in COMPARISON — the install list recommends a tool the catalog "
                "eliminated (#416)")
    ledger_keys = set()
    for name, verdict, in_stack, reason in _LEDGER_ROW.findall(ctx.ledger):
        ids = catalog_lib.identity_keys(name)
        ledger_keys.update(ids)
        if in_stack == "no" and not reason.strip():
            problems.append(f"ledger '{name}' is excluded (no) but records no reason")
        cv = next((comp[k] for k in ids if k in comp), None)
        if cv and cv != verdict and frozenset((cv, verdict)) != frozenset(("KEEP", "ADOPT")):
            problems.append(f"ledger '{name}' verdict {verdict} != COMPARISON {cv}")
        # STACK membership legitimately fans out to basenames (GSD ← superpowers).
        if in_stack in ("yes", "conditional") and \
                not any(k in stack for k in catalog_lib.alias_keys(name)):
            problems.append(f"ledger '{name}' marked '{in_stack}' but not found in STACK.md")
    for r in ctx.comparison_rows:
        if r.verdict in ("ADOPT", "KEEP") and \
                not any(k in ledger_keys for k in catalog_lib.identity_keys(r.tool)):
            problems.append(f"{r.verdict} tool '{r.tool}' in COMPARISON is neither in STACK nor the exclusion ledger (#64)")
    return problems

# ---------------------------------------------------------------- O. row shape (gating)
# A malformed table row used to be silently skipped: the parse sites guarded with
# ad-hoc cell-count thresholds and continued past anything unrecognized, so
# reconcile-counts and backfill-evidence simply rewrote around a bad row and the
# counts quietly excluded it. Validation now happens in one place (catalog_lib)
# and a bad row is a gating finding — it corrupts the counts the suite already
# gates on (G), so it must not pass. (#198)
def audit_row_shapes(ctx):
    problems = []
    for fname, text, validate in (("CATALOG.md", ctx.catalog, catalog_lib.validate_catalog_rows),
                                  ("COMPARISON.md", ctx.comparison, catalog_lib.validate_comparison_rows)):
        problems.extend(f"{fname}:{ln} {msg}" for ln, msg in validate(text))
    return problems

# ---------------------------------------------------------------- K. verdict evidence gate
def verdict_evidence_population(ctx):
    """The evals K examines. Only ADOPT/KEEP asserts something strong enough to gate,
    so the other verdicts are out of scope by design rather than skipped — which is
    exactly why the number belongs in the headline: `38 of 693` says the gate is narrow,
    where a bare `OK` implies it swept the corpus."""
    return [ev for ev in ctx.evals if ev.verdict in ("ADOPT", "KEEP")]


def audit_verdict_evidence(ctx):
    """Detector K (#71): a strong verdict can't rest on a README skim. An ADOPT/KEEP
    eval must be run-backed (Evidence MEASURED or RUN) OR carry an explicit honesty
    disclaimer in its 'How we tested' section (Evidence.honest — the documented escape
    hatch). A REVIEW/SOURCE-ONLY ADOPT/KEEP with no disclaimer is flagged. Generalizes
    the skills-only report-only detector E into a catalog-wide gate. Offline, gating."""
    flagged = []
    for ev in verdict_evidence_population(ctx):
        if ev.evidence_level in ("MEASURED", "RUN"):
            continue  # run-backed
        if ev.evidence.honest:
            continue  # explicit not-run disclaimer present (escape hatch)
        flagged.append((ev.name, ev.verdict, ev.evidence_level))
    return flagged

# ---------------------------------------------------------------- E. skill evidence (report-only)
# A skill's value is a behaviour change, so an ADOPT verdict on a *skill* should
# rest on a measured eval (triggering and/or with-skill-vs-baseline), not a README
# review. This is a backlog report, not a gate — it does not affect the exit code.
MEASURED = re.compile(r"tiktoken|with[- ]skill|baseline|measured a/b|\ba/b\b|trigger rate|"
                      r"assertion (passed|failed)|measured ~|token.*reduction.*measured|"
                      r"\*\*hands-on,? measured|run_eval", re.IGNORECASE)
# A strong, unambiguous measurement marker — strong enough to override a *weak*
# honest-review word (e.g. "inspected"/"read"/"examined") that would otherwise
# demote a genuinely measured eval. (Real case: a measured eval that wrote
# "inspected each SKILL.md" was wrongly held in the backlog because `\binspected\b`
# lives in HONEST. Sealing precedence here makes that a decision, not an accident.)
STRONG_MEASURED = re.compile(r"measured a/b|\ba/b\b|trigger rate|assertion (passed|failed)|"
                             r"\*\*hands-on,? measured|run_eval|tiktoken|measured ~", re.IGNORECASE)

# ---------------------------------------------------------------- I. declared evidence field
# Issue #62: the *declared* evidence-strength field — how hard we looked, recorded
# explicitly as data rather than inferred from prose. Distinct from the Evidence
# class below, which *infers* fabrication/measurement signals from the How section.
EVIDENCE_LEVELS = ("MEASURED", "RUN", "REVIEW", "SOURCE-ONLY")
EVIDENCE_FIELD = re.compile(
    r"\*\*Evidence:\*\*\s*`?(" + "|".join(EVIDENCE_LEVELS) + r")\b")

# ---------------------------------------------------------------- evidence seam
class Evidence:
    """Evidentiary status of an eval's 'How we tested' section.

    The HONEST / VERIFIED / RUN_CLAIM / MEASURED regexes are consumed only here,
    so the precedence between them is decided in ONE place instead of being
    recombined differently inside each detector. The interface is the test
    surface — see selftest()."""
    def __init__(self, how):
        self._how      = how
        self.honest    = bool(HONEST.search(how))
        self.verified  = bool(VERIFIED.search(how))
        self.run_claim = bool(RUN_CLAIM.search(how))
        self.measured  = bool(MEASURED.search(how))
        self._strong   = bool(STRONG_MEASURED.search(how))

    @property
    def level(self):
        """Derive the 4-value evidence strength (issue #67) from the same honesty /
        measurement signals detector B trusts, so the backfill is reproducible and
        grounded in the eval's own text rather than hand-guessed. Precedence: a
        not-run disclaimer (REVIEW) outranks run-ish verbs; an empty How section
        means nothing was tested here (SOURCE-ONLY)."""
        if self.is_measured:                 return "MEASURED"
        if self.honest:                      return "REVIEW"
        if self.run_claim or self.verified:  return "RUN"
        if not self._how.strip():            return "SOURCE-ONLY"
        return "REVIEW"

    @property
    def is_fabrication_candidate(self):
        # claims a specific run, with no honesty disclaimer and no genuine-run marker
        return self.run_claim and not (self.honest or self.verified)

    @property
    def is_measured(self):
        # measured evidence present, and either no honest-not-run disclaimer OR a
        # strong measurement marker that overrides a weak disclaimer word
        return self.measured and (self._strong or not self.honest)

# ---------------------------------------------------------------- eval model
class Evaluation:
    """One evaluation file, parsed once. The eval-file grammar — How section,
    Verdict, dual-verdict set, catalog row, name aliases — lives here so detectors
    consume a value instead of each re-deriving it from raw markdown. Build from a
    path with from_path(); the (name, text) constructor keeps it unit-testable
    without the tree (see selftest)."""
    def __init__(self, name, text):
        self.name = name
        self.text = text

    @classmethod
    def from_path(cls, path):
        return cls(os.path.basename(path)[:-3], Path(path).read_text(encoding="utf-8"))

    @property
    def claims(self):
        """This eval's text with HTML comments removed — what a FIELD is read from.

        A comment carries provenance about a value, not the value (detector AC's rule,
        #417). Reading a field from the raw text made the guidance in TEMPLATE.md into
        the fields it describes: detector Q read `**Last triaged:**` out of the comment
        saying that field is optional, so every eval created the documented way — copy
        the template, fill it in — failed a gating detector, and the remedy the finding
        named would have stamped a triage pass that never happened (#451).

        PROVENANCE markers are read from `self.text`, not from here: `<!-- triaged:
        bulk -->`, `<!-- triaged: human -->` and the backfill marker are themselves
        comments, so stripping is a thing the caller does to one side of the comparison
        and never a mode the whole detector runs in."""
        return catalog_lib.strip_html_comments(self.text)

    @property
    def how(self):
        return how_section(self.text)

    @property
    def evidence(self):
        return Evidence(self.how)

    @property
    def evidence_level(self):
        """The declared **Evidence:** field value (issue #62), or None if absent.
        One of EVIDENCE_LEVELS — records how hard we looked, separate from the verdict."""
        m = EVIDENCE_FIELD.search(self.claims)
        return m.group(1) if m else None

    @property
    def derived_evidence(self):
        """Evidence level inferred from this eval's own signals (issue #67 backfill).
        backfill-evidence.py writes this into the declared field; afterwards the two agree."""
        return self.evidence.level

    @property
    def effective_evidence(self):
        """The declared **Evidence:** value if the eval carries one, else the
        derived level — what every evidence consumer should read (#201)."""
        return self.evidence_level or self.derived_evidence

    @property
    def catalog_rows(self):
        """The catalog-row copies embedded in this eval, via the shared parser (#196)."""
        return catalog_lib.parse_catalog_rows(self.text)

    @property
    def is_skill(self):
        return any(r.url and r.type == "skill" for r in self.catalog_rows)

    @property
    def type(self):
        """The Type cell from the eval's catalog row (tool/skill/MCP server/…), or None."""
        rows = self.catalog_rows
        return rows[0].type if rows else None

    # The `**Dev loop stage:**` header — the eval's own answer to *when do I use this*.
    # COMPARISON.md answers the same question by which `## Section` the row sits under,
    # and detector AG compares the two (#453). Read from `claims`, so the template's
    # commented example line can never be mistaken for a declaration (#451).
    _STAGE_HEADER = re.compile(r"^\*\*Dev loop stage:\*\*\s*([^\n|]+)", re.MULTILINE)

    @property
    def dev_loop_stage(self):
        """The declared **Dev loop stage:** header text, or None. Free prose by design —
        `named_stages()` is what extracts the loop stages it names."""
        m = self._STAGE_HEADER.search(self.claims)
        return m.group(1).strip() if m and m.group(1).strip() else None

    # The `**Layer:**` header — the OTHER coordinate of the same 2-D map. WORKFLOW.md
    # answers the same question twice more (a `| Layer |` column on every stage table,
    # and the `## Adopting This Workflow` ladder), and detector AI compares all three
    # (#475). Read from `claims` for #451's reason, exactly as the stage header is.
    _LAYER_HEADER = re.compile(r"^\*\*Layer:\*\*\s*([^\n|]+)", re.MULTILINE)

    @property
    def layer(self):
        """The declared **Layer:** header text, or None. Free prose by design —
        `named_layers()` is what extracts the layers it names."""
        m = self._LAYER_HEADER.search(self.claims)
        return m.group(1).strip() if m and m.group(1).strip() else None

    @property
    def last_verified(self):
        """The declared **Last verified:** date (issue #65) as a date, or None if absent/bad."""
        m = re.search(r"\*\*Last verified:\*\*\s*(\d{4}-\d{2}-\d{2})", self.claims)
        if not m:
            return None
        try:
            return datetime.date.fromisoformat(m.group(1))
        except ValueError:
            return None

    # The `**Repo:**` header link. Detector U compares it to the CATALOG row's link:
    # when a repo is renamed the catalog row gets repointed and this header does not,
    # so the eval keeps asserting a pre-rename slug forever (#336).
    _REPO_HEADER = re.compile(r"^\*\*Repo:\*\*.*$", re.MULTILINE)
    _MD_LINK = re.compile(r"\[[^\]]*\]\(([^)]*)\)")

    @property
    def repo_link(self):
        """The FIRST URL in this eval's `**Repo:**` header, or None (some evals head
        with `**Site:**` for a commercial platform)."""
        links = self.repo_links
        return links[0] if links else None

    @property
    def repo_links(self):
        """EVERY URL on the `**Repo:**` line. A header that documents a rename names
        both repos — `[old](…) — **now redirects to** [new](…)` — and that form is
        richer than the catalog's single link, not drift. Detector U accepts the header
        when the catalog's URL appears anywhere on the line."""
        m = self._REPO_HEADER.search(self.claims)
        return self._MD_LINK.findall(m.group(0)) if m else []

    # The `**License:**` header field. It shares a line with `**Stars:**` and
    # `**Last updated:**` — pipe-separated — so the value stops at the next `|`, and
    # the field is NOT anchored to the start of a line (#411).
    _LICENSE_HEADER = re.compile(r"\*\*License:\*\*\s*([^|\n]+)")

    @property
    def license_header(self):
        """The declared `**License:**` value as written, or None if the eval has no
        such field. Free text by convention — `MIT`, `Apache-2.0 (repo) / CC-BY (docs)`,
        `source-available (repo SPDX returns NOASSERTION)` — so detector AC compares
        license FAMILIES rather than strings.

        An HTML comment is stripped: it carries PROVENANCE about the value (when the
        license changed upstream, why the record disagrees), not the claim itself. The
        distinction is load-bearing because the honest way to record a correction is to
        quote what you corrected — detector Z's `LICENSE_WITHDRAWN` rule — and a comment
        reading "the header froze at the pre-detection NOASSERTION reading" would
        otherwise make an accurate `AGPL-3.0` header assert an absence (#417). Same
        convention as `**Last verified:**`'s backfill marker."""
        m = self._LICENSE_HEADER.search(self.claims)
        return m.group(1).strip() if m and m.group(1).strip() else None

    # The headline token, drawn from the ONE vocabulary in catalog_lib (#324). An eval
    # whose row is a `discovery-log` lead may headline `discovery-log` and say what it
    # is — a tentative read — instead of borrowing CONDITIONAL, a word ADR-0005 reserves
    # for tools we actually exercised. Longest-first alternation so a token that is a
    # prefix of another can never win the shorter match.
    _VERDICT_HEAD = re.compile(
        r"##\s*Verdict\s*\n+\s*\*\*(" +
        "|".join(re.escape(v) for v in sorted(catalog_lib.VERDICTS, key=len, reverse=True)) + ")")

    @property
    def verdict(self):
        m = self._VERDICT_HEAD.search(self.text)
        return m.group(1) if m else None

    @property
    def verdict_set(self):
        # every verdict word in the Verdict section (handles dual verdicts)
        if not self.verdict:
            return set()
        vsec = re.search(r"##\s*Verdict.*?(?=\n##\s|\Z)", self.text, re.DOTALL)
        if vsec:
            return {w for w in VERDICTS if re.search(rf"\b{w}\b", vsec.group(0))}
        return {self.verdict}

    @property
    def name_aliases(self):
        # normalized names this eval might be keyed by in COMPARISON.md
        cands = {catalog_lib.name_key(self.name)}
        h = re.search(r"^#\s*Evaluation:\s*(.+)$", self.text, re.MULTILINE)
        if h: cands.add(catalog_lib.name_key(h.group(1)))
        rows = self.catalog_rows
        if len(rows) == 1:
            # An eval's `## Catalog entry` mirror names the row it CLAIMS, link or no
            # link — #401's ruling that an unlinked entry is still a catalogued tool.
            # The old `startswith("https://github")` filter discarded exactly the cell
            # that says so, and TEMPLATE.md mirrors are written with a bare name: that
            # is why a bulk pass wrote `prisma.md` beside `prisma-mcp.md` and recorded
            # "no eval file existed before this pass" (#412, #433). It also decided
            # detector AD's two buckets by markdown formatting alone — `sentry-mcp`'s
            # mirror happens to carry a link, `prisma-mcp`'s does not.
            cands.add(catalog_lib.name_key(rows[0].name))
        else:
            # More than one mirror row means a COMPARISON DOCUMENT whose rows are
            # references, not claims (detector AD's rule) — `cost-observability` embeds
            # tokencost, Infracost and abtop. Claiming the first github-linked one is
            # arbitrary and pre-dates that rule; kept so this change loses no alias, and
            # flagged rather than fixed here since dropping it would leave `tokencost`
            # with no eval at all.
            ce = next((r for r in rows if r.url and r.url.startswith("https://github")), None)
            if ce: cands.add(catalog_lib.name_key(ce.name))
        return cands

# ---------------------------------------------------------------- detector context (#199)
class DetectorContext:
    """The detectors' input seam: everything a detector consumes, loaded once
    from one root directory. main() builds one from ROOT; tests build one from
    a fixture directory — the context replaces the ROOT monkeypatch as the test
    surface, so a detector's real inputs are visible in its signature.
    Properties are read lazily and cached — each cached input is read once per
    run, and detectors D, J, and M literally share one comparison_verdict_map
    (#197). (Detector A additionally walks raw file text via ctx.read: it scans
    every evaluations/*.md including the template ctx.evals skips.)"""
    def __init__(self, root):
        self.root = root

    def path(self, rel):
        return os.path.join(self.root, rel)

    def read(self, rel):
        return Path(self.path(rel)).read_text(encoding="utf-8")

    @functools.cached_property
    def catalog(self):
        return self.read("CATALOG.md")

    @functools.cached_property
    def comparison(self):
        return self.read("COMPARISON.md")

    @functools.cached_property
    def stack(self):
        return self.read("STACK.md")

    @functools.cached_property
    def workflow(self):
        return self.read("WORKFLOW.md")

    @functools.cached_property
    def ledger(self):
        return self.read("STACK-LEDGER.md")

    @functools.cached_property
    def evals(self):
        """Every Evaluation under evaluations/, skipping the template."""
        return [Evaluation.from_path(p)
                for p in sorted(glob.glob(os.path.join(self.root, "evaluations/*.md")))
                if os.path.basename(p) != "TEMPLATE.md"]

    @functools.cached_property
    def comparison_rows(self):
        """COMPARISON.md's verdict rows via the shared catalog_lib parser (#193)."""
        return catalog_lib.comparison_verdict_rows(self.comparison)

    @functools.cached_property
    def comparison_verdict_map(self):
        """The ONE COMPARISON name→verdict map detectors D, J, and M share (#197).
        Each row registers under catalog_lib.identity_keys — full and parenthetical-
        stripped name_key, never the slash-basename ('vercel-labs/agent-skills' must
        not shadow the real 'agent-skills' row). When a stripped alias collides
        across rows ('awesome-claude-skills (Composio)' vs '(travisvn)'), setdefault
        keeps the FIRST registration in file order for the ambiguous stripped key;
        each row's full key stays unambiguous, and consumers holding a qualified
        name always hit the full key first."""
        m = {}
        for r in self.comparison_rows:
            for k in catalog_lib.identity_keys(r.tool):
                m.setdefault(k, r.verdict)
        return m

    @functools.cached_property
    def eval_claims(self):
        """COMPARISON row key → the evals CLAIMING it (detector AD's rule, #412/#433).

        An eval claims the row its `## Catalog entry` mirror names — link or no link,
        #401's ruling that an unlinked entry is still a catalogued tool — or the row its
        own aliases resolve to. Two precision rules, both read off the corpus:

        * An eval embedding more than one mirror row is a COMPARISON document and its
          rows are references, not claims (`cost-observability` embeds tokencost,
          Infracost and abtop).
        * Resolution is EXACT catalog name first — verify-installs.py's rule.
          `agent-skills` and `agentskills` collapse to one name_key (detector U's AMBIG
          example) but are two distinct rows, and a key-only match would resolve one to
          the other. A key two rows answer to identifies neither, so it resolves to
          nothing rather than to a coin flip.

        Built once here because AD asks "which rows have more than one eval" and AG
        (#453) asks "which eval does this row's stage claim belong to" — the same
        question, and a second implementation of it would drift."""
        exact = {}
        for line in self.comparison.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) > 1 and catalog_lib.name_key(cells[0]) in self.comparison_verdict_map:
                exact.setdefault(cells[0].lower(), catalog_lib.name_key(cells[0]))
        seen = collections.Counter(exact.values())
        ambiguous = {k for k, n in seen.items() if n > 1}

        claims = collections.defaultdict(list)
        for ev in self.evals:
            keys = set()
            mirrors = ev.catalog_rows
            if len(mirrors) == 1:
                k = exact.get(mirrors[0].name.lower())
                if k and k not in ambiguous:
                    keys.add(k)
            keys |= {a for a in ev.name_aliases
                     if a in self.comparison_verdict_map and a not in ambiguous}
            for k in keys:
                claims[k].append(ev)
        return claims

    @functools.cached_property
    def eval_by_row(self):
        """COMPARISON row key → its ONE claiming eval. A row claimed by several resolves
        to nothing: which of them speaks for the row is detector AD's open question, and
        answering it with a coin flip here would put a stranger's header on the row."""
        return {k: v[0] for k, v in self.eval_claims.items() if len(v) == 1}

    @functools.cached_property
    def evidence_alias_map(self):
        """alias name_key → effective Evidence level, first registration wins —
        the map catalog_lib.evidence_lookup consumes (#201). Built once here so
        detector N, backfill-evidence, and tier-stack all read the same map
        instead of each rebuilding it from the evals."""
        amap = {}
        for ev in self.evals:
            for a in ev.name_aliases:
                amap.setdefault(a, ev.effective_evidence)
        return amap

def audit_evidence_field(ctx):
    """REPORT-ONLY: tally the declared **Evidence:** field across evals (issue #62),
    catalog-wide and within the ADOPT/KEEP set (issue #67 — "what % of ADOPT is
    MEASURED"). Returns (counts, missing, strong) where counts/strong are level->int
    over all evals / over ADOPT+KEEP evals, and missing lists evals with no field.
    Records how hard we looked, separate from the verdict; gating weak backing is #71."""
    counts = dict.fromkeys(EVIDENCE_LEVELS, 0)
    strong = dict.fromkeys(EVIDENCE_LEVELS, 0)  # restricted to ADOPT/KEEP-verdict evals
    missing = []
    for ev in ctx.evals:
        lvl = ev.evidence_level
        if lvl:
            counts[lvl] += 1
            if ev.verdict in ("ADOPT", "KEEP"):  # primary verdict, not every word mentioned
                strong[lvl] += 1
        else:
            missing.append(ev.name)
    return counts, missing, strong

def audit_skill_evidence(ctx):
    measured, backlog = [], []
    for ev in ctx.evals:
        if not ev.is_skill:
            continue  # not a skill-type entry
        if ev.verdict != "ADOPT":
            continue  # only ADOPT skills carry the "needs measured backing" bar
        # genuinely measured = has measurement evidence AND is not a disclosed not-run
        # review (which may merely quote the author's "with-skill" numbers).
        (measured if ev.evidence.is_measured else backlog).append(ev.name)
    return measured, backlog

# ---------------------------------------------------------------- S. skill test-design (report-only)
# TEMPLATE.md's "Test design — skills" section requires every skill/plugin-Type eval to
# record BOTH skill dimensions (issue #38): Triggering (does the description fire on the
# right prompts?) and an Output A/B (with-skill vs baseline). This report surfaces
# skill/plugin evals that record NEITHER — the structural gap the required section
# closes. Conservative by design (same lenient-vocab spirit as detector B's HONEST
# regex): an eval counts as compliant if it names a triggering test OR an A/B anywhere,
# so an honest measured eval is never false-flagged. Widen the vocab if it does; never
# tighten it into a gate here — this mirrors --skills as a tracked metric, not a gate.
_SKILL_TRIGGER_RE = re.compile(r"trigger|run_eval|should[- ]?fire", re.IGNORECASE)
_SKILL_AB_RE = re.compile(r"\bA/B\b|with[- ]skill|without[- ]skill|baseline|skill on vs", re.IGNORECASE)

def audit_skill_design(ctx):
    """Detector S (REPORT-ONLY): skill/plugin-Type evals that record NEITHER a triggering
    test nor an A/B, per TEMPLATE.md's required skills Test-design section (#38). Returns
    (compliant, missing) as lists of eval names. Never affects the exit code."""
    compliant, missing = [], []
    for ev in ctx.evals:
        if ev.type not in ("skill", "plugin"):
            continue  # only skill/plugin-Type evals carry the two-dimension bar
        has = bool(_SKILL_TRIGGER_RE.search(ev.text) or _SKILL_AB_RE.search(ev.text))
        (compliant if has else missing).append(ev.name)
    return compliant, missing

# ---------------------------------------------------------------- F. dangling overlaps (report-only)
# Each entry's "Overlaps with" cell names peer tools. A token naming a tool that
# ISN'T itself catalogued is either a deliberate external/conceptual peer (the
# format allows this — e.g. "e2b (ext.)") or a real gap: a notable tool we forgot
# to add. This is exactly how aider, continue, and agenta were found. The more
# rows reference the same uncatalogued token, the likelier it is a real gap.
# Report-only — surfaces candidates for human review; does not affect exit code.
#
# `(ext.)` used to be a silencer F obeyed and never checked (#403) — and a marker
# is only true on the day it is written. F found `aider`, `aider` was catalogued
# as a ★46K harness, and the three rows pointing at it kept saying it was outside;
# this comment held one of them up as the example of a healthy row. Six markers
# named a catalogued tool. So the marker is now VERIFIED against the one record
# that answers it: CATALOG.md, already parsed on this same pass.
#
# _ovl_display is presentation + heuristics (word counts, report text), NOT a
# same-tool key — matching goes through catalog_lib.name_key (#197).
_ovl_display = lambda s: catalog_lib.strip_parenthetical(s).strip().lower()
_OVL_SKIP = ("complementary", "different", "approach", "same repo",
             "conceptual", "none", "—", "–")
_OVL_PAREN = re.compile(r"\(([^()]*)\)")
# How a DEMONSTRATED peer is described in the report. Each kind is printed with its
# source and never counted — the token resolves to a record, so it is not a lead.
_OVL_PEER_LABEL = {
    "installed": "the legend's allowed case — installed from",
    "contained": "the row discloses its container — catalogued as",
    "repo": "a skill this repo ships at",
}


def _repo_skill_sources(root):
    """name_key(skill dir) -> "skills/<dir>/" for every skill THIS repo ships.

    The strongest record F can consult and the only one that is not a property of
    one laptop: in-tree, versioned, offline, readable in CI. `skills/evaluate-tool/`
    is a real conceptual peer of a skill-evaluation tool and can never be a catalog
    row, so without this it is a permanent resident of the counted bucket."""
    out = {}
    with contextlib.suppress(OSError):
        for d in sorted(os.listdir(os.path.join(root, "skills"))):
            if os.path.isdir(os.path.join(root, "skills", d)):
                out[catalog_lib.name_key(d)] = f"skills/{d}/"
    return out


def audit_overlaps(ctx, home=None):
    """(gaps, stale_ext, peers, records) — "Overlaps with" tokens that don't resolve to a
    catalog row, split by which record answers them.

    CATALOG.md's own legend says a token may name "a notable external tool **or installed
    skill**", so "it's an installed skill" is the sanctioned reason a token doesn't
    resolve. Nothing checked it: every dangling token got the same hand-off sentence,
    even though detector Y (#366) already reads the records that answer it — the same
    unchecked install assertion ADR-0006 removed from `KEEP`.

    `(ext.)` was the same shape (#403). F skipped any token carrying it, so a row could
    assert a tool was outside the catalog and never be contradicted once it was added —
    which is what happened to `aider`: F found it, `9be01ee` catalogued it, and the three
    rows that raised the flag still called it external. **The marker is now verified**
    against CATALOG.md, and a `stale_ext` entry (token, catalogued as, citing row) is
    COUNTED — it is a defect in the row, not a peer awaiting review.

    Verification keys on `identity_keys`, never `alias_keys` (#374): an alias-keyed run
    "resolves" `MCP (ext.)` to **mdn/mcp** by slash-basename, and between two rows that
    each name a tool a basename is not a synonym. `aider-style` is the mirror case — a
    descriptor rather than a name, so no key resolves it and only a human can repoint it.

    A `peer` is a token DEMONSTRATED to resolve to a record, so it is printed with its
    source and not counted (V's `acked`, W's `cleared`, X's `FACETED`, Y's `SHADOWED`).
    Three kinds, asked strongest-record-first — the catalog's own declaration and the
    repo's own tree are facts about the artifact, an install record is a fact about one
    laptop (ADR-0006's split):

      contained  the token's own parenthetical names a catalogued row — the `Ships
                 inside` idea (#343) done informally, in the one column with no such
                 column. The container is PRINTED because the parenthetical is prose:
                 it discloses where the peer lives, it does not prove the peer isn't
                 also a gap, so a human still reads the line.
      repo       the token names a skill this repo ships under `skills/`.
      installed  this machine's records answer to it (#398).

    Local-only, like Y: `--overlaps` is opt-in and report-only, and with no records
    readable this reports exactly as it did before — **0 records, never 0 findings**, so
    an unreadable lockfile can never present as "nothing is installed"."""
    names, ident, rows = set(), {}, []
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        names.update(catalog_lib.alias_keys(r.name))
        for k in catalog_lib.identity_keys(r.name):
            ident.setdefault(k, r.name)  # identity only — a basename is not a synonym
        if r.url is not None:
            rows.append(r)  # unlinked entries ("| OMEGA | ...") name-match only
    by_name, _slugs, on_disk, _fetched = read_install_records(home)
    # name_key on both sides: these are display names on the catalog side and directory
    # / lockfile names on the machine side, and only the key form compares them.
    installed = {catalog_lib.name_key(n): by_name.get(n, "on disk")
                 for n in list(on_disk) + list(by_name)}
    installed.pop("", None)
    shipped = _repo_skill_sources(ctx.root)
    from collections import Counter
    miss, stale, peers = Counter(), [], {}
    for r in rows:
        if r.overlaps is None:
            continue
        for tok in r.overlaps.split(","):  # the "Overlaps with" cell
            t = _ovl_display(tok)
            tl = tok.lower()
            balanced = tok.count("(") == tok.count(")")  # else a mid-parenthetical fragment
            if "ext." in tl:
                # Verify the marker rather than obey it. A prose fragment simply misses:
                # identity_keys is exact-name matching, so nothing has to be filtered out.
                hit = next((ident[k] for k in catalog_lib.identity_keys(t)
                            if k in ident), None) if (t and balanced) else None
                if hit:
                    stale.append((t, hit, r.name))
                continue
            if (not t or "=" in tok or ";" in tok or not balanced
                    or len(t) > 22 or len(t.split()) > 2
                    or any(x in tl for x in _OVL_SKIP)):
                continue  # conceptual peer or prose fragment, not a gap
            if any(k in names for k in catalog_lib.alias_keys(tok)):
                continue
            container = next((ident[k] for p in _OVL_PAREN.findall(tok)
                              for k in catalog_lib.identity_keys(p.strip())
                              if k in ident), None)
            key = catalog_lib.name_key(catalog_lib.strip_parenthetical(tok))
            if container:
                peers[t] = ("contained", container)
            elif key in shipped:
                peers[t] = ("repo", shipped[key])
            elif key in installed:
                peers[t] = ("installed", installed[key])
            else:
                miss[t] += 1
    return miss.most_common(), sorted(stale), sorted(peers.items()), len(installed)


def overlap_pressure_map(ctx):
    """name_key(cited tool) -> set of DISTINCT catalog rows (by their name_key)
    that cite it in 'Overlaps with'. Shares audit_overlaps' tokenization and skip
    filters — the only difference is it counts EVERY cited token, not just the
    uncatalogued ones detector F reports — so next-evals.py can weigh a
    discovery-log candidate by how many peers point at it (#plan-005). A caller
    unions the sets across a candidate's IDENTITY keys — never alias_keys, whose
    slash-basename would let `vercel-labs/agent-skills` collect the citations of
    `addyosmani/agent-skills` (#413, the score half of #374). Self-citations are
    dropped."""
    cites = {}
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if r.overlaps is None:
            continue
        citer = catalog_lib.name_key(r.name)
        for tok in r.overlaps.split(","):
            t, tl = _ovl_display(tok), tok.lower()
            if (not t or "ext." in tl or "=" in tok or ";" in tok
                    or tok.count("(") != tok.count(")")
                    or len(t) > 22 or len(t.split()) > 2
                    or any(x in tl for x in _OVL_SKIP)):
                continue
            key = catalog_lib.name_key(catalog_lib.strip_parenthetical(tok))
            if key and key != citer:
                cites.setdefault(key, set()).add(citer)
    return cites

# ---------------------------------------------------------------- P. WORKFLOW↔STACK drift (report-only)
# README sends readers to WORKFLOW.md as "the full operating manual" and STACK.md is
# the install list; they must not give a newcomer two different answers to "what do I
# use for X". The invariant is ONE-directional: every STACK *pick* must appear
# somewhere in WORKFLOW.md (the manual must at least mention every pick). The reverse
# is NOT required — WORKFLOW legitimately lists non-STACK CONDITIONAL options.
# Matched by github owner/repo slug, NOT display name (names vary — "GSD" links to
# obra/superpowers), reusing catalog_lib.github_repos so the extraction can't drift.
# STACK picks are scoped to the install-command *table rows*, so the prose that names
# *excluded* tools (the "excluded (#37)" batch: brooks-lint, code-on-incus) and self/
# issue links aren't mistaken for picks. Slugs are lowercased (GitHub is case-
# insensitive: STACK links NVIDIA/SkillSpector but clones NVIDIA/skillspector).
# Report-only, not a gate — prints a count so it's "a number to shrink" (plan 003).
def audit_workflow_drift(ctx):
    """Detector P: ([(slug, stack_line)], picks) — STACK picks absent from WORKFLOW.md.

    `picks` is the POPULATION, and it is returned because the headline used to print only
    the findings while CLAUDE.md described P as *"prints a count so it's a number to
    shrink"* — the same confusion #467 fixed in detector U, where `0 … across 0` read
    identically to *nothing was checked*.

    A pick is `catalog_lib.stack_picks`' definition and no longer this function's own
    (#469). Reading any github link on any `|`-line counted `graphify`, out of a row
    whose third cell reads *"graphify is not in STACK — evaluations/ only"*, so P was one
    WORKFLOW.md edit away from demanding the manual document a tool STACK disclaims —
    flagging a healthy row, which detector V's rule calls the expensive direction."""
    wf = {s.lower() for s in catalog_lib.github_repos(ctx.workflow)}
    lines = ctx.stack.splitlines()
    first_line = {}
    for pick in catalog_lib.stack_picks(ctx.stack):
        # `stack_picks` is order-preserving but not line-numbered; the first line whose
        # text contains this pick's URL is the row to point a human at.
        if pick.slug not in first_line:
            first_line[pick.slug] = next(
                (i for i, ln in enumerate(lines, 1) if pick.url in ln), 0)
    missing = [(slug, ln) for slug, ln in sorted(first_line.items()) if slug not in wf]
    return missing, len(first_line)

# ---------------------------------------------------------------- M. clusters without a pick (report-only)
# ADR 0001 / #69: when several catalogued tools solve the same problem (an overlap
# cluster), the catalog should name ONE best-in-class ADOPT pick rather than hedge
# CONDITIONAL on all of them. This report surfaces overlap clusters (connected via
# the "Overlaps with" graph) where NO member is ADOPT/KEEP yet at least one is
# CONDITIONAL — i.e. clusters still awaiting a pick. Report-only; it makes the #69
# migration findable, it does not migrate anything.
def audit_clusters(ctx):
    # name_key -> set(overlap peer keys), restricted to catalogued names; disp
    # keeps the human-readable member name the report prints (#197).
    rows = [r for r in catalog_lib.parse_catalog_rows(ctx.catalog) if r.url is not None]
    cat_names, edges, disp, nverd = set(), {}, {}, {}
    verd = ctx.comparison_verdict_map
    for r in rows:
        nm = catalog_lib.name_key(r.name)
        cat_names.add(nm)
        disp.setdefault(nm, _ovl_display(r.name))
        nverd[nm] = next((verd[k] for k in catalog_lib.identity_keys(r.name) if k in verd), None)
    for r in rows:  # second pass: peer tokens resolve against the full name set
        nm = catalog_lib.name_key(r.name)
        peers = []
        if r.overlaps:
            for tok in r.overlaps.split(","):
                t = _ovl_display(tok)
                if t and "ext." not in tok.lower() and len(t.split()) <= 2:
                    p = next((k for k in catalog_lib.alias_keys(tok) if k in cat_names), None)
                    if p: peers.append(p)
        edges[nm] = peers
    # union-find over overlap edges (only between catalogued names)
    parent = {n: n for n in cat_names}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        if a in parent and b in parent:
            parent[find(a)] = find(b)
    for nm, peers in edges.items():
        for p in peers:
            union(nm, p)
    from collections import defaultdict
    clusters = defaultdict(set)
    for n in cat_names:
        clusters[find(n)].add(n)
    flagged = []
    for members in clusters.values():
        if len(members) < 2:
            continue
        verds = {nverd.get(m) for m in members}
        has_pick = "ADOPT" in verds or "KEEP" in verds
        awaiting = "CONDITIONAL" in verds or "discovery-log" in verds
        if awaiting and not has_pick:
            flagged.append(sorted(disp[m] for m in members))
    return sorted(flagged, key=lambda c: (-len(c), c[0].lower()))

# ---------------------------------------------------------------- N. token-savings claims (report-only)
# Nearly every Optimize-cluster entry advertises a self-reported "% token savings"
# headline (60-95% fewer tokens, 96% reduction, 50x token reduction, ~98% fewer
# tokens) yet almost none are hands-on MEASURED in this repo — the loudest claims in
# the catalog rest on the weakest evidence. This report flags every CATALOG row whose
# one-liner makes a numeric token-savings claim but whose eval is not run-backed
# (Evidence MEASURED/RUN), so the unverified backlog is a number to watch shrink
# (mirrors --skills; gating is a later #71-style decision). An in-row "self-reported"/
# "unverified" disclaimer is the honest path — like detector B's HONEST vocab — and is
# bucketed apart from the silent claims. Report-only; does not affect exit code.
_SAVINGS_NUM = re.compile(r"~?\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*%\+?|~?\d+(?:\.\d+)?\s*(?:×|x\b)")
_SAVINGS_NEAR = re.compile(r"token|context|prompt|saving|reduc|fewer|less|waste|compress|consumption|lower|smaller|\bcut", re.IGNORECASE)
_SAVINGS_CTX = re.compile(r"token|context|prompt", re.IGNORECASE)
_SAVINGS_DISCLAIMER = re.compile(r"self-?reported|unverified", re.IGNORECASE)

def _has_savings_claim(one_liner):
    """A numeric token-savings headline: a percentage or N× figure sitting next to
    reduction/token vocabulary, in a one-liner that is itself about tokens/context.
    Scopes to the Optimize cluster without computing cluster membership, and avoids
    false positives like '94% of languages' or '2M-token context' (figure, no verb)."""
    if not _SAVINGS_CTX.search(one_liner):
        return False
    for m in _SAVINGS_NUM.finditer(one_liner):
        lo, hi = max(0, m.start() - 28), m.end() + 28
        if _SAVINGS_NEAR.search(one_liner[lo:hi]):
            return True
    return False

def audit_savings_claims(ctx):
    """Return (name, evidence_level, disclosed) for every CATALOG row making a numeric
    token-savings claim that is NOT run-backed. Verified rows (MEASURED/RUN) drop out;
    rows with no eval surface as '(no eval)'. Sorted by name. Report-only."""
    levels = ctx.evidence_alias_map  # normalized catalog name -> effective evidence level
    flagged = []
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if r.url is None or r.one_liner is None or not _has_savings_claim(r.one_liner):
            continue
        # NOT catalog_lib.evidence_lookup: N distinguishes "(no eval)" (None) from an
        # eval-derived SOURCE-ONLY, which the lookup's SOURCE-ONLY default would erase.
        lvl = next((levels[k] for k in catalog_lib.alias_keys(r.name) if k in levels), None)
        if lvl in ("MEASURED", "RUN"):
            continue  # claim is run-backed — exactly what we want
        disclosed = any(_SAVINGS_DISCLAIMER.search(c) for c in r.cells)
        flagged.append((r.name, lvl or "(no eval)", disclosed))
    return sorted(flagged, key=lambda r: r[0].lower())

# ---------------------------------------------------------------- G. comparison consistency
# COMPARISON.md mirrors CATALOG.md: its per-stage Summary must be an honest funnel.
# Tools must sum to its own body rows and equal the CATALOG entry count; Validated
# must equal the real-verdict rows (discovery-log excluded, per ADR 0001) — not the
# raw catalogued count. Manual edits drift easily (a single tool addition touches both
# files) and nothing else cross-checks them, so a disagreement could ship silently.
# Gating, offline.
def _summary_cells(line):
    """Cells of a Summary table row, outer pipes dropped and bold markers stripped."""
    return [c.strip().replace("**", "") for c in line.strip().strip("|").split("|")]

# ---------------------------------------------------------------- Q. eliminate-only bulk triage
# An unattended bulk-triage pass (triage.py's bands) may REJECT a lead but never
# promote one: it writes SKIP, or leaves the lead at discovery-log. A false SKIP is
# cheap and reversible; a false ADOPT poisons STACK, and detector K's honesty-
# disclaimer escape hatch would happily let a README skim carry an ADOPT.
#
# Policy is worthless unattended unless it is mechanical. An eval touched by the bulk
# lane carries BULK_MARKER; this gate fails if such an eval claims anything stronger
# than SKIP. Gating, offline. A human who genuinely exercises the tool drops the
# marker (and says so in "How we tested it") before writing a stronger verdict.
BULK_MARKER = "<!-- triaged: bulk -->"
# SKIP is the disposal; `discovery-log` is the leave. The latter used to be expressible
# only as the ABSENCE of a headline, because a left lead borrowed CONDITIONAL and this
# gate would have failed the build for prose the lane never wrote. Since #324 a lead
# headlines `discovery-log`, so the leave outcome is a token the gate can recognize.
BULK_ALLOWED = frozenset({"SKIP", "discovery-log"})
# A `**Last triaged:**` stamp says *some* lane examined this lead — but not which, and Q
# can only police a lane it can identify. The bulk marker is that identification; a human
# pass writes HUMAN_MARKER instead, which exempts the eval (a human may reach any verdict,
# which is the whole difference between the lanes). A stamp carrying NEITHER is the hole
# #327 names: it looks exactly like a lane that behaved, and Q never sees it. The
# /triage-lead skill has written the bulk marker on both outcomes since #323; this makes
# that protocol mechanical instead of a promise.
TRIAGE_STAMP = "**Last triaged:**"
HUMAN_MARKER = "<!-- triaged: human -->"
UNATTRIBUTED = "unattributed"  # the second finding kind audit_bulk_triage returns

BulkCoverage = collections.namedtuple("BulkCoverage", "bulk human stamped")


def bulk_triage_coverage(ctx):
    """Q's population is the STAMPED evals (#481). One with no `**Last triaged:**` was
    never triaged, so there is no lane to police — that is scope, not an abstention.
    `human` is the exemption a human pass earns (reaching a real verdict is what it is
    for), and it is disclosed rather than folded into the pass, because an exemption
    silently included in `OK` is indistinguishable from a check that ran.

    The stamp is read from `claims` and the markers from `text`, mirroring the gate
    itself — the markers ARE comments (#451), so stripping them here would make the two
    disagree about which evals are marked."""
    stamped = [ev for ev in ctx.evals if TRIAGE_STAMP in ev.claims]
    bulk = [ev for ev in ctx.evals if BULK_MARKER in ev.text]
    human = [ev for ev in ctx.evals
             if HUMAN_MARKER in ev.text and BULK_MARKER not in ev.text]
    return BulkCoverage(len(bulk), len(human), len(stamped))


def audit_bulk_triage(ctx):
    """(eval name, verdict) for every bulk-marked eval whose verdict exceeds the
    eliminate-only authority. A marked eval with no verdict is fine — it stayed at
    discovery-log, which is the other permitted outcome.

    Keys on the HEADLINE verdict, not verdict_set: the latter collects every verdict
    word in the section, so a SKIP whose prose reads "not an ADOPT" would trip a
    set-based check. The headline is what COMPARISON.md and detector D consume."""
    flagged = []
    for ev in ctx.evals:
        if BULK_MARKER not in ev.text:
            # An unattributed stamp is unpoliceable, not innocent: Q cannot tell a lane
            # that left a lead from one that raised it (#327). Reported at the stamp, so
            # the fix is attribution rather than a verdict argument.
            # The stamp is read from `claims` and the markers from `text`, because the
            # markers ARE comments (#451). Testing the stamp against the raw text made
            # TEMPLATE.md's guidance comment a stamp on every copy of it.
            if TRIAGE_STAMP in ev.claims and HUMAN_MARKER not in ev.text:
                flagged.append((ev.name, UNATTRIBUTED))
            continue
        if ev.verdict and ev.verdict not in BULK_ALLOWED:
            flagged.append((ev.name, ev.verdict))
    return flagged

# ---------------------------------------------------------------- T. lead headline overreach
# A COMPARISON row reading `discovery-log` says the tool was never exercised — its eval
# is notes, not a recommendation. 324 such evals nonetheless opened `## Verdict` with
# **CONDITIONAL**, a word ADR-0005 grants only to a tool we ran or one carrying a real
# `adopt-if:` gate (#324). That is not cosmetic: the /triage-lead protocol escalates any
# lead whose headline reads CONDITIONAL, so the mislabel shielded 11 of 13 leads in one
# band and nearly made the pass a no-op. #324 relabelled them; this keeps them relabelled.
#
# Scoped to REVIEW/SOURCE-ONLY evidence deliberately. A run-backed eval that headlines
# CONDITIONAL has earned the word — there the *row* is what's stale, which is a verdict
# decision for a human, not a headline this detector can call wrong.
LEAD_ALLOWED_HEADLINES = frozenset({"discovery-log", "SKIP"})  # "it's a lead" / "we rejected it"

def audit_lead_headlines(ctx):
    """(eval name, headline verdict, evidence level) for every `discovery-log` row whose
    unexercised eval headlines a verdict word it is not entitled to. Report-only: the
    survivors are escalations awaiting a human verdict (#259), not build breakers."""
    comp = ctx.comparison_verdict_map
    flagged = []
    for ev in ctx.evals:
        if not ev.verdict or ev.verdict in LEAD_ALLOWED_HEADLINES:
            continue
        cv = next((comp[c] for c in ev.name_aliases if c in comp), None)
        if cv != "discovery-log":
            continue
        level = ev.effective_evidence
        if level in ("MEASURED", "RUN"):
            continue  # earned the word; the row is the stale half — a human call
        flagged.append((ev.name, ev.verdict, level))
    return flagged


# ---------------------------------------------------------------- U. catalog-entry mirror drift (report-only)
# TEMPLATE.md has every eval close with a `## Catalog entry` section holding that tool's
# CATALOG.md row. It is a mirror — a fact restated in two places with no generator and no
# test — so it drifts, and 62% of it had (#345). This is the same class root CLAUDE.md
# calls out for plugin/README.md: *gate the shared facts, not the file*.
#
# Two kinds, reported apart because they are not equally dangerous:
#
#   LINK  — the eval points at a different repo than the catalog does (#336). When a repo
#           is renamed the daily discovery pass repoints the CATALOG row and nothing
#           repoints the eval, so the eval asserts a dead slug (and the stars/license it
#           was written against) indefinitely. `herdr` was SKIP-eligible on stale facts
#           for exactly this reason. This is the class worth gating first.
#   TEXT  — the one-liner / problem / overlaps cells disagree. Cosmetic-looking, but the
#           overlaps cell is what `triage.py` bands leads from, so a disagreement here
#           decides which band a lead lands in (`softaworks/agent-toolkit`, #344).
#
# Report-only, and deliberately NOT a bulk fixer: #345's sequencing note is that whichever
# direction is applied wholesale destroys real work in the other, because the eval side is
# sometimes the better text (`azure-skills`). This prints the number to shrink; a human
# decides per row which side is right.
CatalogMirrorFinding = collections.namedtuple("CatalogMirrorFinding", "eval_name tool kind detail")

# How many evals U actually walked, and why the rest were not (#467). The headline used
# to print `len({f.eval_name for f in drift})` — the evals it FOUND something in — where
# every other detector here prints `n/total`. That is a second cardinality of the
# numerator, and it made "0 disagreement(s) across 0 eval(s)" on a clean tree read
# identically to "0 evals were checked": #319's *silence is not success*, and the reason
# detector C reports `n/total target(s) checked` at all. `walked` is the population;
# `skipped` is printed and NEVER counted (V's `acked`, W's `cleared`, X's `FACETED`),
# because some evals correctly have no mirror and turning 88 of them into a backlog would
# put a number on the board for a question nobody has asked.
MirrorCoverage = collections.namedtuple(
    "MirrorCoverage", "walked skipped headers header_total")

_MIRROR_SECTION = re.compile(r"^##\s*Catalog entry\b[^\n]*", re.MULTILINE)
_MIRROR_NA = re.compile(r"\bn/?a\b", re.IGNORECASE)

SKIP_NA = "declares `## Catalog entry: n/a` with a reason (the documented way to have none)"
SKIP_NO_ROW = "`## Catalog entry` section holds no parseable row (a comparison document)"
SKIP_NO_SECTION_CATALOGUED = "no `## Catalog entry` section — and the tool HAS a CATALOG.md row"
SKIP_NO_SECTION = "no `## Catalog entry` section, and no CATALOG.md row either"


def _mirror_skip_reason(ev, lookup):
    """Why this eval never reached the comparison. Whether a missing mirror is a defect
    is a human's call — `cost-audit-compress-recipe` is a recipe that correctly has none
    — so the split names the one bucket where it probably is: a tool the catalog lists."""
    section = _MIRROR_SECTION.search(ev.text)
    if section:
        return SKIP_NA if _MIRROR_NA.search(section.group(0)) else SKIP_NO_ROW
    row, _ambig = lookup(ev.name)
    return SKIP_NO_SECTION_CATALOGUED if row else SKIP_NO_SECTION


def _header_finding(ev, crow, tool):
    """(finding-or-None, was-compared) for an eval's `**Repo:**` header against `crow`.

    Two abstentions, neither a finding. An eval with **no header** asserts no repo —
    commercial platforms head with `**Site:**` — and an **unlinked** catalog row has no
    URL to compare, which is #401's rule (an entry with no repo to link is still a
    catalogued tool; only its URL comparison is skipped)."""
    heads = ev.repo_links
    if not heads or crow is None or not crow.url:
        return None, False
    if crow.url in heads:
        return None, True
    return CatalogMirrorFinding(
        ev.name, tool, _link_kind(heads[0], crow.url),
        f"**Repo:** header {heads[0]} != catalog {crow.url}"), True


def audit_catalog_mirror(ctx):
    """CatalogMirrorFindings for every eval whose embedded `## Catalog entry` row (or
    `**Repo:**` header) disagrees with CATALOG.md's row for the same tool. Offline —
    a string comparison between two files already in the tree, unlike detector C's
    ~450 HTTP requests, which is what makes it cheap enough to run every time."""
    # Two maps, because one is not enough. name_key collapses non-alphanumerics, so
    # `agent-skills` (addyosmani) and `agentskills` (the spec) key identically — and a
    # single setdefault map silently handed one eval the OTHER tool's row and reported a
    # LINK against it. Exact name wins; the collapsed key is a fallback, and a fallback
    # key reaching two different rows resolves to nothing rather than to a coin flip.
    # UNLINKED rows are indexed too (#401). An entry with no repo to link — `server-github`,
    # "DEPRECATED, archived — superseded by github-mcp-server" — is still a catalogued
    # tool; excluding it from IDENTITY resolution made its own eval's mirror a false
    # ORPHAN. Detector F already draws this line and says so: unlinked entries name-match
    # only. Skipping the URL comparison for such a row is right (there is no URL to
    # compare); skipping the row is not, and flagging a healthy row costs more than
    # missing a sick one.
    exact, fuzzy, ambiguous = {}, {}, set()
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        exact.setdefault(r.name, r)
        for k in catalog_lib.identity_keys(r.name):
            if k in fuzzy and fuzzy[k].name != r.name:
                ambiguous.add(k)
            fuzzy.setdefault(k, r)

    def lookup(name):
        """(row, ambiguous_key) for a name — never a guess between two distinct tools."""
        if name in exact:
            return exact[name], None
        for k in catalog_lib.identity_keys(name):
            if k in ambiguous:
                return None, k
            if k in fuzzy:
                return fuzzy[k], None
        return None, None

    findings, walked, skipped = [], 0, collections.Counter()
    headers = header_total = 0
    for ev in ctx.evals:
        header_total += bool(ev.repo_links)
        # An UNLINKED embedded row is indexed too, and only its URL comparison is skipped
        # (#467). This filter used to read `if r.url is not None`, the exact mirror of the
        # one #401 removed on the CATALOG side for the same reason: a row with no repo to
        # link still names a tool, its other cells are still a mirror, and only the URL
        # has nothing to compare against. #401 fixed one half of a symmetric filter.
        rows = ev.catalog_rows
        if not rows:
            skipped[_mirror_skip_reason(ev, lookup)] += 1
            # The CELLS need a mirror; the `**Repo:**` header needs only a header. The
            # header check used to sit inside this loop's other branch, so it inherited
            # the MIRROR's population and ran on 580 of the 677 evals that assert a repo
            # (#479) — #467's lesson (a check reporting the population it walked) one
            # clause over, and #401's (one half of a symmetric filter fixed, the other
            # never looked at) one file over. Resolution is `lookup(ev.name)`, the SAME
            # call that just chose this eval's skip bucket, so the bucket and the
            # comparison cannot disagree about which row the eval is about.
            crow, _ = lookup(ev.name)
            finding, ran = _header_finding(ev, crow, ev.name)
            headers += ran
            if finding:
                findings.append(finding)
            continue
        walked += 1
        # A pack eval embeds several rows (8090-software-factory carries the platform's);
        # every one of them mirrors some catalog row, so check each against its own.
        for row in rows:
            crow, ambig = lookup(row.name)
            if ambig:
                findings.append(CatalogMirrorFinding(
                    ev.name, row.name, "AMBIG",
                    f"two CATALOG.md rows collapse to the key '{ambig}' — cannot tell which is mirrored"))
                continue
            if crow is None:
                findings.append(CatalogMirrorFinding(
                    ev.name, row.name, "ORPHAN",
                    "embedded row names a tool with no CATALOG.md row"))
                continue
            # An UNLINKED row on EITHER side is not a disagreement: there is no URL on
            # that side to compare against (#401 for the catalog side, #467 for the eval's).
            if row.url is not None and crow.url is not None and row.url != crow.url:
                findings.append(CatalogMirrorFinding(
                    ev.name, row.name, _link_kind(row.url, crow.url),
                    f"eval row {row.url} != catalog {crow.url}"))
            for field in ("type", "one_liner", "overlaps"):
                mine, theirs = getattr(row, field), getattr(crow, field)
                if mine != theirs:
                    findings.append(CatalogMirrorFinding(
                        ev.name, row.name, "TEXT", f"{field}: {_clip(mine)} != {_clip(theirs)}"))
        # The header link is checked against the FIRST embedded row's catalog match: that
        # row is the eval's own subject (pack evals lead with theirs).
        crow, _ = lookup(rows[0].name)
        finding, ran = _header_finding(ev, crow, rows[0].name)
        headers += ran
        if finding:
            findings.append(finding)
    return findings, MirrorCoverage(walked, skipped, headers, header_total)


def _link_kind(a, b):
    """LINK for a genuine repo disagreement, CASE when the two URLs differ only in
    capitalization. GitHub owner/repo names are case-insensitive and redirect, so a
    case-only diff cannot make an eval assert the wrong repo's facts — the failure
    #336 is about. Reported apart rather than dropped: it is still a tidy-up, and a
    silently-filtered finding reads as "clean" when it isn't."""
    return "CASE" if a.lower() == b.lower() else "LINK"


def _clip(s, n=58):
    s = (s or "").replace("\n", " ")
    return s if len(s) <= n else s[:n - 1] + "…"


# ---------------------------------------------------------------- V. maintenance signal (report-only)
# `archived == true` is triage.py's P1 successor-check band, and it only catches
# maintainers who flipped GitHub's archive flag. daytonaio/daytona — ★72K, the catalog's
# canonical answer to "run untrusted AI-generated code" — announced discontinuation in
# its README in June 2026 and moved development to a private codebase, and sat in P3
# backlog as ordinary un-examined work for two months because `archived` stayed false
# (#351). P1 reading "0 leads" presents as "nothing archived to check"; that is true and
# also says nothing about how many catalogued projects are dead.
#
# This reports the two per-record signals `refresh-metadata.py --maintenance` writes:
# `discontinued` (the README banner phrase) and `license_lost` (a real license that
# became NONE/404 since the last snapshot — daytona went AGPL-3.0 → 404 while
# vercel-labs/skills went NONE → MIT, and detector R can see neither, because it ages
# the snapshot as a whole and both records were well inside the threshold).
#
# Report-only, and the ordering is the point: a discontinued tool with an ADOPT/KEEP
# verdict is a live recommendation to install a dead project, which is worth more than a
# dead `discovery-log` lead nobody was going to reach anyway.
#
# Each DISCONTINUED finding also carries whether the CATALOG row DISCLOSES it (#395).
# The verdict lives in COMPARISON.md and the eval; the catalog row is what a reader
# scans, and all three findings read as live projects — daytona's still advertises
# ★72K and "secure, elastic sandbox infrastructure" with no hint that core development
# moved to a private codebase. The catalog already has the convention (23 rows carry a
# `⚠️ archived` / `⚠️ no license` note, and detector C states the expectation outright);
# V just never propagated its own findings into it. A sub-signal, not a gate: these
# findings arrive from upstream's README via the network, so failing the build on one
# would fail it for a reason no commit caused (detector R's rule).
MaintenanceFinding = collections.namedtuple(
    "MaintenanceFinding", "slug kind detail verdict tool disclosed silent")

# Deliberately GENEROUS. A row that already discloses and is reported anyway pressures a
# human to re-add a note that is there, and V's own rule is that flagging a healthy row
# costs more than missing a sick one — the miss costs a stale row, the false positive
# costs trust in every other finding. Widen this when it flags a row that discloses in
# words not listed; do not narrow it to make the count look worse.
DISCLOSED = re.compile(
    r"discontinued|no longer (?:actively )?(?:maintained|developed)|unmaintained"
    r"|not maintained|archived|read-only|deprecated|sunset"
    r"|development .{0,20}moved|moved to a private", re.IGNORECASE)


def audit_maintenance(ctx):
    """MaintenanceFindings for every catalogued repo whose metadata records a
    discontinuation banner or a lost license, strongest verdict first. A cache with no
    maintenance fields yields nothing and says so via the count — the signal is opt-in
    on the refresher, so its absence means "not collected", never "nothing is dead"."""
    try:
        records = json.loads(ctx.read("repo-metadata.json"))
    except (OSError, ValueError):
        return [], 0, []
    if not isinstance(records, dict):
        return [], 0, []
    # slug -> EVERY catalog row behind it, because a record is a fact about a REPO and a
    # pack has several rows. "Does the row disclose?" (#395) is the wrong question for a
    # shared slug: if `mattpocock/skills` were discontinued, six rows would need the note
    # and asking `by_slug.setdefault(...)` asked one of them (#465).
    index = catalog_lib.link_index(ctx.catalog)
    verd = ctx.comparison_verdict_map
    collected = sum(1 for m in records.values()
                    if isinstance(m, dict) and ("discontinued" in m or "license_lost" in m))
    findings, acked = [], []
    for slug, meta in sorted(records.items()):
        if not isinstance(meta, dict):
            continue
        rows = catalog_lib.rows_for_slug(index, slug)
        container = catalog_lib.container_row(index, slug)
        # The pack's own row names the repo; with none, the slug does. Never "the first
        # row", which is what made this arbitrary.
        tool = container.name if container else (rows[0].name if len(rows) == 1 else slug)
        vs = sorted({next((verd[k] for k in catalog_lib.identity_keys(r.name) if k in verd), "—")
                     for r in rows}) or ["—"]
        v = ", ".join(vs)
        silent = tuple(r.name for r in rows if not _discloses(r))
        phrase = meta.get("discontinued")
        if phrase:
            f = MaintenanceFinding(slug, "DISCONTINUED", f'README: "{phrase}"', v, tool,
                                   not silent, silent)
            (acked if _acked(meta, phrase) else findings).append(f)
        if meta.get("license_lost"):
            # Scoped to DISCONTINUED: the catalog convention is about a project being
            # dead, and a row already prints its license, so there is nothing here for
            # a reader to be misled about in the same way.
            findings.append(MaintenanceFinding(slug, "LICENSE-LOST",
                                               f"now {meta.get('license_spdx')}", v, tool,
                                               True, ()))
    rank = {"ADOPT": 0, "KEEP": 0, "CONDITIONAL": 1, "DEFER": 2, "discovery-log": 3, "SKIP": 4}
    # Strongest verdict first, and a shared slug carries several — a dead tool we still
    # RECOMMEND outranks a dead lead nobody was going to reach, whatever its siblings say.
    def strongest(f):
        return min(rank.get(x, 3) for x in f.verdict.split(", "))
    for bucket in (findings, acked):
        bucket.sort(key=lambda f: (strongest(f), f.slug))
    return findings, collected, acked


def _discloses(row):
    """True when the CATALOG row itself tells a reader the project is dead (#395).

    A row with no catalog entry at all reports as disclosed rather than as a gap: there
    is no row to fix, so counting it would put a number on the board that nothing in
    this repo can move."""
    if row is None:
        return True
    return bool(DISCLOSED.search(" ".join(c for c in row.cells if c)))


def _acked(meta, phrase):
    """True when a human has recorded that THIS phrase is a false positive. The ack
    pins the exact phrase it was granted against, so a README that later gains a real
    repo-level banner reports again instead of hiding behind a stale acknowledgment.

    This exists because V's version-scoped class is not mechanically separable —
    giskard-oss says "no longer actively maintained" of Giskard **v2** while the repo
    ships v3 — and a permanently-stuck false positive turns "a number to shrink" into
    noise. Acked findings are still PRINTED, just not counted (no silent caps)."""
    ack = meta.get("discontinued_ack")
    return isinstance(ack, dict) and ack.get("phrase") == phrase


def audit_comparison(ctx):
    text = ctx.comparison
    body = catalog_lib.comparison_body_counts(text)          # shared with reconcile-counts.py
    breakdown = catalog_lib.comparison_verdict_breakdown(text)  # per-stage (validated, recommended)
    # Parse the Summary table into per-stage {tools, validated} plus the Total row.
    summary, total, in_summary = {}, None, False
    for l in text.splitlines():       # second pass: the Summary table only
        hm = re.match(r"^##\s+(.*)", l)
        if hm:
            in_summary = hm.group(1).strip().lower() == "summary"
            continue
        if not in_summary or not l.lstrip().startswith("|"):
            continue
        cells = _summary_cells(l)
        name = cells[0]
        if len(cells) < 3 or not cells[1].isdigit() or not cells[2].isdigit():
            continue  # header, separator, or a malformed row
        rec = {"tools": int(cells[1]), "validated": int(cells[2])}
        if name.lower() == "total":
            total = rec
        else:
            summary[name] = rec
    problems = []
    for s, rec in summary.items():
        if body.get(s, 0) != rec["tools"]:
            problems.append(f"section '{s}': summary Tools {rec['tools']}, body has {body.get(s, 0)}")
        exp_val = breakdown.get(s, (0, 0))[0]
        if rec["validated"] != exp_val:
            problems.append(f"section '{s}': summary Validated {rec['validated']}, real-verdict rows total {exp_val}")
    body_total = sum(body.values())
    val_total = sum(v for v, _ in breakdown.values())
    cat = catalog_lib.catalog_count(ctx.catalog)
    if total is not None:
        if total["tools"] != body_total:
            problems.append(f"Total Tools says {total['tools']}, body rows sum to {body_total}")
        if total["validated"] != val_total:
            problems.append(f"Total Validated says {total['validated']}, real-verdict rows sum to {val_total}")
        if total["tools"] != cat:
            problems.append(f"COMPARISON Total {total['tools']} != CATALOG.md {cat} entries")
    return problems

# ---------------------------------------------------------------- selftest
def selftest():
    """Lock in the evidence-classification precedence. Run: audit-evals.py --selftest"""
    cases = [
        # (label, how-section text, expect_fabrication, expect_measured)
        ("disclosed not-run review",
         "We did not install this; source review only.", False, False),
        ("verified hands-on run",
         "Ran it **live** via pip install; exercised the CLI.", False, False),
        ("bare run claim, no disclaimer = fabrication candidate",
         "We ran it on our repo and it generated the report.", True, False),
        ("measured A/B with no honest word = measured",
         "**Hands-on, measured** with-skill vs baseline A/B.", False, True),
        ("STRONG measured marker overrides a weak honest word (the bug we hit)",
         "**Hands-on, measured** — inspected each SKILL.md, ran a measured A/B.", False, True),
        ("weak measured token + honest disclaimer = NOT measured",
         "We did not run it; the author reports a with-skill number.", False, False),
    ]
    fails = []
    for label, how, exp_fab, exp_meas in cases:
        ev = Evidence(how)
        if ev.is_fabrication_candidate != exp_fab:
            fails.append(f"  FAIL [fabrication] {label}: got {ev.is_fabrication_candidate}, want {exp_fab}")
        if ev.is_measured != exp_meas:
            fails.append(f"  FAIL [measured] {label}: got {ev.is_measured}, want {exp_meas}")

    # Evidence.level derivation (issue #67 backfill)
    level_cases = [
        ("**Hands-on, measured** A/B with token deltas.", "MEASURED"),
        ("Source-grounded review — not run hands-on; read the docs.", "REVIEW"),
        ("We ran it on our repo and exercised the CLI flow.", "RUN"),
        ("", "SOURCE-ONLY"),
    ]
    for how, want in level_cases:
        got = Evidence(how).level
        if got != want:
            fails.append(f"  FAIL [level] {how[:32]!r}: got {got}, want {want}")

    # Evaluation parsing — the eval-file grammar is now a unit-testable surface
    def expect(cond, msg):
        if not cond: fails.append(f"  FAIL [eval] {msg}")
    skill = Evaluation("foo",
        "# Evaluation: Foo\n\n| [foo](https://github.com/a/foo) | skill | x | y | z |\n\n## Verdict\n\n**ADOPT**\n")
    expect(skill.is_skill, "skill-type row not detected")
    expect(skill.verdict == "ADOPT", f"verdict {skill.verdict!r} != ADOPT")
    expect("foo" in skill.name_aliases, "name alias from heading missing")
    tool = Evaluation("bar",
        "| [bar](https://github.com/a/bar) | tool | x | y | z |\n\n## Verdict\n\n**SKIP**\n")
    expect(not tool.is_skill, "tool-type row misdetected as skill")
    dual = Evaluation("baz", "## Verdict\n\n**ADOPT** for X — **CONDITIONAL** otherwise\n")
    expect(dual.verdict_set == {"ADOPT", "CONDITIONAL"}, f"dual verdict_set {dual.verdict_set}")
    none = Evaluation("qux", "## Overview\n\nNo verdict here.\n")
    expect(none.verdict is None and none.verdict_set == set(), "missing verdict not handled")
    # A lead headlines its own status rather than borrowing CONDITIONAL (#324).
    lead = Evaluation("lead", "## Verdict\n\n**discovery-log — tentative read** — notes only.\n")
    expect(lead.verdict == "discovery-log", f"lead verdict {lead.verdict!r} != discovery-log")
    # declared Evidence field (issue #62)
    eviz = Evaluation("ev", "## How we tested it\n\n**Evidence:** MEASURED\n\nran it live.\n")
    expect(eviz.evidence_level == "MEASURED", f"evidence_level {eviz.evidence_level!r} != MEASURED")
    src = Evaluation("sv", "**Evidence:** SOURCE-ONLY\n")
    expect(src.evidence_level == "SOURCE-ONLY", f"hyphenated level {src.evidence_level!r} != SOURCE-ONLY")
    expect(none.evidence_level is None, "absent Evidence field not None")
    n_eval_checks = 10

    if fails:
        print("== selftest ==")
        print("\n".join(fails))
        return 1
    print(f"== selftest ==\n  OK — {len(cases)} evidence + {len(level_cases)} level + {n_eval_checks} eval-parsing cases pass")
    return 0

# ---------------------------------------------------------------- CLI flag sets
# The seven offline gates `--offline` selects — the set `make check`, the
# `.claude/hooks/audit-gate.sh` pre-commit hook and the opencode commit-gate plugin all
# run (all three invoke `--offline` bare, so they move together). This tuple is the
# source of truth for what "offline" means; CLAUDE.md's prose list documents it and
# must be updated alongside any change here.
# ---------------------------------------------------------------- W. P0 scope mismatch (report-only)
# The score has no scope term (#353). Every term measures attention, so a lead that
# WORKFLOW.md's one-line exclusion already disposes of can still rank into P0 measure —
# the band reserved for leads that might reach ADOPT, and the one an unattended pass may
# not write to. Spending a measured evaluation to reach a SKIP a codified rule already
# reached is the most expensive path to that SKIP.

# The eval's OWN concession, harvested from the corpus rather than invented. The two
# dominant strings are WORKFLOW.md's exclusion quoted verbatim by the #348 SKIP pass.
SCOPE_CONCESSION = re.compile(
    r"for building AI products"
    r"|not for your own dev workflow"
    r"|building agentic products"
    r"|building an agentic product"
    r"|for building agent products"
    r"|build(?:s|ing) LLM apps"       # pydantic-ai: "It builds LLM apps, not coding agents."
    r"|building LLM-powered"
    r"|not a coding (?:agent|harness)"
    r"|drop-in coding harness"
    r"|not authoring code"
    r"|tangential to (?:the )?(?:coding|authoring)"
    r"|adjacent to the coding dev loop", re.IGNORECASE)

# An eval that quotes the exclusion in order to DISTINGUISH itself from it. Same shape as
# detector B's HONEST vocabulary: the escape hatch is what keeps the finding count honest,
# so widen this when it false-flags rather than narrowing the concession vocab above.
SCOPE_CLEARED = re.compile(
    r"clears the bar"
    r"|catalog-relevant as"
    r"|genuine bridge into"
    r"|not (?:merely |just )?a library for building", re.IGNORECASE)

# The Types WORKFLOW.md's exclusion is about ("visual/programmatic agent builders").
# A harness or tool is something you RUN; the exclusion was never aimed at it.
SCOPE_TYPES = frozenset({"framework", "platform"})

ScopeFinding = collections.namedtuple("ScopeFinding", "tool band typ phrase")


def audit_scope(ctx):
    """(findings, cleared) — leads whose own eval concedes the WORKFLOW.md scope
    exclusion, P0 first. `cleared` holds the ones that argue they clear the bar; they
    are printed but not counted, because a detector whose headline number includes its
    own known false positives is not a number anyone shrinks."""
    # Lazy import: triage.py loads THIS module at import time, so a module-level import
    # here would recurse. Called from main(), the nested copy never re-enters.
    triage = _load_sibling("triage_bands", "triage.py")
    try:
        ordered, _ranked, _incumbents = triage.assign(ctx)
    except (OSError, ValueError, KeyError):
        return [], []

    types = {catalog_lib.name_key(r.name): (r.type or "").strip()
             for r in catalog_lib.parse_catalog_rows(ctx.catalog)}
    by_key = {}
    for ev in ctx.evals:
        for k in catalog_lib.identity_keys(ev.name):
            by_key.setdefault(k, ev)

    findings, cleared = [], []
    for band, rows in ordered.items():
        for row in rows:
            tool = row[1]
            typ = types.get(catalog_lib.name_key(tool), "")
            if typ not in SCOPE_TYPES:
                continue
            ev = next((by_key[k] for k in catalog_lib.identity_keys(tool) if k in by_key), None)
            if ev is None:
                continue
            m = SCOPE_CONCESSION.search(ev.text)
            if not m:
                continue
            f = ScopeFinding(tool, band, typ, _scope_quote(ev.text, m))
            (cleared if SCOPE_CLEARED.search(ev.text) else findings).append(f)

    # P0 first: it is the only band a bulk lane cannot reach, so a finding there is the
    # one that stays stuck until a human looks.
    for bucket in (findings, cleared):
        bucket.sort(key=lambda f: (0 if f.band.startswith("P0") else 1, f.band, f.tool))
    return findings, cleared


def _scope_quote(text, match, width=110):
    """The conceding phrase in its own line, windowed around the match. Quoted rather
    than summarized so a human judges the eval's own words — detector V's rule, for the
    same reason: a phrase match is a candidate, not a disposition.

    Line-scoped on purpose. A sentence-scoped window ran past `\n` and produced quotes
    that spliced a header into a prose line ("...dev loop **Layer:** Infrastructure"),
    which reads as a garbled claim rather than as the eval's words."""
    ls = text.rfind("\n", 0, match.start()) + 1
    le = text.find("\n", match.end())
    line = " ".join(text[ls: le if le != -1 else len(text)].split()).strip(" -*_#|")
    hit = line.lower().find(match.group(0).lower().split("\n")[0][:20])
    if len(line) <= width or hit == -1:
        return line[:width] + ("…" if len(line) > width else "")
    start = max(0, hit - (width - len(match.group(0))) // 2)
    frag = line[start:start + width]
    return ("…" if start else "") + frag + ("…" if start + width < len(line) else "")



# ---------------------------------------------------------------- X. collapsed catalog identity (report-only)
# Two rows, one artifact (#343). A row naming a COMPONENT of something catalogued as a
# WHOLE overstates the lead queue, makes a redundancy verdict between the two meaningless
# ("redundant with X" is not a thing you can say about X's own contents), and strands the
# eliminate-only band, which can neither SKIP it nor explain it in a verdict.

IdentityFinding = collections.namedtuple("IdentityFinding", "kind slug tool verdict peers")

SETTLED_VERDICTS = frozenset({"ADOPT", "KEEP"})


def _names_container(row, declared):
    """True when this row IS one of the containers `declared` names — the pack row, whose
    own `Ships inside` cell is legitimately empty because it does not ship inside itself.

    Asked with `identity_keys`, NEVER `alias_keys` (#374). alias_keys adds the URL's repo
    basename, and every row in a collapsed group shares that URL — so a lead named `b`
    sitting at `github.com/o/pack` would answer to `pack` and be mistaken for the pack
    itself, which would let one declared row silently settle an undeclared sibling. The
    row's own NAME is the only thing that identifies it as the container."""
    keys = catalog_lib.identity_keys(row.name)
    return any(catalog_lib.name_key(c) in keys
               or catalog_lib.name_key(c.split("/")[-1]) in keys for c in declared)


def audit_identity(ctx):
    """(findings, faceted) — leads that are facets of one catalogued artifact, plus the
    multi-row groups that are NOT findings, carried so neither goes unmentioned.

    The split is by LINK SHAPE, and it carries all the precision. Where every row in a
    slug group points at one identical URL, nothing in the catalog tells them apart —
    that is the #343 pattern. Where each row links its own subpath, the group is a
    monorepo of independently-installable artifacts (`claude-plugins-official`: 8 rows,
    8 subpaths), which is a different thing and must not be counted as drift."""
    rows = [r for r in catalog_lib.parse_catalog_rows(ctx.catalog) if r.url]
    groups = collections.defaultdict(list)
    for r in rows:
        slug = next(iter(catalog_lib.github_repos(r.url)), None)
        if slug:
            groups[slug.lower()].append(r)

    verd = ctx.comparison_verdict_map

    def verdict_of(name):
        return next((verd[k] for k in catalog_lib.identity_keys(name) if k in verd), "—")

    findings, context = [], []
    for slug, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        by_verdict = [(r.name, verdict_of(r.name)) for r in members]
        names = tuple(n for n, _ in by_verdict)
        # DECLARED (#343) is checked FIRST, ahead of the link-shape split below, because
        # it is the stronger statement: FACETED *infers* from distinct subpaths that the
        # catalog distinguishes the rows, while DECLARED means the catalog says so, in a
        # column triage.py's P5 band already reads to keep them out of the queue. A group
        # qualifies when every member either names its container or IS the container the
        # others name — so the pack row's own empty cell is not a hole. Printed, never
        # counted: the same shape as FACETED, and what makes X's headline a number the
        # column can actually shrink.
        declared = {r.ships_inside for r in members if r.ships_inside}
        if declared and all(r.ships_inside or _names_container(r, declared) for r in members):
            context.append(IdentityFinding("DECLARED", slug, "", "", names))
            continue
        if len({r.url for r in members}) == len(members):
            context.append(IdentityFinding("FACETED", slug, "", "", names))
            continue
        settled = tuple((n, v) for n, v in by_verdict if v in SETTLED_VERDICTS)
        # A row that names its container is no longer an independent lead even when its
        # siblings stay undeclared — triage.py's P5 band already takes it out of the
        # queue. Filtering per row rather than per group is what makes the headline
        # monotone: filling one cell drops one finding, so the count walks to zero
        # instead of staying flat until the last row in a group is declared.
        resolved = {r.name for r in members
                    if r.ships_inside or (declared and _names_container(r, declared))}
        leads = [n for n, v in by_verdict if v == "discovery-log" and n not in resolved]
        if not leads:
            # The identity is still collapsed, but no queue slot is wasted — every row
            # is already disposed. Reported so the group is not silently invisible.
            context.append(IdentityFinding("NO-LEADS", slug, "", "", names))
            continue
        for name in leads:
            findings.append(IdentityFinding(
                "SETTLED" if settled else "COLLAPSED", slug, name,
                settled[0][1] if settled else "",
                tuple(n for n, _ in settled) if settled
                else tuple(n for n in names if n != name)))

    # SETTLED first: a lead whose artifact is already ADOPT/KEEP is the one whose queue
    # slot is provably wasted, where a COLLAPSED group is merely two facets of one
    # undecided thing.
    findings.sort(key=lambda f: (0 if f.kind == "SETTLED" else 1, f.slug, f.tool))
    return findings, context



# ---------------------------------------------------------------- Y. install-record mismatch (report-only)
# KEEP is DEFINED as the validated-installed status, and nothing checked the installed
# half (#366). Joined on SLUG rather than name, because name-matching is the bug itself:
# #332's "already installed/active" was a marketplace cache directory, and three STACK
# members are name collisions with an artifact from a different source.

SKILL_LOCK = "~/.agents/.skill-lock.json"          # npx skills (vercel-labs/skills) v3
PLUGIN_RECORD = "~/.claude/plugins/installed_plugins.json"
SKILL_DIR = "~/.claude/skills"
PLUGIN_CACHE = "~/.claude/plugins/cache"           # <marketplace>/<plugin>/<version|unknown>
# #332's discriminator, generalized. A directory under the plugin cache means the
# MARKETPLACE was added, never that a plugin was installed — that is the trap #332 fell
# into. But the version subdirectory splits the trap in two: `unknown` is listing metadata
# for a plugin whose code was never fetched, while a real version string ('3.1.0', a commit
# sha) means this machine pulled that plugin at that version. #332 used exactly this to
# separate the genuinely-installed claude-md-management (`1.0.0`, matching its installPath)
# from plugin-dev (`unknown`). Evidence of a fetch is strictly more than `unknown` and
# strictly less than an installed_plugins.json entry, so it gets its own bucket rather
# than being collapsed into either.
UNFETCHED = "unknown"
# The only Types these records can cover. A CLI or an MCP server is installed by npm,
# brew or a settings entry, none of which leaves a mark here — flagging them would be
# noise indistinguishable from signal.
INSTALLABLE_TYPES = frozenset({"skill", "plugin"})

InstallFinding = collections.namedtuple("InstallFinding", "kind tool verdict detail")


def read_install_records(home=None):
    """(skill_name -> source slug, set of installed slugs, set of names on disk,
    plugin name -> fetched version).

    Every value is absent-tolerant: a machine with no lockfile is a machine we know
    nothing about, which must read as 0 records rather than as a clean bill."""
    def path(p):
        return os.path.join(home, p.replace("~/", "")) if home else os.path.expanduser(p)

    by_name, slugs, on_disk, fetched = {}, set(), set(), {}
    try:
        with open(path(SKILL_LOCK), encoding="utf-8") as fh:
            for name, meta in (json.load(fh).get("skills") or {}).items():
                src = (meta or {}).get("source")
                if src:
                    by_name[name] = src.lower()
                    slugs.add(src.lower())
    except (OSError, ValueError, AttributeError):
        pass
    try:
        with open(path(PLUGIN_RECORD), encoding="utf-8") as fh:
            for key in (json.load(fh).get("plugins") or {}):
                on_disk.add(key.split("@")[0])
    except (OSError, ValueError, AttributeError):
        pass
    with contextlib.suppress(OSError):
        on_disk |= set(os.listdir(path(SKILL_DIR)))
    cache = path(PLUGIN_CACHE)
    for market in _listdir(cache):
        for plugin in _listdir(os.path.join(cache, market)):
            vers = [v for v in _listdir(os.path.join(cache, market, plugin))
                    if v != UNFETCHED]
            if vers:                       # a real version string: the code was pulled
                # Every fetched version, not a "latest": these are opaque strings (semver
                # AND commit shas), and a lexicographic max reads 13.11.0 as older than
                # 13.4.0. Reporting the set states what is on disk and invents no order.
                fetched.setdefault(plugin, ", ".join(vers))
    return by_name, slugs, on_disk, fetched


def _listdir(p):
    try:
        return sorted(d for d in os.listdir(p) if not d.startswith("."))
    except OSError:
        return []


def audit_installed(ctx, home=None):
    """(findings, shadowed, records) — ADOPT/KEEP skill/plugin rows this machine's install
    records do not back, plus installed sources the catalog does not know.

    THE SLUG IS ASKED FIRST (#366). The row's own slug being present in the lockfile
    settles the row: it is installed, full stop. A skill of the same name sourced from
    somewhere else is then a name shadow, not a missing install — `caveman` (ADOPT,
    JuliusBrussee/caveman) ships four `caveman-*` skills that ARE installed here, while
    the bare name `caveman` in the lockfile belongs to mattpocock/skills. Testing the
    name first reported that row as a COLLISION, i.e. as an unbacked ADOPT, which it is
    not. A detector that flags a healthy row is worse than one that misses a sick one —
    detector V's rule, and the same identity-by-name root the detector exists to find.

    Shadows are returned APART and printed rather than counted: the name really does
    resolve elsewhere on this machine, which is worth knowing and is not a defect in
    the row (V's `acked`, W's `cleared`, X's `FACETED`).

    CACHE-ONLY sits between NO-RECORD and clean (#366). The plugin cache is #332's trap
    — a directory there means the marketplace was added — but the version subdirectory
    splits it: `unknown` is listing metadata, while a real version string means the code
    was pulled. Four rows sat in NO-RECORD holding a fetched version (claude-reflect
    3.1.0, superpowers 5.1.0, security-guidance 2.0.6, claude-mem 13.11.0/13.4.0), which
    'nothing on the machine answers to this row' does not describe. It is still a finding
    — a fetch is not an activation, and nothing records which of the two happened — but
    calling it NO-RECORD overstates by exactly the amount #332 warned about in the other
    direction."""
    by_name, slugs, on_disk, fetched = read_install_records(home)
    records = len(by_name) + len(on_disk) + len(fetched)
    if not records:
        return [], [], 0

    verd = ctx.comparison_verdict_map
    rows = [r for r in catalog_lib.parse_catalog_rows(ctx.catalog) if r.url]
    catalogued = {(next(iter(catalog_lib.github_repos(r.url)), "") or "").lower()
                  for r in rows}
    lock_by_key = {catalog_lib.name_key(n): s for n, s in by_name.items()}
    disk_keys = {catalog_lib.name_key(n) for n in on_disk}
    fetched_keys = {catalog_lib.name_key(n): v for n, v in fetched.items()}

    findings, shadowed = [], []
    for r in rows:
        v = next((verd[k] for k in catalog_lib.identity_keys(r.name) if k in verd), "—")
        if v not in SETTLED_VERDICTS or (r.type or "").strip() not in INSTALLABLE_TYPES:
            continue
        slug = (next(iter(catalog_lib.github_repos(r.url)), "") or "").lower()
        key = catalog_lib.name_key(r.name)
        installed_from = lock_by_key.get(key)
        shadow = installed_from and installed_from != slug
        if slug in slugs:                      # the row's own repo is installed: settled
            if shadow:
                shadowed.append(InstallFinding(
                    "SHADOWED", r.name, v,
                    f"{slug} is installed; the name '{r.name}' resolves to "
                    f"{installed_from} instead"))
        elif shadow:
            findings.append(InstallFinding(
                "COLLISION", r.name, v,
                f"row says {slug}, installed skill of that name comes from {installed_from}"))
        elif key in fetched_keys:
            findings.append(InstallFinding(
                "CACHE-ONLY", r.name, v,
                f"no install record; plugin cache holds fetched version(s) "
                f"{fetched_keys[key]} — code was pulled, activation is unrecorded"))
        elif key not in disk_keys:
            findings.append(InstallFinding(
                "NO-RECORD", r.name, v, f"no record and no directory answers to {slug}"))

    for slug in sorted(slugs - catalogued):
        n = sum(1 for s in by_name.values() if s == slug)
        findings.append(InstallFinding("UNCATALOGUED", slug, "—",
                                       f"{n} installed skill(s), no catalog row"))

    rank = {"COLLISION": 0, "NO-RECORD": 1, "CACHE-ONLY": 2, "UNCATALOGUED": 3}
    findings.sort(key=lambda f: (rank[f.kind], f.tool))
    shadowed.sort(key=lambda f: f.tool)
    return findings, shadowed, records



# ---------------------------------------------------------------- Z. unread license declaration (report-only)
# `license_spdx: NONE` is what GitHub returns when there is no root LICENSE file. It is
# recorded, and read by triage.py's P4 mechanical-skip band, as though it meant the repo
# grants nothing — and for 8 of 28 records it did not (#372). This reports the gap
# against the disposition each row already carries, strongest first: a SKIP whose stated
# ground is the license is a wrong disposition, not merely a wrong record.

# A verdict "rests on the license" when it says so. Deliberately narrow — a passing
# mention ("MIT, permissive") must not count, or every clean row becomes a finding.
LICENSE_GROUND = re.compile(
    r"no (?:declared |real |explicit )?licen[cs]e"
    r"|licen[cs]e(?: is)? (?:not declared|absent|missing)"
    r"|no LICENSE file"
    r"|carrying no licen[cs]e grant"
    r"|licen[cs]e alone"
    r"|\*\*SKIP\*\* ?\(licen[cs]e\)", re.IGNORECASE)

# A verdict that has ALREADY withdrawn its license ground still quotes the claim it
# withdrew — because quoting it is the honest way to record a correction (detector V's
# rule). Without this, an eval is punished for documenting its own repair and the count
# can never reach zero. Same shape as W's "argues it clears the bar" and V's ack: still
# printed, not counted.
#
# The recognized form is a STRUCK-THROUGH claim, `~~…licen…~~`, or an explicit
# withdrawn/retracted sentence naming the license. Widen this vocabulary if it misses an
# honest retraction — never narrow LICENSE_GROUND to compensate, which would hide live
# findings to clear stale ones.
LICENSE_WITHDRAWN = re.compile(
    r"~~[^~]{0,300}licen[a-z]*[^~]{0,300}~~"
    r"|licen[a-z]*[^.\n]{0,100}(?:is |was |been )?(?:withdrawn|retracted)"
    r"|(?:withdrawn|retracted)[^.\n]{0,100}licen[a-z]*", re.IGNORECASE)

LicenseFinding = collections.namedtuple(
    "LicenseFinding", "kind tool slug verdict spdx where phrase conflict")


def _license_subject(index, slug, verd, grounds):
    """(tool, verdict, verdict-section, grounded) for the row a license record is ABOUT.

    Every row behind the slug is asked; the first whose SKIP rests on the license wins,
    because that is the disposition the declaration refutes. With none, the pack's own
    row names the repo, then a lone row, then the slug — never "whichever came first"."""
    rows = catalog_lib.rows_for_slug(index, slug)

    def read(name):
        v = next((verd[k] for k in catalog_lib.identity_keys(name) if k in verd), "—")
        sec = next((grounds[a] for a in catalog_lib.alias_keys(name) if a in grounds), "")
        return v, sec, bool(v == "SKIP" and LICENSE_GROUND.search(sec))

    for r in rows:
        v, sec, grounded = read(r.name)
        if grounded:
            return r.name, v, sec, True
    container = catalog_lib.container_row(index, slug)
    subject = container.name if container else (rows[0].name if len(rows) == 1 else slug)
    v, sec, _ = read(subject)
    return subject, v, sec, False


def audit_license_declared(ctx):
    """(findings, records) — catalogued repos whose metadata records a license declared
    outside a LICENSE file, plus the number of records carrying the field.

    A cache with no `license_declared` anywhere yields 0 RECORDS, not 0 findings: the
    field is written by the refresher, so its absence means "not collected", never
    "every NONE is a real absence" (detector V's rule, same reason)."""
    try:
        records = json.loads(ctx.read("repo-metadata.json"))
    except (OSError, ValueError):
        return [], 0, []
    if not isinstance(records, dict):
        return [], 0, []

    index = catalog_lib.link_index(ctx.catalog)
    verd = ctx.comparison_verdict_map
    # alias -> the eval's Verdict section, so "is the license the stated ground?" reads
    # the argument rather than the whole file (a How-we-tested `gh api ... .license` line
    # is evidence of a check, not of a disposition).
    grounds = {}
    for ev in ctx.evals:
        sec = re.search(r"##\s*Verdict.*?(?=\n##\s|\Z)", ev.text, re.DOTALL)
        if sec:
            for a in ev.name_aliases:
                grounds.setdefault(a, sec.group(0))

    collected = sum(1 for m in records.values()
                    if isinstance(m, dict) and m.get("license_declared"))
    findings, withdrawn = [], []
    for slug, meta in sorted(records.items()):
        if not isinstance(meta, dict):
            continue
        d = meta.get("license_declared")
        if not isinstance(d, dict) or not d.get("spdx"):
            continue
        # A record is a fact about a REPO, and several rows can sit behind one slug —
        # `modelcontextprotocol/servers` holds two SKIPs and a container. Asking
        # `by_slug.setdefault(...)` asked whichever row CATALOG.md listed first, so a
        # mechanical SKIP grounded in a license absence could hide behind a sibling
        # (#465). Ask them all, and report the GROUNDED one: that is the row whose
        # disposition the declaration voids.
        tool, v, sec, grounded = _license_subject(index, slug, verd, grounds)
        if grounded:
            kind = "GROUNDED"
        elif d.get("conflict"):
            kind = "CONFLICT"
        else:
            kind = "RECORDED"
        f = LicenseFinding(kind, tool, slug, v, d["spdx"], d.get("where", "?"),
                           d.get("phrase", ""), d.get("conflict"))
        (withdrawn if grounded and LICENSE_WITHDRAWN.search(sec) else findings).append(f)

    rank = {"GROUNDED": 0, "CONFLICT": 1, "RECORDED": 2}
    for bucket in (findings, withdrawn):
        bucket.sort(key=lambda f: (rank[f.kind], f.tool))
    return findings, collected, withdrawn


# ---------------------------------------------------------------- AA. unactionable containment (report-only)
# `Ships inside` (#343) exists to make containment machine-readable, and triage.py reads
# it FIRST — ahead of even the mechanical bands — to put a row in P5, whose disposition is
# "settle the container, or SKIP `ships inside <container>` — never an independent lead".
# That remedy has a precondition nobody checked: the container has to be findable. The
# cell is free text, and its two documented rules (a slug, never a display name; empty
# means independently installable) are enforced by nothing (#405).
#
# Resolution keys on the URL SLUG, never the display name, and that gap is the whole
# reason this went unlooked-at: the column stores `anthropics/claude-plugins-official`
# while the row is named `claude-plugins-official`. Same identity discipline as #343 /
# #366 / #374 — key on what the row *is*, which in slug-space is its link.

ContainmentFinding = collections.namedtuple("ContainmentFinding", "kind tool container verdict")


def _repo_path(url):
    """The github.com path segments of `url`, or [] for a non-GitHub link. `o/r` is the
    repo identity `Ships inside` names; anything past it is a link to a component."""
    if not url or "github.com/" not in url.lower():
        return []
    return url.lower().rstrip("/").split("github.com/")[-1].split("/")


def _repo_root(url):
    """`https://github.com/o/r/tree/main/x` -> `o/r`; None for a non-GitHub link."""
    p = _repo_path(url)
    return "/".join(p[:2]) if len(p) >= 2 else None


def _links_repo_root(url):
    """True when the link points at the repo ROOT rather than at a path inside it.
    The distinction is the whole SELF-LINKED test: `.../claude-plugins-official/tree/
    main/plugins/frontend-design` names an artifact, `.../claude-plugins-official`
    names the pack, and both share a repo root."""
    return len(_repo_path(url)) == 2


def audit_containment(ctx):
    """(findings, declared) — `Ships inside` declarations P5 cannot act on.

    Two kinds, reported apart because their remedies differ:

      UNROWED      the declared container has no catalog row, so "settle the container"
                   names something not in the inventory. This is the case CLAUDE.md
                   records as invisible to detector X and needing a human — true before
                   the column existed, a slug compare after it (`presentation-creator`
                   declares `getsentry/skills` in a cell now).
      SELF-LINKED  the row's own link IS the declared container's repo root, so the row
                   asserts *I am a component of X* while pointing at X. Every fact hanging
                   off that link then describes the container, not the artifact — `prisma`'s
                   ★46.9K measures the ORM, not the MCP server. The fix is a narrower link
                   or a dropped declaration, which is why it is not folded into UNROWED.

    A row can carry either independently: `modelcontextprotocol/servers`' three rows each
    link their own subpath and have no container row; the five `mattpocock/skills` rows
    have a container row they cannot be told apart from.

    Report-only. Each finding's remedy is a human deciding WHICH of the two facts is
    wrong — the link, the declaration, or the missing row — and that is not a call a bulk
    lane may make."""
    rows = list(catalog_lib.parse_catalog_rows(ctx.catalog))
    # A container row is one that links the repo ROOT and does not itself declare a
    # container — a row that ships inside something is a member, never the pack.
    containers = {_repo_root(r.url) for r in rows
                  if not r.ships_inside and _links_repo_root(r.url)}
    verd = ctx.comparison_verdict_map
    findings, declared = [], 0
    for r in rows:
        if not r.ships_inside:
            continue
        declared += 1
        c = r.ships_inside.strip().strip("`").lower()
        v = next((verd[k] for k in catalog_lib.identity_keys(r.name) if k in verd), "—")
        if c not in containers:
            findings.append(ContainmentFinding("UNROWED", r.name, c, v))
        if _links_repo_root(r.url) and _repo_root(r.url) == c:
            findings.append(ContainmentFinding("SELF-LINKED", r.name, c, v))
    # UNROWED first: a disposition pointing at nothing outranks one pointing at a row
    # whose link is merely too coarse. Leads before disposed rows within a kind — a
    # stalled queue slot is the cost this is about.
    rank = {"UNROWED": 0, "SELF-LINKED": 1}
    findings.sort(key=lambda f: (rank[f.kind], f.verdict != "discovery-log", f.container, f.tool))
    return findings, declared


# ---------------------------------------------------------------- AF. unfalsified containment (report-only)
# `Ships inside` is DEFINED by "empty is the default and means independently installable"
# (#343), so every filled cell asserts an artifact is NOT independently installable — and
# until #431 nothing in the repo could contradict one. Detector AA checks the OTHER rules
# (the container is findable, the row does not link it); this checks the one the column is
# defined by.
#
# It matters more than an ordinary unvalidated field because of what the cell buys.
# triage.py reads it FIRST, ahead of even the mechanical bands, and bands the row P5
# ships-inside, whose disposition is the strongest instruction in the triage system:
# "never an independent lead". A wrong cell does not misrank a lead; it removes it from
# the queue and forbids the conclusion.
#
# Three cells were wrong. Each `modelcontextprotocol/servers` subpath ships its own
# package.json — `@modelcontextprotocol/server-memory` and its two siblings each live on
# npm with their own release stream — while the container's own manifest is `"private":
# true`, so "settle the container" named an operation that cannot be performed. The
# catalog said so itself: the container row reads "each independently installable".
#
# The signal is collected by `refresh-metadata.py --containment` and read here offline —
# detector V's exact shape, and for V's reason: this finding arrives from upstream's
# package layout over the network, so failing a build on one would fail it for a reason
# no commit caused.

ContainmentEvidenceFinding = collections.namedtuple(
    "ContainmentEvidenceFinding", "kind tool container path package verdict")


def audit_containment_evidence(ctx):
    """(refuted, confirmed, unchecked, records) — `Ships inside` cells npm contradicts.

    One counted kind:

      REFUTED    the declared subpath publishes its own package, so the artifact IS
                 independently installable and the cell should be empty. P5 is holding a
                 lead it has no claim to.

    Two printed and never counted (V's `acked`, W's `cleared`, X's `FACETED`):

      confirmed  checked, and the subpath publishes nothing. This is NOT proof of
                 containment — a pack could publish to npm without a per-member manifest
                 — so the absence keeps the row here rather than promoting it to a
                 finding. The published-package test only ever REFUTES, which makes
                 detector V's rule (flagging a healthy row costs more than missing a sick
                 one) structural rather than promised.
      unchecked  no record for the subpath, or the row links a repo ROOT so there is no
                 component to ask about (`prisma`, `jira`, `confluence` — already
                 detector AA's SELF-LINKED). An uncollected signal reports 0 records,
                 never 0 findings.

    Report-only. The remedy for a REFUTED row is a human deciding whether to empty the
    cell or narrow the row, which is not a call a bulk lane may make."""
    try:
        records = json.loads(ctx.read("repo-metadata.json"))
    except (OSError, ValueError):
        records = {}
    verd = ctx.comparison_verdict_map
    refuted, confirmed, unchecked, seen = [], [], [], 0
    for r in catalog_lib.parse_catalog_rows(ctx.catalog):
        if not r.ships_inside:
            continue
        container = r.ships_inside.strip().strip("`").lower()
        v = next((verd[k] for k in catalog_lib.identity_keys(r.name) if k in verd), "—")
        m = re.match(r"https://github\.com/[^/]+/[^/]+/tree/[^/]+/(.+?)/?$",
                     (r.url or "").strip(), re.IGNORECASE)
        members = (records.get(container) or {}).get("member_packages") or {}
        path = m.group(1) if m else None
        if path is None or path not in members:
            unchecked.append(ContainmentEvidenceFinding(
                "unchecked", r.name, container, path, None, v))
            continue
        seen += 1
        pkg = members[path]
        f = ContainmentEvidenceFinding(
            "REFUTED" if pkg else "confirmed", r.name, container, path, pkg, v)
        (refuted if pkg else confirmed).append(f)
    # Leads first within each bucket: a stalled queue slot is the cost this is about,
    # and a cell on an already-disposed row is a wrong fact with no queue effect.
    for bucket in (refuted, confirmed, unchecked):
        bucket.sort(key=lambda f: (f.verdict != "discovery-log", f.container, f.tool))
    return refuted, confirmed, unchecked, seen


# ---------------------------------------------------------------- AG. stage drift (report-only)
# A tool's dev loop stage is written twice: every eval declares `**Dev loop stage:**` in
# its header, and every COMPARISON.md row *sits under* a stage section. Nothing compared
# them, and 16 rows sit under a stage their own eval never names (#453).
#
# The cost is not the ranking — recomputing next-evals.py's score with each lead moved to
# the stage its header names shifts nothing by more than 1.7 and moves no lead between
# bands. It is the per-stage Summary, and through it `stage_gap_weight`, the one term
# whose job is to say which stage is starving. Ship holds THREE rows, one of which
# (`worktrunk`) its own eval assigns to Implement while `commit-commands`, filed under
# Implement, says Ship; that bucket produces the largest inner-loop gap weight there is,
# 6.67, and taking the headers at face value drops it to 5.00 — from hungriest by a
# distance to fourth. "Ship is our thinnest stage" is a claim COMPARISON's Summary makes
# on the front of a derived page, and one row decides it.
#
# The two sources already meet, unchecked, on one page: watchlist.py builds a single
# `| Tool | Stage |` table whose cell comes from the COMPARISON section for row-backed
# entries and from the eval's own header for eval-only ones (#416). They happen to agree
# there today, which is exactly the condition under which this gets found late.
LOOP_STAGES = ("Plan", "Implement", "Verify", "Review", "Ship", "Reflect")

StageFinding = collections.namedtuple("StageFinding", "kind tool section named header")


def named_stages(header):
    """The loop stages a `**Dev loop stage:**` header names, in loop order.

    Word-anchored, so `Implementation` and `Planning` are prose rather than stage names.
    A header naming none — `Cross-cutting`, `Mostly off-loop (an SDK for building LLM
    apps)`, `Outer loop / Discover` — is an honest non-answer and returns []; grading
    prose into a finding is what check-stars.py refuses to do with a legitimately-`n/a`
    field."""
    return [s for s in LOOP_STAGES if re.search(rf"\b{s}\b", header, re.IGNORECASE)]


def _comparison_section_map(ctx):
    """COMPARISON row key → its `## Section`, exact name first, ambiguous keys dropped.

    Mirrors ctx.comparison_verdict_map's identity keying, except that an ambiguous
    stripped key resolves to NOTHING rather than first-wins: a verdict picked by coin
    flip is a wrong verdict, but a *section* picked by coin flip would file a pick under
    a stranger's stage and manufacture a finding — the expensive direction (detector V's
    rule)."""
    by_section = catalog_lib.comparison_rows_by_section(ctx.comparison)
    out, dupes = {}, set()
    for section, rows in by_section.items():
        for r in rows:
            for k in catalog_lib.identity_keys(r.tool):
                if k in out and out[k] != section:
                    dupes.add(k)
                out.setdefault(k, section)
    return {k: v for k, v in out.items() if k not in dupes}


def audit_stage_drift(ctx):
    """(drift, stack_drift, comparable, unusable) — the stage written in two places.

    Two counted kinds, reported apart because their remedies differ:

      DRIFT        a COMPARISON row under one of the six inner-loop stage sections whose
                   eval's header names loop stages and the section is none of them.
      STACK-DRIFT  a STACK.md stage-table pick whose COMPARISON section is also a loop
                   stage and is a different one. STACK is a THIRD copy of the same fact.

    Four precision rules:

    * Only the six inner-loop stage sections are compared. COMPARISON's other sections
      (`MCP Servers`, `Reference`, `Skills & Plugins`, …) are *categories*, not stages —
      a row under `MCP Servers` whose eval says Implement contradicts nothing, and
      comparing them would flag 316 healthy rows. That rule is also why STACK-DRIFT
      requires BOTH sides to name a stage: three of STACK's four disagreements are a
      stage table vs a category section, a different axis and legitimate.
    * A header naming no loop stage is never a finding — see named_stages().
    * ANY named stage matching the section is agreement. A tool that spans stages must
      still be filed under one: `sandboxd` reads `Verify / Ship`, `agnix` reads `Verify
      … also Ship (CI gate) and Implement (in-editor LSP)`. Generous by construction —
      detector V's rule. It is already doing work: `resolving-merge-conflicts` reads
      `Ship … touches Implement` and its section is Implement, so it is NOT a DRIFT
      finding even though STACK and COMPARISON disagree about it. Widen the stage
      vocabulary when it misses one; never narrow it to make the count look worse.
    * The detector never says which side is wrong and bands nothing. The header can be
      the stale one (written before the tool's scope was understood) or the section can
      be, so the header is QUOTED (detector V's rule) and a human reads the sentence.

    Report-only: the remedy is a human moving a row or rewriting a header, a judgement
    call rather than bookkeeping."""
    stages = frozenset(LOOP_STAGES)
    sections = _comparison_section_map(ctx)
    drift, comparable, unusable = [], 0, 0
    for section, rows in catalog_lib.comparison_rows_by_section(ctx.comparison).items():
        if section not in stages:
            continue
        for r in rows:
            ev = next((ctx.eval_by_row[k] for k in catalog_lib.identity_keys(r.tool)
                       if k in ctx.eval_by_row), None)
            header = ev.dev_loop_stage if ev else None
            named = named_stages(header) if header else []
            if not named:
                unusable += 1
                continue
            comparable += 1
            if section not in named:
                drift.append(StageFinding("DRIFT", r.tool, section, named, header))

    stack_drift, stack_section = [], None
    for line in ctx.stack.splitlines():
        hm = re.match(r"^##\s+(.*)", line)
        if hm:
            stack_section = catalog_lib.strip_parenthetical(hm.group(1).strip()).strip()
            continue
        if not line.lstrip().startswith("|"):
            continue  # picks live in the install-command tables, not the prose
        m = re.match(r"^\|\s*\[([^\]]+)\]", line.strip())
        if not m or stack_section not in stages:
            continue
        pick = m.group(1)
        row_section = next((sections[k] for k in catalog_lib.identity_keys(pick)
                            if k in sections), None)
        if row_section in stages and row_section != stack_section:
            stack_drift.append(StageFinding(
                "STACK-DRIFT", pick, row_section, [stack_section],
                f"STACK.md files it under {stack_section}"))

    drift.sort(key=lambda f: (f.section, f.tool))
    stack_drift.sort(key=lambda f: f.tool)
    return drift, stack_drift, comparable, unusable


# ---------------------------------------------------------------- AI. layer drift (report-only)
# `**Layer:**` was the one eval header field NOTHING read (#475). Every other field has a
# consumer — `**Stars:**` (check-stars.py), `**Last verified:**` (backfill-lastverified.py
# + the staleness sweep), `**Evidence:**` (backfill-evidence.py, tier-stack.py),
# `**Last triaged:**` (detector Q), `**Dev loop stage:**` (detector AG since #453). Layer
# had a comment and three test fixtures.
#
# It is not decorative: CLAUDE.md's opening states the model ("three layers per stage —
# process, tooling, infrastructure") and TEMPLATE.md declares a CLOSED set. The fact is
# then written in three places and all three drifted:
#
#   1. 30 evals name a layer TEMPLATE.md does not define (Harness ×12, Reference ×9,
#      Platform, Skill pack, N/A), and 9 carry no `**Layer:**` line at all.
#   2. 18 of 34 resolvable WORKFLOW.md layer-table rows sit under a layer their own eval
#      never names — 53%, against detector AG's 5% for the STAGE axis of the same table.
#   3. `## Adopting This Workflow` is a third copy and contradicts the stage tables on 11
#      of the 14 tools it names twice, using a FOURTH layer name (`Orchestration`) that
#      appears in no template, no eval header and no stage table.
#
# (3) is the one a newcomer acts on: the ladder's Process heading reads "install the
# skills that enforce discipline — NO INFRASTRUCTURE NEEDED" and lists four tools the
# stage tables all file under Tooling. Detector P exists on the sentence "the operating
# manual and the install list must not give a newcomer two different answers"; here both
# answers are inside the operating manual, 300 lines apart.
#
# AG checked the stage axis of this 2-D map and stopped there, because #453 was scoped to
# `**Dev loop stage:**`: the layer is the other axis of the same table, one cell to the
# left, in the same file.

LAYERS = ("Process", "Tooling", "Infrastructure")

LayerFinding = collections.namedtuple(
    "LayerFinding", "kind tool declared named header line")
# Every bucket reports n/total, never a bare finding count (#467): "12 within WORKFLOW.md
# itself" reads identically whether 14 tools were compared or none were.
LayerCoverage = collections.namedtuple("LayerCoverage", "rows filed_twice declaring")

# A layer table is any markdown table whose header row's first cell is `Layer`. The layer
# cell is bold (`| **Process** |`) and continuation rows leave it empty, so it carries
# forward — which is why this is a line-by-line walk rather than a regex.
_LAYER_CELL = re.compile(r"^\**\s*(Process|Tooling|Infrastructure)\s*\**$", re.IGNORECASE)
# `### Start here: Process`, `### Add when you want data: Infrastructure`.
_LADDER_HEAD = re.compile(r"^###\s+(?:Start here|Add when you want\s+\w+):\s*(\w+)\s*$")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_MD_LINK_TEXT = re.compile(r"\[([^\]]+)\]\(")


def named_layers(header):
    """The layers a `**Layer:**` header names, in model order.

    Word-anchored, and generous by construction: `Process / Tooling` names both, so a row
    filed under either is agreement. Detector V's rule — flagging a healthy row costs more
    than missing a sick one — so widen this when it misses a layer and never narrow it to
    make the count look worse. A header naming none (`Harness`, `Reference`, `N/A`) is
    what UNDECLARED reports; it is deliberately NOT treated as an honest non-answer, the
    way `named_stages` treats `Cross-cutting`, because TEMPLATE.md declares a closed set
    here and an absent header is the honest way to decline it."""
    return [ly for ly in LAYERS if re.search(rf"\b{ly}\b", header, re.IGNORECASE)]


def _workflow_layer_rows(text):
    """[(line, layer, cell)] — every tool row under a `| Layer |` table's layer cell."""
    rows, cur, in_table = [], None, False
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.startswith("#"):
            cur, in_table = None, False
            continue
        if not ln.lstrip().startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not cells:
            continue
        if cells[0].strip("* ").lower() == "layer":  # the table's own header row
            cur, in_table = None, True
            continue
        if not in_table or len(cells) < 2:
            continue
        m = _LAYER_CELL.match(cells[0])
        if m:
            cur = m.group(1).capitalize()
        if cur and cells[1]:
            rows.append((i, cur, cells[1]))
    return rows


def _ladder_entries(text):
    """{tool-key: layer} from `## Adopting This Workflow`'s bulleted ladder.

    Its headings carry a FOURTH layer name (`Orchestration`) that exists nowhere else, so
    the value is kept verbatim rather than normalised into the closed set — reporting the
    name it actually uses is the finding."""
    out, head = {}, None
    for ln in text.splitlines():
        m = _LADDER_HEAD.match(ln)
        if m:
            head = m.group(1)
            continue
        if ln.startswith("##") and not ln.startswith("###"):
            head = None
        if not head or not ln.startswith("- **"):
            continue
        for name in _BOLD.findall(ln):
            # `code-review plugin + pr-review-toolkit` and `headroom + context-mode` name
            # two tools in one bullet; a trailing `plugin`/`skill` is a noun, not a name.
            for part in re.split(r"\s*\+\s*", name):
                tool = re.sub(r"\s+(plugin|skill)$", "", part.strip(), flags=re.IGNORECASE)
                if tool:
                    out.setdefault(catalog_lib.name_key(tool), (tool, head))
    return out


def audit_layer_drift(ctx):
    """(drift, self_drift, undeclared, no_layer, comparable) — the layer axis of the map.

    Three counted kinds:

      DRIFT       a WORKFLOW.md layer-table row whose eval's `**Layer:**` header names a
                  different layer. The eval defines the tool; the table files it.
      SELF-DRIFT  a tool the adoption ladder and a stage table file differently. Purely
                  internal to WORKFLOW.md, so it needs no join and cannot be a resolution
                  artifact — the strongest kind for that reason, and the one a newcomer
                  actually acts on.
      UNDECLARED  an eval whose `**Layer:**` names none of TEMPLATE.md's three.

    One printed and never counted (V's `acked`, W's `cleared`, X's `FACETED`):

      no-layer    an eval with no `**Layer:**` line. 8 of the 9 are comparison, collection
                  or scan documents with no single subject, so declining the field is the
                  honest answer and check-stars.py's rule against grading a legitimately-
                  `n/a` field applies verbatim. The ninth (`composio`) is a single-subject
                  eval whose field is simply absent — which is why the bucket is PRINTED
                  rather than dropped: a human can see the one that differs.

    Two rules carried straight from AG. ANY named layer matching is agreement, so
    `Process / Tooling` filed under either is healthy (detector V's rule). And the detector
    never says WHICH side is wrong — the eval header can be the stale one or the table can
    be — so the header is QUOTED and it bands nothing. Report-only: every remedy is a human
    choosing between two judgements."""
    index = catalog_lib.link_index(ctx.catalog)
    drift, self_drift, undeclared, no_layer = [], [], [], []

    # --- UNDECLARED / no-layer: the eval corpus against TEMPLATE.md's closed set.
    for ev in ctx.evals:
        hdr = ev.layer
        if not hdr:
            no_layer.append(LayerFinding("no-layer", ev.name, None, [], "", 0))
        elif not named_layers(hdr):
            undeclared.append(LayerFinding("UNDECLARED", ev.name, None, [], hdr, 0))

    # --- DRIFT: WORKFLOW.md's layer tables against each row's own eval.
    table = {}
    comparable = 0
    for line, layer, cell in _workflow_layer_rows(ctx.workflow):
        # A linked row identifies its tool by link text; an unlinked one (`**Beads**
        # — …`) still names it, and the ladder cites those by name, so both are indexed.
        lm = _MD_LINK_TEXT.search(cell)
        text = lm.group(1) if lm else re.sub(r"\s+—.*", "", cell).strip("* ")
        if text:
            table.setdefault(catalog_lib.name_key(text), (text, layer, line))
        url = re.search(r"\((https://github\.com/[^)]+)\)", cell)
        if not url:
            continue
        slug = next(iter(catalog_lib.github_repos(url.group(1))), "")
        row, _ambig = catalog_lib.resolve_link(index, text, url.group(1), slug)
        if not row:
            continue
        ev = ctx.eval_by_row.get(catalog_lib.name_key(row.name))
        hdr = ev.layer if ev else None
        named = named_layers(hdr) if hdr else []
        if not named:
            continue
        comparable += 1
        if layer not in named:
            drift.append(LayerFinding("DRIFT", row.name, layer, named, hdr, line))

    # --- SELF-DRIFT: WORKFLOW.md against itself, no join at all.
    filed_twice = 0
    for key, (name, head) in sorted(_ladder_entries(ctx.workflow).items()):
        if key not in table:
            continue
        filed_twice += 1
        if table[key][1] != head:
            self_drift.append(
                LayerFinding("SELF-DRIFT", name, head, [table[key][1]],
                             f"its own stage table files it under {table[key][1]}",
                             table[key][2]))

    drift.sort(key=lambda f: (f.declared, f.tool))
    undeclared.sort(key=lambda f: (f.header.lower(), f.tool))
    no_layer.sort(key=lambda f: f.tool)
    cover = LayerCoverage(comparable, filed_twice,
                          len(ctx.evals) - len(no_layer))
    return drift, self_drift, undeclared, no_layer, cover


# ---------------------------------------------------------------- AJ. link identity mismatch (report-only)
# Every identity fix this repo has landed asked the same question in one direction: given a
# SLUG, which catalog row is it about (#343, #366, #374, #413, #457, #463, #465). Nothing
# ever asked the other one — given the NAME a link puts in front of a reader, does the URL
# under it point at that tool. It does not, 8 times, and 4 of them are in `STACK.md`, the
# page whose whole purpose is to be executed (#416): the Plan-stage row reads
# `| [GSD](https://github.com/obra/superpowers) | ... | claude install-plugin obra/superpowers |`,
# so a reader who wants GSD installs `superpowers`, a different catalogued tool with a
# different verdict, a different owner and none of GSD's skills.
#
# Every detector passes on it, and they pass for the same reason: they all resolve by slug,
# and `obra/superpowers` is a perfectly good ADOPT row. Detector J derives STACK from the
# ledger and finds `superpowers` ADOPT — fine. Detector P demands every STACK pick appear in
# `WORKFLOW.md` and finds `superpowers` on line 77 — fine, and note what that agreement is
# worth: the manual never names GSD at all, so the two pages "agree" about a tool the
# install list is not actually recommending. Detector AE asks whether a WORKFLOW link
# carries a SKIP — `superpowers` is ADOPT. Detector U compares an eval's mirror against its
# catalog row and never reads STACK. The one fact none of them holds is the link's own TEXT.
LinkIdentityFinding = collections.namedtuple(
    "LinkIdentityFinding", "rel line text named slug rows")


def _text_row_index(catalog_text):
    """(by_name, by_key) for resolving a link's TEXT to a catalog row.

    Exact name first, `identity_keys` second — `verify-installs.py`'s rule, and the key
    fallback keeps `identity_keys` rather than `alias_keys` because a URL basename is not
    a synonym between two rows that each name a tool (#374). A key two rows claim resolves
    to NOTHING rather than to a coin flip (detector U's AMBIG rule).
    """
    by_name, by_key = {}, collections.defaultdict(list)
    for r in catalog_lib.parse_catalog_rows(catalog_text):
        by_name.setdefault(r.name.strip().lower(), r)
        for k in catalog_lib.identity_keys(r.name):
            if not any(x.name == r.name for x in by_key[k]):
                by_key[k].append(r)
    return by_name, dict(by_key)


def _resolve_link_text(by_name, by_key, text):
    """The one catalog row a link's text names, or None. Markdown emphasis is stripped —
    the corpus cites this tool as ``GSD`` as often as GSD — and nothing else is guessed."""
    t = re.sub(r"[`*_]", "", text).strip()
    if not t:
        return None
    row = by_name.get(t.lower())
    if row:
        return row
    seen = []
    for k in catalog_lib.identity_keys(t):
        for c in by_key.get(k, []):
            if not any(x.name == c.name for x in seen):
                seen.append(c)
    return seen[0] if len(seen) == 1 else None


# Where a link RECOMMENDS or CITES a tool by name. `CATALOG.md` is deliberately out of
# scope: a row's Name cell names its own row by construction, so it could never be a
# finding, and eval-vs-catalog link disagreement is detector U's `LINK` bucket already.
LINK_IDENTITY_FILES = ("STACK.md", "WORKFLOW.md")
_MD_LINK = re.compile(r"\[([^\]\n]+)\]\((https://github\.com/[^)\s]+)\)")


def audit_link_identity(ctx):
    """(findings, walked) — links whose TEXT names catalogued row A while their URL points
    at a repo row A is not behind.

    Both sides must resolve to something catalogued or the link is not walked, which is
    what keeps this conservative: prose text that is not a tool name resolves to nothing,
    and an uncatalogued repo has no rows to compare against. 907 of the corpus's links
    clear both bars today.

    The precision rule is that the healthy set is EVERY row behind the slug
    (`catalog_lib.rows_for_slug`), never the one row a single-answer resolver would pick.
    `STACK.md` and the evals link a pack member at the pack ROOT — `[feature-dev](.../
    claude-plugins-official)`, `[resolving-merge-conflicts](.../mattpocock/skills)` — which
    #465 documents as the healthy shape, and 85 walked links sit behind a shared slug. A
    first-row resolver flags 49 of them; asking the whole set flags none.

    Report-only, and it bands and fixes nothing. The detector cannot say which side is
    wrong — the link may need repointing or the text may need renaming — and here it is
    the harder direction: the 8 live findings are one conflated pair whose repair reaches
    `STACK.md`, `STACK-LEDGER.md`, `CATALOG.md`'s own "now redirects here" prose and 8 SKIP
    verdicts that name one tool as the incumbent while citing the other. That is a per-item
    human read (#345's rule against bulk-fixing in either direction), not a fixer.
    """
    idx = catalog_lib.link_index(ctx.catalog)
    by_name, by_key = _text_row_index(ctx.catalog)
    files = [*LINK_IDENTITY_FILES,
             *sorted(glob.glob("evaluations/*.md", root_dir=ctx.root))]
    findings, walked = [], 0
    for rel in files:
        if not os.path.exists(ctx.path(rel)):
            continue
        for i, line in enumerate(ctx.read(rel).splitlines(), 1):
            for text, url in _MD_LINK.findall(line):
                slugs = catalog_lib.github_repos(url)
                if not slugs:
                    continue
                rows = catalog_lib.rows_for_slug(idx, slugs[0])
                named = _resolve_link_text(by_name, by_key, text)
                if named is None or not rows:
                    continue
                walked += 1
                if not any(x.name == named.name for x in rows):
                    findings.append(LinkIdentityFinding(
                        rel, i, text.strip(), named.name, slugs[0],
                        [x.name for x in rows]))
    # Reported in WALK order, which is detector A's shape ("in file order — this IS the
    # reported order") and which already puts `STACK.md` first: an executed page outranks
    # a cited one, the same ordering detector V uses when it sorts a dead tool we still
    # recommend above a dead lead nobody was going to reach. A `sort()` here would be a
    # second expression of the same intent, agreeing with `files` until one of them moved.
    return findings, walked


# ---------------------------------------------------------------- AH. unread repo install record (report-only)
# `skills-lock.json` is the one install record that lives INSIDE the tree, and nothing in
# the repo read it (#473). Detector F (#398) and detector Y (#366) both want an install
# fact and both read `~/.agents/.skill-lock.json` — the HOME lockfile, a fact about one
# laptop. Y is documented local-only for exactly that reason: "CI has no lockfile, and a
# build that fails for a reason no code change caused is worse than the drift it would
# catch." That is right about the home lockfile and does NOT transfer here: this file is
# committed, so it is as readable in CI as CATALOG.md is.
#
# What the silence cost is that "we already run this" reaches no derived surface:
#
#   lead                 band            score   overlap_pressure   run here?
#   openskills           P2 challenger   18.5625        5           no
#   vercel-labs/skills   P3 backlog      12.5625        2           YES (lockfile at root)
#
# Six points and one band apart, in the wrong order — and the bands compound it. P3's
# disposition is "leave; stamp **Last triaged:** only", so the tool in use sits in the one
# band that cannot dispose of anything, while its un-run competitor sits in P2, whose
# disposition is SKIP "redundant with <incumbent>". next-evals.py scores
# `2*overlap_pressure + stage_gap_weight + evidence_bonus`; all three terms measure how
# much attention a lead attracts and none asks whether we are already running it, which is
# detector W's observation ("none asks whether it is a tool this catalog is for") in a
# second dimension.

RepoInstallFinding = collections.namedtuple(
    "RepoInstallFinding", "kind key slug verdict tool")

# The `npx skills` project lockfile (vercel-labs/skills). Same record shape detector Y
# reads from the home lockfile — a `source` slug per entry — one directory over.
REPO_SKILL_LOCK = "skills-lock.json"


def audit_repo_installs(ctx):
    """(findings, evaluated, records) — vendored sources this repo runs but never judged.

    Two counted kinds:

      UNEVALUATED-INCUMBENT  the repo vendors it and its catalog row is still a
                             `discovery-log` lead. The strongest kind: the queue holds a
                             lead for a tool already in use here, and ranks it purely on
                             the attention it attracts.
      UNCATALOGUED           the vendored source has no catalog row at all — found from
                             the INSTALL side, which is the only side that can see it
                             (detector Y's rule: a scan looks at what exists, never at
                             what is already running here).

    One printed and never counted (V's `acked`, W's `cleared`, X's `FACETED`):

      evaluated              the row carries a real verdict. This is the healthy state and
                             the outcome the detector exists to produce; counting it would
                             leave the headline unable to reach zero.

    Resolution is by SLUG, never by the lockfile KEY. `find-skills` is the key and is a
    skill NAME several packs ship; `vercel-labs/skills` is the identity (#343/#366/#374).

    A missing, empty or unparseable lockfile yields 0 records, and 0 records is never 0
    findings (detector V's rule): vendoring nothing is a different statement from a clean
    sweep. Report-only, and staying that way — the remedy for the live finding is a human
    running an eval, which is work rather than bookkeeping, so unlike check-links.py this
    does not gate."""
    try:
        lock = json.loads(ctx.read(REPO_SKILL_LOCK))
    except (OSError, ValueError):
        lock = {}
    entries = lock.get("skills") or {}
    if not isinstance(entries, dict):
        entries = {}

    index = catalog_lib.link_index(ctx.catalog)
    verd = ctx.comparison_verdict_map
    findings, evaluated, records = [], [], 0
    for key, rec in sorted(entries.items()):
        slug = ((rec or {}).get("source") or "").strip().lower()
        if not slug:
            continue
        records += 1
        rows = catalog_lib.rows_for_slug(index, slug)
        if not rows:
            findings.append(RepoInstallFinding("UNCATALOGUED", key, slug, "—", None))
            continue
        # A slug can carry several rows (#465). The container row — the one linking the
        # repo root — is what the lockfile's `source` names, so it is the subject; with no
        # such row, fall back to the first rather than to a coin flip between the rest.
        row = catalog_lib.container_row(index, slug) or rows[0]
        v = next((verd[k] for k in catalog_lib.identity_keys(row.name) if k in verd), "—")
        kind = "UNEVALUATED-INCUMBENT" if v == "discovery-log" else "evaluated"
        f = RepoInstallFinding(kind, key, slug, v, row.name)
        (findings if kind != "evaluated" else evaluated).append(f)

    findings.sort(key=lambda f: (f.kind, f.slug))
    evaluated.sort(key=lambda f: f.slug)
    return findings, evaluated, records


# ---------------------------------------------------------------- AB. unentitled CONDITIONAL (report-only)
# ADR-0005 collapsed the CONDITIONAL bucket because at 83% of rows the verdict carried no
# discriminating signal, and its rule is a disjunction: a real verdict requires EITHER the
# tool to have been exercised OR a genuine `adopt-if:` condition — "no genuine condition ⇒
# it is not a CONDITIONAL". #69 demoted the 404 rows that satisfied neither and parked
# point 1 (condition strings on the survivors) as an optional follow-up. It was never
# done, and nothing has ever asked the verdict data (#407).
#
# Detector T guards ONE direction of the same rule: an eval headlining CONDITIONAL over a
# `discovery-log` row. It exits early on any other row verdict, so a row reading
# CONDITIONAL in COMPARISON.md itself is never examined — and D, which checks that eval
# and row AGREE, passes happily when both name a verdict neither is entitled to.
ADOPT_IF = re.compile(r"adopt-if\s*:", re.IGNORECASE)
EXERCISED = frozenset({"MEASURED", "RUN"})

ConditionalFinding = collections.namedtuple("ConditionalFinding", "tool evidence gated")


def audit_conditional_gate(ctx):
    """(unentitled, ungated, total) — CONDITIONAL rows against ADR-0005's two clauses.

    A finding is a row entitled to NEITHER clause: not exercised and carrying no
    `adopt-if:` condition. Two remedies, and the detector names both because it cannot
    pick between them — declare the gate (usually a one-line edit by whoever wrote the
    verdict), or demote to `discovery-log`, which is #69's operation and the
    eliminate-only-safe direction since it removes a verdict rather than asserting one.

    `ungated` is the exercised-but-conditionless set: entitled to the word under the
    second clause, so NOT findings, but ADR-0005 point 1 still wants a condition on them
    and that number should be visible rather than implied (V's `acked`, W's `cleared`,
    X's `FACETED`, F's demonstrated peers).

    Report-only, and deliberately not a bulk demotion: blanket-demoting would destroy the
    real judgment inside rows whose gate was merely never written in the parseable form —
    #345's reason for declining to bulk-fix mirror drift in either direction."""
    by_alias = {}
    for ev in ctx.evals:
        for a in ev.name_aliases:
            by_alias.setdefault(a, ev)
    unentitled, ungated, total = [], [], 0
    for key, verdict in sorted(ctx.comparison_verdict_map.items()):
        if verdict != "CONDITIONAL":
            continue
        total += 1
        ev = by_alias.get(key)
        # No eval at all is the weakest possible ground for a verdict, so it can never be
        # entitled: SOURCE-ONLY by definition (backfill-evidence's rule) and ungateable.
        level = ev.effective_evidence if ev else "SOURCE-ONLY"
        gated = bool(ev and ADOPT_IF.search(ev.text))
        f = ConditionalFinding(ev.name if ev else key, level, gated)
        if gated or level in EXERCISED:
            if not gated:
                ungated.append(f)
        else:
            unentitled.append(f)
    return unentitled, ungated, total


# ---------------------------------------------------------------- AE. WORKFLOW recommends a SKIP (report-only)
# Detector P guards ONE direction of the "two different answers to what do I use for X"
# invariant — every STACK pick must appear in WORKFLOW.md — and grants the reverse an
# explicit exemption: "WORKFLOW legitimately lists non-STACK CONDITIONAL options." That
# exemption is right for CONDITIONAL and discovery-log; it is not right for SKIP, which
# is the catalog concluding DON'T USE THIS. Five of the manual's 62 catalogued links
# carry one, none disclosing it — including `trailofbits/skills`, listed twice as a
# Review-stage option and SKIPped because vendoring it attaches CC-BY-SA ShareAlike to
# the consuming repo (#414). P was scoped to a missing pick; a recommended elimination is
# the louder failure and nothing looked for it. Detector V's shape (#395) one file over.

# WORKFLOW.md already carries the disclosure convention — a `## Tools Deliberately
# Excluded` section and in-line forms like codeburn's "logged-excluded from STACK" — so a
# line that discloses is context, not a recommendation. Deliberately GENEROUS: flagging a
# line that already discloses pressures a human to re-add a note that is there, which
# inverts detector V's rule that flagging a healthy row costs more than missing a sick
# one. Widen it when it misses a disclosure phrased differently; never narrow it to make
# the count look worse.
WF_DISCLOSED = re.compile(
    r"\bSKIP\b|excluded|exclude\b|superseded|deliberately not|not recommended"
    r"|⚠️|do not use|don't use|rejected", re.IGNORECASE)
_WF_EXCLUDED_SECTION = re.compile(r"^##\s*Tools Deliberately Excluded", re.IGNORECASE)

WorkflowSkipFinding = collections.namedtuple("WorkflowSkipFinding", "tool slug line text")


_MD_LINK = re.compile(r"\[([^\]]+)\]\((https://github\.com/[^)\s]+)\)")


def _line_links(line):
    """(text, url) for every markdown github link on a line, plus ('', url) for a bare
    one. The text is not decoration: it is what distinguishes `[codebase-design]
    (github.com/mattpocock/skills)` from the five other rows behind that slug."""
    links = _MD_LINK.findall(line)
    linked = {u for _t, u in links}
    bare = [("", "https://github.com/" + s) for s in catalog_lib.github_repos(line)
            if not any(("github.com/" + s).lower() in u.lower() for u in linked)]
    return links + bare


def audit_workflow_skips(ctx):
    """(findings, disclosed, linked) — WORKFLOW.md links whose catalog row reads SKIP.

    Matched by github slug, NEVER display name — detector P's rule, since names vary
    ("GSD" links to `obra/superpowers`). Only SKIP counts: CONDITIONAL and
    `discovery-log` mentions are the exemption P deliberately grants, and DEFER means
    revisit rather than don't-use, so reporting them would drown the ones that matter.

    Report-only, like P: the remedy is a human choosing between two edits — drop the
    line, or disclose the verdict on it — and a bulk lane may not make that call."""
    try:
        workflow = ctx.read("WORKFLOW.md")
    except OSError:
        return [], [], 0
    index = catalog_lib.link_index(ctx.catalog)
    verd = ctx.comparison_verdict_map

    findings, disclosed, linked, in_excluded = [], [], 0, False
    for n, line in enumerate(workflow.splitlines(), 1):
        if line.startswith("## "):
            in_excluded = bool(_WF_EXCLUDED_SECTION.match(line))
        for text, url in _line_links(line):
            # The manual links a component at the pack root too — nine WORKFLOW lines do
            # — so the link text is what tells the candidates apart. Reading the slug
            # alone asked whichever row CATALOG.md listed first, and three of the seven
            # shared slugs hold a SKIP (#465).
            row, candidates = catalog_lib.resolve_link(index, text, url)
            if candidates or not row:
                continue
            linked += 1
            v = next((verd[k] for k in catalog_lib.identity_keys(row.name) if k in verd), None)
            if v != "SKIP":
                continue
            f = WorkflowSkipFinding(row.name, next(iter(catalog_lib.github_repos(url)), ""),
                                    n, line.strip()[:110])
            (disclosed if in_excluded or WF_DISCLOSED.search(line) else findings).append(f)

    findings.sort(key=lambda f: (f.tool, f.line))
    disclosed.sort(key=lambda f: (f.tool, f.line))
    return findings, disclosed, linked


# ---------------------------------------------------------------- AC. license header vs record (report-only)
# `repo-metadata.json` is the tree's record of upstream facts, and every eval header
# restates one of them by hand next to it. Nothing compared the two (#411) — and the
# license is the one restated fact that DISPOSITIONS rest on: `pi-subagents` carries a
# SKIP reading "no declared license … text carrying no license grant cannot be copied
# in" against a record fetched two days earlier reading MIT.
#
# This is #372's shape in the file #372 did not look at. Detector Z reports when the
# RECORD understates the license — `license_spdx: NONE` means "no LICENSE *file*" — and
# fires only on NONE, so an understatement on the EVAL's side is invisible to it.
#
# Stars and `Last updated` are deliberately out of scope. They are point-in-time facts
# that SHOULD move as the repo does (39 headers hold star counts off by >25%, 172 of 420
# dates differ from `pushed_at`), and reporting them would be --staleness a second time.
# A license is a ground: it changes rarely, and `license_lost` already treats a change as
# an event. The same line detector V draws between dormancy and discontinuation.

# GitHub's licensee detector reads a root LICENSE file and nothing else, so all three of
# these mean "no readable LICENSE file", never "no license": NONE (live repo, no file),
# NOASSERTION (a file it could not parse), 404 (unreachable). None is a ground a header
# can contradict — that gap belongs to detector Z, and re-reporting it here would put
# #372's rows on a second scoreboard.
UNREADABLE_SPDX = frozenset({"NONE", "NOASSERTION", "404"})

# An honest non-answer, not a claim — check-stars.py's rule, which refuses to grade a
# legitimately-`n/a` field rather than pressure an author into inventing a value.
LICENSE_VAGUE = re.compile(r"^(?:n/?a|unknown|unspecified|not specified|tbd|[-—?])\s*$",
                           re.IGNORECASE)

# A POSITIVE, checkable claim that the repo grants nothing — the one ground a P4
# mechanical SKIP may rest on. Unlike the vague values above it is refutable, and a
# record naming a real SPDX refutes it.
LICENSE_ABSENT = re.compile(
    r"noassertion|no licen[cs]e|none specified|unlicensed|not licen[cs]ed"
    r"|licen[cs]e[ds]? (?:absent|missing)|^none\b", re.IGNORECASE)

# Family, not string equality: `MIT` / `MIT License` / `mit` is not drift. A header may
# name SEVERAL — `Apache-2.0 (docs CC-BY-4.0)` licenses code and prose differently, and
# the record can only hold one — so this yields a SET and a conflict means the two sets
# are disjoint. Comparing a single "first family found" made that header a finding
# against a record naming one of the two licenses it declares.
LICENSE_FAMILIES = {
    "agpl": "AGPL", "lgpl": "LGPL", "gpl": "GPL", "cc-by-sa": "CC-BY-SA",
    "cc-by": "CC-BY", "cc0": "CC0", "mpl": "MPL", "mozilla": "MPL",
    "apache": "Apache", "mit": "MIT", "0bsd": "0BSD", "bsd": "BSD",
    "isc": "ISC", "unlicense": "Unlicense", "busl": "BSL", "bsl": "BSL",
    "business source": "BSL", "elastic": "Elastic", "eupl": "EUPL",
    "epl": "EPL", "osl": "OSL", "afl": "AFL", "artistic": "Artistic",
    "zlib": "Zlib", "wtfpl": "WTFPL", "proprietary": "PROPRIETARY",
}

# Longest alternative first and non-overlapping, so a longer discriminator always wins:
# AGPL must never match as GPL nor CC-BY-SA as CC-BY, since those obligations differ and
# collapsing them would hide a real conflict. The letter guards keep `mit` out of
# "permitted" and `unlicense` out of "unlicensed" (an absence claim, not The Unlicense).
_LICENSE_FAMILY_RE = re.compile(
    r"(?<![a-z])(?:" +
    "|".join(re.escape(t) for t in sorted(LICENSE_FAMILIES, key=len, reverse=True)) +
    r")(?![a-z])", re.IGNORECASE)


def license_families(text):
    """Every license family named in `text`, as a set (empty if it names none)."""
    return {LICENSE_FAMILIES[m.group(0).lower()]
            for m in _LICENSE_FAMILY_RE.finditer(text or "")}


LicenseHeaderFinding = collections.namedtuple(
    "LicenseHeaderFinding", "kind name slug header spdx")


def audit_license_header(ctx):
    """(findings, redirected, compared) — eval `**License:**` headers against the SPDX
    `repo-metadata.json` records for the same repo.

    UNGROUNDED (the header asserts an absence the record refutes) sorts ahead of
    CONFLICT (both name a license, they differ), because only the first can invalidate a
    disposition rather than merely a fact — and UNGROUNDED-SKIP sorts ahead of both,
    because there it *has* (#417).

    That split is the whole point of reporting a header at all. AC used to print all
    three of the tree's UNGROUNDED findings identically, and they were not the same
    thing: `pi-subagents` carried a live `SKIP` whose entire stated ground was the
    absence, while `kreuzberg` and `repowise` carried `discovery-log` open items that the
    record simply answered. The line already read "a mechanical SKIP resting on it has no
    ground" while checking nothing about whether one did.

    The grounding test is detector Z's, reused rather than re-implemented (`LICENSE_GROUND`
    / `LICENSE_WITHDRAWN`), so the two license detectors cannot disagree about what
    "rests on the license" means. A verdict that has already withdrawn its ground drops
    back to plain UNGROUNDED — the header is still wrong, but the disposition is a
    documented repair, and Z's rule is that quoting the claim you retract is the honest
    way to record one.

    Why this direction needs watching at all: every one of those headers was correct when
    it was written, and upstream moved afterwards — `pi-subagents` added its MIT LICENSE
    twenty days *after* the P4 bulk triage SKIPped it for having none. `license_lost`
    (detector V) already treats a license *disappearing* as an event; a license appearing
    is the direction that voids a disposition rather than aging a fact, and a header
    frozen at triage time is exactly the frozen claim that makes it visible.

    `redirected` is printed and never counted: a record whose `resolved_name` differs in
    its OWNER arrived through a redirect and describes the destination, so it is not
    evidence about this row — `samuraigpt/awesome-hermes-agent` resolves to
    `Anil-matcha/ai-creator-academy`, and that eval says so by hand. Counting it would
    pressure a human to copy a known-false fact into a header, which inverts detector V's
    rule that flagging a healthy row costs more than missing a sick one.

    A missing or unreadable cache yields 0 COMPARED, never 0 findings (V's rule)."""
    try:
        records = json.loads(ctx.read("repo-metadata.json"))
    except (OSError, ValueError):
        return [], [], 0
    if not isinstance(records, dict):
        return [], [], 0
    by_lower = {k.lower(): (k, v) for k, v in records.items() if isinstance(v, dict)}
    verd = ctx.comparison_verdict_map

    findings, redirected, compared = [], [], 0
    for ev in ctx.evals:
        header = ev.license_header
        if header is None:
            continue
        slug = rec = None
        for url in ev.repo_links:
            hit = next((by_lower[s.lower()] for s in catalog_lib.github_repos(url)
                        if s.lower() in by_lower), None)
            if hit:
                slug, rec = hit
                break
        if not rec:
            continue
        resolved = rec.get("resolved_name") or slug
        spdx = rec.get("license_spdx")
        if resolved.split("/")[0].lower() != slug.split("/")[0].lower():
            redirected.append(LicenseHeaderFinding("redirected", ev.name, resolved,
                                                   header, spdx))
            continue
        if not spdx or spdx in UNREADABLE_SPDX:
            continue
        compared += 1
        if LICENSE_VAGUE.match(header):
            continue
        if LICENSE_ABSENT.search(header):
            # Does a disposition rest on the absence the record just refuted? Z's test,
            # reused: the ROW's verdict (the disposition of record, per detector D) plus
            # LICENSE_GROUND over the eval's own argument. A verdict that already
            # withdrew its ground is a documented repair, not a live invalid disposition.
            v = next((verd[k] for k in ev.name_aliases if k in verd), None) or ev.verdict
            sec = re.search(r"##\s*Verdict.*?(?=\n##\s|\Z)", ev.text, re.DOTALL)
            sec = sec.group(0) if sec else ""
            grounded = (v == "SKIP" and LICENSE_GROUND.search(sec)
                        and not LICENSE_WITHDRAWN.search(sec))
            kind = "UNGROUNDED-SKIP" if grounded else "UNGROUNDED"
            findings.append(LicenseHeaderFinding(kind, ev.name, slug, header, spdx))
            continue
        hf, rf = license_families(header), license_families(spdx)
        if hf and rf and hf.isdisjoint(rf):
            findings.append(LicenseHeaderFinding("CONFLICT", ev.name, slug, header, spdx))

    rank = {"UNGROUNDED-SKIP": 0, "UNGROUNDED": 1, "CONFLICT": 2}
    findings.sort(key=lambda f: (rank[f.kind], f.name))
    redirected.sort(key=lambda f: f.name)
    return findings, redirected, compared


# ---------------------------------------------------------------- AD. duplicate evals (report-only)
# `prisma-mcp.md` carries a written CONDITIONAL and its row reads `discovery-log` /
# `SOURCE-ONLY` — the value backfill-evidence assigns to "a name with no eval" — so
# NEXT-EVALS.md queues an evaluation that already exists, and detector D, whose whole job
# is that an eval agrees with its row, cannot see the disagreement because it cannot find
# the eval (#412). Eight rows have two eval files and in every one the WEAKER file wins:
# the row-keyed maps are built with setdefault, so resolution is first-wins in filename
# order and a later stub sorts first.
#
# The lane that wrote those stubs could not resolve the name. `name_aliases` keys an eval
# by its embedded mirror's Name cell only when that cell carries a github link, and
# TEMPLATE.md mirrors are written with a bare name — so the clause discards exactly the
# cell that says which row the eval claims. That is #401's bug in the shared alias
# function: there it produced a false ORPHAN, here a silently missing finding.

EVIDENCE_STRENGTH = {lvl: i for i, lvl in enumerate(reversed(EVIDENCE_LEVELS))}

DuplicateFinding = collections.namedtuple("DuplicateFinding", "kind row resolved shadows")


def _claim_strength(ev):
    """How much a claimant says. A real verdict outranks none; Evidence breaks ties."""
    return (ev.verdict in catalog_lib.REAL_VERDICTS,
            EVIDENCE_STRENGTH.get(ev.effective_evidence, 0))


def audit_duplicate_evals(ctx):
    """(findings, claimed) — COMPARISON rows claimed by more than one eval file.

    An eval CLAIMS the row its `## Catalog entry` mirror names, link or no link — #401's
    ruling that an unlinked entry is still a catalogued tool — or the row its own aliases
    resolve to. Two precision rules, both read off the corpus:

    * An eval embedding more than one mirror row is a COMPARISON document and its rows
      are references, not claims (`cost-observability` embeds tokencost, Infracost and
      abtop; without this it reads as a second eval of abtop, which it is not).
    * Resolution is EXACT catalog name first — verify-installs.py's rule. `agent-skills`
      and `agentskills` collapse to one name_key (detector U's AMBIG example) but are two
      distinct rows with two distinct evals, and a key-only match would report a
      duplicate that isn't one.

    SHADOWED sorts ahead of DUPLICATE: it is the kind where the row resolves to the
    weaker file, so the row reports less than the tree holds — a wrong record, not merely
    a redundant one."""
    claims = ctx.eval_claims
    findings = []
    for row, evs in sorted(claims.items()):
        if len(evs) < 2:
            continue
        # What the row-keyed maps see today: first-wins over ctx.evals (filename) order,
        # and only via name_aliases — the mirror claim is exactly what they cannot read.
        resolved = next((e for e in evs if row in e.name_aliases), None)
        shadows = [e for e in evs if e is not resolved]
        kind = ("SHADOWED" if resolved and any(
            _claim_strength(s) > _claim_strength(resolved) for s in shadows)
            else "DUPLICATE")
        findings.append(DuplicateFinding(
            kind, row,
            (resolved.name, resolved.verdict, resolved.effective_evidence)
            if resolved else None,
            sorted((s.name, s.verdict, s.effective_evidence) for s in shadows)))

    findings.sort(key=lambda f: (f.kind != "SHADOWED", f.row))
    return findings, len(claims)


OFFLINE_GATES = ("--fabrication", "--verdicts", "--comparison", "--drift",
                 "--verdict-evidence", "--rows", "--bulk-triage")
# With no flags at all: the offline gates plus the network install resolver.
DEFAULT_GATES = (*OFFLINE_GATES, "--installs")
# Opt-in reports. Never in the default set; never affect the exit code.
REPORT_FLAGS = ("--links", "--archived", "--skills", "--skill-design", "--overlaps",
                "--workflow-drift", "--clusters", "--savings-claims", "--evidence",
                "--staleness", "--metadata-staleness", "--lead-headlines",
                "--catalog-mirror", "--maintenance", "--scope", "--identity", "--installed",
                "--license-declared", "--containment", "--conditional-gate",
                "--license-header", "--duplicate-evals", "--workflow-skips",
                "--containment-evidence", "--stage-drift", "--repo-installs",
                "--layer-drift", "--link-identity")
DETECTOR_FLAGS = DEFAULT_GATES + REPORT_FLAGS
# Every argument main() accepts. Anything else is a typo, and a typo used to be silently
# dropped from `sel` — which made the argument list read as empty and turned `--ofline`
# into "run everything, including the ~26s network resolver", exit 0. Fail loudly instead.
KNOWN_FLAGS = (*DETECTOR_FLAGS, "--offline", "--selftest")

# ---------------------------------------------------------------- main
def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())

    unknown = [a for a in args if a not in KNOWN_FLAGS]
    if unknown:
        print(f"audit-evals: unknown argument(s): {' '.join(unknown)}", file=sys.stderr)
        print(f"  known: {' '.join(sorted(KNOWN_FLAGS))}", file=sys.stderr)
        sys.exit(2)

    # Requested detectors are a UNION, so a flag can only ever ADD work. The old matrix
    # ended in an `if explicit:` block that dropped the `or "--offline" in sel` clause,
    # so `--offline --verdicts` ran 1 detector where `--offline` alone ran 7 — adding a
    # flag silently deleted six gates and still exited 0.
    # Every surviving arg is a detector flag or `--offline`: `--selftest` returned above
    # and anything unrecognized exited 2, so no filtering is left to do here.
    sel = set(args)
    want = set()
    if "--offline" in sel:
        want |= set(OFFLINE_GATES)
    want |= (sel - {"--offline"})
    if not want:
        want = set(DEFAULT_GATES)

    do_inst = "--installs" in want
    do_fab  = "--fabrication" in want
    do_verd = "--verdicts" in want           # offline, fast
    do_comp = "--comparison" in want         # offline gate
    do_drift = "--drift" in want             # offline gate (#70)
    do_vev = "--verdict-evidence" in want    # offline gate (#71)
    do_rows = "--rows" in want               # offline gate (#198)
    do_bulk = "--bulk-triage" in want        # offline gate
    do_links = "--links" in want             # opt-in: ~450 network requests, slow
    do_archived = "--archived" in want       # opt-in: ~450 gh-api calls; report-only
    do_skills = "--skills" in want           # opt-in report (does not affect exit code)
    do_skill_design = "--skill-design" in want  # opt-in report (does not affect exit code)
    do_overlaps = "--overlaps" in want       # opt-in report (does not affect exit code)
    do_wf_drift = "--workflow-drift" in want    # opt-in report (does not affect exit code)
    do_clusters = "--clusters" in want       # opt-in report (does not affect exit code)
    do_savings = "--savings-claims" in want  # opt-in report (does not affect exit code)
    do_evidence = "--evidence" in want       # opt-in report (does not affect exit code)
    do_staleness = "--staleness" in want     # opt-in report (does not affect exit code)
    do_meta_stale = "--metadata-staleness" in want  # opt-in report (does not affect exit code)
    do_lead_head = "--lead-headlines" in want   # opt-in report (does not affect exit code)
    do_mirror = "--catalog-mirror" in want   # opt-in report (does not affect exit code)
    do_maint = "--maintenance" in want       # opt-in report (does not affect exit code)
    do_scope = "--scope" in want             # opt-in report (does not affect exit code)
    do_ident = "--identity" in want          # opt-in report (does not affect exit code)
    # NOT `do_inst` — that name belongs to detector A's `--installs`. Reusing it
    # silently rebound it, so `--installed` also ran the network install resolver.
    do_instrec = "--installed" in want       # opt-in LOCAL report (never a gate)
    do_licdecl = "--license-declared" in want  # opt-in report (does not affect exit code)
    do_contain = "--containment" in want      # opt-in report (does not affect exit code)
    do_condgate = "--conditional-gate" in want  # opt-in report (does not affect exit code)
    do_lichdr = "--license-header" in want    # opt-in report (does not affect exit code)
    do_dupev = "--duplicate-evals" in want    # opt-in report (does not affect exit code)
    do_wfskip = "--workflow-skips" in want    # opt-in report (does not affect exit code)
    do_contev = "--containment-evidence" in want  # opt-in report (does not affect exit code)
    do_stage = "--stage-drift" in want  # opt-in report (does not affect exit code)
    do_repoinst = "--repo-installs" in want  # opt-in report (does not affect exit code)
    do_layer = "--layer-drift" in want  # opt-in report (does not affect exit code)
    do_linkid = "--link-identity" in want  # opt-in report (does not affect exit code)

    ctx = DetectorContext(ROOT)  # the one place the module global feeds the detectors (#199)
    rc = 0
    if do_inst:
        broken, unknown, targets = audit_installs(ctx)
        # n/total checked, detector C's shape: a run that reached 33 of 85 registries
        # must not read like one that reached all of them.
        unreached = len({(k, p) for _r, k, p, _why in unknown})
        print(f"== A. install resolver — {targets - unreached}/{targets} target(s) checked ==")
        for rel, kind, pkg in broken:
            print(f"  BROKEN [{kind}] {pkg}  ({rel})")
        # Deduped by target, unlike BROKEN. A broken package cited in three evals is
        # three rows to fix; an unreachable registry is one thing to re-run, so printing
        # it once per citation is noise with no remedy attached. Capped, and the cap is
        # disclosed rather than silently truncating (the no-silent-caps rule).
        by_target = {}
        for rel, kind, pkg, why in unknown:
            by_target.setdefault((kind, pkg), (rel, why))
        for i, ((kind, pkg), (rel, why)) in enumerate(by_target.items()):
            if i == UNCHECKED_SHOWN:
                print(f"  UNCHECKED …and {len(by_target) - UNCHECKED_SHOWN} more target(s)")
                break
            print(f"  UNCHECKED [{kind}] {pkg}  ({rel}) — {why}")
        if broken:
            rc = 1   # a 404 is a defect a commit caused; an unreachable registry is not
        if unknown:
            # Never OK while unknowns exist (#319), and never a build failure either:
            # nothing a commit did caused it and re-running would give a different answer.
            print(f"  INCONCLUSIVE — {unreached} target(s) could not be checked; "
                  "not a gate failure (no commit caused it)")
        elif not broken:
            print("  OK — every install target resolves")
    if do_fab:
        pop = fabrication_population(ctx)
        print(f"== B. fabrication classifier — {len(pop)}/{len(ctx.evals)} eval(s) checked ==")
        flagged = audit_fabrication(ctx)
        if flagged:
            rc = 1
            print(f"  REVIEW ({len(flagged)}): a 'How we tested' that claims a run with no honesty disclaimer")
            for b in flagged:
                print(f"    - {b}")
        else:
            print("  OK — every 'How we tested' either discloses not-run or shows a verified run")
    if do_verd:
        vcov = verdict_coverage(ctx)
        print(f"== D. verdict sync (eval ## Verdict vs COMPARISON.md) — "
              f"{vcov.compared}/{vcov.declared} eval(s) with a verdict compared ==")
        vflag = audit_verdicts(ctx)
        if vflag:
            rc = 1
            for name, ev, cv in vflag:
                print(f"  MISMATCH {name}: eval={ev}  COMPARISON={cv}")
        else:
            print("  OK — eval verdicts agree with COMPARISON (dual verdicts & KEEP tolerated)")
        # Printed and never counted: both buckets are documented abstentions, and a
        # `discovery-log` lead has no verdict to sync. `unmapped` is the one that was
        # never stated — see verdict_coverage's note on `design-extract`.
        if vcov.leads:
            print(f"  not compared  {len(vcov.leads):4d}  COMPARISON row reads `discovery-log` "
                  "— a lead, not a verdict")
        if vcov.unmapped:
            print(f"  not compared  {len(vcov.unmapped):4d}  no COMPARISON.md row at all — "
                  "a tool with a verdict and no row is invisible to this gate (#481)")
            for name in sorted(vcov.unmapped):
                print(f"                      - {name}")
    if do_comp:
        # G's population is the whole file — it is an arithmetic identity, not a walk —
        # so the number says "the gate ran on a corpus this size", which is what tells
        # a clean `OK` apart from an `OK` on an empty tree (#319).
        print(f"== G. comparison consistency (COMPARISON.md vs CATALOG.md) — "
              f"{sum(catalog_lib.comparison_body_counts(ctx.comparison).values())} body row(s) "
              f"vs {catalog_lib.catalog_count(ctx.catalog)} catalog entr(ies) ==")
        cprob = audit_comparison(ctx)
        if cprob:
            rc = 1
            for p in cprob:
                print(f"  DRIFT {p}")
        else:
            print("  OK — COMPARISON summary sums to its body rows and Total matches CATALOG.md")
    if do_rows:
        # Two files, two numbers. One `walked/total` across both would be the defect
        # #479 removed from detector U — a single figure standing for two populations.
        print(f"== O. row shape — "
              f"{len(list(catalog_lib.catalog_body_rows(ctx.catalog)))} CATALOG.md + "
              f"{len(list(catalog_lib.comparison_body_rows(ctx.comparison)))} COMPARISON.md "
              f"body row(s) validated ==")
        rprob = audit_row_shapes(ctx)
        if rprob:
            rc = 1
            for p in rprob:
                print(f"  MALFORMED {p}")
        else:
            print("  OK — every table row parses as a well-formed entry row")
    if do_bulk:
        bcov = bulk_triage_coverage(ctx)
        print(f"== Q. eliminate-only bulk triage — {bcov.bulk}/{bcov.stamped} stamped eval(s) "
              f"held to the ceiling, {bcov.human} human-marked (exempt) ==")
        bprob = audit_bulk_triage(ctx)
        if bprob:
            rc = 1
            for name, verdict in bprob:
                if verdict == UNATTRIBUTED:
                    print(f"  UNATTRIBUTED {name}: carries `{TRIAGE_STAMP}` with neither "
                          f"`{BULK_MARKER}` nor `{HUMAN_MARKER}` — Q cannot police a lane "
                          f"it cannot identify (#327)")
                else:
                    print(f"  OVERREACH {name}: bulk-triaged eval claims {verdict} — "
                          f"the bulk lane may only SKIP or leave at discovery-log")
        else:
            print("  OK — every bulk-triaged eval stays within eliminate-only authority")
    if do_drift:
        # Three checks, three numbers — J runs picks->verdict, ledger->STACK/verdict and
        # ADOPT/KEEP->ledger, and one figure could only stand for one of them (#479).
        print(f"== J. stack-derivation drift — "
              f"{len(_stack_picks_by_slug(ctx.stack))} STACK pick(s), "
              f"{len(_LEDGER_ROW.findall(ctx.ledger))} ledger row(s), "
              f"{sum(1 for r in ctx.comparison_rows if r.verdict in ('ADOPT', 'KEEP'))} "
              f"ADOPT/KEEP row(s) ==")
        dprob = audit_stack_drift(ctx)
        if dprob:
            rc = 1
            for p in dprob:
                print(f"  DRIFT {p}")
        else:
            print("  OK — every ADOPT/KEEP tool is in STACK or the ledger; STACK & ledger agree with verdicts")
    if do_vev:
        print(f"== K. verdict evidence (ADOPT/KEEP must be run-backed or disclaimered) — "
              f"{len(verdict_evidence_population(ctx))}/{len(ctx.evals)} eval(s) checked ==")
        vev = audit_verdict_evidence(ctx)
        if vev:
            rc = 1
            for name, verd, lvl in vev:
                print(f"  WEAK {name}: {verd} backed only by {lvl} and no honesty disclaimer "
                      f"(graduate the eval to MEASURED/RUN, or add a not-run disclaimer)")
        else:
            print("  OK — every ADOPT/KEEP eval is run-backed (MEASURED/RUN) or carries a disclaimer")
    if do_links:
        problems, unknowns, total = audit_links(ctx)
        checked = total - len(unknowns)
        print(f"== C. link rot (CATALOG.md repo links) — {checked}/{total} checked ==")
        if problems:
            rc = 1
            for slug, res in problems:
                print(f"  {'DEAD' if res=='dead' else 'MOVED'} {slug}" + (f" -> {res[6:]}" if res.startswith('moved:') else ""))
        if unknowns:
            # Never "OK" on an inconclusive run: this detector once printed a clean
            # sweep of 612 links while GitHub 429'd every single request (#319).
            reasons = collections.Counter(r for _, r in unknowns)
            summary = ", ".join(f"{n}x {r}" for r, n in reasons.most_common())
            print(f"  INCONCLUSIVE — {len(unknowns)} link(s) could not be verified ({summary}).")
            print("  Re-run later, or authenticate: an unauthenticated burst of ~600 HEAD "
                  "requests is rate-limited. Findings above are still real; absence of "
                  "findings is NOT a pass.")
        elif not problems:
            print(f"  OK — all {total} catalog repo links resolve to their canonical names")
    if do_archived:
        print("== H. archived repos (report-only) ==")
        arch, total = audit_archived(ctx)
        undisclosed = [(s, p) for s, p, flagged in arch if not flagged]
        for s, p, flagged in arch:
            tag = "" if flagged else "  <- NOT disclosed in the entry; add a ⚠️ archived note or repoint"
            print(f"  ARCHIVED {s} (last push {p}){tag}")
        if not arch:
            print(f"  OK — none of {total} catalog repos are archived")
        elif not undisclosed:
            print(f"  ({len(arch)} archived, all already disclosed with a ⚠️ note)")
    if do_skills:
        measured, backlog = audit_skill_evidence(ctx)
        tot = len(measured) + len(backlog)
        print(f"== E. skill evidence (report-only) — {len(measured)}/{tot} ADOPT skills have measured backing ==")
        for n in measured:
            print(f"  MEASURED {n}")
        for n in backlog:
            print(f"  backlog  {n}  (ADOPT skill, review-based — would benefit from a measured A/B; see TEMPLATE.md)")
    if do_skill_design:
        compliant, missing = audit_skill_design(ctx)
        tot = len(compliant) + len(missing)
        print(f"== S. skill test-design (report-only) — {len(compliant)}/{tot} skill/plugin evals record a triggering test or A/B ==")
        for n in compliant:
            print(f"  ok       {n}")
        for n in missing:
            print(f"  MISSING  {n}  (skill/plugin eval records neither a triggering test nor an A/B; see TEMPLATE.md's skills Test-design section)")
        if not missing:
            print("  OK — every skill/plugin eval records at least one skill dimension")
    if do_evidence:
        counts, missing, strong = audit_evidence_field(ctx)
        have = sum(counts.values()); tot = have + len(missing)
        strong_tot = sum(strong.values())
        print(f"== I. evidence-strength field (report-only) — {have}/{tot} evals declare Evidence ==")
        for lvl in EVIDENCE_LEVELS:
            print(f"  {lvl:<12} {counts[lvl]}")
        if missing:
            print(f"  {'(none)':<12} {len(missing)}  (eval declares no Evidence field — run ./backfill-evidence.py)")
        if strong_tot:
            backed = strong['MEASURED'] + strong['RUN']
            pct = round(100 * strong['MEASURED'] / strong_tot)
            print(f"  ADOPT/KEEP set ({strong_tot}): {strong['MEASURED']} MEASURED ({pct}%), "
                  f"{strong['RUN']} RUN, {strong['REVIEW']} REVIEW, {strong['SOURCE-ONLY']} SOURCE-ONLY "
                  f"→ {backed}/{strong_tot} run-backed (the rest are review-only — #68 graduates them, #71 gates)")
    if do_staleness:
        stale, undated = audit_staleness(ctx)
        print(f"== L. staleness sweep (report-only) — {len(stale)} stale eval(s), {undated} undated ==")
        for name, typ, d, age, thr in sorted(stale, key=lambda r: -r[3]):
            print(f"  STALE {name} ({typ}) last verified {d} — {age}d old > {thr}d threshold")
        if not stale:
            print("  OK — no dated eval is past its category staleness threshold")
        if undated:
            print(f"  ({undated} evals carry no **Last verified:** date yet — add one when you re-check them)")
    if do_meta_stale:
        total, undated, stale, oldest = audit_metadata_staleness(ctx)
        print(f"== R. metadata staleness (report-only) — {total} record(s), "
              f"{len(stale)} past {METADATA_STALE_DAYS}d, {undated} undated ==")
        if not total:
            print("  no repo-metadata.json — run `python3 refresh-metadata.py` to build it")
        elif oldest is None:
            print("  UNDATED — no record carries a fetch date, so the cache's age is unknown.")
            print("  Run `python3 refresh-metadata.py` to stamp them (not backfilled: a "
                  "floor date would assert a fetch that never happened).")
        else:
            slug, date, age = oldest
            print(f"  oldest fetch {date} ({age}d ago, {slug})")
            if stale:
                print(f"  {len(stale)} record(s) past the {METADATA_STALE_DAYS}d threshold — "
                      "an archived-since repo still reads as live to the triage bands.")
                print("  Refresh: `python3 refresh-metadata.py`")
            else:
                print("  OK — every stamped record is within the threshold")
            if undated:
                print(f"  ({undated} record(s) carry no fetch date — refresh to stamp them)")
    if do_overlaps:
        gaps, stale_ext, peers, inst_records = audit_overlaps(ctx)
        strong = [(t, c) for t, c in gaps if c >= 2]
        print(f"== F. dangling overlaps (report-only) — {len(gaps)} uncatalogued peer "
              f"tokens, {len(stale_ext)} stale `(ext.)` marker(s), {len(peers)} "
              f"demonstrated peer(s) across {inst_records} install record(s) ==")
        if not gaps and not stale_ext:
            print("  OK — every 'Overlaps with' token resolves to a catalog entry")
        # Counted: a row asserting a tool is outside a catalog that holds it. Not a lead
        # to review — a defect to repoint, which also restores the overlap pressure the
        # dangling token was withholding from triage.py (#403).
        for t, hit, citer in stale_ext:
            print(f"  STALE-EXT {t}  (cited by {citer} as external — catalogued as {hit})")
        for t, c in strong:
            print(f"  GAP?  {t}  ({c} refs — likely a notable tool missing from the catalog)")
        for t, c in gaps:
            if c < 2:
                print(f"  maybe {t}  ({c} ref — check: real gap or external/conceptual peer)")
        # Printed, never counted: a token DEMONSTRATED to resolve to a record rather than
        # asserted to. 0 records means "this machine keeps none", never "nothing is
        # installed" — so an empty bucket here is not a clean bill (#398).
        for t, (kind, src) in peers:
            print(f"  {kind}-peer {t}  ({_OVL_PEER_LABEL[kind]} {src})")
    if do_wf_drift:
        wfmiss, picks = audit_workflow_drift(ctx)
        print(f"== P. WORKFLOW↔STACK drift (report-only) — {len(wfmiss)} of {picks} "
              f"STACK pick(s) missing from WORKFLOW.md ==")
        if not picks:
            print("  no STACK picks found — nothing was compared, which is not the same "
                  "as nothing being wrong")
        if not wfmiss:
            print("  OK — every STACK pick appears somewhere in WORKFLOW.md")
        for slug, ln in wfmiss:
            print(f"  MISSING {slug}  (STACK.md:{ln} — add it to the appropriate WORKFLOW stage)")
    if do_clusters:
        cl = audit_clusters(ctx)
        print(f"== M. clusters without a pick (report-only, #69) — {len(cl)} overlap cluster(s) all-CONDITIONAL, no ADOPT/KEEP pick ==")
        if not cl:
            print("  OK — every overlap cluster with a CONDITIONAL member also has an ADOPT/KEEP pick")
        for members in cl:
            print(f"  PICK?  {' / '.join(members)}")
    if do_savings:
        sav = audit_savings_claims(ctx)
        silent = [r for r in sav if not r[2]]
        print(f"== N. token-savings claims (report-only) — {len(silent)} unverified savings claim(s), "
              f"{len(sav) - len(silent)} self-reported ==")
        if not sav:
            print("  OK — every numeric token-savings headline is run-backed (MEASURED/RUN)")
        for name, lvl, disclosed in sav:
            tag = "  [self-reported — honest, but verify]" if disclosed else \
                  "  (run the token-savings protocol to graduate to MEASURED)"
            print(f"  UNVERIFIED {name}  ({lvl}){tag}")
    if do_lead_head:
        leads = audit_lead_headlines(ctx)
        print(f"== T. lead headline overreach (report-only) — {len(leads)} lead(s) "
              f"headlining a verdict they are not entitled to ==")
        if not leads:
            print("  OK — every discovery-log lead headlines discovery-log or SKIP")
        for name, verd, lvl in leads:
            print(f"  OVERREACH {name}: row=discovery-log but eval headlines {verd} at {lvl} evidence "
                  f"(relabel it a tentative read, or promote the row with a run behind it)")
    if do_mirror:
        drift, cover = audit_catalog_mirror(ctx)
        kinds = collections.Counter(f.kind for f in drift)
        evals_hit = len({f.eval_name for f in drift})
        # Two populations, reported apart because they ARE apart: the cells need a mirror,
        # the `**Repo:**` header needs only a header (#479). One number for both would be
        # the coverage claim #467 removed from this same headline.
        print(f"== U. catalog-entry mirror drift (report-only) — {len(drift)} disagreement(s) "
              f"in {evals_hit} of {cover.walked} mirrored eval(s), header checked in "
              f"{cover.headers} of {cover.header_total} declaring one: {kinds['LINK']} LINK, "
              f"{kinds['ORPHAN']} ORPHAN, {kinds['TEXT']} TEXT, {kinds['CASE']} CASE, "
              f"{kinds['AMBIG']} AMBIG ==")
        if not cover.walked:
            print("  no embedded catalog rows — nothing was compared, which is not the "
                  "same as nothing being wrong")
        elif not drift:
            print("  OK — every embedded catalog row matches CATALOG.md")
        # Printed, never counted: what U did NOT look at. Silence here reads as coverage.
        for reason, n in sorted(cover.skipped.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  not compared  {n:4}  {reason}")
        # LINK first: a stale slug makes an eval assert facts about the wrong repo (#336),
        # where TEXT drift is a disagreement about wording that a human resolves per row.
        order = {"LINK": 0, "ORPHAN": 1, "AMBIG": 2, "TEXT": 3, "CASE": 4}
        for f in sorted(drift, key=lambda f: (order[f.kind], f.eval_name)):
            print(f"  {f.kind:6} {f.eval_name} [{f.tool}]: {f.detail}")
    if do_maint:
        finds, collected, acked = audit_maintenance(ctx)
        undisclosed = sum(1 for f in finds if not f.disclosed)
        print(f"== V. maintenance signal (report-only) — {len(finds)} finding(s) "
              f"across {collected} record(s) carrying the signal, "
              f"{undisclosed} undisclosed in CATALOG.md ==")
        if not collected:
            print("  no maintenance data — run `python3 refresh-metadata.py --maintenance` "
                  "to collect it (absence of the field is 'not collected', not 'nothing is dead')")
        elif not finds:
            print("  OK — no catalogued repo announces discontinuation or has lost its license")
        for f in finds:
            # The catalog row is what a reader scans; the verdict is one file away. An
            # undisclosed row advertises a dead project in the present tense (#395).
            # A pack has several rows and every one of them advertises the repo, so the
            # note names them: "the row" is the wrong question for a shared slug (#465).
            note = ""
            if not f.disclosed:
                note = ("  ← CATALOG.md row does not say so" if len(f.silent) == 1
                        else f"  ← {len(f.silent)} CATALOG.md rows do not say so: "
                             + ", ".join(f.silent))
            print(f"  {f.kind} [{f.verdict}] {f.tool} ({f.slug}): {f.detail}{note}")
        for f in acked:
            print(f"  acknowledged false positive — {f.tool} ({f.slug}): {f.detail}")
    if do_scope:
        finds, cleared = audit_scope(ctx)
        p0 = sum(1 for f in finds if f.band.startswith("P0"))
        print(f"== W. P0 scope mismatch (report-only) — {len(finds)} lead(s) whose eval "
              f"concedes the scope exclusion, {p0} in P0 ==")
        if not finds:
            print("  OK — no framework/platform lead concedes it is out of scope")
        for f in finds:
            print(f"  SCOPE [{f.band}] {f.tool} ({f.typ}): \"{f.phrase}\"")
        for f in cleared:
            print(f"  argues it clears the bar — [{f.band}] {f.tool} ({f.typ}): \"{f.phrase}\"")
    if do_ident:
        finds, context = audit_identity(ctx)
        settled = sum(1 for f in finds if f.kind == "SETTLED")
        print(f"== X. collapsed catalog identity (report-only) — {len(finds)} lead(s) that "
              f"are facets of one artifact, {settled} already settled ==")
        if not finds:
            print("  OK — no lead shares a catalog link with another row")
        for f in finds:
            tail = (f"already {f.verdict} as {f.peers[0]}" if f.kind == "SETTLED"
                    else f"shares its link with {', '.join(f.peers)}")
            print(f"  {f.kind:9} {f.tool} ({f.slug}): {tail}")
        for f in context:
            why = {"FACETED": "each row links its own subpath",
                   "DECLARED": "every row names its container in `Ships inside` (#343)",
                   }.get(f.kind, "collapsed, but every row is already disposed")
            print(f"  {f.kind.lower()} ({why}) — {f.slug}: "
                  f"{len(f.peers)} rows, {', '.join(f.peers)}")
    if do_instrec:
        finds, shadowed, records = audit_installed(ctx)
        print(f"== Y. install-record mismatch (report-only, this machine) — "
              f"{len(finds)} finding(s) across {records} install record(s) ==")
        if not records:
            print("  no install records found — absence of a record is 'nothing known "
                  "about this machine', never 'nothing is installed'")
        elif not finds:
            print("  OK — every ADOPT/KEEP skill/plugin row is backed by an install record")
        for f in finds:
            print(f"  {f.kind:12} {f.tool} [{f.verdict}]: {f.detail}")
        for f in shadowed:
            print(f"  {f.kind:12} (installed; name shadowed, not counted) "
                  f"{f.tool} [{f.verdict}]: {f.detail}")
    if do_licdecl:
        finds, records, withdrawn = audit_license_declared(ctx)
        grounded = sum(1 for f in finds if f.kind == "GROUNDED")
        print(f"== Z. unread license declaration (report-only) — {len(finds)} record(s) "
              f"whose 'NONE' license is declared elsewhere, {grounded} carrying a "
              f"license-grounded SKIP ==")
        if not records:
            print("  no license_declared data — run `python3 refresh-metadata.py` to "
                  "collect it (absence of the field is 'not collected', never 'every "
                  "NONE is a real absence')")
        elif not finds:
            print("  OK — no catalogued repo declares a license GitHub failed to read")
        for f in finds:
            extra = f" — manifest says {f.conflict}" if f.conflict else ""
            print(f"  {f.kind:8} {f.tool} ({f.slug}) [{f.verdict}]: {f.spdx} in "
                  f"{f.where}{extra} — \"{f.phrase}\"")
        for f in withdrawn:
            print(f"  ground already withdrawn — {f.tool} ({f.slug}) [{f.verdict}]: "
                  f"{f.spdx} in {f.where}")
    if do_contain:
        finds, declared = audit_containment(ctx)
        unrowed = sum(1 for f in finds if f.kind == "UNROWED")
        print(f"== AA. unactionable containment (report-only) — {len(finds)} finding(s) "
              f"across {declared} `Ships inside` declaration(s): {unrowed} UNROWED, "
              f"{len(finds) - unrowed} SELF-LINKED ==")
        if not declared:
            print("  no `Ships inside` declarations — the column is empty, which is its "
                  "default and means every row is independently installable (#343)")
        elif not finds:
            print("  OK — every declared container is a catalog row the row itself "
                  "does not link")
        for f in finds:
            why = ("the catalog holds no row for this container — P5's \"settle the "
                   "container\" names nothing" if f.kind == "UNROWED"
                   else "this row's own link IS that container — nothing tells the "
                        "artifact apart from its pack")
            print(f"  {f.kind:11} {f.tool} [{f.verdict}] ships inside `{f.container}` — {why}")
    if do_condgate:
        unent, ungated, total = audit_conditional_gate(ctx)
        print(f"== AB. unentitled CONDITIONAL (report-only) — {len(unent)} of {total} "
              f"CONDITIONAL row(s) satisfy neither ADR-0005 clause, "
              f"{total - len(unent) - len(ungated)} declare a condition ==")
        if not total:
            print("  no CONDITIONAL rows — the bucket ADR-0005 collapsed is empty")
        elif not unent:
            print("  OK — every CONDITIONAL row was exercised or declares an `adopt-if:`")
        for f in unent:
            print(f"  UNENTITLED {f.tool} ({f.evidence}, no `adopt-if:`) — declare the gate "
                  "or demote the row to `discovery-log` (#69's operation)")
        # Printed, never counted: entitled under ADR-0005's *exercised* clause, so not a
        # finding — but point 1 still wants a condition string, and that number should be
        # visible rather than implied.
        for f in ungated:
            print(f"  no-condition {f.tool} ({f.evidence}) — entitled by the exercised "
                  "clause; ADR-0005 point 1 still wants an `adopt-if:`")
    if do_lichdr:
        finds, redirected, compared = audit_license_header(ctx)
        print(f"== AC. license header vs record (report-only) — {len(finds)} of "
              f"{compared} comparable eval header(s) contradict repo-metadata.json ==")
        if not compared:
            print("  no comparable records — run `python3 refresh-metadata.py` to "
                  "populate repo-metadata.json (0 records is not 0 findings)")
        elif not finds:
            print("  OK — every eval header agrees with the license on record")
        WHY = {
            "UNGROUNDED-SKIP": "a live SKIP rests on this absence and the record refutes "
                               "it — the DISPOSITION is void, not just the header (#417)",
            "UNGROUNDED": "the record names a license, so the absence this header asserts "
                          "is not one; no disposition rests on it here (#372)",
            "CONFLICT": "both name a license and they differ — one of the two is wrong",
        }
        for f in finds:
            print(f"  {f.kind:16} {f.name} [{f.slug}] header `{f.header}` vs record "
                  f"`{f.spdx}` — {WHY[f.kind]}")
        # Printed, never counted: the record came through a redirect and describes the
        # DESTINATION, so it is not evidence about this row.
        for f in redirected:
            print(f"  redirected {f.name} — record resolves to `{f.slug}`, a different "
                  f"owner; its `{f.spdx}` is the destination's, not this row's")
    if do_dupev:
        finds, claimed = audit_duplicate_evals(ctx)
        print(f"== AD. duplicate evals (report-only) — {len(finds)} of {claimed} "
              f"claimed row(s) have more than one eval file ==")
        if not claimed:
            print("  no rows claimed by any eval — check COMPARISON.md parses")
        elif not finds:
            print("  OK — every claimed row has exactly one eval")
        for f in finds:
            got = (f"resolves to {f.resolved[0]} ({f.resolved[1] or 'no verdict'}, "
                   f"{f.resolved[2]})" if f.resolved else "resolves to no eval at all")
            rest = "; ".join(f"{n} ({v or 'no verdict'}, {e})" for n, v, e in f.shadows)
            why = ("the row reports less than the tree holds — the weaker file wins on "
                   "filename order" if f.kind == "SHADOWED"
                   else "the row already resolves to the stronger file; the second is "
                        "a redundant eval of one tool")
            print(f"  {f.kind:9} `{f.row}` {got}, shadowing {rest} — {why}")
    if do_wfskip:
        finds, disclosed, linked = audit_workflow_skips(ctx)
        print(f"== AE. WORKFLOW recommends a SKIP (report-only) — {len(finds)} of "
              f"{linked} catalogued WORKFLOW.md link(s) name a SKIPped tool, "
              f"{len(disclosed)} disclosed ==")
        if not linked:
            print("  no catalogued links in WORKFLOW.md — check the file is present")
        elif not finds:
            print("  OK — the manual recommends nothing the catalog eliminated")
        for f in finds:
            print(f"  RECOMMENDED {f.tool} [{f.slug}] WORKFLOW.md:{f.line} — the row "
                  f"reads SKIP and the line does not say so: {f.text}")
        # Printed, never counted: the line already discloses, or sits in the manual's own
        # `## Tools Deliberately Excluded` section (V's `acked`, W's `cleared`).
        for f in disclosed:
            print(f"  disclosed {f.tool} WORKFLOW.md:{f.line} — named as an exclusion, "
                  "not a recommendation")
    if do_contev:
        refuted, confirmed, unchecked, seen = audit_containment_evidence(ctx)
        total = len(refuted) + len(confirmed) + len(unchecked)
        print(f"== AF. unfalsified containment (report-only) — {len(refuted)} of {seen} "
              f"checked `Ships inside` declaration(s) refuted, {len(unchecked)} of "
              f"{total} unchecked ==")
        if not total:
            print("  no `Ships inside` declarations — the column is empty, which is its "
                  "default and means every row is independently installable (#343)")
        elif not seen:
            # 0 records is not 0 findings (detector V's rule): nothing was asked.
            print("  no member_packages records — run `python3 refresh-metadata.py "
                  "--containment` to collect them (0 records is not 0 findings)")
        elif not refuted:
            print("  OK — every checked declaration survives the one test that can "
                  "contradict it")
        for f in refuted:
            print(f"  REFUTED   {f.tool} [{f.verdict}] declares `{f.container}` but "
                  f"{f.path} publishes `{f.package}` — it IS independently installable, "
                  "so the cell should be empty and P5 has no claim on it")
        # Printed, never counted (V's `acked`, W's `cleared`, X's `FACETED`).
        for f in confirmed:
            print(f"  confirmed {f.tool} ships inside `{f.container}` — {f.path} "
                  "publishes no package of its own")
        for f in unchecked:
            why = ("links the repo root, so there is no component to ask about"
                   if f.path is None else f"no record for {f.path}")
            print(f"  unchecked {f.tool} ships inside `{f.container}` — {why}")
    if do_stage:
        drift, stack_drift, comparable, unusable = audit_stage_drift(ctx)
        print(f"== AG. stage drift (report-only) — {len(drift)} of {comparable} comparable "
              f"row(s) sit under a stage their eval never names ==")
        if not comparable:
            print("  no comparable rows — no COMPARISON row under an inner-loop stage "
                  "section resolves to an eval whose header names one")
        elif not drift and not stack_drift:
            print("  OK — every row's stage section agrees with its eval's own header")
        for f in drift:
            print(f"  DRIFT       {f.tool} — COMPARISON files it under {f.section}; its "
                  f"eval names {'/'.join(f.named)}: \"{f.header}\"")
        for f in stack_drift:
            print(f"  STACK-DRIFT {f.tool} — COMPARISON files it under {f.section}; "
                  f"{f.header}")
        print(f"  ({unusable} row(s) not compared — the header names no loop stage, an "
              "honest non-answer)")
    if do_repoinst:
        findings, evaluated, records = audit_repo_installs(ctx)
        print(f"== AH. unread repo install record (report-only) — {len(findings)} of "
              f"{records} vendored source(s) this repo runs but never judged ==")
        if not records:
            # 0 records is not 0 findings (detector V's rule): vendoring nothing is a
            # different statement from every vendored source being settled.
            print(f"  no `{REPO_SKILL_LOCK}` records — this repo vendors nothing into its "
                  "own tree (0 records is not 0 findings)")
        elif not findings:
            print("  OK — every source this repo vendors carries a real verdict")
        for f in findings:
            if f.kind == "UNCATALOGUED":
                print(f"  UNCATALOGUED          `{f.slug}` is vendored here as "
                      f"`{f.key}` and has no CATALOG.md row — found from the install "
                      "side, the only side that can see it")
            else:
                print(f"  UNEVALUATED-INCUMBENT {f.tool} [`{f.slug}`] is vendored here "
                      f"as `{f.key}`, and its row is still a `{f.verdict}` lead — the "
                      "queue ranks it on attention alone, never on the fact we run it")
        # Printed, never counted (V's `acked`, W's `cleared`, X's `FACETED`): a settled
        # source is the outcome this detector exists to produce.
        for f in evaluated:
            print(f"  evaluated {f.tool} [`{f.slug}`] vendored as `{f.key}` — "
                  f"row reads {f.verdict}")
    if do_layer:
        drift, self_drift, undecl, no_layer, cover = audit_layer_drift(ctx)
        n = len(drift) + len(self_drift) + len(undecl)
        print(f"== AI. layer drift (report-only) — {n} disagreement(s): {len(drift)} of "
              f"{cover.rows} comparable WORKFLOW.md row(s), {len(self_drift)} of "
              f"{cover.filed_twice} tool(s) WORKFLOW.md files twice, {len(undecl)} of "
              f"{cover.declaring} eval(s) declaring a layer ==")
        if not cover.rows and not undecl and not self_drift:
            print("  no comparable rows — no WORKFLOW.md `| Layer |` row resolves to an "
                  "eval whose header names one of the three")
        elif not n:
            print("  OK — every layer table, the adoption ladder and every eval header "
                  "agree, and no eval names a layer TEMPLATE.md does not define")
        # SELF-DRIFT first: it is internal to one file, so it cannot be a resolution
        # artifact, and it is the copy a newcomer acts on.
        for f in self_drift:
            print(f"  SELF-DRIFT {f.tool} — the adoption ladder files it under "
                  f"{f.declared}; {f.header} (WORKFLOW.md:{f.line})")
        for f in drift:
            print(f"  DRIFT      {f.tool} WORKFLOW.md:{f.line} — filed under "
                  f"{f.declared}; its eval names {'/'.join(f.named)}: \"{f.header}\"")
        for f in undecl:
            print(f"  UNDECLARED {f.tool} — `**Layer:** {f.header}` names none of "
                  f"{'/'.join(LAYERS)} (TEMPLATE.md declares a closed set)")
        # Printed, never counted (V's `acked`, W's `cleared`, X's `FACETED`): declining
        # the field is the honest way to have no single subject.
        for f in no_layer:
            print(f"  no-layer   {f.tool} declares no `**Layer:**` — an honest "
                  "non-answer, not a finding")
    if do_linkid:
        mism, walked = audit_link_identity(ctx)
        print(f"== AJ. link identity (report-only) — {len(mism)} of {walked} "
              f"catalogued link(s) name one tool and point at another ==")
        if not walked:
            print("  no catalogued links — no link resolves on BOTH sides (a text naming "
                  "a catalog row, a URL behind one), so nothing was compared")
        elif not mism:
            print("  OK — every link whose text names a catalogued tool points at a repo "
                  "that tool is catalogued behind")
        for f in mism:
            print(f"  MISNAMED   {f.rel}:{f.line} — text \"{f.text}\" names "
                  f"{f.named}; `{f.slug}` is {'/'.join(f.rows)}")
    sys.exit(rc)

if __name__ == "__main__":
    main()
