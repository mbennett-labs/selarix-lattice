# INTAKE PIPELINE

**Document type:** Operating discipline — workflow definition
**Status:** Canonical (v1)
**Location:** `/operating/INTAKE_PIPELINE.md`
**Last updated:** 2026-04-25 by Mike + Claude
**Read before:** Any session where new external content (videos, articles, podcasts, transcripts, market reports) might be reviewed and decided on.

---

## Why this doc exists

Mike consumes a lot of high-quality content that contains genuinely useful patterns. The historical failure mode: each piece gets reviewed enthusiastically, surfaces ideas, and then accumulates in unindexed piles of documents. Months later, a useful nugget is lost because nobody knows where to look.

This pipeline makes the existing extraction practice formal, with defined handoffs, explicit storage locations, and an index that makes any past finding retrievable in 60 seconds.

---

## The pipeline (5 stages)

```
[1] Source identified          → YouTube / podcast / article / report
       ↓
[2] Extraction Claude          → separate Claude project does deep extraction
       │                          - reads transcript / source
       │                          - produces a reference doc with:
       │                            - TL;DR, datapoints, tooling, quotes,
       │                              gaps, glossary, QSL convergence section
       │                          - delivers as in.md or similarly named .md
       ↓
[3] Build Claude (this project) → reviews reference doc with mission-tier lens
       │                          - assigns tier (1, 2, 3, or park)
       │                          - identifies extractable tactical patterns
       │                          - flags convergence-section bias
       │                          - decides: act / extract / park / reject
       ↓
[4] Indexing                   → reference doc gets registered in
       │                          /operating/CONTENT_REGISTRY.md
       │                          (one row, dated, tier, status)
       │                          - canonical copy stored in /content-inputs/
       │                            with original filename preserved
       ↓
[5] Action                     → if extracted: tactical patterns become
                                  toolshed entries (skill, adapter, candidate)
                                  if parked: 1-page candidate card with
                                  activation criteria
                                  if rejected: decision logged
```

Total handling per resource: ~3 touch points (extract, review, slot). After that, it lives in the registry and is findable forever.

---

## Stage 1 — Source identification

What counts as worth extracting:

- ✅ Long-form content (YouTube videos >15 min, podcasts >30 min, articles >2,500 words)
- ✅ Practitioner content (someone showing actual workflows, not opinion pieces)
- ✅ Industry primary sources (e.g., Stripe Engineering blog, NIST publications)
- ✅ Adjacent-niche operator stories (someone solo-building something Mike could learn from)
- ❌ News/aggregation pieces — too shallow to extract
- ❌ Pure opinion / hot takes — not worth the extraction overhead
- ❌ Anything Mike can summarize for himself in 60 seconds — skip the pipeline

**Bias check:** if a piece feels like it confirms what Mike already wants to do, that's *more* reason to extract it formally — the convergence section will almost certainly try to upsell. Better to catch it in the pipeline than to act on extraction enthusiasm.

---

## Stage 2 — Extraction (separate Claude project)

Mike maintains a separate Claude project specifically for video/article extraction. That project's role is **transcription + structured analysis**, not strategic decision-making.

**Standard extraction output structure** (used in the four reference docs to date):

1. Source metadata (URL, creator, length, date, format)
2. TL;DR (30-second summary)
3. Core thesis / framework (the one big idea)
4. Workflow / step-by-step (if applicable)
5. Tooling stack (with links and pricing)
6. Key datapoints and statistics
7. Glossary
8. Quotable hooks (per audience: business / tech / consumer)
9. **Cross-content connections** (the "QSL convergence" section — see Bias Warning below)
10. Gaps and open questions
11. Markdown quick-reference (copy-paste portable summary)

**Bias warning to fold into extraction Claude's instructions:**

> The "QSL convergence" / "cross-content connections" section tends toward enthusiastic overreach. It will propose new directories, new product lines, new content series, often pitched in terms that mix Tier 1 / 2 / 3 framing without distinction. **Mark this section as inspiration only. Do not present convergence ideas as roadmap recommendations.** The build-Claude project applies the mission-tier filter in Stage 3.

---

## Stage 3 — Review (this Claude project)

When Mike brings a reference doc to the build-Claude session, the workflow is:

**3a. Read the doc fully before responding.** Both the body and the convergence section. Do not bucket from TL;DR alone.

