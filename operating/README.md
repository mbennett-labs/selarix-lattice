# /operating/ — SELARIX Operating Discipline

**This folder is the meta-organizational layer for SELARIX / Quantum Shield Labs LLC.**

It is distinct from `/toolshed/` (tools and skills agents use), `/projects/` (per-project state), and `/agents/` (agent personas). It is for the discipline of running the system itself.

---

## What's in here

| File | What it does | When to read |
|---|---|---|
| **MISSION_TIERS.md** | The three-tier framework (Tier 1 QSL healthcare, Tier 2 SELARIX directories, Tier 3 cash channels) that anchors all decisions about what to build and what to defer. | Before evaluating any new project, agent, directory, or content piece. |
| **INTAKE_PIPELINE.md** | The 5-stage workflow for processing external content (videos, articles, podcasts) from extraction → review → indexing → action. | Before reviewing any new reference doc. |
| **CONTENT_REGISTRY.md** | Living index of every reference doc that has come through the pipeline. One row per doc. Searchable in seconds. | When asking "have we already looked at this topic?" or "where's that John Rush doc again?" |
| **DECISIONS_LOG.md** | Append-only log of major decisions with rationale, reversibility, and source. | At session start, scan top 10-20 entries to understand recent direction. Before suggesting a tactic, search by topic. |
| **CAMPAIGNS_LOG.md** | Append-only log of outreach campaigns (email, ads, social, partnerships) with hypotheses, metrics, results, and lessons. | Before starting any new outreach campaign. After every campaign send. 7 days post-send for metrics review. |
| **CLAUDE_SESSION_PRINCIPLES.md** | Meta-instructions for Claude on how to think about this project — lenses that work, mistakes to avoid, what's been tried, Mike's preferences. | At the start of every new chat session in this project. Before responding to anything. |

---

## How these docs relate to each other

```
                        MISSION_TIERS
                        (the why)
                            │
                ┌───────────┼───────────┐
                ↓           ↓           ↓
        INTAKE_PIPELINE   CLAUDE_SESSION    DECISIONS_LOG
        (workflow for     PRINCIPLES        (record of why
         new content)     (how Claude       each call was
              │            should think)     made)
              ↓                                  ↑
        CONTENT_REGISTRY ──────────────────────┐ │
        (index of every                        │ │
         doc consumed)                         │ │
                                               │ │
                              CAMPAIGNS_LOG ───┘ │
                              (record of every  │
                               outreach effort) │
                                                │
                                  All decisions feed
                                  back into Mission Tiers
                                  validation (or revision)
```

---

## Conventions

- **ALL_CAPS_SNAKE filenames** distinguish operating docs from toolshed entries (lowercase_snake) and agent personas (AGENT_PascalCase)
- **Append-only** for logs (DECISIONS, CAMPAIGNS, CONTENT_REGISTRY) — newest at the top, never delete entries, mark superseded with notes
- **Versioned via "Last updated" date** for structure docs (MISSION_TIERS, INTAKE_PIPELINE, CLAUDE_SESSION_PRINCIPLES)
- Every doc declares its own status, last-updated date, and intended reader

---

## Adding new operating docs

If a new piece of organizational discipline emerges that doesn't fit into the six existing docs, add a new one here. Examples that could become future docs:

- `INFRASTRUCTURE_REGISTRY.md` — index of all servers, services, credentials (currently scattered across SESSION_HANDOFF docs)
- `REVENUE_TRACKER.md` — monthly revenue per project per source (currently nowhere)
- `LEGAL_AND_COMPLIANCE.md` — when SELARIX touches anything regulated (currently informal)
- `POSTMORTEM_LOG.md` — failures, root causes, prevention measures (currently lives in DAILY_LOGs)

Don't pre-create these. Add when there's a real need.

---

## Why /operating/ exists at all

Because the alternative is what Mike had on 2026-04-24 morning:

- A reference doc for TherapistIndex monetization that didn't surface that an outreach campaign had already been tried 31 days ago
- A broken Brevo CTA link sitting unfixed because nobody was watching post-send metrics
- Two stalled Paperclip companies because no mission-tier framework existed to question their existence
- Four extracted reference docs all converging on "build quantumshieldtools.org" without anyone asking whether that aligned with the real mission

This folder is the discipline layer that catches those failure modes early.

---

*Operating folder README v1 | SELARIX / Quantum Shield Labs LLC | 2026-04-25*