**3b. Apply the mission-tier filter from `/operating/MISSION_TIERS.md`:**

- Does this advance Tier 1 (QSL healthcare/PQC)?
- Does this serve an active Tier 2 project (TherapistIndex, TheBinMap)?
- Does this enable a Tier 3 candidate with a real business case?
- None of the above → park

**3c. Identify extractable tactical patterns separately from strategic ideas.**

Tactical patterns (e.g., "use Perplexity API for live-cited research", "use printf for env file writes") have direct utility. Strategic ideas (e.g., "build quantumshieldtools.org") are usually convergence-section bias and need separate evaluation.

**3d. Honest pushback.** Flag overreach explicitly:

- If the doc proposes a new project, name it as a proposal, not a foregone conclusion
- If the doc has multiple convergence connections that all point in the same direction, that's pattern-matching by the extraction Claude — not signal
- If the doc would expand active scope while existing work is stalled, push back

**3e. Decide:**

- ✅ **Act** — extract specific patterns, draft toolshed entries this session
- ⏸ **Defer** — note in decisions log; act later when conditions are right
- 📦 **Park** — write a 1-page candidate card with activation criteria
- ❌ **Reject** — log reason; doc still gets registered for future reference

---

## Stage 4 — Indexing

Every reference doc that comes through the pipeline gets:

**4a. Permanent storage in `/content-inputs/`** with original filename and a date prefix:

```
/content-inputs/
  2026-04-25_lewis_jackson_zero_human_trading_firm.md
  2026-04-25_john_rush_seo_directories.md
  2026-04-25_connor_finlayson_directory_data_sourcing.md
  2026-04-25_stripe_minions_agentic_engineering.md
```

Naming convention: `YYYY-MM-DD_creator-or-source_topic-slug.md`.

**4b. One-line registration in `/operating/CONTENT_REGISTRY.md`:**

```
| 2026-04-25 | Connor Finlayson | Directory Data Sourcing | Tier 2 | Acted (Perplexity skill, Tag Generation pattern) | /content-inputs/2026-04-25_connor_finlayson_directory_data_sourcing.md |
```

Registry sorted by date descending. Searchable by Ctrl+F on creator, topic, or tier.

**4c. Decision recorded in `/operating/DECISIONS_LOG.md`** with one line per significant decision made during the review (act / defer / park / reject + rationale).

---

## Stage 5 — Action

Based on the decision in Stage 3:

**If Act:** Tactical patterns get extracted as `/toolshed/` entries (skills, adapters, tools, context, templates, candidates) per the Lattice toolshed structure. Each entry follows the standard toolshed header.

**If Defer:** Logged in decisions log with a clear "revisit when [condition]" note.

**If Park:** A `/toolshed/candidates/CANDIDATE_<slug>.md` card is written with:
- One-paragraph summary of what it is
- Why it's parked (mission-tier mismatch, dependency on other work, etc.)
- Specific activation criteria (e.g., "Build only when CrawDaddy clears $500/mo revenue AND Bookkeeper agent is live")

**If Reject:** Logged in decisions log with a clear reason. Reference doc still gets stored for completeness.

---

## What this pipeline prevents

The pipeline exists to prevent specific failure modes Mike has already experienced:

1. **The "lost in piles of documents" problem** — solved by `/content-inputs/` + `CONTENT_REGISTRY.md`
2. **The "convergence enthusiasm pulls focus" problem** — solved by the bias warning + explicit tier filter in Stage 3
3. **The "we already tried that" problem** — solved by registry searchability (look up topic before suggesting tactic)
4. **The "two stalled Paperclip companies" problem** — solved by mission-tier discipline blocking new builds without tier declaration
5. **The "broken Brevo link sat for 31 days" problem** — solved at the campaigns log level (separate doc), but the pipeline ensures patterns from extraction docs about email/outreach get logged and applied

---

## Pipeline maintenance

This doc gets updated when:

- A new stage is needed (e.g., legal review for content involving real people)
- The extraction Claude project's standard format changes
- The toolshed structure evolves
- The bias warning needs tightening based on new failure modes

Update by appending a "Pipeline changes" section at the bottom, dated, with rationale.

---

*Intake Pipeline v1 | SELARIX / Quantum Shield Labs LLC | 2026-04-25*
*Extract once. Index forever. Act with the mission-tier filter on.*
